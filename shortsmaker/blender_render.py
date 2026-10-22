"""Draw a Short in Blender (2026-10-22): after the voice sets every scene's length, write work/build.json (the build
plan + each scene's frames and failure peak), run headless Blender on blender/build_scene.py, and cut the frames
into one clip per scene (work/blender{i}.mp4) that the renderers play like real film. Unchanged build.json and all
frames present: the frames are reused (fix rounds, re-runs). Blender failing twice raises BlenderFailed."""

import hashlib
import json
import subprocess
from pathlib import Path

from shortsmaker import config, media_tools, plan_rules

FPS = 30
TIMEOUT = 30 * 60  # a 40-second Short draws in about 10 minutes
SCRIPT = config.ROOT / "blender" / "build_scene.py"


class BlenderFailed(RuntimeError):
    """Blender couldn't draw the Short (missing, crashed or timed out twice)."""


def code_version() -> str:
    """A fingerprint of the drawing code (blender/*.py): frames drawn by older code are never reused."""
    h = hashlib.sha1()
    for f in sorted(SCRIPT.parent.glob("*.py")):
        h.update(f.read_bytes())
    return h.hexdigest()[:12]


def scene_frames(bounds: list[float], fps: int = FPS) -> list[tuple[int, int]]:
    """(first, last) frame of every scene, 1-based and back to back; even a very short scene gets one frame."""
    out, first = [], 1
    for end in bounds[1:]:
        last = max(round(end * fps), first)
        out.append((first, last))
        first = last + 1
    return out


def peaks(short: dict, bounds: list[float], all_words: list) -> list[float]:
    """When each scene's failure peaks: on its emphasis word when spoken, else 70% into the scene."""
    out = []
    for i, sc in enumerate(short["scenes"]):
        a, b = bounds[i], bounds[i + 1]
        said = [w for w in all_words if a <= w[0] < b]
        t = plan_rules.spoken_at(said, sc["emphasis"]) if sc.get("emphasis") else None
        out.append(t if t is not None else a + 0.7 * (b - a))
    return out


def _run(exe: Path, job_path: Path) -> str:
    """'' when Blender finished, else why not."""
    try:
        r = subprocess.run([str(exe), "-b", "--factory-startup", "--python-exit-code", "1", "--python", str(SCRIPT),
                            "--", str(job_path)],
                           capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return f"timed out after {TIMEOUT // 60} minutes"
    tail = (r.stderr or r.stdout or "").strip().splitlines()[-1:]
    return "" if r.returncode == 0 else f"exit code {r.returncode}: {tail[0] if tail else 'no message'}"


def render_clips(short: dict, bounds: list[float], all_words: list, work: Path, exe: Path | None = None) -> dict[int, Path]:
    exe = exe or config.BLENDER
    if not exe.exists():
        raise BlenderFailed(f"Blender not found at {exe}")
    work.mkdir(parents=True, exist_ok=True)
    frames = work / "blender_frames"
    ranges, pk = scene_frames(bounds), peaks(short, bounds, all_words)
    job = {"plan": short["build"], "code": code_version(), "fps": FPS, "frames_dir": str(frames), "only_frames": None,
           "scenes": [{"start": bounds[i], "end": bounds[i + 1], "first": a, "last": b, "peak": pk[i],
                       "peak_frame": round(pk[i] * FPS) + 1} for i, (a, b) in enumerate(ranges)]}
    text = json.dumps(job, ensure_ascii=False, sort_keys=True)
    done = frames / "build.json"
    clips = {i: work / f"blender{i}.mp4" for i in range(len(ranges))}
    ends = sorted({f for pair in ranges for f in pair})  # kept after cutting: each scene's still, the zoom's last frame
    if done.exists() and done.read_text(encoding="utf-8") == text and all(c.exists() for c in clips.values()) \
            and all((frames / f"f_{f:04d}.png").exists() for f in ends):
        return clips
    frames.mkdir(exist_ok=True)
    for old in list(frames.glob("f_*.png")) + [done]:
        old.unlink(missing_ok=True)
    (work / "build.json").write_text(text, encoding="utf-8")
    print(f"  Blender: drawing {ranges[-1][1]} frames (about {ranges[-1][1] * 0.3 / 60:.0f} min)...")
    why = ""
    for attempt in range(2):
        why = _run(exe, work / "build.json")
        missing = [f for f in range(1, ranges[-1][1] + 1) if not (frames / f"f_{f:04d}.png").exists()]
        if not why and not missing:
            break
        why = why or f"{len(missing)} frames missing"
        print(f"    Blender failed ({why}){', trying once more' if not attempt else ''}")
    else:
        raise BlenderFailed(why)
    for i, (a, b) in enumerate(ranges):
        media_tools.ffmpeg("-framerate", str(FPS), "-start_number", str(a), "-i", str(frames / "f_%04d.png"),
                           "-frames:v", str(b - a + 1), *media_tools.video_encoder(), "-pix_fmt", "yuv420p",
                           clips[i].name, cwd=work)
    keep = {f"f_{f:04d}.png" for f in ends}  # ~1.5 GB of PNGs per Short otherwise, kept for KEEP_WORK_DAYS
    for png in frames.glob("f_*.png"):
        if png.name not in keep:
            png.unlink()
    done.write_text(text, encoding="utf-8")
    return clips
