"""Music/SFX metadata, recent choices, approval and short mix previews."""

import json
import hashlib
import math
import random
import re
import shutil
import subprocess
from pathlib import Path

from shortsmaker import media_library, media_tools
from shortsmaker.config import MOODS, MUSIC, SFX, STORY_SFX


AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".flac", ".m4a"}
MUSIC_HISTORY = MUSIC / "recent.json"
SOUND_HISTORY = SFX / "recent.json"


def audio_metadata(path: Path) -> dict:
    try:
        data = json.loads(path.with_suffix(path.suffix + ".json").read_text(encoding="utf-8-sig"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def set_audio_metadata(path: Path, **values) -> None:
    data = audio_metadata(path)
    data.update(values)
    media_tools.write_json(path.with_suffix(path.suffix + ".json"), data)


def usable_audio(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in AUDIO_EXTS and audio_metadata(path).get("approved") is not False


def import_audio_file(path: Path, name: str, mood: str | None, credit: str, source: str = "") -> Path:
    path = path.expanduser().resolve(strict=True)
    if path.suffix.lower() not in AUDIO_EXTS or (mood is not None and mood not in MOODS):
        raise ValueError("Choose a supported sound/music file and a valid music mood.")
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "sound"
    folder = MUSIC / mood if mood else STORY_SFX / slug
    folder.mkdir(parents=True, exist_ok=True)
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()[:12]
    target = folder / f"{slug}_{digest}{path.suffix.lower()}"
    if target != path:
        shutil.copy2(path, target)
    set_audio_metadata(target, title=name or path.stem, aliases=[] if mood else [name.lower()],
                       approved=False, review_status="pending", source_url=source,
                       license=credit or "Owner supplied; rights not specified", start=0)
    target.with_suffix(target.suffix + ".txt").write_text(f"{name}: {credit or 'Owner supplied; rights not specified'}\n{source}\n", encoding="utf-8")
    return target


def history_read(path: Path) -> list:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return [row for row in data if isinstance(row, dict)] if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def record_audio(path: Path, root: Path, history: Path, job: str = "") -> None:
    entries = history_read(history)
    # A fix/resume replaces this job's choice rather than using up the no-repeat window again.
    entries = [row for row in entries if not job or row.get("job") != job]
    entries.append({"file": path.relative_to(root).as_posix(), "job": job})
    history.parent.mkdir(parents=True, exist_ok=True)
    media_tools.write_json(history, entries[-30:])


def select_music(short: dict, prior: Path | None = None) -> Path | None:
    if prior and usable_audio(prior):
        return prior
    mood = short.get("music_mood")
    if mood not in MOODS:
        short["music_note"] = "No recognized music mood; left silent"
        return None
    tracks = [p for p in sorted((MUSIC / mood).glob("*")) if usable_audio(p)]
    if not tracks:
        short["music_note"] = f"No approved {mood} music; left silent (add tracks with media.bat)"
        return None
    recent = [row.get("file") for row in history_read(MUSIC_HISTORY)[-5:]]
    fresh = [p for p in tracks if p.relative_to(MUSIC).as_posix() not in recent]
    available = fresh or tracks
    intensity = short.get("music_intensity", "low")
    instruments = set(short.get("music_instruments") or [])

    def score(path):
        meta = audio_metadata(path)
        return (2 * (meta.get("intensity") == intensity)
                + len(instruments & set(meta.get("instruments") or [])))

    best = max(map(score, available))
    choices = [p for p in available if score(p) == best]
    if not fresh:
        # Reuse the least recently heard file once a small mood library is exhausted.
        oldest = sorted(choices, key=lambda p: max((i for i, name in enumerate(recent)
                                                    if name == p.relative_to(MUSIC).as_posix()), default=-1))
        return oldest[0]
    return random.choice(choices)


def source_music(short: dict, prior: Path | None = None) -> Path | None:
    """For one Short, search metadata and fetch only its selected track. Saved/local music is the fallback."""
    if prior and usable_audio(prior):
        return prior
    mood = short.get("music_mood")
    if mood not in MOODS:
        return select_music(short)
    fallback = select_music(short)
    if media_library.settings().get("music_online", True) is False:
        return fallback
    from shortsmaker import audio_mix
    base = {"mysterious": "mysterious music", "tense": "suspense music", "playful": "playful music",
            "somber": "sad music", "epic": "epic music"}[mood]
    instruments = [v.lower().strip() for v in short.get("music_instruments", []) if isinstance(v, str) and v.strip()][:2]
    queries = list(dict.fromkeys([" ".join([base, *instruments]), base]))
    recent = {row.get("file") for row in history_read(MUSIC_HISTORY)[-5:]}
    candidates = []
    for query in queries:
        # Avoid singing/speech competing with the narrator. These are metadata searches, not downloads.
        rows = audio_mix.freesound_results(query + " -vocals -speech -singing", music=True, limit=10)
        for row in rows:
            if type(row.get("id")) is not int or row["id"] <= 0:
                continue
            license_name = str(row.get("license", "")).lower()
            if "creativecommons.org/publicdomain/zero/" not in license_name and license_name not in ("cc0", "creative commons 0"):
                continue
            path = MUSIC / mood / f"fs_{row['id']}.mp3"
            if audio_metadata(path).get("approved") is False:
                continue  # explicit pending/rejected choices remain the owner's decision
            candidates.append((path, row))
        if candidates:
            break
    fresh = [(path, row) for path, row in candidates if path.relative_to(MUSIC).as_posix() not in recent]
    if candidates and not fresh and fallback:
        short["music_note"] = "Online matches were used recently; using the local library"
        return fallback
    choices = fresh or candidates
    if not choices:
        short["music_note"] = ("Online search found no fitting music; using the local library" if fallback else
                               f"No fitting online or local {mood} music; left silent")
        return fallback
    path, row = choices[0]  # the source ranks query matches before popularity
    if usable_audio(path):
        short["music_note"] = "Reused the selected online track from the local cache"
        return path
    print(f"  sourcing one {mood} music track for this Short...")
    blob = audio_mix.freesound_preview(row)
    if not blob:
        short["music_note"] = "Selected online music unavailable; using the local library" if fallback else "Selected online music unavailable; left silent"
        return fallback
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".part.mp3")
    try:
        temp.write_bytes(blob)
        length = media_tools.duration(temp)
        if not math.isfinite(length) or length < 10:
            raise ValueError("Music preview is too short or invalid")
        source = f"https://freesound.org/s/{row['id']}/"
        set_audio_metadata(path, approved=True, review_status="automatic", title=row.get("name"),
                           source_url=source, license=row.get("license"), tags=row.get("tags") or [],
                           description=str(row.get("description") or "")[:2000], start=0,
                           instruments=[v for v in instruments if v in (row.get("tags") or [])])
        path.with_suffix(".mp3.txt").write_text(
            f"{row.get('name')} — Freesound #{row['id']} — {row.get('license')}\n{source}\n", encoding="utf-8")
        temp.replace(path)
        short["music_note"] = "Selected and downloaded for this Short from Freesound (CC0)"
        return path
    except (OSError, ValueError, subprocess.SubprocessError):
        short["music_note"] = "Selected online music failed validation; using the local library" if fallback else "Selected online music failed validation; left silent"
        return fallback
    finally:
        temp.unlink(missing_ok=True)


def track_start(path: Path, short: dict) -> float:
    meta = audio_metadata(path)
    raw = short.get("music_start", meta.get("start", 0))
    try:
        start = float(raw)
        return max(0.0, min(start, max(0.0, media_tools.duration(path) - 1))) if math.isfinite(start) else 0.0
    except (OSError, ValueError, TypeError, subprocess.SubprocessError):
        return 0.0


def ducking_filter() -> str:
    options = media_library.settings().get("music_ducking") or {}
    values = {}
    for key, default, lo, hi in (("threshold", 0.03, 0.001, 0.5), ("ratio", 4, 1, 20),
                                  ("attack", 15, 1, 100), ("release", 350, 50, 1500)):
        try:
            value = float(options.get(key, default))
            values[key] = max(lo, min(hi, value)) if math.isfinite(value) else default
        except (ValueError, TypeError):
            values[key] = default
    return "sidechaincompress=" + ":".join(f"{k}={v:g}" for k, v in values.items())


def approved_sound(name: str, lib: Path = STORY_SFX) -> Path | None:
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    found = []
    for path in sorted(lib.rglob("*")) if lib.exists() else []:
        if not usable_audio(path):
            continue
        meta = audio_metadata(path)
        aliases = [str(x).lower() for x in meta.get("aliases", [])]
        names = {path.stem, path.parent.name, re.sub(r"__.*$", "", path.stem)}
        if slug in names or name.lower() in aliases:
            found.append(path)
    if not found:
        return None
    recent = [row.get("file") for row in history_read(SOUND_HISTORY)[-6:]]
    preferred = [p for p in found if p.relative_to(SFX).as_posix() not in recent] if lib == STORY_SFX else found
    return random.choice(preferred or found)


def sound_profile(path: Path) -> dict:
    """Measure once: duration and strongest 10-ms window (the impact: where the hit lands), with explicit owner
    overrides. A steady sound (static, rain, a crowd) has no hit: impact 0, so it starts on its word."""
    meta = audio_metadata(path)
    stamp = [path.stat().st_size, path.stat().st_mtime_ns, 2]  # 2: steady sounds get impact 0 (2026-11-05)
    if meta.get("profile_stamp") == stamp and "duration" in meta and "impact" in meta:
        return meta
    result = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-t", "30", "-f", "s16le", "-ac", "1",
                             "-ar", "8000", "-"], capture_output=True, timeout=20)
    if result.returncode:
        return {**meta, "duration": 0.5, "impact": 0}
    import array
    samples = array.array("h", result.stdout[:len(result.stdout) // 2 * 2])
    windows = [sum(v * v for v in samples[i:i + 80]) for i in range(0, len(samples), 80)]
    loud = sorted(w for w in windows if w)
    # A hit stands out (4x the median energy, +6 dB); radio static's "loudest" 10 ms fell at 3.2 s of 3.5 s, so it
    # started 3.2 s early and ran under the whole sentence (wooden-eagle Short, 2026-11-05)
    hit = bool(loud) and max(windows) >= 4 * loud[len(loud) // 2]
    measured = windows.index(max(windows)) * 0.01 if hit else 0.0
    set_audio_metadata(path, duration=len(samples) / 8000, impact=meta.get("impact_override", measured), profile_stamp=stamp)
    return audio_metadata(path)


def preview_mix(voice: Path, track: Path, out: Path, start: float = 0) -> Path:
    from shortsmaker import audio_mix
    media_tools.ffmpeg("-i", str(voice), "-stream_loop", "-1", "-ss", str(start), "-i", str(track),
                       "-filter_complex", f"[0:a]asplit[v][key];[1:a]volume={audio_mix.music_gain(track):.5f}[m];"
                       f"[m][key]{ducking_filter()}[duck];[v][duck]amix=inputs=2:normalize=0,"
                       "loudnorm=I=-14:TP=-1.5:LRA=11[out]", "-map", "[out]", "-t", "12", str(out), cwd=out.parent)
    return out
