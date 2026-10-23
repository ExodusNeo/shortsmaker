"""Tests for colab/h3_run.py (the MiniMax H3 job runner that ships inside veo.zip) and the Colab notebook.
No GPU, no ComfyUI. Run: .venv\\Scripts\\python.exe tests\\test_h3_run.py"""
import sys
import tempfile
import traceback
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "colab"))
import h3_run  # noqa: E402


def test_frames_snap_to_17k_plus_5():
    assert [h3_run.frames(s) for s in (0, 1, 2, 3.04, 8)] == [5, 39, 56, 73, 192]
    assert all(h3_run.frames(s) % 17 == 5 for s in (0.3, 4.7, 9.9))


def test_graph_wiring():
    g = h3_run.graph("p", "start1.jpg", 73, 7, turbo=True, prefix="h3/scene1")
    by = {n["class_type"]: n for n in g.values()}
    assert set(h3_run.REQUIRED) <= set(by)
    i2v = by["MiniMaxH3ImageToVideo"]["inputs"]
    assert (i2v["width"], i2v["height"], i2v["length"], i2v["prompt"]) == (768, 1344, 73, "p")
    assert by["BasicScheduler"]["inputs"]["steps"] == 8 and by["RandomNoise"]["inputs"]["noise_seed"] == 7
    assert by["LoadImage"]["inputs"]["image"] == "start1.jpg"
    assert by["SaveVideo"]["inputs"]["filename_prefix"] == "h3/scene1"
    for node in g.values():  # every link points at a node that exists
        for v in node["inputs"].values():
            if isinstance(v, list):
                assert v[0] in g, v
    plain_g = h3_run.graph("p", "s", 73, 7, False, "x")
    plain = {n["class_type"]: n for n in plain_g.values()}
    assert "LoraLoaderModelOnly" not in plain and plain["BasicScheduler"]["inputs"]["steps"] == 20
    unet = next(k for k, n in plain_g.items() if n["class_type"] == "UNETLoader")
    assert plain["BasicScheduler"]["inputs"]["model"][0] == unet and plain["BasicGuider"]["inputs"]["model"][0] == unet


def test_fit_start_is_768x1344():
    with tempfile.TemporaryDirectory() as d:
        src, dst = Path(d) / "a.jpg", Path(d) / "b.png"
        im = Image.new("RGB", (1080, 1920), (0, 0, 255))
        im.paste((255, 0, 0), (0, 0, 540, 1920))  # left half red
        im.save(src, quality=95)
        h3_run.fit_start(src, dst)
        out = Image.open(dst)
        assert out.size == (768, 1344)
        assert out.getpixel((380, 672))[0] > 200 and out.getpixel((388, 672))[2] > 200  # split stays at the centre


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
