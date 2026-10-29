"""Shot templates (blender/shot_templates.json, 2026-10-28): every template, with every `of` choice and optional slot
it allows, filled from models in blender/assets/library and the real people library, must build headless and pass
every opener check. With --render each build is also rendered at 50% into cache/shot_templates/<name>.mp4 and a
contact strip <name>.jpg, to look at by eye. Real headless Blender, several minutes. No AI usage.
Run: .venv\\Scripts\\python.exe tests\\test_shot_templates.py [--render] [sample names]"""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shortsmaker import config, media_tools, opener_plan, opener_render  # noqa: E402

SAMPLES = {  # name -> the planner's reply; every template, and every pick and optional slot each one allows
    "chop_bird": {"template": "chop", "moment": "an axe chops a rooster's head off on a stump; the body staggers away",
                  "set": {"ground": "dirt", "light": "day", "backdrop": "barn"},
                  "fill": {"target": {"find": "rooster", "size_m": 0.55},
                           "block": {"find": "tree stump", "size_m": 1.2}, "tool": {"find": "axe", "size_m": 0.8}}},
    "slice": {"template": "slice", "moment": "a knife slices an onion into rings",
              "set": {"ground": "table", "light": "day", "backdrop": None},
              "fill": {"food": {"find": "onion", "size_m": 0.09}, "board": {"find": "cutting board", "size_m": 0.45},
                       "tool": {"find": "kitchen knife", "size_m": 0.3}, "slices": 5}},
    "falls_on_cheer": {"template": "falls_on", "moment": "a sack of onions topples onto a trader as a farmer cheers",
                       "set": {"ground": "wood floor", "light": "day", "backdrop": "warehouse"},
                       "fill": {"victim": "businessman", "thing": {"find": "gunny sack", "size_m": 1.2},
                                "witness": "farmer", "witness_does": "cheer"}},
    "falls_on_night": {"template": "falls_on", "moment": "a sack topples onto a worker as his boss cheers",
                       "set": {"ground": "stone", "light": "night", "backdrop": None},
                       "fill": {"victim": "worker", "thing": {"find": "gunny sack", "size_m": 0.9},
                                "witness": "businessman", "witness_does": "cheer"}},
    "falls_on_despair": {"template": "falls_on", "moment": "a sack topples onto a farmer; his wife hangs her head",
                         "set": {"ground": "dirt", "light": "dusk", "backdrop": "barn"},
                         "fill": {"victim": "farmer", "thing": {"find": "gunny sack", "size_m": 1.0},
                                  "witness": "woman", "witness_does": "despair"}},
    "hand_over_walk": {"template": "hand_over", "moment": "a dealer drops a briefcase and a con man walks off with it",
                       "set": {"ground": "stone", "light": "day", "backdrop": "eiffel tower"},
                       "fill": {"giver": "worker", "taker": "businessman", "item": "briefcase", "leaves": "walk"}},
    "hand_over_run": {"template": "hand_over", "moment": "a banker drops a bag of coins and a pirate runs off with it",
                      "set": {"ground": "wood floor", "light": "day", "backdrop": None},
                      "fill": {"giver": "victorian_gentleman", "taker": "pirate", "item": "coin bag", "leaves": "run"}},
    "sink_ship": {"template": "sink", "moment": "a warship tilts and sinks a mile into its maiden voyage",
                  "set": {"ground": "water", "light": "day", "backdrop": None},
                  "fill": {"ship": {"find": "ship", "size_m": 12}}},
    "chase_day": {"template": "chase", "moment": "a policeman chases a speeding driver down a country road",
                  "set": {"ground": "dirt", "light": "day", "backdrop": None},
                  "fill": {"runner": "victorian_gentleman", "chaser": "soldier_1800s"}},
    "chase_night": {"template": "chase", "moment": "guards chase an escaped prisoner through the snow",
                    "set": {"ground": "snow", "light": "night", "backdrop": "row house"},
                    "fill": {"runner": "man", "chaser": "ww2_soldier"}},
    "drink_collapse": {"template": "drink", "moment": "a doctor drinks a beaker of bacteria and collapses",
                     "set": {"ground": "wood floor", "light": "day", "backdrop": None},
                     "fill": {"drinker": "doctor", "cup": "beaker", "after": "collapse"}},
    "drink_despair": {"template": "drink", "moment": "a farmer drinks the rainmaker's tonic and hangs his head",
                      "set": {"ground": "dirt", "light": "dusk", "backdrop": "barn"},
                      "fill": {"drinker": "farmer", "cup": "mug", "after": "despair"}},
    "drink_cheer": {"template": "drink", "moment": "the ship's baker downs a bottle of whiskey and cheers",
                    "set": {"ground": "wood floor", "light": "night", "backdrop": None},
                    "fill": {"drinker": "chef", "cup": "bottle", "after": "cheer"}},
}
SECONDS = 3.0
OUT = ROOT / "cache" / "shot_templates"


def build(name: str, render: bool) -> dict:
    plan = opener_plan.fill_template(copy.deepcopy(SAMPLES[name]))
    assert plan, f"{name}: the fill is not clean"
    plan = opener_render.scale_beats(plan, SECONDS)
    models, why = opener_render.resolve_models(plan)
    assert not why, f"{name}: {why}"
    d = Path(tempfile.mkdtemp(prefix=f"shot_{name}_"))
    job = {"plan": plan, "models": models, "seconds": SECONDS, "fps": 30, "size": [1080, 1920],
           "frames_dir": str(d / "frames"), "report": str(d / "report.json"), "render": render,
           "render_failed": False, "render_scale": 50,
           "people": {"blend": str(config.PEOPLE_BLEND), "json": str(config.PEOPLE_JSON)}}
    (d / "job.json").write_text(json.dumps(job), encoding="utf-8")
    r = subprocess.run([str(config.BLENDER), "-b", "--factory-startup", "--python-exit-code", "1", "--python",
                        str(opener_render.SCRIPT), "--", str(d / "job.json")], capture_output=True, text=True, timeout=900)
    assert r.returncode == 0 and (d / "report.json").exists(), (r.stdout or "")[-2000:] + (r.stderr or "")[-2000:]
    report = json.loads((d / "report.json").read_text(encoding="utf-8"))
    if render and report.get("ok"):
        from PIL import Image
        OUT.mkdir(parents=True, exist_ok=True)
        frames = d / "frames"
        media_tools.ffmpeg("-y", "-framerate", "30", "-i", str(frames / "f_%04d.png"), "-pix_fmt", "yuv420p",
                           f"{name}.mp4", cwd=OUT)
        picked = opener_render.review_frames(report, len(list(frames.glob("f_*.png"))))
        tiles = [Image.open(frames / f"f_{f:04d}.png").convert("RGB").resize((216, 384)) for f in picked]
        strip = Image.new("RGB", (216 * len(tiles), 384))
        for i, t in enumerate(tiles):
            strip.paste(t, (216 * i, 0))
        strip.save(OUT / f"{name}.jpg", quality=88)
    shutil.rmtree(d, ignore_errors=True)
    return report


def test_every_template_has_samples():
    assert {s["template"] for s in SAMPLES.values()} == set(opener_plan.TEMPLATES)


if __name__ == "__main__":
    render = "--render" in sys.argv
    names = [a for a in sys.argv[1:] if a != "--render"] or list(SAMPLES)
    test_every_template_has_samples()
    failed = 0
    for n in names:
        try:
            rep = build(n, render)
            ok = rep.get("ok") and not rep.get("failures")
            print(("PASS " if ok else "FAIL ") + n + ("" if ok else f": {rep.get('failures')}"))
            failed += not ok
        except AssertionError as e:
            failed += 1
            print(f"FAIL {n}: {str(e)[:1500]}")
    print(f"{len(names) - failed}/{len(names)} passed")
    sys.exit(1 if failed else 0)
