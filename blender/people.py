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
