"""Per-frame checks on a built opener (2026-10-27), plain bpy. Each check came from a fault the owner caught in the
hand-built Mike probe: an axe through the chicken, legs through the stump, a cut half the bird's size, the bird
walking out of shot, a blade seen edge-on, a head floating above the block. Every function returns a list of
failure strings ("overlap: axe/rooster frames 21-23"); an empty list means it passed."""

import math

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
from mathutils.bvhtree import BVHTree

IN_X, IN_Y = (0.04, 0.96), (0.03, 0.97)  # the subject stays inside these parts of the frame
MAX_PIECES, MIN_PIECE_M = 80, 0.003
SHARE_TOLERANCE = 0.5  # a planned share of 0.15 allows 0.075-0.225


def spans(frames) -> str:
    """[3, 4, 5, 9] -> "3-5, 9"."""
    out, run = [], []
    for f in sorted(frames):
        if run and f == run[-1] + 1:
            run.append(f)
            continue
        if run:
            out.append(f"{run[0]}-{run[-1]}" if len(run) > 1 else str(run[0]))
        run = [f]
    if run:
        out.append(f"{run[0]}-{run[-1]}" if len(run) > 1 else str(run[0]))
    return ", ".join(out)


def world_verts(o, dg=None) -> list[Vector]:
    dg = dg or bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(dg)
    me = ev.to_mesh()
    vs = [ev.matrix_world @ v.co for v in me.vertices]
    ev.to_mesh_clear()
    return vs


def tree(o, dg) -> BVHTree:
    ev = o.evaluated_get(dg)
    me = ev.to_mesh()
    t = BVHTree.FromPolygons([ev.matrix_world @ v.co for v in me.vertices], [p.vertices[:] for p in me.polygons])
    ev.to_mesh_clear()
    return t


def at(frame: int):
    bpy.context.scene.frame_set(frame)
    return bpy.context.evaluated_depsgraph_get()


def visible(o) -> bool:
    return not o.hide_render


def overlaps(objs, frames, allowed: dict) -> list[str]:
    """No two meshes intersect, except a pair on its allowed frames ({frozenset((name, name)): {frame, ...}})."""
    hits: dict[tuple[str, str], list[int]] = {}
    for f in frames:
        dg = at(f)
        live = [o for o in objs if visible(o)]
        trees = {o.name: tree(o, dg) for o in live}
        for i, a in enumerate(live):
            for b in live[i + 1:]:
                if f in allowed.get(frozenset((a.name, b.name)), set()):
                    continue
                if trees[a.name].overlap(trees[b.name]):
                    hits.setdefault(tuple(sorted((a.name, b.name))), []).append(f)
    return [f"overlap: {a}/{b} frames {spans(fs)}" for (a, b), fs in hits.items()]


def resting(pairs, frames, tol: float = 0.01) -> list[str]:
    """Each object touches what it rests on, within tol: no floating above it, no sinking into it. The support may
    come with others it may also lie on ((obj, support, [also, ...])): a mince bit on top of another bit is resting."""
    out = []
    for pair in pairs:
        o, support = pair[0], pair[1]
        also = list(pair[2]) if len(pair) > 2 else []
        floating, sinking = [], []
        for f in frames:
            dg = at(f)
            ts, to, vs = tree(support, dg), tree(o, dg), world_verts(o, dg)
            if to.overlap(ts):  # touching counts; sinking means its lowest point is more than tol under the surface
                low = min(v.z for v in vs)
                centre = sum(vs, Vector()) / len(vs)
                hit = ts.ray_cast(Vector((centre.x, centre.y, low + 50)), Vector((0, 0, -1)))
                if hit[0] is not None and hit[0].z - low > tol:
                    sinking.append(f)
                continue
            gaps = []
            for s in [support] + [a for a in also if a is not o and visible(a)]:
                t = tree(s, dg)
                near = [t.find_nearest(v)[0] for v in vs]
                gaps.append(min((p - v).length for p, v in zip(near, vs) if p is not None))
            if min(gaps) > tol:
                floating.append(f)
        if floating:
            out.append(f"resting: {o.name} floats above {support.name} on frames {spans(floating)}")
        if sinking:
            out.append(f"resting: {o.name} sinks into {support.name} on frames {spans(sinking)}")
    return out


def screen_box(o, cam, dg) -> tuple[float, float, float, float]:
    sc = bpy.context.scene
    pts = [world_to_camera_view(sc, cam, v) for v in world_verts(o, dg)]
    return min(p.x for p in pts), max(p.x for p in pts), min(p.y for p in pts), max(p.y for p in pts)


def in_frame(subject, cam, frames) -> list[str]:
    out = []
    for f in frames:
        x0, x1, y0, y1 = screen_box(subject, cam, at(f))
        if x0 < IN_X[0] or x1 > IN_X[1] or y0 < IN_Y[0] or y1 > IN_Y[1]:
            out.append(f)
    return [f"in_frame: {subject.name} leaves the frame on frames {spans(out)}"] if out else []


def hidden(subject, cam, frames, occluders, min_visible: float = 0.4) -> list[str]:
    """The subject stays visible: on every frame at least min_visible of its points can be seen from the camera
    past `occluders` (a stump between the camera and the walking rooster hid it in the second live run)."""
    out = []
    for f in frames:
        dg = at(f)
        if not visible(subject):
            continue
        pts = world_verts(subject, dg)
        pts = pts[::max(1, len(pts) // 40)]
        eye = cam.matrix_world.translation
        trees = [tree(o, dg) for o in occluders if visible(o) and o is not subject]  # its own front doesn't hide it
        seen = 0
        for p in pts:
            ray = p - eye
            dist = ray.length
            if not any(t.ray_cast(eye, ray.normalized(), dist - 0.01)[0] is not None for t in trees):
                seen += 1
        if seen < min_visible * len(pts):
            out.append(f)
    return [f"hidden: {subject.name} is hidden behind something on frames {spans(out)}"] if out else []


def first_frame(subject, threat, cam, min_height: float = 0.15) -> list[str]:
    """Frame 1 shows the subject, big enough to read, and the threat: the frame that has to stop the scroll."""
    dg, out = at(bpy.context.scene.frame_start), []
    x0, x1, y0, y1 = screen_box(subject, cam, dg)
    if x1 < 0 or x0 > 1 or y1 < 0 or y0 > 1:
        out.append(f"first_frame: {subject.name} is not in the first frame")
    elif min(y1, 1) - max(y0, 0) < min_height:
        out.append(f"first_frame: {subject.name} is {100 * (min(y1, 1) - max(y0, 0)):.0f}% of the frame height "
                   f"(needs {100 * min_height:.0f}%)")
    tx0, tx1, ty0, ty1 = screen_box(threat, cam, dg)
    if tx1 < 0 or tx0 > 1 or ty1 < 0 or ty0 > 1:
        out.append(f"first_frame: {threat.name} (the threat) is not in the first frame")
    return out


def edge_point(tool, edge_axis, dg) -> Vector:
    axis = (tool.matrix_world.to_3x3() @ Vector(edge_axis)).normalized()
    return max(world_verts(tool, dg), key=lambda v: v.dot(axis))


def edge_leads(tool, edge_axis, target, frame: int) -> list[str]:
    """At contact, the edge faces the way the tool moves and points at the target (the probe's first fault)."""
    p0 = edge_point(tool, edge_axis, at(frame - 1))
    dg = at(frame)
    p1 = edge_point(tool, edge_axis, dg)
    edge = (tool.matrix_world.to_3x3() @ Vector(edge_axis)).normalized()
    motion = p1 - p0
    tv = world_verts(target, dg)
    to_target = sum(tv, Vector()) / len(tv) - p1
    out = []
    if motion.length > 1e-6 and edge.dot(motion.normalized()) <= 0:
        out.append(f"edge: {tool.name}'s edge faces away from where it moves on frame {frame}")
    if to_target.length > 1e-6 and edge.dot(to_target.normalized()) <= 0:
        out.append(f"edge: {tool.name}'s edge faces away from {target.name} on frame {frame}")
    return out


def blade_face(tool, cam, frame: int, min_deg: float = 35) -> list[str]:
    """The camera sees the blade's flat side, not its edge: the view is at least min_deg off the blade's plane.
    The blade's plane normal is the tool's thinnest axis."""
    at(frame)
    dims = list(tool.dimensions)
    thin = dims.index(min(dims))
    normal = (tool.matrix_world.to_3x3().col[thin]).normalized()
    centre = tool.matrix_world.translation
    view = (centre - cam.matrix_world.translation).normalized()
    off = math.degrees(math.asin(min(1.0, abs(view.dot(normal)))))
    return [f"blade: {tool.name} is seen edge-on on frame {frame} ({off:.0f} degrees off, needs {min_deg:.0f}): "
            "use stroke angle \"diagonal\" (or \"across\") so the camera sees the blade's flat side"] \
        if off < min_deg else []


def area(o) -> float:
    """How much of a model there is, as its surface area without the filled cut faces (materials named "cut_..."):
    the owner-approved chicken cut is 12% by area but 5% by hull volume, which a long tail inflates (2026-10-27)."""
    dg = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(dg)
    me = ev.to_mesh()
    cut = {i for i, m in enumerate(me.materials) if m and m.name.startswith("cut_")}
    m = ev.matrix_world
    total = 0.0
    for p in me.polygons:
        if p.material_index not in cut:
            vs = [m @ me.vertices[i].co for i in p.vertices]
            total += sum(((vs[0] - vs[k]).cross(vs[0] - vs[k + 1])).length / 2 for k in range(1, len(vs) - 1))
    ev.to_mesh_clear()
    return total


def cut_result(pieces, target_area: float, expect: list[dict]) -> list[str]:
    """The pieces match what the plan expected: named shares (by area()) within ±50%, counts within range, every
    piece at least 3 mm, at most 80 pieces. Each piece object carries its expect name in o["piece"]."""
    out = []
    if len(pieces) > MAX_PIECES:
        out.append(f"cut: {len(pieces)} pieces, at most {MAX_PIECES}")
    small = [o.name for o in pieces if min(o.dimensions) < MIN_PIECE_M]
    if small:
        out.append(f"cut: {len(small)} piece(s) under 3 mm ({', '.join(small[:3])})")
    named = {e["piece"] for e in expect if "piece" in e}
    for e in expect:
        if "share" in e:
            got = sum(area(o) for o in pieces if o.get("piece") == e["piece"]) / max(target_area, 1e-9)
            lo, hi = e["share"] * (1 - SHARE_TOLERANCE), e["share"] * (1 + SHARE_TOLERANCE)
            if not lo <= got <= hi:
                out.append(f"cut: {e['piece']} is {got:.2f} of the target, planned {e['share']:.2f}")
        if "pieces" in e:
            lo, hi = (int(x) for x in str(e["pieces"]).split("-"))
            n = sum(1 for o in pieces if o.get("piece") not in named)
            if not lo <= n <= hi:
                out.append(f"cut: {n} pieces, planned {e['pieces']}")
    return out


def staging(plan: dict, gaits: dict) -> list[str]:
    """Walks and hops that read badly, sent back to the planner (owner, 2026-10-27): an animal walking "away" or
    "camera" shows its back or its chest instead of its side, and a body walking the way its head flew off walks
    over its own head."""
    out = []
    legs = {a["id"] for a in plan["actors"] if gaits.get(a.get("gait", "object"), {}).get("legs") or a.get("person")}
    facing = {a["id"]: a.get("facing", "camera") for a in plan["actors"]}
    flew = {b["target"] for b in plan["beats"] if b["move"] == "cut"
            and any(e.get("then") == "fly_off" for e in b.get("expect", []))}
    for b in plan["beats"]:
        if b["move"] not in ("walk", "hop_off") or b.get("actor") not in legs:
            continue
        actor, way = b["actor"], b.get("toward", "left")
        if way in ("away", "camera"):
            out.append(f"staging: {actor} {b['move']}s toward \"{way}\" and shows the camera its "
                       f"{'back' if way == 'away' else 'chest'}; use \"left\" or \"right\" so it crosses the frame side-on")
        elif actor in flew and way == facing[actor]:
            other = "left" if way == "right" else "right"
            out.append(f"staging: {actor} {b['move']}s \"{way}\", the way its cut piece flew, over its own piece; "
                       f"use \"{other}\"")
    return out
