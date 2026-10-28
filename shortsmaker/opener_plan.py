"""Opener staging plans (2026-10-27; shot templates 2026-10-28): for channels with `opener: blender`, the planner AI
picks one of the shot templates in blender/shot_templates.json for each Short's strangest moment and fills its slots
(who, which library models, a few picks). The template's staging was built and checked by eye once, so the AI never
writes beats or Blender code (free-composed plans passed 0 of ~10 live runs). Every value is checked against the
template and blender/opener_tables.json. No template fits, or no usable fill after one retry: the Short gets a CHECK
note (s["opener_check"]) and its motion-graphic opener plays."""

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
ROLES, PEOPLE_MOVES = TABLES["roles"], TABLES["people_moves"]  # people openers (part 2, 2026-10-27)
PIECES = re.compile(r"^(\d+)-(\d+)$")
TEMPLATES = {k: v for k, v in json.loads((config.ROOT / "blender" / "shot_templates.json").read_text(encoding="utf-8")).items()
             if not k.startswith("_")}
SLOT = re.compile(r"\$(\w+)(?:\.(find|size_m))?")

DEFAULT_RULES = """Show the story's strangest moment, the one its first line describes, as a 2-3 second animation
made from one shot template. Models are free low-poly library models and cartoon people by era and role (no faces).
Name models plainly, as a free low-poly library titles them ("truck", "house", "rocks"). Pick no template when none
shows the moment itself: a motion graphic opens the Short instead, which is better than a 3D shot of something else."""

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


def _takeable(b: dict, actors: list[dict], beats: list[dict]) -> bool:
    """pick_up's "take" lies on the ground: a thing of at most 1 m (not on anything), or a person's prop after their
    earlier drop_prop. The first pick_up only bent where the con artist stood (Eiffel Short, 2026-10-28)."""
    a = next((x for x in actors if x["id"] == b.get("take")), None)
    if a is None or a["id"] == b.get("actor"):
        return False
    if "person" in a:
        return bool(a.get("prop")) and any(d.get("move") == "drop_prop" and d.get("actor") == a["id"]
                                           and _num(d.get("at"), 0, b["at"]) and d["at"] < b["at"] for d in beats)
    return a.get("on") in (None, "ground") and _size(a.get("size_m")) and a["size_m"] <= 1.0


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
        if "person" in a:  # a person: a role from the table and an optional prop find text
            if a["person"] not in ROLES or ("prop" in a and not str(a["prop"] or "").strip()) \
                    or ("prop_size_m" in a and not _size(a["prop_size_m"])):
                return None
        elif not str(a.get("find") or "").strip() or not _size(a.get("size_m")):
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
    find = {a["id"]: a["find"] for a in actors if "person" not in a}
    people = {a["id"] for a in actors if "person" in a}
    for b in beats:
        if not isinstance(b, dict) or not _num(b.get("at"), 0, LIMITS["max_at_s"]):
            return None
        way = b.get("toward", "left")  # a direction as seen, or another actor to go at
        if way not in TOWARDS and (way not in ids or way == b.get("actor")):
            return None
        if b.get("actor") in people:  # people move by their clips only
            if b.get("move") not in PEOPLE_MOVES:
                return None
            if b["move"] == "pick_up" and not _takeable(b, actors, beats):
                return None
            continue
        if b.get("move") not in MOVES:
            return None
        gait = next((a.get("gait") for a in actors if a["id"] == b.get("actor")), None)
        if b["move"] == "roll" and gait == "wheeled":  # roll is a tumble: the people run's car tipped onto its nose
            return None
        if b.get("style", "normal") not in STYLES:
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




def _keep(cond: str, fill: dict) -> bool:
    """A template item's "if": "slot" (the slot is set) or "slot=a|b" (it is one of those)."""
    name, _, vals = cond.partition("=")
    return str(fill.get(name)) in vals.split("|") if vals else bool(fill.get(name))


def _sub(node, fill: dict):
    """The template's plan with its "$slot" values filled in and its "if" items kept or dropped."""
    if isinstance(node, dict):
        return {k: _sub(v, fill) for k, v in node.items() if k != "if"}
    if isinstance(node, list):
        return [_sub(x, fill) for x in node if not (isinstance(x, dict) and "if" in x and not _keep(x["if"], fill))]
    if isinstance(node, str):
        m = SLOT.fullmatch(node)
        if m:
            return fill[m[1]][m[2]] if m[2] else fill[m[1]]
        return SLOT.sub(lambda m: str(fill[m[1]]), node)
    return node


def _slot_ok(spec: dict, v) -> bool:
    kind = spec["kind"]
    if v is None:
        return bool(spec.get("optional"))
    if kind == "role":
        return v in ROLES
    if kind == "prop":
        return isinstance(v, str) and bool(v.strip())
    if kind == "pick":
        return not isinstance(v, bool) and v in spec["of"]
    return (isinstance(v, dict) and isinstance(v.get("find"), str) and bool(v["find"].strip())
            and _num(v.get("size_m"), *spec["size_m"]) and (kind != "tool" or tool_kind(v["find"]) is not None)
            and (not spec.get("words") or bool(set(v["find"].lower().split()) & set(spec["words"]))))


def fill_template(reply) -> dict | None:
    """The plan from the planner's {"template", "moment", "set", "fill"}, or None when any value is outside the
    template or the tables. Nothing is patched: a bad fill is asked for again."""
    if not isinstance(reply, dict) or reply.get("template") not in TEMPLATES or not str(reply.get("moment") or "").strip():
        return None
    tpl, fill, st = TEMPLATES[reply["template"]], reply.get("fill"), reply.get("set")
    if not isinstance(fill, dict) or not isinstance(st, dict) or st.get("ground") not in tpl["grounds"] \
            or st.get("light", "day") not in LIGHTS or not isinstance(st.get("backdrop") or "", str):
        return None
    fill = dict(fill)
    for name, spec in tpl["slots"].items():
        if spec["kind"] == "pick" and fill.get(name) is None:  # a pick only its "if" item uses may be left out
            fill[name] = spec["of"][0]
        if not _slot_ok(spec, fill.get(name)):
            return None
    backdrop = str(st.get("backdrop") or "").strip()
    plan = {"buildable": True, "moment": str(reply["moment"]).strip()[:300], "template": reply["template"],
            "set": {"ground": st["ground"], "light": st.get("light", "day"),
                    "backdrop": [{"find": backdrop, "size_m": 8}] if backdrop else []},
            **_sub(tpl["plan"], fill)}
    return clean_opener(plan)


def _templates_text() -> str:
    def slot(name, sp):
        extra = (f" {sp['size_m'][0]}-{sp['size_m'][1]} m" if "size_m" in sp else "") + \
                (f" one of {sp['of']}" if "of" in sp else "") + (" or null" if sp.get("optional") else "")
        return f"{name} ({sp['kind']}{extra}{': ' + sp['note'] if sp.get('note') else ''})"
    return "\n".join(f"- {k}: {t['shows']}. Grounds {t['grounds']}. Slots: " +
                     "; ".join(slot(n, sp) for n, sp in t["slots"].items()) for k, t in TEMPLATES.items())


REPLY = """A thing slot is {"find": "sack", "size_m": 1.2} (its real size in metres, inside the slot's range); a tool slot
is a thing whose find names one of """ + json.dumps(list(TOOLS)) + """; a role slot is one of """ + json.dumps(list(ROLES)) + """;
a prop slot is a find text. set.light one of """ + json.dumps(list(LIGHTS)) + """; set.backdrop is one big thing behind
the action ("warehouse", "barn") or null.
Reply with ONLY JSON: {"shorts": [{"index": 0, "template": "falls_on", "moment": "one sentence: what the animation shows",
"set": {"ground": "wood floor", "light": "day", "backdrop": "warehouse"},
"fill": {"victim": "businessman", "thing": {"find": "sack", "size_m": 1.2}, "witness": "farmer", "witness_does": "cheer"}}]}
For a moment no template shows: {"index": 0, "template": null, "why": "..."}"""


def plan_openers(shorts: list[dict], ch: dict) -> None:
    """One AI call picks and fills a shot template for every Short (s["opener"], and s["opener_fill"] for model
    swaps); unusable fills are asked for once more. A Short without one gets s["opener_check"]: its motion-graphic
    opener plays."""
    def ask(idx: list[int], note: str = "") -> dict:
        rows = [{"index": i, "title": shorts[i]["title"],
                 "scene_1": shorts[i]["scenes"][0]["narration"],
                 "narration": " ".join(sc["narration"] for sc in shorts[i]["scenes"]),
                 "research": " ".join(str(t) for t in (shorts[i].get("research") or {}).values())[:4000]} for i in idx]
        data = llm.ask_ai(f"""You are the animation director of a faceless YouTube Shorts channel. Niche: {ch.get('niche', '')}.
Every Short opens on a short 3D animation of its strangest moment, played under the first line. {note}
{session.RULES.get("Opener") or DEFAULT_RULES}
Shot templates: the staging is fixed and proven; you only pick one and fill its slots. Pick one only when it shows
the moment itself (who, what and what happens), else none:
{_templates_text()}
{REPLY}
Shorts: {json.dumps(rows, ensure_ascii=False)}""", fatal=False)
        got = data.get("shorts") if isinstance(data, dict) else None
        return {r["index"]: r for r in got or [] if isinstance(r, dict) and r.get("index") in idx}

    todo = list(range(len(shorts)))
    for attempt in range(2):
        replies = ask(todo, "" if not attempt else "Your last reply for these could not be used: every slot must be filled "
                                                   "from its allowed values.")
        for i in list(todo):
            r = replies.get(i)
            if isinstance(r, dict) and "template" in r and r["template"] is None:
                shorts[i]["opener_check"] = f"opener: no template fits ({str(r.get('why') or 'no reason given')[:200]})"
                todo.remove(i)
                continue
            plan = fill_template(r)
            if plan:
                shorts[i]["opener"], shorts[i]["opener_fill"], shorts[i]["opener_check"] = plan, r, None
                todo.remove(i)
        if not todo:
            break
    for i in todo:
        shorts[i]["opener_check"] = "opener: no usable template fill"


def swap_models(short: dict, unfound: list[str]) -> dict | None:
    """The same template refilled with more common things for the models no library has (the first people run asked
    for a "ww2 armored car"), or None."""
    data = llm.ask_ai(f"""This filled shot template stages the opener of the Short "{short.get('title', '')}":
{json.dumps(short.get('opener_fill'), ensure_ascii=False)}
No free library has a model for: {json.dumps(unfound, ensure_ascii=False)}. Replace each with a more common thing that
reads the same (a truck for an armoured car) or, for a backdrop, null. Keep everything else.
{REPLY.split("Reply with ONLY JSON")[0]}Reply with ONLY the same JSON object (template, moment, set, fill).""", fatal=False)
    plan = fill_template(data)
    if plan:
        short["opener_fill"] = data
    return plan
