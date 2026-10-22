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


def _edge_girders(b: Bridge, s: int, depth: float) -> None:
    """The deck's two edge girders (named like truss bottom chords) with splice plates at every panel point."""
    for side in ("left", "right"):
        for i in range(b.P):
            a, c = b.node(s, i, "bottom", side), b.node(s, i + 1, "bottom", side)
            b.add("members", parts.member(f"span{s}_panel{i + 1}_bottom_{side}_chord", a - Vector((0, 0, depth / 2)),
                                          c - Vector((0, 0, depth / 2)), b.th, "steel", b.col, depth=depth), s)
        for i in range(b.P + 1):
            b.add("details", parts.gusset_plate(f"span{s}_node{i}_bottom_{side}_gusset",
                                                b.node(s, i, "bottom", side) - Vector((0, 0, depth / 2)), depth * 0.9,
                                                -1 if side == "left" else 1, b.col), s)


def girder_bridge(st: dict) -> Bridge:
    """Deck on deep plate girders (four lines of them), spliced at every panel point."""
    b = Bridge(st)
    _piers_and_deck(b)
    depth = min(max(b.L / 18, 1.5), max(b.H, 1.5))
    for s in range(1, b.spans + 1):
        _edge_girders(b, s, depth)
        for y in (-0.15, 0.15):
            b.add("members", parts.member(f"span{s}_inner_girder_{y}", Vector((b.x0(s), y * b.W, b.deck_z - depth / 2)),
                                          Vector((b.x0(s) + b.L, y * b.W, b.deck_z - depth / 2)), b.th, "steel", b.col,
                                          depth=depth), s)
    return b


def _towers(b: Bridge, height: float, at: list[float]) -> list[tuple[float, float]]:
    tops = []
    for k, x in enumerate(at):
        b.add("members", parts.tower(f"tower{k}", x, b.deck_z - 1, height + 1, b.W * 1.1, b.col))
        tops.append((x, b.deck_z + height))
    return tops


def _sag_points(x0: float, x1: float, z_top: float, z_low: float, n: int, y: float) -> list[Vector]:
    xm, half = (x0 + x1) / 2, (x1 - x0) / 2
    return [Vector((x0 + (x1 - x0) * k / n, y, z_top - (z_top - z_low) * (1 - ((x0 + (x1 - x0) * k / n - xm) / half) ** 2)))
            for k in range(n + 1)]


def _hung_deck(b: Bridge, tower_h: float, link: str) -> Bridge:
    """Suspension or eyebar-chain bridge: towers at the piers, a main cable (or a chain of eyebars on pins) sagging
    between them, hangers down to the deck's edge girders at every panel point."""
    _piers_and_deck(b)
    at = [-b.length / 2 + k * b.L for k in range(b.spans + 1)]
    tops = dict(_towers(b, tower_h, at[1:-1] if b.spans > 2 else at))
    for s in range(1, b.spans + 1):
        _edge_girders(b, s, max(b.L / 60, 1.2))
        x0, x1 = b.x0(s), b.x0(s) + b.L
        z0 = tops.get(x0, b.deck_z + tower_h * 0.25)
        z1 = tops.get(x1, b.deck_z + tower_h * 0.25)
        for side in ("left", "right"):
            y = (-1 if side == "left" else 1) * b.W / 2
            pts = _sag_points(x0, x1, max(z0, z1), b.deck_z + tower_h * 0.12, b.P, y)
            if z0 != z1:  # a side span: straight-ish from the tower down to the anchorage
                pts = [Vector((p.x, y, z0 + (z1 - z0) * k / b.P - tower_h * 0.1 * (1 - abs(2 * k / b.P - 1))))
                       for k, p in enumerate(pts)]
            for p in range(b.P):
                if link == "eyebar":
                    b.add("members", parts.eyebar(f"span{s}_panel{p + 1}_{side}_eyebar", pts[p], pts[p + 1], b.th * 2, b.col), s)
                else:
                    b.add("members", parts.main_cable(f"span{s}_panel{p + 1}_{side}_cable", [pts[p], pts[p + 1]], b.th * 0.6, b.col), s)
            for i in range(b.P + 1):
                if link == "eyebar":
                    b.add("details", parts.cylinder(f"span{s}_node{i}_{side}_pin", pts[i] - Vector((0, 0.9, 0)),
                                                    pts[i] + Vector((0, 0.9, 0)), b.th * 0.8, "dark", b.col), s)
                if 0 < i < b.P:
                    b.add("details", parts.hanger(f"span{s}_node{i}_{side}_hanger", pts[i], b.node(s, i, "bottom", side),
                                                  b.th * 0.18, b.col), s)
    return b


def suspension_bridge(st: dict) -> Bridge:
    b = Bridge(st)
    return _hung_deck(b, max(b.H, b.L * 0.11), "cable")


def eyebar_chain_bridge(st: dict) -> Bridge:
    b = Bridge(st)
    return _hung_deck(b, max(b.H, b.L * 0.11), "eyebar")


def cable_stayed_bridge(st: dict) -> Bridge:
    """A tower at each inner pier (one in the middle for a single span) with stays fanning down to the deck edges."""
    b = Bridge(st)
    _piers_and_deck(b)
    tower_h = max(b.H, b.L * 0.22)
    at = [-b.length / 2 + k * b.L for k in range(1, b.spans)] or [0.0]
    _towers(b, tower_h, at)
    for s in range(1, b.spans + 1):
        _edge_girders(b, s, max(b.L / 60, 1.2))
        for side in ("left", "right"):
            y = (-1 if side == "left" else 1) * b.W / 2
            for i in range(b.P + 1):
                deck_pt = b.node(s, i, "bottom", side)
                x = min(at, key=lambda t: abs(t - deck_pt.x))
                if abs(x - deck_pt.x) < 1e-6:
                    continue
                top = Vector((x, y * 0.8, b.deck_z + tower_h * (0.55 + 0.4 * min(abs(x - deck_pt.x) / b.L, 1))))
                b.add("members", parts.main_cable(f"span{s}_panel{max(i, 1)}_{side}_cable_{i}", [top, deck_pt], b.th * 0.35, b.col), s)
    return b


TEMPLATES = {"truss_bridge": truss_bridge, "girder_bridge": girder_bridge, "suspension_bridge": suspension_bridge,
             "cable_stayed_bridge": cable_stayed_bridge, "eyebar_chain_bridge": eyebar_chain_bridge}


def build(st: dict) -> Bridge:
    return TEMPLATES.get(st["template"], truss_bridge)(st)


def focus_object(b: Bridge, focus: dict):
    """(part, exact): the part the Short is about, by the plan's spot; the gusset at that joint (exact False) when
    this bridge has no such part, so the AI's label for it isn't printed on the wrong part."""
    at = focus["at"]
    s, p, chord, side = at["span"], at["panel"], at["chord"], at["side"]
    names = {"gusset_plate": f"span{s}_node{p}_{chord}_{side}_gusset",
             "chord": f"span{s}_panel{p}_{chord}_{side}_chord",
             "diagonal": f"span{s}_panel{p}_{side}_diagonal",
             "vertical": f"span{s}_node{p}_{side}_vertical",
             "eyebar": f"span{s}_panel{p}_{side}_eyebar",
             "pin_joint": f"span{s}_node{p}_{side}_pin",
             "hanger": f"span{s}_node{p}_{side}_hanger",
             "cable": f"span{s}_panel{p}_{side}_cable_0",
             "pier": f"pier{s}"}
    if focus["part"] in ("gusset_plate", "fastener_group"):  # the plate is the fastener group's home
        names[focus["part"]] = f"span{s}_node{p}_{chord}_{side}_gusset"
    exact = names.get(focus["part"])
    if focus["part"] == "cable":  # cable-stayed stays are named per deck point: the first one of that panel
        exact = next((n for n in sorted(b.objects) if n.startswith(f"span{s}_panel{p}_{side}_cable")), exact)
    if exact in b.objects:
        return b.objects[exact], True
    for name in (f"span{s}_node{p}_{chord}_{side}_gusset", f"span{s}_node{p}_bottom_{side}_gusset"):
        if name in b.objects:
            return b.objects[name], False
    return next(o for o in b.stages["details"] + b.stages["members"] + b.stages["deck"]), False


def dress(b: Bridge, plan: dict) -> None:
    """What the plan says was on the bridge: rails on a rail deck, cars or a train for scale (they ride the span
    they stand on), tiny people on the approach (never on a bridge that falls)."""
    top = b.deck_z + 0.6
    for s in range(1, b.spans + 1):
        x0, x1 = b.x0(s), b.x0(s) + b.L
        if plan["structure"]["deck"] == "rail":
            for y in (-0.75, 0.75):
                b.add("details", parts.member(f"span{s}_rail_{y}", (x0, y, top + 0.1), (x1, y, top + 0.1), 0.15, "dark",
                                              b.col), s)
        if "car" in plan["scale"] and plan["structure"]["deck"] == "road":
            for k, frac in enumerate((0.3, 0.7)):
                b.add("details", parts.car(f"car_s{s}_{k}", x0 + b.L * frac, top, -1 if k else 1, b.col), s)
    if "train" in plan["scale"]:
        s = (b.spans + 1) // 2
        b.add("details", parts.train(f"train_s{s}", b.x0(s) + b.L * 0.2, b.deck_z + 0.6, b.col), s)
    if "people" in plan["scale"] and plan["failure"]["then"] != "collapse_span":
        for k in range(3):
            b.add("piers", parts.person(f"person{k}", -b.length / 2 - 4 - k * 1.5, -b.W * 0.3, b.deck_z + 0.6, b.col))
