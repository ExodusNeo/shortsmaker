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


def test_person_card_hold_and_exit_gap():
    import io
    from PIL import Image
    from shortsmaker import editplan
    buf = io.BytesIO()
    Image.new("RGB", (100, 100), "white").save(buf, format="JPEG")
    fake_jpg = buf.getvalue()
    words = [(0.0, 0.4, "his"), (0.4, 0.8, "cousin"), (0.8, 1.2, "Virginia"), (1.2, 1.6, "Woolf")]
    sc = {"graphic": None, "emphasis": None, "person": {"name": "Virginia Woolf", "trigger": "Virginia Woolf"}}
    cue = editplan.scene_cues(sc, words, 0.0, 5.0, 1, (fake_jpg, "photo.jpg", None))
    assert cue.get("card") is not None
    assert cue["off"] - cue["on"] >= 2.0, f"Card duration too short: {cue['off'] - cue['on']}"
    assert 5.0 - cue["off"] >= 0.35, f"Not enough breathing room before scene transition: {5.0 - cue['off']}"


def test_scene_hold_padding():
    from shortsmaker import plan_rules, editplan
    # Simulate a scene with a full-screen motion graphic:
    # 2.5s speech, ends at 2.4s. Only needs a subtle micro-settle (at most 0.25s) to avoid dead air pauses.
    words = [(0.0, 0.5, "Navy"), (0.6, 1.2, "flagship"), (1.3, 2.4, "telegram")]
    dur = 2.5
    last_word = words[-1][1]
    tail = max(0.0, dur - last_word)  # 0.1s
    needed = max(0.0, 0.25 - tail)    # 0.15s
    pad = min(0.25, needed)
    assert 0.1 <= pad <= 0.25, f"Full scene settle padding should be subtle, not a dead stall: {pad}"

    # Simulate a person card in a short scene (1.4s):
    short_dur = 1.4
    pad_needed = max(0.0, 1.6 - short_dur)  # 0.2s
    pad = min(0.25, pad_needed)
    assert 0.15 <= pad <= 0.25, f"Short scene person card pad should be tight: {pad}"

    # A normal-length scene (2.3s) with a late trigger (1.6s) starts the card early and needs 0s padding
    sc = {"graphic": None, "emphasis": None, "person": {"name": "Douglas Bader", "trigger": "Douglas Bader"}}
    late_words = [(0.0, 0.4, "British"), (0.4, 0.8, "ace"), (1.2, 1.6, "Douglas"), (1.6, 2.0, "Bader")]
    import io
    from PIL import Image
    buf = io.BytesIO()
    Image.new("RGB", (100, 100), "white").save(buf, format="JPEG")
    fake_jpg = buf.getvalue()
    cue = editplan.scene_cues(sc, late_words, 0.0, 2.3, 1, (fake_jpg, "photo.jpg", None))
    assert cue.get("card") is not None
    assert cue["on"] <= 0.5, f"Card should start early in the scene rather than waiting for late trigger: {cue['on']}"
    assert cue["off"] - cue["on"] >= 1.5, f"Card duration on screen should be readable: {cue['off'] - cue['on']}"


def test_graphic_card_hold_duration():
    from shortsmaker import editplan
    # Late trigger in a 2.7s scene with a stamp card: starts early to ensure >= 1.8s hold time
    stamp_words = [(0.0, 0.5, "blinding"), (0.5, 0.8, "the"), (0.8, 1.2, "driver"),
                   (1.3, 1.7, "and"), (1.7, 2.1, "knocking"), (2.1, 2.5, "the"), (2.5, 2.7, "out")]
    sc_stamp = {"graphic": {"style": "stamp", "text": "KNOCKED OUT", "trigger": "knocking the out"},
                "emphasis": None, "person": None}
    cue = editplan.scene_cues(sc_stamp, stamp_words, 0.0, 2.7, 2, None)
    at = cue["graphic"]
    # Even though "knocking" was spoken at 1.7s, card shifts earlier to give at least 1.8s hold before end - 0.25
    assert (2.7 - 0.25) - at >= 1.8 - 1e-6, f"Stamp card hold time too short: {(2.7 - 0.25) - at}"
    assert at <= 0.65 + 1e-6, f"Stamp card should shift early in the scene: {at}"

    # Late trigger in a 1.9s scene with kinetic title: starts early to maximize hold
    kinetic_words = [(0.0, 0.4, "shoved"), (0.4, 0.8, "the"), (0.8, 1.1, "tip"),
                     (1.1, 1.4, "viewing"), (1.4, 1.8, "slit")]
    sc_kinetic = {"graphic": {"style": "kinetic", "text": "VIEWING SLIT", "trigger": "viewing slit"},
                  "emphasis": None, "person": None}
    cue_k = editplan.scene_cues(sc_kinetic, kinetic_words, 0.0, 1.9, 1, None)
    at_k = cue_k["graphic"]
    assert (1.9 - 0.25) - at_k >= 1.4, f"Kinetic title hold time too short: {(1.9 - 0.25) - at_k}"
    assert abs(at_k - 0.2) < 1e-6, f"Kinetic title should start at scene earliest bound: {at_k}"


def test_solo_brain_selection_options():
    from shortsmaker import channel_profiles
    assert channel_profiles.BRAINS == ["claude-only", "gemini-only", "claude", "gemini", "both"]

    # Test number selections 1-5
    import builtins
    old_input = builtins.input
    try:
        builtins.input = lambda prompt="": "1"
        assert channel_profiles.ask_brain("claude") == "claude-only"
        builtins.input = lambda prompt="": "2"
        assert channel_profiles.ask_brain("claude") == "gemini-only"
        builtins.input = lambda prompt="": "3"
        assert channel_profiles.ask_brain("claude") == "claude"
        builtins.input = lambda prompt="": "4"
        assert channel_profiles.ask_brain("claude") == "gemini"
        builtins.input = lambda prompt="": "5"
        assert channel_profiles.ask_brain("claude") == "both"
        # Test default Enter preserving last choice
        builtins.input = lambda prompt="": ""
        assert channel_profiles.ask_brain("claude-only") == "claude-only"
        assert channel_profiles.ask_brain("gemini-only") == "gemini-only"
        assert channel_profiles.ask_brain("claude") == "claude"
        assert channel_profiles.ask_brain("gemini") == "gemini"
        assert channel_profiles.ask_brain("both") == "both"
    finally:
        builtins.input = old_input


def test_solo_edit_scripts_uses_same_ai():
    from shortsmaker import writing
    old_ask, old_brain, old_solo, old_rules = llm.ask_ai, session.BRAIN, session.SOLO, dict(session.RULES)
    session.RULES["Story rules"] = "Be gripping"
    called_brains = []
    llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: (
        called_brains.append(brain) if prompt.startswith("You are the script editor") else None) or {
        "shorts": [{"index": 0, "scenes": ["Scene 1 narration"], "title": "T", "hook_text": "H", "thumbnail_text": "Th", "notes": []}]
    }
    try:
        # Collaborative mode: Claude writer -> Gemini editor
        session.BRAIN, session.SOLO = "claude", False
        shorts = [{"topic": "Top", "title": "T", "lines": ["Line 1"], "hook_options": ["Opt 1"]}]
        writing.edit_scripts(shorts, {"niche": "niche"})
        assert called_brains[-1] == "gemini", f"Collaborative Claude should use Gemini editor, got: {called_brains[-1]}"

        # Solo Claude mode: Claude writer -> Claude editor
        session.BRAIN, session.SOLO = "claude", True
        writing.edit_scripts(shorts, {"niche": "niche"})
        assert called_brains[-1] == "claude", f"Solo Claude should use Claude editor, got: {called_brains[-1]}"

        # Solo Gemini mode: Gemini writer -> Gemini editor
        session.BRAIN, session.SOLO = "gemini", True
        writing.edit_scripts(shorts, {"niche": "niche"})
        assert called_brains[-1] == "gemini", f"Solo Gemini should use Gemini editor, got: {called_brains[-1]}"
    finally:
        llm.ask_ai, session.BRAIN, session.SOLO, session.RULES = old_ask, old_brain, old_solo, old_rules


def test_solo_ask_ai_never_falls_back():
    import subprocess
    old_run, old_agy, old_brain, old_solo, old_no_quota = subprocess.run, llm.run_agy, session.BRAIN, session.SOLO, set(session.NO_QUOTA)
    claude_called = []
    gemini_called = []
    subprocess.run = lambda cmd, **kw: claude_called.append(cmd) or type("R", (), {"stdout": "invalid json", "stderr": ""})()
    llm.run_agy = lambda prompt, folder, timeout=900, model=None: gemini_called.append(prompt) or "invalid json"
    shutil_which = shutil.which
    shutil.which = lambda name: name
    try:
        # Solo Claude: when Claude returns invalid JSON, it retries Claude, never asks Gemini
        session.BRAIN, session.SOLO, session.NO_QUOTA = "claude", True, set()
        ans = llm.ask_ai("test prompt", fatal=False)
        assert ans is None
        assert len(claude_called) == 2, f"Claude should be retried twice, got: {len(claude_called)}"
        assert len(gemini_called) == 0, f"Gemini must not be called in solo Claude mode, got: {len(gemini_called)}"

        # Solo Gemini: when Gemini returns invalid JSON, it retries Gemini, never asks Claude
        claude_called.clear()
        gemini_called.clear()
        session.BRAIN, session.SOLO, session.NO_QUOTA = "gemini", True, set()
        ans = llm.ask_ai("test prompt", fatal=False)
        assert ans is None
        assert len(gemini_called) == 2, f"Gemini should be retried twice, got: {len(gemini_called)}"
        assert len(claude_called) == 0, f"Claude must not be called in solo Gemini mode, got: {len(claude_called)}"
    finally:
        subprocess.run, llm.run_agy, session.BRAIN, session.SOLO, session.NO_QUOTA, shutil.which = old_run, old_agy, old_brain, old_solo, old_no_quota, shutil_which


def test_solo_ask_ai_hands_over_when_out_of_credits():
    import subprocess
    old_run, old_agy, old_brain, old_solo, old_no_quota = subprocess.run, llm.run_agy, session.BRAIN, session.SOLO, set(session.NO_QUOTA)
    claude_called, gemini_called = [], []
    subprocess.run = lambda cmd, **kw: claude_called.append(cmd) or type("R", (), {"stdout": "", "stderr": "You've hit your limit"})()
    llm.run_agy = lambda prompt, folder, timeout=900, model=None: gemini_called.append(prompt) or '{"ok": 1}'
    shutil_which = shutil.which
    shutil.which = lambda name: name
    try:
        # Solo Claude out of credits: Gemini answers and carries on solo for the rest of the run
        session.BRAIN, session.SOLO, session.NO_QUOTA = "claude", True, set()
        assert llm.ask_ai("test prompt", fatal=False) == {"ok": 1}
        assert len(claude_called) == 1 and len(gemini_called) == 1
        assert session.BRAIN == "gemini" and session.SOLO
        llm.ask_ai("next step", fatal=False)
        assert len(claude_called) == 1, "the empty account must not be asked again"
    finally:
        subprocess.run, llm.run_agy, session.BRAIN, session.SOLO, session.NO_QUOTA, shutil.which = old_run, old_agy, old_brain, old_solo, old_no_quota, shutil_which





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
