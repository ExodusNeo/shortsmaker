"""Tests for opener staging plans (opener_plan.py, 2026-10-27; shot templates 2026-10-28): the plan format and its
tables, template fills, the batch call and its one retry, model swaps. The AI is faked. No AI usage. Run: .venv\\Scripts\\python.exe tests\\test_opener_plan.py"""
import copy
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shortsmaker import llm, opener_plan  # noqa: E402
sys.path.insert(0, str(ROOT / "tests"))
from test_shot_templates import SAMPLES  # noqa: E402

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




def test_pick_up_needs_something_on_the_ground():
    """The Eiffel plan's pick_up named nothing to pick up: "take" is a person who dropped their prop earlier, or a
    thing of at most 1 m on the ground."""
    p = copy.deepcopy(PEOPLE)
    p["actors"] = [{"id": "dealer", "person": "worker", "facing": "right", "prop": "briefcase"},
                   {"id": "con", "person": "businessman", "facing": "left"},
                   {"id": "case", "find": "suitcase", "size_m": 0.6},
                   {"id": "car", "find": "car", "size_m": 4}]
    p["beats"] = [{"move": "drop_prop", "actor": "dealer", "at": 0.3},
                  {"move": "pick_up", "actor": "con", "at": 0.8, "take": "dealer"}]
    p["camera"] = {"angle": "side", "follow": "con"}
    assert opener_plan.clean_opener(copy.deepcopy(p))
    for take, at in ((None, 0.8), ("con", 0.8), ("car", 0.8), ("dealer", 0.2), ("nobody", 0.8)):
        q = copy.deepcopy(p)
        q["beats"][1].update(take=take, at=at)
        assert opener_plan.clean_opener(q) is None, (take, at)
    q = copy.deepcopy(p)
    q["beats"][1]["take"] = "case"
    assert opener_plan.clean_opener(q)







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





def test_toward_an_actor_is_clean():
    p = copy.deepcopy(PEOPLE)
    p["beats"][0]["toward"] = "rubble"
    assert opener_plan.clean_opener(p) is not None
    p["beats"][0]["toward"] = "officer"  # not toward itself
    assert opener_plan.clean_opener(p) is None





def test_vehicle_roll_rejected():
    """"roll" is the physics tumble for round things; the people run's car rolled and tipped onto its nose. A
    vehicle (gait wheeled) drives with "walk"."""
    p = copy.deepcopy(PEOPLE)
    p["actors"].append({"id": "car", "find": "truck", "size_m": 4, "gait": "wheeled"})
    p["beats"].append({"move": "roll", "actor": "car", "at": 0.5, "toward": "officer"})
    assert opener_plan.clean_opener(p) is None
    p["beats"][-1]["move"] = "walk"
    assert opener_plan.clean_opener(p) is not None


def test_every_sample_fill_is_clean():
    for name, reply in SAMPLES.items():
        plan = opener_plan.fill_template(copy.deepcopy(reply))
        assert plan and plan["template"] == reply["template"], name


def test_fill_rejects_values_outside_the_template():
    good = SAMPLES["falls_on_cheer"]
    for path, v in (("template", "explode"), ("fill.victim", "astronaut"), ("fill.thing.size_m", 4),
                    ("fill.witness_does", "dance"), ("set.ground", "water"), ("set.light", "noon"), ("moment", "")):
        r = copy.deepcopy(good)
        node, keys = r, path.split(".")
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = v
        assert opener_plan.fill_template(r) is None, path
    r = copy.deepcopy(SAMPLES["chop_bird"])
    r["fill"]["tool"]["find"] = "spoon"  # not a cut tool
    assert opener_plan.fill_template(r) is None
    r = copy.deepcopy(SAMPLES["falls_on_cheer"])
    r["fill"]["thing"]["find"] = "crate"  # only sacks and bags passed
    assert opener_plan.fill_template(r) is None


def test_fill_if_items():
    """A pick fills in a beat's move or a stroke; every slot must be filled."""
    r = copy.deepcopy(SAMPLES["falls_on_cheer"])
    r["fill"]["witness"] = None  # a falls_on with nobody reacting hid its victim behind the crate (2026-10-28)
    assert opener_plan.fill_template(r) is None
    cheer = opener_plan.fill_template(copy.deepcopy(SAMPLES["falls_on_cheer"]))
    assert cheer["beats"][-1] == {"move": "cheer", "actor": "witness", "at": 1.7}
    sl = opener_plan.fill_template(copy.deepcopy(SAMPLES["slice"]))
    assert sl["beats"][0]["strokes"] == [{"rows": 5}] and sl["beats"][0]["expect"][0]["pieces"] == "5-5"
    run = opener_plan.fill_template(copy.deepcopy(SAMPLES["hand_over_run"]))
    assert run["beats"][-1]["move"] == "run" and run["actors"][0]["prop"] == "coin bag"


def short(i=0):
    return {"title": f"Short {i}", "research": {"wiki": "text"},
            "scenes": [{"narration": "The sack fell."}, {"narration": "He was ruined."}]}


def test_no_template_fits():
    old = llm.ask_ai
    try:
        llm.ask_ai = lambda *a, **k: {"shorts": [{"index": 0, "template": None, "why": "a crowd of thousands"}]}
        s = short()
        opener_plan.plan_openers([s], {"niche": "history"})
        assert "opener" not in s and s["opener_check"] == "opener: no template fits (a crowd of thousands)", s
    finally:
        llm.ask_ai = old


def test_fill_retry_then_none():
    old, calls = llm.ask_ai, []
    try:
        llm.ask_ai = lambda *a, **k: calls.append(1) or {"shorts": [{"index": 0, "template": "falls_on", "fill": {}}]}
        s = short()
        opener_plan.plan_openers([s], {"niche": "history"})
        assert len(calls) == 2 and s["opener_check"] == "opener: no usable template fill" and "opener" not in s
    finally:
        llm.ask_ai = old


def test_good_fill_is_kept_and_prompt_has_templates_and_rules():
    old, prompts = (llm.ask_ai, opener_plan.session.RULES), []
    try:
        opener_plan.session.RULES = {"Opener": "RULES-MARKER"}
        llm.ask_ai = lambda prompt, **k: prompts.append(prompt) or {"shorts": [{"index": 0, **copy.deepcopy(SAMPLES["hand_over_walk"])}]}
        s = short()
        opener_plan.plan_openers([s], {"niche": "history"})
        assert s["opener"]["template"] == "hand_over" and s.get("opener_check") is None
        assert s["opener_fill"]["fill"]["taker"] == "businessman"
        assert "RULES-MARKER" in prompts[0] and "- falls_on:" in prompts[0] and "ww2_british_officer" in prompts[0]
    finally:
        llm.ask_ai, opener_plan.session.RULES = old


def test_swap_models_refills_the_template():
    old, prompts = llm.ask_ai, []
    try:
        swapped = copy.deepcopy(SAMPLES["falls_on_cheer"])
        swapped["fill"]["thing"]["find"] = "sack of grain"
        llm.ask_ai = lambda prompt, **k: prompts.append(prompt) or copy.deepcopy(swapped)
        s = {"title": "t", "opener_fill": copy.deepcopy(SAMPLES["falls_on_cheer"])}
        plan = opener_plan.swap_models(s, ["gunny sack"])
        assert plan["actors"][1]["find"] == "sack of grain" and s["opener_fill"]["fill"]["thing"]["find"] == "sack of grain"
        assert '"gunny sack"' in prompts[0]
        llm.ask_ai = lambda prompt, **k: {"template": "falls_on"}
        assert opener_plan.swap_models(s, ["sack of grain"]) is None and s["opener_fill"]["fill"]["thing"]["find"] == "sack of grain"
    finally:
        llm.ask_ai = old


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
