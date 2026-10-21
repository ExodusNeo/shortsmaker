"""Command-line entry: making a batch (`main`), fix.bat's one-scene re-render, `library`, `notes`."""

import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path

from shortsmaker import (
    channel_profiles, llm, logbook, picker, picture_pool, review, seo, session, short_render, style_lab, writing,
)
from shortsmaker.config import OUTPUT


def main() -> None:
    # make_shorts.py [count] [channel] [claude|gemini]: anything missing is asked for (run.bat passes nothing);
    # with a count given, the planner defaults to the profile's last choice
    # make_shorts.py fix: fix.bat, re-render one scene of a recent Short
    if sys.argv[1:2] == ["fix"]:
        return fix_short()
    if sys.argv[1:2] == ["library"]:  # library.bat: approve or throw away the AI's invented looks/overlays/cuts
        return style_lab.library_menu()
    if sys.argv[1:2] == ["notes"]:  # rebuild the Obsidian vault's Short pages
        return logbook.vault_refresh()
    name = sys.argv[2] if len(sys.argv) > 2 else channel_profiles.pick_channel()
    channel_profiles.use_channel(name)
    n = int(sys.argv[1]) if len(sys.argv) > 1 else channel_profiles.ask_count()
    ch, failed = channel_profiles.load_channel(), 0
    choice = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] in channel_profiles.BRAINS else (
        channel_profiles.ask_brain(ch.get("brain", "claude")) if len(sys.argv) < 2 else ch.get("brain", "claude"))
    ch["brain"] = choice
    if len(sys.argv) < 2:  # run.bat: ask; scripted runs never pause
        session.VEO_HANDOFF = channel_profiles.ask_yes("Make the AI video clips yourself in Google Flow (Veo)? The batch pauses at each Short "
                              "until you've saved them", ch.get("veo", False))
        ch["veo"] = session.VEO_HANDOFF
        session.SHORT_FORM = channel_profiles.ask_yes("Make shorter Shorts, about 25-30 seconds instead of 40-50 (a test)?", ch.get("short_form", False))
        ch["short_form"] = session.SHORT_FORM
    if choice != "claude":
        print(f"Gemini: {llm.gemini_model()}, high effort; Claude steps in if Gemini fails")
    picture_pool.prune_cache()
    short_render.prune_work()
    topics = pools = None
    for session.BRAIN in (["claude", "gemini"] if choice == "both" else [choice]):
        if topics == []:  # Claude's half made nothing: nothing to compare
            break
        shorts = writing.write_scripts(ch, n, topics, pools)
        if choice == "both" and topics is None:  # Gemini then writes the very same topics, with the same pictures
            topics = [s.get("topic") or s["title"] for s in shorts]
            pools = [s["pool_dir"] for s in shorts]
        seo.seo_pass(shorts, ch)
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
        for short in shorts:
            slug = re.sub(r"[^a-z0-9]+", "-", short["title"].lower()).strip("-")[:50]
            folder = OUTPUT / name / f"{date.today()}_{slug}{f'-{session.BRAIN}' if choice == 'both' else ''}"
            print(f"Making: {short['title']} ({session.BRAIN.capitalize()})")
            try:
                short_render.render(short, ch, folder)
            except Exception as e:  # one bad Short shouldn't kill the whole batch
                print(f"  FAILED, skipping this one: {type(e).__name__}: {e}")
                shutil.rmtree(folder, ignore_errors=True)
                failed += 1
                continue
            if short.get("topic", short["title"]) not in ch["done_topics"]:
                ch["done_topics"].append(short.get("topic", short["title"]))
            if short["shape"]:
                ch["recent_shapes"] = (ch.get("recent_shapes", []) + [short["shape"]])[-3:]
            if (short.get("look") or {}).get("name") not in (None, "invented") and any(sc.get("look") for sc in short["scenes"]):
                ch["recent_looks"] = (ch.get("recent_looks", []) + [short["look"]["name"]])[-2:]  # the next Shorts pick another
            channel_profiles.save_channel(ch)  # save after each video so a crash keeps progress
            logbook.log_short(short, folder)
            logbook.vault_page(short["title"], folder, name)
            print(f"  done -> {folder}")
    if choice == "both":
        print("\nComparison: each topic's two versions end in -claude and -gemini. Watch both, post the better one.")
    print(f"\nAll done{f' ({failed} failed, run again to replace them)' if failed else ''}. Open {OUTPUT / name}")


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
    state = short_render.load_state(folder / "work")
    short, choices = state["short"], state["choices"]
    for k, sc in enumerate(short["scenes"], 1):
        print(f"  {k}) {sc['narration'][:80]}")
    i = channel_profiles.ask_number("Which scene?", len(short["scenes"])) - 1
    sc = short["scenes"][i]
    channel_profiles.use_channel(folder.parent.name)
    ch = channel_profiles.load_channel()
    session.BRAIN = ch.get("brain") if ch.get("brain") in ("claude", "gemini") else "claude"
    print("What should change?\n  1) No AI motion (a smooth camera move instead)\n"
          "  2) Use the picture from another scene\n  3) Remove its text graphic, map or motion graphic\n"
          "  4) Paint a new picture for it (the AI first writes a better picture prompt)\n"
          "  5) Turn it into a motion graphic (map, number, document or custom animation)")
    what = channel_profiles.ask_number("Pick a number", 5)
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
    else:
        old = sc.get("full")
        sc["full"] = None
        if not picker.rescue_graphics(short, [i], {i: "owner asked"}):
            sc["full"] = old
            print("No motion graphic fits this line; nothing changed.")
            return
    print(f"Re-rendering {folder.name}...")
    short_render.render(short, ch, folder, state)
    print(f"  done -> {folder} (the logbook entry stays as it was)")
