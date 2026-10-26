"""Paths, fixed settings, palettes and the style/skin tables every module shares. Importing it puts the
bundled ffmpeg on PATH and checks the palettes' caption contrast."""

import os
import warnings
from pathlib import Path


ROOT = Path(__file__).parent.parent
if (ROOT / "ffmpeg").exists():
    os.environ["PATH"] = f"{ROOT / 'ffmpeg'}{os.pathsep}{os.environ.get('PATH', '')}"
CHANNELS = ROOT / "channels"  # one profile per YouTube channel: <name>.json (+ <name>.research.json)
# Obsidian vault (owner, 2026-10-21): open this folder in Obsidian. It holds the logbook and one page per Short;
# kept apart from output/ and cache/ so Obsidian never indexes thousands of video and cache files.
VAULT = ROOT / "vault"
LOGBOOK = VAULT / "Logbook"  # <channel>.md: each Short made, with the YouTube numbers the owner fills in
OUTPUT = ROOT / "output"  # each channel's Shorts go in output/<name>/
REMOTION = ROOT / "remotion"  # React/Remotion renderer for motion-graphics-heavy plans
BLENDER = Path(r"D:\Blender\blender.exe")  # headless Blender for channels with visuals: blender (blender/build_scene.py)
LIBRARY = ROOT / "blender" / "assets" / "library"  # opener models fetched through the owner's Blender (gitignored)
BLENDER_TMP = ROOT / "cache" / "blender_tmp"  # the MCP add-on's download temp folder, kept off the nearly full C:
MCP_PORT = 9876  # the Blender MCP add-on's socket (Start MCP Server in Blender's N-panel)
SHOTCUT = Path(r"D:\Shotcut\shotcut.exe")  # open-source editor for fixing by hand what the fix rounds left (edit.mlt)
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




warnings.filterwarnings("ignore", "Palette images with Transparency")  # harmless PIL note on some GIF/PNG candidates
