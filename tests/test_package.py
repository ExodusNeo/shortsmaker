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
    llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None: calls.append(prompt) or {"code": None}
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
