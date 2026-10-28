"""Tests for the full-screen motion graphic scenes. No AI usage, no rendering.
Run: .venv\\Scripts\\python.exe tests\\test_full_scenes.py"""
import json
import random
import shutil
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import (  # noqa: E402
    audio_mix, channel_profiles, cli, config, editplan, gpu, image_sources, llm, logbook, motion, picker,
    picture_pool, plan_rules, remotion_render, review, session, short_render, writing,
    topic_ideas,
)
from patching import owner  # noqa: E402
from PIL import Image  # noqa: E402
from shortsmaker import rules  # noqa: E402

rules.load_rules("strange-history")  # the prompts read the channel's rules file


def test_make_paper():
    with tempfile.TemporaryDirectory() as d:
        folder = Path(d) / "paper"
        remotion_render.make_paper(folder)
        with Image.open(folder / "paper.jpg") as im:
            assert im.size == (1300, 2300)
        for k in range(6):
            with Image.open(folder / f"grain{k}.png") as im:
                assert im.size == (1080, 1920) and im.mode == "RGBA"
                assert im.getchannel("A").getextrema()[1] <= 255 * 0.18 + 1  # grain stays faint
        before = (folder / "paper.jpg").stat().st_mtime_ns
        remotion_render.make_paper(folder)  # existing files are kept
        assert (folder / "paper.jpg").stat().st_mtime_ns == before


SAID = plan_rules.words_of("Jack the baboon worked the signal box at Uitenhage near Port Elizabeth for twenty years")


def test_clean_full_board():
    item = lambda k: {"label": f"print {k}", "find": f"photo {k}", "word": "jack"}  # noqa: E731
    assert plan_rules.clean_full({"type": "board", "items": [item(1), item(2)], "links": []}, SAID) is None
    f = plan_rules.clean_full({"type": "board", "items": [item(k) for k in range(6)], "links": [[0, 1], [1, 9], [2, 2], ["a", 1]]}, SAID)
    assert len(f["items"]) == 5 and f["links"] == [[0, 1]]
    assert f["items"][0]["label"] == "PRINT 0" and f["items"][0]["word"] == "jack"
    assert plan_rules.clean_full({"type": "board", "items": [item(1), {"label": ""}, item(3)], "links": []}, SAID) is None


def test_clean_full_journey():
    stop = {"name": "Uitenhage", "lat": -33.76, "lon": 25.40, "word": "Uitenhage"}
    f = plan_rules.clean_full({"type": "journey", "stops": [stop, {"name": "Nowhere", "lat": 200, "lon": 0}], "note": "1881 · 32 km"}, SAID)
    assert [s["name"] for s in f["stops"]] == ["Uitenhage"] and f["note"] == "1881 · 32 KM"
    assert plan_rules.clean_full({"type": "journey", "stops": []}, SAID) is None
    five = plan_rules.clean_full({"type": "journey", "stops": [stop] * 5}, SAID)
    assert len(five["stops"]) == 4


def test_clean_full_document():
    ok = {"type": "document", "kind": "telegram", "key_line": "The baboon stays and gets paid", "date": "1890"}
    assert plan_rules.clean_full(ok, SAID)["kind"] == "telegram"
    assert plan_rules.clean_full({**ok, "key_line": " ".join(["word"] * 15)}, SAID) is None
    assert plan_rules.clean_full({**ok, "kind": "memo"}, SAID) is None
    assert plan_rules.clean_full({**ok, "key_line": ""}, SAID) is None


def test_clean_full_limits():
    f = plan_rules.clean_full({"type": "journey", "stops": [{"name": "Llanfairpwllgwyngyllgogerychwyrndrobwll", "lat": 53.2, "lon": -4.2,
                                                      "word": "Cardiff"}]}, SAID)
    assert len(f["stops"][0]["name"]) <= 28 and "word" not in f["stops"][0]  # never spoken -> no timing word
    b = plan_rules.clean_full({"type": "board", "items": [{"label": "a very long label here", "find": "x" * 300}] * 3, "links": []}, SAID)
    assert b["items"][0]["label"] == "A VERY LONG" and len(b["items"][0]["find"]) <= 120
    assert plan_rules.clean_full({"type": "spiral"}, SAID) is None and plan_rules.clean_full("journey", SAID) is None


def test_number_scaling():
    assert plan_rules.number_figures(30000, 1000) == (1000, 30)
    assert plan_rules.number_figures(1.5e6, None) == (50000, 30)
    each, n = plan_rules.number_figures(1e9, 7)  # 7 would need far more than 60 figures
    assert n <= 60 and each >= 1e9 / 60
    assert plan_rules.show_number(30000) == "30,000" and plan_rules.show_number(1.5e6) == "1.5 MILLION"
    assert plan_rules.show_number(2e9) == "2 BILLION" and plan_rules.show_number(0.3) == "0.3"
    f = plan_rules.clean_full({"type": "number", "value": 30000, "label": "mourners", "icon": "dragon", "each": 1000}, SAID)
    assert (f["icon"], f["show"], f["figures"], f["label"]) == ("person", "30,000", 30, "MOURNERS")
    assert plan_rules.clean_full({"type": "number", "value": -5, "label": "x"}, SAID) is None
    c = plan_rules.clean_full({"type": "number", "value": 100, "label": "deaths", "compare": {"a_label": "1858", "a_value": 100,
                                                                                    "b_label": "today", "b_value": "lots"}}, SAID)
    assert "compare" not in c


def test_limit_full():
    j = {"type": "journey", "stops": [{"name": "A", "lat": 1, "lon": 1}]}
    scenes = [{"full": dict(j), "graphic": {"style": "date"}, "person": {"name": "x"}, "animate": True,
               "narration": f"Jack worked the signal levers at the busy junction for scene {k}"} for k in range(6)]
    scenes[1]["narration"] = "Too short for a map."  # under FULL_MIN_WORDS: refused, scene 3 takes its place
    plan_rules.limit_full(scenes, 2)
    kept = [i for i, sc in enumerate(scenes) if sc["full"]]
    assert kept == [2, 4]  # never scene 1, never a short scene, never adjacent, at most 2
    assert all(scenes[i]["graphic"] is None and scenes[i]["person"] is None and not scenes[i]["animate"] for i in kept)
    assert scenes[3]["graphic"] == {"style": "date"}  # scenes without a full keep their overlay


WORDS = [(0.0, 0.3, "Wide"), (0.3, 0.6, "went"), (0.6, 0.8, "from"), (0.8, 1.2, "Port"), (1.2, 1.7, "Elizabeth"),
         (1.7, 1.9, "to"), (1.9, 2.5, "Uitenhage"), (2.5, 2.7, "the"), (2.7, 3.0, "baboon"), (3.0, 3.3, "stays")]


def test_full_cues_fallback():
    full = {"type": "journey", "stops": [{"name": "Port Elizabeth", "lat": -33.96, "lon": 25.6, "word": "Port Elizabeth"},
                                         {"name": "Cape Town", "lat": -33.9, "lon": 18.4, "word": "Cape Town"},
                                         {"name": "Uitenhage", "lat": -33.76, "lon": 25.4, "word": "Uitenhage"}]}
    cue = plan_rules.full_cues(full, WORDS, 10.0, 15.0)
    ts = cue["times"]
    assert len(ts) == 3 and ts == sorted(ts) and ts[0] == 10.8
    assert all(10.4 <= x <= 14.0 for x in ts)
    one = plan_rules.full_cues({"type": "number", "value": 5, "label": "X"}, WORDS, 10.0, 15.0)
    assert 10.0 < one["at"] < 14.0


def test_full_cues_leave_time_to_finish():
    """Mike's 'WHY MIKE DIED' (2.7 s scene, last word 1 s before the cut): its stamp showed for 0.3 s. The last beat
    now comes FULL_SETTLE before the cut, earlier beats move up with it in order, and an early scene is unchanged."""
    words = [(0.4, 0.7, "owners"), (1.07, 1.4, "syringe"), (1.68, 2.2, "sideshow")]
    full = {"type": "custom", "kind": "flow", "title": "WHY", "brief": "b", "words": ["owners", "syringe", "sideshow"]}
    cues = plan_rules.full_cues(full, words, 28.7, 31.385)["cues"]
    assert cues == sorted(cues) and len(set(cues)) == 3 and cues[0] >= 29.1
    assert cues[-1] <= 31.385 - plan_rules.FULL_SETTLE + 1e-9
    board = {"type": "board", "items": [{"word": "owners"}, {"word": "syringe"}, {"word": "sideshow"}]}
    assert plan_rules.full_cues(board, words, 28.7, 31.385)["times"][-1] <= 31.385 - plan_rules.FULL_SETTLE + 1e-9
    roomy = plan_rules.full_cues(full, words, 28.7, 34.0)["cues"]  # plenty of time: still on the spoken words
    assert roomy == [29.1, 29.77, 30.38]


def test_full_cues_document():
    full = {"type": "document", "kind": "telegram", "key_line": "the baboon stays", "word": "baboon"}
    cue = plan_rules.full_cues(full, WORDS, 10.0, 15.0)
    assert (cue["at"], cue["lineEnd"]) == (12.5, 13.3)  # the spoken key line, start to end
    cue = plan_rules.full_cues({**full, "key_line": "he gets paid in beer"}, WORDS, 10.0, 15.0)
    assert cue["at"] == 12.7 and abs(cue["lineEnd"] - (cue["at"] + 1.2)) < 1e-9  # key line not said: from its word


def _fake_planning(monkey_reply_full):
    """Runs write_scripts with every AI/network step replaced by canned answers; returns (short, director prompt)."""
    lines = ["A railway hired a baboon.", "Wide lost his legs near Uitenhage.", "He bought Jack at a market.",
             "Thirty thousand people heard about it.", "Jack pulled the levers.", "He never made a mistake.",
             "That railway hired a baboon."]
    lines[1:6] = [x.rstrip(".") + " on the old line near the station that year." for x in lines[1:6]]  # long enough for a full
    seen = {}

    def ask(prompt, fatal=True, read_dir=None, brain=None, bulk=False):
        if "You choose stories" in prompt:
            return {"shorts": [{"topic": "Jack", "subject": "Jack", "wiki_articles": ["Jack (baboon)"], "search_terms": []}]}
        if "You write YouTube Shorts narration" in prompt:
            return {"shorts": [{"index": 0, "title": "Jack", "hook_text": "PAID IN BEER", "scenes": lines}]}
        if "You are the director" in prompt:
            seen["director"] = prompt
            return {"shorts": [{"index": 0, "scenes": [{"image_search": "x", "graphic": {"style": "date", "text": "1881"},
                                                       "full": monkey_reply_full(k)} for k in range(len(lines))]}]}
        return {}

    saved = {k: getattr(owner(k), k) for k in ("ask_ai", "trend_research", "logbook_results", "article_text", "edit_scripts", "fact_check",
                                        "prepare_topic", "pick_ideas")}
    llm.ask_ai, channel_profiles.trend_research, logbook.logbook_results = ask, (lambda ch: []), (lambda: "")
    topic_ideas.pick_ideas = lambda *a, **k: []
    picture_pool.prepare_topic = lambda s, folder=None: (s.update(_texts={"A": "text"}, pool_dir="pool", catalog=[], picture_check="9 usable of 9"), True)[1]
    writing.article_text, writing.edit_scripts, writing.fact_check = (lambda t: "text"), (lambda shorts, ch: None), (lambda s: True)
    try:
        ch = {"niche": "history", "done_topics": [], "myths": []}
        return writing.write_scripts(ch, 1)[0], seen.get("director", "")
    finally:
        for k, v in saved.items():
            setattr(owner(k), k, v)


def test_director_prompt_mentions_full():
    journey = {"type": "journey", "stops": [{"name": "Uitenhage", "lat": -33.76, "lon": 25.4, "word": "Uitenhage"}]}
    short, prompt = _fake_planning(lambda k: journey if k in (0, 2, 3, 5) else None)
    assert all(w in prompt for w in ('"full"', "journey", "board", "document", "never scene 1"))
    kept = [k for k, sc in enumerate(short["scenes"]) if sc["full"]]
    assert kept == [2, 5]  # scene 1 refused, scene 4 sits next to scene 3, at most 2 planned
    assert short["scenes"][2]["graphic"] is None


def test_fact_check_drops_full():
    s = {"title": "Jack", "wiki_articles": [], "_texts": {"Jack": "text"}, "hook_text": "H", "thumbnail_text": "T",
         "scenes": [{"narration": "Wide went to Uitenhage.", "graphic": None, "person": None,
                     "full": {"type": "number", "value": 9, "label": "LEGS"}},
                    {"narration": "Jack stayed.", "graphic": None, "person": None,
                     "full": {"type": "number", "value": 5, "label": "YEARS"}}]}
    saved = llm.ask_ai
    llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: (
        {"story_holds": True, "fixes": [{"scene": 1, "narration": "Wide went to Uitenhage.", "drop_full": True, "why": "no"},
                                        {"scene": 2, "full_fix": {"type": "number", "value": 9, "label": "YEARS"}, "why": "9"}]}
        if '"full"' in prompt else {})
    try:
        writing.fact_check(s)
    finally:
        llm.ask_ai = saved
    assert s["scenes"][0]["full"] is None and s["scenes"][1]["full"]["value"] == 9


def _board(n):
    return {"type": "board", "items": [{"label": f"P{k}", "find": f"photo {k}"} for k in range(n)], "links": [[0, 1], [2, 3]]}


def test_board_pictures_attached():
    cands = [{"url": f"u{k}", "title": f"t{k}", "credit": None, "site": "Wikimedia Commons"} for k in range(6)]
    cands.append({"url": "film", "title": "f", "credit": None, "film": {"t": 1}})
    short = {"scenes": [{"full": None}, {"full": _board(4)}, {"full": None}, {"full": _board(4)}, {"full": {"type": "document", "kind": "letter", "key_line": "x"}}]}
    picks = {2: {"full_pictures": [1, 2, None, 3]},  # one item has no picture: 3 left, the board stays
             4: {"full_pictures": [4, 7, 99, None]},  # only 1 usable (7 is film, 99 doesn't exist): board dropped
             5: {"full_pictures": [5]}}
    saved = image_sources.get_image
    image_sources.get_image = lambda url, what: b"jpg" + url.encode()
    try:
        got = picker.full_pictures(short, picks, cands, set())
    finally:
        image_sources.get_image = saved
    b = short["scenes"][1]["full"]
    assert [it["label"] for it in b["items"]] == ["P0", "P1", "P3"] and b["links"] == [[0, 1]]
    assert [p[1] for p in got[1]] == ["t0", "t1", "t2"]
    assert short["scenes"][3]["full"] is None and 3 not in got
    assert got[4][0][0] == b"jpgu4"  # the document got its real scan


def test_rescue_respects_caps():
    j = lambda k: {"type": "journey", "stops": [{"name": f"Town {k}", "lat": 1, "lon": 1}]}  # noqa: E731
    short = {"title": "T", "research": {"A": "text"}, "wiki_articles": ["A"],
             "scenes": [{"narration": f"Jack worked the signal levers at the busy junction for scene {k}", "full": None, "graphic": None, "person": None} for k in range(7)]}
    short["scenes"][2]["full"] = j(2)
    short["scenes"][5]["full"] = j(5)
    saved = llm.ask_ai
    llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: {"scenes": [
        {"scene": 4, "full": j(4)},  # next to scene 3 (index 2): refused
        {"scene": 1, "full": j(1)},  # the hook: refused
        {"scene": 7, "full": {"type": "board", "items": [], "links": []}},  # boards need photos: refused
        {"scene": 8, "full": j(8)}]}  # not asked for
    try:
        got = picker.rescue_graphics(short, [0, 3, 6], {3: "no picture"})
    finally:
        llm.ask_ai = saved
    assert got == [] and sum(1 for sc in short["scenes"] if sc["full"]) == 2
    for sc in short["scenes"]:
        sc["full"] = None
    short["scenes"][1]["full"], short["scenes"][3]["full"] = j(1), j(3)
    short["scenes"][5]["graphic"] = {"style": "date", "text": "1881"}
    llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: {"scenes": [{"scene": 6, "full": j(6)}, {"scene": 7, "full": j(7)}]}
    try:
        got = picker.rescue_graphics(short, [5, 6], {})
    finally:
        llm.ask_ai = saved
    assert got == [5] and sum(1 for sc in short["scenes"] if sc["full"]) == 3  # MAX_FULL reached (and 7 sits next to 6)
    assert short["scenes"][5]["graphic"] is None


def test_opener_graphic():
    """Scene 1's motion-graphic opener: set outside the scene-1 and two-in-a-row rules, its reason kept for the edit
    plan; it may not decline: an unusable pick is asked once more (told why), two leave scene 1 alone."""
    num = {"type": "number", "value": 70000, "label": "francs paid for the Eiffel Tower", "icon": "money", "word": "fortune"}
    short = {"title": "T", "research": {"A": "text"}, "wiki_articles": ["A"],
             "scenes": [{"narration": "A scrap dealer paid a fortune for the Eiffel Tower.", "full": None, "graphic": None,
                         "person": None, "animate": True},
                        {"narration": "But the seller used forged papers.", "graphic": None, "person": None,
                         "full": {"type": "document", "kind": "letter", "key_line": "x"}}]}
    saved, prompts = llm.ask_ai, []
    doc = {"full": {"type": "document", "kind": "letter", "key_line": "y"}, "why": "x"}
    replies = iter([{"full": num, "why": "the sum is the shock"}, {"full": None, "why": "a portrait reads better"},
                    {"full": dict(num), "why": "retried"}, doc, doc])
    llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: prompts.append(prompt) or next(replies)
    try:
        note = picker.opener_graphic(short)
        assert note.startswith("motion graphic: ") and note.endswith("(the sum is the shock)"), note
        sc = short["scenes"][0]
        assert sc["full"]["type"] == "number" and sc["animate"] is False and sc["full_rescued"] == "motion-graphic opener"
        assert sc["full"]["label"] == "FRANCS PAID FOR THE" and "word" not in sc["full"]  # cut at a word; moves on frame 0
        assert plan_rules.full_cues(sc["full"], [(1.0, 1.4, "fortune")], 0.0, 2.6) == {"at": 0.0}
        assert "Not a document" in prompts[0]
        assert picker.opener_graphic(short).endswith("(already planned)") and len(prompts) == 1
        sc["full"] = None
        assert picker.opener_graphic(short).endswith("(retried)") and sc["full"]["type"] == "number"  # a decline is re-asked
        assert "Pick the FULL-SCREEN" in prompts[1] and "rejected: the AI gave none" in prompts[2]
        sc["full"] = None
        assert picker.opener_graphic(short) == "no motion graphic (the AI picked an unusable one)" and sc["full"] is None
        assert len(prompts) == 5
    finally:
        llm.ask_ai = saved
    # the opener's first element lands on frame 0; later scenes still wait out their transition
    assert plan_rules.full_cues({"type": "journey", "stops": [{"name": "Paris"}]}, [], 0.0, 2.6)["times"] == [0.0]
    assert plan_rules.full_cues({"type": "journey", "stops": [{"name": "Paris"}]}, [], 10.0, 12.6)["times"] == [10.4]


def test_state_roundtrip_full_pics():
    with tempfile.TemporaryDirectory() as d:
        work = Path(d)
        choices = [{"bg": None, "person": None}, {"bg": (b"bg", "t", None), "person": None,
                                                  "full_pics": [(b"a", "ta", "cr", "Wikimedia Commons"), (b"b", "tb", None, "NASA")]}]
        short = {"title": "T", "research": {"A": "long text"}, "scenes": []}
        short_render.save_state(work, short, choices, None, set())
        st = short_render.load_state(work)
        assert st["choices"][1]["full_pics"] == [(b"a", "ta", "cr", "Wikimedia Commons"), (b"b", "tb", None, "NASA")]
        assert "research" not in st["short"] and short["research"]  # not saved, and the live plan keeps it


def _jpg(w=40, h=30) -> bytes:
    import io
    buf = io.BytesIO()
    Image.new("RGB", (w, h), (90, 80, 70)).save(buf, "JPEG")
    return buf.getvalue()


def test_remotion_props_full():
    with tempfile.TemporaryDirectory() as d:
        job = Path(d)
        sc = {"full": {"type": "journey", "stops": [{"name": "A", "lat": 1, "lon": 2, "word": "a"}, {"name": "B", "lat": 3, "lon": 4}], "note": "1881"}}
        p = motion.full_props(sc, {"full": {"times": [1.0, 2.0], "noteAt": 2.4}}, 3, None, job)
        assert p["seed"] == 4 and [s["at"] for s in p["stops"]] == [1.0, 2.0] and p["noteAt"] == 2.4
        board = {"full": _board(3)}
        pics = [(_jpg(60, 30), "t", None, "NASA")] * 3
        p = motion.full_props(board, {"full": {"times": [1.0, 1.5, 2.0]}}, 2, pics, job)
        assert [it["image"] for it in p["items"]] == ["job/full2_0.jpg", "job/full2_1.jpg", "job/full2_2.jpg"]
        assert (job / "full2_1.jpg").exists() and abs(p["items"][0]["aspect"] - 2.0) < 0.01 and p["items"][2]["at"] == 2.0
        assert motion.full_props(board, {"full": {"times": [1.0, 1.5, 2.0]}}, 2, None, job) is None  # board without photos
        doc = {"full": {"type": "document", "kind": "letter", "key_line": "x y"}}
        p = motion.full_props(doc, {"full": {"at": 1.0, "lineEnd": 2.0}}, 5, [(_jpg(30, 60), "scan", None, "Wikimedia Commons")], job)
        assert p["image"] == "job/full5_0.jpg" and p["lineEnd"] == 2.0 and abs(p["aspect"] - 0.5) < 0.01
        p = motion.full_props({"full": {"type": "number", "value": 5, "show": "5", "label": "X", "icon": "coin", "each": 1, "figures": 5}},
                         {"full": {"at": 1.3}}, 1, None, job)
        assert p["at"] == 1.3 and p["figures"] == 5


def test_remotion_failure_paints():
    with tempfile.TemporaryDirectory() as d:
        work = Path(d)
        short = {"scenes": [{"narration": "a", "shot": "WIDE: a harbour", "ai_image": "", "full": None},
                            {"narration": "b", "shot": "WIDE: a map of the bay", "ai_image": "", "full": {"type": "number"}}]}
        images, sources = [Image.new("RGB", (10, 10)), Image.new("RGB", (10, 10))], ["x", "MOTION GRAPHIC"]
        asked, order = [], []

        def fake_moss(items, folder):  # MOSS paints first; here it can't, so Gemini gets the picture
            order.append("moss")
            return set()

        def fake_gemini(items, folder):
            order.append("gemini")
            asked.extend(items)
            for it in items:
                Image.new("RGB", (1200, 800), (200, 10, 10)).save(it["out"])
            return {it["out"] for it in items}

        saved = gpu.gemini_images, shutil.which, gpu.moss_images
        gpu.gemini_images, gpu.moss_images = fake_gemini, fake_moss
        shutil.which = lambda name: "agy" if name == "agy" else saved[1](name)
        try:
            made = remotion_render.paint_instead(short, work, [1], images, sources)
        finally:
            gpu.gemini_images, shutil.which, gpu.moss_images = saved
        assert order == ["moss", "gemini"]
        assert short["scenes"][1]["full"] is None and "map of the bay" in asked[0]["prompt"]
        assert sources[1].startswith("AI-GENERATED") and "Remotion failed" in sources[1]
        assert images[1].size != (10, 10) and str(work / "ai1.jpg") in made


def test_sfx_full():
    scenes = [{"transition": "fade", "graphic": None, "full": None},
              {"transition": "fade", "graphic": None, "full": _board(3)},
              {"transition": "fade", "graphic": None, "full": {"type": "journey", "stops": [{}, {}]}},
              {"transition": "fade", "graphic": None, "full": {"type": "number"}},
              {"transition": "fade", "graphic": None, "full": {"type": "document"}}]
    cues = [{}, {"full": {"times": [5.0, 6.0, 7.0]}}, {"full": {"times": [10.5, 12.0], "noteAt": 12.4}},
            {"full": {"at": 15.0}}, {"full": {"at": 21.0, "lineEnd": 22.0}}]
    random.seed(1)
    ev = audio_mix.sfx_events({"scenes": scenes}, cues, [0, 4, 10, 14, 20, 25], True)
    what = [(e["sound"], e["t"]) for e in ev]
    assert [t for s, t in what if s == "pin"][:3] == [5.0, 6.0, 7.0]  # one pin per print
    assert ("pin", 10.5) in what and ("pin", 12.0) in what and ("scratch", 10.7) in what  # route draws to the 2nd stop
    assert ("ticks", 15.0) in what and ("scratch", 21.0) in what
    assert any(s.startswith("stamp") and 20.0 <= t <= 20.3 for s, t in what)  # the document lands
    assert audio_mix.SFX_FILES.count("scratch") == 1


def test_full_summary():
    assert motion.full_summary({"type": "journey", "stops": [{"name": "Port Elizabeth"}, {"name": "Uitenhage"}], "note": "1881"}) \
        == "map journey: Port Elizabeth -> Uitenhage, 1881"
    assert motion.full_summary({"type": "number", "show": "30,000", "label": "MOURNERS", "each": 1000, "figures": 30}) \
        == "big number: 30,000 MOURNERS (30 figures, each = 1,000)"
    assert motion.full_summary({"type": "board", "items": [{"label": "JACK"}, {"label": "WIDE"}, {"label": "STATION"}]}) \
        == "evidence board: JACK / WIDE / STATION"
    assert motion.full_summary({"type": "document", "kind": "telegram", "key_line": "He stays"}) == 'document (telegram): "He stays" underlined'


def test_review_fix_kinds():
    data = {"problems": [{"second": 3, "scene": 2, "what": "blurry crop", "fix": "repaint"},
                         {"second": 9, "scene": 4, "what": "a modern photo for a line about a journey", "fix": "graphic"},
                         {"second": 1, "scene": 1, "what": "wrong era", "fix": "graphic"},  # the hook never becomes a graphic
                         {"second": 12, "scene": 5, "what": "logo in the corner", "repaint": True},  # old-style answer
                         {"second": 14, "scene": 6, "what": "text over a face", "fix": None}]}
    found, fixes = review.review_fixes(data, 7)
    assert len(found) == 5 and found[0].startswith("LOOK at 0:03")
    assert fixes == {1: ("repaint", "blurry crop"), 3: ("graphic", "a modern photo for a line about a journey"),
                     0: ("repaint", "wrong era"), 4: ("repaint", "logo in the corner")}


def test_auto_fix_graphic():
    with tempfile.TemporaryDirectory() as d:
        work = Path(d)
        st = {"short": {"scenes": [{"narration": f"l{k}", "full": None, "ai_image": "p", "animate": False} for k in range(7)]},
              "choices": [{"bg": (b"x", "t", None), "person": None} for _ in range(7)], "by_gemini": []}
        calls = []

        def fake_rescue(short, scenes, why):
            calls.append(sorted(scenes))
            short["scenes"][2]["full"] = {"type": "number"}
            return [2]

        saved = picker.rescue_graphics, llm.ask_ai
        picker.rescue_graphics, llm.ask_ai = fake_rescue, (lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: None)
        try:
            notes = review.apply_review_fixes(st, work, {2: ("graphic", "weak"), 4: ("repaint", "blurry"), 5: ("graphic", "dull"),
                                                    6: ("repaint", "a"), 1: ("repaint", "b")})
        finally:
            picker.rescue_graphics, llm.ask_ai = saved
        assert calls == [[2, 5]] and len(notes) == short_render.AUTO_REPAINT_MAX
        assert notes[0] == "scene 3 became a motion graphic (weak)"
        assert st["choices"][2]["bg"] is not None  # its picture stays as the fallback
        assert st["choices"][4]["bg"] is None and st["choices"][5]["bg"] is None  # repainted (5: no graphic fit)


def test_review_uses_unused_pool_pictures_before_painting():
    """Togo vs Balto: 4 real pictures the review rejected became paintings while ~20 usable pool pictures sat unused.
    A rejected scene now gets an unused real one when the AI finds one that fits; only the rest are painted."""
    with tempfile.TemporaryDirectory() as d:
        work, pool = Path(d), Path(d) / "pool"
        pool.mkdir()
        titles = ["used.jpg", "rejected-before.jpg", "musher.jpg", "blurry.jpg", "ice.jpg"]
        (pool / "pool.json").write_text(json.dumps([{"title": t, "url": f"http://x/{t}", "credit": None, "source": "test"}
                                                    for t in titles]), encoding="utf-8")
        catalog = [{"n": k + 1, "what": t[:-4], "era_ok": True, "sharp": 1 if t == "blurry.jpg" else 3, "hook": False,
                    "reject": None} for k, t in enumerate(titles)]
        scenes = [{"narration": f"l{k}", "full": None, "ai_image": "p", "animate": False, "graphic": None} for k in range(3)]
        scenes[1]["graphic"] = {"style": "mark"}
        st = {"short": {"title": "Togo", "scenes": scenes, "pool_dir": str(pool), "catalog": catalog,
                        "review_rejected": ["rejected-before.jpg"]},
              "choices": [{"bg": (b"x", "used.jpg", None), "person": None}, {"bg": (b"x", "satellite.jpg", None), "person": None},
                          {"bg": None, "person": None}], "by_gemini": []}
        prompts = []

        def ask(prompt, fatal=True, read_dir=None, brain=None, bulk=False):
            prompts.append(prompt)
            if "haven't used yet" in prompt:  # scene 2 gets #3; scene 3: #1 is on screen already, so it's refused
                return {"picks": [{"scene": 2, "picture": 3}, {"scene": 3, "picture": 1}]}
            return None
        saved = llm.ask_ai, image_sources.get_image
        llm.ask_ai, image_sources.get_image = ask, (lambda url, why: b"jpg:" + url.encode())
        try:
            notes = review.apply_review_fixes(st, work, {1: ("repaint", "modern satellite photo"), 2: ("repaint", "garbled")})
        finally:
            llm.ask_ai, image_sources.get_image = saved
        offered = prompts[0].split("Unused real pictures")[1]
        assert "#3 photo: musher" in offered and "#5 photo: ice" in offered
        assert "#1" not in offered and "#2" not in offered and "#4" not in offered  # on screen, rejected before, blurry
        assert st["choices"][1]["bg"] == (b"jpg:http://x/musher.jpg", "musher.jpg", None)
        assert st["short"]["scenes"][1]["graphic"] is None  # its mark circled the old picture
        assert "satellite.jpg" in st["short"]["review_rejected"]
        assert st["choices"][2]["bg"] is None  # nothing fit: painted
        assert notes[0].startswith("scene 2 got an unused real picture from the pool (musher)")
        assert notes[1].startswith("scene 3 got a new painted picture"), notes


def test_rewrite_paint_prompts():
    """Mike's newsstand: a repaint from the unchanged prompt painted the identical picture (MOSS seeds from the prompt).
    Rejected paintings get a rewritten prompt that follows the picture rules; a bad or missing answer still changes it."""
    scenes = [{"narration": f"line {k}", "shot": None, "ai_image": f"old {k}"} for k in range(4)]
    short = {"topic": "Mike the headless chicken", "scenes": scenes}
    seen = []

    def ask(prompt, fatal=True, read_dir=None, brain=None, bulk=False):
        seen.append(prompt)
        return {"prompts": [{"scene": 2, "ai_image": "A newsboy holds up a magazine reading \"LIFE\", gouache."},
                            {"scene": 3, "ai_image": "old 2"},  # unchanged: refused
                            {"scene": 4, "ai_image": "A photograph of a motel"},  # never a fake photo
                            {"scene": 1, "ai_image": "not asked for"}]}

    saved = llm.ask_ai
    llm.ask_ai = ask
    try:
        done = review.rewrite_paint_prompts(short, {1: "garbled lettering", 2: "dull", 3: "wrong era"})
    finally:
        llm.ask_ai = saved
    assert done == [1] and scenes[1]["ai_image"].startswith("A newsboy")
    assert scenes[2]["ai_image"] != "old 2" and scenes[3]["ai_image"].startswith("old 3 Seen from a different angle")
    assert scenes[0]["ai_image"] == "old 0"  # not being repainted: untouched
    assert session.RULES["AI paintings"] in seen[0] and "garbled lettering" in seen[0]


def test_paint_new_clears_full():
    with tempfile.TemporaryDirectory() as d:
        st = {"short": {"scenes": [{"narration": "a", "full": None, "ai_image": "p", "animate": True},
                                   {"narration": "b", "full": {"type": "number"}, "ai_image": "p", "animate": False}]},
              "choices": [{"bg": (b"x", "t", None), "person": None}, {"bg": None, "person": None}], "by_gemini": []}
        review.paint_new(Path(d), st, 1)
        assert st["short"]["scenes"][1]["full"] is None
        st["short"]["scenes"][1]["full"] = {"type": "number"}
        cli.use_picture_from(Path(d), st, 1, 0)
        assert st["short"]["scenes"][1]["full"] is None


def test_clean_full_custom_and_skin():
    c = plan_rules.clean_full({"type": "custom", "kind": "diagram", "skin": "blueprint", "title": "signal box levers",
                      "brief": "Four railway levers lock in sequence", "words": ["Jack", "Uitenhage", "notspoken"],
                      "photos": [{"label": "jack the baboon", "find": "photo of jack", "word": "Jack"}]}, SAID)
    assert c["kind"] == "diagram" and c["skin"] == "blueprint" and c["title"] == "SIGNAL BOX LEVERS"
    assert c["words"] == ["Jack", "Uitenhage"] and c["photos"][0]["label"] == "JACK THE BABOON"
    assert plan_rules.clean_full({"type": "custom", "title": "", "brief": "x"}, SAID) is None
    assert plan_rules.clean_full({"type": "custom", "title": "x", "brief": ""}, SAID) is None
    assert config.short_skin({"palette": "sky", "music_mood": "curious"}) == "blueprint"
    assert config.short_skin({"palette": "crimson", "music_mood": "tense"}) == "dossier"
    assert config.short_skin({"palette": "teal", "music_mood": "playful"}) == "hud"
    assert config.short_skin({"palette": "parchment", "music_mood": "calm"}) == "parchment"


def test_custom_cues_props_and_pictures():
    full = {"type": "custom", "kind": "collage", "title": "JACK", "brief": "Archival collage",
            "words": ["Port Elizabeth", "Uitenhage", "baboon"],
            "photos": [{"label": "JACK", "find": "jack"}, {"label": "BOX", "find": "box"}]}
    cue = plan_rules.full_cues(full, WORDS, 10.0, 15.0)
    assert len(cue["cues"]) == 3 and cue["cues"] == sorted(cue["cues"]) and cue["cues"][0] == 10.8
    with tempfile.TemporaryDirectory() as d:
        job = Path(d)
        p = motion.full_props({"full": full}, {"full": cue}, 2, [(_jpg(60, 30), "t", None, "NASA")], job, skin="dossier", slot=1)
        assert p["slot"] == 1 and p["skin"] == "dossier" and len(p["photos"]) == 1
        assert p["photos"][0]["image"] == "job/full2_0.jpg" and p["photos"][0]["label"] == "JACK"


def test_code_custom_scenes_fallback():
    gen_dir = config.REMOTION / "src" / "full" / "generated"
    saved = (gen_dir / "Custom0.tsx").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as d:
        work = Path(d)
        short = {"title": "Test Short", "scenes": [{"narration": "Step one happened, then step two, and finally the twist.",
                                                    "full": {"type": "custom", "kind": "flow", "title": "THE LOOPHOLE",
                                                             "brief": "Three step chain"}}]}
        scenes = [{"start": 4.0, "end": 9.0, "full": {"type": "custom", "slot": 0, "kind": "flow", "skin": "hud",
                                                      "seed": 1, "title": "THE LOOPHOLE", "cues": [4.5, 6.0, 7.5], "photos": []}}]
        old_ask = llm.ask_ai
        llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: {"code": "not valid typescript"}
        try:
            motion.code_custom_scenes(short, scenes, work)
            assert (work / "Custom0.tsx").exists()
            assert "export const Custom0" in (work / "Custom0.tsx").read_text(encoding="utf-8")
        finally:
            llm.ask_ai = old_ask
            (gen_dir / "Custom0.tsx").write_text(saved, encoding="utf-8")


def test_quota_fallback_both_ways():
    old_run, old_agy, old_brain, old_no_quota = subprocess.run, llm.run_agy, session.BRAIN, set(session.NO_QUOTA)
    calls = []

    class DummyRes:
        def __init__(self, stdout="", stderr=""):
            self.stdout, self.stderr = stdout, stderr

    try:
        session.NO_QUOTA.clear()
        session.BRAIN = "claude"
        subprocess.run = lambda cmd, **kw: (calls.append("claude") or
                                              DummyRes("You've hit your weekly limit · resets 1pm (Asia/Manila)"))
        llm.run_agy = lambda prompt, folder, timeout=900, model=None: (calls.append("gemini") or '{"ok": 1}')
        ans = llm.ask_ai("test prompt", fatal=False)
        assert ans == {"ok": 1} and session.LAST_AI == "gemini" and session.BRAIN == "gemini"
        assert calls == ["claude", "gemini"] and "claude" in session.NO_QUOTA  # only 1 try on Claude before switching!
        # Next call skips Claude completely because it's in NO_QUOTA:
        ans2 = llm.ask_ai("second prompt", fatal=False, brain="claude")
        assert ans2 == {"ok": 1} and calls == ["claude", "gemini", "gemini"]

        # Reverse direction: Gemini out of quota -> switches to Claude
        session.NO_QUOTA.clear()
        calls.clear()
        session.BRAIN = "gemini"
        llm.run_agy = lambda prompt, folder, timeout=900, model=None: (calls.append("gemini") or "RESOURCE_EXHAUSTED: Quota exceeded")
        subprocess.run = lambda cmd, **kw: (calls.append("claude") or DummyRes('{"ok": 2}'))
        ans3 = llm.ask_ai("third prompt", fatal=False)
        assert ans3 == {"ok": 2} and session.LAST_AI == "claude" and session.BRAIN == "claude"
        assert calls == ["gemini", "claude"] and "gemini" in session.NO_QUOTA
    finally:
        subprocess.run, llm.run_agy, session.BRAIN = old_run, old_agy, old_brain
        session.NO_QUOTA.clear()
        session.NO_QUOTA.update(old_no_quota)


def _review_state(work: Path):
    custom = {"type": "custom", "kind": "clock", "title": "NINE YEARS", "brief": "a clock", "cues": [1.0]}
    st = {"short": {"title": "Jack", "scenes": [{"narration": f"l{k}", "full": None, "ai_image": "p", "animate": False}
                                                for k in range(6)]},
          "choices": [{"bg": (b"x", "t", None), "person": None} for _ in range(6)], "by_gemini": []}
    st["short"]["scenes"][1]["full"] = dict(custom, title="FIRST")  # slot 0
    st["short"]["scenes"][3]["full"] = custom  # slot 1
    st["short"]["scenes"][5]["full"] = {"type": "number", "value": 5, "label": "X"}
    (work / "Custom1.tsx").write_text("// Custom1: NINE YEARS | clock\nold code\n", encoding="utf-8")
    return st


def test_review_redraws_custom():
    with tempfile.TemporaryDirectory() as d:
        work = Path(d)
        st = _review_state(work)
        prompts = []

        def ask(prompt, fatal=True, read_dir=None, brain=None, bulk=False):
            prompts.append(prompt)
            if "were rejected" in prompt:
                return {"prompts": [{"scene": 6, "ai_image": "A sharper new picture, charcoal drawing on toned paper."}]}
            return {"code": GOOD_TSX.replace("Custom0", "Custom1")}  # must follow the scene rules too

        saved = llm.ask_ai, motion.tsc_check
        llm.ask_ai, motion.tsc_check = ask, (lambda: None)
        try:
            notes = review.apply_review_fixes(st, work, {3: ("repaint", "the title covers the clock"), 5: ("repaint", "blurry")})
        finally:
            llm.ask_ai, motion.tsc_check = saved
        assert notes == ["scene 4's motion graphic was redrawn (the title covers the clock)",
                         "scene 6 got a new painted picture from a rewritten prompt (blurry)"]
        assert st["short"]["scenes"][5]["ai_image"] == "A sharper new picture, charcoal drawing on toned paper."
        assert "the title covers the clock" in prompts[0] and "old code" in prompts[0]
        cached = (work / "Custom1.tsx").read_text(encoding="utf-8")
        assert cached.startswith("// Custom1: NINE YEARS | clock\n") and "export const Custom1" in cached  # same signature: the re-render uses it
        assert st["short"]["scenes"][3]["full"] and st["short"]["scenes"][5]["full"] is None  # templates still get painted


def test_redraw_failure_paints():
    with tempfile.TemporaryDirectory() as d:
        work = Path(d)
        st = _review_state(work)
        saved = llm.ask_ai, motion.tsc_check
        llm.ask_ai, motion.tsc_check = (lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: {"code": "export const Custom1 = (;"}), \
            (lambda: "error TS1109: Expression expected.")
        try:
            notes = review.apply_review_fixes(st, work, {3: ("repaint", "broken")})
        finally:
            llm.ask_ai, motion.tsc_check = saved
        assert notes == ["scene 4 got a new painted picture from its old prompt, seen from a new angle (broken)"]
        assert st["short"]["scenes"][3]["full"] is None
        assert "old code" in (work / "Custom1.tsx").read_text(encoding="utf-8")  # the cache was not overwritten by bad code


def test_new_picture_drops_mark():
    """A "mark" card circles a detail of the old picture: it must go when the picture changes (Unsinkable Sam, 2026-10-18)."""
    with tempfile.TemporaryDirectory() as d:
        mark = {"style": "mark", "text": "A PLANK", "shape": "arrow", "x": 0.5, "y": 0.7}
        date = {"style": "date", "text": "1941"}
        st = {"short": {"scenes": [{"narration": "a", "full": None, "ai_image": "p", "animate": False, "graphic": dict(date)},
                                   {"narration": "b", "full": None, "ai_image": "p", "animate": False, "graphic": dict(mark)}]},
              "choices": [{"bg": (b"x", "t", None), "person": None}, {"bg": (b"y", "t", None), "person": None}], "by_gemini": []}
        review.paint_new(Path(d), st, 1)
        assert st["short"]["scenes"][1]["graphic"] is None
        st["short"]["scenes"][1]["graphic"] = dict(mark)
        cli.use_picture_from(Path(d), st, 1, 0)
        assert st["short"]["scenes"][1]["graphic"] is None
        review.paint_new(Path(d), st, 0)
        assert st["short"]["scenes"][0]["graphic"] == date  # other graphics don't depend on the picture


GOOD_TSX = """import React from 'react';
import {Card, Connect, CustomFull, FullProps, Paper, TitleBanner, cueAt, focusCam, layoutColumn} from '../toolkit';
export const Custom0: React.FC<FullProps<CustomFull>> = ({full, t, start, end}) => {
	const b = layoutColumn(2);
	return (
		<Paper t={t} start={start} seed={full.seed} cam={focusCam(540, 630, 1)} skin={full.skin}>
			<TitleBanner title={full.title || 'X'} t={t} at={start} skin={full.skin} />
			<Card box={b[0]} title="a" t={t} at={cueAt(full, 0, start, end, 2)} />
			<Connect from={b[0]} to={b[1]} avoid={b} t={t} at={start + 1} />
		</Paper>
	);
};
"""


def test_lint_custom_code():
    assert motion.lint_custom_code(GOOD_TSX) == []
    bad = [GOOD_TSX.replace("'../toolkit'", "'../Paper'"),  # imports from elsewhere
           GOOD_TSX.replace("<Connect from={b[0]} to={b[1]} avoid={b} t={t} at={start + 1} />",
                            "<FlowArrow x1={1} y1={2} x2={3} y2={4} t={t} at={start} />"),  # hand-placed arrow
           GOOD_TSX.replace("<Card box={b[0]}", "<FlowCard x={540} y={400}"),  # card that can grow and overlap
           GOOD_TSX.replace("<Paper t={t}", "<Paper style={{transition: 'all 1s'}} t={t}"),  # CSS animation
           GOOD_TSX.replace("<TitleBanner title={full.title || 'X'} t={t} at={start} skin={full.skin} />", ""),
           GOOD_TSX.replace("const b = layoutColumn(2);", "const b = layoutColumn(2); const h = <marker id='x' />;")]
    for code in bad:
        assert motion.lint_custom_code(code), code[:200]


def test_fallback_custom_is_clean():
    code = motion.fallback_custom_tsx(2, "San Diego hired Hatfield, then the dam burst, and he was never paid.", "rain deal")
    assert motion.lint_custom_code(code) == [] and "export const Custom2" in code


def test_look_check_fixes_code():
    with tempfile.TemporaryDirectory() as d:
        work = Path(d)
        sheet = work / "look" / "sheet.jpg"
        sheet.parent.mkdir()
        Image.new("RGB", (10, 10)).save(sheet)
        asked = []

        def ask(prompt, fatal=True, read_dir=None, brain=None, bulk=False):
            asked.append((prompt, read_dir))
            return {"ok": False, "problems": ["the stamp covers card 3"], "code": GOOD_TSX}

        saved = llm.ask_ai, motion.tsc_check, motion.preview_custom
        llm.ask_ai, motion.tsc_check, motion.preview_custom = ask, (lambda: None), (lambda short, sc, slot, work: sheet)
        try:
            fixed = motion.look_and_fix({"title": "T", "palette": "gold"}, {"start": 0, "end": 5, "full": {}}, 0, GOOD_TSX.replace("'X'", "'Y'"), work)
            assert fixed == GOOD_TSX and asked[0][1] == sheet.parent and "the stage" in asked[0][0].lower()
            llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: {"ok": True}
            assert motion.look_and_fix({"title": "T", "palette": "gold"}, {"start": 0, "end": 5, "full": {}}, 0, "CODE", work) == "CODE"
            llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: {"ok": False, "code": GOOD_TSX.replace("'../toolkit'", "'fs'")}
            assert motion.look_and_fix({"title": "T", "palette": "gold"}, {"start": 0, "end": 5, "full": {}}, 0, "CODE", work) == "CODE"  # a rule-breaking fix is refused
            motion.preview_custom = lambda short, sc, slot, work: None  # preview failed: nothing to look at, code unchanged
            assert motion.look_and_fix({"title": "T", "palette": "gold"}, {"start": 0, "end": 5, "full": {}}, 0, "CODE", work) == "CODE"
        finally:
            llm.ask_ai, motion.tsc_check, motion.preview_custom = saved


def test_short_credit():
    """On-screen credit tags are short (Emu War review: the long tag covered the emus and was cut mid-name)."""
    sc = image_sources.short_credit
    assert sc("Eduardo Mariz from Sydney, Australia, CC BY 2.0") == "Photo: E. Mariz · CC BY 2.0"
    assert sc("Jim Bendon from Karratha, Australia, CC BY-SA 2.0") == "Photo: J. Bendon · CC BY-SA 2.0"
    assert sc("Blue Mountains Library, Local Studies, CC BY-SA 2.0") == "Photo: Blue Mountains Library · CC BY-SA 2.0"
    assert sc("Disrupt", film=True) == "Video: Disrupt"
    assert sc("Bernard DUPONT from FRANCE, CC BY-SA 2.0") == "Photo: B. DUPONT · CC BY-SA 2.0"
    long = sc("The International Society for the Preservation of Very Old Photographs, CC BY 4.0")
    assert len(long) <= 44 and long.endswith("· CC BY 4.0") and "…" not in long  # whole words only
    assert sc("Wikimedia user Xyz123") == "Photo: Wikimedia user Xyz123"
    # Mike the Headless Chicken: the Commons author field was two links, shown raw on screen
    assert sc("http://www.miketheheadlesschicken.org/ https://www.life, Fair use") == "Photo: miketheheadlesschicken.org"


def test_local_job_retries_a_hard_crash():
    """Mike the Headless Chicken, fix round 3: the LTX worker died without writing results; the same job then worked."""
    import json
    import subprocess
    calls = []

    def fake_run(cmd, **kw):
        calls.append(cmd)
        job = Path(cmd[-1])
        if len(calls) == 2:  # second try: the worker finishes and writes its results
            data = json.loads(job.read_text(encoding="utf-8"))
            data["items"][0]["ok"], data["seconds"] = True, 1.0
            job.write_text(json.dumps(data), encoding="utf-8")
        return subprocess.CompletedProcess(cmd, 3221225477 if len(calls) == 1 else 0, "", "boom")

    real = subprocess.run
    subprocess.run = fake_run
    try:
        with tempfile.TemporaryDirectory() as d:
            items = gpu.local_job("video", [{"out": "x.mp4"}], Path(d), 60)
    finally:
        subprocess.run = real
    assert len(calls) == 2 and items[0]["ok"]


def test_music_gain_evens_out_tracks():
    """Mike's Thinking Music (-22 LUFS) vanished under the voice with the old fixed volume: quiet and loud tracks now
    end up at the same level (MUSIC_LUFS)."""
    import math
    import subprocess
    with tempfile.TemporaryDirectory() as d:
        gains = []
        for name, vol in (("quiet.wav", 1.0), ("loud.wav", 4.0)):  # 12 dB apart (lavfi's sine is -18 dBFS)
            p = Path(d) / name
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"sine=frequency=440:duration=5",
                            "-af", f"volume={vol}", str(p)], check=True)
            gains.append(audio_mix.music_gain(p))
        assert abs(20 * math.log10(gains[0] / gains[1]) - 12.04) < 0.3
        assert audio_mix.music_gain(Path(d) / "missing.mp3") == 0.22


def test_ink_silhouette():
    """A painted figure (black ink on white) becomes a cropped, transparent silhouette; a bad painting is refused."""
    with tempfile.TemporaryDirectory() as d:
        src, dst = Path(d) / "raw.jpg", Path(d) / "fig.png"
        img = Image.new("RGB", (1024, 1024), (250, 248, 240))
        from PIL import ImageDraw
        ImageDraw.Draw(img).ellipse((400, 300, 650, 800), fill=(15, 12, 10))  # a dark blob = the figure
        img.save(src)
        assert remotion_render.ink_silhouette(src, dst)
        with Image.open(dst) as f:
            assert f.mode == "RGBA" and max(f.size) <= 256
            assert f.getpixel((0, 0))[3] == 0  # the paper became transparent
            assert f.getpixel((f.width // 2, f.height // 2))[3] == 255  # the figure stayed solid
            assert abs(f.width / f.height - 250 / 500) < 0.1  # cropped to the figure
        Image.new("RGB", (1024, 1024), (250, 248, 240)).save(src)  # blank painting
        assert not remotion_render.ink_silhouette(src, dst)
        Image.new("RGB", (1024, 1024), (10, 10, 10)).save(src)  # all ink: no shape
        assert not remotion_render.ink_silhouette(src, dst)


def test_clean_full_keeps_thing():
    f = plan_rules.clean_full({"type": "number", "value": 20000, "label": "emus", "icon": "bird", "each": 1000, "thing": " Emu "}, SAID)
    assert f["thing"] == "emu" and f["icon"] == "bird"
    f = plan_rules.clean_full({"type": "number", "value": 20000, "label": "emus", "thing": "<script>x" * 9}, SAID)
    assert "thing" not in f  # only plain words
    assert all(i in config.ICONS for i in ("bird", "fish", "insect", "rat", "horse", "car", "plane", "gun", "barrel", "dollar"))


def test_full_props_figure():
    with tempfile.TemporaryDirectory() as d:
        work, job = Path(d) / "work", Path(d) / "job"
        work.mkdir()
        job.mkdir()
        Image.new("RGBA", (100, 200), (0, 0, 0, 255)).save(work / "fig2.png")
        sc = {"full": {"type": "number", "value": 20000, "show": "20,000", "label": "EMUS", "icon": "bird", "each": 1000,
                       "figures": 20, "thing": "emu", "figure": str(work / "fig2.png")}}
        p = motion.full_props(sc, {"full": {"at": 1.0}}, 2, None, job)
        assert p["image"] == "job/fig2.png" and (job / "fig2.png").exists() and "figure" not in p
        sc["full"]["figure"] = str(work / "missing.png")  # painting failed: the built-in icon is used
        assert "image" not in motion.full_props(sc, {"full": {"at": 1.0}}, 2, None, job)
        assert "painted" in motion.full_summary({**sc["full"], "figure": str(work / "fig2.png")})


def test_clean_sound():
    said = plan_rules.words_of("At a dam, over a thousand emus approached. The gun jammed after just twelve kills.")
    assert audio_mix.clean_sound({"word": "jammed", "sound": "Gun cock!"}, said) == {"word": "jammed", "sound": "gun cock"}
    assert audio_mix.clean_sound({"word": "exploded", "sound": "explosion"}, said) is None  # word never spoken
    assert audio_mix.clean_sound({"word": "jammed", "sound": "x" * 60}, said) is None
    assert audio_mix.clean_sound("gun", said) is None
    scenes = [{"sound": {"word": "a", "sound": "bell"}} for _ in range(5)]
    audio_mix.limit_sounds(scenes)
    assert sum(1 for sc in scenes if sc["sound"]) == config.MAX_STORY_SOUNDS == 3


def _tone_wav(seconds=0.6) -> bytes:
    import io
    import math
    import wave
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(44100)
        frames = [0] * 4410 + [int(12000 * math.sin(2 * math.pi * 900 * k / 44100)) for k in range(int(44100 * seconds))]
        w.writeframes(b"".join(v.to_bytes(2, "little", signed=True) for v in frames))
    return buf.getvalue()


def test_story_sound_library():
    with tempfile.TemporaryDirectory() as d:
        lib = Path(d)
        fetched = []

        def fetch(name):
            fetched.append(name)
            return (_tone_wav(), {"id": 182234, "name": "gun cock slow.wav", "license": "Creative Commons 0"})

        path = audio_mix.story_sound("gun cock", lib, fetch)
        assert path == lib / "gun_cock.wav" and path.exists() and fetched == ["gun cock"]
        assert "182234" in (lib / "gun_cock.txt").read_text(encoding="utf-8")  # where it came from
        assert audio_mix.story_sound("gun cock", lib, fetch) == path and len(fetched) == 1  # saved: fetched only once
        own = lib / "ship_horn.mp3"
        own.write_bytes(b"owner's file")
        assert audio_mix.story_sound("ship horn", lib, fetch) == own and len(fetched) == 1  # the owner's file wins
        assert audio_mix.story_sound("bell", lib, lambda name: None) is None  # nothing found: no sound, no crash


def test_story_sound_wins_its_moment():
    scenes = [{"transition": "fade", "graphic": None, "full": None, "sound": None},
              {"transition": "fade", "graphic": {"style": "fact", "text": "GUN JAMMED"}, "full": None,
               "sound": {"word": "jammed", "sound": "gun cock", "file": "story/gun_cock"}}]
    cues = [{}, {"graphic": 7.0, "sound_at": 7.1}]
    random.seed(3)
    ev = audio_mix.sfx_events({"scenes": scenes}, cues, [0, 5, 10], True)
    kinds = [(e["sound"], e["t"]) for e in ev]
    assert ("story/gun_cock", 7.1) in kinds
    assert not any(s.startswith("stamp") and abs(t - 7.1) < 0.5 for s, t in kinds)  # the stamp gives way


def test_counter_finishes_before_it_leaves():
    # Ghost Army: "fifteen" spoken 0.4 s before the scene ended, so the 15 MILES counter left at 13
    words = [(0.0, 0.5, "That"), (0.5, 1.0, "rumble"), (1.0, 2.5, "carried"), (2.6, 3.0, "fifteen"), (3.0, 3.6, "miles")]
    sc = {"graphic": {"style": "stat", "text": "MILES", "value": 15, "trigger": "fifteen"},
          "emphasis": None, "person": None}
    at = editplan.scene_cues(sc, words, 10.0, 14.0, 4, None)["graphic"]
    assert at + editplan.GRAPHIC_BUILD["stat"] + 0.87 <= 14.0  # counted up, held, then the exit
    sc["graphic"] = {"style": "fact", "text": "FAKE", "trigger": "fifteen"}
    assert editplan.scene_cues(sc, words, 10.0, 14.0, 4, None)["graphic"] == 12.5  # a plain callout still waits for its word


def test_fill_money_graphics_and_caps():
    from shortsmaker import frame_render
    scenes = [
        {"narration": "Two brothers made $800 million from a dead team.", "graphic": None, "full": None, "person": None},
        {"narration": "Each surviving owner had to pay $3.3 million.", "graphic": None, "full": None, "person": None},
        {"narration": "Wait, the league offered them $2.2 million to fold.", "graphic": None, "full": None, "person": None},
        {"narration": "In year one, the check was $521,749,", "graphic": None, "full": None, "person": None},
        {"narration": "but by 2010, TV deals sent $17.45 million yearly.", "graphic": None, "full": None, "person": None},
    ]
    plan_rules.fill_money_graphics(scenes)
    assert scenes[0]["graphic"] is None  # hook keeps its title
    assert scenes[1]["graphic"]["style"] == "compare" and scenes[1]["graphic"]["b_show"] == "$3.3M"
    assert scenes[2]["graphic"]["style"] == "compare" and scenes[2]["graphic"]["a_show"] == "$3.3M" and scenes[2]["graphic"]["b_show"] == "$2.2M"
    assert scenes[3]["graphic"]["style"] == "compare" and scenes[3]["graphic"]["b_show"] == "$521,749"
    assert scenes[4]["graphic"]["style"] == "compare" and scenes[4]["graphic"]["a_label"] == "YEAR 1" and scenes[4]["graphic"]["b_label"] == "2010"
    assert scenes[4]["graphic"]["b_show"] == "$17.45M"
    # AI-painted human subjects lower the callout so it doesn't cover faces
    assert frame_render.graphic_low({"subject_y": None, "bg": None}, Path("missing.jpg"), None,
                                    {"shot": "MEDIUM: two brothers standing", "ai_image": "two men in suits"}) is True
    assert frame_render.graphic_low({"subject_y": None, "bg": None}, Path("missing.jpg"), None,
                                    {"shot": "CLOSE-UP: stack of broadcast tapes", "ai_image": "magnetic tape reels"}) is False
    # Falling numbers mark stat direction='down' so StatCard counts down instead of up from 0
    g = plan_rules.clean_graphic({"style": "stat", "text": "SHARE PRICE", "value": 39, "trigger": "$39"},
                                 plan_rules.words_of("pushing the share price down to $39."))
    assert g and g.get("direction") == "down"
    g_up = plan_rules.clean_graphic({"style": "stat", "text": "DIVIDEND %", "value": 11, "trigger": "11%"},
                                    plan_rules.words_of("So his 1,267 stores paid an 11% dividend."))
    assert g_up and "direction" not in g_up
    # Portrait-on-portrait detection filters solo portraits of the PersonCard subject from background candidates
    cat = [{"n": 1, "what": "Portrait of Clarence Saunders"}, {"n": 2, "what": "Piggly Wiggly grocery store interior"}]
    assert plan_rules.is_person_portrait({"title": "File:Clarence Saunders.jpg"}, "Clarence Saunders", cat, 1) is True
    assert plan_rules.is_person_portrait({"title": "File:Clarence Saunders LCCN2014715807.jpg"}, "Clarence Saunders", cat, 1) is True
    assert plan_rules.is_person_portrait({"title": "File:Interior of Piggly Wiggly store.jpg"}, "Clarence Saunders", cat, 2) is False
    # Loop bridge detection
    assert plan_rules.is_loop_short([{"narration": "One grocer borrowed $10 million."},
                                     {"narration": "so Saunders lost $9 million, all because"}]) is True
    assert plan_rules.is_loop_short([{"narration": "A passenger looked out."},
                                     {"narration": "and half a bottle of beer every week."}]) is False
    # Glass-plate negative mount border trimming (noisy outer negative strip + flat inner mount border)
    from shortsmaker import photo_prep
    im = Image.new("RGB", (400, 400), (120, 110, 100))
    for y in range(400):
        for x in range(400):
            if 20 <= x < 380 and 20 <= y < 380:
                im.putpixel((x, y), ((x * 7 + y * 13) % 200 + 30, (x * 5 + y * 11) % 200 + 30, (x * 3 + y * 17) % 200 + 30))
            elif 6 <= x < 20 or 380 <= x < 394 or 6 <= y < 20 or 380 <= y < 394:
                im.putpixel((x, y), (20, 20, 20))  # flat inner mount border
            else:
                im.putpixel((x, y), ((x * 37 + y * 19) % 255, (x * 37 + y * 19) % 255, (x * 37 + y * 19) % 255))  # noisy outer negative edge
    trimmed = photo_prep.trim_borders(im)
    assert trimmed.size == (360, 360)



def test_model_graphic():
    """The three.js model graphic (2026-10-28): motion-graphic openers only, its model found before it is planned
    (a thing no library has is asked for once more), its credit kept, its headline after the model lands."""
    from shortsmaker import opener_render
    m = {"type": "model", "find": "Eiffel Tower", "label": "sold for scrap", "note": "1925"}
    assert plan_rules.clean_full(dict(m), []) is None  # never a slideshow scene
    f = plan_rules.clean_full(dict(m), [], opener=True)
    assert f == {"type": "model", "find": "Eiffel Tower", "label": "SOLD FOR SCRAP", "note": "1925"}, f
    assert plan_rules.clean_full({"type": "model", "find": "tower"}, [], opener=True) is None  # no headline
    assert plan_rules.full_cues(f, [], 0.0, 3.0) == {"at": 0.55, "noteAt": 1.05}
    assert motion.full_summary(f) == '3D model: Eiffel Tower under "SOLD FOR SCRAP", 1925'
    short = {"title": "T", "research": {"A": "text"},
             "scenes": [{"narration": "A con man sold the Eiffel Tower.", "full": None, "graphic": None, "person": None}]}
    saved = (llm.ask_ai, opener_render.model_for)
    prompts, finds = [], []
    replies = iter([{"full": {**m, "find": "eiffel tower made of gold"}, "why": "a"}, {"full": dict(m), "why": "the tower itself"}])
    llm.ask_ai = lambda prompt, **k: prompts.append(prompt) or next(replies)
    lib = config.ROOT / "tests" / "fixtures" / "openers" / "polypizza_6NTegstc5Jy.blend"  # a CC-BY model
    opener_render.model_for = lambda find: finds.append(find) or ((lib, None) if find == "Eiffel Tower" else (None, f"no 3D model of '{find}'"))
    try:
        note = picker.opener_graphic(short)
    finally:
        llm.ask_ai, opener_render.model_for = saved
    full = short["scenes"][0]["full"]
    assert note.endswith("(the tower itself)") and full["model"] == str(lib) and "Rooster" in full["credit"], (note, full)
    assert '"type": "model"' in prompts[0] and "no 3D model of 'eiffel tower made of gold'" in prompts[1], prompts[1][-600:]
    with tempfile.TemporaryDirectory() as d:  # the props: the model as job/model0.glb, no file paths or credit
        saved = opener_render.to_glb
        glb = Path(d) / "m.glb"
        glb.write_bytes(b"glb")
        opener_render.to_glb = lambda blend: glb
        try:
            props = motion.full_props(short["scenes"][0], {"full": {"at": 0.55, "noteAt": 1.05}}, 0, None, Path(d))
        finally:
            opener_render.to_glb = saved
        assert props["src"] == "job/model0.glb" and (Path(d) / "model0.glb").exists()
        assert "model" not in props and "credit" not in props and "find" not in props and props["at"] == 0.55


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

