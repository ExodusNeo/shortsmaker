"""Tests for opener staging plans (opener_plan.py, 2026-10-27): the plan format and its tables, the batch call and
its one retry. The AI is faked. No AI usage. Run: .venv\\Scripts\\python.exe tests\\test_opener_plan.py"""
import copy
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shortsmaker import llm, opener_plan  # noqa: E402

EXAMPLE = {  # the spec's example plan
    "buildable": True,
    "moment": "an axe chops a rooster's head off on a stump; the headless body hops off and staggers away",
    "set": {"ground": "dirt", "backdrop": [{"find": "red barn", "size_m": 8}], "light": "day"},
    "actors": [
        {"id": "rooster", "find": "rooster", "size_m": 0.55, "on": "stump", "facing": "right"},
        {"id": "stump", "find": "tree stump", "size_m": 1.2},
        {"id": "axe", "find": "axe", "size_m": 0.8},
    ],
    "beats": [
        {"move": "cut", "tool": "axe", "target": "rooster", "at": 0.55,
         "strokes": [{"through": "neck", "angle": "level"}],
         "expect": [{"piece": "head", "share": 0.15, "then": "fly_off"}, {"piece": "rest", "then": "stay"}]},
        {"move": "hop_off", "actor": "rooster", "at": 1.3, "style": "stagger"},
        {"move": "walk", "actor": "rooster", "at": 1.8, "toward": "left", "style": "stagger"},
    ],
    "camera": {"angle": "three_quarter", "follow": "rooster"},
}


def plan(**changes):
    p = copy.deepcopy(EXAMPLE)
    for path, v in changes.items():
        node, keys = p, path.split(".")
        for k in keys[:-1]:
            node = node[int(k)] if k.isdigit() else node[k]
        last = keys[-1]
        node[int(last) if last.isdigit() else last] = v
    return p


def short(i=0):
    return {"title": f"Short {i}", "research": {"wiki": "text"},
            "scenes": [{"narration": "The axe fell."}, {"narration": "He walked away."}]}


def test_spec_example_is_clean():
    assert opener_plan.clean_opener(copy.deepcopy(EXAMPLE)) == EXAMPLE


def test_rejects_unknown_move_tool_and_id():
    assert opener_plan.clean_opener(plan(**{"beats.1.move": "explode"})) is None
    assert opener_plan.clean_opener(plan(**{"beats.0.tool": "laser"})) is None  # not an actor
    with_laser = plan(**{"beats.0.tool": "laser"})
    with_laser["actors"].append({"id": "laser", "find": "laser", "size_m": 0.3})
    assert opener_plan.clean_opener(with_laser) is None  # an actor, but not a tool in the table
    assert opener_plan.clean_opener(plan(**{"beats.2.actor": "dog"})) is None


def test_first_beat_by_one_second():
    p = plan(**{"beats.0.at": 1.2})
    assert opener_plan.clean_opener(p) is None
    assert opener_plan.clean_opener(plan(**{"beats.0.at": 1.0})) is not None


def test_sizes_bounded():
    assert opener_plan.clean_opener(plan(**{"actors.0.size_m": 0.01})) is None
    assert opener_plan.clean_opener(plan(**{"actors.0.size_m": 50})) is None
    assert opener_plan.clean_opener(plan(**{"set.backdrop.0.size_m": 31})) is None


def test_cut_needs_expect():
    p = plan()
    del p["beats"][0]["expect"]
    assert opener_plan.clean_opener(p) is None
    mince = plan(**{"beats.0.strokes": [{"mince": 50}], "beats.0.expect": [{"pieces": "40-60", "then": "scatter"}]})
    assert opener_plan.clean_opener(mince) is not None
    assert opener_plan.clean_opener(plan(**{"beats.0.expect": [{"pieces": "60-40", "then": "scatter"}]})) is None
    assert opener_plan.clean_opener(plan(**{"beats.0.expect.0.then": "explode"})) is None


def test_unbuildable():
    old = llm.ask_ai
    try:
        llm.ask_ai = lambda *a, **k: {"shorts": [{"index": 0, "buildable": False, "why": "people in uniforms"}]}
        s = short()
        opener_plan.plan_openers([s], {"niche": "history"})
        assert "opener" not in s and s["opener_check"] == "opener: not buildable (people in uniforms)", s
    finally:
        llm.ask_ai = old


def test_plan_retry_then_none():
    old, calls = llm.ask_ai, []
    try:
        llm.ask_ai = lambda *a, **k: calls.append(1) or {"shorts": [{"index": 0, "junk": True}]}
        s = short()
        opener_plan.plan_openers([s], {"niche": "history"})
        assert len(calls) == 2 and s["opener_check"] == "opener: no usable plan" and "opener" not in s
    finally:
        llm.ask_ai = old


def test_good_plan_is_kept():
    old = llm.ask_ai
    try:
        llm.ask_ai = lambda *a, **k: {"shorts": [{"index": 0, **copy.deepcopy(EXAMPLE)}]}
        s = short()
        opener_plan.plan_openers([s], {"niche": "history"})
        assert s["opener"] == EXAMPLE and s.get("opener_check") is None
    finally:
        llm.ask_ai = old


def test_fix_plan_returns_clean_or_none():
    old = llm.ask_ai
    try:
        llm.ask_ai = lambda *a, **k: copy.deepcopy(EXAMPLE)
        assert opener_plan.fix_plan({"opener": EXAMPLE, "title": "t"}, ["overlap: axe/rooster frames 21-23"]) == EXAMPLE
        llm.ask_ai = lambda *a, **k: None
        assert opener_plan.fix_plan({"opener": EXAMPLE, "title": "t"}, ["x"]) is None
    finally:
        llm.ask_ai = old


def test_rejects_on_cycles_and_self():
    assert opener_plan.clean_opener(plan(**{"actors.1.on": "stump"})) is None  # stands on itself
    assert opener_plan.clean_opener(plan(**{"actors.1.on": "rooster"})) is None  # rooster on stump on rooster
    assert opener_plan.clean_opener(plan(**{"actors.1.on": "ground"})) is not None


def test_through_cut_names_its_rest():
    assert opener_plan.clean_opener(plan(**{"beats.0.expect": [{"piece": "head", "share": 0.15, "then": "fly_off"}]})) is None


def test_only_buildable_cuts():
    assert "drill" not in opener_plan.TOOLS and "cookie cutter" not in opener_plan.TOOLS  # no boolean cuts yet
    two = plan(**{"beats.0.strokes": [{"through": "neck", "angle": "diagonal"}, {"rows": 3}]})
    assert opener_plan.clean_opener(two) is None  # one stroke group per cut


def test_fix_plan_gets_scene_length():
    old, prompts = llm.ask_ai, []
    try:
        llm.ask_ai = lambda prompt, **k: prompts.append(prompt) or copy.deepcopy(EXAMPLE)
        scaled = copy.deepcopy(EXAMPLE)
        scaled["beats"][2]["at"] = 1.7
        opener_plan.fix_plan({"opener": EXAMPLE, "title": "t"}, ["in_frame: x"], seconds=1.8, scaled=scaled)
        assert "1.8 seconds" in prompts[0] and '"at": 1.7' in prompts[0], prompts[0][:400]
    finally:
        llm.ask_ai = old


def test_prompt_explains_stroke_angles():
    text = opener_plan._tables_text()
    assert "diagonal" in text and "edge-on" in text and "flat side" in text, text  # the live run chose "down" blindly



PEOPLE = {  # the spec's people example: the umbrella officer walking across while shells burst behind him
    "buildable": True,
    "moment": "an officer strolls across a bridge with his umbrella while shells burst behind him",
    "set": {"ground": "stone", "backdrop": [], "light": "day"},
    "actors": [{"id": "officer", "person": "ww2_british_officer", "facing": "right", "prop": "umbrella"},
               {"id": "rubble", "find": "rocks", "size_m": 0.6}],
    "beats": [{"move": "walk", "actor": "officer", "at": 0.3, "toward": "left"},
              {"move": "scatter", "actor": "rubble", "at": 0.6}],
    "camera": {"angle": "side", "follow": "officer"},
}


def test_person_actor_is_clean():
    assert opener_plan.clean_opener(copy.deepcopy(PEOPLE)) is not None


def test_unknown_role_rejected():
    p = copy.deepcopy(PEOPLE)
    p["actors"][0]["person"] = "astronaut"
    assert opener_plan.clean_opener(p) is None


def test_people_move_on_animal_rejected():
    """People moves are for people, Part 1's for everything else."""
    assert opener_plan.clean_opener(plan(**{"beats.2.move": "die"})) is None  # the rooster can't "die" by clip
    p = copy.deepcopy(PEOPLE)
    p["beats"][0]["move"] = "hop_off"  # nor a person by a Part 1 move
    assert opener_plan.clean_opener(p) is None


def test_prompt_lists_people():
    text = opener_plan._tables_text()
    assert "ww2_british_officer" in text and "swing_prop" in text, text[:400]


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
