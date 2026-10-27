"""The openers' one brand look (part 2, owner 2026-10-27: "everything"): every material cel-shaded in three flat
light bands and every model outlined in ink, so animals, people, props and set read as one 2D cartoon. Applied after
the checks; physics shapes ignore it (rigid bodies read the deformed mesh, and an outline is not a deform)."""

import bpy

BANDS = ((0.0, 1.05), (0.35, 1.5), (0.95, 2.0))  # (light intensity where the band starts, brightness of the band)
INK = (0.02, 0.018, 0.016)
OUTLINE = 0.008  # outline thickness as a share of the model's size
OUTLINE_THIN = 0.2  # and never more than this share of its thinnest side (an axe handle drowned in black)


def toon(mat) -> None:
    """The material's own colour (value or texture) times a banded light: Diffuse on white -> Shader to RGB ->
    constant colour ramp -> times the colour -> emission. Bands come from light alone, so a dark coat and a white
    shirt change band at the same light."""
    nt = mat.node_tree
    out = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"), None)
    bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if out is None or bsdf is None or mat.get("toon"):
        return
    colour = bsdf.inputs["Base Color"]
    source = colour.links[0].from_socket if colour.links else None
    light = nt.nodes.new("ShaderNodeBsdfDiffuse")
    light.inputs["Color"].default_value = (1, 1, 1, 1)
    to_rgb = nt.nodes.new("ShaderNodeShaderToRGB")
    nt.links.new(light.outputs[0], to_rgb.inputs[0])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "CONSTANT"
    els = ramp.color_ramp.elements
    while len(els) < len(BANDS):
        els.new(0.5)
    for el, (pos, level) in zip(els, BANDS):
        el.position, el.color = pos, (level, level, level, 1)
    nt.links.new(to_rgb.outputs["Color"], ramp.inputs["Fac"])
    tint = nt.nodes.new("ShaderNodeVectorMath")
    tint.operation = "MULTIPLY"
    if source is not None:
        nt.links.new(source, tint.inputs[0])
    else:
        tint.inputs[0].default_value = colour.default_value[:3]
    nt.links.new(ramp.outputs["Color"], tint.inputs[1])
    glow = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(tint.outputs[0], glow.inputs["Color"])
    nt.links.new(glow.outputs[0], out.inputs["Surface"])
    mat["toon"] = True


def ink() -> bpy.types.Material:
    m = bpy.data.materials.get("ink") or bpy.data.materials.new("ink")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    glow, out = nt.nodes.new("ShaderNodeEmission"), nt.nodes.new("ShaderNodeOutputMaterial")
    glow.inputs["Color"].default_value = (*INK, 1)
    nt.links.new(glow.outputs[0], out.inputs["Surface"])
    m.use_backface_culling = True  # only the shell's inside faces the camera, round the model's edge
    m["toon"] = True
    return m


def outline(o, ink_mat) -> None:
    """An inverted hull: a slightly bigger copy of the surface, faces flipped, drawn in ink only where it peeks out."""
    if any(m.name == "ink" for m in o.modifiers):
        return
    dims = sorted(d for d in o.dimensions if d > 1e-4) or [0.1]
    size = (sum(d * d for d in dims)) ** 0.5
    o.data.materials.append(ink_mat)
    mod = o.modifiers.new("ink", "SOLIDIFY")
    mod.thickness = -min(OUTLINE * size, OUTLINE_THIN * dims[0])
    mod.offset, mod.use_flip_normals, mod.use_rim = 1.0, True, False
    mod.material_offset = len(o.data.materials) - 1


def apply(objs: list) -> dict:
    """Toon every material of the visible meshes and outline each one but the ground; returns counts for the report."""
    ink_mat = ink()
    meshes = [o for o in objs if o.type == "MESH"]  # pieces hidden until their cut still show later
    mats = {s.material for o in meshes for s in o.material_slots if s.material and s.material is not ink_mat}
    for m in mats:
        if m.node_tree:
            toon(m)
    shells = [o for o in meshes if o.name != "ground"]
    for o in shells:
        if o.data.users > 1:
            o.data = o.data.copy()  # an instanced mesh would get one outline per user
        outline(o, ink_mat)
    return {"meshes": len(shells), "outlined": sum(any(m.name == "ink" for m in o.modifiers) for o in shells),
            "materials": len(mats), "toon": sum(bool(m.get("toon")) for m in mats)}
