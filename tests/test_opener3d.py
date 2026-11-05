"""3D opener checks (shortsmaker/opener3d.py).
Run: .venv\\Scripts\\python.exe tests\\test_opener3d.py   (--look renders STAGE3D.md's example to test_renders/opener3d)"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shortsmaker import drawn_opener, opener3d  # noqa: E402

WORDS = [[0.1, 0.181, "The"], [0.221, 0.723, "ambassador"], [0.784, 1.206, "speaks,"], [1.648, 1.728, "and"],
         [1.769, 1.869, "his"], [1.949, 2.211, "wooden"], [2.311, 2.572, "eagle"], [2.653, 3.416, "broadcasts"],
         [3.497, 3.698, "every"], [3.778, 4.08, "word."]]
SECONDS = 4.47


def example() -> dict:
    text = (ROOT / "drawn" / "STAGE3D.md").read_text(encoding="utf-8")
    return json.loads(re.search(r"## Example.*?```json\n(.*?)```", text, re.S).group(1))


def test_example_is_clean():
    stage, bad = opener3d.clean(example(), WORDS, SECONDS)
    assert bad == [], bad
    assert stage["shots"][1]["at"] == 2.311  # "eagle" resolved to its spoken time
    assert stage["effects"][0]["at"] == 0 and stage["effects"][1]["at"] == 2.653 and stage["effects"][1]["on"] == "eagle"
    assert stage["cutouts"][0]["talk"] == [0.221, 4.4]


def test_bad_parts_go_back_to_the_coder():
    raw = example()
    raw["props"].append({"type": "spaceship", "at": [0, 0]})
    raw["cutouts"][0]["code"] += "\nconst x = Math.random();"
    raw["shots"].append({"at": 1, "target": "nobody", "distance": 2})
    stage, bad = opener3d.clean(raw, WORDS, SECONDS)
    text = " ".join(bad)
    assert "spaceship" in text and "Math.random" in text and "nobody" in text, bad
    assert all(p["type"] in opener3d.PROPS for p in stage["props"])


def test_a_shot_can_frame_several_things():
    raw = example()
    raw["shots"][0]["target"] = ["amb", "eagle"]
    stage, bad = opener3d.clean(raw, WORDS, SECONDS)
    assert bad == [] and stage["shots"][0]["target"] == ["amb", "eagle"], bad
    raw["shots"][0]["target"] = ["amb", "ghost"]
    assert any("ghost" in p for p in opener3d.clean(raw, WORDS, SECONDS)[1])


def test_lint_needs_draw():
    assert opener3d.lint_cutout("export default function draw(k, f) { k.person(1, 2, 3, {}); }") == []
    assert any("draw(k, f)" in p for p in opener3d.lint_cutout("export default function scene(k, t) {}"))
    assert any("process" in p for p in opener3d.lint_cutout("export default function draw(k, f) { process.exit(); }"))


def test_numbers_are_clamped():
    raw = example()
    raw["shots"][0].update(distance=999, fov=5)
    raw["cutouts"][0].update(frames=40, w=99999)
    stage, _ = opener3d.clean(raw, WORDS, SECONDS)
    assert stage["shots"][0]["distance"] == 14 and stage["shots"][0]["fov"] == 28
    assert stage["cutouts"][0]["frames"] == 6 and stage["cutouts"][0]["w"] == 1400


def test_shot_sizes_must_change():
    raw = example()
    raw["shots"][1]["distance"] = 3.5  # 3.9 vs 3.5: one framing twice (the McLean draft used 1.95-2.35 m)
    assert any("same size" in p for p in opener3d.clean(raw, WORDS, SECONDS)[1])
    raw["shots"][1]["over"] = "amb"  # looking past the ambassador at the eagle is a new size
    stage, bad = opener3d.clean(raw, WORDS, SECONDS)
    assert bad == [] and stage["shots"][1]["over"] == "amb", bad
    raw["shots"][1]["over"] = "eagle"  # over its own target: no
    assert any("looks over" in p for p in opener3d.clean(raw, WORDS, SECONDS)[1])


def test_hits_and_world_effects():
    raw = example()
    raw["cutouts"][0]["hits"] = ["eagle", 1.0]
    raw["effects"] += [{"type": "puff", "at": "eagle", "on": "amb"}, {"type": "jolt", "at": 1.0, "on": "amb"}]
    stage, bad = opener3d.clean(raw, WORDS, SECONDS)
    assert bad == [] and stage["cutouts"][0]["hits"] == [1.0, 2.311], bad
    assert [e["type"] for e in stage["effects"]][-2:] == ["puff", "jolt"]


KNOCK = "export default function draw(k, f) { const d = k.door(390, 1170, 3.8, {open: %s}); k.person(540, 1170, 3, {reach: [[d.knob[0], d.knob[1] - 135], null]}); }"


def test_a_knock_needs_a_closed_door_and_a_messenger_his_letter():
    """The 3D McLean opener (2026-11-05): a messenger with empty hands knocking on a half-open door."""
    narration = "A messenger knocked on his door."
    found = drawn_opener.missing_parts({"moment": "the messenger knocks", "code": KNOCK % "0.56"}, narration)
    assert any("OPEN door" in p for p in found) and any("letter" in p for p in found), found
    ok = KNOCK % "0" + " k.letter(1, 2, 1);"
    assert drawn_opener.missing_parts({"moment": "the messenger knocks", "code": ok}, narration) == []
    # a 3D door prop counts as the door, and its own `open` is checked too
    code = "export default function draw(k, f) { k.person(1, 2, 3, {}); k.letter(1, 2, 1); }"
    assert drawn_opener.missing_parts({"moment": "he knocks", "code": code}, "", {"door"}, [0]) == []
    assert any("OPEN" in p for p in drawn_opener.missing_parts({"moment": "he knocks", "code": code}, "", {"door"}, [0.6]))


def test_hold_counts_as_drawing_the_letter_and_scenery_stays_3d():
    code = "export default function draw(k, f) { k.person(1, 2, 3, {hold: [null, 'letter']}); }"
    assert drawn_opener.missing_parts({"moment": "the messenger waits", "code": code}) == []
    assert any("letter" in p for p in drawn_opener.missing_parts({"moment": "the messenger waits", "code": code.replace("letter", "cup")}))
    assert any("scenery" in p and "k.house" in p for p in opener3d.lint_cutout(
        "export default function draw(k, f) { k.house(1, 2, 3); k.person(1, 2, 3, {}); }"))
    assert opener3d.lint_cutout("export default function draw(k, f) { const d = k.door(1, 2, 3); k.person(1, 2, 3, {}); }") == []
    knock = "export default function draw(k, f) { k.knock(600, 1080, 3.4, {person: {hold: ['letter', null]}}); }"
    assert drawn_opener.missing_parts({"moment": "the messenger knocks", "code": knock}) == []


def test_against_puts_a_cutout_at_the_house_door_and_inside_is_rejected():
    raw = example()
    raw["place"] = "street"
    raw["props"] = [{"type": "house", "id": "home", "at": [0.4, -2.6]}]
    raw["cutouts"][0]["at"] = [0, -2.42]  # inside the house's walls (live McLean draft, 2026-11-06)
    raw["cutouts"] = raw["cutouts"][:1]
    raw["shots"] = [{"at": 0, "target": "amb", "distance": 4}, {"at": 1, "target": "amb", "distance": 2}]
    raw["effects"] = []
    assert any("inside home" in p for p in opener3d.clean(raw, WORDS, SECONDS)[1])
    raw["cutouts"][0]["against"] = "home"
    stage, bad = opener3d.clean(raw, WORDS, SECONDS)
    assert bad == [] and stage["cutouts"][0]["at"] == [0.4, -1.36], bad  # house 0: its door is module 1 (the middle)
    raw["cutouts"][0]["against"] = "nowhere"
    assert any("against" in p for p in opener3d.clean(raw, WORDS, SECONDS)[1])


def test_a_cutout_that_melts_into_the_wall_goes_back():
    from PIL import Image
    tmp = ROOT / "test_renders" / "opener3d" / "blend_test"
    (tmp / "cutouts").mkdir(parents=True, exist_ok=True)
    for name, colour in (("grocer", (122, 78, 44)), ("messenger", (40, 52, 96))):
        im = Image.new("RGBA", (100, 200), (0, 0, 0, 0))
        im.paste((*colour, 255), (20, 20, 80, 190))
        im.save(tmp / "cutouts" / f"{name}_0.png")
    stage = {"place": "room", "colors": {"wall": "#7E5A40"},
             "cutouts": [{"name": "grocer", "w": 100, "h": 200}, {"name": "messenger", "w": 100, "h": 200}]}
    found = opener3d.blends(stage, tmp)
    assert len(found) == 1 and found[0].startswith("grocer"), found
    assert opener3d.blends({**stage, "place": "street"}, tmp) == []


def test_the_preview_sees_every_shot():
    shots = [{"at": 0}, {"at": 1.409}, {"at": 2.396}]
    times = opener3d.sheet_times(4.47, shots)
    assert len(times) == 6 and times[0] == 0 and 1.76 in times and 2.75 in times, times
    assert len(opener3d.sheet_times(4.47)) == 6


def look():
    """Renders the manual's example through the real path (cut-outs, Remotion) and its review sheet."""
    out = ROOT / "test_renders" / "opener3d" / "example"
    out.mkdir(parents=True, exist_ok=True)
    stage, bad = opener3d.clean(example(), WORDS, SECONDS)
    assert not bad, bad
    print(opener3d.render(stage, SECONDS, out) or f"wrote {out / 'opener.mp4'}")
    print(f"wrote {opener3d.sheet(out / 'opener.mp4', SECONDS, out / 'sheet.png')}")


if __name__ == "__main__":
    if sys.argv[1:] == ["--look"]:
        look()
        sys.exit(0)
    names = [n for n in sorted(globals()) if n.startswith("test_")]
    for n in names:
        globals()[n]()
        print(f"PASS {n}")
    print(f"{len(names)}/{len(names)} passed")
