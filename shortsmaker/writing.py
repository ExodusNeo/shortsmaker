"""Topics -> Wikipedia research -> writer -> editor -> director -> fact check."""

import json
import shutil
import urllib.parse
from pathlib import Path

from shortsmaker import (
    audio_mix, channel_profiles, image_sources, llm, logbook, picture_pool, plan_rules, session, style_lab,
)
from shortsmaker.config import (
    CUSTOM_KINDS, DOC_KINDS, FULL_TYPES, ICONS, MAX_FULL_PLANNED, MOODS, MOVES, MOVE_NAMES, PALETTES, SHAPES,
)


def length_plan() -> tuple[int, int, int, int, str]:
    """(min words, max words, min scenes, max scenes, seconds) for this batch's scripts."""
    return (60, 72, 8, 10, "25-30") if session.SHORT_FORM else (95, 125, 11, 16, "40-50")


def write_scripts(ch: dict, n: int, topics: list[str] | None = None, pools: list[str] | None = None) -> list[dict]:
    """Plan n Shorts on new topics, or on exactly `topics` (comparison runs: the other AI's topics), as a small
    team: the planner picks topics, Wikipedia is read for each, the planner writes the narration, the OTHER AI
    edits it (edit_scripts), the planner plans the edit on the final words (direct_scripts), then the fact check.
    Before any writing, each topic's real pictures are gathered and listed (prepare_topic); a topic with too few
    is replaced by a backup. `pools` (Both mode): the pool folders of the same topics, by position."""
    trends = channel_profiles.trend_research(ch)
    trend_text = ""
    if trends:
        rows = [f"- \"{s['title']}\" | {s['views']:,} views" + (f", {s['views_per_day']:,}/day" if s.get("views_per_day") else "")
                + f" | {s['channel']}" for s in trends[:20]]
        trend_text = f"""
WHAT'S WORKING NOW in this niche (real YouTube data, today; top recent Shorts from proven channels):
{chr(10).join(rows)}
Use this to choose topics with proven demand and to write titles and hooks in the patterns that
recur among the leaders. Never remake one of these videos or copy its wording: every story must
be our own, true and not already covered above.
"""
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
views to judge" say little). The weak spot so far is the first second: Shorts the feed pushed still lost
4-8 of every 10 viewers there, so compare the hook lines and opening pictures of the Shorts that kept the
most viewers with those that kept the fewest.
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
{trend_text}
{what}
Viewers decide in one second whether to swipe, so pick stories whose single most shocking fact can be
said in 8 words or fewer that a stranger understands instantly (e.g. "A dead man won this horse race.").
Every Short needs a MAIN CHARACTER: one named person or animal the story follows, with a real photo or
portrait of them. Our Shorts built around one strange person or animal (Jack the baboon, Violet Jessop,
Emperor Norton, Lord Byron and his bear, Hiroo Onoda, Mike the headless chicken, the emus) were all pushed by
YouTube, and the named characters brought nearly all our subscribers; the ones about a thing, an event or a
group (a smell, a newspaper hoax, a fake statue, the WW2 Ghost Army) stalled, some under 60 views. This does not
narrow the topics: tell an event through the person at its center (the Great Stink through engineer Joseph
Bazalgette, the Cardiff Giant through George Hull who carved it). Choose an event with nobody to follow
only when nothing better is left.
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
Pictures and footage are gathered from these before any script is written: prefer stories with real photos or film.
Reply with ONLY JSON: {{"shorts": [{{"topic": "...", "character": "...", "subject": "...", "wiki_articles": ["..."],
"search_terms": ["..."], "visual_terms": ["..."], "people": ["..."]}}]}}""")
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
    assert shorts, f"no usable topics: {data}"
    kept, dropped = [], []
    for i, s in enumerate(shorts):
        if len(kept) == wanted:
            break
        print(f'Topic {i + 1}/{len(shorts)}: "{s["subject"]}": reading Wikipedia, finding real pictures and footage...')
        k = s.pop("_pos")
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
- {lo}-{hi} spoken words (about {secs} seconds: story Shorts hold viewers best under ~50 s), simple words a 5th grader understands.
- Structure, written like a documentary editor would cut it:
  hook (scene 1): viewers decide in one second whether to swipe. Its first sentence is 8 words or
  fewer: a concrete, surprising claim understood with no context that OPENS A QUESTION the viewer
  needs answered (how? why? what happened next?). Show the surprise, hold back the explanation.
  The opening picture already shows the subject, so the words must add what the picture can't: the
  stakes, the contradiction, the strange part. Good: "Parliament nearly fled London over one smell."
  (why?), "A broke man crowned himself Emperor of America." (and then?). Weak: "A railway once hired
  a baboon." over a photo of a baboon at the levers: the line and picture tell the whole story, so
  nothing is left to stay for (that Short lost 3 of 4 viewers in the first second); better: "This
  signalman never made one mistake in nine years." over an opening picture that doesn't show the
  baboon yet (the reveal comes a few scenes later). Never a setup, a greeting,
  a date first, a name nobody knows yet, or a technical detail. Tell the story through its
  main_character: the hook is about them ("This man...", "This baboon..."), and the story follows
  what they did and what happened to them. Draft 3 first sentences in hook_options, each from a
  different hook family (curiosity gap, result first, stakes, contrarian claim, before/after), then
  open scene 1 with the strongest. Scene 1 is that sentence plus at most one short line.
  confirmation (scene 2): one concrete, showable detail that proves the hook's claim is real (a
  record, a number, a witness, an object), without answering the hook's question.
  open loop right after: promise a twist ("but that wasn't the strangest part").
  scenes 2-3 keep moving FORWARD: they are where most viewers leave (on every one of our Shorts the
  retention curve holds through the hook, then drops hardest 4-12 seconds in, right where the script
  rewound to background: "In 1852, Joshua Norton tried to corner the rice market.", "James Wide bought
  Jack at a market."). Our Short that went forward instead ("And that stink hid a far deadlier secret in
  the same water.") lost the fewest. So after the hook: raise the stakes or show what happened next;
  never start a sentence with a date or with a name the viewer hasn't met yet; give background only as
  a half-line at the moment the story needs it.
  rising tension, drip-fed: every scene adds one new concrete fact, cause then effect, no filler.
  Answer each small question within a scene or two and raise the next one, so viewers always have
  one open question; the hook's main question stays open until the payoff.
  re-hook around the middle: a turn that raises the stakes ("then it got worse").
  payoff: the twist, then ONE last line that calls back to the hook's words or image, so the
  ending loops into the opening on a rewatch. End there: no "follow for more", no outro (an
  on-screen subscribe button and the pinned comment handle engagement).
- Never repeat yourself: every line adds something new. Apart from that one callback to the hook,
  no phrase of 3+ words may appear twice, and the callback must not reuse the previous scene's wording.
- Write for the picture: every scene must be about something a camera could show (a person,
  place, object, document or crowd), never an abstract line like "this changed everything". If a
  line has nothing to show, rewrite it around a concrete detail.
- Build on the real pictures: each topic's "pictures" lists the real photos and film found for it (#number,
  what it shows; [opener] = strong enough to open the Short). Where a strong picture exists, let the story pass
  through what it shows, and write the hook for an [opener] picture when one fits. The story rules above still
  come first: never bend a fact or the pacing to fit a picture.
- Every fact must be true: take facts from the research; anything else only if you are certain it
  is well documented. No made-up statistics or quotes.
- shape: the story's shape, one of {SHAPES}. Not one of the channel's last ones
  ({ch.get('recent_shapes', [])}), and a different one for each Short in this batch.
- scenes: the narration split into {s_lo}-{s_hi} short scenes of 4-{channel_profiles.SCENE_WORDS} words (about 3 seconds: each
  scene gets its own picture, and a new picture every ~3 seconds keeps viewers watching), cutting where the
  picture would naturally change: one image per scene. Only a scene that needs time on one picture (a trip
  between places, a big number, a document, several things that connect) may run up to {channel_profiles.LONG_SCENE_WORDS} words.
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
            em = sc.get("emphasis")
            sc["emphasis"] = em.strip() if isinstance(em, str) and plan_rules.contains(said, plan_rules.words_of(em)) else None
            sc["transition"] = plan_rules.clean_transition(sc.get("transition")) if i else "fade"
        plan_rules.limit_full(s["scenes"], MAX_FULL_PLANNED)
        picture_pool.clean_pics(s, (picture_pool.load_pool(Path(s["pool_dir"]), thumbs=False) or []) if s.get("pool_dir") else [])
        plan_rules.settle_style(s, ch)
        plan_rules.limit_style(s["scenes"])
        audio_mix.limit_sounds(s["scenes"])
    return kept


def narration_lines(v) -> list[str]:
    """Scene narrations from an AI reply: a list of strings (or of {"narration": ...})."""
    items = v if isinstance(v, list) else []
    return [t for t in (str((x.get("narration") if isinstance(x, dict) else x) or "").strip() for x in items) if t]


def edit_scripts(shorts: list[dict], ch: dict) -> None:
    """The OTHER AI edits the drafts: strongest hook, read-aloud fixes, cuts, hook/thumbnail/title consistency.
    A second model catches what the writer can't see in its own text. A failed or malformed reply keeps the draft."""
    editor = "gemini" if session.BRAIN == "claude" else "claude"
    lo, hi, s_lo, s_hi, _ = length_plan()
    print(f"{editor.capitalize()} is editing the script(s)...")
    drafts = [{"index": i, "topic": s["topic"], "shape": s.get("shape"), "title": s["title"],
               "hook_text": s.get("hook_text"), "thumbnail_text": s.get("thumbnail_text"),
               "hook_options": s.get("hook_options"), "scenes": s["lines"], "pictures": picture_pool.pictures_of(s) or "none listed"}
              for i, s in enumerate(shorts)]
    data = llm.ask_ai(f"""You are the script editor of a faceless YouTube Shorts channel. Niche: {ch['niche']}.
Tone: {ch.get('tone', '')}. Another writer drafted the scripts below; make each one as gripping as possible.
About half our viewers swipe away in the first second, so the hook matters most.
For each script:
1. Hook: score every candidate first sentence (hook_options and scene 1's first sentence) 1-10 for
   "would a stranger scrolling past stop, AND need to stay for the answer?". Strong: a concrete,
   surprising claim, 8 words or fewer, understood with no context, that opens a question (how? why?
   what next?) the script answers later. Weak: a setup, a name nobody knows, a date first, vague words
   ("strange", "mysterious", "incredible"), or a line that tells the whole story at once (with the
   opening picture of the subject, nothing is left to stay for). Open scene 1 with the best one, or a
   better one you write from the script's own facts.
2. Read every line aloud in your head as the narrator would say it: fix tongue-twisters, sentences over
   about 14 words, stacked numbers, awkward words for a text-to-speech voice, anything a 5th grader
   wouldn't get.
3. Cut filler and empty lines ("this changed everything", "little did they know"): every scene adds one
   new concrete fact a camera could show. No phrase of 3+ words twice, except one last line that calls
   back to the hook.
4. Keep the shape working: scene 2 proves the hook's claim is real with one concrete detail (without
   answering its question), then an open loop, a re-hook around the middle, the twist,
   then the callback ending. At every scene the viewer should have one open question: small ones
   answered within a scene or two, the hook's main question kept open until the payoff. Scenes 2-3 are
   where most viewers leave (our retention curves drop hardest 4-12 seconds in, where scripts rewound to
   background): they must move forward or raise the stakes; no sentence there may start with a date or a
   name the viewer hasn't met; background only as a half-line when the story needs it.
5. hook_text (big words over the first second), thumbnail_text and title must tease the same story
   without repeating each other's words or the hook sentence; hook_text sharpens the same question as
   the hook sentence (sound-off viewers read it instead), never a separate idea. Fix whichever fails.
Each script's "pictures" lists the real pictures found for it: keep lines built on them showable.
Change wording, never claims: add no fact that isn't already in the script. Keep {s_lo}-{s_hi} scenes of 4-{channel_profiles.SCENE_WORDS}
words each (a new picture every ~3 seconds; only a scene that needs time on one picture may run up to
{channel_profiles.LONG_SCENE_WORDS}), {lo}-{hi} words in total. Return every scene, changed or not.
notes: 1-4 short lines: the hook scores and what you changed and why.
Scripts: {json.dumps(drafts, ensure_ascii=False)}
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
        s["editor_notes"] = [f"{who}: {x}" for x in notes] or [f"{who}: no changes"]


# How an AI painting prompt (ai_image) is written: the director plans them with it and rewrite_paint_prompts()
# rewrites rejected ones with it. Owner 2026-10-21: paintings looked "way too AI" -> a named period medium.
AI_IMAGE_RULE = """One or two descriptive sentences, not a keyword list: the subject first with era-accurate details,
  then the setting, then the light (always name it: "low winter sun", "one oil lamp", "flat overcast daylight"),
  then a REAL hand-made medium of the story's era named with its physical marks, so it looks made by a person and
  can't pass for a real photo: "19th-century wood engraving from an illustrated newspaper, dense black hatching on
  yellowed newsprint"; "hand-colored copperplate etching, fine cross-hatching, faded watercolor washes on foxed
  paper"; "1940s gouache magazine illustration, flat matte paint, visible brush marks, coarse paper with halftone dots
  and slightly off-register colors"; "1930s silkscreen poster, three flat inks on grainy paper, misaligned color
  layers"; "loose oil sketch on canvas board, thick visible brushstrokes, unfinished edges"; "charcoal drawing on
  toned paper, smudged shading". Never "concept art", "digital illustration", "stylized", "cinematic", "highly
  detailed", "8k" or "vibrant" (they give the glossy AI look). The artwork fills the whole frame (never a framed
  poster, card or page with a border). Never "photograph" (a fake photo would pass
  as real evidence). Never a recognizable real person's face: show places, objects, crowds, hands,
  silhouettes or figures from behind. Never a close-up of the specific real object the story is about
  (a famous artifact, statue, building or document): the AI would invent what it looked like; show the
  setting or the people around it instead. Writing in the painting (a shop sign, a poster, a ship's name,
  a headline) is allowed when it helps tell the story: put the exact words in double quotes, at most 6,
  true to the story and its era (no invented names, dates or numbers). Without quotes the painting has no writing,
  so never paint a subject made of print without quoting its words (a newsstand, magazine rack, newspaper page,
  poster wall: the painter fills it with gibberish): quote the one cover that matters ("LIFE") or pick another subject."""


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
- pic = the number of the real picture from that Short's "pictures" list that shows this scene best, or null
  when none does. Never the same number twice in a Short; at most 2 different frames of one film. Scene 1 gets
  the most striking fitting one ([opener] first): from the story's own time (never a modern museum,
  replica or tourist photo), ideally the main character's face, and never a picture that shows the twist
  or the whole story at once (it must raise the hook's question, not answer it). Write shot from the
  picture you chose. An evidence board's
  items may carry "pic" the same way.
- image_search = a 2-5 word query to find a real photo, screenshot, portrait, artwork, document,
  place or object for this scene (e.g. "Nintendo Ultra Hand toy", "Lord Byron portrait").
  video_search = a 2-6 word video search query to find real video footage showing what this
  scene is about: gameplay, hardware demo, speedrun moment, historical newsreel, documentary clip,
  experiment or place in motion (e.g. "Super Mario 64 Bowser throw gameplay",
  "Nintendo Ultra Hand 1966 demonstration", "Niagara Falls barrel 1901 film"). Make each scene's
  video_search specific to that scene's action or subject so different scenes pull different clips.
- Edit plan for every scene:
  shot = the director's note for this scene's visual, one sentence: framing (WIDE, MEDIUM,
  CLOSE-UP or DETAIL), exactly what is on screen, and what the viewer should notice. E.g.
  "CLOSE-UP: a player spinning Bowser by the tail in Super Mario 64 and launching him toward a spike bomb."
  or "CLOSE-UP: a 1500s physician in a long robe examining a dancer's swollen feet; he looks baffled."
  The visual editor uses it to pick the real video clip or image, so describe something real footage
  or pictures from this topic's era and niche could show.
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
  scene. {AI_IMAGE_RULE}
  sound = a sound of the STORY itself on one spoken word, or null (the usual): {{"word": "jammed", "sound": "gun cock"}}
  (word = spoken in this scene; sound = 1-4 plain words naming a real recordable sound: "gun cock", "ship horn",
  "crowd gasp", "splash", "church bell", "typewriter"). At most 3 per Short, only for concrete moments where the
  sound makes the line land; never for abstract lines, never music.
  full = a FULL-SCREEN motion graphic that replaces this scene's picture, or null (the usual). Use it on at
  most 2 scenes, only where it shows the moment better than any picture or footage could: a trip between
  places, a number too big to picture, a document that matters, several people/things that connect, or a
  story-specific mechanism/diagram/cause-and-effect chain.
  Rules: never scene 1 (real footage hooks better), never two in a row, only on a scene of at least
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
    return next((p.get("extract") or "" for p in pages.values()), "")


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
Rewrite only the scenes that need it. Keep each about as long as it was (at most {channel_profiles.LONG_SCENE_WORDS} words) with the same role in the story, scene
1's first sentence at most 8 words, and every word a graphic or person card pops up on ("trigger")
when it is still correct. drop_graphic = true when that scene's graphic itself shows a wrong fact.
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
