"""Codex subscription calls and the Gemini/Codex pair. No network or AI usage."""
import os
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import channel_profiles, llm, session, writing


def test_codex_uses_subscription_stdin_and_read_only_images():
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        (folder / "sheet.png").write_bytes(b"png")
        (folder / "private.txt").write_text("not an image")
        response = subprocess.CompletedProcess([], 0, '{"ok":true}', "")
        with patch.object(llm.shutil, "which", return_value="codex"), \
             patch.object(llm.subprocess, "run", return_value=response) as run, \
             patch.dict(os.environ, {"OPENAI_API_KEY": "not-for-this-job", "CODEX_API_KEY": "not-for-this-job"}):
            assert llm.run_codex("Return JSON only", folder) == '{"ok":true}'
        cmd = run.call_args.args[0]
        opts = run.call_args.kwargs
        assert cmd[:2] == ["codex", "exec"] and cmd[-1] == "-"
        assert "Return JSON only" in opts["input"] and "Return JSON only" not in cmd
        assert cmd[cmd.index("--sandbox") + 1] == "read-only"
        assert "--ephemeral" in cmd and "--ignore-user-config" in cmd
        assert 'forced_login_method="chatgpt"' in cmd and "features.shell_tool=false" in cmd
        assert "OPENAI_API_KEY" not in opts["env"] and "CODEX_API_KEY" not in opts["env"]
        assert str(folder / "sheet.png") in cmd and str(folder / "private.txt") not in cmd


def test_codex_failure_is_bounded():
    with patch.object(llm.shutil, "which", return_value="codex"):
        for failure in (subprocess.TimeoutExpired("codex", 900), OSError("missing executable")):
            with patch.object(llm.subprocess, "run", side_effect=failure):
                assert llm.run_codex("task") is None
        with patch.object(llm.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "", "usage limit reached")):
            assert llm.quota_exhausted(llm.run_codex("task"))


def test_gemini_modes_choose_codex_and_keep_editor_choice():
    old = session.BRAIN, session.SOLO, session.PARTNER
    try:
        for choice in ("gemini", "gemini-only"):
            channel_profiles.configure_brain(choice)
            assert session.BRAIN == "gemini" and session.PARTNER == "codex"
            assert session.SOLO == (choice == "gemini-only")
            assert llm.other_ai("gemini") == "codex"
            assert llm.other_ai("codex") == "gemini"
    finally:
        session.BRAIN, session.SOLO, session.PARTNER = old


def test_codex_cold_reader_and_quota_fallback_never_call_claude():
    old = session.BRAIN, session.SOLO, session.PARTNER, session.NO_QUOTA, session.LAST_AI
    try:
        channel_profiles.configure_brain("gemini-only")
        session.NO_QUOTA = set()
        reply = '{"shorts":[{"index":0,"question":"Why?","answer":2}]}'
        with patch.object(llm.shutil, "which", side_effect=lambda name: name), \
             patch.object(llm, "run_codex", return_value=reply) as codex, \
             patch.object(llm, "run_agy", return_value=reply) as gemini, \
             patch.object(llm.subprocess, "run", side_effect=AssertionError("Claude must not run")):
            result = writing.cold_read([{"lines": ["He stayed.", "He was paid."]}])
            assert result[0]["reviewer"] == "codex" and codex.call_count == 1 and gemini.call_count == 0
            codex.return_value = "usage limit reached"
            result = writing.cold_read([{"lines": ["He stayed.", "He was paid."]}])
            assert result[0]["reviewer"] == "gemini" and "codex" in session.NO_QUOTA
            before = codex.call_count
            writing.cold_read([{"lines": ["He stayed.", "He was paid."]}])
            assert codex.call_count == before
            assert session.BRAIN == "gemini" and session.SOLO
    finally:
        session.BRAIN, session.SOLO, session.PARTNER, session.NO_QUOTA, session.LAST_AI = old


if __name__ == "__main__":
    names = [n for n in sorted(globals()) if n.startswith("test_")]
    failed = 0
    for name in names:
        try:
            globals()[name]()
            print(f"PASS {name}")
        except Exception:
            failed += 1
            traceback.print_exc()
    print(f"{len(names) - failed}/{len(names)} passed")
    sys.exit(bool(failed))
