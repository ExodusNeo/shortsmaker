"""Blender build plans (2026-10-22): for channels with `visuals: blender`, the engineer AI plans each Short as a 3D
build (a bridge template, the part that failed, how it failed, a camera beat per scene). Every value is checked
against the tables below; a plan that can't be used is asked for once more, then replaced by a generic one, so
every scene is still drawn. blender/build_scene.py reads the cleaned plan; the tables here are its vocabulary."""

import json
import math

from shortsmaker import llm, picture_pool, session

# allowed values, the default first
TEMPLATES = ("truss_bridge", "girder_bridge", "suspension_bridge", "cable_stayed_bridge", "eyebar_chain_bridge")
TRUSSES = ("warren", "pratt", "howe", "k")
DECKS = ("road", "rail")
SETTINGS = ("river", "valley", "bay")
FASTENERS = ("rivet", "bolt", "pin", "weld")  # never screws: bridges clamp steel through holes or melt it together
FOCUS_PARTS = ("gusset_plate", "chord", "diagonal", "vertical", "eyebar", "pin_joint", "hanger", "cable", "bearing",
               "pier", "fastener_group")
CHORDS = ("bottom", "top")
SIDES = ("left", "right")
FAILURES = ("bend", "crack", "shear", "sway")
THENS = ("none", "collapse_span")
SCALES = ("car", "train", "people")
BEATS = ("wide", "orbit", "build", "zoom", "failure", "aftermath", "failure_preview")
RANGES = {"spans": (1, 5, 1), "span_m": (20, 1300, 100), "height_m": (2, 250, 15), "width_m": (4, 60, 15)}
GENERIC = "generic build plan: the engineer's plan was unusable"


def pick(v, allowed: tuple) -> str:
    return v if v in allowed else allowed[0]


def clamp(v, lo, hi, default):
    """A number in [lo, hi] (whole numbers stay whole), or the default for anything that isn't a number."""
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):  # JSON allows NaN
        return default
    return min(max(v, lo), hi) if isinstance(lo, float) or isinstance(v, int) else min(max(round(v), lo), hi)


def panels(structure: dict) -> int:
    """Truss panels per span: about square panels, 4-16 of them."""
    return min(max(round(structure["span_m"] / max(structure["height_m"], 1)), 4), 16)


def ending(n: int) -> list[str]:
    """The last part of every Short: zoom in, the failure, what it left behind."""
    k = min(max(2, n // 3), n)  # a 1-scene Short still gets one beat
    part = max(1, k // 3)
    return (["zoom"] * part + ["failure"] * part + ["aftermath"] * k)[:k]


def clean_build(raw, n_scenes: int) -> dict | None:
    """The engineer's plan with every value checked: unknown values get the default, numbers are clamped, every scene
    gets a beat (an unlisted scene repeats the one before it), and there is always a zoom before a failure.
    None when it can't be used at all (no structure)."""
    if not isinstance(raw, dict) or not isinstance(raw.get("structure"), dict):
        return None
    s = raw["structure"]
    st = {"template": pick(s.get("template"), TEMPLATES), "truss": pick(s.get("truss"), TRUSSES),
          **{k: clamp(s.get(k), *RANGES[k]) for k in RANGES},
          "deck": pick(s.get("deck"), DECKS), "setting": pick(s.get("setting"), SETTINGS),
          "fastener": pick(s.get("fastener"), FASTENERS)}
    st["spans"] = int(st["spans"])
    st["panels"] = panels(st)
    f = raw.get("focus") if isinstance(raw.get("focus"), dict) else {}
    at = f.get("at") if isinstance(f.get("at"), dict) else {}
    label = f.get("label")
    focus = {"part": pick(f.get("part"), FOCUS_PARTS),
             "at": {"span": clamp(at.get("span"), 1, st["spans"], (st["spans"] + 1) // 2),
                    "panel": clamp(at.get("panel"), 1, st["panels"], (st["panels"] + 1) // 2),
                    "chord": pick(at.get("chord"), CHORDS), "side": pick(at.get("side"), SIDES)},
             "label": " ".join(label.split()).upper()[:40] or None if isinstance(label, str) else None}
    fl = raw.get("failure") if isinstance(raw.get("failure"), dict) else {}
    failure = {"kind": pick(fl.get("kind"), FAILURES), "then": pick(fl.get("then"), THENS),
               "span": clamp(fl.get("span"), 1, st["spans"], focus["at"]["span"])}
    scale = list(dict.fromkeys(x for x in raw.get("scale") or [] if x in SCALES)) if isinstance(raw.get("scale"), list) else []
    beats: list[str | None] = [None] * n_scenes
    for e in raw.get("scenes") or [] if isinstance(raw.get("scenes"), list) else []:
        k = e.get("scene") if isinstance(e, dict) else None
        if isinstance(k, int) and not isinstance(k, bool) and 1 <= k <= n_scenes and e.get("beat") in BEATS:
            beats[k - 1] = e["beat"]
    for i in range(n_scenes):
        beats[i] = beats[i] or (beats[i - 1] if i else "failure_preview")
    if beats and beats[0] == "failure":  # a failure that opens the Short is the hook's preview, not the story's
        beats[0] = "failure_preview"
    if not ("zoom" in beats and "failure" in beats and beats.index("zoom") < beats.index("failure")):
        tail = ending(n_scenes)
        beats[n_scenes - len(tail):] = tail
    return {"structure": st, "focus": focus, "failure": failure, "scale": scale, "beats": beats}


def default_build(n_scenes: int) -> dict:
    """A plan that always works: a truss bridge whose mid-span gusset plate bends."""
    beats = ["failure_preview", "wide"] + ["build"] * max(0, n_scenes - 2)
    plan = clean_build({"structure": {}, "scale": ["car"],
                        "scenes": [{"scene": k + 1, "beat": b} for k, b in enumerate(beats[:n_scenes])]}, n_scenes)
    return {**plan, "generic": True}


FORMAT = """Reply with ONLY JSON: {"shorts": [{"index": 0,
"structure": {"template": "truss_bridge", "truss": "warren", "spans": 3, "span_m": 140, "height_m": 18,
              "width_m": 20, "deck": "road", "setting": "river", "fastener": "rivet"},
"focus": {"part": "gusset_plate", "at": {"span": 2, "panel": 3, "chord": "bottom", "side": "left"},
          "label": "GUSSET PLATE U10 · 1/2 INCH"},
"failure": {"kind": "bend", "then": "collapse_span", "span": 2},
"scale": ["car", "people"],
"scenes": [{"scene": 1, "beat": "failure_preview"}, {"scene": 2, "beat": "wide"}, {"scene": 3, "beat": "build"}]}]}"""


def plan_builds(shorts: list[dict], ch: dict) -> None:
    """The engineer step: one AI call plans every Short's build (s["build"]); Shorts whose plan can't be used are
    asked for once more, then get default_build and a CHECK note (s["build_check"]). Scenes are drawn whole, so
    they carry no motion graphic, callout, person card, photo look or special scene change."""
    def ask(idx: list[int], note: str = "") -> dict:
        rows = [{"index": i, "title": shorts[i]["title"],
                 "scenes": [{"scene": k + 1, "narration": sc["narration"]} for k, sc in enumerate(shorts[i]["scenes"])],
                 "research": " ".join(str(t) for t in (shorts[i].get("research") or {}).values())[:6000]} for i in idx]
        data = llm.ask_ai(f"""You are the engineer of a YouTube Shorts channel drawn entirely in 3D (Blender, an ink
technical-manual look). Niche: {ch.get('niche', '')}. Plan the 3D build of every Short below so each scene shows
what its narration says. {note}
Allowed values (anything else is replaced by the first one):
- structure.template: {list(TEMPLATES)}; truss: {list(TRUSSES)}; spans 1-5; span_m 20-1300; height_m 2-250;
  width_m 4-60; deck: {list(DECKS)}; setting: {list(SETTINGS)}; fastener: {list(FASTENERS)} (the real bridge's, by era)
- focus.part: {list(FOCUS_PARTS)}; at: span (1..spans), panel, chord {list(CHORDS)}, side {list(SIDES)};
  label: what the drawn label on the part says, 40 characters at most, or null
- failure.kind: {list(FAILURES)}; then: {list(THENS)}; span: which span collapses
- scale: any of {list(SCALES)}
- scenes[].beat, one per scene: {list(BEATS)}
{session.RULES["Build plan"]}
Shorts: {json.dumps(rows, ensure_ascii=False)}
{FORMAT}""", fatal=False)
        got = data.get("shorts") if isinstance(data, dict) else None
        return {r["index"]: r for r in got or [] if isinstance(r, dict) and r.get("index") in idx}

    todo = list(range(len(shorts)))
    for attempt in range(2):
        replies = ask(todo, "" if not attempt else "Your last plan for these could not be used: send a full plan.")
        for i in list(todo):
            build = clean_build(replies.get(i), len(shorts[i]["scenes"]))
            if build:
                shorts[i]["build"], shorts[i]["build_check"] = build, None
                todo.remove(i)
        if not todo:
            break
    for i in todo:
        shorts[i]["build"], shorts[i]["build_check"] = default_build(len(shorts[i]["scenes"])), GENERIC
    for s in shorts:  # no photo look or special scene change either: the Python renderer hard-cuts drawn scenes
        s["look"] = s["invented_transition"] = s["invented_overlay"] = None
        for sc in s["scenes"]:
            sc["full"] = sc["graphic"] = sc["person"] = None
            sc["transition"] = "fade"


def thumbnail_order(short: dict, rows: list[dict]) -> list[int]:
    """Pool indexes to try for the thumbnail's real photo, best first: usable pictures the picture list marked as
    openers, then the other usable ones. Film frames are left out (their URL is the video file)."""
    usable = [e["n"] - 1 for e in short.get("catalog") or [] if picture_pool.is_usable(e)]
    usable = [k for k in usable if 0 <= k < len(rows) and not rows[k].get("film")]
    hooks = {e["n"] - 1 for e in short.get("catalog") or [] if e.get("hook")}
    return [k for k in usable if k in hooks] + [k for k in usable if k not in hooks]
