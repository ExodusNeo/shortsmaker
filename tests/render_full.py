"""Render one full-screen motion graphic test scene through the real Short composition.
Usage: .venv\\Scripts\\python.exe tests\\render_full.py remotion\\test_props\\<name>.json [--still SECONDS]
A test props file is {"total": 6, "narration": "words spread evenly as captions", "scenes": [{"start", "end", "full"}]}.
Output: test_renders\\<name>.mp4 (or .png) and <name>_sheet.jpg (4 frames per second). Never run during a batch."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REMOTION = ROOT / "remotion"
OUT = ROOT / "test_renders"


def props_for(test: dict) -> dict:
    words = test.get("narration", "").split()
    total = test["total"]
    step = total / max(1, len(words))
    return {"fps": 30, "total": total, "xfade": 0.3, "hook": "", "flashes": [], "cta": None, "ctaLine": "",
            "palette": test.get("palette"),
            "scenes": [{"image": "", "move": "in", "transition": "fade", "graphic": None, "card": None, "clip": None,
                        **sc} for sc in test["scenes"]],
            "words": [{"start": k * step, "end": (k + 0.9) * step, "text": w, "emphasis": False, "line": k // 3}
                      for k, w in enumerate(words)]}


def main() -> None:
    src = Path(sys.argv[1]).resolve()
    still = float(sys.argv[sys.argv.index("--still") + 1]) if "--still" in sys.argv else None
    test = json.loads(src.read_text(encoding="utf-8"))
    if not test.get("palette"):
        test.pop("palette", None)
    OUT.mkdir(exist_ok=True)
    job = REMOTION / "public" / "job"
    shutil.rmtree(job, ignore_errors=True)
    shutil.copytree(REMOTION / "test_props" / "media", job)
    props = OUT / f"{src.stem}_props.json"
    props.write_text(json.dumps({k: v for k, v in props_for(test).items() if v is not None or k == "cta"}), encoding="utf-8")
    npx = shutil.which("npx")
    try:
        if still is not None:
            out = OUT / f"{src.stem}.png"
            subprocess.run([npx, "remotion", "still", "src/index.ts", "Short", str(out), f"--props={props}",
                            f"--frame={round(still * 30)}", "--log=error", "--gl=angle"], cwd=REMOTION, check=True)
        else:
            out = OUT / f"{src.stem}.mp4"
            subprocess.run([npx, "remotion", "render", "src/index.ts", "Short", str(out), f"--props={props}",
                            "--log=error", "--gl=angle", "--concurrency=4", "--x264-preset=ultrafast", "--crf=18"],
                           cwd=REMOTION, check=True)
            cols = 8
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out), "-vf",
                            f"fps=4,scale=180:-1,tile={cols}x{-(-int(test['total'] * 4) // cols)}",
                            "-frames:v", "1", str(OUT / f"{src.stem}_sheet.jpg")], check=True)
    finally:
        shutil.rmtree(job, ignore_errors=True)
    print(out)


if __name__ == "__main__":
    main()
