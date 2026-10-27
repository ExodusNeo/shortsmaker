"""One-time packer: blender.exe -b --factory-startup --python blender/pack_people.py -- <src dir> <out dir>

Turns the Quaternius Ultimate Animated Character Pack (FBX, one shared 32-bone rig, 17 clips each; owner download,
2026-10-27) into people.blend (every person as mesh "body:<name>" on armature "rig:<name>", every clip once as an
action named after it, e.g. "Walk") and people.json (bodies with their material names and rest height, bones,
clips with frames / loop / stride). The files stay in blender/assets/people (gitignored: the licence forbids
redistributing them). Animals, hats and hair pieces in the pack are skipped."""

import json
import sys
from pathlib import Path

import bpy

SKIP = {"Cow", "Pug", "Chef_Hat", "Cowboy_Hair", "VikingHelmet", "BaseCharacter"}
LOOPS = {"Idle", "Walk", "Run", "Walk_Carry", "Run_Carry"}
BONES = {"head": "Head", "hand_r": "Fist.R", "foot_l": "Foot.L", "foot_r": "Foot.R"}


def clip_name(action_name: str) -> str:
    return action_name.split("|")[-1]


def base_name(material_name: str) -> str:
    """"Main.001" -> "Main": the importer numbers clashing names; roles name the material as the pack does."""
    stem, _, tail = material_name.rpartition(".")
    return stem if stem and tail.isdigit() else material_name


def stride(arm, action) -> float:
    """Ground covered by one loop of an in-place clip: a planted foot slides back by the step length while the
    other swings, so one loop (two steps) covers twice the foot's forward-back range."""
    arm.animation_data.action = action
    sc = bpy.context.scene
    f0, f1 = (int(x) for x in action.frame_range)
    ys = []
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        ys.append((arm.matrix_world @ arm.pose.bones[BONES["foot_l"]].head).y)
    return round(2 * (max(ys) - min(ys)), 4)


def height(mesh) -> float:
    dg = bpy.context.evaluated_depsgraph_get()
    ev = mesh.evaluated_get(dg)
    zs = [(ev.matrix_world @ v.co).z for v in ev.data.vertices]
    return round(max(zs) - min(zs), 4)


def main(src: Path, out: Path) -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    out.mkdir(parents=True, exist_ok=True)
    data = {"bodies": {}, "bones": BONES, "clips": {}}
    bones_ref = None
    for fbx in sorted(src.rglob("*.fbx")):
        name = fbx.stem
        if name in SKIP:
            continue
        before = set(bpy.data.objects)
        before_actions = set(bpy.data.actions)
        bpy.ops.import_scene.fbx(filepath=str(fbx))
        new = [o for o in bpy.data.objects if o not in before]
        arm = next((o for o in new if o.type == "ARMATURE"), None)
        meshes = [o for o in new if o.type == "MESH"]
        if arm is None or not meshes:
            print(f"skip {name}: no armature or mesh")
            continue
        bones = sorted(b.name for b in arm.data.bones)
        if bones_ref is None:
            bones_ref = bones
        elif bones != bones_ref:
            print(f"skip {name}: a different skeleton")
            for o in new:
                bpy.data.objects.remove(o, do_unlink=True)
            continue
        if len(meshes) > 1:
            with bpy.context.temp_override(active_object=meshes[0], selected_editable_objects=meshes,
                                           selected_objects=meshes):
                bpy.ops.object.join()
        body = meshes[0]
        body.name, arm.name = f"body:{name}", f"rig:{name}"
        for action in [a for a in bpy.data.actions if a not in before_actions]:
            clip = clip_name(action.name)
            if clip in data["clips"]:
                bpy.data.actions.remove(action)  # one shared rig: the first character's clips serve all
                continue
            action.name, action.use_fake_user = clip, True
            data["clips"][clip] = {"frames": int(action.frame_range[1] - action.frame_range[0]),
                                   "loop": clip in LOOPS, "stride_m": None}
        if arm.animation_data:
            arm.animation_data.action = None
        bpy.context.view_layer.update()
        data["bodies"][name] = {"object": body.name, "armature": arm.name,
                                "materials": sorted({base_name(s.material.name) for s in body.material_slots if s.material}),
                                "height": height(body)}
        print(f"packed {name}")
    first = next(iter(data["bodies"].values()))
    data["rig_height"] = first["height"]  # strides are measured on this body; scale them by height / rig_height
    arm = bpy.data.objects[first["armature"]]
    arm.animation_data_create()
    for clip in ("Walk", "Run", "Walk_Carry", "Run_Carry"):
        if clip in data["clips"]:
            data["clips"][clip]["stride_m"] = stride(arm, bpy.data.actions[clip])
    arm.animation_data.action = None
    bpy.ops.wm.save_as_mainfile(filepath=str(out / "people.blend"))
    (out / "people.json").write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(f"PACKED {len(data['bodies'])} bodies, {len(data['clips'])} clips")


if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:]
    main(Path(args[0]), Path(args[1]))
