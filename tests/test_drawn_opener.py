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

EXAMPLE = (ROOT / "drawn" / "examples" / "dexter.mjs").read_text(encoding="utf-8")
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


def look():
    """Renders drawn/out/sheet.png: every kit part, one page per second (look at it after changing kit.mjs)."""
    out = ROOT / "drawn" / "out"
    out.mkdir(exist_ok=True)
    job = {"scene": str(ROOT / "drawn" / "examples" / "kit_parts.mjs"), "seconds": 6, "mode": "sheet",
           "times": [0.5, 1.5, 2.5, 3.5, 4.5, 5.5], "out": str(out), "name": "kit", "scale": 0.3}
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
