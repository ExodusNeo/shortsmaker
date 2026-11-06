"""3D openers (owner, 2026-11-05): scene 1 as flat drawn cut-outs standing in a lit three.js set
(remotion/src/Opener3D.tsx), filmed by a moving camera. The opener crew (opener_crew.py) writes the stage: its placer
names WHERE things go by relation (`place`: a mark on the set, at a house's door, beside the desk) and which shot
sizes to use (`shot`: wide / medium / close / over / low / top); this file turns that into positions and camera
numbers, checks it, paints the cut-outs and renders it. Since 2026-11-06 no AI types 3D coordinates: every live
failure before that was a guessed position (doors off the house, a fist short of the door, people cut off at the
edge). Lesson from the removed Blender openers (2026-10-30): fixed sets and parts; the AI only chooses among them."""

import json
import math
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

from shortsmaker import drawn_opener, media_tools
from shortsmaker.config import FPS, ROOT

REMOTION = ROOT / "remotion"
STAGE = ROOT / "drawn" / "STAGE3D.md"
PUBLIC = REMOTION / "public" / "opener3d" / "job"  # Remotion loads images only from its public folder
TIMEOUT = 900
PLACES, MOODS = ("room", "street", "outdoors"), ("day", "golden", "dusk", "night", "interior")
PROPS = {"desk", "table", "chair", "door", "window", "frame", "shelf", "lamp", "bed", "rug", "crate", "barrel", "cabinet",
         "counter", "fireplace", "house", "shopfront", "cabin", "garden", "field", "tree", "rock", "fence", "lamppost",
         "stall", "cart", "fountain", "bookcase", "coatrack", "hedge", "walllamp", "sidetable"}
# the visible signs of an invisible strange thing (electricity, heat, a sky event): a muted viewer must see it
SIGN_EFFECTS = ("sparks", "smoke", "glow", "aurora")
EFFECTS = {"rings", "dust", "shafts", "burst", "shake", "rain", "snow", "jolt", "puff", *SIGN_EFFECTS}
SPREAD = 1.5  # the widest shot stands at least this many times farther back than the closest (McLean: 1.95-2.35 m)
MOVES = {"cut", "whip", "push"}
SCENERY = ("house", "shop", "bank", "factory", "tower", "room", "sky", "ground", "hills", "sea", "island", "window",
           "shelf", "bed", "rug", "palm", "pine", "tree")
NAME = re.compile(r"^[a-z][a-z0-9_]{0,19}$")
COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")
DRAW = re.compile(r"export\s+default\s+function\s+draw\s*\(\s*k\s*,\s*f\s*(,\s*u\s*)?\)")


def available() -> str | None:
    """Why a 3D opener can't be made on this PC, or None."""
    return drawn_opener.available() or (
        None if shutil.which("npx") and (REMOTION / "node_modules" / "@remotion" / "three").exists()
        else r"the 3D library isn't installed (run: cd remotion && npm install)")


def word_time(words: list, w, fallback: float) -> float:
    """A time given as seconds or as a spoken word (its start; the same rule as the kit's k.word)."""
    if isinstance(w, (int, float)) and not isinstance(w, bool):
        return float(w)
    want = re.sub(r"[^a-z0-9']", "", str(w).lower())
    hit = next((s for s, _, txt in words if want and re.sub(r"[^a-z0-9']", "", str(txt).lower()).startswith(want)), None)
    return float(hit) if hit is not None else fallback


def num(v, lo: float, hi: float, default: float) -> float:
    return min(hi, max(lo, float(v))) if isinstance(v, (int, float)) and not isinstance(v, bool) else default


def xz(v, default=(0.0, -1.5)) -> list[float]:
    return [num(v[0], -40, 40, default[0]), num(v[1], -60, 10, default[1])] if isinstance(v, list) and len(v) == 2 else list(default)


PATCHES = {"garden", "field", "rug"}  # flat: people and animals stand IN them (`{"in": id}`), never nudged out
HOUSE_UNIT = 2.4  # one town-kit wall module of a `house` / `shopfront` prop (Opener3D.tsx), in metres at size 1

# Named spots on each place (x, z): `{"mark": "left"}`. Room: the back wall is at z -4; street/outdoors run to -z.
MARKS = {"room": {"left": (-1.5, -1.7), "centre": (0, -1.7), "right": (1.5, -1.7), "front-left": (-1.1, -.6),
                  "front-right": (1.1, -.6), "back-left": (-2.2, -3.0), "back": (0, -3.0), "back-right": (2.2, -3.0)},
         "street": {"left": (-1.6, -2), "centre": (0, -2), "right": (1.6, -2), "front-left": (-1.1, -.5),
                    "front-right": (1.1, -.5), "back-left": (-2, -7), "back": (0, -8), "back-right": (2, -7)},
         "outdoors": {"left": (-1.8, -2), "centre": (0, -2), "right": (1.8, -2), "front-left": (-1.2, -.5),
                      "front-right": (1.2, -.5), "back-left": (-3, -8), "back": (0, -9), "back-right": (3, -8)}}
WALL_SPOTS = {"left": -2.2, "centre": 0, "right": 2.2}  # a room's back wall: `{"wall": "left"}` for a window or picture
# What a prop takes up on the floor at size 1 (width x, depth z, height): placing and the overlap nudge use it.
FOOT = {"desk": (2.3, 1.0, .86), "table": (1.6, .9, .8), "chair": (.5, .5, 1.0), "door": (1.3, .12, 2.45),
        "shelf": (1.3, .45, 2.3), "lamp": (.3, .3, .5), "bed": (1.1, 2.1, 1.1), "cabinet": (1.0, .5, 1.8),
        "counter": (3.0, .7, 1.05), "fireplace": (1.6, .45, 1.3), "crate": (.7, .7, .7), "barrel": (.6, .6, .9),
        "rock": (1.1, 1.0, .6), "tree": (1.4, 1.4, 4.6), "lamppost": (.3, .3, 3.3), "house": (7.2, 2.6, 6.0),
        "shopfront": (7.2, 2.6, 6.0), "cabin": (4.8, 2.6, 3.6), "garden": (3.0, 3.0, .4), "field": (4.0, 3.2, .9), "fence": (4.0, .1, 1.0),
        "stall": (2.4, 1.6, 2.4), "cart": (2.0, 1.1, 1.3), "fountain": (2.6, 2.6, 1.2), "bookcase": (1.1, .45, 2.0),
        "coatrack": (.5, .5, 1.8), "hedge": (2.0, .8, 1.1), "sidetable": (.6, .5, .6)}
# Set dressing (2026-11-06: reviews kept calling the sets plain): period pieces the code adds at the edges of each
# place, (type, x, z, turn), skipped where they would touch anything placed. They have no id, so no shot aims at them.
# (no wall lamps: lit ones glared through the bloom and pulled the eye off the people, live 2026-11-06)
DRESS = {"room": [("bookcase", 3.2, -3.7, 0), ("coatrack", -3.4, -3.5, 0), ("sidetable", -3.55, -1.4, 90)],
         "street": [("stall", -3.1, -5.2, 90), ("cart", 3.2, -3.4, -70), ("barrel", -3.5, -1.6, 0), ("barrel", -3.6, -2.7, 0),
                    ("lamppost", 3.6, -7.0, 0), ("crate", 3.4, -9.5, 20)],
         "outdoors": [("hedge", -3.6, -4.2, 10), ("rock", 3.3, -3.2, 30), ("tree", -5.2, -7.5, 0), ("tree", 5.6, -9.0, 0),
                      ("fence", 0, -12.5, 0)]}
BUILDINGS = {"house": (3, 1), "shopfront": (3, 7), "cabin": (2, 13)}  # wall modules across, door seed offset (Opener3D.tsx)
# A shot by size: distance and camera height for a 1.75 m person (scaled to the target's height), and the lens.
# Sized for a 9:16 frame, where the vertical view decides how big a person reads (2026-11-06: the first presets showed
# 4.2 m of height in a "wide", a person filled 40% of the frame and every live review called it too small/empty):
# wide = whole body (~2.6 m of view), medium = knees up (~1.5 m), close = head and shoulders (~0.8 m, aimed at the face).
SHOT_SIZES = {"wide": (2.4, .45, 58), "medium": (1.55, .15, 52), "close": (.9, .05, 48), "low": (2.0, -.8, 56),
              "top": (2.6, 1.9, 56), "over": (1.8, .1, 50)}
TOPS = {"desk": .86, "table": .8, "counter": 1.05, "crate": .7, "barrel": .9, "cabinet": 1.8, "fireplace": 1.3, "bed": .7,
        "sidetable": .6, "cart": .9}  # top heights
KNOCK_CALL = re.compile(r"k\.knock\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)")


def box_of(p: dict) -> tuple[float, float, float, float] | None:
    """A floor prop's footprint (x0, x1, z0, z1) in the set, or None (rugs and things on the wall take no floor)."""
    if p["type"] not in FOOT or p.get("wall"):
        return None
    w, d, _ = FOOT[p["type"]]
    w, d = (p.get("length") or w if p["type"] == "fence" else w) * p["size"], d * p["size"]
    if 45 < abs(p["turn"]) % 180 < 135:
        w, d = d, w
    x, z = p["at"]
    if p["type"] in tuple(BUILDINGS):  # its front wall is .5 of a storey in front of `at` (front_door)
        return x - w / 2, x + w / 2, z - .6 * HOUSE_UNIT * p["size"], z + .5 * HOUSE_UNIT * p["size"]
    return x - w / 2, x + w / 2, z - d / 2, z + d / 2


def dress(place: str, props: list[dict], cutouts: list[dict]) -> list[dict]:
    """The DRESS pieces for this place that touch nothing placed (a prop's footprint, a cut-out's spot or walk,
    a wall lamp where a window or picture hangs), as props marked `dressing`."""
    taken = [b for p in props if (b := box_of(p))]
    spots = [c["at"] for c in cutouts if not c.get("wall")] + [st[1:] for c in cutouts for st in c.get("path") or []]
    hung = [p["at"][0] for p in props if p.get("wall")] + [c["at"][0] for c in cutouts if c.get("wall")]
    out = []
    for kind, x, z, turn in DRESS[place]:
        q = {"type": kind, "at": [x, z], "turn": turn, "size": 1, "dressing": True}
        if kind == "walllamp":  # on the back wall, at head height
            if all(abs(x - h) > 1.0 for h in hung):
                out.append({**q, "at": [x, 2.5], "wall": True, "lit": True})
            continue
        b = box_of(q)
        if kind == "fence":
            q["length"] = 6
            b = (x - 3, x + 3, z - .1, z + .1)
        if any(b[0] - .3 < t[1] and t[0] < b[1] + .3 and b[2] - .3 < t[3] and t[2] < b[3] + .3 for t in taken):
            continue
        if any(b[0] - .6 < sx < b[1] + .6 and b[2] - .6 < sz < b[3] + .6 for sx, sz in spots):
            continue
        taken.append(b)
        out.append(q)
    return out


def spread_out(shots: list[dict], cutouts: list[dict], props: list[dict]) -> list[str]:
    """Medium/close/low shots on a list of cut-outs standing so far apart that the camera must back off well past the
    size's distance to fit them (Opener3D.tsx `aim`), so everyone reads tiny: all three live stories opened that way
    (2026-11-06, "far too wide, pushed to the screen edges"). Worded for the placer."""
    found = []
    for sh in shots:
        names = sh["target"] if isinstance(sh["target"], list) else []
        cuts = [c for c in cutouts if c["name"] in names and not c.get("wall")]
        if sh.get("size") not in ("medium", "close", "low") or len(cuts) < 2:
            continue
        others = [p["at"][0] for p in props if p.get("id") in names]
        cx = (sum(c["at"][0] for c in cuts) + .3 * sum(others)) / (len(cuts) + .3 * len(others))
        half = max(abs(c["at"][0] - cx) + .42 * c["height"] * c["aspect"] + .1 for c in cuts)
        fit = half / math.tan(math.atan(math.tan(math.radians(sh["fov"]) / 2) * 9 / 16))
        if fit > 2.6 * sh["distance"]:  # side by side needs ~2.5x in a 9:16 frame; the live openers were 4-5x
            found.append(f"camera: the {sh['size']} shot at {sh['at']:g}s on {' + '.join(c['name'] for c in cuts)} has to stand "
                         f"{fit:.1f} m back to fit them all, so they read tiny on a phone: stand them side by side "
                         f"(`beside`, within about 1 m) or give each its own shot")
    return found


def half_width(c: dict) -> float:
    """Half of what a cut-out's drawing really covers (its canvas has a margin round the person)."""
    return .4 * c["height"] * c["aspect"]


def resolve(spec, named: dict, place: str, size: float = 1) -> tuple[list[float] | None, str | None]:
    """[x, z] for a `place` relation, or (None, what's wrong). `named` maps ids/names to placed props and cut-outs."""
    if not isinstance(spec, dict) or len(spec) not in (1, 2):
        return None, "`place` must be one relation, e.g. {\"mark\": \"left\"} or {\"beside\": \"desk1\", \"side\": \"right\"}"
    if "mark" in spec:
        m = MARKS[place].get(str(spec["mark"]))
        return (list(m), None) if m else (None, f"no mark {spec['mark']!r}: use {', '.join(MARKS[place])}")
    key = next((k for k in ("beside", "front", "in") if k in spec), None)
    if not key:
        return None, f"unknown relation {', '.join(map(str, spec))}: use mark, door, beside, front, in or wall"
    other = named.get(spec[key])
    if other is None:
        return None, f"{key} {spec[key]!r}: nothing placed before it has that id or name"
    if "type" in other:  # a prop
        b = box_of(other) or (other["at"][0] - .3, other["at"][0] + .3, other["at"][1] - .2, other["at"][1] + .2)
    else:  # a cut-out: a thin board
        hw = half_width(other)
        b = (other["at"][0] - hw, other["at"][0] + hw, other["at"][1] - .1, other["at"][1] + .1)
    cx, cz = (b[0] + b[1]) / 2, (b[2] + b[3]) / 2
    if key == "in":  # standing in a garden or field patch: a little in front of its middle, so it reads as inside
        if other.get("type") not in PATCHES:
            return None, f"in {spec['in']!r}: things stand `in` a {', '.join(sorted(PATCHES))}; use beside or front for anything else"
        return [round(cx + {"left": -.25, "right": .25}.get(str(spec.get("side")), 0) * (b[1] - b[0]), 3), round(cz + .2 * (b[3] - b[2]), 3)], None
    if key == "front":
        return [round(cx, 3), round(b[3] + .45, 3)], None
    side = -1 if spec.get("side") == "left" else 1
    return [round(cx + side * ((b[1] - b[0]) / 2 + size + .1), 3), round(min(cz, b[3] - .05) if "type" in other else cz, 3)], None


def on_top(spec: dict, named: dict) -> tuple[list[float] | None, str | None]:
    """[x, z, y] of a spot on top of a desk, table, counter... (`{"on": id, "side": "left"}`), or (None, why)."""
    p = named.get(spec["on"])
    if not p or "type" not in p or p["type"] not in TOPS:
        return None, f"on {spec['on']!r}: things stand on a prop with an id of type {', '.join(sorted(TOPS))}"
    b = box_of(p)
    dx = {"left": -.3, "right": .3}.get(str(spec.get("side") or "centre"), 0) * (b[1] - b[0])
    return [round(p["at"][0] + dx, 3), round(b[3] - .2, 3), round(TOPS[p["type"]] * p["size"] + p.get("y", 0), 3)], None


def in_order(cutouts: list) -> list:
    """Cut-outs ordered so each one comes after the cut-out its `place` names (a live draft put the battery beside
    a telegraph listed after it, 2026-11-06). Unknown names and loops keep their order; resolve reports them."""
    left, out, placed = list(cutouts), [], set()
    ref = lambda c: next((v for k, v in (c.get("place") or {}).items() if k in ("beside", "front", "in")), None) if isinstance(c, dict) and isinstance(c.get("place"), dict) else None  # noqa: E731
    names = {c.get("name") for c in cutouts if isinstance(c, dict)}
    while left:
        ready = [c for c in left if ref(c) not in names or ref(c) in placed]
        if not ready:
            ready = left[:1]
        for c in ready:
            left.remove(c)
            out.append(c)
            placed.add(c.get("name") if isinstance(c, dict) else None)
    return out


def nudge(cutouts: list[dict], props: list[dict], place: str) -> None:
    """Moves floor cut-outs out of furniture (to stand in front of it: nobody hidden behind a desk) and apart from
    each other (side by side, never one board through another). In place."""
    floor = [c for c in cutouts if not c.get("wall") and not c.get("against") and not c.get("path") and not c.get("on")]
    for c in floor:
        for p in props:
            b = box_of(p) if p["type"] not in PATCHES else None  # a pig in the potato patch stays in it (2026-11-06)  # inside furniture or a building's walls: step out in front of it (a live placer put a
            if b and b[0] < c["at"][0] < b[1] and b[2] - .15 < c["at"][1] < b[3] + .15:  # bystander in a house, 2026-11-06)
                c["at"][1] = round(b[3] + .35, 3)
    for _ in range(3):
        for i, c in enumerate(floor):
            for o in floor[:i]:
                gap = half_width(c) + half_width(o) + .05 - abs(c["at"][0] - o["at"][0])
                if gap > 0 and abs(c["at"][1] - o["at"][1]) < .6:
                    side = 1 if c["at"][0] >= o["at"][0] else -1
                    c["at"][0] = round(c["at"][0] + side * gap, 3)
    if place == "room":
        for c in floor:
            c["at"][0] = max(-3.4, min(3.4, c["at"][0]))


def front_door(p: dict, i: int) -> tuple[float, float]:
    """Where a cut-out stands flush against prop `p` (number i in the stage): a house or shopfront's own front door
    (Opener3D.tsx's Building puts it at module seed % 3), or a 3D door's face."""
    u = HOUSE_UNIT * p["size"]
    wide, seed = BUILDINGS.get(p["type"], (3, 1))
    dx, dz = (((i + seed) % wide - (wide - 1) / 2) * u, .5 * u + .04) if p["type"] != "door" else (0, .1)
    a = math.radians(p["turn"])  # three.js turns about y: x' = x cos + z sin, z' = -x sin + z cos
    return round(p["at"][0] + dx * math.cos(a) + dz * math.sin(a), 3), round(p["at"][1] - dx * math.sin(a) + dz * math.cos(a), 3)


def inside(c: dict, props: list[dict]) -> str | None:
    """The house or shop a floor cut-out stands inside of (a live McLean draft put the messenger in the wall)."""
    for p in props:
        if p["type"] in tuple(BUILDINGS) and abs(p["turn"]) < 20:
            u = HOUSE_UNIT * p["size"]
            if abs(c["at"][0] - p["at"][0]) < 1.5 * u and p["at"][1] - .6 * u < c["at"][1] < p["at"][1] + .5 * u:
                return p.get("id") or p["type"]
    return None


def lint_cutout(code: str) -> list[str]:
    """Rule breaks in an AI-written cut-out module (the drawn opener's code rules, with draw(k, f))."""
    found = [p for p in drawn_opener.lint(code) if "export default function scene" not in p]
    live = drawn_opener.INERT.sub('""', code)
    scenery = sorted(set(re.findall(r"\bk\.(" + "|".join(SCENERY) + r")\(", live)))
    if scenery:  # a live draft painted the house, its door frame and the street into one flat board (2026-11-06)
        found.append(f"draws scenery in a cut-out ({', '.join('k.' + n for n in scenery)}): buildings, rooms, ground "
                     f"and sky are the 3D place and props; a cut-out is one person or animal and what it holds or touches")
    if not DRAW.search(code):
        found.append("missing `export default function draw(k, f, u)`")
    return found


def clean(raw, words: list, seconds: float) -> tuple[dict | None, list[str]]:
    """The AI's stage, checked and made safe for Remotion (word times resolved, numbers clamped), and what was wrong
    with it. A stage with problems goes back to the coder."""
    if not isinstance(raw, dict):
        return None, ["the reply was not a JSON object"]
    bad: list[str] = []
    place = raw.get("place") if raw.get("place") in PLACES else "room"
    mood = raw.get("mood") if raw.get("mood") in MOODS else "interior"
    colors = {k: v for k, v in (raw.get("colors") or {}).items() if k in ("wall", "floor", "ground", "sky", "trim")
              and isinstance(v, str) and COLOR.match(v)} if isinstance(raw.get("colors"), dict) else {}
    props, named = [], {}
    for p in raw.get("props") or []:
        if not isinstance(p, dict) or p.get("type") not in PROPS:
            bad.append(f"unknown prop {p.get('type') if isinstance(p, dict) else p!r}: use only the listed props")
            continue
        q = {"type": p["type"], "at": xz(p.get("at")), "turn": num(p.get("turn"), -360, 360, 0), "size": num(p.get("size"), 0.2, 4, 1)}
        for k in ("wall", "lit"):
            if isinstance(p.get(k), bool):
                q[k] = p[k]
        if q.get("wall"):
            q["at"] = [num((p.get("at") or [0, 2])[0], -3.8, 3.8, 0), num((p.get("at") or [0, 2])[1], 0.3, 4.2, 2)]
        for k, lo, hi in (("y", 0, 4), ("open", 0, 1), ("length", 0.5, 20)):
            if k in p:
                q[k] = num(p[k], lo, hi, 0)
        if isinstance(p.get("color"), str) and COLOR.match(p["color"]):
            q["color"] = p["color"]
        if isinstance(p.get("id"), str) and NAME.match(p["id"]):
            q["id"] = p["id"]
        spec = p.get("place")
        if isinstance(spec, dict) and "wall" in spec:  # hung on the room's back wall: a window, a picture
            q["wall"], q["at"] = True, [WALL_SPOTS.get(str(spec["wall"]), 0), num(spec.get("height"), .5, 4, 2.4)]
        elif isinstance(spec, dict) and "on" in spec:  # a lamp on the desk, a barrel on a crate
            spot, why = on_top(spec, named)
            if why:
                bad.append(f"prop {q.get('id') or q['type']}: {why}")
            else:
                q["at"], q["y"] = spot[:2], spot[2]
        elif isinstance(spec, dict) and q["type"] == "door" and place == "room":  # a room's door stands in the back wall
            at, why = resolve(spec, named, place)
            q["at"] = [at[0], -3.95] if at else q["at"]
            bad += [f"prop {q.get('id') or q['type']}: {why}"] if why else []
        elif spec is not None:
            at, why = resolve(spec, named, place, max(FOOT.get(q["type"], (.6,))[0], .6) * q["size"] / 2)
            if why:
                bad.append(f"prop {q.get('id') or q['type']}: {why}")
            else:
                q["at"] = at
                if q["type"] in tuple(BUILDINGS):  # a building's front, not its middle, stands on the spot
                    q["at"][1] = round(at[1] - .5 * HOUSE_UNIT * q["size"] - .6, 3)
        if q.get("id"):
            named[q["id"]] = q
        props.append(q)
    cutouts, names = [], set()
    for c in in_order(raw.get("cutouts") or []):
        if not isinstance(c, dict) or not isinstance(c.get("name"), str) or not NAME.match(c["name"]) or c["name"] in names:
            bad.append("each cut-out needs a unique lowercase `name` (letters, digits, _)")
            continue
        code = drawn_opener.clean_code(c.get("code"))
        problems = lint_cutout(code) if code else ["no code"]
        if problems:
            bad += [f"cut-out {c['name']}: {p}" for p in problems]
            continue
        w, h = int(num(c.get("w"), 100, 1400, 700)), int(num(c.get("h"), 100, 1400, 1100))
        q = {"name": c["name"], "w": w, "h": h, "aspect": w / h, "frames": int(num(c.get("frames"), 1, 6, 1)),
             "height": num(c.get("height"), 0.1, 6, 1.75), "at": xz(c.get("at")), "y": num(c.get("y"), 0, 4, 0),
             "flip": c.get("flip") is True, "wall": c.get("wall") is True, "fps": num(c.get("fps"), 2, 12, 7), "code": code}
        spec = c.get("place")
        door = c.get("against") or (spec.get("door") if isinstance(spec, dict) else None)
        if isinstance(spec, dict) and "wall" in spec:  # a painting, a carved seal, a clock on the back wall
            q["wall"], q["at"] = True, [WALL_SPOTS.get(str(spec["wall"]), 0), num(spec.get("height"), .5, 4, 2.4)]
        elif q["wall"]:
            q["at"] = [num((c.get("at") or [0, 2])[0], -3.8, 3.8, 0), num((c.get("at") or [0, 2])[1], 0.3, 4.2, 2)]
        if isinstance(c.get("talk"), list) and len(c["talk"]) == 2:
            q["talk"] = [word_time(words, c["talk"][0], 0), word_time(words, c["talk"][1], seconds)]
        if isinstance(door, str):  # flush on a house's front door (a knock), or a 3D door
            k = next((j for j, p in enumerate(props) if p.get("id") == door and p["type"] in (*BUILDINGS, "door")), None)
            if k is None:
                bad.append(f"cut-out {c['name']} stands at the door of {door!r}: give a house, shopfront or door prop that id")
            else:
                q["at"], q["against"] = list(front_door(props[k], k)), door
        elif isinstance(spec, dict) and "on" in spec:  # a small thing standing on a desk, table, counter, crate...
            spot, why = on_top(spec, named)
            if why:
                bad.append(f"cut-out {c['name']} can't stand there: {why}")
            else:
                q["at"], q["y"], q["on"] = spot[:2], spot[2], spec["on"]
        elif isinstance(spec, dict) and "wall" not in spec:
            at, why = resolve(spec, {**named, **{x["name"]: x for x in cutouts}}, place, half_width(q))
            if why:
                bad.append(f"cut-out {c['name']} can't stand there: {why}")  # a placer's mistake, not the painter's
            else:
                q["at"] = at
        if "k.knock(" in code:  # shots aim at the knocker and his fist, left of the door at the canvas centre
            q["focus"] = round(-.36 * q["height"] * 1100 / h, 3)
            m = KNOCK_CALL.search(drawn_opener.INERT.sub('""', code))
            if m:  # where the fist meets the door (kit.mjs k.knock: x - 40 s, y - 150 s), in metres from the board's foot
                kx, ky, ks = (float(v) for v in m.groups())
                q["contact"] = [round(((kx - 40 * ks) / w - .5) * q["height"] * q["aspect"], 3), round((1 - (ky - 150 * ks) / h) * q["height"], 3)]
        if isinstance(c.get("hits"), list):  # a squash on each hit (a knock, a stamp): seconds or spoken words
            q["hits"] = sorted(word_time(words, x, 0) for x in c["hits"][:8])
        if isinstance(c.get("path"), list):  # [[time, "mark"], ...] (or [time, x, z]): a walk from spot to spot
            steps = []
            for k in c["path"]:
                if isinstance(k, dict):  # {"at": time, "mark": "left"}, the way placers like to write it
                    k = [k.get("at", k.get("time", 0)), k.get("mark") or k.get("place")]
                spot = k[1].get("mark") if isinstance(k, list) and len(k) == 2 and isinstance(k[1], dict) else (k[1] if isinstance(k, list) and len(k) == 2 else None)
                if spot is not None and str(spot) in MARKS[place]:
                    steps.append([word_time(words, k[0], 0), *MARKS[place][str(spot)]])
                elif isinstance(k, list) and len(k) == 3:
                    steps.append([word_time(words, k[0], 0), num(k[1], -40, 40, 0), num(k[2], -60, 10, -1.5)])
                else:  # worded so the opener crew sends it to the placer, not the painter
                    bad.append(f"cut-out {c['name']} can't walk there: a path step is [time, mark] with a mark from {', '.join(MARKS[place])}")
            if steps:
                q["path"] = sorted(steps)
        names.add(c["name"])
        cutouts.append(q)
    nudge(cutouts, props, place)
    for q in cutouts:
        if not q["wall"] and not q.get("against") and (hit := inside(q, props)):
            bad.append(f"cut-out {q['name']} stands inside {hit}: put it at the door ({{\"door\": \"{hit}\"}}) or `front` of it")
    if not cutouts:
        bad.append("no usable cut-out: the subject must be a drawn cut-out")
    ids = names | {p["id"] for p in props if p.get("id")}
    # how big a shot's target is: a knocker's board is 2.3 m because of its door, but the shot is about the man
    tall = {**{c["name"]: 1.75 if c.get("focus") else c["height"] for c in cutouts},
            **{p["id"]: FOOT.get(p["type"], (0, 0, 1.2))[2] * p["size"] for p in props if p.get("id")}}
    shots = []
    for sh in raw.get("shots") or []:
        tg = sh.get("target") if isinstance(sh, dict) else None
        names = tg if isinstance(tg, list) else [tg]  # a list frames them all
        if not names or len(names) > 4 or any(not isinstance(n, str) or n not in ids for n in names):
            bad.append(f"a shot aims at {tg!r}: use cut-out names or prop ids (a list of up to 4 frames them all)")
            continue
        size = sh.get("shot") if sh.get("shot") in SHOT_SIZES else None
        # sized to the target: a 0.3 m machine's close-up stands much nearer than a man's (a live close-up on a small
        # thing on a desk showed mostly desk front, 2026-11-06); a thing up on furniture is filmed a little from above
        scale = max(.2, min(3.0, max(tall.get(n, 1.75) for n in names) / 1.75))
        d0, h0, f0 = SHOT_SIZES[size or "medium"]
        up = .35 if size in ("close", "medium") and any(c.get("on") for c in cutouts if c["name"] in names) else 0
        typed = {} if size else sh  # a named size ignores typed numbers (a live placer's "fix" typed a distance and
        shot = {"at": num(word_time(words, sh.get("at", 0), 0), 0, seconds, 0), "target": tg,  # cut a head off)
                "distance": num(typed.get("distance"), 0.5, 14, max(.5, round(d0 * scale, 2))),
                "height": num(typed.get("height"), -3, 6, round(h0 * scale + up, 2)),
                "turn": num(sh.get("turn"), -170, 170, 0), "fov": num(typed.get("fov"), 28, 72, f0),
                "move": sh.get("move") if sh.get("move") in MOVES else "cut"}
        if size:
            shot["size"] = size
        if sh.get("over") is not None:  # over the shoulder of another thing than its target
            if sh["over"] in ids and sh["over"] not in names:
                shot["over"] = sh["over"]
            else:
                bad.append(f"a shot looks over {sh['over']!r}: use another cut-out name or prop id than its target")
        elif size == "over":
            bad.append("an `over` shot needs `over`: the name of the person or thing the camera looks past")
        shots.append(shot)
    shots.sort(key=lambda s: s["at"])
    bad += spread_out(shots, cutouts, props)
    if not shots:
        bad.append("no usable shot")
    near = [sh["distance"] for sh in shots if not sh.get("over")]
    if shots and all(sh.get("size") for sh in shots):  # named sizes are each a different framing: only no repeats
        if len(shots) == 1 or any(a["size"] == b["size"] and a["target"] == b["target"] for a, b in zip(shots, shots[1:])):  # close on him, then close on the machine: fine
            bad.append(f"the shots repeat a size ({' -> '.join(sh['size'] for sh in shots)}): change the size at every cut, "
                       f"wide or medium first, close on the strange word")
    elif len(shots) == 1 or (len(shots) > 1 and not any(sh.get("over") for sh in shots) and max(near) < SPREAD * min(near)):
        bad.append(f"the shots are all the same size ({', '.join(f'{d:g}' for d in near)} m): cut from a wide shot to a "
                   f"close-up at least {SPREAD:g}x nearer on the strange word, or look over someone's shoulder (`over`)")
    effects = [{"type": e["type"], "at": word_time(words, e.get("at", 0), 0), **({"on": e["on"]} if e.get("on") in ids else {}),
                **({"color": e["color"]} if COLOR.match(str(e.get("color") or "")) else {})}
               for e in raw.get("effects") or [] if isinstance(e, dict) and e.get("type") in EFFECTS]
    bad += [f"the {e['type']} effect needs `on`: the id or cut-out name it comes from" for e in effects
            if e["type"] in ("sparks", "smoke", "glow") and "on" not in e]
    if place == "room" and any(e["type"] == "aurora" for e in effects) and not any(p["type"] == "window" for p in props):
        bad.append("the aurora shows through a window in a room: hang a `window` prop on the back wall and aim a shot past it")
    needs = [str(x).strip()[:40] for x in raw.get("needs") or [] if str(x).strip()][:8] if isinstance(raw.get("needs"), list) else []
    stage = {"moment": str(raw.get("moment") or "the strangest moment").strip()[:200], "needs": needs, "place": place, "mood": mood,
             "colors": colors, "props": props[:24] + dress(place, props[:24], cutouts[:6]), "cutouts": cutouts[:6],
             "shots": shots[:5], "effects": effects[:8]}
    return stage, bad


def render(stage: dict, seconds: float, folder: Path) -> str | None:
    """Paints the cut-outs and renders folder/opener.mp4; None when it worked, else what went wrong."""
    folder = folder.resolve()  # node and Remotion run in other folders
    folder.mkdir(parents=True, exist_ok=True)
    for c in stage["cutouts"]:
        (folder / f"cut_{c['name']}.mjs").write_text(c["code"], encoding="utf-8")
    job = {"out": str(folder / "cutouts"), "cutouts": [{**{k: c.get(k) for k in ("name", "w", "h", "frames", "fps")},
                                                         "module": str(folder / f"cut_{c['name']}.mjs")} for c in stage["cutouts"]]}
    (folder / "cutouts.json").write_text(json.dumps(job), encoding="utf-8")
    try:  # the cut-outs' code was written by the AI: same locked-down node as the drawn opener
        r = subprocess.run(["node", "--disallow-code-generation-from-strings", str(drawn_opener.DRAWN / "cutouts.mjs"),
                            str(folder / "cutouts.json")], cwd=drawn_opener.DRAWN, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=300)
    except subprocess.TimeoutExpired:
        return "painting the cut-outs took too long"
    if r.returncode:
        return "a cut-out crashed when it ran: " + " | ".join(line.strip() for line in (r.stderr or r.stdout).splitlines()
                                                              if line.strip() and "node:internal" not in line)[:500]
    sizes = json.loads((folder / "cutouts" / "sizes.json").read_text(encoding="utf-8"))  # the cropped boards (cutouts.mjs)
    shutil.rmtree(PUBLIC, ignore_errors=True)
    shutil.copytree(folder / "cutouts", PUBLIC)
    props = {"fps": FPS, "seconds": seconds, "dir": "opener3d/job", **{k: v for k, v in stage.items() if k not in ("moment", "needs")},
             "cutouts": [{**{k: v for k, v in c.items() if k not in ("code", "w", "h")}, **sizes.get(c["name"], {})}
                         for c in stage["cutouts"]]}
    (folder / "props.json").write_text(json.dumps(props), encoding="utf-8")
    try:
        r = subprocess.run([shutil.which("npx") or "npx", "remotion", "render", "src/index.ts", "Opener3D", str(folder / "opener.mp4"),
                            f"--props={folder / 'props.json'}", "--log=error", "--gl=angle", "--concurrency=4"],
                           cwd=REMOTION, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return f"the 3D render took longer than {TIMEOUT} s"
    finally:
        shutil.rmtree(PUBLIC, ignore_errors=True)
    if r.returncode or not (folder / "opener.mp4").exists():
        return "the 3D render failed: " + (r.stderr or r.stdout or "no message").strip()[-500:]
    return None


def sheet_times(seconds: float, shots: list | None = None) -> list[float]:
    """Six preview times: the first and last frame, just after each camera cut (the art director must see every
    framing, not six evenly spaced frames that can all land in one shot), then even spacing for the rest."""
    base = drawn_opener.sheet_times(seconds)
    picked = [base[0], base[-1]] + [round(sh["at"] + .35, 2) for sh in (shots or [])[1:4] if sh["at"] + .35 < seconds - .15]
    for t in base[1:-1]:
        if len(picked) < 6 and all(abs(t - q) > .4 for q in picked):
            picked.append(t)
    return sorted(picked)[:6]


def blends(stage: dict, folder: Path) -> list[str]:
    """Cut-outs whose main colour melts into the room's wall behind them (McLean, 2026-11-05: the grocer's brown coat
    on a brown wall). Compares each painted cut-out's most common non-ink colour with the wall colour."""
    if stage["place"] != "room":
        return []
    wall = stage["colors"].get("wall") or "#7E5A40"
    wr, wg, wb = (int(wall[i:i + 2], 16) for i in (1, 3, 5))
    found = []
    for c in stage["cutouts"]:
        png = folder / "cutouts" / f"{c['name']}_0.png"
        if c.get("wall") or c.get("on") or not png.exists():  # a thing on a desk is seen against the desk
            continue
        im = Image.open(png).convert("RGBA")
        im = im.resize((120, max(1, 120 * im.height // max(1, im.width))))
        buckets: dict[tuple, list] = {}
        for r, g, b, a in im.getdata():
            if a > 200 and r + g + b > 120:  # opaque, not the ink lines
                buckets.setdefault((r // 32, g // 32, b // 32), []).append((r, g, b))
        if not buckets:
            continue
        main = max(buckets.values(), key=len)
        r, g, b = (sum(px[i] for px in main) / len(main) for i in range(3))
        lum = lambda r, g, b: .2126 * r + .7152 * g + .0722 * b  # noqa: E731
        if ((r - wr) ** 2 + (g - wg) ** 2 + (b - wb) ** 2) ** .5 < 70 and abs(lum(r, g, b) - lum(wr, wg, wb)) < 40:
            found.append(f"{c['name']}'s main colour (#{int(r):02X}{int(g):02X}{int(b):02X}) melts into the wall ({wall}): "
                         f"give it a coat or wall colour that stands out in hue and brightness")
    return found


PAIR = .2  # the review sheet's second row: the same moments this much later, so the reviewer sees what moves


def sheet(clip: Path, seconds: float, out: Path, shots: list | None = None, cutouts: Path | None = None) -> Path:
    """The art director's preview: six moments left to right (the time on each), and under each the same moment
    PAIR s later. Live reviewers called a cycling knock "frozen" from single stills (2026-11-05); a pair shows it.
    With `cutouts` (the painted folder), a third row shows each cut-out's cycle as 4 of its drawings: reviewers kept
    calling a dance "floating" and a clattering sounder "static" from stills (2026-11-06), and the agy reviewer can't
    watch video (tested 2026-11-06); the camera drifts in every shot, so onion-skin ghosts would smear the frame."""
    times, clip, out = sheet_times(seconds, shots), clip.resolve(), out.resolve()  # ffmpeg runs in out.parent
    sizes = json.loads((cutouts / "sizes.json").read_text(encoding="utf-8")) if cutouts and (cutouts / "sizes.json").exists() else {}
    cycling = [n for n, z in sizes.items() if z.get("steps", 1) > 1][:len(times)]
    S = Image.new("RGB", (324 * len(times), 576 * (2 + bool(cycling))), (40, 40, 44))
    for row, dt in enumerate((0, PAIR)):
        for k, t0 in enumerate(times):
            t = min(t0 + dt, seconds - .05)
            media_tools.ffmpeg("-y", "-ss", f"{t:.2f}", "-i", str(clip), "-frames:v", "1", "-vf", "scale=324:576", f"f{row}{k}.png", cwd=out.parent)
            im = Image.open(out.parent / f"f{row}{k}.png").convert("RGB")
            d = ImageDraw.Draw(im)
            d.rectangle((0, 0, 86, 26), fill=(0, 0, 0))
            d.text((6, 6), f"{t:.2f}s", fill="white")
            S.paste(im, (324 * k, 576 * row))
    for k, name in enumerate(cycling):  # 2 x 2 drawings of its cycle, in order
        n, tile = sizes[name]["steps"], Image.new("RGB", (324, 576), (205, 205, 200))
        for j in range(4):
            im = Image.open(cutouts / f"{name}_{j * n // 4}.png").convert("RGBA")
            im.thumbnail((158, 262))
            tile.paste(im, (4 + 162 * (j % 2) + (158 - im.width) // 2, 34 + 270 * (j // 2) + 262 - im.height), im)
        d = ImageDraw.Draw(tile)
        d.rectangle((0, 0, 324, 26), fill=(0, 0, 0))
        d.text((6, 6), f"{name}: its drawings cycle 1-2-3-4", fill="white")
        S.paste(tile, (324 * k, 576 * 2))
    S.save(out)
    return out
