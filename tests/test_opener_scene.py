"""Tests for building openers in Blender (blender/opener_scene.py + moves.py, 2026-10-27): the reference plans in
tests/fixtures/openers (the owner-approved chicken chop, onion slices, an onion mince, a falling crate) must pass every
check, and broken variants must fail the matching check. Real headless Blender, a few minutes. No AI usage.
Run: .venv\\Scripts\\python.exe tests\\test_opener_scene.py"""
import copy
import json
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shortsmaker import config, opener_plan  # noqa: E402

FIX = ROOT / "tests" / "fixtures" / "openers"
SCRIPT = ROOT / "blender" / "opener_scene.py"


def fixture(name: str) -> dict:
    return json.loads((FIX / f"{name}.json").read_text(encoding="utf-8"))


def run(job_fixture: dict, render: bool = False) -> tuple[dict, Path]:
    """Build (and optionally render at 25%) one opener; returns (report, frames dir)."""
    d = Path(tempfile.mkdtemp(prefix="opener_test_"))
    models = {k: v if v.startswith("primitive:") else str(FIX / v) for k, v in job_fixture["models"].items()}
    job = {"plan": job_fixture["plan"], "models": models, "seconds": job_fixture["seconds"], "fps": 30,
           "size": [1080, 1920], "frames_dir": str(d / "frames"), "report": str(d / "report.json"),
           "render": render, "render_failed": False, "render_scale": 25}
    (d / "job.json").write_text(json.dumps(job), encoding="utf-8")
    r = subprocess.run([str(config.BLENDER), "-b", "--factory-startup", "--python-exit-code", "1", "--python",
                        str(SCRIPT), "--", str(d / "job.json")], capture_output=True, text=True, timeout=900)
    assert r.returncode == 0 and (d / "report.json").exists(), (r.stdout or "")[-3000:] + (r.stderr or "")[-3000:]
    return json.loads((d / "report.json").read_text(encoding="utf-8")), d / "frames"


def test_fixture_plans_are_clean():
    for name in ("chicken_chop", "onion_slices", "onion_mince", "box_fall"):
        assert opener_plan.clean_opener(copy.deepcopy(fixture(name)["plan"])) is not None, name


def test_box_fall_rests_and_renders():
    report, frames = run(fixture("box_fall"), render=True)
    assert report["ok"], report["failures"]
    assert abs(report["lowest"]["box"]) < 0.01, report["lowest"]  # lying on the ground at the end
    pngs = sorted(frames.glob("f_*.png"))
    assert len(pngs) == 60, len(pngs)
    first = Image.open(pngs[0]).convert("RGB")
    assert first.size == (270, 480) and len(set(first.resize((27, 48)).getdata())) > 5  # a real picture, not blank


def test_chicken_chop_reference():
    report, _ = run(fixture("chicken_chop"))
    assert report["ok"], report["failures"]
    assert 0.075 <= report["cut_shares"]["head"] <= 0.225, report["cut_shares"]
    # a blade tilted to show its face must move across the frame, not at the lens (the axe ballooned in live run 6)
    assert all(t < 0.3 for t in report["stroke_toward_camera"]), report["stroke_toward_camera"]
    assert report["held_offscreen"] == {"axe": True}, report["held_offscreen"]
    assert report["key_frames"] and all(1 <= f <= report["frames"] for f in report["key_frames"]), report["key_frames"]  # the unseen hand's side runs off the frame


def test_onion_slices():
    report, _ = run(fixture("onion_slices"))
    assert report["ok"], report["failures"]
    assert report["pieces"] == 5, report["pieces"]


def test_onion_mince():
    report, _ = run(fixture("onion_mince"))
    assert report["ok"], report["failures"]
    assert 40 <= report["pieces"] <= 60, report["pieces"]


def test_chicken_live_plan():
    """The plan Claude wrote for Mike in the first live run (2026-10-27): a wider stump whose rim the hop clipped."""
    report, _ = run(fixture("chicken_live"))
    assert report["ok"], report["failures"]


def test_walk_stops_short_of_obstacles():
    """Third live run (Mike): hop off to the left, then walk right, back into the stump: the walk must stop short."""
    job = fixture("chicken_live")
    for b in job["plan"]["beats"]:
        if b["move"] == "hop_off":
            b.pop("toward", None)
        if b["move"] == "walk":
            b["toward"], b["at"] = "right", 1.9
    report, _ = run(job)
    assert report["ok"], report["failures"]


def test_unbuildable_cut_is_reported_not_crashed():
    """Fourth live run (Mike): a fix round asked for an at_fraction slice but still expected "head" and "rest"; the
    split didn't match and Blender crashed, which tells the planner nothing. It must come back as a failure."""
    report, _ = run(fixture("chicken_live_crash"))  # the exact job that crashed
    assert not report["ok"] and any(f.startswith("cut") for f in report["failures"]), report["failures"]


def test_subject_without_follow():
    """Fifth live run (Mike): no camera follow and the stump listed first; the checks took the stump as the subject
    and found it hidden by itself on every frame."""
    report, _ = run(fixture("chicken_live_nofollow"))
    assert report["ok"], report["failures"]


def test_bad_plans_fail():
    crowded = fixture("chicken_chop")  # a crate on the stump right where the rooster stands
    crowded["plan"]["actors"].append({"id": "crate", "find": "crate", "size_m": 0.3, "on": "stump"})
    crowded["models"]["crate"] = "primitive:cube"
    wrong_count = fixture("onion_mince")
    wrong_count["plan"]["beats"][0]["expect"] = [{"pieces": "2-3", "then": "scatter"}]
    for job, word in ((crowded, "overlap"), (wrong_count, "cut")):
        report, _ = run(job)
        assert not report["ok"] and any(f.startswith(word) for f in report["failures"]), (word, report["failures"])


def test_swung_blade_shows_its_face():
    """A chop planned edge-on to the camera turns about its stroke until the camera sees the blade's flat side (owner,
    2026-10-27: the profile shot); it used to fail the blade check and go back to the planner."""
    edge_on = fixture("chicken_chop")
    edge_on["plan"]["beats"][0]["strokes"] = [{"through": "neck", "angle": "down"}]
    report, _ = run(edge_on)
    assert not any(f.startswith("blade") for f in report["failures"]), report["failures"]


def test_camera_follows_unasked():
    """The Mike plan left camera.follow out and the rooster walked off alone; the camera now follows the subject
    whatever the plan says."""
    wanders = fixture("chicken_chop")
    wanders["plan"]["camera"] = {"angle": "three_quarter"}
    report, _ = run(wanders)
    assert report["ok"], report["failures"]


def test_slow_motion_keeps_length():
    """The hit plays at half speed; the clip keeps its frame count (scene 1 is timed to the voice) and its last frame."""
    code = ("import sys; sys.path.insert(0, r'%s'); import opener_scene as o; t = o.retime(101, 12); "
            "assert len(t) == 101 and t == sorted(t) and t[0] == 1 and t[-1] >= 99, t; "
            "assert abs(t[t.index(next(x for x in t if x >= 10)) + 1] - next(x for x in t if x >= 10) - 0.5) < 1e-6; "
            "assert o.retime(30, 5) == [float(f) for f in range(1, 31)]") % SCRIPT.parent
    r = subprocess.run([str(config.BLENDER), "-b", "--factory-startup", "--python-exit-code", "1", "--python-expr", code],
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, (r.stdout or "")[-2000:] + (r.stderr or "")[-2000:]


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
