"""Entry point: blender.exe -b --factory-startup --python blender/opener_scene.py -- <opener_job.json>

Builds a Short's opener (scene 1) from its staging plan (shortsmaker/opener_plan.py, 2026-10-27): the set and the
brand look, the library models, the moves (moves.py), then runs every check (opener_checks.py) and renders PNG frames
(frames_dir/f_0001.png ...). Job: {"plan", "models": {actor id or "backdrop:N": .blend path or "primitive:cube"},
"seconds", "fps", "size": [w, h], "frames_dir", "report", "render": bool, "render_failed": bool, "render_scale": %}.
The report: {"ok", "failures", "pieces", "frames", "cut_shares", "lowest"}. Exit code 0 even when checks fail."""

import json
import math
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
PUSH_IN = 0.92  # the camera ends this much closer


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
    for i, b in enumerate(st.get("backdrop") or []):
        o = kit.load_model(models[f"backdrop:{i}"], f"backdrop{i}")
        kit.fit(o, b["size_m"], "camera")
        lo, hi = kit.bbox(o)
        back = -cam_dir.normalized()
        back.z = 0
        o.location = back.normalized() * (max(hi.x - lo.x, hi.y - lo.y) / 2 + 5 + 3 * i) + Vector((2.5 * (-1) ** i, 0, 0))
    return ground


def place_actors(plan: dict, models: dict, st: moves.State) -> None:
    tools = {b["tool"] for b in plan["beats"] if b["move"] == "cut"}
    for a in plan["actors"]:
        o = kit.load_model(models[a["id"]], a["id"])
        kit.fit(o, a["size_m"], a.get("facing", "camera"))
        st.objs[a["id"]] = o
        st.support[a["id"]] = a.get("on") or "ground"
    bpy.context.view_layer.update()
    # supports and free actors on the ground in a row around the origin, then everything standing on something
    on_ground = [a["id"] for a in plan["actors"] if a.get("on") in (None, "ground") and a["id"] not in tools]
    x = 0.0
    for k, aid in enumerate(on_ground):
        o = st.objs[aid]
        lo, hi = kit.bbox(o)
        width = hi.x - lo.x
        if k:
            x += width / 2
        o.location = (x if k % 2 == 0 else -x, 0, 0)
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
    view = Vector((math.sin(yaw) * math.cos(pitch), -math.cos(yaw) * math.cos(pitch), math.sin(pitch)))
    sc.frame_set(1)
    # framed on the subject (a 30 cm knife beside a 9 cm onion made the onion 10% of the frame); the start aim leans
    # toward the threat so it shows too, which the first-frame check confirms
    first = st.intact.get(subject_id, st.objs[subject_id])
    lo, hi = kit.bbox(first)
    size = hi - lo
    vfov = 2 * math.atan(18 / LENS)
    hfov = 2 * math.atan(18 * sc.render.resolution_x / sc.render.resolution_y / LENS)
    dist = max(size.z / SUBJECT_FILL / (2 * math.tan(vfov / 2)),
               max(size.x, size.y) / FILL / (2 * math.tan(hfov / 2))) + max(size.x, size.y) / 2
    aim = bpy.data.objects.new("aim", None)
    sc.collection.objects.link(aim)
    start = (lo + hi) / 2
    if st.threat is not None and st.threat is not first:
        tlo, thi = kit.bbox(st.threat)
        start = start.lerp((tlo + thi) / 2, 0.3)
    follow = plan["camera"].get("follow")
    moved = st.moved_from.get(follow, sc.frame_end + 1) if follow else sc.frame_end + 1
    for f in range(1, sc.frame_end + 1, 2):
        target = start
        if follow and f >= moved:
            sc.frame_set(f)
            o = st.objs[follow]
            blo, bhi = kit.bbox(o)
            target = start.lerp((blo + bhi) / 2, min(1.0, (f - moved) / 6))
        kit.key_loc(aim, f, target)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.data.lens = LENS
    cam.data.dof.use_dof, cam.data.dof.aperture_fstop, cam.data.dof.focus_object = True, FSTOP, aim
    for f in range(1, sc.frame_end + 1, 2):
        sc.frame_set(f)
        k = 1 - (1 - PUSH_IN) * (f - 1) / max(sc.frame_end - 1, 1)
        kit.key_loc(cam, f, aim.matrix_world.translation + view * dist * k)
    con = cam.constraints.new("TRACK_TO")
    con.target, con.track_axis, con.up_axis = aim, "TRACK_NEGATIVE_Z", "UP_Y"
    return cam


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
    held = hold_offscreen(st, cam)
    failures = checks(plan, st, cam, subject_id)
    sc.frame_set(sc.frame_end)
    lowest = {aid: round(min(v.z for v in kit.world_verts(o)), 4) for aid, o in st.objs.items()
              if aid not in tools}
    report = {"ok": not failures, "failures": failures, "frames": sc.frame_end,
              "pieces": sum(len(p) for p, *_ in st.cuts),
              "cut_shares": {k: v for *_, s in st.cuts for k, v in s.items()}, "lowest": lowest,
              "held_offscreen": held}
    if job.get("render", True) and (report["ok"] or job.get("render_failed")):
        frames_dir = Path(job["frames_dir"])
        frames_dir.mkdir(parents=True, exist_ok=True)
        sc.render.image_settings.file_format = "PNG"
        sc.render.filepath = str(frames_dir / "f_")
        bpy.ops.render.render(animation=True)
    Path(job["report"]).write_text(json.dumps(report, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1])
