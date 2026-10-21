"""Local voice worker for ShortsMaker: CosyVoice 3 through VoiceStudio (items with "engine"), else Qwen3-TTS
(CustomVoice 1.7B, no style instruction), + word timings.

Runs in its own venv (qwen_venv: qwen-tts pins transformers versions that would break gen.py's LTX/SDXL).
Usage: python qwen_voice.py job.json, same job format as gen.py: {"task": "tts", "items": [{"text",
"speaker", "seed", "out" (.wav)}]} -> each item gets "words": [[start, end, word], ...] and "ok".
Qwen gives no timestamps, so the known script is force-aligned to the audio with torchaudio's MMS model.
"""
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

HERE = Path(__file__).parent
os.environ.setdefault("TORCH_HOME", str(HERE / "hf" / "torch"))  # MMS aligner weights live next to the HF models
QWEN_REPO = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"
STUDIO = "http://127.0.0.1:3900"  # VoiceStudio's local backend (D:\VoiceStudio), for CosyVoice items
NUM = re.compile(r"(\$)?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)(%|s|st|nd|rd|th)?", re.I)


def say_number(tok: str) -> str:
    """How a narrator reads a number token: 1932 -> nineteen thirty-two, 20,000 -> twenty thousand, 1880s ->
    eighteen eighties, 3rd -> third, $10,000 -> ten thousand dollars, 40% -> forty percent."""
    from num2words import num2words

    def one(m: re.Match) -> str:
        dollar, digits, suf = m.group(1), m.group(2).replace(",", ""), (m.group(3) or "").lower()
        n = float(digits) if "." in digits else int(digits)
        if suf in ("st", "nd", "rd", "th"):
            return num2words(n, to="ordinal")
        year = isinstance(n, int) and "," not in m.group(2) and 1100 <= n <= 2099 and not dollar
        words = num2words(n, to="year") if year else num2words(n)
        if suf == "s":  # decades: "eighteen eighty" -> "eighteen eighties"
            words = re.sub(r"y$", "ies", words) if words.endswith("y") else words + "s"
        return words + (" percent" if suf == "%" else "") + (" dollars" if dollar else "")
    return NUM.sub(lambda m: f" {one(m)} ", tok)


def align_words(text: str) -> list[tuple[str, list[str]]]:
    """Caption words (as written, punctuation attached) with the a-z words the aligner listens for.
    A token with nothing to say ("-", "&") sticks to the word before it, like Kokoro's punctuation."""
    out: list[tuple[str, list[str]]] = []
    for tok in text.split():
        spoken = unicodedata.normalize("NFKD", say_number(tok).replace("&", " and ")).encode("ascii", "ignore").decode()
        parts = [p for p in re.sub(r"[^a-z']+", " ", spoken.lower().replace("-", " ")).split() if p.strip("'")]
        parts = [p.strip("'") for p in parts]
        if parts:
            out.append((tok, parts))
        elif out:
            out[-1] = (out[-1][0] + " " + tok, out[-1][1])
    return out


def speak(items: list[dict]) -> None:
    import numpy as np
    import soundfile as sf
    import torch
    from huggingface_hub import snapshot_download
    from qwen_tts import Qwen3TTSModel
    # a local folder: from_pretrained with a repo id calls the Hub API, which fails in offline batch runs
    model = Qwen3TTSModel.from_pretrained(snapshot_download(QWEN_REPO, local_files_only=True), device_map="cuda:0",
                                          dtype=torch.bfloat16, attn_implementation="sdpa")
    for it in items:
        torch.manual_seed(int(it.get("seed", 0)))  # same scene, same delivery on a fix.bat re-render
        wavs, sr = model.generate_custom_voice(text=it["text"], language="English", speaker=it["speaker"])
        audio = np.asarray(wavs[0], dtype=np.float32)
        if audio.size < sr // 4:
            raise RuntimeError(f"no audio for {it['text'][:40]!r}")
        sf.write(it["out"], audio, sr)
    del model
    torch.cuda.empty_cache()


def studio_speak(items: list[dict]) -> None:
    """CosyVoice 3 in VoiceStudio (owner's pick 2026-10-20): aiden's voice cloned from a reference clip, read
    with the item's `instruct`. Numbers go in already spelled out so the voice says exactly what align() expects."""
    import urllib.request
    import uuid
    for it in items:
        spoken = re.sub(r"\s+([,.!?;:])", r"\1", " ".join(say_number(tok).strip() for tok in it["text"].split()))
        fields = {"text": spoken, "language": "en",
                  "engine": it["engine"], "ref_text": it["ref_text"], "instruct": it["instruct"],
                  "seed": str(int(it.get("seed", 0)))}
        b = uuid.uuid4().hex
        body = b"".join(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
                        for k, v in fields.items())
        body += (f'--{b}\r\nContent-Disposition: form-data; name="ref_audio"; filename="ref.wav"\r\n'
                 "Content-Type: audio/wav\r\n\r\n").encode() + Path(it["ref"]).read_bytes() + f"\r\n--{b}--\r\n".encode()
        req = urllib.request.Request(STUDIO + "/generate", body, {"Content-Type": f"multipart/form-data; boundary={b}"})
        with urllib.request.urlopen(req, timeout=300) as r:
            audio = r.read()
        if audio[:4] != b"RIFF" or len(audio) < 24000:  # not a wav, or under ~0.5 s of speech
            raise RuntimeError(f"no audio for {it['text'][:40]!r}")
        out = Path(it["out"])
        if float(it.get("speed", 1.0)) == 1.0:
            out.write_bytes(audio)
            continue
        # VoiceStudio ignores `speed` for CosyVoice (tested 2026-10-20), so tempo it here; pitch stays the same
        raw = out.with_name(out.stem + "_raw.wav")
        raw.write_bytes(audio)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-filter:a", f"atempo={it['speed']}",
                        str(out)], check=True)
        raw.unlink()


def align(items: list[dict]) -> None:
    import soundfile as sf
    import torch
    import torchaudio
    bundle = torchaudio.pipelines.MMS_FA
    model = bundle.get_model(with_star=False).to("cuda")
    tokenizer, aligner = bundle.get_tokenizer(), bundle.get_aligner()
    for it in items:
        words = align_words(it["text"])
        audio, sr = sf.read(it["out"], dtype="float32")
        wave = torchaudio.functional.resample(torch.from_numpy(audio).unsqueeze(0), sr, bundle.sample_rate).to("cuda")
        with torch.inference_mode():
            emission, _ = model(wave)
        flat = [p for _, parts in words for p in parts]
        spans = aligner(emission[0], tokenizer(flat))
        sec = wave.size(1) / emission.size(1) / bundle.sample_rate
        out, k = [], 0
        for shown, parts in words:  # a number read as several words keeps one caption word over their whole span
            first, last = spans[k], spans[k + len(parts) - 1]
            out.append([round(first[0].start * sec, 3), round(last[-1].end * sec, 3), shown])
            k += len(parts)
        it.update(words=out, ok=True)


def main() -> None:
    path = Path(sys.argv[1])
    job = json.loads(path.read_text(encoding="utf-8"))
    t = time.time()
    try:
        (studio_speak if job["items"][0].get("engine") else speak)(job["items"])
        align(job["items"])
    except Exception as e:  # items without "ok" fall back to Kokoro in shortsmaker/gpu.py local_voice()
        job["error"] = f"{type(e).__name__}: {e}"
    job["seconds"] = round(time.time() - t, 1)
    path.write_text(json.dumps(job, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
