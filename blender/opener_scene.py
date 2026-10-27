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
import people  # noqa: E402
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
    # the sun 135 degrees round from where the camera looks: side and back light shows form and rims the subject,
    # front light flattened it (owner, 2026-10-27: "the light is flat"; blender-time-of-day skill)
    look = -cam_dir
    heading = math.atan2(look.x, look.y) + math.radians(135)
    el = math.radians(light.get("elevation", 35))
    to_sun = Vector((math.sin(heading) * math.cos(el), math.cos(heading) * math.cos(el), math.sin(el)))
    if "elevation" in light:  # a measured sky to match the sun (Multiple Scattering, Blender 5.x); night stays flat
        sky = w.node_tree.nodes.new("ShaderNodeTexSky")
        try:
            sky.sky_type = "MULTIPLE_SCATTERING"
        except TypeError:
            pass
        sky.sun_disc, sky.sun_elevation, sky.sun_rotation = False, el, heading
        w.node_tree.links.new(sky.outputs["Color"], bg.inputs["Color"])
        bg.inputs["Strength"].default_value = 0.0285 * 1.4  # the skill's sky-to-scene scale, a touch brighter for AgX
    else:
        bg.inputs["Color"].default_value = (*light["sky"], 1)
        bg.inputs["Strength"].default_value = 0.8
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy, sun.data.color, sun.data.angle = light["sun"], light["color"], math.radians(3)
    sun.rotation_euler = Vector((0, 0, 1)).rotation_difference(to_sun).to_euler()
    sc.collection.objects.link(sun)
    bpy.ops.mesh.primitive_plane_add(size=400)  # to the horizon: past its edge the sky shows a dark "ground"
    ground = bpy.context.active_object
    ground.name = "ground"
    ground.data.materials.append(ground_material(kit.TABLES["grounds"][st["ground"]]))
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


def ground_material(rgb) -> bpy.types.Material:
    """The ground's colour broken up by soft patches, lighter and darker: one flat colour read as a floor, not earth."""
    m = kit.material("ground", rgb)
    nt = m.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value, noise.inputs["Detail"].default_value = 1.2, 6.0
    amount = nt.nodes.new("ShaderNodeMath")
    amount.operation, amount.inputs[1].default_value, amount.inputs[2].default_value = "MULTIPLY_ADD", 0.5, 0.75
    nt.links.new(noise.outputs["Fac"], amount.inputs[0])
    tint = nt.nodes.new("ShaderNodeVectorMath")
    tint.operation = "SCALE"
    tint.inputs[0].default_value = rgb
    nt.links.new(amount.outputs[0], tint.inputs["Scale"])
    nt.links.new(tint.outputs[0], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.95
    return m


DRESS = {"grass": ("tuft", "stone"), "dirt": ("tuft", "stone"), "sand": ("stone",), "snow": ("stone",),
         "stone": ("stone",)}  # what lies about on each ground; floors, tables and water stay clear


def dress_set(plan: dict, st: moves.State) -> None:
    """Tufts and stones scattered behind and beside the action, never on its ground or between it and the camera:
    the yard was one bare plane (owner, 2026-10-27). Added after the checks: it is only a look."""
    kinds = DRESS.get(plan["set"]["ground"])
    if not kinds:
        return
    sc = bpy.context.scene
    reach = 0.0  # how far anything goes from the middle over the clip
    for f in range(1, sc.frame_end + 1, 5):
        for o in st.objs.values():
            reach = max(reach, kit.loc_at(o, f).xy.length)
    reach += 0.8
    across = Vector((-st.cam_h.y, st.cam_h.x, 0))
    rng = random.Random(9)
    parts = bpy.data.collections.new("dressing")
    sc.collection.children.link(parts)
    greens = [(0.24, 0.38, 0.12), (0.32, 0.42, 0.15), (0.2, 0.3, 0.1)]
    greys = [(0.42, 0.4, 0.37), (0.5, 0.47, 0.42), (0.33, 0.32, 0.3)]
    placed = 0
    while placed < 140:
        r = reach + rng.uniform(0, 7)
        a = rng.uniform(0, 2 * math.pi)
        p = Vector((math.cos(a) * r, math.sin(a) * r, 0))
        if p.dot(st.cam_h) > 0.3 * reach and abs(p.dot(across)) < r:  # in front: between the camera and the action
            continue
        kind = rng.choice(kinds)
        if kind == "tuft":
            h = rng.uniform(0.08, 0.2)
            bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=h * 0.35, depth=h, location=(p.x, p.y, h / 2))
            ob = bpy.context.active_object
            ob.rotation_euler = (rng.uniform(-0.25, 0.25), rng.uniform(-0.25, 0.25), rng.uniform(0, 6.3))
            ob.data.materials.append(kit.material(f"tuft{placed % 3}", greens[placed % 3]))
        else:
            s = rng.uniform(0.03, 0.12)
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=s, location=(p.x, p.y, s * 0.25))
            ob = bpy.context.active_object
            ob.scale = (rng.uniform(0.8, 1.3), rng.uniform(0.8, 1.3), rng.uniform(0.4, 0.7))
            ob.rotation_euler.z = rng.uniform(0, 6.3)
            ob.data.materials.append(kit.material(f"stone{placed % 3}", greys[placed % 3]))
        for c in ob.users_collection:
            c.objects.unlink(ob)
        parts.objects.link(ob)
        placed += 1


def place_actors(plan: dict, models: dict, st: moves.State, lib: dict | None = None) -> None:
    tools = {b["tool"] for b in plan["beats"] if b["move"] == "cut"}
    frames = set(range(1, bpy.context.scene.frame_end + 1))
    for a in plan["actors"]:
        if "person" in a:  # people (part 2): dressed from the library; their hat and prop may touch them
            o = people.dress(a, kit.TABLES["roles"][a["person"]], lib, models)
            for item in (o.get("hat"), o.get("prop")):
                if item:
                    st.allow(o, bpy.data.objects[item], frames)
        else:
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
    its feet (origin) closest to touching it, its feet near the middle and away from what already stands there.
    The probe's first placement at the centre point dipped the rooster into the uneven moss; every foot has the
    support under it, and the feet (not the origin, which can sit behind them) are what is centred: the Mike rooster
    stood on the rim with its toes over the edge (owner, 2026-10-27)."""
    t = kit.tree(sup)
    lo, hi = kit.bbox(sup)
    mid = Vector(((lo.x + hi.x) / 2, (lo.y + hi.y) / 2))
    radius = max(hi.x - lo.x, hi.y - lo.y) / 2 or 1.0
    verts = [v.co.copy() for v in o.data.vertices]  # o's own space: origin at its bottom centre
    z0 = min(v.z for v in verts)
    feet = [v for v in verts if v.z < z0 + 0.03 * ((max(v.z for v in verts) - z0) or 1)]
    foot_c = sum((v for v in feet), Vector()) / len(feet)
    best = None
    for i in range(9):
        for j in range(9):
            cx = lo.x + (0.1 + 0.8 * i / 8) * (hi.x - lo.x)
            cy = lo.y + (0.1 + 0.8 * j / 8) * (hi.y - lo.y)
            under = t.ray_cast(Vector((cx, cy, 1000)), Vector((0, 0, -1)))[0]
            if under is None or any(t.ray_cast(Vector((cx + v.x, cy + v.y, 1000)), Vector((0, 0, -1)))[0] is None
                                    for v in feet):
                continue
            lift = under.z
            for v in verts:
                hit = t.ray_cast(Vector((cx + v.x, cy + v.y, 1000)), Vector((0, 0, -1)))[0]
                if hit is not None:
                    lift = max(lift, hit.z - v.z)
            crowd = sum(1 for n in neighbours if (n.location.xy - Vector((cx, cy))).length < 0.15)
            off = (Vector((cx + foot_c.x, cy + foot_c.y)) - mid).length / radius
            score = (lift - under.z) + 0.03 * off + crowd  # 3 cm of float weighs the same as standing on the rim
            if best is None or score < best[0]:
                best = (score, Vector((cx, cy, lift + 0.001)))
    return best[1] if best else Vector((mid.x - foot_c.x, mid.y - foot_c.y, hi.z + 0.001))


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
    out = list(st.failures) + oc.staging(plan, kit.TABLES["gaits"])
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
    for prop, frame in st.swings:
        out += oc.blade_face(prop, cam, frame)
    for a in plan["actors"]:  # a person's planned prop shows in frame 0
        if a.get("person") and a.get("prop") and st.objs[a["id"]].get("prop"):
            out += oc.prop_shown(bpy.data.objects[st.objs[a["id"]]["prop"]], cam)
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
    lib = people.load_library(job) if any("person" in a for a in plan["actors"]) else None
    place_actors(plan, job["models"], st, lib)
    st.people = lib
    for o in st.objs.values():
        if o.get("person"):
            people.idle(o, lib)
    starts = {aid: o.matrix_world.translation.copy() for aid, o in st.objs.items()}
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
    highest = {aid: round(max(v.z for v in kit.world_verts(o)), 4) for aid, o in st.objs.items() if aid not in tools}
    for aid, o in st.objs.items():  # a person's prop, e.g. "officer.prop", where it ends up
        if o.get("prop"):
            lowest[f"{aid}.prop"] = round(min(v.z for v in kit.world_verts(bpy.data.objects[o["prop"]])), 4)
    moved = {aid: round((o.matrix_world.translation - starts[aid]).length, 4) for aid, o in st.objs.items()
             if aid in starts and aid not in tools}
    report = {"ok": not failures, "failures": failures, "frames": sc.frame_end,
              "pieces": sum(len(p) for p, *_ in st.cuts),
              "cut_shares": {k: v for *_, s in st.cuts for k, v in s.items()}, "lowest": lowest,
              "highest": highest, "moved": moved, "swings": [p.name for p, _ in st.swings],
              "held_offscreen": held, "stroke_toward_camera": st.stroke_toward,
              "key_frames": []}
    times = retime(sc.frame_end, first_hit(st))
    # key moments as output frames: the review picks them from the rendered (retimed) frames
    report["key_frames"] = sorted({next((i for i, t in enumerate(times, 1) if t >= k), len(times))
                                   for k in {c[3] + 2 for c in st.contacts} | set(st.moved_from.values())})
    if job.get("render", True) and (report["ok"] or job.get("render_failed")):
        dress_set(plan, st)
        kit.simulate()  # what's added after the checks can drop the physics cache; slow-motion subframes can't rebuild it
        render(job, times)
    Path(job["report"]).write_text(json.dumps(report, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1])
