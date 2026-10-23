"""MiniMax H3 image-to-video jobs for a ShortsMaker Short, run on Colab next to jobs.json (both come in veo.zip).
Builds ComfyUI API graphs that mirror the official template (Comfy-Org workflow_templates video_minimax_h3_i2v.json),
queues them on the local ComfyUI, and zips the clips into clips.zip for the owner to download."""

import json
import shutil
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

from PIL import Image, ImageOps

COMFY = "http://127.0.0.1:8188"
COMFY_DIR = Path("/content/ComfyUI")
HERE = Path(__file__).resolve().parent
W, H, FPS = 768, 1344, 24  # H3's native portrait canvas (768px short edge, cap 768x1344, multiples of 32)
UNET = "minimax_h3_fl2va_pruned_bf16.safetensors"
TEXT = "qwen3vl_32b_minimax_h3_int8_convrot.safetensors"
VIDEO_VAE = "minimax_h3_video_vae_fp16.safetensors"
AUDIO_VAE = "minimax_h3_audio_vae_fp32.safetensors"
TURBO_LORA = "minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors"
REQUIRED = ("UNETLoader", "CLIPLoader", "VAELoader", "LoadImage", "MiniMaxH3ImageToVideo", "LoraLoaderModelOnly",
            "BasicScheduler", "KSamplerSelect", "RandomNoise", "BasicGuider", "SamplerCustomAdvanced", "VAEDecode",
            "VAEDecodeAudio", "CreateVideo", "SaveVideo")


def frames(seconds: float) -> int:
    """Seconds -> a valid H3 length, snapped up to its 17k+5 frame grid (the template's Math Expression)."""
    n = max(5, round(seconds * FPS))
    return n + (5 - n % 17) % 17


def fit_start(src: Path, dst: Path) -> None:
    """Centre-crop the start picture to 768x1344: the H3 node stretches off-aspect first frames."""
    ImageOps.fit(Image.open(src).convert("RGB"), (W, H), Image.LANCZOS).save(dst)


def graph(prompt: str, image: str, length: int, seed: int, turbo: bool, prefix: str) -> dict:
    """ComfyUI API graph for one first-frame clip. No negative prompt: H3's graph uses BasicGuider (no CFG)."""
    g = {
        "unet": {"class_type": "UNETLoader", "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
        "text": {"class_type": "CLIPLoader", "inputs": {"clip_name": TEXT, "type": "minimax", "device": "default"}},
        "vae": {"class_type": "VAELoader", "inputs": {"vae_name": VIDEO_VAE}},
        "avae": {"class_type": "VAELoader", "inputs": {"vae_name": AUDIO_VAE}},
        "img": {"class_type": "LoadImage", "inputs": {"image": image}},
        "i2v": {"class_type": "MiniMaxH3ImageToVideo", "inputs": {
            "clip": ["text", 0], "vae": ["vae", 0], "first_frame": ["img", 0], "prompt": prompt,
            "width": W, "height": H, "length": length}},
        "sched": {"class_type": "BasicScheduler", "inputs": {
            "model": ["unet", 0], "scheduler": "simple", "steps": 8 if turbo else 20, "denoise": 1.0}},
        "sampler": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "res_multistep"}},
        "noise": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "guider": {"class_type": "BasicGuider", "inputs": {"model": ["unet", 0], "conditioning": ["i2v", 0]}},
        "sample": {"class_type": "SamplerCustomAdvanced", "inputs": {
            "noise": ["noise", 0], "guider": ["guider", 0], "sampler": ["sampler", 0], "sigmas": ["sched", 0],
            "latent_image": ["i2v", 1]}},
        "decode": {"class_type": "VAEDecode", "inputs": {"samples": ["sample", 0], "vae": ["vae", 0]}},
        "adecode": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["sample", 0], "vae": ["avae", 0]}},
        "video": {"class_type": "CreateVideo", "inputs": {"images": ["decode", 0], "audio": ["adecode", 0], "fps": FPS}},
        "save": {"class_type": "SaveVideo", "inputs": {
            "video": ["video", 0], "filename_prefix": prefix, "format": "auto", "format.codec": "auto"}},  # nested input
    }
    if turbo:  # 8-step distilled LoRA: ~2.5x fewer steps than the 20-step default
        g["lora"] = {"class_type": "LoraLoaderModelOnly", "inputs": {
            "model": ["unet", 0], "lora_name": TURBO_LORA, "strength_model": 1.0}}
        g["sched"]["inputs"]["model"] = g["guider"]["inputs"]["model"] = ["lora", 0]
    return g


def call(path: str, data: dict | None = None) -> dict:
    req = urllib.request.Request(COMFY + path, data=json.dumps(data).encode() if data is not None else None,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:  # ComfyUI explains a rejected graph in the body (node_errors)
        raise RuntimeError(f"ComfyUI said {e.code}: {e.read().decode(errors='replace')[:2000]}") from None


def saved_file(history: dict) -> Path | None:
    """The video SaveVideo wrote, found by scanning the job's outputs (the key name varies by ComfyUI version)."""
    for out in history.get("outputs", {}).values():
        for items in out.values():
            for it in items if isinstance(items, list) else []:
                if isinstance(it, dict) and str(it.get("filename", "")).lower().endswith((".mp4", ".webm", ".mov")):
                    return COMFY_DIR / it.get("type", "output") / it.get("subfolder", "") / it["filename"]
    return None


def main(only: list[int], seed: int, turbo: bool) -> None:
    jobs = json.loads((HERE / "jobs.json").read_text(encoding="utf-8"))
    if only:
        jobs = [j for j in jobs if j["scene"] in only]
    have = call("/object_info")
    missing = [n for n in REQUIRED if n not in have]
    if missing:
        raise SystemExit(f"ComfyUI is missing node {', '.join(missing)}: run the setup cell again (it updates ComfyUI)")
    clips = HERE / "clips"
    clips.mkdir(exist_ok=True)
    for j in jobs:
        n, length, t0 = j["scene"], frames(j["seconds"]), time.time()
        fit_start(HERE / j["image"], COMFY_DIR / "input" / j["image"])
        print(f"scene {n}: {length} frames ({length / FPS:.1f} s)...", flush=True)
        try:
            pid = call("/prompt", {"prompt": graph(j["prompt"], j["image"], length, seed, turbo, f"h3/scene{n}")})["prompt_id"]
            h = None
            while not h:  # ComfyUI adds the history entry once the job has finished or failed
                time.sleep(5)
                h = call(f"/history/{pid}").get(pid)
            src = saved_file(h)
            if not src or not src.exists():
                print(f"  scene {n} failed: {json.dumps(h.get('status', {}))[:800]}")
                continue
            shutil.copy(src, clips / j["out"])
            print(f"  scene {n} done in {(time.time() - t0) / 60:.1f} min")
        except Exception as e:  # one bad clip shouldn't lose the others
            print(f"  scene {n} failed: {type(e).__name__}: {str(e)[:800]}")
    video_clips = sorted(p for p in clips.glob("scene*") if p.suffix.lower() in (".mp4", ".mov", ".webm"))
    with zipfile.ZipFile(HERE / "clips.zip", "w") as z:
        for p in video_clips:
            z.write(p, p.name)
    print(f"{len(video_clips)} clip(s) in clips.zip")
