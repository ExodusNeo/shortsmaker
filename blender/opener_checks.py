"""Per-frame checks on a built opener (2026-10-27), plain bpy. Each check came from a fault the owner caught in the
hand-built Mike probe: an axe through the chicken, legs through the stump, a cut half the bird's size, the bird
walking out of shot, a blade seen edge-on, a head floating above the block. Every function returns a list of
failure strings ("overlap: axe/rooster frames 21-23"); an empty list means it passed."""

import math

import bmesh
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
    """Each object touches what it rests on, within tol: no floating above it, no sinking into it."""
    out = []
    for o, support in pairs:
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
            near = [ts.find_nearest(v)[0] for v in vs]
            if min((p - v).length for p, v in zip(near, vs) if p is not None) > tol:
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
    return [f"blade: {tool.name} is seen edge-on on frame {frame} ({off:.0f} degrees off, needs {min_deg:.0f})"] \
        if off < min_deg else []


def volume(o) -> float:
    """The volume of the object's convex hull (works for open low-poly meshes too)."""
    bm = bmesh.new()
    for v in world_verts(o):
        bm.verts.new(v)
    if len(bm.verts) < 4:
        bm.free()
        return 0.0
    bmesh.ops.convex_hull(bm, input=bm.verts)
    vol = bm.calc_volume()
    bm.free()
    return abs(vol)


def cut_result(pieces, target_volume: float, expect: list[dict]) -> list[str]:
    """The pieces match what the plan expected: named shares within ±50%, counts within range, every piece at least
    3 mm, at most 80 pieces. Each piece object carries its expect name in o["piece"]."""
    out = []
    if len(pieces) > MAX_PIECES:
        out.append(f"cut: {len(pieces)} pieces, at most {MAX_PIECES}")
    small = [o.name for o in pieces if min(o.dimensions) < MIN_PIECE_M]
    if small:
        out.append(f"cut: {len(small)} piece(s) under 3 mm ({', '.join(small[:3])})")
    named = {e["piece"] for e in expect if "piece" in e}
    for e in expect:
        if "share" in e:
            got = sum(volume(o) for o in pieces if o.get("piece") == e["piece"]) / max(target_volume, 1e-9)
            lo, hi = e["share"] * (1 - SHARE_TOLERANCE), e["share"] * (1 + SHARE_TOLERANCE)
            if not lo <= got <= hi:
                out.append(f"cut: {e['piece']} is {got:.2f} of the target, planned {e['share']:.2f}")
        if "pieces" in e:
            lo, hi = (int(x) for x in str(e["pieces"]).split("-"))
            n = sum(1 for o in pieces if o.get("piece") not in named)
            if not lo <= n <= hi:
                out.append(f"cut: {n} pieces, planned {e['pieces']}")
    return out
