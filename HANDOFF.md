# ShortsMaker: handoff for a new session

Read this first, then the code it points to. It says how things work **today** (rewritten 2026-10-28). The why
behind each rule, dated decisions, test runs and old designs are in `HANDOFF_history.md` (the full handoff as of
2026-10-28 is at its end): `grep -n "<word>" HANDOFF_history.md`. When you change something, update the section
here that describes it (current state, a line or two of why); put long stories in the history file.

## What this is
A faceless YouTube Shorts generator for **several channels** (profiles in `channels/`): `strange-history` (main,
"Plot Twist Archive"), `weird-economics`, `engineering-failures` (drawn in Blender) and `gaming` (rules drafted,
waiting for the owner). Goal: YouTube Partner Program monetization from a fresh account. The owner runs `run.bat`,
reviews each Short and **uploads manually** in YouTube Studio (no API uploads: an unaudited API project locks videos
to private). The owner is **not a programmer**: explain in plain words.

An AI plans everything (topics, script, fact check, SEO, picture choices, edit plan, review); the owner's PC renders
everything (voice, paintings, video). Real archival/online pictures and film are the main material; AI fills gaps.

## Owner's standing rules
- **Install everything on D:** (C: is nearly full).
- **Subscription access only: Google AI Pro and signed-in ChatGPT/Codex; Claude Pro currently has no credits.** No paid per-use APIs. Free keys allowed: Pixabay, vidIQ (chat use
  only), Freesound (`freesound_key.txt`). Never print a key. Ask before adding another. Sounds only from the
  Freesound API or the owner's own files (Pixabay forbids scraping).
- **No other creators' YouTube videos as footage** (YouTube cuts reach for re-uploads). Other sourcing is the owner's
  choice and stays open: all of Internet Archive, Openverse incl. Flickr/BY-SA/NC, all Wikimedia licences, each
  credited on screen and in `upload.txt`. Don't re-lock sourcing; don't build tools that disguise others' footage.
  Internet Archive re-uploads of YouTube videos are skipped (`archive_films()`); other creators' Archive uploads
  (Rooster Teeth, TV news) stay allowed (owner declined skipping them).
- **Topics are our own research**; bigger channels' Shorts are only a list of stories to avoid (see Pipeline 2).
- **Strategy advice needs evidence**: before recommending a change to what the Shorts say or how, look at other
  channels' successful Shorts (vidIQ transcripts, view counts), not only ours.
- **Don't narrow the niche**; **don't add logbook columns**.
- Gemini: **Argon (Gemini 4) at high effort when the account has it, else Flash, high effort.** Claude: Opus, high
  effort (the plan can't afford xhigh/max).
- Sound: no sub-bass thumps (SFX high-passed at 220 Hz), no loud repetitive whooshes, no "pop" punch-ins.
- **No 2.5D parallax** (it bent pictures). Stills get a plain zoom/pan.
- **Code map**: after every commit that changes code, refresh `code-map/` + `graphify-out/` as its own commit
  ("docs: refresh code map"); commands in Layout.
- **Blender work** (`blender/*.py`, engineering-failures only): load the Blender skills first (`blender-core`, then
  the one for the job). The Blender openers, people and model library were removed 2026-10-30 (owner: the drawn and
  motion-graphic openers are more consistent); `git log -- shortsmaker/opener_render.py` has them.
- Hardware: RTX 5060 8 GB, 32 GB RAM, Ryzen 7 5700X3D, Windows 11; Roblox, Wallpaper Engine, Discord and Chrome are
  often open (VRAM/RAM). Page file is only 2 GB.

## Layout (`D:\ShortsMaker`)
| Path | What |
|---|---|
| `run.bat` | Asks: channel (Enter = last), how many, who plans (1 Claude only, 2 Gemini only, 3 Claude [Gemini edits], 4 Gemini [Codex edits], 5 Both to compare), make AI clips yourself (Colab H3 / Flow, y/N), shorter Shorts (25-30 s test, y/N). Answers remembered in the profile. `make_shorts.py [count] [channel] [claude-only\|gemini-only\|claude\|gemini\|both]` skips them |
| `fix.bat` | `make_shorts.py fix`: re-render a recent Short (7 days) with one scene changed (see fix.bat) |
| `library.bat` | `make_shorts.py library`: approve or throw away looks/overlays/cuts the AI invented (`style_candidates/`) |
| `make_shorts.py` | Entry point only; the pipeline is `shortsmaker/` |
| `channels/<name>.json` | Profile: niche, audience, tone, voice, `done_topics`, `research_seeds`, `cta_line`, `brain`, `veo`, `short_form`, `recent_shapes`, `myths`. `<name>.research.json` = today's bigger-channel Shorts (the "taken" list); `last.txt` = default channel |
| `channels/<name>.rules.md` | The channel's rules, read by `##` heading (see Rules per channel) |
| `vault/` | Obsidian vault: `Logbook/<name>.md` (the owner's results log), `Shorts/<channel>/<folder>.md` (one page per Short, `vault_page()`), `Home.md`. `make_shorts.py notes` rebuilds the pages |
| `code-map/`, `graphify-out/` | graphify code map (second Obsidian vault + `graph.html`). Refresh: `C:\Python314\python.exe -m graphify update .`, delete `code-map\*.md` and `code-map\graph.canvas` (keep `.obsidian`), `C:\Python314\python.exe -m graphify export obsidian --dir code-map`. No auto hook (needs the owner's go-ahead) |
| `blender/` | Blender scripts (plain bpy, run headless by `D:\Blender\blender.exe` 5.2.1): engineering-failures drawings (`build_scene.py`, `look.py`, `parts.py`, `templates.py`, `failures.py`) |
| `drawn/` | Drawn openers: `kit.mjs` (the parts), `KIT.md` (the AI's manual), `run.mjs` (renders a scene: sheet or clip), `lib/` (claude-animation, MIT), `examples/` |
| `remotion/src/` | `Short.tsx`, `Graphics.tsx`, `Cards.tsx`, `Extras.tsx`, `MapCard.tsx`, `Captions.tsx`; `full/` = full-screen motion graphics; `style/` = style library (see those sections) |
| `remotion/test_props/` | Test scenes for full-screen graphics (+ `media/`); `tests/render_full.py` renders them into `test_renders/` |
| `local_ai/` | GPU worker `gen.py` (own venv: Kokoro, SDXL-Lightning, LTX-Video 0.9.8); voice worker `qwen_voice.py` (`qwen_venv`: Qwen3-TTS, MMS aligner, VoiceStudio client); models in `hf/` |
| `colab/` | `h3_clips.ipynb` + `h3_run.py` + `README.md`: AI video clips the owner makes on Colab Pro (gutierrezdishann@gmail.com, A100) |
| `music/<mood>/`, `sfx/`, `sfx/story/` | Music by mood (`.mp3.txt` = credit; somber is empty), synthesized SFX, story sounds (owner's files + CC0 Freesound) |
| `branding/` | Profile picture, banner, channel text |
| `cache/` | Downloads (30-day prune), `pools/` (a topic's pictures + AI picture list), `ideas/` (Wikipedia idea pages) |
| `output/<channel>/<date>_<slug>/` | `short.mp4`, `thumbnail.jpg`, `upload.txt`, `captions.srt`, `edit_plan.txt`, `storyboard.jpg`, `work/` (kept 7 days), `veo/` (clip hand-off), `edit.mlt` + `edit_in_shotcut.bat` (only when CHECK lines are left) |
| `docs/superpowers/` | Specs and plans of the bigger features (dated names) |
| `ffmpeg/` | FFmpeg build (put on PATH by `config.py`) |
| `backup/` | Old single-file versions from before git (history only) |

## Code layout (`shortsmaker/`)
Git repo (`master`, pushed to `origin/master` at github.com/ExodusNeo/shortsmaker).
Push every completed change set and its separate code-map refresh (owner, 2026-10-31).
Find any function with `grep -n "def <name>" shortsmaker/*.py`. Files
are stored LF (`.gitattributes`).

| Module | Job |
|---|---|
| `config.py` | Paths, fixed settings, palettes, style/skin tables; puts ffmpeg on PATH |
| `session.py` | Run state: `BRAIN`, `SOLO`, `PARTNER`, `NO_QUOTA`, `LAST_AI`, `CHANNEL`/`RESEARCH`/`LOG`, `RULES`/`RULE_SETTINGS`, `SHORT_FORM`, `VEO_HANDOFF` |
| `llm.py` | `ask_ai()`, `run_agy()`, quota detection, model pick |
| `channel_profiles.py` | Profiles, run.bat menus, `trend_research()` (the taken list) |
| `topic_ideas.py` | Our own story ideas from Wikipedia's Unusual articles pages; `clash()` |
| `rules.py` | Reads/checks `channels/<name>.rules.md`; drafts rules for new profiles |
| `writing.py` | Topics -> research -> writer -> editor -> director -> fact check (`write_scripts()`) |
| `plan_rules.py` | Cleaning the planner's JSON, word timings, full-scene cues |
| `seo.py` | `seo_pass()`, autocomplete, `srt()` |
| `image_sources.py`, `footage.py` | Pictures (Wikimedia, Openverse, NASA, Archive) and film clips; licences and credits |
| `picture_pool.py` | Pictures-first pool, AI picture list, cache pruning, contact sheets |
| `picker.py` | `choose_images()`, full-scene pictures, rescue graphics, `opener_graphic()` |
| `photo_prep.py` | Stereo cards, border trimming, vertical crops |
| `audio_mix.py` | Voice call, captions, SFX, story sounds, music gain |
| `gpu.py` | MOSS (ComfyUI), VoiceStudio, Gemini paintings, LTX clips, Colab/Flow clip hand-off |
| `frame_render.py` | Python renderer (fallback), thumbnail |
| `remotion_render.py` | `render_remotion()`, fallback, redraws |
| `motion.py` | Full-scene props, AI-coded custom scenes, `custom_rules()`, `look_and_fix()` |
| `style_lab.py` | Style library inventions and candidates |
| `review.py` | Quality check, visual review, first-second check, review fixes, repaints, storyboard |
| `editplan.py` | `edit_plan()`, `scene_cues()` (graphic timing) |
| `short_render.py` | `render()`, work state, `use_opener()` |
| `drawn_opener.py` | Drawn opener: AI scene code, lint, preview, art-director review and fixes, render |
| `blender_plan.py`, `blender_render.py` | Blender-drawn channels: build plans, headless render |
| `edit_project.py` | Shotcut timeline for hand fixes |
| `logbook.py` | Logbook entries, vault pages |
| `cli.py` | `main()`, `fix_short()`, `fix` / `library` / `notes` |
| `media_tools.py` | `fetch()`, `ffmpeg()`, `video_encoder()`, `duration()`, `write_json()` |

Rules that keep it working:
- Use another module's function through its module (`llm.ask_ai(...)`), never `from x import f` (test fakes and the
  quota switch are set on the module). Only fixed `config` names are imported by name.
- Tests swap fakes on the owning module; by name via `tests/patching.py`'s `owner(name)`.
- Don't name variables after modules (`pool`, `plan`, `audio`).
- Pipeline `claude -p` calls run lean (`--setting-sources project,local --disable-slash-commands`): skills never reach
  the pipeline. Whatever a skill teaches has to live in the prompts or code.

## Pipeline (`main()` -> `write_scripts()` -> `seo_pass()` -> `render()` per Short)
1. **AI calls** go through `ask_ai()`. Planner = `BRAIN`. Solo modes (1, 2) use one AI except for the independent cold read; a bad answer is
   retried by the same AI, and only running out of quota hands the rest of the run to the other one (`NO_QUOTA`).
   Gemini modes (2, 4) pair with Codex (ChatGPT subscription), never Claude. Mode 2 keeps Gemini as editor;
   mode 4 uses Codex as editor. Explicit Claude modes retain the Claude/Gemini pair. `configure_brain()` also
   applies this in fix.bat; `llm.other_ai()` selects the partner for all fallbacks, including picture catalogs.
   The cold read alone sets `allow_fallback=True`, so it can try both AIs even in solo mode.
   Collaborative modes (3, 4): the partner edits the scripts. "Both" makes each topic twice (folders end
   `-claude`/`-gemini`; post the better one). Codex: `codex exec --model gpt-6-astra`, high effort, ChatGPT login enforced, API-key environment variables
   removed for the child, read-only sandbox, shell tools disabled, no user config or project instructions, ephemeral
   sessions; prompts via stdin and review images attached directly. Claude: `--model opus --effort high`. Gemini via Antigravity's `agy`
   (Google login, no key; prompt in a task file; `--disable-slash-commands`, no shell/tools for review calls;
   timeouts 300 s review / 180 s text): Argon if listed, Flash on `RESOURCE_EXHAUSTED` or a timeout for the rest of
   the run; bulk picture jobs (`catalog_pool`, `choose_images`) always Flash. agy can't make video.
2. **Topics, our own research** (`topic_ideas.py`): ~60 random ideas from Wikipedia's "Unusual articles" pages
   (`idea_pages: History; Military` in Settings, else 10 default pages; cached 30 days in `cache/ideas/`), none in
   `done_topics` or on the taken list, go to the topic picker with the logbook results and the `myths` list.
   `trend_research()` (bigger channels' recent Shorts, yt-dlp, daily cache) is ONLY the "TAKEN" list: the picker must
   not pick those, and a picked topic whose subject/character holds every real word of a taken title
   (`topic_ideas.clash`, 2+ words) is dropped for a backup, and so is one whose main character (else subject) clashes
   with our own `done_topics`. The writer and SEO never see competitor titles. Every
   Short needs a main `character` (soft rule: one named person or animal; events told through them). Each topic
   comes with a pitch (`fact8`, `question`, `payoff`, `fame` 1-3; edit_plan "Topic pitch" line): `fame` 3 (told
   everywhere) is skipped for a backup; a pitch the picker left out keeps its topic.
3. **Pictures first**: the picker gives n + 2 backup topics with `visual_terms` and `people`; `prepare_topic()` reads
   Wikipedia, gathers the pool (`gather_pool()`), has the AI list every picture (`catalog_pool()`: what, era_ok,
   sharp, hook, reject) and keeps topics with >= `min_real_pictures` usable (frames of one video count once); weak
   topics are skipped (`dropped_topics`). No picture list from either AI = the run stops. Then `check_twists()`: each
   twist against Wikipedia (a legend becomes "the story says X; in fact Y").
4. **Script team**: the planner writes narration -> the editor (`edit_scripts()`: hooks, read-aloud fixes, cuts) ->
   the cold reader (`cold_read()`, the partner AI with planner fallback, including solo modes; one call per batch:
   sees only the final scenes and reports the
   question line 1 opens, the scene that answers it, `new` per scene, list_like, first swipe scene, hook_kind; the
   editor no longer supplies its own grades) -> `story_problems()` sends a failing script back once (answer before the
   last two scenes, no question, 2+ scenes with nothing new, swipe in scenes 1-4, list, summary hook, plus the text
   rules); edit_plan "Cold read" line (including the AI that actually answered) -> the director
   (`direct_scripts()`, can't change narration: per scene `pic`, image/video search, shot, move, graphic, person,
   emphasis, transition, `ai_image`, animate/motion, sound, optional `full`; per Short palette, music mood, look,
   thumbnail, SEO drafts) -> fact check against the Wikipedia text (rewrites unsupported lines, drops wrong graphics,
   myths go to the profile). When the fact check rewrote lines, the text rules (`story_problems` without a cold
   read) and the word total are checked again; leftovers are `STILL (after the fact check):` notes.
   Lengths: 95-125 words in 11-16 scenes (~40-50 s), or `SHORT_FORM` 60-72 words in 8-10: `writing.length_plan()` is
   the only length target (the strange-history rules file no longer repeats one; weird-economics' rules still say
   110-135); `writing.max_seconds()` is quality_check's limit. Scenes of 4-10 words
   (`SCENE_WORDS`), up to 16 where one picture needs time; sentences may run across cuts (`SCENE_CUTS`), but the first
   sentence ends by scene 2 (checked). `plan_rules.first_sentence()` reads it across the cut for the logbook, the
   first-second check and SEO. The hook opens inside the strangest moment; story rules (but / so / you see, answer
   last) live in each rules file.
5. **SEO** (`seo_pass()`): YouTube autocomplete for the subject + variants + `search_terms` + profile seeds, the logbook
   results and the fact check's corrections. Title < 60 chars, first 40 work alone, no emoji, never repeats the hook.
   Then description, tags, pinned comment. Title/hashtag/pinned-comment examples come from the channel's optional
   `## SEO` rules section (the prompt in `seo.py` holds no niche's examples).
6. **Pictures** (`choose_images()`): keeps each director `pic` unless it doesn't fit; new searches only for scenes
   without one and for portraits. The AI looks at numbered contact sheets; rejects violence, logos/watermarks,
   look-alikes from another culture or era; one solo portrait of a person per Short; portraits never under that
   person's own card. Scenes with nothing fitting go to `rescue_graphics()` (full-screen graphic) or a painting.
7. **Media**: voice = **CosyVoice 3 through VoiceStudio** (`D:\VoiceStudio`, backend 127.0.0.1:3900, started by
   `voicestudio_up()`), cloned Mark Nelson (`local_ai/voices/nelson_ref.wav` with `aiden_ref.wav` fallback; brisk
   investigative storyteller, CC0/PD), story-arc delivery (`cosy_instruct`: urgent hook -> suspenseful middle -> punchline payoff),
   tempo `COSY_SPEED` (1.10 in `gpu.py`, brisk ~2.8 wps base pace with zero audio stretching); each sentence run is one take (`sentence_groups()`), cut per scene by MMS word alignment. Backups in order:
   Qwen3-TTS (aiden), Kokoro, Edge, never mixed in one Short. Paintings: **MOSS-Image** (ComfyUI `D:\ComfyUI`), then
   Gemini, then SDXL. Paintings may show only words quoted in `ai_image`; a hand-made period medium, never "concept
   art"/"cinematic". Real stills -> `clean_photo()` -> 9:16 cover; film -> `FILM_CROP` + `FILM_VF` band. AI video
   (`animate`, max 5): the owner's Colab H3 / Flow clips if chosen (start pictures checked first,
   `start_picture_problems()`), else LTX. Motion only for what the picture shows.
8. **Render**: Remotion when there are >= 3 graphics, any look/special cut, or any full-screen scene; else the Python
   renderer. Graphic styles: date, place (map), fact, stat, timeline, mark, headline, quote, compare, stamp, question,
   kinetic; card overlays hold >= 1.8 s and start early when their word comes late (`editplan.py`); person cards pop
   on the spoken name. Palettes (9) drive all graphics and map to a full-scene skin. Credit tag bottom-left
   (`short_credit()`), 2.8 s. Loop Shorts (weird-economics) end straight into frame 0.
9. **Audio**: voice + music (loudness-matched to `MUSIC_LUFS`, ducked) + SFX cue sheet + story sounds; loudnorm
   -14 LUFS + limiter; h264_nvenc.
10. **Checks and fixes**: `quality_check()` (also flags a scene that reuses another scene's picture because nothing
    fit, and narration pauses over `PAUSE_MAX` 0.8 s in `work/voice.wav`), `visual_review()` (1 frame/s sheets; told
    about overlay windows; also notes, as CHECK lines without a fix, a weak reveal visual, 5+ s with nothing new and
    crowded scenes), `first_second_check()` (every score goes in edit_plan.txt's quality block; score < 7 may swap in
    a later real picture once; an opener is judged as what it is, never swapped). Flagged scenes get an unused pool
    picture, a full-screen graphic or a repaint with a rewritten prompt (`rewrite_paint_prompts()`); a flagged custom
    scene goes back to its coder once. Re-render and re-review up to `AUTO_FIX_ROUNDS` (3); it pauses for Enter first.
    Left-over findings are `CHECK:` lines in edit_plan.txt (and a Shotcut timeline).
11. **Outputs**: edit_plan.txt (Opening line, fact-check changes, per-scene edit list, sound cues, checks),
    upload.txt (credits for every non-PD source and CC-BY 3D model; "altered or synthetic content: Yes" when AI was
    used), storyboard, thumbnail, captions.srt, logbook entry, vault page, `work/state.json` for fix.bat.

## Openers (scene 1 of every Short on `opener: animated` channels)
Order (owner, 2026-10-30): drawn opener -> motion graphic (2 fixes) -> AI clip of the strangest moment (`use_opener`).
- **Drawn opener** (`drawn_opener.make_opener`, `drawn/`): a hand-drawn brush-ink + watercolour animation of the
  strangest moment, scene 1 + the crossfade long. The AI codes one scene module against the kit (`drawn/kit.mjs`; its
  manual `drawn/KIT.md`, with the approved Dexter example) -> lint (only `k.*` calls and plain JS; node runs with
  `--disallow-code-generation-from-strings`: the coder has read Wikipedia text) -> a 6-frame preview sheet ->
  the AI as art director, who scores it 1-10 (passes at `PASS` 7; a bare list of flaws rejected every draft on the
  first live runs, good ones included; no verdict = the draft is kept with `unreviewed` and a CHECK line says nobody
  judged it) -> below 7 the coder fixes what it found, up to `FIXES` (2) times -> `drawn/run.mjs` renders
  `work/drawn/opener.mp4`. The plan stays in `short["drawn"]` (fix rounds and fix.bat reuse the clip by
  fingerprint); a failure stays in `short["drawn_failed"]` and is never retried for that Short. Final-review findings
  on a drawn opener stay CHECK lines (it passed its own art director). The channel's optional `## Opener` rules
  replace `DEFAULT_RULES`. Library: claude-animation (MIT), vendored in `drawn/lib` (`VERSION` = the upstream commit);
  install once: `cd drawn && npm install`. Adding a kit part: write it in `kit.mjs`, document it in `KIT.md`, add it
  to `drawn/examples/kit_parts.mjs`, run `tests\test_drawn_opener.py --look` and look at `drawn\out\sheet.png`.
  Look lessons: the library's over-mode wash lays paper grain on top and greys colours (`k.paint` = solid, then a
  thin multiplied wash); multiplied washes over the teal sea turn brown into green.
- **Motion-graphic opener** (`picker.opener_graphic`, planned in `render` for every Short on these channels; Opening
  line `motion graphic: ...`). It goes first and is judged on every render (owner, 2026-10-30): the visual review's
  scene-1 finding or a first-second score < 7 makes it weak (`review.weak_opener_graphic`), and the fix rounds fix it
  `OPENER_GRAPHIC_FIXES` (2) times (`review.fix_opener_graphic`: a custom one is redrawn, any other picked again
  with the complaint). Still weak after that on "make AI clips yourself" runs -> scene 1 goes into the owner's clip
  hand-off as the strangest moment (`opener_clip`, 3rd fix round); a skipped one is made by LTX; whichever clip
  comes back plays instead of the graphic (`use_opener`, Opening line `AI clip of the strangest moment (made by ...)
  (the motion graphic still looked weak after 2 fixes: ...)`). Without the hand-off it stays a CHECK line. Only a
  Short with no graphic at all hands scene 1 off on the first render. The hand-off sends close-ups too.

- Scene 1's clip starts from a painting of the strangest moment (`review.paint_opener_start` ->
  `work/opener_start.jpg`, `gpu.start_picture`; same painters and `AI paintings` rules), not scene 1's own picture:
  the Dexter Short (2026-10-30) sent Flow the woodcut of Dexter walking, so the clip couldn't show the bed warmers.
## Full-screen motion graphics (`remotion/src/full/`)
- 4 skins (`parchment`, `blueprint`, `dossier`, `hud`) chosen from the palette/mood (`short_skin()`).
- Templates: map `journey`, big `number` (counter + figures, painted silhouette or icons, or `compare` bars),
  evidence `board` (3-5 real photos), `document` (only the key line readable, underlined as spoken).
- `custom` (diagram / collage / flow / clock): the AI codes a React scene per Short (`code_custom_scenes()`) from the
  guarded toolkit (`guarded.tsx`: never-overlapping layouts, arrow router, fitted cards, `MIN_MOVE` 0.9 s); lint +
  `tsc` (one repair) + a small preview the coder fixes once (`look_and_fix()`); fallback scene if it still fails.
  The owner wants these varied, not bland: they declined turning custom scenes into fixed templates. Rule 9
  "TASTE" in `custom_rules()` mirrors the repo's `.claude/skills/motion-design` (from claude-motion, MIT): keep the
  two in step.
- Max planned per Short: 2 (`max_full_planned`), total 3 (`max_full`), never scene 1 (except the opener graphic),
  never adjacent, a scene of >= 8 words (6 on channels that raise `max_full`, e.g. weird-economics: 4/5);
  one `document` per Short. Last beat 1.6 s before the cut (`FULL_SETTLE`).
- `TitleBanner` is screen-locked; stage objects sit between the title (y 74-170) and the captions (y 1170-1300).

## Style library (`remotion/src/style/`)
The director picks the Short's `look` (halftone, engraving, riso, miniature, silent) or invents one, each scene's
transition (cut, fade, flash, wipe, whip, leak) and overlays (question, kinetic). Caps (`STYLE_CAPS`): clean hook,
no look on film or AI clips, max 1 question / 2 kinetic / 4 look scenes / 3 special cuts; `recent_looks` blocks
repeats. Inventions are linted, compile-checked and previewed; failures fall back to a library entry and finished
ones wait in `library.bat`. The invention path has never run in a real Short.

## Rules per channel (`channels/<name>.rules.md`)
Read by `##` heading: `Settings` (`status: draft|ready`, `visuals: photos|blender`, `min_real_pictures`,
`max_full_planned`, `max_full`, `opener: animated|none`, `hook: moment|money_claim`, `idea_pages`), `Topic picking`,
`Story rules`, `Writing for the picture`, `Lessons from our numbers`, `Opening picture` (must define `- era_ok:`,
`- sharp:`, `- hook:`), `Picture picking`, `Directing`, `First-second check`, `AI paintings`,
`Build plan` (Blender channels); optional: `Opener`, `SEO`. A missing section or `status: draft` stops the run;
never another channel's rules.
A new profile gets drafted rules (`rules.draft_rules()`) and waits for the owner to set `status: ready`.
`tests/golden/prompts.json` holds strange-history's prompts; re-save (`tests\test_rules.py --save-golden`) only for
an intended prompt change, and diff it per prompt first.

## Blender-drawn channels (`visuals: blender`, engineering-failures)
Every scene is a 3D "ink manual" drawing of a bridge failure (truss, girder, suspension, cable-stayed, eyebar chain;
crack / bend / shear / sway, optionally collapse). The engineer step (`blender_plan.plan_builds`) writes a checked
build plan; `blender_render.render_clips` runs `blender/build_scene.py` headless (~0.3 s a frame) and the scenes play
like film with hard cuts. Thumbnail = one archival photo of the real structure. No pictures, paintings, graphics or
person cards; review findings stay CHECK lines; fix.bat can't change these Shorts.

## fix.bat
Pick a recent Short (7 days), a scene, then: 1) no AI motion, 2) another scene's picture, 3) remove its graphic,
4) paint a new picture (asks what's wrong; rewrites the prompt), 5) make it a motion graphic. Reuses pictures,
music and palette; re-makes voice and video (a few minutes); no automatic fix rounds; logbook untouched.

## Shotcut timeline
When CHECK lines are left after the last fix round, the Short's folder gets `edit.mlt` + `edit_in_shotcut.bat`
(Shotcut portable in `D:\Shotcut`, settings in `D:\Shotcut\appdata`): pictures, graphics (with alpha) and captions as
separate tracks cut per scene, voice/music/sounds as 3 audio tracks, a gain + limiter for -14 LUFS, a red marker per
CHECK. `work/` is pruned after 7 days, which breaks the timeline too. Not yet used on a real Short.

## Logbook (`vault/Logbook/<channel>.md`)
One entry per Short; the owner's YouTube Studio numbers (Views, Comments, Subscribers gained, Stayed to watch,
Average % viewed, likes, a note). When the owner names a channel, read Studio with Claude in Chrome (already logged
in; Content -> Shorts and each Short's Analytics; exact % viewed and likes from the Analytics overview's "Latest
content" card by zoomed screenshot) and fill it without asking. Entries under 100 views are marked "Too few views to
judge". Filled entries feed the topic picker, writer and SEO. Channel id UCMVMdmkpRb1a7EjBaSOQ4cQ; video IDs and the
read procedure in detail: `HANDOFF_history.md` "Logbook".

What the numbers say so far (strange-history): views stall around 1,000-1,350; character-led stories get pushed,
hoax/group/thing stories flop; most viewers leave in the first second or 4-12 s in; the hits open inside the
strangest moment. Same story, other channel: Voggle's Mike 2M views vs ours 1.2K.

## Hard-won lessons
- Wikimedia serves only thumbnail widths 330/500/960/1280/1920 (use `thumb_url()`); other sizes get 429 Retry-After
  600. Never wait > 30 s. `WM_UA` carries the owner's email (approved, Wikimedia only).
- LTX on 8 GB: two-stage load, fp8 layerwise casting. Wan 2.2 rejected (~50 min per 2 s clip).
- agy: the prompt goes inline in `-p=`; no `--mode auto`; Argon's quota is weekly, keep it for text.
- Remotion: `--gl=angle --concurrency=4`; never render tests while a batch runs (shared `remotion/public/job`).
- Edge TTS 403: `uv pip install -U edge-tts --python .venv\Scripts\python.exe`. Qwen voice: load the local snapshot
  folder (the Hub call fails offline); qwen-tts pins transformers 4.57.3 (keep it out of gen.py's venv).
- PowerShell-written JSON has a BOM: read profiles with utf-8-sig.
- MOSS's seed comes from the prompt text: an unchanged prompt repaints the identical picture.
- A .tsx with JSX at module level needs `import React from 'react'`.
- Blender 5.2: no video output (render PNG, join with ffmpeg); `matrix_world` is stale until a depsgraph update.
- The automatic review reliably catches burned-in subtitles, watermarks, wrong eras and blank frames.
- How Shorts get pushed: a seed audience first, then wider or stop; never delete and re-upload a flop. Since
  2026-08-24 a view counts from the first frame, so "Stayed to watch" is the hook signal. Monetization (reported):
  1,000 subs + 10M Shorts views in 90 days; 20M from 2027-02-01.

## Open items and next steps
- **Audit improvements (2026-10-31)**: Parts 1 and 2.1/2.3-2.5 were already on master and pushed at
  `beaae733`; the previous branch/wait notes were stale. This continuation implements 2.2 with Codex + Gemini
  (owner has no Claude credits), leaving the selected editor unchanged in solo mode. No Part 3 changes yet.
  Plan: `docs/superpowers/plans/2026-10-31-audit-improvements.md` (git-ignored on purpose).
  Malformed cold reads now count as no review; a failed second read removes the old draft's verdict. A failed
  opener preview also clears the old render's score. A live Codex cold read passed. Still to verify: a complete live Short with these changes.
  Separate open question: weird-economics' 110-135 words vs the code's 95-125.
- **Openers**: the drawn opener has only run on past Shorts (`test_renders\drawn_samples\`), not inside a full run;
  the motion-graphic fix rounds have no live run yet. More kit parts as stories need them.
- run.bat's "press any key" at the end doesn't close the window for the owner: not found in the code; waiting for
  the window's last line.
- Never seen in a real run: style inventions, question beats, wipes, the Shotcut timeline.
- `channels/gaming.rules.md` is drafted and waiting for the owner's review.
- `FILM_CROP` (cuts film edges, made for other creators' captions): removing it was offered; owner hasn't decided.

## Ideas offered, not built
- Voice cloning of the owner, SFX on the music's beat, YouTube Audio Library tracks for somber/epic.
- Rejected: logbook extras (noise), MoneyPrinterTurbo, AutoSocial, kie.ai, Wan 2.2, browser-automating Google
  Flow/Gemini (account ToS risk), Hyper3D Rodin's shared trial key, Hunyuan3D 2.1 (licence excludes EU/UK/KR).

## How to verify changes
- `.venv\Scripts\python.exe -m compileall -q make_shorts.py shortsmaker`; Remotion: `cd remotion && npx tsc -p .`
- Tests, no AI usage (`.venv\Scripts\python.exe tests\<name>.py`): `test_package`, `test_codex`, `test_pictures_first`,
  `test_full_scenes`, `test_style`, `test_rules` (golden prompts), `test_story`, `test_first_second`,
  `test_topic_ideas`, `test_h3_handoff`, `test_h3_run`, `test_edit_project`, `test_blender_plan`,
  `test_blender_render`, `test_opener_graphic`, `test_drawn_opener` (real node, ~1 min);
  `tests\run_ts_tests.py` (TypeScript); `local_ai\qwen_venv\Scripts\python.exe tests\test_qwen_voice.py`.
- With real headless Blender (engineering-failures): `test_blender_run`, `test_blender_scene`.
- One full-screen scene: `tests\render_full.py remotion\test_props\<name>.json [--still SECONDS]`.
- Prompt changes without AI usage: fake `llm.ask_ai` (and `writing.article_text`, `channel_profiles.trend_research`,
  `topic_ideas.pick_ideas`) and read the captured prompts. Single steps: in a scratch script call
  `channel_profiles.use_channel("<name>")` first, then the function.
- Full run: `.venv\Scripts\python.exe -u make_shorts.py 1 strange-history gemini`, then a 1 frame/s sheet
  (`ffmpeg -i short.mp4 -vf "fps=1,scale=180:-1,tile=11x5" -frames:v 1 sheet.jpg`) and edit_plan.txt's CHECK lines.
