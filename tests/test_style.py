"""Tests for the style library: looks, overlays, transitions, inventions (plain asserts, no AI usage, no rendering).
Run: .venv\\Scripts\\python.exe tests\\test_style.py"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import make_shorts as m  # noqa: E402


def test_library_entries_have_fields():
    lib = m.style_library()
    assert lib, "library.json is empty"
    names = [e["name"] for e in lib]
    assert len(names) == len(set(names)), "duplicate names"
    for e in lib:
        assert set(e) >= {"name", "kind", "description", "fits", "file", "origin"}, e
        assert e["kind"] in ("look", "overlay", "transition"), e
        assert re.fullmatch(r"[a-z0-9-]+", e["name"]) and e["name"] != "invented", e
        assert (m.STYLE_DIR / e["file"]).exists(), e["file"]
    assert {"cut", "fade", "flash"} <= {e["name"] for e in m.style_library("transition")}


def test_write_style_index_is_deterministic():
    m.write_style_index()
    first = (m.STYLE_DIR / "index.ts").read_text(encoding="utf-8")
    m.write_style_index()
    assert (m.STYLE_DIR / "index.ts").read_text(encoding="utf-8") == first
    for e in m.style_library():
        stem = Path(e["file"]).with_suffix("").as_posix()
        assert f"'./{stem}'" in first, f"{e['file']} not imported"
    for slot in ("InventedLook", "InventedOverlay", "InventedTransition"):
        assert f"'./generated/{slot}'" in first, slot
    assert first.count("invented:") == 3


SAID = m.words_of("The army sent three soldiers with two machine guns, but why did the guns jam")


def test_clean_question_and_kinetic():
    q = m.clean_graphic({"style": "question", "text": "Why did the guns jam?"}, SAID)
    assert q and q["style"] == "question" and q["text"] == "WHY DID THE GUNS JAM?"
    assert m.clean_graphic({"style": "question", "text": "The guns jammed"}, SAID) is None  # not a question
    assert m.clean_graphic({"style": "question", "text": "Why did all of the big guns jam?"}, SAID) is None  # > 6 words
    k = m.clean_graphic({"style": "kinetic", "text": "three soldiers", "trigger": "three"}, SAID)
    assert k and k["text"] == "THREE SOLDIERS" and k["trigger"] == "three"
    assert m.clean_graphic({"style": "kinetic", "text": "three tanks", "trigger": "three"}, SAID) is None  # not spoken
    assert m.clean_graphic({"style": "kinetic", "text": "three soldiers", "trigger": "tanks"}, SAID) is None  # trigger unspoken
    assert m.clean_graphic({"style": "kinetic", "text": "army sent three soldiers with"}, SAID) is None  # > 4 words
    assert m.clean_graphic({"style": "kinetic", "text": "machinegunsjammed", "trigger": "army"}, SAID) is None  # unspoken
    inv = m.clean_graphic({"style": "invented", "text": "Two machine guns"}, SAID)
    assert inv and inv["style"] == "invented"
    for style in ("question", "kinetic", "invented"):
        assert style in m.PLANNED_STYLES and style in m.REMOTION_ONLY and style in m.GRAPHIC_STYLES


def test_unknown_names_fall_back():
    assert m.clean_transition("dissolve") == "fade" and m.clean_transition(None) == "fade" and m.clean_transition(3) == "fade"
    assert m.clean_transition("wipe") == "wipe" and m.clean_transition("invented") == "invented"
    assert m.clean_look({"name": "nope"}, {}) is None and m.clean_look("halftone", {}) is None and m.clean_look(None, {}) is None
    assert m.clean_look({"name": "engraving"}, {}) == {"name": "engraving"}


def test_recent_looks_blocked():
    ch = {"recent_looks": ["riso", "silent", "engraving"]}
    assert m.clean_look({"name": "engraving"}, ch) is None and m.clean_look({"name": "silent"}, ch) is None
    assert m.clean_look({"name": "riso"}, ch) == {"name": "riso"}  # only the last 2 are blocked


def test_invented_look_needs_fallback():
    spec = {"title": "Telegraph tape", "brief": "the photo printed as dots and dashes on a paper tape"}
    assert m.clean_look({"invent": spec}, {}) is None  # no fallback
    assert m.clean_look({"invent": {**spec, "fallback": "nope"}}, {}) is None
    got = m.clean_look({"invent": {**spec, "fallback": "halftone"}}, {})
    assert got == {"name": "invented", "title": "Telegraph tape", "brief": spec["brief"], "fallback": "halftone"}


def test_limit_style_caps():
    def scene(style=None, transition="fade"):
        return {"graphic": {"style": style, "text": "X?"} if style else None, "transition": transition}
    scs = [scene()] + [scene("question") for _ in range(2)] + [scene("kinetic") for _ in range(3)] \
        + [scene("invented") for _ in range(3)] + [scene(transition="wipe") for _ in range(4)]
    m.limit_style(scs)
    styles = [sc["graphic"]["style"] for sc in scs if sc["graphic"]]
    assert styles.count("question") == 1 and styles.count("kinetic") == 2 and styles.count("invented") == 2
    assert [sc["transition"] for sc in scs].count("wipe") == 3 and scs[-1]["transition"] == "fade"
    first = [{"graphic": {"style": "question", "text": "WHY?"}, "transition": "wipe"}, scene()]
    m.limit_style(first)
    assert first[0]["graphic"] is None  # the hook keeps only its title


LINES = ["Australia's army once lost a war to birds.", "Twenty thousand emus flooded the wheat farms.",
         "The army sent three soldiers with two machine guns.", "But why did the guns keep jamming?",
         "The emus scattered and outran the trucks.", "The soldiers pulled out within a month."]


def plan_with(director_reply: dict) -> tuple[dict, str]:
    """write_scripts with every AI/network step faked; the director answers `director_reply`. Returns (short, prompt)."""
    seen = {}

    def ask(prompt, fatal=True, read_dir=None, brain=None):
        if "You choose stories" in prompt:
            return {"shorts": [{"topic": "Emu War", "subject": "Emu War", "wiki_articles": ["Emu War"], "search_terms": []}]}
        if "You write YouTube Shorts narration" in prompt:
            return {"shorts": [{"index": 0, "title": "Emu War", "hook_text": "BIRDS WON", "scenes": LINES}]}
        if "You are the director" in prompt:
            seen["director"] = prompt
            return {"shorts": [{"index": 0, **director_reply}]}
        return {}

    names = ("ask_ai", "trend_research", "logbook_results", "article_text", "edit_scripts", "fact_check", "prepare_topic")
    saved = {k: getattr(m, k) for k in names}
    m.ask_ai, m.trend_research, m.logbook_results = ask, (lambda ch: []), (lambda: "")
    m.prepare_topic = lambda s, folder=None: (s.update(_texts={"A": "text"}, pool_dir="pool", catalog=[], picture_check="9 usable of 9"), True)[1]
    m.article_text, m.edit_scripts, m.fact_check = (lambda t: "text"), (lambda shorts, ch: None), (lambda s: True)
    try:
        return m.write_scripts({"niche": "history", "done_topics": [], "myths": [], "recent_looks": ["riso"]}, 1)[0], seen["director"]
    finally:
        for k, v in saved.items():
            setattr(m, k, v)


def test_director_prompt_lists_library():
    scenes = [{"image_search": "emu", "transition": t} for t in ("wipe", "whip", "invented", "cut", "fade", "leak")]
    scenes[3]["graphic"] = {"style": "question", "text": "Why did the guns keep jamming?"}
    scenes[2]["graphic"] = {"style": "invented", "text": "TWO GUNS"}
    short, prompt = plan_with({"look": {"name": "engraving"}, "scenes": scenes})
    for e in m.style_library():
        assert e["name"] in prompt, e["name"]
    assert "riso" in prompt  # the recent look is named so the director avoids it
    assert short["look"] == {"name": "engraving"}
    # no invented_transition / invented_overlay spec: an "invented" cut becomes a fade, an invented overlay is dropped
    assert [sc["transition"] for sc in short["scenes"]] == ["fade", "whip", "fade", "cut", "fade", "leak"]
    assert short["scenes"][2]["graphic"] is None and short["scenes"][3]["graphic"]["style"] == "question"


def test_director_inventions_are_kept_with_a_spec():
    spec = {"title": "Morse tape", "brief": "a paper tape of dots and dashes runs across the cut", "fallback": "wipe"}
    scenes = [{"image_search": "emu"}, {"image_search": "emu", "transition": "invented"}]
    short, _ = plan_with({"look": {"name": "riso"}, "invented_transition": spec, "scenes": scenes})
    assert short["look"] is None  # riso is one of the channel's last 2 looks
    assert short["invented_transition"] == {"title": "Morse tape", "brief": spec["brief"], "fallback": "wipe"}
    assert short["scenes"][1]["transition"] == "invented"


def test_apply_look_scenes():
    short = {"look": {"name": "silent"}, "scenes": [{} for _ in range(8)]}
    short["scenes"][3]["full"] = {"type": "number"}
    choices = [{"bg": object()} for _ in range(8)]
    choices[2]["film"] = {"path": "x.mp4"}
    short["scenes"][5]["animate"] = True  # an AI motion clip: Short.tsx draws no look on clips
    m.apply_look_scenes(short, choices, [1, 2, 3, 4, 5, 6, 7, 8, "x", 99])
    looked = [i for i, sc in enumerate(short["scenes"]) if sc.get("look")]
    assert looked == [1, 4, 6, 7]  # scene 1, the film and AI-clip scenes, the motion-graphic scene and anything past 4 are refused
    assert all(short["scenes"][i]["look"] == "silent" and short["scenes"][i]["look_seed"] == i for i in looked)
    m.apply_look_scenes({"look": None, "scenes": short["scenes"]}, choices, [2])
    assert not any(sc.get("look") for sc in short["scenes"])  # no look: every scene plain again


def test_remotion_forced_by_look():
    plain = {"graphic": None, "full": None, "transition": "fade"}
    assert not m.wants_remotion([plain, {**plain, "transition": "flash"}], 0)
    assert m.wants_remotion([plain, {**plain, "look": "riso"}], 0)
    assert m.wants_remotion([plain, {**plain, "transition": "wipe"}], 0)
    assert m.wants_remotion([plain, {**plain, "transition": "cut"}], 0)
    assert m.wants_remotion([plain], m.REMOTION_MIN_GRAPHICS)


def test_style_sounds():
    def sc(transition="fade", graphic=None):
        return {"transition": transition, "graphic": graphic, "sound": None, "full": None}
    short = {"scenes": [sc(), sc("whip"), sc("wipe"), sc("cut", {"style": "question", "text": "WHY?"}),
                        sc("leak", {"style": "kinetic", "text": "THREE SOLDIERS"})]}
    bounds = [0, 3, 6, 9, 12, 15]
    cues = [{}, {}, {}, {"graphic": 9.3}, {"graphic": 12.3}]
    ev = m.sfx_events(short, cues, bounds, True)
    whip = [e for e in ev if 2.5 < e["t"] < 3.1]
    assert len(whip) == 1 and whip[0]["sound"].startswith("whoosh") and whip[0]["gain"] == 0.2, whip
    assert not [e for e in ev if 5.5 < e["t"] < 6.2], "wipe should be silent"
    assert [e for e in ev if e["t"] == 9.3 and e["sound"] == "ticks" and e["gain"] == 0.25], ev
    assert [e for e in ev if e["t"] == 12.3 and e["sound"] == "ticks" and e["gain"] == 0.3], ev
    assert not [e for e in ev if 11.5 < e["t"] < 12.2], "leak should be silent"


def test_fact_check_sees_new_graphics():
    s = {"title": "Emu War", "wiki_articles": [], "_texts": {"Emu War": "text"},
         "scenes": [{"narration": "Birds won."}, {"narration": "Three soldiers went.",
                    "graphic": {"style": "kinetic", "text": "THREE SOLDIERS", "trigger": "three"}}]}
    seen = {}

    def ask(prompt, fatal=True, read_dir=None, brain=None):
        seen["p"] = prompt
        return {"fixes": [{"scene": 2, "drop_graphic": True, "why": "it was two soldiers"}]}

    saved, m.ask_ai = m.ask_ai, ask
    try:
        m.fact_check(s)
    finally:
        m.ask_ai = saved
    assert "THREE SOLDIERS" in seen["p"]
    assert s["scenes"][1]["graphic"] is None  # dropped even though the spoken line wasn't rewritten
    assert s["scenes"][1]["narration"] == "Three soldiers went."


def test_old_state_renders_plain():
    assert m.style_props({"transition": "fade"}, 3) == {"transition": "fade", "look": None, "lookSeed": 3}
    assert m.style_props({"transition": "flash", "look": "silent", "look_seed": 5}, 1) == \
        {"transition": "flash", "look": "silent", "lookSeed": 5}


GOOD_TRANSITION = """import {clamp01} from '../kit';
import type {Transition} from '../types';

export const InventedTransition: Transition = {duration: 0.4, render: (p) => ({to: {opacity: clamp01(p * 2 - 0.5)}})};
"""
SPEC = {"title": "Morse tape", "brief": "a paper tape of dots and dashes wipes across the cut", "fallback": "wipe"}
SCENE = {"image": "job/1.jpg", "start": 3.0, "end": 6.0, "transition": "invented", "graphic": None}


def with_fakes(codes: list, tsc=None, fn=None):
    """Runs fn() with ask_ai answering `codes` in turn, tsc_check returning `tsc`, and no preview render."""
    replies = iter(codes)
    saved = {k: getattr(m, k) for k in ("ask_ai", "tsc_check", "preview_sheet")}
    m.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None: {"code": next(replies, None)}
    m.tsc_check, m.preview_sheet = (lambda: tsc), (lambda *a, **k: None)
    try:
        return fn()
    finally:
        for k, v in saved.items():
            setattr(m, k, v)
        m.restore_style_slots()


def test_placeholders_match_the_slots():
    for slot, code in m.style_placeholders().items():
        assert (m.STYLE_DIR / "generated" / f"{slot}.tsx").read_text(encoding="utf-8") == code, slot
        kind = next(k for k, s in m.STYLE_SLOTS.items() if s == slot)
        assert not m.lint_style_code(code, kind), f"{slot} placeholder is not a valid {kind}: {m.lint_style_code(code, kind)}"


def test_invention_passes_into_slot():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        work = Path(d)
        slot_file = m.STYLE_DIR / "generated" / "InventedTransition.tsx"
        seen = {}

        def run():
            name = m.invent_component("transition", SPEC, {"title": "Emu War"}, SCENE, {"scenes": [SCENE]}, work)
            seen["slot"] = slot_file.read_text(encoding="utf-8")
            return name
        assert with_fakes([GOOD_TRANSITION], fn=run) == "invented"
        assert "export const InventedTransition" in seen["slot"]
        cache = (work / "InventedTransition.tsx").read_text(encoding="utf-8")
        assert cache.startswith("// InventedTransition: Morse tape | ") and cache == seen["slot"]
        # a re-render (fix.bat) reuses the cached invention without asking the AI again
        assert with_fakes([], fn=lambda: m.invent_component("transition", SPEC, {"title": "Emu War"}, SCENE,
                                                             {"scenes": [SCENE]}, work)) == "invented"
    assert slot_file.read_text(encoding="utf-8") == m.style_placeholders()["InventedTransition"]


def test_invention_lint_failure_uses_fallback():
    import tempfile
    bad = "import fs from 'fs';\n" + GOOD_TRANSITION
    with tempfile.TemporaryDirectory() as d:
        name = with_fakes([bad, bad], fn=lambda: m.invent_component("transition", SPEC, {"title": "E"}, SCENE,
                                                                     {"scenes": [SCENE]}, Path(d)))
        assert name == "wipe" and not (Path(d) / "InventedTransition.tsx").exists()
    assert m.lint_style_code(bad, "transition")
    assert m.lint_style_code(GOOD_TRANSITION.replace("Transition =", "Transition = (setTimeout(() => 0, 1), "), "transition")
    assert not m.lint_style_code(GOOD_TRANSITION, "transition")
    assert m.lint_style_code(GOOD_TRANSITION, "look")  # wrong export for a look


def test_invention_compile_failure_uses_fallback():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        name = with_fakes([GOOD_TRANSITION, GOOD_TRANSITION], tsc="error TS2322",
                          fn=lambda: m.invent_component("transition", SPEC, {"title": "E"}, SCENE, {"scenes": [SCENE]}, Path(d)))
        assert name == "wipe"


def test_invention_runtime_failure_uses_fallback():
    calls = []

    def render(props):
        calls.append(json.loads(json.dumps(props)))
        if any(sc.get("transition") == "invented" for sc in props["scenes"]):
            raise RuntimeError("the invented transition crashed the browser")
    props = {"scenes": [dict(SCENE), {**SCENE, "transition": "cut"}]}
    survived = m.run_remotion_with_fallback(render, props, {"transition": SPEC})
    assert survived == {} and len(calls) == 2 and calls[1]["scenes"][0]["transition"] == "wipe"
    ok_calls = []
    assert m.run_remotion_with_fallback(ok_calls.append, {"scenes": []}, {"look": SPEC}) == {"look": SPEC}
    try:
        m.run_remotion_with_fallback(lambda p: (_ for _ in ()).throw(RuntimeError("x")), {"scenes": []}, {})
        raise AssertionError("a render failure without inventions must still raise")
    except RuntimeError:
        pass


LOOK_MARK = "// the look invented a moment ago\n"


def test_failed_invention_keeps_the_others():
    import tempfile
    look_slot = m.STYLE_DIR / "generated" / "InventedLook.tsx"
    seen = {}

    def run():
        look_slot.write_text(LOOK_MARK, encoding="utf-8")
        with tempfile.TemporaryDirectory() as d:
            seen["name"] = m.invent_component("transition", SPEC, {"title": "E"}, SCENE, {"scenes": [SCENE]}, Path(d))
        seen["look"] = look_slot.read_text(encoding="utf-8")
        seen["transition"] = (m.STYLE_DIR / "generated" / "InventedTransition.tsx").read_text(encoding="utf-8")
    with_fakes([GOOD_TRANSITION, GOOD_TRANSITION], tsc="error TS2322", fn=run)
    assert seen["name"] == "wipe"
    assert seen["look"] == LOOK_MARK  # only the failed slot is emptied
    assert seen["transition"] == m.style_placeholders()["InventedTransition"]


def test_good_look_check_skips_the_extra_compile():
    import tempfile
    replies = iter([{"code": GOOD_TRANSITION}, {"ok": True}])
    calls = []
    saved = {k: getattr(m, k) for k in ("ask_ai", "tsc_check", "preview_sheet")}
    with tempfile.TemporaryDirectory() as d:
        sheet = Path(d) / "sheet.jpg"
        m.ask_ai = lambda *a, **k: next(replies)
        m.tsc_check, m.preview_sheet = (lambda: calls.append(1)), (lambda *a, **k: sheet)
        try:
            assert m.invent_component("transition", SPEC, {"title": "E"}, SCENE, {"scenes": [SCENE]}, Path(d)) == "invented"
        finally:
            for k, v in saved.items():
                setattr(m, k, v)
            m.restore_style_slots()
    assert len(calls) == 1  # the art director said ok: no second compile of the same code


def test_swap_inventions():
    props = {"scenes": [{"look": "invented", "transition": "invented", "graphic": {"style": "invented", "text": "X"}},
                        {"look": "silent", "transition": "cut", "graphic": None}]}
    m.swap_inventions(props, {"look": {"fallback": "engraving"}, "transition": {"fallback": "leak"},
                              "overlay": {"fallback": "kinetic"}})
    assert props["scenes"][0] == {"look": "engraving", "transition": "leak", "graphic": {"style": "kinetic", "text": "X"}}
    assert props["scenes"][1]["look"] == "silent"


def test_slots_restored_after_render():
    slot = m.STYLE_DIR / "generated" / "InventedLook.tsx"
    original = slot.read_text(encoding="utf-8")
    try:
        slot.write_text("// junk\n", encoding="utf-8")
        m.restore_style_slots()
        assert slot.read_text(encoding="utf-8") == m.style_placeholders()["InventedLook"]
    finally:  # never leave junk behind, even when this test fails (it once corrupted placeholders.json)
        slot.write_text(original, encoding="utf-8", newline="\n")
    assert "restore_style_slots()" in Path(m.__file__).read_text(encoding="utf-8").split("def render_remotion")[1].split("\ndef ")[0]


def library_snapshot():
    """The library files a candidate test may touch, to put back afterwards."""
    files = [m.STYLE_LIBRARY, m.STYLE_DIR / "index.ts"]
    return {f: f.read_bytes() for f in files}


def restore_library(snap):
    for f, data in snap.items():
        f.write_bytes(data)


def test_save_candidate_unique_slug():
    import tempfile
    saved = m.CANDIDATES
    with tempfile.TemporaryDirectory() as d:
        m.CANDIDATES = Path(d)
        try:
            code = "// InventedTransition: Morse tape | x\n" + GOOD_TRANSITION
            a = m.save_candidate("transition", "Morse tape!", "dots and dashes", "telegraph stories", code, None, "Emu War")
            b = m.save_candidate("transition", "Morse tape!", "dots and dashes", "telegraph stories", code, None, "Emu War")
            assert (a.name, b.name) == ("transition-morse-tape", "transition-morse-tape-2")
            comp = (a / "Component.tsx").read_text(encoding="utf-8")
            assert "export const MorseTape: Transition" in comp and "InventedTransition" not in comp
            meta = json.loads((a / "meta.json").read_text(encoding="utf-8"))
            assert meta["name"] == "morse-tape" and meta["kind"] == "transition" and meta["from_short"] == "Emu War"
            assert meta["description"] == "dots and dashes" and meta["fits"] == "telegraph stories"
            assert json.loads((b / "meta.json").read_text(encoding="utf-8"))["name"] == "morse-tape-2"
        finally:
            m.CANDIDATES = saved
    assert not str(m.CANDIDATES).startswith(str(m.REMOTION / "src"))  # tsc must never see a candidate


def candidate_in(d: Path) -> Path:
    m.CANDIDATES = d
    return m.save_candidate("transition", "Morse tape", "dots and dashes", "telegraph stories",
                            "// InventedTransition: Morse tape | x\n" + GOOD_TRANSITION, None, "Emu War")


def test_approve_adds_to_library():
    import tempfile
    snap, saved, saved_tsc = library_snapshot(), m.CANDIDATES, m.tsc_check
    dest = m.STYLE_DIR / "transitions" / "MorseTape.tsx"
    with tempfile.TemporaryDirectory() as d:
        try:
            folder = candidate_in(Path(d))
            m.tsc_check = lambda: None
            assert m.approve_candidate(folder) is True
            assert dest.exists() and not folder.exists()
            entry = next(e for e in m.style_library() if e["name"] == "morse-tape")
            assert entry == {"name": "morse-tape", "kind": "transition", "description": "dots and dashes",
                             "fits": "telegraph stories", "file": "transitions/MorseTape.tsx", "origin": "approved"}
            assert "import {MorseTape} from './transitions/MorseTape';" in (m.STYLE_DIR / "index.ts").read_text(encoding="utf-8")
        finally:
            m.CANDIDATES, m.tsc_check = saved, saved_tsc
            dest.unlink(missing_ok=True)
            restore_library(snap)


def test_approve_rolls_back_on_tsc_failure():
    import tempfile
    snap, saved, saved_tsc = library_snapshot(), m.CANDIDATES, m.tsc_check
    with tempfile.TemporaryDirectory() as d:
        try:
            folder = candidate_in(Path(d))
            m.tsc_check = lambda: "error TS2304: Cannot find name"
            assert m.approve_candidate(folder) is False
            assert library_snapshot() == snap  # library.json and index.ts byte-identical
            assert not (m.STYLE_DIR / "transitions" / "MorseTape.tsx").exists() and folder.exists()
        finally:
            m.CANDIDATES, m.tsc_check = saved, saved_tsc
            (m.STYLE_DIR / "transitions" / "MorseTape.tsx").unlink(missing_ok=True)
            restore_library(snap)


def test_approve_rolls_back_when_the_check_crashes():
    import subprocess
    import tempfile
    snap, saved, saved_tsc = library_snapshot(), m.CANDIDATES, m.tsc_check
    with tempfile.TemporaryDirectory() as d:
        try:
            folder = candidate_in(Path(d))

            def timeout():
                raise subprocess.TimeoutExpired("tsc", 120)
            m.tsc_check = timeout
            assert m.approve_candidate(folder) is False
            assert library_snapshot() == snap
            assert not (m.STYLE_DIR / "transitions" / "MorseTape.tsx").exists() and folder.exists()
        finally:
            m.CANDIDATES, m.tsc_check = saved, saved_tsc
            (m.STYLE_DIR / "transitions" / "MorseTape.tsx").unlink(missing_ok=True)
            restore_library(snap)


def test_candidate_names_unique_across_kinds():
    import tempfile
    saved = m.CANDIDATES
    with tempfile.TemporaryDirectory() as d:
        try:
            a = candidate_in(Path(d))
            b = m.save_candidate("look", "Morse tape", "dots", "telegraph stories",
                                 "// InventedLook: Morse tape | x\n" + m.style_placeholders()["InventedLook"], None, "Emu War")
            assert a.name == "transition-morse-tape" and b.name == "look-morse-tape-2"  # index.ts imports by name
        finally:
            m.CANDIDATES = saved


def test_reject_deletes():
    import tempfile
    saved = m.CANDIDATES
    with tempfile.TemporaryDirectory() as d:
        try:
            folder = candidate_in(Path(d))
            m.reject_candidate(folder)
            assert not folder.exists()
        finally:
            m.CANDIDATES = saved


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print("PASS", t.__name__)
        except Exception as e:  # report every test, not just the first failure
            failed += 1
            print("FAIL", t.__name__, type(e).__name__, e)
    print(f"{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
