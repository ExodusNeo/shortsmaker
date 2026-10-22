"""Bridge templates: each builds a whole structure from the parts kit with predictable part names
(span2_node3_bottom_left_gusset) and returns its parts in assembly order (piers, deck, members, details), so the
AI's build plan only names a template, its sizes and one spot. Runs inside Blender (bpy)."""

from mathutils import Vector

import look
import parts


class Bridge:
    """What a template built: parts by name and stage, the spans' x ranges, and the sizes the camera works from."""

    def __init__(self, st: dict):
        self.st = st
        self.spans, self.P = st["spans"], st["panels"]
        self.L, self.H, self.W = st["span_m"], st["height_m"], st["width_m"]
        self.length = self.L * self.spans
        self.clear = max(8.0, self.L * 0.12)  # deck height above the water
        self.deck_z = self.clear
        self.th = min(max(self.H * 0.035, 0.25), 3.0)  # member thickness
        self.stages: dict[str, list] = {"piers": [], "deck": [], "members": [], "details": []}
        self.objects: dict[str, object] = {}
        self.span_of: dict[str, int] = {}
        self.col = look.collection(__import__("bpy").context.scene, "structure")

    def add(self, stage: str, objs, span: int | None = None):
        for o in objs if isinstance(objs, list) else [objs]:
            self.stages[stage].append(o)
            self.objects[o.name] = o
            if span is not None:
                self.span_of[o.name] = span
        return objs

    def x0(self, s: int) -> float:  # s is 1-based
        return -self.length / 2 + (s - 1) * self.L

    def node(self, s: int, i: int, chord: str, side: str) -> Vector:
        y = (-1 if side == "left" else 1) * self.W / 2
        z = self.deck_z + (self.H if chord == "top" else 0)
        return Vector((self.x0(s) + i * self.L / self.P, y, z))

    @property
    def center(self) -> Vector:
        return Vector((0, 0, self.deck_z + self.H / 2))


def _piers_and_deck(b: Bridge) -> None:
    for k in range(b.spans + 1):
        x = -b.length / 2 + k * b.L
        b.add("piers", parts.pier(f"pier{k}", x, b.deck_z - 0.6, -2.0, b.W, b.col))
    for s in range(1, b.spans + 1):
        b.add("deck", parts.deck(f"span{s}_deck", b.x0(s), b.x0(s) + b.L, b.deck_z + 0.6, b.W * 0.96, 0.6, b.col), s)


def _truss_panel_members(b: Bridge, s: int, side: str, style: str) -> list:
    out, P, n = [], b.P, b.node
    for i in range(P):
        out.append(parts.member(f"span{s}_panel{i + 1}_bottom_{side}_chord", n(s, i, "bottom", side), n(s, i + 1, "bottom", side), b.th, "steel", b.col))
        out.append(parts.member(f"span{s}_panel{i + 1}_top_{side}_chord", n(s, i, "top", side), n(s, i + 1, "top", side), b.th, "steel", b.col))
        left_half = i < P / 2
        if style == "warren":
            a, c = ((n(s, i, "bottom", side), n(s, i + 1, "top", side)) if i % 2 == 0
                    else (n(s, i, "top", side), n(s, i + 1, "bottom", side)))
        elif style == "howe":
            a, c = ((n(s, i, "bottom", side), n(s, i + 1, "top", side)) if left_half
                    else (n(s, i, "top", side), n(s, i + 1, "bottom", side)))
        else:  # pratt and k: diagonals slope down toward the middle
            a, c = ((n(s, i, "top", side), n(s, i + 1, "bottom", side)) if left_half
                    else (n(s, i, "bottom", side), n(s, i + 1, "top", side)))
        if style == "k":
            mid = (n(s, i, "bottom", side) + n(s, i, "top", side)) / 2
            out.append(parts.member(f"span{s}_panel{i + 1}_{side}_diagonal", mid, n(s, i + 1, "top", side), b.th * 0.7, "steel", b.col))
            out.append(parts.member(f"span{s}_panel{i + 1}_{side}_diagonal_low", mid, n(s, i + 1, "bottom", side), b.th * 0.7, "steel", b.col))
        else:
            out.append(parts.member(f"span{s}_panel{i + 1}_{side}_diagonal", a, c, b.th * 0.75, "steel", b.col))
    for i in range(P + 1):
        if style != "warren" or i in (0, P):
            out.append(parts.member(f"span{s}_node{i}_{side}_vertical", n(s, i, "bottom", side), n(s, i, "top", side), b.th * 0.7, "steel", b.col))
    return out


def truss_bridge(st: dict) -> Bridge:
    b = Bridge(st)
    _piers_and_deck(b)
    for s in range(1, b.spans + 1):
        for side in ("left", "right"):
            b.add("members", _truss_panel_members(b, s, side, st["truss"]), s)
        for i in range(b.P + 1):
            for chord in ("bottom", "top"):
                for side in ("left", "right"):
                    b.add("details", parts.gusset_plate(f"span{s}_node{i}_{chord}_{side}_gusset", b.node(s, i, chord, side),
                                                        b.th * 3.2, -1 if side == "left" else 1, b.col), s)
            b.add("details", parts.member(f"span{s}_node{i}_top_strut", b.node(s, i, "top", "left"), b.node(s, i, "top", "right"),
                                          b.th * 0.6, "steel", b.col), s)
    return b


TEMPLATES = {"truss_bridge": truss_bridge}


def build(st: dict) -> Bridge:
    return TEMPLATES.get(st["template"], truss_bridge)(st)


def focus_object(b: Bridge, focus: dict):
    """The part the Short is about, by the plan's spot; the gusset at that joint when the exact part doesn't exist."""
    at = focus["at"]
    s, p, chord, side = at["span"], at["panel"], at["chord"], at["side"]
    names = {"gusset_plate": f"span{s}_node{p}_{chord}_{side}_gusset",
             "chord": f"span{s}_panel{p}_{chord}_{side}_chord",
             "diagonal": f"span{s}_panel{p}_{side}_diagonal",
             "vertical": f"span{s}_node{p}_{side}_vertical"}
    for name in (names.get(focus["part"]), f"span{s}_node{p}_{chord}_{side}_gusset", f"span{s}_node{p}_bottom_{side}_gusset"):
        if name and name in b.objects:
            return b.objects[name]
    return next(o for o in b.stages["details"] + b.stages["members"] + b.stages["deck"])
