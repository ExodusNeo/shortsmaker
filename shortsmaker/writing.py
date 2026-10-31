"""Topics -> Wikipedia research -> writer -> editor -> director -> fact check."""

import json
import re
import shutil
import urllib.parse
from pathlib import Path

from shortsmaker import (
    audio_mix, blender_plan, channel_profiles, image_sources, llm, logbook, picture_pool, plan_rules, rules,
    session, style_lab, topic_ideas,
)
from shortsmaker.config import (
    CUSTOM_KINDS, DOC_KINDS, FULL_TYPES, ICONS, MAX_FULL_PLANNED, MOODS, MOVES, MOVE_NAMES, PALETTES, SHAPES,
)


# The voice reads each run of scenes that makes whole sentences in one take (gpu.sentence_groups), so a scene may
# end mid-sentence; before this, 4-10 word scenes forced choppy fragments ("He called them enemy tricks.").
SCENE_CUTS = """Cut where the picture would change, even in the middle of a
  sentence (the narrator reads each sentence in one take across the cuts): at a natural pause, after a comma or
  before "but", "so", "and" or "who", never between "the" and its noun."""


def length_plan() -> tuple[int, int, int, int, str]:
    """(min words, max words, min scenes, max scenes, seconds) for this batch's scripts."""
    return (60, 72, 8, 10, "25-30") if session.SHORT_FORM else (95, 125, 11, 16, "40-50")


def max_seconds() -> float:
    """Past this, review.quality_check says the Short ran long (the planned seconds of length_plan, plus slack)."""
    return 36 if session.SHORT_FORM else 62


def write_scripts(ch: dict, n: int, topics: list[str] | None = None, pools: list[str] | None = None) -> list[dict]:
    """Plan n Shorts on new topics, or on exactly `topics` (comparison runs: the other AI's topics), as a small
    team: the planner picks topics, Wikipedia is read for each, the planner writes the narration, the OTHER AI
    edits it (edit_scripts), the planner plans the edit on the final words (direct_scripts), then the fact check.
    Before any writing, each topic's real pictures are gathered and listed (prepare_topic); a topic with too few
    is replaced by a backup. `pools` (Both mode): the pool folders of the same topics, by position."""
    # our own research (owner, 2026-10-28): proven channels' recent Shorts are only stories to stay away from
    taken = [t["title"] for t in channel_profiles.trend_research(ch)]
    ideas = topic_ideas.pick_ideas(ch, taken)
    idea_text = ""
    if ideas:
        idea_text += f"""
STORY IDEAS FROM OUR OWN RESEARCH (Wikipedia's list of unusual articles; each is an article title and why it is odd):
{chr(10).join(f"- {i['title']}: {i['why']}" for i in ideas)}
Pick from these where one fits this channel, or from your own knowledge of true, little-known stories.
"""
    if taken:
        idea_text += f"""
TAKEN: bigger channels in this niche posted these Shorts recently. Never pick the same story, person or event
(a story they just told is one we lose):
{chr(10).join(f"- {t}" for t in taken)}
"""
    trend_text = ""
    results = logbook.logbook_results()
    if results:
        trend_text += f"""
HOW OUR OWN POSTED SHORTS DID (the owner's numbers from YouTube Studio, oldest first):
{results}
Learn from these before choosing topics and writing. "Stayed to watch" shows whether the first second
(topic, hook line, opening picture) stopped the scroll; "Average % viewed" shows whether the story held
to the end (over 100% means rewatches). Do more of what the best ones share (kinds of topic, hook
patterns, story shapes) and less of what the weakest share; read the owner's notes too. With only a
few Shorts, treat this as hints, not rules. Judge only entries with enough views (the ones marked "Too few
views to judge" say little). {session.RULES["Lessons from our numbers"]}
"""
    if topics:
        what = f"Use exactly these {len(topics)} topics, in this order: {topics}"
    else:
        what = (f"Pick {n + picture_pool.TOPIC_BACKUPS} NEW topics, none of these already-used ones: {ch['done_topics'][-200:]}\n"
                f"The last {picture_pool.TOPIC_BACKUPS} are backups, used only if an earlier topic has too few real pictures or footage.")
        if ch.get("myths"):  # stories the fact check caught: worth telling as the real story behind the myth
            what += ("\nMyths our fact check caught earlier, each good for a \"myth vs truth\" Short that tells "
                     f"what really happened (skip any already covered above): {ch['myths'][-20:]}")
    about = f"Niche: {ch['niche']}. Audience: {ch.get('audience', '')}. Tone: {ch.get('tone', '')}."
    print(f"Choosing topics with {session.BRAIN.capitalize()}...")
    data = llm.ask_ai(f"""You choose stories for a faceless YouTube Shorts channel.
{about}
{idea_text}{trend_text}
{what}
{session.RULES["Topic picking"]}
For each:
- topic: 1-2 sentences: the story and the twist that makes it worth telling, told through its main character.
- character: the main character's name (e.g. "Joseph Bazalgette", "Jack the baboon").
- subject: the main person, game, product, place, event or thing the story is about (e.g. "Super Mario 64", "Joshua Norton").
- wiki_articles: 2-4 exact English Wikipedia article titles for the story's subject, key people,
  places, games, inventions or events (e.g. ["Super Mario 64", "Shigeru Miyamoto"]); the writer gets
  their text as research.
- search_terms: 3 short phrases people really type into YouTube search that this Short answers, in
  everyday words about its angle, not only the name (e.g. "titanic survivor", "worst warship ever").
- visual_terms: 4-6 short search phrases for the real people, places, objects and events of this story a
  camera could show, as photo archives would title them (e.g. "Ghost Army inflatable tank", "Rhine crossing 1945").
- people: the key people's full names (e.g. ["Ellsworth Kelly"]), [] if none. Their portraits are searched.
- fact8: its single most shocking fact in 8 words or fewer, as a stranger would get it instantly.
- question: what a viewer must stay to the very end to find out.
- payoff: the concrete ending that answers it (a number, a verdict, a twist, a legend proved wrong).
- fame: 1 = little-known, 2 = known to history or niche fans, 3 = told everywhere (big channels, documentaries,
  school). Pick 1 or 2: a story told everywhere is skipped.
Pictures and footage are gathered from these before any script is written: prefer stories with real photos or film.
Reply with ONLY JSON: {{"shorts": [{{"topic": "...", "character": "...", "subject": "...", "wiki_articles": ["..."],
"search_terms": ["..."], "visual_terms": ["..."], "people": ["..."], "fact8": "...", "question": "...", "payoff": "...",
"fame": 1}}]}}""")
    shorts = []
    wanted = len(topics) if topics else n
    for k, p in enumerate(data.get("shorts", [])[:len(topics) if topics else n + picture_pool.TOPIC_BACKUPS]):
        if not (isinstance(p, dict) and str(p.get("topic") or "").strip() and str(p.get("subject") or "").strip()):
            continue  # LLM output is untrusted
        subject, arts, terms = str(p["subject"]).strip(), p.get("wiki_articles"), p.get("search_terms")
        arts = [a.strip() for a in arts if isinstance(a, str) and a.strip()] if isinstance(arts, list) else []
        shorts.append({"topic": str(p["topic"]).strip(), "subject": subject, "_pos": k,
                       "character": str(p.get("character") or "").strip()[:80],
                       "wiki_articles": list(dict.fromkeys([subject] + arts))[:5],
                       "search_terms": [t.strip() for t in terms if isinstance(t, str) and t.strip()][:3]
                       if isinstance(terms, list) else [],
                       **{k: [t.strip() for t in p[k] if isinstance(t, str) and t.strip()][:cap]
                          if isinstance(p.get(k), list) else [] for k, cap in (("visual_terms", 6), ("people", 4))}})
        if (who := shorts[-1]["character"]) and who not in shorts[-1]["people"]:  # their portrait is searched first
            shorts[-1]["people"] = [who] + shorts[-1]["people"][:3]
        pitch = {f: str(p.get(f) or "").strip()[:160] for f in ("fact8", "question", "payoff")}
        fame = p.get("fame") if type(p.get("fame")) is int and 1 <= p["fame"] <= 3 else None
        shorts[-1]["fame"] = fame  # a pitch the picker left out keeps its topic: a thin reply mustn't lose a run
        shorts[-1]["pitch"] = " | ".join([f"{f}: {v}" for f, v in pitch.items() if v]
                                         + ([f"fame {fame}/3"] if fame else [])) or None
    assert shorts, f"no usable topics: {data}"
    kept, dropped = [], []
    for i, s in enumerate(shorts):
        if len(kept) == wanted:
            break
        print(f'Topic {i + 1}/{len(shorts)}: "{s["subject"]}": reading Wikipedia, finding real pictures and footage...')
        k = s.pop("_pos")
        if s.pop("fame") == 3 and not topics:  # Emu War: ~1K on ours and ~8K on Voggle, a channel that gets millions
            dropped.append(f'"{s["topic"]}": told everywhere already (fame 3/3)')
            print(f"  Skipped {dropped[-1]}")
            continue
        if hit := next((t for name in (s["subject"], s.get("character", "")) if (t := topic_ideas.clash(name, taken))), None):
            dropped.append(f'"{s["topic"]}": a bigger channel posted it recently ("{hit}")')
            print(f"  Skipped {dropped[-1]}")
            continue
        # by the main character's name (a subject like "Royal Navy" would match many of our stories)
        if not topics and (hit := topic_ideas.clash(s.get("character") or s["subject"], ch.get("done_topics") or [])):
            dropped.append(f'"{s["topic"]}": we already made it ("{hit[:80]}")')  # the prompt alone let repeats through
            print(f"  Skipped {dropped[-1]}")
            continue
        if picture_pool.prepare_topic(s, Path(pools[k]) if pools and k < len(pools) else None):
            kept.append(s)
        else:
            dropped.append(f'"{s["topic"]}": only {s["picture_check"]} real pictures/clips')
            if s.get("pool_dir"):  # not kept for 30 days: the topic may come back once better pictures exist
                shutil.rmtree(s["pool_dir"], ignore_errors=True)
            print(f"  Skipped {dropped[-1]}")
    for s in kept:
        s["dropped_topics"] = dropped
    shorts = kept
    if not shorts:
        print("No topic had enough real pictures this time; nothing was made.")
        return []
    check_twists(shorts)
    research = [{"index": i, "topic": s["topic"], "subject": s["subject"], "main_character": s.get("character") or s["subject"],
                 "wikipedia": {t: x[:8000] for t, x in s["_texts"].items() if x} or "none found: use only facts you are sure of",
                 "pictures": picture_pool.pictures_of(s) or "none listed"}
                for i, s in enumerate(shorts)]
    lo, hi, s_lo, s_hi, secs = length_plan()
    print(f"Writing {len(shorts)} script(s) with {session.BRAIN.capitalize()}...")
    data = llm.ask_ai(f"""You write YouTube Shorts narration for a faceless channel.
{about}
{trend_text}
Write one Short on each topic below, using the Wikipedia research given with it.
Rules for each Short:
- {lo}-{hi} spoken words (about {secs} seconds), simple words a 5th grader understands.
{session.RULES["Story rules"]}
- Never repeat yourself: every line adds something new; no phrase of 3+ words may appear twice.
{session.RULES["Writing for the picture"]}
- Every fact must be true: take facts from the research; anything else only if you are certain it
  is well documented. No made-up statistics or quotes.
- shape: the story's shape, one of {SHAPES}. Not one of the channel's last ones
  ({ch.get('recent_shapes', [])}), and a different one for each Short in this batch.
- scenes: the narration split into {s_lo}-{s_hi} short scenes of 4-{channel_profiles.SCENE_WORDS} words (about 3 seconds: each
  scene gets its own picture, and a new picture every ~3 seconds keeps viewers watching). {SCENE_CUTS}
  Only a scene that needs time on one picture (a trip between places, a big number, a document, several
  things that connect) may run up to {channel_profiles.LONG_SCENE_WORDS} words.
- title: draft (refined later with real search data): under 60 characters, main keyword early, no "#shorts".
- thumbnail_text: 2-4 punchy words.
- hook_text: 2-4 words shown big over the first second, for viewers watching with the sound off:
  sharpens the SAME question the first sentence opens, in other words (e.g. "NOBODY FIRED HIM"),
  never a separate idea, not a repeat of the title or thumbnail_text.
Topics and research: {json.dumps(research, ensure_ascii=False)}
Reply with ONLY JSON: {{"shorts": [{{"index": 0, "shape": "...", "title": "...", "hook_options": ["...", "...", "..."],
"hook_text": "...", "thumbnail_text": "...", "scenes": ["narration of scene 1", "narration of scene 2", "..."]}}]}}""")
    for k, r in enumerate(data.get("shorts", [])):
        i = r.get("index") if isinstance(r, dict) and isinstance(r.get("index"), int) else k
        if isinstance(r, dict) and 0 <= i < len(shorts) and str(r.get("title") or "").strip():
            shorts[i].update({f: r[f] for f in ("shape", "hook_options", "hook_text", "thumbnail_text") if r.get(f)},
                             title=str(r["title"]).strip(), lines=narration_lines(r.get("scenes")))
    shorts = [s for s in shorts if s.get("lines")]
    assert shorts, f"no usable scripts: {data}"
    edit_scripts(shorts, ch)
    direct_scripts(shorts, ch)
    kept = []
    for s in shorts:  # LLM output is untrusted: check required fields, normalize the edit plan
        assert s.get("title") and s.get("scenes") and all(
            sc.get("narration") and sc.get("image_search") for sc in s["scenes"]), f"bad short: {s}"
        if not fact_check(s):
            print(f'  Dropped "{s["title"]}": its central claim didn\'t hold up against the sources')
            myth = f"{s.get('topic') or s['title']}: {s.get('myth_note') or 'not true as told'}"[:300]
            ch["myths"] = [m for m in ch.get("myths", []) if m != myth] + [myth]
            channel_profiles.save_channel(ch)
            continue
        kept.append(s)
        if s.get("fact_check"):  # its rewrites come after the story checks: the text rules again, as edit_plan notes
            lines, notes = [sc["narration"] for sc in s["scenes"]], s.get("editor_notes") or []
            left = story_problems(lines)
            if not lo - 15 <= (words := sum(len(t.split()) for t in lines)) <= hi + 15:  # the editor's own slack
                left.append(f"the script has {words} words, planned {lo}-{hi}")
            s["editor_notes"] = notes + [f"STILL (after the fact check): {p}" for p in left if f"STILL: {p}" not in notes]
        s["shape"] = s.get("shape") if s.get("shape") in SHAPES else ""
        s["thumbnail_prompt"] = str(s.get("thumbnail_prompt") or "").strip()[:400]
        s["music_mood"] = s.get("music_mood") if s.get("music_mood") in MOODS else ""
        s["palette"] = s.get("palette") if s.get("palette") in PALETTES else ""
        s["hook_text"] = str(s.get("hook_text") or s.get("thumbnail_text") or "").strip().upper()[:40]
        opts = s.get("hook_options")
        s["hook_options"] = [str(o).strip() for o in opts if str(o).strip()][:3] if isinstance(opts, list) else []
        for i, sc in enumerate(s["scenes"]):
            sc["image_search"] = str(sc.get("image_search") or "").strip()[:120]
            sc["video_search"] = str(sc.get("video_search") or sc["image_search"]).strip()[:120]
            sc["ai_image"] = str(sc.get("ai_image") or "").strip()[:400]
            sc["motion"] = str(sc.get("motion") or "").strip()[:200]
            sc["motion_people"] = sc.get("motion_people") is True
            sc["animate"] = sc.get("animate") is True and bool(sc["motion"])
        for sc in [sc for sc in s["scenes"] if sc["animate"]][5:]:  # GPU time (~2 min each): at most 5 clips
            sc["animate"] = False
        for i, sc in enumerate(s["scenes"]):
            if sc.get("move") not in MOVE_NAMES:
                sc["move"] = MOVES[i % len(MOVES)]
            sc["shot"] = str(sc.get("shot") or "").strip()[:300]
            said = plan_rules.words_of(sc["narration"])
            sc["graphic"] = plan_rules.clean_graphic(sc.get("graphic"), said) if i else None
            sc["full"] = plan_rules.clean_full(sc.get("full"), said) if i else None
            sc["sound"] = audio_mix.clean_sound(sc.get("sound"), said)
            pr = sc.get("person")
            ok = (isinstance(pr, dict) and all(isinstance(pr.get(k), str) and pr[k].strip()
                                               for k in ("name", "trigger", "image_search"))
                  and plan_rules.contains(said, plan_rules.words_of(pr["trigger"]))
                  and len(plan_rules.words_of(pr["name"])) >= 2)  # single names ("Jack") match too many photos
            sc["person"] = {k: pr[k].strip() for k in ("name", "trigger", "image_search")} if ok else None
            if sc["person"]:
                sc["graphic"] = None  # one overlay per scene
                if any(w in sc.get("shot", "").lower() for w in ("portrait", "headshot")):
                    sc["shot"] = f"Wide view of {s['subject']}: {sc['narration']}"[:300]
                    if sc["person"]["name"].lower() in sc.get("image_search", "").lower():
                        sc["image_search"] = s["subject"][:120]
            em = sc.get("emphasis")
            sc["emphasis"] = em.strip() if isinstance(em, str) and plan_rules.contains(said, plan_rules.words_of(em)) else None
            sc["transition"] = plan_rules.clean_transition(sc.get("transition")) if i else "fade"
        max_full_p = rules.max_full_planned()
        plan_rules.limit_full(s["scenes"], max_full_p)
        if max_full_p > MAX_FULL_PLANNED:
            plan_rules.fill_money_graphics(s["scenes"])
            if s["scenes"]:
                s["scenes"][-1]["narration"] = re.sub(r"[.;…]+$", "", s["scenes"][-1]["narration"].strip())
        pool_cands = (picture_pool.load_pool(Path(s["pool_dir"]), thumbs=False) or []) if s.get("pool_dir") else []
        picture_pool.clean_pics(s, pool_cands)
        for sc in s["scenes"]:
            if sc.get("person") and isinstance(sc.get("pic"), int) and 1 <= sc["pic"] <= len(pool_cands):
                if plan_rules.is_person_portrait(pool_cands[sc["pic"] - 1], sc["person"]["name"], s.get("catalog"), sc["pic"]):
                    sc["pic"] = None
        plan_rules.settle_style(s, ch)
        plan_rules.limit_style(s["scenes"])
        audio_mix.limit_sounds(s["scenes"])
    if kept and session.RULE_SETTINGS.get("visuals") == "blender":  # every scene is drawn: the engineer plans it
        blender_plan.plan_builds(kept, ch)
    return kept


def narration_lines(v) -> list[str]:
    """Scene narrations from an AI reply: a list of strings (or of {"narration": ...})."""
    items = v if isinstance(v, list) else []
    return [t for t in (str((x.get("narration") if isinstance(x, dict) else x) or "").strip() for x in items) if t]


def edit_scripts(shorts: list[dict], ch: dict, problems: dict[int, list[str]] | None = None) -> None:
    """The script editor pass: strongest hook, read-aloud fixes, cuts, hook/thumbnail/title consistency,
    the story rules. In collaborative mode, the OTHER AI edits the drafts; in solo mode, the same AI
    critiques and refines its own drafts. A failed or malformed reply keeps the draft. A script that still breaks
    a checkable story rule (story_problems) goes back once with `problems` ({index: [problem]}); whatever is left
    becomes a STILL: line in the editor notes."""
    editor = session.BRAIN if session.SOLO else ("gemini" if session.BRAIN == "claude" else "claude")
    lo, hi, s_lo, s_hi, _ = length_plan()
    mode_str = " (solo)" if session.SOLO else ""
    print(f"{editor.capitalize()}{mode_str} is editing the script(s)...")
    retry = (f"""SECOND PASS: these scripts still break the story rules. Fix exactly these problems:
{json.dumps(problems, ensure_ascii=False)}
""" if problems else "")
    drafts = [{"index": i, "topic": s["topic"], "shape": s.get("shape"), "title": s["title"],
               "hook_text": s.get("hook_text"), "thumbnail_text": s.get("thumbnail_text"),
               "hook_options": s.get("hook_options"), "scenes": s["lines"], "pictures": picture_pool.pictures_of(s) or "none listed"}
              for i, s in enumerate(shorts)]
    role_desc = ("You drafted the scripts below; refine and edit each one to make it as gripping as possible."
                 if session.SOLO else
                 "Another writer drafted the scripts below; make each one as gripping as possible.")
    data = llm.ask_ai(f"""You are the script editor of a faceless YouTube Shorts channel. Niche: {ch['niche']}.
Tone: {ch.get('tone', '')}. {role_desc}
About half our viewers swipe away in the first second, so the hook matters most.
For each script:
1. Hook: score every candidate first sentence (hook_options and scene 1's first sentence) 1-10 for
   "would a stranger scrolling past stop, AND need to stay for the answer?". Strong: the story's strangest
   moment told as it happens, at most 12 words, understood with no context, showing what happens and holding
   back why. Weak: a summary of the whole story, a setup, a name nobody knows, a date first, vague words
   ("strange", "mysterious", "incredible"). Open scene 1 with the best one, or a better one you write from
   the script's own facts.
2. Read every line aloud in your head as the narrator would say it: fix tongue-twisters, sentences over
   about 20 words, stacked numbers, awkward words for a text-to-speech voice, anything a 5th grader
   wouldn't get. The narration should flow as one story; choppy fragments read like a list.
3. Cut filler and empty lines ("this changed everything", "little did they know"): every scene adds
   something new a camera could show. No phrase of 3+ words twice.
4. Make it follow these rules; reorder and rephrase as much as needed (our retention curves drop hardest
   4-12 seconds in and keep sliding when a script recaps, rewinds to a timeline or answers its question early):
{session.RULES["Story rules"]}
5. hook_text (big words over the first second), thumbnail_text and title must tease the same story
   without repeating each other's words or the hook sentence; hook_text sharpens the same question as
   the hook sentence (sound-off viewers read it instead), never a separate idea. Fix whichever fails.
Each script's "pictures" lists the real pictures found for it: keep lines built on them showable.
Change wording, never claims: add no fact that isn't already in the script. Keep {s_lo}-{s_hi} scenes of 4-{channel_profiles.SCENE_WORDS}
words each (a new picture every ~3 seconds; only a scene that needs time on one picture may run up to
{channel_profiles.LONG_SCENE_WORDS}), {lo}-{hi} words in total. {SCENE_CUTS} Return every scene, changed or not.
notes: 1-4 short lines: the hook scores and what you changed and why.
{retry}Scripts: {json.dumps(drafts, ensure_ascii=False)}
Reply with ONLY JSON: {{"shorts": [{{"index": 0, "scenes": ["...", "..."], "title": "...", "hook_text": "...",
"thumbnail_text": "...", "notes": ["..."]}}]}}""", fatal=False, brain=editor) or {}
    who = session.LAST_AI.capitalize()  # Claude steps in when Gemini fails
    for r in data.get("shorts", []) if isinstance(data.get("shorts"), list) else []:
        i = r.get("index") if isinstance(r, dict) else None
        if not (isinstance(i, int) and 0 <= i < len(shorts)):
            continue
        s, lines = shorts[i], narration_lines(r.get("scenes"))
        words = [len(t.split()) for t in lines]
        notes = [str(x).strip()[:300] for x in r.get("notes") or [] if str(x).strip()][:4] \
            if isinstance(r.get("notes"), list) else []
        if s_lo <= len(lines) <= s_hi and max(words) <= channel_profiles.LONG_SCENE_WORDS + 2 and lo - 15 <= sum(words) <= hi + 15:
            s["lines"] = lines
        else:
            notes.append("its scene edit broke the length rules, so the writer's scenes were kept")
        for k in ("title", "hook_text", "thumbnail_text"):
            if isinstance(r.get(k), str) and r[k].strip():
                s[k] = r[k].strip()
        s["editor_notes"] = (s.get("editor_notes") or [] if problems else []) + ([f"{who}: {x}" for x in notes] or [f"{who}: no changes"])
    reads = cold_read(shorts)  # every Short, also one whose edit was refused: the kept scenes are what gets judged
    for i, s in enumerate(shorts):
        if i in reads:
            s["story_read"] = reads[i]
        else:
            s["editor_notes"] = (s.get("editor_notes") or []) + ["the cold reader didn't answer: only the text rules were checked"]
        s["_problems"] = story_problems(s["lines"], reads.get(i))
    failing = [s for s in shorts if s.get("_problems")]
    if problems is None and failing:  # once: the editor gets the problems and fixes its version
        print(f"  {len(failing)} script(s) broke the story rules, sending back to the editor once...")
        edit_scripts(failing, ch, {i: s["_problems"] for i, s in enumerate(failing)})
    for s in shorts:
        if left := s.pop("_problems", None):
            s["editor_notes"] = (s.get("editor_notes") or []) + [f"STILL: {p}" for p in left]


HOOK_KINDS = ("moment", "summary", "money_claim")


def cold_read(shorts: list[dict]) -> dict[int, dict]:
    """How a stranger hears each final script (audit 2026-10-31): the editor used to report payoff_scene, list_like and
    hook_kind about its own version and story_problems believed it. This reader sees only the scenes (no topic, notes
    or research). One call for all Shorts; {index: reading} for the valid answers ({} when it doesn't answer)."""
    rows = [{"index": i, "scenes": [{"scene": k + 1, "narration": t} for k, t in enumerate(s["lines"])]}
            for i, s in enumerate(shorts)]
    print(f"{session.BRAIN.capitalize()} is reading the script(s) as a stranger would...")
    data = llm.ask_ai(f"""You are a stranger scrolling YouTube Shorts and you know nothing about these stories. Read each script
below exactly as a viewer hears it, scene by scene, and say honestly what you get from it. Nobody here wrote it:
praise nothing that isn't there.
For each Short:
- question: the question the first sentence makes you need answered, in your own words; "none" if it leaves you
  nothing to wonder about (it already told you the whole story, or you don't care yet).
- answer: the number of the scene where that question is answered, or null if it never is.
- new: one true/false per scene, in order: does this scene give you new information or a new question? false for a
  recap, a fact said again, filler, or background you didn't need yet.
- list_like: true if the scenes could be reordered without breaking the story (a list of facts, not one story).
- swipe: the number of the first scene where most strangers would swipe away, or null if it holds them to the end;
  swipe_why: one short reason, else null.
- hook_kind: "moment" if the first line happens inside the strangest moment, "summary" if it states the whole story,
  "money_claim" if it is a specific money figure tied to someone or something the viewer can picture.
Scripts: {json.dumps(rows, ensure_ascii=False)}
Reply with ONLY JSON: {{"shorts": [{{"index": 0, "question": "...", "answer": 12, "new": [true, false], "list_like": false,
"swipe": null, "swipe_why": null, "hook_kind": "moment"}}]}}""", fatal=False) or {}
    out = {}
    for r in data.get("shorts") if isinstance(data.get("shorts"), list) else []:  # LLM output is untrusted
        i = r.get("index") if isinstance(r, dict) else None
        if not (type(i) is int and 0 <= i < len(shorts) and isinstance(r.get("question"), str) and r["question"].strip()):
            continue
        n = len(shorts[i]["lines"])
        scene = lambda v: v if type(v) is int and 1 <= v <= n else None  # noqa: E731
        new = r.get("new")
        out[i] = {"question": r["question"].strip()[:200], "answer": scene(r.get("answer")),
                  "new": new if isinstance(new, list) and len(new) == n and all(type(x) is bool for x in new) else None,
                  "list_like": r.get("list_like") is True, "swipe": scene(r.get("swipe")),
                  "swipe_why": str(r.get("swipe_why") or "").strip()[:160],
                  "hook_kind": r.get("hook_kind") if r.get("hook_kind") in HOOK_KINDS else None}
    return out


def story_problems(lines: list[str], read: dict | None = None) -> list[str]:
    """The checkable story rules (STORY_RULES): the text rules (no line opens with a date, a short first sentence that
    ends by scene 2) and, with the cold reader's `read` (cold_read), the answer comes last, line 1 opens a question,
    no run of scenes adds nothing, no early swipe point, the beats aren't a list, and (rules setting `hook`,
    2026-10-27 first-second research) what kind of first line it is."""
    found, read = [], read or {}
    if (answer := read.get("answer")) and answer < len(lines) - 1:
        found.append(f"the hook's question is answered in scene {answer} of {len(lines)}: the answer must come in the "
                     "last scene or the last two, and the Short ends there")
    if read.get("question", "").lower().strip(" .") == "none":
        found.append("the first sentence leaves a stranger nothing to wonder about: open a question only the ending answers")
    new, k = read.get("new") or [], 0
    while k < len(new):  # runs of 2+ scenes that add nothing
        end = k
        while end < len(new) and not new[end]:
            end += 1
        if end - k >= 2:
            found.append(f"scenes {k + 1}-{end} add nothing new for a viewer (a recap, filler or background too early): "
                         "cut them or turn them into the next question")
        k = end + 1
    if (swipe := read.get("swipe")) and swipe <= 4:
        found.append(f"a stranger would likely swipe at scene {swipe} ({read.get('swipe_why') or 'no reason given'}): "
                     "make it raise the stakes or open the next question")
    for k, line in enumerate(lines):
        if DATE_FIRST.match(line):
            found.append(f'scene {k + 1} starts with a date ("{line}"): bring the year in mid-sentence, or leave it out')
    first = plan_rules.first_sentence(lines)
    if len(first.split()) > 12:
        found.append(f'the first sentence has {len(first.split())} words ("{first}"): at most 12')
    if len(lines) > 1 and not " ".join(t.strip() for t in lines[:2]).startswith(first):
        found.append(f'the first sentence ("{first}") runs past scene 2: it must end in scene 1 or scene 2')
    if read.get("list_like"):
        found.append('the beats read as a list of facts: link each one to the one before with "but", "so" or "you see"')
    want, hook_kind = session.RULE_SETTINGS.get("hook"), read.get("hook_kind")
    if want == "moment" and hook_kind == "summary":
        found.append('the first line sums up the story: open inside the strangest moment, told as it happens '
                     '(Voggle: "The axe cut off the rooster\'s head, but...")')
    if want == "money_claim" and hook_kind is not None and hook_kind != "money_claim":
        found.append('the first line needs a specific money figure tied to a person or thing the viewer can picture '
                     '("This man effectively created a free money machine...")')
    return found


# "In 1932, ...", "By the 1850s", "1974:", "On 16 October", "In October" (STORY_RULES: no line starts with a date)
DATE_FIRST = re.compile(r"^\W*(?:(?:in|on|by|from|until|since|during|around)\s+(?:the\s+)?)?(?:(?:early|late|mid)[\s-]+)?"
                        r"(?:\d{3,4}s?\b|\d{1,2}(?:st|nd|rd|th)?\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)|"
                        r"(?:january|february|march|april|june|july|august|september|october|november|december)\b)", re.I)




def direct_scripts(shorts: list[dict], ch: dict) -> None:
    """The planner plans the edit (footage searches, shots, camera, graphics, person cards, AI fallbacks,
    palette, music, thumbnail) on the final narration, which it may not change."""
    print(f"{session.BRAIN.capitalize()} is planning the edit...")
    final = [{"index": i, "topic": s["topic"], "title": s["title"], "pictures": picture_pool.pictures_of(s) or "none listed",
              "scenes": [{"scene": k + 1, "narration": t} for k, t in enumerate(s["lines"])]} for i, s in enumerate(shorts)]
    style_text = "\n".join(f"  - {e['name']} ({e['kind']}): {e['description']}; fits: {e['fits']}" for e in style_lab.style_library())
    recent_looks = ch.get("recent_looks", [])[-2:] or "none"
    data = llm.ask_ai(f"""You are the director of YouTube Shorts for a faceless channel. Niche: {ch['niche']}.
The narration below is final: never change a word of it. Plan the edit of every scene of every Short.
{session.RULES["Directing"]}
  move = camera move that suits the image: "in" (faces, details, tension), "out" (reveals),
  "left"/"right" (wide places, crowds, landscapes), "up"/"down" (tall buildings, full-length
  portraits). Vary them; never the same move twice in a row.
  graphic = on-screen callout or null. Use on 4-7 scenes, mixing at least 3 different styles,
  never scene 1 (it gets the hook title):
  {{"style": "question", "text": "WHY DIDN'T THE GUNS WORK?"}} at most once, at a cliffhanger the script
  answers LATER (the picture dims and the question holds; up to 6 words, ends with "?"),
  {{"style": "kinetic", "text": "THREE SOLDIERS", "trigger": "three"}} at most twice, for a key phrase
  that should hit hard (1-4 words, ALL spoken in that scene; its letters drop in one by one),
  {{"style": "invented", "text": "...", "trigger": "..."}} only with an invented_overlay (below), at most twice,
  {{"style": "date", "text": "1911", "trigger": "1911"}} when a key year/date is first said,
  {{"style": "place", "text": "PARIS, FRANCE", "lat": 48.86, "lon": 2.35, "trigger": "Paris"}} when
  the location is introduced (lat/lon of that place, used for an animated map); when the scene is a
  journey, add where it started and a route line is drawn:
  "from": {{"text": "NEW YORK", "lat": 40.71, "lon": -74.01}},
  {{"style": "fact", "text": "2 YEARS MISSING", "trigger": "two years"}} for the single most
  surprising fact,
  {{"style": "stat", "value": 62, "of": 97, "text": "SURVIVED", "trigger": "sixty two"}} for a number
  worth seeing: with "of" (up to 200) it becomes a grid of dots with "value" of them lighting up;
  without "of" a counter ticks up to "value" (e.g. {{"style": "stat", "value": 9000, "text": "WORDS"}}),
  {{"style": "timeline", "start": "SEPT 1", "end": "SEPT 2", "text": "17 HOURS LATER", "trigger":
  "seventeen hours"}} when time passes between two moments (a marker slides from start to end),
  {{"style": "headline", "text": "RAINMAKER BLAMED FOR FLOOD", "paper": "THE SAN DIEGO UNION", "date":
  "JANUARY 28, 1916", "trigger": "newspapers"}} when the press or the public reacted (a front page slams
  in; up to 7 words; give "paper" only if that real paper covered it, else leave it out),
  {{"style": "quote", "text": "I could make it rain anywhere", "by": "Charles Hatfield", "trigger": "he
  boasted"}} for a real, documented quote of up to 12 words (typed out on aged paper; never invent one),
  {{"style": "compare", "text": "HIS FEE", "a_label": "1916", "a_value": 10000, "a_show": "$10,000",
  "b_label": "TODAY", "b_value": 290000, "b_show": "$290,000", "trigger": "ten thousand"}} when two
  sizes, amounts or heights are worth seeing side by side (two bars grow; values must be true),
  {{"style": "stamp", "text": "HOAX", "trigger": "fake"}} for the verdict at a twist or payoff (a red
  rubber stamp thumps on; 1-2 words like HOAX, BANNED, DENIED, CONFIRMED, GUILTY).
  Max 4 words per text, and it must match what the narration says in that scene.
  trigger = the exact narration words at which it should pop up (it appears as they are spoken).
  person = when a real, named HUMAN (not an animal) is mentioned in the scene, using their full
  name (first and last); not in scene 1's first 2 seconds:
  {{"name": "Thomas Hicks", "trigger": "Thomas Hicks", "image_search": "Thomas J. Hicks 1904 marathon"}}.
  trigger = the exact words of the name as spoken in this scene's narration (their photo pops up
  at that moment). image_search must be specific enough to find THAT person (add the year or what
  they're known for). Use it every time a new person is introduced; otherwise null. A scene has a
  person OR a graphic, never both.
  emphasis = the single most important word in the scene, copied exactly from the narration
  (it glows in the captions), or null.
  transition = how this scene starts, your choice for every cut, from the STYLE LIBRARY transitions below
  (or "invented"). Edit like a good editor: a hard "cut" keeps the energy up inside one moment, "fade"
  suits time jumps and calm or sad beats, "flash" only the 2-3 biggest reveals (it has an impact sound),
  and the special ones (wipe, whip, leak, invented) at most 3 per Short, matched to the look. Scene 1's
  transition is ignored.
  ai_image = prompt for a local image generator, used only if no real video clip or photo fits this
  scene. {session.RULES["AI paintings"]}
  sound = a sound of the STORY itself on one spoken word, or null (the usual): {{"word": "jammed", "sound": "gun cock"}}
  (word = spoken in this scene; sound = 1-4 plain words naming a real recordable sound: "gun cock", "ship horn",
  "crowd gasp", "splash", "church bell", "typewriter"). At most 3 per Short, only for concrete moments where the
  sound makes the line land; never for abstract lines, never music.
  full = a FULL-SCREEN motion graphic that replaces this scene's picture, or null (the usual). Use it on at
  most 2 scenes, only where it shows the moment better than any picture or footage could: a trip between
  places, a number too big to picture, a document that matters, several people/things that connect, or a
  story-specific mechanism/diagram/cause-and-effect chain.
  Rules: never scene 1 (its opening is planned on its own), never two in a row, only on a scene of at least
  {channel_profiles.FULL_MIN_WORDS} words (it needs ~3 seconds), real facts only (they are
  fact-checked), labels at most 3 words, "word" = a word or name spoken in that scene's narration when that
  element should appear. One of:
  {{"type": "journey", "stops": [{{"name": "Port Elizabeth", "lat": -33.96, "lon": 25.6, "word": "Port Elizabeth"}},
   {{"name": "Uitenhage", "lat": -33.76, "lon": 25.4, "word": "Uitenhage"}}], "note": "1881 · 32 km"}}
   (1-4 real places in travel order; an old-atlas map, pins drop as named, a route line draws between them);
  {{"type": "number", "value": 30000, "label": "mourners", "icon": "person", "thing": "mourner", "each": 1000, "word": "thirty"}}
   (a big counter, then ink figures each standing for `each`; thing = what ONE figure is, a singular noun ("emu",
   "barrel", "cat"): it is painted as an ink silhouette; icon = the closest of {list(ICONS)} as a backup; for "then vs now"
   add "compare": {{"a_label": "1858", "a_value": 100, "b_label": "today", "b_value": 3}});
  {{"type": "board", "items": [{{"label": "JACK, 1890", "find": "photo of Jack the baboon at the levers", "word": "Jack"}}],
   "links": [[0, 1]]}} (an evidence board of 3-5 REAL photos pinned up with red thread between linked ones;
   find = what real photo of the story to look for; only when such photos of each item surely exist);
  {{"type": "document", "kind": "telegram", "key_line": "The baboon stays and gets paid", "date": "1890",
   "word": "telegram"}} (kind one of {list(DOC_KINDS)}; the key line is underlined in red as it is said: a
   real, documented line of at most 14 words, or a plain summary of what the document said; "paper" = the
   masthead only for a real newspaper that covered it; "find" = what real scan of it to look for, if any);
  {{"type": "custom", "kind": "diagram", "title": "VASA CROSS-SECTION", "brief": "Cross-section of the top-heavy warship tilting 20 degrees in a wind gust as water floods the open lower gunports", "words": ["gust", "twenty", "gunports"], "photos": [{{"label": "THE VASA", "find": "Vasa warship hull", "word": "warship"}}]}}
   (a bespoke scene coded from scratch for this moment when a custom visual metaphor, mechanism, cross-section,
   flow chart or photo collage fits better than the 4 standard templates; kind one of {list(CUSTOM_KINDS)}:
   "diagram" for a custom SVG cross-section/mechanism/scale/gauge, "collage" for 1-3 real archival photos
   sliding in with drawn arrows and callouts, "flow" for a step-by-step cause->effect->twist chain, "clock"
   for a clock/countdown/schedule with levers or gauges; "words" = 2-4 spoken words from the scene that trigger
   each animation beat; "photos" = 0-3 optional real photos from the pool to cut out into the scene).
  animate = true on 3-5 scenes (include scene 1 when its picture could move: motion in the very
  first frame stops people scrolling) whose picture would come alive with gentle motion of one of
  two kinds: ATMOSPHERE (water, waves, clouds, rain, snow, flags, fire, light, or smoke and steam rising
  from a visible source; never dust, fog or mist added to a picture that has none)
  or PEOPLE moving slowly and simply (working, a crowd shifting, someone walking calmly). Never fast
  action, fights, vehicles or machines in motion, or a close-up of a real person's face.
  motion = for those scenes, one short line describing the movement, else null;
  motion_people = true when the movement is people, false when it is atmosphere.
- palette: the colour scheme of this Short's graphics and captions, one of {list(PALETTES)}, chosen to
  fit the story (fire/disaster: ember or crimson; sea/ice: sky or teal; old documents: parchment; royal or
  mystical: violet; nature: lime). Vary it across Shorts.
- music_mood: the background music that fits the story's feeling, one of {MOODS} (vary it across
  Shorts; a disaster is "tense" or "somber", a funny loophole "playful", a big achievement "epic").
- thumbnail_prompt: image-generator prompt for the thumbnail background, written like ai_image (subject, setting,
  light, a real hand-made medium with its marks; same face rule). It raises the title's question without answering
  it, true to the story: ONE big focal subject that reads in under a second at phone-thumbnail size, little else,
  strong light-dark contrast. Use the strongest of these: extreme size contrast (something huge beside something
  tiny from the story); one real element of the story shown oversized; a lone small figure in a vast setting; a map
  or aerial view with one route or spot marked; a before/after split of one subject; many copies of one object.
  Clothing, buildings, tech and objects must match the story's era and niche.
- Draft description (2-3 sentences plus 3 hashtags) and 10-15 tags (refined later with real search data).
- look: ONE photo look for this Short's still pictures, or null (null is a good answer: use a look only when
  it adds to the story). {{"name": "<a library look>"}}, never {recent_looks} (used on the channel's last
  Shorts). If no library look fits but a new one would really serve THIS story, invent it:
  {{"invent": {{"title": "Wanted poster", "brief": "what it looks like, specific: materials, colours, texture,
  what moves", "fallback": "<the closest library look>"}}}}. The picture picker puts it on 2-4 still scenes
  (never scene 1, never real film).
- invented_transition / invented_overlay: null, or (only if you use "invented" as a transition / a graphic
  style) {{"title": "...", "brief": "what it looks like and how it moves", "fallback": "<closest library
  transition / overlay>"}}. Invent only when the library has nothing that fits; a fallback is used if it fails.
STYLE LIBRARY (name (kind): what it is; fits):
{style_text}
Shorts: {json.dumps(final, ensure_ascii=False)}
Reply with ONLY JSON, one entry in "scenes" per scene, in order: {{"shorts": [{{"index": 0, "palette": "...",
"music_mood": "...", "thumbnail_prompt": "...", "description": "...", "tags": ["..."], "look": null,
"invented_transition": null, "invented_overlay": null,
"scenes": [{{"pic": null, "image_search": "...", "video_search": "...", "shot": "...", "move": "in", "graphic": null,
"person": null, "emphasis": "...", "transition": "fade", "ai_image": "...", "animate": false,
"motion": null, "motion_people": false, "sound": null, "full": null}}]}}]}}""")
    plans = {r["index"]: r for r in data.get("shorts", []) if isinstance(r, dict) and isinstance(r.get("index"), int)}
    for i, s in enumerate(shorts):
        r = plans.get(i, {})
        s.update({k: r[k] for k in ("palette", "music_mood", "thumbnail_prompt", "description", "tags") if r.get(k)})
        s.update({k: r.get(k) for k in ("look", "invented_transition", "invented_overlay")})  # validated in write_scripts
        scenes = r.get("scenes") if isinstance(r.get("scenes"), list) else []
        s["scenes"] = [{**(scenes[k] if k < len(scenes) and isinstance(scenes[k], dict) else {}), "narration": t}
                       for k, t in enumerate(s.pop("lines"))]  # the final words win over anything the director echoed
        for sc in s["scenes"]:
            sc["image_search"] = str(sc.get("image_search") or "").strip() or s["subject"]


def article_text(title: str) -> str:
    """Plain text of an English Wikipedia article ('' when missing or unreachable)."""
    raw = image_sources.wm_get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext=1"
                 f"&redirects=1&titles={urllib.parse.quote(title)}", f'Wikipedia "{title}" text')
    pages = json.loads(raw).get("query", {}).get("pages", {}) if raw else {}
    text = next((p.get("extract") or "" for p in pages.values()), "")
    for marker in ("\n== References ==", "\n== See also ==", "\n== External links ==", "\n== Further reading ==", "\n== Notes =="):
        if marker in text:
            text = text.split(marker)[0].strip()
    return text


def check_twists(shorts: list[dict]) -> None:
    """Before any script is written: each topic's twist against its Wikipedia text. The Oxford Short (2026-10-26)
    was written around the 1915 legend that Murray found Minor in an asylum by surprise; the fact check, run on
    the finished script, only patched one line and the ending still told the legend. It also left out what the
    articles lead with (Minor had killed a man), which the 402K-view Short on the same story opened with.
    One AI call; a rewritten topic replaces s["topic"] and the reason goes in s["twist_check"] (edit_plan.txt)."""
    rows = [{"index": i, "topic": s["topic"], "main_character": s.get("character") or s["subject"],
             "wikipedia": {t: x[:8000] for t, x in (s.get("_texts") or {}).items() if x}} for i, s in enumerate(shorts)]
    rows = [r for r in rows if r["wikipedia"]]
    if not rows:
        return
    print("Checking each story's twist against Wikipedia...")
    data = llm.ask_ai(f"""Before the scripts are written, check each story's twist (the surprise it saves for the end) against
its Wikipedia text.
- If the articles call the twist a legend, a myth, disputed or wrong, rewrite the topic so the Short tells what really
  happened: the famous version may set it up, but the ending must be the true one ("the famous story says X; in fact Y").
- If the articles give the main character a far stronger true fact that the topic leaves out (a crime, a death, a
  secret that explains the whole story), add it to the topic so the Short can open with it.
- Otherwise topic = null. A rewritten topic is 1-2 sentences told through the same main character, with the twist
  that makes it worth telling.
Stories: {json.dumps(rows, ensure_ascii=False)}
Reply with ONLY JSON: {{"stories": [{{"index": 0, "topic": null, "why": "one line"}}]}}""", fatal=False)
    got = data.get("stories") if isinstance(data, dict) else None
    for r in got if isinstance(got, list) else []:  # LLM output is untrusted
        i = r.get("index") if isinstance(r, dict) else None
        if isinstance(i, int) and not isinstance(i, bool) and 0 <= i < len(shorts) \
                and isinstance(r.get("topic"), str) and r["topic"].strip():
            s, new = shorts[i], r["topic"].strip()[:600]
            why = str(r.get("why") or "the twist didn't hold up").strip()[:300]
            s["twist_check"] = f'topic rewritten ({why}): "{s["topic"]}" -> "{new}"'
            s["topic"] = new
            print(f'  "{s["subject"]}": {s["twist_check"][:200]}')


def fact_check(s: dict) -> bool:
    """Check every line against the story's Wikipedia articles and rewrite what they don't support.
    Runs before the edit plan is validated, so callouts whose trigger words changed drop out there.
    Notes go in s["fact_check"] (edit_plan.txt). False when the story's central claim is false."""
    print(f'Fact-checking "{s["title"]}"...')
    texts = s.pop("_texts", None) or {t: article_text(t)[:15000] for t in s["wiki_articles"][:4]}
    s["research"] = texts  # motion-graphic rescues reuse it (never saved in state.json)
    script = [{"scene": i + 1, "narration": sc["narration"], "shot": sc.get("shot"), "ai_image": sc.get("ai_image"),
               "image_search": sc.get("image_search"), "video_search": sc.get("video_search"),
               "graphic": sc.get("graphic"), "person": sc.get("person"), "full": sc.get("full")}
              for i, sc in enumerate(s["scenes"])]
    data = llm.ask_ai(f"""You are a strict fact-checker for a fact-based Shorts channel. Check every claim in
this script and its on-screen text against the Wikipedia articles below.
- Supported by the articles: keep it.
- Contradicted by them: fix it.
- Not in the articles: keep it only if you are confident it is true and well documented. If sources
  disagree or it is a legend, make the line accurate ("legend says", "reports claim") or replace it
  with a supported fact.
- A legend stays a legend in every line: when one line tells it as "legend says", fix every later line that
  tells the same legend (or what follows from it) as fact. When the Short's ending is the legend, story_holds = false.
Rewrite only the scenes that need it. Keep each about as long as it was (at most {channel_profiles.LONG_SCENE_WORDS} words) with the same role in the story, scene
1's first sentence at most 12 words, and every word a graphic or person card pops up on ("trigger")
when it is still correct. A scene may be part of a sentence that runs on into the next scene: keep the
corrected part joining up with its neighbours. drop_graphic = true when that scene's graphic itself shows a wrong fact.
"full" is a full-screen motion graphic (map stops, a number, board labels, a document's key line): when any
of its places, numbers, labels or quoted words is wrong, give full_fix = the same object corrected, or
drop_full = true when it can't be fixed.
shot / ai_image / image_search / video_search: when your fix changes what that scene shows happening,
rewrite them to match the corrected line (same format and art style as before); else null.
story_holds = false only when the story's central claim is false or a myth; then myth_note = one line
on what really happened (else null).
hook_text / thumbnail_text: a corrected version only if the current one is false, else null.
Script: {json.dumps(script, ensure_ascii=False)}
hook_text: {s.get("hook_text")!r} | thumbnail_text: {s.get("thumbnail_text")!r}
Wikipedia articles: {json.dumps(texts, ensure_ascii=False)}
Reply with ONLY JSON: {{"story_holds": true, "fixes": [{{"scene": 3, "narration": "...", "drop_graphic": false, "drop_full": false, "full_fix": null,
"shot": null, "ai_image": null, "image_search": null, "video_search": null, "why": "..."}}], "hook_text": null, "thumbnail_text": null, "myth_note": null}}""", fatal=False)
    if not isinstance(data, dict):
        s["fact_check"] = ["NOT CHECKED (the AI didn't reply): check the facts yourself before posting"]
        return True
    s["fact_check"] = []
    for f in data.get("fixes") or []:
        n, line = (f.get("scene"), f.get("narration")) if isinstance(f, dict) else (None, None)
        if isinstance(n, int) and 1 <= n <= len(s["scenes"]) and isinstance(line, str) and 0 < len(line.split()) <= 30:
            sc = s["scenes"][n - 1]
            s["fact_check"].append(f'scene {n}: "{sc["narration"]}" -> "{line.strip()}" ({str(f.get("why") or "")[:500]})')
            sc["narration"] = line.strip()
            for k in ("shot", "ai_image", "image_search", "video_search"):  # the picture/footage must not show the corrected-away version
                if isinstance(f.get(k), str) and f[k].strip():
                    sc[k] = f[k].strip()
        if isinstance(n, int) and 1 <= n <= len(s["scenes"]) and f.get("drop_graphic") is True \
                and s["scenes"][n - 1].get("graphic"):  # wrong on-screen text goes even when the spoken line was right
            s["fact_check"].append(f"scene {n}: on-screen graphic removed ({str(f.get('why') or '')[:300]})")
            s["scenes"][n - 1]["graphic"] = None
        if isinstance(n, int) and 1 <= n <= len(s["scenes"]) and s["scenes"][n - 1].get("full"):
            sc = s["scenes"][n - 1]  # a motion-graphic correction counts even when the spoken line was right
            if f.get("drop_full") is True:
                s["fact_check"].append(f"scene {n}: motion graphic removed ({str(f.get('why') or '')[:300]})")
                sc["full"] = None
            elif isinstance(f.get("full_fix"), dict) and f["full_fix"].get("type") in FULL_TYPES:
                s["fact_check"].append(f"scene {n}: motion graphic corrected ({str(f.get('why') or '')[:300]})")
                sc["full"] = f["full_fix"]  # validated with the rest of the plan afterwards (clean_full)
    for k in ("hook_text", "thumbnail_text"):
        if isinstance(data.get(k), str) and data[k].strip():
            s["fact_check"].append(f'{k}: "{s.get(k)}" -> "{data[k].strip()}"')
            s[k] = data[k].strip()
    print(f"  {len(s['fact_check'])} fixes" if s["fact_check"] else "  every line holds up")
    s["myth_note"] = str(data.get("myth_note") or "").strip()
    return data.get("story_holds") is not False
