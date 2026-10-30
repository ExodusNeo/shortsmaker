"""Tests for the motion-graphic opener on `opener: animated` channels (2026-10-30): the graphic goes first, a weak
one gets review.OPENER_GRAPHIC_FIXES fixes, then scene 1 goes to the owner's AI clip hand-off, and a clip that comes
back plays instead of the graphic (short_render.use_opener). The AI is faked. No AI usage.
Run: .venv\\Scripts\\python.exe tests\\test_opener_graphic.py"""
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shortsmaker import picker, plan_rules, review, session, short_render  # noqa: E402


def fresh():
    return {"title": "x", "opener_graphic": "motion graphic: map journey: Newburyport -> Caribbean",
            "scenes": [{"narration": "He shipped bed warmers to the tropics.",
                        "full": {"type": "journey", "stops": [{"name": "Newburyport"}]}, "full_rescued": "motion-graphic opener"}]}


def test_weak_opener_graphic_fixes_then_handoff():
    """Owner, 2026-10-30: a weak motion-graphic opener is fixed OPENER_GRAPHIC_FIXES times (a new pick with the
    complaint) before scene 1 goes to the owner's clip hand-off; without the hand-off it stays a CHECK line."""
    picks, old_pick, old_veo = [], picker.opener_graphic, session.VEO_HANDOFF
    def fake_pick(short, weak=""):
        picks.append(weak)
        short["scenes"][0]["full"] = {"type": "journey", "stops": [{"name": f"stop {len(picks)}"}]}
        return f"motion graphic: map journey: stop {len(picks)}"
    picker.opener_graphic = fake_pick
    try:
        session.VEO_HANDOFF = True
        st = {"short": fresh()}
        sc = st["short"]["scenes"][0]
        fixes = {0: ("repaint", "the map is unreadable"), 3: ("repaint", "blur")}
        why = review.weak_opener_graphic(st["short"], fixes, ["FIRST SECOND: 4/10: nothing strange"])
        assert why == "the map is unreadable; 4/10: nothing strange" and list(fixes) == [3], (why, fixes)
        for _ in range(review.OPENER_GRAPHIC_FIXES):
            notes = review.fix_opener_graphic(st, Path("."), why)
            assert "replaced by map journey" in notes[0] and not sc.get("opener_clip"), notes
        assert len(picks) == review.OPENER_GRAPHIC_FIXES and "unreadable" in picks[0]
        notes = review.fix_opener_graphic(st, Path("."), why)
        assert sc["opener_clip"] and sc["animate"] and "hand-off" in notes[0], notes
        assert sc["full"]["stops"][0]["name"] == "stop 2"  # still plays if no clip comes back
        assert review.weak_opener_graphic(st["short"], {}, ["FIRST SECOND: 3/10: x"]) is None  # a clip took over
        assert review.weak_opener_graphic(fresh(), {}, []) is None  # passed
        session.VEO_HANDOFF = False
        st = {"short": {**fresh(), "opener_fixes": review.OPENER_GRAPHIC_FIXES}}
        assert review.weak_opener_graphic(st["short"], {}, ["FIRST SECOND: 3/10: x"]) is None  # nothing left to try
    finally:
        picker.opener_graphic, session.VEO_HANDOFF = old_pick, old_veo


def test_use_opener_ai_clip_replaces_graphic():
    """An AI clip of scene 1 came back (the owner's or LTX's): it plays instead of the motion graphic, and the
    Opening line says why; archival film on scene 1 does not count."""
    for name, maker in (("clip0_veo.mp4", "made by you"), ("clip0_soft.mp4", "made on this PC")):
        s = fresh()
        s["opener_graphic_failed"] = "the motion graphic still looked weak after 2 fixes: x"
        s["scenes"][0]["opener_clip"] = True
        sources = ["photo"]
        assert short_render.use_opener(s, {0: Path(name)}, sources) is None
        assert s["scenes"][0]["full"] is None and maker in sources[0], sources
        assert s["opening_note"] == f"AI clip of the strangest moment ({maker}) (the motion graphic still looked weak after 2 fixes: x)"
    s = fresh()
    s["scenes"][0]["opener_clip"] = True
    short_render.use_opener(s, {0: Path("film0.mp4")}, ["x"])
    assert s["scenes"][0]["full"]["type"] == "journey" and s["opening_note"] == s["opener_graphic"]


def test_use_opener_without_graphic():
    """No graphic came back: scene 1 opens on its picture and a CHECK line says so; a channel without openers
    gets neither."""
    s = fresh()
    s["opener_graphic"], s["scenes"][0]["full"] = "no motion graphic (the AI gave none)", None
    assert short_render.use_opener(s, {}, ["x"]) == "opener: no motion graphic (the AI gave none)"
    assert s["opening_note"].endswith("; scene 1 opens on its picture")
    s = {"title": "x", "scenes": [{"full": None}]}
    assert short_render.use_opener(s, {}, ["x"]) is None and s["opening_note"] is None


def test_model_graphic_is_gone():
    """The three.js model graphic left with Blender (2026-10-30): a planned one is dropped."""
    assert plan_rules.clean_full({"type": "model", "find": "eiffel tower", "label": "SOLD"}, []) is None


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
