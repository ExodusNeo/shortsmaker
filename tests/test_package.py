"""Tests for the shortsmaker package wiring (one owner per setting, fakes reach every caller). No AI usage.
Run: .venv\\Scripts\\python.exe tests\\test_package.py"""
import os
import shutil
import sys
import tempfile
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from shortsmaker import audio_mix, cli, config, llm, media_tools, motion, session  # noqa: E402


def test_root():
    assert config.ROOT == REPO, config.ROOT
    assert (config.ROOT / "remotion").exists()


def test_ffmpeg_on_path():
    assert str(config.ROOT / "ffmpeg") in os.environ["PATH"].split(os.pathsep)


def test_session_shared():
    old = session.BRAIN, session.LAST_AI, set(session.NO_QUOTA), llm.run_agy, shutil.which
    session.BRAIN, session.NO_QUOTA = "gemini", set()
    llm.run_agy = lambda prompt, folder, timeout=900, model=None: '{"ok": 1}'
    shutil.which = lambda name: name
    try:
        assert llm.ask_ai("plan this") == {"ok": 1}
        assert session.LAST_AI == "gemini"
    finally:
        session.BRAIN, session.LAST_AI, session.NO_QUOTA, llm.run_agy, shutil.which = old


def test_fake_reaches_callers():
    gen = config.REMOTION / "src" / "full" / "generated" / "Custom0.tsx"
    saved, old_ask, calls = gen.read_bytes(), llm.ask_ai, []  # bytes: put it back exactly (git sees CRLF changes)
    llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: calls.append(prompt) or {"code": None}
    try:
        with tempfile.TemporaryDirectory() as d:
            short = {"title": "T", "scenes": [{"narration": "One, then two, then three.",
                                               "full": {"type": "custom", "brief": "Three step chain"}}]}
            scenes = [{"start": 0.0, "end": 3.0, "full": {"type": "custom", "slot": 0, "kind": "flow", "skin": "hud",
                                                          "seed": 1, "title": "T", "cues": [0.5, 1.5, 2.5]}}]
            motion.code_custom_scenes(short, scenes, Path(d))
            assert calls, "motion must call the fake installed on llm"
            assert "THREE STEP CHAIN" in (Path(d) / "Custom0.tsx").read_text(encoding="utf-8")  # the fallback scene
    finally:
        llm.ask_ai = old_ask
        gen.write_bytes(saved)


def test_claude_pinned_to_opus_high():
    import subprocess
    assert llm.CLAUDE_MODEL == "opus" and llm.CLAUDE_EFFORT in ("high", "xhigh", "max"), "never below Opus at high"
    old = session.BRAIN, set(session.NO_QUOTA), subprocess.run, shutil.which
    seen = []
    session.BRAIN, session.NO_QUOTA = "claude", set()
    subprocess.run = lambda cmd, **kw: seen.append(cmd) or type("R", (), {"stdout": '{"ok": 1}', "stderr": ""})()
    shutil.which = lambda name: name
    try:
        assert llm.ask_ai("plan this") == {"ok": 1}
    finally:
        session.BRAIN, session.NO_QUOTA, subprocess.run, shutil.which = old
    cmd = seen[0]
    assert cmd[cmd.index("--model") + 1] == "opus" and cmd[cmd.index("--effort") + 1] == "high", cmd


def test_gemini_reviews_get_the_main_model_bulk_pictures_flash():
    old = session.BRAIN, set(session.NO_QUOTA), llm.run_agy, shutil.which
    models = []
    session.BRAIN, session.NO_QUOTA = "gemini", set()
    llm.run_agy = lambda prompt, folder, timeout=900, model=None: models.append(model) or '{"ok": 1}'
    shutil.which = lambda name: name
    try:
        with tempfile.TemporaryDirectory() as d:
            llm.ask_ai("review these frames", read_dir=Path(d))
            llm.ask_ai("pick from 40 pictures", read_dir=Path(d), bulk=True)
    finally:
        session.BRAIN, session.NO_QUOTA, llm.run_agy, shutil.which = old
    assert models == [None, llm.GEMINI_FALLBACK], models  # None = gemini_model(): Argon when the account has it


def test_argon_out_of_quota_switches_to_flash():
    import subprocess
    old = (llm._gemini_model, llm._argon_exhausted, subprocess.run, shutil.which, session.BRAIN, set(session.NO_QUOTA))
    asked = []

    def fake_run(cmd, **kw):
        model = cmd[cmd.index("--model") + 1]
        asked.append(model)
        out = "RESOURCE_EXHAUSTED: weekly quota" if model != llm.GEMINI_FALLBACK else '{"ok": 1}'
        return type("R", (), {"stdout": out, "stderr": ""})()
    llm._gemini_model, llm._argon_exhausted = "gemini-4-argon-high", False
    subprocess.run, shutil.which = fake_run, (lambda name: name)
    session.BRAIN, session.NO_QUOTA = "gemini", set()
    try:
        with tempfile.TemporaryDirectory() as d:
            assert llm.ask_ai("review these frames", read_dir=Path(d)) == {"ok": 1}  # a review picture job, on Argon first
        assert asked == ["gemini-4-argon-high", llm.GEMINI_FALLBACK], asked
        assert llm.gemini_model() == llm.GEMINI_FALLBACK  # the rest of the run stays on Flash
    finally:
        llm._gemini_model, llm._argon_exhausted, subprocess.run, shutil.which, session.BRAIN, session.NO_QUOTA = old


def test_run_agy_flags_and_boundaries():
    import subprocess
    seen = []
    old_run = subprocess.run
    old_which = shutil.which
    subprocess.run = lambda cmd, **kw: seen.append((cmd, kw)) or type("R", (), {"stdout": '{"ok": 1}', "stderr": ""})()
    shutil.which = lambda name: "agy.cmd" if name == "agy" else name
    try:
        with tempfile.TemporaryDirectory() as d:
            f = Path(d)
            res = llm.run_agy("test prompt", f, timeout=120, model="gemini-4-argon-high")
            assert res == '{"ok": 1}'
    finally:
        subprocess.run, shutil.which = old_run, old_which
    assert seen, "subprocess.run should have been called"
    cmd, kw = seen[0]
    assert "--disable-slash-commands" in cmd, f"--disable-slash-commands missing from agy cmd: {cmd}"
    assert "--model" in cmd and cmd[cmd.index("--model") + 1] == "gemini-4-argon-high"
    assert kw.get("timeout") == 120
    p_arg = [arg for arg in cmd if arg.startswith("-p=")][0]
    assert "Do not run any shell commands" in p_arg
    assert "read_file" in p_arg


def test_gemini_timeout_switches_to_flash():
    import subprocess
    old = (llm._gemini_model, llm._argon_exhausted, subprocess.run, shutil.which, session.BRAIN, set(session.NO_QUOTA))
    asked = []

    def fake_run(cmd, **kw):
        model = cmd[cmd.index("--model") + 1]
        asked.append(model)
        if model != llm.GEMINI_FALLBACK:
            raise subprocess.TimeoutExpired(cmd, kw.get("timeout", 180))
        return type("R", (), {"stdout": '{"ok": 1}', "stderr": ""})()

    llm._gemini_model, llm._argon_exhausted = "gemini-4-argon-high", False
    subprocess.run, shutil.which = fake_run, (lambda name: name)
    session.BRAIN, session.NO_QUOTA = "gemini", set()
    try:
        with tempfile.TemporaryDirectory() as d:
            assert llm.ask_ai("review these frames", read_dir=Path(d)) == {"ok": 1}
        assert asked == ["gemini-4-argon-high", llm.GEMINI_FALLBACK], asked
        assert llm.gemini_model() == llm.GEMINI_FALLBACK  # the rest of the run stays on Flash
    finally:
        llm._gemini_model, llm._argon_exhausted, subprocess.run, shutil.which, session.BRAIN, session.NO_QUOTA = old


def test_encoder_cache_lives_with_video_encoder():
    assert not hasattr(audio_mix, "_encoder"), "the encoder cache belongs to media_tools"
    old = list(media_tools._encoder)
    media_tools._encoder[:] = ["-c:v", "cached"]
    try:
        assert media_tools.video_encoder() == ["-c:v", "cached"]  # chosen once per run, ffmpeg isn't asked again
    finally:
        media_tools._encoder[:] = old


def test_entry_point():
    import make_shorts
    assert make_shorts.main is cli.main


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
