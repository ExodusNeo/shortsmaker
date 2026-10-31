"""Settings that change during a run (who plans, quota-out agents, the channel's files, run.bat modes,
this Short's accent colours). Always read and set them as `session.NAME`."""

from pathlib import Path


CHANNEL = RESEARCH = LOG = Path()  # this batch's profile files, set by use_channel()
RULES: dict[str, str] = {}  # this channel's rules file by heading, and its "## Settings" (rules.load_rules)
RULE_SETTINGS: dict[str, str] = {}
YELLOW = (255, 221, 0)  # this Short's accent colour: render() sets it from the Short's palette
EMPHASIS = (255, 160, 0)  # the glowing emphasis word in the captions


BRAIN = "claude"  # who plans, writes and picks pictures: "claude" (Claude Code) or "gemini" (Google Antigravity
# CLI, `agy`, signed in with the owner's Google account). Chosen per batch in run.bat, saved in the profile.
# Gemini (agy image generator, Flash) paints the AI gap images and thumbnail art for either planner; SDXL is the backup.
SOLO = False  # one AI writes, edits, plans and reviews visuals; the independent story check can use the other AI
PARTNER = "claude"  # legacy pair for direct callers; configure_brain selects Codex for Gemini CLI runs
NO_QUOTA: set[str] = set()  # agents ("claude" / "gemini") that ran out of credits/quota during this run


LAST_AI = "claude"  # who answered the last ask_ai() call


SHORT_FORM = False  # run.bat question: shorter Shorts (~25-30 s), a test against the usual 40-50 s


VEO_HANDOFF = False  # run.bat question: the owner makes the AI clips in Google Flow (Veo, AI Pro credits)
