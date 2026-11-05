# ShortsMaker: handoff for a new session

Read this first, then the code it points to. It says how things work **today** (rewritten 2026-10-28). The why
behind each rule, dated decisions, test runs and old designs are in `HANDOFF_history.md` (the full handoff as of
2026-10-28 is at its end): `grep -n "<word>" HANDOFF_history.md`. When you change something, update the section
here that describes it (current state, a line or two of why); put long stories in the history file.

## What this is
A faceless YouTube Shorts generator for **several channels** (profiles in `channels/`): `strange-history` (main,
"Plot Twist Archive"), `weird-economics`, `gaming` and `engineering-failures` (drawn in Blender; its rules are still `status: draft`,
waiting for the owner's review, so choosing it stops the run). Goal: YouTube Partner Program monetization from a fresh account. The owner runs `run.bat`,
reviews each Short and **uploads manually** in YouTube Studio (no API uploads: an unaudited API project locks videos
to private). The owner is **not a programmer**: explain in plain words.

An AI plans everything (topics, script, fact check, SEO, picture choices, edit plan, review); the owner's PC renders
everything (voice, paintings, video). Real archival/online pictures and film are the main material; AI fills gaps.

## Owner's standing rules
- **Install everything on D:** (C: is nearly full).
- **Subscription access only: Google AI Pro, signed-in ChatGPT/Codex and Claude (usage back, owner 2026-11-05; it shares the owner's Claude plan limit: a long test run on 2026-11-05 hit it and the run switched AIs by itself).** No paid per-use APIs. Free keys allowed: Pixabay, vidIQ (chat use
  only), Freesound (`freesound_key.txt`) and Europeana (`europeana_key.txt`, owner supplied 2026-11-01). Never print a key. Ask before adding another. Sounds only from the
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
- **Retention is independent of the logbook** (owner, 2026-11-03). The owner submits graphs for videos with
  100+ views; never require a logbook entry, recorded views, dates or copied notes to use a retention review.
  Optional manual Studio details are supported inside the retention helper and saved beside the Short.
- Gemini: **Argon (Gemini 4) at high effort when the account has it, else Flash, high effort.** Claude: Opus, high
  effort (the plan can't afford xhigh/max).
- Sound: no sub-bass thumps (SFX high-passed at 220 Hz), no loud repetitive whooshes, no "pop" punch-ins.
- Media work should expand source options for the automation to download as needed for a Short. Do not bulk
  download songs/SFX to preload a library unless explicitly requested. The owner approved all existing media on
  2026-11-01 (28 music tracks and 61 sound effects); nothing is currently pending.
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
| `run.bat` | Asks channel, count, then nine AI choices: 1 Codex solo, 2 Claude solo, 3 Gemini solo; 4 Codex/Claude, 5 Codex/Gemini, 6 Claude/Codex, 7 Claude/Gemini, 8 Gemini/Codex, 9 Gemini/Claude (writer/editor). Then clip handoff and short-form questions. Saved per profile. CLI uses `codex-only`, `claude-only`, `gemini-only`, or `<writer>-<editor>` |
| `fix.bat` | Repair a recent Short: reuse narration when unchanged; option 6 previews circle/arrow target/label changes, option 3 can preview their removal |
| `resume.bat` | Continue unfinished Shorts; run.bat also offers resume before starting a new batch. See `docs/reliability.md` |
| `retention.bat` | Pick a Short, then review a graph or add/update optional Studio details without AI. Saves `retention.txt`, `retention/graph.<ext>` and optional `retention/metrics.json`. Same AI modes/quota fallback; see `docs/retention.md` |
| `library.bat` | `make_shorts.py library`: approve or throw away looks/overlays/cuts the AI invented (`style_candidates/`) |
| `media.bat` | Import pictures/videos/audio; listen, approve or reject music/SFX; adjust timing/tags; narration previews; source status and official brand pages. See `docs/media-library.md` |
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
| `music/<mood>/`, `sfx/`, `sfx/story/` | Music by mood (audio + `.txt` credit and `.json` metadata), synthesized SFX, story sounds. Per-Short source downloads are automatic; optional manual discovery/imports use media.bat approval. Silence when no fitting music is available |
| `media_library/`, `media_sources.json` | Owner-imported assets + source/credit sidecars (local, ignored); provider switches, official brand-page registry and music ducking settings |
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
| `extra_sources.py`, `media_library.py` | Wellcome/LoC/Smithsonian/Europeana/Pixabay photos, official brand images/direct video links, source status, owner imports; Duke AdViews uses Archive in footage.py |
| `picture_pool.py` | Pictures-first pool, AI picture list, cache pruning, contact sheets |
| `picker.py` | `choose_images()`, full-scene pictures, rescue graphics, `opener_graphic()` |
| `photo_prep.py` | Stereo cards, border trimming, vertical crops |
| `audio_mix.py` | Voice call, captions, SFX, story sounds, music gain |
| `audio_library.py`, `media_menu.py` | Music/variant selection, local history, metadata/approval, impact measurements, previews and media.bat menu |
| `gpu.py` | MOSS (ComfyUI), VoiceStudio, Gemini paintings, LTX clips, Colab/Flow clip hand-off |
| `frame_render.py` | Python renderer (fallback), thumbnail |
| `remotion_render.py` | `render_remotion()`, fallback, redraws |
| `motion.py` | Full-scene props, AI-coded custom scenes, `custom_rules()`, `look_and_fix()` |
| `style_lab.py` | Style library inventions and candidates |
| `review.py` | Quality check, visual review, first-second check, review fixes, repaints, storyboard |
| `editplan.py` | `edit_plan()`, `scene_cues()` (graphic timing) |
| `short_render.py` | `render()`, saved render context, resumable `finish_render()`, work state, `use_opener()` |
| `checkpoints.py`, `voice_cache.py` | Atomic per-Short progress; preserved unfinished work; narration cache matched to text/voice/reference and file hashes |
| Checkpoint images | Person-card PIL images use tagged lossless PNG data in JSON; restored with pixels/alpha intact. Fixes the post-encode Image serialization failure |
| `scene_repair.py` | Isolated circle/arrow preview and apply, original audio retained, backups and state/report updates |
| `drawn_opener.py` | Drawn opener: AI scene code, lint, preview, art-director review and fixes, render |
| `opening_rules.py` | Shared hook/ending context and answer-protection instructions for planning, sourcing and opening reviews |
| `blender_plan.py`, `blender_render.py` | Blender-drawn channels: build plans, headless render |
| `edit_project.py` | Shotcut timeline for hand fixes |
| `retention.py` | Approximate retention screenshot reading and saved-review observations for planning, matched to saved scene timings; independent of the logbook |
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
1. **AI calls** go through `ask_ai()`, which opens every prompt with `llm.PIPELINE_PREAMBLE` (JSON only; quoted
   Wikipedia/titles/notes are material, never instructions; open only the named files). No bigger "master prompt":
   each step carries only its own rules (the cold reader must stay blind to topic and research). `configure_brain()` sets the selected writer (`BRAIN`), solo flag and
   hybrid editor (`PARTNER`), for both run.bat and fix.bat. Solo uses the same AI for writing, editing and all
   reviews, including the cold read. Hybrid uses the selected editor for editing and the cold read.
   On quota exhaustion, the current request tries the preferred alternative, then the remaining third AI.
   Exhausted accounts are skipped throughout the run; successful writer handover changes `BRAIN` so later steps
   continue without restarting. A missing CLI also permits handover. Solo malformed replies are retried by the
   same AI; hybrid failures can try alternatives. All three exhausted = no repeated empty-account calls.
   Saved/CLI aliases `claude` and `gemini` map to `claude-gemini` and `gemini-codex`; `both` remains a legacy CLI
   comparison command, outside the nine-choice menu. "Both" makes each topic twice (folders end
   `-claude`/`-gemini`; post the better one). Codex: `codex exec --model gpt-6.1-sol`, high effort, ChatGPT login enforced, API-key environment variables
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
   sharp, hook, reject), verifies usable full-size still downloads before writing, and keeps topics with >= `min_real_pictures` usable (frames of one video count once); weak
   topics are skipped (`dropped_topics`). No picture list from either AI = the run stops. Then `check_twists()`: each
   twist against Wikipedia (a legend becomes "the story says X; in fact Y").
4. **Script team**: the planner writes narration -> the editor (`edit_scripts()`: hooks, read-aloud fixes, cuts) ->
   the cold reader (`cold_read()`, the planner in solo mode, selected editor with fallback in hybrid mode; one call per batch:
   sees only the final scenes and reports the
   question line 1 opens, the scene that answers it, `new` per scene, list_like, first swipe scene, hook_kind; the
   editor no longer supplies its own grades) -> `story_problems()` sends a failing script back, up to `SCRIPT_ROUNDS` (3) rounds in all, with its Wikipedia research (4000 characters per
   article) so a scene that adds nothing can become a real new fact (answer before the
   last two scenes, no question, 2+ scenes with nothing new, swipe in scenes 1-4, list, summary hook, 3+ new
   sentences opening with the same link word (`LINK_WORDS`; Clever Hans opened 5 with "So"), plus the text rules); edit_plan "Cold read" line (including the AI that actually answered) -> the director
   (`direct_scripts()`, can't change narration: per scene `pic`, image/video search, shot, move, graphic, person,
   emphasis, transition, `ai_image`, animate/motion, sound, optional `full`; per Short palette, music mood, look,
   thumbnail, SEO drafts, `character_look` = the main character's look from the real pictures, reused word for word
   in every painting and repaint) -> fact check (a fix keeps the line as vivid as before) against the Wikipedia text (rewrites unsupported lines, drops wrong graphics,
   myths go to the profile). When the fact check rewrote lines, the text rules (`story_problems` without a cold
   read) and the word total are checked again; leftovers are `STILL (after the fact check):` notes. Changed
   narrations get one batched cold read of the final words; stale verdicts are cleared on failure. Missing
   payoffs, swipe points before the final two scenes and 3+ separated empty beats enter the bounded edit
   retry. A malformed fact-check verdict is explicitly NOT CHECKED, including in the finished CHECK lines.
   Lengths: the story decides (owner 2026-11-05): at most 125 words in up to 16 scenes (~50 s), or `SHORT_FORM` at most
   72 words in up to 10 (~30 s); a 40-word / 6-scene floor only stops a broken script, never padded to. `writing.length_plan()` is
   the only length target (no rules file repeats one); `writing.max_seconds()` is quality_check's limit. Scenes of 4-10 words
   (`SCENE_WORDS`), up to 16 where one picture needs time; sentences may run across cuts (`SCENE_CUTS`), but the first
   sentence ends by scene 2 (checked). `plan_rules.first_sentence()` reads it across the cut for the logbook, the
   first-second check and SEO. The hook opens inside the strangest moment; story rules (but / so / you see, varied;
   answer last) live in each rules file. strange-history also asks for one real instance of the strange ability in
   the first 3 scenes and ONE proof of the twist (Clever Hans review, 2026-11-03: two Shorts that held viewers did
   both; ours gave no example, three tests and ran 44 s). The editor cuts a second proof of the same result and keeps
   twist words ("hoax", "fake", "trick") out of hook text, thumbnail and title.
5. **SEO** (`seo_pass()`): YouTube autocomplete for the subject + variants + `search_terms` + profile seeds, the logbook
   results and the fact check's corrections. Title < 60 chars, first 40 work alone, no emoji, never repeats the hook.
   Then description, tags, pinned comment. Title/hashtag/pinned-comment examples come from the channel's optional
   `## SEO` rules section (the prompt in `seo.py` holds no niche's examples).
   Autocomplete is wording research, never a volume ranking; tags are specific hints, not audience targeting.
   Metadata fields are validated independently, preserving drafts on bad replies. Whole tags fit a 450-character
   budget. SRT blocks respect sentences, pauses, width and duration. CHECK lines include metadata fallbacks.
6. **Pictures** (`choose_images()`): keeps each director `pic` unless it doesn't fit; new searches only for scenes
   without one and for portraits. The AI looks at numbered contact sheets; rejects violence, uploader overlays and
   look-alikes from another culture or era. Genuine brand marks, prices, packaging and original ad text are allowed.
   Sources share candidate space; visual duplicates are removed before numbering. Contact sheets include vertical
   crop previews; the picker saves a focal point and the selected crop as `work/crop_preview_<scene>.jpg`.
   One solo portrait of a person per Short; portraits never under that
   person's own card. Scenes with nothing fitting go to `rescue_graphics()` (full-screen graphic) or a painting;
   a scene with no planned painting gets a prompt from `short_render.plan_gap_paintings()` (one AI call through
   `rewrite_paint_prompts`) instead of repeating an earlier picture.
7. **Media**: voice = **CosyVoice 3 through VoiceStudio** (data in `D:\VoiceStudio`; its installer moved the app to
   `C:\Program Files\VoiceStudio`, `gpu.VOICESTUDIO_EXE` checks both; backend 127.0.0.1:3900, started by
   `voicestudio_up()`; if it still isn't up, the run pauses and asks: open it and press Enter, or type `aiden`), cloned Mark Nelson (`local_ai/voices/nelson_ref.wav` with `aiden_ref.wav` fallback; brisk
   investigative storyteller, CC0/PD), story-arc delivery (`cosy_instruct`: urgent hook -> suspenseful middle -> punchline payoff),
   tempo `COSY_SPEED` (1.10 in `gpu.py`, brisk ~2.8 wps; VoiceStudio ignores `speed`, so `qwen_voice.py` speeds each take up with ffmpeg atempo, pitch kept); each sentence run is one take (`sentence_groups()`), cut per scene by MMS word alignment. Backups in order:
   Qwen3-TTS (aiden), Kokoro, Edge, never mixed in one Short. Paintings: **MOSS-Image** (ComfyUI `D:\ComfyUI`), then
   Gemini, then SDXL. Paintings may show only words quoted in `ai_image`; a hand-made period medium, never "concept
   art"/"cinematic". Real stills -> `clean_photo()` -> focal-point 9:16 crop; film -> complete source frame fitted
   inside `FILM_VF` (legacy `FILM_CROP` only when explicitly requested). Short ads/local clips get camera-shot
   samples; targeted brand/product/year searches include Duke AdViews via Archive and owner imports. AI video
   (`animate`, max 5): the owner's Colab H3 / Flow clips if chosen (start pictures checked first,
   `start_picture_problems()`), else LTX. Motion only for what the picture shows.
8. **Render**: Detail callouts (`mark_details`) choose coordinates on `photo_prep.clean_photo()` output, matching
   the cleaned `_raw.jpg` shown by MarkCard; the downloaded scan can have different borders or stereo framing.
   Remotion when there are >= 3 graphics, any look/special cut, or any full-screen scene; else the Python
   renderer. Graphic styles: date, place (map), fact, stat, timeline, mark, headline, quote, compare, stamp, question,
   kinetic; card overlays hold >= 1.8 s and start early when their word comes late (`editplan.py`); a kinetic title
   with less than its reading hold (`review.callout_hold`, the same `plan_rules.read_need` that places callouts) is dropped (it only repeats the captions); circled details
   must fill 2x2 grid cells; person cards pop on the spoken name. Captions (owner, 2026-11-05, after the "Second Draw" Short): one word or two short ones (`caption_lines`, <= 10 letters, a sentence end closes a line), white Segoe UI Black with a black outline, as spoken, no colours; same in both renderers (`audio_mix.captions`, `Captions.tsx`). No hook title is drawn any more (`hook_text` is still written and used by SEO/logbook/spoiler checks). Palettes (9) drive all graphics and map to a full-scene skin. Credit tag bottom-left
   (`short_credit()`), 2.8 s. Loop Shorts (weird-economics) end straight into frame 0.
9. **Audio**: voice + music (loudness-matched to `MUSIC_LUFS`, ducked) + SFX cue sheet + story sounds; loudnorm
   -14 LUFS + limiter; h264_nvenc.
   Each new Short searches Freesound music metadata for its mood/instruments and downloads only the selected
   track (at most one), ready to use without an approval pause. Cached matches are reused; failures or recently
   used online matches fall back to fitting local music, else silence. `music_online` in media_sources.json can
   disable online music. Music choices/offsets are saved before encoding, so interrupted/fix renders reuse them.
   Music avoids recent repeats and uses a saved start offset. New manually requested music/variant downloads
   wait for approval in media.bat; the owner approved all
   existing media on 2026-11-01. A narration/music preview is saved beside the video. Story sounds align their measured or
   owner-adjusted impact to the spoken word (a steady sound such as static has no impact and starts on its word) and
   are ducked under the voice like the music; `review.sound_masking` flags any effect within 12 dB of the speaking
   voice for 0.5 s+; effects compete over full durations, with at most one quiet texture
   underneath. Freesound uses the current `/apiv2/search/` endpoint. Details: `docs/media-library.md`.
10. **Checks and fixes**: Visual/opening review status is explicitly Passed / Problems found / Not reviewed;
    failed previews, absent replies and malformed verdicts add NOT REVIEWED checks.
    `quality_check()` (also flags a scene that reuses another scene's picture because nothing
    fit, and narration pauses over `PAUSE_MAX` 0.8 s in `work/voice.wav`), `visual_review()` (1 frame/s sheets; told
    about overlay windows; also notes, as CHECK lines without a fix, a weak reveal visual, 5+ s with nothing new and
    crowded scenes), `first_second_check()` (every score goes in edit_plan.txt's quality block; score < 7 may swap in
    a later real picture once; an opener is judged as what it is, never swapped). Flagged scenes get an unused pool
    picture, a full-screen graphic or a repaint with a rewritten prompt (`rewrite_paint_prompts()`); a flagged custom
    scene goes back to its coder once. Re-render and re-review up to `AUTO_FIX_ROUNDS` (3); it pauses for Enter first.
    Left-over findings are `CHECK:` lines in edit_plan.txt (and a Shotcut timeline).
11. **Resume**: Completed scripts are queued before SEO. Failed renders keep folders; run.bat offers resume
    (`resume.bat` / `make_shorts.py resume [folder]`). Checkpoints after pictures, voice and successful encoding
    let the next run reuse finished work. Unchanged narration is cached by text/voice/reference and audio hashes.
    Rendering writes a temporary video before replacing short.mp4; a rendered-stage resume finishes reports
    and reviews without another encode. Finalization does not duplicate logbook entries. Incomplete work is not
    pruned by the seven-day cleanup. Legacy outputs have no batch checkpoints.
    JSON render contexts support real person-card images (PNG + base64), not just paths/photo bytes. Existing-video
    report recovery may call finish_render(build_timeline=False) to run reviews/reports without rerendering Shotcut
    layers. The 2026-11-01 Bobby Leach Short was recovered this way; original video/audio hashes are unchanged,
    progress is complete, and upload/thumbnail/storyboard/edit-plan files exist. Visual review passed; opening
    review scored 3/10 because the orange-peel label reveals the ending immediately. This is a quality note,
    not a broken-file error. The original randomized SFX event list was unavailable and is noted in the report.
12. **Outputs**: edit_plan.txt (Opening line, fact-check changes, per-scene edit list, sound cues, checks),
    upload.txt (credits for every non-PD source and CC-BY 3D model; "altered or synthetic content: Yes" when AI was
    used), storyboard, thumbnail, captions.srt, logbook entry, vault page, `work/state.json` for fix.bat.

## Openers (scene 1 of every Short on `opener: animated` channels)
Order (owner, 2026-11-05): 3D opener -> drawn opener -> motion graphic (2 fixes) -> AI clip of the strangest moment
(`use_opener`).
- **Protect the unanswered question** (`opening_rules.py`, all channels): planning, hook text, picture selection,
  motion-graphic planning, drawn coding/review, clip starting-image rewrites and final opening review must withhold
  new answers saved for later narration. Check recognizable objects as well as labels, signs, diagrams and titles;
  facts already spoken in the hook stay allowed. Both opening reviewers return `reveals_answer`/`answer_why`;
  a positive finding caps the score below 7 even if the art otherwise scores highly. Final review still records
  CHECK lines when a repair is skipped/exhausted or the AI cannot review. No promise of automatic detection.
- **Drawn opener** (`drawn_opener.make_opener`, `drawn/`): a hand-drawn brush-ink + watercolour animation of the
  strangest moment, scene 1 + the crossfade long. The AI codes one scene module against the kit (`drawn/kit.mjs`; its
  manual `drawn/KIT.md`, with the approved Dexter example) -> lint (only `k.*` calls and plain JS; node runs with
  `--disallow-code-generation-from-strings`: the coder has read Wikipedia text) -> a 6-frame preview sheet ->
  the AI as art director, who scores it 1-10 (passes at `PASS` 7; a bare list of flaws rejected every draft on the
  first live runs, good ones included; no verdict = the draft is kept with `unreviewed` and a CHECK line says nobody
  judged it) -> below 7 the coder fixes what it found, up to `FIXES` (2) times -> `drawn/run.mjs` renders
  `work/drawn/opener.mp4`. The plan stays in `short["drawn"]` (fix rounds and fix.bat reuse the clip by
  fingerprint); a failure stays in `short["drawn_failed"]`. A final-review answer reveal can request one bounded
  rewrite via the existing owner-approved fix round (`drawn_answer_fixes`, `drawn_repair`); this bypasses cached
  opener reuse, runs the usual draft/review loop, and restores a protected motion-graphic fallback first. A failed
  rewrite cannot reuse the known spoiler clip. Other final-review findings stay CHECK lines. The channel's optional `## Opener` rules
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

  Custom openers use dedicated portrait/action rules (optional banner, large solid subject, immediate action;
  physical motion can be faster than reading cards). `motion.opener_preflight()` renders the actual headline and
  captions before the full encode, grades it, and allows one local compiled-and-rendered repair. It keeps the
  strongest reviewed candidate; outer redraws get the same check before encoding and can restore the prior winner.
  Full-video complaints supersede an earlier preview pass. Content fingerprints cover narration, brief, shared
  question context, hook and caption timings. Sources/previews/full verdicts are saved under
  `work/opener-attempts/`; final reviews and frames under `work/opening-reviews/` (normal seven-day work retention).
  Opening repair feedback is no longer truncated. Missing previews/verdicts stay Not reviewed; full-video review
  and the existing two outer repairs/clip fallback remain authoritative. Number/map/document openers still use
  their existing templates and final-video review. Visual fixture:
  `.venv\Scripts\python.exe tests\render_opener_preview.py` (restores the generated slot).

- Scene 1's clip starts from a painting of the strangest moment (`review.paint_opener_start` ->
  `work/opener_start.jpg`, `gpu.start_picture`; same painters and `AI paintings` rules), not scene 1's own picture:
  the Dexter Short (2026-10-30) sent Flow the woodcut of Dexter walking, so the clip couldn't show the bed warmers.
- **Drawn reveal** (2026-11-03): on these channels, a reveal scene (`motion.is_payoff`: one of the last two) planned
  as a `custom` diagram is drawn with the same kit and loop (`make_opener(..., i=i)`, `PAYOFF_RULES`, the art
  director asks "do you SEE the answer happen?"; no spoiler check) by `short_render.drawn_payoff`. Files in
  `work/drawn_{i}/`, plan in `short["drawn_{i}"]`; a failure keeps the diagram; fix rounds reuse the drawing and a
  `paint_new` repaint retires it. Not yet seen in a full live run (see Open items).
- **Person cards and the reveal picture** (2026-11-03): no PersonCard when the scene's picture already names that
  person (`plan_rules.shows_person`, surname in the title or catalog note; the card would cover their face), and the
  photo look never goes on the last two scenes (`style_lab.apply_look_scenes`), so the reveal keeps a plain picture.
- **Clean look** (owner, 2026-11-05, reference: Ricks Clips' "Why the Second Draw Always Wins", 8.2M views: flat
  characters in a lit 3D set, a moving camera, no labels): KIT.md now forbids labels/signs/bubbles (the art director
  counts one as a real flaw) and gives the coder `camera = (k) => [shots]` (cut / whip with motion blur / push; every
  shot drifts in), `light = {mood, from}` (day/golden/dusk/night/interior grade, ground shadows under people and
  animals cast away from it), `k.depth()` (blurs and hazes everything drawn so far), `k.dust`, `k.rays`, `k.shadow`.
  The Dexter example uses all of it. Old `camera = {zoom, focus}` modules still render.
- **3D opener** (owner, 2026-11-05, after liking the wooden-eagle 3D test): `opener3d.py`, tried first by
  `drawn_opener.make_opener` (i == 0). The AI writes only a stage JSON against `drawn/STAGE3D.md`: a fixed place
  (room / street / outdoors), a mood, props from a fixed library, cut-outs drawn with the kit (`export default
  function draw(k, f)`, 1-4 drawings, painted by `drawn/cutouts.mjs` under the same locked-down node) and shots aimed
  at named things (distance/height/turn/fov; cut/whip/push). `opener3d.clean` validates and clamps it and resolves
  word times; `render` paints the cut-outs into `remotion/public/opener3d/job/` and renders composition `Opener3D`
  (`remotion/src/Opener3D.tsx`, @remotion/three + three + @react-three/fiber) to `work/drawn/opener.mp4` (~15 s);
  the art director (`drawn_opener.review`) judges a 6-frame sheet; FIXES rounds as usual. The passed plan is
  `short["drawn"]` with `kind: "3d"` (fix rounds reuse it by fingerprint); a failure sets
  `short["opener3d_failed"]` and the drawn opener is made instead (Opening line says so). Lesson kept from the
  removed Blender openers: fixed sets and parts, the AI only places and frames. Wall-hung cut-outs get a picture
  light; a portrait frame needs a wide vertical fov (~60) for a set to read. Tests: `tests	est_opener3d.py`
  (`--look` renders the manual's example to `test_renders/opener3d/example/`); `test_drawn_opener.py` switches
  3D off.
  Live runs 2026-11-05: Claude 5/6/6 on the eagle (desk front filled the frame, a paper floated) -> manual rules;
  Gemini passed the eagle first draft (it copied the example: same story); McLean failed 4/4/4 (fist through the 3D
  door, grocer cut off) -> things that touch go in ONE cut-out (kit `reach`), shots may aim at a list of names (the
  camera backs off to fit them all); McLean then passed on draft 2. Clips: `test_renders/opener3d/`. A failing 3D
  attempt costs 3 drafts + reviews before the drawn opener starts.
- Kit expansion (2026-11-05): 11 more hats (fedora, flatcap, boater, cowboy, ranger, kepi, officer, bobby, bicorne,
  nurse, hardhat), rooms/furniture (`k.door` with `open` + knob, `k.bed`, `k.rug`, `k.shelf`, `k.lamp`, `k.window`,
  `k.frame`), devices (`k.phone`, `k.radio`, `k.letter`), animals `k.cat`, `k.rabbit`, `k.bear` (also in
  `missing_parts`). Hands are painted opaque (washed hands went muddy on dark coats). KIT.md asks for one action arm
  + hand on hip or hanging, never an arm across the body (it read as a line on the coat). `--look` has a 7th page.
- Kit animals: `k.horse` has jointed legs, hooves, mane, `tap: [times]` (a counting/pawing horse) and returns
  `{hoof, head}`. `missing_parts()` rejects a draft whose moment or narration names a kit animal it doesn't call
  (the Clever Hans opener built a boxy horse from shapes and passed 7/10). Labels: size 48+, clear of y 1120-1320.
- Solid things (2026-11-03, McLean opener: the knocking fist went through the door, the beard read as a mask):
  `k.person` `reach: [[x, y] | null, ...]` puts a hand exactly on a point (two-bone IK; a knock moves the target);
  the beard is a jaw beard around the mouth; KIT.md asks for a cutaway wall between inside and outside; the art
  director counts limbs through solid things, covered faces and missing walls as real flaws. Not yet seen live.
## Full-screen motion graphics (`remotion/src/full/`)
- 4 skins (`parchment`, `blueprint`, `dossier`, `hud`) chosen from the palette/mood (`short_skin()`).
- Templates: map `journey`, big `number` (counter + figures, painted silhouette or icons, or `compare` bars),
  evidence `board` (3-5 real photos), `document` (only the key line readable, underlined as spoken).
- `custom` (diagram / collage / flow / clock): the AI codes a React scene per Short (`code_custom_scenes()`) from the
  guarded toolkit (`guarded.tsx`: never-overlapping layouts, arrow router, fitted cards, `MIN_MOVE` 0.9 s); lint +
  `tsc` (one repair) + a small preview the coder fixes once (`look_and_fix()`); fallback scene if it still fails.
  The owner wants these varied, not bland: they declined turning custom scenes into fixed templates. Rule 9
  "TASTE" in `custom_rules()` mirrors the repo's `.claude/skills/motion-design` (from claude-motion, MIT): keep the
  two in step. Rule 10 "SIZE": one main drawing at least half the stage height, solid shapes (Clever Hans's tiny
  outlines read as blank paper); reveal scenes also get rule 11 (`PAYOFF_RULES` in motion.py: one big subject,
  an unmistakable change). The cache fingerprint carries "size-v1" so older cached scenes are recoded.
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
`max_full_planned`, `max_full`, `opener: animated|none`, `hook: moment|money_claim`, `loop: yes|no`, `idea_pages`),
`Topic picking`,
`Story rules`, `Writing for the picture`, `Lessons from our numbers`, `Opening picture` (must define `- era_ok:`,
`- sharp:`, `- hook:`), `Picture picking`, `Directing`, `First-second check`, `AI paintings`,
`Build plan` (Blender channels); optional: `Opener`, `SEO`. A missing section or `status: draft` stops the run;
never another channel's rules. `loop: yes` (weird-economics) is the only switch for loop Shorts (last line runs
into scene 1, no tail, short music fade); `hook: money_claim` adds money charts (`fill_money_graphics`). Rules
files give no word/second targets (`writing.length_plan()` owns them) and keep years as digits (the voice
worker speaks them; date graphics and captions need them).
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
music and palette; reuses verified narration when unchanged; no automatic fix rounds; logbook untouched.
Option 6 adjusts circle/arrow position or label; option 3 can remove it with a scene preview. The fast path
requires a still with hard cuts; overlapping scenes use the ordinary render path. Applying archives originals,
updates state/storyboard/edit-plan, preserves original audio, and archives the stale Shotcut timeline.
See `docs/reliability.md` for checkpoint and repair details.

## Shotcut timeline
When CHECK lines are left after the last fix round, the Short's folder gets `edit.mlt` + `edit_in_shotcut.bat`
(Shotcut portable in `D:\Shotcut`, settings in `D:\Shotcut\appdata`): pictures, graphics (with alpha) and captions as
separate tracks cut per scene, voice/music/sounds as 3 audio tracks, a gain + limiter for -14 LUFS, a red marker per
CHECK. `work/` is pruned after 7 days for complete Shorts, which breaks the timeline too; unfinished checkpoints are preserved. Not yet used on a real Short.

## Logbook (`vault/Logbook/<channel>.md`)
Fresh performance baseline started 2026-10-31 at the owner's request: all 38 old entries from three logbooks
were backed up under `vault/Archive/Logbooks/2026-10-31_200433/` and cleared from active logbooks. Earlier numerical
`Lessons from our numbers` sections were archived there and replaced with fresh-baseline instructions; old
performance claims were removed from the editor prompt. Archives are not read by `logbook_results()`. Videos
and `done_topics` were preserved. Retention is separate: planning and SEO call `retention.observations()`
directly on the active channel's saved output reports, even with no logbook. The owner chooses graphs for
videos with 100+ views; the reader does not require recorded views, logbook entries or dates. It counts each scene type
once per Short and reports overlaps repeated in 3+ Shorts (observations, not causes/failure rates).
No copy-to-logbook suggestion remains. Posting age in the separate numbers log is included;
metrics collection age remains unknown. No logbook columns or contents are changed automatically.

The retention menu also offers optional manual Studio details: views, stayed-to-watch, average percentage
viewed, average view duration, posting/collection dates, reporting period, likes/comments/subscribers and
notes. Enter skips/keeps, `-` clears; validated values are saved atomically to `retention/metrics.json`.
Graph reviews receive these details and include a snapshot in their report. Planning/SEO read the latest
details directly (including details-only Shorts) as bounded per-Short context with saved length, without
view gates or any logbook access. Missing details remain unknown; notes are not instructions or proven causes.

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
  `beaae733`; the previous branch/wait notes were stale. Part 2.2 supports all three AIs. Owner clarified: three true solo modes and all six ordered writer/editor
  pairs; quota handover can use the third AI within the same run. Part 3.1 (retention reader) is implemented;
  3.2 (automatic use of reports) is implemented independently of the logbook; 3.3 and 3.4 remain open.
  Plan: `docs/superpowers/plans/2026-10-31-audit-improvements.md` (git-ignored on purpose).
  Malformed cold reads now count as no review; a failed second read removes the old draft's verdict. A failed
  opener preview also clears the old render's score. A live Codex cold read passed. Owner completed the Mary Toft Short (2026-10-31); its 19-21 s callout
  exposed a cleaned-image coordinate mismatch, now fixed. A corrected copy is saved alongside the original.
  The run also left CHECK notes for a reused picture and weaker reveal visual.
  Reliability follow-up is implemented: resume checkpoints, narration reuse, explicit review statuses, circle/arrow
  scene repairs, and reviewed-pool download recovery. Plan: `docs/superpowers/plans/2026-10-31-reliability-improvements.md`.
  Separate open question: weird-economics' 110-135 words vs the code's 95-125.
- **Openers**: the drawn opener ran inside a full run for the first time on 2026-11-03 (Wilmer McLean,
  `output\strange-history\2026-11-03_he-fled-120-miles-then-came-the-knock`): draft 1 scored 5/10 (figures too
  small), a later draft passed, first-second score 8/10. The drawn reveal did not trigger (no reveal was planned as a
  custom diagram), so it still has no live run; the motion-graphic fix rounds have no live run yet. More kit parts as stories need them.
- run.bat's "press any key" at the end doesn't close the window for the owner: not found in the code; waiting for
  the window's last line.
- Never seen in a real run: style inventions, question beats, wipes, the Shotcut timeline.
- `channels/engineering-failures.rules.md` is drafted (`status: draft`) and waiting for the owner's review; gaming is ready.
- Media sources/audio expansion implemented 2026-11-01. Source status and local import fallback in media.bat;
  McDonald's/LoC blocked automated requests here, Smithsonian demo key hit its rate limit. Europeana's owner-
  supplied key is configured locally and a live image search succeeded. Duke AdViews works; Duke's separate Ad*Access print site has no working connector
  here (local import available). No new keys acquired. New film preserves its frame; legacy crop is opt-in.
- Quality audit (2026-11-01): `docs/short-quality-research.md` records evidence, GitHub options and next priorities.
  Rendered CHECK lines now include measured seconds of cold-reader detours, mid-story swipe timestamps,
  short callout reading holds and unresolved script/metadata/fact-review notes. No new runtime dependencies.

## Ideas offered, not built
- Voice cloning of the owner, SFX on the music's beat, YouTube Audio Library tracks for somber/epic.
- Rejected: logbook extras (noise), MoneyPrinterTurbo, AutoSocial, kie.ai, Wan 2.2, browser-automating Google
  Flow/Gemini (account ToS risk), Hyper3D Rodin's shared trial key, Hunyuan3D 2.1 (licence excludes EU/UK/KR).

## How to verify changes
- Media changes: `tests/test_media.py` (source fixtures + real FFmpeg shot/crop/audio checks) and
  `tests/test_render_resume.py` (real renders with and without music/SFX, saved offset and report resume).
- `.venv\Scripts\python.exe -m compileall -q make_shorts.py shortsmaker`; Remotion: `cd remotion && npx tsc -p .`
- Tests, no AI usage (`.venv\Scripts\python.exe tests\<name>.py`): `test_reliability`, `test_render_resume` (real FFmpeg, fake AI), `test_package`, `test_codex`, `test_ai_modes`, `test_marks`, `test_retention`, `test_pictures_first`,
  `test_full_scenes`, `test_style`, `test_rules` (golden prompts), `test_story`, `test_first_second`,
  `test_topic_ideas`, `test_h3_handoff`, `test_h3_run`, `test_edit_project`, `test_blender_plan`,
  `test_blender_render`, `test_opener_graphic`, `test_drawn_opener` (real node, ~1 min), `test_opener3d`;
  `tests\run_ts_tests.py` (TypeScript); `local_ai\qwen_venv\Scripts\python.exe tests\test_qwen_voice.py`.
- Quality changes: `tests/test_quality.py` (metadata validation, final-script reviews, pacing and retention feedback).
- With real headless Blender (engineering-failures): `test_blender_run`, `test_blender_scene`.
- One full-screen scene: `tests\render_full.py remotion\test_props\<name>.json [--still SECONDS]`.
- Prompt changes without AI usage: fake `llm.ask_ai` (and `writing.article_text`, `channel_profiles.trend_research`,
  `topic_ideas.pick_ideas`) and read the captured prompts. Single steps: in a scratch script call
  `channel_profiles.use_channel("<name>")` first, then the function.
- Full run: `.venv\Scripts\python.exe -u make_shorts.py 1 strange-history gemini`, then a 1 frame/s sheet
  (`ffmpeg -i short.mp4 -vf "fps=1,scale=180:-1,tile=11x5" -frames:v 1 sheet.jpg`) and edit_plan.txt's CHECK lines.
