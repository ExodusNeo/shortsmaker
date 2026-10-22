"""Channel profiles (channels/<name>.json), the run.bat menus, and YouTube/trend research."""

import json
import logging
import re
import sys
import time
from datetime import date

from shortsmaker import llm, rules, session
from shortsmaker.config import CHANNELS, LOGBOOK, VOICES


def use_channel(name: str) -> None:
    session.CHANNEL, session.RESEARCH = CHANNELS / f"{name}.json", CHANNELS / f"{name}.research.json"
    session.LOG = LOGBOOK / f"{name}.md"
    CHANNELS.mkdir(exist_ok=True)
    (CHANNELS / "last.txt").write_text(name, encoding="utf-8")


def pick_channel() -> str:
    """Ask which channel this batch is for (Enter = the one used last time), or set up a new one."""
    CHANNELS.mkdir(exist_ok=True)
    names = sorted(p.stem for p in CHANNELS.glob("*.json") if not p.stem.endswith(".research"))
    last = (CHANNELS / "last.txt").read_text(encoding="utf-8").strip() if (CHANNELS / "last.txt").exists() else ""
    default = names.index(last) + 1 if last in names else (1 if names else len(names) + 1)
    print("Which channel?")
    for k, name in enumerate(names, 1):
        made = len(json.loads((CHANNELS / f"{name}.json").read_text(encoding="utf-8-sig")).get("done_topics", []))
        print(f"  {k}) {name}   ({made} Shorts made)")
    print(f"  {len(names) + 1}) + New channel")
    while True:
        ans = input(f"Pick [{default}]: ").strip() or str(default)
        if ans.isdigit() and 1 <= int(ans) <= len(names):
            return names[int(ans) - 1]
        if ans == str(len(names) + 1):
            break
    while True:
        name = re.sub(r"[^a-z0-9]+", "-", input("Short name for the new channel (e.g. space): ").lower()).strip("-")[:30]
        if name and name not in names:
            break
        print("  Needs a name that isn't taken yet.")
    use_channel(name)
    ch = new_channel(input("Describe its niche in a sentence (or press Enter to let Claude choose): ").strip())
    path = rules.draft_rules(ch, name)  # nothing is made until the owner has read the drafted rules
    sys.exit(rules.REVIEW.format(path.name))


def ask_count() -> int:
    while True:
        ans = input("How many Shorts to make? [3]: ").strip() or "3"
        if ans.isdigit() and int(ans) > 0:
            return int(ans)


def ask_number(question: str, n: int, default: int | None = None) -> int:
    """Ask for a number 1..n (Enter = default, when there is one)."""
    while True:
        ans = input(f"{question} [{default if default else f'1-{n}'}]: ").strip() or str(default or "")
        if ans.isdigit() and 1 <= int(ans) <= n:
            return int(ans)


def ask_yes(question: str, default: bool) -> bool:
    ans = input(f"{question} [{'Y/n' if default else 'y/N'}]: ").strip().lower()
    return default if not ans else ans.startswith("y")


BRAINS = ["claude", "gemini", "both"]


def ask_brain(last: str) -> str:
    """Who plans this batch (scripts, fact check, SEO, picture choices, AI images): Enter = last time's.
    "both" makes every topic twice, once by each AI, to compare them side by side."""
    print("Who writes and plans these Shorts? (the other AI edits each script)\n  1) Claude (Gemini edits)\n"
          "  2) Gemini, Argon when your account has it (Claude edits)\n"
          "  3) Both, to compare: each topic made once by Claude and once by Gemini (post only the better one)")
    return BRAINS[ask_number("Pick a number", 3, BRAINS.index(last) + 1 if last in BRAINS else 1) - 1]


def load_channel() -> dict:
    return json.loads(session.CHANNEL.read_text(encoding="utf-8-sig"))  # tolerate Notepad's BOM


def new_channel(niche: str) -> dict:
    """Create this channel's profile: the owner's niche (or one Claude picks), with audience, tone,
    narrator voice and the line under the subscribe button."""
    print("Setting up the new channel...")
    what = (f"Write the profile for a new faceless YouTube Shorts channel in the owner's niche: {niche}\n"
            "Keep that niche (you may sharpen its wording)." if niche else
            """Pick ONE niche for a new faceless YouTube Shorts channel whose goal is YouTube Partner Program
monetization as fast as possible: advertiser-friendly, evergreen, high viewer retention, decent RPM,
hundreds of distinct topics, not gameplay, sports clips or news, no medical or financial advice.""")
    ch = llm.ask_ai(f"""{what}
Videos are an AI voiceover over real archival photos and film (AI images only where none fit), with
motion graphics and captions. Pick the best-fitting narrator voice from: {VOICES}.
cta_line = the small line under the on-screen SUBSCRIBE button, "for more <the niche in 2-4 words>".
Reply with ONLY JSON: {{"niche": "...", "channel_name_ideas": ["..."], "audience": "...",
"tone": "...", "voice": "...", "cta_line": "for more ..."}}""")
    assert ch.get("niche") and ch.get("voice") in VOICES, f"bad channel reply: {ch}"
    cta = str(ch.get("cta_line") or "").strip()
    ch["cta_line"] = cta if 0 < len(cta) <= 40 else "for more stories like this"
    ch["done_topics"] = []
    save_channel(ch)
    print(f"  Niche: {ch['niche']}\n  Name ideas: {', '.join(ch.get('channel_name_ideas', []))}")
    return ch


def save_channel(ch: dict) -> None:
    session.CHANNEL.write_text(json.dumps(ch, indent=2, ensure_ascii=False), encoding="utf-8")


QUIET_LOG = logging.getLogger("yt-dlp")
QUIET_LOG.disabled = True  # a channel without a Shorts tab is expected; callers count what came back


def yt_list(url: str, limit: int = 30) -> list[dict]:
    """Flat listing (title, views, duration, url) of a YouTube search, channel tab or playlist."""
    import yt_dlp
    opts = {"quiet": True, "no_warnings": True, "extract_flat": "in_playlist", "playlistend": limit,
            "ignoreerrors": True, "skip_download": True, "logger": QUIET_LOG}
    try:
        with yt_dlp.YoutubeDL(opts) as y:
            info = y.extract_info(url, download=False) or {}
    except Exception:
        return []
    return [e for e in info.get("entries") or [] if e]


def channel_url(handle: str) -> str:
    return f"https://www.youtube.com/{handle if handle.startswith('@') else '@' + handle}"


def seed_ideas(ch: dict, n: int, avoid: list[str]) -> dict:
    """Claude's picks of channels to study (plus a few search queries viewers use) for trend research."""
    got = llm.ask_ai(f"""For a YouTube Shorts channel in this niche: {ch['niche']}
List {n} established YouTube channels that regularly post Shorts (they must have a Shorts tab) in this
niche or a close one (their @handles, exactly as on YouTube), none of these: {avoid},
and 4 short YouTube search queries viewers in this niche use.
Reply with ONLY JSON: {{"handles": ["@..."], "queries": ["..."]}}""", fatal=False) or {}
    return {k: [str(v).strip() for v in got.get(k, []) if isinstance(v, str) and v.strip()][:12]
            for k in ("handles", "queries")}


def trend_research(ch: dict) -> list[dict]:
    """What's working in the niche right now: recent Shorts from channels that are proven in it.
    Claude suggests channels once; each is verified against real view counts (made-up or weak
    channels drop out), plus channels found through YouTube search. Their recent Shorts are ranked
    by views per day. Cached for the day; returns [] if YouTube can't be reached."""
    today = str(date.today())
    if session.RESEARCH.exists():
        cached = json.loads(session.RESEARCH.read_text(encoding="utf-8"))
        if cached.get("date") == today and cached.get("niche") == ch["niche"]:
            return cached["shorts"]
    print("Researching what's working in the niche on YouTube...")
    if not ch.get("research_seeds"):
        ch["research_seeds"] = seed_ideas(ch, 12, [])
        save_channel(ch)
    seeds = ch["research_seeds"]
    channels = {channel_url(h): h for h in seeds.get("handles", [])}
    for q in seeds.get("queries", []):  # plus channels that rank for real searches
        for e in yt_list(f"ytsearch30:{q} #shorts", 30):
            if (e.get("duration") or 999) <= 180 and e.get("channel_url"):
                channels.setdefault(e["channel_url"], None)
    found = {url: yt_list(url.rstrip("/") + "/shorts", 30) for url in channels}  # newest first: recent work
    dead = [h for url, h in channels.items() if h and not found[url]]
    if dead and any(found.values()):  # YouTube answered, so these channels really post no Shorts
        seeds["handles"] = [h for h in seeds["handles"] if h not in dead]
        seeds["dropped"] = (seeds.get("dropped", []) + dead)[-100:]  # never suggested again
        new = seed_ideas(ch, len(dead), seeds["handles"] + seeds["dropped"])["handles"]
        seeds["handles"] += new
        save_channel(ch)
        print(f"  {len(dead)} studied channels post no Shorts; swapped in {len(new)} new ones")
        found.update({channel_url(h): yt_list(channel_url(h) + "/shorts", 30) for h in new})
    pool = []
    for url, shorts in found.items():
        views = sorted(e.get("view_count") or 0 for e in shorts)
        if len(views) >= 5 and views[len(views) // 2] >= 20_000:  # proven: median recent Short >= 20k
            pool += [{"title": e.get("title") or "", "views": e.get("view_count") or 0, "url": e.get("url"),
                      "channel": url.rsplit("/", 1)[-1]} for e in shorts]
    pool = sorted(pool, key=lambda s: -s["views"])[:24]
    import yt_dlp
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "ignoreerrors": True, "skip_download": True}) as y:
        for s in pool[:12]:  # upload dates cost one request each, so only for the leaders
            try:
                info = y.extract_info(s["url"], download=False) or {}
            except Exception:
                continue
            if info.get("upload_date"):
                days = max(1, (date.today() - date(*time.strptime(info["upload_date"], "%Y%m%d")[:3])).days)
                s.update(days_old=days, views_per_day=s["views"] // days, likes=info.get("like_count"))
    pool.sort(key=lambda s: -(s.get("views_per_day") or s["views"] / 365))
    n_ch = len({s["channel"] for s in pool})
    print(f"  {len(pool)} top recent Shorts from {n_ch} proven channels")
    session.RESEARCH.write_text(json.dumps({"date": today, "niche": ch["niche"], "shorts": pool}, ensure_ascii=False,
                                   indent=1), encoding="utf-8")
    return pool


# Pacing (owner 2026-10-18): 5-8 s per picture lost viewers (every retention curve drops hardest 4-12 s in), so
# scenes are short, ~3 s, each with its own picture. A scene for a full-screen motion graphic needs ~4 s or more.
# full-screen graphics: 8 words (~3 s; the templates fit their timing to the scene). It was 11, above
# SCENE_WORDS, so after the faster pacing no scene could have one (Ghost Army, 2026-10-19)
SCENE_WORDS, LONG_SCENE_WORDS, FULL_MIN_WORDS = 10, 16, 8
