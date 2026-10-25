"""Choosing each scene's picture, pictures for full-screen scenes, and rescue graphics."""

import json
from pathlib import Path

from shortsmaker import (
    channel_profiles, footage, image_sources, llm, picture_pool, plan_rules, rules, session, style_lab, writing,
)
from shortsmaker.config import DOC_KINDS, ICONS, MAX_FULL, MOVE_NAMES, STYLE_CAPS


def choose_images(short: dict, work: Path, ch: dict | None = None) -> list[dict]:
    """Build a broad multi-source pool of images and real video footage (per-scene video search on
    Internet Archive, Wikimedia Commons, Wikipedia, Openverse, Pixabay,
    NASA), show numbered contact sheets to the AI visual editor, and let it match video clips or stills
    to every scene. Picked video frames download ~14s around that moment and credit the owner on screen."""
    print("  researching images and video footage across sources...")
    ch = ch or (channel_profiles.load_channel() if session.CHANNEL.exists() else {})
    niche = ch.get("niche", "educational")
    names = [sc["person"]["name"] for sc in short["scenes"] if sc["person"]]
    scene_imgs = list(dict.fromkeys(sc["image_search"] for sc in short["scenes"] if sc.get("image_search")))
    scene_vids = list(dict.fromkeys((sc.get("video_search") or sc["image_search"])
                                    for sc in short["scenes"] if sc.get("video_search") or sc.get("image_search")))
    pool = picture_pool.load_pool(Path(short["pool_dir"])) if short.get("pool_dir") else None
    if pool is None:  # an old plan: search per scene, as before pictures-first
        cands = picture_pool.gather_pool(short.get("wiki_articles", []), names, scene_imgs, scene_vids)
    else:  # the pool the script was planned with; new finds go at the end so its numbers stay valid
        open_ = [sc for sc in short["scenes"] if not sc.get("pic") and sc.get("image_search")]
        film_srcs = {c["film"]["src"] for c in pool if c.get("film")}
        n_stills = sum(1 for c in pool if not c.get("film"))
        extra = picture_pool.gather_pool([], names, list(dict.fromkeys(sc["image_search"] for sc in open_)),
                            list(dict.fromkeys(sc.get("video_search") or sc["image_search"] for sc in open_)),
                            skip={c["url"] for c in pool} | film_srcs, limit=max(24, 64 - n_stills),
                            film_limit=max(0, 14 - len(film_srcs)))  # about the old totals, room for the open scenes
        cands, have = list(pool), {c["url"] for c in pool}
        for c in extra:
            if c["url"] not in have:
                have.add(c["url"])
                cands.append(c)
    planned_full = lambda sc: [it.get("pic") for it in sc["full"]["items"]] if (sc.get("full") or {}).get("type") == "board" else None  # noqa: E731
    if not cands:
        return [{"bg": None, "person": None} for _ in short["scenes"]]

    n_film = sum(1 for c in cands if c.get("film"))
    print(f"  {len(cands) - n_film} candidate images + {n_film} video frames; {session.BRAIN.capitalize()} is looking at them...")
    sheets = picture_pool.contact_sheets(cands, work / "sheets")
    scenes = [{"scene": i + 1, "narration": sc["narration"],
               "person_card_for": sc["person"]["name"] if sc["person"] else None,
               "shot": sc["shot"], "animate": sc["animate"],
               **({"planned_picture": sc["pic"]} if pool is not None and sc.get("pic") else {}),
               **({"planned_full_pictures": planned_full(sc)} if pool is not None and any(planned_full(sc) or []) else {}),
               **({"motion_graphic_photos_wanted": [it["find"] or it["label"] for it in sc["full"]["items"]]}
                  if (sc.get("full") or {}).get("type") == "board" else
                  {"motion_graphic_photos_wanted": [p["find"] or p["label"] for p in sc["full"]["photos"]]}
                  if (sc.get("full") or {}).get("type") == "custom" and sc["full"].get("photos") else
                  {"document_scan_wanted": sc["full"]["find"]} if (sc.get("full") or {}).get("type") == "document"
                  and sc["full"].get("find") else {})}
              for i, sc in enumerate(short["scenes"])]
    look, look_rule = short.get("look"), ""
    if look:  # the picker sees the pictures, so it picks the scenes the look suits (tilt-shift only on wide shots...)
        what = look.get("brief") or next((e["description"] for e in style_lab.style_library("look") if e["name"] == look["name"]), "")
        look_rule = (f'LOOK: this Short uses the photo look "{look.get("title") or look["name"]}" ({what}). Also give '
                     f'look_scenes = the numbers of 2-{STYLE_CAPS["look_scenes"]} scenes whose chosen STILL picture suits this '
                     "look best (never scene 1, never a REAL FILM pick, never a motion-graphic scene); [] if none suits it.\n")
    plan_rule = ("""A scene with planned_picture was written around that candidate before the script: keep it as bg unless it
clearly doesn't fit the final narration; if you pick another (or null), give swap_why in a few words. Use
planned_full_pictures as full_pictures the same way (null for a planned photo that doesn't fit).
""" if pool is not None else "")
    rules = f"""You are the visual editor for a YouTube Short in the "{niche}" niche: "{short['title']}".
For every scene choose the background candidate (video clip or image) that best matches its shot note
(subject and framing), or else what the narration is about at that moment: the right game, person,
place, object or event, from the right era. Never pick pictures of graphic violence, torture, executions,
corpses or suffering: use null instead. All REAL FILM frames have already had their top 6% and bottom 20%
cropped off to remove standard bottom subtitles; if a frame STILL has burned-in subtitles, captions, or
"subscribe" text visible inside the cropped image, DO NOT pick it (normal in-game UI/HUDs are fine).
Scene 1 is the hook that decides whether viewers swipe away: give it the single most striking,
eye-catching candidate that fits the story (REAL FILM first whenever it shows the subject), even when
another picture matches its words more literally. {session.RULES["Picture picking"]}
Candidates whose source says REAL FILM are frames from real video footage (Internet
Archive, Wikimedia Commons, Pixabay, NASA): picking one plays a clip of that real video in the scene
and automatically credits the owner on screen. Prefer REAL FILM over still pictures whenever a video
frame genuinely shows what the scene is about — you may pick REAL FILM on as many scenes as it fits,
up to every scene! A REAL FILM frame that only shows a static text slide, a modern talking head in front
of a mic/camera for a historical scene, an AI-generated cartoon slideshow when real photos/footage exist,
or an unrelated screen is not good footage: skip it.
Keep the Short visually varied: never use the exact same candidate number twice, and pick at most 2
different moments from the same source video across the Short. Avoid: a different person/game that
shares a name, near-duplicates of an image already used, maps or text pages unless the narration is
about them, and any picture whose printed caption names a different event, place or person.
For scenes with person_card_for, also pick a still portrait (never a REAL FILM frame) that clearly
shows that exact person (face visible), and that is a different picture from the scene's background.
Use null when nothing fits: an unrelated image is worse than none, and a painted illustration of the
scene is made instead.
Some scenes are full-screen motion graphics. For a scene with motion_graphic_photos_wanted (an evidence
board or custom collage of real photos), give full_pictures = one candidate per wanted photo, in order: a STILL picture (never
REAL FILM) that really shows it, never the same candidate twice in the Short, null where none does. For a
scene with document_scan_wanted, full_pictures = [the candidate that is a real scan of that document] or
[null]. Still pick a normal bg for those scenes too (used if the graphic can't be made).
For scenes with animate true where you picked a STILL picture (not REAL FILM), an AI video model will
bring your chosen picture to life: write motion = one short line describing gentle movement of what is
actually in that picture, of one kind:
ATMOSPHERE (water, waves, clouds, rain, snow, flags, fire, light, or smoke and steam rising from a visible
source; everyone stays still) or
PEOPLE moving slowly and simply (working, a crowd shifting, walking calmly). Set motion_people true
for the PEOPLE kind, false for ATMOSPHERE. Use motion null when you picked REAL FILM, or for fast action,
vehicles or machines in motion, a close-up of a face, when nothing would naturally move, or for a line
drawing, engraving, portrait or document page. Never add dust, fog, mist or smoke that isn't in the picture.
Also choose move = the camera move that suits the picture you chose: "in" (faces, details),
"out" (reveals), "left"/"right" (wide places, crowds), "up"/"down" (tall pictures, full-length
figures). Never the same move in two scenes in a row.
Also give subject_row = where the main subject sits in the background you chose (the face, if there is
one), as a row from 1 (top edge) to 10 (bottom edge); null when there's no single subject. Text callouts
are moved out of the subject's way.
{plan_rule}Scenes: {json.dumps(scenes, ensure_ascii=False)}
{look_rule}Reply with ONLY JSON: {{"picks": [{{"scene": 1, "bg": 7, "person": null, "move": "in", "motion": null, "motion_people": false, "subject_row": 3, "full_pictures": null, "swap_why": null}}], "look_scenes": []}}"""
    titles = [f"{k + 1}: {c['title']} ({c['source']})" for k, c in enumerate(cands)]
    sheet_list = "\n".join(str(s) for s in sheets)
    data = llm.ask_ai(f"""{rules}
The candidates are numbered on these contact sheets. Open and look at every sheet:
{sheet_list}
For reference, their file titles: {json.dumps(titles, ensure_ascii=False)}""",
                      fatal=False, read_dir=work / "sheets", bulk=True)
    if data is None:
        print("    visual check failed, picking by file title instead")
        data = llm.ask_ai(f"{rules}\nCandidates (number: file title): {json.dumps(titles, ensure_ascii=False)}",
                          fatal=False)
    if data is None and pool is not None:  # no picker answer: the director's plan stands
        data = {"picks": [{"scene": i + 1, "bg": sc.get("pic"), "full_pictures": planned_full(sc)}
                          for i, sc in enumerate(short["scenes"])]}
    picks = {p.get("scene"): p for p in (data or {}).get("picks", []) if isinstance(p, dict)}

    chosen, taken = [], set()
    for i in range(len(short["scenes"])):
        result = {}
        for kind in ("bg", "person"):
            num = picks.get(i + 1, {}).get(kind)
            c = cands[num - 1] if isinstance(num, int) and 1 <= num <= len(cands) else None
            result[kind] = None
            if c and c.get("film") and kind == "person":
                c = None  # person cards need a clear portrait
            if c and c["url"] not in taken:
                if c.get("film"):
                    piece = footage.film_piece(c["film"], work / f"film{i}_src.mp4")
                    img = piece[0] if piece else None
                    if piece:
                        result["film"] = {**c["film"], "path": work / f"film{i}_src.mp4", "offset": piece[1]}
                else:
                    img = image_sources.get_image(c["url"], "image download")
                if img:
                    result[kind] = (img, c["title"], c["credit"])
                    if kind == "bg":
                        result["site"] = c.get("site", "Wikimedia Commons")
                    taken.add(c["url"])
        sc = short["scenes"][i]
        if pool is not None and sc.get("pic"):
            got, why = picks.get(i + 1, {}).get("bg"), str(picks.get(i + 1, {}).get("swap_why") or "").strip()[:120]
            result["plan_note"] = ("planned picture kept" if got == sc["pic"] and result["bg"] else
                                   f"planned #{sc['pic']} swapped: " + (why or (
                                       "the picker chose another" if got != sc["pic"] else
                                       "it was already used in another scene" if cands[got - 1]["url"] in taken else
                                       "it could not be downloaded")))
        row = picks.get(i + 1, {}).get("subject_row")
        if result["bg"] and isinstance(row, int) and 1 <= row <= 10:
            result["subject_y"] = (row - 0.5) / 10  # 0..1 down the picture
        if result["bg"] and picks.get(i + 1, {}).get("move") in MOVE_NAMES:
            sc["move"] = picks[i + 1]["move"]
        if sc["animate"] and result["bg"]:  # the planner wrote motion before any picture was chosen
            sc["motion"] = str(picks.get(i + 1, {}).get("motion") or "").strip()[:200]
            sc["motion_people"] = picks.get(i + 1, {}).get("motion_people") is True
            sc["animate"] = bool(sc["motion"]) and not result.get("film")
        chosen.append(result)
    for i, pics in full_pictures(short, picks, cands, taken).items():
        chosen[i]["full_pics"] = pics
    style_lab.apply_look_scenes(short, chosen, (data or {}).get("look_scenes"))
    return chosen


def full_pictures(short: dict, picks: dict, cands: list[dict], taken: set) -> dict[int, list]:
    """Downloads the real photos the picker chose for evidence boards, custom scenes and documents.
    An item without a usable photo leaves the board (with its threads); a board left with fewer than 3 photos
    is dropped and the scene uses its normal picture. Returns scene -> [(bytes, title, credit, site)]."""
    out = {}
    for i, sc in enumerate(short["scenes"]):
        full = sc.get("full")
        if not full or full["type"] not in ("board", "document", "custom"):
            continue
        if full["type"] == "custom" and not full.get("photos"):
            continue
        nums = picks.get(i + 1, {}).get("full_pictures")
        nums = nums if isinstance(nums, list) else []
        want = len(full["items"]) if full["type"] == "board" else (len(full["photos"]) if full["type"] == "custom" else 1)
        pics = []
        for k in range(want):
            num = nums[k] if k < len(nums) else None
            c = cands[num - 1] if isinstance(num, int) and not isinstance(num, bool) and 1 <= num <= len(cands) else None
            img = image_sources.get_image(c["url"], "image download") if c and not c.get("film") and c["url"] not in taken else None
            if img:
                taken.add(c["url"])
            pics.append((img, c["title"], c["credit"], c.get("site", "Wikimedia Commons")) if img else None)
        if full["type"] == "document":
            out[i] = [p for p in pics if p]
            continue
        keep = [k for k, p in enumerate(pics) if p]
        if full["type"] == "custom":
            full["photos"] = [full["photos"][k] for k in keep]
            out[i] = [pics[k] for k in keep]
            if full.get("kind") == "collage" and not keep:
                full["kind"] = "diagram"
            continue
        if len(keep) < 3:
            print(f"    scene {i + 1}: too few real photos for the evidence board, using a normal picture")
            sc["full"] = None
            continue
        new = {old: k for k, old in enumerate(keep)}
        full["items"] = [full["items"][k] for k in keep]
        full["links"] = [[new[a], new[b]] for a, b in full["links"] if a in new and b in new]
        out[i] = [pics[k] for k in keep]
    return out


def rescue_graphics(short: dict, scenes: list[int], why: dict[int, str]) -> list[int]:
    """Scenes whose picture is missing or weak may become a full-screen motion graphic (map journey, big number,
    document, or a custom AI-coded diagram/flow/clock) when one shows their line better than a painting.
    One AI call; the same caps as planned ones (MAX_FULL, never scene 1, never two in a row).
    Returns the scenes that got one."""
    scs = short["scenes"]
    max_full = rules.max_full()
    min_words = 6 if max_full > MAX_FULL else channel_profiles.FULL_MIN_WORDS
    asked = [i for i in scenes if 0 < i < len(scs) and not scs[i].get("full")
             and len(scs[i]["narration"].split()) >= min_words]  # a shorter scene can't play one: it gets a painting
    if not asked or sum(1 for sc in scs if sc.get("full")) >= max_full:
        return []
    texts = short.get("research") or {t: writing.article_text(t)[:15000] for t in short.get("wiki_articles", [])[:3]}
    script = [{"scene": i + 1, "narration": sc["narration"],
               **({"needs_help": why.get(i, "the picture is weak")} if i in asked else {})} for i, sc in enumerate(scs)]
    print(f"  asking {session.BRAIN.capitalize()} whether a motion graphic fits {len(asked)} scene(s) without a good picture...")
    data = llm.ask_ai(f"""You are the director of a YouTube Short: "{short['title']}". The scenes marked needs_help
have no good picture. For each of them, decide whether a FULL-SCREEN motion graphic would show its line well
(else null: the scene gets a painting instead). Real facts only, from the articles below. "word" = a word or
name spoken in that scene's narration when that element should appear. Formats:
{{"type": "journey", "stops": [{{"name": "Uitenhage", "lat": -33.76, "lon": 25.4, "word": "Uitenhage"}}], "note": "1881"}}
 (1-4 real places in travel order);
{{"type": "number", "value": 30000, "label": "mourners", "icon": "person", "thing": "mourner", "each": 1000, "word": "thirty"}}
 (thing = what one figure is, a singular noun; icon = the closest of {list(ICONS)}; optional "compare": {{"a_label": "1858", "a_value": 100, "b_label": "today", "b_value": 3}});
{{"type": "document", "kind": "telegram", "key_line": "...", "date": "1890", "word": "..."}}
 (kind one of {list(DOC_KINDS)}; key_line at most 14 words, documented or a plain summary; "paper" only for a
 real newspaper that covered it);
{{"type": "custom", "kind": "diagram", "title": "...", "brief": "...", "words": ["...", "...", "..."]}}
 (a bespoke animated scene coded from scratch for this moment when the line explains a mechanism, physical
 layout/cross-section, loophole/cause-and-effect chain, or schedule/countdown; kind one of
 ["diagram", "flow", "clock"]; "words" = 2-4 spoken words from the scene that trigger each animation beat).
Script: {json.dumps(script, ensure_ascii=False)}
Wikipedia articles: {json.dumps(texts, ensure_ascii=False)}
Reply with ONLY JSON: {{"scenes": [{{"scene": 3, "full": null}}]}}""", fatal=False)
    got = []
    for r in sorted((r for r in (data or {}).get("scenes") or [] if isinstance(r, dict) and isinstance(r.get("scene"), int)),
                    key=lambda r: r["scene"]):
        i = r["scene"] - 1
        f = r.get("full")
        if i not in asked or not isinstance(f, dict) or f.get("type") == "board":
            continue
        if f.get("type") == "document" and any((sc.get("full") or {}).get("type") == "document" for sc in scs):
            continue  # at most one document scene per Short so a rescued slot isn't wasted repeating the same contract
        f = plan_rules.clean_full(f, plan_rules.words_of(scs[i]["narration"]))
        near = any(0 <= k < len(scs) and scs[k].get("full") for k in (i - 1, i + 1))
        if f and not near and sum(1 for sc in scs if sc.get("full")) < max_full:
            scs[i].update(full=f, graphic=None, person=None, animate=False, full_rescued=why.get(i, "the picture was weak"))
            got.append(i)
    return got
