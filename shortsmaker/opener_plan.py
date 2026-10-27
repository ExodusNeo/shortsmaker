"""Opener staging plans (2026-10-27): for channels with `opener: blender`, the planner AI stages each Short's
strangest moment as a short Blender animation for scene 1: which library models, where they stand, and moves from a
fixed list. Every value is checked against blender/opener_tables.json (shared with blender/moves.py); the AI never
writes Blender code. A plan that can't be used is asked for once more; a moment the moves can't show is
`buildable: false`. Either way the Short keeps today's scene 1 and gets a CHECK note (s["opener_check"])."""

import json
import math
import re

from shortsmaker import config, llm, session

TABLES = json.loads((config.ROOT / "blender" / "opener_tables.json").read_text(encoding="utf-8"))
GROUNDS, LIGHTS, FACINGS, ANGLES = TABLES["grounds"], TABLES["lights"], TABLES["facings"], TABLES["angles"]
MOVES, TOOLS, GAITS, OUTCOMES, CUT_FACE = (TABLES["moves"], TABLES["tools"], TABLES["gaits"], TABLES["outcomes"],
                                           TABLES["cut_face"])
STYLES, TOWARDS, STROKE_ANGLES, LIMITS = TABLES["styles"], TABLES["towards"], TABLES["stroke_angles"], TABLES["limits"]
ACTOR_MOVES = {"fall", "topple", "hop_off", "walk", "fly_off", "scatter", "sink", "roll", "push"}  # cut: tool+target
PIECES = re.compile(r"^(\d+)-(\d+)$")

DEFAULT_RULES = """Stage the story's strangest moment, the one its first line describes, as a 2-3 second animation.
It is built from free low-poly library models (animals, objects, vehicles, food, tools, buildings, plants), so
it can't show people: if the moment needs a person on screen, answer buildable false and say why. Frame 0 must
already show the subject and the threat (the raised tool, the drop, the wave); the first beat starts by 1.0 s."""

FORMAT = """Reply with ONLY JSON: {"shorts": [{"index": 0, "buildable": true, "moment": "...",
"set": {"ground": "dirt", "backdrop": [{"find": "red barn", "size_m": 8}], "light": "day"},
"actors": [{"id": "rooster", "find": "rooster", "size_m": 0.55, "on": "stump", "facing": "right", "gait": "bird"},
           {"id": "stump", "find": "tree stump", "size_m": 1.2}, {"id": "axe", "find": "axe", "size_m": 0.8}],
"beats": [{"move": "cut", "tool": "axe", "target": "rooster", "at": 0.55,
           "strokes": [{"through": "neck", "angle": "level"}],
           "expect": [{"piece": "head", "share": 0.15, "then": "fly_off"}, {"piece": "rest", "then": "stay"}]},
          {"move": "hop_off", "actor": "rooster", "at": 1.3, "style": "stagger"},
          {"move": "walk", "actor": "rooster", "at": 1.8, "toward": "left", "style": "stagger", "ends": {"on": "ground"}}],
"camera": {"angle": "three_quarter", "follow": "rooster"}}]}
For a moment the moves can't show: {"index": 0, "buildable": false, "why": "..."}"""


def _num(v, lo, hi) -> bool:
    return not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v) and lo <= v <= hi


def _size(v) -> bool:
    return _num(v, *LIMITS["size_m"])


def _stroke(st) -> bool:
    if not isinstance(st, dict) or (st.get("angle") is not None and st["angle"] not in STROKE_ANGLES):
        return False
    kinds = [k for k in ("through", "at_fraction", "rows", "mince") if k in st]
    if len(kinds) != 1:
        return False
    k = kinds[0]
    if k == "through":
        return isinstance(st[k], str) and bool(st[k].strip())
    if k == "at_fraction":
        return _num(st[k], 0.0, 1.0)
    if k == "rows":
        return _num(st[k], 1, 40) and (st.get("cols") is None or _num(st["cols"], 1, 40))
    return _num(st[k], 1, LIMITS["max_pieces"])


def _expect(items) -> bool:
    if not isinstance(items, list) or not items:
        return False
    for e in items:
        if not isinstance(e, dict) or e.get("then") not in OUTCOMES:
            return False
        if "pieces" in e:
            m = PIECES.match(str(e["pieces"]))
            if not m or not 1 <= int(m.group(1)) <= int(m.group(2)) <= LIMITS["max_pieces"]:
                return False
        elif not (isinstance(e.get("piece"), str) and e["piece"].strip()) \
                or ("share" in e and not _num(e["share"], 0.001, 0.999)):
            return False
    return True


def tool_kind(find: str) -> str | None:
    """The tool-table row a model's search text names ("kitchen knife" -> "knife"), longest name first."""
    text = f" {str(find).lower()} "
    return next((TOOLS[k] for k in sorted(TOOLS, key=len, reverse=True) if f" {k} " in text), None)


def clean_opener(raw) -> dict | None:
    """The plan when every value is in its table and every name exists, else None. Nothing is filled in or changed:
    a plan the AI got wrong goes back to it (fix_plan), never silently patched."""
    if not isinstance(raw, dict) or raw.get("buildable") is not True or not str(raw.get("moment") or "").strip():
        return None
    st = raw.get("set")
    if not isinstance(st, dict) or st.get("ground") not in GROUNDS or st.get("light", "day") not in LIGHTS:
        return None
    if not all(isinstance(b, dict) and str(b.get("find") or "").strip() and _size(b.get("size_m"))
               for b in st.get("backdrop") or []):
        return None
    actors = raw.get("actors")
    if not isinstance(actors, list) or not actors:
        return None
    ids = [a.get("id") if isinstance(a, dict) else None for a in actors]
    if not all(isinstance(i, str) and i for i in ids) or len(set(ids)) != len(ids):
        return None
    for a in actors:
        if not str(a.get("find") or "").strip() or not _size(a.get("size_m")):
            return None
        if a.get("on") not in (None, "ground", *ids) or a.get("facing", "right") not in FACINGS \
                or a.get("gait", "object") not in GAITS:
            return None
    on = {a["id"]: a.get("on") for a in actors}
    for a in ids:  # standing on itself, or A on B on A, would never be placed
        seen, cur = set(), a
        while on.get(cur) not in (None, "ground"):
            if cur in seen:
                return None
            seen.add(cur)
            cur = on[cur]
    beats = raw.get("beats")
    if not isinstance(beats, list) or not beats:
        return None
    find = {a["id"]: a["find"] for a in actors}
    for b in beats:
        if not isinstance(b, dict) or b.get("move") not in MOVES or not _num(b.get("at"), 0, LIMITS["max_at_s"]):
            return None
        if b.get("style", "normal") not in STYLES or b.get("toward", "left") not in TOWARDS:
            return None
        if b.get("ends") is not None and (not isinstance(b["ends"], dict) or b["ends"].get("on") not in ("ground", *ids)):
            return None
        if b["move"] == "cut":
            if b.get("tool") not in find or b.get("target") not in find or not tool_kind(find[b["tool"]]):
                return None
            # one stroke group per cut (rows + cols is one group): moves.cut builds no more yet
            if not isinstance(b.get("strokes"), list) or len(b["strokes"]) != 1 or not _stroke(b["strokes"][0]) \
                    or not _expect(b.get("expect")):
                return None
            if "through" in b["strokes"][0] and not any(e.get("piece") == "rest" or "pieces" in e for e in b["expect"]):
                return None  # the part left behind must be named too
        elif b.get("actor") not in find or (b["move"] == "push" and b.get("target") not in find):
            return None
    if min(b["at"] for b in beats) > LIMITS["first_beat_s"]:
        return None
    cam = raw.get("camera")
    if not isinstance(cam, dict) or cam.get("angle") not in ANGLES or cam.get("follow") not in (None, *ids):
        return None
    return raw


def _tables_text() -> str:
    return (f"Allowed values: set.ground {list(GROUNDS)}; set.light {list(LIGHTS)}; actor facing {FACINGS}; "
            f"actor gait (how it moves) {list(GAITS)}; moves {MOVES}; cut tools (an actor whose find names one) "
            f"{list(TOOLS)}; stroke angle {STROKE_ANGLES}; one stroke is {{\"through\": \"neck\"}} or "
            f"{{\"at_fraction\": 0.5}} or {{\"rows\": 8}} (slices) or {{\"rows\": 6, \"cols\": 6}} (dice) or "
            f"{{\"mince\": 50}}; expect items {{\"piece\": name, \"share\": 0-1, \"then\": outcome}} or "
            f"{{\"pieces\": \"40-60\", \"then\": outcome}}, outcomes {OUTCOMES}; style {STYLES}; toward {TOWARDS}; "
            f"camera.angle {ANGLES}; size_m {LIMITS['size_m'][0]}-{LIMITS['size_m'][1]}; at = seconds into the "
            f"scene, 0-{LIMITS['max_at_s']}, the first beat by {LIMITS['first_beat_s']} s; at most "
            f"{LIMITS['max_pieces']} pieces in all.")


def plan_openers(shorts: list[dict], ch: dict) -> None:
    """One AI call stages every Short's opener (s["opener"]); unusable plans are asked for once more. A Short
    without a usable plan gets s["opener_check"] and keeps today's scene 1."""
    def ask(idx: list[int], note: str = "") -> dict:
        rows = [{"index": i, "title": shorts[i]["title"],
                 "scene_1": shorts[i]["scenes"][0]["narration"],
                 "narration": " ".join(sc["narration"] for sc in shorts[i]["scenes"]),
                 "research": " ".join(str(t) for t in (shorts[i].get("research") or {}).values())[:4000]} for i in idx]
        data = llm.ask_ai(f"""You are the animation director of a faceless YouTube Shorts channel. Niche: {ch.get('niche', '')}.
Every Short opens on a short 3D animation of its strangest moment, played under the first line. {note}
{session.RULES.get("Opener") or DEFAULT_RULES}
{_tables_text()}
Shorts: {json.dumps(rows, ensure_ascii=False)}
{FORMAT}""", fatal=False)
        got = data.get("shorts") if isinstance(data, dict) else None
        return {r["index"]: r for r in got or [] if isinstance(r, dict) and r.get("index") in idx}

    todo = list(range(len(shorts)))
    for attempt in range(2):
        replies = ask(todo, "" if not attempt else "Your last plan for these could not be used: send a full plan.")
        for i in list(todo):
            r = replies.get(i)
            if isinstance(r, dict) and r.get("buildable") is False:
                shorts[i]["opener_check"] = f"opener: not buildable ({str(r.get('why') or 'no reason given')[:200]})"
                todo.remove(i)
                continue
            plan = clean_opener({k: v for k, v in r.items() if k != "index"} if isinstance(r, dict) else None)
            if plan:
                shorts[i]["opener"], shorts[i]["opener_check"] = plan, None
                todo.remove(i)
        if not todo:
            break
    for i in todo:
        shorts[i]["opener_check"] = "opener: no usable plan"


def fix_plan(short: dict, failures: list[str], seconds: float | None = None, scaled: dict | None = None) -> dict | None:
    """The planner fixes its own plan after the checks or the review found these failures; None if unusable. It is
    told scene 1's real length and the beat times as played (the voice can make the scene shorter than planned)."""
    played = (f"Scene 1 is {seconds:.1f} seconds long; the beats were fitted into it and played like this: "
              f"{json.dumps(scaled, ensure_ascii=False)}\n") if seconds is not None and scaled is not None else ""
    data = llm.ask_ai(f"""You staged this 3D opener for the Short "{short.get('title', '')}". Rendering it showed these
problems: {json.dumps(failures, ensure_ascii=False)}
{played}
Fix the plan so none of them happens again (move things apart, change the tool's start, the timing, the camera, or
the expected pieces). Keep the same moment.
{_tables_text()}
Plan: {json.dumps(short.get('opener'), ensure_ascii=False)}
Reply with ONLY the fixed plan as JSON, in the same format.""", fatal=False)
    return clean_opener(data)
