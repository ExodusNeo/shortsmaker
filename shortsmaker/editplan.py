"""edit_plan.txt (the timestamped edit list) and per-scene cue timing."""

from pathlib import Path

from shortsmaker import frame_render, media_tools, plan_rules, style_lab
from shortsmaker.config import FPS, GRAPHIC_STYLES, MOVE_NAMES, MUSIC, PALETTES, REMOTION_ONLY, XFADE


def look_text(short: dict) -> str:
    """Plain-English name of the Short's photo look for edit_plan.txt."""
    look = short.get("look") or {}
    if look.get("name") == "invented":
        return f'invented "{look["title"]}" ({look["brief"][:120]}; if it failed: {look["fallback"]})'
    return next((f"{e['name']} ({e['description']})" for e in style_lab.style_library("look") if e["name"] == look.get("name")),
                str(look.get("name")))


def cut_text(short: dict, name: str, renderer: str) -> str:
    """Plain-English scene change for edit_plan.txt."""
    if short.get("build") and not renderer.startswith("Remotion"):
        return "hard cut (the Blender camera runs on)"
    if name == "fade" or (name != "flash" and not renderer.startswith("Remotion")):
        return f"{XFADE}s crossfade" + ("" if name == "fade" else f" (planned: {name}; the built-in renderer can't draw that cut)")
    if name == "flash":
        return "camera-flash hard cut"
    if name == "invented":
        inv = short.get("invented_transition") or {}
        return f'invented "{inv.get("title")}" ({str(inv.get("brief"))[:100]}; if it failed: {inv.get("fallback")})'
    return next((e["description"] for e in style_lab.style_library("transition") if e["name"] == name), name)


def picture_line(short: dict) -> str | None:
    """edit_plan.txt: what the pictures-first check found (None for a plan made before it)."""
    if not short.get("picture_check"):
        return None
    dropped = short.get("dropped_topics") or []
    return f"Pictures found before writing: {short['picture_check']}" + (f" (topics dropped: {'; '.join(dropped)})" if dropped else "")


def cold_read_line(read: dict) -> str:
    """edit_plan.txt: how the cold reader (writing.cold_read) heard the final script."""
    stale = [str(k + 1) for k, v in enumerate(read.get("new") or []) if not v]
    return (f"Cold read (a stranger's view of the script): question \"{read['question']}\" | answered in scene "
            f"{read.get('answer') or 'none'} | first swipe: "
            + (f"scene {read['swipe']} ({read.get('swipe_why') or 'no reason'})" if read.get("swipe") else "none")
            + (f" | nothing new in scene(s) {', '.join(stale)}" if stale else "")
            + (f" | reviewed by {read['reviewer'].capitalize()}" if read.get("reviewer") else ""))


def edit_plan(short: dict, bounds: list[float], sources: list[str], cues: list[dict],
              events: list[dict], music: Path | None, path: Path, renderer: str,
              clips: dict[int, Path]) -> None:
    """Timestamped edit decision list of exactly what was rendered, plus the sound-design cue sheet."""
    total = bounds[-1]
    lines = [f"EDIT PLAN: {short['title']}",
             f"Length {media_tools.clock(total)} | 1080x1920 vertical | {FPS} fps | captions: up to 3 words (about 16 letters) per line, spoken word "
             "in yellow, emphasis word glows orange to the end of its line",
             f"Renderer: {renderer}",
             *([picture_line(short)] if picture_line(short) else []),
             f"Music: {music.stem if music else 'none'}{f' ({music.parent.name} mood)' if music and music.parent != MUSIC else ''} (ducked under the voice, fades out over the last 2s)",
             f"Colours: {short['palette']} palette (accent {PALETTES[short['palette']]['accent']}, "
             f"emphasis {PALETTES[short['palette']]['emphasis']}, map {PALETTES[short['palette']]['panel']})",
             "Photo look: " + (f"{look_text(short)} on scenes "
                               + ", ".join(str(k + 1) for k, sc in enumerate(short["scenes"]) if sc.get("look"))
                               if any(sc.get("look") for sc in short["scenes"]) else "none (plain pictures)"),
             f"Opening: hook title \"{short['hook_text']}\" 0:00.0-0:01.8"
             + (f" | {short['opening_note']}" if short.get("opening_note") else "")
             + (f" | hook lines considered: {' / '.join(short['hook_options'])}" if short["hook_options"] else ""),
             "Script editor: " + ("\n  ".join([""] + short["editor_notes"]) if short.get("editor_notes") else "none"),
             *([cold_read_line(short["story_read"])] if short.get("story_read") else []),
             *([f"Topic pitch: {short['pitch']}"] if short.get("pitch") else []),
             *([f"Twist check (topic against Wikipedia, before writing): {short['twist_check']}"]
               if short.get("twist_check") else []),
             "Fact check (against the Wikipedia articles): "
             + ("\n  ".join([""] + short["fact_check"]) if short.get("fact_check") else "every line held up"),
             *([f"Fixed automatically after reviewing the finished video:\n  " + "\n  ".join(short["auto_fixed"])]
               if short.get("auto_fixed") else []),
             ""]
    for i, sc in enumerate(short["scenes"]):
        start, end = bounds[i], bounds[i + 1]
        lines.append(f"[{media_tools.clock(start)} - {media_tools.clock(end)}]  SCENE {i + 1}" + ("  (hook)" if i == 0 else ""))
        lines.append(f"  VO:      \"{sc['narration']}\"")
        if sc["shot"]:
            lines.append(f"  SHOT:    {sc['shot']}")
        lines.append(f"  MOTION GRAPHIC: {sources[i]}" if sc.get("full") else f"  IMAGE:   {sources[i]}")
        if sc.get("credit_tag"):
            lines.append(f"  CREDIT:  on-screen tag (bottom-left) \"{sc['credit_tag']}\"")
        if sc.get("full"):
            camera = "slow drift and push-in on old paper; each element lands on its spoken word"
        elif i in clips and clips[i].name.startswith("blender"):
            camera = "DRAWN IN BLENDER (the camera move of this beat, continuing from the scene before)"
        elif i in clips and clips[i].name.startswith("film"):
            camera = "REAL VIDEO FOOTAGE (one shot; a short shot plays slowed, credited on screen when required)"
        elif i in clips and clips[i].name.endswith("_veo.mp4"):
            camera = f"AI MOTION CLIP made by the owner in Google Flow (Veo): \"{sc['motion']}\""
        elif i in clips and clips[i].name.startswith("clip"):
            kind = ("people move gently, softened with grain to hide AI ghosting" if sc["motion_people"]
                    else "atmosphere only, people stay still")
            camera = f"AI MOTION CLIP made on this PC (LTX-Video, {kind}): \"{sc['motion']}\""
        else:
            camera = MOVE_NAMES[sc["move"]]
        lines.append(f"  CAMERA:  {camera}")
        g = sc["graphic"]
        if g:
            style = GRAPHIC_STYLES[g["style"]]
            if renderer.startswith("Remotion") and "lat" in g:
                style = f"animated map flying to {g['lat']:.2f}, {g['lon']:.2f} + pin drop, label"
            elif renderer.startswith("Remotion") and g["style"] == "date" and g["text"].isdigit():
                style = "date stamp (year counts up)"
            elif not renderer.startswith("Remotion") and g["style"] in REMOTION_ONLY:
                style = f"fact box (built-in renderer stand-in for a {GRAPHIC_STYLES[g['style']]})"
            elif g["style"] == "stat":
                style = f"dot grid, {g['value']:.0f} of {g['of']} light up," if "of" in g else f"counter ticks up to {g['value']:,.10g},"
            elif g["style"] == "timeline":
                style = f"timeline {g['start']} -> {g['end']}, gap label"
            elif g["style"] == "mark":
                style = f"photo card, {g['shape']} drawn at {g['x']:.0%} across / {g['y']:.0%} down, then push-in; label"
            if "from" in g and renderer.startswith("Remotion"):
                style = style.replace("+ pin drop", f"+ route line from {g['from']['text']} + pin drop")
            on_word = f" on \"{g['trigger']}\"" if "trigger" in g else ""
            is_map = g["style"] == "place" and g.get("lat") is not None and renderer.startswith("Remotion")
            low = " (lowered: the subject is at the top)" if g.get("low") and not is_map else ""
            lines.append(f"  GRAPHIC: {style} \"{g['text']}\" {media_tools.clock(cues[i]['graphic'])}-{media_tools.clock(end - 0.25)}{on_word}{low}")
        cue = cues[i]
        if cue.get("card"):
            lines.append(f"  PERSON:  photo card \"{sc['person']['name']}\" pops in {media_tools.clock(cue['on'])}-"
                         f"{media_tools.clock(cue['off'])} (background dims) | {cue['card_source']}")
        elif cue.get("card_note"):
            lines.append(f"  PERSON:  skipped ({cue['card_note']})")
        if cue.get("cta") is not None:
            lines.append(f"  CTA:     on-screen SUBSCRIBE button + \"{short['cta_line']}\" {media_tools.clock(cue['cta'])}-{media_tools.clock(end - 0.25)} (no voice)")
        if cue.get("emphasis") is not None:
            lines.append(f"  EMPHASIS: \"{sc['emphasis']}\" glows at {media_tools.clock(cue['emphasis'])}")
        if i:
            lines.append(f"  CUT IN:  {cut_text(short, sc['transition'], renderer)} at {media_tools.clock(start)}")
        if sc.get("look"):
            lines.append(f"  LOOK:    {look_text(short)}")
        sounds = [e for e in events if start <= e["t"] + (0.35 if e["sound"].startswith(("whoosh", "flash")) else 0) < end
                  and e["sound"] != "riser"]
        if sounds:
            lines.append("  SOUND:   " + "; ".join(f"{e['what']} @ {media_tools.clock(e['t'])}" for e in sounds))
        lines.append("")
    lines.append("SOUND DESIGN CUE SHEET (time | sound file | volume | why)")
    lines += [f"  {media_tools.clock(e['t'])}  {e['sound']:<9} {e['gain']:.2f}  {e['what']}" for e in events]
    path.write_text("\n".join(lines), encoding="utf-8")


# Map card (MapCard.tsx) at full speed: fly-in, pin and place name take MAP_FLY s; the name then stays readable
# MAP_HOLD s; the card starts leaving MAP_EXIT s before the scene ends (0.25 + its 0.22 s exit).
MAP_FLY, MAP_HOLD, MAP_EXIT = 1.8, 1.2, 0.47


# Seconds an overlay animates after it pops in (Cards.tsx, Extras.tsx, Graphics.tsx); it starts early enough to
# finish and hold before leaving (the Ghost Army "15 MILES" counter left at 13)
GRAPHIC_BUILD = {
    "stat": 1.25, "timeline": 1.35, "compare": 1.55, "date": 0.7,
    "kinetic": 0.6, "stamp": 0.35, "headline": 0.45, "question": 0.4, "mark": 0.4,
}


def scene_cues(sc: dict, words: list[tuple[float, float, str]], start: float, end: float,
               i: int, found: tuple[bytes, str] | None) -> dict:
    """Timed extras for one scene: a person card (photo `found`) when their name is spoken,
    and when the emphasis word is spoken (caption glow), and when the graphic pops up."""
    cue = {"full": plan_rules.full_cues(sc["full"], words, start, end)} if sc.get("full") else {}
    if sc.get("sound") and plan_rules.spoken_at(words, sc["sound"]["word"]) is not None:
        cue["sound_at"] = start + plan_rules.spoken_at(words, sc["sound"]["word"])
    g = sc["graphic"]
    if g:
        build = 0.6 + 0.035 * len(g["text"]) if g.get("style") == "quote" else GRAPHIC_BUILD.get(g.get("style"), 0.3)
        if "lat" in g:
            # Map fly-ins illustrate the whole setting; start early so the camera travels during speech
            # and drops the pin as the place is spoken about
            cue["graphic"] = max(start + 0.2, min(start + 0.25, end - MAP_EXIT - 0.6))
            cue["map_pace"] = round(min(1.0, max(0.4, (end - MAP_EXIT - MAP_HOLD - cue["graphic"]) / MAP_FLY)), 2)
        else:
            t = plan_rules.spoken_at(words, g["trigger"]) if "trigger" in g else None
            is_card = g.get("style") in ("kinetic", "stamp", "headline", "quote", "question",
                                         "stat", "timeline", "compare", "mark", "date")
            need_time = max(1.8 if is_card else 1.1, build + (1.0 if is_card else 0.7))
            latest = end - 0.25 - need_time
            if t is not None:
                # Start on trigger word, or shift earlier if late in the scene so the graphic has readable hold time
                cue["graphic"] = max(start + 0.2, min(start + t - 0.1, latest))
            else:
                cue["graphic"] = max(start + 0.2, min(start + 0.3, latest))
    if sc["emphasis"]:
        t = plan_rules.spoken_at(words, sc["emphasis"])
        if t is not None:
            cue["emphasis"] = start + t
    pr = sc["person"]
    if pr:
        t = plan_rules.spoken_at(words, pr["trigger"])
        if t is None or not found:
            cue["card_note"] = f"no photo found for {pr['name']}" if t is not None else "name not heard in voice"
            return cue
        # Start when the person's name is spoken, or earlier in the sentence if the name comes late,
        # so the card has readable hold time without requiring awkward silence padding at the end.
        need_card = 1.8
        latest_on = end - 0.25 - need_card
        on = max(start + 0.2, min(start + t - 0.1, latest_on))
        if i == 0:
            on = max(on, 1.9)  # don't cover the hook title
        off = min(on + 2.5, end - 0.25)
        if off - on < 1.4:
            on = max(start + 0.15, off - 1.4)
            if i == 0:
                on = max(on, 1.9)
        if off - on >= 1.2:
            cue.update(card=frame_render.person_card(found[0], pr["name"]), photo=found[0], on=on, off=off,
                       card_source=f"Wikimedia Commons, {found[2] or 'public domain'}: {found[1]}")
        else:
            cue["card_note"] = "scene too short for a person card"
    return cue
