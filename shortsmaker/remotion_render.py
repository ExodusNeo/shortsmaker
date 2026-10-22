"""Rendering a Short with Remotion (with the Python renderer as fallback), redraws, paper and ink."""

import json
import random
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

from shortsmaker import audio_mix, gpu, llm, media_tools, motion, photo_prep, style_lab
from shortsmaker.config import FPS, PALETTES, REMOTION, REMOTION_MIN_GRAPHICS, REMOTION_ONLY, XFADE, hex_rgb, short_skin


def wants_remotion(scenes: list[dict], n_graphics: int) -> bool:
    """Remotion renders when the plan is graphics-heavy or uses anything only it can draw: a full-screen motion
    graphic, a Remotion-only graphic, a map route, a photo look, or a scene change other than fade/flash."""
    return n_graphics >= REMOTION_MIN_GRAPHICS or any(
        sc.get("full") or sc.get("look") or sc.get("transition", "fade") not in ("fade", "flash")
        or (sc["graphic"] and (sc["graphic"]["style"] in REMOTION_ONLY or "from" in sc["graphic"])) for sc in scenes)


def run_remotion_with_fallback(render, props: dict, used: dict) -> dict:
    """render(props); if it fails while AI inventions are in use, they are swapped for their library fallbacks and
    the render runs once more. Returns the inventions that made it into the video ({kind: spec})."""
    try:
        render(props)
        return used
    except Exception as e:
        if not used:
            raise
        print(f"    an invented style broke the render ({str(e)[:120]}): using the library fallbacks")
        style_lab.restore_style_slots()
        style_lab.swap_inventions(props, used)
        render(props)
        return {}


def redraw_custom(short: dict, i: int, slot: int, why: str, work: Path) -> bool:
    """The review saw custom scene i look wrong: its coder gets the complaint and its current code, rewrites it once,
    and the fix replaces the cached code (same signature line, so the re-render uses it). False = not fixed."""
    cached = work / f"Custom{slot}.tsx"
    if not cached.exists():
        return False
    sig, _, code = cached.read_text(encoding="utf-8").partition("\n")
    print(f"    redrawing the motion graphic of scene {i + 1} ({why[:80]})...")
    data = llm.ask_ai(f"""You wrote the Remotion component `Custom{slot}` below for scene {i + 1} of the YouTube Short
"{short['title']}" (narration: {short['scenes'][i]['narration']!r}). The finished video was reviewed and this scene
looked wrong: {why!r}
Rewrite the component to fix exactly that.
{motion.custom_rules(slot)}
Current code:
{code}
Reply with ONLY JSON: {{"code": "import React from 'react';\\n..."}}""", fatal=False)
    new = motion.clean_tsx_code((data or {}).get("code"), slot)
    if not new or motion.lint_custom_code(new):
        return False
    target = REMOTION / "src" / "full" / "generated" / f"Custom{slot}.tsx"
    before = target.read_text(encoding="utf-8") if target.exists() else None
    try:  # the check needs the code in the project; the project's own slot file is put back afterwards
        target.write_text(sig + "\n" + new, encoding="utf-8")
        if motion.tsc_check() is not None:
            return False
    finally:
        if before is not None:
            target.write_text(before, encoding="utf-8")
    cached.write_text(sig + "\n" + new, encoding="utf-8")
    return True


def paint_instead(short: dict, work: Path, idx: list[int], images: list, sources: list[str]) -> set[str]:
    """Remotion failed: the full-screen motion graphic scenes get a painted picture (Gemini, else this PC) so the
    built-in renderer can still finish the Short. Returns the pictures Gemini made."""
    items = [{"prompt": short["scenes"][i]["ai_image"]
              or f"{short['scenes'][i].get('shot') or short['scenes'][i]['narration']} {gpu.PAINT_FALLBACK}",
              "out": str(work / f"ai{i}.jpg")} for i in idx]
    by_moss = gpu.moss_images(items, work)  # same painter order as render(): MOSS, Gemini, SDXL
    made = gpu.gemini_images([it for it in items if it["out"] not in by_moss], work) if shutil.which("agy") else set()
    rest = [it for it in items if it["out"] not in made | by_moss]
    if rest:
        gpu.local_job("images", rest, work, timeout=900)
    for i, it in zip(idx, items):
        short["scenes"][i]["full"] = None
        if Path(it["out"]).exists():
            for name in (f"{i}.jpg", f"{i}_raw.jpg"):
                shutil.copy(it["out"], work / name)
            photo_prep.to_vertical(work / f"{i}.jpg")
            images[i] = Image.open(work / f"{i}.jpg").convert("RGB")
            maker = ("by Gemini" if it["out"] in made else "on this PC (MOSS-Image)" if it["out"] in by_moss
                     else "on this PC (SDXL-Lightning)")
            sources[i] = f"AI-GENERATED {maker}: \"{it['prompt']}\" (painted instead of the motion graphic: Remotion failed)"
        else:
            sources[i] += " (the motion graphic could not be drawn because Remotion failed; this picture stands in)"
    return made


FIGURE_PROMPT = ("A single {thing}, full body in side view, drawn as one solid flat black ink silhouette on a plain pure "
                 "white background. No text, no ground, no shadow, no frame, nothing else in the picture; centered, a "
                 "simple clear shape that reads at a small size.")


def ink_silhouette(src: Path, dst: Path) -> bool:
    """A painted figure (dark ink on light paper) -> a cropped RGBA silhouette (dark ink, transparent paper, at most
    256 px) for the big-number scene. False when the painting has no clear single shape (blank, or mostly ink)."""
    with Image.open(src) as im:
        gray = ImageOps.autocontrast(im.convert("L"))
    ink = gray.point(lambda v: 255 if v < 110 else 0)  # alpha: dark = figure
    share = sum(ink.histogram()[255:]) / (ink.width * ink.height)
    box = ink.getbbox()
    if not box or not 0.02 <= share <= 0.6:
        return False
    ink = ink.crop(box).filter(ImageFilter.GaussianBlur(0.8))  # soft edge, no jaggies when scaled
    ink.thumbnail((256, 256))
    fig = Image.new("RGBA", ink.size, (20, 15, 10, 0))
    fig.putalpha(ink)
    fig.save(dst)
    return True


def make_paper(folder: Path = REMOTION / "public" / "paper") -> None:
    """The aged-paper texture and film-grain frames the full-screen motion graphics draw on (style A,
    "archival documentary"). Made once with Pillow, so no downloaded textures and no licences."""
    folder.mkdir(parents=True, exist_ok=True)
    if not (folder / "paper.jpg").exists():
        w, h = 1300, 2300
        rnd = random.Random(7)
        paper = Image.new("RGB", (w, h), hex_rgb("#eadcbf"))
        shade = Image.effect_noise((26, 46), 60).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40))
        paper = Image.composite(paper, Image.new("RGB", (w, h), hex_rgb("#cdb88f")), shade.point(lambda v: min(255, v + 70)))
        fibres = Image.effect_noise((w, h // 12), 35).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1))
        paper = Image.composite(paper, Image.new("RGB", (w, h), hex_rgb("#bfa77c")), fibres.point(lambda v: 255 if v > 90 else 200))
        stains = Image.new("L", (w, h), 0)
        d = ImageDraw.Draw(stains)
        for _ in range(3):
            x, y, r = rnd.randrange(w), rnd.randrange(h), rnd.randrange(120, 320)
            d.ellipse((x - r, y - r * 0.8, x + r, y + r * 0.8), outline=60, width=rnd.randrange(6, 14))
            d.ellipse((x - r, y - r * 0.8, x + r, y + r * 0.8), fill=18)
        paper = Image.composite(Image.new("RGB", (w, h), hex_rgb("#9c7d4c")), paper, stains.filter(ImageFilter.GaussianBlur(12)))
        paper.save(folder / "paper.jpg", quality=90)
    for k in range(6):
        if not (folder / f"grain{k}.png").exists():
            alpha = Image.effect_noise((1080, 1920), 50).point(lambda v: min(45, abs(v - 128) // 2))
            grain = Image.new("RGBA", (1080, 1920), (40, 28, 12, 0))
            grain.putalpha(alpha)
            grain.save(folder / f"grain{k}.png")


def render_remotion(short: dict, cues: list[dict], bounds: list[float], total: float,
                    words: list[tuple[float, float, str]], work: Path, emphasis: set[float],
                    flashes: set[float], clips: dict[int, Path], full_pics: dict[int, list] | None = None,
                    layers: bool = False) -> Path:
    """Render the silent video (with captions) through the Remotion project; returns the mp4. With `layers` (the
    Shotcut timeline) it makes work/pictures.mp4 and work/graphics.mov (see-through) instead, without captions."""
    npx = shutil.which("npx")
    if not npx or not (REMOTION / "node_modules" / "remotion").exists():
        raise RuntimeError("Remotion isn't installed")
    job = REMOTION / "public" / "job"  # Remotion can only load images from its public folder
    shutil.rmtree(job, ignore_errors=True)
    job.mkdir(parents=True)
    make_paper()  # paper + grain for the full-screen motion graphics (made once)
    style_lab.restore_style_slots()  # a run closed mid-invention may have left half-made code in a slot
    gen_dir = REMOTION / "src" / "full" / "generated"
    saved_gen = {p: p.read_text(encoding="utf-8") for p in gen_dir.glob("Custom*.tsx") if p.exists()}
    scenes, custom_slot = [], 0
    for i, sc in enumerate(short["scenes"]):
        shutil.copy(work / f"{i}.jpg", job / f"{i}.jpg")
        cue, card = cues[i], None
        if cue.get("card"):
            (job / f"card{i}.jpg").write_bytes(cue["photo"])
            card = {"image": f"job/card{i}.jpg", "name": sc["person"]["name"], "on": cue["on"], "off": cue["off"]}
        clip = None
        if i in clips:
            shutil.copy(clips[i], job / f"clip{i}.mp4")
            clip = {"src": f"job/clip{i}.mp4", "duration": media_tools.duration(clips[i])}
        skin = short_skin(short, sc.get("full"))
        slot = min(3, custom_slot)
        if (sc.get("full") or {}).get("type") == "custom":
            custom_slot += 1
        scenes.append({"image": f"job/{i}.jpg", "start": bounds[i], "end": bounds[i + 1], "move": sc["move"],
                       **style_lab.style_props(sc, i), "card": card, "clip": clip, "credit": sc.get("credit_tag"),
                       "full": motion.full_props(sc, cue, i, (full_pics or {}).get(i), job, skin=skin, slot=slot),
                       "graphic": sc["graphic"] and {**sc["graphic"], "at": cue["graphic"], "pace": cue.get("map_pace", 1)}})
        if sc["graphic"] and sc["graphic"]["style"] == "mark":  # the card shows the original framing
            shutil.copy(work / f"{i}_raw.jpg", job / f"raw{i}.jpg")
            with Image.open(job / f"raw{i}.jpg") as im:
                scenes[-1]["graphic"].update(image=f"job/raw{i}.jpg", aspect=im.width / im.height)
    props = {"fps": FPS, "total": total, "xfade": XFADE, "hook": short["hook_text"], "palette": PALETTES[short["palette"]],
             "scenes": scenes, "flashes": sorted(flashes), "cta": cues[-1].get("cta"), "ctaLine": short["cta_line"],
             "words": [{"start": s, "end": e, "text": t, "emphasis": s in emphasis, "line": g}
                       for g, line in enumerate(audio_mix.caption_lines(words)) for s, e, t in line]}
    out = work / "remotion.mp4"
    # a quick high-quality intermediate encode: the final pass re-encodes it on the GPU
    h264 = ("--x264-preset=ultrafast", "--crf=14")

    def remotion(p: dict, to: Path, encode: tuple[str, ...]) -> None:
        (work / "props.json").write_text(json.dumps(p, ensure_ascii=False), encoding="utf-8")
        subprocess.run([npx, "remotion", "render", "src/index.ts", "Short", str(to),
                        f"--props={work / 'props.json'}", "--log=error",
                        "--gl=angle", "--concurrency=4", *encode],  # GPU drawing in Chrome, fewer tabs (RAM)
                       cwd=REMOTION, check=True, timeout=3600)

    def render(p: dict) -> None:
        if not layers:
            return remotion(p, out, h264)
        remotion({**p, "words": [], "layer": "pictures"}, work / "pictures.mp4", h264)
        remotion({**p, "words": [], "layer": "graphics"}, work / "graphics.mov",  # ProRes 4444 keeps the alpha
                 ("--codec=prores", "--prores-profile=4444", "--pixel-format=yuva444p10le", "--image-format=png"))
    try:
        motion.code_custom_scenes(short, scenes, work)
        # AI-invented looks/overlays/transitions; a broken one falls back to its library preset
        short["inventions"] = run_remotion_with_fallback(render, props, style_lab.invent_styles(short, props, work))
    finally:
        shutil.rmtree(job, ignore_errors=True)
        for p, txt in saved_gen.items():
            p.write_text(txt, encoding="utf-8")
        style_lab.restore_style_slots()
    return work / "pictures.mp4" if layers else out
