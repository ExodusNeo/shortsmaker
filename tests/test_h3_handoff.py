"""Tests for the Colab H3 / Flow hand-off: frame-checked video prompts, veo.zip, clips.zip. No AI usage, no rendering.
Run: .venv\\Scripts\\python.exe tests\\test_h3_handoff.py"""
import builtins
import sys
import tempfile
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import gpu, llm  # noqa: E402

GOOD = {"subject": "A wooden tower with open pans stands on a hill under dark clouds, men in coats at its base",
        "motion": "White vapour rises slowly from the pans", "camera": "Locked-off, no camera movement",
        "look": "Black-and-white 1910s photograph, film grain, soft overcast light",
        "avoid": ["morphing faces", "extra fingers", "text", "colour", "camera shake"]}


def short_with(n):
    return {"title": "Charles Hatfield", "scenes": [
        {"narration": f"line {k}", "motion": "vapour rises", "motion_people": False, "shot": ""} for k in range(n)]}


def fake_ai(replies, asked=None):
    def ask(prompt, fatal=True, read_dir=None, brain=None, bulk=False):
        if asked is not None:
            asked.append(prompt)
        return replies.pop(0)
    return ask


def with_fakes(fn):
    """Run fn with llm.ask_ai and input restored afterwards."""
    old_ask, old_input = llm.ask_ai, builtins.input
    try:
        return fn()
    finally:
        llm.ask_ai, builtins.input = old_ask, old_input


def test_problems():
    assert gpu.h3_problems(GOOD) == []
    assert any("camera" in p for p in gpu.h3_problems({**GOOD, "camera": ""}))
    assert any("subject" in p for p in gpu.h3_problems({**GOOD, "subject": "a tower"}))
    assert any("avoid" in p for p in gpu.h3_problems({**GOOD, "avoid": ["text"]}))
    assert gpu.h3_problems(None) == ["no entry for this scene"]


def test_prompt_joins_fields():
    p = gpu.h3_prompt({"motion_people": False}, GOOD)
    for part in (GOOD["subject"], GOOD["motion"], "Locked-off", "film grain", "first frame",
                 "stay completely still", "Avoid: morphing faces, extra fingers, text, colour, camera shake."):
        assert part in p, part


def test_retries_only_failing_scene_with_reason():
    def run():
        asked = []
        llm.ask_ai = fake_ai([{"scenes": [{"scene": 1, **GOOD}, {"scene": 3, **GOOD, "camera": ""}]},
                              {"scenes": [{"scene": 3, **GOOD}]}], asked)
        short = short_with(4)
        out = gpu.h3_prompts(short, Path(tempfile.gettempdir()), [0, 2])
        assert set(out) == {0, 2}
        assert "no camera" in asked[1] and "SCENE 1" not in asked[1] and "SCENE 3" in asked[1]
        assert all(gpu.motion_prompt(short["scenes"][i]) not in out[i] for i in out)
    with_fakes(run)


def test_missing_scene_is_asked_again():
    def run():
        asked = []
        llm.ask_ai = fake_ai([{"scenes": [{"scene": 1, **GOOD}]}, {"scenes": [{"scene": 2, **GOOD}]}], asked)
        out = gpu.h3_prompts(short_with(2), Path(tempfile.gettempdir()), [0, 1])
        assert set(out) == {0, 1} and "SCENE 2" in asked[1] and "no entry" in asked[1]
    with_fakes(run)


def test_waits_for_enter_when_no_ai_answers():
    def run():
        waits = []
        llm.ask_ai = fake_ai([None, {"scenes": [{"scene": 1, **GOOD}]}])
        builtins.input = lambda msg="": waits.append(msg) or ""
        assert set(gpu.h3_prompts(short_with(2), Path(tempfile.gettempdir()), [0])) == {0}
        assert len(waits) == 1 and "Enter" in waits[0]
    with_fakes(run)


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
