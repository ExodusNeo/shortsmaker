"""Tests for the people tables (blender/opener_tables.json "roles" and "people_moves", 2026-10-27) and the stand-in
people library the opener tests build (tests/people_standin.py: no Quaternius file may be in git). When the real
library is packed on D: (blender/pack_people.py) the tables are also checked against it. Real headless Blender for
the stand-in, under a minute. No AI usage.
Run: .venv\\Scripts\\python.exe tests\\test_people_tables.py"""
import json
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shortsmaker import config  # noqa: E402

TABLES = json.loads((ROOT / "blender" / "opener_tables.json").read_text(encoding="utf-8"))
REAL = json.loads(config.PEOPLE_JSON.read_text(encoding="utf-8")) if config.PEOPLE_JSON.exists() else None
STANDIN = ROOT / "tests" / "people_standin.py"


def standin(out: Path, drop: str = "") -> dict:
    """Build the stand-in library into `out` (drop = a material its bodies leave out); returns its people.json."""
    r = subprocess.run([str(config.BLENDER), "-b", "--factory-startup", "--python-exit-code", "1", "--python",
                        str(STANDIN), "--", str(out), drop], capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, (r.stdout or "")[-2000:] + (r.stderr or "")[-2000:]
    assert (out / "people.blend").exists()
    return json.loads((out / "people.json").read_text(encoding="utf-8"))


def test_every_role_is_complete():
    roles = TABLES["roles"]
    assert len(roles) >= 15, len(roles)
    for name, r in roles.items():
        assert isinstance(r["body"], str) and r["body"], name
        assert 1.0 <= r["height_m"] <= 2.1, name
        assert r.get("hat") is None or isinstance(r["hat"], str), name
        for mat, rgb in r["colours"].items():
            assert len(rgb) == 3 and all(0 <= c <= 1 for c in rgb), (name, mat)
        if REAL:
            assert r["body"] in REAL["bodies"], (name, r["body"])
            missing = set(r["colours"]) - set(REAL["bodies"][r["body"]]["materials"])
            assert not missing, (name, missing)


def test_every_move_has_a_clip_and_kind():
    moves = TABLES["people_moves"]
    assert {"walk", "run", "die", "swing_prop"} <= set(moves)
    for name, m in moves.items():
        assert m["kind"] in ("travel", "in_place"), name
        if REAL:
            clip = REAL["clips"].get(m["clip"])
            assert clip, (name, m["clip"])
            assert (m["kind"] == "travel") == bool(clip["stride_m"]), name


def test_standin_matches_tables():
    lib = standin(Path(tempfile.mkdtemp(prefix="people_standin_")))
    for name, r in TABLES["roles"].items():
        assert r["body"] in lib["bodies"], name
        assert set(r["colours"]) <= set(lib["bodies"][r["body"]]["materials"]), name
    for name, m in TABLES["people_moves"].items():
        clip = lib["clips"][m["clip"]]
        assert (m["kind"] == "travel") == bool(clip["stride_m"]), name
    assert set(lib["bones"]) >= {"head", "hand_r", "foot_l", "foot_r"}
    assert lib["rig_height"] > 0


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
