"""Blender side of tests/test_opener_checks.py (2026-10-27): builds tiny cases from primitives, runs each check in
blender/opener_checks.py on them and writes {case: failures} as JSON.
Run by the test: blender.exe -b --factory-startup --python tests/opener_check_cases.py -- <out.json>"""
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "blender"))
import opener_checks as oc  # noqa: E402

out = Path(sys.argv[sys.argv.index("--") + 1])
results = {}


def fresh():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, 30
    sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
    return sc


def cube(name, loc, size=1.0, dims=None):
    bpy.ops.mesh.primitive_cube_add(size=size, location=loc)
    o = bpy.context.active_object
    o.name = name
    if dims:
        o.dimensions = dims
        bpy.ops.object.transform_apply(scale=True)
    return o


def plane(z=0.0):
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, z))
    return bpy.context.active_object


def camera(loc, target):
    d = bpy.data.cameras.new("cam")
    d.lens = 50
    c = bpy.data.objects.new("cam", d)
    bpy.context.scene.collection.objects.link(c)
    c.location = loc
    c.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = c
    return c


def key(o, f, loc):
    o.location = loc
    o.keyframe_insert("location", frame=f)


# overlap: B passes through A on frames 5-6 only
sc = fresh()
a, b = cube("A", (0, 0, 0)), cube("B", (3, 0, 0))
for f, x in ((1, 3), (4, 3), (5, 0.5), (6, 0.5), (7, 3), (30, 3)):
    key(b, f, (x, 0.3, 0.2))  # offset: exactly coplanar faces don't count as crossing
for fc in b.animation_data.action.fcurves if hasattr(b.animation_data.action, "fcurves") else []:
    for k in fc.keyframe_points:
        k.interpolation = "CONSTANT"
results["overlap_bad"] = oc.overlaps([a, b], range(1, 31), {})
results["overlap_allowed"] = oc.overlaps([a, b], range(1, 31), {frozenset(("A", "B")): {5, 6}})

# resting: 3 cm above the ground vs touching it
sc = fresh()
g = plane()
floating = cube("float", (0, 0, 0.5 + 0.03))
results["resting_float"] = oc.resting([(floating, g)], [1])
sc = fresh()
g = plane()
sitting = cube("sit", (0, 0, 0.5 + 0.002))
results["resting_ok"] = oc.resting([(sitting, g)], [1])

# in frame: the cube walks out of the camera's view on frames 15-30
sc = fresh()
mover = cube("mover", (0, 0, 0))
key(mover, 1, (0, 0, 0))
key(mover, 10, (0, 0, 0))
key(mover, 15, (6, 0, 0))
key(mover, 30, (6, 0, 0))
cam = camera((0, -8, 0), (0, 0, 0))
bad = oc.in_frame(mover, cam, range(1, 31))
results["in_frame_bad"] = bad
results["in_frame_ok"] = oc.in_frame(mover, cam, range(1, 10))

# first frame: a tiny far subject vs a big one
sc = fresh()
small, threat = cube("small", (0, 0, 0), size=0.2), cube("threat", (0.6, 0, 0.5), size=0.2)
cam = camera((0, -8, 0), (0, 0, 0))
results["first_small"] = oc.first_frame(small, threat, cam)
big = cube("big", (0, 0, 0), size=2.0)
results["first_ok"] = oc.first_frame(big, threat, cam)
car = cube("car", (0, 0, 3), size=1.0)  # wide and low: a car filling half the width but under 15% of the height
car.scale = (4.0, 1.0, 0.25)
bpy.context.view_layer.update()
results["first_wide"] = oc.first_frame(car, threat, cam)
edge = cube("edge", (1.85, 0, 0), size=1.0)  # a threat only a sliver of which is in frame (the people run's car)
results["threat_sliver"] = oc.first_frame(big, edge, cam, threat_whole=True)
results["threat_sliver_tool"] = oc.first_frame(big, edge, cam)  # a blade's handle may run off: in frame is enough
person = cube("person", (-0.4, 0, -0.4), size=0.6)  # 11% tall beside a big thing he goes at: still too small
truck = cube("truck", (0.6, 2, 0), size=2.5)  # (a pair rule let a tiny officer beside a van through, 2026-10-27)
results["pair_small"] = oc.first_frame(person, truck, cam, threat_whole=True)

# edge leads: a blade moving +x, its edge facing -x (wrong) or +x (right)
sc = fresh()
blade = cube("blade", (0, 0, 0), dims=(0.4, 0.02, 0.3))
key(blade, 1, (0, 0, 0))
key(blade, 10, (1, 0, 0))
target = cube("target", (2, 0, 0))
results["edge_wrong"] = oc.edge_leads(blade, (-1, 0, 0), target, 5)
results["edge_right"] = oc.edge_leads(blade, (1, 0, 0), target, 5)

# hidden: a box right behind a bigger one from the camera's view, then the same box in the open
sc = fresh()
cam = camera((0, -8, 0), (0, 0, 0))
small_box = cube("small_box", (0, 2, 0), size=0.5)
wall = cube("wall", (0, 0, 0), size=1.5)
results["hidden_bad"] = oc.hidden(small_box, cam, [1], [wall])
small_box.location = (2.5, 2, 0)
results["hidden_ok"] = oc.hidden(small_box, cam, [1], [wall, small_box])  # never hidden by itself

# blade face: seen face-on (camera on the thin axis) vs edge-on (camera along the blade)
sc = fresh()
blade = cube("blade", (0, 0, 0), dims=(0.4, 0.02, 0.3))
results["face_ok"] = oc.blade_face(blade, camera((0, -5, 0.5), (0, 0, 0)), 1)
results["face_edge_on"] = oc.blade_face(blade, camera((5, 0, 0.2), (0, 0, 0)), 1)

# cut result: piece shares, piece count, piece size
sc = fresh()
whole = cube("whole", (0, 0, 0), dims=(1, 1, 1))
target_area = oc.area(whole)  # 6 m2
half = cube("half", (5, 0, 0), dims=(1, 1, 0.5))
half["piece"] = "head"
rest = cube("rest", (8, 0, 0), dims=(1, 1, 0.5))
rest["piece"] = "rest"
expect = [{"piece": "head", "share": 0.15, "then": "fly_off"}, {"piece": "rest", "then": "stay"}]
results["cut_half"] = oc.cut_result([half, rest], target_area, expect)
small = cube("smallhead", (11, 0, 0), dims=(0.387, 0.387, 0.387))  # 0.9 m2 = 0.15
small["piece"] = "head"
rest2 = cube("rest2", (14, 0, 0), dims=(1, 1, 0.85))
rest2["piece"] = "rest"
results["cut_ok"] = oc.cut_result([small, rest2], target_area, expect)
bits = []
for i in range(81):
    o = cube(f"bit{i}", (i * 0.2, 5, 0), size=0.05)
    o["piece"] = "bit"
    bits.append(o)
results["cut_too_many"] = oc.cut_result(bits, target_area, [{"pieces": "40-81", "then": "scatter"}])
crumb = cube("crumb", (0, 9, 0), size=0.002)
crumb["piece"] = "bit"
results["cut_crumb"] = oc.cut_result(bits[:50] + [crumb], target_area, [{"pieces": "40-60", "then": "scatter"}])
results["cut_bits_ok"] = oc.cut_result(bits[:50], target_area, [{"pieces": "40-60", "then": "scatter"}])

out.write_text(json.dumps(results, indent=1), encoding="utf-8")
