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
        opener_plan.fix_plan = lambda short, failures, seconds=None, scaled=None: self.fixes.append(list(failures)) or copy.deepcopy(short["opener"])
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


def test_review_frames_include_key_moments():
    """Sixth live run (Mike): 8 evenly spaced frames skipped the whole 0.3-second chop, so the review said it never
    happened. The strip must show the key moments."""
    picked = opener_render.review_frames({"key_frames": [17]}, 101)
    assert {15, 17, 20} <= set(picked) and picked[0] == 1 and picked[-1] == 101 and picked == sorted(picked)
    assert len(picked) <= 12
    assert opener_render.review_frames({}, 90)[0] == 1 and len(opener_render.review_frames({}, 90)) == 8


def test_review_reads_the_channel_opener_rules():
    from shortsmaker import session
    with Env() as e:
        old = dict(session.RULES)
        session.RULES["Opener"] = "Owner-approved: the chop stops at the first thing it isn't cutting."
        prompts = []
        llm.ask_ai = lambda prompt, **k: prompts.append(prompt) or {"ok": True, "problems": []}
        try:
            opener_render.render_opener(short(), 3.0, e.work, e.exe)
        finally:
            session.RULES.clear()
            session.RULES.update(old)
        assert any("the chop stops at the first thing it isn't cutting" in p for p in prompts), prompts[:1]


def test_channels_have_opener_rules():
    from shortsmaker import rules, session
    for name in ("strange-history", "weird-economics"):
        rules.load_rules(name)
        text = session.RULES.get("Opener", "")
        assert "unseen hand" in text and "stops at the first thing" in text, (name, text[:200])


def _wiring(render_result):
    """short_render.use_opener with render_opener faked; returns (check line, short, clips, images, sources, calls)."""
    from PIL import Image
    from shortsmaker import short_render
    d = Path(tempfile.mkdtemp(prefix="opener_wire_"))
    clip = d / "opener.mp4"
    media_tools.ffmpeg("-f", "lavfi", "-i", "color=c=orange:s=216x384:d=1", "-pix_fmt", "yuv420p", clip.name, cwd=d)
    s = {"title": "Mike", "opener": copy.deepcopy(PLAN), "scenes": [{"full": {"type": "custom"}, "credit_tag": "Photo: X (CC BY)"}, {"full": None}]}
    clips, images, sources = {1: d / "film1.mp4"}, [Image.new("RGB", (8, 8)), Image.new("RGB", (8, 8))], ["photo", "photo"]
    calls, old = [], opener_render.render_opener
    opener_render.render_opener = lambda short, seconds, work, exe=None: calls.append(seconds) or (
        (clip, None) if render_result == "ok" else render_result)
    try:
        why = short_render.use_opener(s, [0.0, 2.4, 5.0], d, clips, images, sources)
    finally:
        opener_render.render_opener = old
    return why, s, clips, images, sources, calls, clip


def test_use_opener_on_success():
    why, s, clips, images, sources, calls, clip = _wiring("ok")
    assert why is None and clips[0] == clip and calls == [2.4]
    assert sources[0] == "drawn in Blender (opener): " + PLAN["moment"] and s["scenes"][0]["full"] is None
    assert images[0].size == (216, 384) and s.get("opener_used") is True
    assert s["scenes"][0]["credit_tag"] is None  # the replaced photo's credit must not show on the animation


def test_use_opener_failure_keeps_scene():
    why, s, clips, images, sources, _, _ = _wiring((None, "opener failed: overlap: a/b frames 3-4"))
    assert why == "opener failed: overlap: a/b frames 3-4" and 0 not in clips and sources[0] == "photo"
    assert s["scenes"][0]["full"] == {"type": "custom"} and not s.get("opener_used")


def test_use_opener_planner_check():
    from shortsmaker import short_render
    s = {"title": "x", "opener_check": "opener: no usable plan", "scenes": [{"full": None}]}
    calls, old = [], opener_render.render_opener
    opener_render.render_opener = lambda *a, **k: calls.append(1) or (None, None)
    try:
        assert short_render.use_opener(s, [0.0, 2.0], Path("."), {}, [None], ["x"]) == "opener: no usable plan"
    finally:
        opener_render.render_opener = old


def test_blender_note():
    import builtins
    import io
    from contextlib import redirect_stdout
    from shortsmaker import cli
    pings, answers = [], iter(["", "s"])
    old_ping, old_input = blender_link.ping, builtins.input
    try:
        blender_link.ping = lambda timeout=2.0: pings.append(1) and False
        builtins.input = lambda prompt="": next(answers)
        out = io.StringIO()
        with redirect_stdout(out):
            cli.blender_note(True)
        assert len(pings) == 2 and "Blender MCP is off: new opener models can't be fetched. Open Blender, press N, " \
            "click Start MCP Server, then press Enter to retry (or S to skip)." in out.getvalue(), out.getvalue()
        pings.clear()
        builtins.input = lambda prompt="": (_ for _ in ()).throw(AssertionError("asked in a scripted run"))
        out = io.StringIO()
        with redirect_stdout(out):
            cli.blender_note(False)
        assert len(pings) == 1 and "Blender MCP is off" in out.getvalue()
        blender_link.ping = lambda timeout=2.0: True
        out = io.StringIO()
        with redirect_stdout(out):
            cli.blender_note(True)
        assert out.getvalue() == ""
    finally:
        blender_link.ping, builtins.input = old_ping, old_input


def test_search_failure_falls_back():
    with Env() as e:
        for f in config.LIBRARY.glob("polypizza_6NTegstc5Jy.*"):
            f.unlink()
        blender_link.ping = lambda timeout=2.0: True

        def broken(find):
            raise blender_link.LinkError("Unknown command type: search_polypizza_models")
        blender_link.search = broken
        clip, why = opener_render.render_opener(short(), 3.0, e.work, e.exe)
        assert clip is None and why.startswith("opener failed: model 'rooster' could not be searched"), why


def test_use_opener_never_raises():
    from shortsmaker import short_render
    old = opener_render.render_opener

    def boom(*a, **k):
        raise RuntimeError("boom")
    opener_render.render_opener = boom
    try:
        s = {"title": "x", "opener": copy.deepcopy(PLAN), "scenes": [{"full": None}]}
        assert short_render.use_opener(s, [0.0, 2.0], Path("."), {}, [None], ["x"]) == "opener failed: RuntimeError: boom"
    finally:
        opener_render.render_opener = old


def test_reuse_after_small_length_change():
    with Env() as e:
        s = short()
        opener_render.render_opener(s, 3.0, e.work, e.exe)
        clip, why = opener_render.render_opener(s, 3.012, e.work, e.exe)  # a voice a few ms longer
        assert why is None and clip.exists() and e.runs() == 1


def test_fix_round_gets_scaled_plan():
    with Env() as e:
        e.fail.write_text("in_frame: rooster leaves the frame on frames 50-54")
        seen = []
        opener_plan.fix_plan = lambda short, failures, seconds=None, scaled=None: seen.append((seconds, scaled)) or None
        opener_render.render_opener(short(), 1.8, e.work, e.exe)
        assert seen and abs(seen[0][0] - 1.8) < 0.04 and max(b["at"] for b in seen[0][1]["beats"]) <= 1.8



PERSON = {"buildable": True, "moment": "an officer strolls across a street with his umbrella",
          "set": {"ground": "stone", "backdrop": [], "light": "day"},
          "actors": [{"id": "officer", "person": "ww2_british_officer", "facing": "right", "prop": "umbrella"}],
          "beats": [{"move": "walk", "actor": "officer", "at": 0.3, "toward": "left"}],
          "camera": {"angle": "side", "follow": "officer"}}


def _people_files(e, present: bool):
    saved = (config.PEOPLE_BLEND, config.PEOPLE_JSON)
    config.PEOPLE_BLEND, config.PEOPLE_JSON = e.dir / "people.blend", e.dir / "people.json"
    if present:
        config.PEOPLE_BLEND.write_text("x")
        config.PEOPLE_JSON.write_text("{}")
    return saved


def test_people_library_missing():
    with Env() as e:
        saved = _people_files(e, present=False)
        try:
            clip, why = opener_render.render_opener({"title": "Umbrella", "opener": copy.deepcopy(PERSON)}, 3.0, e.work, e.exe)
        finally:
            config.PEOPLE_BLEND, config.PEOPLE_JSON = saved
        assert clip is None and why == "opener failed: people library missing", why
        assert e.runs() == 0


def test_missing_prop_model():
    with Env() as e:
        saved = _people_files(e, present=True)
        blender_link.ping = lambda timeout=2.0: False
        try:
            clip, why = opener_render.render_opener({"title": "Umbrella", "opener": copy.deepcopy(PERSON)}, 3.0, e.work, e.exe)
        finally:
            config.PEOPLE_BLEND, config.PEOPLE_JSON = saved
        assert clip is None and why == "opener failed: model 'umbrella' not in the library and Blender is off", why


def test_person_job_has_library():
    with Env() as e:
        saved = _people_files(e, present=True)
        p = copy.deepcopy(PERSON)
        p["actors"][0]["prop"] = "axe"  # in the test library
        try:
            opener_render.render_opener({"title": "Umbrella", "opener": p}, 3.0, e.work, e.exe)
            job = json.loads(e.lastjob.read_text())
        finally:
            config.PEOPLE_BLEND, config.PEOPLE_JSON = saved
        assert job["people"] == {"blend": str(e.dir / "people.blend"), "json": str(e.dir / "people.json")}, job.get("people")
        assert "officer" not in job["models"] and job["models"]["officer:prop"].endswith(".blend"), job["models"]



def test_unfound_model_goes_back_to_the_planner():
    """The first people run (umbrella officer) asked for a "ww2 armored car" no free library has and lost the whole
    opener: a model that can't be found goes back to the planner like any failure."""
    with Env() as e:
        blender_link.ping = lambda timeout=2.0: True
        blender_link.search = lambda find: []  # nothing found for anything not in the library
        s = short()
        s["opener"]["actors"][1]["find"] = "ww2 armored car"
        fixed = copy.deepcopy(PLAN)  # the planner swaps it for something the library has
        opener_plan.fix_plan = lambda short, failures, seconds=None, scaled=None: e.fixes.append(list(failures)) or copy.deepcopy(fixed)
        clip, why = opener_render.render_opener(s, 3.0, e.work, e.exe)
        assert why is None and clip.exists(), why
        assert e.fixes and "ww2 armored car" in e.fixes[0][0], e.fixes



def test_every_unfound_model_named_at_once():
    """Rounds went one missing model at a time (armoured car, then bricks, then a ruined house) and ran out: every
    model no library has is named in the same round."""
    with Env() as e:
        blender_link.ping = lambda timeout=2.0: True
        blender_link.search = lambda find: []
        p = copy.deepcopy(PLAN)
        p["actors"][1]["find"], p["set"]["backdrop"] = "ww2 armored car", [{"find": "ruined brick house", "size_m": 8}]
        models, why = opener_render.resolve_models(p)
        assert models == {} and "ww2 armored car" in why and "ruined brick house" in why, why


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
