"""Tests for pictures-first planning (gather the pool, the AI picture list, topic check, planned pictures).
No AI usage, no network. Run: .venv\\Scripts\\python.exe tests\\test_pictures_first.py"""
import json
import os
import sys
import tempfile
import time
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import (  # noqa: E402
    channel_profiles, editplan, footage, image_sources, llm, logbook, picker, picture_pool, plan_rules, seo, session,
    writing,
    topic_ideas,
)
from patching import owner  # noqa: E402

NET = ("article_images", "commons_search", "openverse_images", "archive_images", "nasa_images",
       "archive_films", "commons_films", "pixabay_films", "nasa_films", "get_image", "film_frames")
from shortsmaker import rules  # noqa: E402

rules.load_rules("strange-history")  # the prompts read the channel's rules file


def still(k: int) -> dict:
    return {"url": f"https://img/{k}.jpg", "small": f"https://img/{k}s.jpg", "title": f"File:Pic {k}.jpg",
            "credit": None, "source": "Wikimedia Commons"}


def film(k: int) -> dict:
    return {"title": f"Film {k}", "credit": None, "src": f"https://film/{k}.mp4", "dur": 60, "site": "Internet Archive"}


class stubbed:
    """Replaces the network functions for one test; `calls` records the search queries."""
    def __init__(self, stills=6, films=1, **over):
        self.calls, self.stills, self.films, self.over = [], stills, films, over

    def __enter__(self):
        self.saved = {k: getattr(owner(k), k) for k in NET}
        n = iter(range(10_000))
        rec = lambda name, out: (lambda *a, **k: (self.calls.append((name, a[0] if a else None)), out())[1])  # noqa: E731
        image_sources.article_images = rec("article", lambda: [still(next(n)) for _ in range(self.stills)])
        image_sources.commons_search = rec("commons", lambda: [still(next(n))])
        image_sources.openverse_images = image_sources.archive_images = image_sources.nasa_images = rec("other", lambda: [])
        footage.archive_films = rec("films", lambda: [film(k) for k in range(self.films)])
        footage.commons_films = footage.pixabay_films = footage.nasa_films = rec("films2", lambda: [])
        image_sources.get_image = lambda url, what: b"jpg:" + url.encode()
        footage.film_frames = lambda f, n=4: [(float(t), b"frame%d" % t) for t in (5, 15, 25, 35)]
        for k, v in self.over.items():
            setattr(owner(k), k, v)
        return self

    def __exit__(self, *exc):
        for k, v in self.saved.items():
            setattr(owner(k), k, v)


def test_gather_pool_shape():
    with stubbed(stills=70, films=1):
        cands = picture_pool.gather_pool(["Ghost Army"], ["Ellsworth Kelly"], ["rubber tank"], ["rubber tank film"])
    stills_ = [c for c in cands if not c.get("film")]
    films_ = [c for c in cands if c.get("film")]
    assert all(c["url"] and c["title"] and "credit" in c and c["thumb"] for c in stills_)
    assert len(films_) == 4 and all(c["url"] == f"https://film/0.mp4#t={c['film']['t']:.0f}" for c in films_)
    assert len({c["url"] for c in cands}) == len(cands)
    assert len(stills_) <= 64


def test_pool_roundtrip():
    with stubbed(stills=3, films=1):
        cands = picture_pool.gather_pool(["X"], [], ["y"], ["y"])
    with tempfile.TemporaryDirectory() as d:
        picture_pool.save_pool(Path(d) / "p", cands)
        back = picture_pool.load_pool(Path(d) / "p")
        assert [c["url"] for c in back] == [c["url"] for c in cands]
        assert [c["thumb"] for c in back] == [c["thumb"] for c in cands]
        assert back[-1]["film"]["src"] == cands[-1]["film"]["src"]
        assert picture_pool.load_pool(Path(d) / "empty") is None


def test_prune_cache_handles_pools():
    saved = image_sources.CACHE, image_sources.POOLS
    with tempfile.TemporaryDirectory() as d:
        image_sources.CACHE = Path(d)
        image_sources.POOLS = image_sources.CACHE / "pools"
        old_file, old_pool, new_pool = image_sources.CACHE / "a.bin", image_sources.POOLS / "old", image_sources.POOLS / "new"
        for p in (old_pool, new_pool):
            p.mkdir(parents=True)
            (p / "pool.json").write_text("[]")
        old_file.write_bytes(b"x")
        past = time.time() - 31 * 86400
        for p in (old_file, old_pool / "pool.json"):
            os.utime(p, (past, past))
        try:
            picture_pool.prune_cache()
            assert not old_file.exists() and not old_pool.exists() and new_pool.exists()
        finally:
            image_sources.CACHE, image_sources.POOLS = saved


def pool_of(n_stills: int, film_frames: int = 0) -> list[dict]:
    cands = [{**still(k), "thumb": b"t%d" % k} for k in range(n_stills)]
    cands += [{"title": "Film 0", "url": f"https://film/0.mp4#t={t}", "credit": None, "thumb": b"f", "source": "REAL FILM",
               "film": {**film(0), "t": float(t)}, "site": "Internet Archive"} for t in range(5, 5 + 10 * film_frames, 10)]
    return cands


TOPIC = {"topic": "The Ghost Army fooled Germany", "subject": "Ghost Army", "wiki_articles": ["Ghost Army"]}


class fake_ai:
    """ask_ai replaced by `reply` (a dict, None, or a function of the prompt); `prompts` records every call."""
    def __init__(self, reply):
        self.reply, self.prompts = reply, []

    def __enter__(self):
        self.saved = llm.ask_ai
        llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: (
            self.prompts.append(prompt), self.reply(prompt) if callable(self.reply) else self.reply)[1]
        return self

    def __exit__(self, *exc):
        llm.ask_ai = self.saved


def entry(n: int, **kw) -> dict:
    return {"n": n, "what": f"picture {n}", "era_ok": True, "sharp": 3, "hook": False, "reject": None, **kw}


def test_catalog_junk():
    cands = pool_of(5)
    reply = {"pictures": [entry("3"), entry(True), entry(99), entry(2, sharp=7), entry(1), entry(1, what="again"), "junk"]}
    with tempfile.TemporaryDirectory() as d, fake_ai(reply):
        got = picture_pool.catalog_pool(TOPIC, cands, Path(d))
        saved = json.loads((Path(d) / "catalog.json").read_text(encoding="utf-8"))
    assert [e["n"] for e in got] == [1] and got[0]["what"] == "picture 1"
    assert saved == got


def test_catalog_failure_stops():
    with tempfile.TemporaryDirectory() as d, fake_ai(None):
        try:
            picture_pool.catalog_pool(TOPIC, pool_of(3), Path(d))
        except SystemExit as e:
            assert TOPIC["topic"] in str(e)
        else:
            raise AssertionError("no SystemExit")


def test_catalog_redone_when_missing():
    cands = pool_of(3)
    with tempfile.TemporaryDirectory() as d:
        picture_pool.save_pool(Path(d), cands)
        with fake_ai({"pictures": [entry(1), entry(2)]}) as ai:
            picture_pool.catalog_pool(TOPIC, cands, Path(d))
            again = picture_pool.catalog_pool(TOPIC, cands, Path(d))
        assert len(ai.prompts) == 1 and [e["n"] for e in again] == [1, 2]


def test_catalog_empty_pool_no_ai():
    with tempfile.TemporaryDirectory() as d, fake_ai(None) as ai:
        assert picture_pool.catalog_pool(TOPIC, [], Path(d)) == [] and ai.prompts == []


def test_usable_counts_film_once():
    cands = pool_of(5, film_frames=4)  # stills 1-5, film frames 6-9
    cat = [entry(1), entry(2), entry(3, reject="watermark"), entry(4, era_ok=False), entry(5, sharp=1),
           entry(6, sharp=2), entry(7), entry(8), entry(9)]
    got = picture_pool.usable(cands, cat)
    assert len(got) == 3 and {e["n"] for e in got} == {1, 2, 7}  # the film counts once, its sharpest frame


def test_catalog_text():
    cands = pool_of(4, film_frames=2)
    text = picture_pool.catalog_text(cands, [entry(5, hook=True, what="rubber tanks inflating"), entry(2), entry(3, reject="logo")])
    assert "#5 film: rubber tanks inflating [opener]" in text and "#2 photo: picture 2" in text and "#3" not in text


LINES = ["Germany feared an army that didn't exist.", "Men pumped up rubber tanks with air compressors.",
         "Then hid them badly so planes would spot them."]


def planning_ai(prompt: str) -> dict:
    """Canned replies for every planning step of write_scripts()."""
    if "You choose stories" in prompt:
        return {"shorts": [{"topic": f"Topic {k}", "subject": f"Subject {k}", "wiki_articles": [f"Article {k}"],
                            "search_terms": ["a"], "visual_terms": ["rubber tank", "", 5], "people": ["Bill Blass"]}
                           for k in range(1, 4)]}
    if "You write YouTube Shorts narration" in prompt:
        return {"shorts": [{"index": 0, "title": "Ghost Army", "hook_text": "FAKE", "scenes": LINES}]}
    if "You are the director" in prompt:
        return {"shorts": [{"index": 0, "scenes": [{"image_search": "x"} for _ in LINES]}]}
    return {}


class planning:
    """write_scripts() with every AI step canned and `prepare` standing in for prepare_topic (unless None)."""
    def __init__(self, prepare=None, **over):
        self.prepare, self.over = prepare, over

    def __enter__(self):
        keys = ("trend_research", "logbook_results", "article_text", "edit_scripts", "fact_check", "prepare_topic", "pick_ideas", *self.over)
        self.saved = {k: getattr(owner(k), k) for k in keys}
        self.ai = fake_ai(planning_ai).__enter__()
        channel_profiles.trend_research, logbook.logbook_results = (lambda ch: []), (lambda: "")
        topic_ideas.pick_ideas = lambda *a, **k: []
        writing.article_text, writing.edit_scripts, writing.fact_check = (lambda t: "text"), (lambda shorts, ch: None), (lambda s: True)
        if self.prepare:
            picture_pool.prepare_topic = self.prepare
        for k, v in self.over.items():
            setattr(owner(k), k, v)
        return self

    def __exit__(self, *exc):
        self.ai.__exit__()
        for k, v in self.saved.items():
            setattr(owner(k), k, v)


def passing(names: set[str]):
    def prepare(s, folder=None):
        s.update(_texts={"A": "text"}, pool_dir=str(folder or "pool"), catalog=[], picture_check="9 usable of 41")
        return s["topic"] in names
    return prepare


def test_topic_prompt_asks_backups_and_visuals():
    with planning(passing({"Topic 1"})) as pl:
        writing.write_scripts({"niche": "history", "done_topics": [], "myths": []}, 1)
    prompt = next(p for p in pl.ai.prompts if "You choose stories" in p)
    assert "Pick 3 NEW topics" in prompt and "visual_terms" in prompt and "people" in prompt


def test_weak_topic_swapped_for_backup():
    ch = {"niche": "history", "done_topics": [], "myths": []}
    seen = {}

    def prepare(s, folder=None):
        seen[s["topic"]] = s
        return passing({"Topic 2"})(s, folder)
    with planning(prepare):
        shorts = writing.write_scripts(ch, 1)
    assert [s["topic"] for s in shorts] == ["Topic 2"]
    assert any("Topic 1" in d for d in shorts[0]["dropped_topics"]) and "Topic 1" not in ch["done_topics"]
    assert seen["Topic 1"]["visual_terms"] == ["rubber tank"] and seen["Topic 1"]["people"] == ["Bill Blass"]
    assert "Topic 3" not in seen  # enough topics passed: the last backup is never gathered


def test_all_weak_returns_empty():
    with planning(passing(set())) as pl:
        shorts = writing.write_scripts({"niche": "history", "done_topics": [], "myths": []}, 1)
    assert shorts == [] and not any("You write YouTube Shorts narration" in p for p in pl.ai.prompts)


def test_empty_pool_drops_topic_without_ai():
    saved = image_sources.POOLS
    with tempfile.TemporaryDirectory() as d, planning(gather_pool=lambda *a: [], article_text=lambda t: "") as pl:
        image_sources.POOLS = Path(d)
        try:
            s = {"topic": "Nothing", "subject": "Nothing", "wiki_articles": ["Nothing"], "visual_terms": [], "people": []}
            assert picture_pool.prepare_topic(s) is False
        finally:
            image_sources.POOLS = saved
    assert pl.ai.prompts == [] and s["picture_check"] == "0 usable of 0"


def test_both_mode_reuses_pools():
    def no_gather(*a):
        raise AssertionError("gathered again")
    with tempfile.TemporaryDirectory() as d:
        picture_pool.save_pool(Path(d), pool_of(8))
        (Path(d) / "catalog.json").write_text(json.dumps([entry(k) for k in range(1, 9)]), encoding="utf-8")
        with planning(gather_pool=no_gather) as pl:
            shorts = writing.write_scripts({"niche": "history", "done_topics": [], "myths": []}, 1, ["Topic 1"], [d])
    assert shorts[0]["pool_dir"] == d and not any("picture researcher" in p for p in pl.ai.prompts)


def test_prompts_carry_picture_list():
    real_edit = writing.edit_scripts
    with tempfile.TemporaryDirectory() as d:
        picture_pool.save_pool(Path(d), pool_of(8))
        cat = [entry(k, hook=k == 2, what=f"tank picture {k}") for k in range(1, 9)]

        def prepare(s, folder=None):
            s.update(_texts={"A": "text"}, pool_dir=d, catalog=cat, picture_check="8 usable of 8")
            return True
        with planning(prepare, edit_scripts=real_edit) as pl:
            writing.write_scripts({"niche": "history", "done_topics": [], "myths": []}, 1)
    for head in ("You write YouTube Shorts narration", "You are the script editor", "You are the director"):
        prompt = next(p for p in pl.ai.prompts if head in p)
        assert "#3 photo: tank picture 3" in prompt, head
    assert "[opener]" in next(p for p in pl.ai.prompts if "You write YouTube Shorts narration" in p)


def pic_short(pics: list, catalog: list[dict], cands: list[dict], d: str, full=None) -> dict:
    picture_pool.save_pool(Path(d), cands)
    return {"pool_dir": d, "catalog": catalog,
            "scenes": [{"narration": "x", "pic": p, "full": full if k == 0 else None} for k, p in enumerate(pics)]}


def test_clean_pics():
    cands = pool_of(4, film_frames=4)  # stills 1-4, frames of one film 5-8
    cat = [entry(1), entry(2, reject="watermark"), entry(3), entry(4), entry(5), entry(6), entry(7), entry(8)]
    with tempfile.TemporaryDirectory() as d:
        s = pic_short([3, 3, True, 99, "4", 5, 6, 7, 2], cat, cands, d)
        picture_pool.clean_pics(s, cands)
    assert [sc["pic"] for sc in s["scenes"]] == [3, None, None, None, None, 5, 6, None, None]


def test_board_item_pics_cleaned():
    cands = pool_of(4)
    board = {"type": "board", "items": [{"label": "A", "pic": 2}, {"label": "B", "pic": 2}, {"label": "C", "pic": 0}], "links": []}
    with tempfile.TemporaryDirectory() as d:
        s = pic_short([None], [entry(k) for k in range(1, 5)], cands, d, full=board)
        picture_pool.clean_pics(s, cands)
    assert [it.get("pic") for it in s["scenes"][0]["full"]["items"]] == [2, None, None]


def test_clean_full_keeps_board_pic():
    f = plan_rules.clean_full({"type": "board", "items": [{"label": "JACK", "find": "Jack photo", "pic": 4},
                                                 {"label": "BOX", "find": "signal box"}, {"label": "TRAIN", "find": "train"}]},
                     plan_rules.words_of("Jack the box train"))
    assert f and f["items"][0]["pic"] == 4 and "pic" not in f["items"][1]


def scene(pic=None, q="ship") -> dict:
    return {"narration": "The ship sailed.", "person": None, "shot": "", "animate": False, "full": None,
            "image_search": q, "video_search": q, "pic": pic, "move": "in"}


class picking:
    """choose_images() with network stubbed; gather_pool returns `extra` (and records its arguments)."""
    def __init__(self, extra=(), reply=None):
        self.extra, self.reply, self.gathered = list(extra), reply, []

    def __enter__(self):
        self.st = stubbed().__enter__()
        self.saved = picture_pool.gather_pool, footage.film_piece
        picture_pool.gather_pool = lambda *a, **kw: (self.gathered.append((a, kw) if kw else a), [dict(c) for c in self.extra])[1]
        footage.film_piece = lambda f, out: (b"film", 0.0)
        self.ai = fake_ai(self.reply).__enter__()
        return self

    def __exit__(self, *exc):
        self.ai.__exit__()
        picture_pool.gather_pool, footage.film_piece = self.saved
        self.st.__exit__()


def planned_short(d: str, scenes: list[dict]) -> dict:
    picture_pool.save_pool(Path(d), pool_of(5))
    return {"title": "Ship", "wiki_articles": ["Ship"], "pool_dir": d, "catalog": [entry(k) for k in range(1, 6)], "scenes": scenes}


def test_choose_keeps_plan_and_appends():
    extra = [{**still(100), "thumb": b"x"}, {**still(101), "thumb": b"y"}, {**still(0), "thumb": b"dup"}]
    reply = {"picks": [{"scene": 1, "bg": 2}, {"scene": 2, "bg": 6}]}
    with tempfile.TemporaryDirectory() as d, picking(extra, reply) as pk:
        short = planned_short(d, [scene(pic=2), scene(q="harbour")])
        chosen = picker.choose_images(short, Path(d) / "work", {"niche": "history"})
    prompt = pk.ai.prompts[0]
    assert '"planned_picture": 2' in prompt and "6: File:Pic 100.jpg" in prompt and "8: " not in prompt  # url dup dropped
    assert pk.gathered[0][0][2] == ["harbour"]  # only the unplanned scene is searched
    assert chosen[0]["plan_note"] == "planned picture kept" and chosen[1]["bg"][1] == "File:Pic 100.jpg"
    assert "plan_note" not in chosen[1]


def test_choose_swap_note():
    reply = {"picks": [{"scene": 1, "bg": 4, "swap_why": "wrong ship"}]}
    with tempfile.TemporaryDirectory() as d, picking((), reply):
        chosen = picker.choose_images(planned_short(d, [scene(pic=2)]), Path(d) / "work", {"niche": "history"})
    assert chosen[0]["plan_note"] == "planned #2 swapped: wrong ship" and chosen[0]["bg"][1] == "File:Pic 3.jpg"


def test_choose_falls_back_to_plan():
    with tempfile.TemporaryDirectory() as d, picking((), None):
        chosen = picker.choose_images(planned_short(d, [scene(pic=2)]), Path(d) / "work", {"niche": "history"})
    assert chosen[0]["bg"][1] == "File:Pic 1.jpg" and chosen[0]["plan_note"] == "planned picture kept"


def test_choose_old_path_unchanged():
    reply = {"picks": [{"scene": 1, "bg": 1}]}
    with tempfile.TemporaryDirectory() as d, picking([{**still(7), "thumb": b"x"}], reply) as pk:
        short = {"title": "Ship", "wiki_articles": ["Ship"], "scenes": [scene(q="old ship")]}
        chosen = picker.choose_images(short, Path(d) / "work", {"niche": "history"})
    assert pk.gathered == [(["Ship"], [], ["old ship"], ["old ship"])]
    assert not any("planned_picture" in p for p in pk.ai.prompts) and "plan_note" not in chosen[0]


def test_edit_plan_picture_line():
    line = editplan.picture_line({"picture_check": "9 usable of 41", "dropped_topics": ['"Emu War": only 3 usable of 20 real pictures/clips']})
    assert line == 'Pictures found before writing: 9 usable of 41 (topics dropped: "Emu War": only 3 usable of 20 real pictures/clips)'
    assert editplan.picture_line({"picture_check": "9 usable of 41", "dropped_topics": []}) == "Pictures found before writing: 9 usable of 41"
    assert editplan.picture_line({}) is None


def test_catalog_empty_reply_asks_other_ai():
    brains, replies = [], [{"pictures": []}, {"pictures": [entry(1)]}]
    saved = llm.ask_ai
    llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: (brains.append(brain), replies.pop(0))[1]
    try:
        with tempfile.TemporaryDirectory() as d:
            got = picture_pool.catalog_pool(TOPIC, pool_of(3), Path(d))
    finally:
        llm.ask_ai = saved
    assert [e["n"] for e in got] == [1] and brains[1] == ("gemini" if session.BRAIN == "claude" else "claude")


def test_catalog_both_empty_stops_uncached():
    with tempfile.TemporaryDirectory() as d, fake_ai({"pictures": [entry("1")]}):
        try:
            picture_pool.catalog_pool(TOPIC, pool_of(3), Path(d))
        except SystemExit:
            pass
        else:
            raise AssertionError("no SystemExit")
        assert not (Path(d) / "catalog.json").exists()


def test_small_pool_skips_ai():
    saved = image_sources.POOLS
    with tempfile.TemporaryDirectory() as d, planning(gather_pool=lambda *a: pool_of(3)) as pl:
        image_sources.POOLS = Path(d)
        try:
            s = {"topic": "Thin", "subject": "Thin", "wiki_articles": ["Thin"], "visual_terms": [], "people": []}
            assert picture_pool.prepare_topic(s) is False
        finally:
            image_sources.POOLS = saved
    assert pl.ai.prompts == [] and s["picture_check"] == "0 usable of 3"


def test_dropped_topic_pool_removed():
    with tempfile.TemporaryDirectory() as d:
        folders = {}

        def prepare(s, folder=None):
            f = Path(d) / s["topic"].replace(" ", "")
            f.mkdir()
            folders[s["topic"]] = f
            return passing({"Topic 2"})(s, f)
        with planning(prepare):
            writing.write_scripts({"niche": "history", "done_topics": [], "myths": []}, 1)
        assert not folders["Topic 1"].exists() and folders["Topic 2"].exists()


def test_seo_pass_empty_no_ai():
    with fake_ai(None) as ai:
        seo.seo_pass([], {"niche": "history"})
    assert ai.prompts == []


def test_seo_pass_research_seeds_dict_and_list():
    short = {
        "title": "Old Title",
        "subject": "Jack Churchill",
        "description": "Old desc",
        "scenes": [{"narration": "He charged with a sword and a longbow. It sounds impossible."}],
        "wiki_articles": ["Jack Churchill", "Commandos", "WW2"],
        "search_terms": ["mad jack churchill", "jack churchill ww2"]
    }
    channel_dict = {
        "niche": "Strange history",
        "research_seeds": {
            "handles": ["@HistoryMatters"],
            "queries": ["weird history facts", "strange but true history"],
            "dropped": []
        }
    }
    ai_reply = {
        "shorts": [{
            "index": 0,
            "title": "Why Captors Pampered This Commando",
            "description": "Jack Churchill defied normal warfare. #History #WW2 #shorts",
            "tags": ["Jack Churchill", "history", "WW2"],
            "pinned_comment": "Would you carry a sword into WW2?"
        }]
    }
    saved_suggestions = seo.search_suggestions
    saved_trend = channel_profiles.trend_research
    seo.search_suggestions = lambda q: [f"{q} suggestion 1"]
    channel_profiles.trend_research = lambda ch: [{"title": "Top Leader Short"}]
    try:
        with fake_ai(ai_reply) as ai:
            shorts = [dict(short)]
            seo.seo_pass(shorts, channel_dict)
            assert shorts[0]["title"] == "Why Captors Pampered This Commando"
            assert "weird history facts" in ai.prompts[0]
            assert "Jack Churchill" in ai.prompts[0]

        channel_list = {"niche": "Strange history", "research_seeds": ["weird history facts"]}
        with fake_ai(ai_reply):
            shorts = [dict(short)]
            seo.seo_pass(shorts, channel_list)
            assert shorts[0]["title"] == "Why Captors Pampered This Commando"

        channel_none = {"niche": "Strange history", "research_seeds": None}
        with fake_ai(ai_reply):
            shorts = [dict(short)]
            seo.seo_pass(shorts, channel_none)
            assert shorts[0]["title"] == "Why Captors Pampered This Commando"
    finally:
        seo.search_suggestions = saved_suggestions
        channel_profiles.trend_research = saved_trend


def test_both_mode_pools_follow_reply_position():
    def reply(prompt):
        if "You choose stories" in prompt:
            return {"shorts": [{"topic": "", "subject": "x"}, {"topic": "Topic 2", "subject": "S2", "wiki_articles": []}]}
        return planning_ai(prompt)
    got = {}

    def prepare(s, folder=None):
        got[s["topic"]] = folder
        return passing({"Topic 2"})(s, folder)
    with planning(prepare) as pl:
        pl.ai.reply = reply
        writing.write_scripts({"niche": "history", "done_topics": [], "myths": []}, 2, ["Topic 1", "Topic 2"], ["dirA", "dirB"])
    assert got == {"Topic 2": Path("dirB")}


def test_board_item_refuses_film():
    cands = pool_of(3, film_frames=2)  # stills 1-3, film frames 4-5
    board = {"type": "board", "items": [{"label": "A", "pic": 4}, {"label": "B", "pic": 1}, {"label": "C", "pic": 2}], "links": []}
    with tempfile.TemporaryDirectory() as d:
        s = pic_short([5], [entry(k) for k in range(1, 6)], cands, d, full=board)
        picture_pool.clean_pics(s, cands)
    assert [it["pic"] for it in s["scenes"][0]["full"]["items"]] == [None, 1, 2] and s["scenes"][0]["pic"] == 5


def test_gather_pool_skip_and_limits():
    with stubbed(stills=10, films=3) as st:
        cands = picture_pool.gather_pool(["X"], [], [], [], skip={"https://img/0.jpg", "https://film/1.mp4"}, limit=4, film_limit=1)
    stills_ = [c for c in cands if not c.get("film")]
    assert len(stills_) == 4 and "https://img/0.jpg" not in {c["url"] for c in stills_}
    assert {c["film"]["src"] for c in cands if c.get("film")} == {"https://film/0.mp4"}


def test_choose_extra_gather_is_bounded():
    with tempfile.TemporaryDirectory() as d, picking((), {"picks": []}) as pk:
        picker.choose_images(planned_short(d, [scene(q="harbour")]), Path(d) / "work", {"niche": "history"})
    args, kw = pk.gathered[0]
    assert kw["skip"] >= {f"https://img/{k}.jpg" for k in range(5)} and kw["limit"] == 59 and kw["film_limit"] == 14


def test_corrupt_pool_and_catalog_redone():
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "pool.json").write_text('[{"url": "x"', encoding="utf-8")
        assert picture_pool.load_pool(Path(d)) is None
        picture_pool.save_pool(Path(d), pool_of(2))
        (Path(d) / "catalog.json").write_text('[{"n": 1', encoding="utf-8")
        with fake_ai({"pictures": [entry(1)]}) as ai:
            assert [e["n"] for e in picture_pool.catalog_pool(TOPIC, pool_of(2), Path(d))] == [1] and len(ai.prompts) == 1
        assert not list(Path(d).glob("*.tmp"))


def test_plan_note_already_used():
    reply = {"picks": [{"scene": 1, "bg": 2}, {"scene": 2, "bg": 2}]}
    with tempfile.TemporaryDirectory() as d, picking((), reply):
        chosen = picker.choose_images(planned_short(d, [scene(pic=3), scene(pic=2)]), Path(d) / "work", {"niche": "history"})
    assert chosen[0]["plan_note"] == "planned #3 swapped: the picker chose another"
    assert chosen[1]["plan_note"] == "planned #2 swapped: it was already used in another scene"


def test_planned_full_pictures_not_sent_when_empty():
    board = {"type": "board", "items": [{"label": "A", "find": "a", "pic": None}, {"label": "B", "find": "b"},
                                         {"label": "C", "find": "c"}], "links": []}
    with tempfile.TemporaryDirectory() as d, picking((), {"picks": []}) as pk:
        sc = {**scene(pic=None), "full": board}
        picker.choose_images(planned_short(d, [scene(pic=1), sc]), Path(d) / "work", {"niche": "history"})
    assert '"planned_full_pictures":' not in pk.ai.prompts[0]  # the scene data, not the rule text


def test_pool_rows_without_thumbs():
    with tempfile.TemporaryDirectory() as d:
        picture_pool.save_pool(Path(d), pool_of(3))
        rows = picture_pool.load_pool(Path(d), thumbs=False)
    assert [r["url"] for r in rows] == [c["url"] for c in pool_of(3)] and all("thumb" not in r for r in rows)


def test_on_topic_ignores_a_lone_shared_name():
    """The Oxford pool (2026-10-26) got stock videos that only shared a first name or "portrait" with the search; animal
    stories must still find their animal."""
    minor, murray = ["William Chester Minor", "James Murray"], ["James Murray", "William Chester Minor"]
    assert not image_sources.on_topic("james webb space telescope, nasa", "James Murray lexicographer", murray)
    assert not image_sources.on_topic("water, south australia, murray mouth", "James Murray lexicographer", murray)
    assert not image_sources.on_topic("boat, beech, stranded, scotland, snow, fort, william", "dr william minor", minor)
    assert not image_sources.on_topic("labrador, dog, pet, animal, portrait", "William Chester Minor portrait", minor)
    assert not image_sources.on_topic("Jimmy Savile - The Rhodesia Solution", "Broadmoor Hospital", minor)
    assert image_sources.on_topic("File:Dr. William Chester Minor.jpg", "William Chester Minor portrait", minor)
    assert image_sources.on_topic("James Murray in a scriptorium", "James Murray lexicographer", murray)
    assert image_sources.on_topic("bear, brown bear, furry, predator", "Wojtek bear", ["Wojtek"])
    assert image_sources.on_topic("bird, nandu, emu, plumage", "Emu War", ["G. P. W. Meredith"])
    assert image_sources.on_topic("Super Mario 64 any% speedrun", "Mario 64")
    assert image_sources.on_topic("Minecraft creeper", "Minecraft") and not image_sources.on_topic("Terraria", "Minecraft")
    # strict (Pixabay's modern stock): one ordinary shared word is the wrong era; two words or the only word are fine
    assert image_sources.on_topic("dialysis, machine, hospital", "Broadmoor Hospital Victorian", minor)
    assert not image_sources.on_topic("dialysis, machine, hospital", "Broadmoor Hospital Victorian", minor, strict=True)
    assert image_sources.on_topic("bear, brown, brown bear, nature", "Syrian brown bear", strict=True)
    assert image_sources.on_topic("emu, bird", "emu", strict=True)


def test_pixabay_keeps_only_on_topic_videos():
    hits = {"hits": [{"id": 1, "tags": "james webb space telescope, nasa", "duration": 10,
                      "videos": {"small": {"url": "https://x/1.mp4"}}},
                     {"id": 2, "tags": "steam locomotive, train, smoke", "duration": 10,
                      "videos": {"small": {"url": "https://x/2.mp4"}}}]}
    old = (footage.PIXABAY_KEY_FILE, image_sources.CACHE, footage.media_tools.fetch)
    with tempfile.TemporaryDirectory() as d:
        footage.PIXABAY_KEY_FILE = Path(d) / "key.txt"
        footage.PIXABAY_KEY_FILE.write_text("k", encoding="utf-8")
        image_sources.CACHE = Path(d) / "cache"
        footage.media_tools.fetch = lambda url, timeout, ua: json.dumps(hits).encode()
        try:
            got = footage.pixabay_films("Victorian steam locomotive", 5)
            named = footage.pixabay_films("James Murray steam train", 5, names=["James Murray"])
        finally:
            footage.PIXABAY_KEY_FILE, image_sources.CACHE, footage.media_tools.fetch = old
    assert [f["src"] for f in got] == ["https://x/2.mp4"], got
    assert [f["src"] for f in named] == ["https://x/2.mp4"], named


def test_fact_check_rewrites_get_the_story_rules_again():
    def fact_check(s):  # its rewrite lands after the editor's story checks
        s["fact_check"] = ['scene 1: "..." -> "..."']
        s["scenes"][0]["narration"] = "In the cold spring of nineteen forty four a whole German army feared rubber tanks."
        return True
    with planning(passing({"Topic 1"}), fact_check=fact_check):
        shorts = writing.write_scripts({"niche": "history", "done_topics": [], "myths": []}, 1)
    notes = shorts[0]["editor_notes"]
    assert any(n.startswith("STILL (after the fact check):") and "15 words" in n for n in notes), notes
    assert any("words, planned" in n for n in notes), notes  # three short lines are far below the planned length


if __name__ == "__main__":
    names = [n for n in sorted(globals()) if n.startswith("test_") and (len(sys.argv) < 2 or n in sys.argv[1:])]
    failed = 0
    for n in names:
        try:
            globals()[n]()
            print(f"PASS {n}")
        except Exception:
            failed += 1
            print(f"FAIL {n}")
            traceback.print_exc()
    print(f"{len(names) - failed}/{len(names)} passed")
    sys.exit(1 if failed else 0)
