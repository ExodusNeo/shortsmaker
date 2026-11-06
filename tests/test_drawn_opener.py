"""Tests for the drawn opener (drawn_opener.py + drawn/, 2026-10-30): the lint on AI-written scenes, a draft that
passes its art director and renders with real node, a draft that keeps failing until the motion graphic takes over,
reuse on a re-render, and use_opener putting the clip on scene 1. The AI is faked; node and ffmpeg are real (~1 min).
Run: .venv\\Scripts\\python.exe tests\\test_drawn_opener.py   (--look renders drawn\\out\\sheet.png of every kit part)"""
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from PIL import Image  # noqa: E402

from shortsmaker import drawn_opener, llm, media_tools, session, short_render  # noqa: E402
from shortsmaker import opener3d  # noqa: E402

opener3d.available = lambda: "switched off: these tests are about the drawn opener (tests/test_opener3d.py covers 3D)"

EXAMPLE = (ROOT / "drawn" / "examples" / "umbrellas.mjs").read_text(encoding="utf-8")
WORDS = [(0.06, 0.2, "He"), (0.25, 0.6, "shipped"), (0.7, 1.0, "brass"), (1.05, 1.2, "bed"), (1.25, 1.6, "warmers"),
         (2.2, 2.7, "tropical"), (2.75, 3.4, "Caribbean")]


def short():
    return {"title": "How Rivals Accidentally Made Him Rich", "topic": "Timothy Dexter",
            "scenes": [{"narration": "He shipped brass bed warmers straight to the tropical Caribbean.", "full": None},
                       {"narration": "But local merchants set the trap to bankrupt him.", "full": None}]}


def test_no_verdict_is_not_a_pass():
    saved = llm.ask_ai
    llm.ask_ai = lambda *a, **k: None  # the art director's call failed
    try:
        assert drawn_opener.review(short(), {"moment": "m"}, Path("sheet") / "sheet1.png", 2.0) == (None, [])
    finally:
        llm.ask_ai = saved


def fake_ai(replies, prompts):
    it = iter(replies)
    return lambda prompt, **k: prompts.append(prompt) or next(it)


def test_lint():
    assert drawn_opener.lint(EXAMPLE) == []
    assert drawn_opener.lint('// this imports nothing\nexport default function scene(k, t) { k.text("Date: 1790", 1, 2); }') == []
    bad = drawn_opener.lint("export default function scene(k, t) { k.constructor; process.exit(); k.ctx.canvas; Math.random(); }")
    assert len(bad) == 4 and any("constructor" in b for b in bad) and any(".ctx" in b for b in bad), bad
    assert drawn_opener.lint('export default function scene(k, t) { k.text(`${require("fs")}`, 1, 2); }')  # template literals run
    assert drawn_opener.lint("function scene(k, t) {}") == ["missing `export default function scene(k, t)`"]


def test_kit_animals_must_be_used():
    moment = "Clever Hans taps a hoof while his owner stands aside"
    boxes = {"moment": moment.replace("Clever Hans", "the horse Hans"), "code": "k.shape(k.rect(1, 2, 3, 4), '#A7784D'); // k.horse( in a comment"}
    assert len(drawn_opener.missing_parts(boxes)) == 1 and "k.horse" in drawn_opener.missing_parts(boxes)[0]
    assert drawn_opener.missing_parts({"moment": "a stallion taps", "code": "const h = k.horse(560, 1600, 2, {tap: [1]});"}) == []
    assert drawn_opener.missing_parts({"moment": moment, "code": ""}) == []  # no animal word: nothing to require
    assert drawn_opener.missing_parts({"moment": moment, "code": ""}, "His owner wasn't asking, but this horse")  # the real case
    assert drawn_opener.missing_parts({"moment": "horseradish ships", "code": ""}) == []  # whole words only


def test_drawn_opener_renders_and_is_reused():
    """A draft that passes: coded, previewed (6 frames), approved, rendered as scene 1 + the crossfade; a second call
    (a fix round) reuses the clip without asking the AI."""
    saved, prompts = llm.ask_ai, []
    llm.ask_ai = fake_ai([{"moment": "a ship of bed warmers sails into the tropics", "code": EXAMPLE}, {"score": 8, "problems": ["the sun is a bit flat"]}], prompts)
    try:
        with tempfile.TemporaryDirectory() as d:
            s = short()
            clip, why = drawn_opener.make_opener(s, WORDS, 3.5, Path(d))
            assert clip and why is None and clip.exists(), why
            assert abs(media_tools.duration(clip) - 3.8) < 0.1, media_tools.duration(clip)
            assert s["drawn"]["moment"].startswith("a ship") and "brass 0.70s" in prompts[0] and "KIT" not in prompts[1]
            assert (Path(d) / "drawn" / "sheet1.png").exists() and "sheet1.png" in prompts[1]
            assert drawn_opener.make_opener(s, WORDS, 3.5, Path(d)) == (clip, None) and len(prompts) == 2  # reused
    finally:
        llm.ask_ai = saved


def test_drawn_opener_gives_up_after_fixes():
    """The art director scores every draft below PASS: FIXES rewrites (each told the problems), then the failure is kept and
    never retried for this Short. A crash and a lint break count as problems too."""
    saved, prompts = llm.ask_ai, []
    crash = EXAMPLE.replace("k.sky(", "k.nothing(")
    replies = [{"moment": "m", "code": crash},                                   # draft 1 crashes in node
               {"moment": "m", "code": EXAMPLE + "\nconst x = Math.random();"},  # draft 2 breaks the lint
               {"moment": "m", "code": EXAMPLE}, {"score": 5, "problems": ["the ship is too small"]}]
    llm.ask_ai = fake_ai(replies, prompts)
    try:
        with tempfile.TemporaryDirectory() as d:
            s = short()
            clip, why = drawn_opener.make_opener(s, WORDS, 3.5, Path(d))
            assert clip is None and "scored 5/10" in why and "the ship is too small" in why and s["drawn_failed"] == why, why
            assert "crashed when it ran" in prompts[1] and "k.nothing is not a function" in prompts[1], prompts[1][-800:]
            assert "Math.random" in prompts[2] and "Last draft" in prompts[2]
            assert len(prompts) == 4 and "drawn" not in s
            assert drawn_opener.make_opener(s, WORDS, 3.5, Path(d)) == (None, why) and len(prompts) == 4
    finally:
        llm.ask_ai = saved


def test_drawn_opener_stops_when_a_fix_does_not_help():
    """Two reviewed drafts and the second scored no better: no third draft (each one cost ~4-9 minutes, 2026-11-05)."""
    saved, prompts = llm.ask_ai, []
    replies = [{"moment": "m", "code": EXAMPLE}, {"score": 5, "problems": ["the ship is too small"]},
               {"moment": "m", "code": EXAMPLE}, {"score": 4, "problems": ["the ship is still small"]}]
    llm.ask_ai = fake_ai(replies, prompts)
    try:
        with tempfile.TemporaryDirectory() as d:
            clip, why = drawn_opener.make_opener(short(), WORDS, 3.5, Path(d))
            assert clip is None and "scored 4/10" in why and len(prompts) == 4, (why, len(prompts))
    finally:
        llm.ask_ai = saved


def test_neither_passes_so_the_best_draft_at_keep_is_used():
    """Owner, 2026-11-06: when neither the 3D nor the drawn opener reaches PASS, the better one is kept from KEEP (6).
    A draft that gives the answer away is never kept, however it scored; below KEEP the motion graphic takes over."""
    saved, prompts = llm.ask_ai, []
    spoil = {"score": 9, "reveals_answer": True, "answer_why": "the bankrupt sign", "problems": []}
    try:
        llm.ask_ai = fake_ai([{"moment": "m", "code": EXAMPLE}, {"score": 6, "problems": ["the ship is small"]},
                              {"moment": "m", "code": EXAMPLE}, {"score": 5, "problems": ["still small"]}], prompts)
        with tempfile.TemporaryDirectory() as d:
            s = {**short(), "opener3d_best": {"score": 5, "plan": {"kind": "3d", "moment": "3d"}}}
            clip, why = drawn_opener.make_opener(s, WORDS, 3.5, Path(d))
            assert clip and clip.exists() and why is None and s["drawn"]["kept"] == 6 and "kind" not in s["drawn"], why
        llm.ask_ai = fake_ai([{"moment": "m", "code": EXAMPLE}, spoil, {"moment": "m", "code": EXAMPLE}, spoil], [])
        with tempfile.TemporaryDirectory() as d:
            clip, why = drawn_opener.make_opener(short(), WORDS, 3.5, Path(d))  # the spoiler is capped at 6: still not kept
            assert clip is None and "reveals the answer" in why, why
        llm.ask_ai = fake_ai([{"moment": "m", "code": EXAMPLE}, {"score": 5, "problems": ["small"]},
                              {"moment": "m", "code": EXAMPLE}, {"score": 4, "problems": ["small"]}], [])
        with tempfile.TemporaryDirectory() as d:
            clip, why = drawn_opener.make_opener(short(), WORDS, 3.5, Path(d))
            assert clip is None and "scored 4/10" in why, why
    finally:
        llm.ask_ai = saved


def test_use_opener_plays_the_drawn_opener():
    """use_opener puts the drawn clip on scene 1 (its first frame as the still, no graphic, no photo credit tag);
    when it fails, the motion graphic plays and the Opening line says why."""
    saved = drawn_opener.make_opener
    with tempfile.TemporaryDirectory() as d:
        work = Path(d)
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=red:s=108x192:d=1", str(work / "o.mp4")], check=True)
        try:
            drawn_opener.make_opener = lambda s, words, secs, w: (s.update(drawn={"moment": "a ship of bed warmers"}) or (work / "o.mp4", None))
            s = short()
            s["opener_graphic"], s["scenes"][0]["full"] = "motion graphic: map journey", {"type": "journey"}
            clips, images, sources = {}, [Image.new("RGB", (8, 8))], ["photo"]
            assert short_render.use_opener(s, [0.0, 3.5], WORDS, work, clips, images, sources) is None
            assert clips[0] == work / "o.mp4" and images[0].size == (108, 192) and s["opener_used"]
            assert s["scenes"][0]["full"] is None and s["opening_note"] == "drawn opener: a ship of bed warmers"
            drawn_opener.make_opener = lambda s, words, secs, w: (None, "the ship is too small")
            s = short()
            s["opener_graphic"], s["scenes"][0]["full"] = "motion graphic: map journey", {"type": "journey"}
            assert short_render.use_opener(s, [0.0, 3.5], WORDS, work, {}, [None], ["photo"]) is None
            assert s["opening_note"] == "drawn opener failed (the ship is too small) -> motion graphic: map journey"
            assert not s["opener_used"] and s["scenes"][0]["full"]
        finally:
            drawn_opener.make_opener = saved


def test_reveal_scene_is_drawn_with_its_own_rules():
    """A reveal (one of the last two scenes) planned as a custom diagram is drawn: the coder gets PAYOFF_RULES and the
    story so far (not the opener's hook rules), the art director judges the reveal, words are timed from the scene's
    start, and the scene's diagram gives way to the clip. A re-render reuses the drawing; a fix-round repaint retires it."""
    saved_ask, saved_rules, prompts = llm.ask_ai, dict(session.RULE_SETTINGS), []
    llm.ask_ai = fake_ai([{"moment": "the questioner relaxes as the hoof stops", "code": EXAMPLE},
                          {"score": 8, "problems": []}], prompts)
    session.RULE_SETTINGS["opener"] = "animated"
    try:
        with tempfile.TemporaryDirectory() as d:
            work = Path(d)
            s = short()
            s["scenes"].append({"narration": "so their own bodies told Hans when to stop.", "full": {"type": "custom"}})
            bounds = [0.0, 3.5, 6.0, 9.0]
            words = WORDS + [(6.1, 6.4, "so"), (8.2, 8.6, "stop.")]
            clips, images, sources = {}, [None, None, Image.new("RGB", (8, 8))], ["a", "b", "custom diagram"]
            assert short_render.drawn_payoff(s, bounds, words, work, clips, images, sources) == [2]
            assert "This scene is the REVEAL" in prompts[0] and "OPEN INSIDE" not in prompts[0]
            assert "so 0.10s" in prompts[0] and "stop. 2.20s" in prompts[0]  # timed from the scene's start
            assert "The story the viewer has heard so far" in prompts[0] and "brass bed warmers" in prompts[0]
            assert "hand-drawn reveal (scene 3" in prompts[1] and "reveals_answer is false here" in prompts[1]
            assert clips[2] == work / "drawn_2" / "opener.mp4" and s["scenes"][2]["full"] is None
            assert sources[2].startswith("drawn reveal") and images[2].size != (8, 8) and "drawn" not in s
            clips = {}  # a fix round: the diagram is gone from the saved plan, the drawing is reused without the AI
            assert short_render.drawn_payoff(s, bounds, words, work, clips, images, sources) == [2] and len(prompts) == 2
            from shortsmaker import review
            state = {"short": s, "choices": [{"bg": None, "person": None}] * 3, "by_gemini": []}
            review.paint_new(work, state, 2)
            assert "drawn_2" not in s and short_render.drawn_payoff(s, bounds, words, work, {}, images, sources) == []
            mid = short()  # scene 2 of 5 isn't a reveal (no AI call); a channel without openers draws nothing
            mid["scenes"][1:1] = [{"narration": "x", "full": {"type": "custom"}}, {"narration": "y"}, {"narration": "z"}]
            assert short_render.drawn_payoff(mid, bounds + [10.0, 11.0], words, work, {}, images, sources) == []
            assert len(prompts) == 2
            session.RULE_SETTINGS["opener"] = None
            assert short_render.drawn_payoff(short(), bounds, words, work, {}, images, sources) == []
    finally:
        llm.ask_ai = saved_ask
        session.RULE_SETTINGS.clear()
        session.RULE_SETTINGS.update(saved_rules)


def look():
    """Renders drawn/out/sheet.png: every kit part, one page per second (look at it after changing kit.mjs)."""
    out = ROOT / "drawn" / "out"
    out.mkdir(exist_ok=True)
    job = {"scene": str(ROOT / "drawn" / "examples" / "kit_parts.mjs"), "seconds": 7, "mode": "sheet",
           "times": [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], "out": str(out), "name": "kit", "scale": 0.3}
    print(drawn_opener.node_run(job, out) or f"wrote {out / 'sheet.png'}")


if __name__ == "__main__":
    if sys.argv[1:] == ["--look"]:
        look()
        sys.exit(0)
    session.RULES = {**session.RULES}
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
