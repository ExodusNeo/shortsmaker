"""3D opener checks (shortsmaker/opener3d.py): the placer's relations, named shots and the stage rules.
Run: .venv\\Scripts\\python.exe tests\\test_opener3d.py   (--look renders STAGE3D.md's example to test_renders/opener3d)"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shortsmaker import drawn_opener, opener3d, opener_crew  # noqa: E402

# STAGE3D.md's invented example: "At midnight a ferryman knocks on the lighthouse keeper's door, a sealed letter in his hand."
WORDS = [[0.1, 0.3, "At"], [0.32, 0.8, "midnight"], [0.85, 0.9, "a"], [0.92, 1.4, "ferryman"], [1.45, 1.8, "knocks"],
         [1.85, 1.95, "on"], [1.98, 2.1, "the"], [2.12, 2.6, "keeper's"], [2.62, 2.9, "door,"], [3.0, 3.1, "a"],
         [3.12, 3.5, "sealed"], [3.52, 3.9, "letter"], [3.95, 4.05, "in"], [4.08, 4.2, "his"], [4.22, 4.5, "hand."]]
SECONDS = 4.8
KNOCKER = {"w": 1200, "h": 1100, "height": 2.3, "frames": 4, "fps": 8,
           "code": "export default function draw(k, f) { k.knock(600, 1080, 3.4, {phase: f / 4, person: {hat: 'cap', "
                   "coat: k.C.navy, skin: k.SKIN[1], face: f % 2 ? 'open' : 'flat', hold: ['letter', null]}}); }"}
PERSON = {"w": 700, "h": 1100, "height": 1.75, "frames": 2,
          "code": "export default function draw(k, f) { k.person(350, 1080, 4, {hat: 'none', coat: k.C.red}); }"}


def example() -> dict:
    """The manual's placer JSON, with the painter's cut-out added (the crew merges them the same way)."""
    text = (ROOT / "drawn" / "STAGE3D.md").read_text(encoding="utf-8")
    raw = json.loads(re.search(r"## Example.*?```json\n(.*?)```", text, re.S).group(1))
    raw["cutouts"] = [{**c, **KNOCKER} for c in raw["cutouts"]]
    return raw


def room(*people) -> dict:
    """A small room stage: a desk, and each named person on the given relation."""
    return {"place": "room", "mood": "interior", "props": [{"type": "desk", "id": "desk", "place": {"mark": "centre"}}],
            "cutouts": [{"name": n, "place": spec, **PERSON} for n, spec in people],
            "shots": [{"at": 0, "target": people[0][0], "shot": "wide"}, {"at": 1, "target": people[0][0], "shot": "close"}]}


def test_example_is_clean_and_the_knocker_stands_on_the_door():
    stage, bad = opener3d.clean(example(), WORDS, SECONDS)
    assert bad == [], bad
    house = stage["props"][0]
    assert stage["cutouts"][0]["at"] == list(opener3d.front_door(house, 0)) and stage["cutouts"][0]["against"] == "cottage"
    assert stage["shots"][1]["at"] == 1.45 and stage["shots"][1]["size"] == "close"  # "knocks" resolved to its time
    assert stage["cutouts"][0]["hits"] == [1.45, 2.62] and stage["cutouts"][0]["focus"] < 0  # aims at the knocker
    # the house's FRONT stands on its mark: the knocker is on the action line, not inside the walls
    assert -3.2 < stage["cutouts"][0]["at"][1] < -2.2, stage["cutouts"][0]["at"]


def test_named_shots_change_size_and_scale_with_the_target():
    stage, _ = opener3d.clean(example(), WORDS, SECONDS)
    wide, close = stage["shots"][0], stage["shots"][1]
    assert wide["distance"] >= opener3d.SPREAD * close["distance"], (wide, close)
    # a knocker's board is 2.3 m because of its door: his shots are sized for the man (1.75 m), not the door
    assert wide["distance"] == opener3d.SHOT_SIZES["wide"][0] and stage["cutouts"][0]["contact"][0] < 0
    raw = room(("keeper", {"mark": "left"}))
    raw["cutouts"][0]["height"] = 3.5  # a giant: every shot stands twice as far back
    assert opener3d.clean(raw, WORDS, SECONDS)[0]["shots"][0]["distance"] == round(2 * opener3d.SHOT_SIZES["wide"][0], 2)
    raw = example()
    raw["shots"] = [{"at": 0, "target": "ferryman", "shot": "medium"}, {"at": 1, "target": "ferryman", "shot": "medium"}]
    assert any("repeat a size" in p for p in opener3d.clean(raw, WORDS, SECONDS)[1])
    raw["shots"][1] = {"at": 1, "target": "ferryman", "shot": "over"}
    assert any("needs `over`" in p for p in opener3d.clean(raw, WORDS, SECONDS)[1])


def test_marks_beside_front_and_wall():
    raw = room(("keeper", {"mark": "left"}), ("clerk", {"beside": "desk", "side": "right"}), ("boy", {"front": "desk"}))
    raw["props"].append({"type": "window", "place": {"wall": "left"}})
    stage, bad = opener3d.clean(raw, WORDS, SECONDS)
    assert bad == [], bad
    at = {c["name"]: c["at"] for c in stage["cutouts"]}
    desk = opener3d.box_of(stage["props"][0])
    assert at["keeper"] == list(opener3d.MARKS["room"]["left"])
    assert at["clerk"][0] > desk[1] and at["boy"][1] > desk[3], (at, desk)  # beside it on the right; in front of it
    assert stage["props"][1]["wall"] and stage["props"][1]["at"][0] == opener3d.WALL_SPOTS["left"]
    raw = room(("keeper", {"mark": "left"}), ("sounder", {"on": "desk", "side": "right"}))  # a machine on the desk
    stage, bad = opener3d.clean(raw, WORDS, SECONDS)
    sounder, desk = stage["cutouts"][1], opener3d.box_of(stage["props"][0])
    assert bad == [] and sounder["y"] == .86 and desk[0] < sounder["at"][0] < desk[1] and desk[2] < sounder["at"][1] < desk[3], (bad, sounder)
    raw["cutouts"][1]["place"] = {"on": "keeper"}
    assert any("things stand on a prop" in p for p in opener3d.clean(raw, WORDS, SECONDS)[1])
    raw = room(("clerk", {"beside": "keeper", "side": "left"}), ("keeper", {"mark": "right"}))  # names one listed after it
    stage, bad = opener3d.clean(raw, WORDS, SECONDS)
    assert bad == [] and {c["name"]: c["at"] for c in stage["cutouts"]}["clerk"][0] < opener3d.MARKS["room"]["right"][0], bad
    raw["cutouts"][0]["place"] = {"beside": "nobody"}
    assert any("nobody" in p for p in opener3d.clean(raw, WORDS, SECONDS)[1])
    raw["cutouts"][0]["place"] = {"mark": "moon"}
    assert any("no mark" in p for p in opener3d.clean(raw, WORDS, SECONDS)[1])


def test_signs_of_the_strange_thing():
    """Sparks, smoke and glow come off a named thing; an aurora in a room needs a window to be seen (2026-11-06:
    the unplugged Carrington telegraph showed nothing electric)."""
    raw = room(("keeper", {"mark": "left"}))
    raw["effects"] = [{"type": "sparks", "at": 0, "on": "keeper"}, {"type": "glow", "on": "desk", "color": "#7FB8FF"},
                      {"type": "smoke", "at": 1}, {"type": "aurora"}]
    stage, bad = opener3d.clean(raw, WORDS, SECONDS)
    assert any("smoke effect needs `on`" in p for p in bad) and any("aurora shows through a window" in p for p in bad), bad
    assert len(bad) == 2 and {"type": "glow", "at": 0, "on": "desk", "color": "#7FB8FF"} in stage["effects"], bad
    raw["effects"][2]["on"] = "desk"
    raw["props"].append({"type": "window", "place": {"wall": "right"}})
    assert opener3d.clean(raw, WORDS, SECONDS)[1] == []


def test_nobody_hides_in_furniture_or_inside_another_person():
    raw = room(("keeper", {"mark": "centre"}), ("clerk", {"mark": "centre"}))  # both on the desk's own spot
    stage, bad = opener3d.clean(raw, WORDS, SECONDS)
    assert bad == [], bad
    desk, (a, b) = opener3d.box_of(stage["props"][0]), stage["cutouts"]
    assert a["at"][1] > desk[3] and b["at"][1] > desk[3], (a["at"], b["at"], desk)  # moved to stand in front of the desk
    assert abs(a["at"][0] - b["at"][0]) >= opener3d.half_width(a) + opener3d.half_width(b), (a["at"], b["at"])


def test_a_walk_goes_from_mark_to_mark():
    raw = room(("keeper", {"mark": "left"}))
    raw["cutouts"][0]["path"] = [[0, "left"], ["midnight", "right"]]
    stage, bad = opener3d.clean(raw, WORDS, SECONDS)
    assert bad == [] and stage["cutouts"][0]["path"] == [[0, -1.5, -1.7], [0.32, 1.5, -1.7]], (bad, stage["cutouts"][0].get("path"))
    raw["cutouts"][0]["path"] = [{"at": 0, "mark": "left"}, ["midnight", {"mark": "right"}]]  # the other ways placers write it
    assert opener3d.clean(raw, WORDS, SECONDS)[0]["cutouts"][0]["path"] == [[0, -1.5, -1.7], [0.32, 1.5, -1.7]]
    raw["cutouts"][0]["path"] = [[0, "moon"]]
    bad = opener3d.clean(raw, WORDS, SECONDS)[1]
    assert any("path step" in p for p in bad) and all(opener_crew.owner(p, ["keeper"]) == "stager" for p in bad), bad


def test_bad_parts_go_back():
    raw = example()
    raw["props"].append({"type": "spaceship", "place": {"mark": "left"}})
    raw["cutouts"][0]["code"] += "\nconst x = Math.random();"
    raw["shots"].append({"at": 1, "target": "nobody", "shot": "close"})
    stage, bad = opener3d.clean(raw, WORDS, SECONDS)
    text = " ".join(bad)
    assert "spaceship" in text and "Math.random" in text and "nobody" in text, bad
    assert all(p["type"] in opener3d.PROPS for p in stage["props"])


def test_lint_needs_draw():
    assert opener3d.lint_cutout("export default function draw(k, f) { k.person(1, 2, 3, {}); }") == []
    assert any("draw(k, f" in p for p in opener3d.lint_cutout("export default function scene(k, t) {}"))
    assert any("process" in p for p in opener3d.lint_cutout("export default function draw(k, f) { process.exit(); }"))


def test_numbers_are_clamped():
    raw = example()
    raw["shots"][0].update(distance=999, fov=5)  # a named size ignores typed numbers...
    raw["cutouts"][0].update(frames=40, w=99999)
    stage, _ = opener3d.clean(raw, WORDS, SECONDS)
    assert stage["shots"][0]["distance"] == opener3d.SHOT_SIZES["wide"][0] and stage["shots"][0]["fov"] == opener3d.SHOT_SIZES["wide"][2]
    raw["shots"][0].pop("shot")  # ...an unnamed (older) shot keeps them, clamped
    stage, _ = opener3d.clean(raw, WORDS, SECONDS)
    assert stage["shots"][0]["distance"] == 14 and stage["shots"][0]["fov"] == 28
    assert stage["cutouts"][0]["frames"] == 6 and stage["cutouts"][0]["w"] == 1400


KNOCK = "export default function draw(k, f) { const d = k.door(390, 1170, 3.8, {open: %s}); k.person(540, 1170, 3, {reach: [[d.knob[0], d.knob[1] - 135], null]}); }"


def test_a_knock_needs_a_closed_door_and_a_messenger_his_letter():
    narration = "A messenger knocked on his door."
    found = drawn_opener.missing_parts({"moment": "the messenger knocks", "code": KNOCK % "0.56"}, narration)
    assert any("OPEN door" in p for p in found) and any("letter" in p for p in found), found
    ok = KNOCK % "0" + " k.letter(1, 2, 1);"
    assert drawn_opener.missing_parts({"moment": "the messenger knocks", "code": ok}, narration) == []
    code = "export default function draw(k, f) { k.person(1, 2, 3, {}); k.letter(1, 2, 1); }"
    assert drawn_opener.missing_parts({"moment": "he knocks", "code": code}, "", {"door"}, [0]) == []
    assert any("OPEN" in p for p in drawn_opener.missing_parts({"moment": "he knocks", "code": code}, "", {"door"}, [0.6]))


def test_hold_counts_as_drawing_the_letter_and_scenery_stays_3d():
    code = "export default function draw(k, f) { k.person(1, 2, 3, {hold: [null, 'letter']}); }"
    assert drawn_opener.missing_parts({"moment": "the messenger waits", "code": code}) == []
    assert any("letter" in p for p in drawn_opener.missing_parts({"moment": "the messenger waits", "code": code.replace("letter", "cup")}))
    assert any("scenery" in p and "k.house" in p for p in opener3d.lint_cutout(
        "export default function draw(k, f) { k.house(1, 2, 3); k.person(1, 2, 3, {}); }"))
    knock = "export default function draw(k, f) { k.knock(600, 1080, 3.4, {person: {hold: ['letter', null]}}); }"
    assert drawn_opener.missing_parts({"moment": "the messenger knocks", "code": knock}) == []


def test_a_cabin_has_its_own_door():
    raw = example()
    raw["props"][0]["type"] = "cabin"  # two wall modules: its door is one of them, half a module off the centre
    stage, bad = opener3d.clean(raw, WORDS, SECONDS)
    cabin, knocker = stage["props"][0], stage["cutouts"][0]
    assert bad == [] and abs(abs(knocker["at"][0] - cabin["at"][0]) - opener3d.HOUSE_UNIT / 2) < 1e-6, (bad, knocker["at"], cabin["at"])


def test_someone_inside_a_house_steps_out_and_a_door_needs_a_real_id():
    raw = example()
    raw["cutouts"][0].pop("place")
    raw["cutouts"][0]["at"] = [0, -3.2]  # within the house's walls
    stage, bad = opener3d.clean(raw, WORDS, SECONDS)
    front = opener3d.box_of(stage["props"][0])[3]
    assert bad == [] and stage["cutouts"][0]["at"][1] > front, (bad, stage["cutouts"][0]["at"], front)  # moved in front
    raw["cutouts"][0]["place"] = {"door": "nowhere"}
    assert any("door of 'nowhere'" in p for p in opener3d.clean(raw, WORDS, SECONDS)[1])


def test_a_cutout_that_melts_into_the_wall_goes_back():
    from PIL import Image
    tmp = ROOT / "test_renders" / "opener3d" / "blend_test"
    (tmp / "cutouts").mkdir(parents=True, exist_ok=True)
    for name, colour in (("brown", (122, 78, 44)), ("navy", (40, 52, 96))):
        im = Image.new("RGBA", (100, 200), (0, 0, 0, 0))
        im.paste((*colour, 255), (20, 20, 80, 190))
        im.save(tmp / "cutouts" / f"{name}_0.png")
    stage = {"place": "room", "colors": {"wall": "#7E5A40"},
             "cutouts": [{"name": "brown", "w": 100, "h": 200}, {"name": "navy", "w": 100, "h": 200}]}
    found = opener3d.blends(stage, tmp)
    assert len(found) == 1 and found[0].startswith("brown"), found
    assert opener3d.blends({**stage, "place": "street"}, tmp) == []


def test_the_preview_sees_every_shot():
    shots = [{"at": 0}, {"at": 1.409}, {"at": 2.396}]
    times = opener3d.sheet_times(4.47, shots)
    assert len(times) == 6 and times[0] == 0 and 1.76 in times and 2.75 in times, times
    assert len(opener3d.sheet_times(4.47)) == 6


def test_an_arm_past_the_canvas_edge_is_kept():
    """cutouts.mjs paints with room to spare and crops round the drawing (owner, 2026-11-06: a waving arm was cut off
    at its widest, "like an invisible wall"): nothing touches the edge, the board grows, the feet stay put."""
    import subprocess, tempfile
    from PIL import Image
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "wave.mjs").write_text("export default function draw(k, f, u) { k.person(150, 1080, 4, {arms: [100, 100 + 60 * u], "
                                    "bend: [0, 0], dance: u * 2 * Math.PI}); }", encoding="utf-8")
        job = {"out": str(d / "out"), "cutouts": [{"name": "w", "w": 300, "h": 1100, "frames": 2, "fps": 6, "module": str(d / "wave.mjs")}]}
        (d / "job.json").write_text(json.dumps(job), encoding="utf-8")
        r = subprocess.run(["node", str(ROOT / "drawn" / "cutouts.mjs"), str(d / "job.json")], cwd=ROOT / "drawn",
                           capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        size = json.loads((d / "out" / "sizes.json").read_text())["w"]
        assert size["wide"] > 1.5 and size["steps"] == 12, size
        pngs = sorted((d / "out").glob("w_*.png"))
        assert len(pngs) == 12
        for png in pngs:
            a = Image.open(png).getchannel("A")
            w, h = a.size
            for edge in (a.crop((0, 0, 1, h)), a.crop((w - 1, 0, w, h)), a.crop((0, 0, w, 1))):
                assert edge.getextrema()[1] <= 8, png.name
            assert a.crop((0, h - 150, w, h)).getextrema()[1] > 8  # the feet (hop + walk bounce lift them) stay near the bottom


def test_an_animal_in_the_garden_stays_in_it():
    """The live Pig War pig was placed in the potato patch and the furniture nudge pushed it out to the front edge."""
    raw = {"place": "outdoors", "props": [{"type": "garden", "id": "garden", "place": {"mark": "centre"}}],
           "cutouts": [{"name": "pig", "place": {"in": "garden"}, **PERSON}, {"name": "b", "place": {"mark": "back"}, **PERSON}],
           "shots": [{"at": 0, "target": "pig", "shot": "wide"}, {"at": 1, "target": "pig", "shot": "close"}]}
    stage, bad = opener3d.clean(raw, [], 2)
    x0, x1, z0, z1 = opener3d.box_of(stage["props"][0])
    assert not bad and x0 < stage["cutouts"][0]["at"][0] < x1 and z0 < stage["cutouts"][0]["at"][1] < z1, (bad, stage["cutouts"][0])
    raw["cutouts"][0]["place"] = {"in": "b"}
    assert any("in 'b'" in p for p in opener3d.clean(raw, [], 2)[1])


def test_a_close_shot_on_people_far_apart_goes_back_to_the_placer():
    """All three live stories (2026-11-06) opened on a 'medium' of two people at opposite sides of the set: the
    camera backed off to fit both and they read tiny. clean() sends that back before anything renders."""
    raw = {"place": "room", "props": [], "cutouts": [{"name": "a", "place": {"mark": "back-left"}, **PERSON},
                                                    {"name": "b", "place": {"mark": "back-right"}, **PERSON}],
           "shots": [{"at": 0, "target": ["a", "b"], "shot": "medium"}, {"at": 1, "target": "a", "shot": "close"}]}
    bad = opener3d.clean(raw, [], 2)[1]
    assert any(p.startswith("camera: the medium shot") and "a + b" in p for p in bad), bad
    raw["cutouts"][1]["place"] = {"beside": "a", "side": "right"}
    assert not opener3d.clean(raw, [], 2)[1]


def test_set_dressing_keeps_clear_of_what_was_placed():
    """opener3d.dress: edge pieces on every place, none touching a prop, a cut-out's spot or a picture on the wall."""
    for place in opener3d.PLACES:
        stage, bad = opener3d.clean({"place": place, "props": [], "cutouts": [{"name": "a", "place": {"mark": "centre"}, **PERSON}],
                                     "shots": [{"at": 0, "target": "a", "shot": "wide"}, {"at": 1, "target": "a", "shot": "close"}]}, [], 2)
        assert not bad and sum(p.get("dressing", False) for p in stage["props"]) >= 3, (place, stage["props"])
        assert all(not p.get("id") for p in stage["props"] if p.get("dressing"))  # no shot can aim at dressing
    # a stall the placer put where the street's stall would go: the street's own stall is left out
    mine = {"type": "stall", "id": "mine", "at": [-3.1, -5.2], "turn": 0, "size": 1}
    out = opener3d.dress("street", [mine], [])
    assert all(not (p["type"] == "stall") for p in out), out
    # someone standing by the bookcase: no bookcase; a picture on the wall: no lamp beside it
    out = opener3d.dress("room", [{"type": "frame", "at": [-1.5, 2.4], "turn": 0, "size": 1, "wall": True}],
                         [{"name": "b", "at": [3.0, -3.2], "height": 1.75, "aspect": .64}])
    assert "bookcase" not in [p["type"] for p in out] and "walllamp" not in [p["type"] for p in out], out


def look():
    """Renders the manual's example through the real path (cut-outs, Remotion) and its review sheet."""
    out = ROOT / "test_renders" / "opener3d" / "example"
    out.mkdir(parents=True, exist_ok=True)
    stage, bad = opener3d.clean(example(), WORDS, SECONDS)
    assert not bad, bad
    print(opener3d.render(stage, SECONDS, out) or f"wrote {out / 'opener.mp4'}")
    print(f"wrote {opener3d.sheet(out / 'opener.mp4', SECONDS, out / 'sheet.png', stage['shots'], out / 'cutouts')}")


if __name__ == "__main__":
    if sys.argv[1:] == ["--look"]:
        look()
        sys.exit(0)
    names = [n for n in sorted(globals()) if n.startswith("test_")]
    for n in names:
        globals()[n]()
        print(f"PASS {n}")
    print(f"{len(names)}/{len(names)} passed")
