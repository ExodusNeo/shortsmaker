"""Tests for the Blender side (blender/build_scene.py, 2026-10-22): a tiny fixed build plan is rendered by the real
headless Blender and the frames are checked by their pixels. Takes about a minute; no AI usage.
Run: .venv\\Scripts\\python.exe tests\\test_blender_scene.py"""
import json
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shortsmaker import blender_plan, config  # noqa: E402

RED = (0xD8, 0x1F, 0x1A)


def near(px, rgb, tol=30):
    return all(abs(a - b) <= tol for a, b in zip(px[:3], rgb))


def count(img: Image.Image, rgb, tol=30) -> int:
    small = img.convert("RGB").resize((270, 480))  # quarter size: fast to scan
    return sum(near(px, rgb, tol) for px in small.getdata()) * 16


def render(plan: dict, seconds: list[float], beats_frames: str = "middle", peaks=None) -> dict[int, Image.Image]:
    """Render `plan` with scenes of the given lengths; returns {frame: image} for one frame per scene (its middle),
    or for every frame listed when beats_frames is a list."""
    fps, t, scenes = 30, 0.0, []
    for k, s in enumerate(seconds):
        first = round(t * fps) + 1
        t += s
        last = round(t * fps)
        scenes.append({"start": t - s, "end": t, "first": first, "last": last,
                       "peak": (peaks or {}).get(k, t - s * 0.3), "peak_frame": round(((peaks or {}).get(k, t - s * 0.3)) * fps) + 1})
    frames = [(sc["first"] + sc["last"]) // 2 for sc in scenes] if beats_frames == "middle" else beats_frames
    out = Path(tempfile.mkdtemp())
    job = {"plan": plan, "scenes": scenes, "fps": fps, "frames_dir": str(out), "only_frames": frames}
    (out / "build.json").write_text(json.dumps(job), encoding="utf-8")
    r = subprocess.run([str(config.BLENDER), "-b", "--factory-startup", "--python", str(ROOT / "blender" / "build_scene.py"),
                        "--", str(out / "build.json")], capture_output=True, text=True, timeout=900)
    got = {f: out / f"f_{f:04d}.png" for f in frames}
    missing = [f for f, p in got.items() if not p.exists()]
    assert not missing, f"no frames {missing}\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}"
    return {f: Image.open(p) for f, p in got.items()}


def plan_with(beats: list[str], **over) -> dict:
    p = blender_plan.default_build(len(beats))
    p["beats"] = beats
    p.update(over)
    return p


def test_truss_build_and_zoom_frames():
    plan = plan_with(["wide", "build", "build", "zoom"])
    plan["focus"]["label"] = "GUSSET PLATE U10"
    imgs = list(render(plan, [1.0, 1.0, 1.0, 1.5], [15, 45, 75, 135]).values())  # the zoom's last frame: arrived
    assert all(im.size == (1080, 1920) for im in imgs)
    wide, build1, build2, zoom = imgs
    assert count(zoom, RED) >= 400, count(zoom, RED)  # the focus part shows red when zoomed in
    assert count(zoom, (0x14, 0x14, 0x19), 40) >= 200  # ink: lines and the label
    assert build1.tobytes() != build2.tobytes()  # parts keep arriving
    assert count(wide, RED) < 400  # nothing is red before the zoom


STEEL, CONCRETE = (0x9E, 0xA8, 0xB3), (0xE3, 0xDC, 0xCD)


def changed(a: Image.Image, b: Image.Image) -> float:
    """Share of pixels that differ clearly between two frames."""
    x, y = a.convert("L").resize((270, 480)), b.convert("L").resize((270, 480))
    return sum(abs(p - q) > 25 for p, q in zip(x.getdata(), y.getdata())) / (270 * 480)


def test_each_failure_changes_the_focus():
    # the same peak frame with and without the failure ("none": Blender ignores it; the plan checker never sends it)
    def peak(kind):
        plan = plan_with(["build", "zoom", "failure"])
        plan["failure"]["kind"] = kind
        return render(plan, [1.0, 1.5, 2.0], [136], peaks={2: 4.1})[136]
    still = peak("none")
    for kind in ("bend", "crack", "shear", "sway"):
        need = 0.002 if kind == "crack" else 0.015  # a crack is a line: it changes few pixels
        assert changed(still, peak(kind)) >= need, (kind, changed(still, peak(kind)))


def test_collapse_moves_the_span_down():
    def after(then):
        plan = plan_with(["build", "zoom", "failure", "aftermath"])
        plan["failure"]["then"] = then
        return render(plan, [1.0, 1.0, 1.0, 2.5], [165], peaks={2: 2.6})[165]
    standing, fallen = after("none"), after("collapse_span")
    assert count(fallen, STEEL, 20) < count(standing, STEEL, 20) * 0.8, (count(standing, STEEL, 20), count(fallen, STEEL, 20))


def test_every_template_renders():
    for template in ("girder_bridge", "suspension_bridge", "cable_stayed_bridge", "eyebar_chain_bridge"):
        plan = plan_with(["build", "wide"])
        plan["structure"] = {**plan["structure"], "template": template, "spans": 3}
        (wide,) = render(plan, [1.0, 1.0], [60]).values()
        assert count(wide, STEEL, 20) + count(wide, CONCRETE, 12) >= 0.03 * 1080 * 1920, template  # bridges are slender: 3.4-4.8% in a wide shot


def test_bridge_stands_until_the_build_starts_over():
    # the hook (scene 1) and the next scene show the finished bridge; the first build scene cuts to the empty site
    plan = plan_with(["failure_preview", "wide", "build", "zoom"])
    wide, site = render(plan, [1.5, 1.0, 1.0, 1.0], [60, 76]).values()
    assert count(site, STEEL, 20) < count(wide, STEEL, 20) * 0.5, (count(wide, STEEL, 20), count(site, STEEL, 20))


if __name__ == "__main__":
    if not config.BLENDER.exists():
        print(f"SKIPPED: no Blender at {config.BLENDER}")
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
