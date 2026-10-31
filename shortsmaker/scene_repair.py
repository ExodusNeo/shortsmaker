"""Preview and apply a callout repair using existing video/audio, without new AI or narration."""
import copy
import json
import math
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from shortsmaker import checkpoints, edit_project, media_tools, review, short_render
from shortsmaker.config import FPS, MUSIC, REMOTION


def preview(folder: Path, state: dict, index: int) -> Path:
    """Fast path for a mark card on a still, with hard cuts on both sides. Preserve original captions below it."""
    work = folder / "work"
    props = json.loads((work / "props.json").read_text(encoding="utf-8"))
    old = props["scenes"][index]
    graphic = state["short"]["scenes"][index].get("graphic")
    if (old.get("graphic") or {}).get("style") != "mark" or graphic and graphic.get("style") != "mark":
        raise ValueError("Fast preview currently supports circle/arrow cards; use the normal repair for other graphics.")
    if old.get("clip") or old.get("full") or old.get("card") or old.get("transition") != "cut" or (
            index + 1 < len(props["scenes"]) and props["scenes"][index + 1].get("transition") != "cut"):
        raise ValueError("This scene has a clip or overlapping transition; use the normal repair with cached narration.")
    if graphic and not all(type(graphic.get(key)) in (int, float) and math.isfinite(graphic[key])
                           and 0 <= graphic[key] <= 1 for key in ("x", "y")):
        raise ValueError("Callout coordinates must be between 0 and 100 percent.")
    repair = work / "repairs" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    repair.mkdir(parents=True)
    assets = REMOTION / "public" / ("repair-" + repair.name)
    assets.mkdir()
    original_props = copy.deepcopy(props)
    start, end = math.ceil(old["start"] * FPS), math.ceil(old["end"] * FPS) - 1
    try:
        for k, scene in enumerate(props["scenes"]):
            source = work / f"{k}.jpg"
            if not source.exists():
                source = work / f"{index}.jpg"
            shutil.copy2(source, assets / f"{k}.jpg")
            scene["image"] = f"{assets.name}/{k}.jpg"
            # Other scenes are outside this frame range; do not preload their clips/custom graphics.
            if k != index:
                scene["clip"], scene["full"], scene["card"] = None, None, None
        raw = work / f"{index}_raw.jpg"
        shutil.copy2(raw, assets / "raw.jpg")
        props["scenes"][index]["graphic"] = ({**old["graphic"], **graphic, "image": f"{assets.name}/raw.jpg"}
                                               if graphic else None)
        props.pop("layer", None)
        props["words"] = []  # the original video's captions are retained below the card
        path = repair / "props.json"
        media_tools.write_json(path, props)
        subprocess.run([shutil.which("npx") or "npx", "remotion", "render", "src/index.ts", "Short",
                        str(repair / "scene.mp4"), f"--props={path}", f"--frames={start}-{end}",
                        "--log=error", "--gl=angle", "--concurrency=4", "--x264-preset=ultrafast", "--crf=14"],
                       cwd=REMOTION, check=True, timeout=600)
        duration = (end - start + 1) / FPS
        media_tools.ffmpeg("-ss", f"{start / FPS:.9f}", "-i", str(folder / "short.mp4"),
                           "-i", str(repair / "scene.mp4"), "-filter_complex",
                           "[1:v]crop=1080:1100:0:0[patch];[0:v][patch]overlay=0:0[v]",
                           "-map", "[v]", "-map", "0:a?", *media_tools.video_encoder(), "-c:a", "aac",
                           "-t", f"{duration:.9f}", "-movflags", "+faststart", "preview.mp4", cwd=repair)
        media_tools.ffmpeg("-i", "preview.mp4", "-vf", "fps=2,scale=270:-2,tile=6x1", "-frames:v", "1",
                           "sheet.jpg", cwd=repair)
        media_tools.write_json(repair / "repair.json", {"index": index, "start": start, "end": end,
                                                        "graphic": graphic, "props": original_props})
        return repair / "preview.mp4"
    finally:
        # Only the exact files created for this isolated preview, never the shared job directory.
        for file in assets.iterdir():
            file.unlink()
        assets.rmdir()


def apply(folder: Path, state: dict, preview_path: Path) -> None:
    repair, work = preview_path.parent, folder / "work"
    data = json.loads((repair / "repair.json").read_text())
    start, end = data["start"], data["end"]
    if state["short"]["scenes"][data["index"]].get("graphic") != data["graphic"]:
        raise ValueError("The callout changed after preview; make another preview first.")
    media_tools.ffmpeg("-i", str(folder / "short.mp4"), "-i", str(repair / "scene.mp4"), "-filter_complex",
                       f"[1:v]crop=1080:1100:0:0,setpts=PTS+{start}/{FPS}/TB[patch];"
                       "[0:v][patch]overlay=0:0:eof_action=pass:repeatlast=0[v]",
                       "-map", "[v]", "-map", "0:a?", *media_tools.video_encoder(), "-pix_fmt", "yuv420p",
                       "-c:a", "copy", "-movflags", "+faststart", "fixed.mp4", cwd=repair)
    if abs(media_tools.duration(repair / "fixed.mp4") - media_tools.duration(folder / "short.mp4")) > 1 / FPS:
        raise ValueError("Repair changed the video length; the original was kept.")
    for name in ("short.mp4", "edit_plan.txt", "storyboard.jpg", "edit.mlt", "edit_in_shotcut.bat"):
        if (folder / name).exists():
            shutil.copy2(folder / name, repair / ("original-" + name))
    for name in ("state.json", "props.json", "render-context.json"):
        if (work / name).exists():
            shutil.copy2(work / name, repair / ("original-" + name))
    (repair / "fixed.mp4").replace(folder / "short.mp4")
    props = data["props"]
    index, graphic = data["index"], data["graphic"]
    old = props["scenes"][index]["graphic"]
    props["scenes"][index]["graphic"] = {**old, **graphic} if graphic else None
    media_tools.write_json(work / "props.json", props)
    review.review_status(state["short"], "Visual review", "Not reviewed", "manual callout repair; inspect the preview")
    short_render.save_state(work, state["short"], state["choices"], MUSIC / state["music"] if state.get("music") else None,
                            set(state.get("by_gemini", [])))
    plan = folder / "edit_plan.txt"
    lines = [line for line in plan.read_text(encoding="utf-8").splitlines()
             if "Review status: Visual review:" not in line]
    current = 0
    for k, line in enumerate(lines):
        if "]  SCENE " in line:
            current = int(line.split("]  SCENE ")[1].split()[0])
        if current == index + 1 and line.startswith("  GRAPHIC:"):
            lines[k] = (f"  GRAPHIC: repaired {graphic.get('shape', 'circle')} at {graphic['x']:.0%} across / "
                        f"{graphic['y']:.0%} down; label {graphic['text']}" if graphic else "  GRAPHIC: removed in manual repair")
    lines += ["", f"Manual callout repair: scene {index + 1}; original audio retained. Backup/preview: {repair}",
              "  Review status: Visual review: Not reviewed (manual repair; inspect preview)"]
    plan.write_text("\n".join(lines) + "\n", encoding="utf-8")
    bounds = [scene["start"] for scene in props["scenes"]] + [props["total"]]
    review.storyboard(folder / "short.mp4", bounds, folder / "storyboard.jpg")
    edit_project.remove(folder)  # archived above: the old layered timeline no longer matches
