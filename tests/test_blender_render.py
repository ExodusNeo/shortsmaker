"""Tests for running Blender from a Short (blender_render.py, 2026-10-22): frame ranges per scene, the failure peak on
the emphasis word, one clip per scene, reusing frames, retry then BlenderFailed. Blender is faked by a tiny script
that writes numbered PNGs. No AI usage. Run: .venv\\Scripts\\python.exe tests\\test_blender_render.py"""
import json
import sys
import tempfile
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shortsmaker import blender_plan, blender_render, media_tools  # noqa: E402

FAKE = '''import json, sys
from pathlib import Path
from PIL import Image
args = sys.argv[1:]
log = Path(r"{log}")
log.write_text(log.read_text() + "run\\n" if log.exists() else "run\\n")
if Path(r"{crash}").exists():
    sys.exit(1)
job = json.loads(Path(args[args.index("--") + 1]).read_text(encoding="utf-8"))
out = Path(job["frames_dir"]); out.mkdir(parents=True, exist_ok=True)
for f in job["only_frames"] or range(1, job["scenes"][-1]["last"] + 1):
    Image.new("RGB", (216, 384), (f % 255, 80, 80)).save(out / f"f_{{f:04d}}.png")
'''


def fake_blender(d: Path, crash: bool = False) -> tuple[Path, Path]:
    """A .cmd that behaves like blender.exe for build_scene.py; returns (exe, run log)."""
    log, flag = d / "runs.txt", d / "crash.flag"
    if crash:
        flag.write_text("x")
    (d / "fake.py").write_text(FAKE.format(log=log, crash=flag), encoding="utf-8")
    exe = d / "blender.cmd"
    exe.write_text(f'@"{sys.executable}" "{d / "fake.py"}" %*\n', encoding="utf-8")
    return exe, log


def short(n: int) -> dict:
    return {"build": blender_plan.default_build(n),
            "scenes": [{"narration": f"line {k}", "emphasis": "snapped" if k == 1 else None} for k in range(n)]}


def test_scene_frames_cover_every_frame_once():
    bounds = [0.0, 1.017, 1.2, 3.333, 3.5, 6.01]
    ranges = blender_render.scene_frames(bounds)
    assert ranges[0][0] == 1 and ranges[-1][1] == round(6.01 * 30)
    for (a, b), (c, _) in zip(ranges, ranges[1:]):
        assert c == b + 1, ranges
    assert all(b >= a for a, b in ranges), ranges  # even a 0.17 s scene gets a frame


def test_peak_on_the_emphasis_word():
    words = [(0.0, 0.5, "The"), (0.6, 1.0, "bolt"), (2.2, 2.6, "snapped."), (2.7, 3.0, "Then")]
    peaks = blender_render.peaks(short(3), [0.0, 2.0, 4.0, 6.0], words)
    assert abs(peaks[1] - 2.2) < 1e-6  # scene 2's emphasis word
    assert abs(peaks[0] - 1.4) < 1e-6 and abs(peaks[2] - 5.4) < 1e-6  # no emphasis: 70% into the scene


def test_render_clips_makes_one_clip_per_scene():
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        exe, _ = fake_blender(d)
        bounds = [0.0, 1.0, 2.5, 4.0]
        clips = blender_render.render_clips(short(3), bounds, [], d / "work", exe)
        assert sorted(clips) == [0, 1, 2]
        for i, clip in clips.items():
            assert abs(media_tools.duration(clip) - (bounds[i + 1] - bounds[i])) < 0.05, (i, media_tools.duration(clip))


def test_same_build_json_reuses_frames():
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        exe, log = fake_blender(d)
        s = short(3)
        blender_render.render_clips(s, [0.0, 1.0, 2.0, 3.0], [], d / "work", exe)
        blender_render.render_clips(s, [0.0, 1.0, 2.0, 3.0], [], d / "work", exe)
        assert log.read_text().count("run") == 1
        s["build"]["failure"]["kind"] = "crack"
        blender_render.render_clips(s, [0.0, 1.0, 2.0, 3.0], [], d / "work", exe)
        assert log.read_text().count("run") == 2


def test_crash_retries_then_raises():
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        exe, log = fake_blender(d, crash=True)
        try:
            blender_render.render_clips(short(3), [0.0, 1.0, 2.0, 3.0], [], d / "work", exe)
            raise AssertionError("no BlenderFailed")
        except blender_render.BlenderFailed as e:
            assert "exit" in str(e).lower(), e
        assert log.read_text().count("run") == 2


def test_missing_blender_raises():
    with tempfile.TemporaryDirectory() as d:
        try:
            blender_render.render_clips(short(3), [0.0, 1.0, 2.0, 3.0], [], Path(d) / "work", Path(d) / "nope.exe")
            raise AssertionError("no BlenderFailed")
        except blender_render.BlenderFailed as e:
            assert "not found" in str(e), e


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
