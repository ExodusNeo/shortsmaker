"""Local GPU worker for ShortsMaker: voice (Kokoro), images (SDXL-Lightning), video (LTX-Video).

Runs in its own venv (CUDA PyTorch). Usage: python gen.py job.json -> writes job.json's "result".
A job is {"task": "tts" | "images" | "video", "items": [...]}; each item gets an "ok" flag so one
failure never sinks the batch. Models load once per job and are freed when the process exits.
"""
import gc
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image

SDXL_BASE = "stabilityai/stable-diffusion-xl-base-1.0"
LTX_REPO = "Lightricks/LTX-Video-0.9.5"  # tokenizer, scheduler, configs and the T5 text encoder
# Video weights: LTX-Video 0.9.8 2B distilled (same 2B architecture as 0.9.5). Tested 2026-10-15 on the
# owner's RTX 5060: people stay coherent where 0.9.5 warped them, and 8 steps take ~22s instead of ~95s.
LTX_CKPT = ("Lightricks/LTX-Video", "ltxv-2b-0.9.8-distilled.safetensors")
LTX_STEPS = [1000, 993, 987, 981, 975, 909, 725, 0.03]  # the distilled model's own 8-step schedule
NEGATIVE = "text, watermark, logo, signature, letters, words, deformed, blurry, low quality"


def tts(items: list[dict]) -> None:
    """item: {"text", "voice", "out" (.wav)} -> adds "words": [[start, end, word], ...]."""
    import soundfile as sf
    from kokoro import KPipeline
    pipe = KPipeline(lang_code=items[0]["voice"][0], repo_id="hexgrad/Kokoro-82M")  # "a"m_/"b"m_ = US/UK
    for it in items:
        audio, words = [], []
        for r in pipe(it["text"], voice=it["voice"], speed=it.get("speed", 1.0)):
            off = sum(len(a) for a in audio) / 24000
            audio.append(r.audio.numpy())
            for tk in r.tokens:
                if tk.start_ts is None:
                    continue
                if not re.search(r"\w", tk.text):  # punctuation sticks to the word before it
                    if words:
                        words[-1][2] += tk.text
                    continue
                words.append([round(off + tk.start_ts, 3), round(off + tk.end_ts, 3), tk.text])
        if not audio:
            raise RuntimeError(f"no audio for {it['text'][:40]!r}")
        sf.write(it["out"], np.concatenate(audio), 24000)
        it.update(words=words, ok=True)


def images(items: list[dict]) -> None:
    """item: {"prompt", "out", "width", "height"} -> 4-step SDXL-Lightning image."""
    from diffusers import EulerDiscreteScheduler, StableDiffusionXLPipeline, UNet2DConditionModel
    from huggingface_hub import hf_hub_download
    from safetensors.torch import load_file
    unet = UNet2DConditionModel.from_config(SDXL_BASE, subfolder="unet").to(torch.float16)
    unet.load_state_dict(load_file(hf_hub_download("ByteDance/SDXL-Lightning", "sdxl_lightning_4step_unet.safetensors")))
    pipe = StableDiffusionXLPipeline.from_pretrained(SDXL_BASE, unet=unet, torch_dtype=torch.float16, variant="fp16")
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")
    pipe.enable_model_cpu_offload()  # ~5.4GB peak on an 8GB card
    for it in items:
        img = pipe(it["prompt"], negative_prompt=NEGATIVE, num_inference_steps=4, guidance_scale=0,
                   width=it.get("width", 768), height=it.get("height", 1344)).images[0]
        img.save(it["out"], quality=95)
        it["ok"] = True


T5_CACHE = Path(__file__).parent / "models" / "ltx_t5_bf16"


def t5_encoder():
    """LTX's text encoder on the GPU. The repo ships it as 19GB fp32; a one-time bf16 copy (9.5GB)
    halves every later load, and fp8 weight storage lets it fit in 8GB of VRAM (layers are upcast
    to bf16 one at a time while they run; norms and embeddings stay full precision)."""
    from diffusers.hooks import apply_layerwise_casting
    from transformers import T5EncoderModel
    if (T5_CACHE / "config.json").exists():
        te = T5EncoderModel.from_pretrained(T5_CACHE, torch_dtype=torch.bfloat16)
    else:
        te = T5EncoderModel.from_pretrained(LTX_REPO, subfolder="text_encoder", torch_dtype=torch.bfloat16)
        te.save_pretrained(T5_CACHE)
    apply_layerwise_casting(te, torch.float8_e4m3fn, torch.bfloat16,
                            # "wo": T5 casts its input to wo's *stored* dtype, which breaks with fp8
                            skip_modules_pattern=("norm", "shared", "embed", "relative_attention_bias", r"\.wo$"))
    return te.to("cuda")


def video(items: list[dict]) -> None:
    """item: {"image", "prompt", "out" (.mp4), "frames"} -> image-to-video clip at 24fps.
    Everything runs on the GPU, one model at a time: text encoder, then video transformer, then VAE."""
    from diffusers import AutoencoderKLLTXVideo, LTXConditionPipeline, LTXVideoTransformer3DModel
    from diffusers.pipelines.ltx.pipeline_ltx_condition import LTXVideoCondition
    from huggingface_hub import hf_hub_download
    from diffusers.utils import export_to_video
    # Stage 1: the 4.7B-parameter T5 text encoder, alone on the GPU with fp8 weight storage (~5GB).
    # Stage 2 (the video model) never has it loaded at the same time.
    enc = LTXConditionPipeline.from_pretrained(LTX_REPO, text_encoder=t5_encoder(), transformer=None, vae=None,
                                               torch_dtype=torch.bfloat16)
    negative = ("worst quality, inconsistent motion, blurry, jittery, distorted, morphing faces, text, "
                "distorted bodies, extra limbs, warped people")
    with torch.no_grad():
        embeds = [enc.encode_prompt(it["prompt"], negative, do_classifier_free_guidance=True,
                                    device="cuda", max_sequence_length=256) for it in items]
    del enc
    gc.collect()
    torch.cuda.empty_cache()
    ckpt = hf_hub_download(*LTX_CKPT)
    transformer = LTXVideoTransformer3DModel.from_single_file(ckpt, config=LTX_REPO, subfolder="transformer",
                                                              torch_dtype=torch.bfloat16)
    # 8GB cards: keep transformer weights in fp8 and upcast one layer at a time (~2GB saved).
    transformer.enable_layerwise_casting(storage_dtype=torch.float8_e4m3fn, compute_dtype=torch.bfloat16)
    vae = AutoencoderKLLTXVideo.from_single_file(ckpt, config=LTX_REPO, subfolder="vae", torch_dtype=torch.bfloat16)
    pipe = LTXConditionPipeline.from_pretrained(LTX_REPO, transformer=transformer, vae=vae, text_encoder=None,
                                                tokenizer=None, torch_dtype=torch.bfloat16)
    pipe.enable_model_cpu_offload()
    pipe.vae.enable_tiling()
    for it, emb in zip(items, embeds):
        pe, pm, ne, nm = (x.to("cuda") for x in emb)
        img = Image.open(it["image"]).convert("RGB").resize((512, 896), Image.LANCZOS)
        frames = pipe(conditions=[LTXVideoCondition(image=img, frame_index=0)],
                      prompt_embeds=pe, prompt_attention_mask=pm,
                      negative_prompt_embeds=ne, negative_prompt_attention_mask=nm,
                      width=512, height=896, num_frames=it.get("frames", 97), timesteps=LTX_STEPS,
                      guidance_scale=1.0, decode_timestep=0.05, decode_noise_scale=0.025,  # distilled: no CFG
                      generator=torch.Generator().manual_seed(it.get("seed", 0))).frames[0]
        export_to_video(frames, it["out"], fps=24)
        it["ok"] = True


def main() -> None:
    path = Path(sys.argv[1])
    job = json.loads(path.read_text(encoding="utf-8"))
    t = time.time()
    try:
        {"tts": tts, "images": images, "video": video}[job["task"]](job["items"])
    except Exception as e:  # keep whatever finished; the caller falls back for the rest
        job["error"] = f"{type(e).__name__}: {e}"
    job["seconds"] = round(time.time() - t, 1)
    path.write_text(json.dumps(job, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
