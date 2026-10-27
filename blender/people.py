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
        names = list(dst.actions)
    # kept by object, not looked up by name: a backdrop's own "Idle" action took the name (final review); the
    # appended actions come back in the order asked for, whatever Blender renamed them to
    lib["actions"] = dict(zip(names, dst.actions))
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
    """item (origin at its bottom) stands on `at` and follows the bone's place and turn, not its scale: the clips
    scale the hand bones, and a prop parented to one shrank to a third of its size."""
    item.location = at
    bpy.context.view_layer.update()
    pb = arm.pose.bones[bone]
    loc, rot, _ = (arm.matrix_world @ pb.matrix).decompose()
    con = item.constraints.new("CHILD_OF")
    con.name, con.target, con.subtarget = "held", arm, bone
    con.use_scale_x = con.use_scale_y = con.use_scale_z = False
    con.inverse_matrix = Matrix.LocRotScale(loc, rot, Vector((1, 1, 1))).inverted()


def _is_blade(find: str) -> bool:
    return any(f" {k} " in f" {find.lower()} " for k in kit.TABLES["tools"])


GRIP_ZONE = 0.08  # the part of a prop this close to its grip is in the hand and may touch it


def _through(prop, body_tree, grip: Vector) -> bool:
    """Does the prop, apart from the bit in the hand, go through its owner?"""
    from mathutils.bvhtree import BVHTree
    pts = [prop.matrix_world @ v.co for v in prop.data.vertices]
    faces = [p.vertices[:] for p in prop.data.polygons if all((pts[i] - grip).length > GRIP_ZONE for i in p.vertices)]
    return bool(faces) and bool(BVHTree.FromPolygons(pts, faces).overlap(body_tree))


def _hold(prop, body, hand: Vector, blade: bool, turn: float = 0.0) -> bool:
    """The prop held by its handle end in the hand: a blade raised up and forward, anything else (a cane, a closed
    umbrella) pointing down and forward, turned `turn` about its length; tilted out from the body (the handle kept
    in the hand) until it clears its owner, slid out only if tilting isn't enough (the first people run stood an
    umbrella on the hand, its canopy through the officer's waist). True when it clears."""
    import moves
    out = hand - Vector((body.location.x, body.location.y, hand.z))
    out.z = 0
    out = out.normalized() if out.length > 1e-4 else Vector((0, 0, 0))
    body_tree = kit.tree(body)
    dims = sorted(prop.dimensions)
    if dims[2] < 1.8 * dims[1]:  # not a long thing (a box, a bag): carried, centred on the hand, out from the body
        mid = sum((v.co for v in prop.data.vertices), Vector()) / len(prop.data.vertices)
        prop["grip"] = mid[:]
        for k in range(16):
            prop.rotation_euler, prop.location = (0, 0, 0), hand + out * (0.02 * k) - mid
            bpy.context.view_layer.update()
            if not _through(prop, body_tree, hand + out * (0.02 * k)):
                return True
        return False
    _, _, long = moves.tool_axes(prop)
    forward = kit.facing_vec(body)
    aim = (Vector((0, 0, 1)) + 0.35 * forward if blade else Vector((0, 0, -1)) + 0.35 * forward).normalized()
    grip = moves.handle_end_local(prop)
    prop["grip"] = grip[:]
    # forward lean up to near level: a 0.9 m closed umbrella held down from a 0.75 m hand hit the ground
    tilts = sorted(((0.15 * a, 0.25 * b) for a in range(9) for b in range(17)), key=lambda t: t[0] + t[1])
    for (tilt, lean), slide in [(t, 0.0) for t in tilts] + [((1.2, 1.0), 0.02 * k) for k in range(1, 11)]:
        r = long.rotation_difference((aim + out * tilt + forward * lean).normalized()).to_matrix()             @ Matrix.Rotation(turn, 3, long)
        prop.rotation_euler = r.to_euler()
        prop.location = hand + out * slide - r @ grip
        bpy.context.view_layer.update()
        above = min((prop.matrix_world @ v.co).z for v in prop.data.vertices) >= body.location.z + 0.01
        if above and not _through(prop, body_tree, hand + out * slide):  # clear of the owner and the ground
            return True
    return False


def held(body, lib: dict) -> dict:
    """How a person holds their prop at frame 1, for the report: the handle's gap to the hand, whether the prop cuts
    through its owner, which way it points."""
    import moves
    prop = bpy.data.objects[body["prop"]]
    arm = bpy.data.objects[body["rig"]]
    bpy.context.scene.frame_set(1)
    hand = arm.matrix_world @ arm.pose.bones[lib["bones"]["hand_r"]].head
    grip = prop.matrix_world @ Vector(prop["grip"])
    tip = max((prop.matrix_world @ v.co for v in prop.data.vertices), key=lambda p: (p - grip).length)
    return {"hand_gap": round((grip - hand).length, 4), "through_body": _through(prop, kit.tree(body), grip),
            "lowest": round(min((prop.matrix_world @ v.co).z for v in prop.data.vertices) - body.location.z, 4),
            "points": "up" if tip.z > grip.z else "down"}


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
        top = max((mesh.matrix_world @ v.co).z for v in mesh.data.vertices)  # on top of the head, wherever the bone
        _attach(hat, arm, lib["bones"]["head"], Vector((pose["head"][0].x, pose["head"][0].y, top - 0.02)))
        mesh["hat"] = hat.name
    if models.get(f"{actor['id']}:prop") and "hand_r" in pose:
        prop = kit.load_model(models[f"{actor['id']}:prop"], f"{actor['id']}.prop")
        kit.fit(prop, actor.get("prop_size_m") or PROP_SHARE * role["height_m"], "camera", view=False)
        # the hand is the fist bone's head: the importer guesses bone tails, and the Fist tail sat at knee height
        _hold(prop, mesh, pose["hand_r"][0], _is_blade(actor.get("prop", "")))
        prop["hand"] = pose["hand_r"][0][:]  # where the hand is at rest: a swing holds the blade again from here
        _attach(prop, arm, lib["bones"]["hand_r"], prop.location.copy())
        mesh["prop"] = prop.name
    mesh["facing"], mesh["person"], mesh["rig"] = actor.get("facing", "camera"), actor["person"], arm.name
    return mesh


def _strip(arm, lib: dict, clip: str, start: int, repeat: float = 1.0):
    """The clip on its own NLA track from `start`, held after it ends, blended in over 4 frames."""
    track = arm.animation_data.nla_tracks.new()
    strip = track.strips.new(clip, start, lib["actions"][clip])
    strip.repeat = max(repeat, 0.05)
    strip.extrapolation = "HOLD_FORWARD"
    strip.blend_in = min(4.0, (strip.frame_end - strip.frame_start) / 2)
    return strip


def idle(o, lib: dict) -> None:
    """Every person breathes on their Idle clip from frame 1 under whatever they do (a rest pose looked frozen)."""
    arm = bpy.data.objects[o["rig"]]
    arm.animation_data_create()
    if "Idle" in lib["actions"]:
        frames = bpy.context.scene.frame_end
        track = arm.animation_data.nla_tracks.new()
        strip = track.strips.new("Idle", 1, lib["actions"]["Idle"])
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
        strip = _strip(arm, lib, clip, f0)
        _ground(o, st, f0, int(strip.frame_end))
        if beat["move"] in ("swing_prop", "throw_prop", "drop_prop"):
            prop_move(beat, st, o, strip)
        return
    if st.support.get(actor, "ground") != "ground":
        st.failures.append(f"walk: {actor} would {beat['move']} off the {st.support[actor]} it stands on; start "
                           f"{actor} on the ground")
    d = moves.toward(beat, st=st)
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
    reach = 0.0  # how far a held prop sticks out ahead of the body: an umbrella poked into the car
    prop = bpy.data.objects.get(o.get("prop") or "")
    if prop is not None:
        ahead = lambda pts: max(p.dot(d) for p in pts)  # noqa: E731
        reach = max(0.0, ahead(kit.world_verts(prop)) - ahead(kit.world_verts(o)))
    stride = info["stride_m"] * role["height_m"] / lib["rig_height"]
    reach += 0.3 * stride  # a step swings the leading foot and arm this far ahead of the standing pose
    room = max(0.0, moves.clear_distance_at_end(o, d, obstacles, want, sc.frame_end) * moves.share_of_gap(st, beat)
               - 0.04 - reach)
    o.location, o.rotation_euler = keep_loc, keep_rot
    bpy.context.view_layer.update()
    stop = min(sc.frame_end, f0 + round(room / speed * st.fps)) if speed > 0 else f0
    _strip(arm, lib, clip, f0, repeat=(stop - f0) / info["frames"])
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


def _bake_free(item, last: int) -> None:
    """Keys item's world transform over frames 1..last (it rode the hand bone), then frees it from the bone, so
    physics can take it from there: a rigid body still parented to an animated bone doesn't fall cleanly."""
    sc = bpy.context.scene
    path = []
    for f in range(1, last + 1):
        sc.frame_set(f)
        path.append(item.matrix_world.copy())
    for con in [c for c in item.constraints if c.name == "held"]:
        item.constraints.remove(con)
    for f, m in enumerate(path, 1):
        loc, rot, _ = m.decompose()
        item.location, item.rotation_euler = loc, rot.to_euler()
        item.keyframe_insert("location", frame=f)
        item.keyframe_insert("rotation_euler", frame=f)
    sc.frame_set(1)


def _show_blade(prop, st, frame: int, body) -> None:
    """Hold the blade turned about its length so the camera sees its flat side at the height of the swing: each
    turn is held again (tilted clear of the owner), and the clear one showing the most face is kept."""
    import moves
    sc = bpy.context.scene
    _, thin, _ = moves.tool_axes(prop)
    hand = Vector(prop["hand"])
    best = None
    for k in range(12):
        t = math.radians(15 * k)
        if not _hold(prop, body, hand, True, turn=t):
            continue
        sc.frame_set(frame)
        face = abs((prop.matrix_world.to_3x3() @ thin).normalized().dot(st.cam_h))
        sc.frame_set(1)
        if best is None or face > best[0]:
            best = (face, t)
    _hold(prop, body, hand, True, turn=best[1] if best else 0.0)
    sc.frame_set(1)


def prop_move(beat: dict, st, o, strip) -> None:
    """What the prop does in a prop move: a swung blade turns to show its face and is judged by the blade check;
    a thrown or dropped prop leaves the hand to physics."""
    import moves
    prop = bpy.data.objects.get(o.get("prop") or "")
    if prop is None:
        st.failures.append(f"{beat['move']}: {beat['actor']} has no prop to {beat['move'].split('_')[0]}")
        return
    actor = next(a for a in st.plan["actors"] if a["id"] == beat["actor"])
    start, end = int(strip.frame_start), int(strip.frame_end)
    if beat["move"] == "swing_prop":
        mid = (start + end) // 2
        if any(f" {k} " in f" {actor.get('prop', '').lower()} " for k in kit.TABLES["tools"]):
            _show_blade(prop, st, mid, o)
            st.swings.append((prop, mid))
        return
    let_go = start + round(0.45 * (end - start)) if beat["move"] == "throw_prop" else start
    _bake_free(prop, let_go)
    launch = kit.facing_vec(o) * 3.0 + Vector((0, 0, 2.0)) if beat["move"] == "throw_prop" else None
    moves.release(st, prop, let_go + 1, launch=launch)
    # it starts inside its owner's hand: collide with everything still but the person who held it (a box let go
    # stayed stuck on the officer)
    kit.layers(prop, [2])
    for other in bpy.context.scene.objects:
        if other is not o and other.rigid_body is not None and other.rigid_body.type == "PASSIVE":
            other.rigid_body.collision_collections[2] = True
    st.resting.append((prop, st.ground))
