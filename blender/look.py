"""The ink-manual look shared by every Blender Short: flat colours, a paper sky, dark ink outlines (Freestyle).
Runs inside Blender (bpy); not imported by the shortsmaker package."""

import bpy

COLORS = {"paper": "#EEE8DC", "steel": "#9EA8B3", "concrete": "#E3DCCD", "water": "#C3D7E5", "red": "#D81F1A",
          "ink": "#141419", "dark": "#7C8894", "ground": "#D9D0BC"}
NOLINES = "nolines"  # labels and leader lines: already ink, no outline drawn around them


def linear(hex_color: str) -> tuple[float, float, float, float]:
    """sRGB hex to the linear colour Blender's shaders use (the Standard view transform turns it back)."""
    out = []
    for k in (1, 3, 5):
        c = int(hex_color[k:k + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, 1.0)


def setup(scene: bpy.types.Scene, fps: int = 30) -> None:
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = 1080, 1920, 100
    scene.render.fps = fps
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "Standard"
    try:
        scene.eevee.taa_render_samples = 16  # flat colours need few samples
    except AttributeError:
        pass
    world = bpy.data.worlds.new("paper")
    scene.world = world
    world.use_nodes = True
    bg = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs[0].default_value = linear(COLORS["paper"])
    scene.render.use_freestyle = True
    scene.render.line_thickness_mode = "ABSOLUTE"
    scene.render.line_thickness = 2.2
    fs = scene.view_layers[0].freestyle_settings
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new("ink")
    ls.linestyle = ls.linestyle or bpy.data.linestyles.new("ink")
    ls.linestyle.color = linear(COLORS["ink"])[:3]
    ls.linestyle.thickness = 2.2
    ls.select_by_collection = True
    ls.collection = collection(scene, NOLINES)
    ls.collection_negation = "EXCLUSIVE"


def collection(scene: bpy.types.Scene, name: str) -> bpy.types.Collection:
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        scene.collection.children.link(col)
    return col


def material(name: str) -> bpy.types.Material:
    """A flat (emission-only) material in one of COLORS, made once."""
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs[0].default_value = linear(COLORS[name])
    nt.links.new(em.outputs[0], out.inputs[0])
    return mat
