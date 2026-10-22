"""Failure animations on the focus part: bend (it buckles), crack (a dark crack grows across it), shear (its rivets,
bolts, pin or weld let go and the joint slips), sway (the span twists harder and harder); `collapse_span` then drops
that span into the water. Each runs from t0 to its peak frame; `reset` puts everything back (after the hook's
preview, the story starts again from an empty site). Runs inside Blender (bpy)."""

import math
import random

import bpy
from mathutils import Matrix, Vector

import look
import parts


def key(o, path: str, frame: int, value=None, index: int = -1) -> None:
    if value is not None:
        if index >= 0:
            getattr(o, path)[index] = value
        else:
            setattr(o, path, value)
    o.keyframe_insert(path, frame=frame, index=index)


class Failure:
    def __init__(self, b, plan: dict, focus, red, fasteners: list):
        self.b, self.plan, self.focus, self.red, self.fasteners = b, plan, focus, red, fasteners
        self.kind, self.then = plan["failure"]["kind"], plan["failure"]["then"]
        self.side = -1 if plan["focus"]["at"]["side"] == "left" else 1
        self.size = parts.bbox_size(focus)
        span = plan["failure"]["span"]
        self.pivot = bpy.data.objects.new("span_pivot", None)  # sway and collapse turn the span around this
        bpy.context.scene.collection.objects.link(self.pivot)
        self.pivot.location = Vector((b.x0(span) + b.L / 2, 0, b.deck_z))
        self.pivot.rotation_mode = "XYZ"
        self.pivot_home = self.pivot.location.copy()
        inv = Matrix.Translation(self.pivot.location).inverted()
        focus_span = plan["focus"]["at"]["span"]
        members = [o for name, o in b.objects.items() if b.span_of.get(name) == span]
        members += [red] + fasteners if focus_span == span else []
        for o in members:
            o.parent, o.matrix_parent_inverse = self.pivot, inv
        self.home = {o.name: o.location.copy() for o in [focus, red] + fasteners}
        self.crack = self._crack() if self.kind == "crack" else []
        if self.kind == "bend":
            for o in (focus, red):  # a box has 8 corners: subdivide it so it can curve, then warp it in its plane
                sub = o.modifiers.new("detail", "SUBSURF")
                sub.subdivision_type, sub.levels, sub.render_levels = "SIMPLE", 4, 4
                m = o.modifiers.new("bend", "SIMPLE_DEFORM")
                m.deform_method, m.deform_axis, m.angle = "BEND", "Y", 0.0

    def _crack(self) -> list:
        """A jagged crack across the plate's outer face, in short ink segments that appear one after another."""
        rnd = random.Random(7)
        sx, sy, sz = self.focus.scale
        face = self.focus.location + Vector((0, self.side * sy * 0.62, 0))
        pts = [face + Vector((sx * (-0.5 + k / 10), 0, sz * (0.35 - 0.07 * k + rnd.uniform(-0.08, 0.08)))) for k in range(11)]
        col = bpy.data.collections[look.NOLINES]
        segs = [parts.member(f"crack_{k}", a, c, max(sx, sz) * 0.07, "ink", col) for k, (a, c) in enumerate(zip(pts, pts[1:]))]
        for o in segs:
            key(o, "hide_render", 1, True)
        return segs

    def play(self, t0: int, peak: int, until: int | None = None) -> None:
        """The failure from t0 to its peak, then the collapse; `until` (the hook's last frame) cuts it short."""
        peak = max(peak, t0 + 6)
        span = peak - t0
        if self.kind == "bend":
            for o in (self.focus, self.red):
                o.keyframe_insert('modifiers["bend"].angle', frame=t0)
                o.modifiers["bend"].angle = math.radians(70)
                o.keyframe_insert('modifiers["bend"].angle', frame=peak)
            for o in (self.focus, self.red, *self.fasteners):  # it sags as it gives way, its rivets with it
                key(o, "location", t0, self.home[o.name])
                key(o, "location", peak, self.home[o.name] + Vector((0, 0, -self.size * 0.3)))
        elif self.kind == "crack":
            for k, o in enumerate(self.crack):
                key(o, "hide_render", t0 + span * k // len(self.crack), False)
        elif self.kind == "shear":
            out = Vector((0, self.side * self.size * 1.2, -self.size * 0.9))
            for k, o in enumerate(self.fasteners):
                pop = t0 + span * k // max(len(self.fasteners), 1)
                key(o, "location", pop, self.home[o.name])
                key(o, "location", pop + 10, self.home[o.name] + out)
                key(o, "hide_render", pop + 12, True)
            for o in (self.focus, self.red):  # the joint slips once its fasteners are gone
                key(o, "location", peak - 4, self.home[o.name])
                key(o, "location", peak, self.home[o.name] + Vector((0, 0, -self.size * 0.25)))
        elif self.kind == "sway":
            for f in range(t0, peak + 1, 2):
                grow = ((f - t0) / span) ** 1.5  # growing swings, the biggest one on the peak
                key(self.pivot, "rotation_euler", f, math.radians(12) * grow * math.cos(2 * math.pi * (f - peak) / 16), 0)
        fall = min(peak + 33, until - 1) if until else peak + 33  # the hook's fall must end before its cut
        if self.then == "collapse_span" and fall > peak + 6:
            home = self.pivot_home
            key(self.pivot, "location", peak + 3, home)
            key(self.pivot, "rotation_euler", peak + 3, None, 1)
            key(self.pivot, "location", fall, home + Vector((0, 0, -(self.b.deck_z + self.b.H + 8))))
            key(self.pivot, "rotation_euler", fall, math.radians(14), 1)

    def reset(self, frame: int) -> None:
        """Back to whole: the story after the hook starts from the beginning."""
        if self.kind == "bend":
            for o in (self.focus, self.red):
                o.modifiers["bend"].angle = 0.0
                o.keyframe_insert('modifiers["bend"].angle', frame=frame)
        for o in self.crack:
            key(o, "hide_render", frame, True)
        if self.kind in ("shear", "bend"):
            for o in [self.focus, self.red] + self.fasteners:
                key(o, "location", frame, self.home[o.name])
            for o in self.fasteners:
                key(o, "hide_render", frame, False)
        key(self.pivot, "location", frame, self.pivot_home.copy())
        self.pivot.rotation_euler = (0.0, 0.0, 0.0)
        self.pivot.keyframe_insert("rotation_euler", frame=frame)
