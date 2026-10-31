"""Command-line entry: making a batch (`main`), fix.bat's one-scene re-render, `library`, `notes`."""

import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

from shortsmaker import (
    blender_render, channel_profiles, checkpoints, llm, logbook, picker, picture_pool, retention, review, rules, scene_repair, seo, session,
    short_render, style_lab, writing,
)
from shortsmaker.config import OUTPUT


def main() -> None:
    # make_shorts.py [count] [channel] [claude|gemini]: anything missing is asked for (run.bat passes nothing);
    # with a count given, the planner defaults to the profile's last choice
    # make_shorts.py fix: fix.bat, re-render one scene of a recent Short
    if sys.argv[1:2] == ["resume"]:
        return resume_runs(Path(sys.argv[2]) if len(sys.argv) > 2 else None)
    if sys.argv[1:2] == ["retention"]:
        return retention.command(sys.argv[2:])
    if sys.argv[1:2] == ["fix"]:
        return fix_short()
    if sys.argv[1:2] == ["library"]:  # library.bat: approve or throw away the AI's invented looks/overlays/cuts
        return style_lab.library_menu()
    if sys.argv[1:2] == ["notes"]:  # rebuild the Obsidian vault's Short pages
        return logbook.vault_refresh()
    if len(sys.argv) == 1 and checkpoints.pending() and channel_profiles.ask_yes("Resume unfinished Shorts?", True):
        return resume_runs()
    name = sys.argv[2] if len(sys.argv) > 2 else channel_profiles.pick_channel()
    rules.require_rules(name)  # stops on a draft, a broken file or no file yet, before last.txt changes
    channel_profiles.use_channel(name)
    n = int(sys.argv[1]) if len(sys.argv) > 1 else channel_profiles.ask_count()
    ch, failed = channel_profiles.load_channel(), 0
    raw_choice = channel_profiles.normalize_brain(sys.argv[3]) if len(sys.argv) > 3 else None
    choice = raw_choice if raw_choice in channel_profiles.BRAINS + ["both"] else (
        channel_profiles.ask_brain(ch.get("brain", "gemini-only")) if len(sys.argv) < 2 else ch.get("brain", "gemini-only"))
    choice = channel_profiles.normalize_brain(choice)
    if choice not in channel_profiles.BRAINS + ["both"]:
        choice = "gemini-only"
    ch["brain"] = choice
    if len(sys.argv) < 2 and session.RULE_SETTINGS.get("visuals") != "blender":  # Blender draws every scene
        session.VEO_HANDOFF = channel_profiles.ask_yes("Make the AI video clips yourself (Colab H3 or Google Flow)? The batch pauses at each Short "
                              "until you've saved them", ch.get("veo", False))
        ch["veo"] = session.VEO_HANDOFF
    if len(sys.argv) < 2:  # run.bat: ask; scripted runs never pause
        session.SHORT_FORM = channel_profiles.ask_yes("Make shorter Shorts, about 25-30 seconds instead of 40-50 (a test)?", ch.get("short_form", False))
        ch["short_form"] = session.SHORT_FORM
    channel_profiles.configure_brain(choice)
    print(f"{session.BRAIN.capitalize()} writes and plans; "
          + ("solo editing and reviews." if session.SOLO else f"{session.PARTNER.capitalize()} edits and checks."))
    print("Quota exhausted: an available AI takes over without restarting the batch.")
    picture_pool.prune_cache()
    short_render.prune_work()
    topics = pools = None
    brains = ["claude", "gemini"] if choice == "both" else [session.BRAIN]
    for session.BRAIN in brains:
        if topics == []:  # Claude's half made nothing: nothing to compare
            break
        shorts = writing.write_scripts(ch, n, topics, pools)
        if choice == "both" and topics is None:  # Gemini then writes the very same topics, with the same pictures
            topics = [s.get("topic") or s["title"] for s in shorts]
            pools = [s["pool_dir"] for s in shorts]
        folders = []
        for short in shorts:
            slug = re.sub(r"[^a-z0-9]+", "-", short["title"].lower()).strip("-")[:50]
            base = OUTPUT / name / f"{date.today()}_{slug}{f'-{session.BRAIN}' if choice == 'both' else ''}"
            folder, suffix = base, 2
            while folder.exists():
                folder = base.with_name(f"{base.name}-{suffix}")
                suffix += 1
            checkpoints.begin(folder, short, choice)
            folders.append(folder)
        seo.seo_pass(shorts, ch)
        for short, folder in zip(shorts, folders):
            checkpoints.update(folder / "work", "planned", short)
        # Force invention look for testing if environment variable is set
        if os.environ.get("SHORTSMAKER_FORCE_INVENTION") == "1" and shorts:
            library = style_lab.style_library()
            if library:
                fallback = library[0]["name"]  # first look in the library
                shorts[0]["look"] = {
                    "name": "invented",
                    "title": "Test Invention",
                    "brief": "A test look for invention path",
                    "fallback": fallback
                }
        for short, folder in zip(shorts, folders):
            mode_str = " (solo)" if session.SOLO else ""
            print(f"Making: {short['title']} ({session.BRAIN.capitalize()}{mode_str})")
            try:
                short_render.render(short, ch, folder)
            except blender_render.BlenderFailed as e:
                print(f"  Blender could not draw this Short ({e}); files kept for resume")
                record_failure(folder, e)
                failed += 1
                continue
            except Exception as e:  # one bad Short shouldn't kill the whole batch
                print(f"  FAILED, skipping this one: {type(e).__name__}: {e}")
                record_failure(folder, e)
                failed += 1
                continue
            finish_short(short, ch, folder)
            print(f"  done -> {folder}")
    if choice == "both":
        print("\nComparison: each topic's two versions end in -claude and -gemini. Watch both, post the better one.")
    print(f"\nAll done{f' ({failed} unfinished; run again to resume)' if failed else ''}. Open {OUTPUT / name}")


def record_failure(folder: Path, error: Exception) -> None:
    work = folder / "work"
    path = work / "progress.json"
    if path.exists():
        try:
            job = checkpoints.read(path)
            checkpoints.update(work, job["stage"], error=f"{type(error).__name__}: {error}")
        except (ValueError, OSError, KeyError) as checkpoint_error:
            print(f"  Progress record could not be updated: {checkpoint_error}")
    print(f"  Files preserved: {folder}. Run run.bat again and choose resume.")


def finish_short(short: dict, ch: dict, folder: Path) -> None:
    topic = short.get("topic", short["title"])
    if topic not in ch["done_topics"]:
        ch["done_topics"].append(topic)
        if short.get("shape"):
            ch["recent_shapes"] = (ch.get("recent_shapes", []) + [short["shape"]])[-3:]
        if (short.get("look") or {}).get("name") not in (None, "invented") and any(sc.get("look") for sc in short["scenes"]):
            ch["recent_looks"] = (ch.get("recent_looks", []) + [short["look"]["name"]])[-2:]
    channel_profiles.save_channel(ch)
    logbook.log_short(short, folder)
    logbook.vault_page(short["title"], folder, folder.parent.name)
    checkpoints.update(folder / "work", "complete", short)


def resume_runs(folder: Path | None = None) -> None:
    folders = [folder.resolve()] if folder is not None else checkpoints.pending()
    if not folders:
        print("No unfinished Shorts found.")
    for folder in folders:
        try:
            work = folder / "work"
            job = checkpoints.read(work / "progress.json")
            if job["stage"] == "complete":
                continue
            rules.require_rules(folder.parent.name)
            channel_profiles.use_channel(folder.parent.name)
            ch = channel_profiles.load_channel()
            channel_profiles.configure_brain(job["mode"])
            session.BRAIN, session.PARTNER = job["brain"], job["partner"]
            session.SHORT_FORM, session.VEO_HANDOFF = job["short_form"], job["veo"]
            short = job["short"]
            print(f"Resuming {folder.name}: {job['stage']}")
            if job["stage"] == "scripted":
                seo.seo_pass([short], ch)
                checkpoints.update(work, "planned", short)
            state = short_render.load_state(work) if (work / "state.json").exists() else None
            if state:
                short = state["short"]
            if job["stage"] == "rendered" and (work / "render-context.json").is_file() and (folder / "short.mp4").is_file():
                context = checkpoints.context(work)
                if abs(short_render.media_tools.duration(folder / "short.mp4") - context["total"]) <= .15:
                    short_render.finish_render(short, ch, folder, **context)
                else:
                    print("  saved video is incomplete; rendering again from saved pictures and narration")
                    short_render.render(short, ch, folder, state)
            else:
                short_render.render(short, ch, folder, state)
            finish_short(short, ch, folder)
        except Exception as error:
            print(f"Could not finish {folder.name}: {error}")
            record_failure(folder, error)


def use_picture_from(work: Path, state: dict, i: int, k: int) -> None:
    """fix: scene i shows scene k's picture. A real photo/film is a picture choice; an AI painting only exists
    as work/ai<k>.jpg, so that file (and its prompt, for the edit plan's label) is copied instead."""
    choices, scenes = state["choices"], state["short"]["scenes"]
    choices[i] = {**choices[k], "person": choices[i]["person"]}
    scenes[i]["full"] = None  # it shows a picture now
    if (scenes[i].get("graphic") or {}).get("style") == "mark":  # it circled a detail of the old picture
        scenes[i]["graphic"] = None
    if not choices[k]["bg"] and (work / f"ai{k}.jpg").exists():
        shutil.copy(work / f"ai{k}.jpg", work / f"ai{i}.jpg")
        scenes[i]["ai_image"] = scenes[k]["ai_image"]
        if str(work / f"ai{k}.jpg") in state["by_gemini"]:
            state["by_gemini"].append(str(work / f"ai{i}.jpg"))
    scenes[i]["animate"] = False  # its AI motion was written for the old picture


def fix_short() -> None:
    """fix.bat: re-render a recent Short with one scene changed, keeping its pictures, voice and music
    (a few minutes instead of a new Short). Only Shorts made in the last KEEP_WORK_DAYS days still have
    the working files this needs."""
    short_render.prune_work()
    recent = sorted((w.parent for w in OUTPUT.glob("*/*/work") if (w / "state.json").exists()),
                    key=lambda p: (p / "work" / "state.json").stat().st_mtime, reverse=True)[:9]
    if not recent:
        print(f"No Short can be fixed: only ones made in the last {short_render.KEEP_WORK_DAYS} days keep their working files.")
        return
    print("Which Short?")
    for k, f in enumerate(recent, 1):
        print(f"  {k}) {f.parent.name} / {f.name}")
    folder = recent[channel_profiles.ask_number("Pick a number", len(recent), 1) - 1]
    rules.require_rules(folder.parent.name)  # a draft or broken rules file stops before any more questions
    state = short_render.load_state(folder / "work")
    short, choices = state["short"], state["choices"]
    if short.get("build"):  # every scene is a Blender drawing: there is no picture or graphic to swap yet
        print("This Short is drawn in Blender: fix.bat can't change its scenes. Make a new one with run.bat, or edit\n"
              f"it by hand with {folder.name}\\edit_in_shotcut.bat when that file is there.")
        return
    for k, sc in enumerate(short["scenes"], 1):
        print(f"  {k}) {sc['narration'][:80]}")
    i = channel_profiles.ask_number("Which scene?", len(short["scenes"])) - 1
    sc = short["scenes"][i]
    channel_profiles.use_channel(folder.parent.name)
    ch = channel_profiles.load_channel()
    channel_profiles.configure_brain(str(ch.get("brain", "gemini-only")))
    print("What should change?\n  1) No AI motion (a smooth camera move instead)\n"
          "  2) Use the picture from another scene\n  3) Remove its text graphic, map or motion graphic\n"
          "  4) Paint a new picture for it (the AI first writes a better picture prompt)\n"
          "  5) Turn it into a motion graphic (map, number, document or custom animation)\n"
          "  6) Adjust a circle/arrow target or label and preview the scene")
    old_mark = dict(sc["graphic"]) if (sc.get("graphic") or {}).get("style") == "mark" else None
    what = channel_profiles.ask_number("Pick a number", 6)
    if what == 6:
        if not old_mark:
            print("This scene has no circle or arrow. Option 3 removes other graphics.")
            return
        for key, label in (("x", "across from the left"), ("y", "down from the top")):
            while True:
                answer = input(f"Target percent {label} [{old_mark[key] * 100:g}]: ").strip()
                try:
                    value = float(answer) if answer else old_mark[key] * 100
                    if 0 <= value <= 100:
                        sc["graphic"][key] = value / 100
                        break
                except ValueError:
                    pass
                print("Enter a number between 0 and 100.")
        sc["graphic"]["text"] = input(f"Label [{old_mark['text']}]: ").strip().upper()[:24] or old_mark["text"]
    if what == 1:
        sc["animate"] = False
    elif what == 2:
        use_picture_from(folder / "work", state, i, channel_profiles.ask_number("The picture from which scene?", len(short["scenes"])) - 1)
    elif what == 3:
        sc["graphic"], sc["full"] = None, None
    elif what == 4:
        why = input("What's wrong with the picture? (Enter to skip): ").strip()
        review.paint_new(folder / "work", state, i)
        review.rewrite_paint_prompts(short, {i: why or "the owner wants a different, better picture"})
        print(f"  new prompt: {sc['ai_image']}")
    elif what == 5:
        old = sc.get("full")
        sc["full"] = None
        if not picker.rescue_graphics(short, [i], {i: "owner asked"}):
            sc["full"] = old
            print("No motion graphic fits this line; nothing changed.")
            return
    if old_mark and what in (3, 6):
        try:
            preview_path = scene_repair.preview(folder, state, i)
        except (ValueError, OSError, subprocess.SubprocessError) as error:
            print(f"Fast preview unavailable ({error}); using normal repair with cached narration where available.")
        else:
            print(f"Review this scene preview: {preview_path} (contact sheet alongside it)")
            if channel_profiles.ask_yes("Apply this preview to the finished Short?", False):
                scene_repair.apply(folder, state, preview_path)
                print(f"  repaired -> {folder / 'short.mp4'}; original backed up beside the preview")
            else:
                print("  original video kept; preview remains available")
            return
    print(f"Re-rendering {folder.name}...")
    short_render.render(short, ch, folder, state)
    print(f"  done -> {folder} (the logbook entry stays as it was)")
