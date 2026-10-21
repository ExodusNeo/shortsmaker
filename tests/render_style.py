"""Preview of every style-library preset for the owner: each look on two real photos from past Shorts, the overlays,
then every transition, each labelled in the caption area.
Usage: .venv\\Scripts\\python.exe tests\\render_style.py   ->  test_renders\\STYLE_PREVIEW.mp4. Never run during a batch."""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shortsmaker import config, style_lab  # noqa: E402

OUT = ROOT / "test_renders"
PHOTOS = ["job/jack0.jpg", "job/stink4.jpg"]  # Jack the Baboon (outdoor photo) and The Great Stink (wide interior)


def build() -> dict:
    scenes, words, flashes, t = [], [], [], 0.0

    def add(label: str, dur: float, early: float = 0.0, **scene) -> None:
        """`early`: show the label that many seconds before the scene, so a transition (which straddles the cut)
        plays under its own name."""
        nonlocal t
        scenes.append({"image": PHOTOS[0], "move": "in", "transition": "cut", "graphic": None, "card": None, "clip": None,
                       "start": round(t, 3), "end": round(t + dur, 3), **scene})
        for k, w in enumerate(label.split()):
            words.append({"start": t + 0.1 - early + k * 0.05, "end": t + dur - 0.1 - early, "text": w, "emphasis": k == 0,
                          "line": len(scenes)})
        t += dur

    for e in style_lab.style_library("look"):
        for k, photo in enumerate(PHOTOS):
            add(f"{e['name'].upper()} LOOK", 3, image=photo, look=e["name"], lookSeed=k + 1)
    for e in style_lab.style_library("overlay"):
        text = {"question": "WHY DID THEY KEEP HIM?", "kinetic": "THREE SOLDIERS"}.get(e["name"], e["name"].upper())
        add(f"{e['name'].upper()} OVERLAY", 3.5, graphic={"style": e["name"], "text": text, "at": t + 0.4})
    add("TRANSITIONS NEXT", 1.5, image=PHOTOS[1])
    for k, e in enumerate(style_lab.style_library("transition")):
        add(f"{e['name'].upper()} CUT", 2.5, early=0.7, image=PHOTOS[k % 2], transition=e["name"])
        if e["name"] == "flash":
            flashes.append(scenes[-1]["start"])
    palette = config.PALETTES[next(iter(config.PALETTES))]
    return {"fps": 30, "total": round(t, 3), "xfade": 0.3, "hook": "", "palette": palette, "scenes": scenes,
            "flashes": flashes, "words": words, "cta": None, "ctaLine": ""}


def main() -> None:
    job = config.REMOTION / "public" / "job"
    shutil.rmtree(job, ignore_errors=True)
    shutil.copytree(config.REMOTION / "test_props" / "media", job)
    OUT.mkdir(exist_ok=True)
    props = OUT / "STYLE_PREVIEW_props.json"
    props.write_text(json.dumps(build()), encoding="utf-8")
    out = OUT / "STYLE_PREVIEW.mp4"
    start = time.time()
    try:
        subprocess.run([shutil.which("npx"), "remotion", "render", "src/index.ts", "Short", str(out), f"--props={props}",
                        "--log=error", "--gl=angle", "--concurrency=4", "--x264-preset=ultrafast", "--crf=14"],
                       cwd=config.REMOTION, check=True)
    finally:
        shutil.rmtree(job, ignore_errors=True)
    print(f"{out} rendered in {time.time() - start:.0f}s")


if __name__ == "__main__":
    main()
