# ShortsMaker — handoff for a new Claude session

Read this first, then read the code it points to. Last updated 2026-10-16.

## What this is
A faceless YouTube Shorts generator, now for **several channels** via profiles (`channels/`):
`strange-history` (the original; suggested name "Plot Twist Archive", @PlotTwistArchive) and `gaming`
(gaming facts & lore, made by the owner 2026-10-14). The owner's goal is YouTube Partner Program monetization
from a fresh account. The owner runs `run.bat`, reviews each Short, and **uploads manually** in
YouTube Studio (no API uploads: an unaudited API project locks videos to private).

**Division of labour (the owner's explicit choice, "Hybrid"):**
- **Claude** (headless `claude -p`) plans everything: niche, trend-informed topics, script,
  frame-by-frame edit plan, image choices (it *looks* at contact sheets), SEO, thumbnail plan.
- **The owner's PC** generates everything: voice, gap images, thumbnail art, video clips, parallax
  camera moves, rendering. Real archival photos (Wikimedia) stay the main footage; AI fills gaps.

**Planner switch: Claude or Gemini (2026-10-15, owner's request).** run.bat asks a 3rd question, "Who writes and
plans these Shorts? 1) Claude 2) Gemini" (Enter = the profile's last choice, saved as `"brain"` in the profile;
`make_shorts.py [count] [channel] [claude|gemini]` skips it). Every AI call goes through `ask_ai()`; with Gemini it
runs Google's Antigravity CLI `agy` (already installed, signed in with the owner's Google account, no key) via
`run_agy()`: agy only takes the prompt inline (`-p=...`, and ignores stdin), so the prompt is written to a task file
inside the folder it may read (`agy_tasks/` or the contact-sheet folder) and agy is told to read it. Model:
`gemini_model()` picks a Gemini 4 "Argon" model automatically once `agy models` lists one, else
`gemini-3.8-flash-high`; always `--effort high` (owner's wish). If Gemini fails twice, Claude answers that step.
With Gemini, the AI gap images + thumbnail art are painted by agy's built-in image generator (`gemini_images()`,
768x1376, ~2-3 min each, 3 at a time) instead of SDXL; failures fall back to SDXL. **agy cannot make video**
(no Veo/Flow): AI video stays LTX on the PC. Tested 2026-10-15: 55k-char prompt -> correct JSON (~50 s); picture
reading (bear, face row 3, ~2 min); painted image clean, no watermark. **Not yet tried in a full run.**

## Owner preferences and constraints (important)
- **Install everything on D:.** C: is nearly full. Caches and models live under `D:\ShortsMaker`.
- **Prefers no API keys or sign-ups** (abandoned MoneyPrinterTurbo over them). Approved exceptions:
  Pixabay (free key, 2026-10-15) and vidIQ (free account, chat use only). Ask before adding another.
- **Broad multi-niche footage with automatic on-screen + description credits (2026-10-16, owner's explicit choice):**
  The owner unlocked full YouTube video sourcing (`youtube_films()` across all of YouTube, prioritizing the niche's
  `research_seeds` channels), full Internet Archive movies & images (`archive_films()`, `archive_images()`), full
  Openverse (including Flickr and CC BY-SA/NC), and all Wikimedia/Wikipedia licenses (including `CC BY-SA`,
  `Attribution`, and `Fair use` game screenshots/covers >= 250px wide). Every non-PD source automatically gets an
  on-screen credit badge (`credit_tag` at `y=170`, e.g. `Video: Channel Name (@handle) (YouTube)`) and a line in
  `upload.txt`. Do NOT re-lock `youtube_films()` to Creative Commons (`sp=EgIwAQ==`) or `archive_films()` to
  `prelinger`/`universal_newsreels`.
- Hardware: **RTX 5060 8GB VRAM**, 32GB RAM, Ryzen 7 5700X3D, Windows 11. The owner often has
  Roblox, Wallpaper Engine, Discord and Chrome open, which take VRAM and RAM.
- Sound: the owner disliked a loud repetitive whoosh and **sub-bass "thumps"**. All SFX are
  high-passed at 220Hz; the impact/hit sounds were removed. Keep it that way.
- The owner disliked background images that "pop" (a punch-in zoom). It was removed.
- The owner is not a programmer. Explain in plain language and avoid jargon.

## Layout (`D:\ShortsMaker`)
| Path | What |
|---|---|
| `run.bat` | Runs `make_shorts.py` with `.venv` (Python 3.14); it asks which channel profile (Enter = last used, or "+ New channel"), then how many Shorts. `make_shorts.py [count] [channel]` skips the questions |
| `make_shorts.py` | The whole pipeline (about 1,900 lines) |
| `pixabay_key.txt` | The owner's Pixabay API key (never print it) |
| `ltx_compare/` | Owner's viewing copies of the 2026-10-15 LTX comparison clips; not used by the program, safe to delete |
| `channels/<name>.json` | One profile per YouTube channel (owner asked 2026-10-14): niche, audience, tone, Edge voice name, `done_topics`, `research_seeds`, `cta_line` (under the SUBSCRIBE button); optional `local_voice`. `new_channel()` makes one from the owner's niche sentence (or Claude picks). `last.txt` = default pick. The original channel is `strange-history` |
| `channels/<name>.research.json` | That channel's trend research cache (daily) |
| `logbook/<name>.md` | **The owner's logbook** (asked 2026-10-15): `log_short()` appends an entry per finished Short (title, date, length, folder, topic, story shape, hook line, hook title) with empty lines the owner fills in from YouTube Studio: Posted on, Views, Likes, Comments, Subscribers gained, Stayed to watch (%), Average % viewed, My notes. `logbook_results()` feeds every entry with Views filled in (last 30) to the planner. When the owner asks how the channel is doing, read this file and explain it in plain words |
| `local_ai/` | GPU worker: own venv (Python 3.12, torch cu128), `gen.py`, `hf/` model cache (~31GB), `models/ltx_t5_bf16` (8.9GB) |
| `remotion/` | Remotion 4 project (`src/Short.tsx`, `Graphics.tsx`, `Cards.tsx`, `MapCard.tsx`, `Captions.tsx`), official Remotion agent skills in `.agents/skills` |
| `music/` | 8 Kevin MacLeod tracks (CC BY; credit sidecar `<track>.mp3.txt`) |
| `sfx/` | Synthesized sound library (regenerated by `make_sfx()` if files are missing) |
| `cache/` | Wikimedia download cache (30-day prune) |
| `output/<channel>/<date>_<slug>/` (older ones directly in `output/`) | `short.mp4`, `thumbnail.jpg`, `upload.txt`, `captions.srt`, `edit_plan.txt`, `storyboard.jpg` |

## Pipeline (in order, see `main()` and `render()` in make_shorts.py)
1. `trend_research()`: Claude suggests channels once (`research_seeds`). yt-dlp lists their
   /shorts tabs; channels with median recent Short views of at least 20k pass. Saved handles with no Shorts tab are
   moved to `research_seeds.dropped` and replaced by `seed_ideas()` in the same run (yt-dlp's errors are silenced via
   `QUIET_LOG`). Top Shorts are ranked
   by views/day. Cached daily. YouTube does not expose captions for Shorts, so titles stand in for hooks.
2. `write_scripts()`: one Claude call returns scenes with narration, image_search, shot (director's
   note: framing + what's on screen + what to notice), move, graphic (date/place+lat/lon/fact, with a
   spoken `trigger`), person, emphasis, transition (fade|flash), ai_image, animate+motion,
   plus wiki_articles, thumbnail_prompt, SEO drafts. Everything is validated, because LLM output is untrusted. The prompt also gets the filled-in logbook entries
   (what kept viewers) and a story `shape` from `SHAPES`, never one of the channel's last 3 (`recent_shapes`),
   so the channel doesn't read as one template. `ai_image` prompts ask for a painted/illustrated style, never
   "photograph" (a fake old photo would pass as real evidence; owner approved 2026-10-15).
   **Fact check** (`fact_check()`, inside `write_scripts()` before validation): one Claude call checks every line,
   graphic, hook_text and thumbnail_text against the plain text of the story's Wikipedia articles (`article_text()`,
   first 4, 15k chars each) and rewrites unsupported lines; a graphic showing a wrong fact is dropped; callouts whose
   trigger words changed drop out in validation. A story whose central claim is a myth is skipped and added to
   done_topics as "(myth, skipped)". Changes are listed at the top of edit_plan.txt. Tested 2026-10-15: passes the
   real Annie Taylor script; caught a planted wrong year (and dropped its date card) and a wrong age.
   Script rules: hook on the subject, open loop, re-hook at 20-30s, last line calls back to the hook
   (rewatch loop), every scene about something showable, no repeated 3+ word phrases (the callback
   must not reuse the previous scene's wording). Thumbnail art must match the story's era.
   **First second** (owner's first upload: 49% stayed / 51% swiped): hook sentence <= 8 words stating
   the shocking fact, Claude drafts 3 (`hook_options`, listed in edit_plan.txt) and uses the best;
   `hook_text` is its own 2-4 word tease (not the thumbnail text), drawn smaller and higher (120px at
   y=220) so it doesn't cover faces; the photo editor gives scene 1 the most striking picture (film
   first) and scene 1 may be animated; scene 1's voice lead-in silence is trimmed (first word ~0.05s);
   music fades in over 0.1s instead of 1s. (Tested on a stubbed plan in Remotion: first word at 0.05s,
   hook text clears the face. Don't run tests while the owner's batch runs: they share RAM/VRAM and
   `remotion/public/job`.)
   No spoken CTA (owner chose on-screen only, to keep the rewatch loop): a silent red SUBSCRIBE
   button + the profile's `cta_line` (copied to `short["cta_line"]` in `render()`) shows for the last ~3s
   under the captions (y 1330) in both renderers, with a soft "pin" sound.
3. `seo_pass()`: free YouTube autocomplete phrases, then Claude rewrites title, description, tags and pinned comment.
4. `choose_images()`: pool = images from the story's Wikipedia articles + a Commons search per scene
   + portraits + Openverse (incl. Flickr) + Internet Archive images + NASA images (up to `POOL_MAX = 64`).
   Licenses (2026-10-16): all Wikimedia/Wikipedia licenses (incl. `CC BY-SA`, `Attribution`, and `Fair use`
   screenshots/box art >= 250px wide) are allowed and credited on screen (`credit_tag` at `y=170`) and in `upload.txt`.
   Claude/Gemini views numbered contact sheets (`claude -p --allowedTools Read --add-dir` or `run_agy`), with a
   title-based fallback. It matches each scene's shot note, refuses violent/suffering pictures, and
   re-picks `move` and `motion` (or turns LTX off) for the picture it actually chose.
   **Real video & YouTube footage (upgraded 2026-10-16):** Every scene in `write_scripts()` now includes both
   `image_search` and a specific `video_search` query (e.g. `"Super Mario 64 Bowser throw gameplay"`,
   `"Apollo 11 liftoff footage"`). `choose_images()` searches:
   - `youtube_films()`: searches all of YouTube per scene (`video_search`) + topic queries (no Creative Commons lock,
     up to 10 videos per Short, <=40 min), ranks the channel profile's `research_seeds` (`handles` + `dropped`) first,
     then keyword match count, then 15s-15m duration, then view count (filtering out parodies/cartoons/reactions unless
     in the query). Extracts matching video `chapters` into `moments` so `film_frames()` grabs frames right from the
     relevant chapter midpoints (and samples 15%..85% of longer videos to skip intros/outros). Sets `credit` to
     `"Channel Name (@handle)"` so `Video: Channel Name (@handle) (YouTube)` shows on-screen and in `upload.txt`.
   - `archive_films()` & `archive_images()`: searches all of Internet Archive (`mediatype:movies` sorted by downloads,
     supporting `.mp4`/`MPEG4`/`h.264` with or without `__ia_thumb.jpg`, and `mediatype:image`).
   - `commons_films()`, `pixabay_films()` (key in `pixabay_key.txt`), `nasa_films()`.
   Up to `FILM_MAX = 14` videos x 4 frames go on the contact sheets, sampled concurrently via `ThreadPoolExecutor(4)`.
   Both `film_frames()` (contact sheets) and `film_piece()` (downloaded ~14s clip) apply `FILM_CROP` (cuts the top 6%
   chapter/watermark bar, the bottom 20% burned-in subtitle/caption zone, and 4% per side) so burned-in bottom captions
   never appear in the video or the blurred background. `youtube_films()` also skips vertical Shorts (`/shorts/`, `w <= h`).
   The visual editor can pick `REAL FILM` on **as many scenes as fit** (up to every scene in the Short; old 4-scene
   cap removed). `local_clips()` cuts each picked clip to one camera shot (`shot_span()`) and always lays out horizontal
   footage zoomed-out with `FILM_VF` (full width centred over a blurred, darkened copy of the cropped video, so people
   and objects on the left/right are never cut off; `fills_frame()` only uses `FILL_VF` for already-vertical clips).
   `mark_details()` skips `REAL FILM` scenes so it never places a duplicate still photo card over a playing video clip.
   Any non-PD background gets an on-screen credit tag (top-left, y=170: `credit_tag_image()` / Remotion `credit`) plus
   its line in `upload.txt`; `choices[i]["site"]` names the source. `get_image()` routes downloads (Wikimedia -> `wm_get`,
   Openverse -> `ov_get`, others plain, never with the owner's email).
   Callouts appear on their trigger word (`scene_cues()` -> `cue["graphic"]`, used by both renderers,
   the SFX cue sheet and edit_plan.txt); the map is held back so it gets ~2.3s to animate.
5. GPU worker (`local_job()` -> `local_ai/gen.py <job.json>`, runs with `HF_HUB_OFFLINE=1`):
   - `tts`: Kokoro (speed 1.1) with word timestamps; voice = profile `local_voice` or `KOKORO_VOICES[voice]`
     (strange-history: am_michael, gaming: am_fenrir). Falls back to Edge TTS.
   - `images`: SDXL-Lightning 4-step 768x1344 for scenes with no real photo, plus thumbnail art.
   - `video`: LTX-Video **0.9.8 2B distilled** (since 2026-10-15; single file `ltxv-2b-0.9.8-distilled.safetensors`
     loaded with 0.9.5's configs/tokenizer/scheduler, 8-step schedule `LTX_STEPS`, no CFG) image-to-video
     (512x896, 97 frames, ~25 s each, 4.8 GB VRAM) for the 3-5 `animate` scenes (cap 5; the 0.9.5 weights stay for rollback;
     scenes that got real film skip it).
   - `parallax`: Depth Anything V2 Small + torch `grid_sample`, a full-screen 2.5D move for every other scene.
6. Renderer: **Remotion** if there are 3 or more callouts/person cards (`REMOTION_MIN_GRAPHICS`) or any
   `REMOTION_ONLY` style / map route, else the built-in Python/Pillow renderer. Remotion failure falls
   back to Python, which shows stat/timeline/mark as plain fact boxes (`fallback_graphic()`). Both play
   the GPU clips (Python streams them via `ClipReader`).
   **Graphic styles** (validated by `clean_graphic()`): date (year counts up), place (map; optional
   `from` = route line), fact, stat (`value` + optional `of` <= 200 = dot grid, else counter), timeline
   (`start`/`end` + gap text), mark (circle/arrow on a photo card; placed by `mark_details()`, one extra
   Claude call that reads the chosen pictures under a lettered 10x10 grid; max 2, only on scenes with no
   callout/person). Planner must use 3-5 graphics with 3+ styles. Remotion: `Cards.tsx` (stat, timeline,
   mark), `MapCard.tsx`, `Graphics.tsx` (`useWindow` spring ~8% overshoot + accelerating exit; `moveIn`
   rotates rise/slide/drop entrances by graphic order, scale never below 0.9).
7. Audio: voice + ducked music + the `sfx_events()` cue sheet, loudnorm -14 LUFS + limiter (below), final
   encode **h264_nvenc** (x264 fallback).
8. `quality_check()` runs on the finished video (ffmpeg blackdetect/freezedetect/ebur128, ~2 s): black or frozen
   stretches, loudness off -14 LUFS, peaks above -0.5 dB, plain-frame scenes, length > 75 s. Printed as "CHECK:" lines
   and appended to edit_plan.txt. The final mix ends with a 4x-oversampled limiter (`alimiter` 0.79 at 176.4 kHz):
   one-pass loudnorm alone let an Atari Short peak at -0.1 dB.
9. Outputs: storyboard from the finished video, `edit_plan.txt` (timestamped edit list + sound cue
   sheet), `upload.txt` (title, description + credits, tags, pinned comment, settings, and an
   "altered or synthetic content: Yes" line when AI images or LTX clips were used).

## Hard-won lessons (don't relearn these)
- **Wikimedia** only serves thumbnail widths 330/500/960/1280/1920. Bulk originals or odd sizes get
  HTTP 429 with Retry-After 600. Always use `thumb_url()`, never wait more than 30s, space requests 1s.
  API file URLs carry `?utm_...` query strings: strip them before building thumb URLs.
- **LTX on 8GB:** load in two stages (text encoder first, then the transformer), never both at once
  (RAM segfault). Transformer uses fp8 layerwise casting. The T5 text encoder runs **on the GPU** with
  fp8 storage from the one-time bf16 copy. Its `.wo$` layers must stay bf16 (T5 casts its input to
  wo's stored dtype). Running T5 on the CPU was the CPU/RAM hog the owner noticed.
- Remotion render flags: `--gl=angle --concurrency=4 --x264-preset=ultrafast --crf=14` (re-encoded by NVENC).
- **AI motion is situational** (owner's request, 2026-10-15). LTX 0.9.5 warped people and machines (2026-10-14
  gaming test); 0.9.8 keeps people coherent. The planner and photo editor now pick one of two kinds per scene:
  ATMOSPHERE (smoke, water, clouds, dust, flags, light; `motion_people` false: the LTX prompt says people,
  animals and machines stay completely still) or PEOPLE moving slowly and simply (`motion_people` true: the
  prompt asks for slow natural movement with intact bodies, and the finished clip gets `PEOPLE_CLIP_VF`: downscale,
  slight blur, film grain and a vignette to hide the remaining AI ghosting; owner's request, 2026-10-15). Never fast action, moving vehicles/machines or
  close-ups of real faces; those get parallax. YouTube "Wikipedia Spoken Articles"-style slideshows are not
  footage: the photo editor skips them. (LTX's negative prompt is unused: the distilled model runs without CFG.)
- Edge TTS occasionally returns NoAudioReceived: `speak()` retries.
- Edge TTS 403 (`WSServerHandshakeError`) = Microsoft changed its handshake: update edge-tts. `.venv` has no pip;
  use `uv pip install -U edge-tts --python .venv\Scripts\python.exe` (7.2.8 -> 7.3.1 fixed it on 2026-10-14).
- Kokoro runs with HF_HUB_OFFLINE=1, so every voice in `KOKORO_VOICES` must already be in `local_ai/hf`. All 5
  (am_michael, am_fenrir, af_heart, af_bella, bm_george) are; adding a new mapped voice means downloading it once.
- Writing JSON from PowerShell adds a BOM: `load_channel()` reads utf-8-sig.
- Keyword-first image search gave namesakes (Lincoln for a jockey, Neptune for a person): hence the
  Claude visual pick and the full-name-in-title rule for person cards.

## Status
- **Full runs so far:** Timothy Dexter (10-13), Dancing Plague and Carrington (10-14, history), Walter Arnold
  (10-14, batch), Atari burial (10-14, gaming: its warped LTX workers and a -0.1 dB audio peak led to the
  0.9.8 switch, motion rules and the limiter), Annie Edson Taylor (10-15, history, Claude's test run).
- **Annie Edson Taylor run (2026-10-15) confirmed in a full run:** first-second hook (8-word hook, 3 options),
  Pixabay film (scenes 1, 6), Commons CC BY film + on-screen credit tag (scene 7), date/timeline/map/arrow mark/
  fact/person cards in Remotion, SUBSCRIBE + cta_line, quality check (all OK), credits in upload.txt. Fixed after
  it: widescreen film now fills the frame (`FILL_VF`, chosen by `fills_frame()`); the cue sheet said "circle drawn" for arrow marks.
  **Nintendo cards-to-taxis run (2026-10-15, gaming, Claude's test)** confirmed logbook entry, story shape
  (`recent_shapes` saved), fact check (2 fixes listed in edit_plan.txt), painted AI image (watercolor taxi), seed
  swap (7 gaming channels replaced, 5 proven). Weak spot: free sources are thin for gaming (carnival costume for the
  Ultra Hand). Again no LTX ran: the photo editor turned motion off for its card/drawing picks, as the rules say.
  **Still untested in a full run:** LTX 0.9.8 clips and people-clip softening (the planner's animate scenes were
  the water scenes, which all got real film instead, so no LTX ran), Openverse/NASA/YouTube CC picks.
- Trend research: 11 of 14 strange-history `research_seeds` channels have no /shorts tab (yt-dlp ERROR lines,
  harmless), so only 3 channels feed the research. Refreshing the seeds would help; not done.
- Throwaway test scripts live in the old session's scratchpad; recreate as needed. Tests that import
  `make_shorts` must set `m.CHANNEL = m.CHANNELS / "strange-history.json"` (or call `use_channel`).
- Earlier details:
- Fixed after that run: the planner wrote `motion` before an image was picked, so LTX turned a
  woodcut portrait's white background into sky and water. `choose_images()` now has the photo
  editor rewrite `motion` for the picture it chose, or null (no LTX) for drawings/documents/portraits.
- Fixed: Wikimedia 429s ("does not comply with our robot policy", ~9 min lost per run). The
  User-Agent lacked contact info; `WM_UA` now carries the owner's email (owner approved), sent to
  Wikimedia only, not to YouTube autocomplete. Probe: 19/19 fresh thumbnails in 19s, zero 429s
  (before: 23/25 in 238s).
- 2026-10-14 "Dancing Plague" run looked good; its weak spots (off-topic images, violent painting,
  1800s-looking thumbnail, soft ending) led to the shot/trigger/editor changes above. Tested with a
  stubbed 4-scene plan in both renderers and a real photo-editor call; **not yet in a full run**.
- 2026-10-14: new graphic styles + motion tested with a stubbed 8-scene plan (real mark_details call)
  in Remotion and the forced Python fallback; **not yet in a full run**.
- About 16-20 min per Short (up to 5 LTX clips) when Wikimedia isn't throttling.

- **Frame-by-frame review (2026-10-15)** of both test Shorts (1 frame/s via ffmpeg `fps=1,tile=8x4`; do this after
  every change that affects the picture, the storyboard alone misses things). Sound fine (-14.8/-14.5 LUFS, peaks
  -1.9/-1.7 dB, no gaps). System fixes made from it (owner: "improve the system overall, not just this short"):
  - `clean_photo()` on every real still (not film): `is_stereo()` keeps one photo of a stereograph card (halves
    compared after removing row averages; real card 0.52, other wide pictures <= 0.1, bar 0.4) with a fixed crop
    for the standard card layout; `trim_borders()` cuts plain scan borders (a line counts when 90% is one tone,
    stepping over up to 3 soft edge lines; max 15% per side). Tested on the real 1901 Falls plate, the stereo card,
    the hanafuda scan and an untouched normal photo.
  - Photo editor: look-alikes from another culture/era (Western card for hanafuda, carnival costume for a toy)
    count as nothing fitting -> null -> painted illustration; the person card must differ from the background.
  - Captions: `caption_lines()` (<= 3 words, ~16 letters) is shared by both renderers (Remotion gets a `line`
    per word), so a long word no longer shrinks the hook caption to a tiny size.
  - edit_plan.txt printed big counters as 1e+06.
  Verified in a full run (Roy Sullivan, 2026-10-15, strange-history): large readable captions, no scan borders,
  **first real LTX 0.9.8 clips** (3 atmosphere clips of storm skies, clean, 83 s for all 3), fact check fixed 2 lines,
  sound -14.4 LUFS / -1.8 dB. People-clip softening (`PEOPLE_CLIP_VF`) still untested in a full run.
  - **Callouts move off faces (2026-10-15, fixes the "7 LIGHTNING BOLTS" counter on the bear's face):** the photo
    editor also returns `subject_row` (1-10, where the subject/face sits in the chosen background) ->
    `choices[i]["subject_y"]`. After `local_clips()`, `graphic_low()` maps it onto the 1080x1920 frame (cover crop, or
    the centred band for FILM_VF film) and sets `graphic["low"]` when it lands at y 180-680, under the top callouts.
    Low callouts end at y=1110 (`LOW_BOTTOM` / Remotion `slot()`), just above the captions. Applies to date, fact,
    place pill, stat, timeline; map, mark and person cards are full panels and stay put. edit_plan.txt says
    "(lowered: the subject is at the top)". Tested on the real bear frame in Remotion (stat + timeline) and the Python
    renderer; **the photo editor's `subject_row` answer is not yet seen in a full run.**

- **Cardiff Giant review (2026-10-15, first Gemini-planned Short)**: script/fact check good; fixes made for future
  Shorts: (1) LTX "dust drifting" over a photo with no dust made a white smoke cloud over the giant (scenes 1, 3):
  ATMOSPHERE motion is now only what's visible (water, clouds, rain, snow, flags, fire, light, smoke/steam from a
  visible source), never added dust/fog/mist (planner + photo editor rules). (2) The ending painted an invented face
  of the real artifact (real photos are mostly CC BY-SA): `ai_image` never paints a close-up of the real object the
  story is about. (3) A courtroom engraving captioned with another trial: the photo editor rejects pictures whose
  printed caption names another event/place/person. (4) The fact check rewrote a line but the AI image still showed
  the old version: `fact_check()` now also returns corrected `shot`/`ai_image`. None of these seen in a full run yet.
- **Map card timing (owner's report 2026-10-15)**: on fast Shorts the map left before the place name finished
  (Cardiff: name complete at 9.9 s, exit started 9.9 s). Now the map starts by `end - (MAP_EXIT + MAP_FLY + MAP_HOLD)`
  (3.47 s before the scene ends) and a too-short scene gets `cue["map_pace"]` (0.4-1) that speeds up the fly-in
  (`graphic.pace` in MapCard.tsx, pin sound in `sfx_events()`), so the name stays readable >= ~1.1 s. Asserted on
  5.8/3.0/2.6 s scenes and rendered in Remotion.

- **Built 2026-10-15 from the owner's "do the fixes you recommended":**
  - `visual_review()`: after `quality_check()`, the planner AI views the finished Short as 6x5 sheets of 1 frame/s
    (`work/review/`) with the scene list and reports viewer-visible problems (AI blobs, covered faces, wrong
    picture/era, washed-out frames, stray captions/logos, AI stand-ins for real things) as `LOOK at m:ss (scene n)`
    CHECK lines. One AI call per Short.
  - **fix.bat** (`make_shorts.py fix`): `render()` no longer deletes `work/`; it writes `work/state.json` (final plan,
    picture choices with bytes in `keep_<i>_<kind>.bin`, music, Gemini-painted files) via `save_state()`. `fix_short()`
    lists Shorts with a state (newest 9), asks scene + change (no AI motion / another scene's picture / remove the
    graphic) and calls `render(..., state)`, which skips `choose_images`/`mark_details`, keeps painted AI images
    and the music; voice, clips and video are re-made (a few minutes). `prune_work()` deletes work folders after
    `KEEP_WORK_DAYS` (7). The logbook entry and done_topics are untouched.
  - **Compare mode**: run.bat's 3rd answer "Both" (`BRAINS`): Claude plans n topics, then Gemini writes the same
    topics (`write_scripts(..., topics)`); folders end in `-claude` / `-gemini`; the owner posts only the better one.
    The logbook's Made line now says "Written by".
  - **Myths list**: a story the fact check rejects goes to the profile's `myths` (with `myth_note`, what really
    happened) instead of done_topics; the planner gets the last 20 as "myth vs truth" story ideas.
  - Tested: state round trip and the fix flow with a stubbed render. **Not yet seen in a full run: a real fix
    re-render, compare mode, the myths list.**

## Open ideas the owner has seen (none started)
- **Google Flow / Veo hand-off: BUILT 2026-10-15 (owner's design).** run.bat asks "Make the AI video clips yourself
  in Google Flow (Veo)?" (y/N, saved as profile `veo`; scripted runs never ask or pause). With yes, `local_clips()`
  calls `veo_handoff()` for the animate scenes: `<Short>/veo/` gets `start<N>.jpg` (9:16 cover crop) and
  `prompts.txt` (same `motion_prompt()` as LTX + "Vertical 9:16, no text, no music"), both opened, and the batch
  waits for Enter. Any `scene<N>.mp4/.mov/.webm` saved there becomes `work/clip<i>_veo.mp4` (FILL_VF, no audio,
  cut to the scene); missing scenes fall back to LTX. fix.bat re-renders reuse existing `clip<i>_veo.mp4`. Edit plan
  says "made by the owner in Google Flow (Veo)"; `clip*` names keep the synthetic-content label. Tested with a fake
  720x1280 clip + stubbed GPU jobs; not yet with real Veo output. Do NOT automate Flow/Gemini apps via the Chrome
  extension: ToS risk to the account that owns the channel. Owner declined paid APIs (kie.ai) on 2026-10-15.
- Gaming channel caveat: game footage/art is publisher-owned; free sources find little for gaming topics,
  so expect more AI images there. Recording own gameplay under publisher video policies was mentioned.
- Quote/headline card (a real quote typed out on aged paper): suggested 2026-10-14, not chosen yet.
- Voice cloning (the owner's own voice) via Qwen3-TTS or Chatterbox in `gen.py` + Whisper
  alignment: offered, no answer yet.
- Snapping SFX to the music's beat. Helios video model as an LTX upgrade (untested, likely too big).
- **Wan 2.2 TI2V-5B tested 2026-10-15 and rejected** for the 8GB RTX 5060: even with a bf16 copy + fp8 layerwise
  casting + CPU offload, 480x832 / 49 frames ran ~155 s per step (~50 min per 2 s clip; LTX: 2 min) and 720p
  never reached step 1 (VRAM overflow, GPU at 46 W). Files deleted. Revisit only with a 16GB+ card.
- Windows page file is only 2 GB on C: (C: is nearly full). The owner tried adding one on D: but it didn't take
  effect (2026-10-15). Big model loads can hit MemoryError when other apps hold memory.
- **vidIQ MCP** (2026-10-15, owner's choice): connected to Claude Code for interactive use only (`claude mcp add
  --transport http --scope local vidiq https://mcp.vidiq.com/mcp`, local scope for C:\Users\ddgut), so the batch's
  `claude -p` calls (cwd D:\ShortsMaker) never load it or spend its credits (Free plan: 150 credits/month, most
  calls 5). Not wired into the pipeline; a one-call-per-batch lookup was offered and declined.
- Also reviewed 2026-10-15 and not adopted: AutoSocial (browser-automated posting + a "uniquifier" for reposting
  others' videos: account and copyright risk), mortiflix-oss (overlapping Claude+Remotion studio; its QC idea was
  borrowed), OpenCreator (needs ChatGPT/API keys), huashu-art-motion (interactive art-animation skill, own engine;
  its QC ideas borrowed), diffusionstudio/editor (again: footage editor).
- Rejected after review: MoneyPrinterTurbo (needed keys), agent-reach (yt-dlp used directly),
  vox-director (paid cloud), hypit (framework replacement, paid default), KittenTTS (no word
  timings), VoiceStudio/Voicebox (GUI apps; Kokoro already used), video-shotcraft (product promos,
  16:9), diffusionstudio editor, LongCat-Video, LongLive.

## How to verify changes
- Owner's results: `logbook/<channel>.md`. Read it before advising on topics or hooks.
- `.venv\Scripts\python.exe -m py_compile make_shorts.py`; for Remotion: `cd remotion && npx tsc -p .`
- Full run: `.venv\Scripts\python.exe -u make_shorts.py 1 strange-history` (count, channel), then check
  `storyboard.jpg` and `edit_plan.txt`. Never test while the owner's batch runs (shared RAM/VRAM and
  `remotion/public/job`); check first for a running `make_shorts.py` process.
- Run single steps by importing `make_shorts` in a scratch script (call `use_channel("strange-history")` first, then e.g. `render(short, load_channel(), folder)`
  with a handwritten `short` dict) to avoid spending Claude usage.

## 2026-10-16 (Claude)
- **Wide clips fill more of the screen (owner: "make every short better")**: `FILM_VF` no longer fits the whole
  (already `FILM_CROP`ped) width into a ~490 px strip; the clip is scaled to a `FILM_BAND` = 1100 px tall band,
  sides trimmed to the centre (`crop='min(iw,1080)':ih`), over the blurred copy. A 16:9 clip keeps its middle ~45%.
  `graphic_low()` maps subject rows onto that band. Tested on 16:9, 4:3 and 4:5 test clips (all 1080x1920).
- **fix.bat bug fixed**: "use the picture from another scene" copied nothing when that scene was an AI painting
  (it only exists as `work/ai<k>.jpg`); `use_picture_from()` now copies the file, its prompt and its Gemini label.
- Owner's choice (2026-10-16): Gemini's unrestricted sourcing stays (any YouTube video, fair-use/NC/SA images,
  all of Internet Archive, credited on screen). Claude warned about strikes/YPP reused-content and was told not to
  restore the license rules. Gemini also added `FILM_CROP` (bottom 20% / top 6% / 4% sides) on all film.
- **2.5D parallax removed (owner, 2026-10-16: images "very distorted", esp. the intro)**: its depth warp bent the
  painted tower's beams and the men's hats in the Hatfield hook. `local_clips()` no longer calls the `parallax`
  job (gen.py still has it, unused); scenes without film/LTX/Veo get the renderer's flat zoom/pan. `to_vertical()`
  now cover-fills 9:16 (was: picture centred over a blurred copy), so stills stay full screen like parallax was.
- **New graphics (owner asked for more motion graphics, 2026-10-16)**, all Remotion (`remotion/src/Extras.tsx`),
  planned like the others and validated in `clean_graphic()`; the Python fallback shows them as fact boxes:
  `headline` (newspaper front page slams in; optional `paper` only if a real paper covered it, `date`),
  `quote` (real documented quote <= 12-14 words typed on aged paper, `by` required), `compare` (two bars:
  `a_label/a_value/a_show`, `b_...`), `stamp` (red rubber stamp, 1-2 words). Sounds in `sfx_events()` (stamp
  for stamp/headline, ticks for quote, whoosh for compare). All use `slot()` (move below a face). Tested: each
  rendered over the Hatfield pictures.
- **Music moods**: `music/<mood>/` with `MOODS` = mysterious, tense, playful, somber, epic; the planner returns
  `music_mood`; `render()` picks a random track of that mood (any track if the folder is empty). The 8 Kevin
  MacLeod tracks were sorted into mysterious/tense/playful/epic; somber is empty. state.json stores the music path
  relative to music/. Safest source for more tracks: YouTube Studio's Audio Library (no Content ID claims);
  incompetech (Kevin MacLeod, CC BY, credit in the `.mp3.txt` sidecar) also works.
- **Colour palettes (owner, 2026-10-16: not always yellow/navy)**: `PALETTES` (gold, ember, crimson, teal, sky,
  lime, rose, violet, parchment; each accent + emphasis + dark map panel, land/border derived; an assert keeps
  black-on-accent contrast >= 6:1). The planner returns `palette` (story-fitting), else `render()` picks one at
  random; it is saved in the plan, so fix.bat keeps it. Python: `YELLOW`/`EMPHASIS` globals are set per Short
  (fact boxes, person-card banner, ASS caption colours via `ass_colour()`, thumbnail text). Remotion: a shared
  `theme` object in Graphics.tsx that `Short` fills from `props.palette` before drawing (all cards, map, captions,
  caption glow). edit_plan.txt has a "Colours:" line. Tested: crimson/teal/parchment renders + Python fact box.
- **Shorter scripts (2026-10-16)**: 95-125 words (~40-50 s), 6-9 scenes; quality check flags > 62 s.
- **fix.bat option 4 "Paint a new picture"**: `paint_new()` drops the scene's picture/film, deletes `ai<i>.jpg` and
  lets render() paint it again (Gemini via agy when the channel's planner is Gemini, else SDXL) from its
  `ai_image` prompt, or one built from the shot note.
- **Automatic repaint**: `visual_review()` now also returns `repaint` (scene -> problem) for problems a different
  picture would fix; after the first render, `render()` repaints up to `AUTO_REPAINT_MAX` (4) of those scenes with
  `paint_new()` and re-renders once (`state` set, so it never loops; fix.bat re-renders don't auto-repaint).
  edit_plan.txt lists them under "Fixed automatically after the review of the first render". A full Short now
  takes a few minutes longer when this kicks in.
- **Argon quota (2026-10-16 test run)**: Argon appeared on the account and was picked automatically, then hit
  "Individual quota reached ... Resets in 165h" (weekly) during the picture-choosing call. Every picture job then
  failed over to Claude (choice/review) or SDXL (painting: weak results). Fixes: `run_agy(model=...)`; picture jobs
  (`ask_ai` with read_dir, `gemini_images`) always use Flash (`GEMINI_FALLBACK`); Argon is kept for text (script,
  fact check, SEO). On RESOURCE_EXHAUSTED for a non-Flash model, `run_agy` writes the reset time to
  `agy_tasks/argon_quota_until.txt` and retries on Flash; `gemini_model()` returns Flash until then. Tested live.
- **Gemini paints for either planner (2026-10-16, Voigt Short)**: with Claude as planner, AI images had gone to SDXL
  (US flag on a 1906 German town hall, faceless soldiers). `render()` now calls `gemini_images()` whenever `agy`
  is installed (Flash), SDXL only as backup. Stamp graphic: red ink now sits on a cream paper slip (red-on-brick
  was unreadable) and stamps over 8 letters use a smaller font.
