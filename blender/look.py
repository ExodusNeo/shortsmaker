"""The ink-manual look shared by every Blender Short: flat colours, a paper sky, dark ink outlines (GPU compositor).
Runs inside Blender (bpy); not imported by the shortsmaker package."""

import bpy

COLORS = {"paper": "#EEE8DC", "steel": "#9EA8B3", "concrete": "#E3DCCD", "water": "#C3D7E5", "red": "#D81F1A",
          "ink": "#141419", "dark": "#7C8894", "ground": "#D9D0BC"}
NOLINES = "nolines"  # labels, leader lines and cracks: kept in their own collection (the outline pass draws them too)


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
    collection(scene, NOLINES)
    ink_lines(scene)


def ink_lines(scene: bpy.types.Scene) -> None:
    """Ink outlines drawn on the GPU after each frame: edges where the surface turns (the normal pass) or the flat
    colour changes (deck against water). Freestyle drew the same look at 3-7 s a frame on a full bridge (one CPU
    core); this costs a fraction of a second."""
    vl = scene.view_layers[0]
    vl.use_pass_normal = True
    ng = bpy.data.node_groups.new("ink", "CompositorNodeTree")
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    n, link = ng.nodes.new, ng.links.new
    rl, out = n("CompositorNodeRLayers"), n("NodeGroupOutput")

    def edges(src, threshold: float):
        sob = n("CompositorNodeFilter")
        sob.inputs["Type"].default_value = "Sobel"
        link(src, sob.inputs["Image"])
        cut = n("ShaderNodeMath")
        cut.operation = "GREATER_THAN"
        link(sob.outputs[0], cut.inputs[0])
        cut.inputs[1].default_value = threshold
        return cut.outputs[0]

    both = n("ShaderNodeMath")
    both.operation = "MAXIMUM"
    link(edges(rl.outputs["Image"], 0.08), both.inputs[0])
    link(edges(rl.outputs["Normal"], 0.5), both.inputs[1])
    mix = n("ShaderNodeMix")
    mix.data_type = "RGBA"
    link(both.outputs[0], mix.inputs["Factor"])
    link(rl.outputs["Image"], mix.inputs[6])
    mix.inputs[7].default_value = linear(COLORS["ink"])
    link(mix.outputs[2], out.inputs[0])
    scene.compositing_node_group = ng
    scene.render.use_compositing = True


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
