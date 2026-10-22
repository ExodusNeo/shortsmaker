"""The parts kit: every piece a bridge is drawn from. Boxes and cylinders share one mesh each (linked duplicates), so
a bridge of a thousand members stays light. Fasteners are era-correct: rivet, bolt (with nut), pin or weld, never
screws. Runs inside Blender (bpy)."""

import math

import bpy
from mathutils import Vector

import look

_MESH: dict[str, bpy.types.Mesh] = {}


def _mesh(kind: str) -> bpy.types.Mesh:
    if kind not in _MESH:
        if kind == "box":
            bpy.ops.mesh.primitive_cube_add(size=1)
        elif kind == "cyl":
            bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.5, depth=1)
        elif kind == "hex":
            bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.5, depth=1)
        tmp = bpy.context.object
        _MESH[kind] = tmp.data
        _MESH[kind].materials.append(look.material("steel"))
        bpy.data.objects.remove(tmp)
    return _MESH[kind]


def _obj(name: str, kind: str, mat: str, col: bpy.types.Collection) -> bpy.types.Object:
    o = bpy.data.objects.new(name, _mesh(kind))
    col.objects.link(o)
    o.material_slots[0].link = "OBJECT"
    o.material_slots[0].material = look.material(mat)
    return o


def box(name, center, size, mat, col, rot=(0.0, 0.0, 0.0)) -> bpy.types.Object:
    o = _obj(name, "box", mat, col)
    o.location, o.scale, o.rotation_euler = Vector(center), Vector(size), rot
    return o


def member(name, p1, p2, thick, mat, col, depth=None) -> bpy.types.Object:
    """A straight steel member (chord, diagonal, vertical, girder) from p1 to p2 with a square-ish section."""
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    o = _obj(name, "box", mat, col)
    o.location = (p1 + p2) / 2
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = d.to_track_quat("X", "Z")
    o.scale = (d.length, thick, depth or thick)
    return o


def cylinder(name, p1, p2, radius, mat, col, kind="cyl") -> bpy.types.Object:
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    o = _obj(name, kind, mat, col)
    o.location = (p1 + p2) / 2
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = d.to_track_quat("Z", "Y")
    o.scale = (radius * 2, radius * 2, max(d.length, 1e-3))
    return o


def deck(name, x0, x1, z, width, thick, col) -> bpy.types.Object:
    return box(name, ((x0 + x1) / 2, 0, z - thick / 2), (x1 - x0, width, thick), "concrete", col)


def gusset_plate(name, center, size, side_y, col) -> bpy.types.Object:
    """A flat plate on the outside face of a truss joint (side_y: -1 left, +1 right)."""
    c = Vector(center) + Vector((0, side_y * size * 0.12, 0))
    return box(name, c, (size, size * 0.08, size * 0.85), "steel", col)


def pier(name, x, z_top, z_bottom, width, col) -> bpy.types.Object:
    h = z_top - z_bottom
    return box(name, (x, 0, z_bottom + h / 2), (max(3.0, width * 0.18), width * 1.15, h), "concrete", col)


def tower(name, x, z0, height, width, col) -> list[bpy.types.Object]:
    legs = [member(f"{name}_leg_{s}", (x, s * width / 2, z0), (x, s * width / 2 * 0.8, z0 + height), width * 0.06,
                   "steel", col) for s in (-1, 1)]
    beam = member(f"{name}_beam", (x, -width / 2 * 0.8, z0 + height * 0.92), (x, width / 2 * 0.8, z0 + height * 0.92),
                  width * 0.05, "steel", col)
    return legs + [beam]


def main_cable(name, points, radius, col) -> list[bpy.types.Object]:
    return [cylinder(f"{name}_{k}", a, b, radius, "dark", col) for k, (a, b) in enumerate(zip(points, points[1:]))]


def hanger(name, top, bottom, radius, col) -> bpy.types.Object:
    return cylinder(name, top, bottom, radius, "dark", col)


def eyebar(name, p1, p2, thick, col) -> bpy.types.Object:
    return member(name, p1, p2, thick * 0.35, "steel", col, depth=thick * 1.3)


def fastener(kind: str, name: str, plate: bpy.types.Object, side_y: int, col) -> list[bpy.types.Object]:
    """The fasteners on a plate's outer face: a grid of rivet heads or bolt heads, one big pin, or a weld seam."""
    sx, sy, sz = plate.scale
    face = plate.location + Vector((0, side_y * sy / 2, 0))
    out = []
    if kind == "pin":
        out.append(cylinder(f"{name}_pin", face - Vector((0, side_y * sy * 2, 0)), face + Vector((0, side_y * sy * 3, 0)),
                            min(sx, sz) * 0.16, "dark", col))
    elif kind == "weld":
        out.append(box(f"{name}_weld", face + Vector((0, side_y * sy * 0.3, -sz * 0.42)), (sx * 0.95, sy * 0.6, sz * 0.05),
                       "dark", col))
    else:
        n, r = 4, min(sx, sz) * 0.045
        for i in range(n):
            for j in range(n):
                c = face + Vector(((i - (n - 1) / 2) * sx * 0.2, 0, (j - (n - 1) / 2) * sz * 0.2))
                tip = c + Vector((0, side_y * r * (1.2 if kind == "rivet" else 2.2), 0))
                out.append(cylinder(f"{name}_{kind}_{i}_{j}", c, tip, r, "dark", col, "cyl" if kind == "rivet" else "hex"))
    return out


def water(z, size, col) -> bpy.types.Object:
    return box("water", (0, 0, z - 0.5), (size, size, 1.0), "water", col)


def valley(z, size, col) -> bpy.types.Object:
    return box("valley_floor", (0, 0, z - 0.5), (size, size, 1.0), "ground", col)


def car(name, x, z, side, col) -> list[bpy.types.Object]:
    return [box(f"{name}_body", (x, side * 1.8, z + 0.8), (4.4, 1.8, 1.2), "steel", col),
            box(f"{name}_cab", (x - 0.3, side * 1.8, z + 1.6), (2.2, 1.6, 0.7), "steel", col)]


def train(name, x, z, col) -> list[bpy.types.Object]:
    return [box(f"{name}_car{k}", (x + k * 21, 0, z + 2.1), (20, 3.1, 3.8), "steel", col) for k in range(3)]


def person(name, x, y, z, col) -> list[bpy.types.Object]:
    return [cylinder(f"{name}_body", (x, y, z), (x, y, z + 1.4), 0.22, "dark", col),
            box(f"{name}_head", (x, y, z + 1.6), (0.3, 0.3, 0.3), "dark", col)]


def label(text: str, anchor: Vector, at: Vector, size: float, camera: bpy.types.Object) -> list[bpy.types.Object]:
    """Manual-style callout: a thin leader line from the part to short capital text that always faces the camera."""
    col = bpy.data.collections[look.NOLINES]
    lines = []
    for chunk in text.split(" · "):  # "GUSSET PLATE U10 · 1/2 INCH": a line each; long chunks wrap at ~20 characters
        cur = ""
        for w in chunk.split():
            if cur and len(cur) + len(w) > 20:
                lines.append(cur)
                cur = w
            else:
                cur = f"{cur} {w}".strip()
        lines.append(cur)
    curve = bpy.data.curves.new("label", "FONT")
    curve.body = "\n".join(lines)
    curve.size, curve.align_x, curve.align_y = size, "CENTER", "BOTTOM"
    txt = bpy.data.objects.new("label", curve)
    col.objects.link(txt)
    txt.data.materials.append(look.material("ink"))
    txt.location = at
    con = txt.constraints.new("TRACK_TO")
    con.target, con.track_axis, con.up_axis = camera, "TRACK_Z", "UP_Y"
    lead = member("label_leader", anchor, at, size * 0.06, "ink", col)
    dot = box("label_dot", anchor, (size * 0.25,) * 3, "ink", col)
    return [txt, lead, dot]


def bbox_size(o: bpy.types.Object) -> float:
    return max(o.scale) if o.data.name in {m.name for m in _MESH.values()} else max(o.dimensions)


def look_at_quat(eye: Vector, target: Vector):
    return (target - eye).to_track_quat("-Z", "Y")


def radians(d: float) -> float:
    return math.radians(d)
