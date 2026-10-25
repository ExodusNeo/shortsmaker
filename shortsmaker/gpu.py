"""Local AI on the owner's GPU and helpers: ComfyUI/MOSS, VoiceStudio, Gemini images, LTX clips, Veo hand-off."""

import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path, PurePosixPath

from PIL import Image, ImageOps

from shortsmaker import footage, frame_render, llm, media_tools, plan_rules, session
from shortsmaker.config import FPS, H, ROOT, W, XFADE


LOCAL_AI = ROOT / "local_ai"  # GPU worker (Kokoro voice, SDXL images, LTX video) in its own venv
# First painter (owner, 2026-10-21: testing its range; was after Gemini on 10-20): MOSS-Image in ComfyUI (D:\ComfyUI).
COMFY = "http://127.0.0.1:8188"
COMFY_PY = Path(r"D:\ComfyUI\.venv\Scripts\python.exe")
# The official negative plus garbled lettering (its test note was gibberish); real, quoted text stays allowed.
MOSS_NEGATIVE = "nsfw, worst quality, bad anatomy, watermark, jpeg artifact, gibberish text, illegible lettering"
MOSS_NO_TEXT = ", text, caption, title, letters, words, inscription, signature"
# Owner 2026-10-21: the paintings looked "way too AI" (glossy, cartoonish). Prompts now name a real period medium;
# this keeps MOSS off its default digital finish. PAINT_FALLBACK is the medium when a scene has no ai_image;
# PAINT_HANDMADE tells Gemini the same (it has no negative prompt).
PAINT_FALLBACK = ("Loose oil sketch on canvas board, thick visible brushstrokes, unfinished edges, muted earth colors, "
                  "soft natural daylight.")
PAINT_HANDMADE = ("Make it look hand-made in the medium the prompt names, with that medium's real marks (paper grain, "
                  "brushstrokes, ink lines, print dots), not a smooth glossy digital painting or a 3D render. The artwork fills "
                  "the whole frame edge to edge, with no border or paper margin.")
MOSS_AI_LOOK = (", 3d render, cgi, glossy plastic look, airbrushed, smooth digital painting, concept art, video game art, "
                "cartoon, oversaturated, lens flare, border, picture frame, paper margin, rounded corners")
# Owner's rule 2026-10-20: found pictures must not carry captions/logos, but AI paintings MAY show writing. Only
# quoted words, so the painter writes real text (MOSS and Gemini render quoted text exactly) instead of gibberish.
PAINT_TEXT_RULE = ("Any writing in the picture must be exactly the words in double quotes in this prompt; with no "
                   "quoted words, no writing. No logos or watermarks.")
# Main voice (owner's pick 2026-10-20, over OmniVoice and VoxCPM2): CosyVoice 3 in VoiceStudio, cloning aiden
# from a 10 s clip of his own Qwen voice, read as a documentary narrator. Needs the VoiceStudio app (D:).
VOICESTUDIO = "http://127.0.0.1:3900"
VOICESTUDIO_EXE = Path(r"D:\VoiceStudio\app\VoiceStudio.exe")
COSY_REF = LOCAL_AI / "voices" / "aiden_ref.wav"  # its words are in aiden_ref.txt
COSY_INSTRUCT = "Speak with dry wit, curiosity, and building suspense, like a storyteller sharing an incredible secret."
# Owner's pick 2026-10-24 for natural documentary cadence without breathlessness (at 95-110 words, ~35-42s)
COSY_SPEED = 1.20
# Backup voice (owner's pick 2026-10-18 over Chatterbox and Kokoro): Qwen3-TTS "aiden", no style instruction,
# in its own venv (qwen-tts pins transformers versions that would break gen.py). Then Kokoro, then Edge.
QWEN_SPEAKER = "aiden"
# Kokoro equivalents of the Edge voices the niche picker chooses from (US "a" / UK "b" voices).
KOKORO_VOICES = {"en-US-AndrewNeural": "am_michael", "en-US-BrianNeural": "am_fenrir",
                 "en-US-ChristopherNeural": "am_michael", "en-US-AvaMultilingualNeural": "af_heart",
                 "en-US-EmmaNeural": "af_bella", "en-GB-RyanNeural": "bm_george"}


def local_job(task: str, items: list[dict], work: Path, timeout: int,
              worker: str = "gen.py", venv: str = ".venv") -> list[dict] | None:
    """Run a batch on this PC's GPU through a local_ai worker (gen.py, or qwen_voice.py in qwen_venv).
    Returns the items (each with an "ok" flag), or None if the local setup is missing or crashed, so the
    caller can fall back."""
    py = LOCAL_AI / venv / "Scripts" / "python.exe"
    if not items or not py.exists():
        return None
    job = work / f"{task}_job.json"
    job.write_text(json.dumps({"task": task, "items": items}, ensure_ascii=False), encoding="utf-8")
    # Offline: never start a surprise multi-GB model download in the middle of a batch.
    env = {**os.environ, "HF_HOME": str(LOCAL_AI / "hf"), "HF_HUB_OFFLINE": "1", "PYTHONIOENCODING": "utf-8"}
    try:
        for attempt in (1, 2):  # a hard crash (LTX on 8 GB, 2026-10-21) leaves no "seconds"; the same job then worked
            proc = subprocess.run([str(py), str(LOCAL_AI / worker), str(job)], env=env, timeout=timeout,
                                  capture_output=True, text=True, encoding="utf-8", errors="replace")
            result = json.loads(job.read_text(encoding="utf-8"))
            if "seconds" in result or attempt == 2:
                break
            print(f"    local {task} worker crashed (exit {proc.returncode}): "
                  f"{(proc.stderr.strip().splitlines() or [''])[-1][:160]}; trying once more")
    except Exception as e:
        print(f"    local {task} failed ({type(e).__name__}), falling back")
        return None
    if result.get("error"):
        print(f"    local {task}: {result['error'][:160]}")
    done = sum(1 for it in result["items"] if it.get("ok"))
    print(f"    local {task}: {done}/{len(items)} done on the GPU in {result.get('seconds', '?')}s")
    return result["items"]


def voicestudio_up() -> bool:
    """VoiceStudio's backend answers, starting the app (and waiting up to 2 min) if it isn't running."""
    def up() -> bool:
        try:
            urllib.request.urlopen(VOICESTUDIO + "/health", timeout=3).read()
            return True
        except Exception:
            return False
    if up():
        return True
    if not VOICESTUDIO_EXE.exists():
        return False
    print("    starting VoiceStudio for the CosyVoice voice...")
    subprocess.Popen([str(VOICESTUDIO_EXE)])
    for _ in range(40):
        time.sleep(3)
        if up():
            return True
    return False


def voicestudio_unload() -> None:
    """Free VoiceStudio's GPU memory: the 8 GB card is needed next for SDXL, LTX and parallax."""
    try:
        loaded = json.loads(urllib.request.urlopen(VOICESTUDIO + "/model/loaded", timeout=10).read())["models"]
        for model_id in [m["id"] for m in loaded] + ["sidecars"]:
            req = urllib.request.Request(f"{VOICESTUDIO}/model/unload/{urllib.parse.quote(model_id, safe='')}",
                                         method="POST")
            try:
                urllib.request.urlopen(req, timeout=60).read()
            except urllib.error.HTTPError:  # nothing of that kind loaded
                pass
    except Exception as e:
        print(f"    couldn't unload VoiceStudio's models ({type(e).__name__}): close the app if the GPU runs out")


def sentence_groups(scenes: list[dict]) -> list[list[int]]:
    """Runs of scenes that together make whole sentences. A sentence may run across picture cuts (2026-10-22:
    flowing narration, as in the Shorts that hold viewers best), so each run is voiced in one take."""
    groups, run = [], []
    for i, sc in enumerate(scenes):
        run.append(i)
        if re.search(r"[.!?][\"')\]]*$", sc["narration"].strip()) or i == len(scenes) - 1:
            groups.append(run)
            run = []
    return groups


def spoken_count(text: str) -> int:
    """Caption words the aligner gives for `text` (qwen_voice.align_words: a token with no letter, digit or "&"
    sticks to the word before it)."""
    return sum(1 for tok in text.split()
               if re.search(r"[A-Za-z0-9&]", unicodedata.normalize("NFKD", tok).encode("ascii", "ignore").decode()))


def split_takes(done: list[dict], groups: list[list[int]], scenes: list[dict], work: Path) -> list[tuple[Path, list]] | None:
    """Cut each take into its scenes halfway through the pause between their words: per scene (wav, words).
    None if a take's words don't match its scenes."""
    out = []
    loop = plan_rules.is_loop_short(scenes)
    for it, group in zip(done, groups):
        take, words = Path(it["out"]), [tuple(w) for w in it["words"]]
        counts = [spoken_count(scenes[i]["narration"]) for i in group]
        extra = int(it.get("loop_tail") or 0)
        if len(words) not in (sum(counts), sum(counts) + extra) or 0 in counts:
            return None
        k, start, length = 0, 0.0, media_tools.duration(take)
        for j, (i, c) in enumerate(zip(group, counts)):
            mine, k = words[k:k + c], k + c
            if j < len(group) - 1:
                end = (mine[-1][1] + words[k][0]) / 2
            elif loop and i == len(scenes) - 1:
                end = min(length, mine[-1][1] + 0.04, (mine[-1][1] + words[k][0]) / 2 if k < len(words) else length)
            else:
                end = length
            path = work / f"{i}.wav"
            media_tools.ffmpeg("-i", take.name, "-ss", f"{start:.3f}", "-t", f"{max(0.05, end - start):.3f}", path.name, cwd=work)
            out.append((path, [(a - start, b - start, w) for a, b, w in mine]))
            start = end
    return out


def local_voice(short: dict, ch: dict, work: Path) -> list[tuple[Path, list] | None]:
    """Voice every scene on the GPU: CosyVoice (aiden, documentary) for the whole Short, else Qwen (aiden),
    else Kokoro; per scene (wav, words) or None to fall back to Edge. A voice counts only if every scene worked,
    so one Short never mixes voices. CosyVoice and Qwen read whole sentences in one take (sentence_groups)."""
    scenes, groups = short["scenes"], sentence_groups(short["scenes"])
    items = [{"text": " ".join(scenes[i]["narration"] for i in g), "seed": g[0], "out": str(work / f"take{g[0]}.wav")}
             for g in groups]
    if items and len(scenes) > 1 and plan_rules.is_loop_short(scenes):
        tail_words = " ".join(scenes[0]["narration"].split()[:4])
        tail_n = spoken_count(tail_words)
        if tail_n > 0:
            items[-1]["text"] = re.sub(r"[.;…]+$", "", items[-1]["text"].strip()) + " " + tail_words
            items[-1]["loop_tail"] = tail_n
    if COSY_REF.exists() and voicestudio_up():
        ref_text = COSY_REF.with_suffix(".txt").read_text(encoding="utf-8").strip()
        done = local_job("tts", [{**it, "engine": "cosyvoice", "ref": str(COSY_REF), "ref_text": ref_text,
                                  "instruct": COSY_INSTRUCT, "speed": COSY_SPEED} for it in items],
                         work, timeout=1200, worker="qwen_voice.py", venv="qwen_venv") or []
        voicestudio_unload()
        if done and all(it.get("ok") and it.get("words") for it in done) and (cut := split_takes(done, groups, scenes, work)):
            return cut
        print("    CosyVoice failed: using Qwen (aiden)")
    items = [{**it, "speaker": QWEN_SPEAKER} for it in items]
    done = local_job("tts", items, work, timeout=900, worker="qwen_voice.py", venv="qwen_venv") or []
    if done and all(it.get("ok") and it.get("words") for it in done) and (cut := split_takes(done, groups, scenes, work)):
        return cut
    print("    Qwen voice failed: using Kokoro")
    voice = ch.get("local_voice") or KOKORO_VOICES.get(ch["voice"], "am_michael")
    items = [{"text": sc["narration"], "voice": voice, "speed": 1.1, "out": str(work / f"{i}.wav")}
             for i, sc in enumerate(short["scenes"])]
    done = local_job("tts", items, work, timeout=600) or []
    return [(Path(it["out"]), [tuple(w) for w in it["words"]]) if it.get("ok") and it.get("words") else None
            for it in done] or [None] * len(items)


def gemini_images(items: list[dict], work: Path) -> set[str]:
    """Paint the AI images with Gemini (agy's built-in image generator, ~2 min each, 3 at a time) instead
    of SDXL on this PC. Returns the `out` paths made; anything missing falls back to SDXL."""
    def one(it: dict) -> str | None:
        if "gemini" in session.NO_QUOTA:
            return None
        folder = work / "gemini_img" / Path(it["out"]).stem
        shutil.rmtree(folder, ignore_errors=True)
        folder.mkdir(parents=True)
        out = llm.run_agy(f"Generate one image: {it['prompt']}\nVertical 9:16 portrait format. {PAINT_HANDMADE} {PAINT_TEXT_RULE} Save the "
                      f"image in the folder {folder} as image.png, then reply with only the saved file path.",
                      folder, timeout=600, model=llm.GEMINI_FALLBACK)
        made = [p for p in folder.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
        if not made and llm.quota_exhausted(out or ""):
            session.NO_QUOTA.add("gemini")
            print("  Gemini has no credits/quota left for images: falling back to SDXL on this PC")
            return None
        try:
            Image.open(made[0]).convert("RGB").save(it["out"], quality=95)
            return it["out"]
        except (IndexError, OSError):
            return None

    if not items or "gemini" in session.NO_QUOTA:
        return set()
    print(f"  Gemini is painting {len(items)} AI image(s)...")
    with ThreadPoolExecutor(3) as pool:
        return {out for out in pool.map(one, items) if out}


def comfy_call(path: str, data: dict | None = None, timeout: int = 30):
    req = urllib.request.Request(COMFY + path, json.dumps(data).encode() if data is not None else None,
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read() or b"null")


def moss_graph(prompt: str, seed: int, width: int, height: int) -> dict:
    """Comfy-Org's official MOSS-Image text-to-image template (25 steps, CFG 2.5, er_sde, skip-layer guidance on
    layer 22), without its prompt upsampler: our prompts are already full scene descriptions."""
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "moss_image_sft_int8_convrot.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen3.5_9b_w4a8_gptq.safetensors", "type": "moss_image", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "flux2-vae_small.safetensors"}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["2", 0]}},
        # no quoted words = no writing: "engraving" alone made it print a gibberish plate caption (test 2026-10-20)
        "5": {"class_type": "CLIPTextEncode", "inputs": {"text": MOSS_NEGATIVE + MOSS_AI_LOOK + ("" if '"' in prompt else MOSS_NO_TEXT),
                                                         "clip": ["2", 0]}},
        "6": {"class_type": "SkipLayerGuidanceDiTSimple", "inputs": {"model": ["1", 0], "double_layers": "", "single_layers": "22",
                                                                     "start_percent": 0.0, "end_percent": 0.5}},
        "7": {"class_type": "EmptyFlux2LatentImage", "inputs": {"width": width, "height": height, "batch_size": 1}},
        "8": {"class_type": "KSampler", "inputs": {"model": ["6", 0], "positive": ["4", 0], "negative": ["5", 0],
                                                   "latent_image": ["7", 0], "seed": seed, "steps": 25, "cfg": 2.5,
                                                   "sampler_name": "er_sde", "scheduler": "simple", "denoise": 1.0}},
        "9": {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["3", 0]}},
        "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": "shortsmaker/paint"}},
    }


def moss_images(items: list[dict], work: Path) -> set[str]:
    """Paint on this PC with MOSS-Image in ComfyUI (owner's pick 2026-10-20 over SDXL-Lightning: follows the
    prompt far better, ~2 min a picture). Starts ComfyUI if needed, stops it again afterwards so its 7 GB text
    encoder leaves RAM and the GPU. Returns the `out` paths made; the rest fall back to SDXL."""
    if not items or not COMFY_PY.exists():
        return set()
    proc = log = None
    try:
        comfy_call("/system_stats", timeout=3)
    except Exception:
        log = open(work / "comfyui.log", "w", encoding="utf-8")
        proc = subprocess.Popen([str(COMFY_PY), "main.py", "--listen", "127.0.0.1", "--port", COMFY.rsplit(":", 1)[1],
                                 "--disable-auto-launch"], cwd=COMFY_PY.parents[2], stdout=log, stderr=subprocess.STDOUT)
        for _ in range(60):  # up to 3 min to start
            time.sleep(3)
            if proc.poll() is not None:
                break
            try:
                comfy_call("/system_stats", timeout=3)
                break
            except Exception:
                pass
    made = set()
    try:
        comfy_call("/system_stats", timeout=3)
        print(f"  MOSS-Image is painting {len(items)} AI image(s) on this PC (~2 min each)...")
        for it in items:
            seed = int(hashlib.md5(it["prompt"].encode()).hexdigest()[:8], 16)  # same prompt, same picture on a re-render
            try:
                pid = comfy_call("/prompt", {"prompt": moss_graph(it["prompt"], seed, it.get("width", 768),
                                                                  it.get("height", 1344))})["prompt_id"]
                for _ in range(300):  # up to 10 min
                    time.sleep(2)
                    hist = comfy_call(f"/history/{pid}").get(pid)
                    if hist:
                        break
                pic = ((hist or {}).get("outputs", {}).get("10") or {}).get("images") or []
                if not pic:
                    print(f"    MOSS-Image failed on {Path(it['out']).name}: {json.dumps((hist or {}).get('status'))[:200]}")
                    continue
                q = urllib.parse.urlencode({k: pic[0][k] for k in ("filename", "subfolder", "type")})
                Image.open(io.BytesIO(urllib.request.urlopen(f"{COMFY}/view?{q}", timeout=60).read())).convert("RGB") \
                    .save(it["out"], quality=95)
                made.add(it["out"])
            except Exception as e:
                print(f"    MOSS-Image failed on {Path(it['out']).name} ({type(e).__name__})")
        comfy_call("/free", {"unload_models": True, "free_memory": True})
    except Exception as e:
        print(f"  MOSS-Image unavailable ({type(e).__name__}): painting with SDXL instead")
    finally:
        if proc:  # we started it: stop it, so the next GPU job gets all the memory
            proc.terminate()
            proc.wait(timeout=60)
            log.close()
    return made


def cover_crop(src: Path, out: Path) -> None:
    """Fill a 9:16 frame with the picture (centre crop), for the AI video model's start frame."""
    ImageOps.fit(Image.open(src).convert("RGB"), (W, H), Image.LANCZOS).save(out, quality=95)


# AI clips of moving people still ghost a little (smeared hands and faces in the background): a soft,
# grainy "old footage" finish hides it (owner's request). Atmosphere clips look clean and stay sharp.
PEOPLE_CLIP_VF = "scale=232:-2,scale=512:896:flags=bicubic,gblur=sigma=1.1,noise=alls=14:allf=t+u,vignette=PI/5"


PEOPLE_MOVE = "People move slowly and naturally; bodies, faces and hands stay realistic and intact."
PEOPLE_STILL = "People and animals stay completely still; only water, atmosphere, light or the moving subject moves."


def motion_prompt(sc: dict) -> str:
    """Short image-to-video prompt for an animate scene made by LTX on this PC."""
    return (f"{sc['motion']}. Gentle, slow, realistic motion, steady camera, consistent with the original photograph. "
            + (PEOPLE_MOVE if sc["motion_people"] else PEOPLE_STILL))  # atmosphere: keep everyone still


H3_MIN = {"subject": 40, "motion": 20, "camera": 10, "look": 15}  # shortest acceptable field, in characters


def h3_problems(entry: dict | None) -> list[str]:
    """What is missing from the AI's prompt fields for one scene (empty list = usable)."""
    if not isinstance(entry, dict):
        return ["no entry for this scene"]
    out = []
    for field, least in H3_MIN.items():
        text = str(entry.get(field) or "").strip()
        if not text:
            out.append(f"no {field} line")
        elif len(text) < least:
            out.append(f"{field} too short (describe it in more detail)")
    avoid = entry.get("avoid")
    if not isinstance(avoid, list) or len([a for a in avoid if str(a).strip()]) < 3:
        out.append("avoid list needs at least 3 things")
    return out


def h3_prompt(sc: dict, entry: dict) -> str:
    """Join checked fields into one image-to-video prompt. H3 has no negative prompt, so the avoid list is its last
    sentence (Veo in Flow reads it the same way)."""
    f = {k: str(entry[k]).strip().rstrip(".") for k in H3_MIN}
    avoid = ", ".join(str(a).strip().rstrip(".") for a in entry["avoid"] if str(a).strip())
    return (f"{f['subject']}. {f['motion']}. Camera: {f['camera']}. Look: {f['look']}. The video starts exactly on "
            f"the given first frame and stays consistent with it. {PEOPLE_MOVE if sc['motion_people'] else PEOPLE_STILL}"
            f" Vertical 9:16. No text, captions or watermarks. Avoid: {avoid}.")


def h3_prompts(short: dict, folder: Path, scenes: list[int]) -> dict[int, str]:
    """Detailed prompts for the owner-made clips (Colab H3 or Flow), written by the AI while it looks at each exact
    start<N>.jpg in folder. Scenes that fail h3_problems go back with the reasons until every one passes; never the
    short motion_prompt (owner: a vague prompt wastes paid compute)."""
    done: dict[int, str] = {}
    problems = {i: [] for i in scenes}
    rnd = 1
    while problems:
        lines = []
        for i, why in problems.items():
            sc = short["scenes"][i]
            lines += [f"SCENE {i + 1}: open start{i + 1}.jpg",
                      f"  Narration: {sc['narration']}",
                      f"  Motion idea: {sc['motion'] or '(none)'}",
                      f"  Movement is {'people' if sc['motion_people'] else 'atmosphere only (everyone stays still)'}"]
            if why:
                lines.append(f"  Fix last answer: {'; '.join(why)}")
        reply = llm.ask_ai(f"""You write image-to-video prompts for a YouTube Short about "{short['title']}". Each clip
starts on the given picture, so a prompt that describes something not in the picture wastes the paid generation.
Open every picture listed below and look at it before writing. Write entirely in English (never use foreign scripts or words).

For each scene give:
- subject: what is actually in the frame (people, objects, setting, era), in one concise sentence. Do NOT list every clothing item or accessory (the model already sees the first frame; over-describing makes faces and objects melt).
- motion: ONE active physical movement. For water, waves, steam, or smoke, use dynamic motion (e.g. rolling ocean swells, splashing white foam, churning wake, billowing smoke); never weak words like "gentle ripples" or "stationary". Never ask a formal group portrait of multiple people to shift or move (animating multiple faces in a still photo causes uncanny rubbery warping; keep people still).
- camera: Locked-off / static camera whenever water, smoke, weather, or an object is moving (a panning or moving camera drowns out and freezes water/smoke into a flat 2D slide). Use a slow move (slow push-in) ONLY when the subject is completely stationary.
- look: match the picture (black-and-white or colour, archival photograph, film grain, lighting, period).
- avoid: 3-5 concise items, e.g. morphing faces, extra fingers, text or captions, modern objects, camera shake,
  and colour when the picture is black-and-white.

{chr(10).join(lines)}

Reply with ONLY JSON: {{"scenes": [{{"scene": 1, "subject": "...", "motion": "...", "camera": "...", "look": "...",
"avoid": ["...", "...", "..."]}}]}}""", fatal=False, read_dir=folder)
        if reply is None:
            input("  >> Neither Claude nor Gemini answered (quota or network). Press Enter to try again. ")
            continue
        got = {}
        for e in reply.get("scenes") if isinstance(reply.get("scenes"), list) else []:
            try:
                got[int(str(e.get("scene")).strip()) - 1] = e
            except (AttributeError, ValueError):
                pass
        for i in list(problems):
            why = h3_problems(got.get(i))
            if why:
                problems[i] = why
            else:
                done[i] = h3_prompt(short["scenes"][i], got[i])
                del problems[i]
        if problems:
            rnd += 1
            print(f"  video prompts: round {rnd}, {len(problems)} scene(s) to fix")
            if (rnd - 1) % 5 == 0:  # don't spend quota silently on a scene the AI keeps getting wrong
                stuck = "; ".join(f"scene {i + 1}: {', '.join(w)}" for i, w in problems.items())
                input(f"  >> The AI still hasn't fixed {stuck}. Press Enter to keep trying. ")
    return done


def unpack_clips(folder: Path) -> list[str]:
    """Unpack scene<N>.mp4/.mov/.webm from folder/clips*.zip (the Colab notebook's download) into folder, by bare
    name only, so nothing lands outside it. Returns the names written."""
    zips = sorted([p for p in folder.glob("*.zip") if p.name.lower().startswith("clips")],
                  key=lambda p: p.stat().st_mtime, reverse=True)
    if not zips:
        return []
    written, seen = set(), set()
    for z_path in zips:
        try:
            with zipfile.ZipFile(z_path) as z:
                for member in z.namelist():
                    base = PurePosixPath(member.replace("\\", "/")).name
                    if re.fullmatch(r"scene\d+\.(mp4|mov|webm)", base, re.I):
                        if base.lower() in seen:
                            continue
                        seen.add(base.lower())
                        dest = folder / base
                        if dest.exists() and dest.stat().st_mtime > z_path.stat().st_mtime:
                            continue
                        dest.write_bytes(z.read(member))
                        written.add(base)
        except zipfile.BadZipFile:
            print(f"    {z_path.name} couldn't be opened, using the loose scene files")
    return sorted(written)


def veo_handoff(short: dict, work: Path, bounds: list[float], marked: list[int]) -> dict[int, Path]:
    """Pause the batch: write each animate scene's start picture + detailed prompt to <Short>/veo (with jobs.json and
    veo.zip for the Colab H3 notebook), open it, wait while the owner makes the clips in Colab or Google Flow by hand
    (no automation of Google's apps: account ToS), then take clips.zip / whichever scene<N>.mp4 files are there.
    Scenes left without a file fall back to LTX."""
    folder = work.parent / "veo"
    folder.mkdir(exist_ok=True)
    scenes = [i for i in marked if not short["scenes"][i].get("shot", "").startswith("CLOSE-UP:")]
    if not scenes:
        return {}
    for old_zip in folder.glob("*.zip"):
        if old_zip.name.lower().startswith("clips"):
            try:
                old_zip.unlink()
            except OSError:
                pass
    for i in scenes:
        cover_crop(work / f"{i}_raw.jpg", folder / f"start{i + 1}.jpg")
    flagged = start_picture_problems(short, folder, scenes)
    for i, why in flagged.items():
        print(f"    scene {i + 1}: not sent for a clip, its start picture {why} (the review replaces the picture)")
        short["scenes"][i]["animate"] = False
    scenes = [i for i in scenes if i not in flagged]
    if not scenes:
        return {}
    prompts = h3_prompts(short, folder, scenes)
    jobs = [{"scene": i + 1, "image": f"start{i + 1}.jpg", "prompt": prompts[i],
             "seconds": round(bounds[i + 1] - bounds[i] + XFADE, 2), "out": f"scene{i + 1}.mp4"} for i in scenes]
    (folder / "jobs.json").write_text(json.dumps(jobs, indent=1), encoding="utf-8")
    with zipfile.ZipFile(folder / "veo.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.write(folder / "jobs.json", "jobs.json")
        z.write(ROOT / "colab" / "h3_run.py", "h3_run.py")
        for j in jobs:
            z.write(folder / j["image"], j["image"])
    notes = ["Colab (MiniMax H3): open colab/h3_clips.ipynb in Colab with gutierrezdishann@gmail.com (the Pro account),",
             "runtime A100 + High-RAM, run the cells top to bottom, upload veo.zip from this folder when asked, then",
             "download clips.zip into this folder and press Enter in the black window.", "",
             "Or Google Flow (labs.google/flow): for each scene, Frames to Video -> upload the start picture -> paste the",
             "prompt -> portrait 9:16, Veo Fast (cheapest credits) -> download -> save it here with the name shown.",
             "Skip any scene you like: this PC's AI video fills it in.", ""]
    for j in jobs:
        n = j["scene"]
        notes += [f"SCENE {n}{'  (the hook: if you only make one, make this one)' if n == 1 else ''}",
                  f"  Start picture: {j['image']}    Save as: {j['out']}    (about {j['seconds']:.0f} s of it is used)",
                  f"  Prompt: {j['prompt']}", ""]
    (folder / "prompts.txt").write_text("\n".join(notes), encoding="utf-8")
    os.startfile(folder)
    os.startfile(folder / "prompts.txt")
    input(f"\n  >> {len(jobs)} AI clip(s) to make in Colab (H3) or Google Flow: see {folder / 'prompts.txt'}\n"
          "  >> Save them in that folder, then press Enter here (skipped ones are made on this PC). ")
    unpack_clips(folder)
    got = {}
    for i in [i for i in marked if i not in flagged]:
        src = next((p for p in sorted(folder.glob(f"scene{i + 1}.*")) if p.suffix.lower() in (".mp4", ".mov", ".webm")), None)
        if src and (out := cut_owner_clip(src, i, bounds, work)):
            got[i] = out
            short["scenes"][i]["owner_clip"] = src.name  # the clip belongs to this picture: it moves when the picture does
    print(f"  using {len(got)} AI clip(s) you made (Colab H3 / Flow)")
    return got


def cut_owner_clip(src: Path, i: int, bounds: list[float], work: Path) -> Path | None:
    """The owner's clip `src` cut to scene i's length: fills the vertical frame, drops Veo's own sound."""
    out = work / f"clip{i}_veo.mp4"  # "clip*" name: counts as AI for the synthetic-content label
    try:
        media_tools.ffmpeg("-i", str(src), "-t", f"{bounds[i + 1] - bounds[i] + XFADE:.2f}", "-vf", footage.FILL_VF,
                           "-an", "-r", str(FPS), *media_tools.video_encoder(), out.name, cwd=work)
        return out
    except subprocess.CalledProcessError:
        print(f"    scene {i + 1}: couldn't read {src.name}, this PC makes that clip instead")
        return None


def start_picture_problems(short: dict, folder: Path, scenes: list[int]) -> dict[int, str]:
    """Start pictures (folder/start<N>.jpg) the owner shouldn't spend a clip on: a clip keeps every flaw of its first
    frame (Oxford 2026-10-26: a Los Angeles street label and a page of made-up newspaper text reached the owner,
    both clips were made and then thrown out with their pictures). One AI call; failure flags nothing.
    Returns scene index -> what is wrong."""
    rows = [f"SCENE {i + 1}: open start{i + 1}.jpg | narration: \"{short['scenes'][i]['narration']}\"" for i in scenes]
    data = llm.ask_ai(f"""These pictures are about to be turned into AI video clips for a YouTube Short: "{short['title']}"
(story: {short.get('topic') or short['title']}). Open each one and flag only a picture that is wrong for its scene,
because a clip keeps everything that is in its first frame:
- another place, country or era than the story and its narration (e.g. an American street in a story set in England);
- readable labels, street names, captions, watermarks or logos printed on it, or garbled, made-up lettering (a page
  of fake newspaper text, nonsense signs);
- AI artifacts: melted or extra faces, hands or limbs, warped buildings;
- a different person than the one its narration is about.
Don't flag a picture for being black-and-white, old, grainy or simple.
{chr(10).join(rows)}
Reply with ONLY JSON: {{"problems": [{{"scene": 3, "why": "shows a street sign reading SAN PEDRO ST"}}]}}""",
                      fatal=False, read_dir=folder)
    found = data.get("problems") if isinstance(data, dict) else None
    out = {}
    for p in found if isinstance(found, list) else []:  # LLM output is untrusted
        n = p.get("scene") if isinstance(p, dict) else None
        if isinstance(n, int) and not isinstance(n, bool) and n - 1 in scenes and str(p.get("why") or "").strip():
            out[n - 1] = str(p["why"]).strip()[:160]
    return out


def local_clips(short: dict, work: Path, sources: list[str], bounds: list[float],
                films: dict[int, dict]) -> dict[int, Path]:
    """Real motion for every scene with a picture: scenes Claude matched to archival film play that
    footage; the scenes it marked become AI video (LTX-Video, on this PC's GPU, or Veo by the owner). Every
    other scene gets the renderer's slow zoom/pan on the full-screen still (2.5D parallax was dropped: its
    depth warp bent paintings and buildings)."""
    usable = [i for i in range(len(short["scenes"]))
              if not sources[i].startswith("PLAIN") and (work / f"{i}_raw.jpg").exists()]
    clips: dict[int, Path] = {}
    for i, f in films.items():
        out, need = work / f"film{i}.mp4", bounds[i + 1] - bounds[i] + XFADE
        a, b = footage.shot_span(f["path"], f["offset"])
        if b - a >= need / 2:  # stay inside the picked shot; a short one plays in slow motion (down to half speed)
            length = min(need, b - a)
            start = min(max(a, f["offset"] - 1), b - length)
        else:  # shot too short to stretch: real speed from just before the picked moment
            length, start = need, max(0.0, f["offset"] - 1)
        try:
            media_tools.ffmpeg("-ss", f"{start:.2f}", "-i", str(f["path"]), "-t", f"{length:.2f}", "-vf", footage.FILL_VF if frame_render.fills_frame(f["path"]) else footage.FILM_VF, "-r", str(FPS),
                   *media_tools.video_encoder(), out.name, cwd=work)
            clips[i] = out
        except subprocess.CalledProcessError:
            print(f"    scene {i + 1}: couldn't cut the film clip, using its still instead")
    marked = [i for i in usable if short["scenes"][i]["animate"] and i not in clips]
    for i in marked:  # clips the owner made earlier (fix rounds and fix.bat re-renders keep them)
        own = short["scenes"][i].get("owner_clip")
        src = work.parent / "veo" / own if own else None
        if src and src.exists():  # re-cut every render: an opener swap may have moved it to a scene of another length
            clips.update({i: out} if (out := cut_owner_clip(src, i, bounds, work)) else {})
        elif not own and (work / f"clip{i}_veo.mp4").exists():  # Shorts made before owner_clip was recorded
            clips[i] = work / f"clip{i}_veo.mp4"
    marked = [i for i in marked if i not in clips]
    if session.VEO_HANDOFF and marked:
        clips.update(veo_handoff(short, work, bounds, marked))
        marked = [i for i in marked if i not in clips and short["scenes"][i]["animate"]]  # rejected start pictures stay stills
    if marked:
        print(f"  animating {len(marked)} scenes with AI video on this PC (a few minutes)...")
        for i in marked:
            cover_crop(work / f"{i}_raw.jpg", work / f"{i}_9x16.jpg")
        items = [{"image": str(work / f"{i}_9x16.jpg"), "out": str(work / f"clip{i}.mp4"), "seed": i, "frames": 97,
                  "prompt": motion_prompt(short["scenes"][i])} for i in marked]
        done = local_job("video", items, work, timeout=3600) or []
        clips.update({i: Path(it["out"]) for i, it in zip(marked, done) if it.get("ok") and Path(it["out"]).exists()})
        for i in [i for i in marked if i in clips and short["scenes"][i]["motion_people"]]:
            soft = work / f"clip{i}_soft.mp4"  # still named clip*: counts as AI for the synthetic-content label
            try:
                media_tools.ffmpeg("-i", clips[i].name, "-vf", PEOPLE_CLIP_VF, *media_tools.video_encoder(), "-pix_fmt", "yuv420p", soft.name, cwd=work)
                clips[i] = soft
            except subprocess.CalledProcessError:
                print(f"    scene {i + 1}: couldn't soften the AI clip, using it as made")
    return clips
