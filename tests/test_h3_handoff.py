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


def test_scene_number_given_as_text_is_accepted():
    def run():
        llm.ask_ai = fake_ai([{"scenes": [{"scene": " 1", **{k: v for k, v in GOOD.items()}}]}])
        assert set(gpu.h3_prompts(short_with(1), Path(tempfile.gettempdir()), [0])) == {0}
    with_fakes(run)


def test_tells_owner_after_five_failed_rounds():
    def run():
        bad = {"scenes": [{"scene": 1, **GOOD, "camera": ""}]}
        llm.ask_ai = fake_ai([bad] * 5 + [{"scenes": [{"scene": 1, **GOOD}]}])
        waits = []
        builtins.input = lambda msg="": waits.append(msg) or ""
        assert set(gpu.h3_prompts(short_with(1), Path(tempfile.gettempdir()), [0])) == {0}
        assert len(waits) == 1 and "scene 1" in waits[0] and "no camera line" in waits[0]
    with_fakes(run)


def handoff(tmp: Path, during_pause=lambda folder: None):
    """veo_handoff on 3 marked scenes (scene 2 is a CLOSE-UP) with AI, cropping, Explorer and ffmpeg faked."""
    work = tmp / "short" / "work"
    work.mkdir(parents=True)
    short = short_with(3)
    short["scenes"][1]["shot"] = "CLOSE-UP: a hand"
    old = (gpu.h3_prompts, gpu.cover_crop, gpu.os.startfile, builtins.input, gpu.media_tools.ffmpeg,
           gpu.media_tools.video_encoder)
    asked = []
    gpu.h3_prompts = lambda s, folder, scenes: asked.append(scenes) or {i: f"PROMPT {i + 1}" for i in scenes}
    gpu.cover_crop = lambda src, out: out.write_bytes(b"jpg")
    gpu.os.startfile = lambda p: None
    builtins.input = lambda msg="": during_pause(work.parent / "veo")
    gpu.media_tools.ffmpeg = lambda *a, cwd: (Path(cwd) / a[-1]).write_bytes(b"mp4")
    gpu.media_tools.video_encoder = lambda: []
    try:
        got = gpu.veo_handoff(short, work, [0.0, 3.0, 5.0, 9.5], [0, 1, 2])
    finally:
        (gpu.h3_prompts, gpu.cover_crop, gpu.os.startfile, builtins.input, gpu.media_tools.ffmpeg,
         gpu.media_tools.video_encoder) = old
    return got, work.parent / "veo", asked


def test_handoff_writes_jobs_and_zip():
    import json
    import zipfile
    with tempfile.TemporaryDirectory() as d:
        _, folder, asked = handoff(Path(d))
        assert asked == [[0, 2]]  # no prompt asked for the CLOSE-UP
        jobs = json.loads((folder / "jobs.json").read_text(encoding="utf-8"))
        assert jobs == [
            {"scene": 1, "image": "start1.jpg", "prompt": "PROMPT 1", "seconds": round(3.0 + gpu.XFADE, 2), "out": "scene1.mp4"},
            {"scene": 3, "image": "start3.jpg", "prompt": "PROMPT 3", "seconds": round(4.5 + gpu.XFADE, 2), "out": "scene3.mp4"}]
        assert set(zipfile.ZipFile(folder / "veo.zip").namelist()) == {"jobs.json", "start1.jpg", "start3.jpg", "h3_run.py"}
        notes = (folder / "prompts.txt").read_text(encoding="utf-8")
        assert "Colab" in notes and "Google Flow" in notes and "PROMPT 1" in notes and "PROMPT 3" in notes


def zip_of(path: Path, names):
    import zipfile
    with zipfile.ZipFile(path, "w") as z:
        for n in names:
            z.writestr(n, b"x")


def test_unpack_clips():
    with tempfile.TemporaryDirectory() as d:
        folder = Path(d) / "veo"
        folder.mkdir()
        zip_of(folder / "clips.zip", ["clips/scene3.mp4", "scene1.MP4", "../evil.mp4", "scene1.mp4.exe", "notes.txt",
                                      "clips\\scene4.webm"])
        assert gpu.unpack_clips(folder) == ["scene1.MP4", "scene3.mp4", "scene4.webm"]
        assert sorted(p.name for p in folder.iterdir()) == ["clips.zip", "scene1.MP4", "scene3.mp4", "scene4.webm"]
        assert not (Path(d) / "evil.mp4").exists()
        (folder / "clips.zip").write_bytes(b"not a zip")
        assert gpu.unpack_clips(folder) == []
        (folder / "clips.zip").unlink()
        assert gpu.unpack_clips(folder) == []


def test_handoff_picks_up_clips_zip():
    with tempfile.TemporaryDirectory() as d:
        got, _, _ = handoff(Path(d), lambda folder: zip_of(folder / "clips.zip", ["scene1.mp4"]))
        assert list(got) == [0] and got[0].name == "clip0_veo.mp4" and got[0].exists()


def test_renamed_zip_is_picked_up():
    with tempfile.TemporaryDirectory() as d:
        folder = Path(d) / "veo"
        folder.mkdir()
        zip_of(folder / "clips (1).zip", ["scene2.mp4"])
        assert gpu.unpack_clips(folder) == ["scene2.mp4"]
        assert (folder / "scene2.mp4").exists()


def test_old_zip_does_not_overwrite_newer_clip():
    import os, time
    with tempfile.TemporaryDirectory() as d:
        folder = Path(d) / "veo"
        folder.mkdir()
        z_file = folder / "clips.zip"
        zip_of(z_file, ["scene1.mp4"])
        past = time.time() - 100
        os.utime(z_file, (past, past))
        flow_clip = folder / "scene1.mp4"
        flow_clip.write_bytes(b"newer flow clip")
        os.utime(flow_clip, (time.time(), time.time()))
        assert gpu.unpack_clips(folder) == []
        assert flow_clip.read_bytes() == b"newer flow clip"


def test_duplicate_clip_names_deduplicated():
    with tempfile.TemporaryDirectory() as d:
        folder = Path(d) / "veo"
        folder.mkdir()
        zip_of(folder / "clips.zip", ["clips/scene1.mp4", "scene1.mp4", "clips/scene2.mp4"])
        assert gpu.unpack_clips(folder) == ["scene1.mp4", "scene2.mp4"]


def test_all_closeup_marked_scenes_skip_pause():
    with tempfile.TemporaryDirectory() as d:
        work = Path(d) / "short" / "work"
        work.mkdir(parents=True)
        short = short_with(2)
        short["scenes"][0]["shot"] = "CLOSE-UP: face"
        short["scenes"][1]["shot"] = "CLOSE-UP: hand"
        old_input = builtins.input
        waited = []
        builtins.input = lambda msg="": waited.append(msg) or ""
        try:
            got = gpu.veo_handoff(short, work, [0.0, 3.0, 6.0], [0, 1])
            assert got == {}
            assert len(waited) == 0  # no pause with 0 clips to make
            assert not (work.parent / "veo" / "jobs.json").exists()
        finally:
            builtins.input = old_input


def test_old_zips_cleaned_up_on_handoff_start():
    with tempfile.TemporaryDirectory() as d:
        veo = Path(d) / "short" / "veo"
        veo.mkdir(parents=True)
        (veo / "clips.zip").write_bytes(b"old")
        (veo / "clips (1).zip").write_bytes(b"old")
        handoff(Path(d))
        assert not (veo / "clips.zip").exists()
        assert not (veo / "clips (1).zip").exists()


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
