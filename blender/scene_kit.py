"""Shared helpers for building openers (2026-10-27), plain bpy: loading library models as one clean mesh each, world
bounding boxes and surfaces, keyframes, and rigid-body physics. Library models face -Y (glTF's forward)."""

import json
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

TABLES = json.loads((Path(__file__).resolve().parent / "opener_tables.json").read_text(encoding="utf-8"))
FACING = {"right": Vector((1, 0, 0)), "left": Vector((-1, 0, 0)), "camera": Vector((0, -1, 0)), "away": Vector((0, 1, 0))}
MARGIN = 0.001  # rigid-body collision margin; Blender's default 4 cm leaves things hovering


def frame_of(t: float, fps: int) -> int:
    return 1 + round(t * fps)


def world_verts(o) -> list[Vector]:
    dg = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(dg)
    me = ev.to_mesh()
    vs = [ev.matrix_world @ v.co for v in me.vertices]
    ev.to_mesh_clear()
    return vs


def bbox(o) -> tuple[Vector, Vector]:
    vs = world_verts(o)
    return (Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs))),
            Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs))))


def tree(o) -> BVHTree:
    dg = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(dg)
    me = ev.to_mesh()
    t = BVHTree.FromPolygons([ev.matrix_world @ v.co for v in me.vertices], [p.vertices[:] for p in me.polygons])
    ev.to_mesh_clear()
    return t


def surface_z(o, x: float, y: float) -> float | None:
    """The height of o's top surface above (x, y), or None when nothing of o is there."""
    hit = tree(o).ray_cast(Vector((x, y, 1000)), Vector((0, 0, -1)))
    return hit[0].z if hit[0] is not None else None


def material(name: str, rgb) -> bpy.types.Material:
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1)
    bsdf.inputs["Roughness"].default_value = 0.9
    m.diffuse_color = (*rgb, 1)
    return m


def merge(objs: list, name: str) -> bpy.types.Object:
    """One mesh object from many (world transforms applied, materials kept), origin at the bottom centre."""
    sc = bpy.context.scene
    bm, mats = bmesh.new(), []
    dg = bpy.context.evaluated_depsgraph_get()
    for o in objs:
        if o.type != "MESH":
            continue
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.transform(ev.matrix_world)
        offset = len(mats)
        mats += [s.material for s in o.material_slots]
        part = bmesh.new()
        part.from_mesh(me)
        for f in part.faces:
            f.material_index += offset
        tmp = bpy.data.meshes.new("tmp")
        part.to_mesh(tmp)
        part.free()
        bm.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
        ev.to_mesh_clear()
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(m)
    obj = bpy.data.objects.new(name, me)
    sc.collection.objects.link(obj)
    vs = [v.co for v in me.vertices]
    base = Vector(((min(v.x for v in vs) + max(v.x for v in vs)) / 2, (min(v.y for v in vs) + max(v.y for v in vs)) / 2,
                   min(v.z for v in vs)))
    me.transform(Matrix.Translation(-base))
    obj.location = base
    return obj


def load_model(source: str, name: str) -> bpy.types.Object:
    """A library .blend (every object in it) or "primitive:cube", as one mesh object called `name`."""
    sc = bpy.context.scene
    if source.startswith("primitive:"):
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        cube = bpy.context.active_object
        cube.data.materials.append(material("crate", (0.62, 0.45, 0.28)))
        obj = merge([cube], name)
        bpy.data.objects.remove(cube, do_unlink=True)
        return obj
    with bpy.data.libraries.load(source) as (src, dst):
        dst.objects = list(src.objects)
    loaded = [o for o in dst.objects if o is not None]
    for o in loaded:
        sc.collection.objects.link(o)
    bpy.context.view_layer.update()
    obj = merge(loaded, name)
    for o in loaded:
        bpy.data.objects.remove(o, do_unlink=True)
    return obj


def fit(obj, size_m: float, facing: str) -> None:
    """Largest side = size_m, turned so its front (-Y) faces `facing`; transforms applied, origin at the bottom."""
    me = obj.data
    vs = [v.co for v in me.vertices]
    big = max(max(v[i] for v in vs) - min(v[i] for v in vs) for i in range(3)) or 1.0
    turn = {"right": 90, "left": -90, "camera": 0, "away": 180}[facing]
    me.transform(Matrix.Rotation(__import__("math").radians(turn), 4, "Z") @ Matrix.Scale(size_m / big, 4))
    me.update()
    obj["facing"] = facing


def facing_vec(obj) -> Vector:
    return FACING.get(obj.get("facing", "camera"), FACING["camera"]).copy()


def fcurves(obj) -> list:
    ad = obj.animation_data
    if not ad or not ad.action:
        return []
    a = ad.action
    if hasattr(a, "fcurves"):
        return list(a.fcurves)
    return [fc for layer in a.layers for strip in layer.strips for cb in strip.channelbags for fc in cb.fcurves]


def loc_at(obj, frame: int) -> Vector:
    """Where obj's keys put it on `frame`, without stepping the scene (stepping would run physics too early)."""
    out = obj.location.copy()
    for fc in fcurves(obj):
        if fc.data_path == "location":
            out[fc.array_index] = fc.evaluate(frame)
    return out


def rot_at(obj, frame: int) -> Vector:
    out = Vector(obj.rotation_euler)
    for fc in fcurves(obj):
        if fc.data_path == "rotation_euler":
            out[fc.array_index] = fc.evaluate(frame)
    return out


def lift_for(obj, rot) -> float:
    """How far a tilt about the origin (its feet) pushes obj's lowest point below the feet: lift it by that much so
    a stagger never sinks it into what it stands on."""
    from mathutils import Euler
    m = Euler(rot).to_matrix()
    return max(0.0, -min((m @ v.co).z for v in obj.data.vertices))


def layers(obj, which: list[int]) -> None:
    """The physics collision layers obj is in: two bodies collide only when they share one. Statics are in 0 and 1,
    a cut's resting "rest" piece in 1, its moving pieces in 0, so a cut-off head never collides with the body it
    came from (their hulls start overlapping and physics would blast the head away)."""
    obj.rigid_body.collision_collections = [i in which for i in range(20)]


def remove_body(obj) -> None:
    if obj.rigid_body is not None:
        with bpy.context.temp_override(object=obj, active_object=obj, selected_objects=[obj]):
            bpy.ops.rigidbody.object_remove()


def key_loc(obj, frame: int, loc) -> None:
    obj.location = loc
    obj.keyframe_insert("location", frame=frame)


def key_rot(obj, frame: int, rot) -> None:
    obj.rotation_euler = rot
    obj.keyframe_insert("rotation_euler", frame=frame)


def key_vis(obj, frame: int, visible: bool) -> None:
    obj.hide_render = obj.hide_viewport = not visible
    obj.keyframe_insert("hide_render", frame=frame)
    obj.keyframe_insert("hide_viewport", frame=frame)


def interpolation(obj, kind: str, frames=None, easing: str | None = None) -> None:
    """Set the interpolation of obj's keys (all, or only those on `frames`); visibility keys are always CONSTANT."""
    for fc in fcurves(obj):
        for k in fc.keyframe_points:
            if fc.data_path.startswith(("hide", "rigid_body")):
                k.interpolation = "CONSTANT"
            elif frames is None or round(k.co[0]) in frames:
                k.interpolation = kind
                if easing:
                    k.easing = easing


def ensure_world() -> None:
    if bpy.context.scene.rigidbody_world is None:
        bpy.ops.rigidbody.world_add()
    w = bpy.context.scene.rigidbody_world
    w.point_cache.frame_start, w.point_cache.frame_end = bpy.context.scene.frame_start, bpy.context.scene.frame_end
    w.substeps_per_frame, w.solver_iterations = 20, 20


def add_body(obj, kind: str, shape: str) -> None:
    ensure_world()
    if obj.rigid_body is None:
        with bpy.context.temp_override(object=obj, active_object=obj, selected_objects=[obj]):
            bpy.ops.rigidbody.object_add(type=kind)
    rb = obj.rigid_body
    rb.type, rb.collision_shape = kind, shape
    rb.use_margin, rb.collision_margin = True, MARGIN
    rb.friction, rb.restitution = 0.8, 0.15
    rb.linear_damping, rb.angular_damping = 0.1, 0.3


def make_static(obj) -> None:
    """Something physics bodies land on and bounce off; it may still move by its own keyframes."""
    add_body(obj, "PASSIVE", "MESH")
    obj.rigid_body.kinematic = True
    layers(obj, [0, 1])


def make_dynamic(obj, release: int, launch: Vector | None = None, spin: Vector | None = None) -> None:
    """Held by its keyframes until `release`, then moved by physics. A launch (m/s) and spin (rad/s) are given by
    keying the two frames before the release: physics keeps the speed of the keyed motion (checked 2026-10-27)."""
    add_body(obj, "ACTIVE", "CONVEX_HULL")
    layers(obj, [0])
    rb = obj.rigid_body
    fps = bpy.context.scene.render.fps
    if launch is not None or spin is not None:
        # where it was until release - 2, then one frame of the launch motion: nothing moves before its time
        start, rot = loc_at(obj, max(release - 2, 1)), rot_at(obj, max(release - 2, 1))
        key_loc(obj, max(release - 2, 1), start)
        key_rot(obj, max(release - 2, 1), rot)
        key_loc(obj, max(release - 1, 1), start + (launch or Vector()) / fps)
        key_rot(obj, max(release - 1, 1), Vector(rot) + (spin or Vector()) / fps)
        interpolation(obj, "LINEAR", {release - 2, release - 1})
    rb.kinematic = True
    obj.keyframe_insert("rigid_body.kinematic", frame=1)
    obj.keyframe_insert("rigid_body.kinematic", frame=max(release - 1, 1))
    rb.kinematic = False
    obj.keyframe_insert("rigid_body.kinematic", frame=release)
    interpolation(obj, "LINEAR", set())  # only makes the kinematic switch keys CONSTANT


def simulate() -> None:
    """Step every frame in order once so the rigid-body cache holds the whole clip."""
    sc = bpy.context.scene
    if sc.rigidbody_world is None:
        return
    for f in range(sc.frame_start, sc.frame_end + 1):
        sc.frame_set(f)
