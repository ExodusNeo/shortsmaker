"""Each channel's own rules (channels/<name>.rules.md, 2026-10-22): the niche's topic, story, picture and directing
rules, read by heading into session.RULES, so a new channel never changes another channel's Shorts. The owner
can read and edit the file; a draft (status: draft) or a missing section stops the run before anything is made."""

import re

from shortsmaker import session
from shortsmaker.config import CHANNELS

REQUIRED = ("Settings", "Topic picking", "Story rules", "Writing for the picture", "Lessons from our numbers",
            "Opening picture", "Directing", "First-second check", "AI paintings")
HEADING = re.compile(r"^##(?!#)\s*(.*?)\s*$")
TAG = re.compile(r"^\s*<!--.*?-->\s*", re.S)  # "<!-- copied from strange-history -->": for the owner, not the AI


def parse_rules(text: str, label: str) -> tuple[dict[str, str], dict[str, str]]:
    """(sections by canonical heading, settings) of a rules file; `label` names the file in stop messages."""
    canon = {h.lower(): h for h in REQUIRED}
    sections: dict[str, str] = {}
    name, lines = None, []
    for line in text.lstrip("﻿").replace("\r\n", "\n").split("\n") + ["## "]:  # the sentinel closes the last
        m = HEADING.match(line)
        if not m:
            lines.append(line)
            continue
        if name is not None:
            if name in sections:
                raise SystemExit(f'Stopped: {label} has "## {name}" twice.')
            sections[name] = TAG.sub("", "\n".join(lines), count=1).strip("\n")
        name, lines = canon.get(m.group(1).lower(), m.group(1)), []
    for h in REQUIRED:
        if not sections.get(h, "").strip():
            raise SystemExit(f'Stopped: {label} has no "## {h}" section.')
    settings = {}
    for line in sections["Settings"].split("\n"):
        key, sep, value = line.partition(":")
        if sep:
            settings[key.strip().lower()] = value.strip().lower()
    if settings.get("status") != "ready":
        raise SystemExit(f'Stopped: {label} is a draft. Read it, edit anything you want, then change "status: draft" '
                         'to "status: ready".')
    if settings.get("visuals") == "blender":
        raise SystemExit(f"Stopped: {label} asks for Blender visuals, which aren't built yet.")
    if not settings.get("min_real_pictures", "").isdigit() or int(settings["min_real_pictures"]) < 1:
        raise SystemExit(f"Stopped: {label}: min_real_pictures must be a whole number.")
    return sections, settings


def load_rules(name: str) -> None:
    """Read and check channels/<name>.rules.md into session.RULES / session.RULE_SETTINGS (no file = no Settings)."""
    path = CHANNELS / f"{name}.rules.md"
    text = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    session.RULES, session.RULE_SETTINGS = parse_rules(text, f"channels/{name}.rules.md")


def min_real_pictures() -> int:
    """Usable real pictures/clips a topic needs, else a backup topic replaces it."""
    return int(session.RULE_SETTINGS["min_real_pictures"])
