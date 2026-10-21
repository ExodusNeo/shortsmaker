"""Make ready-to-upload YouTube Shorts with no API keys.

Claude Code (headless) picks the niche and writes scripts + SEO, Wikimedia Commons
supplies images, Edge TTS does the voice, Pillow renders smooth motion + thumbnails,
ffmpeg mixes music/sound effects and encodes.
"""
import asyncio
import hashlib
import io
import json
import logging
import math
import os
import random
import re
import shutil
import statistics
import subprocess
import sys
import threading
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import warnings
import wave
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import edge_tts
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).parent
if (ROOT / "ffmpeg").exists():
    os.environ["PATH"] = f"{ROOT / 'ffmpeg'}{os.pathsep}{os.environ.get('PATH', '')}"
CHANNELS = ROOT / "channels"  # one profile per YouTube channel: <name>.json (+ <name>.research.json)
CHANNEL = RESEARCH = LOG = Path()  # this batch's profile files, set by use_channel()
# Obsidian vault (owner, 2026-10-21): open this folder in Obsidian. It holds the logbook and one page per Short;
# kept apart from output/ and cache/ so Obsidian never indexes thousands of video and cache files.
VAULT = ROOT / "vault"
LOGBOOK = VAULT / "Logbook"  # <channel>.md: each Short made, with the YouTube numbers the owner fills in
OUTPUT = ROOT / "output"  # each channel's Shorts go in output/<name>/
REMOTION = ROOT / "remotion"  # React/Remotion renderer for motion-graphics-heavy plans
# Style library (2026-10-19): photo looks, overlays and transitions, presets + owner-approved AI inventions
STYLE_DIR = REMOTION / "src" / "style"
STYLE_LIBRARY = STYLE_DIR / "library.json"
STYLE_SLOTS = {"look": "InventedLook", "overlay": "InventedOverlay", "transition": "InventedTransition"}
REMOTION_MIN_GRAPHICS = 3     # callouts + person cards needed before Remotion is worth its render time
MUSIC = ROOT / "music"  # music/<mood>/*.mp3; an optional "<track>.mp3.txt" holds its credit line
MOODS = ["mysterious", "tense", "playful", "somber", "epic"]  # one folder each; an empty mood uses any track
SFX = ROOT / "sfx"
STORY_SOUND_GAIN = 0.3  # gain for story sounds in the mix (0.0 to 1.0)
FONT = "C:/Windows/Fonts/impact.ttf"
W, H, FPS = 1080, 1920, 30
SRC = 1.5        # images are stored 1.5x output size so zooms stay sharp
XFADE = 0.3      # seconds of crossfade between scenes
MOVES = ["in", "right", "out", "left", "up", "in", "down", "out"]  # fallback if the plan has none
MOVE_NAMES = {"in": "slow zoom in", "out": "slow zoom out", "left": "pan left", "right": "pan right",
              "up": "tilt up", "down": "tilt down"}
GRAPHIC_STYLES = {"date": "date stamp (slides down)", "place": "location label (slides in)",
                  "fact": "fact box (pops in)", "stat": "number visual", "timeline": "timeline",
                  "mark": "circle/arrow on a detail of the picture"}
GRAPHIC_STYLES.update({"headline": "newspaper front page (slams in)", "quote": "quote typed on aged paper",
                       "compare": "two bars side by side", "stamp": "red rubber stamp (thumps on)"})
GRAPHIC_STYLES.update({"question": "question beat (picture dims, a big question holds)",
                       "kinetic": "kinetic title (letters drop in and squash)", "invented": "AI-invented overlay"})
PLANNED_STYLES = {"date", "place", "fact", "stat", "timeline", "headline", "quote", "compare", "stamp",
                  "question", "kinetic", "invented"}  # "mark": later
REMOTION_ONLY = {"stat", "timeline", "mark", "headline", "quote", "compare", "stamp",
                 "question", "kinetic", "invented"}  # Python: plain fact boxes
# Style-library guardrails per Short (owner 2026-10-18): upper limits, never targets
STYLE_CAPS = {"question": 1, "kinetic": 2, "invented": 2, "look_scenes": 4, "special": 3}
SPECIAL_TRANSITIONS = {"wipe", "whip", "leak", "invented"}
# Full-screen motion graphic scenes (remotion/src/full/), drawn instead of a picture, with mood-matched skins.
FULL_TYPES = ("board", "journey", "number", "document", "custom")
FULL_NAMES = {"board": "evidence board", "journey": "map journey", "number": "big number",
              "document": "document", "custom": "custom animation"}
CUSTOM_KINDS = ("diagram", "collage", "flow", "clock")
SKINS = ("parchment", "blueprint", "dossier", "hud")
PALETTE_SKINS = {"parchment": "parchment", "gold": "parchment", "ember": "dossier", "crimson": "dossier",
                 "rose": "dossier", "sky": "blueprint", "violet": "blueprint", "teal": "hud", "lime": "hud"}
ICONS = ("person", "coin", "ship", "house", "train", "soldier", "animal", "day",
         "bird", "fish", "insect", "rat", "horse", "car", "plane", "gun", "barrel", "dollar")
DOC_KINDS = ("newspaper", "letter", "telegram", "form")
MAX_FULL = 3          # per Short, planned + rescued: it stays a documentary, not a slideshow
MAX_FULL_PLANNED = 2  # planned by the director
MAX_FIGURES = 60      # big-number scene: ink figures drawn
MAX_STORY_SOUNDS = 3  # sounds of the story itself (a gun cocking on "jammed"), planned by the director
STORY_SFX = ROOT / "sfx" / "story"  # the owner's own files first, then CC0 sounds fetched from Freesound and kept
FREESOUND_KEY = ROOT / "freesound_key.txt"  # free Freesound API key (owner, 2026-10-18); never print it
YELLOW = (255, 221, 0)  # this Short's accent colour: render() sets it from the Short's palette
EMPHASIS = (255, 160, 0)  # the glowing emphasis word in the captions


def hex_rgb(h: str) -> tuple[int, int, int]:
    return int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)


def luminance(h: str) -> float:
    c = [v / 255 for v in hex_rgb(h)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


# Colour palettes for a Short's graphics, captions and cards (owner, 2026-10-16: not always yellow and navy).
# The planner picks one that suits the story; accent = boxes, pins, bars and the spoken caption word (black
# text sits on it), emphasis = the glowing key word, panel = the map's dark ocean.
PALETTES = {
    "gold": {"accent": "#FFD400", "emphasis": "#FF7A1A", "panel": "#0d1320"},
    "ember": {"accent": "#FF9F43", "emphasis": "#FF5252", "panel": "#1a110c"},
    "crimson": {"accent": "#FF5A5F", "emphasis": "#FFD166", "panel": "#170c10"},
    "teal": {"accent": "#2EE6C5", "emphasis": "#FFD166", "panel": "#08191a"},
    "sky": {"accent": "#4FC3FF", "emphasis": "#FFB020", "panel": "#0a1424"},
    "lime": {"accent": "#A8F04A", "emphasis": "#FFB020", "panel": "#0f170b"},
    "rose": {"accent": "#FF7EB3", "emphasis": "#7FDBFF", "panel": "#1a0e16"},
    "violet": {"accent": "#B49BFF", "emphasis": "#FFD166", "panel": "#120e22"},
    "parchment": {"accent": "#F4D6A0", "emphasis": "#FF7A1A", "panel": "#1c160e"},
}
for _p in PALETTES.values():  # readable: black text on the accent, and both colours bright against dark pictures
    assert (luminance(_p["accent"]) + 0.05) / 0.05 >= 6 and (luminance(_p["emphasis"]) + 0.05) / 0.05 >= 6, _p
    _land = hex_rgb(_p["panel"])  # map land and borders: the panel lifted toward white
    _p["land"] = "#%02x%02x%02x" % tuple(int(v + (255 - v) * 0.16) for v in _land)
    _p["border"] = "#%02x%02x%02x" % tuple(int(v + (255 - v) * 0.3) for v in _land)


def short_skin(short: dict, full: dict | None = None) -> str:
    """Visual skin for a Short's full-screen motion graphics (parchment, blueprint, dossier, hud)."""
    if isinstance(full, dict) and full.get("skin") in SKINS:
        return full["skin"]
    mood, pal = short.get("music_mood"), short.get("palette")
    if pal in ("gold", "parchment") and mood in ("tense", "somber"):
        return "dossier"
    if pal in ("gold", "") and mood in ("curious", "epic"):
        return "blueprint"
    return PALETTE_SKINS.get(pal, "parchment")


def ass_colour(rgb: tuple[int, int, int], dim: float = 1.0) -> str:
    """ASS subtitle colour (&H00BBGGRR&), optionally darkened (for an outline)."""
    r, g, b = (int(v * dim) for v in rgb)
    return f"&H00{b:02X}{g:02X}{r:02X}&"
# Story shapes rotated between Shorts so the channel doesn't read as one template.
SHAPES = ["mystery solved", "rise and fall", "countdown to disaster", "myth vs truth",
          "one person against the odds", "the hidden reason", "chain of unlikely events"]
VOICES = ["en-US-AndrewNeural", "en-US-BrianNeural", "en-US-ChristopherNeural",
          "en-US-AvaMultilingualNeural", "en-US-EmmaNeural", "en-GB-RyanNeural"]


BRAIN = "claude"  # who plans, writes and picks pictures: "claude" (Claude Code) or "gemini" (Google Antigravity
# CLI, `agy`, signed in with the owner's Google account). Chosen per batch in run.bat, saved in the profile.
# Gemini (agy image generator, Flash) paints the AI gap images and thumbnail art for either planner; SDXL is the backup.
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
NO_QUOTA: set[str] = set()  # agents ("claude" / "gemini") that ran out of credits/quota during this run


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
        r = subprocess.run([agy, "--model", model, "--effort", "high", "--add-dir", str(folder),
                            f"-p=Read the file {task} and do exactly what it says. Your whole reply must be "
                            "what that file asks for, nothing else."],
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


LAST_AI = "claude"  # who answered the last ask_ai() call


def ask_ai(prompt: str, fatal: bool = True, read_dir: Path | None = None, brain: str | None = None) -> dict | None:
    """Headless planner call (BRAIN, or `brain`: Claude or Gemini) that returns parsed JSON; with fatal=False, None
    on failure. Either agent automatically falls back to the other on failure or when out of credits/quota
    (and remembers exhausted quota in NO_QUOTA so later steps don't wait on the empty account). With read_dir,
    the AI may look at the images in that folder."""
    global BRAIN, LAST_AI
    first = brain or BRAIN
    second = "gemini" if first == "claude" else "claude"
    order = [w for w in (first, second) if w not in NO_QUOTA] or [first, second]
    for idx, who in enumerate(order):
        name, exe = who.capitalize(), shutil.which("agy" if who == "gemini" else "claude")
        fallback = ("gemini" if who == "claude" else "claude").capitalize()
        if not exe:
            print(f"  {name} isn't installed ({'Antigravity agy' if who == 'gemini' else 'Claude Code'})")
            continue
        for attempt in range(2):
            if who == "gemini":
                out = run_agy(prompt, read_dir or ROOT / "agy_tasks", model=GEMINI_FALLBACK if read_dir else None)  # pictures: Flash
            else:
                # Lean call: no personal plugins, hooks or skill list (the owner's interactive setup has ~20
                # plugins/skills and output-rewriting hooks; a JSON-only planner call needs none of them), always
                # started in ROOT so per-Short work folders don't each become a Claude Code project.
                cmd = [exe, "-p", "--setting-sources", "project,local", "--disable-slash-commands"] + (
                    ["--allowedTools", "Read", "--add-dir", str(read_dir)] if read_dir else [])
                try:
                    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8",
                                       timeout=900, cwd=ROOT)
                    out = r.stdout if (r.stdout or "").strip() else f"{r.stdout or ''}\n{r.stderr or ''}"
                except subprocess.TimeoutExpired:
                    out = None
            if out is None:
                print(f"  {name} timed out (try {attempt + 1}/2)")
                continue
            try:
                start, end = out.find("{"), out.rfind("}")
                if start >= 0 and end > start:
                    data = json.loads(out[start: end + 1])
                    LAST_AI = who
                    return data
            except json.JSONDecodeError:
                pass
            if quota_exhausted(out):
                NO_QUOTA.add(who)
                other = "gemini" if who == "claude" else "claude"
                if BRAIN == who and other not in NO_QUOTA:
                    BRAIN = other
                print(f"  {name} has no credits/quota left: switching to {fallback} for the rest of this run")
                break
            print(f"  {name} reply wasn't valid JSON (try {attempt + 1}/2)")
        if idx == 0 and len(order) > 1 and who not in NO_QUOTA:
            print(f"  {name} didn't give a usable answer, asking {fallback} instead")
    if fatal:
        sys.exit("The AI didn't return usable JSON. Run again.")
    return None


def use_channel(name: str) -> None:
    global CHANNEL, RESEARCH, LOG
    CHANNEL, RESEARCH = CHANNELS / f"{name}.json", CHANNELS / f"{name}.research.json"
    LOG = LOGBOOK / f"{name}.md"
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
    new_channel(input("Describe its niche in a sentence (or press Enter to let Claude choose): ").strip())
    return name


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
    return json.loads(CHANNEL.read_text(encoding="utf-8-sig"))  # tolerate Notepad's BOM


def new_channel(niche: str) -> dict:
    """Create this channel's profile: the owner's niche (or one Claude picks), with audience, tone,
    narrator voice and the line under the subscribe button."""
    print("Setting up the new channel...")
    what = (f"Write the profile for a new faceless YouTube Shorts channel in the owner's niche: {niche}\n"
            "Keep that niche (you may sharpen its wording)." if niche else
            """Pick ONE niche for a new faceless YouTube Shorts channel whose goal is YouTube Partner Program
monetization as fast as possible: advertiser-friendly, evergreen, high viewer retention, decent RPM,
hundreds of distinct topics, not gameplay, sports clips or news, no medical or financial advice.""")
    ch = ask_ai(f"""{what}
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
    CHANNEL.write_text(json.dumps(ch, indent=2, ensure_ascii=False), encoding="utf-8")




warnings.filterwarnings("ignore", "Palette images with Transparency")  # harmless PIL note on some GIF/PNG candidates
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
    got = ask_ai(f"""For a YouTube Shorts channel in this niche: {ch['niche']}
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
    if RESEARCH.exists():
        cached = json.loads(RESEARCH.read_text(encoding="utf-8"))
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
    RESEARCH.write_text(json.dumps({"date": today, "niche": ch["niche"], "shorts": pool}, ensure_ascii=False,
                                   indent=1), encoding="utf-8")
    return pool


SHORT_FORM = False  # run.bat question: shorter Shorts (~25-30 s), a test against the usual 40-50 s


# Pacing (owner 2026-10-18): 5-8 s per picture lost viewers (every retention curve drops hardest 4-12 s in), so
# scenes are short, ~3 s, each with its own picture. A scene for a full-screen motion graphic needs ~4 s or more.
# full-screen graphics: 8 words (~3 s; the templates fit their timing to the scene). It was 11, above
# SCENE_WORDS, so after the faster pacing no scene could have one (Ghost Army, 2026-10-19)
SCENE_WORDS, LONG_SCENE_WORDS, FULL_MIN_WORDS = 10, 16, 8


def style_library(kind: str | None = None) -> list[dict]:
    """The style library (remotion/src/style/library.json): [{name, kind, description, fits, file, origin}]."""
    return [e for e in json.loads(STYLE_LIBRARY.read_text(encoding="utf-8")) if kind in (None, e["kind"])]


def write_style_index() -> None:
    """Regenerates remotion/src/style/index.ts from library.json: Remotion's bundle needs static imports, so each
    library file and the three per-Short invention slots are imported and mapped by name ("invented" = the slot)."""
    lib = sorted(style_library(), key=lambda e: (e["kind"], e["name"]))
    imports = [(Path(e["file"]).stem, Path(e["file"]).with_suffix("").as_posix()) for e in lib]
    imports += [(slot, f"generated/{slot}") for slot in STYLE_SLOTS.values()]
    maps = {}
    for kind, var, typ in (("look", "LOOKS", "Look"), ("overlay", "OVERLAYS", "Overlay"), ("transition", "TRANSITIONS", "Transition")):
        pairs = [f"{json.dumps(e['name'])}: {Path(e['file']).stem}" for e in lib if e["kind"] == kind]
        maps[kind] = f"export const {var}: Record<string, {typ}> = {{{', '.join(pairs + [f'invented: {STYLE_SLOTS[kind]}'])}}};"
    text = "\n".join(
        ["// GENERATED by make_shorts.py write_style_index() from library.json: do not edit by hand.",
         "import type {Look, Overlay, Transition} from './types';"]
        + [f"import {{{name}}} from './{path}';" for name, path in sorted(imports)]
        + ["", maps["look"], maps["overlay"], maps["transition"], "",
           "const has = (o: object, k?: string | null): k is string => !!k && Object.prototype.hasOwnProperty.call(o, k);",
           "export const lookFor = (name?: string | null): Look | null => (has(LOOKS, name) ? LOOKS[name] : null);",
           "export const overlayFor = (style?: string | null): Overlay | null => (has(OVERLAYS, style) ? OVERLAYS[style] : null);",
           "export const transitionFor = (name?: string | null): Transition => (has(TRANSITIONS, name) ? TRANSITIONS[name] : TRANSITIONS.fade);",
           ""])
    (STYLE_DIR / "index.ts").write_text(text, encoding="utf-8", newline="\n")


def length_plan() -> tuple[int, int, int, int, str]:
    """(min words, max words, min scenes, max scenes, seconds) for this batch's scripts."""
    return (60, 72, 8, 10, "25-30") if SHORT_FORM else (95, 125, 11, 16, "40-50")


def write_scripts(ch: dict, n: int, topics: list[str] | None = None, pools: list[str] | None = None) -> list[dict]:
    """Plan n Shorts on new topics, or on exactly `topics` (comparison runs: the other AI's topics), as a small
    team: the planner picks topics, Wikipedia is read for each, the planner writes the narration, the OTHER AI
    edits it (edit_scripts), the planner plans the edit on the final words (direct_scripts), then the fact check.
    Before any writing, each topic's real pictures are gathered and listed (prepare_topic); a topic with too few
    is replaced by a backup. `pools` (Both mode): the pool folders of the same topics, by position."""
    trends = trend_research(ch)
    trend_text = ""
    if trends:
        rows = [f"- \"{s['title']}\" | {s['views']:,} views" + (f", {s['views_per_day']:,}/day" if s.get("views_per_day") else "")
                + f" | {s['channel']}" for s in trends[:20]]
        trend_text = f"""
WHAT'S WORKING NOW in this niche (real YouTube data, today; top recent Shorts from proven channels):
{chr(10).join(rows)}
Use this to choose topics with proven demand and to write titles and hooks in the patterns that
recur among the leaders. Never remake one of these videos or copy its wording: every story must
be our own, true and not already covered above.
"""
    results = logbook_results()
    if results:
        trend_text += f"""
HOW OUR OWN POSTED SHORTS DID (the owner's numbers from YouTube Studio, oldest first):
{results}
Learn from these before choosing topics and writing. "Stayed to watch" shows whether the first second
(topic, hook line, opening picture) stopped the scroll; "Average % viewed" shows whether the story held
to the end (over 100% means rewatches). Do more of what the best ones share (kinds of topic, hook
patterns, story shapes) and less of what the weakest share; read the owner's notes too. With only a
few Shorts, treat this as hints, not rules.
"""
    if topics:
        what = f"Use exactly these {len(topics)} topics, in this order: {topics}"
    else:
        what = (f"Pick {n + TOPIC_BACKUPS} NEW topics, none of these already-used ones: {ch['done_topics'][-200:]}\n"
                f"The last {TOPIC_BACKUPS} are backups, used only if an earlier topic has too few real pictures or footage.")
        if ch.get("myths"):  # stories the fact check caught: worth telling as the real story behind the myth
            what += ("\nMyths our fact check caught earlier, each good for a \"myth vs truth\" Short that tells "
                     f"what really happened (skip any already covered above): {ch['myths'][-20:]}")
    about = f"Niche: {ch['niche']}. Audience: {ch.get('audience', '')}. Tone: {ch.get('tone', '')}."
    print(f"Choosing topics with {BRAIN.capitalize()}...")
    data = ask_ai(f"""You choose stories for a faceless YouTube Shorts channel.
{about}
{trend_text}
{what}
Viewers decide in one second whether to swipe, so pick stories whose single most shocking fact can be
said in 8 words or fewer that a stranger understands instantly (e.g. "A dead man won this horse race.").
Every Short needs a MAIN CHARACTER: one named person or animal the story follows, with a real photo or
portrait of them. Our Shorts built around one strange person or animal (Jack the baboon, Violet Jessop,
Emperor Norton, Lord Byron and his bear, the emus) were all pushed by YouTube; the ones about a thing, an
event or a group (a smell, a newspaper hoax, a fake statue, an army unit) all stalled. This does not
narrow the topics: tell an event through the person at its center (the Great Stink through engineer Joseph
Bazalgette, the Cardiff Giant through George Hull who carved it). Choose an event with nobody to follow
only when nothing better is left.
For each:
- topic: 1-2 sentences: the story and the twist that makes it worth telling, told through its main character.
- character: the main character's name (e.g. "Joseph Bazalgette", "Jack the baboon").
- subject: the main person, game, product, place, event or thing the story is about (e.g. "Super Mario 64", "Joshua Norton").
- wiki_articles: 2-4 exact English Wikipedia article titles for the story's subject, key people,
  places, games, inventions or events (e.g. ["Super Mario 64", "Shigeru Miyamoto"]); the writer gets
  their text as research.
- search_terms: 3 short phrases people really type into YouTube search that this Short answers, in
  everyday words about its angle, not only the name (e.g. "titanic survivor", "worst warship ever").
- visual_terms: 4-6 short search phrases for the real people, places, objects and events of this story a
  camera could show, as photo archives would title them (e.g. "Ghost Army inflatable tank", "Rhine crossing 1945").
- people: the key people's full names (e.g. ["Ellsworth Kelly"]), [] if none. Their portraits are searched.
Pictures and footage are gathered from these before any script is written: prefer stories with real photos or film.
Reply with ONLY JSON: {{"shorts": [{{"topic": "...", "character": "...", "subject": "...", "wiki_articles": ["..."],
"search_terms": ["..."], "visual_terms": ["..."], "people": ["..."]}}]}}""")
    shorts = []
    wanted = len(topics) if topics else n
    for k, p in enumerate(data.get("shorts", [])[:len(topics) if topics else n + TOPIC_BACKUPS]):
        if not (isinstance(p, dict) and str(p.get("topic") or "").strip() and str(p.get("subject") or "").strip()):
            continue  # LLM output is untrusted
        subject, arts, terms = str(p["subject"]).strip(), p.get("wiki_articles"), p.get("search_terms")
        arts = [a.strip() for a in arts if isinstance(a, str) and a.strip()] if isinstance(arts, list) else []
        shorts.append({"topic": str(p["topic"]).strip(), "subject": subject, "_pos": k,
                       "character": str(p.get("character") or "").strip()[:80],
                       "wiki_articles": list(dict.fromkeys([subject] + arts))[:5],
                       "search_terms": [t.strip() for t in terms if isinstance(t, str) and t.strip()][:3]
                       if isinstance(terms, list) else [],
                       **{k: [t.strip() for t in p[k] if isinstance(t, str) and t.strip()][:cap]
                          if isinstance(p.get(k), list) else [] for k, cap in (("visual_terms", 6), ("people", 4))}})
        if (who := shorts[-1]["character"]) and who not in shorts[-1]["people"]:  # their portrait is searched first
            shorts[-1]["people"] = [who] + shorts[-1]["people"][:3]
    assert shorts, f"no usable topics: {data}"
    kept, dropped = [], []
    for i, s in enumerate(shorts):
        if len(kept) == wanted:
            break
        print(f'Topic {i + 1}/{len(shorts)}: "{s["subject"]}": reading Wikipedia, finding real pictures and footage...')
        k = s.pop("_pos")
        if prepare_topic(s, Path(pools[k]) if pools and k < len(pools) else None):
            kept.append(s)
        else:
            dropped.append(f'"{s["topic"]}": only {s["picture_check"]} real pictures/clips')
            if s.get("pool_dir"):  # not kept for 30 days: the topic may come back once better pictures exist
                shutil.rmtree(s["pool_dir"], ignore_errors=True)
            print(f"  Skipped {dropped[-1]}")
    for s in kept:
        s["dropped_topics"] = dropped
    shorts = kept
    if not shorts:
        print("No topic had enough real pictures this time; nothing was made.")
        return []
    research = [{"index": i, "topic": s["topic"], "subject": s["subject"], "main_character": s.get("character") or s["subject"],
                 "wikipedia": {t: x[:8000] for t, x in s["_texts"].items() if x} or "none found: use only facts you are sure of",
                 "pictures": pictures_of(s) or "none listed"}
                for i, s in enumerate(shorts)]
    lo, hi, s_lo, s_hi, secs = length_plan()
    print(f"Writing {len(shorts)} script(s) with {BRAIN.capitalize()}...")
    data = ask_ai(f"""You write YouTube Shorts narration for a faceless channel.
{about}
{trend_text}
Write one Short on each topic below, using the Wikipedia research given with it.
Rules for each Short:
- {lo}-{hi} spoken words (about {secs} seconds: story Shorts hold viewers best under ~50 s), simple words a 5th grader understands.
- Structure, written like a documentary editor would cut it:
  hook (scene 1): viewers decide in one second whether to swipe. Its first sentence is 8 words or
  fewer: a concrete, surprising claim understood with no context that OPENS A QUESTION the viewer
  needs answered (how? why? what happened next?). Show the surprise, hold back the explanation.
  The opening picture already shows the subject, so the words must add what the picture can't: the
  stakes, the contradiction, the strange part. Good: "Parliament nearly fled London over one smell."
  (why?), "A broke man crowned himself Emperor of America." (and then?). Weak: "A railway once hired
  a baboon." over a photo of a baboon at the levers: the line and picture tell the whole story, so
  nothing is left to stay for (that Short lost 3 of 4 viewers in the first second); better: "This
  signalman never made one mistake in nine years." over an opening picture that doesn't show the
  baboon yet (the reveal comes a few scenes later). Never a setup, a greeting,
  a date first, a name nobody knows yet, or a technical detail. Tell the story through its
  main_character: the hook is about them ("This man...", "This baboon..."), and the story follows
  what they did and what happened to them. Draft 3 first sentences in hook_options, each from a
  different hook family (curiosity gap, result first, stakes, contrarian claim, before/after), then
  open scene 1 with the strongest. Scene 1 is that sentence plus at most one short line.
  confirmation (scene 2): one concrete, showable detail that proves the hook's claim is real (a
  record, a number, a witness, an object), without answering the hook's question.
  open loop right after: promise a twist ("but that wasn't the strangest part").
  scenes 2-3 keep moving FORWARD: they are where most viewers leave (on every one of our Shorts the
  retention curve holds through the hook, then drops hardest 4-12 seconds in, right where the script
  rewound to background: "In 1852, Joshua Norton tried to corner the rice market.", "James Wide bought
  Jack at a market."). Our Short that went forward instead ("And that stink hid a far deadlier secret in
  the same water.") lost the fewest. So after the hook: raise the stakes or show what happened next;
  never start a sentence with a date or with a name the viewer hasn't met yet; give background only as
  a half-line at the moment the story needs it.
  rising tension, drip-fed: every scene adds one new concrete fact, cause then effect, no filler.
  Answer each small question within a scene or two and raise the next one, so viewers always have
  one open question; the hook's main question stays open until the payoff.
  re-hook around the middle: a turn that raises the stakes ("then it got worse").
  payoff: the twist, then ONE last line that calls back to the hook's words or image, so the
  ending loops into the opening on a rewatch. End there: no "follow for more", no outro (an
  on-screen subscribe button and the pinned comment handle engagement).
- Never repeat yourself: every line adds something new. Apart from that one callback to the hook,
  no phrase of 3+ words may appear twice, and the callback must not reuse the previous scene's wording.
- Write for the picture: every scene must be about something a camera could show (a person,
  place, object, document or crowd), never an abstract line like "this changed everything". If a
  line has nothing to show, rewrite it around a concrete detail.
- Build on the real pictures: each topic's "pictures" lists the real photos and film found for it (#number,
  what it shows; [opener] = strong enough to open the Short). Where a strong picture exists, let the story pass
  through what it shows, and write the hook for an [opener] picture when one fits. The story rules above still
  come first: never bend a fact or the pacing to fit a picture.
- Every fact must be true: take facts from the research; anything else only if you are certain it
  is well documented. No made-up statistics or quotes.
- shape: the story's shape, one of {SHAPES}. Not one of the channel's last ones
  ({ch.get('recent_shapes', [])}), and a different one for each Short in this batch.
- scenes: the narration split into {s_lo}-{s_hi} short scenes of 4-{SCENE_WORDS} words (about 3 seconds: each
  scene gets its own picture, and a new picture every ~3 seconds keeps viewers watching), cutting where the
  picture would naturally change: one image per scene. Only a scene that needs time on one picture (a trip
  between places, a big number, a document, several things that connect) may run up to {LONG_SCENE_WORDS} words.
- title: draft (refined later with real search data): under 60 characters, main keyword early, no "#shorts".
- thumbnail_text: 2-4 punchy words.
- hook_text: 2-4 words shown big over the first second, for viewers watching with the sound off:
  sharpens the SAME question the first sentence opens, in other words (e.g. "NOBODY FIRED HIM"),
  never a separate idea, not a repeat of the title or thumbnail_text.
Topics and research: {json.dumps(research, ensure_ascii=False)}
Reply with ONLY JSON: {{"shorts": [{{"index": 0, "shape": "...", "title": "...", "hook_options": ["...", "...", "..."],
"hook_text": "...", "thumbnail_text": "...", "scenes": ["narration of scene 1", "narration of scene 2", "..."]}}]}}""")
    for k, r in enumerate(data.get("shorts", [])):
        i = r.get("index") if isinstance(r, dict) and isinstance(r.get("index"), int) else k
        if isinstance(r, dict) and 0 <= i < len(shorts) and str(r.get("title") or "").strip():
            shorts[i].update({f: r[f] for f in ("shape", "hook_options", "hook_text", "thumbnail_text") if r.get(f)},
                             title=str(r["title"]).strip(), lines=narration_lines(r.get("scenes")))
    shorts = [s for s in shorts if s.get("lines")]
    assert shorts, f"no usable scripts: {data}"
    edit_scripts(shorts, ch)
    direct_scripts(shorts, ch)
    kept = []
    for s in shorts:  # LLM output is untrusted: check required fields, normalize the edit plan
        assert s.get("title") and s.get("scenes") and all(
            sc.get("narration") and sc.get("image_search") for sc in s["scenes"]), f"bad short: {s}"
        if not fact_check(s):
            print(f'  Dropped "{s["title"]}": its central claim didn\'t hold up against the sources')
            myth = f"{s.get('topic') or s['title']}: {s.get('myth_note') or 'not true as told'}"[:300]
            ch["myths"] = [m for m in ch.get("myths", []) if m != myth] + [myth]
            save_channel(ch)
            continue
        kept.append(s)
        s["shape"] = s.get("shape") if s.get("shape") in SHAPES else ""
        s["thumbnail_prompt"] = str(s.get("thumbnail_prompt") or "").strip()[:400]
        s["music_mood"] = s.get("music_mood") if s.get("music_mood") in MOODS else ""
        s["palette"] = s.get("palette") if s.get("palette") in PALETTES else ""
        s["hook_text"] = str(s.get("hook_text") or s.get("thumbnail_text") or "").strip().upper()[:40]
        opts = s.get("hook_options")
        s["hook_options"] = [str(o).strip() for o in opts if str(o).strip()][:3] if isinstance(opts, list) else []
        for i, sc in enumerate(s["scenes"]):
            sc["image_search"] = str(sc.get("image_search") or "").strip()[:120]
            sc["video_search"] = str(sc.get("video_search") or sc["image_search"]).strip()[:120]
            sc["ai_image"] = str(sc.get("ai_image") or "").strip()[:400]
            sc["motion"] = str(sc.get("motion") or "").strip()[:200]
            sc["motion_people"] = sc.get("motion_people") is True
            sc["animate"] = sc.get("animate") is True and bool(sc["motion"])
        for sc in [sc for sc in s["scenes"] if sc["animate"]][5:]:  # GPU time (~2 min each): at most 5 clips
            sc["animate"] = False
        for i, sc in enumerate(s["scenes"]):
            if sc.get("move") not in MOVE_NAMES:
                sc["move"] = MOVES[i % len(MOVES)]
            sc["shot"] = str(sc.get("shot") or "").strip()[:300]
            said = words_of(sc["narration"])
            sc["graphic"] = clean_graphic(sc.get("graphic"), said) if i else None
            sc["full"] = clean_full(sc.get("full"), said) if i else None
            sc["sound"] = clean_sound(sc.get("sound"), said)
            pr = sc.get("person")
            ok = (isinstance(pr, dict) and all(isinstance(pr.get(k), str) and pr[k].strip()
                                               for k in ("name", "trigger", "image_search"))
                  and contains(said, words_of(pr["trigger"]))
                  and len(words_of(pr["name"])) >= 2)  # single names ("Jack") match too many photos
            sc["person"] = {k: pr[k].strip() for k in ("name", "trigger", "image_search")} if ok else None
            if sc["person"]:
                sc["graphic"] = None  # one overlay per scene
            em = sc.get("emphasis")
            sc["emphasis"] = em.strip() if isinstance(em, str) and contains(said, words_of(em)) else None
            sc["transition"] = clean_transition(sc.get("transition")) if i else "fade"
        limit_full(s["scenes"], MAX_FULL_PLANNED)
        clean_pics(s, (load_pool(Path(s["pool_dir"]), thumbs=False) or []) if s.get("pool_dir") else [])
        settle_style(s, ch)
        limit_style(s["scenes"])
        limit_sounds(s["scenes"])
    return kept


def pictures_of(s: dict) -> str:
    """The topic's usable pictures as prompt lines ("" without a picture list)."""
    cands = load_pool(Path(s["pool_dir"]), thumbs=False) if s.get("pool_dir") and s.get("catalog") else None
    return catalog_text(cands, s["catalog"]) if cands else ""


def clean_pics(s: dict, cands: list[dict]) -> None:
    """The director's `pic` numbers (scenes and evidence-board items), checked: a usable listed picture, never twice,
    at most 2 frames of one film. Anything else becomes None (the picture step then searches for that scene)."""
    ok = {e["n"] for e in s.get("catalog") or [] if is_usable(e)}
    used, per_film = set(), {}

    def check(n, still=False):
        if type(n) is not int or n not in ok or n in used or n > len(cands):
            return None
        f = cands[n - 1].get("film")
        if f and still:  # evidence boards pin prints, never film frames (full_pictures() skips them)
            return None
        if f and per_film.get(f["src"], 0) >= 2:
            return None
        used.add(n)
        if f:
            per_film[f["src"]] = per_film.get(f["src"], 0) + 1
        return n

    for sc in s["scenes"]:
        sc["pic"] = check(sc.get("pic"))
        for it in (sc.get("full") or {}).get("items") or [] if (sc.get("full") or {}).get("type") == "board" else []:
            it["pic"] = check(it.get("pic"), still=True)


def prepare_topic(s: dict, folder: Path | None = None) -> bool:
    """Before writing: the topic's Wikipedia research (`_texts`; fact_check() reuses it), its real pictures and
    footage (a cached pool, else gathered now) and their AI picture list. True when it has MIN_USABLE usable ones."""
    s["_texts"] = {t: article_text(t)[:15000] for t in s["wiki_articles"][:4]}
    folder = folder or pool_folder(s["topic"])
    cands = load_pool(folder)
    if cands is None:
        cands = gather_pool(s["wiki_articles"], s.get("people", []), s.get("visual_terms", []), s.get("visual_terms", []))
        if len(cands) < MIN_USABLE:  # can't pass: no AI call, and not cached (a network blip may have caused it)
            s.update(catalog=[], pool_dir=None, picture_check=f"0 usable of {len(cands)}")
            return False
        save_pool(folder, cands)
    s["catalog"] = catalog_pool(s, cands, folder)
    good = usable(cands, s["catalog"])
    s["pool_dir"], s["picture_check"] = str(folder), f"{len(good)} usable of {len(cands)}"
    return len(good) >= MIN_USABLE


def narration_lines(v) -> list[str]:
    """Scene narrations from an AI reply: a list of strings (or of {"narration": ...})."""
    items = v if isinstance(v, list) else []
    return [t for t in (str((x.get("narration") if isinstance(x, dict) else x) or "").strip() for x in items) if t]


def edit_scripts(shorts: list[dict], ch: dict) -> None:
    """The OTHER AI edits the drafts: strongest hook, read-aloud fixes, cuts, hook/thumbnail/title consistency.
    A second model catches what the writer can't see in its own text. A failed or malformed reply keeps the draft."""
    editor = "gemini" if BRAIN == "claude" else "claude"
    lo, hi, s_lo, s_hi, _ = length_plan()
    print(f"{editor.capitalize()} is editing the script(s)...")
    drafts = [{"index": i, "topic": s["topic"], "shape": s.get("shape"), "title": s["title"],
               "hook_text": s.get("hook_text"), "thumbnail_text": s.get("thumbnail_text"),
               "hook_options": s.get("hook_options"), "scenes": s["lines"], "pictures": pictures_of(s) or "none listed"}
              for i, s in enumerate(shorts)]
    data = ask_ai(f"""You are the script editor of a faceless YouTube Shorts channel. Niche: {ch['niche']}.
Tone: {ch.get('tone', '')}. Another writer drafted the scripts below; make each one as gripping as possible.
About half our viewers swipe away in the first second, so the hook matters most.
For each script:
1. Hook: score every candidate first sentence (hook_options and scene 1's first sentence) 1-10 for
   "would a stranger scrolling past stop, AND need to stay for the answer?". Strong: a concrete,
   surprising claim, 8 words or fewer, understood with no context, that opens a question (how? why?
   what next?) the script answers later. Weak: a setup, a name nobody knows, a date first, vague words
   ("strange", "mysterious", "incredible"), or a line that tells the whole story at once (with the
   opening picture of the subject, nothing is left to stay for). Open scene 1 with the best one, or a
   better one you write from the script's own facts.
2. Read every line aloud in your head as the narrator would say it: fix tongue-twisters, sentences over
   about 14 words, stacked numbers, awkward words for a text-to-speech voice, anything a 5th grader
   wouldn't get.
3. Cut filler and empty lines ("this changed everything", "little did they know"): every scene adds one
   new concrete fact a camera could show. No phrase of 3+ words twice, except one last line that calls
   back to the hook.
4. Keep the shape working: scene 2 proves the hook's claim is real with one concrete detail (without
   answering its question), then an open loop, a re-hook around the middle, the twist,
   then the callback ending. At every scene the viewer should have one open question: small ones
   answered within a scene or two, the hook's main question kept open until the payoff. Scenes 2-3 are
   where most viewers leave (our retention curves drop hardest 4-12 seconds in, where scripts rewound to
   background): they must move forward or raise the stakes; no sentence there may start with a date or a
   name the viewer hasn't met; background only as a half-line when the story needs it.
5. hook_text (big words over the first second), thumbnail_text and title must tease the same story
   without repeating each other's words or the hook sentence; hook_text sharpens the same question as
   the hook sentence (sound-off viewers read it instead), never a separate idea. Fix whichever fails.
Each script's "pictures" lists the real pictures found for it: keep lines built on them showable.
Change wording, never claims: add no fact that isn't already in the script. Keep {s_lo}-{s_hi} scenes of 4-{SCENE_WORDS}
words each (a new picture every ~3 seconds; only a scene that needs time on one picture may run up to
{LONG_SCENE_WORDS}), {lo}-{hi} words in total. Return every scene, changed or not.
notes: 1-4 short lines: the hook scores and what you changed and why.
Scripts: {json.dumps(drafts, ensure_ascii=False)}
Reply with ONLY JSON: {{"shorts": [{{"index": 0, "scenes": ["...", "..."], "title": "...", "hook_text": "...",
"thumbnail_text": "...", "notes": ["..."]}}]}}""", fatal=False, brain=editor) or {}
    who = LAST_AI.capitalize()  # Claude steps in when Gemini fails
    for r in data.get("shorts", []) if isinstance(data.get("shorts"), list) else []:
        i = r.get("index") if isinstance(r, dict) else None
        if not (isinstance(i, int) and 0 <= i < len(shorts)):
            continue
        s, lines = shorts[i], narration_lines(r.get("scenes"))
        words = [len(t.split()) for t in lines]
        notes = [str(x).strip()[:300] for x in r.get("notes") or [] if str(x).strip()][:4] \
            if isinstance(r.get("notes"), list) else []
        if s_lo <= len(lines) <= s_hi and max(words) <= LONG_SCENE_WORDS + 2 and lo - 15 <= sum(words) <= hi + 15:
            s["lines"] = lines
        else:
            notes.append("its scene edit broke the length rules, so the writer's scenes were kept")
        for k in ("title", "hook_text", "thumbnail_text"):
            if isinstance(r.get(k), str) and r[k].strip():
                s[k] = r[k].strip()
        s["editor_notes"] = [f"{who}: {x}" for x in notes] or [f"{who}: no changes"]


# How an AI painting prompt (ai_image) is written: the director plans them with it and rewrite_paint_prompts()
# rewrites rejected ones with it. Owner 2026-10-21: paintings looked "way too AI" -> a named period medium.
AI_IMAGE_RULE = """One or two descriptive sentences, not a keyword list: the subject first with era-accurate details,
  then the setting, then the light (always name it: "low winter sun", "one oil lamp", "flat overcast daylight"),
  then a REAL hand-made medium of the story's era named with its physical marks, so it looks made by a person and
  can't pass for a real photo: "19th-century wood engraving from an illustrated newspaper, dense black hatching on
  yellowed newsprint"; "hand-colored copperplate etching, fine cross-hatching, faded watercolor washes on foxed
  paper"; "1940s gouache magazine illustration, flat matte paint, visible brush marks, coarse paper with halftone dots
  and slightly off-register colors"; "1930s silkscreen poster, three flat inks on grainy paper, misaligned color
  layers"; "loose oil sketch on canvas board, thick visible brushstrokes, unfinished edges"; "charcoal drawing on
  toned paper, smudged shading". Never "concept art", "digital illustration", "stylized", "cinematic", "highly
  detailed", "8k" or "vibrant" (they give the glossy AI look). The artwork fills the whole frame (never a framed
  poster, card or page with a border). Never "photograph" (a fake photo would pass
  as real evidence). Never a recognizable real person's face: show places, objects, crowds, hands,
  silhouettes or figures from behind. Never a close-up of the specific real object the story is about
  (a famous artifact, statue, building or document): the AI would invent what it looked like; show the
  setting or the people around it instead. Writing in the painting (a shop sign, a poster, a ship's name,
  a headline) is allowed when it helps tell the story: put the exact words in double quotes, at most 6,
  true to the story and its era (no invented names, dates or numbers). Without quotes the painting has no writing,
  so never paint a subject made of print without quoting its words (a newsstand, magazine rack, newspaper page,
  poster wall: the painter fills it with gibberish): quote the one cover that matters ("LIFE") or pick another subject."""


def direct_scripts(shorts: list[dict], ch: dict) -> None:
    """The planner plans the edit (footage searches, shots, camera, graphics, person cards, AI fallbacks,
    palette, music, thumbnail) on the final narration, which it may not change."""
    print(f"{BRAIN.capitalize()} is planning the edit...")
    final = [{"index": i, "topic": s["topic"], "title": s["title"], "pictures": pictures_of(s) or "none listed",
              "scenes": [{"scene": k + 1, "narration": t} for k, t in enumerate(s["lines"])]} for i, s in enumerate(shorts)]
    style_text = "\n".join(f"  - {e['name']} ({e['kind']}): {e['description']}; fits: {e['fits']}" for e in style_library())
    recent_looks = ch.get("recent_looks", [])[-2:] or "none"
    data = ask_ai(f"""You are the director of YouTube Shorts for a faceless channel. Niche: {ch['niche']}.
The narration below is final: never change a word of it. Plan the edit of every scene of every Short.
- pic = the number of the real picture from that Short's "pictures" list that shows this scene best, or null
  when none does. Never the same number twice in a Short; at most 2 different frames of one film. Scene 1 gets
  the most striking fitting one ([opener] first): from the story's own time (never a modern museum,
  replica or tourist photo), ideally the main character's face, and never a picture that shows the twist
  or the whole story at once (it must raise the hook's question, not answer it). Write shot from the
  picture you chose. An evidence board's
  items may carry "pic" the same way.
- image_search = a 2-5 word query to find a real photo, screenshot, portrait, artwork, document,
  place or object for this scene (e.g. "Nintendo Ultra Hand toy", "Lord Byron portrait").
  video_search = a 2-6 word video search query to find real video footage showing what this
  scene is about: gameplay, hardware demo, speedrun moment, historical newsreel, documentary clip,
  experiment or place in motion (e.g. "Super Mario 64 Bowser throw gameplay",
  "Nintendo Ultra Hand 1966 demonstration", "Niagara Falls barrel 1901 film"). Make each scene's
  video_search specific to that scene's action or subject so different scenes pull different clips.
- Edit plan for every scene:
  shot = the director's note for this scene's visual, one sentence: framing (WIDE, MEDIUM,
  CLOSE-UP or DETAIL), exactly what is on screen, and what the viewer should notice. E.g.
  "CLOSE-UP: a player spinning Bowser by the tail in Super Mario 64 and launching him toward a spike bomb."
  or "CLOSE-UP: a 1500s physician in a long robe examining a dancer's swollen feet; he looks baffled."
  The visual editor uses it to pick the real video clip or image, so describe something real footage
  or pictures from this topic's era and niche could show.
  move = camera move that suits the image: "in" (faces, details, tension), "out" (reveals),
  "left"/"right" (wide places, crowds, landscapes), "up"/"down" (tall buildings, full-length
  portraits). Vary them; never the same move twice in a row.
  graphic = on-screen callout or null. Use on 4-7 scenes, mixing at least 3 different styles,
  never scene 1 (it gets the hook title):
  {{"style": "question", "text": "WHY DIDN'T THE GUNS WORK?"}} at most once, at a cliffhanger the script
  answers LATER (the picture dims and the question holds; up to 6 words, ends with "?"),
  {{"style": "kinetic", "text": "THREE SOLDIERS", "trigger": "three"}} at most twice, for a key phrase
  that should hit hard (1-4 words, ALL spoken in that scene; its letters drop in one by one),
  {{"style": "invented", "text": "...", "trigger": "..."}} only with an invented_overlay (below), at most twice,
  {{"style": "date", "text": "1911", "trigger": "1911"}} when a key year/date is first said,
  {{"style": "place", "text": "PARIS, FRANCE", "lat": 48.86, "lon": 2.35, "trigger": "Paris"}} when
  the location is introduced (lat/lon of that place, used for an animated map); when the scene is a
  journey, add where it started and a route line is drawn:
  "from": {{"text": "NEW YORK", "lat": 40.71, "lon": -74.01}},
  {{"style": "fact", "text": "2 YEARS MISSING", "trigger": "two years"}} for the single most
  surprising fact,
  {{"style": "stat", "value": 62, "of": 97, "text": "SURVIVED", "trigger": "sixty two"}} for a number
  worth seeing: with "of" (up to 200) it becomes a grid of dots with "value" of them lighting up;
  without "of" a counter ticks up to "value" (e.g. {{"style": "stat", "value": 9000, "text": "WORDS"}}),
  {{"style": "timeline", "start": "SEPT 1", "end": "SEPT 2", "text": "17 HOURS LATER", "trigger":
  "seventeen hours"}} when time passes between two moments (a marker slides from start to end),
  {{"style": "headline", "text": "RAINMAKER BLAMED FOR FLOOD", "paper": "THE SAN DIEGO UNION", "date":
  "JANUARY 28, 1916", "trigger": "newspapers"}} when the press or the public reacted (a front page slams
  in; up to 7 words; give "paper" only if that real paper covered it, else leave it out),
  {{"style": "quote", "text": "I could make it rain anywhere", "by": "Charles Hatfield", "trigger": "he
  boasted"}} for a real, documented quote of up to 12 words (typed out on aged paper; never invent one),
  {{"style": "compare", "text": "HIS FEE", "a_label": "1916", "a_value": 10000, "a_show": "$10,000",
  "b_label": "TODAY", "b_value": 290000, "b_show": "$290,000", "trigger": "ten thousand"}} when two
  sizes, amounts or heights are worth seeing side by side (two bars grow; values must be true),
  {{"style": "stamp", "text": "HOAX", "trigger": "fake"}} for the verdict at a twist or payoff (a red
  rubber stamp thumps on; 1-2 words like HOAX, BANNED, DENIED, CONFIRMED, GUILTY).
  Max 4 words per text, and it must match what the narration says in that scene.
  trigger = the exact narration words at which it should pop up (it appears as they are spoken).
  person = when a real, named HUMAN (not an animal) is mentioned in the scene, using their full
  name (first and last); not in scene 1's first 2 seconds:
  {{"name": "Thomas Hicks", "trigger": "Thomas Hicks", "image_search": "Thomas J. Hicks 1904 marathon"}}.
  trigger = the exact words of the name as spoken in this scene's narration (their photo pops up
  at that moment). image_search must be specific enough to find THAT person (add the year or what
  they're known for). Use it every time a new person is introduced; otherwise null. A scene has a
  person OR a graphic, never both.
  emphasis = the single most important word in the scene, copied exactly from the narration
  (it glows in the captions), or null.
  transition = how this scene starts, your choice for every cut, from the STYLE LIBRARY transitions below
  (or "invented"). Edit like a good editor: a hard "cut" keeps the energy up inside one moment, "fade"
  suits time jumps and calm or sad beats, "flash" only the 2-3 biggest reveals (it has an impact sound),
  and the special ones (wipe, whip, leak, invented) at most 3 per Short, matched to the look. Scene 1's
  transition is ignored.
  ai_image = prompt for a local image generator, used only if no real video clip or photo fits this
  scene. {AI_IMAGE_RULE}
  sound = a sound of the STORY itself on one spoken word, or null (the usual): {{"word": "jammed", "sound": "gun cock"}}
  (word = spoken in this scene; sound = 1-4 plain words naming a real recordable sound: "gun cock", "ship horn",
  "crowd gasp", "splash", "church bell", "typewriter"). At most 3 per Short, only for concrete moments where the
  sound makes the line land; never for abstract lines, never music.
  full = a FULL-SCREEN motion graphic that replaces this scene's picture, or null (the usual). Use it on at
  most 2 scenes, only where it shows the moment better than any picture or footage could: a trip between
  places, a number too big to picture, a document that matters, several people/things that connect, or a
  story-specific mechanism/diagram/cause-and-effect chain.
  Rules: never scene 1 (real footage hooks better), never two in a row, only on a scene of at least
  {FULL_MIN_WORDS} words (it needs ~3 seconds), real facts only (they are
  fact-checked), labels at most 3 words, "word" = a word or name spoken in that scene's narration when that
  element should appear. One of:
  {{"type": "journey", "stops": [{{"name": "Port Elizabeth", "lat": -33.96, "lon": 25.6, "word": "Port Elizabeth"}},
   {{"name": "Uitenhage", "lat": -33.76, "lon": 25.4, "word": "Uitenhage"}}], "note": "1881 · 32 km"}}
   (1-4 real places in travel order; an old-atlas map, pins drop as named, a route line draws between them);
  {{"type": "number", "value": 30000, "label": "mourners", "icon": "person", "thing": "mourner", "each": 1000, "word": "thirty"}}
   (a big counter, then ink figures each standing for `each`; thing = what ONE figure is, a singular noun ("emu",
   "barrel", "cat"): it is painted as an ink silhouette; icon = the closest of {list(ICONS)} as a backup; for "then vs now"
   add "compare": {{"a_label": "1858", "a_value": 100, "b_label": "today", "b_value": 3}});
  {{"type": "board", "items": [{{"label": "JACK, 1890", "find": "photo of Jack the baboon at the levers", "word": "Jack"}}],
   "links": [[0, 1]]}} (an evidence board of 3-5 REAL photos pinned up with red thread between linked ones;
   find = what real photo of the story to look for; only when such photos of each item surely exist);
  {{"type": "document", "kind": "telegram", "key_line": "The baboon stays and gets paid", "date": "1890",
   "word": "telegram"}} (kind one of {list(DOC_KINDS)}; the key line is underlined in red as it is said: a
   real, documented line of at most 14 words, or a plain summary of what the document said; "paper" = the
   masthead only for a real newspaper that covered it; "find" = what real scan of it to look for, if any);
  {{"type": "custom", "kind": "diagram", "title": "VASA CROSS-SECTION", "brief": "Cross-section of the top-heavy warship tilting 20 degrees in a wind gust as water floods the open lower gunports", "words": ["gust", "twenty", "gunports"], "photos": [{{"label": "THE VASA", "find": "Vasa warship hull", "word": "warship"}}]}}
   (a bespoke scene coded from scratch for this moment when a custom visual metaphor, mechanism, cross-section,
   flow chart or photo collage fits better than the 4 standard templates; kind one of {list(CUSTOM_KINDS)}:
   "diagram" for a custom SVG cross-section/mechanism/scale/gauge, "collage" for 1-3 real archival photos
   sliding in with drawn arrows and callouts, "flow" for a step-by-step cause->effect->twist chain, "clock"
   for a clock/countdown/schedule with levers or gauges; "words" = 2-4 spoken words from the scene that trigger
   each animation beat; "photos" = 0-3 optional real photos from the pool to cut out into the scene).
  animate = true on 3-5 scenes (include scene 1 when its picture could move: motion in the very
  first frame stops people scrolling) whose picture would come alive with gentle motion of one of
  two kinds: ATMOSPHERE (water, waves, clouds, rain, snow, flags, fire, light, or smoke and steam rising
  from a visible source; never dust, fog or mist added to a picture that has none)
  or PEOPLE moving slowly and simply (working, a crowd shifting, someone walking calmly). Never fast
  action, fights, vehicles or machines in motion, or a close-up of a real person's face.
  motion = for those scenes, one short line describing the movement, else null;
  motion_people = true when the movement is people, false when it is atmosphere.
- palette: the colour scheme of this Short's graphics and captions, one of {list(PALETTES)}, chosen to
  fit the story (fire/disaster: ember or crimson; sea/ice: sky or teal; old documents: parchment; royal or
  mystical: violet; nature: lime). Vary it across Shorts.
- music_mood: the background music that fits the story's feeling, one of {MOODS} (vary it across
  Shorts; a disaster is "tense" or "somber", a funny loophole "playful", a big achievement "epic").
- thumbnail_prompt: image-generator prompt for the thumbnail background, written like ai_image (subject, setting,
  light, a real hand-made medium with its marks; same face rule). It raises the title's question without answering
  it, true to the story: ONE big focal subject that reads in under a second at phone-thumbnail size, little else,
  strong light-dark contrast. Use the strongest of these: extreme size contrast (something huge beside something
  tiny from the story); one real element of the story shown oversized; a lone small figure in a vast setting; a map
  or aerial view with one route or spot marked; a before/after split of one subject; many copies of one object.
  Clothing, buildings, tech and objects must match the story's era and niche.
- Draft description (2-3 sentences plus 3 hashtags) and 10-15 tags (refined later with real search data).
- look: ONE photo look for this Short's still pictures, or null (null is a good answer: use a look only when
  it adds to the story). {{"name": "<a library look>"}}, never {recent_looks} (used on the channel's last
  Shorts). If no library look fits but a new one would really serve THIS story, invent it:
  {{"invent": {{"title": "Wanted poster", "brief": "what it looks like, specific: materials, colours, texture,
  what moves", "fallback": "<the closest library look>"}}}}. The picture picker puts it on 2-4 still scenes
  (never scene 1, never real film).
- invented_transition / invented_overlay: null, or (only if you use "invented" as a transition / a graphic
  style) {{"title": "...", "brief": "what it looks like and how it moves", "fallback": "<closest library
  transition / overlay>"}}. Invent only when the library has nothing that fits; a fallback is used if it fails.
STYLE LIBRARY (name (kind): what it is; fits):
{style_text}
Shorts: {json.dumps(final, ensure_ascii=False)}
Reply with ONLY JSON, one entry in "scenes" per scene, in order: {{"shorts": [{{"index": 0, "palette": "...",
"music_mood": "...", "thumbnail_prompt": "...", "description": "...", "tags": ["..."], "look": null,
"invented_transition": null, "invented_overlay": null,
"scenes": [{{"pic": null, "image_search": "...", "video_search": "...", "shot": "...", "move": "in", "graphic": null,
"person": null, "emphasis": "...", "transition": "fade", "ai_image": "...", "animate": false,
"motion": null, "motion_people": false, "sound": null, "full": null}}]}}]}}""")
    plans = {r["index"]: r for r in data.get("shorts", []) if isinstance(r, dict) and isinstance(r.get("index"), int)}
    for i, s in enumerate(shorts):
        r = plans.get(i, {})
        s.update({k: r[k] for k in ("palette", "music_mood", "thumbnail_prompt", "description", "tags") if r.get(k)})
        s.update({k: r.get(k) for k in ("look", "invented_transition", "invented_overlay")})  # validated in write_scripts
        scenes = r.get("scenes") if isinstance(r.get("scenes"), list) else []
        s["scenes"] = [{**(scenes[k] if k < len(scenes) and isinstance(scenes[k], dict) else {}), "narration": t}
                       for k, t in enumerate(s.pop("lines"))]  # the final words win over anything the director echoed
        for sc in s["scenes"]:
            sc["image_search"] = str(sc.get("image_search") or "").strip() or s["subject"]


def article_text(title: str) -> str:
    """Plain text of an English Wikipedia article ('' when missing or unreachable)."""
    raw = wm_get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext=1"
                 f"&redirects=1&titles={urllib.parse.quote(title)}", f'Wikipedia "{title}" text')
    pages = json.loads(raw).get("query", {}).get("pages", {}) if raw else {}
    return next((p.get("extract") or "" for p in pages.values()), "")


def fact_check(s: dict) -> bool:
    """Check every line against the story's Wikipedia articles and rewrite what they don't support.
    Runs before the edit plan is validated, so callouts whose trigger words changed drop out there.
    Notes go in s["fact_check"] (edit_plan.txt). False when the story's central claim is false."""
    print(f'Fact-checking "{s["title"]}"...')
    texts = s.pop("_texts", None) or {t: article_text(t)[:15000] for t in s["wiki_articles"][:4]}
    s["research"] = texts  # motion-graphic rescues reuse it (never saved in state.json)
    script = [{"scene": i + 1, "narration": sc["narration"], "shot": sc.get("shot"), "ai_image": sc.get("ai_image"),
               "image_search": sc.get("image_search"), "video_search": sc.get("video_search"),
               "graphic": sc.get("graphic"), "person": sc.get("person"), "full": sc.get("full")}
              for i, sc in enumerate(s["scenes"])]
    data = ask_ai(f"""You are a strict fact-checker for a fact-based Shorts channel. Check every claim in
this script and its on-screen text against the Wikipedia articles below.
- Supported by the articles: keep it.
- Contradicted by them: fix it.
- Not in the articles: keep it only if you are confident it is true and well documented. If sources
  disagree or it is a legend, make the line accurate ("legend says", "reports claim") or replace it
  with a supported fact.
Rewrite only the scenes that need it. Keep each about as long as it was (at most {LONG_SCENE_WORDS} words) with the same role in the story, scene
1's first sentence at most 8 words, and every word a graphic or person card pops up on ("trigger")
when it is still correct. drop_graphic = true when that scene's graphic itself shows a wrong fact.
"full" is a full-screen motion graphic (map stops, a number, board labels, a document's key line): when any
of its places, numbers, labels or quoted words is wrong, give full_fix = the same object corrected, or
drop_full = true when it can't be fixed.
shot / ai_image / image_search / video_search: when your fix changes what that scene shows happening,
rewrite them to match the corrected line (same format and art style as before); else null.
story_holds = false only when the story's central claim is false or a myth; then myth_note = one line
on what really happened (else null).
hook_text / thumbnail_text: a corrected version only if the current one is false, else null.
Script: {json.dumps(script, ensure_ascii=False)}
hook_text: {s.get("hook_text")!r} | thumbnail_text: {s.get("thumbnail_text")!r}
Wikipedia articles: {json.dumps(texts, ensure_ascii=False)}
Reply with ONLY JSON: {{"story_holds": true, "fixes": [{{"scene": 3, "narration": "...", "drop_graphic": false, "drop_full": false, "full_fix": null,
"shot": null, "ai_image": null, "image_search": null, "video_search": null, "why": "..."}}], "hook_text": null, "thumbnail_text": null, "myth_note": null}}""", fatal=False)
    if not isinstance(data, dict):
        s["fact_check"] = ["NOT CHECKED (the AI didn't reply): check the facts yourself before posting"]
        return True
    s["fact_check"] = []
    for f in data.get("fixes") or []:
        n, line = (f.get("scene"), f.get("narration")) if isinstance(f, dict) else (None, None)
        if isinstance(n, int) and 1 <= n <= len(s["scenes"]) and isinstance(line, str) and 0 < len(line.split()) <= 30:
            sc = s["scenes"][n - 1]
            s["fact_check"].append(f'scene {n}: "{sc["narration"]}" -> "{line.strip()}" ({str(f.get("why") or "")[:500]})')
            sc["narration"] = line.strip()
            for k in ("shot", "ai_image", "image_search", "video_search"):  # the picture/footage must not show the corrected-away version
                if isinstance(f.get(k), str) and f[k].strip():
                    sc[k] = f[k].strip()
        if isinstance(n, int) and 1 <= n <= len(s["scenes"]) and f.get("drop_graphic") is True \
                and s["scenes"][n - 1].get("graphic"):  # wrong on-screen text goes even when the spoken line was right
            s["fact_check"].append(f"scene {n}: on-screen graphic removed ({str(f.get('why') or '')[:300]})")
            s["scenes"][n - 1]["graphic"] = None
        if isinstance(n, int) and 1 <= n <= len(s["scenes"]) and s["scenes"][n - 1].get("full"):
            sc = s["scenes"][n - 1]  # a motion-graphic correction counts even when the spoken line was right
            if f.get("drop_full") is True:
                s["fact_check"].append(f"scene {n}: motion graphic removed ({str(f.get('why') or '')[:300]})")
                sc["full"] = None
            elif isinstance(f.get("full_fix"), dict) and f["full_fix"].get("type") in FULL_TYPES:
                s["fact_check"].append(f"scene {n}: motion graphic corrected ({str(f.get('why') or '')[:300]})")
                sc["full"] = f["full_fix"]  # validated with the rest of the plan afterwards (clean_full)
    for k in ("hook_text", "thumbnail_text"):
        if isinstance(data.get(k), str) and data[k].strip():
            s["fact_check"].append(f'{k}: "{s.get(k)}" -> "{data[k].strip()}"')
            s[k] = data[k].strip()
    print(f"  {len(s['fact_check'])} fixes" if s["fact_check"] else "  every line holds up")
    s["myth_note"] = str(data.get("myth_note") or "").strip()
    return data.get("story_holds") is not False


def is_num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def coords(lat, lon) -> bool:
    return is_num(lat) and is_num(lon) and -85 <= lat <= 85 and -180 <= lon <= 180


def clean_graphic(g, said: list[str]) -> dict | None:
    """One planned callout, validated (LLM output is untrusted); None drops it."""
    if not (isinstance(g, dict) and g.get("style") in PLANNED_STYLES and str(g.get("text", "")).strip()):
        return None
    text = str(g["text"]).strip()
    out = {"style": g["style"], "text": text[:90] if g["style"] == "quote" else text.upper()[:48 if g["style"] == "headline" else 28]}
    if g["style"] == "headline":
        out.update({k: str(g[k]).strip().upper()[:28] for k in ("paper", "date") if str(g.get(k) or "").strip()})
    if g["style"] == "quote":
        if not str(g.get("by") or "").strip() or len(text.split()) > 14:
            return None
        out["by"] = str(g["by"]).strip()[:40]
    if g["style"] == "compare":
        labels = [str(g.get(k) or "").strip().upper()[:14] for k in ("a_label", "b_label")]
        values = [g.get(k) for k in ("a_value", "b_value")]
        if not all(labels) or not all(is_num(v) and 0 < v < 1e12 for v in values):
            return None
        for side, label, v in zip("ab", labels, values):
            show = str(g.get(f"{side}_show") or "").strip().upper()[:14] or f"{v:,.10g}"
            out.update({f"{side}_label": label, f"{side}_value": float(v), f"{side}_show": show})
    if g["style"] == "stamp" and len(text.split()) > 2:
        return None
    if g["style"] == "question":  # answered later in the script: a question, never a claim
        if not text.endswith("?") or len(text.split()) > 6:
            return None
        out["text"] = text.upper()[:40]
    if g["style"] == "kinetic":  # the spoken words themselves, landing hard
        spoken = words_of(text)
        if not 1 <= len(text.split()) <= 4 or len(re.sub(r"\W", "", text)) > 20 or not spoken \
                or not all(w in said for w in spoken) or not (isinstance(g.get("trigger"), str) and contains(said, words_of(g["trigger"]))):
            return None
    if g["style"] == "invented" and len(text.split()) > 6:
        return None
    if g["style"] == "place" and coords(g.get("lat"), g.get("lon")):  # coordinates feed the animated map
        out.update(lat=float(g["lat"]), lon=float(g["lon"]))
        f = g.get("from")
        if isinstance(f, dict) and coords(f.get("lat"), f.get("lon")) and str(f.get("text", "")).strip():
            out["from"] = {"text": str(f["text"]).strip().upper()[:28], "lat": float(f["lat"]), "lon": float(f["lon"])}
    if g["style"] == "stat":
        v, of = g.get("value"), g.get("of")
        if not (is_num(v) and 0 < v < 1e9):
            return None
        out["value"] = v
        if isinstance(of, int) and not isinstance(of, bool) and float(v).is_integer() and v <= of <= 200:
            out["of"] = of
    if g["style"] == "timeline":
        ends = [str(g.get(k) or "").strip().upper()[:16] for k in ("start", "end")]
        if not all(ends):
            return None
        out["start"], out["end"] = ends
    if isinstance(g.get("trigger"), str) and contains(said, words_of(g["trigger"])):
        out["trigger"] = g["trigger"].strip()
    return out


def show_number(v: float) -> str:
    """How the big-number scene prints a value: 30,000 / 1.5 MILLION / 2 BILLION / 0.3."""
    for size, word in ((1e9, "BILLION"), (1e6, "MILLION")):
        if v >= size:
            return f"{v / size:,.1f}".removesuffix(".0") + f" {word}"
    return f"{v:,.2f}".rstrip("0").rstrip(".") if not float(v).is_integer() else f"{v:,.0f}"


def number_figures(value: float, each) -> tuple[float, int]:
    """(what one ink figure stands for, how many to draw): the planner's `each` when it gives 1-60 figures,
    else the smallest round 1/2/5 x 10^k that does."""
    if not (is_num(each) and each > 0 and value / each <= MAX_FIGURES):
        each = next(m * 10 ** k for k in range(-2, 13) for m in (1, 2, 5) if value / (m * 10 ** k) <= MAX_FIGURES)
    return each, max(1, round(value / each))


def clean_full(f, said: list[str]) -> dict | None:
    """One planned full-screen motion graphic, validated (AI output is untrusted); None drops it. Timing words
    (`word`) are kept only when the narration says them; the renderer times everything else evenly."""
    if not (isinstance(f, dict) and f.get("type") in FULL_TYPES):
        return None

    def text(v, n: int, upper: bool = False) -> str:
        s = str(v or "").strip()[:n].strip()
        return s.upper() if upper else s

    def word(d: dict) -> dict:
        w = d.get("word")
        return {"word": w.strip()} if isinstance(w, str) and contains(said, words_of(w)) else {}

    out = {"type": f["type"]}
    if f.get("skin") in SKINS:
        out["skin"] = f["skin"]
    if f["type"] == "board":
        items = [{"label": " ".join(text(it.get("label"), 60, True).split()[:3])[:24], "find": text(it.get("find"), 120), **word(it),
                  **({"pic": it["pic"]} if type(it.get("pic")) is int else {})}
                 for it in f.get("items") or [] if isinstance(it, dict) and text(it.get("label"), 60)][:5]
        if len(items) < 3:
            return None
        links = [[a, b] for a, b in (lk for lk in f.get("links") or [] if isinstance(lk, list) and len(lk) == 2)
                 if isinstance(a, int) and isinstance(b, int) and not isinstance(a, bool) and not isinstance(b, bool)
                 and a != b and 0 <= a < len(items) and 0 <= b < len(items)]
        out.update(items=items, links=links)
    elif f["type"] == "journey":
        stops = [{"name": text(s.get("name"), 28), "lat": float(s["lat"]), "lon": float(s["lon"]), **word(s)}
                 for s in f.get("stops") or [] if isinstance(s, dict) and text(s.get("name"), 28) and coords(s.get("lat"), s.get("lon"))][:4]
        if not stops:
            return None
        out["stops"] = stops
        if text(f.get("note"), 24):
            out["note"] = text(f.get("note"), 24, True)
    elif f["type"] == "number":
        v = f.get("value")
        if not (is_num(v) and 0 < v < 1e12 and text(f.get("label"), 24)):
            return None
        each, figures = number_figures(v, f.get("each"))
        out.update(value=v, show=show_number(v), label=text(f["label"], 24, True), each=each, figures=figures,
                   icon=f.get("icon") if f.get("icon") in ICONS else "person", **word(f))
        thing = text(f.get("thing"), 24).lower()
        if re.fullmatch(r"[a-z][a-z '-]{1,23}", thing):  # what one figure is: painted as an ink silhouette
            out["thing"] = thing
        c = f.get("compare")
        if isinstance(c, dict) and all(text(c.get(k), 14) for k in ("a_label", "b_label")) and all(
                is_num(c.get(k)) and 0 <= c[k] < 1e12 for k in ("a_value", "b_value")) and max(c["a_value"], c["b_value"]) > 0:
            out["compare"] = {"a_label": text(c["a_label"], 14, True), "a_value": c["a_value"],
                              "b_label": text(c["b_label"], 14, True), "b_value": c["b_value"]}
    elif f["type"] == "custom":
        title, brief = text(f.get("title"), 38, True), text(f.get("brief"), 260)
        if not title or not brief:
            return None
        kind = f.get("kind") if f.get("kind") in CUSTOM_KINDS else "diagram"
        raw_words = f.get("words") if isinstance(f.get("words"), list) else ([f["word"]] if isinstance(f.get("word"), str) else [])
        words = [w.strip() for w in raw_words if isinstance(w, str) and contains(said, words_of(w))][:4]
        photos = [{"label": " ".join(text(p.get("label") or p.get("find"), 40, True).split()[:3])[:22],
                   "find": text(p.get("find") or p.get("label"), 120), **word(p)}
                  for p in (f.get("photos") or []) if isinstance(p, dict) and (text(p.get("label"), 40) or text(p.get("find"), 120))][:3]
        out.update(kind=kind, title=title, brief=brief, words=words, photos=photos)
    else:
        line = text(f.get("key_line"), 160)
        if f.get("kind") not in DOC_KINDS or not line or len(line.split()) > 14:
            return None
        out.update(kind=f["kind"], key_line=line, **word(f),
                   **{k: text(f.get(k), 40) for k in ("date", "paper", "find") if text(f.get(k), 40)})
        if "find" in out:
            out["find"] = text(f.get("find"), 120)
    return out


def clean_transition(v) -> str:
    """A planned scene change: a library transition name or "invented"; anything else is a fade (the old default)."""
    names = {e["name"] for e in style_library("transition")} | {"invented"}
    return v if isinstance(v, str) and v in names else "fade"


def clean_look(v, ch: dict) -> dict | None:
    """The Short's photo look: {"name": <library look>} (not one of the channel's last 2), or an invention
    {"name": "invented", "title", "brief", "fallback": <library look>}; None = no look."""
    if not isinstance(v, dict):
        return None
    if isinstance(v.get("invent"), dict):
        inv = clean_invention(v["invent"], "look")
        return {"name": "invented", **inv} if inv else None
    looks = {e["name"] for e in style_library("look")}
    name = v.get("name")
    return {"name": name} if name in looks and name not in ch.get("recent_looks", [])[-2:] else None


def clean_invention(v, kind: str) -> dict | None:
    """A planned invention {"title", "brief", "fallback": <library name of that kind>}, validated; None drops it."""
    if not isinstance(v, dict):
        return None
    title, brief = str(v.get("title") or "").strip(), str(v.get("brief") or "").strip()
    names = {e["name"] for e in style_library(kind)}
    return {"title": title[:40], "brief": brief[:400], "fallback": v["fallback"]} \
        if title and brief and v.get("fallback") in names else None


def settle_style(s: dict, ch: dict) -> None:
    """Validates the Short's style plan (look, invented transition/overlay); an "invented" transition or overlay
    without its validated spec falls back to a fade / no graphic."""
    s["look"] = clean_look(s.get("look"), ch)
    s["invented_transition"] = clean_invention(s.get("invented_transition"), "transition")
    s["invented_overlay"] = clean_invention(s.get("invented_overlay"), "overlay")
    for sc in s["scenes"]:
        if sc.get("transition") == "invented" and not s["invented_transition"]:
            sc["transition"] = "fade"
        if (sc.get("graphic") or {}).get("style") == "invented" and not s["invented_overlay"]:
            sc["graphic"] = None


def limit_style(scenes: list[dict]) -> None:
    """Guardrails for the style library (STYLE_CAPS): the hook keeps only its title (no question/kinetic/invented
    overlay), at most 1 question beat, 2 kinetic titles, 2 invented overlays and 3 special transitions per Short;
    later ones are dropped (graphics) or become fades (transitions)."""
    used = {"question": 0, "kinetic": 0, "invented": 0, "special": 0}
    for i, sc in enumerate(scenes):
        style = (sc.get("graphic") or {}).get("style")
        if style in ("question", "kinetic", "invented"):
            used[style] += 1
            if i == 0 or used[style] > STYLE_CAPS[style]:
                sc["graphic"] = None
        if i and sc.get("transition") in SPECIAL_TRANSITIONS:
            used["special"] += 1
            if used["special"] > STYLE_CAPS["special"]:
                sc["transition"] = "fade"


def limit_full(scenes: list[dict], most: int) -> None:
    """Never scene 1 (real footage keeps the hook), never two in a row, never a scene too short to play it
    (FULL_MIN_WORDS), at most `most`; a kept one replaces that scene's overlay graphic and person card (one
    thing on screen at a time)."""
    kept, last = 0, -2
    for i, sc in enumerate(scenes):
        if not sc.get("full"):
            sc["full"] = None
        elif i == 0 or i == last + 1 or kept >= most or len(sc["narration"].split()) < FULL_MIN_WORDS:
            sc["full"] = None
        else:
            kept, last = kept + 1, i
            sc["graphic"] = sc["person"] = None
            sc["animate"] = False  # no AI clip for a scene nobody will see as a picture


def mark_details(short: dict, choices: list[dict], work: Path) -> None:
    """Let Claude circle (or point an arrow at) a detail in up to 2 chosen pictures. It sees each
    picture under a lettered 10x10 grid and names the cell, which places the mark accurately. Only
    scenes with a picture and no other callout or person card qualify. Failure just means no marks."""
    folder = work / "marks"
    folder.mkdir(exist_ok=True)
    eligible = {}
    for i, (sc, c) in enumerate(zip(short["scenes"], choices)):
        if i and c["bg"] and not c.get("film") and not sc["graphic"] and not sc["person"] and not sc.get("full"):
            try:
                img = Image.open(io.BytesIO(c["bg"][0])).convert("RGB")
            except Exception:
                continue
            img.thumbnail((1000, 1000))
            d, font = ImageDraw.Draw(img), ImageFont.truetype(FONT, 26)
            for k in range(1, 10):
                x, y = img.width * k / 10, img.height * k / 10
                d.line((x, 0, x, img.height), fill=YELLOW, width=2)
                d.line((0, y, img.width, y), fill=YELLOW, width=2)
            for k in range(10):
                d.text((img.width * (k + 0.5) / 10 - 8, 4), "ABCDEFGHIJ"[k], font=font, fill=YELLOW, stroke_width=3, stroke_fill="black")
                d.text((6, img.height * (k + 0.5) / 10 - 14), str(k + 1), font=font, fill=YELLOW, stroke_width=3, stroke_fill="black")
            img.save(folder / f"scene{i + 1}.jpg", quality=90)
            eligible[i + 1] = sc
    if not eligible:
        return
    lines = "\n".join(f"scene {n}: {folder / f'scene{n}.jpg'} | narration: {sc['narration']}" for n, sc in eligible.items())
    data = ask_ai(f"""You are the motion-graphics editor of a YouTube Short: "{short['title']}". Open and look at
these pictures; each has a 10x10 grid, columns A-J left to right, rows 1-10 top to bottom.
{lines}
For at most 2 scenes, choose ONE specific detail that the narration is about and a viewer could
miss (a face in a crowd, a sign, a crack, a small object), clearly visible in the picture. Give the
grid cell of its centre, shape "circle" (an object or face) or "arrow" (a spot in a wide view), and
a label of 1-3 words. If no picture has such a detail, reply with an empty list.
Reply with ONLY JSON: {{"marks": [{{"scene": 3, "cell": "D4", "shape": "circle", "label": "THE CRACK"}}]}}""",
                      fatal=False, read_dir=folder)
    for m in ((data or {}).get("marks") or [])[:2]:
        if not isinstance(m, dict):
            continue
        cell = re.fullmatch(r"([A-J])(10|[1-9])", str(m.get("cell", "")).strip().upper())
        sc = eligible.get(m.get("scene")) if cell else None
        label = str(m.get("label") or "").strip().upper()
        if sc and not sc["graphic"] and 0 < len(label.split()) <= 3:
            sc["graphic"] = {"style": "mark", "text": label[:24], "shape": "arrow" if m.get("shape") == "arrow" else "circle",
                             "x": ("ABCDEFGHIJ".index(cell[1]) + 0.5) / 10, "y": (int(cell[2]) - 0.5) / 10}


def fallback_graphic(g: dict) -> tuple[str, str]:
    """(style, text) for the built-in renderer, which draws only dates, places and fact boxes."""
    if g["style"] == "stat":
        num = f"{g['value']:,.0f}" if float(g["value"]).is_integer() else f"{g['value']:,.1f}"
        return "fact", f"{num}{' OF ' + str(g['of']) if 'of' in g else ''} {g['text']}"
    if g["style"] == "compare":
        return "fact", f"{g['a_label']} {g['a_show']} VS {g['b_label']} {g['b_show']}"
    if g["style"] == "quote":
        return "fact", f"\"{g['text']}\" - {g['by']}"
    return (g["style"] if g["style"] in ("date", "place", "fact") else "fact"), g["text"]


def words_of(text: str) -> list[str]:
    """Lowercase, accent-free word tokens, for matching names against spoken words."""
    plain = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.findall(r"[a-z0-9]+", plain.lower())


def contains(words: list[str], phrase: list[str]) -> bool:
    return bool(phrase) and any(words[k:k + len(phrase)] == phrase for k in range(len(words)))


def spoken_span(words: list[tuple[float, float, str]], phrase: str) -> tuple[float, float] | None:
    """(start, end) of the first time `phrase` is spoken, from TTS word timings."""
    target, flat = words_of(phrase), []
    for start, end, text in words:  # a TTS "word" can hold punctuation or several tokens
        flat += [(start, end, tok) for tok in words_of(text)]
    toks = [tok for _, _, tok in flat]
    for k in range(len(toks)):
        if target and toks[k:k + len(target)] == target:
            return flat[k][0], flat[k + len(target) - 1][1]
    return None


def spoken_at(words: list[tuple[float, float, str]], phrase: str) -> float | None:
    """Start time of the first time `phrase` is spoken, from TTS word timings."""
    span = spoken_span(words, phrase)
    return span[0] if span else None


# Seconds a full-screen motion graphic's last beat needs before the cut: the AI-coded scene adds its own delay
# (Mike's "NO SYRINGE" stamp: beat + 0.35 s, ~0.5 s to land), then it should stay a moment (it showed 0.3 s, 2026-10-21).
FULL_SETTLE = 1.6


def full_cues(full: dict, words: list[tuple[float, float, str]], start: float, end: float) -> dict:
    """When each element of a full-screen motion graphic appears (absolute seconds): on its spoken `word`, else
    on an even slot inside the scene; board prints and map stops always appear in order, 0.4 s apart at least.
    The last beat comes FULL_SETTLE before the cut so it can finish and be seen; a late beat pulls the earlier ones
    forward with it (squeezed, order kept) instead of all piling up at the end."""
    lo, hi = start + 0.4, max(start + 0.7, end - FULL_SETTLE)
    said = lambda w: (start + spoken_at(words, w)) if isinstance(w, str) and spoken_at(words, w) is not None else None  # noqa: E731

    def squeeze(ts: list[float]) -> list[float]:
        k = min(1.0, (hi - lo) / max(1e-6, ts[-1] - lo)) if ts else 1.0
        return [round(lo + (t - lo) * k, 3) for t in ts]

    if full["type"] in ("board", "journey"):
        parts = full["items" if full["type"] == "board" else "stops"]
        times, last = [], lo - 0.4
        for k, p in enumerate(parts):
            t = said(p.get("word"))
            t = lo + (hi - lo) * k / max(1, len(parts) - 1) * 0.85 if t is None else t
            last = max(t, last + 0.4)
            times.append(last)
        times = squeeze(times)
        cue = {"times": times}
        if full["type"] == "journey":
            cue["noteAt"] = round(min(hi, times[-1] + 0.4), 3)
        return cue
    if full["type"] == "custom":
        tokens = list(full.get("words") or []) or [p.get("word") for p in full.get("photos") or [] if isinstance(p, dict) and p.get("word")]
        n = max(3, len(tokens))
        cues, last = [], lo - 0.35
        for k in range(n):
            t = said(tokens[k]) if k < len(tokens) else None
            t = lo + (hi - lo) * k / max(1, n - 1) * 0.85 if t is None else t
            last = max(t, last + 0.35)
            cues.append(last)
        return {"cues": squeeze(cues)}
    if full["type"] == "number":
        t = said(full.get("word"))
        return {"at": round(min(hi, t if t is not None else lo), 3)}
    span = spoken_span(words, full["key_line"])
    if span:
        return {"at": round(start + span[0], 3), "lineEnd": round(start + span[1], 3)}
    t = said(full.get("word"))
    at = min(hi, t if t is not None else start + 0.6)
    return {"at": round(at, 3), "lineEnd": round(at + 1.2, 3)}


def search_suggestions(query: str) -> list[str]:
    """What people actually type into YouTube search (free autocomplete endpoint, no key)."""
    try:
        url = ("https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q="
               + urllib.parse.quote(query))
        return json.loads(fetch(url, timeout=15))[1]
    except Exception:
        return []


def seo_pass(shorts: list[dict], ch: dict | None = None) -> None:
    """Rewrite title/description/tags around real YouTube search phrases; add a pinned comment."""
    if not shorts:
        return
    print("Researching search keywords...")
    ch = ch or (load_channel() if CHANNEL.exists() else {})
    niche = ch.get("niche", "")
    leaders = [t["title"] for t in trend_research(ch)[:15]] if niche else []  # cached for the day
    results = logbook_results()
    research = []
    for i, s in enumerate(shorts):
        subject = s.get("subject") or s["title"]
        seeds = dict.fromkeys([subject, f"{subject} facts", f"why {subject}"] + s.get("wiki_articles", [])[1:3]
                              + s.get("search_terms", []))
        suggestions = {q: got for q in seeds if (got := search_suggestions(q))}  # each list: most-searched first
        research.append({"index": i, "title": s["title"], "description": s.get("description", ""),
                         "hook_sentence": re.split(r"(?<=[.!?])\s+", s["scenes"][0]["narration"].strip())[0],
                         "hook_text": s.get("hook_text"), "thumbnail_text": s.get("thumbnail_text"),
                         "script": " ".join(sc["narration"] for sc in s["scenes"]),
                         "fact_check_corrections": s.get("fact_check", []),
                         "youtube_search_suggestions": suggestions})
    data = ask_ai(f"""You are a YouTube SEO specialist for a Shorts channel{f' in this niche: {niche}' if niche else ''}. For each Short
below you get its draft metadata, its script, what viewers see in the first second (hook_sentence
spoken, hook_text big on screen, thumbnail_text), and REAL YouTube autocomplete phrases, grouped by what
was typed, each list in YouTube's order: most-searched first (some are irrelevant, e.g. unrelated songs
or movies with the same name: ignore those).
{f"Titles of the top recent Shorts in this niche, by views per day (learn their patterns, never copy them):{chr(10)}{json.dumps(leaders, ensure_ascii=False)}{chr(10)}" if leaders else ""}{f"How our own posted Shorts did (title, views, notes):{chr(10)}{results}{chr(10)}" if results else ""}For each Short write:
- title: under 60 characters, and its first 40 characters must work alone (the Shorts player can cut
  the rest). Curiosity-driven, containing the most-searched relevant phrase near the start. It must
  promise what the hook delivers without repeating the hook_sentence, hook_text or thumbnail_text
  (viewers see all of them together). No "#shorts", no emoji, no clickbait that the video doesn't deliver.
- Title, description and pinned comment may only claim what the script says. fact_check_corrections
  lists claims our fact check removed as false or unproven: never bring one back.
- description: first sentence naturally contains the main search phrase (it shows in search
  results), the second a different relevant search phrase; 2-3 sentences total; then a line with
  exactly 3 relevant hashtags, #shorts last.
- tags: 10-15, mixing the relevant real search phrases with broader niche terms.
- pinned_comment: one short question that invites viewers to reply (opinion or "did you know").
Shorts: {json.dumps(research, ensure_ascii=False)}
Reply with ONLY JSON: {{"shorts": [{{"index": 0, "title": "...", "description": "...",
"tags": ["..."], "pinned_comment": "..."}}]}}""")
    for r in data.get("shorts", []):  # keep the draft if the reply is incomplete
        i = r.get("index")
        if isinstance(i, int) and 0 <= i < len(shorts) and r.get("title") and r.get("tags"):
            shorts[i].update({k: r[k] for k in ("title", "description", "tags", "pinned_comment") if r.get(k)})
    for s in shorts:  # emoji in titles: no search value, off-tone; the pinned comment may keep them
        s["title"] = re.sub(r"\s{2,}", " ", re.sub(r"[\U0001F000-\U0001FAFF☀-➿️‍]", "", s["title"])).strip()


def srt(words: list[tuple[float, float, str]], path: Path) -> None:
    """Exact-narration caption file to upload in YouTube Studio (searchable, unlike burned-in text)."""
    def ts(t: float) -> str:
        ms = round(t * 1000)
        return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"
    blocks = []
    for n, i in enumerate(range(0, len(words), 7), 1):
        chunk = words[i:i + 7]
        blocks.append(f"{n}\n{ts(chunk[0][0])} --> {ts(chunk[-1][1])}\n{' '.join(w[2] for w in chunk)}\n")
    path.write_text("\n".join(blocks), encoding="utf-8")


def fetch(url: str, timeout: int = 60, ua: str = "ShortsMaker/1.0 (personal video script)") -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


_last_wm = 0.0
_wm_lock = threading.Lock()
# Wikimedia's User-Agent policy wants contact info; without it nearly every request gets a 429.
WM_UA = "ShortsMaker/1.0 (gutierrezdishann@gmail.com) python-urllib"
CACHE = ROOT / "cache"  # downloaded Wikimedia images, pruned after 30 days
POOLS = CACHE / "pools"  # per topic: the pictures gathered before writing + their AI picture list
MIN_USABLE = 6  # usable real pictures/clips a topic needs, else a backup topic replaces it
TOPIC_BACKUPS = 2
IMG_PROPS = "&prop=imageinfo&iiprop=url|size|mime|extmetadata&iiextmetadatafilter=LicenseShortName|Artist|Credit"
# Wikimedia serves thumbnails only at these widths; anything else (or bulk original files) gets
# rate-limited with a 10-minute ban (mediawiki.org/wiki/Common_thumbnail_sizes).
THUMB_STEPS = [330, 500, 960, 1280, 1920]
# File-title words that mean "not a scene image": signatures, heraldry, site furniture, diagrams, Wiki icons.
JUNK = {"signature", "autograph", "logo", "icon", "coat", "arms", "flag", "seal", "symbol", "emblem",
        "blank", "placeholder", "stub", "diagram", "chart", "graph", "plaque", "barnstar", "wikipedia",
        "cscr", "oojs", "shackle", "padlock", "ambox", "portal", "nuvola", "wpvg"}
STOPWORDS = {"the", "and", "for", "with", "from", "that", "this", "into", "over", "under", "about",
             "how", "why", "who", "what", "when", "where", "was", "were", "are", "his", "her", "its",
             "out", "old", "new", "one", "two", "first", "last", "most", "more", "some", "any"}
JUNK_VIDEO = {"reaction", "reacts", "podcast", "tierlist", "unboxing", "lyric", "lyrics", "karaoke",
              "livestream", "asmr", "reupload", "compilation", "parody", "animated", "animation",
              "cartoon", "gmod", "sfm", "meme", "memes", "soundtrack", "ost", "remix", "lego"}


def wm_get(url: str, what: str = "Wikimedia request", gap: float = 1.0) -> bytes | None:
    """GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate limits (HTTP 429).
    Long bans are not waited out: that one request is skipped. Image files are cached on disk, so
    nothing is downloaded twice. None on failure."""
    global _last_wm
    cached = CACHE / hashlib.sha1(url.encode()).hexdigest() if "upload.wikimedia.org" in url else None
    if cached and cached.exists():
        return cached.read_bytes()
    for attempt in range(3):
        with _wm_lock:
            time.sleep(max(0.0, _last_wm + gap - time.time()))
            _last_wm = time.time()
        try:
            data = fetch(url, ua=WM_UA)
            if cached:
                CACHE.mkdir(exist_ok=True)
                cached.write_bytes(data)
            return data
        except urllib.error.HTTPError as e:
            wait = int(e.headers.get("Retry-After") or 0) or 5 * (attempt + 1)
            if e.code != 429 or attempt == 2 or wait > 30:
                print(f"    {what} failed ({e.code}), skipping it")
                return None
            print(f"    Wikimedia busy, waiting {wait}s...")
            time.sleep(wait)
        except Exception as e:
            print(f"    {what} failed ({e})")
            return None
    return None


def thumb_url(original: str, width: int, orig_w: int) -> str:
    """URL of a standard-size Wikimedia thumbnail: the largest allowed step that fits in the image
    (capped at `width`), or the original file if it's smaller than every step."""
    original = original.split("?", 1)[0]  # the API adds tracking parameters to file URLs
    w = max((st for st in THUMB_STEPS if st <= width and st < orig_w), default=0)
    if not w or "/thumb/" in original:
        return original
    site, _, rest = original.partition("/wikipedia/")
    project, _, path = rest.partition("/")
    return f"{site}/wikipedia/{project}/thumb/{path}/{w}px-{path.rsplit('/', 1)[-1]}"


def usable_license(meta: dict) -> tuple[bool, str | None]:
    """(ok, credit). Public domain/CC0 need no credit; all other Wikimedia/Wikipedia media (CC BY,
    CC BY-SA, Attribution, GFDL, Fair use screenshots/covers) is allowed and credited on screen + in upload.txt."""
    lic = re.sub(r"<[^>]+>", "", meta.get("LicenseShortName", {}).get("value", "")).strip()
    low = lic.lower()
    if "public domain" in low or "cc0" in low or low.startswith("pd"):
        return True, None
    raw_artist = meta.get("Artist", {}).get("value", "") or meta.get("Credit", {}).get("value", "")
    artist = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw_artist)).strip()
    if artist and lic:
        return True, f"{artist[:55]}, {lic[:20]}"
    return True, (artist[:60] or lic[:40] or "Wikimedia")


def wm_files(api_url: str, source: str) -> list[dict]:
    """Usable images from a Wikimedia/Wikipedia API query: photos, screenshots, paintings and art,
    big enough (250px+ so retro game screenshots and portraits qualify), not a thin strip or icon."""
    raw = wm_get(api_url, f"{source} lookup")
    if not raw:
        return []
    found = []
    for p in json.loads(raw).get("query", {}).get("pages", {}).values():
        info = (p.get("imageinfo") or [{}])[0]
        ok, credit = usable_license(info.get("extmetadata", {}))
        w, h = info.get("width", 0), info.get("height", 1) or 1
        if (ok and info.get("mime") in ("image/jpeg", "image/png") and w >= 250 and 0.33 <= w / h <= 3
                and not JUNK & set(words_of(p["title"]))):
            found.append({"title": p["title"], "url": thumb_url(info["url"], 1920, w), "credit": credit,
                          "small": thumb_url(info["url"], 330, w), "source": source, "size": w * h})
    return sorted(found, key=lambda c: -c["size"])


def commons_search(query: str, limit: int = 4) -> list[dict]:
    api = ("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search"
           f"&gsrsearch={urllib.parse.quote(query + ' filetype:bitmap')}&gsrnamespace=6&gsrlimit=20" + IMG_PROPS)
    return wm_files(api, f'Commons search "{query}"')[:limit]


def article_images(title: str, limit: int = 12) -> list[dict]:
    """Images used in an English Wikipedia article: chosen by editors, so almost always on topic."""
    api = ("https://en.wikipedia.org/w/api.php?action=query&format=json&redirects=1&generator=images"
           f"&gimlimit=60&titles={urllib.parse.quote(title)}" + IMG_PROPS)
    return wm_files(api, f'Wikipedia "{title}"')[:limit]


FILM_UA = "ShortsMaker/1.0 (personal video script)"  # non-Wikimedia sites don't get the contact email
PIXABAY_KEY_FILE = ROOT / "pixabay_key.txt"  # the owner's free Pixabay API key (stock video); optional
# Sourced videos (esp. YouTube) often have burned-in subtitles in the bottom ~20% and chapter/watermark bars
# in the top ~6%: crop those off first so neither the video nor the blurred background shows them.
FILM_CROP = "crop=trunc(iw*0.92/2)*2:trunc(ih*0.74/2)*2:trunc(iw*0.04/2)*2:trunc(ih*0.06/2)*2"
# Vertical frame for horizontal video clips: a FILM_BAND-tall band (sides trimmed to the centre) over a
# blurred, darkened copy of the cropped video. Fitting the full width left a ~490 px strip on a 1920 px
# screen (owner, 2026-10-16: "make every short better"); 1100 px keeps the middle ~45% of a 16:9 clip.
FILM_BAND = 1100
FILM_VF = (f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=30,"
           f"colorchannelmixer=rr=0.55:gg=0.55:bb=0.55[bg];[b]scale=-2:{FILM_BAND},crop='min(iw,{W})':ih[fg];"
           "[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p")
# Already-vertical clips (9:16 Veo clips or vertical stock footage) fill the whole 1080x1920 frame.
FILL_VF = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},format=yuv420p"


_last_ov = 0.0
_ov_lock = threading.Lock()


def ov_get(url: str) -> bytes | None:
    """GET from Openverse, spaced to its anonymous limit (20 requests a minute). None on failure."""
    global _last_ov
    with _ov_lock:
        time.sleep(max(0.0, _last_ov + 3.1 - time.time()))
        _last_ov = time.time()
    try:
        return fetch(url, 30, FILM_UA)
    except Exception as e:
        print(f"    Openverse request failed ({e})")
        return None


def get_image(url: str, what: str) -> bytes | None:
    """Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse via its rate
    limit, anything else (museums, Internet Archive, NASA) as a plain download. None on failure."""
    if "wikimedia.org" in url:
        return wm_get(url, what)
    if "api.openverse.org" in url:
        return ov_get(url)
    try:
        return fetch(url, 60, FILM_UA)
    except Exception as e:
        print(f"    {what} failed ({e})")
        return None


def openverse_images(query: str, limit: int = 4) -> list[dict]:
    """Images from museums, archives and photographers through Openverse (no key), including CC BY,
    CC BY-SA and Flickr; Wikimedia is searched directly. Creators are credited on screen + in upload.txt."""
    raw = ov_get("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
        {"q": query, "license": "cc0,pdm,by,by-sa,by-nc,by-nc-sa", "excluded_source": "wikimedia", "page_size": 20}))
    found = []
    for r in (json.loads(raw).get("results", []) if raw else []):
        w, h = r.get("width"), r.get("height")
        lic = str(r.get("license") or "").lower()
        if not r.get("url") or (w and h and (w < 300 or not 0.33 <= w / h <= 3)):
            continue
        credit = None if lic in ("cc0", "pdm") else (
            f"{str(r.get('creator') or r.get('source') or 'unknown')[:60]}, CC {lic.upper()} {r.get('license_version') or ''}".strip())
        found.append({"title": f"{r.get('title') or 'untitled'} ({r.get('source')})", "url": r["url"],
                      "small": r.get("thumbnail") or r["url"], "credit": credit, "source": f"Openverse: {r.get('source')}",
                      "site": "Openverse"})
    return found[:limit]


def nasa_search(query: str, media: str) -> list[dict]:
    try:
        return json.loads(fetch("https://images-api.nasa.gov/search?" + urllib.parse.urlencode(
            {"q": query, "media_type": media}), 30, FILM_UA))["collection"]["items"]
    except Exception as e:
        print(f'    NASA search "{query}" failed ({e})')
        return []


def nasa_images(query: str, limit: int = 3) -> list[dict]:
    """NASA photos (public domain), when the story touches space, flight or science."""
    found = []
    for it in nasa_search(query, "image"):
        d = (it.get("data") or [{}])[0]
        preview = next((l["href"] for l in it.get("links", []) if l.get("render") == "image"), None)
        if preview and on_topic(f"{d.get('title', '')} {str(d.get('description', ''))[:300]}", query):
            found.append({"title": f"{d.get('title')} (NASA {d.get('nasa_id')})", "url": preview.replace("~thumb", "~large"),
                          "small": preview, "credit": None, "source": "NASA", "site": "NASA"})
    return found[:limit]


def nasa_films(query: str, limit: int = 2) -> list[dict]:
    """NASA videos (public domain), as their medium/small MP4 renditions."""
    found = []
    for it in nasa_search(query, "video"):
        d = (it.get("data") or [{}])[0]
        if len(found) >= limit or not on_topic(f"{d.get('title', '')} {str(d.get('description', ''))[:300]}", query):
            continue
        try:
            files = [a["href"] for a in json.loads(fetch(f"https://images-api.nasa.gov/asset/{urllib.parse.quote(d['nasa_id'])}",
                                                        30, FILM_UA))["collection"]["items"]]
            src = next(f for tag in ("~medium.mp4", "~small.mp4", "~mobile.mp4") for f in files if f.endswith(tag))
            src = src.replace("http://", "https://")
            dur = duration(src)
        except Exception:
            continue
        if 3 <= dur <= 1800:
            found.append({"title": f"{d.get('title')} (NASA {d['nasa_id']})", "credit": None, "src": src, "dur": dur, "site": "NASA"})
    return found


def pixabay_films(query: str, limit: int = 2) -> list[dict]:
    """Pixabay stock video: free to use in videos, no credit needed (Pixabay Content License).
    AI-generated clips are skipped (they would pass as real footage). Search replies are cached for
    a day, as Pixabay's API terms ask. [] without a key in pixabay_key.txt."""
    if not PIXABAY_KEY_FILE.exists():
        return []
    url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode(
        {"key": PIXABAY_KEY_FILE.read_text(encoding="utf-8").strip(), "q": query[:100], "per_page": 10, "safesearch": "true"})
    cached = CACHE / f"pixabay-{hashlib.sha1(url.encode()).hexdigest()}.json"
    try:
        if cached.exists() and time.time() - cached.stat().st_mtime < 86400:
            raw = cached.read_bytes()
        else:
            raw = fetch(url, 30, FILM_UA)
            CACHE.mkdir(exist_ok=True)
            cached.write_bytes(raw)
        hits = json.loads(raw).get("hits", [])
    except Exception as e:  # the message never includes the URL, so the key isn't printed
        print(f'    Pixabay search "{query}" failed ({type(e).__name__})')
        return []
    found = []
    for h in hits:
        tags = str(h.get("tags", "")).lower()
        v = (h.get("videos") or {}).get("small") or {}  # 1920x1080, ~5 MB
        if "ai generated" in tags or not v.get("url") or not 3 <= (h.get("duration") or 0) <= 120:
            continue
        found.append({"title": f"{tags[:60]} (pixabay.com, video {h.get('id')})", "credit": None, "src": v["url"],
                      "dur": float(h["duration"]), "site": "Pixabay"})
    return found[:limit]


CREDIT_SECONDS = 2.8  # the on-screen credit tag shows this long at the start of its scene, then fades
# owner (2026-10-19): credits at the bottom, just above YouTube's channel name/title (lower is covered by the app)
CREDIT_Y = 1500
CREDIT_ORGS = {"library", "museum", "archive", "archives", "studies", "collection", "university", "society", "government",
               "department", "office", "agency", "news", "service", "institute", "commons", "user"}


def short_credit(credit: str, film: bool = False, max_len: int = 44) -> str:
    """The on-screen credit tag: kind, a short name and the licence ("Photo: E. Mariz · CC BY 2.0"). The full
    credit stays in upload.txt. A long name loses whole words from its end, never letters mid-word."""
    credit = re.sub(r"https?://(?:www\.)?([^/\s,]+)[^\s,]*(?:\s+https?://[^\s,]*)*", r"\1", credit)  # links -> first domain
    lic = re.search(r",\s*((?:CC[ -]?(?:BY|0)[A-Z-]*|public domain|GFDL)(?:[ -][\d.]+)?)\s*$", credit, re.I)
    name = re.split(r"\s+from\s+|,", credit[:lic.start()] if lic else credit)[0].strip()
    words = name.split()
    if 2 <= len(words) <= 3 and all(w[:1].isupper() for w in words) and not CREDIT_ORGS & {w.lower() for w in words}:
        name = f"{words[0][0]}. {' '.join(words[1:])}"  # a person: initial + surname
    head, tail = ("Video: " if film else "Photo: "), (f" · {lic.group(1)}" if lic else "")
    while len(head + name + tail) > max_len and " " in name:
        name = name.rsplit(" ", 1)[0]
    return head + name + tail


def credit_tag_image(text: str) -> Image.Image:
    """Small credit label (bottom-left, CREDIT_Y) while credited material (YouTube channel, CC, Archive) is on screen."""
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
    tw = int(font.getlength(text))
    img = Image.new("RGBA", (tw + 20, 34))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, tw + 20, 34), radius=8, fill=(0, 0, 0, 130))
    d.text((10, 5), text, font=font, fill=(255, 255, 255, 225))
    return img


def on_topic(title: str, query: str) -> bool:
    """Keep titles that share at least one meaningful word (including 2-3 letter terms like NES, N64,
    GTA, ET, UFO) with the query; the visual editor still inspects every frame."""
    q_words = {w for w in words_of(query) if len(w) >= 2 and w not in STOPWORDS} or set(words_of(query))
    return bool(q_words & set(words_of(title)))


def commons_films(query: str, limit: int = 2) -> list[dict]:
    """Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable)."""
    api = ("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6"
           f"&gsrlimit=10&gsrsearch={urllib.parse.quote(query + ' filetype:video')}&prop=videoinfo"
           "&viprop=url|size|mime|extmetadata|derivatives&viextmetadatafilter=LicenseShortName|Artist|Credit")
    raw = wm_get(api, f'Commons film search "{query}"')
    found = []
    for p in json.loads(raw).get("query", {}).get("pages", {}).values() if raw else []:
        info = (p.get("videoinfo") or [{}])[0]
        ok, credit = usable_license(info.get("extmetadata", {}))
        webm = [d for d in info.get("derivatives", []) if "/transcoded/" in d.get("src", "")
                and d.get("type", "").startswith("video/webm") and 0 < d.get("height", 0) <= 720]
        if ok and webm and 3 <= (info.get("duration") or 0) <= 1800 and on_topic(p["title"], query):
            found.append({"title": p["title"], "credit": credit, "src": max(webm, key=lambda d: d["height"])["src"],
                          "dur": info["duration"], "site": "Wikimedia Commons"})
    return found[:limit]


def archive_films(query: str, limit: int = 2) -> list[dict]:
    """Videos across the entire Internet Archive (historical film, retro gaming, commercials, tech,
    broadcasts, documentaries), ranked by downloads. Non-public-domain uploads credit their creator."""
    clean = " ".join(w for w in words_of(query) if w not in STOPWORDS) or re.sub(r"[^\w\s]", " ", query).strip()
    if not clean:
        return []
    search = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(
        {"q": f"(title:({clean}) OR subject:({clean})) AND mediatype:movies AND NOT collection:(opensource_audio OR audio)",
         "fl[]": ["identifier", "title", "creator", "licenseurl"], "sort[]": "downloads desc", "rows": 6, "output": "json"},
        doseq=True)
    found = []
    try:
        for doc in json.loads(fetch(search, 30, FILM_UA)).get("response", {}).get("docs", []):
            if len(found) >= limit:
                break
            ident = doc.get("identifier")
            # "youtube-<id>" items are re-uploads of other creators' YouTube videos (dropped 2026-10-16)
            if not ident or ident.lower().startswith("youtube-"):
                continue
            meta = json.loads(fetch(f"https://archive.org/metadata/{urllib.parse.quote(ident)}", 30, FILM_UA))
            md = meta.get("metadata", {})
            if "youtube" in f"{md.get('collection', '')} {md.get('source', '')} {md.get('originalurl', '')}".lower():
                continue
            title = str(md.get("title") or doc.get("title") or ident)
            if not on_topic(f"{title} {md.get('subject', '')}", query):
                continue
            mp4 = [f for f in meta.get("files", [])
                   if (f.get("format") in ("h.264", "MPEG4", "h.264 IA") or str(f.get("name", "")).lower().endswith(".mp4"))
                   and f.get("length") and not str(f.get("name", "")).startswith("_")]
            thumbs = sorted((int(m.group(1)), f["name"]) for f in meta.get("files", [])
                            if f.get("format") == "Thumbnail" and (m := re.search(r"_(\d+)\.jpg$", f["name"])))
            try:
                dur = float(mp4[0]["length"]) if mp4 else 0.0
            except ValueError:
                dur = 0.0
            if mp4 and 3 <= dur <= 2400:
                lic = str(md.get("licenseurl") or doc.get("licenseurl") or "").lower()
                creator = md.get("creator") or doc.get("creator") or md.get("uploader") or "Internet Archive"
                if isinstance(creator, list):
                    creator = ", ".join(str(x) for x in creator)
                credit = None if ("publicdomain" in lic or "cc0" in lic or "zero" in lic) else str(creator).split("@")[0].strip()[:50]
                base = f"https://archive.org/download/{urllib.parse.quote(ident)}/"
                found.append({"title": f"{title} (archive.org/details/{ident})", "credit": credit,
                              "src": base + urllib.parse.quote(mp4[0]["name"]), "dur": dur,
                              "site": "Internet Archive",
                              "thumbs": [(t, base + urllib.parse.quote(n)) for t, n in thumbs] if len(thumbs) >= 4 else []})
    except Exception as e:
        print(f'    Internet Archive video search "{query}" failed ({e})')
    return found


def archive_images(query: str, limit: int = 3) -> list[dict]:
    """Still images, magazine/manual scans, art and archival photos from the Internet Archive."""
    clean = " ".join(w for w in words_of(query) if w not in STOPWORDS) or re.sub(r"[^\w\s]", " ", query).strip()
    if not clean:
        return []
    search = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(
        {"q": f"(title:({clean}) OR subject:({clean})) AND mediatype:image",
         "fl[]": ["identifier", "title", "creator", "licenseurl"], "sort[]": "downloads desc", "rows": 6, "output": "json"},
        doseq=True)
    found = []
    try:
        for doc in json.loads(fetch(search, 30, FILM_UA)).get("response", {}).get("docs", []):
            if len(found) >= limit:
                break
            ident = doc.get("identifier")
            if not ident:
                continue
            title = str(doc.get("title") or ident)
            if not on_topic(title, query) or JUNK & set(words_of(title)):
                continue
            lic = str(doc.get("licenseurl") or "").lower()
            creator = doc.get("creator") or "Internet Archive"
            if isinstance(creator, list):
                creator = ", ".join(str(x) for x in creator)
            credit = None if ("publicdomain" in lic or "cc0" in lic or "zero" in lic) else str(creator).split("@")[0].strip()[:50]
            thumb = f"https://archive.org/services/img/{urllib.parse.quote(ident)}"
            found.append({"title": f"{title} (archive.org/details/{ident})", "url": thumb, "small": thumb,
                          "credit": credit, "source": "Internet Archive", "site": "Internet Archive"})
    except Exception as e:
        print(f'    Internet Archive image search "{query}" failed ({e})')
    return found


def film_ffmpeg(film: dict, before: list[str], after: list[str], timeout: int) -> subprocess.CompletedProcess:
    """ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the same 1s spacing as
    wm_get() and a short wait on rate limits (HTTP 429); a seek is several requests, so it trips them."""
    global _last_wm
    wiki = film["site"] == "Wikimedia Commons"
    for attempt in range(3):
        if wiki:
            with _wm_lock:
                time.sleep(max(0.0, _last_wm + 1.0 - time.time()))
                _last_wm = time.time()
        ua = film.get("ua") or (WM_UA if wiki else FILM_UA)  # YouTube streams need yt-dlp's own User-Agent
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *before, "-user_agent", ua,
                            "-i", film["src"], *after], capture_output=True, timeout=timeout)
        if b"429" not in r.stderr or attempt == 2:
            return r
        print("    Wikimedia busy, waiting 10s...")
        time.sleep(10)
    return r


def crop_film_bytes(data: bytes) -> bytes:
    """Match FILM_CROP on downloaded thumbnail JPEGs (cut top 6%, bottom 20%, and 4% per side)."""
    try:
        im = Image.open(io.BytesIO(data)).convert("RGB")
        w, h = im.size
        im = im.crop((int(w * 0.04), int(h * 0.06), int(w * 0.96), int(h * 0.80)))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=92)
        return buf.getvalue()
    except Exception:
        return data


def film_frames(film: dict, n: int = 4) -> list[tuple[float, bytes]]:
    """n moments spread through a film, for the contact sheets (with FILM_CROP applied so bottom
    captions and top bars are already cut off): the Internet Archive's own preview frames, or matching
    YouTube chapter timestamps, or single frames fetched by ffmpeg (skipping the first/last 15% on
    longer videos to avoid channel intros and end screens)."""
    if film.get("thumbs"):
        picks = [film["thumbs"][round(k * (len(film["thumbs"]) - 1) / max(1, n - 1))] for k in range(n)]
        out = []
        for t, url in dict(picks).items():
            try:
                out.append((float(t), crop_film_bytes(fetch(url, 30, FILM_UA))))
            except Exception:
                pass
        if out:
            return out
    dur = film["dur"]
    times = list(film.get("moments") or [])
    for k in range(n):
        if len(times) >= n:
            break
        t = dur * (0.15 + 0.70 * k / max(1, n - 1)) if dur > 90 else dur * (k + 0.5) / n
        if all(abs(t - x) > 4.0 for x in times):
            times.append(t)
    out = []
    for t in sorted(times[:n]):
        r = film_ffmpeg(film, ["-ss", f"{t:.1f}"], ["-frames:v", "1", "-vf", FILM_CROP, "-f", "image2pipe", "-vcodec", "mjpeg", "-"], 60)
        if r.returncode == 0 and r.stdout:
            out.append((t, r.stdout))
    return out


def film_piece(film: dict, out: Path) -> tuple[bytes, float] | None:
    """Download ~14s of film around the chosen moment (cropped with FILM_CROP to remove bottom captions
    and top bars, and re-encoded so it seeks locally), and return a full-size still of that moment plus
    its offset in the piece. None on failure."""
    start = max(0.0, film["t"] - 3)
    try:
        r = film_ffmpeg(film, ["-ss", f"{start:.1f}"], ["-t", "14", "-an", "-vf", FILM_CROP, "-c:v", "libx264",
                                                        "-preset", "veryfast", "-crf", "16", str(out)], 300)
        if r.returncode or not out.exists():
            print(f"    film download failed ({r.stderr.decode(errors='replace').strip()[-120:]})")
            return None
        still = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{film['t'] - start:.1f}", "-i", str(out),
                                "-frames:v", "1", "-f", "image2pipe", "-vcodec", "mjpeg", "-q:v", "2", "-"],
                               capture_output=True, timeout=60).stdout
        return (still, film["t"] - start) if still else None
    except Exception as e:
        print(f"    film download failed ({e})")
        return None


def shot_span(path: Path, at: float) -> tuple[float, float]:
    """Start and end of the camera shot containing time `at` (newsreels cut to title cards and other
    scenes every few seconds), found with ffmpeg's scene-change detection."""
    log = subprocess.run(["ffmpeg", "-i", str(path), "-vf", "select='gt(scene,0.3)',showinfo", "-f", "null", "-"],
                         capture_output=True, text=True, errors="replace").stderr
    cuts = [float(t) for t in re.findall(r"pts_time:([\d.]+)", log)]
    return max([0.0] + [c for c in cuts if c <= at]), min([duration(path)] + [c for c in cuts if c > at])


def contact_sheets(cands: list[dict], folder: Path, per_sheet: int = 24) -> list[Path]:
    """Numbered thumbnail grids (6x4) so Claude can look at every candidate at once."""
    folder.mkdir(parents=True, exist_ok=True)
    tile, cols, font = 300, 6, ImageFont.truetype(FONT, 46)
    sheets = []
    for s in range(0, len(cands), per_sheet):
        batch = cands[s:s + per_sheet]
        rows = (len(batch) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tile, rows * tile), (24, 24, 30))
        d = ImageDraw.Draw(sheet)
        for k, c in enumerate(batch):
            x, y = (k % cols) * tile, (k // cols) * tile
            if c.get("thumb"):
                try:
                    im = Image.open(io.BytesIO(c["thumb"])).convert("RGB")
                    im.thumbnail((tile - 12, tile - 12))
                    sheet.paste(im, (x + (tile - im.width) // 2, y + (tile - im.height) // 2))
                except Exception:
                    pass  # unreadable thumbnail: the tile stays blank and Claude skips it
            num = str(s + k + 1)
            d.rectangle((x + 4, y + 4, x + 18 + 26 * len(num), y + 58), fill=YELLOW)
            d.text((x + 11, y + 6), num, font=font, fill="black")
        path = folder / f"sheet{len(sheets) + 1}.png"
        sheet.save(path)
        sheets.append(path)
    return sheets


def gather_pool(articles: list[str], people: list[str], image_terms: list[str], video_terms: list[str],
                skip: set[str] = frozenset(), limit: int = 64, film_limit: int = 14) -> list[dict]:
    """Candidate pictures (with preview `thumb` bytes) and sampled real-film frames from every allowed source:
    Wikipedia article images, Commons, Openverse, Internet Archive, NASA stills, then Internet Archive, Commons,
    Pixabay and NASA videos (4 frames each). Only previews are fetched; full files download when picked.
    `skip`: picture urls and video sources already gathered (nothing is downloaded twice); at most `limit` stills
    and `film_limit` videos."""
    pool: dict[str, dict] = {}

    def add(cands: list[dict]) -> None:
        for c in cands:
            pool.setdefault(c["url"], c)

    names, scene_imgs, scene_vids = list(people), list(dict.fromkeys(image_terms)), list(dict.fromkeys(video_terms))
    articles = list(dict.fromkeys(list(articles) + names))[:7]

    for title in articles:
        add(article_images(title))
    for q in scene_imgs:
        hits = commons_search(q)
        if len(hits) < 2 and len(q.split()) > 2:
            hits += commons_search(" ".join(q.split()[:2]), 2)
        add(hits)
    for name in dict.fromkeys(names):
        surname = words_of(name)[-1:]
        add([c for c in commons_search(f"{name} portrait", 3) if contains(words_of(c["title"]), surname)])
    for q in list(dict.fromkeys(articles[:3] + scene_imgs[:4]))[:6]:  # Openverse (museums/Flickr/archives) + Internet Archive
        add(openverse_images(q, 3) + archive_images(q, 3))
    for q in articles[:2]:
        add(nasa_images(q, 2))
    cands = [c for c in pool.values() if c["url"] not in skip][:limit]

    def load_thumb(c: dict) -> dict | None:
        c["thumb"] = get_image(c["small"], "thumbnail") or (
            get_image(c["url"], "thumbnail") if c["small"] != c["url"] else None)
        return c if c["thumb"] else None

    with ThreadPoolExecutor(4) as ex:
        cands = [c for c in ex.map(load_thumb, cands) if c]

    # Video footage research: Internet Archive, Wikimedia Commons, Pixabay and NASA. No other creators' YouTube
    # videos: since Oct 2026 YouTube cuts the Shorts reach of content re-uploaded from other creators.
    films: list[dict] = []
    other_queries = list(dict.fromkeys(articles[:3] + scene_vids[:5]))
    for search, cap, queries in ((archive_films, 4, other_queries[:6]),
                                 (commons_films, 4, other_queries[:5]),
                                 (pixabay_films, 4, list(dict.fromkeys(scene_vids[:5] + scene_imgs[:4]))[:6]),
                                 (nasa_films, 2, articles[:3])):
        got: dict[str, dict] = {}
        for q in queries:
            if len(got) < cap:
                got.update({f["src"]: f for f in search(q) if f["src"] not in skip})
        films += list(got.values())[:cap]
    films = films[:film_limit]

    if films:
        print(f"  sampling frames from {len(films)} archival/stock videos...")
        with ThreadPoolExecutor(4) as ex:
            sampled = list(ex.map(film_frames, films))
        for f, frames in zip(films, sampled):
            cands += [{"title": f["title"], "url": f"{f['src']}#t={t:.0f}", "credit": f["credit"], "thumb": jpg,
                       "source": f"REAL FILM ({f['site']}: {f['credit'] or 'no credit needed'}), frame at {clock(t)}",
                       "film": {**f, "t": t}, "site": f["site"]}
                      for t, jpg in frames]
    return cands


def pool_folder(topic: str) -> Path:
    return POOLS / hashlib.sha1(topic.encode("utf-8")).hexdigest()[:12]


def write_json(path: Path, data) -> None:
    """Write via a temp file, so an interrupted run never leaves a half-written file behind."""
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def save_pool(folder: Path, cands: list[dict]) -> None:
    """pool.json (the candidates without bytes) + thumb<k>.jpg; list positions are the picture numbers."""
    folder.mkdir(parents=True, exist_ok=True)
    for k, c in enumerate(cands):
        (folder / f"thumb{k}.jpg").write_bytes(c["thumb"])
    rows = [{key: v for key, v in c.items() if key != "thumb"} for c in cands]
    write_json(folder / "pool.json", rows)


def load_pool(folder: Path, thumbs: bool = True) -> list[dict] | None:
    """The saved pool (None if missing or unreadable: it is gathered again); thumbs=False skips the preview bytes."""
    try:
        rows = json.loads((folder / "pool.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return [{**c, "thumb": (folder / f"thumb{k}.jpg").read_bytes()} if thumbs else c for k, c in enumerate(rows)]


def prune_cache() -> None:
    """Drop cached downloads and topic pools older than 30 days."""
    old = lambda p: time.time() - p.stat().st_mtime > 30 * 86400  # noqa: E731
    for f in CACHE.glob("*") if CACHE.exists() else []:
        if f.is_file() and old(f):
            f.unlink()
    for d in POOLS.glob("*") if POOLS.exists() else []:
        if d.is_dir() and old(d / "pool.json" if (d / "pool.json").exists() else d):
            shutil.rmtree(d, ignore_errors=True)


def catalog_pool(s: dict, cands: list[dict], folder: Path) -> list[dict]:
    """The picture list the writer, editor and director plan with: the AI looks at the topic's numbered contact
    sheets once and describes every picture. Reused from folder/catalog.json; both AIs are tried, and if neither
    answers, the run stops (owner, 2026-10-19: no Short without its picture list)."""
    try:
        return json.loads((folder / "catalog.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # missing or half-written: list it again
    if not cands:
        return []
    sheets = contact_sheets(cands, folder / "sheets")
    titles = [f"{k + 1}: {c['title']} ({c['source']})" for k, c in enumerate(cands)]
    print(f"  {BRAIN.capitalize()} is listing the {len(cands)} pictures/frames found for \"{s['subject']}\"...")
    prompt = f"""You are the picture researcher for a YouTube Short about: {s['topic']} (subject: {s['subject']}).
Before any script is written, describe every numbered candidate so the writer can build the story around the
real pictures that exist. Candidates whose source says REAL FILM are frames of real video footage.
Open and look at every contact sheet:
{chr(10).join(str(x) for x in sheets)}
For EVERY number give:
- what: what it really shows, 12 words or fewer (people, place, object, event; "film:" frames say what moves);
- era_ok: true if it is from this story's era and place (or shows the real subject), false for a look-alike
  from another culture/era, a namesake, or something unrelated;
- sharp: 1 (blurry, tiny, damaged), 2 (usable), 3 (crisp and striking);
- hook: true only if it could open the Short: striking at a glance, clearly about the story, from the
  story's own time (never a modern museum display, replica, statue, reenactment, tourist or present-day
  photo of the place), and it raises a question instead of answering it: it must not show the twist or
  the whole story at once (a baboon working the signal levers tells the whole baboon-signalman story;
  a museum's inflatable tank gives away that the army was fake). Best: the main character's face or a
  strange moment whose explanation the viewer has to wait for;
- reject: null, or why it must never be used: graphic violence, torture, executions, corpses or suffering; a
  watermark or channel logo; burned-in subtitles, captions or "subscribe" text (film frames already had their top
  6% and bottom 20% cropped); a printed caption naming a different event, place or person.
For reference, their file titles: {json.dumps(titles, ensure_ascii=False)}
Reply with ONLY JSON: {{"pictures": [{{"n": 1, "what": "...", "era_ok": true, "sharp": 3, "hook": false, "reject": null}}]}}"""
    data = ask_ai(prompt, fatal=False, read_dir=folder / "sheets")
    out = catalog_entries(data, len(cands))
    if data is not None and not out:  # valid JSON but no usable entry: ask_ai only falls back on broken JSON
        other = "gemini" if LAST_AI == "claude" else "claude"
        print(f"  {LAST_AI.capitalize()}'s picture list was empty, asking {other.capitalize()} instead")
        out = catalog_entries(ask_ai(prompt, fatal=False, read_dir=folder / "sheets", brain=other), len(cands))
    if not out:
        sys.exit(f'Stopped: no picture list for "{s["topic"]}". Neither Claude nor Gemini gave a usable answer '
                 "(their messages are above). Run again later.")
    folder.mkdir(parents=True, exist_ok=True)
    write_json(folder / "catalog.json", out)
    return out


def catalog_entries(data: dict | None, n_cands: int) -> list[dict]:
    """The valid entries of a picture-list reply (LLM output is untrusted)."""
    out, seen = [], set()
    for e in (data or {}).get("pictures") or [] if isinstance((data or {}).get("pictures"), list) else []:
        n = e.get("n") if isinstance(e, dict) else None
        sharp = e.get("sharp") if isinstance(e, dict) else None
        if not (type(n) is int and 1 <= n <= n_cands and n not in seen and type(sharp) is int and 1 <= sharp <= 3):
            continue
        seen.add(n)
        reject = str(e["reject"]).strip()[:120] if e.get("reject") else None
        out.append({"n": n, "what": str(e.get("what") or "").strip()[:100], "era_ok": e.get("era_ok") is True,
                    "sharp": sharp, "hook": e.get("hook") is True, "reject": reject})
    return out


def is_usable(e: dict) -> bool:
    return not e["reject"] and e["era_ok"] and e["sharp"] >= 2


def usable(cands: list[dict], catalog: list[dict]) -> list[dict]:
    """Usable list entries for the topic check: all frames of one video count once (its sharpest frame)."""
    best: dict[str, dict] = {}
    for e in sorted(filter(is_usable, catalog), key=lambda e: -e["sharp"]):
        f = cands[e["n"] - 1].get("film")
        best.setdefault(f["src"] if f else cands[e["n"] - 1]["url"], e)
    return sorted(best.values(), key=lambda e: e["n"])


def catalog_text(cands: list[dict], catalog: list[dict]) -> str:
    """The usable pictures as prompt lines: "#12 film: 1944 newsreel of rubber tanks [opener]"."""
    return "\n".join(f"#{e['n']} {'film' if cands[e['n'] - 1].get('film') else 'photo'}: {e['what']}"
                     + (" [opener]" if e["hook"] else "") for e in catalog if is_usable(e))

def choose_images(short: dict, work: Path, ch: dict | None = None) -> list[dict]:
    """Build a broad multi-source pool of images and real video footage (per-scene video search on
    Internet Archive, Wikimedia Commons, Wikipedia, Openverse, Pixabay,
    NASA), show numbered contact sheets to the AI visual editor, and let it match video clips or stills
    to every scene. Picked video frames download ~14s around that moment and credit the owner on screen."""
    print("  researching images and video footage across sources...")
    ch = ch or (load_channel() if CHANNEL.exists() else {})
    niche = ch.get("niche", "educational")
    names = [sc["person"]["name"] for sc in short["scenes"] if sc["person"]]
    scene_imgs = list(dict.fromkeys(sc["image_search"] for sc in short["scenes"] if sc.get("image_search")))
    scene_vids = list(dict.fromkeys((sc.get("video_search") or sc["image_search"])
                                    for sc in short["scenes"] if sc.get("video_search") or sc.get("image_search")))
    pool = load_pool(Path(short["pool_dir"])) if short.get("pool_dir") else None
    if pool is None:  # an old plan: search per scene, as before pictures-first
        cands = gather_pool(short.get("wiki_articles", []), names, scene_imgs, scene_vids)
    else:  # the pool the script was planned with; new finds go at the end so its numbers stay valid
        open_ = [sc for sc in short["scenes"] if not sc.get("pic") and sc.get("image_search")]
        film_srcs = {c["film"]["src"] for c in pool if c.get("film")}
        n_stills = sum(1 for c in pool if not c.get("film"))
        extra = gather_pool([], names, list(dict.fromkeys(sc["image_search"] for sc in open_)),
                            list(dict.fromkeys(sc.get("video_search") or sc["image_search"] for sc in open_)),
                            skip={c["url"] for c in pool} | film_srcs, limit=max(24, 64 - n_stills),
                            film_limit=max(0, 14 - len(film_srcs)))  # about the old totals, room for the open scenes
        cands, have = list(pool), {c["url"] for c in pool}
        for c in extra:
            if c["url"] not in have:
                have.add(c["url"])
                cands.append(c)
    planned_full = lambda sc: [it.get("pic") for it in sc["full"]["items"]] if (sc.get("full") or {}).get("type") == "board" else None  # noqa: E731
    if not cands:
        return [{"bg": None, "person": None} for _ in short["scenes"]]

    n_film = sum(1 for c in cands if c.get("film"))
    print(f"  {len(cands) - n_film} candidate images + {n_film} video frames; {BRAIN.capitalize()} is looking at them...")
    sheets = contact_sheets(cands, work / "sheets")
    scenes = [{"scene": i + 1, "narration": sc["narration"],
               "person_card_for": sc["person"]["name"] if sc["person"] else None,
               "shot": sc["shot"], "animate": sc["animate"],
               **({"planned_picture": sc["pic"]} if pool is not None and sc.get("pic") else {}),
               **({"planned_full_pictures": planned_full(sc)} if pool is not None and any(planned_full(sc) or []) else {}),
               **({"motion_graphic_photos_wanted": [it["find"] or it["label"] for it in sc["full"]["items"]]}
                  if (sc.get("full") or {}).get("type") == "board" else
                  {"motion_graphic_photos_wanted": [p["find"] or p["label"] for p in sc["full"]["photos"]]}
                  if (sc.get("full") or {}).get("type") == "custom" and sc["full"].get("photos") else
                  {"document_scan_wanted": sc["full"]["find"]} if (sc.get("full") or {}).get("type") == "document"
                  and sc["full"].get("find") else {})}
              for i, sc in enumerate(short["scenes"])]
    look, look_rule = short.get("look"), ""
    if look:  # the picker sees the pictures, so it picks the scenes the look suits (tilt-shift only on wide shots...)
        what = look.get("brief") or next((e["description"] for e in style_library("look") if e["name"] == look["name"]), "")
        look_rule = (f'LOOK: this Short uses the photo look "{look.get("title") or look["name"]}" ({what}). Also give '
                     f'look_scenes = the numbers of 2-{STYLE_CAPS["look_scenes"]} scenes whose chosen STILL picture suits this '
                     "look best (never scene 1, never a REAL FILM pick, never a motion-graphic scene); [] if none suits it.\n")
    plan_rule = ("""A scene with planned_picture was written around that candidate before the script: keep it as bg unless it
clearly doesn't fit the final narration; if you pick another (or null), give swap_why in a few words. Use
planned_full_pictures as full_pictures the same way (null for a planned photo that doesn't fit).
""" if pool is not None else "")
    rules = f"""You are the visual editor for a YouTube Short in the "{niche}" niche: "{short['title']}".
For every scene choose the background candidate (video clip or image) that best matches its shot note
(subject and framing), or else what the narration is about at that moment: the right game, person,
place, object or event, from the right era. Never pick pictures of graphic violence, torture, executions,
corpses or suffering: use null instead. All REAL FILM frames have already had their top 6% and bottom 20%
cropped off to remove standard bottom subtitles; if a frame STILL has burned-in subtitles, captions, or
"subscribe" text visible inside the cropped image, DO NOT pick it (normal in-game UI/HUDs are fine).
Scene 1 is the hook that decides whether viewers swipe away: give it the single most striking,
eye-catching candidate that fits the story (REAL FILM first whenever it shows the subject), even when
another picture matches its words more literally. It must be from the story's own time (never a modern
museum display, replica, statue, reenactment or present-day photo), ideally the main character's face, and
must raise the hook's question, not answer it: never a picture that shows the twist or the whole story at
once (a baboon at the signal levers tells the whole baboon-signalman story; a museum's inflatable tank
gives away that the army was fake).
Candidates whose source says REAL FILM are frames from real video footage (Internet
Archive, Wikimedia Commons, Pixabay, NASA): picking one plays a clip of that real video in the scene
and automatically credits the owner on screen. Prefer REAL FILM over still pictures whenever a video
frame genuinely shows what the scene is about — you may pick REAL FILM on as many scenes as it fits,
up to every scene! A REAL FILM frame that only shows a static text slide, a modern talking head in front
of a mic/camera for a historical scene, an AI-generated cartoon slideshow when real photos/footage exist,
or an unrelated screen is not good footage: skip it.
Keep the Short visually varied: never use the exact same candidate number twice, and pick at most 2
different moments from the same source video across the Short. Avoid: a different person/game that
shares a name, near-duplicates of an image already used, maps or text pages unless the narration is
about them, and any picture whose printed caption names a different event, place or person.
For scenes with person_card_for, also pick a still portrait (never a REAL FILM frame) that clearly
shows that exact person (face visible), and that is a different picture from the scene's background.
Use null when nothing fits: an unrelated image is worse than none, and a painted illustration of the
scene is made instead.
Some scenes are full-screen motion graphics. For a scene with motion_graphic_photos_wanted (an evidence
board or custom collage of real photos), give full_pictures = one candidate per wanted photo, in order: a STILL picture (never
REAL FILM) that really shows it, never the same candidate twice in the Short, null where none does. For a
scene with document_scan_wanted, full_pictures = [the candidate that is a real scan of that document] or
[null]. Still pick a normal bg for those scenes too (used if the graphic can't be made).
For scenes with animate true where you picked a STILL picture (not REAL FILM), an AI video model will
bring your chosen picture to life: write motion = one short line describing gentle movement of what is
actually in that picture, of one kind:
ATMOSPHERE (water, waves, clouds, rain, snow, flags, fire, light, or smoke and steam rising from a visible
source; everyone stays still) or
PEOPLE moving slowly and simply (working, a crowd shifting, walking calmly). Set motion_people true
for the PEOPLE kind, false for ATMOSPHERE. Use motion null when you picked REAL FILM, or for fast action,
vehicles or machines in motion, a close-up of a face, when nothing would naturally move, or for a line
drawing, engraving, portrait or document page. Never add dust, fog, mist or smoke that isn't in the picture.
Also choose move = the camera move that suits the picture you chose: "in" (faces, details),
"out" (reveals), "left"/"right" (wide places, crowds), "up"/"down" (tall pictures, full-length
figures). Never the same move in two scenes in a row.
Also give subject_row = where the main subject sits in the background you chose (the face, if there is
one), as a row from 1 (top edge) to 10 (bottom edge); null when there's no single subject. Text callouts
are moved out of the subject's way.
{plan_rule}Scenes: {json.dumps(scenes, ensure_ascii=False)}
{look_rule}Reply with ONLY JSON: {{"picks": [{{"scene": 1, "bg": 7, "person": null, "move": "in", "motion": null, "motion_people": false, "subject_row": 3, "full_pictures": null, "swap_why": null}}], "look_scenes": []}}"""
    titles = [f"{k + 1}: {c['title']} ({c['source']})" for k, c in enumerate(cands)]
    sheet_list = "\n".join(str(s) for s in sheets)
    data = ask_ai(f"""{rules}
The candidates are numbered on these contact sheets. Open and look at every sheet:
{sheet_list}
For reference, their file titles: {json.dumps(titles, ensure_ascii=False)}""",
                      fatal=False, read_dir=work / "sheets")
    if data is None:
        print("    visual check failed, picking by file title instead")
        data = ask_ai(f"{rules}\nCandidates (number: file title): {json.dumps(titles, ensure_ascii=False)}",
                          fatal=False)
    if data is None and pool is not None:  # no picker answer: the director's plan stands
        data = {"picks": [{"scene": i + 1, "bg": sc.get("pic"), "full_pictures": planned_full(sc)}
                          for i, sc in enumerate(short["scenes"])]}
    picks = {p.get("scene"): p for p in (data or {}).get("picks", []) if isinstance(p, dict)}

    chosen, taken = [], set()
    for i in range(len(short["scenes"])):
        result = {}
        for kind in ("bg", "person"):
            num = picks.get(i + 1, {}).get(kind)
            c = cands[num - 1] if isinstance(num, int) and 1 <= num <= len(cands) else None
            result[kind] = None
            if c and c.get("film") and kind == "person":
                c = None  # person cards need a clear portrait
            if c and c["url"] not in taken:
                if c.get("film"):
                    piece = film_piece(c["film"], work / f"film{i}_src.mp4")
                    img = piece[0] if piece else None
                    if piece:
                        result["film"] = {**c["film"], "path": work / f"film{i}_src.mp4", "offset": piece[1]}
                else:
                    img = get_image(c["url"], "image download")
                if img:
                    result[kind] = (img, c["title"], c["credit"])
                    if kind == "bg":
                        result["site"] = c.get("site", "Wikimedia Commons")
                    taken.add(c["url"])
        sc = short["scenes"][i]
        if pool is not None and sc.get("pic"):
            got, why = picks.get(i + 1, {}).get("bg"), str(picks.get(i + 1, {}).get("swap_why") or "").strip()[:120]
            result["plan_note"] = ("planned picture kept" if got == sc["pic"] and result["bg"] else
                                   f"planned #{sc['pic']} swapped: " + (why or (
                                       "the picker chose another" if got != sc["pic"] else
                                       "it was already used in another scene" if cands[got - 1]["url"] in taken else
                                       "it could not be downloaded")))
        row = picks.get(i + 1, {}).get("subject_row")
        if result["bg"] and isinstance(row, int) and 1 <= row <= 10:
            result["subject_y"] = (row - 0.5) / 10  # 0..1 down the picture
        if result["bg"] and picks.get(i + 1, {}).get("move") in MOVE_NAMES:
            sc["move"] = picks[i + 1]["move"]
        if sc["animate"] and result["bg"]:  # the planner wrote motion before any picture was chosen
            sc["motion"] = str(picks.get(i + 1, {}).get("motion") or "").strip()[:200]
            sc["motion_people"] = picks.get(i + 1, {}).get("motion_people") is True
            sc["animate"] = bool(sc["motion"]) and not result.get("film")
        chosen.append(result)
    for i, pics in full_pictures(short, picks, cands, taken).items():
        chosen[i]["full_pics"] = pics
    apply_look_scenes(short, chosen, (data or {}).get("look_scenes"))
    return chosen


def wants_remotion(scenes: list[dict], n_graphics: int) -> bool:
    """Remotion renders when the plan is graphics-heavy or uses anything only it can draw: a full-screen motion
    graphic, a Remotion-only graphic, a map route, a photo look, or a scene change other than fade/flash."""
    return n_graphics >= REMOTION_MIN_GRAPHICS or any(
        sc.get("full") or sc.get("look") or sc.get("transition", "fade") not in ("fade", "flash")
        or (sc["graphic"] and (sc["graphic"]["style"] in REMOTION_ONLY or "from" in sc["graphic"])) for sc in scenes)


def style_props(sc: dict, i: int) -> dict:
    """A scene's style-library props for Remotion (an old Short's state has no look: the plain picture)."""
    return {"transition": sc["transition"], "look": sc.get("look"), "lookSeed": sc.get("look_seed", i)}


def apply_look_scenes(short: dict, choices: list[dict], look_scenes) -> None:
    """Puts the Short's photo look on the scenes the picker chose for it (it saw the pictures): at most
    STYLE_CAPS["look_scenes"], never scene 1 (the hook), a real film clip, an AI motion clip (Short.tsx draws no
    look on any clip) or a full-screen motion graphic. Every other scene, and every scene of a Short without a look, shows the plain picture."""
    for sc in short["scenes"]:
        sc["look"] = None
    look = short.get("look")
    if not look or not isinstance(look_scenes, list):
        return
    picked: list[int] = []
    for n in look_scenes:
        i = n - 1 if isinstance(n, int) and not isinstance(n, bool) else -1
        if 0 < i < len(short["scenes"]) and i not in picked and not choices[i].get("film") \
                and not short["scenes"][i].get("full") and not short["scenes"][i].get("animate") \
                and len(picked) < STYLE_CAPS["look_scenes"]:
            picked.append(i)
    for i in picked:
        short["scenes"][i].update(look=look["name"], look_seed=i)


def full_pictures(short: dict, picks: dict, cands: list[dict], taken: set) -> dict[int, list]:
    """Downloads the real photos the picker chose for evidence boards, custom scenes and documents.
    An item without a usable photo leaves the board (with its threads); a board left with fewer than 3 photos
    is dropped and the scene uses its normal picture. Returns scene -> [(bytes, title, credit, site)]."""
    out = {}
    for i, sc in enumerate(short["scenes"]):
        full = sc.get("full")
        if not full or full["type"] not in ("board", "document", "custom"):
            continue
        if full["type"] == "custom" and not full.get("photos"):
            continue
        nums = picks.get(i + 1, {}).get("full_pictures")
        nums = nums if isinstance(nums, list) else []
        want = len(full["items"]) if full["type"] == "board" else (len(full["photos"]) if full["type"] == "custom" else 1)
        pics = []
        for k in range(want):
            num = nums[k] if k < len(nums) else None
            c = cands[num - 1] if isinstance(num, int) and not isinstance(num, bool) and 1 <= num <= len(cands) else None
            img = get_image(c["url"], "image download") if c and not c.get("film") and c["url"] not in taken else None
            if img:
                taken.add(c["url"])
            pics.append((img, c["title"], c["credit"], c.get("site", "Wikimedia Commons")) if img else None)
        if full["type"] == "document":
            out[i] = [p for p in pics if p]
            continue
        keep = [k for k, p in enumerate(pics) if p]
        if full["type"] == "custom":
            full["photos"] = [full["photos"][k] for k in keep]
            out[i] = [pics[k] for k in keep]
            if full.get("kind") == "collage" and not keep:
                full["kind"] = "diagram"
            continue
        if len(keep) < 3:
            print(f"    scene {i + 1}: too few real photos for the evidence board, using a normal picture")
            sc["full"] = None
            continue
        new = {old: k for k, old in enumerate(keep)}
        full["items"] = [full["items"][k] for k in keep]
        full["links"] = [[new[a], new[b]] for a, b in full["links"] if a in new and b in new]
        out[i] = [pics[k] for k in keep]
    return out


def rescue_graphics(short: dict, scenes: list[int], why: dict[int, str]) -> list[int]:
    """Scenes whose picture is missing or weak may become a full-screen motion graphic (map journey, big number,
    document, or a custom AI-coded diagram/flow/clock) when one shows their line better than a painting.
    One AI call; the same caps as planned ones (MAX_FULL, never scene 1, never two in a row).
    Returns the scenes that got one."""
    scs = short["scenes"]
    asked = [i for i in scenes if 0 < i < len(scs) and not scs[i].get("full")
             and len(scs[i]["narration"].split()) >= FULL_MIN_WORDS]  # a shorter scene can't play one: it gets a painting
    if not asked or sum(1 for sc in scs if sc.get("full")) >= MAX_FULL:
        return []
    texts = short.get("research") or {t: article_text(t)[:15000] for t in short.get("wiki_articles", [])[:3]}
    script = [{"scene": i + 1, "narration": sc["narration"],
               **({"needs_help": why.get(i, "the picture is weak")} if i in asked else {})} for i, sc in enumerate(scs)]
    print(f"  asking {BRAIN.capitalize()} whether a motion graphic fits {len(asked)} scene(s) without a good picture...")
    data = ask_ai(f"""You are the director of a YouTube Short: "{short['title']}". The scenes marked needs_help
have no good picture. For each of them, decide whether a FULL-SCREEN motion graphic would show its line well
(else null: the scene gets a painting instead). Real facts only, from the articles below. "word" = a word or
name spoken in that scene's narration when that element should appear. Formats:
{{"type": "journey", "stops": [{{"name": "Uitenhage", "lat": -33.76, "lon": 25.4, "word": "Uitenhage"}}], "note": "1881"}}
 (1-4 real places in travel order);
{{"type": "number", "value": 30000, "label": "mourners", "icon": "person", "thing": "mourner", "each": 1000, "word": "thirty"}}
 (thing = what one figure is, a singular noun; icon = the closest of {list(ICONS)}; optional "compare": {{"a_label": "1858", "a_value": 100, "b_label": "today", "b_value": 3}});
{{"type": "document", "kind": "telegram", "key_line": "...", "date": "1890", "word": "..."}}
 (kind one of {list(DOC_KINDS)}; key_line at most 14 words, documented or a plain summary; "paper" only for a
 real newspaper that covered it);
{{"type": "custom", "kind": "diagram", "title": "...", "brief": "...", "words": ["...", "...", "..."]}}
 (a bespoke animated scene coded from scratch for this moment when the line explains a mechanism, physical
 layout/cross-section, loophole/cause-and-effect chain, or schedule/countdown; kind one of
 ["diagram", "flow", "clock"]; "words" = 2-4 spoken words from the scene that trigger each animation beat).
Script: {json.dumps(script, ensure_ascii=False)}
Wikipedia articles: {json.dumps(texts, ensure_ascii=False)}
Reply with ONLY JSON: {{"scenes": [{{"scene": 3, "full": null}}]}}""", fatal=False)
    got = []
    for r in sorted((r for r in (data or {}).get("scenes") or [] if isinstance(r, dict) and isinstance(r.get("scene"), int)),
                    key=lambda r: r["scene"]):
        i = r["scene"] - 1
        f = r.get("full")
        if i not in asked or not isinstance(f, dict) or f.get("type") == "board":
            continue
        f = clean_full(f, words_of(scs[i]["narration"]))
        near = any(0 <= k < len(scs) and scs[k].get("full") for k in (i - 1, i + 1))
        if f and not near and sum(1 for sc in scs if sc.get("full")) < MAX_FULL:
            scs[i].update(full=f, graphic=None, person=None, animate=False, full_rescued=why.get(i, "the picture was weak"))
            got.append(i)
    return got


def is_stereo(img: Image.Image) -> bool:
    """A stereograph card: two near-identical photos side by side. Compares the halves' photo areas
    (right one shifted up to 10%, since mounts are off-centre) after removing each row's average, so
    any landscape's shared sky-over-ground doesn't count. Tested 2026-10-15: a real card scored 0.52,
    wide photos, a card grid and drone footage 0.1 or less."""
    if not 1.6 <= img.width / img.height <= 2.4:
        return False
    half, n = img.width // 2, 48

    def detail(x0: int) -> list[float]:
        b = img.crop((x0 + int(half * 0.04), int(img.height * 0.06), x0 + int(half * 0.97),
                      int(img.height * 0.84))).convert("L").resize((n, n)).tobytes()
        return [v - sum(b[y * n:(y + 1) * n]) / n for y in range(n) for v in b[y * n:(y + 1) * n]]

    left, best = detail(0), -1.0
    for d in range(-half // 10, half // 10 + 1, max(1, half // 100)):
        try:
            best = max(best, statistics.correlation(left, detail(half + d)))
        except statistics.StatisticsError:  # a blank half
            pass
    return best > 0.4


def trim_borders(img: Image.Image) -> Image.Image:
    """Cut plain strips (white mounts, black plate edges) off the sides, at most 15% per side.
    shortcut: a plain sky or wall touching the edge can lose up to 15% too; harmless once cover-cropped."""
    g = img.convert("L")
    g.thumbnail((400, 400))
    box = [0, 0, g.width, g.height]  # left, top, right, bottom in thumbnail pixels

    def plain(b: tuple) -> bool:  # 90% one flat tone: lets a line through dust, lettering or a crossing strip
        px = sorted(g.crop(b).tobytes())
        mid = px[len(px) // 2]
        return sum(abs(v - mid) <= 16 for v in px) >= 0.9 * len(px)

    def border(line) -> bool:  # plain, or one of up to 3 soft edge lines just before more plain border
        return any(plain(line(k)) for k in range(4))

    changed = True
    while changed:  # borders nest (black frame, then a white strip): repeat until nothing more is plain
        changed = False
        l, t, r, b = box
        if l < g.width * 0.15 and border(lambda k: (l + k, t, l + k + 1, b)):
            box[0], changed = l + 1, True
        if r > g.width * 0.85 and border(lambda k: (r - k - 1, t, r - k, b)):
            box[2], changed = r - 1, True
        if t < g.height * 0.15 and border(lambda k: (l, t + k, r, t + k + 1)):
            box[1], changed = t + 1, True
        if b > g.height * 0.85 and border(lambda k: (l, b - k - 1, r, b - k)):
            box[3], changed = b - 1, True
    sx, sy = img.width / g.width, img.height / g.height
    return img.crop((round(box[0] * sx), round(box[1] * sy), round(box[2] * sx), round(box[3] * sy)))


def clean_photo(data: bytes) -> bytes:
    """Archive scans look broken on screen with their extras: a stereograph card keeps only its left
    photo, and plain borders are cut off. Returns the original bytes when there's nothing to fix."""
    img = Image.open(io.BytesIO(data)).convert("RGB")
    size = img.size
    if is_stereo(img):
        img = img.crop((0, 0, img.width // 2, img.height))
        # shortcut: fixed box for the standard card layout (mount around, caption below the photo);
        # upgrade to detecting the photo's edge if odd cards slip through
        img = img.crop((int(img.width * 0.22), int(img.height * 0.12), int(img.width * 0.97), int(img.height * 0.84)))
    img = trim_borders(img)
    if img.size == size:
        return data
    out = io.BytesIO()
    img.save(out, "JPEG", quality=95)
    return out.getvalue()


def to_vertical(path: Path) -> None:
    """Fill the 9:16 frame with the picture (centre crop) for the slow zoom/pan. This was the 2.5D parallax
    clip's full-screen framing; parallax itself was dropped (2026-10-16) because its depth warp bent paintings."""
    img = Image.open(path).convert("RGB")
    ImageOps.fit(img, (int(W * SRC), int(H * SRC)), Image.LANCZOS).save(path, quality=95)


def speak(text: str, voice: str, path: Path) -> list[tuple[float, float, str]]:
    """TTS with retries: Microsoft's free Edge voice service drops a request now and then."""
    for attempt in range(5):
        try:
            return asyncio.run(tts(text, voice, path))
        except Exception as e:
            if attempt == 4:
                raise
            print(f"    voice service hiccup ({type(e).__name__}), retrying...")
            time.sleep(3 * (attempt + 1))


async def tts(text: str, voice: str, path: Path) -> list[tuple[float, float, str]]:
    words = []
    with open(path, "wb") as f:
        async for chunk in edge_tts.Communicate(text, voice, boundary="WordBoundary").stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":  # offsets are in 100ns units
                start = chunk["offset"] / 1e7
                words.append((start, start + chunk["duration"] / 1e7, chunk["text"]))
    return words


def duration(path: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout)


def fills_frame(path: Path) -> bool:
    """True only when a video is already vertical (9:16-ish, 720p+); horizontal videos use FILM_VF
    (zoomed out over a blurred background) so subjects on the left/right are never cut off."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout
    try:
        w, h = (int(v) for v in out.strip().split(",")[:2])
    except ValueError:
        return False
    return h >= 720 and w < h


_encoder: list[str] = []


def video_encoder() -> list[str]:
    """Final H.264 encode: NVENC on the GPU when available (frees the CPU), else x264."""
    if not _encoder:
        out = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True).stdout
        _encoder.extend(["-c:v", "h264_nvenc", "-preset", "p5", "-cq", "20", "-b:v", "0"] if "h264_nvenc" in out
                        else ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20"])
    return _encoder


def ffmpeg(*args: str, cwd: Path) -> None:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], cwd=cwd, check=True)


def ass_time(t: float) -> str:
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02}:{t % 60:05.2f}"


def caption_lines(words: list[tuple[float, float, str]]) -> list[list[tuple[float, float, str]]]:
    """Caption lines of up to 3 words and about 16 letters: a long word ("SIXTY-THREE-YEAR-OLD") gets a
    shorter line instead of shrinking the whole line to a tiny size. Both renderers use these lines."""
    lines: list[list[tuple[float, float, str]]] = []
    for w in words:
        if lines and len(lines[-1]) < 3 and len(" ".join(x[2] for x in lines[-1] + [w])) <= 16:
            lines[-1].append(w)
        else:
            lines.append([w])
    return lines


def captions(words: list[tuple[float, float, str]], path: Path, emphasis: set[float]) -> None:
    """ASS captions, one caption_lines() line at a time; the spoken word turns yellow. Emphasis words (by start
    time) turn orange, grow and stay lit for the rest of their line."""
    lines = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "",
             "[V4+ Styles]",
             "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, "
             "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV",
             "Style: Default,Impact,120,&H00FFFFFF,&H00000000,&H90000000,0,1,8,4,2,60,60,620", "",
             "[Events]", "Format: Layer, Start, End, Style, Text"]
    groups = caption_lines(words)
    for g, chunk in enumerate(groups):
        chunk_end = groups[g + 1][0][0] if g + 1 < len(groups) else chunk[-1][1]
        for j, (start, _, _) in enumerate(chunk):
            end = chunk[j + 1][0] if j + 1 < len(chunk) else chunk_end

            def styled(k: int, w: tuple[float, float, str]) -> str:
                if w[0] in emphasis and k <= j:  # emphasis colour, 15% bigger, from when it's said to line end
                    return f"{{\\c{ass_colour(EMPHASIS)}\\3c{ass_colour(EMPHASIS, 0.4)}\\fscx115\\fscy115}}" + w[2].upper() + \
                        "{\\c&H00FFFFFF&\\3c&H00000000&\\fscx100\\fscy100}"
                return (f"{{\\c{ass_colour(YELLOW)}}}" + w[2].upper() + "{\\c&H00FFFFFF&}") if k == j else w[2].upper()
            text = " ".join(styled(k, w) for k, w in enumerate(chunk))
            pop = "{\\fscx80\\fscy80\\t(0,90,\\fscx100\\fscy100)}" if j == 0 else ""
            lines.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Default,{pop}{text}")
    path.write_text("\n".join(lines), encoding="utf-8")


SFX_FILES = ["whoosh0", "whoosh1", "whoosh2", "whoosh3", "flash0", "flash1",
             "stamp0", "stamp1", "shutter0", "shutter1", "pin", "ticks", "riser", "scratch"]


def clean_sound(v, said: list[str]) -> dict | None:
    """A planned story sound {"word", "sound"}, validated: the word must be spoken in the scene, the sound 1-4 plain words."""
    if not isinstance(v, dict) or not isinstance(v.get("word"), str) or not contains(said, words_of(v["word"])):
        return None
    name = " ".join(re.sub(r"[^a-z ]+", " ", str(v.get("sound") or "").lower()).split())
    return {"word": v["word"].strip(), "sound": name} if 0 < len(name.split()) <= 4 and len(name) <= 30 else None


def limit_sounds(scenes: list[dict]) -> None:
    """At most MAX_STORY_SOUNDS story sounds per Short (the first ones), so each one stays special."""
    kept = 0
    for sc in scenes:
        if sc.get("sound") and kept < MAX_STORY_SOUNDS:
            kept += 1
        else:
            sc["sound"] = None


def freesound_fetch(name: str) -> tuple[bytes, dict] | None:
    """One CC0 (no credit, any use) sound for `name` from Freesound's official API: the best-scoring short sound,
    preferring well-rated, much-downloaded ones; its high-quality preview MP3. None without a key or a match."""
    key = FREESOUND_KEY.read_text(encoding="utf-8-sig").strip() if FREESOUND_KEY.exists() else ""
    if not key:
        return None
    q = urllib.parse.urlencode({"query": name, "filter": 'license:"Creative Commons 0" duration:[0.15 TO 4]',
                                "fields": "id,name,duration,avg_rating,num_downloads,previews,license",
                                "page_size": 10, "sort": "score"})
    try:
        req = urllib.request.Request(f"https://freesound.org/apiv2/search/text/?{q}",
                                     headers={"Authorization": f"Token {key}", "User-Agent": "ShortsMaker/1.0"})
        results = json.load(urllib.request.urlopen(req, timeout=30)).get("results") or []
        if not results:
            return None
        best = next((r for r in results if (r.get("avg_rating") or 0) >= 3 and (r.get("num_downloads") or 0) >= 20), results[0])
        audio = urllib.request.urlopen(urllib.request.Request(best["previews"]["preview-hq-mp3"],
                                                              headers={"User-Agent": "ShortsMaker/1.0"}), timeout=30).read()
        return audio, best
    except (OSError, ValueError, KeyError):
        return None


def story_sound(name: str, lib: Path = STORY_SFX, fetch=freesound_fetch) -> Path | None:
    """The sound file for a story sound: the owner's own file in sfx/story/<name>.(wav|mp3|ogg|flac) wins; else one
    fetched from Freesound, trimmed, high-passed like every SFX, evened out and kept as sfx/story/<name>.wav (with a
    .txt note of where it came from), so each sound is fetched only once."""
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    for ext in (".wav", ".mp3", ".ogg", ".flac"):
        if (lib / f"{slug}{ext}").exists():
            return lib / f"{slug}{ext}"
    got = fetch(name)
    if not got:
        return None
    audio, meta = got
    lib.mkdir(parents=True, exist_ok=True)
    raw, out = lib / f"_{slug}.tmp", lib / f"{slug}.wav"
    raw.write_bytes(audio)
    try:
        ffmpeg("-i", raw.name, "-af", "silenceremove=start_periods=1:start_threshold=-45dB,atrim=0:3.5,"
               "highpass=f=220,highpass=f=220,loudnorm=I=-18:TP=-2:LRA=11", "-ar", "44100", "-ac", "2", out.name, cwd=lib)
    except subprocess.CalledProcessError:
        return None
    finally:
        raw.unlink(missing_ok=True)
    (lib / f"{slug}.txt").write_text(f"Freesound #{meta.get('id')}: {meta.get('name')} ({meta.get('license')}) "
                                     f"https://freesound.org/s/{meta.get('id')}/\n", encoding="utf-8")
    return out


def make_sfx() -> None:
    """Synthesize the sound-effect library once (no downloads, no copyright). Hits, flashes and
    stamps get a short room reverb through ffmpeg so they sound designed, not like raw tones."""
    SFX.mkdir(exist_ok=True)
    sr = 44100

    def save(name: str, samples: list[float], reverb: bool = False) -> None:
        peak = max(abs(s) for s in samples) or 1
        dry = SFX / (name + "_dry.wav")
        with wave.open(str(dry), "wb") as f:
            f.setnchannels(1), f.setsampwidth(2), f.setframerate(sr)
            f.writeframes(b"".join(int(s / peak * 0.9 * 32767).to_bytes(2, "little", signed=True)
                                   for s in samples))
        # Everything is high-passed: synthetic low end comes out as a dull thump on phone speakers.
        chain = "apad=pad_dur=0.6,aecho=0.9:0.9:45|95|160:0.32|0.22|0.12,lowpass=f=7500," if reverb else ""
        ffmpeg("-i", dry.name, "-af", chain + "highpass=f=220,highpass=f=220,alimiter=limit=0.9",
               name + ".wav", cwd=SFX)
        dry.unlink()

    def noise() -> float:
        return random.uniform(-1, 1)

    for v, bright in enumerate([0.35, 0.55]):  # flash cut: bright noise burst over a soft low thump
        n, out, phase, lp, prev = int(sr * 0.7), [], 0.0, 0.0, 0.0
        for k in range(n):
            t = k / sr
            x = noise()
            hp, prev = x - prev * (1 - bright), x  # crude high-pass keeps it airy
            phase += 2 * math.pi * 70 / sr
            out.append(hp * math.exp(-t * 9) * 0.6 + math.sin(phase) * math.exp(-t * 10))
        save(f"flash{v}", out, reverb=True)

    for v, f0 in enumerate([95, 80]):  # stamp: low thump + papery slap
        n, out, phase, b1, b2 = int(sr * 0.45), [], 0.0, 0.0, 0.0
        for k in range(n):
            t = k / sr
            phase += 2 * math.pi * f0 / sr
            b1 += 0.35 * (noise() - b1)
            b2 += 0.08 * (b1 - b2)
            out.append(math.sin(phase) * math.exp(-t * 22) + 1.6 * (b1 - b2) * math.exp(-t * 45))
        save(f"stamp{v}", out, reverb=True)

    for v, ring in enumerate([2100, 1700]):  # camera shutter: two quick mechanical clicks
        n, out = int(sr * 0.2), []
        for k in range(n):
            t = k / sr
            click = 0.0
            for t0, g in ((0.0, 1.0), (0.055, 0.7)):
                if t >= t0:
                    d = t - t0
                    click += g * (noise() * math.exp(-d * 900) + 0.5 * math.sin(2 * math.pi * ring * d) * math.exp(-d * 120))
            out.append(click)
        save(f"shutter{v}", out)

    n, out = int(sr * 0.6), []
    for k in range(n):  # map pin: soft plink with a tiny thud
        t = k / sr
        out.append(math.sin(2 * math.pi * 1320 * t) * math.exp(-t * 9) + 0.4 * math.sin(2 * math.pi * 1980 * t) * math.exp(-t * 14)
                   )
    save("pin", out)

    ticks, tt, gap = [], 0.0, 0.03  # year counter: fast ticks that slow down as it lands (~0.7s)
    while tt < 0.7:
        ticks.append(tt)
        tt += gap
        gap *= 1.18
    n, out = int(sr * 0.85), []
    for k in range(n):
        t = k / sr
        out.append(sum(math.sin(2 * math.pi * 3200 * (t - t0)) * math.exp(-(t - t0) * 260) for t0 in ticks if 0 <= t - t0 < 0.03))
    save("ticks", out)

    n, out, b1, b2 = int(sr * 2.2), [], 0.0, 0.0
    for k in range(n):  # riser: noise band sweeping up plus a rising tone, swelling into the payoff
        t = k / sr
        x = t / 2.2
        a = 1 - math.exp(-2 * math.pi * (300 * 18 ** x) / sr)
        b1 += a * (noise() - b1)
        b2 += a * 0.5 * (b1 - b2)
        tone = math.sin(2 * math.pi * (180 * t + 160 * t * t))
        out.append(((b1 - b2) * 1.4 + 0.25 * tone) * x ** 2.2)
    save("riser", out)

    n, out, b1, b2 = int(sr * 0.6), [], 0.0, 0.0
    for k in range(n):  # pen scratch (red underline, route line): bright noise in quick nib strokes
        t = k / sr
        b1 += 0.55 * (noise() - b1)
        b2 += 0.2 * (b1 - b2)
        stroke = max(0.0, math.sin(2 * math.pi * 11 * t)) ** 0.6
        out.append((b1 - b2) * stroke * min(1.0, t / 0.02) * math.exp(-t * 1.5))
    save("scratch", out)

    for v, (length, peak_hz) in enumerate([(0.55, 1400), (0.7, 1900), (0.85, 1100), (0.65, 2300)]):
        n, out, lp1, lp2 = int(sr * length), [], 0.0, 0.0
        for k in range(n):  # soft whoosh: noise through a lowpass that sweeps open then closed
            x = k / n
            cutoff = 200 + peak_hz * math.sin(math.pi * x) ** 2
            a = 1 - math.exp(-2 * math.pi * cutoff / sr)
            lp1 += a * (random.uniform(-1, 1) - lp1)
            lp2 += a * (lp1 - lp2)
            out.append(lp2 * math.sin(math.pi * x) ** 3)
        save(f"whoosh{v}", out)


def shot(img: Image.Image, move: str, p: float) -> Image.Image:
    """One frame of slow Ken Burns motion; affine sampling is sub-pixel so it never shakes."""
    zmax = 1.12
    z = {"in": 1 + (zmax - 1) * p, "out": zmax - (zmax - 1) * p}.get(move, zmax)
    vw, vh = img.width / z, img.height / z
    cx, cy = img.width / 2, img.height / 2
    dx, dy = (img.width - vw) / 2, (img.height - vh) / 2
    cx += {"right": dx * (2 * p - 1), "left": dx * (1 - 2 * p)}.get(move, 0)
    cy += {"down": dy * (2 * p - 1), "up": dy * (1 - 2 * p)}.get(move, 0)
    s = vw / W
    return img.transform((W, H), Image.AFFINE, (s, 0, cx - vw / 2, 0, s, cy - vh / 2), Image.BICUBIC)


def fit_font(text: str, size: int, max_w: int) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(FONT, size)
    while font.getlength(text) > max_w and size > 30:
        size -= 6
        font = ImageFont.truetype(FONT, size)
    return font


def graphic_overlay(style: str, text: str) -> Image.Image:
    """Pre-render a callout as a small transparent image (animated per frame later)."""
    if style == "hook":  # title over the opening, up to two lines; also makes frame 0 thumbnail-ready
        words = text.upper().split()
        lines = [" ".join(words)]
        if len(words) > 1 and len(lines[0]) > 12:  # two lines, split where they're most even in length
            k = min(range(1, len(words)), key=lambda k: max(len(" ".join(words[:k])), len(" ".join(words[k:]))))
            lines = [" ".join(words[:k]), " ".join(words[k:])]
        font = fit_font(max(lines, key=len), 120, W - 140)
        img = Image.new("RGBA", (W, 150 * len(lines) + 40))
        d = ImageDraw.Draw(img)
        for k, line in enumerate(lines):
            d.text(((W - font.getlength(line)) / 2, 20 + k * 150), line, font=font, fill=YELLOW,
                   stroke_width=10, stroke_fill="black")
        return img
    if style == "cta":  # red subscribe button with a small line under it
        big, small = ImageFont.truetype(FONT, 80), ImageFont.truetype(FONT, 50)
        bw = int(big.getlength("SUBSCRIBE")) + 120
        img = Image.new("RGBA", (max(bw, int(small.getlength(text))) + 20, 200))
        d = ImageDraw.Draw(img)
        x = (img.width - bw) // 2
        d.rounded_rectangle((x, 0, x + bw, 120), radius=60, fill=(204, 0, 0, 255), outline="black", width=5)
        d.text((x + 60, 12), "SUBSCRIBE", font=big, fill="white")
        d.text(((img.width - small.getlength(text)) / 2, 130), text, font=small, fill="white",
               stroke_width=5, stroke_fill="black")
        return img
    if style == "date":  # big white year with a yellow underline
        font = fit_font(text, 170, W - 200)
        tw = int(font.getlength(text))
        img = Image.new("RGBA", (tw + 100, 290))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, tw + 100, 290), radius=36, fill=(0, 0, 0, 160))  # readable on any image
        d.text((50, 20), text, font=font, fill="white", stroke_width=8, stroke_fill="black")
        d.rounded_rectangle((50 + tw * 0.15, 242, 50 + tw * 0.85, 258), radius=8, fill=YELLOW)
        return img
    if style == "place":  # dark pill with a yellow map pin
        font = fit_font(text, 64, W - 300)
        tw = int(font.getlength(text))
        img = Image.new("RGBA", (tw + 150, 110))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, tw + 150, 110), radius=55, fill=(0, 0, 0, 185))
        d.ellipse((34, 22, 76, 64), fill=YELLOW)
        d.polygon([(38, 52), (72, 52), (55, 92)], fill=YELLOW)
        d.ellipse((47, 35, 63, 51), fill=(0, 0, 0, 185))
        d.text((100, 18), text, font=font, fill="white")
        return img
    font = fit_font(text, 84, W - 220)  # fact: black text on a yellow box
    tw = int(font.getlength(text))
    img = Image.new("RGBA", (tw + 80, 130))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, tw + 80, 130), radius=22, fill=YELLOW, outline="black", width=5)
    d.text((40, 16), text, font=font, fill="black")
    return img


def graphic_low(choice: dict, raw: Path, film: Path | None) -> bool:
    """True when the picture's subject would land under the top callouts (y ~180-680 of the frame):
    the callout then sits just above the captions instead, so it doesn't cover a face. Maps the photo
    editor's subject row through how the picture is framed: cover crop for photos, parallax, AI clips
    and widescreen film, or the whole film centred (FILM_VF)."""
    y = choice.get("subject_y")
    if y is None or not raw.exists():
        return False
    with Image.open(raw) as im:
        aspect = im.width / im.height
    if film and not fills_frame(film):
        fy = (H - FILM_BAND) / 2 + y * FILM_BAND  # FILM_VF: always a FILM_BAND-tall band, centred
    else:  # a wide picture keeps its full height; a tall one loses some top and bottom
        shown = min(1.0, aspect / (W / H))
        fy = ((y - 0.5) / shown + 0.5) * H
    return 180 <= fy <= 680


LOW_BOTTOM = 1110  # a lowered callout ends here, just above the captions (~1175-1300)


def draw_graphic(frame: Image.Image, style: str, ov: Image.Image, t: float, start: float, end: float,
                 low: bool = False) -> None:
    """Animate the callout in, hold it, fade it out before the scene ends."""
    if style == "hook":  # fully visible on the first frame, fades out by 1.8s
        k, dx, dy, scale = min(1.0, max(0.0, (1.8 - t) / 0.3)), 0, 0, 1.0
    else:
        t_in, t_out = start, end - 0.25  # start = when the callout appears
        if not t_in <= t <= t_out:
            return
        e = min(1.0, (t - t_in) / 0.35)
        e = 1 - (1 - e) ** 3  # ease-out
        k = e * min(1.0, (t_out - t) / 0.3)
        dx = -60 * (1 - e) if style == "place" else 0
        dy = -40 * (1 - e) if style == "date" else 40 * (1 - e) if style == "cta" else 0
        scale = 0.7 + 0.3 * e if style == "fact" else 1.0
    if k <= 0:
        return
    img = ov if scale == 1.0 else ov.resize((max(1, int(ov.width * scale)), max(1, int(ov.height * scale))))
    if k < 1:
        img = img.copy()
        img.putalpha(img.getchannel("A").point(lambda v: int(v * k)))
    # clear of YouTube's top icons and the captions; the subscribe button sits just under the captions
    top = LOW_BOTTOM - ov.height if low else {"hook": 220, "cta": 1330}.get(style, 300)
    frame.paste(img, (int((W - img.width) / 2 + dx), int(top + (ov.height - img.height) / 2 + dy)), img)


def person_card(data: bytes, name: str) -> Image.Image:
    """Tilted photo card with a white border, drop shadow and a yellow name banner."""
    photo = Image.open(io.BytesIO(data)).convert("RGB")
    pw, ph = 520, 624  # 5:6 portrait crop, biased to the top where faces usually are
    scale = max(pw / photo.width, ph / photo.height)
    photo = photo.resize((int(photo.width * scale) + 1, int(photo.height * scale) + 1), Image.LANCZOS)
    left, top = (photo.width - pw) // 2, int((photo.height - ph) * 0.2)
    photo = photo.crop((left, top, left + pw, top + ph))
    b, pad, banner = 12, 40, 96
    card = Image.new("RGBA", (pw + 2 * b + 2 * pad, ph + 2 * b + banner // 2 + 2 * pad))
    shadow = Image.new("RGBA", card.size)
    ImageDraw.Draw(shadow).rounded_rectangle((pad + 10, pad + 16, pad + pw + 2 * b + 10, pad + ph + 2 * b + 16),
                                             radius=30, fill=(0, 0, 0, 170))
    card.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((pad, pad, pad + pw + 2 * b, pad + ph + 2 * b), radius=30, fill="white")
    mask = Image.new("L", (pw, ph))
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw, ph), radius=22, fill=255)
    card.paste(photo, (pad + b, pad + b), mask)
    font = fit_font(name.upper(), 64, pw - 40)
    tw = font.getlength(name.upper())
    bx0, by0 = pad + b + (pw - tw) / 2 - 28, pad + ph + 2 * b - banner // 2
    d.rounded_rectangle((bx0, by0, bx0 + tw + 56, by0 + banner), radius=18, fill=YELLOW, outline="black", width=5)
    d.text((bx0 + 28, by0 + 12), name.upper(), font=font, fill="black")
    return card.rotate(-3, resample=Image.BICUBIC, expand=True)


def draw_card(frame: Image.Image, card: Image.Image, t: float, on: float, off: float) -> Image.Image:
    """Pop the card in with a slight overshoot over a dimmed background, then shrink it away."""
    if not on <= t <= off:
        return frame
    a = min(1.0, (t - on) / 0.3)
    c1 = 1.70158  # easeOutBack: overshoots ~6% then settles
    scale = 0.6 + 0.4 * (1 + (c1 + 1) * (a - 1) ** 3 + c1 * (a - 1) ** 2)
    alpha = min(1.0, a * 2)
    if t > off - 0.2:  # exit
        e = (off - t) / 0.2
        scale, alpha = scale * (0.85 + 0.15 * e), alpha * e
    frame = frame.point(lambda v: int(v * (1 - 0.35 * alpha)))  # dim the background
    img = card.resize((max(1, int(card.width * scale)), max(1, int(card.height * scale))), Image.BILINEAR)
    if alpha < 1:
        img.putalpha(img.getchannel("A").point(lambda v: int(v * alpha)))
    frame.paste(img, ((W - img.width) // 2, 680 - img.height // 2), img)  # between top graphics and captions
    return frame


class ClipReader:
    """Streams a clip's frames in order. Decoding a whole 1080x1920 clip up front would hold GBs of
    RAM; the renderer only ever moves forward through a scene, so one pass is enough."""

    def __init__(self, path: Path):
        meta = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
                               "-show_entries", "stream=width,height,nb_read_packets", "-of", "csv=p=0", str(path)],
                              capture_output=True, text=True).stdout.strip().split(",")
        self.w, self.h, self.n = (int(v) for v in meta[:3])
        self.proc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", str(path), "-f", "rawvideo",
                                      "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.pos, self.buf = -1, None

    def at(self, p: float) -> Image.Image | None:
        """Frame at fraction p (0..1) of the clip; p never goes backwards within a scene."""
        want, size = round(p * (self.n - 1)), self.w * self.h * 3
        while self.pos < want:
            chunk = self.proc.stdout.read(size)
            if len(chunk) < size:
                break
            self.buf, self.pos = chunk, self.pos + 1
        if self.buf is None:
            return None
        img = Image.frombytes("RGB", (self.w, self.h), self.buf)
        return img if img.size == (W, H) else img.resize((W, H), Image.BICUBIC)

    def close(self) -> None:
        self.proc.kill()


def frame_maker(images, scenes, hook_text, cta_line, bounds, cues, clips: dict[int, Path]):
    """Returns frame(i, t): scene i at time t with camera move and graphics applied.
    cues[i] holds the timed extras for scene i, e.g. "card" (+ "on"/"off"). Scenes in `clips` play
    their clip (AI motion or 2.5D parallax, made on the GPU) stretched over the whole scene,
    instead of the CPU Ken Burns move. Readers are opened lazily: at most two stream at a time."""
    overlays = [graphic_overlay(*fallback_graphic(sc["graphic"])) if sc["graphic"] else None for sc in scenes]
    hook = graphic_overlay("hook", hook_text) if hook_text else None
    cta = graphic_overlay("cta", cta_line)
    tags = [credit_tag_image(sc["credit_tag"]) if sc.get("credit_tag") else None for sc in scenes]
    readers: dict[int, ClipReader] = {}

    def frame(i: int, t: float) -> Image.Image:
        start, end, cue = bounds[i], bounds[i + 1], cues[i]
        p = min(max((t - start + XFADE / 2) / (end - start + XFADE), 0), 1)
        img = None
        if i in clips:
            if i not in readers:
                for done in [k for k in readers if k < i - 1]:  # scenes behind us: free them
                    readers.pop(done).close()
                readers[i] = ClipReader(clips[i])
            img = readers[i].at(p)
        if img is None:
            img = shot(images[i], scenes[i]["move"], p)
        if overlays[i]:
            draw_graphic(img, scenes[i]["graphic"]["style"], overlays[i], t, cue["graphic"], end,
                         scenes[i]["graphic"].get("low", False))
        if i == 0 and hook:
            draw_graphic(img, "hook", hook, t, start, end)
        if cue.get("cta") is not None:
            draw_graphic(img, "cta", cta, t, cue["cta"], end)
        if cue.get("card"):
            img = draw_card(img, cue["card"], t, cue["on"], cue["off"])
        if tags[i] and t - start < CREDIT_SECONDS and (cue.get("cta") is None or t < cue["cta"]):  # never under the subscribe line
            img.paste(tags[i], (36, CREDIT_Y), tags[i])
        return img
    frame.close = lambda: [r.close() for r in readers.values()]  # type: ignore[attr-defined]
    return frame


def flash_alpha(t: float, cut: float) -> float:
    """White camera-flash curve: snaps up over the 2 frames before the cut, then decays (~0.4s)."""
    if cut - 0.07 <= t < cut:
        return 0.9 * (t - (cut - 0.07)) / 0.07
    return 0.9 * math.exp(-(t - cut) / 0.11) if cut <= t < cut + 0.5 else 0.0


def write_frames(frame, n: int, bounds: list[float], total: float, out, flashes: set[float]) -> None:
    """Stream every frame to ffmpeg. Cuts in `flashes` are hard cuts under a white flash; the
    others crossfade for XFADE seconds."""
    white = Image.new("RGB", (W, H), "white")
    for f in range(int(total * FPS)):
        t = f / FPS
        i = min(sum(1 for b in bounds[1:-1] if b <= t), n - 1)
        img = None
        if i + 1 < n and t >= bounds[i + 1] - XFADE / 2 and bounds[i + 1] not in flashes:
            a, b, cut = i, i + 1, bounds[i + 1]
        elif i > 0 and t < bounds[i] + XFADE / 2 and bounds[i] not in flashes:
            a, b, cut = i - 1, i, bounds[i]
        else:
            img = frame(i, t)
        if img is None:
            img = Image.blend(frame(a, t), frame(b, t), (t - (cut - XFADE / 2)) / XFADE)
        glare = max((flash_alpha(t, c) for c in flashes), default=0.0)
        out.write((Image.blend(img, white, glare) if glare else img).tobytes())


def thumbnail(image: Path, text: str, path: Path) -> None:
    img = Image.open(image).convert("RGB").resize((W, H), Image.LANCZOS)
    draw = ImageDraw.Draw(img)
    words, lines = text.upper().split(), []
    for w in words:  # two words per line
        if lines and len(lines[-1].split()) < 2:
            lines[-1] += " " + w
        else:
            lines.append(w)
    font = fit_font(max(lines, key=len), 190, W - 100)  # shrink long lines so nothing runs off the edge
    y = H * 0.30
    for line in lines:
        tw = draw.textlength(line, font=font)
        draw.text(((W - tw) / 2, y), line, font=font, fill=(255, 221, 0),
                  stroke_width=12, stroke_fill=(0, 0, 0))
        y += font.size * 1.16
    img.save(path, quality=92)


def clock(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:04.1f}"


def quality_check(video: Path, bounds: list[float], sources: list[str]) -> list[str]:
    """Automatic checks on the finished Short, using ffmpeg's own detectors in one pass: black or
    frozen stretches, loudness off target or clipping, scenes with no picture, unplanned length.
    Returns the problems worth a look before uploading ([] = all clear)."""
    def where(t: float) -> str:
        k = next((k for k in range(len(bounds) - 1) if bounds[k] <= t < bounds[k + 1]), len(bounds) - 2)
        return f"{clock(t)} (scene {k + 1})"
    log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video),
                          "-vf", "blackdetect=d=0.25:pix_th=0.08,freezedetect=n=0.002:d=2.5",
                          "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True, errors="replace").stderr
    if "Error opening input" in log or "Invalid data found" in log:
        return ["couldn't check the video: the file is missing or unreadable"]
    issues = [f"black screen at {where(float(t))}" for t in re.findall(r"black_start:\s*([\d.]+)", log)]
    issues += [f"picture frozen for 2.5s+ at {where(float(t))}" for t in re.findall(r"freeze_start:\s*([\d.]+)", log)]
    lufs, peak = re.findall(r"I:\s+(-?[\d.]+) LUFS", log), re.findall(r"Peak:\s+(-?[\d.]+) dBFS", log)
    if not lufs:
        issues.append("no sound found in the video")
    elif not -16 <= float(lufs[-1]) <= -12:  # the last match is ffmpeg's summary for the whole video
        issues.append(f"loudness {float(lufs[-1]):.1f} LUFS, target is -14 (too {'quiet' if float(lufs[-1]) < -16 else 'loud'})")
    if peak and float(peak[-1]) > -0.5:
        issues.append(f"sound peaks at {float(peak[-1]):.1f} dB, close to distorting")
    issues += [f"scene {k + 1} has no picture (plain frame)" for k, src in enumerate(sources) if src.startswith("PLAIN")]
    if bounds[-1] > (36 if SHORT_FORM else 62):
        issues.append(f"{clock(bounds[-1])} long, past the planned {length_plan()[4]} seconds")
    return issues


def visual_review(video: Path, short: dict, bounds: list[float], sources: list[str], work: Path) -> tuple[list[str], dict[int, tuple[str, str]]]:
    """The AI watches the finished Short as sheets of one frame per second and reports what a viewer would
    notice (the 2026-10-15 Cardiff review found smoke blobs, an invented face and another trial's caption only
    by eye). One AI call; its findings join the CHECK lines. Failure means no findings."""
    folder = work / "review"
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir()
    try:  # 6x5 tiles = 30 seconds per sheet
        ffmpeg("-i", str(video), "-vf", "fps=1,scale=300:-2,tile=6x5", "-fps_mode", "vfr", "sheet%d.jpg", cwd=folder)
    except subprocess.CalledProcessError:
        return [], {}
    sheets = sorted(folder.glob("sheet*.jpg"), key=lambda p: int(p.stem[5:]))
    plan = "\n".join(f"scene {i + 1} ({clock(bounds[i])}-{clock(bounds[i + 1])}): \"{sc['narration']}\" | picture: {src[:160]}"
                     for i, (sc, src) in enumerate(zip(short["scenes"], sources)))
    data = ask_ai(f"""You are the final reviewer of a YouTube Short: "{short['title']}". Open and look at each sheet:
{chr(10).join(f"{p} (seconds {30 * k}-{30 * k + 29}, one frame per second, left to right, top to bottom)" for k, p in enumerate(sheets))}
The plan: {plan}
Report only problems a viewer would notice: AI artifacts (smoke or fog blobs, melting or warped people,
faces or objects), text or graphics covering a face, a picture that doesn't match its line or shows the
wrong era/place/person, unreadable, washed-out or nearly blank pictures, printed captions, logos or
watermarks on a real photo or film, a painted or AI picture standing in for a real person or object as if it
were real. Writing inside an AI-GENERATED painting is allowed when it is real, readable words that fit the
story; garbled or made-up lettering there is a problem (fix "repaint"). Ignore
the captions, the subscribe button and normal crossfades. No problems: an empty list.
fix = "repaint" when showing a different picture in that scene would fix it (wrong or blank picture, AI
artifacts, captions/logos in footage, someone else's AI art posing as real); "graphic" when the scene's line is
about places, a number, a document, a mechanism, or a cause-and-effect chain and a full-screen motion graphic
(map journey, big number, document, or custom animated diagram) would show it better than any picture; null
otherwise (e.g. a graphic covering a face).
Reply with ONLY JSON: {{"problems": [{{"second": 12, "scene": 3, "what": "a white smoke cloud covers the statue", "fix": "repaint"}}]}}""",
                  fatal=False, read_dir=folder)
    return review_fixes(data, len(short["scenes"]))


def review_fixes(data, n_scenes: int) -> tuple[list[str], dict[int, tuple[str, str]]]:
    """The review's reply -> (CHECK lines, scene -> ("repaint" | "graphic", why)). Scene 1 is never turned into a
    graphic (the hook keeps a picture); an older-style `repaint: true` still means repaint."""
    found, fixes = [], {}
    for p in (data or {}).get("problems") or []:
        if isinstance(p, dict) and str(p.get("what") or "").strip():
            sec = p.get("second") if is_num(p.get("second")) else None
            what = str(p["what"]).strip()[:200]
            n = p.get("scene") if isinstance(p.get("scene"), int) and 1 <= p["scene"] <= n_scenes else None
            found.append(f"LOOK{f' at {clock(sec)}' if sec is not None else ''}{f' (scene {n})' if n else ''}: {what}")
            kind = p.get("fix") if p.get("fix") in ("repaint", "graphic") else "repaint" if p.get("repaint") is True else None
            if n and kind:
                fixes.setdefault(n - 1, ("repaint" if n == 1 else kind, what))
    return found[:8], fixes


def apply_review_fixes(st: dict, work: Path, fixes: dict[int, tuple[str, str]]) -> list[str]:
    """The automatic fixes after a render's review (up to AUTO_REPAINT_MAX scenes per round): "graphic" scenes
    become a full-screen motion graphic when one fits their line, a custom motion graphic that looked wrong is
    redrawn by its coder, the rest get a new painted picture.
    Returns the edit-plan notes."""
    fixed = list(fixes.items())[:AUTO_REPAINT_MAX]
    want = [i for i, (kind, _) in fixed if kind == "graphic"]
    got = set(rescue_graphics(st["short"], want, {i: why for i, (_, why) in fixed})) if want else set()
    # Same slot numbering as render_remotion (the k-th custom scene uses slot k).
    # shortcut: a rescue that adds a custom scene before this one shifts the slots and the redraw is re-coded fresh.
    customs = [k for k, sc in enumerate(st["short"]["scenes"]) if (sc.get("full") or {}).get("type") == "custom"]
    notes, repaint = [], {}
    for i, (_, why) in fixed:
        if i in customs and redraw_custom(st["short"], i, min(3, customs.index(i)), why, work):
            notes.append(f"scene {i + 1}'s motion graphic was redrawn ({why})")
        elif i in got:  # the picture stays in the plan: it is the fallback if Remotion fails
            notes.append(f"scene {i + 1} became a motion graphic ({why})")
        else:
            paint_new(work, st, i)
            repaint[i] = why
    rewritten = rewrite_paint_prompts(st["short"], repaint) if repaint else []
    for i, why in repaint.items():
        how = "a rewritten prompt" if i in rewritten else "its old prompt, seen from a new angle"
        notes.append(f"scene {i + 1} got a new painted picture from {how} ({why})")
    return notes


def storyboard(video: Path, bounds: list[float], path: Path) -> None:
    """One mid-scene frame per scene from the finished video, labeled with its timestamps."""
    n, cols, tw, th = len(bounds) - 1, 4, 270, 480
    rows = (n + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 12, rows * (th + 52) + 12), (20, 20, 24))
    d, font = ImageDraw.Draw(sheet), ImageFont.truetype(FONT, 30)
    for i in range(n):
        x, y = 12 + (i % cols) * (tw + 12), 12 + (i // cols) * (th + 52)
        still = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{(bounds[i] + bounds[i + 1]) / 2:.2f}",
                                "-i", str(video), "-frames:v", "1", "-vf", f"scale={tw}:{th}", "-f", "image2pipe",
                                "-vcodec", "png", "-"], capture_output=True).stdout
        if still:
            sheet.paste(Image.open(io.BytesIO(still)).convert("RGB"), (x, y))
        d.text((x, y + th + 8), f"{i + 1}  {clock(bounds[i])}-{clock(bounds[i + 1])}", font=font, fill="white")
    sheet.save(path, quality=88)


def sfx_events(short: dict, cues: list[dict], bounds: list[float], remotion: bool) -> list[dict]:
    """Sound design: each timed visual gets a matching sound. Candidates are kept by priority;
    a sound is dropped if it would land within 0.5s of a more important one. No sub-bass hits:
    on phone speakers they read as random thumps. Ticks and the riser are quiet textures that may
    overlap. Returns the cue sheet sorted by time."""
    last: dict[str, int] = {}

    def pick(kind: str, n: int) -> str:  # never the same variant twice in a row
        v = random.choice([k for k in range(n) if k != last.get(kind)] or [0])
        last[kind] = v
        return f"{kind}{v}"

    cand = []
    scenes = short["scenes"]
    for i, sc in enumerate(scenes):
        start, cue, g = bounds[i], cues[i], sc["graphic"]
        if i and sc["transition"] == "flash":
            cand.append({"t": start - 0.05, "sound": pick("flash", 2), "gain": 0.9, "prio": 8, "what": "flash cut"})
        elif i and sc["transition"] == "whip" and remotion:  # owner dislikes loud whooshes: quiet, and only on whips
            cand.append({"t": start - 0.1, "sound": pick("whoosh", 4), "gain": 0.2, "prio": 4, "what": "whip pan"})
        elif i and sc["transition"] == "fade" and random.random() < 0.5:  # cuts, wipes and leaks stay silent
            cand.append({"t": start - 0.35, "sound": pick("whoosh", 4), "gain": 0.12, "prio": 1, "what": "soft whoosh"})
        if (sc.get("sound") or {}).get("file") and cue.get("sound_at") is not None:
            cand.append({"t": cue["sound_at"], "sound": sc["sound"]["file"], "gain": STORY_SOUND_GAIN, "prio": 9,
                         "what": f"story sound: {sc['sound']['sound']}"})
        f, fc = sc.get("full"), cue.get("full")
        if f and fc and remotion:  # full-screen motion graphic: one sound per thing that lands
            if f["type"] == "board":
                cand += [{"t": t, "sound": "pin", "gain": 0.3, "prio": 5, "what": "print pinned to the board"} for t in fc["times"]]
            elif f["type"] == "journey":
                for k, t in enumerate(fc["times"]):
                    cand.append({"t": t, "sound": "pin", "gain": 0.3, "prio": 5, "what": "map pin drops"})
                    if k:
                        cand.append({"t": round(fc["times"][k - 1] + 0.2, 3), "sound": "scratch", "gain": 0.3, "prio": 4,
                                     "what": "route line draws"})
            elif f["type"] == "number":
                cand.append({"t": fc["at"], "sound": "ticks", "gain": 0.25, "prio": 5, "what": "number counts up"})
            elif f["type"] == "custom":
                beats = fc.get("cues") or [start + 0.4]
                for k, t in enumerate(beats):
                    cand.append({"t": t, "sound": "pin" if k == 0 else (pick("stamp", 2) if k == len(beats) - 1 else "scratch"),
                                 "gain": 0.35 if k == len(beats) - 1 else 0.28, "prio": 5, "what": "custom graphic beat"})
            else:
                cand.append({"t": start + 0.1, "sound": pick("stamp", 2), "gain": 0.45, "prio": 6, "what": "document lands"})
                cand.append({"t": fc["at"], "sound": "scratch", "gain": 0.35, "prio": 5, "what": "red underline"})
        at = cue.get("graphic")
        if g and g["style"] == "fact":
            cand.append({"t": at, "sound": pick("stamp", 2), "gain": 0.6, "prio": 6, "what": "fact box stamp"})
        elif g and g["style"] == "date":
            ticks = remotion and g["text"].isdigit()  # Remotion counts the year up; ticks follow it
            cand.append({"t": at, "sound": "ticks" if ticks else pick("stamp", 2),
                         "gain": 0.25 if ticks else 0.35, "prio": 5, "what": "year counter ticks" if ticks else "date stamp"})
        elif g and remotion and "lat" in g:
            cand.append({"t": at, "sound": pick("whoosh", 4), "gain": 0.15, "prio": 4, "what": "map flies in"})
            cand.append({"t": at + 1.5 * cue.get("map_pace", 1), "sound": "pin", "gain": 0.3, "prio": 5, "what": "map pin drop"})
        elif g and remotion and g["style"] == "stat":
            cand.append({"t": at + 0.3, "sound": "ticks", "gain": 0.25, "prio": 5, "what": "number counts up"})
        elif g and remotion and g["style"] == "timeline":
            cand.append({"t": at + 0.4, "sound": pick("whoosh", 4), "gain": 0.15, "prio": 4, "what": "timeline marker slides"})
        elif g and remotion and g["style"] == "mark":
            cand.append({"t": at + 0.4, "sound": "pin", "gain": 0.25, "prio": 5, "what": f"{g.get('shape', 'circle')} drawn"})
        elif g and remotion and g["style"] in ("stamp", "headline"):  # both land with a thump at ~0.25s
            cand.append({"t": at + 0.25, "sound": pick("stamp", 2), "gain": 0.6, "prio": 6, "what": GRAPHIC_STYLES[g["style"]]})
        elif g and remotion and g["style"] in ("question", "kinetic"):
            cand.append({"t": at, "sound": "ticks", "gain": 0.25 if g["style"] == "question" else 0.3, "prio": 5,
                         "what": GRAPHIC_STYLES[g["style"]]})
        elif g and remotion and g["style"] == "quote":
            cand.append({"t": at + 0.3, "sound": "ticks", "gain": 0.2, "prio": 5, "what": "quote types out"})
        elif g and remotion and g["style"] == "compare":
            cand.append({"t": at + 0.3, "sound": pick("whoosh", 4), "gain": 0.15, "prio": 4, "what": "bars grow"})
        elif g:
            cand.append({"t": at, "sound": "pin", "gain": 0.3, "prio": 5, "what": "location label"})
        if cue.get("card"):
            cand.append({"t": cue["on"], "sound": pick("shutter", 2), "gain": 0.45, "prio": 7, "what": "photo card shutter"})
    if cues[-1].get("cta") is not None:
        cand.append({"t": cues[-1]["cta"], "sound": "pin", "gain": 0.25, "prio": 3, "what": "subscribe button"})
    riser = None
    if len(scenes) > 2 and bounds[-2] > 6:  # build tension into the payoff scene
        riser = {"t": bounds[-2] - 2.2, "sound": "riser", "gain": 0.18, "prio": 2, "what": "riser into the payoff"}

    textures = [e for e in cand if e["sound"] in ("ticks", "scratch")] + ([riser] if riser else [])
    chosen: list[dict] = []
    for e in sorted((e for e in cand if e["sound"] not in ("ticks", "scratch")), key=lambda e: (-e["prio"], e["t"])):
        if not any(abs(e["t"] - c["t"]) < 0.5 for c in chosen):
            chosen.append(e)
    chosen += textures
    for e in chosen:
        e["t"] = max(0.0, e["t"])
    return sorted(chosen, key=lambda e: e["t"])


def graphics_count(short: dict, cues: list[dict]) -> int:
    return (sum(1 for sc in short["scenes"] if sc["graphic"] or sc.get("full"))
            + sum(1 for c in cues if c.get("card")))


def full_summary(f: dict) -> str:
    """One plain line for edit_plan.txt saying what a full-screen motion graphic shows."""
    if f["type"] == "journey":
        return f"map journey: {' -> '.join(s['name'] for s in f['stops'])}" + (f", {f['note']}" if f.get("note") else "")
    if f["type"] == "number":
        if f.get("compare"):
            c = f["compare"]
            return f"big number: {f['label']}: {c['a_label']} {c['a_value']:,.10g} vs {c['b_label']} {c['b_value']:,.10g} (two bars)"
        painted = f", painted '{f['thing']}' figure" if f.get("figure") and Path(f["figure"]).exists() else ""
        return f"big number: {f['show']} {f['label']} ({f['figures']} figures, each = {f['each']:,.10g}{painted})"
    if f["type"] == "board":
        return "evidence board: " + " / ".join(it["label"] for it in f["items"])
    if f["type"] == "custom":
        return f"custom animation ({f.get('kind', 'diagram')}): {f.get('title', 'SCENE')} — {f.get('brief', '')}"
    return (f"document ({f['kind']}): \"{f['key_line']}\" underlined"
            + (f", masthead {f['paper']}" if f.get("paper") else ""))


def full_props(sc: dict, cue: dict, i: int, pics: list | None, job: Path,
               skin: str = "parchment", slot: int = 0) -> dict | None:
    """The `full` object Remotion draws for scene i: the plan's data, its word timings, and its pictures copied
    into the job folder. None when it can't be drawn (a board needs 3 photos)."""
    f, c = sc.get("full"), cue.get("full")
    if not f or not c:
        return None
    out = {k: v for k, v in f.items() if k not in ("word", "words", "find", "photos")}
    out["seed"] = i + 1
    out.setdefault("skin", skin)

    def put(k: int, pic: tuple) -> tuple[str, float]:
        path = job / f"full{i}_{k}.jpg"
        path.write_bytes(pic[0])
        with Image.open(path) as im:
            return f"job/{path.name}", im.width / im.height

    if f["type"] == "journey":
        out["stops"] = [{**{k: v for k, v in st.items() if k != "word"}, "at": t} for st, t in zip(f["stops"], c["times"])]
        out["noteAt"] = c.get("noteAt")
    elif f["type"] == "board":
        if not pics or len(pics) < 3:
            return None
        out["items"] = []
        for k, (it, pic, t) in enumerate(zip(f["items"], pics, c["times"])):
            image, aspect = put(k, pic)
            out["items"].append({"image": image, "aspect": aspect, "label": it["label"], "at": t})
    elif f["type"] == "number":
        out["at"] = c["at"]
        fig = Path(out.pop("figure", "") or "")
        if fig.name and fig.exists():  # Gemini's ink silhouette of the counted thing (else the built-in icon)
            shutil.copy(fig, job / f"fig{i}.png")
            out["image"] = f"job/fig{i}.png"
    elif f["type"] == "custom":
        cues_list = c.get("cues") or [0.5, 1.8, 3.0]
        out.update(slot=slot, cues=cues_list, photos=[])
        for k, (it, pic) in enumerate(zip(f.get("photos") or [], pics or [])):
            image, aspect = put(k, pic)
            out["photos"].append({"image": image, "aspect": aspect, "label": it["label"],
                                  "at": cues_list[min(k, len(cues_list) - 1)]})
    else:
        out.update(at=c["at"], lineEnd=c["lineEnd"])
        if pics:
            out["image"], out["aspect"] = put(0, pics[0])
    return out


def fallback_custom_tsx(slot: int, narration: str, brief: str) -> str:
    """Guaranteed-valid Remotion component for slot 0..3 if the AI coder fails or leaves a TypeScript error."""
    parts = [p.strip() for p in re.split(r"[,;:.—–-]+|\band\b|\bthen\b", narration) if p.strip()][:3]
    while len(parts) < 3:
        parts.append(brief[:42] or "KEY MOMENT")
    cards = [json.dumps(p[:36]) for p in parts[:3]]
    stamp = json.dumps(" ".join(parts[-1].upper().split()[:2])[:16] or "VERIFIED")
    return f"""import React from 'react';
import {{Card, Connect, CustomFull, FullProps, Paper, StampBadge, TitleBanner, cueAt, focusCam, layoutColumn, skinOf}} from '../toolkit';

export const Custom{slot}: React.FC<FullProps<CustomFull>> = ({{full, t, start, end}}) => {{
	const sk = skinOf(full.skin);
	const boxes = layoutColumn(3, {{w: 680, bottom: 900}});
	const c = [0, 1, 2].map((i) => cueAt(full, i, start, end, 3));
	const titles = [{', '.join(cards)}];
	return (
		<Paper t={{t}} start={{start}} seed={{full.seed}} cam={{focusCam(540, 630, 1)}} skin={{full.skin}}>
			<TitleBanner title={{full.title || 'CASE FILE'}} sub={{{json.dumps(brief[:48].upper())}}} t={{t}} at={{start + 0.05}} skin={{full.skin}} />
			{{boxes.map((b, i) => (
				<Card key={{i}} box={{b}} step={{i === 2 ? 'Outcome' : `Step 0${{i + 1}}`}} title={{titles[i]}} t={{t}} at={{c[i]}} skin={{full.skin}} highlight={{i === 1}} />
			))}}
			<Connect from={{boxes[0]}} to={{boxes[1]}} avoid={{boxes}} t={{t}} at={{c[1] - 0.3}} skin={{full.skin}} />
			<Connect from={{boxes[1]}} to={{boxes[2]}} avoid={{boxes}} t={{t}} at={{c[2] - 0.3}} skin={{full.skin}} />
			<StampBadge text={{{stamp}}} x={{540}} y={{965}} rot={{-7}} t={{t}} at={{c[2] + 0.5}} color={{sk.accent}} />
		</Paper>
	);
}};
"""


def clean_tsx_code(raw: str, slot: int) -> str | None:
    """Extract clean TypeScript/React code exporting Custom{slot} from an AI reply."""
    if not isinstance(raw, str) or not raw.strip():
        return None
    code = raw.strip()
    fence = re.search(r"```(?:tsx|typescript|ts|jsx|js)?\s*\n(.*?)```", code, re.S)
    if fence:
        code = fence.group(1).strip()
    if f"export const Custom{slot}" not in code and f"export function Custom{slot}" not in code:
        return None
    return code + "\n"


def code_custom_scenes(short: dict, scenes: list[dict], work: Path) -> None:
    """Motion Graphics Agent: writes bespoke React/SVG Remotion code for each `type: 'custom'` scene in `scenes`,
    type-checks with `npx tsc -p .`, retries once on compiler errors, and falls back cleanly if needed."""
    npx = shutil.which("npx")
    gen_dir = REMOTION / "src" / "full" / "generated"
    customs = [(i, sc) for i, sc in enumerate(scenes) if (sc.get("full") or {}).get("type") == "custom"]
    if not customs:
        return
    for i, sc in customs:
        f = sc["full"]
        slot = int(f.get("slot") or 0)
        target = gen_dir / f"Custom{slot}.tsx"
        cached = work / f"Custom{slot}.tsx"
        narration = short["scenes"][i]["narration"]
        brief = short["scenes"][i]["full"].get("brief", "")
        sig = f"// Custom{slot}: {f.get('title')} | {f.get('kind')} | {f.get('skin')} | {brief[:80]}"
        if cached.exists() and cached.read_text(encoding="utf-8", errors="ignore").startswith(sig):
            target.write_text(cached.read_text(encoding="utf-8"), encoding="utf-8")
            continue
        print(f"    coding custom motion graphic for scene {i + 1} ({f.get('kind')}, {f.get('skin')} skin)...")
        prompt = f"""You are the Motion Graphics Coder for a vertical 1080x1920 YouTube Short: "{short['title']}".
Write a bespoke Remotion React/TypeScript component `Custom{slot}` for Scene {i + 1}.
- Scene narration: {narration!r}
- Scene time window: start={sc['start']:.2f}s, end={sc['end']:.2f}s
- Spoken beat timestamps (`full.cues`): {f.get('cues')}
- Visual skin (`full.skin`): {f.get('skin')!r}
- Category (`full.kind`): {f.get('kind')!r}
- Title (`full.title`): {f.get('title')!r}
- Visual brief to draw & animate: {brief!r}
- Available real photos in `full.photos`: {json.dumps(f.get('photos') or [], ensure_ascii=False)}

{custom_rules(slot)}
Reply with ONLY JSON: {{"code": "import React from 'react';\\n..."}}"""
        data = ask_ai(prompt, fatal=False)
        code = clean_tsx_code((data or {}).get("code"), slot)
        ok = False
        for attempt in range(2):
            if not code:
                break
            target.write_text(sig + "\n" + code, encoding="utf-8")
            broken = lint_custom_code(code)
            err = "\n".join(broken) if broken else tsc_check() if npx else None
            if err is None:
                ok = True
                break
            if attempt == 0:
                print(f"      the check found an issue in Custom{slot}.tsx, repairing...")
                fix_data = ask_ai(f"""Fix the problems in `Custom{slot}.tsx` below (compiler errors or broken scene rules).
Keep the same imports from `'../toolkit'` and export `Custom{slot}`.
{custom_rules(slot)}
Problems:
{err}

Broken code:
{code}

Reply with ONLY JSON: {{"code": "import React from 'react';\\n..."}}""", fatal=False)
                code = clean_tsx_code((fix_data or {}).get("code"), slot)
        if ok and npx:  # look at the scene before the real render, fix it once if it looks wrong
            better = look_and_fix(short, sc, slot, code, work)
            if better != code:
                target.write_text(sig + "\n" + better, encoding="utf-8")
                if tsc_check() is not None:  # the fix broke the build: keep the version that compiled
                    target.write_text(sig + "\n" + code, encoding="utf-8")
        if not ok:
            print(f"      using clean fallback layout for Custom{slot}.tsx")
            target.write_text(sig + "\n" + fallback_custom_tsx(slot, narration, brief), encoding="utf-8")
        cached.write_text(target.read_text(encoding="utf-8"), encoding="utf-8")


def custom_rules(slot: int) -> str:
    """The rules every custom motion-graphic scene follows, plus two worked examples (real, compiling scenes in
    remotion/src/full/examples/). Shared by the coder, its repair, the look check and the review's redraw."""
    examples = "\n\n".join(f"// ===== {p.name} =====\n{p.read_text(encoding='utf-8')}"
                             for p in sorted((REMOTION / "src" / "full" / "examples").glob("*.tsx")))
    return f"""RULES (a scene that breaks one is rejected and rewritten):
1. Import ONLY from 'react' and '../toolkit'. Export `export const Custom{slot}: React.FC<FullProps<CustomFull>> = ({{full, t, start, end}}) => {{...}};`
2. Root element `<Paper t={{t}} start={{start}} seed={{full.seed}} cam={{focusCam(fx, fy, fScale)}} skin={{full.skin}}>`, first child
   `<TitleBanner title={{full.title}} sub="..." t={{t}} at={{start + 0.05}} skin={{full.skin}} />`. focusCam within fx 400..680, fy 550..650,
   fScale 0.95..1.14.
3. THE STAGE: everything (cards, photos, drawings, labels, stamps) inside x 110..970, y 260..1020 (SAFE). The title banner sits
   above it and the captions below it.
4. BOXES: every card is `<Card box={{...}}>` with a box from layoutRow / layoutColumn / layoutGrid / boxAt (fixed size, text
   always fits). A photo's outline is photoBox(...). Never FlowCard. Nothing may overlap anything else: leave room for
   stamps and labels on purpose (e.g. layoutColumn(3, {{bottom: 900}}) frees y 900..1020).
5. ARROWS: only `<Connect from={{boxA}} to={{boxB}} avoid={{everyBoxOnStage}} .../>`. It routes edge to edge and never
   crosses a box listed in avoid. Never FlowArrow, never hand-drawn arrow lines or arrowheads (<marker>).
6. MOVEMENT: anything that moves across the stage uses travel(t, at, from, to): it never goes faster than MIN_MOVE
   (0.9 s). No quick hops or zips; things land, then hold still while they are read.
7. TIMING: each element appears on a spoken beat (cueAt(full, i, start, end, n)); one idea per scene, at most ~6
   elements; text never smaller than the Card's own sizing. Animate only with interpolate / spring / appear / popIn /
   travel driven by `t`: CSS transition, animation and @keyframes don't render.
8. Be inventive inside these rules: your own <svg> drawings (a cross-section, a gauge, a route, a scale, a timeline),
   PhotoCutout for real photos in full.photos, ClockDial, CalloutTag, StampBadge, the skin's colours (skinOf(full.skin)).
9. TASTE (numbers from claude-motion's motion-design skill): arrivals ease out Easing.bezier(0.16, 1, 0.3, 1), exits ease
   in Easing.bezier(0.6, 0, 0.9, 0.35) in about half the entrance time, moves between two states Easing.bezier(0.65, 0,
   0.35, 1); linear only for continuous drift, rotation or ticking. Springs: settle {{damping: 14, stiffness: 140, mass:
   0.8}}, stamps/callouts pop {{damping: 10, stiffness: 220, mass: 0.7}}, at most ONE elastic accent {{damping: 8,
   stiffness: 200}} per scene. Stagger words ~0.09 s, list items ~0.2 s; never everything at once with one duration.
   One focal point per frame; the skin's accent colour marks the point, not decoration. Text never moves while it is
   read: it settles and holds >= 1 s (+0.25 s per word past three).
TWO WORKED EXAMPLES (copy their care, not their content):
{examples}"""


def lint_custom_code(code: str) -> list[str]:
    """Rule breaks a compiler can't see in an AI-coded custom scene (see custom_rules). Empty = clean."""
    found = []
    for mod in re.findall(r"""\bfrom\s+['"]([^'"]+)['"]""", code):
        if mod not in ("react", "../toolkit"):
            found.append(f"imports from '{mod}': import only from 'react' and '../toolkit'")
    checks = [(r"<FlowArrow\b", "draws an arrow by hand (FlowArrow): use <Connect from={box} to={box} avoid={allBoxes}>"),
              (r"<FlowCard\b", "uses FlowCard (it grows and overlaps): use <Card box={...}> with a box from layoutRow/layoutColumn/layoutGrid/boxAt"),
              (r"<marker\b|markerEnd|marker-end", "hand-made arrowheads: use <Connect>"),
              (r"\btransition\s*:|\banimation\s*:|@keyframes", "CSS transition/animation doesn't render in Remotion: animate with interpolate/travel")]
    found += [why for pattern, why in checks if re.search(pattern, code)]
    found += [f"missing <{tag}>" for tag in ("Paper", "TitleBanner") if f"<{tag}" not in code]
    return found


def preview_custom(short: dict, sc: dict, slot: int, work: Path) -> Path | None:
    """Renders just this custom scene small (its pictures are already in remotion/public/job) and returns a contact
    sheet of 8 frames across it, for the coder to look at before the real render. None if anything fails."""
    props = {"fps": FPS, "total": sc["end"] + 0.05, "xfade": XFADE, "hook": "", "palette": PALETTES.get(short.get("palette"), None),
             "scenes": [sc], "flashes": [], "words": [], "cta": None, "ctaLine": ""}
    return preview_sheet(props, sc["start"], sc["end"], work)


def preview_sheet(props: dict, start: float, end: float, work: Path) -> Path | None:
    """Renders seconds start..end of a small Short (`props`; its pictures already in remotion/public/job) at 40 %
    size and returns a contact sheet of 8 frames across it (work/look/sheet.jpg, next to preview.mp4), for an AI
    to look at before the real render. None if anything fails."""
    look = work / "look"
    shutil.rmtree(look, ignore_errors=True)
    look.mkdir(parents=True)
    a, b = int(start * FPS), max(int(start * FPS), int(end * FPS) - 1)
    (look / "props.json").write_text(json.dumps({k: v for k, v in props.items() if v is not None or k == "cta"}), encoding="utf-8")
    try:
        subprocess.run([shutil.which("npx") or "npx", "remotion", "render", "src/index.ts", "Short", str(look / "preview.mp4"),
                        f"--props={look / 'props.json'}", f"--frames={a}-{b}", "--scale=0.4", "--log=error", "--gl=angle",
                        "--concurrency=4", "--x264-preset=ultrafast"], cwd=REMOTION, check=True, timeout=600,
                       capture_output=True)
        step = max(1, (b - a + 1) // 8)
        ffmpeg("-i", "preview.mp4", "-vf", f"select='not(mod(n\\,{step}))',scale=300:-1,tile=4x2", "-frames:v", "1",
               "-fps_mode", "vfr", "sheet.jpg", cwd=look)
    except (subprocess.SubprocessError, OSError):
        return None
    return look / "sheet.jpg" if (look / "sheet.jpg").exists() else None


def look_and_fix(short: dict, sc: dict, slot: int, code: str, work: Path) -> str:
    """The coder looks at 8 frames of its own scene before the real render and rewrites it once if something is wrong
    (overlaps, an arrow through a box, off the stage, unreadable, too fast). Returns the code to use: the rewrite
    only when it follows the rules (the caller compile-checks it), else the original."""
    sheet = preview_custom(short, sc, slot, work)
    if not sheet:
        return code
    print(f"      looking at the custom scene before rendering...")
    data = ask_ai(f"""You coded `Custom{slot}` (below) for the YouTube Short "{short['title']}". Open {sheet} and look at it: 8 frames
across the scene, left to right, top to bottom (the captions and title banner are drawn later, ignore their space).
Check, as a strict art director: does anything overlap anything else? does an arrow or line cross a card, photo or
text? is anything outside the stage (x 110..970, y 260..1020) or cut off? is any text too small to read on a phone?
does anything jump or move so fast it looks like a glitch between frames? is the stage badly balanced (all crammed
in one corner, big empty areas)? do two things compete for attention in one frame? is text still sliding or growing
in a frame where it should be read? does everything appear at once instead of one after another? If it is clean, reply {{"ok": true}}. If not, list the problems and give the fixed
code that still follows every rule.
{custom_rules(slot)}
Current code:
{code}
Reply with ONLY JSON: {{"ok": false, "problems": ["..."], "code": "import React from 'react';\\n..."}}""",
                  fatal=False, read_dir=sheet.parent)
    if not isinstance(data, dict) or data.get("ok") is not False:
        return code
    new = clean_tsx_code(data.get("code"), slot)
    if not new or lint_custom_code(new):
        return code
    print(f"      fixed: {'; '.join(str(x) for x in data.get('problems') or [])[:160]}")
    return new


def tsc_check() -> str | None:
    """Type-checks the Remotion project; None when it compiles, else the compiler's complaint (trimmed)."""
    chk = subprocess.run([shutil.which("npx") or "npx", "tsc", "-p", "."], cwd=REMOTION, capture_output=True, text=True,
                         encoding="utf-8", errors="replace", timeout=120)
    return None if chk.returncode == 0 else (chk.stdout + "\n" + chk.stderr).strip()[:1500]


# ---- Style-library inventions (2026-10-19): the AI codes a new look / overlay / transition for one Short ----
STYLE_TYPES = {"look": "Look", "overlay": "Overlay", "transition": "Transition"}
STYLE_INTERFACES = {
    "look": "type Look = React.FC<{src: string; t: number; start: number; end: number; inks: Inks; seed: number}>: draws the "
            "scene's still picture `src` in a style, filling 1080x1920 (the scene's zoom/pan is applied outside it).",
    "overlay": "type Overlay = React.FC<{graphic: {text: string; trigger?: string; low?: boolean}; t: number; start: number; "
               "end: number; variant: number}>: drawn over the picture from `start` (when its word is spoken) to `end`.",
    "transition": "type Transition = {duration: number; render: (p: number, inks: Inks, seed: number) => {from?: CSSProperties; "
                  "to?: CSSProperties; cover?: ReactNode}}: p runs 0..1 across `duration` seconds centred on the cut; `from` "
                  "styles the old scene, `to` the new one, `cover` is drawn above both."}
STYLE_KIND_RULES = {
    "look": "Draw the picture ONCE per scene with useOnceCanvas(src, draw) (heavy pixel work goes there: luminance, stretch, "
            "drawCover help), then show <Img src={url ?? src} style={FILL} /> so a picture that can't be read still shows "
            "plainly. Per-frame life only as cheap layers driven by t and seed (noise). The subject must stay readable on a "
            "phone: the owner rejected a look that turned photos into unreadable dots.",
    "overlay": "Text comes only from graphic.text. Nothing below y CAPTION_TOP (1150, the captions) or above y 120. Appear at "
               "`start` with motion (not a plain fade), hold still enough to read, be gone by `end`. Use theme colours and FONT.",
    "transition": "duration between 0.2 and 0.8. `to` must hide the new scene at p=0 (opacity 0) and show it fully at p=1. "
                  "A cover must be fully gone at p=0 and p=1. Use the Short's inks."}


def style_placeholders() -> dict[str, str]:
    """The empty invention slots (remotion/src/style/placeholders.json), by slot name."""
    return json.loads((STYLE_DIR / "placeholders.json").read_text(encoding="utf-8"))


def restore_style_slots() -> None:
    """Puts the empty placeholders back into remotion/src/style/generated/ (after a render, or a failed invention)."""
    for slot, code in style_placeholders().items():
        (STYLE_DIR / "generated" / f"{slot}.tsx").write_text(code, encoding="utf-8", newline="\n")


def style_rules(kind: str) -> str:
    """The rules every invented component of `kind` follows, with the library's components of that kind as worked
    examples. Shared by the first draft, its repair and the look check."""
    examples = "\n\n".join(f"// ===== {e['file']} ({e['name']}) =====\n{(STYLE_DIR / e['file']).read_text(encoding='utf-8')}"
                           for e in style_library(kind))
    return f"""RULES (code that breaks one is rejected, and the library's fallback is used instead):
1. Import ONLY from 'react', '../kit' and '../types'. Export exactly `export const {STYLE_SLOTS[kind]}: {STYLE_TYPES[kind]} = ...`.
2. INTERFACE: {STYLE_INTERFACES[kind]}
3. Animate only from the props (t, p, seed) with interpolate / spring / Easing / math. No CSS transition, animation or
   @keyframes, no setTimeout / setInterval / requestAnimationFrame, no fetch or other network access, no eval.
4. {STYLE_KIND_RULES[kind]}
'../kit' gives: W, H, FILL, CLAMP, CAPTION_TOP, inksOf, noise(seed, x), clamp01, drawCover, luminance, stretch,
useOnceCanvas, interpolate, spring, Easing, Img, AbsoluteFill, theme, FONT, outline(px), slot(graphic, top).
WORKED EXAMPLES (the library's {kind}s; copy their care, not their look):
{examples}"""


def lint_style_code(code: str, kind: str) -> list[str]:
    """Rule breaks a compiler can't see in an AI-invented style component (see style_rules). Empty = clean."""
    found = [f"imports from '{mod}': import only from 'react', '../kit' and '../types'"
             for mod in re.findall(r"""\bfrom\s+['"]([^'"]+)['"]""", code) if mod not in ("react", "../kit", "../types")]
    checks = [(r"\brequire\s*\(|\bimport\s*\(", "loads code at run time (require/import()): use static imports from '../kit'"),
              (r"\btransition\s*:|\banimation\s*:|@keyframes", "CSS transition/animation doesn't render in Remotion: animate from t/p"),
              (r"\bsetTimeout\b|\bsetInterval\b|\brequestAnimationFrame\b", "timers don't render in Remotion: animate from t/p"),
              (r"\bfetch\s*\(|XMLHttpRequest|WebSocket|\beval\s*\(|new\s+Function\b", "no network access or eval")]
    found += [why for pattern, why in checks if re.search(pattern, code)]
    if not re.search(rf"export\s+const\s+{STYLE_SLOTS[kind]}\s*:\s*{STYLE_TYPES[kind]}\b", code):
        found.append(f"must export `export const {STYLE_SLOTS[kind]}: {STYLE_TYPES[kind]} = ...`")
    return found


def clean_style_code(raw, slot: str) -> str | None:
    """The code from an AI reply (code fences removed); None unless it exports the slot's component."""
    if not isinstance(raw, str) or not raw.strip():
        return None
    code = raw.strip()
    fence = re.search(r"```(?:tsx|typescript|ts|jsx|js)?\s*\n(.*?)```", code, re.S)
    code = fence.group(1).strip() if fence else code
    return code + "\n" if f"export const {slot}" in code else None


def invent_component(kind: str, spec: dict, short: dict, scene: dict, props: dict, work: Path) -> str:
    """The AI invents a new style component (`spec` = {title, brief, fallback}) for this Short and it goes into its
    slot in remotion/src/style/generated/: draft -> lint + compile (one repair) -> a small preview the AI looks at and
    fixes once -> cached in work/ (fix.bat reuses it). Returns "invented", or the spec's library fallback when it
    fails (the slot is emptied again)."""
    slot = STYLE_SLOTS[kind]
    target, cache = STYLE_DIR / "generated" / f"{slot}.tsx", work / f"{slot}.tsx"
    sig = f"// {slot}: {spec['title']} | {spec['brief'][:80]}"
    if cache.exists() and cache.read_text(encoding="utf-8", errors="ignore").startswith(sig):
        target.write_text(cache.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        return "invented"
    print(f'    inventing a new {kind} for this Short: "{spec["title"]}"...')
    base = f"""You are the motion designer of a vertical 1080x1920 YouTube Short: "{short.get('title')}". Invent a NEW {kind}
for it, written as a Remotion React/TypeScript component: "{spec['title']}": {spec['brief']}
It is used on: {json.dumps({k: scene.get(k) for k in ('start', 'end', 'graphic')}, ensure_ascii=False)}.
{style_rules(kind)}"""

    def attempt(code) -> list[str]:  # writes the slot and returns what is wrong (empty = it compiles and follows the rules)
        if not code:
            return ["no usable code (it must export the component)"]
        problems = lint_style_code(code, kind)
        if problems:
            return problems
        target.write_text(f"{sig}\n{code}", encoding="utf-8", newline="\n")
        err = tsc_check()
        return [err] if err else []

    data = ask_ai(base + '\nReply with ONLY JSON: {"code": "import React from \'react\';\\n..."}', fatal=False) or {}
    code = clean_style_code(data.get("code"), slot)
    problems = attempt(code)
    if problems:  # one repair with the exact complaints
        data = ask_ai(f"{base}\nYour code below was rejected:\n- " + "\n- ".join(problems)[:2000]
                      + f"\nCode:\n{code or data.get('code')}\nReply with ONLY JSON: {{\"code\": \"...\"}}", fatal=False) or {}
        code = clean_style_code(data.get("code"), slot)
        problems = attempt(code)
    if problems:
        print(f"      the invention didn't work ({str(problems[0])[:120]}): using the library's {spec['fallback']}")
        target.write_text(style_placeholders()[slot], encoding="utf-8", newline="\n")  # only this slot: others may hold inventions
        return spec["fallback"]
    sheet = preview_sheet(*style_preview(kind, scene, props), work)
    if sheet:  # look at it once as an art director, like the custom scenes
        data = ask_ai(f"""{base}
You wrote the code below. Open {sheet} and look at it: 8 frames across where it is used, left to right, top to
bottom. Check as a strict art director: does it look like the brief? is the picture still readable? is anything
broken, blank, glitchy, off-frame, or under the captions (y > 1150)? If it is good, reply {{"ok": true}}. If not,
list the problems and give the fixed code that still follows every rule.
Code:
{code}
Reply with ONLY JSON: {{"ok": false, "problems": ["..."], "code": "..."}}""", fatal=False, read_dir=sheet.parent) or {}
        fixed = clean_style_code(data.get("code"), slot) if data.get("ok") is False else None
        if fixed and not attempt(fixed):
            code = fixed
            print(f"      improved after a look: {'; '.join(str(x) for x in data.get('problems') or [])[:140]}")
        elif fixed:  # the rewrite failed: put back the version that already compiled
            target.write_text(f"{sig}\n{code}", encoding="utf-8", newline="\n")
        if (sheet.parent / "preview.mp4").exists():
            shutil.copy(sheet.parent / "preview.mp4", work / f"{slot}_preview.mp4")
    cache.write_text(f"{sig}\n{code}", encoding="utf-8", newline="\n")
    return "invented"


def style_preview(kind: str, scene: dict, props: dict) -> tuple[dict, float, float]:
    """(props, start, end) of a small preview where an invention is used: its scene, or 1 s around its cut."""
    scenes = props["scenes"]
    k = next((n for n, sc in enumerate(scenes) if sc is scene), 0)
    shown = scenes[max(0, k - 1):k + 1] if kind == "transition" else [scene]
    a, b = (scene["start"] - 0.5, scene["start"] + 0.5) if kind == "transition" else (scene["start"], scene["end"])
    return ({**props, "scenes": shown, "total": scene["end"] + 0.05, "words": [], "flashes": [], "hook": "", "cta": None},
            max(0.0, a), b)


def swap_inventions(props: dict, specs: dict) -> None:
    """Replaces every use of an invention in the Remotion props by its library fallback ({kind: spec})."""
    for sc in props["scenes"]:
        if "look" in specs and sc.get("look") == "invented":
            sc["look"] = specs["look"]["fallback"]
        if "transition" in specs and sc.get("transition") == "invented":
            sc["transition"] = specs["transition"]["fallback"]
        if "overlay" in specs and (sc.get("graphic") or {}).get("style") == "invented":
            sc["graphic"] = {**sc["graphic"], "style": specs["overlay"]["fallback"]}


def invent_styles(short: dict, props: dict, work: Path) -> dict:
    """Codes this Short's inventions (look / transition / overlay) into their slots; a failed one is swapped for its
    fallback in `props`. Returns {kind: spec} of the inventions in use."""
    look = short.get("look") or {}
    specs = {"look": look if look.get("name") == "invented" else None,
             "transition": short.get("invented_transition"), "overlay": short.get("invented_overlay")}
    used_on = {"look": lambda sc: sc.get("look") == "invented", "transition": lambda sc: sc.get("transition") == "invented",
               "overlay": lambda sc: (sc.get("graphic") or {}).get("style") == "invented"}
    used = {}
    for kind, spec in specs.items():
        scene = next((sc for sc in props["scenes"] if used_on[kind](sc)), None) if spec else None
        if scene is None:
            continue
        if invent_component(kind, spec, short, scene, props, work) == "invented":
            used[kind] = spec
        else:
            swap_inventions(props, {kind: spec})
    return used


CANDIDATES = ROOT / "style_candidates"  # inventions waiting for the owner (outside remotion/src: tsc never sees them)


def save_candidate(kind: str, title: str, brief: str, fits: str, code: str, preview: Path | None, short_title: str) -> Path:
    """Saves an invention that made it into a finished Short as a candidate for the library:
    style_candidates/<kind>-<name>/ with Component.tsx (exported under its own name), meta.json, preview.mp4."""
    base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:30].strip("-") or kind
    taken = {e["name"] for e in style_library()}
    name, n = base, 1
    while name in taken or any((CANDIDATES / f"{k}-{name}").exists() for k in STYLE_SLOTS):  # index.ts imports by name
        n += 1
        name = f"{base}-{n}"
    pascal = "".join(w.capitalize() for w in name.split("-"))
    pascal = pascal if pascal[:1].isalpha() else f"Style{pascal}"
    folder = CANDIDATES / f"{kind}-{name}"
    folder.mkdir(parents=True)
    (folder / "Component.tsx").write_text(code.replace(STYLE_SLOTS[kind], pascal), encoding="utf-8", newline="\n")
    (folder / "meta.json").write_text(json.dumps(
        {"name": name, "kind": kind, "component": pascal, "description": brief, "fits": fits, "title": title,
         "from_short": short_title, "made": time.strftime("%Y-%m-%d")}, indent=1, ensure_ascii=False), encoding="utf-8")
    if preview and preview.exists():
        shutil.copy(preview, folder / "preview.mp4")
    return folder


def approve_candidate(folder: Path) -> bool:
    """Adds a candidate to the library (component file, library.json entry, regenerated index.ts) if the project still
    compiles with it; otherwise everything is put back and the candidate stays. True when it joined the library."""
    meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
    rel = f"{meta['kind']}s/{meta['component']}.tsx"
    dest, index = STYLE_DIR / rel, STYLE_DIR / "index.ts"
    if dest.exists():
        return False
    before = {STYLE_LIBRARY: STYLE_LIBRARY.read_bytes(), index: index.read_bytes()}
    shutil.copy(folder / "Component.tsx", dest)
    lib = style_library() + [{"name": meta["name"], "kind": meta["kind"], "description": meta["description"],
                              "fits": meta["fits"], "file": rel, "origin": "approved"}]
    STYLE_LIBRARY.write_text(json.dumps(lib, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_style_index()
    try:
        err = tsc_check()
    except Exception as e:  # the check itself crashed or timed out: treat as a failure so nothing stays half-added
        err = str(e)
    if err:
        for f, data in before.items():
            f.write_bytes(data)
        dest.unlink(missing_ok=True)
        print(f"  It no longer works with the current library ({err[:160]}); nothing was changed.")
        return False
    shutil.rmtree(folder, ignore_errors=True)
    return True


def reject_candidate(folder: Path) -> None:
    shutil.rmtree(folder, ignore_errors=True)


def library_menu() -> None:
    """library.bat: the owner watches each invention the AI made for a Short and adds it to the library or throws it away."""
    folders = sorted(p for p in CANDIDATES.glob("*") if (p / "meta.json").exists()) if CANDIDATES.exists() else []
    if not folders:
        print("No new inventions are waiting. The AI saves one here when it invents a look, overlay or cut for a Short.")
        return
    kinds = {"look": "photo look", "overlay": "on-screen overlay", "transition": "scene change"}
    for k, folder in enumerate(folders, 1):
        meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
        print(f"\n{k}/{len(folders)}: a new {kinds[meta['kind']]}, \"{meta['title']}\" (made for \"{meta['from_short']}\")")
        print(f"  What it is: {meta['description']}")
        if (folder / "preview.mp4").exists():
            print("  Opening its preview...")
            os.startfile(folder / "preview.mp4")
        what = ask_number("1) Add it to the library (the AI may reuse it)  2) Throw it away  3) Decide later", 3, 3)
        if what == 1:
            print("  Added to the library." if approve_candidate(folder) else "  Kept for later.")
        elif what == 2:
            reject_candidate(folder)
            print("  Thrown away.")


def run_remotion_with_fallback(render, props: dict, used: dict) -> dict:
    """render(props); if it fails while AI inventions are in use, they are swapped for their library fallbacks and
    the render runs once more. Returns the inventions that made it into the video ({kind: spec})."""
    try:
        render(props)
        return used
    except Exception as e:
        if not used:
            raise
        print(f"    an invented style broke the render ({str(e)[:120]}): using the library fallbacks")
        restore_style_slots()
        swap_inventions(props, used)
        render(props)
        return {}


def redraw_custom(short: dict, i: int, slot: int, why: str, work: Path) -> bool:
    """The review saw custom scene i look wrong: its coder gets the complaint and its current code, rewrites it once,
    and the fix replaces the cached code (same signature line, so the re-render uses it). False = not fixed."""
    cached = work / f"Custom{slot}.tsx"
    if not cached.exists():
        return False
    sig, _, code = cached.read_text(encoding="utf-8").partition("\n")
    print(f"    redrawing the motion graphic of scene {i + 1} ({why[:80]})...")
    data = ask_ai(f"""You wrote the Remotion component `Custom{slot}` below for scene {i + 1} of the YouTube Short
"{short['title']}" (narration: {short['scenes'][i]['narration']!r}). The finished video was reviewed and this scene
looked wrong: {why!r}
Rewrite the component to fix exactly that.
{custom_rules(slot)}
Current code:
{code}
Reply with ONLY JSON: {{"code": "import React from 'react';\\n..."}}""", fatal=False)
    new = clean_tsx_code((data or {}).get("code"), slot)
    if not new or lint_custom_code(new):
        return False
    target = REMOTION / "src" / "full" / "generated" / f"Custom{slot}.tsx"
    before = target.read_text(encoding="utf-8") if target.exists() else None
    try:  # the check needs the code in the project; the project's own slot file is put back afterwards
        target.write_text(sig + "\n" + new, encoding="utf-8")
        if tsc_check() is not None:
            return False
    finally:
        if before is not None:
            target.write_text(before, encoding="utf-8")
    cached.write_text(sig + "\n" + new, encoding="utf-8")
    return True


def paint_instead(short: dict, work: Path, idx: list[int], images: list, sources: list[str]) -> set[str]:
    """Remotion failed: the full-screen motion graphic scenes get a painted picture (Gemini, else this PC) so the
    built-in renderer can still finish the Short. Returns the pictures Gemini made."""
    items = [{"prompt": short["scenes"][i]["ai_image"]
              or f"{short['scenes'][i].get('shot') or short['scenes'][i]['narration']} {PAINT_FALLBACK}",
              "out": str(work / f"ai{i}.jpg")} for i in idx]
    by_moss = moss_images(items, work)  # same painter order as render(): MOSS, Gemini, SDXL
    made = gemini_images([it for it in items if it["out"] not in by_moss], work) if shutil.which("agy") else set()
    rest = [it for it in items if it["out"] not in made | by_moss]
    if rest:
        local_job("images", rest, work, timeout=900)
    for i, it in zip(idx, items):
        short["scenes"][i]["full"] = None
        if Path(it["out"]).exists():
            for name in (f"{i}.jpg", f"{i}_raw.jpg"):
                shutil.copy(it["out"], work / name)
            to_vertical(work / f"{i}.jpg")
            images[i] = Image.open(work / f"{i}.jpg").convert("RGB")
            maker = ("by Gemini" if it["out"] in made else "on this PC (MOSS-Image)" if it["out"] in by_moss
                     else "on this PC (SDXL-Lightning)")
            sources[i] = f"AI-GENERATED {maker}: \"{it['prompt']}\" (painted instead of the motion graphic: Remotion failed)"
        else:
            sources[i] += " (the motion graphic could not be drawn because Remotion failed; this picture stands in)"
    return made


FIGURE_PROMPT = ("A single {thing}, full body in side view, drawn as one solid flat black ink silhouette on a plain pure "
                 "white background. No text, no ground, no shadow, no frame, nothing else in the picture; centered, a "
                 "simple clear shape that reads at a small size.")


def ink_silhouette(src: Path, dst: Path) -> bool:
    """A painted figure (dark ink on light paper) -> a cropped RGBA silhouette (dark ink, transparent paper, at most
    256 px) for the big-number scene. False when the painting has no clear single shape (blank, or mostly ink)."""
    with Image.open(src) as im:
        gray = ImageOps.autocontrast(im.convert("L"))
    ink = gray.point(lambda v: 255 if v < 110 else 0)  # alpha: dark = figure
    share = sum(ink.histogram()[255:]) / (ink.width * ink.height)
    box = ink.getbbox()
    if not box or not 0.02 <= share <= 0.6:
        return False
    ink = ink.crop(box).filter(ImageFilter.GaussianBlur(0.8))  # soft edge, no jaggies when scaled
    ink.thumbnail((256, 256))
    fig = Image.new("RGBA", ink.size, (20, 15, 10, 0))
    fig.putalpha(ink)
    fig.save(dst)
    return True


def make_paper(folder: Path = REMOTION / "public" / "paper") -> None:
    """The aged-paper texture and film-grain frames the full-screen motion graphics draw on (style A,
    "archival documentary"). Made once with Pillow, so no downloaded textures and no licences."""
    folder.mkdir(parents=True, exist_ok=True)
    if not (folder / "paper.jpg").exists():
        w, h = 1300, 2300
        rnd = random.Random(7)
        paper = Image.new("RGB", (w, h), hex_rgb("#eadcbf"))
        shade = Image.effect_noise((26, 46), 60).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40))
        paper = Image.composite(paper, Image.new("RGB", (w, h), hex_rgb("#cdb88f")), shade.point(lambda v: min(255, v + 70)))
        fibres = Image.effect_noise((w, h // 12), 35).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1))
        paper = Image.composite(paper, Image.new("RGB", (w, h), hex_rgb("#bfa77c")), fibres.point(lambda v: 255 if v > 90 else 200))
        stains = Image.new("L", (w, h), 0)
        d = ImageDraw.Draw(stains)
        for _ in range(3):
            x, y, r = rnd.randrange(w), rnd.randrange(h), rnd.randrange(120, 320)
            d.ellipse((x - r, y - r * 0.8, x + r, y + r * 0.8), outline=60, width=rnd.randrange(6, 14))
            d.ellipse((x - r, y - r * 0.8, x + r, y + r * 0.8), fill=18)
        paper = Image.composite(Image.new("RGB", (w, h), hex_rgb("#9c7d4c")), paper, stains.filter(ImageFilter.GaussianBlur(12)))
        paper.save(folder / "paper.jpg", quality=90)
    for k in range(6):
        if not (folder / f"grain{k}.png").exists():
            alpha = Image.effect_noise((1080, 1920), 50).point(lambda v: min(45, abs(v - 128) // 2))
            grain = Image.new("RGBA", (1080, 1920), (40, 28, 12, 0))
            grain.putalpha(alpha)
            grain.save(folder / f"grain{k}.png")


def render_remotion(short: dict, cues: list[dict], bounds: list[float], total: float,
                    words: list[tuple[float, float, str]], work: Path, emphasis: set[float],
                    flashes: set[float], clips: dict[int, Path], full_pics: dict[int, list] | None = None) -> Path:
    """Render the silent video (with captions) through the Remotion project; returns the mp4."""
    npx = shutil.which("npx")
    if not npx or not (REMOTION / "node_modules" / "remotion").exists():
        raise RuntimeError("Remotion isn't installed")
    job = REMOTION / "public" / "job"  # Remotion can only load images from its public folder
    shutil.rmtree(job, ignore_errors=True)
    job.mkdir(parents=True)
    make_paper()  # paper + grain for the full-screen motion graphics (made once)
    restore_style_slots()  # a run closed mid-invention may have left half-made code in a slot
    gen_dir = REMOTION / "src" / "full" / "generated"
    saved_gen = {p: p.read_text(encoding="utf-8") for p in gen_dir.glob("Custom*.tsx") if p.exists()}
    scenes, custom_slot = [], 0
    for i, sc in enumerate(short["scenes"]):
        shutil.copy(work / f"{i}.jpg", job / f"{i}.jpg")
        cue, card = cues[i], None
        if cue.get("card"):
            (job / f"card{i}.jpg").write_bytes(cue["photo"])
            card = {"image": f"job/card{i}.jpg", "name": sc["person"]["name"], "on": cue["on"], "off": cue["off"]}
        clip = None
        if i in clips:
            shutil.copy(clips[i], job / f"clip{i}.mp4")
            clip = {"src": f"job/clip{i}.mp4", "duration": duration(clips[i])}
        skin = short_skin(short, sc.get("full"))
        slot = min(3, custom_slot)
        if (sc.get("full") or {}).get("type") == "custom":
            custom_slot += 1
        scenes.append({"image": f"job/{i}.jpg", "start": bounds[i], "end": bounds[i + 1], "move": sc["move"],
                       **style_props(sc, i), "card": card, "clip": clip, "credit": sc.get("credit_tag"),
                       "full": full_props(sc, cue, i, (full_pics or {}).get(i), job, skin=skin, slot=slot),
                       "graphic": sc["graphic"] and {**sc["graphic"], "at": cue["graphic"], "pace": cue.get("map_pace", 1)}})
        if sc["graphic"] and sc["graphic"]["style"] == "mark":  # the card shows the original framing
            shutil.copy(work / f"{i}_raw.jpg", job / f"raw{i}.jpg")
            with Image.open(job / f"raw{i}.jpg") as im:
                scenes[-1]["graphic"].update(image=f"job/raw{i}.jpg", aspect=im.width / im.height)
    props = {"fps": FPS, "total": total, "xfade": XFADE, "hook": short["hook_text"], "palette": PALETTES[short["palette"]],
             "scenes": scenes, "flashes": sorted(flashes), "cta": cues[-1].get("cta"), "ctaLine": short["cta_line"],
             "words": [{"start": s, "end": e, "text": t, "emphasis": s in emphasis, "line": g}
                       for g, line in enumerate(caption_lines(words)) for s, e, t in line]}
    out = work / "remotion.mp4"

    def render(p: dict) -> None:
        (work / "props.json").write_text(json.dumps(p, ensure_ascii=False), encoding="utf-8")
        subprocess.run([npx, "remotion", "render", "src/index.ts", "Short", str(out),
                        f"--props={work / 'props.json'}", "--log=error",
                        # GPU drawing in Chrome, fewer tabs (RAM), and a quick high-quality intermediate
                        # encode: the final pass re-encodes it on the GPU.
                        "--gl=angle", "--concurrency=4", "--x264-preset=ultrafast", "--crf=14"],
                       cwd=REMOTION, check=True, timeout=3600)
    try:
        code_custom_scenes(short, scenes, work)
        # AI-invented looks/overlays/transitions; a broken one falls back to its library preset
        short["inventions"] = run_remotion_with_fallback(render, props, invent_styles(short, props, work))
    finally:
        shutil.rmtree(job, ignore_errors=True)
        for p, txt in saved_gen.items():
            p.write_text(txt, encoding="utf-8")
        restore_style_slots()
    return out


def look_text(short: dict) -> str:
    """Plain-English name of the Short's photo look for edit_plan.txt."""
    look = short.get("look") or {}
    if look.get("name") == "invented":
        return f'invented "{look["title"]}" ({look["brief"][:120]}; if it failed: {look["fallback"]})'
    return next((f"{e['name']} ({e['description']})" for e in style_library("look") if e["name"] == look.get("name")),
                str(look.get("name")))


def cut_text(short: dict, name: str, renderer: str) -> str:
    """Plain-English scene change for edit_plan.txt."""
    if name == "fade" or (name != "flash" and not renderer.startswith("Remotion")):
        return f"{XFADE}s crossfade" + ("" if name == "fade" else f" (planned: {name}; the built-in renderer can't draw that cut)")
    if name == "flash":
        return "camera-flash hard cut"
    if name == "invented":
        inv = short.get("invented_transition") or {}
        return f'invented "{inv.get("title")}" ({str(inv.get("brief"))[:100]}; if it failed: {inv.get("fallback")})'
    return next((e["description"] for e in style_library("transition") if e["name"] == name), name)


def picture_line(short: dict) -> str | None:
    """edit_plan.txt: what the pictures-first check found (None for a plan made before it)."""
    if not short.get("picture_check"):
        return None
    dropped = short.get("dropped_topics") or []
    return f"Pictures found before writing: {short['picture_check']}" + (f" (topics dropped: {'; '.join(dropped)})" if dropped else "")


def edit_plan(short: dict, bounds: list[float], sources: list[str], cues: list[dict],
              events: list[dict], music: Path | None, path: Path, renderer: str,
              clips: dict[int, Path]) -> None:
    """Timestamped edit decision list of exactly what was rendered, plus the sound-design cue sheet."""
    total = bounds[-1]
    lines = [f"EDIT PLAN: {short['title']}",
             f"Length {clock(total)} | 1080x1920 vertical | {FPS} fps | captions: up to 3 words (about 16 letters) per line, spoken word "
             "in yellow, emphasis word glows orange to the end of its line",
             f"Renderer: {renderer}",
             *([picture_line(short)] if picture_line(short) else []),
             f"Music: {music.stem if music else 'none'}{f' ({music.parent.name} mood)' if music and music.parent != MUSIC else ''} (ducked under the voice, fades out over the last 2s)",
             f"Colours: {short['palette']} palette (accent {PALETTES[short['palette']]['accent']}, "
             f"emphasis {PALETTES[short['palette']]['emphasis']}, map {PALETTES[short['palette']]['panel']})",
             "Photo look: " + (f"{look_text(short)} on scenes "
                               + ", ".join(str(k + 1) for k, sc in enumerate(short["scenes"]) if sc.get("look"))
                               if any(sc.get("look") for sc in short["scenes"]) else "none (plain pictures)"),
             f"Opening: hook title \"{short['hook_text']}\" 0:00.0-0:01.8"
             + (f" | hook lines considered: {' / '.join(short['hook_options'])}" if short["hook_options"] else ""),
             "Script editor: " + ("\n  ".join([""] + short["editor_notes"]) if short.get("editor_notes") else "none"),
             "Fact check (against the Wikipedia articles): "
             + ("\n  ".join([""] + short["fact_check"]) if short.get("fact_check") else "every line held up"),
             *([f"Fixed automatically after reviewing the finished video:\n  " + "\n  ".join(short["auto_fixed"])]
               if short.get("auto_fixed") else []),
             ""]
    for i, sc in enumerate(short["scenes"]):
        start, end = bounds[i], bounds[i + 1]
        lines.append(f"[{clock(start)} - {clock(end)}]  SCENE {i + 1}" + ("  (hook)" if i == 0 else ""))
        lines.append(f"  VO:      \"{sc['narration']}\"")
        if sc["shot"]:
            lines.append(f"  SHOT:    {sc['shot']}")
        lines.append(f"  MOTION GRAPHIC: {sources[i]}" if sc.get("full") else f"  IMAGE:   {sources[i]}")
        if sc.get("credit_tag"):
            lines.append(f"  CREDIT:  on-screen tag (bottom-left) \"{sc['credit_tag']}\"")
        if sc.get("full"):
            camera = "slow drift and push-in on old paper; each element lands on its spoken word"
        elif i in clips and clips[i].name.startswith("film"):
            camera = "REAL VIDEO FOOTAGE (one shot; a short shot plays slowed, credited on screen when required)"
        elif i in clips and clips[i].name.endswith("_veo.mp4"):
            camera = f"AI MOTION CLIP made by the owner in Google Flow (Veo): \"{sc['motion']}\""
        elif i in clips and clips[i].name.startswith("clip"):
            kind = ("people move gently, softened with grain to hide AI ghosting" if sc["motion_people"]
                    else "atmosphere only, people stay still")
            camera = f"AI MOTION CLIP made on this PC (LTX-Video, {kind}): \"{sc['motion']}\""
        else:
            camera = MOVE_NAMES[sc["move"]]
        lines.append(f"  CAMERA:  {camera}")
        g = sc["graphic"]
        if g:
            style = GRAPHIC_STYLES[g["style"]]
            if renderer.startswith("Remotion") and "lat" in g:
                style = f"animated map flying to {g['lat']:.2f}, {g['lon']:.2f} + pin drop, label"
            elif renderer.startswith("Remotion") and g["style"] == "date" and g["text"].isdigit():
                style = "date stamp (year counts up)"
            elif not renderer.startswith("Remotion") and g["style"] in REMOTION_ONLY:
                style = f"fact box (built-in renderer stand-in for a {GRAPHIC_STYLES[g['style']]})"
            elif g["style"] == "stat":
                style = f"dot grid, {g['value']:.0f} of {g['of']} light up," if "of" in g else f"counter ticks up to {g['value']:,.10g},"
            elif g["style"] == "timeline":
                style = f"timeline {g['start']} -> {g['end']}, gap label"
            elif g["style"] == "mark":
                style = f"photo card, {g['shape']} drawn at {g['x']:.0%} across / {g['y']:.0%} down, then push-in; label"
            if "from" in g and renderer.startswith("Remotion"):
                style = style.replace("+ pin drop", f"+ route line from {g['from']['text']} + pin drop")
            on_word = f" on \"{g['trigger']}\"" if "trigger" in g else ""
            is_map = g["style"] == "place" and g.get("lat") is not None and renderer.startswith("Remotion")
            low = " (lowered: the subject is at the top)" if g.get("low") and not is_map else ""
            lines.append(f"  GRAPHIC: {style} \"{g['text']}\" {clock(cues[i]['graphic'])}-{clock(end - 0.25)}{on_word}{low}")
        cue = cues[i]
        if cue.get("card"):
            lines.append(f"  PERSON:  photo card \"{sc['person']['name']}\" pops in {clock(cue['on'])}-"
                         f"{clock(cue['off'])} (background dims) | {cue['card_source']}")
        elif cue.get("card_note"):
            lines.append(f"  PERSON:  skipped ({cue['card_note']})")
        if cue.get("cta") is not None:
            lines.append(f"  CTA:     on-screen SUBSCRIBE button + \"{short['cta_line']}\" {clock(cue['cta'])}-{clock(end - 0.25)} (no voice)")
        if cue.get("emphasis") is not None:
            lines.append(f"  EMPHASIS: \"{sc['emphasis']}\" glows at {clock(cue['emphasis'])}")
        if i:
            lines.append(f"  CUT IN:  {cut_text(short, sc['transition'], renderer)} at {clock(start)}")
        if sc.get("look"):
            lines.append(f"  LOOK:    {look_text(short)}")
        sounds = [e for e in events if start <= e["t"] + (0.35 if e["sound"].startswith(("whoosh", "flash")) else 0) < end
                  and e["sound"] != "riser"]
        if sounds:
            lines.append("  SOUND:   " + "; ".join(f"{e['what']} @ {clock(e['t'])}" for e in sounds))
        lines.append("")
    lines.append("SOUND DESIGN CUE SHEET (time | sound file | volume | why)")
    lines += [f"  {clock(e['t'])}  {e['sound']:<9} {e['gain']:.2f}  {e['what']}" for e in events]
    path.write_text("\n".join(lines), encoding="utf-8")


# Map card (MapCard.tsx) at full speed: fly-in, pin and place name take MAP_FLY s; the name then stays readable
# MAP_HOLD s; the card starts leaving MAP_EXIT s before the scene ends (0.25 + its 0.22 s exit).
MAP_FLY, MAP_HOLD, MAP_EXIT = 1.8, 1.2, 0.47


# Seconds an overlay animates after it pops in (Cards.tsx, Extras.tsx, Graphics.tsx); it starts early enough to
# finish and hold before leaving (the Ghost Army "15 MILES" counter left at 13)
GRAPHIC_BUILD = {"stat": 1.25, "timeline": 1.35, "compare": 1.55, "date": 0.7}


def scene_cues(sc: dict, words: list[tuple[float, float, str]], start: float, end: float,
               i: int, found: tuple[bytes, str] | None) -> dict:
    """Timed extras for one scene: a person card (photo `found`) when their name is spoken,
    and when the emphasis word is spoken (caption glow), and when the graphic pops up."""
    cue = {"full": full_cues(sc["full"], words, start, end)} if sc.get("full") else {}
    if sc.get("sound") and spoken_at(words, sc["sound"]["word"]) is not None:
        cue["sound_at"] = start + spoken_at(words, sc["sound"]["word"])
    g = sc["graphic"]
    if g:  # on its trigger word, but early enough to finish animating
        t = spoken_at(words, g["trigger"]) if "trigger" in g else None
        build = 0.6 + 0.035 * len(g["text"]) if g["style"] == "quote" else GRAPHIC_BUILD.get(g["style"], 0.3)
        latest = end - (MAP_EXIT + MAP_FLY + MAP_HOLD if "lat" in g else max(1.2, build + 0.9))
        cue["graphic"] = max(start + 0.3, min(start + t - 0.1, latest)) if t is not None else start + 0.3
        if "lat" in g:  # a short scene plays the fly-in faster, so the place name still gets its hold (owner's report)
            cue["map_pace"] = round(min(1.0, max(0.4, (end - MAP_EXIT - MAP_HOLD - cue["graphic"]) / MAP_FLY)), 2)
    if sc["emphasis"]:
        t = spoken_at(words, sc["emphasis"])
        if t is not None:
            cue["emphasis"] = start + t
    pr = sc["person"]
    if pr:
        t = spoken_at(words, pr["trigger"])
        if t is None or not found:
            cue["card_note"] = f"no photo found for {pr['name']}" if t is not None else "name not heard in voice"
            return cue
        on = start + t - 0.1
        if i == 0:
            on = max(on, 1.9)  # don't cover the hook title
        off = min(on + 2.6, end - 0.15)
        if off - on < 1.2:
            on = max(start + 0.2, off - 1.2)
        if off - on >= 0.8:
            cue.update(card=person_card(found[0], pr["name"]), photo=found[0], on=on, off=off,
                       card_source=f"Wikimedia Commons, {found[2] or 'public domain'}: {found[1]}")
        else:
            cue["card_note"] = "scene too short for a person card"
    return cue


LOCAL_AI = ROOT / "local_ai"  # GPU worker (Kokoro voice, SDXL images, LTX video) in its own venv
# First painter (owner, 2026-10-21: testing its range; was after Gemini on 10-20): MOSS-Image in ComfyUI (D:\ComfyUI).
COMFY = "http://127.0.0.1:8188"
COMFY_PY = Path(r"D:\ComfyUI\.venv\Scripts\python.exe")
# The official negative plus garbled lettering (its test note was gibberish); real, quoted text stays allowed.
MOSS_NEGATIVE = "nsfw, worst quality, bad anatomy, watermark, jpeg artifact, gibberish text, illegible lettering"
MOSS_NO_TEXT = ", text, caption, title, letters, words, inscription, signature"
# Owner 2026-10-21: the paintings looked "way too AI" (glossy, cartoonish). Prompts now name a real period medium;
# this keeps MOSS off its default digital finish. PAINT_FALLBACK is the medium when a scene has no ai_image;
# PAINT_HANDMADE tells Gemini the same (it has no negative prompt).
PAINT_FALLBACK = ("Loose oil sketch on canvas board, thick visible brushstrokes, unfinished edges, muted earth colors, "
                  "soft natural daylight.")
PAINT_HANDMADE = ("Make it look hand-made in the medium the prompt names, with that medium's real marks (paper grain, "
                  "brushstrokes, ink lines, print dots), not a smooth glossy digital painting or a 3D render. The artwork fills "
                  "the whole frame edge to edge, with no border or paper margin.")
MOSS_AI_LOOK = (", 3d render, cgi, glossy plastic look, airbrushed, smooth digital painting, concept art, video game art, "
                "cartoon, oversaturated, lens flare, border, picture frame, paper margin, rounded corners")
# Owner's rule 2026-10-20: found pictures must not carry captions/logos, but AI paintings MAY show writing. Only
# quoted words, so the painter writes real text (MOSS and Gemini render quoted text exactly) instead of gibberish.
PAINT_TEXT_RULE = ("Any writing in the picture must be exactly the words in double quotes in this prompt; with no "
                   "quoted words, no writing. No logos or watermarks.")
# Main voice (owner's pick 2026-10-20, over OmniVoice and VoxCPM2): CosyVoice 3 in VoiceStudio, cloning aiden
# from a 10 s clip of his own Qwen voice, read as a documentary narrator. Needs the VoiceStudio app (D:).
VOICESTUDIO = "http://127.0.0.1:3900"
VOICESTUDIO_EXE = Path(r"D:\VoiceStudio\app\VoiceStudio.exe")
COSY_REF = LOCAL_AI / "voices" / "aiden_ref.wav"  # its words are in aiden_ref.txt
COSY_INSTRUCT = "Speak like a gripping documentary narrator, building suspense."
# Owner's pick 2026-10-21 for shorter Shorts, by ear from voice_speed_test/ (Mike: 36.0 s at 1.15, 31.9 s at 1.30)
COSY_SPEED = 1.30
# Backup voice (owner's pick 2026-10-18 over Chatterbox and Kokoro): Qwen3-TTS "aiden", no style instruction,
# in its own venv (qwen-tts pins transformers versions that would break gen.py). Then Kokoro, then Edge.
QWEN_SPEAKER = "aiden"
# Kokoro equivalents of the Edge voices the niche picker chooses from (US "a" / UK "b" voices).
KOKORO_VOICES = {"en-US-AndrewNeural": "am_michael", "en-US-BrianNeural": "am_fenrir",
                 "en-US-ChristopherNeural": "am_michael", "en-US-AvaMultilingualNeural": "af_heart",
                 "en-US-EmmaNeural": "af_bella", "en-GB-RyanNeural": "bm_george"}


def local_job(task: str, items: list[dict], work: Path, timeout: int,
              worker: str = "gen.py", venv: str = ".venv") -> list[dict] | None:
    """Run a batch on this PC's GPU through a local_ai worker (gen.py, or qwen_voice.py in qwen_venv).
    Returns the items (each with an "ok" flag), or None if the local setup is missing or crashed, so the
    caller can fall back."""
    py = LOCAL_AI / venv / "Scripts" / "python.exe"
    if not items or not py.exists():
        return None
    job = work / f"{task}_job.json"
    job.write_text(json.dumps({"task": task, "items": items}, ensure_ascii=False), encoding="utf-8")
    # Offline: never start a surprise multi-GB model download in the middle of a batch.
    env = {**os.environ, "HF_HOME": str(LOCAL_AI / "hf"), "HF_HUB_OFFLINE": "1", "PYTHONIOENCODING": "utf-8"}
    try:
        for attempt in (1, 2):  # a hard crash (LTX on 8 GB, 2026-10-21) leaves no "seconds"; the same job then worked
            proc = subprocess.run([str(py), str(LOCAL_AI / worker), str(job)], env=env, timeout=timeout,
                                  capture_output=True, text=True, encoding="utf-8", errors="replace")
            result = json.loads(job.read_text(encoding="utf-8"))
            if "seconds" in result or attempt == 2:
                break
            print(f"    local {task} worker crashed (exit {proc.returncode}): "
                  f"{(proc.stderr.strip().splitlines() or [''])[-1][:160]}; trying once more")
    except Exception as e:
        print(f"    local {task} failed ({type(e).__name__}), falling back")
        return None
    if result.get("error"):
        print(f"    local {task}: {result['error'][:160]}")
    done = sum(1 for it in result["items"] if it.get("ok"))
    print(f"    local {task}: {done}/{len(items)} done on the GPU in {result.get('seconds', '?')}s")
    return result["items"]


def voicestudio_up() -> bool:
    """VoiceStudio's backend answers, starting the app (and waiting up to 2 min) if it isn't running."""
    def up() -> bool:
        try:
            urllib.request.urlopen(VOICESTUDIO + "/health", timeout=3).read()
            return True
        except Exception:
            return False
    if up():
        return True
    if not VOICESTUDIO_EXE.exists():
        return False
    print("    starting VoiceStudio for the CosyVoice voice...")
    subprocess.Popen([str(VOICESTUDIO_EXE)])
    for _ in range(40):
        time.sleep(3)
        if up():
            return True
    return False


def voicestudio_unload() -> None:
    """Free VoiceStudio's GPU memory: the 8 GB card is needed next for SDXL, LTX and parallax."""
    try:
        loaded = json.loads(urllib.request.urlopen(VOICESTUDIO + "/model/loaded", timeout=10).read())["models"]
        for model_id in [m["id"] for m in loaded] + ["sidecars"]:
            req = urllib.request.Request(f"{VOICESTUDIO}/model/unload/{urllib.parse.quote(model_id, safe='')}",
                                         method="POST")
            try:
                urllib.request.urlopen(req, timeout=60).read()
            except urllib.error.HTTPError:  # nothing of that kind loaded
                pass
    except Exception as e:
        print(f"    couldn't unload VoiceStudio's models ({type(e).__name__}): close the app if the GPU runs out")


def local_voice(short: dict, ch: dict, work: Path) -> list[tuple[Path, list] | None]:
    """Voice every scene on the GPU: CosyVoice (aiden, documentary) for the whole Short, else Qwen (aiden),
    else Kokoro; per scene (wav, words) or None to fall back to Edge. A voice counts only if every scene worked,
    so one Short never mixes voices."""
    items = [{"text": sc["narration"], "seed": i, "out": str(work / f"{i}.wav")} for i, sc in enumerate(short["scenes"])]
    if COSY_REF.exists() and voicestudio_up():
        ref_text = COSY_REF.with_suffix(".txt").read_text(encoding="utf-8").strip()
        done = local_job("tts", [{**it, "engine": "cosyvoice", "ref": str(COSY_REF), "ref_text": ref_text,
                                  "instruct": COSY_INSTRUCT, "speed": COSY_SPEED} for it in items],
                         work, timeout=1200, worker="qwen_voice.py", venv="qwen_venv") or []
        voicestudio_unload()
        if done and all(it.get("ok") and it.get("words") for it in done):
            return [(Path(it["out"]), [tuple(w) for w in it["words"]]) for it in done]
        print("    CosyVoice failed: using Qwen (aiden)")
    items = [{**it, "speaker": QWEN_SPEAKER} for it in items]
    done = local_job("tts", items, work, timeout=900, worker="qwen_voice.py", venv="qwen_venv") or []
    if done and all(it.get("ok") and it.get("words") for it in done):
        return [(Path(it["out"]), [tuple(w) for w in it["words"]]) for it in done]
    print("    Qwen voice failed: using Kokoro")
    voice = ch.get("local_voice") or KOKORO_VOICES.get(ch["voice"], "am_michael")
    items = [{"text": sc["narration"], "voice": voice, "speed": 1.1, "out": str(work / f"{i}.wav")}
             for i, sc in enumerate(short["scenes"])]
    done = local_job("tts", items, work, timeout=600) or []
    return [(Path(it["out"]), [tuple(w) for w in it["words"]]) if it.get("ok") and it.get("words") else None
            for it in done] or [None] * len(items)


def gemini_images(items: list[dict], work: Path) -> set[str]:
    """Paint the AI images with Gemini (agy's built-in image generator, ~2 min each, 3 at a time) instead
    of SDXL on this PC. Returns the `out` paths made; anything missing falls back to SDXL."""
    def one(it: dict) -> str | None:
        if "gemini" in NO_QUOTA:
            return None
        folder = work / "gemini_img" / Path(it["out"]).stem
        shutil.rmtree(folder, ignore_errors=True)
        folder.mkdir(parents=True)
        out = run_agy(f"Generate one image: {it['prompt']}\nVertical 9:16 portrait format. {PAINT_HANDMADE} {PAINT_TEXT_RULE} Save the "
                      f"image in the folder {folder} as image.png, then reply with only the saved file path.",
                      folder, timeout=600, model=GEMINI_FALLBACK)
        made = [p for p in folder.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
        if not made and quota_exhausted(out or ""):
            NO_QUOTA.add("gemini")
            print("  Gemini has no credits/quota left for images: falling back to SDXL on this PC")
            return None
        try:
            Image.open(made[0]).convert("RGB").save(it["out"], quality=95)
            return it["out"]
        except (IndexError, OSError):
            return None

    if not items or "gemini" in NO_QUOTA:
        return set()
    print(f"  Gemini is painting {len(items)} AI image(s)...")
    with ThreadPoolExecutor(3) as pool:
        return {out for out in pool.map(one, items) if out}


def comfy_call(path: str, data: dict | None = None, timeout: int = 30):
    req = urllib.request.Request(COMFY + path, json.dumps(data).encode() if data is not None else None,
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read() or b"null")


def moss_graph(prompt: str, seed: int, width: int, height: int) -> dict:
    """Comfy-Org's official MOSS-Image text-to-image template (25 steps, CFG 2.5, er_sde, skip-layer guidance on
    layer 22), without its prompt upsampler: our prompts are already full scene descriptions."""
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "moss_image_sft_int8_convrot.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen3.5_9b_w4a8_gptq.safetensors", "type": "moss_image", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "flux2-vae_small.safetensors"}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["2", 0]}},
        # no quoted words = no writing: "engraving" alone made it print a gibberish plate caption (test 2026-10-20)
        "5": {"class_type": "CLIPTextEncode", "inputs": {"text": MOSS_NEGATIVE + MOSS_AI_LOOK + ("" if '"' in prompt else MOSS_NO_TEXT),
                                                         "clip": ["2", 0]}},
        "6": {"class_type": "SkipLayerGuidanceDiTSimple", "inputs": {"model": ["1", 0], "double_layers": "", "single_layers": "22",
                                                                     "start_percent": 0.0, "end_percent": 0.5}},
        "7": {"class_type": "EmptyFlux2LatentImage", "inputs": {"width": width, "height": height, "batch_size": 1}},
        "8": {"class_type": "KSampler", "inputs": {"model": ["6", 0], "positive": ["4", 0], "negative": ["5", 0],
                                                   "latent_image": ["7", 0], "seed": seed, "steps": 25, "cfg": 2.5,
                                                   "sampler_name": "er_sde", "scheduler": "simple", "denoise": 1.0}},
        "9": {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["3", 0]}},
        "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": "shortsmaker/paint"}},
    }


def moss_images(items: list[dict], work: Path) -> set[str]:
    """Paint on this PC with MOSS-Image in ComfyUI (owner's pick 2026-10-20 over SDXL-Lightning: follows the
    prompt far better, ~2 min a picture). Starts ComfyUI if needed, stops it again afterwards so its 7 GB text
    encoder leaves RAM and the GPU. Returns the `out` paths made; the rest fall back to SDXL."""
    if not items or not COMFY_PY.exists():
        return set()
    proc = log = None
    try:
        comfy_call("/system_stats", timeout=3)
    except Exception:
        log = open(work / "comfyui.log", "w", encoding="utf-8")
        proc = subprocess.Popen([str(COMFY_PY), "main.py", "--listen", "127.0.0.1", "--port", COMFY.rsplit(":", 1)[1],
                                 "--disable-auto-launch"], cwd=COMFY_PY.parents[2], stdout=log, stderr=subprocess.STDOUT)
        for _ in range(60):  # up to 3 min to start
            time.sleep(3)
            if proc.poll() is not None:
                break
            try:
                comfy_call("/system_stats", timeout=3)
                break
            except Exception:
                pass
    made = set()
    try:
        comfy_call("/system_stats", timeout=3)
        print(f"  MOSS-Image is painting {len(items)} AI image(s) on this PC (~2 min each)...")
        for it in items:
            seed = int(hashlib.md5(it["prompt"].encode()).hexdigest()[:8], 16)  # same prompt, same picture on a re-render
            try:
                pid = comfy_call("/prompt", {"prompt": moss_graph(it["prompt"], seed, it.get("width", 768),
                                                                  it.get("height", 1344))})["prompt_id"]
                for _ in range(300):  # up to 10 min
                    time.sleep(2)
                    hist = comfy_call(f"/history/{pid}").get(pid)
                    if hist:
                        break
                pic = ((hist or {}).get("outputs", {}).get("10") or {}).get("images") or []
                if not pic:
                    print(f"    MOSS-Image failed on {Path(it['out']).name}: {json.dumps((hist or {}).get('status'))[:200]}")
                    continue
                q = urllib.parse.urlencode({k: pic[0][k] for k in ("filename", "subfolder", "type")})
                Image.open(io.BytesIO(urllib.request.urlopen(f"{COMFY}/view?{q}", timeout=60).read())).convert("RGB") \
                    .save(it["out"], quality=95)
                made.add(it["out"])
            except Exception as e:
                print(f"    MOSS-Image failed on {Path(it['out']).name} ({type(e).__name__})")
        comfy_call("/free", {"unload_models": True, "free_memory": True})
    except Exception as e:
        print(f"  MOSS-Image unavailable ({type(e).__name__}): painting with SDXL instead")
    finally:
        if proc:  # we started it: stop it, so the next GPU job gets all the memory
            proc.terminate()
            proc.wait(timeout=60)
            log.close()
    return made


def cover_crop(src: Path, out: Path) -> None:
    """Fill a 9:16 frame with the picture (centre crop), for the AI video model's start frame."""
    ImageOps.fit(Image.open(src).convert("RGB"), (W, H), Image.LANCZOS).save(out, quality=95)


# AI clips of moving people still ghost a little (smeared hands and faces in the background): a soft,
# grainy "old footage" finish hides it (owner's request). Atmosphere clips look clean and stay sharp.
PEOPLE_CLIP_VF = "scale=232:-2,scale=512:896:flags=bicubic,gblur=sigma=1.1,noise=alls=14:allf=t+u,vignette=PI/5"


def motion_prompt(sc: dict) -> str:
    """Image-to-video prompt for an animate scene (LTX on this PC, or Veo in Flow by the owner)."""
    return (f"{sc['motion']}. Gentle, slow, realistic motion, steady camera, consistent with the original photograph. "
            + ("People move slowly and naturally; bodies, faces and hands stay realistic and intact."
               if sc["motion_people"] else  # atmosphere: keep everyone still
               "People, animals and machines stay completely still; only the air, water, smoke or light moves."))


VEO_HANDOFF = False  # run.bat question: the owner makes the AI clips in Google Flow (Veo, AI Pro credits)


def veo_handoff(short: dict, work: Path, bounds: list[float], marked: list[int]) -> dict[int, Path]:
    """Pause the batch: write each animate scene's start picture + Veo prompt to <Short>/veo, open it, wait
    while the owner makes the clips in Google Flow by hand (no automation of Google's apps: account ToS), then
    take whichever scene<N>.mp4 files are there. Scenes left without a file fall back to LTX."""
    folder = work.parent / "veo"
    folder.mkdir(exist_ok=True)
    notes = ["Make these clips in Google Flow (labs.google/flow), then come back to the black window and press Enter.",
             "For each scene: Frames to Video -> upload the start picture -> paste the prompt -> portrait 9:16,",
             "Veo Fast (cheapest credits) -> download -> save it in this folder with the name shown.",
             "Skip any scene you like (no credits left, or Veo refuses it): this PC's AI video fills it in.", ""]
    for i in marked:
        sc = short["scenes"][i]
        if sc.get("shot", "").startswith("CLOSE-UP:"):
            continue
        cover_crop(work / f"{i}_raw.jpg", folder / f"start{i + 1}.jpg")
        notes += [f"SCENE {i + 1}{'  (the hook: if you only make one, make this one)' if i == 0 else ''}",
                  f"  Start picture: start{i + 1}.jpg    Save as: scene{i + 1}.mp4    "
                  f"(about {bounds[i + 1] - bounds[i]:.0f} s of it is used)",
                  f"  Prompt: {motion_prompt(short['scenes'][i])} Vertical 9:16. No text, no captions, no music.", ""]
    (folder / "prompts.txt").write_text("\n".join(notes), encoding="utf-8")
    os.startfile(folder)
    os.startfile(folder / "prompts.txt")
    input(f"\n  >> {len(marked)} AI clip(s) to make in Google Flow: see {folder / 'prompts.txt'}\n"
          "  >> Save them in that folder, then press Enter here (skipped ones are made on this PC). ")
    got = {}
    for i in marked:
        src = next((p for p in sorted(folder.glob(f"scene{i + 1}.*")) if p.suffix.lower() in (".mp4", ".mov", ".webm")), None)
        if not src:
            continue
        out = work / f"clip{i}_veo.mp4"  # "clip*" name: counts as AI for the synthetic-content label
        try:  # fill the vertical frame, drop Veo's own sound, keep only what the scene needs
            ffmpeg("-i", str(src), "-t", f"{bounds[i + 1] - bounds[i] + XFADE:.2f}", "-vf", FILL_VF, "-an",
                   "-r", str(FPS), *video_encoder(), out.name, cwd=work)
            got[i] = out
        except subprocess.CalledProcessError:
            print(f"    scene {i + 1}: couldn't read {src.name}, this PC makes that clip instead")
    print(f"  using {len(got)} Veo clip(s) from Flow")
    return got


def local_clips(short: dict, work: Path, sources: list[str], bounds: list[float],
                films: dict[int, dict]) -> dict[int, Path]:
    """Real motion for every scene with a picture: scenes Claude matched to archival film play that
    footage; the scenes it marked become AI video (LTX-Video, on this PC's GPU, or Veo by the owner). Every
    other scene gets the renderer's slow zoom/pan on the full-screen still (2.5D parallax was dropped: its
    depth warp bent paintings and buildings)."""
    usable = [i for i in range(len(short["scenes"]))
              if not sources[i].startswith("PLAIN") and (work / f"{i}_raw.jpg").exists()]
    clips: dict[int, Path] = {}
    for i, f in films.items():
        out, need = work / f"film{i}.mp4", bounds[i + 1] - bounds[i] + XFADE
        a, b = shot_span(f["path"], f["offset"])
        if b - a >= need / 2:  # stay inside the picked shot; a short one plays in slow motion (down to half speed)
            length = min(need, b - a)
            start = min(max(a, f["offset"] - 1), b - length)
        else:  # shot too short to stretch: real speed from just before the picked moment
            length, start = need, max(0.0, f["offset"] - 1)
        try:
            ffmpeg("-ss", f"{start:.2f}", "-i", str(f["path"]), "-t", f"{length:.2f}", "-vf", FILL_VF if fills_frame(f["path"]) else FILM_VF, "-r", str(FPS),
                   *video_encoder(), out.name, cwd=work)
            clips[i] = out
        except subprocess.CalledProcessError:
            print(f"    scene {i + 1}: couldn't cut the film clip, using its still instead")
    marked = [i for i in usable if short["scenes"][i]["animate"] and i not in clips]
    for i in marked:  # Veo clips the owner made in Flow earlier (a fix.bat re-render keeps them)
        if (work / f"clip{i}_veo.mp4").exists():
            clips[i] = work / f"clip{i}_veo.mp4"
    marked = [i for i in marked if i not in clips]
    if VEO_HANDOFF and marked:
        clips.update(veo_handoff(short, work, bounds, marked))
        marked = [i for i in marked if i not in clips]
    if marked:
        print(f"  animating {len(marked)} scenes with AI video on this PC (a few minutes)...")
        for i in marked:
            cover_crop(work / f"{i}_raw.jpg", work / f"{i}_9x16.jpg")
        items = [{"image": str(work / f"{i}_9x16.jpg"), "out": str(work / f"clip{i}.mp4"), "seed": i, "frames": 97,
                  "prompt": motion_prompt(short["scenes"][i])} for i in marked]
        done = local_job("video", items, work, timeout=3600) or []
        clips.update({i: Path(it["out"]) for i, it in zip(marked, done) if it.get("ok") and Path(it["out"]).exists()})
        for i in [i for i in marked if i in clips and short["scenes"][i]["motion_people"]]:
            soft = work / f"clip{i}_soft.mp4"  # still named clip*: counts as AI for the synthetic-content label
            try:
                ffmpeg("-i", clips[i].name, "-vf", PEOPLE_CLIP_VF, *video_encoder(), "-pix_fmt", "yuv420p", soft.name, cwd=work)
                clips[i] = soft
            except subprocess.CalledProcessError:
                print(f"    scene {i + 1}: couldn't soften the AI clip, using it as made")
    return clips


KEEP_WORK_DAYS = 7  # a finished Short keeps its work/ folder this long, so fix.bat can re-render one scene
AUTO_REPAINT_MAX = 4  # scenes the automatic review may repaint per fix round
AUTO_FIX_ROUNDS = 3  # review -> fix -> re-render rounds after the first render (each ~1 AI review + a render)


def save_state(work: Path, short: dict, choices: list[dict], music: Path | None, by_gemini: set[str]) -> None:
    """What a fix re-render needs to reproduce this Short without new AI picks: the final plan, the chosen
    pictures (bytes as files) and the music."""
    rows = []
    for i, c in enumerate(choices):
        row = {k: v for k, v in c.items() if k not in ("bg", "person", "full_pics")}
        for kind in ("bg", "person"):
            row[kind] = None
            if c[kind]:
                (work / f"keep_{i}_{kind}.bin").write_bytes(c[kind][0])
                row[kind] = [c[kind][1], c[kind][2]]
        if c.get("full_pics"):  # evidence-board photos / document scan
            for k, p in enumerate(c["full_pics"]):
                (work / f"keep_{i}_full{k}.bin").write_bytes(p[0])
            row["full_pics"] = [list(p[1:]) for p in c["full_pics"]]
        rows.append(row)
    short = {k: v for k, v in short.items() if k != "research"}  # Wikipedia text: re-read when needed
    (work / "state.json").write_text(json.dumps({"short": short, "choices": rows, "music": music.relative_to(MUSIC).as_posix() if music else None,
                                                 "by_gemini": sorted(by_gemini)}, default=str), encoding="utf-8")


def load_state(work: Path) -> dict:
    st = json.loads((work / "state.json").read_text(encoding="utf-8"))
    for i, row in enumerate(st["choices"]):
        for kind in ("bg", "person"):
            if row[kind]:
                row[kind] = ((work / f"keep_{i}_{kind}.bin").read_bytes(), *row[kind])
        if row.get("film"):
            row["film"]["path"] = Path(row["film"]["path"])
        if row.get("full_pics"):
            row["full_pics"] = [((work / f"keep_{i}_full{k}.bin").read_bytes(), *p) for k, p in enumerate(row["full_pics"])]
    return st


def prune_work() -> None:
    for w in OUTPUT.glob("*/*/work"):
        if time.time() - w.stat().st_mtime > KEEP_WORK_DAYS * 86400:
            shutil.rmtree(w, ignore_errors=True)


# Background music level before ducking. The tracks range from -9 to -28 LUFS, so the old fixed volume (0.22) buried
# Thinking Music (-22) under Mike's narration (owner: "no background audio"). The ducking takes ~10 dB more under
# the near-constant voice: -25 here puts the music ~21 dB under a -14.7 LUFS voice (-30 left it 26 dB under, faint).
MUSIC_LUFS = -25.0


def music_gain(track: Path) -> float:
    """Volume factor that brings this track's loudness (first 60 s) to MUSIC_LUFS; 0.22 if it can't be measured."""
    out = subprocess.run(["ffmpeg", "-hide_banner", "-t", "60", "-i", str(track), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    found = re.findall(r"^\s+I:\s+(-?[\d.]+) LUFS", out, re.M)
    if not found or float(found[-1]) < -70:  # unmeasurable or silent
        return 0.22
    return min(4.0, 10 ** ((MUSIC_LUFS - float(found[-1])) / 20))


def render(short: dict, ch: dict, folder: Path, state: dict | None = None, fix_round: int = 0) -> None:
    """Make one Short. With `state` (fix.bat or an automatic fix round), reuse its pictures and music instead of
    new AI picks. `fix_round` counts the automatic review-and-fix re-renders (up to AUTO_FIX_ROUNDS)."""
    global YELLOW, EMPHASIS
    work = folder / "work"
    work.mkdir(parents=True, exist_ok=True)
    all_words, bounds, images, sources, cues, audio = [], [0.0], [], [], [], []
    short["cta_line"] = ch.get("cta_line") or "for more stories like this"
    if short.get("palette") not in PALETTES:  # planner gave none (or an old plan): a random one
        short["palette"] = random.choice(list(PALETTES))
    YELLOW, EMPHASIS = (hex_rgb(PALETTES[short["palette"]][k]) for k in ("accent", "emphasis"))
    if state:
        choices = state["choices"]
    else:
        choices = choose_images(short, work, ch)
        # real footage first, then a full-screen motion graphic, and only then an AI painting
        weak = [i for i, c in enumerate(choices) if not c["bg"] and not short["scenes"][i].get("full")]
        rescue_graphics(short, weak, {i: "no fitting picture was found" for i in weak})
        mark_details(short, choices, work)
    for i, sc in enumerate(short["scenes"]):  # an evidence board needs its real photos (3 or more)
        if (sc.get("full") or {}).get("type") == "board" and len(choices[i].get("full_pics") or []) < 3:
            sc["full"] = None
    print("  voice, gap images and thumbnail art on this PC...")
    voices = local_voice(short, ch, work)
    gen = [{"prompt": sc["ai_image"], "out": str(work / f"ai{i}.jpg")}
           for i, sc in enumerate(short["scenes"]) if not choices[i]["bg"] and sc["ai_image"] and not sc.get("full")]
    figs = {i: sc["full"]["thing"] for i, sc in enumerate(short["scenes"])
            if (sc.get("full") or {}).get("type") == "number" and sc["full"].get("thing") and not sc["full"].get("compare")}
    gen += [{"prompt": FIGURE_PROMPT.format(thing=thing), "out": str(work / f"figraw{i}.jpg")} for i, thing in figs.items()]
    if short["thumbnail_prompt"]:
        gen.append({"prompt": short["thumbnail_prompt"], "out": str(work / "thumb_art.jpg")})
    have = {it["out"] for it in gen if Path(it["out"]).exists()}  # a fix re-render keeps the pictures already painted
    gen = [it for it in gen if it["out"] not in have]
    by_gemini = set(state["by_gemini"]) if state else set()
    # Painter order (owner, 2026-10-21, to test MOSS's range): MOSS-Image on this PC, then Gemini, then SDXL
    by_moss = moss_images(gen, work)
    by_gemini |= gemini_images([it for it in gen if it["out"] not in by_moss], work) if shutil.which("agy") else set()
    rest = [it for it in gen if it["out"] not in by_gemini | by_moss]
    generated = have | by_gemini | by_moss | {it["out"] for it in (local_job("images", rest, work, timeout=900) if rest else None) or []
                                              if it.get("ok")}
    for i in figs:  # the counted thing as a figure; a failed or messy painting leaves the built-in icon
        fig, raw = work / f"fig{i}.png", work / f"figraw{i}.jpg"
        if fig.exists() or (raw.exists() and ink_silhouette(raw, fig)):
            short["scenes"][i]["full"]["figure"] = str(fig)
    for i, sc in enumerate(short["scenes"]):
        print(f"  scene {i + 1}/{len(short['scenes'])}: image + voice")
        sc["credit_tag"] = None
        img, ai = work / f"{i}.jpg", work / f"ai{i}.jpg"
        if choices[i]["bg"]:  # film scenes play the clip; their still only stands in if the cut fails
            img.write_bytes(choices[i]["bg"][0] if choices[i].get("film") else clean_photo(choices[i]["bg"][0]))
            shutil.copy(img, work / f"{i}_raw.jpg")  # original framing, for the GPU camera moves
            to_vertical(img)
            film, site, credit = choices[i].get("film"), choices[i].get("site", "Wikimedia Commons"), choices[i]["bg"][2]
            licence = credit or ("Pixabay license, no credit needed" if site == "Pixabay" else "public domain")
            source = (f"{site}, {licence}: {choices[i]['bg'][1]}"
                      + (f" (real film from {clock(film['t'])})" if film else ""))
            if credit:  # a short tag on screen while it shows; the full credit goes in upload.txt
                sc["credit_tag"] = short_credit(credit, film=bool(film))
        elif str(ai) in generated:  # no real photo fit: AI image made on this PC
            shutil.copy(ai, img)
            shutil.copy(ai, work / f"{i}_raw.jpg")
            to_vertical(img)
            # a fix re-render keeps earlier paintings without knowing which local painter made them
            maker = ("by Gemini" if str(ai) in by_gemini else "on this PC (MOSS-Image)" if str(ai) in by_moss
                     else "on this PC")
            source = f"AI-GENERATED {maker}: \"{sc['ai_image']}\""
        elif i:  # reuse an earlier image; its different camera move keeps it from looking repeated
            print("    no fitting image, reusing an earlier one")
            k = random.randrange(i)
            shutil.copy(work / f"{k}.jpg", img)
            shutil.copy(work / f"{k}_raw.jpg", work / f"{i}_raw.jpg")
            source = f"reused from scene {k + 1} (nothing fit \"{sc['image_search']}\")"
            sc["credit_tag"] = short["scenes"][k]["credit_tag"]
        else:
            print("    no fitting image, using a plain frame")
            Image.new("RGB", (int(W * SRC), int(H * SRC)), (18, 18, 24)).save(img)
            source = f"PLAIN FRAME (nothing fit \"{sc['image_search']}\"), replace before uploading"
        if sc.get("full"):  # drawn by Remotion instead of the picture (the picture stays as a fallback)
            pics = choices[i].get("full_pics") or []
            credited = [p for p in pics if p[2]]
            sc["credit_tag"] = None
            if credited:
                sc["credit_tag"] = short_credit(credited[0][2]) + (f" +{len(credited) - 1}" if len(credited) > 1 else "")
            source = (f"{full_summary(sc['full'])} ("
                      + (f"rescued: {sc['full_rescued']}" if sc.get("full_rescued") else "planned") + ")"
                      + "".join(f" | photo: {p[3]}, {p[2] or 'public domain'}: {p[1]}" for p in pics))
        if choices[i].get("plan_note"):
            source += f" | {choices[i]['plan_note']}"
        sources.append(source)
        if voices[i]:
            sound, words = voices[i]
        else:  # local voice unavailable: Microsoft's free Edge voice
            sound = work / f"{i}.mp3"
            words = speak(sc["narration"], ch["voice"], sound)
        if i == 0 and words and words[0][0] > 0.1:  # speak on the first frame: trim the voice's lead-in silence
            cut = words[0][0] - 0.05
            trimmed = work / f"0_start{sound.suffix}"
            ffmpeg("-ss", f"{cut:.3f}", "-i", str(sound), trimmed.name, cwd=work)
            sound, words = trimmed, [(a - cut, b - cut, w) for a, b, w in words]
        audio.append(sound)
        all_words += [(s + bounds[-1], e + bounds[-1], t) for s, e, t in words]
        bounds.append(bounds[-1] + duration(sound))
        images.append(Image.open(img).convert("RGB"))
        cues.append(scene_cues(sc, words, bounds[-2], bounds[-1], i, choices[i]["person"]))
    total = bounds[-1] + 0.6  # small tail so the last word isn't clipped
    bounds[-1] = total
    cues[-1]["cta"] = max(bounds[-2] + 0.3, total - 3.0)  # silent subscribe button: keeps the rewatch loop
    clips = local_clips(short, work, sources, bounds, {i: c["film"] for i, c in enumerate(choices)
                                                         if c.get("film") and not short["scenes"][i].get("full")})
    for i, sc in enumerate(short["scenes"]):  # keep text callouts off the subject's face (maps and marks are full cards)
        if sc["graphic"] and sc["graphic"]["style"] != "mark":
            film = choices[i]["film"]["path"] if clips.get(i) == work / f"film{i}.mp4" else None
            sc["graphic"]["low"] = graphic_low(choices[i], work / f"{i}_raw.jpg", film)
    (work / "list.txt").write_text("".join(f"file '{a.name}'\n" for a in audio))
    ffmpeg("-f", "concat", "-i", "list.txt", "-ar", "44100", "-ac", "2", "voice.wav", cwd=work)
    emphasis = {c["emphasis"] for c in cues if c.get("emphasis") is not None}
    flashes = {bounds[i] for i, sc in enumerate(short["scenes"]) if sc["transition"] == "flash"}
    captions(all_words, work / "captions.ass", emphasis)
    srt(all_words, folder / "captions.srt")
    if not all((SFX / f"{name}.wav").exists() for name in SFX_FILES):
        make_sfx()

    # Renderer: Remotion when the plan is graphics-heavy (animated maps, spring motion), otherwise the
    # faster built-in Python renderer. Remotion failing never loses the Short: it falls back.
    renderer, n_graphics, video_in = "python", graphics_count(short, cues), ["-f", "rawvideo", "-pix_fmt", "rgb24",
                                                                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if wants_remotion(short["scenes"], n_graphics):
        print(f"  rendering with Remotion ({n_graphics} motion graphics)...")
        try:
            video_in = ["-i", str(render_remotion(short, cues, bounds, total, all_words, work, emphasis, flashes,
                                                  clips, {i: c.get("full_pics") for i, c in enumerate(choices)}))]
            renderer = "remotion"
            for kind, spec in ({} if state else short.get("inventions") or {}).items():  # once, on the first render
                slot = STYLE_SLOTS[kind]
                folder_c = save_candidate(kind, spec["title"], spec["brief"], f'stories like "{short["title"]}"',
                                          (work / f"{slot}.tsx").read_text(encoding="utf-8"), work / f"{slot}_preview.mp4",
                                          short["title"])
                print(f"    the invented {kind} \"{spec['title']}\" is waiting for your OK in library.bat ({folder_c.name})")
        except Exception as e:
            print(f"    Remotion failed ({e}), using the built-in renderer")
            full = [i for i, sc in enumerate(short["scenes"]) if sc.get("full")]
            if full:
                print(f"    painting {len(full)} scene(s) that were full-screen motion graphics...")
                by_gemini |= paint_instead(short, work, full, images, sources)

    # Audio: voice + music ducked under the voice + the sound-design cue sheet.
    tracks = sorted(MUSIC.rglob("*.mp3"))  # music/<mood>/*.mp3; the planner picks the Short's mood
    fitting = [t for t in tracks if t.parent.name == short.get("music_mood")]
    music = random.choice(fitting or tracks) if tracks else None
    if state and state.get("music") and (MUSIC / state["music"]).exists():
        music = MUSIC / state["music"]
    for i, sc in enumerate(short["scenes"]):  # the story's own sounds: owner's file, else fetched once from Freesound
        if sc.get("sound") and not sc["sound"].get("file"):
            found = story_sound(sc["sound"]["sound"])
            if found:
                sc["sound"]["file"] = found.relative_to(SFX).as_posix()
            else:
                print(f"    no sound found for \"{sc['sound']['sound']}\" (scene {i + 1}), skipping it")
                sc["sound"] = None
    events = sfx_events(short, cues, bounds, renderer == "remotion")
    fmt = "aformat=sample_rates=44100:channel_layouts=stereo"
    graph = ["[0:v]null[v]" if renderer == "remotion" else "[0:v]subtitles=captions.ass[v]",  # Remotion draws its own captions
             f"[1:a]{fmt},asplit=2[voice][key]" if music else f"[1:a]{fmt}[voice]"]
    mix = ["[voice]"]
    inputs = ["-i", "voice.wav"]
    if music:
        inputs += ["-stream_loop", "-1", "-i", str(music)]
        graph += [f"[2:a]{fmt},volume={music_gain(music):.4f},afade=t=in:d=0.1,afade=t=out:st={total - 2:.2f}:d=2[m]",
                  "[m][key]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=400[music]"]
        mix.append("[music]")
    for e in events:
        k = 1 + inputs.count("-i")  # ffmpeg input index; input 0 is the video
        src = SFX / e["sound"]
        inputs += ["-i", str(src if src.suffix else src.with_suffix(".wav"))]
        graph.append(f"[{k}:a]{fmt},volume={e['gain']},adelay={int(e['t'] * 1000)}:all=1[s{k}]")
        mix.append(f"[s{k}]")
    graph.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0,"
                 "loudnorm=I=-14:TP=-1.5:LRA=11,"  # -14 LUFS = YouTube's playback level
                 # one-pass loudnorm overshoots (an Atari Short peaked at -0.1 dB): a 4x-oversampled limiter
                 # also catches in-between peaks, so the AAC file stays under -1.5 dB (tested: -1.8)
                 "aresample=176400,alimiter=limit=0.79:level=false,aresample=44100[a]")

    if renderer == "python":
        print("  rendering video...")
    proc = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", *video_in, *inputs,
         "-filter_complex", ";".join(graph), "-map", "[v]", "-map", "[a]",
         *video_encoder(), "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.2f}", "-movflags", "+faststart",
         "../short.mp4"], stdin=subprocess.PIPE if renderer == "python" else None, cwd=work)
    if renderer == "python":
        frame = frame_maker(images, short["scenes"], short["hook_text"], short["cta_line"], bounds, cues, clips)
        write_frames(frame, len(images), bounds, total, proc.stdin, flashes)
        frame.close()
        proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed while rendering")
    storyboard(folder / "short.mp4", bounds, folder / "storyboard.jpg")
    edit_plan(short, bounds, sources, cues, events, music, folder / "edit_plan.txt",
              f"{'Remotion' if renderer == 'remotion' else 'built-in (Python)'}, {n_graphics} motion graphics",
              clips)
    issues = quality_check(folder / "short.mp4", bounds, sources)
    print(f"  {BRAIN.capitalize()} is watching the finished Short for problems...")
    found, fixes = visual_review(folder / "short.mp4", short, bounds, sources, work)
    issues += found
    print("  quality check: " + (f"{len(issues)} thing(s) to look at before uploading:" if issues else "OK, nothing to fix"))
    for issue in issues:
        print(f"    CHECK: {issue}")
    with open(folder / "edit_plan.txt", "a", encoding="utf-8") as f:
        f.write("\n\nQUALITY CHECK (automatic, on the finished video)\n" + ("\n".join(f"  CHECK: {i}" for i in issues) or
                "  OK: no black or frozen stretches, loudness on target, every scene has a picture") + "\n")

    art = work / "thumb_art.jpg"  # Claude's thumbnail plan, painted on this PC; else the first scene
    thumbnail(art if art.exists() else work / "0.jpg", short.get("thumbnail_text", short["title"]),
              folder / "thumbnail.jpg")
    synthetic = any(c.name.startswith("clip") for c in clips.values()) or any(s.startswith("AI-GENERATED") for s in sources)
    credit = music.with_name(music.name + ".txt") if music else None
    credit_text = f"\n\nMusic:\n{credit.read_text(encoding='utf-8').strip()}" if credit and credit.exists() else ""
    image_credits = []  # credited material (CC, Internet Archive, Openverse); public domain needs nothing
    for sc, c in zip(short["scenes"], choices):
        for _, title, who, site in (c.get("full_pics") or []) if sc.get("full") else []:
            if who:
                image_credits.append(f"{re.sub(r'[.](jpe?g|png|tiff?|gif|svg)$', '', title.removeprefix('File:'), flags=re.I)} by {who} ({site})")
        for kind in ("bg", "person"):
            if c[kind] and c[kind][2] and not (kind == "bg" and sc.get("full")):
                name = re.sub(r"\.(jpe?g|png|tiff?|gif|webm|ogv|svg)$", "", c[kind][1].removeprefix("File:"), flags=re.I)
                site = c.get("site", "Wikimedia Commons") if kind == "bg" else "Wikimedia Commons"
                image_credits.append(f"{name} by {c[kind][2]} ({site})")
    if image_credits:
        credit_text += "\n\nFootage and image credits:\n" + "\n".join(dict.fromkeys(image_credits))
    (folder / "upload.txt").write_text(
        f"TITLE:\n{short['title'][:100]}\n\nDESCRIPTION:\n{short.get('description', '')}{credit_text}\n\n"
        f"TAGS (paste into Tags box):\n{', '.join(short.get('tags', []))[:500]}\n\n"
        f"PINNED COMMENT (post it, then pin it):\n{short.get('pinned_comment', '')}\n\n"
        "SETTINGS: Category = Education. Language = English. "
        "Subtitles -> Add language -> Upload file -> captions.srt (with timing)\n"
        + ("ALTERED OR SYNTHETIC CONTENT: Yes. This Short contains AI-generated images or motion that look "
           "like real footage (see edit_plan.txt), and YouTube requires the label.\n" if synthetic else ""),
        encoding="utf-8")
    save_state(work, short, choices, music, by_gemini)  # work/ stays KEEP_WORK_DAYS for fix.bat
    # Fix and re-render while the review finds fixable scenes, capped: an AI reviewer nearly always finds
    # something, so an uncapped loop could repaint forever. fix.bat re-renders (state, round 0) stay manual.
    if fixes and (not state or fix_round) and fix_round < AUTO_FIX_ROUNDS:
        st = load_state(work)
        st["short"]["research"] = short.get("research")  # not in state.json; the motion-graphic rescue reads it
        print(f"  fix round {fix_round + 1}/{AUTO_FIX_ROUNDS}: the review found {min(len(fixes), AUTO_REPAINT_MAX)} "
              "scene(s) to fix: fixing them and re-rendering...")
        st["short"]["auto_fixed"] = (st["short"].get("auto_fixed") or []) + [
            f"round {fix_round + 1}: {note}" for note in apply_review_fixes(st, work, fixes)]
        render(st["short"], ch, folder, st, fix_round + 1)
    elif fixes and fix_round:
        print(f"  stopped fixing after {AUTO_FIX_ROUNDS} rounds: the CHECK lines above are left for you")


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
    if not LOG.exists():
        LOG.write_text(LOG_HEADER.format(name=LOG.stem), encoding="utf-8")
    hook = re.split(r"(?<=[.!?])\s+", short["scenes"][0]["narration"].strip())[0]
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"""
## {short['title']}
Made: {folder.name[:10]} | Written by: {BRAIN.capitalize()} | Length: {clock(duration(folder / "short.mp4"))} | Folder: {folder.relative_to(ROOT)}
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


def logbook_results() -> str:
    """The logbook entries the owner has filled in (Views written down), at most the last 30."""
    if not LOG.exists():
        return ""
    entries = LOG.read_text(encoding="utf-8-sig").split("\n## ")[1:]
    return "\n\n".join(["## " + e.strip() for e in entries if re.search(r"^Views:[ \t]*\d", e, re.M)][-30:])


def main() -> None:
    # make_shorts.py [count] [channel] [claude|gemini]: anything missing is asked for (run.bat passes nothing);
    # with a count given, the planner defaults to the profile's last choice
    # make_shorts.py fix: fix.bat, re-render one scene of a recent Short
    global BRAIN, VEO_HANDOFF, SHORT_FORM
    if sys.argv[1:2] == ["fix"]:
        return fix_short()
    if sys.argv[1:2] == ["library"]:  # library.bat: approve or throw away the AI's invented looks/overlays/cuts
        return library_menu()
    if sys.argv[1:2] == ["notes"]:  # rebuild the Obsidian vault's Short pages
        return vault_refresh()
    name = sys.argv[2] if len(sys.argv) > 2 else pick_channel()
    use_channel(name)
    n = int(sys.argv[1]) if len(sys.argv) > 1 else ask_count()
    ch, failed = load_channel(), 0
    choice = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] in BRAINS else (
        ask_brain(ch.get("brain", "claude")) if len(sys.argv) < 2 else ch.get("brain", "claude"))
    ch["brain"] = choice
    if len(sys.argv) < 2:  # run.bat: ask; scripted runs never pause
        VEO_HANDOFF = ask_yes("Make the AI video clips yourself in Google Flow (Veo)? The batch pauses at each Short "
                              "until you've saved them", ch.get("veo", False))
        ch["veo"] = VEO_HANDOFF
        SHORT_FORM = ask_yes("Make shorter Shorts, about 25-30 seconds instead of 40-50 (a test)?", ch.get("short_form", False))
        ch["short_form"] = SHORT_FORM
    if choice != "claude":
        print(f"Gemini: {gemini_model()}, high effort; Claude steps in if Gemini fails")
    prune_cache()
    prune_work()
    topics = pools = None
    for BRAIN in (["claude", "gemini"] if choice == "both" else [choice]):
        if topics == []:  # Claude's half made nothing: nothing to compare
            break
        shorts = write_scripts(ch, n, topics, pools)
        if choice == "both" and topics is None:  # Gemini then writes the very same topics, with the same pictures
            topics = [s.get("topic") or s["title"] for s in shorts]
            pools = [s["pool_dir"] for s in shorts]
        seo_pass(shorts, ch)
        # Force invention look for testing if environment variable is set
        if os.environ.get("SHORTSMAKER_FORCE_INVENTION") == "1" and shorts:
            library = style_library()
            if library:
                fallback = library[0]["name"]  # first look in the library
                shorts[0]["look"] = {
                    "name": "invented",
                    "title": "Test Invention",
                    "brief": "A test look for invention path",
                    "fallback": fallback
                }
        for short in shorts:
            slug = re.sub(r"[^a-z0-9]+", "-", short["title"].lower()).strip("-")[:50]
            folder = OUTPUT / name / f"{date.today()}_{slug}{f'-{BRAIN}' if choice == 'both' else ''}"
            print(f"Making: {short['title']} ({BRAIN.capitalize()})")
            try:
                render(short, ch, folder)
            except Exception as e:  # one bad Short shouldn't kill the whole batch
                print(f"  FAILED, skipping this one: {type(e).__name__}: {e}")
                shutil.rmtree(folder, ignore_errors=True)
                failed += 1
                continue
            if short.get("topic", short["title"]) not in ch["done_topics"]:
                ch["done_topics"].append(short.get("topic", short["title"]))
            if short["shape"]:
                ch["recent_shapes"] = (ch.get("recent_shapes", []) + [short["shape"]])[-3:]
            if (short.get("look") or {}).get("name") not in (None, "invented") and any(sc.get("look") for sc in short["scenes"]):
                ch["recent_looks"] = (ch.get("recent_looks", []) + [short["look"]["name"]])[-2:]  # the next Shorts pick another
            save_channel(ch)  # save after each video so a crash keeps progress
            log_short(short, folder)
            vault_page(short["title"], folder, name)
            print(f"  done -> {folder}")
    if choice == "both":
        print("\nComparison: each topic's two versions end in -claude and -gemini. Watch both, post the better one.")
    print(f"\nAll done{f' ({failed} failed, run again to replace them)' if failed else ''}. Open {OUTPUT / name}")


def use_picture_from(work: Path, state: dict, i: int, k: int) -> None:
    """fix: scene i shows scene k's picture. A real photo/film is a picture choice; an AI painting only exists
    as work/ai<k>.jpg, so that file (and its prompt, for the edit plan's label) is copied instead."""
    choices, scenes = state["choices"], state["short"]["scenes"]
    choices[i] = {**choices[k], "person": choices[i]["person"]}
    scenes[i]["full"] = None  # it shows a picture now
    if (scenes[i].get("graphic") or {}).get("style") == "mark":  # it circled a detail of the old picture
        scenes[i]["graphic"] = None
    if not choices[k]["bg"] and (work / f"ai{k}.jpg").exists():
        shutil.copy(work / f"ai{k}.jpg", work / f"ai{i}.jpg")
        scenes[i]["ai_image"] = scenes[k]["ai_image"]
        if str(work / f"ai{k}.jpg") in state["by_gemini"]:
            state["by_gemini"].append(str(work / f"ai{i}.jpg"))
    scenes[i]["animate"] = False  # its AI motion was written for the old picture


def paint_new(work: Path, state: dict, i: int) -> None:
    """fix / auto-fix: scene i drops its picture and gets a freshly painted one (Gemini, else SDXL
    on this PC) from its ai_image prompt, or one built from its shot note, in the same never-a-photo style."""
    sc = state["short"]["scenes"][i]
    sc["full"] = None  # a painting replaces whatever the scene showed, motion graphic included
    if (sc.get("graphic") or {}).get("style") == "mark":  # it circled a detail of the old picture
        sc["graphic"] = None
    state["choices"][i] = {"bg": None, "person": state["choices"][i]["person"]}
    old = work / f"ai{i}.jpg"
    old.unlink(missing_ok=True)  # render() only paints what's missing
    state["by_gemini"] = [p for p in state["by_gemini"] if p != str(old)]
    if not sc.get("ai_image"):
        sc["ai_image"] = f"{sc.get('shot') or sc['narration']} {PAINT_FALLBACK}"
    sc["animate"] = False


def rewrite_paint_prompts(short: dict, why: dict[int, str]) -> list[int]:
    """Scenes being repainted (scene index -> what was wrong) get a better ai_image, not the same one again: MOSS
    seeds from the prompt text, so an unchanged prompt painted the identical picture (Mike's garbled newsstand came
    back, 2026-10-21; owner asked for a rewrite on every repaint). One AI call for all of them; a scene it doesn't
    answer gets a new angle so the picture still changes. Returns the scenes the AI rewrote."""
    scenes = short["scenes"]
    rows = [{"scene": i + 1, "narration": scenes[i]["narration"], "shot": scenes[i].get("shot"),
             "old_prompt": scenes[i].get("ai_image"), "problem": why[i]} for i in why]
    data = ask_ai(f"""Some AI paintings in a YouTube Short were rejected and will be painted again. Story: {short.get('topic') or short.get('title')}
For each scene write a NEW painting prompt that fixes its problem and is better than the old prompt. Don't repeat
what failed: if the old subject can't work (it shows what must not be shown, or the painter keeps getting it wrong),
pick another subject that still shows the narration. Rules for a prompt:
{AI_IMAGE_RULE}
Scenes: {json.dumps(rows, ensure_ascii=False)}
Reply with ONLY JSON: {{"prompts": [{{"scene": 3, "ai_image": "..."}}]}}""", fatal=False) or {}
    done = []
    for p in data.get("prompts") or []:
        i = p.get("scene") - 1 if isinstance(p, dict) and isinstance(p.get("scene"), int) else None
        text = str(p.get("ai_image") or "").strip() if i is not None else ""
        if i in why and i not in done and text and text != scenes[i].get("ai_image") and "photograph" not in text.lower():
            scenes[i]["ai_image"] = text[:700]
            done.append(i)
    for i in why:
        if i not in done:
            scenes[i]["ai_image"] = f"{scenes[i]['ai_image']} Seen from a different angle, in different light."
    return done


def fix_short() -> None:
    """fix.bat: re-render a recent Short with one scene changed, keeping its pictures, voice and music
    (a few minutes instead of a new Short). Only Shorts made in the last KEEP_WORK_DAYS days still have
    the working files this needs."""
    global BRAIN
    prune_work()
    recent = sorted((w.parent for w in OUTPUT.glob("*/*/work") if (w / "state.json").exists()),
                    key=lambda p: (p / "work" / "state.json").stat().st_mtime, reverse=True)[:9]
    if not recent:
        print(f"No Short can be fixed: only ones made in the last {KEEP_WORK_DAYS} days keep their working files.")
        return
    print("Which Short?")
    for k, f in enumerate(recent, 1):
        print(f"  {k}) {f.parent.name} / {f.name}")
    folder = recent[ask_number("Pick a number", len(recent), 1) - 1]
    state = load_state(folder / "work")
    short, choices = state["short"], state["choices"]
    for k, sc in enumerate(short["scenes"], 1):
        print(f"  {k}) {sc['narration'][:80]}")
    i = ask_number("Which scene?", len(short["scenes"])) - 1
    sc = short["scenes"][i]
    use_channel(folder.parent.name)
    ch = load_channel()
    BRAIN = ch.get("brain") if ch.get("brain") in ("claude", "gemini") else "claude"
    print("What should change?\n  1) No AI motion (a smooth camera move instead)\n"
          "  2) Use the picture from another scene\n  3) Remove its text graphic, map or motion graphic\n"
          "  4) Paint a new picture for it (the AI first writes a better picture prompt)\n"
          "  5) Turn it into a motion graphic (map, number, document or custom animation)")
    what = ask_number("Pick a number", 5)
    if what == 1:
        sc["animate"] = False
    elif what == 2:
        use_picture_from(folder / "work", state, i, ask_number("The picture from which scene?", len(short["scenes"])) - 1)
    elif what == 3:
        sc["graphic"], sc["full"] = None, None
    elif what == 4:
        why = input("What's wrong with the picture? (Enter to skip): ").strip()
        paint_new(folder / "work", state, i)
        rewrite_paint_prompts(short, {i: why or "the owner wants a different, better picture"})
        print(f"  new prompt: {sc['ai_image']}")
    else:
        old = sc.get("full")
        sc["full"] = None
        if not rescue_graphics(short, [i], {i: "owner asked"}):
            sc["full"] = old
            print("No motion graphic fits this line; nothing changed.")
            return
    print(f"Re-rendering {folder.name}...")
    render(short, ch, folder, state)
    print(f"  done -> {folder} (the logbook entry stays as it was)")


if __name__ == "__main__":
    main()
