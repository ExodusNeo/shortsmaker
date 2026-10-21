"""Automatic checks on a finished Short, the AI visual review and its fixes (incl. repainting a scene, also used by
fix.bat), the storyboard."""

import io
import json
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from shortsmaker import gpu, llm, media_tools, picker, plan_rules, remotion_render, session, short_render, writing
from shortsmaker.config import FONT


def quality_check(video: Path, bounds: list[float], sources: list[str]) -> list[str]:
    """Automatic checks on the finished Short, using ffmpeg's own detectors in one pass: black or
    frozen stretches, loudness off target or clipping, scenes with no picture, unplanned length.
    Returns the problems worth a look before uploading ([] = all clear)."""
    def where(t: float) -> str:
        k = next((k for k in range(len(bounds) - 1) if bounds[k] <= t < bounds[k + 1]), len(bounds) - 2)
        return f"{media_tools.clock(t)} (scene {k + 1})"
    log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video),
                          "-vf", "blackdetect=d=0.25:pix_th=0.08,freezedetect=n=0.002:d=2.5",
                          "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True, errors="replace").stderr
    if "Error opening input" in log or "Invalid data found" in log:
        return ["couldn't check the video: the file is missing or unreadable"]
    issues = [f"black screen at {where(float(t))}" for t in re.findall(r"black_start:\s*([\d.]+)", log)]
    issues += [f"picture frozen for 2.5s+ at {where(float(t))}" for t in re.findall(r"freeze_start:\s*([\d.]+)", log)]
    lufs, peak = re.findall(r"I:\s+(-?[\d.]+) LUFS", log), re.findall(r"Peak:\s+(-?[\d.]+) dBFS", log)
    if not lufs:
        issues.append("no sound found in the video")
    elif not -16 <= float(lufs[-1]) <= -12:  # the last match is ffmpeg's summary for the whole video
        issues.append(f"loudness {float(lufs[-1]):.1f} LUFS, target is -14 (too {'quiet' if float(lufs[-1]) < -16 else 'loud'})")
    if peak and float(peak[-1]) > -0.5:
        issues.append(f"sound peaks at {float(peak[-1]):.1f} dB, close to distorting")
    issues += [f"scene {k + 1} has no picture (plain frame)" for k, src in enumerate(sources) if src.startswith("PLAIN")]
    if bounds[-1] > (36 if session.SHORT_FORM else 62):
        issues.append(f"{media_tools.clock(bounds[-1])} long, past the planned {writing.length_plan()[4]} seconds")
    return issues


def visual_review(video: Path, short: dict, bounds: list[float], sources: list[str], work: Path) -> tuple[list[str], dict[int, tuple[str, str]]]:
    """The AI watches the finished Short as sheets of one frame per second and reports what a viewer would
    notice (the 2026-10-15 Cardiff review found smoke blobs, an invented face and another trial's caption only
    by eye). One AI call; its findings join the CHECK lines. Failure means no findings."""
    folder = work / "review"
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir()
    try:  # 6x5 tiles = 30 seconds per sheet
        media_tools.ffmpeg("-i", str(video), "-vf", "fps=1,scale=300:-2,tile=6x5", "-fps_mode", "vfr", "sheet%d.jpg", cwd=folder)
    except subprocess.CalledProcessError:
        return [], {}
    sheets = sorted(folder.glob("sheet*.jpg"), key=lambda p: int(p.stem[5:]))
    plan = "\n".join(f"scene {i + 1} ({media_tools.clock(bounds[i])}-{media_tools.clock(bounds[i + 1])}): \"{sc['narration']}\" | picture: {src[:160]}"
                     for i, (sc, src) in enumerate(zip(short["scenes"], sources)))
    data = llm.ask_ai(f"""You are the final reviewer of a YouTube Short: "{short['title']}". Open and look at each sheet:
{chr(10).join(f"{p} (seconds {30 * k}-{30 * k + 29}, one frame per second, left to right, top to bottom)" for k, p in enumerate(sheets))}
The plan: {plan}
Report only problems a viewer would notice: AI artifacts (smoke or fog blobs, melting or warped people,
faces or objects), text or graphics covering a face, a picture that doesn't match its line or shows the
wrong era/place/person, unreadable, washed-out or nearly blank pictures, printed captions, logos or
watermarks on a real photo or film, a painted or AI picture standing in for a real person or object as if it
were real. Writing inside an AI-GENERATED painting is allowed when it is real, readable words that fit the
story; garbled or made-up lettering there is a problem (fix "repaint"). Ignore
the captions, the subscribe button and normal crossfades. No problems: an empty list.
fix = "repaint" when showing a different picture in that scene would fix it (wrong or blank picture, AI
artifacts, captions/logos in footage, someone else's AI art posing as real); "graphic" when the scene's line is
about places, a number, a document, a mechanism, or a cause-and-effect chain and a full-screen motion graphic
(map journey, big number, document, or custom animated diagram) would show it better than any picture; null
otherwise (e.g. a graphic covering a face).
Reply with ONLY JSON: {{"problems": [{{"second": 12, "scene": 3, "what": "a white smoke cloud covers the statue", "fix": "repaint"}}]}}""",
                  fatal=False, read_dir=folder)
    return review_fixes(data, len(short["scenes"]))


def review_fixes(data, n_scenes: int) -> tuple[list[str], dict[int, tuple[str, str]]]:
    """The review's reply -> (CHECK lines, scene -> ("repaint" | "graphic", why)). Scene 1 is never turned into a
    graphic (the hook keeps a picture); an older-style `repaint: true` still means repaint."""
    found, fixes = [], {}
    for p in (data or {}).get("problems") or []:
        if isinstance(p, dict) and str(p.get("what") or "").strip():
            sec = p.get("second") if plan_rules.is_num(p.get("second")) else None
            what = str(p["what"]).strip()[:200]
            n = p.get("scene") if isinstance(p.get("scene"), int) and 1 <= p["scene"] <= n_scenes else None
            found.append(f"LOOK{f' at {media_tools.clock(sec)}' if sec is not None else ''}{f' (scene {n})' if n else ''}: {what}")
            kind = p.get("fix") if p.get("fix") in ("repaint", "graphic") else "repaint" if p.get("repaint") is True else None
            if n and kind:
                fixes.setdefault(n - 1, ("repaint" if n == 1 else kind, what))
    return found[:8], fixes


def apply_review_fixes(st: dict, work: Path, fixes: dict[int, tuple[str, str]]) -> list[str]:
    """The automatic fixes after a render's review (up to AUTO_REPAINT_MAX scenes per round): "graphic" scenes
    become a full-screen motion graphic when one fits their line, a custom motion graphic that looked wrong is
    redrawn by its coder, the rest get a new painted picture.
    Returns the edit-plan notes."""
    fixed = list(fixes.items())[:short_render.AUTO_REPAINT_MAX]
    want = [i for i, (kind, _) in fixed if kind == "graphic"]
    got = set(picker.rescue_graphics(st["short"], want, {i: why for i, (_, why) in fixed})) if want else set()
    # Same slot numbering as render_remotion (the k-th custom scene uses slot k).
    # shortcut: a rescue that adds a custom scene before this one shifts the slots and the redraw is re-coded fresh.
    customs = [k for k, sc in enumerate(st["short"]["scenes"]) if (sc.get("full") or {}).get("type") == "custom"]
    notes, repaint = [], {}
    for i, (_, why) in fixed:
        if i in customs and remotion_render.redraw_custom(st["short"], i, min(3, customs.index(i)), why, work):
            notes.append(f"scene {i + 1}'s motion graphic was redrawn ({why})")
        elif i in got:  # the picture stays in the plan: it is the fallback if Remotion fails
            notes.append(f"scene {i + 1} became a motion graphic ({why})")
        else:
            paint_new(work, st, i)
            repaint[i] = why
    rewritten = rewrite_paint_prompts(st["short"], repaint) if repaint else []
    for i, why in repaint.items():
        how = "a rewritten prompt" if i in rewritten else "its old prompt, seen from a new angle"
        notes.append(f"scene {i + 1} got a new painted picture from {how} ({why})")
    return notes


def storyboard(video: Path, bounds: list[float], path: Path) -> None:
    """One mid-scene frame per scene from the finished video, labeled with its timestamps."""
    n, cols, tw, th = len(bounds) - 1, 4, 270, 480
    rows = (n + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 12, rows * (th + 52) + 12), (20, 20, 24))
    d, font = ImageDraw.Draw(sheet), ImageFont.truetype(FONT, 30)
    for i in range(n):
        x, y = 12 + (i % cols) * (tw + 12), 12 + (i // cols) * (th + 52)
        still = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{(bounds[i] + bounds[i + 1]) / 2:.2f}",
                                "-i", str(video), "-frames:v", "1", "-vf", f"scale={tw}:{th}", "-f", "image2pipe",
                                "-vcodec", "png", "-"], capture_output=True).stdout
        if still:
            sheet.paste(Image.open(io.BytesIO(still)).convert("RGB"), (x, y))
        d.text((x, y + th + 8), f"{i + 1}  {media_tools.clock(bounds[i])}-{media_tools.clock(bounds[i + 1])}", font=font, fill="white")
    sheet.save(path, quality=88)


def paint_new(work: Path, state: dict, i: int) -> None:
    """fix / auto-fix: scene i drops its picture and gets a freshly painted one (Gemini, else SDXL
    on this PC) from its ai_image prompt, or one built from its shot note, in the same never-a-photo style."""
    sc = state["short"]["scenes"][i]
    sc["full"] = None  # a painting replaces whatever the scene showed, motion graphic included
    if (sc.get("graphic") or {}).get("style") == "mark":  # it circled a detail of the old picture
        sc["graphic"] = None
    state["choices"][i] = {"bg": None, "person": state["choices"][i]["person"]}
    old = work / f"ai{i}.jpg"
    old.unlink(missing_ok=True)  # render() only paints what's missing
    state["by_gemini"] = [p for p in state["by_gemini"] if p != str(old)]
    if not sc.get("ai_image"):
        sc["ai_image"] = f"{sc.get('shot') or sc['narration']} {gpu.PAINT_FALLBACK}"
    sc["animate"] = False


def rewrite_paint_prompts(short: dict, why: dict[int, str]) -> list[int]:
    """Scenes being repainted (scene index -> what was wrong) get a better ai_image, not the same one again: MOSS
    seeds from the prompt text, so an unchanged prompt painted the identical picture (Mike's garbled newsstand came
    back, 2026-10-21; owner asked for a rewrite on every repaint). One AI call for all of them; a scene it doesn't
    answer gets a new angle so the picture still changes. Returns the scenes the AI rewrote."""
    scenes = short["scenes"]
    rows = [{"scene": i + 1, "narration": scenes[i]["narration"], "shot": scenes[i].get("shot"),
             "old_prompt": scenes[i].get("ai_image"), "problem": why[i]} for i in why]
    data = llm.ask_ai(f"""Some AI paintings in a YouTube Short were rejected and will be painted again. Story: {short.get('topic') or short.get('title')}
For each scene write a NEW painting prompt that fixes its problem and is better than the old prompt. Don't repeat
what failed: if the old subject can't work (it shows what must not be shown, or the painter keeps getting it wrong),
pick another subject that still shows the narration. Rules for a prompt:
{writing.AI_IMAGE_RULE}
Scenes: {json.dumps(rows, ensure_ascii=False)}
Reply with ONLY JSON: {{"prompts": [{{"scene": 3, "ai_image": "..."}}]}}""", fatal=False) or {}
    done = []
    for p in data.get("prompts") or []:
        i = p.get("scene") - 1 if isinstance(p, dict) and isinstance(p.get("scene"), int) else None
        text = str(p.get("ai_image") or "").strip() if i is not None else ""
        if i in why and i not in done and text and text != scenes[i].get("ai_image") and "photograph" not in text.lower():
            scenes[i]["ai_image"] = text[:700]
            done.append(i)
    for i in why:
        if i not in done:
            scenes[i]["ai_image"] = f"{scenes[i]['ai_image']} Seen from a different angle, in different light."
    return done
