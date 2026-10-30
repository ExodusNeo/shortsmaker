"""Each channel's own rules (channels/<name>.rules.md, 2026-10-22): the niche's topic, story, picture and directing
rules, read by heading into session.RULES, so a new channel never changes another channel's Shorts. The owner
can read and edit the file; a draft (status: draft) or a missing section stops the run before anything is made."""

import json
import re
from pathlib import Path

from shortsmaker import llm, session
from shortsmaker.config import CHANNELS, MAX_FULL, MAX_FULL_PLANNED

REQUIRED = ("Settings", "Topic picking", "Story rules", "Writing for the picture", "Lessons from our numbers",
            "Opening picture", "Picture picking", "Directing", "First-second check", "AI paintings")
BLENDER_SECTION = "Build plan"  # the engineer's instructions, needed only with visuals: blender
HEADING = re.compile(r"^##(?!#)\s*(.*?)\s*$")
TAG = re.compile(r"^\s*<!--.*?-->\s*", re.S)  # "<!-- copied from strange-history -->": for the owner, not the AI


def parse_rules(text: str, label: str) -> tuple[dict[str, str], dict[str, str]]:
    """(sections by canonical heading, settings) of a rules file; `label` names the file in stop messages."""
    canon = {h.lower(): h for h in REQUIRED + (BLENDER_SECTION,)}
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
    settings = {}
    for line in sections.get("Settings", "").split("\n"):
        m = re.match(r"\s*([^:=]+?)\s*[:=]\s*(.*?)\s*$", line)  # "status: ready" or "status = ready"
        if m:
            settings[m.group(1).lower()] = m.group(2).lower()
    for h in REQUIRED + ((BLENDER_SECTION,) if settings.get("visuals") == "blender" else ()):
        if not sections.get(h, "").strip():
            raise SystemExit(f'Stopped: {label} has no "## {h}" section.')
    if settings.get("status") != "ready":
        raise SystemExit(f'Stopped: {label} is a draft. Read it, edit anything you want, then change "status: draft" '
                         'to "status: ready".')
    if settings.get("visuals") not in ("photos", "blender"):
        raise SystemExit(f'Stopped: {label}: visuals must be "photos" or "blender", not "{settings.get("visuals", "")}".')
    for key, allowed in (("opener", ("animated", "none")), ("hook", ("moment", "money_claim"))):  # optional
        if key in settings and settings[key] not in allowed:
            raise SystemExit(f'Stopped: {label}: {key} must be {" or ".join(map(repr, allowed))}, not "{settings[key]}".')
    if not re.fullmatch(r"[0-9]+", settings.get("min_real_pictures", "")) or int(settings["min_real_pictures"]) < 1:
        raise SystemExit(f"Stopped: {label}: min_real_pictures must be a whole number above 0.")
    # catalog_pool() asks for these fields with this section's text; without them every "hook" came back false
    # (weird-economics 2026-10-26: 1 opener in 231 pictures, and the Short opened on a generic plane)
    missing = [f for f in ("era_ok", "sharp", "hook") if not re.search(rf"^\s*-\s*{f}:", sections["Opening picture"], re.M)]
    if missing:
        raise SystemExit(f'Stopped: {label}: "## Opening picture" must define each field on a "- name:" line; '
                         f'missing: {", ".join(missing)}.')
    return sections, settings


def load_rules(name: str) -> None:
    """Read and check channels/<name>.rules.md into session.RULES / session.RULE_SETTINGS (no file = no Settings)."""
    path = CHANNELS / f"{name}.rules.md"
    text = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    session.RULES, session.RULE_SETTINGS = parse_rules(text, f"channels/{name}.rules.md")


PURPOSE = {  # what each section is for, told to the AI that drafts a new channel's rules
    "Topic picking": "how the planner picks topics: what makes a story worth a Short in this niche, who or what it follows",
    "Story rules": "how a script is told: hook, pacing, how beats link, where the payoff goes, with an example",
    "Writing for the picture": "how the writer ties lines to what can be shown on screen",
    "Lessons from our numbers": "what the channel's own YouTube numbers taught (a new channel: what to watch for)",
    "Opening picture": "the picture checker's rules as three lines \"- era_ok:\", \"- sharp:\" and \"- hook:\": a "
                       "picture's fit, its sharpness and whether it can open the Short",
    "Picture picking": "what the visual editor wants for scene 1's picture; it follows \"Scene 1 is the hook: give it "
                       "the single most striking candidate that fits the story\"",
    "Directing": "the director's rules for picking each scene's picture, search queries and shot notes, with examples",
    "First-second check": "what the first two seconds should show, finishing the sentence 'check whether another "
                          "scene's picture would open better: ...'",
    "AI paintings": "how an AI painting prompt is written: subject, setting, light, art medium, what to avoid",
    BLENDER_SECTION: "only for visuals blender: how the engineer plans each Short's 3D build (which structure "
                     "template, the part that failed, the failure, the camera beat per scene, labels)",
}


def draft_rules(ch: dict, name: str) -> Path:
    """Draft channels/<name>.rules.md for a new channel: the AI copies the sections of existing channels' rules that
    fit the niche and adapts or writes the rest, tagging each. Always saved as a draft for the owner to read."""
    path = CHANNELS / f"{name}.rules.md"
    if path.exists():
        raise SystemExit(f"Stopped: channels/{name}.rules.md already exists.")
    others = {p.name.removesuffix(".rules.md"): p.read_text(encoding="utf-8-sig") for p in sorted(CHANNELS.glob("*.rules.md"))}
    wanted = [h for h in REQUIRED if h != "Settings"]
    prompt = f"""You set up the rules for a new faceless YouTube Shorts channel. Niche: {ch.get('niche')}.
Audience: {ch.get('audience', '')}. Tone: {ch.get('tone', '')}.
Its scripts, picture choices and edits are planned by AI with these rule sections:
{chr(10).join(f"- {h}: {PURPOSE[h]}" for h in wanted + [BLENDER_SECTION])}
Our other channels' rules files: {json.dumps(others, ensure_ascii=False)}
For every section: when another channel's section fits this niche, copy it word for word (tag "copied from
<channel>"); when part of it fits, adapt it (tag "adapted from <channel>: <what changed, one line>"); otherwise
write it new (tag "new"). Keep the same level of detail and examples as the existing rules, about this niche.
visuals: "photos" (real archival photos and film) or "blender" (3D drawn scenes). min_real_pictures: how many
usable real pictures a topic needs before it is written (a whole number).
Reply with ONLY JSON: {{"visuals": "photos", "min_real_pictures": 6,
"sections": {{"<section heading>": {{"tag": "...", "text": "..."}}}}}}"""
    reason = ""
    for _ in range(2):  # one retry on a bad reply
        data = llm.ask_ai(prompt + (f"\nYour last reply was unusable: {reason}. Send every section." if reason else ""),
                          fatal=False)
        got = data.get("sections") if isinstance(data, dict) else None
        need = wanted + ([BLENDER_SECTION] if isinstance(data, dict) and data.get("visuals") == "blender" else [])
        bad = [h for h in need if not (isinstance(got, dict) and isinstance(got.get(h), dict)
                                         and str(got[h].get("text") or "").strip())]
        if not bad:
            break
        reason = "no reply" if got is None else f"missing or empty: {', '.join(bad)}"
    else:
        raise SystemExit(f"Stopped: couldn't draft rules for {name}: {reason}")
    visuals = data.get("visuals") if data.get("visuals") in ("photos", "blender") else "photos"
    least = data.get("min_real_pictures")
    least = least if isinstance(least, int) and not isinstance(least, bool) and least > 0 else 6
    out = [f"# Rules: {name}\n\nEach section is read by its heading; edit the text under it. Change status to ready "
           "once you've read it.\n",
           f"## Settings\nstatus: draft\nvisuals: {visuals}\nmin_real_pictures: {least}\n"]
    for h in need:
        tag = " ".join(str(got[h].get("tag") or "new").replace("--", "-").split())
        text = re.sub(r"^##(?!#)", "###", str(got[h]["text"]).strip(), flags=re.M)  # its own "## " would split it
        out.append(f"## {h}\n<!-- {tag} -->\n{text}\n")
    path.write_text("\n".join(out), encoding="utf-8")
    return path


REVIEW = 'Rules drafted: channels/{}\nRead it, edit anything you want, then change "status: draft" to "status: ready" and run again.'


def require_rules(name: str) -> None:
    """load_rules, but a channel with no rules file yet (a failed draft, a profile copied in by hand) gets one
    drafted from its profile, and the run stops for the owner to read it."""
    if not (CHANNELS / f"{name}.rules.md").exists():
        ch = json.loads((CHANNELS / f"{name}.json").read_text(encoding="utf-8-sig"))
        raise SystemExit(REVIEW.format(draft_rules(ch, name).name))
    load_rules(name)


def min_real_pictures() -> int:
    """Usable real pictures/clips a topic needs, else a backup topic replaces it."""
    return int(session.RULE_SETTINGS["min_real_pictures"])


def max_full_planned() -> int:
    """Planned full-screen motion graphics allowed per Short (default MAX_FULL_PLANNED = 2)."""
    v = session.RULE_SETTINGS.get("max_full_planned", "")
    return int(v) if re.fullmatch(r"[0-9]+", v) and int(v) > 0 else MAX_FULL_PLANNED


def max_full() -> int:
    """Total full-screen motion graphics (planned + rescued) allowed per Short (default MAX_FULL = 3)."""
    v = session.RULE_SETTINGS.get("max_full", "")
    return int(v) if re.fullmatch(r"[0-9]+", v) and int(v) >= max_full_planned() else max(MAX_FULL, max_full_planned() + 1)
