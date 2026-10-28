"""A library model (.blend) as a .glb for the three.js model graphic (remotion/src/full/Model3D.tsx, 2026-10-28).
Headless: blender -b --factory-startup --python export_glb.py -- <model.blend>  (writes <model>.glb beside it)"""
import sys

import bpy

src = sys.argv[sys.argv.index("--") + 1]
out = src[:-len(".blend")] + ".glb"
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(src) as (lib, dst):
    dst.objects = list(lib.objects)
for o in dst.objects:
    if o is not None:
        bpy.context.scene.collection.objects.link(o)
r = bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", export_apply=True, export_animations=False)
assert r == {"FINISHED"}, r
