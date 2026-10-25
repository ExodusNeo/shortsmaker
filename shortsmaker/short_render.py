"""A Short's saved work state and `render()`, which turns a written Short into the finished video."""

import io
import json
import random
import re
import shutil
import subprocess
import time
from pathlib import Path

from PIL import Image

from shortsmaker import (
    audio_mix, blender_plan, blender_render, edit_project, editplan, frame_render, gpu, image_sources, media_tools,
    motion, photo_prep, picker, picture_pool, plan_rules, remotion_render, review, seo, session, style_lab,
)
from shortsmaker.config import FPS, H, MUSIC, OUTPUT, PALETTES, SFX, SRC, STYLE_SLOTS, W, hex_rgb


KEEP_WORK_DAYS = 7  # a finished Short keeps its work/ folder this long, so fix.bat can re-render one scene
AUTO_REPAINT_MAX = 4  # scenes the automatic review may repaint per fix round
AUTO_FIX_ROUNDS = 3  # review -> fix -> re-render rounds after the first render (each ~1 AI review + a render)


def save_state(work: Path, short: dict, choices: list[dict], music: Path | None, by_gemini: set[str]) -> None:
    """What a fix re-render needs to reproduce this Short without new AI picks: the final plan, the chosen
    pictures (bytes as files) and the music."""
    rows = []
    for i, c in enumerate(choices):
        row = {k: v for k, v in c.items() if k not in ("bg", "person", "full_pics")}
        for kind in ("bg", "person"):
            row[kind] = None
            if c[kind]:
                (work / f"keep_{i}_{kind}.bin").write_bytes(c[kind][0])
                row[kind] = [c[kind][1], c[kind][2]]
        if c.get("full_pics"):  # evidence-board photos / document scan
            for k, p in enumerate(c["full_pics"]):
                (work / f"keep_{i}_full{k}.bin").write_bytes(p[0])
            row["full_pics"] = [list(p[1:]) for p in c["full_pics"]]
        rows.append(row)
    short = {k: v for k, v in short.items() if k != "research"}  # Wikipedia text: re-read when needed
    (work / "state.json").write_text(json.dumps({"short": short, "choices": rows, "music": music.relative_to(MUSIC).as_posix() if music else None,
                                                 "by_gemini": sorted(by_gemini)}, default=str), encoding="utf-8")


def load_state(work: Path) -> dict:
    st = json.loads((work / "state.json").read_text(encoding="utf-8"))
    for i, row in enumerate(st["choices"]):
        for kind in ("bg", "person"):
            if row[kind]:
                row[kind] = ((work / f"keep_{i}_{kind}.bin").read_bytes(), *row[kind])
        if row.get("film"):
            row["film"]["path"] = Path(row["film"]["path"])
        if row.get("full_pics"):
            row["full_pics"] = [((work / f"keep_{i}_full{k}.bin").read_bytes(), *p) for k, p in enumerate(row["full_pics"])]
    return st


def prune_work() -> None:
    for w in OUTPUT.glob("*/*/work"):
        if time.time() - w.stat().st_mtime > KEEP_WORK_DAYS * 86400:
            shutil.rmtree(w, ignore_errors=True)


PAPER = (238, 232, 220)  # the Blender look's paper colour, for the stand-in frames before the drawing exists


def drawn_choices(short: dict) -> list[dict]:
    """A drawn Short's picture choices: none (Blender draws every scene)."""
    return [{"bg": None, "person": None, "film": None} for _ in short["scenes"]]


def drawn_thumbnail(short: dict, work: Path, bounds: list[float]) -> tuple[Path, str | None, str | None]:
    """(picture, credit line, CHECK line) for a drawn Short's thumbnail: the real photo of the structure from the
    topic's pool (opener first), else the drawing where the zoom arrives, said in a CHECK line."""
    pool = (picture_pool.load_pool(Path(short["pool_dir"]), thumbs=False) if short.get("pool_dir") else None) or []
    for k in blender_plan.thumbnail_order(short, pool):  # the first one that downloads as a real image
        data = image_sources.get_image(pool[k]["url"], "thumbnail photo")
        try:
            Image.open(io.BytesIO(data or b"")).verify()
        except Exception:
            continue
        else:
            out = work / "thumb_photo.jpg"
            out.write_bytes(data)
            row = pool[k]
            name = re.sub(r"\.(jpe?g|png|tiff?|gif|svg)$", "", row["title"].removeprefix("File:"), flags=re.I)
            site = "Wikimedia Commons" if "wikimedia" in row["url"] else row.get("source", "")
            return out, (f"{name} by {row['credit']} ({site})" if row.get("credit") else None), None
    zoom = next((i for i, b in enumerate(short["build"]["beats"]) if b == "zoom"), 0)
    last = blender_render.scene_frames(bounds)[zoom][1]
    return (work / "blender_frames" / f"f_{last:04d}.png", None,
            "no real photo of the structure was found: the thumbnail uses a drawing")


def render(short: dict, ch: dict, folder: Path, state: dict | None = None, fix_round: int = 0) -> None:
    """Make one Short. With `state` (fix.bat or an automatic fix round), reuse its pictures and music instead of
    new AI picks. `fix_round` counts the automatic review-and-fix re-renders (up to AUTO_FIX_ROUNDS)."""
    work = folder / "work"
    work.mkdir(parents=True, exist_ok=True)
    all_words, bounds, images, sources, cues, audio, scene_sounds = [], [0.0], [], [], [], [], []
    short["cta_line"] = ch.get("cta_line") or "for more stories like this"
    if short.get("palette") not in PALETTES:  # planner gave none (or an old plan): a random one
        short["palette"] = random.choice(list(PALETTES))
    session.YELLOW, session.EMPHASIS = (hex_rgb(PALETTES[short["palette"]][k]) for k in ("accent", "emphasis"))
    drawn = bool(short.get("build"))  # a Blender channel: every scene is drawn, nothing is picked or painted
    if state:
        choices = state["choices"]
    elif drawn:
        choices = drawn_choices(short)
    else:
        choices = picker.choose_images(short, work, ch)
        # real footage first, then a full-screen motion graphic, and only then an AI painting
        weak = [i for i, c in enumerate(choices) if not c["bg"] and not short["scenes"][i].get("full")]
        picker.rescue_graphics(short, weak, {i: "no fitting picture was found" for i in weak})
        plan_rules.mark_details(short, choices, work)
    for i, sc in enumerate(short["scenes"]):  # an evidence board needs its real photos (3 or more)
        if (sc.get("full") or {}).get("type") == "board" and len(choices[i].get("full_pics") or []) < 3:
            sc["full"] = None
    print("  voice, gap images and thumbnail art on this PC...")
    voices = gpu.local_voice(short, ch, work)
    gen = [{"prompt": sc["ai_image"], "out": str(work / f"ai{i}.jpg")}
           for i, sc in enumerate(short["scenes"]) if not choices[i]["bg"] and sc["ai_image"] and not sc.get("full")]
    figs = {i: sc["full"]["thing"] for i, sc in enumerate(short["scenes"])
            if (sc.get("full") or {}).get("type") == "number" and sc["full"].get("thing") and not sc["full"].get("compare")}
    gen += [{"prompt": remotion_render.FIGURE_PROMPT.format(thing=thing), "out": str(work / f"figraw{i}.jpg")} for i, thing in figs.items()]
    if short["thumbnail_prompt"]:
        gen.append({"prompt": short["thumbnail_prompt"], "out": str(work / "thumb_art.jpg")})
    if drawn:
        gen, figs = [], {}
    have = {it["out"] for it in gen if Path(it["out"]).exists()}  # a fix re-render keeps the pictures already painted
    gen = [it for it in gen if it["out"] not in have]
    by_gemini = set(state["by_gemini"]) if state else set()
    # Painter order (owner, 2026-10-21, to test MOSS's range): MOSS-Image on this PC, then Gemini, then SDXL
    by_moss = gpu.moss_images(gen, work)
    can_gemini_paint = shutil.which("agy") and not (session.SOLO and session.BRAIN == "claude")
    by_gemini |= gpu.gemini_images([it for it in gen if it["out"] not in by_moss], work) if can_gemini_paint else set()
    rest = [it for it in gen if it["out"] not in by_gemini | by_moss]
    generated = have | by_gemini | by_moss | {it["out"] for it in (gpu.local_job("images", rest, work, timeout=900) if rest else None) or []
                                              if it.get("ok")}
    for i in figs:  # the counted thing as a figure; a failed or messy painting leaves the built-in icon
        fig, raw = work / f"fig{i}.png", work / f"figraw{i}.jpg"
        if fig.exists() or (raw.exists() and remotion_render.ink_silhouette(raw, fig)):
            short["scenes"][i]["full"]["figure"] = str(fig)
    for i, sc in enumerate(short["scenes"]):
        print(f"  scene {i + 1}/{len(short['scenes'])}: image + voice")
        sc["credit_tag"] = None
        img, ai = work / f"{i}.jpg", work / f"ai{i}.jpg"
        if drawn:  # Blender draws it once the voice has set the scene lengths; a paper frame until then
            Image.new("RGB", (int(W * SRC), int(H * SRC)), PAPER).save(img)
            shutil.copy(img, work / f"{i}_raw.jpg")
            source = f"drawn in Blender: {short['build']['beats'][i]}"
        elif choices[i]["bg"]:  # film scenes play the clip; their still only stands in if the cut fails
            img.write_bytes(choices[i]["bg"][0] if choices[i].get("film") else photo_prep.clean_photo(choices[i]["bg"][0]))
            shutil.copy(img, work / f"{i}_raw.jpg")  # original framing, for the GPU camera moves
            photo_prep.to_vertical(img)
            film, site, credit = choices[i].get("film"), choices[i].get("site", "Wikimedia Commons"), choices[i]["bg"][2]
            licence = credit or ("Pixabay license, no credit needed" if site == "Pixabay" else "public domain")
            source = (f"{site}, {licence}: {choices[i]['bg'][1]}"
                      + (f" (real film from {media_tools.clock(film['t'])})" if film else ""))
            if credit:  # a short tag on screen while it shows; the full credit goes in upload.txt
                sc["credit_tag"] = image_sources.short_credit(credit, film=bool(film))
        elif str(ai) in generated:  # no real photo fit: AI image made on this PC
            shutil.copy(ai, img)
            shutil.copy(ai, work / f"{i}_raw.jpg")
            photo_prep.to_vertical(img)
            # a fix re-render keeps earlier paintings without knowing which local painter made them
            maker = ("by Gemini" if str(ai) in by_gemini else "on this PC (MOSS-Image)" if str(ai) in by_moss
                     else "on this PC")
            source = f"AI-GENERATED {maker}: \"{sc['ai_image']}\""
        elif i:  # reuse an earlier image; its different camera move keeps it from looking repeated
            print("    no fitting image, reusing an earlier one")
            k = random.randrange(i)
            shutil.copy(work / f"{k}.jpg", img)
            shutil.copy(work / f"{k}_raw.jpg", work / f"{i}_raw.jpg")
            source = f"reused from scene {k + 1} (nothing fit \"{sc['image_search']}\")"
            sc["credit_tag"] = short["scenes"][k]["credit_tag"]
        else:
            print("    no fitting image, using a plain frame")
            Image.new("RGB", (int(W * SRC), int(H * SRC)), (18, 18, 24)).save(img)
            source = f"PLAIN FRAME (nothing fit \"{sc['image_search']}\"), replace before uploading"
        if sc.get("full"):  # drawn by Remotion instead of the picture (the picture stays as a fallback)
            pics = choices[i].get("full_pics") or []
            credited = [p for p in pics if p[2]]
            sc["credit_tag"] = None
            if credited:
                sc["credit_tag"] = image_sources.short_credit(credited[0][2]) + (f" +{len(credited) - 1}" if len(credited) > 1 else "")
            source = (f"{motion.full_summary(sc['full'])} ("
                      + (f"rescued: {sc['full_rescued']}" if sc.get("full_rescued") else "planned") + ")"
                      + "".join(f" | photo: {p[3]}, {p[2] or 'public domain'}: {p[1]}" for p in pics))
        if choices[i].get("plan_note"):
            source += f" | {choices[i]['plan_note']}"
        sources.append(source)
        if voices[i]:
            sound, words = voices[i]
        else:  # local voice unavailable: Microsoft's free Edge voice
            sound = work / f"{i}.mp3"
            words = audio_mix.speak(sc["narration"], ch["voice"], sound)
        if i == 0 and words and words[0][0] > 0.1:  # speak on the first frame: trim the voice's lead-in silence
            cut = words[0][0] - 0.05
            trimmed = work / f"0_start{sound.suffix}"
            media_tools.ffmpeg("-ss", f"{cut:.3f}", "-i", str(sound), trimmed.name, cwd=work)
            sound, words = trimmed, [(a - cut, b - cut, w) for a, b, w in words]
        scene_sounds.append((sound, words, img))

    # Pacing & hold time: full-screen graphics, person cards and overlay graphics need breathing room
    # to be read and understood before the scene transitions to the next beat.
    # Keep narration pacing tight: graphics start earlier within speech, avoiding dead air pauses.
    raw_durs = [media_tools.duration(s) for s, _, _ in scene_sounds]
    raw_total = sum(raw_durs) + 0.6
    max_total = 33.0 if session.SHORT_FORM else 58.5
    budget = max(0.0, max_total - raw_total)
    pads = []
    for i, sc in enumerate(short["scenes"]):
        sound, words, _ = scene_sounds[i]
        dur = raw_durs[i]
        needed = 0.0
        # 1. Full-screen motion graphics: subtle micro-settle (at most 0.25s) after speech so cut is clean
        if sc.get("full"):
            last_word = words[-1][1] if words else dur
            tail = max(0.0, dur - last_word)
            needed = max(needed, max(0.0, 0.25 - tail))
        # 2. Very short scenes (< 1.6s) with a person card or graphic get a tiny breath if needed
        if choices[i].get("person") and sc.get("person"):
            needed = max(needed, max(0.0, 1.6 - dur))
        if sc.get("graphic"):
            needed = max(needed, max(0.0, 1.4 - dur))
        # Keep narrator voice pacing tight: never stall with dead air pauses
        pads.append(min(0.25, needed))
    if sum(pads) > budget and sum(pads) > 0:
        scale = budget / sum(pads)
        pads = [p * scale for p in pads]

    for i, sc in enumerate(short["scenes"]):
        sound, words, img = scene_sounds[i]
        pad = pads[i]
        if pad >= 0.08:
            padded = work / f"{i}_padded{sound.suffix}"
            media_tools.ffmpeg("-y", "-i", str(sound), "-af", f"apad=pad_dur={pad:.2f}", padded.name, cwd=work)
            sound = padded
        audio.append(sound)
        all_words += [(s + bounds[-1], e + bounds[-1], t) for s, e, t in words]
        bounds.append(bounds[-1] + media_tools.duration(sound))
        images.append(Image.open(img).convert("RGB"))
        cues.append(editplan.scene_cues(sc, words, bounds[-2], bounds[-1], i, choices[i]["person"]))
    total = bounds[-1] + 0.6  # small tail so the last word isn't clipped
    bounds[-1] = total
    cues[-1]["cta"] = max(bounds[-2] + 0.3, total - 3.0)  # silent subscribe button: keeps the rewatch loop
    if drawn:  # raises BlenderFailed after a retry: cli keeps this Short's files and goes on
        clips = blender_render.render_clips(short, bounds, all_words, work)
        images = [Image.open(work / "blender_frames" / f"f_{a:04d}.png").convert("RGB")
                  for a, _ in blender_render.scene_frames(bounds)]
    else:
        clips = gpu.local_clips(short, work, sources, bounds, {i: c["film"] for i, c in enumerate(choices)
                                                             if c.get("film") and not short["scenes"][i].get("full")})
    for i, sc in enumerate(short["scenes"]):  # keep text callouts off the subject's face (maps and marks are full cards)
        if sc["graphic"] and sc["graphic"]["style"] != "mark":
            film = choices[i]["film"]["path"] if clips.get(i) == work / f"film{i}.mp4" else None
            sc["graphic"]["low"] = frame_render.graphic_low(choices[i], work / f"{i}_raw.jpg", film, sc)
    (work / "list.txt").write_text("".join(f"file '{a.name}'\n" for a in audio))
    media_tools.ffmpeg("-f", "concat", "-i", "list.txt", "-ar", "44100", "-ac", "2", "voice.wav", cwd=work)
    emphasis = {c["emphasis"] for c in cues if c.get("emphasis") is not None}
    flashes = {bounds[i] for i, sc in enumerate(short["scenes"]) if sc["transition"] == "flash"}
    audio_mix.captions(all_words, work / "captions.ass", emphasis)
    seo.srt(all_words, folder / "captions.srt")
    if not all((SFX / f"{name}.wav").exists() for name in audio_mix.SFX_FILES):
        audio_mix.make_sfx()

    # Renderer: Remotion when the plan is graphics-heavy (animated maps, spring motion), otherwise the
    # faster built-in Python renderer. Remotion failing never loses the Short: it falls back.
    renderer, n_graphics, video_in = "python", motion.graphics_count(short, cues), ["-f", "rawvideo", "-pix_fmt", "rgb24",
                                                                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if remotion_render.wants_remotion(short["scenes"], n_graphics):
        print(f"  rendering with Remotion ({n_graphics} motion graphics)...")
        try:
            video_in = ["-i", str(remotion_render.render_remotion(short, cues, bounds, total, all_words, work, emphasis, flashes,
                                                  clips, {i: c.get("full_pics") for i, c in enumerate(choices)}))]
            renderer = "remotion"
            for kind, spec in ({} if state else short.get("inventions") or {}).items():  # once, on the first render
                slot = STYLE_SLOTS[kind]
                folder_c = style_lab.save_candidate(kind, spec["title"], spec["brief"], f'stories like "{short["title"]}"',
                                          (work / f"{slot}.tsx").read_text(encoding="utf-8"), work / f"{slot}_preview.mp4",
                                          short["title"])
                print(f"    the invented {kind} \"{spec['title']}\" is waiting for your OK in library.bat ({folder_c.name})")
        except Exception as e:
            print(f"    Remotion failed ({e}), using the built-in renderer")
            full = [i for i, sc in enumerate(short["scenes"]) if sc.get("full")]
            if full:
                print(f"    painting {len(full)} scene(s) that were full-screen motion graphics...")
                by_gemini |= remotion_render.paint_instead(short, work, full, images, sources)

    # Audio: voice + music ducked under the voice + the sound-design cue sheet.
    tracks = sorted(MUSIC.rglob("*.mp3"))  # music/<mood>/*.mp3; the planner picks the Short's mood
    fitting = [t for t in tracks if t.parent.name == short.get("music_mood")]
    music = random.choice(fitting or tracks) if tracks else None
    if state and state.get("music") and (MUSIC / state["music"]).exists():
        music = MUSIC / state["music"]
    for i, sc in enumerate(short["scenes"]):  # the story's own sounds: owner's file, else fetched once from Freesound
        if sc.get("sound") and not sc["sound"].get("file"):
            found = audio_mix.story_sound(sc["sound"]["sound"])
            if found:
                sc["sound"]["file"] = found.relative_to(SFX).as_posix()
            else:
                print(f"    no sound found for \"{sc['sound']['sound']}\" (scene {i + 1}), skipping it")
                sc["sound"] = None
    events = audio_mix.sfx_events(short, cues, bounds, renderer == "remotion")
    fmt = "aformat=sample_rates=44100:channel_layouts=stereo"
    # Remotion draws its own captions; the Python video is also kept without them (clean.mp4) for edit_project
    graph = ["[0:v]null[v]" if renderer == "remotion" else "[0:v]split[raw][clean];[raw]subtitles=captions.ass[v]",
             f"[1:a]{fmt},asplit=2[voice][key]" if music else f"[1:a]{fmt}[voice]"]
    mix = ["[voice]"]
    inputs = ["-i", "voice.wav"]
    if music:
        inputs += ["-stream_loop", "-1", "-i", str(music)]
        graph += [f"[2:a]{fmt},volume={audio_mix.music_gain(music):.4f},afade=t=in:d=0.1,afade=t=out:st={total - 2:.2f}:d=2[m]",
                  "[m][key]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=400,asplit[music][music_stem]"]
        mix.append("[music]")
    fx = []
    for e in events:
        k = 1 + inputs.count("-i")  # ffmpeg input index; input 0 is the video
        src = SFX / e["sound"]
        inputs += ["-i", str(src if src.suffix else src.with_suffix(".wav"))]
        graph.append(f"[{k}:a]{fmt},volume={e['gain']},adelay={int(e['t'] * 1000)}:all=1[s{k}]")
        fx.append(f"[s{k}]")
    if fx:  # summed apart first (same total: amix with normalize=0 only adds) so they can be saved as one track
        graph.append("".join(fx) + f"amix=inputs={len(fx)}:normalize=0,asplit[fx][fx_stem]")
        mix.append("[fx]")
    # music.wav / sfx.wav: the mix's own parts before the final loudness pass, for edit_project's sound tracks
    stems = []
    for label, name in (("[music_stem]", "music.wav"), ("[fx_stem]", "sfx.wav")):
        (work / name).unlink(missing_ok=True)  # a track left from an earlier round mustn't reach the timeline
        if label in ";".join(graph):
            stems += ["-map", label, "-c:a", "pcm_f32le", "-t", f"{total:.2f}", name]
    graph.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0,"
                 "loudnorm=I=-14:TP=-1.5:LRA=11,"  # -14 LUFS = YouTube's playback level
                 # one-pass loudnorm overshoots (an Atari Short peaked at -0.1 dB): a 4x-oversampled limiter
                 # also catches in-between peaks, so the AAC file stays under -1.5 dB (tested: -1.8)
                 "aresample=176400,alimiter=limit=0.79:level=false,aresample=44100[a]")

    if renderer == "python":
        print("  rendering video...")
    proc = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", *video_in, *inputs,
         "-filter_complex", ";".join(graph), "-map", "[v]", "-map", "[a]",
         *media_tools.video_encoder(), "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.2f}", "-movflags", "+faststart",
         "../short.mp4", *(["-map", "[clean]", *media_tools.video_encoder(), "-pix_fmt", "yuv420p", "-t", f"{total:.2f}",
                            "clean.mp4"] if renderer == "python" else []), *stems],
        stdin=subprocess.PIPE if renderer == "python" else None, cwd=work)
    if renderer == "python":
        frame = frame_render.frame_maker(images, short["scenes"], short["hook_text"], short["cta_line"], bounds, cues, clips)
        # a drawn Short is one continuous Blender camera: crossfades would show it twice
        frame_render.write_frames(frame, len(images), bounds, total, proc.stdin, flashes, set(bounds[1:-1]) if drawn else set())
        frame.close()
        proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed while rendering")
    review.storyboard(folder / "short.mp4", bounds, folder / "storyboard.jpg")
    editplan.edit_plan(short, bounds, sources, cues, events, music, folder / "edit_plan.txt",
              f"{'Remotion' if renderer == 'remotion' else 'built-in (Python)'}, {n_graphics} motion graphics",
              clips)
    issues = review.quality_check(folder / "short.mp4", bounds, sources)
    print(f"  {session.BRAIN.capitalize()} is watching the finished Short for problems...")
    found, fixes = review.visual_review(folder / "short.mp4", short, bounds, sources, work, drawn=drawn)
    issues += found
    if drawn:  # nothing to repaint or swap in a drawn Short: what the review finds stays a CHECK line
        fixes = {}
        issues += [short["build_check"]] if short.get("build_check") else []
        thumb_pic, thumb_credit, thumb_check = drawn_thumbnail(short, work, bounds)
        issues += [thumb_check] if thumb_check else []
    found, opener = review.first_second_check(folder / "short.mp4", short, choices, folder / "storyboard.jpg", work)
    issues += found
    if short.get("opener_swapped"):  # once per Short: a later round mustn't swap it back
        opener = None
    print("  quality check: " + (f"{len(issues)} thing(s) to look at before uploading:" if issues else "OK, nothing to fix"))
    for issue in issues:
        print(f"    CHECK: {issue}")
    with open(folder / "edit_plan.txt", "a", encoding="utf-8") as f:
        f.write("\n\nQUALITY CHECK (automatic, on the finished video)\n" + ("\n".join(f"  CHECK: {i}" for i in issues) or
                "  OK: no black or frozen stretches, loudness on target, every scene has a picture") + "\n")

    art = work / "thumb_art.jpg"  # Claude's thumbnail plan, painted on this PC; else the first scene
    frame_render.thumbnail(thumb_pic if drawn else art if art.exists() else work / "0.jpg",
                           short.get("thumbnail_text", short["title"]), folder / "thumbnail.jpg")
    synthetic = any(c.name.startswith("clip") for c in clips.values()) or any(s.startswith("AI-GENERATED") for s in sources)
    credit = music.with_name(music.name + ".txt") if music else None
    credit_text = f"\n\nMusic:\n{credit.read_text(encoding='utf-8').strip()}" if credit and credit.exists() else ""
    image_credits = []  # credited material (CC, Internet Archive, Openverse); public domain needs nothing
    for sc, c in zip(short["scenes"], choices):
        for _, title, who, site in (c.get("full_pics") or []) if sc.get("full") else []:
            if who:
                image_credits.append(f"{re.sub(r'[.](jpe?g|png|tiff?|gif|svg)$', '', title.removeprefix('File:'), flags=re.I)} by {who} ({site})")
        for kind in ("bg", "person"):
            if c[kind] and c[kind][2] and not (kind == "bg" and sc.get("full")):
                name = re.sub(r"\.(jpe?g|png|tiff?|gif|webm|ogv|svg)$", "", c[kind][1].removeprefix("File:"), flags=re.I)
                site = c.get("site", "Wikimedia Commons") if kind == "bg" else "Wikimedia Commons"
                image_credits.append(f"{name} by {c[kind][2]} ({site})")
    if drawn and thumb_credit:
        image_credits.append(f"Thumbnail: {thumb_credit}")
    if image_credits:
        credit_text += "\n\nFootage and image credits:\n" + "\n".join(dict.fromkeys(image_credits))
    (folder / "upload.txt").write_text(
        f"TITLE:\n{short['title'][:100]}\n\nDESCRIPTION:\n{short.get('description', '')}{credit_text}\n\n"
        f"TAGS (paste into Tags box):\n{', '.join(short.get('tags', []))[:500]}\n\n"
        f"PINNED COMMENT (post it, then pin it):\n{short.get('pinned_comment', '')}\n\n"
        "SETTINGS: Category = Education. Language = English. "
        "Subtitles -> Add language -> Upload file -> captions.srt (with timing)\n"
        + ("ALTERED OR SYNTHETIC CONTENT: Yes. This Short contains AI-generated images or motion that look "
           "like real footage (see edit_plan.txt), and YouTube requires the label.\n" if synthetic else ""),
        encoding="utf-8")
    save_state(work, short, choices, music, by_gemini)  # work/ stays KEEP_WORK_DAYS for fix.bat
    # Fix and re-render while the review finds fixable scenes, capped: an AI reviewer nearly always finds
    # something, so an uncapped loop could repaint forever. fix.bat re-renders (state, round 0) stay manual.
    if (fixes or opener) and (not state or fix_round) and fix_round < AUTO_FIX_ROUNDS:
        st = load_state(work)
        st["short"]["research"] = short.get("research")  # not in state.json; the motion-graphic rescue reads it
        print(f"  fix round {fix_round + 1}/{AUTO_FIX_ROUNDS}: the review found {min(len(fixes), AUTO_REPAINT_MAX)} "
              f"scene(s) to fix{' and a weak opening' if opener else ''}: fixing them and re-rendering...")
        st["short"]["auto_fixed"] = (st["short"].get("auto_fixed") or []) + [
            f"round {fix_round + 1}: {note}" for note in review.apply_review_fixes(st, work, fixes, opener)]
        render(st["short"], ch, folder, st, fix_round + 1)
        return
    if (fixes or opener) and fix_round:
        print(f"  stopped fixing after {AUTO_FIX_ROUNDS} rounds: the CHECK lines above are left for you")
    if not issues:
        edit_project.remove(folder)  # an older timeline would no longer match this video
        return
    try:  # what the fix rounds left: a Shotcut timeline to fix it by hand
        videos = [("V1", work / "clean.mp4")]  # Python renderer: pictures and graphics stay one video
        if renderer == "remotion":  # same props from the cached code: pictures and graphics apart, no captions
            remotion_render.render_remotion(short, cues, bounds, total, [], work, emphasis, flashes, clips,
                                            {i: c.get("full_pics") for i, c in enumerate(choices)}, layers=True)
            videos = [("V1 pictures", work / "pictures.mp4"), ("V2 graphics", work / "graphics.mov")]
        edit_project.make(folder, work, bounds, issues, videos)
        print(f"  to fix the CHECK lines yourself: double-click {folder.name}\\edit_in_shotcut.bat")
    except Exception as e:
        print(f"    couldn't make the Shotcut timeline ({e})")
