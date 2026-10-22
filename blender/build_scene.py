"""Entry point: blender.exe -b --factory-startup --python blender/build_scene.py -- <build.json>

Builds a Short's structure from its cleaned build plan (shortsmaker/blender_plan.py), keyframes one camera beat per
scene on the voice's timing, and renders the frames as PNG (frames_dir/f_0001.png ...). build.json:
{"plan": {...}, "scenes": [{"first": 1, "last": 84, "peak_frame": 60, ...}], "fps": 30, "frames_dir": "...",
 "only_frames": [frame, ...] or null}."""

import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import failures  # noqa: E402
import look  # noqa: E402
import parts  # noqa: E402
import templates  # noqa: E402

DROP_FRAMES = 8  # a part takes this long to drop into place


def keyvis(o, frame: int, visible: bool) -> None:
    o.hide_render = not visible
    o.keyframe_insert("hide_render", frame=frame)


def keyloc(o, frame: int, loc: Vector) -> None:
    o.location = loc
    o.keyframe_insert("location", frame=frame)


def direction(yaw: float, pitch: float) -> Vector:
    """From the target toward the camera: yaw 0 looks along +y from the -y side (the left trusses)."""
    y, p = math.radians(yaw), math.radians(pitch)
    return Vector((math.sin(y) * math.cos(p), -math.cos(y) * math.cos(p), math.sin(p)))


class Shots:
    """Camera poses (eye, target) for each beat, sized from the bridge and the focus part."""

    def __init__(self, b, focus, chord: str = "bottom"):
        self.center, self.focus = b.center, focus.location.copy()  # matrix_world is stale until a depsgraph update
        self.far = max(b.length * 0.6, b.H * 5, 60.0)
        self.near = max(parts.bbox_size(focus) * 5, 6.0)
        self.pitch = -6.0 if chord == "bottom" else 12.0  # a part under the deck is seen from below it
        self.fallen = None  # where the focus part lies after its span fell (set when it falls)

    def wide(self, k=1.0, yaw=-62.0, pitch=16.0):
        return self.center + direction(yaw, pitch) * self.far * k, self.center

    def close(self, k=1.0, yaw=-25.0, after=False):
        target = self.fallen if after and self.fallen is not None else self.focus
        return target + direction(yaw, self.pitch) * self.near * k, target

    def beat(self, name: str, after: bool = False):
        """(start pose, end pose) of a beat; `after` the collapse, close shots find the fallen part."""
        close = lambda k: self.close(k, after=after)  # noqa: E731
        return {"wide": (self.wide(1.1), self.wide(1.0)),
                "orbit": (self.wide(1.0, -70), self.wide(1.0, -40)),
                "build": (self.wide(0.95, -66), self.wide(0.85, -56)),
                "zoom": (self.wide(0.85, -56), close(1.0)),
                "failure": (close(1.0), close(1.2)),
                "aftermath": (close(3.0), self.wide(1.0, -58)),
                "failure_preview": (self.close(1.4), self.close(1.05))}[name]


def main() -> None:
    job = json.loads(Path(sys.argv[sys.argv.index("--") + 1]).read_text(encoding="utf-8"))
    plan, scenes, fps = job["plan"], job["scenes"], job.get("fps", 30)
    beats = plan["beats"]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    look.setup(scene, fps)
    b = templates.build(plan["structure"])
    floor = parts.valley if plan["structure"]["setting"] == "valley" else parts.water
    floor(0.0, b.length * 8 + 400, b.col)

    cam = bpy.data.objects.new("camera", bpy.data.cameras.new("camera"))
    scene.collection.objects.link(cam)
    scene.camera = cam
    cam.data.lens, cam.data.clip_end = 28, b.length * 40 + 2000
    target = bpy.data.objects.new("camera_target", None)
    scene.collection.objects.link(target)
    con = cam.constraints.new("TRACK_TO")
    con.target, con.track_axis, con.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"

    templates.dress(b, plan)
    focus, exact = templates.focus_object(b, plan["focus"])
    shots = Shots(b, focus, plan["focus"]["at"]["chord"])
    side_y = -1 if plan["focus"]["at"]["side"] == "left" else 1
    red = bpy.data.objects.new(f"{focus.name}_red", focus.data)  # the highlighted part, drawn over the steel one
    b.col.objects.link(red)
    red.material_slots[0].link = "OBJECT"
    red.material_slots[0].material = look.material("red")
    red.location, red.rotation_mode = focus.location.copy(), focus.rotation_mode
    red.rotation_euler, red.rotation_quaternion = focus.rotation_euler.copy(), focus.rotation_quaternion.copy()
    red.scale = focus.scale * 1.04
    fasteners = parts.fastener(plan["structure"]["fastener"], focus.name, focus, side_y, b.col)
    details = [red] + fasteners
    if plan["focus"].get("label") and exact:  # never the AI's name on a stand-in part
        at = shots.focus + Vector((0, side_y * shots.near * 0.1, shots.near * 0.3))  # centred above the part
        label = parts.label(plan["focus"]["label"], shots.focus, at, shots.near * 0.045, cam)
        details += label

    total = scenes[-1]["last"]
    scene.frame_start, scene.frame_end = 1, total
    preview_end = scenes[0]["last"] if beats[0] == "failure_preview" else 0
    story = preview_end + 1
    fail = failures.Failure(b, plan, focus, red, fasteners)
    fail.ride_along([o for o in details if o not in [red] + fasteners])  # the label falls with its part
    if fail.falls():
        shots.fallen = fail.fallen(shots.focus)
    if preview_end:  # the hook shows the failure on the finished bridge, then the story starts over
        hook_peak = min(scenes[0]["peak_frame"], preview_end - 4, 1 + fps * 3 // 2)  # it must move in the first 1.5 s
        fail.play(1, hook_peak, until=preview_end, collapse=False)  # the hook keeps the part in view
        fail.reset(story)
    build_frames = [f for sc, beat in zip(scenes, beats) if beat == "build" for f in range(sc["first"], sc["last"] + 1)]
    for o in b.stages["piers"]:  # the site: piers stand before the steel arrives
        keyvis(o, 1, True)
    order = b.stages["deck"] + b.stages["members"] + b.stages["details"]
    drop = Vector((0, 0, b.H * 1.5 + 12))
    first_build = build_frames[0] if build_frames else None
    for k, o in enumerate(order):  # the bridge stands finished until the build scenes go back to an empty site
        home = o.location.copy()
        keyvis(o, 1, True)
        if first_build:
            appear = build_frames[k * len(build_frames) // len(order)]
            keyloc(o, first_build - 1, home)
            keyvis(o, first_build, appear == first_build)
            keyloc(o, appear, home + drop)
            keyvis(o, appear, True)
            keyloc(o, appear + DROP_FRAMES, home)
    zoom = next((sc for sc, beat in zip(scenes, beats) if beat == "zoom"), None)
    shown = zoom["first"] + (zoom["last"] - zoom["first"]) * 2 // 5 if zoom else story
    for o in details:  # red part, fasteners and label: in the hook, then from partway into the zoom on
        keyvis(o, 1, bool(preview_end))
        keyvis(o, story, False)
        keyvis(o, shown, True)

    hit = next((sc for sc, beat in zip(scenes, beats) if beat == "failure"), None)
    if hit:
        fail.play(hit["first"], min(max(hit["peak_frame"], hit["first"]), hit["last"]))
    hit_index = beats.index("failure") if "failure" in beats else len(beats)
    for i, (sc, beat) in enumerate(zip(scenes, beats)):
        start, end = shots.beat(beat, after=i > hit_index)
        if i == 0 or sc["first"] == story:  # the story's first shot (a cut after the hook)
            keyloc(cam, sc["first"], start[0])
            keyloc(target, sc["first"], start[1])
        keyloc(cam, sc["last"], end[0])
        keyloc(target, sc["last"], end[1])

    out = Path(job["frames_dir"])
    out.mkdir(parents=True, exist_ok=True)
    (out / "objects.json").write_text(json.dumps({"focus": focus.name, "exact": exact,
                                                "objects": sorted(o.name for o in bpy.data.objects)}), encoding="utf-8")
    if job.get("only_frames"):
        for f in job["only_frames"]:
            scene.frame_set(f)
            scene.render.filepath = str(out / f"f_{f:04d}.png")
            bpy.ops.render.render(write_still=True)
    else:
        scene.render.filepath = str(out / "f_")
        bpy.ops.render.render(animation=True)


main()
