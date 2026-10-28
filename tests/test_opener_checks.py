"""Tests for the per-frame opener checks (blender/opener_checks.py, 2026-10-27): every check fails its bad case and
passes its good one, on primitives built in real headless Blender (tests/opener_check_cases.py, about a minute).
No AI usage. Run: .venv\\Scripts\\python.exe tests\\test_opener_checks.py"""
import json
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shortsmaker import config  # noqa: E402

_RESULTS = None


def results() -> dict:
    global _RESULTS
    if _RESULTS is None:
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "out.json"
            r = subprocess.run([str(config.BLENDER), "-b", "--factory-startup", "--python-exit-code", "1", "--python",
                                str(ROOT / "tests" / "opener_check_cases.py"), "--", str(out)],
                               capture_output=True, text=True, timeout=600)
            assert r.returncode == 0 and out.exists(), (r.stdout or "")[-2000:] + (r.stderr or "")[-2000:]
            _RESULTS = json.loads(out.read_text(encoding="utf-8"))
    return _RESULTS


def test_overlap():
    bad = results()["overlap_bad"]
    assert len(bad) == 1 and "A/B" in bad[0] and "frames 5-6" in bad[0], bad
    assert results()["overlap_allowed"] == []


def test_resting():
    assert results()["resting_float"] and "float" in results()["resting_float"][0]
    assert results()["resting_ok"] == []


def test_in_frame():
    bad = results()["in_frame_bad"]
    assert len(bad) == 1 and "mover" in bad[0], bad
    assert results()["in_frame_ok"] == []


def test_first_frame():
    assert any("15%" in f for f in results()["first_small"]), results()["first_small"]
    assert results()["first_ok"] == []
    # a wide, low subject (the people run's armoured car) reads big by its width (40%), not its height
    assert results()["first_wide"] == [], results()["first_wide"]
    assert results()["threat_sliver"] and "mostly out" in results()["threat_sliver"][0], results()["threat_sliver"]
    assert results()["threat_sliver_tool"] == [], results()["threat_sliver_tool"]
    # framed with what he goes at, the person still needs 15%: a pair rule passed a tiny officer beside a van
    assert results()["pair_small"] and "15%" in results()["pair_small"][0], results()["pair_small"]


def test_moves_visibly():
    rocks = results()["moves_rocks"]
    assert len(rocks) == 1 and "rocker barely moves" in rocks[0] and "topple a tall thing" in rocks[0], rocks
    assert results()["moves_drops"] == [], results()["moves_drops"]


def test_edge_leads():
    assert results()["edge_wrong"] and "edge" in results()["edge_wrong"][0]
    assert results()["edge_right"] == []


def test_blade_face():
    assert results()["face_edge_on"] and "edge-on" in results()["face_edge_on"][0]
    assert "diagonal" in results()["face_edge_on"][0]  # says how to fix it, for the planner's fix round
    assert results()["face_ok"] == []


def test_hidden():
    assert results()["hidden_bad"] and "small_box" in results()["hidden_bad"][0], results()["hidden_bad"]
    assert results()["hidden_ok"] == []


def test_cut_result():
    r = results()
    assert any("head" in f and "0.15" in f for f in r["cut_half"]), r["cut_half"]
    assert r["cut_ok"] == [], r["cut_ok"]
    assert any("80" in f for f in r["cut_too_many"]), r["cut_too_many"]
    assert any("3 mm" in f for f in r["cut_crumb"]), r["cut_crumb"]
    assert r["cut_bits_ok"] == [], r["cut_bits_ok"]


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
