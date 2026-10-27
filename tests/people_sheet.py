"""Contact sheets of the people library (part 2, 2026-10-27), to look at by eye: every role standing
(cache/people_sheet/roles.png) and every people move caught mid-clip (cache/people_sheet/moves.png), in the openers'
cel-shaded look. Skips with a note when the real library isn't packed on D: (blender/pack_people.py).
Run: .venv\\Scripts\\python.exe tests\\people_sheet.py   (a minute or two of Blender)"""
import json
import subprocess
import sys
from pathlib import Path

try:
    import bpy  # inside Blender: build and render
except ImportError:
    bpy = None

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "cache" / "people_sheet"


def render_sheet(kind: str) -> None:
    import math
    from mathutils import Vector
    sys.path.insert(0, str(ROOT / "blender"))
    import look_toon
    import people
    import scene_kit as kit
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = 2400, 900
    for engine in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            sc.render.engine = engine
            break
        except TypeError:
            continue
    sc.view_settings.view_transform = "AgX"
    sc.frame_start, sc.frame_end = 1, 120
    lib = people.load_library({"people": {"blend": str(ROOT / "blender/assets/people/people.blend"),
                                          "json": str(ROOT / "blender/assets/people/people.json")}})
    if kind == "roles":
        rows = [(r, "idle", {"id": r, "person": r, "facing": "camera"}) for r in kit.TABLES["roles"]]
    else:
        rows = [(m, m, {"id": m, "person": "ww2_british_officer", "facing": "right"}) for m in kit.TABLES["people_moves"]]
    gap = 0.9
    for k, (label, move, actor) in enumerate(rows):
        o = people.dress(actor, kit.TABLES["roles"][actor["person"]], lib, {})
        o.location = Vector(((k - (len(rows) - 1) / 2) * gap, 0, 0))
        people.idle(o, lib)
        if kind == "moves":
            clip = kit.TABLES["people_moves"][move]["clip"]
            frames = lib["clips"][clip]["frames"]
            people._strip(bpy.data.objects[o["rig"]], lib, clip, max(1, 60 - round(0.6 * frames)))
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 4.5
    sun.rotation_euler = (math.radians(50), 0, math.radians(35))
    sc.collection.objects.link(sun)
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    next(n for n in w.node_tree.nodes if n.type == "BACKGROUND").inputs["Color"].default_value = (0.75, 0.8, 0.85, 1)
    bpy.ops.mesh.primitive_plane_add(size=200)
    bpy.context.active_object.name = "ground"
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.data.type, cam.data.ortho_scale = "ORTHO", len(rows) * gap + 0.6
    cam.location, cam.rotation_euler = (0, -12, 1.6), (math.radians(88), 0, 0)
    look_toon.apply(list(sc.objects))
    sc.frame_set(60)
    OUT.mkdir(parents=True, exist_ok=True)
    sc.render.filepath = str(OUT / f"{kind}.png")
    bpy.ops.render.render(write_still=True)
    (OUT / f"{kind}.txt").write_text("\n".join(label for label, *_ in rows), encoding="utf-8")


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from shortsmaker import config
    if not config.PEOPLE_JSON.exists():
        print(f"SKIP: no people library at {config.PEOPLE_DIR} (run blender/pack_people.py)")
        return 0
    for kind in ("roles", "moves"):
        r = subprocess.run([str(config.BLENDER), "-b", "--factory-startup", "--python-exit-code", "1", "--python",
                            __file__, "--", kind], capture_output=True, text=True, timeout=900)
        if r.returncode != 0:
            print((r.stdout or "")[-2000:] + (r.stderr or "")[-2000:])
            return 1
        print(f"wrote {OUT / (kind + '.png')} ({(OUT / (kind + '.txt')).read_text(encoding='utf-8').count(chr(10)) + 1} people, left to right as in {kind}.txt)")
    return 0


if __name__ == "__main__":
    if bpy is not None:
        render_sheet(sys.argv[sys.argv.index("--") + 1])
    else:
        sys.exit(main())
