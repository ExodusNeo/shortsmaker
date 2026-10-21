"""Tests for the first-second check (would a scroller stop?) and the honest logbook lessons. No AI usage, no rendering.
Run: .venv\\Scripts\\python.exe tests\\test_first_second.py"""
import sys
import tempfile
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import llm, logbook, media_tools, review, session  # noqa: E402


def real(k):
    return (b"jpg", f"File:Photo {k}.jpg", "Someone")


def state(n=4):
    choices = [{"bg": real(k), "person": f"person{k}", "film": None} for k in range(n)]
    choices[2] = {"bg": None, "person": None, "film": None}  # scene 3 is an AI painting
    scenes = [{"narration": f"line {k}", "animate": True, "full": None, "graphic": None} for k in range(n)]
    return {"short": {"title": "Mike the Headless Chicken", "scenes": scenes}, "choices": choices, "by_gemini": []}


def run_check(reply, n=4):
    """first_second_check with ffmpeg and the AI faked; returns its result."""
    old_ff, old_ask = media_tools.ffmpeg, llm.ask_ai
    media_tools.ffmpeg = lambda *a, cwd: (Path(cwd) / a[-1]).write_bytes(b"jpg")
    llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: reply
    try:
        with tempfile.TemporaryDirectory() as d:
            board = Path(d) / "storyboard.jpg"
            board.write_bytes(b"jpg")
            st = state(n)
            return review.first_second_check(Path(d) / "short.mp4", st["short"], st["choices"], board, Path(d))
    finally:
        media_tools.ffmpeg, llm.ask_ai = old_ff, old_ask


def test_swap_pictures_trades_real_pictures():
    st = state()
    review.swap_pictures(st, 0, 3)
    assert st["choices"][0]["bg"] == real(3) and st["choices"][3]["bg"] == real(0)
    assert st["choices"][0]["person"] == "person0" and st["choices"][3]["person"] == "person3"  # name cards stay put
    assert st["short"]["scenes"][0]["animate"] is False and st["short"]["scenes"][3]["animate"] is False


def test_low_score_opens_on_a_better_real_picture():
    issues, opener = run_check({"score": 4, "why": "the picture shows the whole story", "open_with_scene": 4})
    assert issues == ["FIRST SECOND: 4/10: the picture shows the whole story"], issues
    assert opener == (3, "the picture shows the whole story")


def test_opener_must_be_a_later_real_picture():
    for bad in (3, 1, 9, "4", None):  # 3 is a painting, 1 is the opening itself, 9 doesn't exist
        issues, opener = run_check({"score": 5, "why": "no clear subject", "open_with_scene": bad})
        assert opener is None, bad
        assert issues == ["FIRST SECOND: 5/10: no clear subject"]


def test_good_opening_or_no_reply_changes_nothing():
    assert run_check({"score": 8, "why": "strong", "open_with_scene": 4}) == ([], None)
    assert run_check(None) == ([], None)
    assert run_check({"score": "high"}) == ([], None)


def test_opener_fix_swaps_once():
    with tempfile.TemporaryDirectory() as d:
        st = state()
        notes = review.apply_review_fixes(st, Path(d), {}, opener=(3, "shows the twist"))
        assert st["choices"][0]["bg"] == real(3) and st["short"]["opener_swapped"] is True
        assert notes == ["scene 1 now opens on scene 4's picture (first second: shows the twist)"], notes


def test_logbook_marks_tiny_samples():
    old = session.LOG
    with tempfile.TemporaryDirectory() as d:
        session.LOG = Path(d) / "log.md"
        session.LOG.write_text("# Logbook\n\n## Cardiff Giant\nViews: 28\nStayed to watch (%): 81.0\n\n"
                               "## Emperor Norton\nViews: 1,219\nStayed to watch (%): 58.6\n\n## Unposted\nViews:\n",
                               encoding="utf-8")
        try:
            out = logbook.logbook_results()
        finally:
            session.LOG = old
    cardiff, norton = out.split("## Emperor Norton")
    assert "Too few views to judge" in cardiff and "Too few views" not in norton
    assert "Unposted" not in out


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
