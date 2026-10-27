"""Entry point: blender.exe -b --factory-startup --python blender/opener_scene.py -- <opener_job.json>

Builds a Short's opener (scene 1) from its staging plan (shortsmaker/opener_plan.py, 2026-10-27): the set and the
brand look, the library models, the moves (moves.py), then runs every check (opener_checks.py) and renders PNG frames
(frames_dir/f_0001.png ...). Job: {"plan", "models": {actor id or "backdrop:N": .blend path or "primitive:cube"},
"seconds", "fps", "size": [w, h], "frames_dir", "report", "render": bool, "render_failed": bool, "render_scale": %}.
The report: {"ok", "failures", "pieces", "frames", "cut_shares", "lowest"}. Exit code 0 even when checks fail."""

import json
import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import moves  # noqa: E402
import opener_checks as oc  # noqa: E402
import scene_kit as kit  # noqa: E402

YAW = {"front": 0, "three_quarter": 40, "side": 90, "top": 25}
PITCH = {"front": 12, "three_quarter": 12, "side": 10, "top": 60}
LENS, FSTOP = 50, 2.2
FILL = 0.6  # the subject's width fills at most this much of the frame
SUBJECT_FILL = 0.35  # and its height this much, at the start
PUSH_IN = 0.85  # the camera ends this much closer
ORBIT = 14  # degrees the camera arcs around the subject over the clip (owner, 2026-10-27: the locked-off shot read flat)
PUNCH_LENS = 62  # on the first hit the lens snaps to this, then eases back toward LENS
SHAKE, SHAKE_FRAMES = 0.012, 9  # hit shake as a share of the camera distance, gone after this many frames
DRIFT = 0.004  # handheld sway, share of the distance
SLOW, SLOW_BEFORE, SLOW_AFTER = 0.5, 3, 9  # the hit plays at half speed over these scene frames; the rest runs
# a little faster so the clip keeps its length (scene 1 is timed to the voice)
BURST = 24  # feathers knocked off where the blade lands
RISE = 16  # degrees the camera cranes up over the clip, so a subject stepping down stays seen over its support


def setup(job: dict) -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.fps = job["fps"]
    sc.frame_start, sc.frame_end = 1, max(2, round(job["seconds"] * job["fps"]))
    sc.render.resolution_x, sc.render.resolution_y = job["size"]
    sc.render.resolution_percentage = job.get("render_scale", 100)
    for engine in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            sc.render.engine = engine
            break
        except TypeError:
            continue
    try:
        sc.eevee.taa_render_samples = 16
    except AttributeError:
        pass
    sc.view_settings.view_transform = "AgX"
    sc.render.use_motion_blur, sc.render.motion_blur_shutter = True, 0.5  # a fast blade smears instead of stepping


def build_set(plan: dict, models: dict, cam_dir: Vector) -> object:
    sc = bpy.context.scene
    st, light = plan["set"], kit.TABLES["lights"][plan["set"].get("light", "day")]
    w = bpy.data.worlds.new("sky")
    sc.world = w
    w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs["Color"].default_value = (*light["sky"], 1)
    bg.inputs["Strength"].default_value = 0.8
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy, sun.data.color, sun.data.angle = light["sun"], light["color"], math.radians(8)
    sun.rotation_euler = (math.radians(55), 0, math.radians(-40))
    sc.collection.objects.link(sun)
    bpy.ops.mesh.primitive_plane_add(size=60)
    ground = bpy.context.active_object
    ground.name = "ground"
    ground.data.materials.append(kit.material("ground", kit.TABLES["grounds"][st["ground"]]))
    kit.make_static(ground)
    back = -cam_dir.normalized()
    back.z = 0
    back.normalize()
    across = kit.view(Vector((1, 0, 0)))
    edges = [0.0, 0.0]  # how far the row of backdrops reaches right and left of the centre
    for i, b in enumerate(st.get("backdrop") or []):
        o = kit.load_model(models[f"backdrop:{i}"], f"backdrop{i}")
        kit.fit(o, b["size_m"], "camera")
        wide = [v.co.dot(across) for v in o.data.vertices]
        deep = [v.co.dot(back) for v in o.data.vertices]
        half_w, half_d = (max(wide) - min(wide)) / 2, (max(deep) - min(deep)) / 2
        # side by side across the shot, alternating, 0.5 m apart: a fence and a barn offset 2.5 m overlapped
        if i == 0:
            shift, edges = 0.0, [half_w, half_w]
        else:
            k = (i + 1) % 2  # 1 = right, 0 = left
            shift = (edges[k] + 0.5 + half_w) * (1 if k else -1)
            edges[k] += 0.5 + 2 * half_w
        o.location = back * (half_d + 5 + i) + across * shift
    return ground


def place_actors(plan: dict, models: dict, st: moves.State) -> None:
    tools = {b["tool"] for b in plan["beats"] if b["move"] == "cut"}
    for a in plan["actors"]:
        o = kit.load_model(models[a["id"]], a["id"])
        kit.fit(o, a["size_m"], a.get("facing", "camera"), view=a["id"] not in tools)
        st.objs[a["id"]] = o
        st.support[a["id"]] = a.get("on") or "ground"
    bpy.context.view_layer.update()
    # supports and free actors on the ground in a row around the origin, then everything standing on something
    on_ground = [a["id"] for a in plan["actors"] if a.get("on") in (None, "ground") and a["id"] not in tools]
    x = 0.0
    for k, aid in enumerate(on_ground):
        o = st.objs[aid]
        lo, hi = kit.bbox(o)
        width = max(hi.x - lo.x, hi.y - lo.y)  # either way round, the camera may sit on any side
        if k:
            x += width / 2
        o.location = kit.view(Vector((x if k % 2 == 0 else -x, 0, 0)))  # a row across the shot
        x += width / 2 + 0.3
    placed: set = set(on_ground) | tools
    while len(placed) < len(plan["actors"]):
        before = len(placed)
        for a in plan["actors"]:
            if a["id"] in placed or a.get("on") not in placed and a.get("on") not in (None, "ground"):
                continue
            sup = st.objs[a["on"]]
            bpy.context.view_layer.update()
            st.objs[a["id"]].location = stand_on(st.objs[a["id"]], sup,
                                                 [st.objs[b["id"]] for b in plan["actors"]
                                                  if b.get("on") == a["on"] and b["id"] in placed])
            placed.add(a["id"])
        if len(placed) == before:  # clean_opener rejects cycles; never loop forever on one anyway
            raise SystemExit("opener: actors stand on each other in a circle")
    for aid in tools:  # out of sight until its stroke keys place it
        st.objs[aid].location = (0, 0, -50)
    bpy.context.view_layer.update()
    for a in plan["actors"]:
        if a["id"] not in tools:
            kit.make_static(st.objs[a["id"]])


def stand_on(o, sup, neighbours: list) -> Vector:
    """Where o stands on top of sup: of spots on its top, the one where o's whole footprint clears the surface with
    its feet (origin) closest to touching it, near the middle and away from what already stands there. The probe's
    first placement at the centre point dipped the rooster into the uneven moss."""
    t = kit.tree(sup)
    lo, hi = kit.bbox(sup)
    verts = [v.co.copy() for v in o.data.vertices]  # o's own space: origin at its bottom centre
    best = None
    for i in range(7):
        for j in range(7):
            cx = lo.x + (0.15 + 0.7 * i / 6) * (hi.x - lo.x)
            cy = lo.y + (0.15 + 0.7 * j / 6) * (hi.y - lo.y)
            under = t.ray_cast(Vector((cx, cy, 1000)), Vector((0, 0, -1)))[0]
            if under is None:
                continue
            lift = under.z
            for v in verts:
                hit = t.ray_cast(Vector((cx + v.x, cy + v.y, 1000)), Vector((0, 0, -1)))[0]
                if hit is not None:
                    lift = max(lift, hit.z - v.z)
            crowd = sum(1 for n in neighbours if (n.location.xy - Vector((cx, cy))).length < 0.15)
            score = (lift - under.z) + 0.05 * Vector((cx - (lo.x + hi.x) / 2, cy - (lo.y + hi.y) / 2)).length + crowd
            if best is None or score < best[0]:
                best = (score, Vector((cx, cy, lift + 0.001)))
    return best[1] if best else Vector(((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, hi.z + 0.001))


def camera(plan: dict, st: moves.State, subject_id: str) -> bpy.types.Object:
    sc = bpy.context.scene
    angle = plan["camera"]["angle"]
    yaw, pitch = math.radians(YAW[angle]), math.radians(PITCH[angle])
    sc.frame_set(1)
    # framed on the subject (a 30 cm knife beside a 9 cm onion made the onion 10% of the frame); the start aim leans
    # toward the threat so it shows too, which the first-frame check confirms
    first = st.intact.get(subject_id, st.objs[subject_id])
    lo, hi = kit.bbox(first)
    size = hi - lo
    vfov = 2 * math.atan(18 / LENS)
    hfov = 2 * math.atan(18 * sc.render.resolution_x / sc.render.resolution_y / LENS)
    # starts wider by the push-in, so the push ends on this framing instead of past it (the crate left the frame)
    dist = (max(size.z / SUBJECT_FILL / (2 * math.tan(vfov / 2)),
                max(size.x, size.y) / FILL / (2 * math.tan(hfov / 2))) + max(size.x, size.y) / 2) / PUSH_IN
    aim = bpy.data.objects.new("aim", None)
    sc.collection.objects.link(aim)
    start = (lo + hi) / 2
    if st.threat is not None and st.threat is not first:
        tlo, thi = kit.bbox(st.threat)
        start = start.lerp((tlo + thi) / 2, 0.15)  # 0.3 pushed a profile rooster off the frame edge
    # the subject is always followed once it moves (the Mike plan left follow out and the rooster walked off alone)
    follow = plan["camera"].get("follow") or subject_id
    moved = st.moved_from.get(follow, sc.frame_end + 1)
    hit = first_hit(st)
    rng = random.Random(7)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.data.lens = LENS
    cam.data.dof.use_dof, cam.data.dof.aperture_fstop, cam.data.dof.focus_object = True, FSTOP, aim
    n = max(sc.frame_end - 1, 1)
    for f in range(1, sc.frame_end + 1):
        target = start
        if f >= moved:
            sc.frame_set(f)
            blo, bhi = kit.bbox(st.objs[follow])
            target = start.lerp((blo + bhi) / 2, min(1.0, (f - moved) / 6))
        t = (f - 1) / n
        ease = t * t * (3 - 2 * t)
        y, p = yaw + math.radians(ORBIT) * (ease - 0.5), pitch + math.radians(RISE) * ease
        v = Vector((math.sin(y) * math.cos(p), -math.cos(y) * math.cos(p), math.sin(p)))
        sway = Vector((math.sin(f * 0.21), math.sin(f * 0.17 + 2), math.sin(f * 0.13 + 1))) * DRIFT * dist
        if hit is not None and 0 <= f - hit < SHAKE_FRAMES:  # moves aim and camera together so the frame jolts
            sway += Vector([rng.uniform(-1, 1) for _ in range(3)]) * SHAKE * dist * (1 - (f - hit) / SHAKE_FRAMES)
        kit.key_loc(aim, f, target + sway)
        kit.key_loc(cam, f, target + sway + v * dist * (1 - (1 - PUSH_IN) * ease))
    con = cam.constraints.new("TRACK_TO")
    con.target, con.track_axis, con.up_axis = aim, "TRACK_NEGATIVE_Z", "UP_Y"
    return cam


def first_hit(st: moves.State) -> int | None:
    """The hit: the first blade contact, else the first thing that moves."""
    hits = [c[3] for c in st.contacts] or list(st.moved_from.values())
    return min(hits) if hits else None


def punch_in(cam, st: moves.State, subject_id: str) -> None:
    """On the hit the lens snaps in, then eases half back; the strongest punch that keeps the subject in frame (a
    62 mm punch pushed the reference crate, which already fills the frame, out of it)."""
    sc = bpy.context.scene
    hit = first_hit(st)
    for top in (PUNCH_LENS, (LENS + PUNCH_LENS) / 2):
        cam.data.animation_data_clear()
        cam.data.lens = LENS
        if hit is None:
            return
        for f, lens in ((1, LENS), (hit, LENS), (min(hit + 2, sc.frame_end), top), (sc.frame_end, (LENS + top) / 2)):
            cam.data.lens = lens
            cam.data.keyframe_insert("lens", frame=f)
        if not any(oc.in_frame(o, cam, fr) for o, fr in subject_segments(subject_id, st, sc.frame_end)):
            return
    cam.data.animation_data_clear()
    cam.data.lens = LENS


def retime(n: int, hit: int | None) -> list[float]:
    """Scene time for each of the n output frames: slow motion around the hit, the same length overall."""
    if hit is None or n < 40:
        return [float(f) for f in range(1, n + 1)]
    a, b = max(1, hit - SLOW_BEFORE), min(n, hit + SLOW_AFTER)
    fast = (n - 1 - (b - a)) / (n - 1 - (b - a) / SLOW)
    out, t = [], 1.0
    for _ in range(n):
        out.append(min(t, float(n)))
        t += SLOW if a <= t < b else fast
    return out


def feather_colours(obj, near: Vector, k: int) -> list[tuple]:
    """k colours of obj's surface around `near`, read from its texture where it has one (a rooster's neck is orange
    and red, not the whole bird's black)."""
    import numpy as np
    mat = next((m for m in obj.data.materials if m and m.node_tree), None)
    img = next((n.image for n in mat.node_tree.nodes if n.type == "TEX_IMAGE" and n.image), None) if mat else None
    if img is None or not obj.data.uv_layers:
        bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None) if mat else None
        return [tuple(bsdf.inputs["Base Color"].default_value)[:3] if bsdf else (0.5, 0.45, 0.4)]
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    px = px.reshape(h, w, 4)
    uv = obj.data.uv_layers.active.data
    mw = obj.matrix_world
    polys = sorted(obj.data.polygons, key=lambda p: ((mw @ p.center) - near).length)[:60]
    rng = random.Random(3)
    out = []
    for p in rng.sample(polys, min(k, len(polys))):
        u, v = uv[p.loop_start].uv
        c = px[min(int(v % 1 * h), h - 1), min(int(u % 1 * w), w - 1)]
        out.append(tuple(float(x) for x in c[:3]))
    return out


def feather(name: str, length: float, rgb) -> bpy.types.Object:
    """A flat, slightly curled feather, its origin at the middle."""
    import bmesh
    w = length * 0.32
    bm = bmesh.new()
    pts = [(0, -0.5), (0.5, -0.15), (0.38, 0.22), (0, 0.5), (-0.38, 0.22), (-0.5, -0.15)]
    bm.faces.new([bm.verts.new((x * w, y * length, 0.12 * length * (y * 2) ** 2)) for x, y in pts])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(kit.material(name, rgb))
    return bpy.data.objects.new(name, me)


def burst(st: moves.State) -> None:
    """Feathers (or chips) knocked off where the blade lands, in the colours there, drifting down to settle on the
    ground. Added after the checks: it is only a look, nothing touches it. The first try threw textured spheres
    with no UVs, grey blobs the owner called weird (2026-10-27)."""
    if not st.contacts:
        return
    sc = bpy.context.scene
    tool, _, target, frame = min(st.contacts, key=lambda c: c[3])
    sc.frame_set(frame)
    at = kit.tree(target).find_nearest(tool.matrix_world @ moves.edge_point_local(tool))[0]  # on the target, not the blade
    # sized from the whole uncut target: the head piece made 1 cm bits nobody could see
    whole = next((st.intact[k] for k, v in st.pieces.items() if target in v and k in st.intact), target)
    lo, hi = kit.bbox(whole)
    size = max((hi - lo).length, 0.05)
    bits = bpy.data.collections.new("bits")
    for i, rgb in enumerate(feather_colours(whole, at, 4)):
        bits.objects.link(feather(f"feather{i}", size * 0.11, rgb))  # not in the scene: only its instances show
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=size * 0.03, location=at)
    em = bpy.context.active_object
    em.name = "burst"
    em.show_instancer_for_render = em.show_instancer_for_viewport = False
    ps = em.modifiers.new("burst", "PARTICLE_SYSTEM").particle_system.settings
    # out when the first piece comes loose (the contact frame is the stroke's start: bits came out before the blade landed)
    frame = min([f for f in st.released.values() if f >= frame] or [frame])
    ps.count, ps.frame_start, ps.frame_end, ps.lifetime = BURST, frame, frame + 2, st.frames
    # random faces of a round emitter and a random kick: a spray every way (12 vertices threw 12 clumps)
    ps.emit_from, ps.distribution, ps.normal_factor, ps.factor_random = "FACE", "RAND", size * 2.5, size * 1.5
    ps.render_type, ps.instance_collection, ps.use_collection_pick_random = "COLLECTION", bits, True
    ps.particle_size, ps.size_random = 1.0, 0.5
    ps.use_rotations, ps.angular_velocity_mode, ps.angular_velocity_factor = True, "RAND", 6
    ps.phase_factor_random = 2.0
    # feathers: light, dragged by the air, a little flutter; they come to rest on the ground
    ps.effector_weights.gravity, ps.mass, ps.drag_factor, ps.brownian_factor = 0.5, 0.005, 0.6, size * 0.4
    ps.use_die_on_collision = False
    st.ground.modifiers.new("feathers", "COLLISION")
    st.ground.collision.damping_factor, st.ground.collision.friction_factor = 0.9, 1.0


def render(job: dict, times: list[float]) -> None:
    sc = bpy.context.scene
    frames_dir = Path(job["frames_dir"])
    frames_dir.mkdir(parents=True, exist_ok=True)
    sc.render.image_settings.file_format = "PNG"
    for i, t in enumerate(times, 1):  # in order: physics and particles read their caches forward
        sc.frame_set(int(t), subframe=t - int(t))
        sc.render.filepath = str(frames_dir / f"f_{i:04d}.png")
        bpy.ops.render.render(write_still=True)


def hold_offscreen(st: moves.State, cam) -> dict[str, bool]:
    """No people models, so a tool is swung by an unseen hand (owner, 2026-10-27): its wind-up is moved away from
    the subject until the handle end runs off the frame while the blade stays in it, so it reads as held from
    off-screen, not floating. {tool name: done}."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    done = {}
    for tool, last in st.windups:
        sc.frame_set(1)
        handle = tool.matrix_world @ moves.handle_end_local(tool)
        head = tool.matrix_world @ moves.edge_point_local(tool)
        away = handle - head
        away.normalize()
        start = kit.loc_at(tool, 1)
        ok = False
        for k in range(0, 40):
            shift = away * 0.04 * k
            h = world_to_camera_view(sc, cam, handle + shift)
            b = world_to_camera_view(sc, cam, head + shift)
            off = not (0 <= h.x <= 1 and 0 <= h.y <= 1)
            if off and 0.02 <= b.x <= 0.98 and 0.02 <= b.y <= 0.98:
                for f in (1, last):
                    kit.key_loc(tool, f, start + shift)
                ok = True
                break
        done[tool.name] = ok
    return done


def subject_segments(subject_id: str, st: moves.State, frames: int) -> list[tuple]:
    """(object, frames) to keep in frame: the uncut subject until its cut, then its "rest" piece if it has one."""
    if subject_id not in st.intact:
        return [(st.objs[subject_id], range(1, frames + 1))]
    first = st.moved_from.get(subject_id, frames + 1)
    segs = [(st.intact[subject_id], range(1, first))]
    rest = next((p for p in st.pieces[subject_id] if p.get("piece") == "rest"), None)
    if rest is not None:
        segs.append((rest, range(first, frames + 1)))
    return segs


def checks(plan: dict, st: moves.State, cam, subject_id: str) -> list[str]:
    sc = bpy.context.scene
    frames = range(1, sc.frame_end + 1)
    out = list(st.failures)
    meshes = [o for o in sc.objects if o.type == "MESH" and o.name != "ground"]
    allowed = dict(st.allowed)
    for o in meshes:  # physics bodies only touch: depth is the resting check's job
        if o.name in st.released:
            for p in meshes:
                if p is not o:
                    allowed.setdefault(frozenset((o.name, p.name)), set()).update(range(st.released[o.name], sc.frame_end + 1))
    out += oc.overlaps(meshes, frames, allowed)
    tools = {st.objs[b["tool"]] for b in plan["beats"] if b["move"] == "cut"}
    own = set(st.pieces.get(subject_id, [])) | {st.intact.get(subject_id)}
    occluders = [o for o in meshes if o not in tools and o not in own]
    for obj, fr in subject_segments(subject_id, st, sc.frame_end):
        out += oc.in_frame(obj, cam, fr)
        out += oc.hidden(obj, cam, fr, occluders)
    first_subject = st.intact.get(subject_id, st.objs[subject_id])
    out += oc.first_frame(first_subject, st.threat or first_subject, cam)
    for tool, axis, target, frame in st.contacts:
        out += oc.edge_leads(tool, axis, target, frame)
        out += oc.blade_face(tool, cam, frame)
    for pieces, total, expect, _ in st.cuts:
        out += oc.cut_result(pieces, total, expect)
    out += oc.resting(st.resting, [sc.frame_end])
    return out


def main(job_path: str) -> None:
    job = json.loads(Path(job_path).read_text(encoding="utf-8"))
    plan = job["plan"]
    setup(job)
    sc = bpy.context.scene
    yaw = math.radians(YAW[plan["camera"]["angle"]])
    kit.VIEW_YAW = yaw
    cam_h = Vector((math.sin(yaw), -math.cos(yaw), 0))
    st = moves.State(plan, job["fps"], sc.frame_end, cam_h)
    st.ground = build_set(plan, job["models"], cam_h)
    place_actors(plan, job["models"], st)
    for beat in sorted(plan["beats"], key=lambda b: b["at"]):
        try:
            moves.apply(beat, st)
        except Exception as e:  # a move it can't build is a failure the planner can fix, not a crash that says nothing
            report = {"ok": False, "failures": [f"{beat['move']}: could not be built ({type(e).__name__}: {e})"],
                      "frames": sc.frame_end, "pieces": 0, "cut_shares": {}, "lowest": {}, "held_offscreen": {}}
            Path(job["report"]).write_text(json.dumps(report, indent=1), encoding="utf-8")
            return
    for o in st.objs.values():
        kit.interpolation(o, "BEZIER", set())  # visibility and physics switches CONSTANT
    kit.simulate()
    tools = {b["tool"] for b in plan["beats"] if b["move"] == "cut"}
    # the subject is what the action happens to, not whatever is listed first (the fifth live run judged the stump)
    first = sorted(plan["beats"], key=lambda b: b["at"])[0]
    subject_id = plan["camera"].get("follow") or first.get("target") or first.get("actor") \
        or next(a["id"] for a in plan["actors"] if a["id"] not in tools)
    cam = camera(plan, st, subject_id)
    punch_in(cam, st, subject_id)
    held = hold_offscreen(st, cam)
    failures = checks(plan, st, cam, subject_id)
    sc.frame_set(sc.frame_end)
    lowest = {aid: round(min(v.z for v in kit.world_verts(o)), 4) for aid, o in st.objs.items()
              if aid not in tools}
    report = {"ok": not failures, "failures": failures, "frames": sc.frame_end,
              "pieces": sum(len(p) for p, *_ in st.cuts),
              "cut_shares": {k: v for *_, s in st.cuts for k, v in s.items()}, "lowest": lowest,
              "held_offscreen": held, "stroke_toward_camera": st.stroke_toward,
              "key_frames": []}
    times = retime(sc.frame_end, first_hit(st))
    # key moments as output frames: the review picks them from the rendered (retimed) frames
    report["key_frames"] = sorted({next((i for i, t in enumerate(times, 1) if t >= k), len(times))
                                   for k in {c[3] + 2 for c in st.contacts} | set(st.moved_from.values())})
    if job.get("render", True) and (report["ok"] or job.get("render_failed")):
        burst(st)
        kit.simulate()  # the burst's ground collider dropped the physics cache; slow-motion subframes can't rebuild it
        render(job, times)
    Path(job["report"]).write_text(json.dumps(report, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1])
