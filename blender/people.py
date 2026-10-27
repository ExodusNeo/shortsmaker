"""People in openers (part 2, 2026-10-27): Quaternius rigged people dressed by era and role (opener_tables.json
"roles") and moved by their own animation clips ("people_moves"). The library is people.blend + people.json, packed
by pack_people.py (or tests/people_standin.py). A person is one mesh object, origin at the feet, with its armature
parented under it, so Part 1's placing, camera, moves and checks treat it like any actor."""

import json
import math
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

import scene_kit as kit

HAT_WIDTH = 0.18  # a hat is this wide on a 1.8 m person
PROP_SHARE = 0.5  # a prop is this share of the person's height unless the plan says prop_size_m


def load_library(job: dict) -> dict:
    """The people.json of the job's library plus "blend"; every clip is appended once as an action."""
    lib = json.loads(Path(job["people"]["json"]).read_text(encoding="utf-8"))
    lib["blend"] = job["people"]["blend"]
    with bpy.data.libraries.load(lib["blend"]) as (src, dst):
        dst.actions = [a for a in src.actions if a in lib["clips"]]
    return lib


def base_name(material_name: str) -> str:
    stem, _, tail = material_name.rpartition(".")
    return stem if stem and tail.isdigit() else material_name


def _append(lib: dict, body: dict) -> tuple:
    with bpy.data.libraries.load(lib["blend"]) as (src, dst):
        dst.objects = [body["object"], body["armature"]]
    mesh, arm = dst.objects
    for o in (mesh, arm):
        bpy.context.scene.collection.objects.link(o)
    return mesh, arm


def _colour(mesh, colours: dict) -> None:
    """Each role colour on a copy of the material it names (two people never share one); names the body lacks are
    skipped."""
    for slot in mesh.material_slots:
        if slot.material is None:
            continue
        rgb = colours.get(base_name(slot.material.name))
        if rgb is None:
            continue
        m = slot.material.copy()
        bsdf = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None) if m.node_tree else None
        if bsdf is not None:
            for link in list(bsdf.inputs["Base Color"].links):
                m.node_tree.links.remove(link)
            bsdf.inputs["Base Color"].default_value = (*rgb, 1)
        m.diffuse_color = (*rgb, 1)
        slot.material = m


def _attach(item, arm, bone: str, at: Vector) -> None:
    """item (origin at its bottom) stands on `at` and follows the bone from now on."""
    item.location = at
    bpy.context.view_layer.update()
    keep = item.matrix_world.copy()
    item.parent, item.parent_type, item.parent_bone = arm, "BONE", bone
    bpy.context.view_layer.update()
    item.matrix_world = keep


def dress(actor: dict, role: dict, lib: dict, models: dict) -> bpy.types.Object:
    """The person as one mesh (origin at the feet, facing as planned, the role's height and colours), its armature
    under it, hat on the head bone and prop in the right hand. Returns the mesh."""
    body = lib["bodies"][role["body"]]
    mesh, arm = _append(lib, body)
    vl = bpy.context.view_layer
    # bake the import's rotation and scale, the facing and the height into mesh and bones, both left at identity
    s = role["height_m"] / body["height"]
    turn = {"right": 90, "left": -90, "camera": 0, "away": 180}[actor.get("facing", "camera")]
    fx, fy = body.get("front", [0.0, -1.0])
    to_front = -math.pi / 2 - math.atan2(fy, fx)  # the body's own front turned to -Y, as every model faces
    keep = arm.matrix_world.copy()
    arm.matrix_world = Matrix.Rotation(math.radians(turn) + kit.VIEW_YAW + to_front, 4, "Z") @ Matrix.Scale(s, 4) @ keep
    for o in bpy.context.selected_objects:
        o.select_set(False)
    for o in (arm, mesh):
        o.select_set(True)
    vl.objects.active = arm
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    vl.update()
    # the mesh becomes the root: origin at the bottom centre of its rest pose, the armature its child
    world = [mesh.matrix_world @ v.co for v in mesh.data.vertices]
    lo = Vector((min(p.x for p in world), min(p.y for p in world), min(p.z for p in world)))
    hi = Vector((max(p.x for p in world), max(p.y for p in world)))
    base = Vector(((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, lo.z))
    mesh_world, arm_world = mesh.matrix_world.copy(), arm.matrix_world.copy()
    mesh.parent = None
    mesh.matrix_world = mesh_world
    mesh.data.transform(Matrix.Translation(-base) @ mesh.matrix_world)
    mesh.matrix_world = Matrix.Identity(4)
    arm.parent = mesh
    arm.matrix_parent_inverse = Matrix.Identity(4)
    arm.matrix_world = Matrix.Translation(-base) @ arm_world
    mod = next((m for m in mesh.modifiers if m.type == "ARMATURE"), None) or mesh.modifiers.new("rig", "ARMATURE")
    mod.object = arm
    mesh.name, arm.name = actor["id"], f"{actor['id']}.rig"
    _colour(mesh, role.get("colours", {}))
    vl.update()
    pose = {b: (arm.matrix_world @ arm.pose.bones[n].head, arm.matrix_world @ arm.pose.bones[n].tail)
            for b, n in lib["bones"].items() if n in arm.pose.bones}
    if models.get(f"{actor['id']}:hat") and "head" in pose:
        hat = kit.load_model(models[f"{actor['id']}:hat"], f"{actor['id']}.hat")
        kit.fit(hat, HAT_WIDTH * role["height_m"] / 1.8, "camera", view=False)
        _attach(hat, arm, lib["bones"]["head"], pose["head"][1])
        mesh["hat"] = hat.name
    if models.get(f"{actor['id']}:prop") and "hand_r" in pose:
        prop = kit.load_model(models[f"{actor['id']}:prop"], f"{actor['id']}.prop")
        kit.fit(prop, actor.get("prop_size_m") or PROP_SHARE * role["height_m"], "camera", view=False)
        _attach(prop, arm, lib["bones"]["hand_r"], pose["hand_r"][1])
        mesh["prop"] = prop.name
    mesh["facing"], mesh["person"], mesh["rig"] = actor.get("facing", "camera"), actor["person"], arm.name
    return mesh


def _strip(arm, clip: str, start: int, repeat: float = 1.0):
    """The clip on its own NLA track from `start`, held after it ends, blended in over 4 frames."""
    track = arm.animation_data.nla_tracks.new()
    strip = track.strips.new(clip, start, bpy.data.actions[clip])
    strip.repeat = max(repeat, 0.05)
    strip.extrapolation = "HOLD_FORWARD"
    strip.blend_in = min(4.0, (strip.frame_end - strip.frame_start) / 2)
    return strip


def idle(o, lib: dict) -> None:
    """Every person breathes on their Idle clip from frame 1 under whatever they do (a rest pose looked frozen)."""
    arm = bpy.data.objects[o["rig"]]
    arm.animation_data_create()
    if "Idle" in bpy.data.actions:
        frames = bpy.context.scene.frame_end
        track = arm.animation_data.nla_tracks.new()
        strip = track.strips.new("Idle", 1, bpy.data.actions["Idle"])
        strip.repeat = frames / max(lib["clips"]["Idle"]["frames"], 1) + 1
        strip.extrapolation = "HOLD"


def _ground(o, st, start: int, end: int) -> None:
    """At the end of a clip the person's lowest point rests on what they stand on: a fall or a sit authored at another
    height still lands on the floor or the crate."""
    sc = bpy.context.scene
    sc.frame_set(min(end, sc.frame_end))
    under = 0.0 if st.support.get(o.name, "ground") == "ground" else kit.bbox(st.support_obj(o.name))[1].z
    gap = min(v.z for v in kit.world_verts(o)) - under
    if abs(gap) > 0.005:
        z0 = kit.loc_at(o, start).z
        kit.key_loc(o, start, kit.loc_at(o, start))
        end_loc = kit.loc_at(o, end)
        end_loc.z = z0 - gap
        kit.key_loc(o, min(end, sc.frame_end), end_loc)
    sc.frame_set(1)


def move(beat: dict, st, lib: dict) -> None:
    """A people move: an in-place clip from the beat's time, or a travel clip played while the person crosses the
    ground at the clip's own pace (feet don't slide), turning to the way they go and stopping short of obstacles."""
    import moves
    actor = beat["actor"]
    o = st.objs[actor]
    arm = bpy.data.objects[o["rig"]]
    spec = kit.TABLES["people_moves"][beat["move"]]
    clip, info = spec["clip"], lib["clips"][spec["clip"]]
    sc = bpy.context.scene
    f0 = st.f(beat["at"])
    st.moved_from.setdefault(actor, f0)
    if spec["kind"] == "in_place":
        strip = _strip(arm, clip, f0)
        _ground(o, st, f0, int(strip.frame_end))
        return
    if st.support.get(actor, "ground") != "ground":
        st.failures.append(f"walk: {actor} would {beat['move']} off the {st.support[actor]} it stands on; start "
                           f"{actor} on the ground")
    d = moves.toward(beat)
    role = kit.TABLES["roles"][o["person"]]
    seconds_per_loop = info["frames"] / st.fps
    speed = info["stride_m"] * role["height_m"] / lib["rig_height"] / seconds_per_loop
    start = kit.loc_at(o, f0)
    face = kit.facing_vec(o)
    turn = math.atan2(face.x * d.y - face.y * d.x, face.dot(d))
    base_rot = kit.rot_at(o, f0)
    tools = {b["tool"] for b in st.plan["beats"] if b["move"] == "cut"}
    obstacles = [x for k, x in st.objs.items() if x is not o and k not in tools] + \
        [x for x in sc.objects if x.name.startswith("backdrop")]
    keep_loc, keep_rot = o.location.copy(), o.rotation_euler.copy()
    o.location, o.rotation_euler = start + Vector((0, 0, 0.01)), (0, 0, base_rot.z + turn)
    bpy.context.view_layer.update()
    want = speed * (sc.frame_end - f0) / st.fps
    room = max(0.0, moves.clear_distance(o, d, obstacles, want) - 0.04)
    o.location, o.rotation_euler = keep_loc, keep_rot
    bpy.context.view_layer.update()
    stop = min(sc.frame_end, f0 + round(room / speed * st.fps)) if speed > 0 else f0
    _strip(arm, clip, f0, repeat=(stop - f0) / info["frames"])
    kit.key_rot(o, f0, base_rot)
    kit.key_rot(o, min(f0 + 8, sc.frame_end), (base_rot.x, base_rot.y, base_rot.z + turn))
    # along the ground at the clip's pace, the lowest foot pinned to it every other frame: a step caught mid-air
    # on the last frame floated (and a clip's own bob stays)
    for f in list(range(f0, stop, 2)) + [stop]:
        u = (f - f0) / max(stop - f0, 1)
        kit.key_loc(o, f, start + d * room * u)
        sc.frame_set(f)
        gap = min(v.z for v in kit.world_verts(o)) - start.z
        kit.key_loc(o, f, start + d * room * u - Vector((0, 0, gap)))
    sc.frame_set(1)
