"""Tests for Blender build plans (blender_plan.py, 2026-10-22): the engineer AI's plan is checked field by field,
asked for again once, and replaced by a generic plan when still unusable. No AI usage, no Blender.
Run: .venv\\Scripts\\python.exe tests\\test_blender_plan.py"""
import json
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import blender_plan, llm, session  # noqa: E402

EXAMPLE = {"structure": {"template": "truss_bridge", "truss": "warren", "spans": 3, "span_m": 140, "height_m": 18,
                         "width_m": 20, "deck": "road", "setting": "river", "fastener": "rivet"},
           "focus": {"part": "gusset_plate", "at": {"span": 2, "panel": 3, "chord": "bottom", "side": "left"},
                     "label": "GUSSET PLATE U10 · 1/2 INCH"},
           "failure": {"kind": "bend", "then": "collapse_span", "span": 2},
           "scale": ["car", "people"],
           "scenes": [{"scene": 1, "beat": "failure_preview"}, {"scene": 2, "beat": "wide"},
                      {"scene": 3, "beat": "build"}, {"scene": 4, "beat": "build"}, {"scene": 5, "beat": "zoom"},
                      {"scene": 9, "beat": "failure"}, {"scene": 10, "beat": "aftermath"}]}


def plan(**over):
    p = json.loads(json.dumps(EXAMPLE))
    for k, v in over.items():
        p[k] = v
    return p


def test_clean_build_keeps_a_good_plan():
    b = blender_plan.clean_build(plan(), 11)
    assert b["structure"]["template"] == "truss_bridge" and b["structure"]["spans"] == 3
    assert b["focus"]["at"] == {"span": 2, "panel": 3, "chord": "bottom", "side": "left"}
    assert b["failure"] == {"kind": "bend", "then": "collapse_span", "span": 2}
    assert b["scale"] == ["car", "people"]
    assert len(b["beats"]) == 11 and b["beats"][0] == "failure_preview" and b["beats"][8] == "failure"
    assert b["beats"][5:8] == ["zoom", "zoom", "zoom"] and b["beats"][10] == "aftermath"


def test_bad_values_get_defaults():
    s = dict(EXAMPLE["structure"], template="dam", span_m=99999, fastener="screw", truss="banana", spans="lots")
    b = blender_plan.clean_build(plan(structure=s, failure={"kind": "melt", "then": "explode"}), 6)
    assert b["structure"]["template"] == "truss_bridge" and b["structure"]["span_m"] == 1300
    assert b["structure"]["fastener"] == "rivet" and b["structure"]["truss"] == "warren" and b["structure"]["spans"] == 1
    assert b["failure"]["kind"] == "bend" and b["failure"]["then"] == "none"
    assert b["focus"]["at"]["span"] <= b["structure"]["spans"]  # clamped to the real bridge


def test_unlisted_and_bad_scenes_copy_the_previous_beat():
    scenes = [{"scene": "2", "beat": "zoom"}, {"scene": 40, "beat": "wide"}, {"scene": 3, "beat": "dance"},
              {"scene": 4, "beat": "zoom"}, "x", {"scene": 5, "beat": "failure"}]
    b = blender_plan.clean_build(plan(scenes=scenes), 6)
    assert b["beats"] == ["failure_preview", "failure_preview", "failure_preview", "zoom", "failure", "failure"], b["beats"]


def test_zoom_and_failure_are_guaranteed():
    for n in (3, 18):
        b = blender_plan.clean_build(plan(scenes=[{"scene": k + 1, "beat": "build"} for k in range(n)]), n)
        assert len(b["beats"]) == n and "zoom" in b["beats"] and "failure" in b["beats"], b["beats"]
        assert b["beats"].index("zoom") < b["beats"].index("failure")


def test_unusable_plan_is_none():
    for raw in ("x", {}, {"structure": "truss"}, None):
        assert blender_plan.clean_build(raw, 5) is None, raw


def test_label_is_short_and_upper():
    b = blender_plan.clean_build(plan(focus={"part": "chord", "label": "a very long label " * 4}), 5)
    assert len(b["focus"]["label"]) <= 40 and b["focus"]["label"] == b["focus"]["label"].upper()
    assert blender_plan.clean_build(plan(focus={"part": "chord", "label": 7}), 5)["focus"]["label"] is None
    assert blender_plan.clean_build(plan(focus={"part": "rocket"}), 5)["focus"]["part"] == "gusset_plate"


def test_default_build_shape():
    for n in (3, 12, 18):
        d = blender_plan.default_build(n)
        assert d["generic"] is True and len(d["beats"]) == n and "zoom" in d["beats"] and "failure" in d["beats"]
        assert d["beats"][0] == "failure_preview"
        again = blender_plan.clean_build({**d, "scenes": [{"scene": k + 1, "beat": x} for k, x in enumerate(d["beats"])]}, n)
        assert {k: v for k, v in d.items() if k != "generic"} == again


def test_plan_builds_retries_then_defaults():
    calls = []

    def ask(prompt, fatal=True, read_dir=None, brain=None, bulk=False):
        calls.append(prompt)
        return {"shorts": [{"index": 0, **plan()}, {"index": 1, "structure": "nope"}]} if len(calls) == 1 \
            else {"shorts": [{"index": 1, "garbage": True}]}

    shorts = [{"title": f"T{k}", "research": {"A": "text"},
               "scenes": [{"narration": f"line {j}", "full": {"type": "number"}, "graphic": {"style": "x"},
                           "person": {"name": "A B"}, "transition": "wipe"} for j in range(11)],
               "look": {"name": "sepia"}, "invented_transition": {"title": "x"}, "invented_overlay": None} for k in range(2)]
    old, session.RULES = llm.ask_ai, {"Build plan": "plan bridges well"}
    llm.ask_ai = ask
    try:
        blender_plan.plan_builds(shorts, {"niche": "engineering"})
    finally:
        llm.ask_ai = old
    assert len(calls) == 2 and "plan bridges well" in calls[0] and "T1" in calls[1] and "T0" not in calls[1]
    assert shorts[0]["build"]["failure"]["kind"] == "bend" and shorts[0]["build_check"] is None
    assert shorts[1]["build"]["generic"] is True and "generic" in shorts[1]["build_check"]
    assert all(sc["full"] is None and sc["graphic"] is None and sc["person"] is None and sc["transition"] == "fade"
               for s in shorts for sc in s["scenes"])
    assert all(s["look"] is None and s["invented_transition"] is None for s in shorts)  # keeps it on the Python renderer


def test_hard_cuts_never_blend_scenes():
    from shortsmaker import frame_render
    from shortsmaker.config import FPS

    class Out:
        frames = []

        def write(self, b):
            self.frames.append(b)

    def frame(i, t):
        return frame_render.Image.new("RGB", (frame_render.W, frame_render.H), (0, 0, 0) if i == 0 else (255, 255, 255))

    out, bounds = Out(), [0.0, 0.5, 1.0]
    frame_render.write_frames(frame, 2, bounds, 1.0, out, set(), {0.5})
    assert len(out.frames) == FPS and {f[0] for f in out.frames} == {0, 255}  # black, then white: no grey blend


def test_nan_and_infinity_get_defaults():
    s = dict(EXAMPLE["structure"], span_m=float("nan"), height_m=float("inf"), spans=float("-inf"))
    b = blender_plan.clean_build(plan(structure=s), 5)
    assert b["structure"]["span_m"] == 100 and b["structure"]["height_m"] == 15 and b["structure"]["spans"] == 1


def test_a_failure_in_scene_one_becomes_the_hook():
    b = blender_plan.clean_build(plan(scenes=[{"scene": 1, "beat": "failure"}, {"scene": 2, "beat": "wide"},
                                              {"scene": 3, "beat": "zoom"}, {"scene": 4, "beat": "failure"}]), 4)
    assert b["beats"][0] == "failure_preview", b["beats"]


def test_thumbnail_order_skips_film_and_puts_openers_first():
    usable = {"era_ok": True, "sharp": 2, "reject": None}
    cat = [{"n": 1, "hook": False, **usable}, {"n": 2, "hook": True, **usable}, {"n": 3, "hook": True, **usable}]
    rows = [{"url": "a.jpg"}, {"url": "film.webm#t=3", "film": {"src": "film.webm", "t": 3}}, {"url": "c.jpg"}]
    assert blender_plan.thumbnail_order({"catalog": cat}, rows) == [2, 0]

def test_tiny_shorts_get_one_beat_per_scene():
    for n in (1, 2):
        b = blender_plan.clean_build(plan(scenes=[]), n)
        assert len(b["beats"]) == n, b["beats"]


if __name__ == "__main__":
    names = [n for n in sorted(globals()) if n.startswith("test_") and (len(sys.argv) < 2 or n in sys.argv[1:])]
    failed = 0
    for n in names:
        try:
            globals()[n]()
            print(f"PASS {n}")
        except Exception:
            failed += 1
            print(f"FAIL {n}")
            traceback.print_exc()
    print(f"{len(names) - failed}/{len(names)} passed")
    sys.exit(1 if failed else 0)
