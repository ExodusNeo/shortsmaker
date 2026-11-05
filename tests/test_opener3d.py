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
    assert stage["cutouts"][0]["frames"] == 4 and stage["cutouts"][0]["w"] == 1400


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
