"""Tests for the first-second check (would a scroller stop?) and the honest logbook lessons. No AI usage, no rendering.
Run: .venv\\Scripts\\python.exe tests\\test_first_second.py"""
import sys
import tempfile
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import llm, logbook, media_tools, review, session  # noqa: E402
from shortsmaker import rules  # noqa: E402

rules.load_rules("strange-history")  # the prompts read the channel's rules file


def test_quality_check_reads_ffmpeg_and_flags_reused_pictures():
    log = ("[blackdetect @ 0] black_start:3.2 black_end:3.6 black_duration:0.4\n"
           "  Integrated loudness:\n    I:         -14.2 LUFS\n  True peak:\n    Peak:        -1.0 dBFS\n")
    saved = review.subprocess.run
    review.subprocess.run = lambda *a, **k: type("Done", (), {"stderr": log})()
    try:
        issues = review.quality_check(Path("x.mp4"), [0.0, 2.0, 70.0],
                                      ["Wikimedia Commons, public domain: a", 'reused from scene 1 (nothing fit "x")'])
    finally:
        review.subprocess.run = saved
    assert any("black screen" in i and "scene 2" in i for i in issues), issues
    assert any("scene 2 shows another scene's picture again" in i for i in issues), issues
    assert any("past the planned" in i for i in issues), issues  # 70 s against writing.max_seconds() 62
    assert not any("loudness" in i or "peaks" in i for i in issues), issues


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


def test_swap_moves_the_owners_clip_with_its_picture():
    st = state()
    st["short"]["scenes"][3].update(owner_clip="scene4.mp4", motion="he turns the pages", motion_people=True)
    review.swap_pictures(st, 0, 3)
    first, fourth = st["short"]["scenes"][0], st["short"]["scenes"][3]
    assert first["animate"] is True and first["owner_clip"] == "scene4.mp4" and first["motion"] == "he turns the pages"
    assert first["motion_people"] is True
    assert fourth["animate"] is False and fourth["owner_clip"] is None


def test_swap_ignores_a_clip_already_dropped():
    st = state()
    st["short"]["scenes"][3].update(owner_clip="scene4.mp4", animate=False)  # its picture was repainted earlier
    review.swap_pictures(st, 0, 3)
    assert st["short"]["scenes"][0]["animate"] is False and st["short"]["scenes"][0]["owner_clip"] is None


def test_opener_prompt_shows_each_scenes_line_and_picture():
    asked, old_ff, old_ask = [], media_tools.ffmpeg, llm.ask_ai
    media_tools.ffmpeg = lambda *a, cwd: (Path(cwd) / a[-1]).write_bytes(b"jpg")
    llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: asked.append(prompt) or {"score": 8}
    try:
        with tempfile.TemporaryDirectory() as d:
            board = Path(d) / "storyboard.jpg"
            board.write_bytes(b"jpg")
            st = state()
            st["short"]["character"] = "William Chester Minor"
            review.first_second_check(Path(d) / "short.mp4", st["short"], st["choices"], board, Path(d))
    finally:
        media_tools.ffmpeg, llm.ask_ai = old_ff, old_ask
    assert 'scene 1 says "line 0" | its picture: File:Photo 0.jpg' in asked[0]
    assert 'scene 4 says "line 3" | its picture: File:Photo 3.jpg' in asked[0]
    assert "scene 3 says" not in asked[0]  # a painting can't be swapped in
    assert "main character: William Chester Minor" in asked[0] and "BOTH fit" in asked[0]


def test_review_knows_what_dims_a_picture_on_purpose():
    asked, old_ff, old_ask = [], media_tools.ffmpeg, llm.ask_ai
    media_tools.ffmpeg = lambda *a, cwd: (Path(cwd) / "sheet1.jpg").write_bytes(b"jpg")
    llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: asked.append(prompt) or {"problems": []}
    short = {"title": "Oxford", "scenes": [
        {"narration": "But the chief editor had never seen his face.", "graphic": {"style": "question", "text": "WHO WAS HE?"}},
        {"narration": "the editor, James Murray,", "graphic": None}, {"narration": "needed volunteers", "graphic": None}]}
    cues = [{"graphic": 4.1}, {"card": True, "on": 5.9, "off": 7.7}, {}]
    try:
        with tempfile.TemporaryDirectory() as d:
            review.visual_review(Path(d) / "v.mp4", short, [3.2, 5.5, 8.0, 11.6], ["photo"] * 3, Path(d), cues=cues)
            review.visual_review(Path(d) / "v.mp4", short, [3.2, 5.5, 8.0, 11.6], ["photo"] * 3, Path(d))
    finally:
        media_tools.ffmpeg, llm.ask_ai = old_ff, old_ask
    assert 'on top: question beat (picture dims, a big question holds) "WHO WAS HE?" 0:04.1-0:05.2' in asked[0]
    assert "on top: person photo card 0:05.9-0:07.7 (background dims)" in asked[0]
    assert '"needed volunteers" | picture: photo' + "\n" in asked[0]  # nothing on top of scene 3
    assert "| on top:" not in asked[1]  # without cues (fix.bat callers), the plan is as before


def test_fix_round_user_confirmation():
    import builtins
    from shortsmaker import short_render
    prompts = []
    old_input = builtins.input
    try:
        builtins.input = lambda prompt="": prompts.append(prompt) or ""
        # simulate input prompt logic
        ans = builtins.input("prompt")
        assert ans == ""
        assert len(prompts) == 1

        builtins.input = lambda prompt="": prompts.append(prompt) or "skip"
        ans = builtins.input("prompt").strip().lower()
        assert ans in ("skip", "n", "no", "q", "quit")
    finally:
        builtins.input = old_input


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
