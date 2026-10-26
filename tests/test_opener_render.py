"""Tests for running an opener from a Short (opener_render.py, 2026-10-27): models from the library or fetched, the
headless run, the review, up to 2 fix rounds, the fallback, reuse, credits. Blender is faked by a tiny script that
writes numbered PNGs and a report; the AI and the add-on are faked. No AI usage.
Run: .venv\\Scripts\\python.exe tests\\test_opener_render.py"""
import copy
import json
import shutil
import sys
import tempfile
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shortsmaker import blender_link, config, llm, media_tools, opener_plan, opener_render  # noqa: E402

FIX = ROOT / "tests" / "fixtures" / "openers"
PLAN = json.loads((FIX / "chicken_chop.json").read_text(encoding="utf-8"))["plan"]

FAKE = '''import json, sys
from pathlib import Path
from PIL import Image
args = sys.argv[1:]
log = Path(r"{log}")
log.write_text((log.read_text() if log.exists() else "") + "run\\n")
if Path(r"{crash}").exists():
    sys.exit(1)
job = json.loads(Path(args[args.index("--") + 1]).read_text(encoding="utf-8"))
Path(r"{lastjob}").write_text(json.dumps(job))
flag = Path(r"{fail}")
failures = flag.read_text().splitlines() if flag.exists() else []
n = round(job["seconds"] * job["fps"])
if not failures:
    out = Path(job["frames_dir"]); out.mkdir(parents=True, exist_ok=True)
    for f in range(1, n + 1):
        Image.new("RGB", (216, 384), (f % 255, 90, 60)).save(out / f"f_{{f:04d}}.png")
Path(job["report"]).write_text(json.dumps({{"ok": not failures, "failures": failures, "frames": n, "pieces": 2,
                                            "cut_shares": {{}}, "lowest": {{}}}}))
'''


class Env:
    """A temp work folder, a library holding the fixture models, a fake Blender and fakes for the AI and add-on."""

    def __enter__(self):
        self.dir = Path(tempfile.mkdtemp(prefix="opener_render_"))
        self.work, lib = self.dir / "work", self.dir / "library"
        self.work.mkdir()
        lib.mkdir()
        for f in FIX.glob("polypizza_*"):
            shutil.copy(f, lib / f.name)
        self.log, self.crash, self.fail, self.lastjob = (self.dir / n for n in ("runs.txt", "crash.flag", "fail.txt", "job.json"))
        (self.dir / "fake.py").write_text(FAKE.format(log=self.log, crash=self.crash, fail=self.fail, lastjob=self.lastjob),
                                          encoding="utf-8")
        self.exe = self.dir / "blender.cmd"
        self.exe.write_text(f'@"{sys.executable}" "{self.dir / "fake.py"}" %*\n', encoding="utf-8")
        self.saved = (config.LIBRARY, llm.ask_ai, opener_plan.fix_plan, blender_link.ping, blender_link.search,
                      blender_link.fetch_model)
        config.LIBRARY = lib
        self.reviews, self.fixes = [], []
        llm.ask_ai = lambda prompt, **k: self.reviews.append(prompt) or {"ok": True, "problems": []}
        opener_plan.fix_plan = lambda short, failures: self.fixes.append(list(failures)) or copy.deepcopy(short["opener"])
        return self

    def runs(self) -> int:
        return len(self.log.read_text().splitlines()) if self.log.exists() else 0

    def __exit__(self, *exc):
        (config.LIBRARY, llm.ask_ai, opener_plan.fix_plan, blender_link.ping, blender_link.search,
         blender_link.fetch_model) = self.saved
        shutil.rmtree(self.dir, ignore_errors=True)


def short() -> dict:
    return {"title": "Mike", "opener": copy.deepcopy(PLAN)}


def test_success_returns_clip():
    with Env() as e:
        s = short()
        clip, why = opener_render.render_opener(s, 3.0, e.work, e.exe)
        assert why is None and clip == e.work / "opener.mp4" and clip.exists(), why
        assert abs(media_tools.duration(clip) - 3.0) < 0.05, media_tools.duration(clip)
        assert e.runs() == 1 and len(e.reviews) == 1


def test_beats_scaled_into_scene():
    with Env() as e:
        s = short()
        s["opener"]["beats"][2]["at"] = 2.5
        opener_render.render_opener(s, 1.8, e.work, e.exe)
        beats = json.loads(e.lastjob.read_text())["plan"]["beats"]
        ats = [b["at"] for b in beats]
        assert max(ats) <= 1.8 - 1 / 30 + 1e-9 and ats == sorted(ats), ats


def test_failed_checks_fix_then_fallback():
    with Env() as e:
        e.fail.write_text("overlap: a/b frames 3-4")
        clip, why = opener_render.render_opener(short(), 3.0, e.work, e.exe)
        assert clip is None and why == "opener failed: overlap: a/b frames 3-4", why
        assert e.runs() == 3 and len(e.fixes) == 2 and e.fixes[0] == ["overlap: a/b frames 3-4"]


def test_crash_retry_then_fallback():
    with Env() as e:
        e.crash.write_text("x")
        clip, why = opener_render.render_opener(short(), 3.0, e.work, e.exe)
        assert clip is None and "Blender" in why and e.runs() == 2, (why, e.runs())


def test_reuse_unchanged():
    with Env() as e:
        s = short()
        opener_render.render_opener(s, 3.0, e.work, e.exe)
        clip, why = opener_render.render_opener(s, 3.0, e.work, e.exe)
        assert why is None and clip.exists() and e.runs() == 1


def test_missing_model_blender_off():
    with Env() as e:
        for f in config.LIBRARY.glob("polypizza_6NTegstc5Jy.*"):
            f.unlink()
        blender_link.ping = lambda timeout=2.0: False
        clip, why = opener_render.render_opener(short(), 3.0, e.work, e.exe)
        assert clip is None and why == "opener failed: model 'rooster' not in the library and Blender is off", why
        assert e.runs() == 0


def test_review_rejects():
    with Env() as e:
        replies = iter([{"ok": False, "problems": ["the axe hits the breast"]}, {"ok": True, "problems": []}])
        llm.ask_ai = lambda prompt, **k: next(replies)
        clip, why = opener_render.render_opener(short(), 3.0, e.work, e.exe)
        assert why is None and clip.exists() and e.fixes == [["the axe hits the breast"]] and e.runs() == 2


def test_cc_by_credit():
    with Env() as e:
        s = short()
        opener_render.render_opener(s, 3.0, e.work, e.exe)
        assert any("Rooster" in c and "poly.pizza/m/6NTegstc5Jy" in c for c in s["opener_credits"]), s["opener_credits"]
        assert not any("Axe" in c for c in s["opener_credits"])  # CC0 needs no credit


def test_pick_model():
    hits = [{"source": "polypizza", "id": "a", "title": "Rooster statue", "author": "x", "licence": "CC0 1.0", "tags": []},
            {"source": "polypizza", "id": "b", "title": "Rooster", "author": "y", "licence": "CC0 1.0", "tags": []}]
    old = llm.ask_ai
    try:
        llm.ask_ai = lambda prompt, **k: {"pick": 2}
        assert opener_render.pick_model("rooster", hits) == hits[1]
        llm.ask_ai = lambda prompt, **k: {"pick": None}
        assert opener_render.pick_model("rooster", hits) is None
    finally:
        llm.ask_ai = old
    with Env() as e:
        for f in config.LIBRARY.glob("polypizza_6NTegstc5Jy.*"):
            f.unlink()
        blender_link.ping = lambda timeout=2.0: True
        blender_link.search = lambda find: hits
        llm.ask_ai = lambda prompt, **k: {"pick": None}
        clip, why = opener_render.render_opener(short(), 3.0, e.work, e.exe)
        assert clip is None and why == "opener failed: no fitting model for 'rooster'", why


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
