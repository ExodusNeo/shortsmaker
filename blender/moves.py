"""The opener moves (2026-10-27), plain bpy. Each works on roles (actor, target, tool, support), never on particular
models; passive motion (falling, tipping, rolling, flying off, scattering, cut pieces) is Blender rigid-body physics
so it works for any shape and can't pass through things; driven motion (walking, hopping, tool strokes, pushes) is
keyframed from the gait and tool tables in opener_tables.json. `cut` is one general move for every kind of cut:
strokes split the target along the planes the blade travels in (bisect with filled cut faces), the blade stops at
the first thing it isn't cutting, and the plan's `expect` says what the pieces should be."""

import math
import random

import bmesh
import bpy
from mathutils import Matrix, Vector

import scene_kit as kit

TOWARD = {"left": Vector((-1, 0, 0)), "right": Vector((1, 0, 0)), "camera": Vector((0, -1, 0)), "away": Vector((0, 1, 0))}
REGION_SIDE = {"head": "top_front", "neck": "top_front", "top": "top", "tail": "back", "back": "back",
               "front": "front", "middle": "middle", "bottom": "bottom", "base": "bottom", "legs": "bottom"}
STROKE_FRAMES = {"chop": 4, "slash": 4, "press": 5, "drop": 5, "saw": 15, "shape": 8}
MINCE_FRAMES = 3
WIND_DEG = 55  # how far a chop or slash is raised before the stroke
SWING = 4  # frames a raised chop or slash takes to come down to the cut (it snapped there in one, owner 2026-10-27)


class State:
    """Everything the moves share: the scene's objects by plan id, what stands on what, and what the checks need."""

    def __init__(self, plan: dict, fps: int, frames: int, cam_h: Vector):
        self.plan, self.fps, self.frames, self.cam_h = plan, fps, frames, cam_h
        self.objs, self.support, self.find = {}, {}, {a["id"]: a.get("find") or a["person"] for a in plan["actors"]}
        self.ground = None
        self.pieces: dict[str, list] = {}  # target id -> its cut pieces
        self.intact: dict[str, object] = {}  # target id -> the uncut copy shown until the first stroke
        self.allowed: dict[frozenset, set] = {}
        self.released: dict[str, int] = {}  # object name -> frame physics takes over
        self.resting: list[tuple] = []  # (object, support object)
        self.contacts: list[tuple] = []  # (tool, edge axis (local), target, frame)
        self.cuts: list[tuple] = []  # (pieces, target volume, expect, {piece: share})
        self.failures: list[str] = []
        self.threat = None
        self.moved_from: dict[str, int] = {}  # actor id -> first frame it moves
        self.people: dict | None = None  # the people library (people.load_library) when the plan has people
        self.rigs: dict[str, list] = {}  # actor id -> its leg rig (scene_kit.leg_rig), built when it first moves
        self.stroke_toward: list[float] = []  # each stroke's motion toward the camera (0 = across the frame)
        self.windups: list[tuple] = []  # (tool, its last wind-up frame): moved so the unseen hand is off-screen

    def f(self, t: float) -> int:
        return min(kit.frame_of(t, self.fps), self.frames)

    def allow(self, a, b, frames) -> None:
        self.allowed.setdefault(frozenset((a.name, b.name)), set()).update(frames)

    def support_obj(self, actor: str):
        s = self.support.get(actor, "ground")
        return self.ground if s == "ground" else self.objs[s]


def apply(beat: dict, st: State) -> None:
    if beat.get("actor") in st.objs and st.objs[beat["actor"]].get("person"):  # people move by their own clips
        import people
        people.move(beat, st, st.people)
    else:
        {"cut": cut, "fall": fall, "topple": topple, "hop_off": hop_off, "walk": walk, "fly_off": fly_off,
         "scatter": scatter, "sink": sink, "roll": roll, "push": push}[beat["move"]](beat, st)
    if beat["move"] != "cut" and beat.get("actor") in st.objs:  # where it rested before no longer holds
        moved = st.objs[beat["actor"]]
        st.resting = [r for r in st.resting if r[0] is not moved]
    if beat.get("ends") and beat["move"] != "cut":
        on = beat["ends"]["on"]
        st.resting.append((st.objs[beat["actor"]], st.ground if on == "ground" else st.objs[on]))


def toward(beat: dict, default: str = "left") -> Vector:
    return kit.view(TOWARD[beat.get("toward", default)])


# --- passive moves: physics ----------------------------------------------------------------------------------------

def release(st: State, obj, frame: int, launch=None, spin=None) -> None:
    kit.make_dynamic(obj, frame, launch, spin)
    st.released[obj.name] = frame


def fall(beat, st):
    o = st.objs[beat["actor"]]
    lo, hi = kit.bbox(o)
    lift = beat.get("from_m") or max(0.5, hi.z - lo.z)
    o.location.z += lift
    kit.key_loc(o, 1, o.location.copy())
    release(st, o, st.f(beat["at"]))
    st.threat = st.threat or o
    st.moved_from.setdefault(beat["actor"], st.f(beat["at"]))


def topple(beat, st):
    o, d = st.objs[beat["actor"]], toward(beat, "right")
    release(st, o, st.f(beat["at"]), launch=d * 0.2, spin=Vector((0, 0, 1)).cross(d) * 2.5)
    st.moved_from.setdefault(beat["actor"], st.f(beat["at"]))


def roll(beat, st):
    o, d = st.objs[beat["actor"]], toward(beat, "right")
    lo, hi = kit.bbox(o)
    r = max((hi.z - lo.z) / 2, 0.02)
    release(st, o, st.f(beat["at"]), launch=d * 1.2, spin=Vector((0, 0, 1)).cross(d) * (1.2 / r))
    st.moved_from.setdefault(beat["actor"], st.f(beat["at"]))


def fly_off(beat, st):
    o, d = st.objs[beat["actor"]], toward(beat, "right")
    release(st, o, st.f(beat["at"]), launch=d * 1.0 + Vector((0, 0, 1.8)), spin=Vector((3, 6, 2)))
    st.moved_from.setdefault(beat["actor"], st.f(beat["at"]))


def scatter(beat, st):
    rng = random.Random(7)
    items = st.pieces.get(beat["actor"]) or [st.objs[beat["actor"]]]
    for o in items:
        a = rng.uniform(0, 2 * math.pi)
        release(st, o, st.f(beat["at"]), launch=Vector((math.cos(a) * 0.2, math.sin(a) * 0.2, 0.5)),
                spin=Vector((rng.uniform(-4, 4), rng.uniform(-4, 4), 0)))
    st.moved_from.setdefault(beat["actor"], st.f(beat["at"]))


# --- driven moves: keyframes -----------------------------------------------------------------------------------

def gait(st: State, actor: str) -> dict:
    a = next(x for x in st.plan["actors"] if x["id"] == actor)
    return kit.TABLES["gaits"][a.get("gait", "object")]


def legs(st: State, actor: str) -> list:
    """The actor's leg rig, built on whatever now stands for it (after a cut, its "rest" piece); [] without legs."""
    g = gait(st, actor)
    if not g.get("legs"):
        return []
    if actor not in st.rigs:
        o = st.objs[actor]
        st.rigs[actor] = kit.leg_rig(o, g["legs"], g["leg_zone"], kit.facing_vec(o))
    return st.rigs[actor]


def hop_off(beat, st):
    """Up, out at that height until the whole body has passed the support's far edge, then down onto the ground: the
    probe's legs went through the stump, and the first live run dropped too early over a wider stump's rim."""
    actor, d = beat["actor"], toward(beat)
    o, sup = st.objs[actor], st.support_obj(beat["actor"])
    f0 = st.f(beat["at"])
    start = kit.loc_at(o, f0)
    o.location = start
    bpy.context.view_layer.update()
    lo, hi = kit.bbox(o)
    slo, shi = kit.bbox(sup)
    half = (hi - lo) / 2
    centre = (lo + hi) / 2
    along = lambda v: v.dot(d)  # noqa: E731
    out = max(along(Vector((x, y, 0))) for x in (slo.x, shi.x) for y in (slo.y, shi.y))  # support's far edge
    edge = out - along(centre) + abs(along(half)) + 0.02  # here its trailing side has passed the far edge
    clear = edge + 0.06
    land = start + d * clear
    land.z = 0.0
    apex = shi.z + 0.04  # the bottom of the actor stays above the support's highest point
    n = max(15, round(0.55 * st.fps))
    rise, glide = round(n * 0.3), round(n * 0.65)  # frames: up / out at the apex / down
    style = beat.get("style", "normal")
    for k in range(n + 1):
        t = k / n
        if k <= rise:
            out_d, z = 0.0, start.z + (apex - start.z) * math.sin(math.pi / 2 * k / rise)
        elif k <= glide:
            out_d, z = edge * (k - rise) / (glide - rise), apex
        else:
            u = (k - glide) / (n - glide)
            out_d, z = edge + (clear - edge) * u, apex + (land.z - apex) * u * u
        pos = start + d * out_d
        pos.z = z
        if style == "stagger":  # zero at the start: before its first key the actor holds that key's tilt
            rot = (math.radians(8 * math.sin(t * 6)), math.radians(6 * math.sin(t * 5)), o.rotation_euler.z)
            kit.key_rot(o, f0 + k, rot)
            pos.z += kit.lift_for(o, rot)
        kit.key_loc(o, f0 + k, pos)
    kit.key_loc(o, f0, start)
    rig = legs(st, actor)
    if rig:  # legs tucked back in the air, straight again to land (owner, 2026-10-27)
        for f, a in ((f0, 0.0), (f0 + rise, -math.radians(35)), (f0 + glide, -math.radians(35)), (f0 + n, 0.0)):
            kit.key_swing(rig, f, a, together=True)
    st.support[actor] = "ground"
    st.moved_from.setdefault(actor, f0)


def walk(beat, st):
    actor, d = beat["actor"], toward(beat)
    o, g = st.objs[actor], gait(st, actor)
    f0 = st.f(beat["at"])
    speed = g["step"] * g["steps_per_s"] or 0.3
    start = kit.loc_at(o, f0)  # where the moves before this one left it
    if st.support.get(actor, "ground") == "ground":
        start.z = 0.0  # on the ground, even if a hop's landing overlaps the walk's first frames
    face = kit.facing_vec(o)
    turn = math.atan2(face.x * d.y - face.y * d.x, face.dot(d))  # turn to face the way it walks
    base_rot = kit.rot_at(o, f0)
    stagger = beat.get("style") == "stagger"
    # it stops short of whatever is in its way (the third live run walked back into the stump it hopped off)
    tools = {b["tool"] for b in st.plan["beats"] if b["move"] == "cut"}
    obstacles = [x for k, x in st.objs.items() if x is not o and k not in tools] + \
        [x for x in bpy.context.scene.objects if x.name.startswith("backdrop")]
    leg = (o.dimensions.z or 1) * g.get("leg_zone", 0.3)
    swing = max(math.radians(22), math.asin(min(0.9, g["step"] / (2 * leg))))  # a stride's reach, never a shuffle
    reach = leg * math.sin(swing) if g.get("legs") else 0.0  # a foot swings this far ahead of the body
    keep_loc, keep_rot = o.location.copy(), o.rotation_euler.copy()
    o.location, o.rotation_euler = start + Vector((0, 0, 0.01)), (0, 0, base_rot.z + turn)
    bpy.context.view_layer.update()
    room = max(0.0, clear_distance(o, d, obstacles, speed * (st.frames - f0) / st.fps) - 0.04 - reach)  # 4 cm: sway
    o.location, o.rotation_euler = keep_loc, keep_rot
    bpy.context.view_layer.update()
    rig = legs(st, actor)
    if rig:
        kit.key_swing(rig, f0, 0.0)
    last = st.frames if (st.frames - f0) % 2 == 0 else st.frames + 1
    for f in range(f0, last + 1, 2):
        f = min(f, st.frames)
        t = (f - f0) / st.fps
        pos = start + d * min(speed * t, room)
        # the last frame lands the step: it ends standing on the ground, not mid-bob
        pos.z = start.z + (0 if f == st.frames else g["bob"] * abs(math.sin(math.pi * g["steps_per_s"] * t)))
        if stagger:
            pos += Vector((-d.y, d.x, 0)) * 0.03 * math.sin(t * 7)
        rz = base_rot.z + turn * min(1.0, (f - f0) / 8)
        tilt = (math.radians(9 * math.sin(t * 8)), math.radians(7 * math.sin(t * 6))) \
            if stagger and f != st.frames else (0, 0)
        kit.key_rot(o, f, (tilt[0], tilt[1], rz))
        if rig:  # one step per bob; the last frame lands both feet
            kit.key_swing(rig, f, 0.0 if f == st.frames else swing * math.sin(math.pi * g["steps_per_s"] * t))
        pos.z += kit.lift_for(o, (tilt[0], tilt[1], 0))
        kit.key_loc(o, f, pos)
    kit.key_loc(o, f0, start)
    st.moved_from.setdefault(actor, f0)


def sink(beat, st):
    o = st.objs[beat["actor"]]
    f0 = st.f(beat["at"])
    lo, hi = kit.bbox(o)
    kit.key_loc(o, f0, o.location.copy())
    kit.key_rot(o, f0, o.rotation_euler.copy())
    kit.key_loc(o, min(f0 + round(1.5 * st.fps), st.frames), o.location - Vector((0, 0, 0.9 * (hi.z - lo.z))))
    kit.key_rot(o, min(f0 + round(1.5 * st.fps), st.frames), (math.radians(15), 0, o.rotation_euler.z))
    st.moved_from.setdefault(beat["actor"], f0)


def push(beat, st):
    """The actor moves at the target until they touch; from that frame physics carries the target on."""
    actor, target = st.objs[beat["actor"]], st.objs[beat["target"]]
    d = (target.location - actor.location)
    d.z = 0
    d.normalize()
    f0 = st.f(beat["at"])
    gap = travel(actor, d, [target])
    hit = f0 + max(2, round(gap / 0.6 * st.fps))
    kit.key_loc(actor, f0, actor.location.copy())
    kit.key_loc(actor, hit, actor.location + d * max(gap - 0.002, 0))
    release(st, target, min(hit + 1, st.frames), launch=d * 0.6)
    st.moved_from.setdefault(beat["actor"], f0)


def clear_distance(o, d: Vector, others: list, limit: float, step: float = 0.02) -> float:
    """How far o can slide along d (up to limit) before its mesh touches any of `others`: the whole mesh is moved and
    tested, so a narrow root can't slip between rays the way it does with travel()."""
    from mathutils.bvhtree import BVHTree
    trees = [kit.tree(x) for x in others]
    vs = kit.world_verts(o)
    polys = [p.vertices[:] for p in o.data.polygons]
    dist = 0.0
    while dist <= limit:
        moved = BVHTree.FromPolygons([v + d * dist for v in vs], polys)
        if any(moved.overlap(t) for t in trees):
            return max(0.0, dist - step)
        dist += step
    return limit


def travel(o, d: Vector, others: list) -> float:
    """How far o can move along d before it touches any of `others` (rays from its vertices)."""
    best = 100.0
    vs = kit.world_verts(o)
    for other in others:
        t = kit.tree(other)
        for v in vs:
            hit = t.ray_cast(v, d, best)
            if hit[0] is not None:
                best = min(best, hit[3])
    return best


# --- cut ------------------------------------------------------------------------------------------------------------

def to_bm(o) -> bmesh.types.BMesh:
    """o's mesh in world space with duplicate corner points welded: flat-shaded exports give every face its own
    corners, so the mesh is all open edges and a cut face can't be filled (the onion slices came out hollow)."""
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bm.transform(o.matrix_world)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    return bm


def half(src, co: Vector, no: Vector, positive: bool, cap_index: int):
    """The part of `src` on one side of the plane, its cut face filled; None when nothing is on that side."""
    bm = src.copy()
    res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=co, plane_no=no,
                                 clear_inner=positive, clear_outer=not positive)
    if not bm.faces:
        bm.free()
        return None
    cut_edges = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge) and e.is_valid and e.is_boundary]
    if cut_edges:
        filled = bmesh.ops.holes_fill(bm, edges=cut_edges, sides=0)
        for f in filled["faces"]:
            f.material_index = cap_index
    return bm


def islands(bm) -> list:
    """The loose parts of bm, each as its own bmesh."""
    seen, out = set(), []
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        if f.index in seen:
            continue
        stack, part = [f], []
        seen.add(f.index)
        while stack:
            g = stack.pop()
            part.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen:
                        seen.add(h.index)
                        stack.append(h)
        sub = bm.copy()
        keep = {g.index for g in part}
        sub.faces.ensure_lookup_table()
        bmesh.ops.delete(sub, geom=[g for g in sub.faces if g.index not in keep], context="FACES")
        bmesh.ops.delete(sub, geom=[v for v in sub.verts if not v.link_faces], context="VERTS")
        out.append(sub)
    return out


def bm_area(bm, skip_material: int) -> float:
    """Surface area without the filled cut faces: how much of the model a piece is (see opener_checks.area)."""
    return sum(f.calc_area() for f in bm.faces if f.material_index != skip_material)




def centre(bm) -> Vector:
    return sum((v.co for v in bm.verts), Vector()) / max(len(bm.verts), 1)


def to_object(bm, name: str, mats) -> bpy.types.Object:
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    for m in mats:
        me.materials.append(m)
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    vs = [v.co for v in me.vertices]
    base = Vector(((min(v.x for v in vs) + max(v.x for v in vs)) / 2, (min(v.y for v in vs) + max(v.y for v in vs)) / 2,
                   min(v.z for v in vs)))
    me.transform(Matrix.Translation(-base))
    o.location = base
    return o


def join(bms):
    out = bmesh.new()
    for b in bms:
        tmp = bpy.data.meshes.new("tmp")
        b.to_mesh(tmp)
        out.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
    return out


def region_normal(region: str, angle: str, facing: Vector, cam_h: Vector) -> Vector:
    side = REGION_SIDE.get(region, "top_front")
    base = {"top_front": Vector((0, 0, 1)), "top": Vector((0, 0, 1)), "middle": Vector((0, 0, 1)),
            "bottom": Vector((0, 0, -1)), "front": facing, "back": -facing}[side]
    if angle == "across":
        return cam_h.copy()
    if angle == "down":
        return Vector((-cam_h.y, cam_h.x, 0))
    if angle == "diagonal":
        if side == "top_front":  # a neck leans forward: the plane follows it as seen and is not tilted at the lens.
            # In profile a 45-degree tilt over a 6 cm neck took a wedge off the back of the head and left the face on
            # (owner, 2026-10-27); the blade is turned to show its face instead (show_face)
            lean = facing - cam_h * facing.dot(cam_h)
            return (base + lean).normalized()
        return (base + cam_h).normalized()
    return base.copy()


def box_of(bm) -> tuple[Vector, Vector]:
    vs = [v.co for v in bm.verts]
    return (Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs))),
            Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs))))


def clusters(parts: list, gap: float) -> list:
    """Loose parts that touch or nearly touch belong together: a low-poly head is often a beak, comb, eyes and
    wattle modelled as separate parts (the probe's first cut took only the beak)."""
    boxes = [box_of(p) for p in parts]
    group = list(range(len(parts)))

    def root(i):
        while group[i] != i:
            group[i] = group[group[i]]
            i = group[i]
        return i
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            (a0, a1), (b0, b1) = boxes[i], boxes[j]
            if all(a0[k] - gap <= b1[k] and b0[k] - gap <= a1[k] for k in range(3)):
                group[root(i)] = root(j)
    out: dict[int, list] = {}
    for i, p in enumerate(parts):
        out.setdefault(root(i), []).append(p)
    return [join(ps) if len(ps) > 1 else ps[0] for ps in out.values()]


def pick_island(parts: list, region: str, facing: Vector):
    side = REGION_SIDE.get(region, "top_front")
    score = {"top_front": lambda c: c.z + 0.5 * c.dot(facing), "top": lambda c: c.z, "middle": lambda c: -c.length,
             "bottom": lambda c: -c.z, "front": lambda c: c.dot(facing), "back": lambda c: -c.dot(facing)}[side]
    return max(parts, key=lambda b: score(centre(b)))


def through_cut(src, region, angle, share, facing, cam_h, cap, total):
    """Split off the region's piece so it is about `share` of the target: the plane's position is scanned (the
    share jumps as parts separate, so no bisection), the cluster on its far side nearest the region is the piece,
    and everything else stays with the rest."""
    no = region_normal(region, angle, facing, cam_h)
    proj = [v.co.dot(no) for v in src.verts]
    lo, hi = min(proj), max(proj)
    c0 = centre(src)
    lo_b, hi_b = box_of(src)
    # loose parts within 6% of each other are one piece: at 2% a rooster's beak and wattle stayed on the neck stump
    gap = 0.06 * max(hi_b - lo_b)

    def split(d):
        co = c0 + no * (d - c0.dot(no))
        pos = half(src, co, no, True, cap)
        if pos is None:
            return None, [], 0.0, co
        parts = clusters(islands(pos), gap)
        piece = pick_island(parts, region, facing)
        return piece, [p for p in parts if p is not piece], bm_area(piece, cap) / total, co

    def best_in(a, b, steps):
        tries = [a + (b - a) * k / steps for k in range(1, steps)]
        return min(tries, key=lambda d: abs(split(d)[2] - share)), (b - a) / steps
    d, step = best_in(lo, hi, 40)
    d, _ = best_in(d - step, d + step, 10)
    piece, others, got, co = split(d)
    neg = half(src, co, no, False, cap)
    rest = join([neg] + others) if neg is not None else join(others)
    return piece, rest, no, co


def plane_splits(src, planes, cap):
    pieces = [src]
    for co, no in planes:
        nxt = []
        for p in pieces:
            for side in (False, True):
                h = half(p, co, no, side, cap)
                if h is not None and len(h.verts) >= 4:
                    nxt.append(h)
        pieces = nxt
    return pieces


def merge_slivers(pieces, min_m: float):
    """Pieces thinner than min_m are joined to their nearest neighbour (a mince's edge slivers)."""
    def thin(b):
        vs = [v.co for v in b.verts]
        return min(max(v[i] for v in vs) - min(v[i] for v in vs) for i in range(3)) < min_m
    pieces = list(pieces)
    changed = True
    while changed and len(pieces) > 1:
        changed = False
        for p in pieces:
            if thin(p):
                others = [q for q in pieces if q is not p]
                near = min(others, key=lambda q: (centre(q) - centre(p)).length)
                pieces = [q for q in others if q is not near] + [join([near, p])]
                changed = True
                break
    return pieces


def tool_axes(tool):
    """(edge, thin, long) unit axes of a tool in its own space: long = handle-to-head, thin = the blade's plane
    normal, edge = the way the cutting edge faces: the side of the head where the blade is thinnest (a blade tapers
    to its edge; a knife's spine or an axe's poll is thick). "The side that sticks out furthest" picked a knife's
    spine (2026-10-27)."""
    vs = [v.co for v in tool.data.vertices]
    dims = [max(v[i] for v in vs) - min(v[i] for v in vs) for i in range(3)]
    L, T = dims.index(max(dims)), dims.index(min(dims))
    E = 3 - L - T
    mid = (max(v[L] for v in vs) + min(v[L] for v in vs)) / 2
    upper, lower = [v for v in vs if v[L] >= mid], [v for v in vs if v[L] < mid]
    width = lambda part: max(v[E] for v in part) - min(v[E] for v in part)  # noqa: E731
    head = upper if width(upper) >= width(lower) else lower
    head_sign = 1 if head is upper else -1
    e_lo, e_hi = min(v[E] for v in head), max(v[E] for v in head)
    band = 0.2 * (e_hi - e_lo)

    def thickness(near: float) -> float:
        side = [v[T] for v in head if abs(v[E] - near) <= band]
        return max(side) - min(side) if side else 0.0
    e_sign = 1 if thickness(e_hi) <= thickness(e_lo) else -1
    axis = lambda i, s: Vector([s if k == i else 0 for k in range(3)])  # noqa: E731
    return axis(E, e_sign), axis(T, 1), axis(L, head_sign)


def tool_rotation(tool, d: Vector, n: Vector, handle_pref: Vector):
    """The rotation that turns the edge toward d and the blade's plane normal along ±n, the handle toward
    handle_pref; returns (rotation matrix, normal used)."""
    E, T, L = tool_axes(tool)
    local = Matrix((E, T, L)).transposed()
    s = 1 if local.determinant() > 0 else -1
    for nn in (n, -n):
        w = d.cross(nn) * s
        if w.dot(handle_pref) >= 0:
            break
    world = Matrix((d, nn, w)).transposed()
    return world @ local.inverted(), nn


def show_face(R: Matrix, nn: Vector, d: Vector, cam_h: Vector, deg: float = 50) -> tuple[Matrix, Vector]:
    """Turn the blade about its stroke until its flat side is at least `deg` toward the camera; the cut is already
    made, so only the look changes, and the edge still leads along d. 50, not the check's 35: the camera's pitch and
    arc aren't known yet and took 11 degrees off in the Mike run."""
    a, b = nn.dot(cam_h), d.cross(nn).dot(cam_h)
    want = math.sin(math.radians(deg))
    if abs(a) >= want or math.hypot(a, b) < want:
        return R, nn
    phase, spread = math.atan2(b, a), math.acos(want / math.hypot(a, b))
    turns = [phase - spread, phase + spread, phase + math.pi - spread, phase + math.pi + spread]
    t = min(((x + math.pi) % (2 * math.pi) - math.pi for x in turns), key=abs)  # the smallest turn that shows it
    rot = Matrix.Rotation(t, 3, d)
    return rot @ R, rot @ nn


def edge_point_local(tool) -> Vector:
    """The blade's furthest point along its edge direction, over the whole head half: near the tip a knife's blade
    narrows, and an edge point there sat 1.3 cm above the blade's real bottom (2026-10-27)."""
    E, _, L = tool_axes(tool)
    vs = [v.co for v in tool.data.vertices]
    mid = (max(v.dot(L) for v in vs) + min(v.dot(L) for v in vs)) / 2
    return max((v for v in vs if v.dot(L) >= mid), key=lambda v: v.dot(E)).copy()


def handle_end_local(tool) -> Vector:
    _, _, L = tool_axes(tool)
    return min((v.co for v in tool.data.vertices), key=lambda v: v.dot(L)).copy()


def place_tool(tool, R: Matrix, edge_at: Vector) -> Vector:
    """Object location that puts the tool's edge point at edge_at with rotation R."""
    return edge_at - R @ edge_point_local(tool)


def cut(beat, st):
    tool, tid = st.objs[beat["tool"]], beat["target"]
    target = st.objs[tid]
    kind = next(st_ for k, st_ in sorted(kit.TABLES["tools"].items(), key=lambda kv: -len(kv[0]))
                if f" {k} " in f" {st.find[beat['tool']].lower()} ")
    expect = beat["expect"]
    named = [e for e in expect if "piece" in e]
    cap_rgb = next((rgb for word, rgb in kit.TABLES["cut_face"].items() if word in st.find[tid].lower()),
                   kit.TABLES["cut_face"]["default"])
    cap_mat = kit.material(f"cut_{tid}", cap_rgb)
    mats = list(target.data.materials) + [cap_mat]
    cap = len(mats) - 1
    src = to_bm(target)
    total = bm_area(src, cap)
    facing = kit.facing_vec(target)
    lo, hi = kit.bbox(target)
    mid = (lo + hi) / 2
    stroke = beat["strokes"][0]
    shares = {}

    if "through" in stroke:
        region = stroke["through"]
        piece_e = next((e for e in named if e["piece"] != "rest"), {"piece": region, "share": 0.15})
        share = piece_e.get("share", 0.15)
        piece_bm, rest_bm, no, co = through_cut(src, region, stroke.get("angle", "level"), share, facing, st.cam_h,
                                                cap, total)
        bms = [(piece_e["piece"], piece_bm), ("rest", rest_bm)]
        planes = [(co, no)]
        free_stroke = {0: 0, 1: 0}  # one stroke frees both
    else:
        # slices stack at 45 degrees to the view: the blade still shows its face (35 is the limit) and the slices
        # separate where they can be seen; stacked straight at the camera the front slice hid the rest
        c45 = math.sqrt(0.5)
        n_axis = Vector((st.cam_h.x * c45 - st.cam_h.y * c45, st.cam_h.x * c45 + st.cam_h.y * c45, 0))
        m_axis = Vector((-n_axis.y, n_axis.x, 0))
        size_n = max(abs((hi - lo).dot(n_axis)), 1e-4)
        size_m = max(abs((hi - lo).dot(m_axis)), 1e-4)
        rng = random.Random(11)
        planes = []
        if "at_fraction" in stroke:
            planes = [(mid + n_axis * ((stroke["at_fraction"] - 0.5) * size_n), n_axis)]
        elif "rows" in stroke:
            rows, cols = int(stroke["rows"]), int(stroke.get("cols") or 1)
            planes = [(mid + n_axis * ((i / rows - 0.5) * size_n), n_axis) for i in range(1, rows)]
            planes += [(mid + m_axis * ((j / cols - 0.5) * size_m), m_axis) for j in range(1, cols)]
        else:  # mince: a jittered grid plus one level cut, its size tried until the piece count fits the plan
            want = next((e["pieces"] for e in expect if "pieces" in e), f"{stroke['mince']}-{stroke['mince']}")
            lo_n, hi_n = (int(x) for x in str(want).split("-"))
            k0 = max(2, math.ceil(math.sqrt(stroke["mince"] / 2 * 4 / math.pi)))
            best = None
            for k in sorted({max(2, k0 + dk) for dk in (0, -1, 1, -2, 2)}, key=lambda k: abs(k - k0)):
                grid = [(mid + n_axis * (((i + rng.uniform(-0.15, 0.15)) / k - 0.5) * size_n), n_axis) for i in range(1, k)]
                grid += [(mid + m_axis * (((j + rng.uniform(-0.15, 0.15)) / k - 0.5) * size_m), m_axis) for j in range(1, k)]
                grid.append((mid, Vector((0, 0, 1))))
                got = merge_slivers(plane_splits(src, grid, cap), kit.TABLES["limits"]["min_piece_m"])
                miss = 0 if lo_n <= len(got) <= hi_n else min(abs(len(got) - lo_n), abs(len(got) - hi_n))
                if best is None or miss < best[0]:
                    best = (miss, grid, got)
                if miss == 0:
                    break
            planes = best[1]
        parts = best[2] if "mince" in stroke else \
            merge_slivers(plane_splits(src, planes, cap), kit.TABLES["limits"]["min_piece_m"])
        order = sorted(parts, key=lambda b: centre(b).dot(n_axis))
        names = [e["piece"] for e in named] if len(named) == len(order) else ["bit"] * len(order)
        bms = list(zip(names, order))
        stroke_planes = [p for p in planes if abs(p[1].z) < 0.5]  # the blade can't press sideways
        planes = stroke_planes
        # each piece comes loose with the first stroke past it, so a mince falls apart as the knife moves along
        cuts_n = [co.dot(n_axis) for co, no in planes if abs(no.dot(n_axis)) > 0.9]
        free_stroke = {}
        for i, (_, b) in enumerate(bms):
            c = centre(b).dot(n_axis)
            free_stroke[i] = next((k for k, x in enumerate(cuts_n) if x > c), max(len(cuts_n) - 1, 0))

    # pieces: hidden until the first stroke lands, the uncut target shown until then
    pieces = []
    for i, (name, bm) in enumerate(bms):
        o = to_object(bm, f"{tid}.{name}.{i}" if name == "bit" else f"{tid}.{name}", mats)
        o["piece"] = name
        o["facing"] = target.get("facing", "camera")  # the body walking off kept facing the camera (owner's Mike run)
        bm.free()
        pieces.append(o)
    src.free()
    for name, p in zip([n for n, _ in bms], pieces):
        if name != "bit" and "share" in next((e for e in named if e["piece"] == name), {}):
            shares[name] = round(bm_area(to_bm(p), cap) / total, 4)

    # the tool's strokes
    E, T, L = tool_axes(tool)
    f_contact = st.f(beat["at"])
    per = MINCE_FRAMES if "mince" in stroke else STROKE_FRAMES[kind]
    others = [o for k, o in st.objs.items() if k not in (tid, beat["tool"])] + [st.ground]
    stroke_frames = []
    for s_i, (co, no) in enumerate(planes or [(mid, st.cam_h)]):
        # within the blade's plane and never toward the lens (moving at the camera the axe ballooned, live run 6):
        # downward when the plane allows it, else in from the camera's right
        d = no.cross(st.cam_h)
        if d.length < 0.2:  # a plane facing the camera: straight down within it
            d = Vector((0, 0, -1)) - no * Vector((0, 0, -1)).dot(no)
        d.normalize()
        if abs(d.z) < 0.05:
            r = Vector((-st.cam_h.y, st.cam_h.x, 0))
            d = -d if d.dot(r) > 0 else d
        elif d.z > 0:
            d = -d
        st.stroke_toward.append(round(d.dot(st.cam_h), 3))
        piece_side = pieces[0] if "through" in stroke else pieces[min(s_i, len(pieces) - 1)]
        pc = sum(kit.world_verts(piece_side), Vector()) / len(kit.world_verts(piece_side))
        R, nn = tool_rotation(tool, d, no, (pc - mid) if "through" in stroke else no)
        if kind in ("chop", "slash"):  # a knife keeps its slice plane: turned, it was blocked and led with its back
            R, nn = show_face(R, nn, d, st.cam_h)
        tool.rotation_euler = R.to_euler()
        # the cut line: where the plane crosses the piece's attachment; the blade travels across it along d
        cut_pts = [v for v in kit.world_verts(piece_side) if abs((v - co).dot(no)) < 0.004] or kit.world_verts(piece_side)
        along = [p.dot(d) for p in cut_pts]
        cline = co + d * (min(along) - co.dot(d))
        approach = min(max(0.5 * (hi.z - lo.z), 0.03), 0.12)  # the blade starts this far before the cut
        start_edge = cline - d * approach
        need = (max(along) - min(along)) + approach  # past the far side of the cut
        tool.location = place_tool(tool, R, start_edge)
        bpy.context.view_layer.update()
        room = travel(tool, d, others)
        if room < need - 0.005:
            blocker = min(others, key=lambda o: travel(tool, d, [o]))
            st.failures.append(f"cut: {beat['tool']} is blocked by {blocker.name} before it finishes the cut")
        go = min(room - 0.002, need + 0.03)
        f_end = f_contact + s_i * (per + 2)
        f_start = max(2, f_end - per)
        start_loc = tool.location.copy()
        end_loc = start_loc + d * go
        rot = R.to_euler()
        if s_i == 0:
            wind = Matrix.Rotation(math.radians(WIND_DEG), 3, nn)
            arm = R @ (edge_point_local(tool) - handle_end_local(tool))
            if (wind @ arm - arm).dot(d) > 0:  # the edge is pulled back against the stroke (it dipped underground)
                wind = Matrix.Rotation(-math.radians(WIND_DEG), 3, nn)
            pivot = start_loc + R @ handle_end_local(tool)
            wind_R = wind @ R
            wind_loc = pivot - wind_R @ handle_end_local(tool) if kind in ("chop", "slash") else start_loc + Vector((0, 0, approach))
            wind_rot = wind_R.to_euler() if kind in ("chop", "slash") else rot
            kit.key_loc(tool, 1, wind_loc)
            kit.key_rot(tool, 1, wind_rot)
            held = max(f_start - (SWING if kind in ("chop", "slash") else 1), 1)
            kit.key_loc(tool, held, wind_loc)
            kit.key_rot(tool, held, wind_rot)
            st.windups.append((tool, held))
            # judged as the blade arrives: by the stroke's end it has passed the piece
            st.contacts.append((tool, tuple(E), pieces[0] if "through" in stroke else target, f_start + 1))
        else:
            kit.key_loc(tool, f_start, start_loc + Vector((0, 0, 0.03)))
            kit.key_rot(tool, f_start, rot)
        kit.key_loc(tool, f_start, start_loc)
        kit.key_rot(tool, f_start, rot)
        kit.key_loc(tool, f_end, end_loc)
        kit.key_rot(tool, f_end, rot)
        kit.interpolation(tool, "QUAD", {f_start} | ({held} if s_i == 0 else set()), "EASE_IN")  # the swing speeds up
        stroke_frames.append((f_start, f_end))
    last_end = stroke_frames[-1][1]
    # recoil and leave the frame
    kit.key_loc(tool, min(last_end + 3, st.frames), tool.location - d * 0.04 + Vector((0, 0, 0.05)))
    kit.key_loc(tool, min(last_end + 16, st.frames), tool.location + Vector((0, 0, 2.5)) - d * 0.6)
    st.threat = st.threat or tool

    first = stroke_frames[0][1]
    kit.remove_body(target)  # hidden from the first stroke on, it must not push the pieces around
    kit.key_vis(target, 1, True)
    kit.key_vis(target, first, False)
    for p in pieces:
        kit.key_vis(p, 1, False)
        kit.key_vis(p, first, True)
    st.intact[tid] = target
    st.pieces[tid] = pieces
    for p in pieces + [target]:
        st.allow(tool, p, range(stroke_frames[0][0], min(last_end + 4, st.frames) + 1))
    for i, p in enumerate(pieces):  # pieces of one cut may touch each other
        for q in pieces[i + 1:]:
            st.allow(p, q, range(1, st.frames + 1))

    # what each piece does once it's free
    support = st.support_obj(tid)
    ends = beat.get("ends", {}).get("on")
    rest_on = st.ground if ends == "ground" else st.objs.get(ends, support) if ends else support
    rng = random.Random(5)
    for i, (p, (name, _)) in enumerate(zip(pieces, bms)):
        # a piece the plan didn't name stays with the rest; cut_result then reports the mismatch to the planner
        e = next((x for x in named if x["piece"] == name), None) or next((x for x in expect if "pieces" in x), None) \
            or next((x for x in named if x["piece"] == "rest"), {"then": "stay"})
        then = e["then"]
        k = min(free_stroke.get(i, 0), len(stroke_frames) - 1)
        free = min(stroke_frames[k][1] + 1, st.frames)
        away = (sum(kit.world_verts(p), Vector()) / len(p.data.vertices) - mid)
        away.z = 0
        away = away.normalized() if away.length > 1e-6 else st.cam_h.copy()
        if then == "stay":
            if name == "rest":
                st.objs[tid] = p
            kit.make_static(p)
            kit.layers(p, [1])
            st.resting.append((p, rest_on))
        elif then == "fly_off":
            release(st, p, free, launch=away * 0.9 + Vector((0, 0, 1.6)), spin=Vector((4, 7, 2)))
        elif then == "scatter":
            a = rng.uniform(0, 2 * math.pi)  # a gentle spread, not a blast (the first mince exploded)
            release(st, p, free, launch=away * 0.06 + Vector((math.cos(a) * 0.03, math.sin(a) * 0.03, 0.05)),
                    spin=Vector((rng.uniform(-2, 2), rng.uniform(-2, 2), 0)))
            st.resting.append((p, rest_on, pieces))
        elif then == "tip_over":
            release(st, p, free, launch=away * 0.12, spin=Vector((0, 0, 1)).cross(away) * -3.0)
            st.resting.append((p, rest_on, pieces))
        else:  # fall
            release(st, p, free)
            st.resting.append((p, rest_on, pieces))
    st.cuts.append((pieces, total, expect, shares))
    st.moved_from.setdefault(tid, first)
