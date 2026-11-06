"""The opener crew (shortsmaker/opener_crew.py): the stager's plan checked against the kit, made parts kept and
reused, a failed part swapped for its substitute, fixes routed to the one member at fault, and parallel calls capped.
The AI is faked. Run: .venv\\Scripts\\python.exe tests\\test_opener_crew.py   (real node for the part sheets, ~30 s)"""
import json
import os
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
PARTS = Path(tempfile.mkdtemp(prefix="crew_parts_"))
os.environ["SHORTSMAKER_PARTS"] = str(PARTS)  # made parts go here, not into drawn/parts
from shortsmaker import drawn_opener, llm, opener3d, opener_crew  # noqa: E402

WORDS = [[0.1, 0.4, "A"], [0.45, 0.9, "ferryman"], [0.95, 1.4, "knocks"], [1.45, 1.6, "at"], [1.65, 2.2, "midnight"]]
HAT = "export default function draw(k, hy, o) { k.shape([[-30, hy - 18], [-30, hy - 50], [0, hy - 62], [30, hy - 50], [30, hy - 18]], o.hatColor || '#1E1A18'); }"


def staging(**over) -> dict:
    st = {"moment": "a ferryman knocks at midnight", "place": "outdoors", "light": "night",
          "strange": {"what": "a ferryman knocks at a house at midnight", "shows": ["the ferryman's fist on the closed door"]},
          "people": [{"id": "ferryman", "who": "a ferryman", "hat": "cap", "coat": "#3C4A6B", "holds": "letter", "doing": "knocks"}],
          "things": [{"id": "cottage", "kind": "house"}],
          "action": {"who": "ferryman", "does": "knocks", "on": "cottage"},
          "beats": [{"at": 0, "shot": "medium", "on": ["ferryman"]}, {"at": "knocks", "shot": "close", "on": ["ferryman"]}]}
    st.update(over)
    return st


def short() -> dict:
    return {"title": "The Midnight Knock", "topic": "an invented ferryman",
            "scenes": [{"narration": "A ferryman knocks at midnight.", "full": None}, {"narration": "Nobody answers.", "full": None}]}


def blind_ok(prompt):
    """The sound-off test's two calls (drawn_opener.blind_read) pass, so these tests count only the crew's calls."""
    if "You know nothing else about it" in prompt:
        return {"sees": "a man knocks on a cottage door at night holding a letter"}
    if "with the sound off and said" in prompt:
        return {"gets_it": True}
    return None


def fake(replies, prompts):
    it = iter(replies)
    return lambda prompt, **k: blind_ok(prompt) or prompts.append(prompt) or next(it)


def test_staging_is_checked_against_the_kit():
    st, bad = opener_crew.check_staging(staging(), WORDS)
    assert bad == [] and st["action"]["does"] == "knocks", bad
    st, bad = opener_crew.check_staging(staging(people=[{"id": "ferryman", "hat": "samurai", "holds": "lantern"}]), WORDS)
    assert any("samurai" in p for p in bad) and any("lantern" in p for p in bad), bad
    # the same hat and thing are fine once they are new parts with a look and a substitute
    new = [{"kind": "hat", "name": "samurai", "looks": "a lacquered helmet", "instead": "helmet"},
           {"kind": "thing", "name": "lantern", "looks": "a paper lantern", "instead": "none"}]
    st, bad = opener_crew.check_staging(staging(people=[{"id": "ferryman", "hat": "samurai", "holds": "lantern"}], new_parts=new), WORDS)
    assert bad == [] and len(st["new_parts"]) == 2, bad
    st, bad = opener_crew.check_staging(staging(things=[]), WORDS)
    assert any("knock needs a house" in p for p in bad), bad
    st, bad = opener_crew.check_staging(staging(beats=[{"at": 0, "shot": "wide", "on": ["ferryman"]}]), WORDS)
    assert any("2-4 beats" in p for p in bad), bad
    wide_first = staging(beats=[{"at": 0, "shot": "wide", "on": ["ferryman"]}, {"at": 1, "shot": "close", "on": ["ferryman"]}])
    assert any("first beat" in p for p in opener_crew.check_staging(wide_first, WORDS)[1])  # frame 0 must read on a phone
    two = staging(people=staging()["people"] + [{"id": "keeper", "hat": "none", "holds": "none"}])
    assert any("keeper is in no beat" in p for p in opener_crew.check_staging(two, WORDS)[1])  # nobody planned and never filmed
    # the strange thing and what a muted viewer sees of it are required (owner, 2026-11-06: the Carrington opener)
    for odd in (None, {"what": "the wires work unplugged"}, {"what": "", "shows": ["sparks"]}):
        assert any("give `strange`" in p for p in opener_crew.check_staging(staging(strange=odd), WORDS)[1]), odd
    st = opener_crew.check_staging(staging(strange={"what": "x", "shows": ["sparks on the key", " ", "loose wires"]}), WORDS)[0]
    assert st["strange"]["shows"] == ["sparks on the key", "loose wires"] and "strange: x" in opener_crew.staging_text(st)
    signs = [{"type": "sparks", "on": "cottage"}, {"type": "aurora", "on": "moon"}]
    st, bad = opener_crew.check_staging(staging(strange={"what": "x", "shows": ["y"], "effects": signs}), WORDS)
    assert bad == [] and st["strange"]["effects"] == [{"type": "sparks", "on": "cottage"}, {"type": "aurora"}], bad
    for wrong in ({"type": "sparks", "on": "nobody"}, {"type": "lightning", "on": "cottage"}):
        assert any("strange effect" in p for p in opener_crew.check_staging(staging(strange={"what": "x", "shows": ["y"], "effects": [wrong]}), WORDS)[1])


def test_the_stagers_sign_effects_are_put_in_by_code():
    """Carrington, 2026-11-06: the stager's strange thing was electric but the placer added no effect at all."""
    st = opener_crew.check_staging(staging(strange={"what": "x", "shows": ["y"], "effects": [{"type": "sparks", "on": "ferryman"}]}), WORDS)[0]
    cut = {"name": "ferryman", "what": "a ferryman", "w": 1200, "h": 1100, "height": 2.3, "frames": 2,
           "code": "export default function draw(k, f) { k.knock(600, 1080, 3.4, {phase: f / 2, person: {hat: 'cap', hold: ['letter', null]}}); }"}
    raw = {"place": "outdoors", "mood": "night", "props": [{"type": "house", "id": "cottage", "place": {"mark": "centre"}}],
           "cutouts": [{"name": "ferryman", "place": {"door": "cottage"}}],
           "shots": [{"at": 0, "target": "ferryman", "shot": "wide"}, {"at": "knocks", "target": "ferryman", "shot": "close"}]}
    stage, _ = opener_crew.assemble(raw, [cut], st, WORDS, 2.6, "A ferryman knocks at midnight.")
    assert {"type": "sparks", "at": 0, "on": "ferryman"} in stage["effects"], stage["effects"]
    raw["effects"] = [{"type": "sparks", "at": 1, "on": "ferryman"}]  # the placer timed it itself: not doubled
    stage, _ = opener_crew.assemble(raw, [cut], st, WORDS, 2.6, "A ferryman knocks at midnight.")
    assert [e["type"] for e in stage["effects"]] == ["sparks"] and stage["effects"][0]["at"] == 1


def test_a_made_part_is_kept_and_reused_with_no_ai():
    saved, prompts = llm.ask_ai, []
    llm.ask_ai = fake([{"code": HAT}, {"score": 8, "problems": []}], prompts)
    try:
        with tempfile.TemporaryDirectory() as d:
            st = opener_crew.check_staging(staging(people=[{"id": "ferryman", "hat": "spike", "holds": "letter"}],
                                                   new_parts=[{"kind": "hat", "name": "spike", "looks": "a spiked helmet", "instead": "helmet"}]), WORDS)[0]
            log = []
            opener_crew.make_parts(st, Path(d), log)
            assert (PARTS / "hat" / "spike.mjs").exists() and "made the hat spike" in log[0], log
            assert "spike.png" in prompts[1] and "spike" in opener_crew.kit_hats()
            opener_crew.make_parts(st, Path(d), log)  # the next Short: already made, no AI
            assert len(prompts) == 2
    finally:
        llm.ask_ai = saved


def test_a_failed_part_falls_back_to_its_substitute():
    saved = llm.ask_ai
    bad_code = "export default function draw(k, hy, o) { k.text('HAT', 0, hy); }"  # words in a part: rejected
    llm.ask_ai = fake([{"code": bad_code}, {"code": bad_code}], [])
    try:
        with tempfile.TemporaryDirectory() as d:
            st = opener_crew.check_staging(staging(people=[{"id": "ferryman", "hat": "plume", "holds": "letter"}],
                                                   new_parts=[{"kind": "hat", "name": "plume", "looks": "a feathered hat", "instead": "tricorn"}]), WORDS)[0]
            log = []
            opener_crew.make_parts(st, Path(d), log)
            assert st["people"][0]["hat"] == "tricorn" and "using tricorn" in log[0], (st["people"], log)
            assert not (PARTS / "hat" / "plume.mjs").exists()
    finally:
        llm.ask_ai = saved


def test_problems_go_to_the_member_at_fault():
    names = ["ferryman", "keeper"]
    assert opener_crew.owner("person:keeper: his coat melts into the wall", names) == "person:keeper"
    # there is no placer AI: everything that isn't how a cut-out is drawn goes back to the stager (2026-11-06)
    assert opener_crew.owner("camera: the close-up cuts off his hand", names) == "stager"
    assert opener_crew.owner("cut-out ferryman: uses `process`", names) == "person:ferryman"
    assert opener_crew.owner("keeper's main colour (#7A4E2C) melts into the wall", names) == "stager"  # the wall colour
    assert opener_crew.owner("person:ghost: who is this", names) == "stager"  # an unknown painter
    assert opener_crew.owner("stager: sound-off test failed: a stranger saw a man", names) == "stager"
    # a bad `place` relation isn't the painter's (live 2026-11-06: it went to the painter, who couldn't fix it)
    cut = {"w": 700, "h": 1100, "height": 1.75, "code": "export default function draw(k, f) { k.person(350, 1080, 4, {}); }"}
    raw = {"place": "room", "cutouts": [{"name": "keeper", "place": {"beside": "telegraph"}, **cut}],
           "shots": [{"at": 0, "target": "keeper", "shot": "wide"}, {"at": 1, "target": "keeper", "shot": "close"}]}
    stage, bad = opener_crew.assemble(raw, [{"name": "keeper", "what": "a keeper", **cut}], {"things": []}, WORDS, 2.6, "")
    assert bad and all(opener_crew.owner(p, ["keeper"]) == "stager" for p in bad), bad


PERSON = {"w": 700, "h": 1100, "height": 1.75, "frames": 2, "code": "export default function draw(k, f) { k.person(350, 1080, 4, {}); }"}


def test_the_layout_puts_3d_objects_on_the_desk_and_the_operator_at_it():
    """Owner, 2026-11-06: people stay drawn, every object is 3D. The radio stands on the desk as a 3D object, the one
    acting on it stands at the desk, both fit the first shot; the aurora gets a window, the sparks come off the radio."""
    raw = staging(place="room", light="interior", moment="an operator stares at his telegraph register",
                  people=[{"id": "operator", "who": "an operator", "hat": "none", "coat": "#285B83", "holds": "none", "doing": "stares"},
                          {"id": "clerk", "who": "a clerk", "hat": "bowler", "holds": "paper", "doing": "reads"}],
                  things=[{"id": "desk", "kind": "desk"}, {"id": "register", "kind": "radio"}, {"id": "logs", "kind": "logs"}],
                  action={"who": "operator", "does": "looks", "on": "register"},
                  beats=[{"at": 0, "shot": "medium", "on": ["operator", "register"]}, {"at": "knocks", "shot": "close", "on": ["register"]},
                         {"at": "midnight", "shot": "close", "on": ["register"]}, {"at": 2.0, "shot": "medium", "on": ["clerk"]}],
                  strange={"what": "it works unplugged", "shows": ["sparks"], "effects": [{"type": "sparks", "on": "register"}, {"type": "aurora"}]})
    st, bad = opener_crew.check_staging(raw, WORDS)
    assert bad == [], bad
    cuts = [{"name": "operator", "what": "an operator", **PERSON}, {"name": "clerk", "what": "a clerk", **PERSON}]
    stage, bad = opener_crew.assemble(opener_crew.layout(st, cuts, WORDS), cuts, st, WORDS, 2.6, "")
    assert bad == [], bad
    props = {p.get("id"): p for p in stage["props"]}
    op = next(c for c in stage["cutouts"] if c["name"] == "operator")
    assert props["register"]["y"] > .8 and abs(op["at"][0] - props["register"]["at"][0]) < 1.4, (props["register"], op)
    assert props["logs"]["at"][1] < -2.5 and props["register"]["h"] == .32  # big things go back; a shot aims mid-object
    assert opener3d.spread_out(stage["shots"], stage["cutouts"], stage["props"]) == []  # the first shot frames both, big
    sizes = [(s["size"], s["target"]) for s in stage["shots"]]
    assert sizes[1] != sizes[2] and stage["shots"][0]["at"] == 0, sizes  # a repeated framing is changed
    assert any(p["type"] == "window" and p.get("wall") for p in stage["props"])  # the aurora needs a window in a room
    assert {"type": "sparks", "at": 0, "on": "register"} in stage["effects"] and stage["colors"]["wall"] == "#E3D3B0"


def test_the_one_acting_stands_by_what_they_act_on_and_holds_3d_objects():
    """Pig War, 2026-11-06: the farmer stood at the garden's edge and the pig in its middle (5.8 m apart), and a pig
    eating the potatoes stood beside the garden. Now the pig is in the garden with the farmer beside it, in the kit's
    own pink. A held 3D object goes in the hand, and a beat on it frames the one holding it."""
    pig = opener_crew.animal_cutout({"id": "pig", "kind": "pig", "does": "eats"})
    raw = staging(moment="a pig eats a farmer's potatoes", people=[{"id": "farmer", "who": "a farmer", "hat": "none", "holds": "pumpkin", "doing": "points"}],
                  animals=[{"id": "pig", "kind": "pig", "color": "#34302D", "does": "eats"}],
                  things=[{"id": "garden", "kind": "garden"}, {"id": "gourd", "kind": "pumpkin"}],
                  action={"who": "farmer", "does": "points", "on": "pig"},
                  beats=[{"at": 0, "shot": "medium", "on": ["pig", "farmer"]}, {"at": "knocks", "shot": "close", "on": ["gourd"]}])
    st, bad = opener_crew.check_staging(raw, WORDS)
    assert bad == [] and st["animals"][0]["color"] is None and not any(t["kind"] == "pumpkin" for t in st["things"]), (bad, st)
    cuts = [{"name": "farmer", "what": "a farmer", **PERSON}, {**pig, "what": "a pig"}]
    stage, bad = opener_crew.assemble(opener_crew.layout(st, cuts, WORDS), cuts, st, WORDS, 2.6, "")
    assert bad == [] and stage["shots"][0]["size"] == "medium", (bad, stage["shots"])
    at = {c["name"]: c for c in stage["cutouts"]}
    assert abs(at["farmer"]["at"][0] - at["pig"]["at"][0]) < 1.2, at
    assert at["farmer"]["held"] == {"type": "pumpkin", "height": .35, "hand": 1} and stage["shots"][1]["target"] == "farmer"
    raw2 = staging(moment="a pig eats the potatoes", people=[], animals=[{"id": "pig", "kind": "pig", "does": "eats"}],
                   things=[{"id": "garden", "kind": "garden"}], action={"who": "pig", "does": "eats", "on": "garden"},
                   beats=[{"at": 0, "shot": "medium", "on": ["pig"]}, {"at": 1, "shot": "close", "on": ["pig"]}])
    st = opener_crew.check_staging(raw2, WORDS)[0]
    one = [{**pig, "what": "a pig"}]
    stage, bad = opener_crew.assemble(opener_crew.layout(st, one, WORDS), one, st, WORDS, 2.6, "")
    garden, x, z = opener3d.box_of(stage["props"][0]), *stage["cutouts"][0]["at"]
    assert bad == [] and garden[0] < x < garden[1] and garden[2] < z < garden[3], (bad, garden, x, z)


def test_a_person_is_the_kits_person_only():
    """Owner, 2026-11-06: a painter's own skirt polygon read as "a weird red box" and its fingers as weird hands."""
    assert opener_crew.lint_person("export default function draw(k, f, u) { k.person(350, 1080, 4, {dress: '#B74732'}); }") == []
    assert opener_crew.lint_person("export default function draw(k, f) { k.knock(600, 1080, 3.4, {phase: f / 2}); }") == []
    bad = opener_crew.lint_person("export default function draw(k, f, u) { const p = k.person(350, 1080, 4, {}); k.shape([[1, 2]], '#B74732'); k.ink([[1, 2]]); }")
    assert bad and "k.shape" in bad[0] and "k.ink" in bad[0], bad


def test_a_replan_keeps_unchanged_people_and_adds_no_parts():
    saved, prompts = llm.ask_ai, []
    llm.ask_ai = fake([], prompts)  # no AI call may happen: the person is unchanged, no part is made
    try:
        st = opener_crew.check_staging(staging(), WORDS)[0]
        painted = {"name": "ferryman", "w": 700, "h": 1100, "height": 1.75, "frames": 2, "code": "x"}
        people, cuts, _ = opener_crew.crew(st, short(), Path("."), [], {json.dumps(st["people"][0], sort_keys=True): painted})
        assert cuts[0]["code"] == "x" and prompts == []
        new = [{"kind": "thing", "name": "anvil2", "looks": "an anvil", "instead": "none"}]
        st, bad = opener_crew.check_staging(staging(things=[{"id": "cottage", "kind": "house"}, {"id": "a", "kind": "anvil2"}],
                                                    new_parts=new), WORDS, allow_new=False)
        assert st["new_parts"] == [] and any("no new parts" in p for p in bad), bad
    finally:
        llm.ask_ai = saved


def test_a_new_3d_thing_is_built_checked_and_kept():
    """A thing the library lacks is built from primitives, rendered beside a person (real Remotion, ~30 s), checked
    and kept in drawn/parts/thing3d for every later Short; then a staging can hold it."""
    saved, prompts = llm.ask_ai, []
    shapes = [{"shape": "box", "size": [.4, .2, .2], "at": [0, .1, 0], "color": "#5A5A60", "metal": True},
              {"shape": "box", "size": [.2, .1, .15], "at": [0, .25, 0], "color": "#5A5A60", "metal": True}]
    llm.ask_ai = fake([{"shapes": shapes}, {"score": 8, "problems": []}], prompts)
    try:
        with tempfile.TemporaryDirectory() as d:
            ok, note = opener_crew.make_part3d({"kind": "thing", "name": "anvil", "looks": "a blacksmith's anvil", "instead": "none"}, Path(d))
            assert ok and "made the 3D thing anvil" in note and "anvil" in opener3d.made3d() and "anvil.png" in prompts[1], note
        st, bad = opener_crew.check_staging(staging(people=[{"id": "ferryman", "hat": "cap", "holds": "anvil"}]), WORDS)
        assert bad == [] and opener3d.held_of("anvil")["shapes"][0]["shape"] == "box", bad
    finally:
        llm.ask_ai = saved


def test_a_plan_problem_sends_the_stager_back_with_its_last_plan():
    """The sound-off test failed on what the plan shows: the stager plans again (seeing the problem and its last
    plan), the painter paints the new plan, and the next draft passes."""
    saved, prompts = llm.ask_ai, []
    painted = {"w": 1200, "h": 1100, "height": 2.3, "frames": 2, "fps": 8,
               "code": "export default function draw(k, f) { k.knock(600, 1080, 3.4, {phase: f / 2, person: {hat: 'cap', coat: k.C.navy, hold: ['letter', null]}}); }"}
    again = staging(moment="a ferryman pounds on the door at midnight")
    llm.ask_ai = fake([staging(), painted, {"score": 6, "problems": ["stager: nothing says it is midnight"]},
                       again, painted, {"score": 8, "problems": []}], prompts)
    try:
        with tempfile.TemporaryDirectory() as d:
            s = short()
            made, why = opener_crew.plan(s, WORDS, 2.6, Path(d))
            assert made and why is None, why
            assert "STAGER" in prompts[3] and "nothing says it is midnight" in prompts[3] and "Your last plan" in prompts[3]
            assert s["opener_staging"]["moment"].startswith("a ferryman pounds") and any(x.startswith("fix: stager") for x in s["opener_crew"])
    finally:
        llm.ask_ai = saved


def test_a_painter_with_unusable_code_gets_the_plain_kit_cutout():
    saved = llm.ask_ai
    llm.ask_ai = fake([{"code": "process.exit()"}, None], [])
    try:
        st = opener_crew.check_staging(staging(), WORDS)[0]
        cut = opener_crew.paint(st["people"][0], st, short(), Path("."))
        assert "k.knock(" in cut["code"] and "hold: ['letter', null]" in cut["code"] and opener3d.lint_cutout(cut["code"]) == []
    finally:
        llm.ask_ai = saved


def test_parallel_calls_are_capped():
    live, most, lock = [0], [0], threading.Lock()

    def job():
        with lock:
            live[0] += 1
            most[0] = max(most[0], live[0])
        time.sleep(.05)
        with lock:
            live[0] -= 1
        return 1

    assert opener_crew.parallel([job] * 8) == [1] * 8 and most[0] == opener_crew.MAX_PARALLEL, most


def test_the_whole_crew_passes_and_only_the_faulted_painter_repaints():
    """stager -> painter -> layout (code) -> render (real) -> review 5/10 tagged at the painter -> only that painter
    again -> same stage -> review 8/10: passed. The knocker stands at the cottage door and knocks on "knocks"."""
    saved, prompts = llm.ask_ai, []
    painted = {"w": 1200, "h": 1100, "height": 2.3, "frames": 2, "fps": 8,
               "code": "export default function draw(k, f) { k.knock(600, 1080, 3.4, {phase: f / 2, person: {hat: 'cap', coat: k.C.navy, hold: ['letter', null]}}); }"}
    llm.ask_ai = fake([staging(), painted, {"score": 5, "problems": ["person:ferryman: his coat is too dark"]},
                       {**painted, "code": painted["code"].replace("k.C.navy", "k.C.red")}, {"score": 8, "problems": []}], prompts)
    try:
        with tempfile.TemporaryDirectory() as d:
            s = short()
            made, why = opener_crew.plan(s, WORDS, 2.6, Path(d))
            assert made and why is None and made["kind"] == "3d", why
            assert "k.C.red" in made["cutouts"][0]["code"] and s["opener_staging"]["action"]["does"] == "knocks"
            assert made["cutouts"][0]["against"] == "cottage" and made["cutouts"][0]["hits"] == [0.95], made["cutouts"][0]
            assert "STAGER" in prompts[0] and "PAINTER" in prompts[1]
            assert "his coat is too dark" in prompts[3] and "PAINTER" in prompts[3] and len(prompts) == 5  # no stager call
            assert "second row shows the same moments 0.2 s later" in prompts[2] and "person:ferryman (" in prompts[2]
            assert "cycle of drawings" in prompts[2] and (Path(d) / "sheet3d1.png").exists()
            assert s["opener3d_best"]["score"] == 5 and s["opener3d_best"]["plan"]["kind"] == "3d"  # kept for drawn_opener.KEEP
            assert any(line.startswith("draft 2: 8/10") for line in s["opener_crew"]), s["opener_crew"]
    finally:
        llm.ask_ai = saved


if __name__ == "__main__":
    names = [n for n in sorted(globals()) if n.startswith("test_")]
    for n in names:
        globals()[n]()
        print(f"PASS {n}")
    print(f"{len(names)}/{len(names)} passed")
