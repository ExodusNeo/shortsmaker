"""Small shared helpers: downloads, ffmpeg, video encoder choice, durations, JSON files, clock."""

import json
import subprocess
import urllib.request
from pathlib import Path

from shortsmaker import audio_mix


def fetch(url: str, timeout: int = 60, ua: str = "ShortsMaker/1.0 (personal video script)") -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def write_json(path: Path, data) -> None:
    """Write via a temp file, so an interrupted run never leaves a half-written file behind."""
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def duration(path: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout)


def video_encoder() -> list[str]:
    """Final H.264 encode: NVENC on the GPU when available (frees the CPU), else x264."""
    if not audio_mix._encoder:
        out = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True).stdout
        audio_mix._encoder.extend(["-c:v", "h264_nvenc", "-preset", "p5", "-cq", "20", "-b:v", "0"] if "h264_nvenc" in out
                        else ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20"])
    return audio_mix._encoder


def ffmpeg(*args: str, cwd: Path) -> None:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], cwd=cwd, check=True)


def clock(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:04.1f}"
