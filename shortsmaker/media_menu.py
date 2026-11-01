"""Plain-language media.bat: import, audition, approve and tune local media."""

import json
import os
import re
import subprocess
from pathlib import Path

from shortsmaker import audio_library, audio_mix, media_library, media_tools
from shortsmaker.config import MOODS, MUSIC, OUTPUT, ROOT, STORY_SFX


def download_audio_choices(name: str, mood: str | None = None, count: int = 3) -> list[Path]:
    """New library downloads wait for the owner's ears; existing approved files are never overwritten."""
    rows = audio_mix.freesound_results(name, music=mood is not None, limit=25)
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    folder = MUSIC / mood if mood else STORY_SFX / slug
    folder.mkdir(parents=True, exist_ok=True)
    saved = []
    for row in rows:
        if len(saved) >= count:
            break
        path = folder / f"fs_{row['id']}{'.mp3' if mood else '.wav'}"
        if path.exists():
            saved.append(path)
            continue
        blob = audio_mix.freesound_preview(row)
        if not blob:
            continue
        if mood:
            path.write_bytes(blob)
        else:
            raw = path.with_suffix(".download")
            raw.write_bytes(blob)
            try:
                media_tools.ffmpeg("-i", str(raw), "-af", "silenceremove=start_periods=1:start_threshold=-45dB,"
                                   "atrim=0:3.5,highpass=f=220,highpass=f=220,loudnorm=I=-18:TP=-2:LRA=11",
                                   "-ar", "44100", "-ac", "2", str(path), cwd=folder)
            except subprocess.SubprocessError:
                continue
            finally:
                raw.unlink(missing_ok=True)
        source = f"https://freesound.org/s/{row['id']}/"
        audio_library.set_audio_metadata(path, approved=False, review_status="pending", title=row.get("name"),
                                        aliases=[name] if not mood else [], tags=row.get("tags") or [],
                                        description=str(row.get("description") or "")[:2000], source_url=source,
                                        license=row.get("license"), start=0, intensity="low", instruments=[])
        path.with_suffix(path.suffix + ".txt").write_text(
            f"{row.get('name')} — Freesound #{row['id']} — {row.get('license')}\n{source}\n", encoding="utf-8")
        saved.append(path)
    return saved


MUSIC_SEARCHES = {
    "mysterious": ["mysterious music", "ambient mystery"],
    "tense": ["tension music", "suspense music"],
    "playful": ["playful music", "comedy music"],
    "somber": ["sad piano", "somber music"],
    "epic": ["epic music", "orchestral music"],
}


def seed_audio_library(count: int = 4) -> dict:
    totals = {}
    for mood, terms in MUSIC_SEARCHES.items():
        saved = set()
        for query in terms:
            saved.update(download_audio_choices(query, mood, count))
            if len(saved) >= count:
                break
        totals[mood] = len(saved)
        print(f"  {mood}: {len(saved)} music choices ready to review")
    return totals


def audition_audio(path: Path) -> None:
    print(f"Opening {path.name}. Close or pause the player before comparing the next file.")
    os.startfile(str(path))


def review_audio_files(root: Path) -> None:
    files = [p for p in sorted(root.rglob("*")) if p.suffix.lower() in audio_library.AUDIO_EXTS]
    if not files:
        print("No audio files yet.")
        return
    for i, path in enumerate(files, 1):
        meta = audio_library.audio_metadata(path)
        state = meta.get("review_status") or ("approved" if meta.get("approved") is True else "existing")
        print(f"{i:3}. [{state}] {path.relative_to(root)} — {meta.get('title', '')}")
    while True:
        answer = input("File number to listen/edit (Enter to go back): ").strip()
        if not answer:
            return
        if not answer.isdigit() or not 1 <= int(answer) <= len(files):
            continue
        path = files[int(answer) - 1]
        meta = audio_library.audio_metadata(path)
        print(json.dumps({k: meta.get(k) for k in ("title", "source_url", "tags", "start", "impact", "intensity", "instruments", "aliases")}, indent=2))
        action = input("P=play, A=approve, R=reject, E=edit timing/tags: ").strip().lower()
        if action == "p":
            audition_audio(path)
        elif action in ("a", "r"):
            audio_library.set_audio_metadata(path, approved=action == "a", review_status="approved" if action == "a" else "rejected")
        elif action == "e":
            music = root == MUSIC
            value = input("Music start time in seconds: " if music else "Main impact time in seconds: ").strip()
            try:
                seconds = float(value)
                if not 0 <= seconds <= media_tools.duration(path):
                    raise ValueError()
                audio_library.set_audio_metadata(path, **{"start" if music else "impact_override": seconds})
                if not music:
                    audio_library.set_audio_metadata(path, impact=seconds)
            except ValueError:
                print("Timing unchanged: enter seconds within the file.")
            if music:
                intensity = input("Intensity (low/medium/high, Enter to keep): ").strip().lower()
                if intensity in ("low", "medium", "high"):
                    audio_library.set_audio_metadata(path, intensity=intensity)
                instruments = input("Instruments, separated by commas (Enter to keep): ").strip()
                if instruments:
                    audio_library.set_audio_metadata(path, instruments=[s.strip().lower() for s in instruments.split(",") if s.strip()])
            else:
                aliases = input("Sound search names, separated by commas (Enter to keep): ").strip()
                if aliases:
                    audio_library.set_audio_metadata(path, aliases=[s.strip().lower() for s in aliases.split(",") if s.strip()])


def print_source_status() -> None:
    try:
        status = json.loads(media_library.STATUS.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        status = {}
    for name, enabled in media_library.settings().get("sources", {}).items():
        message = status.get(name, {}).get("status", "Not checked yet") if enabled else "Disabled"
        if name == "europeana" and not media_library.optional_key("europeana"):
            message = "Optional: needs your free API key; no account/key was created"
        print(f"  {name}: {message}")
    print(f"Local pictures/videos: {media_library.LIBRARY}")
    print("A saved file can have a .json sidecar containing title, tags, source_url and credit.")


def media_command(args: list[str]) -> None:
    if args == ["--seed-music"]:
        seed_audio_library()
        return
    if args == ["--status"]:
        print_source_status()
        return
    while True:
        print("\nMEDIA LIBRARY\n1 Import a picture/video\n2 Listen/approve music\n3 Listen/approve sound effects\n"
              "4 Find more free music\n5 Find sound variants\n6 Preview music with recent narration\n7 Source status\n"
              "8 Add an official brand media page\n9 Import your music/sound effect\nEnter Exit")
        choice = input("Choose: ").strip()
        if not choice:
            return
        try:
            if choice == "1":
                path = Path(input("Picture/video file (you can drag it here): ").strip().strip('"'))
                out = media_library.import_media(path, input("Title: "), input("Search tags (brand, product, year, country): "),
                                                 input("Original source URL (if known): "), input("Credit/rights note: "))
                print(f"Imported: {out}")
            elif choice == "2":
                review_audio_files(MUSIC)
            elif choice == "3":
                review_audio_files(STORY_SFX)
            elif choice == "4":
                seed_audio_library()
            elif choice == "5":
                query = input("Sound, e.g. single ship bell or mechanical cash register: ").strip()
                if query:
                    print(f"{len(download_audio_choices(query))} variants ready to review.")
            elif choice == "6":
                voices = sorted(OUTPUT.glob("*/*/work/voice.wav"), key=lambda p: p.stat().st_mtime, reverse=True)
                if not voices:
                    print("No recent narration found.")
                    continue
                for i, mood in enumerate(MOODS, 1):
                    print(f"{i}. {mood}")
                selection = input("Mood number: ").strip()
                if not selection.isdigit() or not 1 <= int(selection) <= len(MOODS):
                    continue
                short = {"music_mood": MOODS[int(selection) - 1]}
                track = audio_library.select_music(short)
                if not track:
                    print(short.get("music_note"))
                    continue
                out = ROOT / "cache" / "music_preview.wav"
                out.parent.mkdir(parents=True, exist_ok=True)
                audio_library.preview_mix(voices[0], track, out, audio_library.track_start(track, short))
                audition_audio(out)
            elif choice == "7":
                print_source_status()
            elif choice == "8":
                name = input("Brand/company name: ").strip()
                aliases = input("Search names/products, separated by commas: ").strip()
                pages = [s.strip() for s in input("Public official media page URLs, separated by commas: ").split(",") if s.strip()]
                if not name or not pages or not all(url.startswith("https://") for url in pages):
                    print("Enter a name and public HTTPS page URLs.")
                    continue
                data = media_library.settings()
                brands = [row for row in data.get("brands", []) if row.get("name", "").lower() != name.lower()]
                brands.append({"name": name, "aliases": [name.lower()] + [s.strip().lower() for s in aliases.split(",") if s.strip()], "pages": pages})
                data["brands"] = brands
                media_tools.write_json(media_library.SETTINGS, data)
                print("Saved. Public downloadable pictures/videos will be searched for matching stories.")
            elif choice == "9":
                path = Path(input("Audio file (you can drag it here): ").strip().strip('"'))
                name = input("Track title or sound search name: ").strip()
                mood = input("Music mood (mysterious/tense/playful/somber/epic), or Enter for sound effect: ").strip().lower() or None
                target = audio_library.import_audio_file(path, name, mood, input("Credit/rights note: "), input("Original source URL (if known): "))
                print(f"Imported for listening/approval: {target}")
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            print(f"Could not complete that action ({type(error).__name__}). Your original files were kept.")
