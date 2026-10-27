"""Stand-in people library for the tests: blender.exe -b --factory-startup --python tests/people_standin.py -- <out dir> [drop]

The Quaternius files may not be in git (licence), so the opener tests build this instead: for every body the roles
table names, a plain capsule person on an armature with the real rig's bone names, its materials named as the roles
colour them; for every clip the people moves name, a simple action (legs swing for walks, a topple for deaths, an
arm arc for swings). Same people.blend + people.json format as blender/pack_people.py."""

import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
TABLES = json.loads((ROOT / "blender" / "opener_tables.json").read_text(encoding="utf-8"))
BONES = {"head": "Head", "hand_r": "Fist.R", "foot_l": "Foot.L", "foot_r": "Foot.R"}
H = 1.8  # the stand-in's height
STRIDE = 1.2  # metres covered by one loop of a travel clip
LOOP = 16  # frames in a loop


def part(name: str, loc, scale, mat) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=1, depth=1, location=loc)
    o = bpy.context.active_object
    o.name, o.scale = name, scale
    o.data.materials.append(mat)
    bpy.ops.object.transform_apply(scale=True)
    return o


def body(name: str, materials: list[str]) -> tuple:
    mats = {m: bpy.data.materials.get(f"{name}:{m}") or bpy.data.materials.new(f"{name}:{m}") for m in materials}
    for m in mats.values():
        m.name = m.name.split(":", 1)[1] if ":" in m.name else m.name
    main = mats.get("Main") or next(iter(mats.values()))
    skin = mats.get("Skin") or main
    parts = [part("torso", (0, 0, 1.15), (0.2, 0.14, 0.6), main),
             part("head", (0, 0, 1.62), (0.12, 0.12, 0.3), skin),
             part("leg_l", (0.09, 0, 0.42), (0.07, 0.07, 0.84), main),
             part("leg_r", (-0.09, 0, 0.42), (0.07, 0.07, 0.84), main),
             part("arm_r", (-0.27, 0, 1.15), (0.05, 0.05, 0.6), skin)]
    for extra in [m for m in mats.values() if m not in (main, skin)]:
        parts[0].data.materials.append(extra)  # every named material is on the body, so colouring it works
    with bpy.context.temp_override(active_object=parts[0], selected_editable_objects=parts, selected_objects=parts):
        bpy.ops.object.join()
    mesh = parts[0]
    mesh.name = f"body:{name}"
    arm = bpy.data.objects.new(f"rig:{name}", bpy.data.armatures.new(f"rig:{name}"))
    bpy.context.scene.collection.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    eb = arm.data.edit_bones
    root = eb.new("Body")
    root.head, root.tail = (0, 0, 0.85), (0, 0, 1.45)
    for bname, head, tail in (("Head", (0, 0, 1.45), (0, 0, 1.8)), ("Arm.R", (-0.27, 0, 1.45), (-0.27, 0, 0.85)),
                              ("Foot.L", (0.09, 0, 0.85), (0.09, 0, 0)), ("Foot.R", (-0.09, 0, 0.85), (-0.09, 0, 0))):
        b = eb.new(bname)
        b.head, b.tail, b.parent = head, tail, root
    fist = eb.new("Fist.R")  # like the real rig: a short hand bone whose head is the hand
    fist.head, fist.tail, fist.parent = (-0.27, 0, 0.85), (-0.27, 0, 0.78), eb["Arm.R"]
    bpy.ops.object.mode_set(mode="OBJECT")
    groups = {n: mesh.vertex_groups.new(name=n) for n in ("Body", "Head", "Arm.R", "Foot.L", "Foot.R")}
    for v in mesh.data.vertices:
        c = v.co
        g = "Head" if c.z > 1.45 else "Arm.R" if c.x < -0.2 else "Foot.L" if c.z < 0.85 and c.x > 0 \
            else "Foot.R" if c.z < 0.85 else "Body"
        groups[g].add([v.index], 1.0, "REPLACE")
    mesh.parent = arm
    mesh.modifiers.new("rig", "ARMATURE").object = arm
    for pb in arm.pose.bones:
        pb.rotation_mode = "XYZ"
    return mesh, arm


def key(arm, frames: dict) -> None:
    """frames: {frame: {bone: (x, y, z) degrees}}"""
    for f, pose in frames.items():
        for b, rot in pose.items():
            pb = arm.pose.bones[b]
            pb.rotation_euler = [math.radians(r) for r in rot]
            pb.keyframe_insert("rotation_euler", frame=f)


def clip(arm, name: str, travel: bool) -> dict:
    arm.animation_data_create()
    act = bpy.data.actions.new(name)
    act.use_fake_user = True
    arm.animation_data.action = act
    if travel:
        key(arm, {1: {"Foot.L": (25, 0, 0), "Foot.R": (-25, 0, 0)}, LOOP // 2 + 1: {"Foot.L": (-25, 0, 0), "Foot.R": (25, 0, 0)},
                  LOOP + 1: {"Foot.L": (25, 0, 0), "Foot.R": (-25, 0, 0)}})
        frames = LOOP
    elif name in ("Death", "Defeat"):
        key(arm, {1: {"Body": (0, 0, 0)}, 21: {"Body": (-85, 0, 0)}})
        frames = 20
    elif name in ("SwordSlash", "Punch"):
        key(arm, {1: {"Arm.R": (0, 0, 0)}, 5: {"Arm.R": (150, 0, 0)}, 11: {"Arm.R": (40, 0, 0)}})
        frames = 10
    else:
        key(arm, {1: {"Head": (0, 0, 0)}, 8: {"Head": (15, 0, 0)}, 16: {"Head": (0, 0, 0)}})
        frames = 15
    arm.animation_data.action = None
    return {"frames": frames, "loop": travel or name == "Idle", "stride_m": STRIDE if travel else None}


def main(out: Path, drop: str = "") -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    out.mkdir(parents=True, exist_ok=True)
    needed: dict[str, set] = {}
    for r in TABLES["roles"].values():
        needed.setdefault(r["body"], {"Main", "Skin"}).update(r["colours"])
    for mats in needed.values():
        mats.discard(drop)  # a body missing a material a role colours (test_missing_slot_is_skipped)
    data = {"bodies": {}, "bones": BONES, "clips": {}, "rig_height": H}
    arm = None
    for name, mats in sorted(needed.items()):
        mesh, arm = body(name, sorted(mats))
        data["bodies"][name] = {"object": mesh.name, "armature": arm.name, "materials": sorted(mats), "height": H}
    travel = {m["clip"] for m in TABLES["people_moves"].values() if m["kind"] == "travel"}
    for name in sorted({m["clip"] for m in TABLES["people_moves"].values()}):
        data["clips"][name] = clip(arm, name, name in travel)
    bpy.ops.wm.save_as_mainfile(filepath=str(out / "people.blend"))
    (out / "people.json").write_text(json.dumps(data, indent=1), encoding="utf-8")


if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:]
    main(Path(args[0]), args[1] if len(args) > 1 else "")
