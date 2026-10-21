"""Voice, captions, sound effects, story sounds and music levels."""

import asyncio
import json
import math
import random
import re
import subprocess
import time
import urllib.parse
import urllib.request
import wave
from pathlib import Path

import edge_tts

from shortsmaker import media_tools, plan_rules, session
from shortsmaker.config import (
    FREESOUND_KEY, GRAPHIC_STYLES, H, MAX_STORY_SOUNDS, SFX, STORY_SFX, STORY_SOUND_GAIN, W, ass_colour,
)


def speak(text: str, voice: str, path: Path) -> list[tuple[float, float, str]]:
    """TTS with retries: Microsoft's free Edge voice service drops a request now and then."""
    for attempt in range(5):
        try:
            return asyncio.run(tts(text, voice, path))
        except Exception as e:
            if attempt == 4:
                raise
            print(f"    voice service hiccup ({type(e).__name__}), retrying...")
            time.sleep(3 * (attempt + 1))


async def tts(text: str, voice: str, path: Path) -> list[tuple[float, float, str]]:
    words = []
    with open(path, "wb") as f:
        async for chunk in edge_tts.Communicate(text, voice, boundary="WordBoundary").stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":  # offsets are in 100ns units
                start = chunk["offset"] / 1e7
                words.append((start, start + chunk["duration"] / 1e7, chunk["text"]))
    return words


_encoder: list[str] = []


def ass_time(t: float) -> str:
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02}:{t % 60:05.2f}"


def caption_lines(words: list[tuple[float, float, str]]) -> list[list[tuple[float, float, str]]]:
    """Caption lines of up to 3 words and about 16 letters: a long word ("SIXTY-THREE-YEAR-OLD") gets a
    shorter line instead of shrinking the whole line to a tiny size. Both renderers use these lines."""
    lines: list[list[tuple[float, float, str]]] = []
    for w in words:
        if lines and len(lines[-1]) < 3 and len(" ".join(x[2] for x in lines[-1] + [w])) <= 16:
            lines[-1].append(w)
        else:
            lines.append([w])
    return lines


def captions(words: list[tuple[float, float, str]], path: Path, emphasis: set[float]) -> None:
    """ASS captions, one caption_lines() line at a time; the spoken word turns yellow. Emphasis words (by start
    time) turn orange, grow and stay lit for the rest of their line."""
    lines = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "",
             "[V4+ Styles]",
             "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, "
             "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV",
             "Style: Default,Impact,120,&H00FFFFFF,&H00000000,&H90000000,0,1,8,4,2,60,60,620", "",
             "[Events]", "Format: Layer, Start, End, Style, Text"]
    groups = caption_lines(words)
    for g, chunk in enumerate(groups):
        chunk_end = groups[g + 1][0][0] if g + 1 < len(groups) else chunk[-1][1]
        for j, (start, _, _) in enumerate(chunk):
            end = chunk[j + 1][0] if j + 1 < len(chunk) else chunk_end

            def styled(k: int, w: tuple[float, float, str]) -> str:
                if w[0] in emphasis and k <= j:  # emphasis colour, 15% bigger, from when it's said to line end
                    return f"{{\\c{ass_colour(session.EMPHASIS)}\\3c{ass_colour(session.EMPHASIS, 0.4)}\\fscx115\\fscy115}}" + w[2].upper() + \
                        "{\\c&H00FFFFFF&\\3c&H00000000&\\fscx100\\fscy100}"
                return (f"{{\\c{ass_colour(session.YELLOW)}}}" + w[2].upper() + "{\\c&H00FFFFFF&}") if k == j else w[2].upper()
            text = " ".join(styled(k, w) for k, w in enumerate(chunk))
            pop = "{\\fscx80\\fscy80\\t(0,90,\\fscx100\\fscy100)}" if j == 0 else ""
            lines.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Default,{pop}{text}")
    path.write_text("\n".join(lines), encoding="utf-8")


SFX_FILES = ["whoosh0", "whoosh1", "whoosh2", "whoosh3", "flash0", "flash1",
             "stamp0", "stamp1", "shutter0", "shutter1", "pin", "ticks", "riser", "scratch"]


def clean_sound(v, said: list[str]) -> dict | None:
    """A planned story sound {"word", "sound"}, validated: the word must be spoken in the scene, the sound 1-4 plain words."""
    if not isinstance(v, dict) or not isinstance(v.get("word"), str) or not plan_rules.contains(said, plan_rules.words_of(v["word"])):
        return None
    name = " ".join(re.sub(r"[^a-z ]+", " ", str(v.get("sound") or "").lower()).split())
    return {"word": v["word"].strip(), "sound": name} if 0 < len(name.split()) <= 4 and len(name) <= 30 else None


def limit_sounds(scenes: list[dict]) -> None:
    """At most MAX_STORY_SOUNDS story sounds per Short (the first ones), so each one stays special."""
    kept = 0
    for sc in scenes:
        if sc.get("sound") and kept < MAX_STORY_SOUNDS:
            kept += 1
        else:
            sc["sound"] = None


def freesound_fetch(name: str) -> tuple[bytes, dict] | None:
    """One CC0 (no credit, any use) sound for `name` from Freesound's official API: the best-scoring short sound,
    preferring well-rated, much-downloaded ones; its high-quality preview MP3. None without a key or a match."""
    key = FREESOUND_KEY.read_text(encoding="utf-8-sig").strip() if FREESOUND_KEY.exists() else ""
    if not key:
        return None
    q = urllib.parse.urlencode({"query": name, "filter": 'license:"Creative Commons 0" duration:[0.15 TO 4]',
                                "fields": "id,name,duration,avg_rating,num_downloads,previews,license",
                                "page_size": 10, "sort": "score"})
    try:
        req = urllib.request.Request(f"https://freesound.org/apiv2/search/text/?{q}",
                                     headers={"Authorization": f"Token {key}", "User-Agent": "ShortsMaker/1.0"})
        results = json.load(urllib.request.urlopen(req, timeout=30)).get("results") or []
        if not results:
            return None
        best = next((r for r in results if (r.get("avg_rating") or 0) >= 3 and (r.get("num_downloads") or 0) >= 20), results[0])
        audio = urllib.request.urlopen(urllib.request.Request(best["previews"]["preview-hq-mp3"],
                                                              headers={"User-Agent": "ShortsMaker/1.0"}), timeout=30).read()
        return audio, best
    except (OSError, ValueError, KeyError):
        return None


def story_sound(name: str, lib: Path = STORY_SFX, fetch=freesound_fetch) -> Path | None:
    """The sound file for a story sound: the owner's own file in sfx/story/<name>.(wav|mp3|ogg|flac) wins; else one
    fetched from Freesound, trimmed, high-passed like every SFX, evened out and kept as sfx/story/<name>.wav (with a
    .txt note of where it came from), so each sound is fetched only once."""
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    for ext in (".wav", ".mp3", ".ogg", ".flac"):
        if (lib / f"{slug}{ext}").exists():
            return lib / f"{slug}{ext}"
    got = fetch(name)
    if not got:
        return None
    audio, meta = got
    lib.mkdir(parents=True, exist_ok=True)
    raw, out = lib / f"_{slug}.tmp", lib / f"{slug}.wav"
    raw.write_bytes(audio)
    try:
        media_tools.ffmpeg("-i", raw.name, "-af", "silenceremove=start_periods=1:start_threshold=-45dB,atrim=0:3.5,"
               "highpass=f=220,highpass=f=220,loudnorm=I=-18:TP=-2:LRA=11", "-ar", "44100", "-ac", "2", out.name, cwd=lib)
    except subprocess.CalledProcessError:
        return None
    finally:
        raw.unlink(missing_ok=True)
    (lib / f"{slug}.txt").write_text(f"Freesound #{meta.get('id')}: {meta.get('name')} ({meta.get('license')}) "
                                     f"https://freesound.org/s/{meta.get('id')}/\n", encoding="utf-8")
    return out


def make_sfx() -> None:
    """Synthesize the sound-effect library once (no downloads, no copyright). Hits, flashes and
    stamps get a short room reverb through ffmpeg so they sound designed, not like raw tones."""
    SFX.mkdir(exist_ok=True)
    sr = 44100

    def save(name: str, samples: list[float], reverb: bool = False) -> None:
        peak = max(abs(s) for s in samples) or 1
        dry = SFX / (name + "_dry.wav")
        with wave.open(str(dry), "wb") as f:
            f.setnchannels(1), f.setsampwidth(2), f.setframerate(sr)
            f.writeframes(b"".join(int(s / peak * 0.9 * 32767).to_bytes(2, "little", signed=True)
                                   for s in samples))
        # Everything is high-passed: synthetic low end comes out as a dull thump on phone speakers.
        chain = "apad=pad_dur=0.6,aecho=0.9:0.9:45|95|160:0.32|0.22|0.12,lowpass=f=7500," if reverb else ""
        media_tools.ffmpeg("-i", dry.name, "-af", chain + "highpass=f=220,highpass=f=220,alimiter=limit=0.9",
               name + ".wav", cwd=SFX)
        dry.unlink()

    def noise() -> float:
        return random.uniform(-1, 1)

    for v, bright in enumerate([0.35, 0.55]):  # flash cut: bright noise burst over a soft low thump
        n, out, phase, lp, prev = int(sr * 0.7), [], 0.0, 0.0, 0.0
        for k in range(n):
            t = k / sr
            x = noise()
            hp, prev = x - prev * (1 - bright), x  # crude high-pass keeps it airy
            phase += 2 * math.pi * 70 / sr
            out.append(hp * math.exp(-t * 9) * 0.6 + math.sin(phase) * math.exp(-t * 10))
        save(f"flash{v}", out, reverb=True)

    for v, f0 in enumerate([95, 80]):  # stamp: low thump + papery slap
        n, out, phase, b1, b2 = int(sr * 0.45), [], 0.0, 0.0, 0.0
        for k in range(n):
            t = k / sr
            phase += 2 * math.pi * f0 / sr
            b1 += 0.35 * (noise() - b1)
            b2 += 0.08 * (b1 - b2)
            out.append(math.sin(phase) * math.exp(-t * 22) + 1.6 * (b1 - b2) * math.exp(-t * 45))
        save(f"stamp{v}", out, reverb=True)

    for v, ring in enumerate([2100, 1700]):  # camera shutter: two quick mechanical clicks
        n, out = int(sr * 0.2), []
        for k in range(n):
            t = k / sr
            click = 0.0
            for t0, g in ((0.0, 1.0), (0.055, 0.7)):
                if t >= t0:
                    d = t - t0
                    click += g * (noise() * math.exp(-d * 900) + 0.5 * math.sin(2 * math.pi * ring * d) * math.exp(-d * 120))
            out.append(click)
        save(f"shutter{v}", out)

    n, out = int(sr * 0.6), []
    for k in range(n):  # map pin: soft plink with a tiny thud
        t = k / sr
        out.append(math.sin(2 * math.pi * 1320 * t) * math.exp(-t * 9) + 0.4 * math.sin(2 * math.pi * 1980 * t) * math.exp(-t * 14)
                   )
    save("pin", out)

    ticks, tt, gap = [], 0.0, 0.03  # year counter: fast ticks that slow down as it lands (~0.7s)
    while tt < 0.7:
        ticks.append(tt)
        tt += gap
        gap *= 1.18
    n, out = int(sr * 0.85), []
    for k in range(n):
        t = k / sr
        out.append(sum(math.sin(2 * math.pi * 3200 * (t - t0)) * math.exp(-(t - t0) * 260) for t0 in ticks if 0 <= t - t0 < 0.03))
    save("ticks", out)

    n, out, b1, b2 = int(sr * 2.2), [], 0.0, 0.0
    for k in range(n):  # riser: noise band sweeping up plus a rising tone, swelling into the payoff
        t = k / sr
        x = t / 2.2
        a = 1 - math.exp(-2 * math.pi * (300 * 18 ** x) / sr)
        b1 += a * (noise() - b1)
        b2 += a * 0.5 * (b1 - b2)
        tone = math.sin(2 * math.pi * (180 * t + 160 * t * t))
        out.append(((b1 - b2) * 1.4 + 0.25 * tone) * x ** 2.2)
    save("riser", out)

    n, out, b1, b2 = int(sr * 0.6), [], 0.0, 0.0
    for k in range(n):  # pen scratch (red underline, route line): bright noise in quick nib strokes
        t = k / sr
        b1 += 0.55 * (noise() - b1)
        b2 += 0.2 * (b1 - b2)
        stroke = max(0.0, math.sin(2 * math.pi * 11 * t)) ** 0.6
        out.append((b1 - b2) * stroke * min(1.0, t / 0.02) * math.exp(-t * 1.5))
    save("scratch", out)

    for v, (length, peak_hz) in enumerate([(0.55, 1400), (0.7, 1900), (0.85, 1100), (0.65, 2300)]):
        n, out, lp1, lp2 = int(sr * length), [], 0.0, 0.0
        for k in range(n):  # soft whoosh: noise through a lowpass that sweeps open then closed
            x = k / n
            cutoff = 200 + peak_hz * math.sin(math.pi * x) ** 2
            a = 1 - math.exp(-2 * math.pi * cutoff / sr)
            lp1 += a * (random.uniform(-1, 1) - lp1)
            lp2 += a * (lp1 - lp2)
            out.append(lp2 * math.sin(math.pi * x) ** 3)
        save(f"whoosh{v}", out)


def sfx_events(short: dict, cues: list[dict], bounds: list[float], remotion: bool) -> list[dict]:
    """Sound design: each timed visual gets a matching sound. Candidates are kept by priority;
    a sound is dropped if it would land within 0.5s of a more important one. No sub-bass hits:
    on phone speakers they read as random thumps. Ticks and the riser are quiet textures that may
    overlap. Returns the cue sheet sorted by time."""
    last: dict[str, int] = {}

    def pick(kind: str, n: int) -> str:  # never the same variant twice in a row
        v = random.choice([k for k in range(n) if k != last.get(kind)] or [0])
        last[kind] = v
        return f"{kind}{v}"

    cand = []
    scenes = short["scenes"]
    for i, sc in enumerate(scenes):
        start, cue, g = bounds[i], cues[i], sc["graphic"]
        if i and sc["transition"] == "flash":
            cand.append({"t": start - 0.05, "sound": pick("flash", 2), "gain": 0.9, "prio": 8, "what": "flash cut"})
        elif i and sc["transition"] == "whip" and remotion:  # owner dislikes loud whooshes: quiet, and only on whips
            cand.append({"t": start - 0.1, "sound": pick("whoosh", 4), "gain": 0.2, "prio": 4, "what": "whip pan"})
        elif i and sc["transition"] == "fade" and random.random() < 0.5:  # cuts, wipes and leaks stay silent
            cand.append({"t": start - 0.35, "sound": pick("whoosh", 4), "gain": 0.12, "prio": 1, "what": "soft whoosh"})
        if (sc.get("sound") or {}).get("file") and cue.get("sound_at") is not None:
            cand.append({"t": cue["sound_at"], "sound": sc["sound"]["file"], "gain": STORY_SOUND_GAIN, "prio": 9,
                         "what": f"story sound: {sc['sound']['sound']}"})
        f, fc = sc.get("full"), cue.get("full")
        if f and fc and remotion:  # full-screen motion graphic: one sound per thing that lands
            if f["type"] == "board":
                cand += [{"t": t, "sound": "pin", "gain": 0.3, "prio": 5, "what": "print pinned to the board"} for t in fc["times"]]
            elif f["type"] == "journey":
                for k, t in enumerate(fc["times"]):
                    cand.append({"t": t, "sound": "pin", "gain": 0.3, "prio": 5, "what": "map pin drops"})
                    if k:
                        cand.append({"t": round(fc["times"][k - 1] + 0.2, 3), "sound": "scratch", "gain": 0.3, "prio": 4,
                                     "what": "route line draws"})
            elif f["type"] == "number":
                cand.append({"t": fc["at"], "sound": "ticks", "gain": 0.25, "prio": 5, "what": "number counts up"})
            elif f["type"] == "custom":
                beats = fc.get("cues") or [start + 0.4]
                for k, t in enumerate(beats):
                    cand.append({"t": t, "sound": "pin" if k == 0 else (pick("stamp", 2) if k == len(beats) - 1 else "scratch"),
                                 "gain": 0.35 if k == len(beats) - 1 else 0.28, "prio": 5, "what": "custom graphic beat"})
            else:
                cand.append({"t": start + 0.1, "sound": pick("stamp", 2), "gain": 0.45, "prio": 6, "what": "document lands"})
                cand.append({"t": fc["at"], "sound": "scratch", "gain": 0.35, "prio": 5, "what": "red underline"})
        at = cue.get("graphic")
        if g and g["style"] == "fact":
            cand.append({"t": at, "sound": pick("stamp", 2), "gain": 0.6, "prio": 6, "what": "fact box stamp"})
        elif g and g["style"] == "date":
            ticks = remotion and g["text"].isdigit()  # Remotion counts the year up; ticks follow it
            cand.append({"t": at, "sound": "ticks" if ticks else pick("stamp", 2),
                         "gain": 0.25 if ticks else 0.35, "prio": 5, "what": "year counter ticks" if ticks else "date stamp"})
        elif g and remotion and "lat" in g:
            cand.append({"t": at, "sound": pick("whoosh", 4), "gain": 0.15, "prio": 4, "what": "map flies in"})
            cand.append({"t": at + 1.5 * cue.get("map_pace", 1), "sound": "pin", "gain": 0.3, "prio": 5, "what": "map pin drop"})
        elif g and remotion and g["style"] == "stat":
            cand.append({"t": at + 0.3, "sound": "ticks", "gain": 0.25, "prio": 5, "what": "number counts up"})
        elif g and remotion and g["style"] == "timeline":
            cand.append({"t": at + 0.4, "sound": pick("whoosh", 4), "gain": 0.15, "prio": 4, "what": "timeline marker slides"})
        elif g and remotion and g["style"] == "mark":
            cand.append({"t": at + 0.4, "sound": "pin", "gain": 0.25, "prio": 5, "what": f"{g.get('shape', 'circle')} drawn"})
        elif g and remotion and g["style"] in ("stamp", "headline"):  # both land with a thump at ~0.25s
            cand.append({"t": at + 0.25, "sound": pick("stamp", 2), "gain": 0.6, "prio": 6, "what": GRAPHIC_STYLES[g["style"]]})
        elif g and remotion and g["style"] in ("question", "kinetic"):
            cand.append({"t": at, "sound": "ticks", "gain": 0.25 if g["style"] == "question" else 0.3, "prio": 5,
                         "what": GRAPHIC_STYLES[g["style"]]})
        elif g and remotion and g["style"] == "quote":
            cand.append({"t": at + 0.3, "sound": "ticks", "gain": 0.2, "prio": 5, "what": "quote types out"})
        elif g and remotion and g["style"] == "compare":
            cand.append({"t": at + 0.3, "sound": pick("whoosh", 4), "gain": 0.15, "prio": 4, "what": "bars grow"})
        elif g:
            cand.append({"t": at, "sound": "pin", "gain": 0.3, "prio": 5, "what": "location label"})
        if cue.get("card"):
            cand.append({"t": cue["on"], "sound": pick("shutter", 2), "gain": 0.45, "prio": 7, "what": "photo card shutter"})
    if cues[-1].get("cta") is not None:
        cand.append({"t": cues[-1]["cta"], "sound": "pin", "gain": 0.25, "prio": 3, "what": "subscribe button"})
    riser = None
    if len(scenes) > 2 and bounds[-2] > 6:  # build tension into the payoff scene
        riser = {"t": bounds[-2] - 2.2, "sound": "riser", "gain": 0.18, "prio": 2, "what": "riser into the payoff"}

    textures = [e for e in cand if e["sound"] in ("ticks", "scratch")] + ([riser] if riser else [])
    chosen: list[dict] = []
    for e in sorted((e for e in cand if e["sound"] not in ("ticks", "scratch")), key=lambda e: (-e["prio"], e["t"])):
        if not any(abs(e["t"] - c["t"]) < 0.5 for c in chosen):
            chosen.append(e)
    chosen += textures
    for e in chosen:
        e["t"] = max(0.0, e["t"])
    return sorted(chosen, key=lambda e: e["t"])


# Background music level before ducking. The tracks range from -9 to -28 LUFS, so the old fixed volume (0.22) buried
# Thinking Music (-22) under Mike's narration (owner: "no background audio"). The ducking takes ~10 dB more under
# the near-constant voice: -25 here puts the music ~21 dB under a -14.7 LUFS voice (-30 left it 26 dB under, faint).
MUSIC_LUFS = -25.0


def music_gain(track: Path) -> float:
    """Volume factor that brings this track's loudness (first 60 s) to MUSIC_LUFS; 0.22 if it can't be measured."""
    out = subprocess.run(["ffmpeg", "-hide_banner", "-t", "60", "-i", str(track), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    found = re.findall(r"^\s+I:\s+(-?[\d.]+) LUFS", out, re.M)
    if not found or float(found[-1]) < -70:  # unmeasurable or silent
        return 0.22
    return min(4.0, 10 ** ((MUSIC_LUFS - float(found[-1])) / 20))
