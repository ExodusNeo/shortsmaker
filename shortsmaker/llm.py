"""Headless Claude Code / Gemini (agy) calls that return JSON, with automatic fallback when one fails or
runs out of quota."""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from shortsmaker import session
from shortsmaker.config import ROOT


# Pinned, not left to the CLI's defaults (the lean call skips the owner's settings), so no task can quietly get a
# weaker model. High is the highest effort the owner's Claude plan allows (owner, 2026-10-21).
CLAUDE_MODEL, CLAUDE_EFFORT = "opus", "high"
GEMINI_FALLBACK = "gemini-3.8-flash-high"
_gemini_model: str | None = None
_argon_exhausted: bool = False  # set True for the rest of this run if Argon returns RESOURCE_EXHAUSTED


def gemini_model() -> str:
    """Gemini 4 Argon once the owner's account has it (owner's wish), else Gemini 3.8 Flash; always high effort.
    If Argon hits its quota during this run (_argon_exhausted), uses Flash for the rest of the run."""
    global _gemini_model
    if _argon_exhausted:
        return GEMINI_FALLBACK
    if _gemini_model is None:
        try:
            out = subprocess.run([shutil.which("agy") or "agy", "models"], capture_output=True, text=True,
                                 encoding="utf-8", timeout=90).stdout or ""
        except (OSError, subprocess.TimeoutExpired):
            out = ""
        ids = [line.split()[0] for line in out.splitlines() if "\t" in line]
        argon = [m for m in ids if "argon" in m.lower()]
        _gemini_model = next((m for m in argon if m.endswith("high")), argon[0] if argon else GEMINI_FALLBACK)
    return _gemini_model


QUOTA_PATTERNS = (
    "you've hit your",
    "hit your weekly limit",
    "hit your daily limit",
    "hit your limit",
    "out of extra usage",
    "usage limit",
    "credit balance is too low",
    "insufficient_quota",
    "resource_exhausted",
    "quota exceeded",
    "rate_limit_error",
)


def quota_exhausted(text: str) -> bool:
    """True when a CLI reply is an account quota / credit / rate-limit error rather than a model answer."""
    low = (text or "").lower()
    return any(p in low for p in QUOTA_PATTERNS)


def run_agy(prompt: str, folder: Path, timeout: int = 900, model: str | None = None) -> str | None:
    """One headless Gemini turn. agy only takes the prompt inline on its command line (too short for ours,
    and it ignores stdin), so the prompt goes in a file inside `folder` that Gemini is told to read.
    `model` overrides the default (picture jobs use Flash: dozens of images per call would spend Argon's small
    weekly quota in one Short). If Argon's quota runs out during this run, the turn is retried on Flash and Flash
    is used for the rest of the run."""
    global _argon_exhausted
    agy = shutil.which("agy")
    if not agy:
        print("  Gemini (Antigravity's agy) isn't installed")
        return None
    model = model or gemini_model()
    folder.mkdir(parents=True, exist_ok=True)
    task = folder / f"task_{os.getpid()}_{time.time_ns()}.txt"
    task.write_text(prompt, encoding="utf-8")
    try:
        r = subprocess.run([agy, "--model", model, "--effort", "high", "--disable-slash-commands", "--add-dir", str(folder),
                            f"-p=Read the file {task} and do exactly what it says. Do not run any shell commands, "
                            "scripts, or inspect other files in the codebase. If files or images are listed in the "
                            "task, view them directly with read_file and immediately return the requested JSON. "
                            "Your whole reply must be what that file asks for, nothing else."],
                           capture_output=True, text=True, encoding="utf-8", timeout=timeout, cwd=folder)
    except subprocess.TimeoutExpired:
        return None
    finally:
        task.unlink(missing_ok=True)
    said = f"{r.stdout}\n{r.stderr}"
    if ("RESOURCE_EXHAUSTED" in said or quota_exhausted(said)) and model != GEMINI_FALLBACK:
        _argon_exhausted = True
        print(f"  {model}'s quota is used up: using {GEMINI_FALLBACK} for the rest of this run")
        return run_agy(prompt, folder, timeout, GEMINI_FALLBACK)
    if "RESOURCE_EXHAUSTED" in said or (not (r.stdout or "").strip() and quota_exhausted(said)):
        return said
    return r.stdout or said


def ask_ai(prompt: str, fatal: bool = True, read_dir: Path | None = None, brain: str | None = None,
           bulk: bool = False) -> dict | None:
    """Headless planner call (BRAIN, or `brain`: Claude or Gemini) that returns parsed JSON; with fatal=False, None
    on failure. Either agent automatically falls back to the other on failure or when out of credits/quota
    (and remembers exhausted quota in NO_QUOTA so later steps don't wait on the empty account). With read_dir,
    the AI may look at the images in that folder; `bulk` marks a job reading dozens of them, which Gemini runs on
    Flash (on Argon it would spend the small weekly quota in one Short)."""
    global _argon_exhausted
    first = brain or session.BRAIN
    if session.SOLO:
        order = [first]
    else:
        second = "gemini" if first == "claude" else "claude"
        order = [w for w in (first, second) if w not in session.NO_QUOTA] or [first, second]
    for idx, who in enumerate(order):
        name, exe = who.capitalize(), shutil.which("agy" if who == "gemini" else "claude")
        fallback = ("gemini" if who == "claude" else "claude").capitalize()
        if not exe:
            print(f"  {name} isn't installed ({'Antigravity agy' if who == 'gemini' else 'Claude Code'})")
            continue
        for attempt in range(2):
            if who == "gemini":
                cur_model = GEMINI_FALLBACK if (bulk or attempt > 0) else None
                out = run_agy(prompt, read_dir or ROOT / "agy_tasks", timeout=600 if bulk else 900, model=cur_model)
            else:
                # Lean call: no personal plugins, hooks or skill list (the owner's interactive setup has ~20
                # plugins/skills and output-rewriting hooks; a JSON-only planner call needs none of them), always
                # started in ROOT so per-Short work folders don't each become a Claude Code project.
                cmd = [exe, "-p", "--setting-sources", "project,local", "--disable-slash-commands",
                       "--model", CLAUDE_MODEL, "--effort", CLAUDE_EFFORT] + (
                    ["--allowedTools", "Read", "--add-dir", str(read_dir)] if read_dir else [])
                try:
                    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8",
                                       timeout=900, cwd=ROOT)
                    out = r.stdout if (r.stdout or "").strip() else f"{r.stdout or ''}\n{r.stderr or ''}"
                except subprocess.TimeoutExpired:
                    out = None
            if out is None:
                if who == "gemini" and not bulk and attempt == 0 and not _argon_exhausted:
                    _argon_exhausted = True
                    print(f"  Gemini main model timed out: switching to {GEMINI_FALLBACK} for the rest of this run")
                else:
                    print(f"  {name} timed out (try {attempt + 1}/2)")
                continue
            try:
                start, end = out.find("{"), out.rfind("}")
                if start >= 0 and end > start:
                    data = json.loads(out[start: end + 1])
                    session.LAST_AI = who
                    return data
            except json.JSONDecodeError:
                pass
            if quota_exhausted(out):
                session.NO_QUOTA.add(who)
                if session.SOLO:
                    print(f"  {name} has no credits/quota left for this solo run.")
                    break
                other = "gemini" if who == "claude" else "claude"
                if session.BRAIN == who and other not in session.NO_QUOTA:
                    session.BRAIN = other
                print(f"  {name} has no credits/quota left: switching to {fallback} for the rest of this run")
                break
            print(f"  {name} reply wasn't valid JSON (try {attempt + 1}/2)")
        if idx == 0 and len(order) > 1 and who not in session.NO_QUOTA:
            print(f"  {name} didn't give a usable answer, asking {fallback} instead")
    if fatal:
        sys.exit("The AI didn't return usable JSON. Run again.")
    return None
