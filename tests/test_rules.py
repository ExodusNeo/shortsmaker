"""Tests for per-channel rules files (channels/<name>.rules.md, 2026-10-22). The golden test proves the move left
strange-history's prompts word for word the same. No AI usage, no GPU.
Run: .venv\\Scripts\\python.exe tests\\test_rules.py   (--save-golden rewrites tests/golden/prompts.json)"""
import json
import sys
import tempfile
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from shortsmaker import (  # noqa: E402
    channel_profiles, llm, logbook, media_tools, picture_pool, review, rules, session, style_lab, writing,
)

# a frozen copy of the strange-history profile: the live file's done_topics grow with every run
CH = {
    "niche": "Strange-but-true history: short, surprising stories about real people, places, inventions and events "
             "from history, each built around one hook and a twist ending (avoiding graphic violence and anything political)",
    "audience": "Curious viewers aged 18 to 45, mainly in the US, UK, Canada and Australia",
    "tone": "Like a friend telling a gripping story at a bar",
    "voice": "en-US-AndrewNeural", "cta_line": "for more strange history",
    "done_topics": ["The 1911 theft of the Mona Lisa", "The 1835 Great Moon Hoax"],
    "recent_shapes": ["rise and fall"], "myths": ["The Cardiff Giant: not true as told"],
}
LINES = ["A passenger looked out the train window", "and saw a baboon working the railway signals.",
         "He complained, so the railway sent officials to investigate.", "But the baboon had a very good reason to be there.",
         "You see, the signalman, James Wide,", "had lost both legs in a fall between two train cars.",
         "So he bought a baboon named Jack", "and taught him the code: so many whistles, that lever.",
         "The officials didn't fire Jack. They gave him an exam.", "Whistle after whistle, he never pulled a wrong lever.",
         "So the railway hired him: twenty cents a day", "and half a bottle of beer every week."]
REPLIES = {  # canned AI replies, chosen by the prompt's opening words
    "You choose stories": {"shorts": [{"topic": "Jack the baboon signalman", "character": "Jack the baboon",
                                       "subject": "Jack (baboon)", "wiki_articles": ["Jack (baboon)"],
                                       "search_terms": ["baboon signalman"], "visual_terms": ["Jack baboon"],
                                       "people": ["James Wide"]}]},
    "You write YouTube Shorts narration": {"shorts": [{"index": 0, "shape": "one person against the odds",
                                                       "title": "The Baboon Who Worked the Railway",
                                                       "hook_options": ["a", "b", "c"], "hook_text": "NOBODY FIRED HIM",
                                                       "thumbnail_text": "BABOON SIGNALMAN", "scenes": LINES}]},
    "You are the script editor": {},
    "You are the director": {"shorts": [{"index": 0, "scenes": [{} for _ in LINES]}]},
    "You are a strict fact-checker": {"story_holds": True, "fixes": []},
    "You are the picture researcher": {"pictures": [{"n": 1, "what": "Jack at the levers", "era_ok": True, "sharp": 3,
                                                     "hook": False, "reject": None}]},
    "You judge the first two seconds": {"score": 8, "why": "strong", "open_with_scene": None},
    "Some AI paintings": {"prompts": []},
}
KEYS = {"You choose stories": "topics", "You write YouTube Shorts narration": "writer",
        "You are the script editor": "editor", "You are the director": "director",
        "You are a strict fact-checker": "fact_check", "You are the picture researcher": "picture_list",
        "You judge the first two seconds": "first_second", "Some AI paintings": "repaint"}


def capture_prompts() -> dict[str, str]:
    """Every prompt strange-history's writer, editor, director, fact check, picture list, first-second check and
    repaint send, with the AI and everything outside the prompts faked."""
    rules.load_rules("strange-history")
    got: dict[str, str] = {}
    tmp = tempfile.mkdtemp()

    def ask(prompt, fatal=True, read_dir=None, brain=None, bulk=False):
        start = next(k for k in REPLIES if prompt.startswith(k))
        got.setdefault(KEYS[start], prompt.replace(tmp, "<TMP>").replace(tmp.replace("\\", "/"), "<TMP>"))
        return json.loads(json.dumps(REPLIES[start]))

    def prepare(s, folder=None):
        s.update(_texts={"Jack (baboon)": "Jack was a chacma baboon."}, catalog=[], pool_dir=None, picture_check="9 usable of 9")
        return True

    saved = (llm.ask_ai, channel_profiles.trend_research, logbook.logbook_results, picture_pool.prepare_topic,
             style_lab.style_library, picture_pool.contact_sheets, media_tools.ffmpeg)
    llm.ask_ai = ask
    channel_profiles.trend_research = lambda ch: [{"title": "T", "views": 1000, "channel": "C"}]
    logbook.logbook_results = lambda: "- Example Short | 1,000 views"
    picture_pool.prepare_topic = prepare
    style_lab.style_library = lambda kind=None: [{"name": "silent", "kind": "look", "description": "silent film", "fits": "old stories"}]
    picture_pool.contact_sheets = lambda cands, folder: [Path(tmp) / "sheet1.jpg"]
    media_tools.ffmpeg = lambda *a, cwd: (Path(cwd) / a[-1]).write_bytes(b"jpg")
    try:
        writing.write_scripts(json.loads(json.dumps(CH)), 1)
        picture_pool.catalog_pool({"topic": "Jack the baboon signalman", "subject": "Jack (baboon)"},
                                  [{"title": "File:Jack.jpg", "source": "Commons"}], Path(tmp) / "pool")
        board = Path(tmp) / "storyboard.jpg"
        board.write_bytes(b"jpg")
        scenes = [{"narration": t, "animate": False, "full": None, "graphic": None, "shot": "WIDE", "ai_image": "a painting"}
                  for t in LINES[:4]]
        choices = [{"bg": (b"jpg", f"File:{k}.jpg", "Someone"), "person": None, "film": None} for k in range(4)]
        short = {"title": "The Baboon Who Worked the Railway", "topic": "Jack the baboon signalman", "scenes": scenes}
        review.first_second_check(Path(tmp) / "short.mp4", short, choices, board, Path(tmp))
        review.rewrite_paint_prompts(short, {2: "garbled sign"})
    finally:
        (llm.ask_ai, channel_profiles.trend_research, logbook.logbook_results, picture_pool.prepare_topic,
         style_lab.style_library, picture_pool.contact_sheets, media_tools.ffmpeg) = saved
    return got


LABEL = "channels/x.rules.md"


def make(**override) -> str:
    """A valid rules file; override={"Directing": None} leaves that heading out, a string replaces its text."""
    body = {h: f"{h.lower()} text" for h in rules.REQUIRED}
    body["Settings"] = "status: ready\nvisuals: photos\nmin_real_pictures: 6"
    body.update({k.replace("_", " "): v for k, v in override.items()})
    return "".join(f"## {h}\n{t}\n\n" for h, t in body.items() if t is not None)


def stop_text(text: str) -> str:
    try:
        rules.parse_rules(text, LABEL)
    except SystemExit as e:
        return str(e)
    return "no stop"


def test_parses_sections_and_settings():
    sections, settings = rules.parse_rules(make(Story_rules="story text"), LABEL)
    assert sections["Story rules"] == "story text"
    assert settings == {"status": "ready", "visuals": "photos", "min_real_pictures": "6"}


def test_strips_tag_comments():
    sections, _ = rules.parse_rules(make(Directing="<!-- copied from strange-history -->\nX"), LABEL)
    assert sections["Directing"] == "X"


def test_bom_and_crlf_load_the_same():
    text = make(Story_rules="line one\nline two")
    assert rules.parse_rules("﻿" + text.replace("\n", "\r\n"), LABEL) == rules.parse_rules(text, LABEL)


def test_heading_case_and_spaces():
    text = make(Story_rules=None) + "##  story RULES \nmine\n"
    assert rules.parse_rules(text, LABEL)[0]["Story rules"] == "mine"


def test_level3_heading_stays_inside():
    sections, _ = rules.parse_rules(make(Story_rules="intro\n### Examples\nan example"), LABEL)
    assert sections["Story rules"] == "intro\n### Examples\nan example"


def test_missing_heading_stops():
    assert stop_text(make(Directing=None)) == 'Stopped: channels/x.rules.md has no "## Directing" section.'


def test_empty_heading_stops():
    assert stop_text(make(Directing="<!-- new -->\n\n")) == 'Stopped: channels/x.rules.md has no "## Directing" section.'


def test_duplicate_heading_stops():
    assert stop_text(make() + "## Directing\nagain\n") == 'Stopped: channels/x.rules.md has "## Directing" twice.'


def test_draft_stops():
    assert stop_text(make(Settings="status: Draft\nvisuals: photos\nmin_real_pictures: 6")) == (
        'Stopped: channels/x.rules.md is a draft. Read it, edit anything you want, then change "status: draft" to '
        '"status: ready".')


def test_blender_stops():
    assert stop_text(make(Settings="status: ready\nvisuals: blender\nmin_real_pictures: 6")) == (
        "Stopped: channels/x.rules.md asks for Blender visuals, which aren't built yet.")


def test_bad_min_pictures_stops():
    assert stop_text(make(Settings="status: ready\nvisuals: photos\nmin_real_pictures: six")) == (
        "Stopped: channels/x.rules.md: min_real_pictures must be a whole number.")


def test_load_rules_sets_session():
    with tempfile.TemporaryDirectory() as d:
        old = rules.CHANNELS
        rules.CHANNELS = Path(d)
        try:
            (Path(d) / "x.rules.md").write_text(make(Topic_picking="pick well", Settings="status: ready\nvisuals: photos\nmin_real_pictures:  4 "), encoding="utf-8")
            rules.load_rules("x")
            assert session.RULES["Topic picking"] == "pick well"
            assert rules.min_real_pictures() == 4
        finally:
            rules.CHANNELS = old


def test_min_pictures_from_settings():
    cands = [{"title": f"File:{k}.jpg", "source": "Commons", "url": f"u{k}"} for k in (1, 2)]
    entries = [{"n": k, "what": "x", "era_ok": True, "sharp": 2, "hook": False, "reject": None} for k in (1, 2)]
    saved = writing.article_text, picture_pool.load_pool, picture_pool.catalog_pool, dict(session.RULE_SETTINGS)
    writing.article_text = lambda t: ""
    picture_pool.load_pool = lambda folder: cands
    picture_pool.catalog_pool = lambda s, c, folder: entries
    try:
        for need, ok in (("2", True), ("3", False)):
            session.RULE_SETTINGS = {"min_real_pictures": need}
            s = {"topic": "t", "wiki_articles": ["A"]}
            assert picture_pool.prepare_topic(s, Path(tempfile.mkdtemp())) is ok, need
    finally:
        writing.article_text, picture_pool.load_pool, picture_pool.catalog_pool, session.RULE_SETTINGS = saved


def draft_reply(missing=None, **extra):
    sections = {h: {"tag": "copied from strange-history" if h == "Story rules" else "new", "text": f"{h} for engines"}
                for h in rules.REQUIRED if h not in ("Settings", missing)}
    return {"visuals": "photos", "min_real_pictures": 3, "sections": sections, **extra}


def run_draft(replies, existing=None):
    """draft_rules in a temp channels folder holding strange-history's rules; returns (file text or None, calls)."""
    calls = []

    def ask(prompt, fatal=True, read_dir=None, brain=None, bulk=False):
        calls.append(prompt)
        return replies[min(len(calls), len(replies)) - 1]

    with tempfile.TemporaryDirectory() as d:
        old, old_ask = rules.CHANNELS, llm.ask_ai
        rules.CHANNELS, llm.ask_ai = Path(d), ask
        (Path(d) / "strange-history.rules.md").write_text(make(Story_rules="hook first"), encoding="utf-8")
        if existing is not None:
            (Path(d) / "engines.rules.md").write_text(existing, encoding="utf-8")
        try:
            try:
                rules.draft_rules({"niche": "engines", "audience": "a", "tone": "t"}, "engines")
            except SystemExit as e:
                calls.append(f"STOP {e}")
            path = Path(d) / "engines.rules.md"
            return (path.read_text(encoding="utf-8") if path.exists() else None), calls
        finally:
            rules.CHANNELS, llm.ask_ai = old, old_ask


def test_draft_writes_tagged_draft_file():
    text, calls = run_draft([draft_reply()])
    assert "status: draft" in text and "<!-- copied from strange-history -->" in text and "<!-- new -->" in text
    assert "hook first" in calls[0] and "engines" in calls[0]  # the AI sees the existing rules and the new niche
    assert stop_text(text).startswith("Stopped: channels/x.rules.md is a draft.")
    sections, _ = rules.parse_rules(text.replace("status: draft", "status: ready"), LABEL)
    assert sections["Story rules"] == "Story rules for engines" and "min_real_pictures: 3" in text


def test_draft_settings_come_from_code():
    text, _ = run_draft([draft_reply(status="ready", min_real_pictures="lots", visuals="video")])
    assert "status: draft" in text and "min_real_pictures: 6" in text and "visuals: photos" in text


def test_draft_retries_once_then_stops():
    text, calls = run_draft([draft_reply(missing="Directing"), draft_reply(missing="Directing")])
    assert text is None and len(calls) == 3 and "Directing" in calls[-1], calls[-1]
    assert calls[-1].startswith("STOP Stopped: couldn't draft rules for engines:")


def test_draft_never_overwrites():
    text, calls = run_draft([draft_reply()], existing="mine")
    assert text == "mine" and calls == ["STOP Stopped: channels/engines.rules.md already exists."]


def test_new_channel_stops_for_review():
    import builtins
    saved = builtins.input, channel_profiles.new_channel, rules.draft_rules, channel_profiles.use_channel
    names = sorted(p.stem for p in channel_profiles.CHANNELS.glob("*.json") if not p.stem.endswith(".research"))
    answers = iter([str(len(names) + 1), "engines", "jet engines"])  # "+ New channel" is the last menu number
    builtins.input = lambda q="": next(answers)
    channel_profiles.new_channel = lambda niche: {"niche": niche}
    rules.draft_rules = lambda ch, name: Path(f"{name}.rules.md")
    channel_profiles.use_channel = lambda name: None
    try:
        channel_profiles.pick_channel()
        raise AssertionError("pick_channel returned instead of stopping")
    except SystemExit as e:
        assert str(e).startswith("Rules drafted: channels/engines.rules.md\n"), str(e)
    finally:
        builtins.input, channel_profiles.new_channel, rules.draft_rules, channel_profiles.use_channel = saved


def test_strange_history_prompts_unchanged():
    golden = json.loads((HERE / "golden" / "prompts.json").read_text(encoding="utf-8"))
    now = capture_prompts()
    assert sorted(now) == sorted(golden), sorted(now)
    for key, text in golden.items():
        assert " ".join(now[key].split()) == " ".join(text.split()), key


if __name__ == "__main__":
    if sys.argv[1:] == ["--save-golden"]:
        (HERE / "golden").mkdir(exist_ok=True)
        media_tools.write_json(HERE / "golden" / "prompts.json", capture_prompts())
        sys.exit(0)
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
