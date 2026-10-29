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


def _body_tree(body) -> "BVHTree":
    """The owner's body without the hand that holds the prop: a cartoon fist wraps more than GRIP_ZONE of an umbrella,
    and with every hold 'through' it the umbrella slid 0.2 m off the hand (owner 2026-10-27)."""
    from mathutils.bvhtree import BVHTree
    g = body.vertex_groups.get(body.get("hand_bone", ""))
    if g is None:
        return kit.tree(body)
    fist = {v.index for v in body.data.vertices if any(x.group == g.index and x.weight > 0.5 for x in v.groups)}
    ev = body.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    t = BVHTree.FromPolygons([ev.matrix_world @ v.co for v in me.vertices],
                             [p.vertices[:] for p in me.polygons if not fist.intersection(p.vertices)])
    ev.to_mesh_clear()
    return t


def _handle_first(prop, long: Vector) -> Vector:
    """`long` turned to run from a cane's or umbrella's handle to its tip: the handle is the wider of its two ends (a
    crook, a knob), the tip a point. The blade rule (hold the end away from the wide half) put the umbrella officer's
    hand on the ferrule, the canopy being the wide half (owner 2026-10-27)."""
    vs = [v.co for v in prop.data.vertices]
    along = [v.dot(long) for v in vs]
    lo, hi = min(along), max(along)

    def width(end: float) -> float:
        pts = [v - long * t for v, t in zip(vs, along) if abs(t - end) <= 0.1 * (hi - lo)]
        return max(((p - q).length for p in pts for q in pts), default=0.0)
    return long if width(lo) >= width(hi) else -long


def _hold(prop, body, hand: Vector, blade: bool, turn: float = 0.0) -> bool:
    """The prop held by its handle end in the hand: a blade raised up and forward, anything else (a cane, a closed
    umbrella) pointing down and forward, turned `turn` about its length; tilted out from the body (the handle kept
    in the hand) until it clears its owner, slid out only if tilting isn't enough (the first people run stood an
    umbrella on the hand, its canopy through the officer's waist). True when it clears."""
    import moves
    out = hand - Vector((body.location.x, body.location.y, hand.z))
    out.z = 0
    out = out.normalized() if out.length > 1e-4 else Vector((0, 0, 0))
    body_tree = _body_tree(body)
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
    if not blade:
        long = _handle_first(prop, long)
    forward = kit.facing_vec(body)
    aim = (Vector((0, 0, 1)) + 0.35 * forward if blade else Vector((0, 0, -1)) + 0.35 * forward).normalized()
    grip = min((v.co for v in prop.data.vertices), key=lambda v: v.dot(long)).copy()
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
    return {"hand_gap": round((grip - hand).length, 4), "through_body": _through(prop, _body_tree(body), grip),
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
    arm["size"] = s  # the clips' location keys are scaled by this too (_clip)
    # the legs follow the feet: the clips key the Foot bones and leave the legs to an IK the export dropped, so a
    # walking officer's feet stretched into spikes off rigid shins (owner 2026-10-27)
    for side in "LR":
        shin, foot, pole = (arm.pose.bones.get(f"{n}.{side}") for n in ("LowerLeg", "Foot", "PoleTarget"))
        if shin and foot and not any(c.type == "IK" for c in shin.constraints):
            ik = shin.constraints.new("IK")
            ik.target, ik.subtarget, ik.chain_count = arm, foot.name, 2
            if pole:
                ik.pole_target, ik.pole_subtarget = arm, pole.name
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
        size = actor.get("prop_size_m") or PROP_SHARE * role["height_m"]
        kit.fit(prop, size, "camera", view=False)
        blade = _is_blade(actor.get("prop", ""))
        mesh["hand_bone"] = lib["bones"]["hand_r"]
        # the hand is the fist bone's head: the importer guesses bone tails, and the Fist tail sat at knee height.
        # The biggest prop the hand holds clear of its owner and the ground: the planned 0.9 m umbrella from a 0.5 m
        # hand floated 0.2 m off it, and a cap at the hand's height left it too small (owner 2026-10-27)
        for k in range(8):
            if _hold(prop, mesh, pose["hand_r"][0], blade) or k == 7:
                break
            kit.fit(prop, size * 0.9 ** (k + 1), "camera", view=False)
        prop["hand"] = pose["hand_r"][0][:]  # where the hand is at rest: a swing holds the blade again from here
        _attach(prop, arm, lib["bones"]["hand_r"], prop.location.copy())
        mesh["prop"] = prop.name
    mesh["facing"], mesh["person"], mesh["rig"] = actor.get("facing", "camera"), actor["person"], arm.name
    return mesh


def _clip(lib: dict, clip: str, arm):
    """The clip at this person's size: its location keys (the feet the leg IK follows, the hips' bob) are in the
    library rig's units, and on a rig scaled to 1.8 m every step reached 1.8x too far, the legs locked straight in
    a split and the feet slid (owner 2026-10-27). One copy per clip and size."""
    s = arm.get("size", 1.0)
    key = (clip, round(s, 4))
    scaled = lib.setdefault("scaled", {})
    if key not in scaled:
        act = lib["actions"][clip].copy()
        for fc in kit.fcurves_of(act):
            if fc.data_path.endswith(".location"):
                for k in fc.keyframe_points:
                    k.co[1] *= s
                    k.handle_left[1] *= s
                    k.handle_right[1] *= s
                fc.update()
        scaled[key] = act
    return scaled[key]


def _strip(arm, lib: dict, clip: str, start: int, repeat: float = 1.0):
    """The clip on its own NLA track from `start`, held after it ends, blended in over 4 frames."""
    track = arm.animation_data.nla_tracks.new()
    strip = track.strips.new(clip, start, _clip(lib, clip, arm))
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
        strip = track.strips.new("Idle", 1, _clip(lib, "Idle", arm))
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
    clip = kit.TABLES["people_moves"][beat["move"]]["clip"]
    f0 = max(st.f(beat["at"]), st.busy.get(actor, 1))  # after its pick_up has it in hand and stands up again
    if f0 > st.f(beat["at"]) and f0 >= bpy.context.scene.frame_end - 3:  # the Eiffel plan's escape never showed
        st.failures.append(f"{beat['move']}: {actor} is still picking up until {f0 / st.fps:.1f} s, the end of the "
                           f"scene, so the {beat['move']} never shows; start {actor} next to what it picks up, or "
                           f"pick up earlier")
    st.moved_from.setdefault(actor, f0)
    if beat["move"] == "pick_up":
        pick_up(beat, st, lib, o, arm, f0)
        return
    if beat["move"] == "drink":
        drink(beat, st, lib, o, arm, f0)
        return
    if kit.TABLES["people_moves"][beat["move"]]["kind"] == "in_place":
        strip = _strip(arm, lib, clip, f0)
        _ground(o, st, f0, int(strip.frame_end))
        if beat["move"] in ("swing_prop", "throw_prop", "drop_prop"):
            prop_move(beat, st, o, strip)
        return
    _travel(beat, st, lib, o, arm, clip, f0, moves.toward(beat, st=st))


def facing_now(o, f: int) -> Vector:
    """The way o faces on frame f: its planned facing turned by every turn keyed since frame 1. A run after a pick_up
    turned from the planned facing and set off at the wrong angle."""
    return Matrix.Rotation(kit.rot_at(o, f).z - kit.rot_at(o, 1).z, 3, "Z") @ kit.facing_vec(o)


def _travel(beat: dict, st, lib: dict, o, arm, clip: str, f0: int, d: Vector, want: float | None = None,
            ignore=None) -> int:
    """o walks or runs along d from f0 on `clip` at the clip's own pace, `want` metres (default: to the end of the
    scene), stopping short of obstacles (not `ignore`, what it walks over to pick up). Returns its stop frame."""
    import moves
    actor = beat["actor"]
    info = lib["clips"][clip]
    sc = bpy.context.scene
    if st.support.get(actor, "ground") != "ground":
        st.failures.append(f"walk: {actor} would {beat['move']} off the {st.support[actor]} it stands on; start "
                           f"{actor} on the ground")
    role = kit.TABLES["roles"][o["person"]]
    seconds_per_loop = info["frames"] / st.fps
    speed = info["stride_m"] * role["height_m"] / lib["rig_height"] / seconds_per_loop
    start = kit.loc_at(o, f0)
    base_rot = kit.rot_at(o, f0)
    face = facing_now(o, f0)
    turn = math.atan2(face.x * d.y - face.y * d.x, face.dot(d))
    tools = {b["tool"] for b in st.plan["beats"] if b["move"] == "cut"}
    obstacles = [x for k, x in st.objs.items() if x is not o and x is not ignore and k not in tools] + \
        [x for x in sc.objects if x.name.startswith("backdrop")]
    keep_loc, keep_rot = o.location.copy(), o.rotation_euler.copy()
    o.location, o.rotation_euler = start + Vector((0, 0, 0.01)), (0, 0, base_rot.z + turn)
    bpy.context.view_layer.update()
    want = speed * (sc.frame_end - f0) / st.fps if want is None else want
    reach = 0.0  # how far a held prop sticks out ahead of the body: an umbrella poked into the car
    prop = bpy.data.objects.get(o.get("prop") or "")
    if prop is not None:
        ahead = lambda pts: max(p.dot(d) for p in pts)  # noqa: E731
        reach = max(0.0, ahead(kit.world_verts(prop)) - ahead(kit.world_verts(o)))
    stride = info["stride_m"] * role["height_m"] / lib["rig_height"]
    reach += 0.3 * stride  # a step swings the leading foot and arm this far ahead of the standing pose
    # looked for out to the margin past the walk, so open ground isn't cut short by it (the umbrella officer stopped
    # 0.4 s early with nothing ahead, owner 2026-10-27)
    clear = moves.clear_distance_at_end(o, d, obstacles, want + 0.04 + reach, sc.frame_end) * moves.share_of_gap(st, beat)
    room = min(want, max(0.0, clear - 0.04 - reach))
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
    return stop


DROP_OUT = 1.2  # m/s out from the body: a dropped prop lands about 0.35 m from the leg
DROP_TOWARD = 2.0  # m/s toward the taker: lands about 0.6 m out, clear of the dropper's arms
GRAB_GAP = 0.1  # the hand ends at most this far from the thing it picks up


def _step_to(f: int) -> None:
    """Every frame up to f in order, so physics (a dropped case still landing) is where it really is on frame f."""
    sc = bpy.context.scene
    for k in range(sc.frame_start, f + 1):
        sc.frame_set(k)


def _footprints(others: list, f0: int) -> list[tuple]:
    """Everyone else's xy box over the rest of the scene: the dealer's cheer, keyed later, swung his arms into the
    con artist's bend (live run 2, try 2)."""
    sc = bpy.context.scene
    boxes = []
    for x in others:
        lo, hi = Vector((9e9, 9e9, 0)), Vector((-9e9, -9e9, 0))
        # only people move under their clips; a 30 m backdrop measured every 3 frames took over 10 minutes
        for f in range(f0, sc.frame_end + 1, 3) if x.get("rig") else [f0]:
            sc.frame_set(f)
            a, b = kit.bbox(x)
            lo.x, lo.y, hi.x, hi.y = min(lo.x, a.x), min(lo.y, a.y), max(hi.x, b.x), max(hi.y, b.y)
        boxes.append((lo, hi))
    return boxes


def _clearance(a: Vector, b: Vector, boxes: list, upto: float = 0.6) -> float:
    """How far the stretch from a toward b (the bend: feet to 60 % of the way over to the hand, the head and back but
    not the hand at the item; a walk: all of it) keeps from everyone else's footprint."""
    out = 9.0
    for lo, hi in boxes:
        for k in range(9):
            p = a.lerp(b, upto * k / 8)
            dx, dy = max(lo.x - p.x, 0.0, p.x - hi.x), max(lo.y - p.y, 0.0, p.y - hi.y)
            out = min(out, math.hypot(dx, dy))
    return out


PATH_ROOM = 0.25  # a walk keeps its middle this far from everyone (about half a body's width)


def _detour(a: Vector, b: Vector, boxes: list) -> Vector | None:
    """A point beside whoever blocks the straight walk from a to b, both legs clear, the shorter way round; None if
    neither side is clear."""
    d = (b - a).normalized()
    side = Vector((-d.y, d.x, 0))
    best = None
    for lo, hi in boxes:
        c = Vector(((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, a.z))
        if _clearance(a, b, [(lo, hi)], 1.0) >= PATH_ROOM:
            continue
        r0 = math.hypot(hi.x - lo.x, hi.y - lo.y) / 2 + PATH_ROOM
        # further out until both legs clear its corners (the nearest point clipped the cheering dealer by 0.1 m)
        for r, sgn in [(r0 + 0.2 * k, sgn) for k in range(6) for sgn in (1, -1)]:
            via = c + side * sgn * r
            if _clearance(a, via, boxes, 1.0) >= PATH_ROOM and _clearance(via, b, boxes, 1.0) >= PATH_ROOM:
                length = (via - a).length + (b - via).length
                if best is None or length < best[0]:
                    best = (length, via)
    return best[1] if best else None


REST_FRAMES = 20  # a dropped item has landed and settled this long after it's let go
BEND_ROOM = 0.35
BEND_BACK = 0.3  # how far behind the feet the hips go in a bend  # the bend keeps this far from other people and things (the con artist's head hit the dealer's)
TURN_FRAMES = 6  # a turn on the spot into the reach, after the walk


def pick_up(beat: dict, st, lib: dict, o, arm, f0: int) -> None:
    """pick_up "take" (owner, 2026-10-28): the person walks over to the thing on the ground, turns so the PickUp
    clip's lowest hand lands on it, bends, and from that frame it rides the hand. Of 12 ways to stand, the one whose
    bend keeps clear of everyone, side-on to the camera, nearest. The first version only bent where the con artist
    stood, a metre from the briefcase, and all three tries of the Eiffel Short failed on it."""
    sc = bpy.context.scene
    take = st.objs[beat["take"]]
    item = bpy.data.objects[take["prop"]] if take.get("person") else take
    hand_bone = lib["bones"]["hand_r"]

    def hand_at() -> Vector:
        return arm.matrix_world @ arm.pose.bones[hand_bone].head

    # where the hand reaches in the body's own (scaled) frame, and when: the clip tried out once and taken off again
    probe = _strip(arm, lib, "PickUp", f0)
    lows = []
    for f in range(f0, int(probe.frame_end) + 1):
        sc.frame_set(f)
        lows.append((hand_at().z, f - f0, o.matrix_world.inverted() @ hand_at()))
    arm.animation_data.nla_tracks.remove(next(t for t in arm.animation_data.nla_tracks if probe in t.strips[:]))
    _, contact, local = min(lows, key=lambda x: x[0])
    # where it comes to rest: a bag dropped at 0.0 s was aimed at in mid-fall and missed (live run 2, try 2)
    _step_to(min(max(f0, st.released.get(item.name, 0) + REST_FRAMES), sc.frame_end))
    pts = kit.world_verts(item)
    grab = sum(pts, Vector()) / len(pts)
    grab.z = max(p.z for p in pts)  # its top: a handle, a lid
    sc.frame_set(f0)  # the walk starts from where the person is now
    body = o.matrix_world.translation.copy()
    m = o.matrix_world.to_3x3()
    yaw0 = kit.rot_at(o, f0).z
    face0 = facing_now(o, f0)
    others = [x for x in st.objs.values() if x is not o and x is not item] + \
        [x for x in sc.objects if x.name.startswith("backdrop")]
    boxes = _footprints(others, f0)
    ways = []
    for k in range(12):
        u = Matrix.Rotation(math.radians(30 * k), 3, "Z") @ Vector((1, 0, 0))
        turn = math.atan2(face0.x * u.y - face0.y * u.x, face0.dot(u))
        off = Matrix.Rotation(turn, 3, "Z") @ m @ local
        feet = Vector((grab.x - off.x, grab.y - off.y, body.z))
        to = Vector((grab.x, grab.y, body.z))
        hips = feet - (to - feet).normalized() * BEND_BACK  # a bend pushes the hips back (live run 2, try 2)
        clear = _clearance(hips, to, boxes, 0.6 * (to - hips).length / max((to - hips).length, 1e-6))
        side = abs(u.dot(st.cam_h))  # 0 = across the frame: the bend shows from the side
        ways.append((min(clear, BEND_ROOM) < BEND_ROOM, side > 0.5, (feet - body).length, turn, feet, clear))
    _, _, walked, turn, feet, clear = min(ways, key=lambda w: w[:3])
    legs = [feet]
    if _clearance(body, feet, boxes, 1.0) < PATH_ROOM:  # someone stands in the way (live run 2, try 3: the dealer)
        via = _detour(body, feet, boxes)
        if via is None:
            st.failures.append(f"pick_up: no way around to the {beat['take']} for {beat['actor']}; start "
                               f"{beat['actor']} on the {beat['take']}'s side")
        legs = [via, feet] if via is not None else legs
    start, at = f0, body
    for leg in legs:
        if (leg - at).length >= 0.05:
            start = _travel(beat, st, lib, o, arm, "Walk", start, (leg - at).normalized(), want=(leg - at).length,
                            ignore=item)
            at = kit.loc_at(o, start)
    kit.key_rot(o, start, kit.rot_at(o, start))
    start = min(start + TURN_FRAMES, sc.frame_end)
    r = kit.rot_at(o, f0)
    kit.key_rot(o, start, (r.x, r.y, yaw0 + turn))  # into the reach, from the way it faced before the walk
    strip = _strip(arm, lib, "PickUp", start)
    c = min(start + contact, sc.frame_end)
    # its next move waits until it stands up again: a walk starting mid-bend pinned the bent body 0.5 m into the ground
    st.busy[beat["actor"]] = min(int(strip.frame_end), sc.frame_end)
    # the item is held still from the bend on (it lies at rest by then): the stand-in's bend knocked the box 0.6 m away
    _step_to(start)
    loc, rq, _ = item.matrix_world.decompose()
    item.location, item.rotation_euler = loc, rq.to_euler()
    for f in (start, c):
        item.keyframe_insert("location", frame=f)
        item.keyframe_insert("rotation_euler", frame=f)
    if item.rigid_body is not None:  # physics lets go of it: from here it follows its keys and the hand
        item.rigid_body.kinematic = True
        item.keyframe_insert("rigid_body.kinematic", frame=start)
    _step_to(c)
    gap = kit.tree(item).find_nearest(hand_at())[3]
    if gap is None or gap > GRAB_GAP:
        why = ("the walk over takes the whole scene; start them nearer it" if start >= sc.frame_end - 1
               else "the walk to it was blocked")
        st.failures.append(f"pick_up: {beat['actor']}'s hand misses the {beat['take']} by "
                           f"{gap if gap is not None else 9:.2f} m ({why})")
        sc.frame_set(1)
        return  # it stays on the ground: attached, it flew after a hand 1.7 m away (live run 2, try 3)
    if clear < BEND_ROOM:
        st.failures.append(f"pick_up: no room around the {beat['take']} for {beat['actor']} to bend "
                           f"({clear:.2f} m to the nearest thing): someone else's move reaches over it; keep them still until "
                           f"it is picked up")
    hl, hr, _ = (arm.matrix_world @ arm.pose.bones[hand_bone].matrix).decompose()
    con = item.constraints.new("CHILD_OF")
    con.name, con.target, con.subtarget = "picked", arm, hand_bone
    con.use_scale_x = con.use_scale_y = con.use_scale_z = False
    con.inverse_matrix = Matrix.LocRotScale(hl, hr, Vector((1, 1, 1))).inverted()
    for f, v in ((1, 0.0), (c - 1, 0.0), (c, 1.0)):
        con.influence = v
        con.keyframe_insert("influence", frame=max(f, 1))
    st.resting[:] = [r for r in st.resting if r[0] is not item]  # in the hand now, not on the ground
    # the hand closes on it through the bend, not only from the grab frame (live run 2, try 3: one frame early)
    st.allowed.setdefault(frozenset((o.name, item.name)), set()).update(range(start, sc.frame_end + 1))
    sc.frame_set(1)
    return strip


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
    if beat["move"] == "throw_prop":
        launch = kit.facing_vec(o) * 3.0 + Vector((0, 0, 2.0))
    else:  # let go out to the side: straight down it lay against the foot and nobody could bend for it (Eiffel Short)
        sc = bpy.context.scene
        sc.frame_set(let_go)
        out = prop.matrix_world.translation - o.matrix_world.translation
        taker = next((b["actor"] for b in st.plan["beats"] if b["move"] == "pick_up" and b.get("take") == beat["actor"]), None)
        speed = DROP_OUT
        if taker:  # toward whoever picks it up, out of the dropper's reach (the dealer's cheer: live run 2, try 2)
            out, speed = st.objs[taker].matrix_world.translation - o.matrix_world.translation, DROP_TOWARD
        out.z = 0
        launch = out.normalized() * speed if out.length > 1e-4 else None
        sc.frame_set(1)
    moves.release(st, prop, let_go + 1, launch=launch)
    # it starts inside its owner's hand: collide with everything still but the person who held it (a box let go
    # stayed stuck on the officer)
    kit.layers(prop, [2])
    for other in bpy.context.scene.objects:
        if other is not o and other.rigid_body is not None and other.rigid_body.type == "PASSIVE":
            other.rigid_body.collision_collections[2] = True
    st.resting.append((prop, st.ground))


DRINK_UP, DRINK_TIP, DRINK_GONE, DRINK_DOWN = 0.5, 0.35, 0.12, 0.4  # seconds: to the face, tipped, popped, arm down
DRINK_TILT = 110  # degrees the cup tips back toward the face


def drink(beat: dict, st, lib: dict, o, arm, f0: int) -> None:
    """drink (owner, 2026-10-29): no clip lifts a hand to the mouth, so an IK pulls the right fist up in front of the
    face, the held cup tips back toward it and then shrinks to nothing (the owner's gag: there is no mouth to pour
    into), and the empty hand goes back down. The person's next move waits for it (st.busy)."""
    prop = bpy.data.objects.get(o.get("prop") or "")
    if prop is None:
        st.failures.append(f"drink: {beat['actor']} has no prop to drink from")
        return
    sc = bpy.context.scene
    up = f0 + round(DRINK_UP * st.fps)
    tipped = up + round(DRINK_TIP * st.fps)
    gone = tipped + round(DRINK_GONE * st.fps)
    down = gone + round(DRINK_DOWN * st.fps)
    if gone > sc.frame_end:
        st.failures.append(f"drink: {beat['actor']} starts drinking too late to finish by the end of the scene")
        return
    sc.frame_set(f0)
    hand = arm.pose.bones[lib["bones"]["hand_r"]]
    head = arm.pose.bones[lib["bones"]["head"]]
    base, top = arm.matrix_world @ head.head, arm.matrix_world @ head.tail
    face = facing_now(o, f0)
    # in front of the face, a quarter up the head: measured on the mesh, as the cartoon head is far bigger than its
    # bone (placed from the bone, the cup went to the cheek like a phone call, 2026-10-29)
    chin = base + (top - base) * 0.25
    front = max((v - chin).dot(face) for v in kit.world_verts(o) if base.z <= v.z <= top.z)
    mouth = chin + face * (front + 0.04)
    rest = arm.matrix_world @ hand.head
    aim = bpy.data.objects.new(f"{o.name}.drink", None)
    sc.collection.objects.link(aim)
    for f, at in ((f0, rest), (up, mouth), (gone, mouth), (down, rest)):
        kit.key_loc(aim, f, at)
    ik = hand.parent.constraints.new("IK")  # the forearm: its tail is the wrist
    ik.target, ik.chain_count = aim, 2
    for f, v in ((f0, 0.0), (up, 1.0), (gone, 1.0), (down, 0.0)):
        ik.influence = v
        ik.keyframe_insert("influence", frame=f)
    # tip the cup about its grip, top toward the face; keyed on its own transform under the hand's CHILD_OF
    sc.frame_set(tipped)
    world = prop.matrix_world.copy()
    held = world @ prop.matrix_basis.inverted()  # the hand's part of its world matrix
    grip = world @ Vector(prop["grip"])
    turn = Matrix.Translation(grip) @ Matrix.Rotation(math.radians(DRINK_TILT), 4, face.cross(Vector((0, 0, 1))).normalized()) \
        @ Matrix.Translation(-grip)
    loc0, rot0, size0 = prop.location.copy(), prop.rotation_euler.copy(), prop.scale.copy()
    loc1, quat1, _ = (held.inverted() @ turn @ world).decompose()
    for f, loc, rot, size in ((up, loc0, rot0, size0), (tipped, loc1, quat1.to_euler(rot0.order, rot0), size0),
                              (gone, loc1, quat1.to_euler(rot0.order, rot0), size0 * 0.01)):
        prop.location, prop.rotation_euler, prop.scale = loc, rot, size
        for path in ("location", "rotation_euler", "scale"):
            prop.keyframe_insert(path, frame=f)
    sc.frame_set(1)
    st.busy[beat["actor"]] = down
