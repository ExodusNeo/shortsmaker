"""The owner's logbook and the Obsidian vault pages."""

import re
import shutil
from pathlib import Path

from shortsmaker import media_tools, session
from shortsmaker.config import LOGBOOK, ROOT, VAULT


LOG_HEADER = """# Logbook: {name}

One entry per Short this program made, newest at the bottom. After you post one, fill in its numbers
from YouTube Studio (Content -> click the Short -> Analytics). A week after posting is a good time;
you can update the numbers later too. The next batch reads every entry with Views filled in and
learns from what worked.

- Stayed to watch (%): the "Viewed" share in the "Viewed vs. swiped away" card
- Average % viewed: can be over 100% when people rewatch
- Leave a line empty if you don't know it. Don't change the "## " title lines.
"""


def log_short(short: dict, folder: Path) -> None:
    """Add a finished Short to this channel's logbook, with empty lines for its YouTube numbers."""
    LOGBOOK.mkdir(parents=True, exist_ok=True)
    if not session.LOG.exists():
        session.LOG.write_text(LOG_HEADER.format(name=session.LOG.stem), encoding="utf-8")
    hook = re.split(r"(?<=[.!?])\s+", short["scenes"][0]["narration"].strip())[0]
    with session.LOG.open("a", encoding="utf-8") as f:
        f.write(f"""
## {short['title']}
Made: {folder.name[:10]} | Written by: {session.BRAIN.capitalize()} | Length: {media_tools.clock(media_tools.duration(folder / "short.mp4"))} | Folder: {folder.relative_to(ROOT)}
Topic: {short.get('topic') or short['title']} | Story shape: {short.get('shape') or '-'}
Hook line: "{hook}" | Hook title: {short.get('hook_text') or '-'}

Posted on:
Views:
Likes:
Comments:
Subscribers gained:
Stayed to watch (%):
Average % viewed:
My notes:
""")


VAULT_HOME = """# ShortsMaker

- Logbooks (fill in the YouTube numbers here): {logbooks}
- One page per Short: the `Shorts` folder, by channel
- Project notes: [HANDOFF.md]({handoff})
- Code map of the program: open `D:\\ShortsMaker\\code-map` as its own vault (made by graphify; rebuild it with /graphify)
"""


def vault_page(title: str, folder: Path, channel: str) -> None:
    """The Short's page in the Obsidian vault: thumbnail, storyboard, its logbook lines, upload text, and links to
    its logbook entry and output folder. Rebuilt on every call; the numbers live only in the logbook."""
    shorts = VAULT / "Shorts" / channel
    att = shorts / "attachments"
    att.mkdir(parents=True, exist_ok=True)
    pics = []
    for name, width in (("thumbnail.jpg", 300), ("storyboard.jpg", 640)):
        if (folder / name).exists():
            shutil.copy(folder / name, att / f"{folder.name}_{name}")
            pics.append(f"![[{folder.name}_{name}|{width}]]")
    log = LOGBOOK / f"{channel}.md"
    entry = next((e for e in (log.read_text(encoding="utf-8-sig").split("\n## ")[1:] if log.exists() else [])
                  if e.split("\n", 1)[0].strip() == title), "")
    facts = [ln for ln in entry.splitlines()[1:] if ln.startswith(("Made:", "Topic:", "Hook line:"))]
    upload = (folder / "upload.txt").read_text(encoding="utf-8").strip() if (folder / "upload.txt").exists() else "(no upload.txt)"
    heading = re.sub(r"[#|^\[\]]", " ", title).strip()  # characters a wiki link can't carry
    (shorts / f"{folder.name}.md").write_text(
        f"---\nchannel: {channel}\nmade: {folder.name[:10]}\n---\n# {title}\n\n" + "\n".join(pics)
        + f"\n\n**Logbook:** [[{channel}#{heading}|numbers and notes]] · **Files:** [open the Short's folder]({folder.as_uri()})\n\n"
        + "\n".join(f"- {ln}" for ln in facts) + f"\n\n## Upload text\n\n```text\n{upload}\n```\n", encoding="utf-8")
    home = VAULT / "Home.md"
    logbooks = ", ".join(f"[[{p.stem}]]" for p in sorted(LOGBOOK.glob("*.md")))
    home.write_text(VAULT_HOME.format(logbooks=logbooks, handoff=(ROOT / "HANDOFF.md").as_uri()), encoding="utf-8")


def vault_refresh() -> None:
    """make_shorts.py notes: rebuild every Short's vault page from the logbooks (each entry records its folder)."""
    for log in sorted(LOGBOOK.glob("*.md")):
        for e in log.read_text(encoding="utf-8-sig").split("\n## ")[1:]:
            folder = re.search(r"Folder: (\S[^|\n]*)", e)
            if folder and (ROOT / folder.group(1).strip()).is_dir():
                vault_page(e.split("\n", 1)[0].strip(), ROOT / folder.group(1).strip(), log.stem)
                print(f"  page: {log.stem} / {e.splitlines()[0][:60]}")


JUDGE_MIN_VIEWS = 100  # below this, a Short's watch percentages come from a handful of viewers


def logbook_results() -> str:
    """The logbook entries the owner has filled in (Views written down), at most the last 30. Entries under
    JUDGE_MIN_VIEWS get a note, or the planner learns from noise (Cardiff's 81% stayed-to-watch was 28 views)."""
    if not session.LOG.exists():
        return ""
    out = []
    for e in session.LOG.read_text(encoding="utf-8-sig").split("\n## ")[1:]:
        views = re.search(r"^Views:[ \t]*(\d[\d,]*)", e, re.M)
        if not views:
            continue
        entry = "## " + e.strip()
        if int(views.group(1).replace(",", "")) < JUDGE_MIN_VIEWS:
            entry += "\n(Too few views to judge: its Stayed to watch and Average % viewed come from a handful of viewers.)"
        out.append(entry)
    return "\n\n".join(out[-30:])
