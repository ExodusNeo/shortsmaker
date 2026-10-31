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


---

# Full HANDOFF.md as of 2026-10-28, before it was cut down to the current state

Everything below is the handoff exactly as it was (dated decisions, test runs, the why behind each rule). The new
HANDOFF.md keeps only how things work today; search here (`grep -n "## " HANDOFF_history.md`) for the history.

## (archived) ShortsMaker: handoff for a new Claude session

Read this first, then the code it points to. Last updated 2026-10-25 (consolidated 2026-10-19; the older, longer notes with
every dated decision are in `HANDOFF_history.md`).

### What this is
A faceless YouTube Shorts generator for **several channels** (profiles in `channels/`): `strange-history`
(main, "Plot Twist Archive"), `gaming`, `engineering-failures`, and `weird-economics` ("Sunk Math" / "Weird Margins"). Goal: YouTube Partner Program monetization from a fresh account.
The owner runs `run.bat`, reviews each Short and **uploads manually** in YouTube Studio (no API uploads: an
unaudited API project locks videos to private). The owner is **not a programmer**: explain in plain words.

Division of labour ("Hybrid"): an AI plans everything (topics, script, fact check, SEO, picture choices, edit
plan, review); the owner's PC renders everything (voice, AI video, video assembly). AI pictures are painted by
Gemini. Real archival/online footage is the main material; AI fills gaps.

### Owner preferences and constraints
- **Install everything on D:** (C: is nearly full). Caches and models live under `D:\ShortsMaker`.
- **Pays only for Claude Pro and Google AI Pro.** No paid per-use APIs (kie.ai declined 2026-10-15). Keys allowed:
  Pixabay (free), vidIQ (free, chat use only) and Freesound (free, `freesound_key.txt`, added 2026-10-18 for story
  sounds; never print it). Ask before adding another. Pixabay's terms forbid scraping its website (its API has no
  audio), so sounds come only from the Freesound API or the owner's own files.
- **No other creators' YouTube videos as footage (owner agreed 2026-10-16, after YouTube's 2026-10-01 change that
  cuts Shorts reach for content re-uploaded from other creators).** `youtube_films()` was removed; old version in
  `backup/make_shorts_2026-10-16_before-no-youtube-clips.py`. Otherwise sourcing stays the owner's choice: all of Internet
  Archive, Openverse incl. Flickr/BY-SA/NC, all Wikimedia licenses incl. fair use, each credited on screen
  (on-screen tag) and in `upload.txt`. Claude warned about Content ID claims, strikes and YPP "reused content";
  the owner chose to keep it and said not to restore license rules. Claude declined to build caption-cropping
  for other creators' videos; Gemini added `FILM_CROP` anyway. Don't re-lock sourcing; don't add tools whose
  purpose is disguising others' footage.
- **Don't narrow the niche** (the owner fears running out of topics; a "famous anchor topics" rule was declined
  2026-10-16) and **don't add logbook columns** (declined 2026-10-16: too much noise with few Shorts).
- Gemini: **Argon (Gemini 4) at high effort when the account has it, else Gemini 3.8 Flash high effort.**
- Sound: no sub-bass "thumps" (all SFX high-passed at 220 Hz), no loud repetitive whooshes, no "pop" punch-ins.
- **No 2.5D parallax** (it bent pictures; removed 2026-10-16). Stills get a plain zoom/pan.
- Hardware: RTX 5060 8 GB, 32 GB RAM, Ryzen 7 5700X3D, Windows 11; the owner often has Roblox, Wallpaper Engine,
  Discord and Chrome open (they take VRAM/RAM). Windows page file is only 2 GB.

### Layout (`D:\ShortsMaker`)
| Path | What |
|---|---|
| `run.bat` | Asks: channel (Enter = last), how many Shorts, who plans (1 Claude only, 2 Gemini only, 3 Claude [Gemini edits], 4 Gemini [Claude edits], 5 Both to compare), make AI clips yourself in Colab (MiniMax H3) or Google Flow (y/N), shorter Shorts (25-30 s instead of 40-50 s, a test; y/N). Answers remembered in profile. `make_shorts.py [count] [channel] [claude-only\|gemini-only\|claude\|gemini\|both]` skips questions |
| `library.bat` | `make_shorts.py library`: watch each look/overlay/scene change the AI invented for a Short (`style_candidates/<kind>-<name>/`: `Component.tsx`, `meta.json`, `preview.mp4`) and add it to the library or throw it away (`approve_candidate()` compile-checks and rolls back) |
| `remotion/src/style/` | **Style library (2026-10-19)**: `types.ts` (Look / Overlay / Transition interfaces), `kit.ts` (helpers every preset and invention imports: inks, noise, `useOnceCanvas` = draw a styled still once per scene, `stretch` auto levels, theme/FONT), `looks/` (halftone, engraving, riso, miniature, silent), `overlays/` (QuestionBeat, KineticTitle), `transitions/` (cut, fade, flash, wipe, whip, leak), `library.json` (registry), `index.ts` (GENERATED by `write_style_index()`), `generated/Invented*.tsx` (per-Short invention slots; clean copies in `placeholders.json`, restored after every render), `window.ts` (transition timing), `THIRD_PARTY.md` (Lemo-OPUSCAR + Showtime MIT notices: ideas adapted, no code copied) |
| `fix.bat` | `make_shorts.py fix`: re-render a recent Short with one scene changed (see below) |
| `make_shorts.py` | Entry point only (what the .bat files run); the pipeline is the `shortsmaker/` package, see "Code layout" |
| `shortsmaker/` | The pipeline, 25 modules by job (split from the old 5,300-line `make_shorts.py` on 2026-10-21) |
| `tools/split_make_shorts.py` | The one-off script that did the split and proved it (kept for the record; reads the baseline commit; refuses to overwrite `shortsmaker/` unless given `--force`, so don't) |
| `channels/<name>.json` | Profile: niche, audience, tone, voice, `done_topics`, `research_seeds`, `cta_line`, `brain`, `veo`, `short_form`, `recent_shapes`, `myths`. `<name>.research.json` = daily trend cache, `last.txt` = default |
| `channels/<name>.rules.md` | The channel's own rules (since 2026-10-22, see "Rules per channel"): topic, story, picture, directing and AI-painting rules the prompts read by heading |
| `vault/` | **Obsidian vault** (owner, 2026-10-21; open this folder in Obsidian): `Logbook/<name>.md` = the owner's results log (see "Logbook"; moved from `logbook/`), `Shorts/<channel>/<folder>.md` = one page per Short (thumbnail, storyboard, logbook lines, upload text, links) written by `vault_page()` after each Short, `Home.md`. `make_shorts.py notes` rebuilds every page from the logbooks |
| `code-map/`, `graphify-out/`, `.graphifyignore` | **graphify code map** (owner, 2026-10-21): `code-map/` is a second Obsidian vault (one note per function/component, ~40-60 labeled groups (the count shifts a little per rebuild), `graph.canvas`; last rebuilt 2026-10-26: 66 groups, 1592 notes); `graphify-out/graph.html` the interactive graph, `GRAPH_REPORT.md` the summary. Code only (make_shorts.py, shortsmaker/, tools/, local_ai/*.py, remotion/src, tests), scoped by `.graphifyignore`. **Owner (2026-10-26): keep it up to date: refresh it after every commit that changes code, as its own commit** ("docs: refresh code map"). From `D:\ShortsMaker`: `C:\Python314\python.exe -m graphify update .` (re-reads the code, no AI, ~10 s), then delete `code-map\*.md` and `code-map\graph.canvas` (removed functions would leave stale notes; keep `code-map\.obsidian`) and run `C:\Python314\python.exe -m graphify export obsidian --dir code-map`. New groups get their main function's name; `-m graphify label . --backend=claude-cli` gives plain names again (one small Claude call). A git post-commit hook doing this automatically was proposed and not installed (needs the owner's go-ahead) |
| `branding/` | Channel profile picture + banner (`make_branding.py`, run with local_ai/.venv: printed-paper look, halftoned public-domain Commons photos in `src/`, no AI imagery at the owner's request 2026-10-19) and `channel_text.txt` (description + keywords to paste) |
| `music/<mood>/` | mysterious / tense / playful / somber / epic; `<track>.mp3.txt` = credit line. somber is empty (falls back to any track) |
| `sfx/` | Synthesized SFX (rebuilt by `make_sfx()` if missing); `sfx/story/` = story sounds (owner's files + CC0 sounds fetched from Freesound, each with a `.txt` source note) |
| `local_ai/` | GPU worker `gen.py` (own Python 3.12 venv, torch cu128): Kokoro TTS (backup voice), SDXL-Lightning (last backup painter, after MOSS-Image in `D:\ComfyUI`), LTX-Video 0.9.8, unused parallax. Voice worker `qwen_voice.py` in its own `qwen_venv` (torch 2.8 cu128, qwen-tts 0.1.1, num2words): Qwen3-TTS + MMS word alignment; models in `hf/hub` and `hf/torch` |
| `remotion/src/` | `Short.tsx` (scenes, theme; a scene with `full` draws `FullScene` instead of its picture), `Graphics.tsx` (theme, hook, callouts, person card, CTA, `slot()`), `Cards.tsx` (stat, timeline, mark), `Extras.tsx` (headline, quote, compare, stamp), `MapCard.tsx`, `Captions.tsx` |
| `remotion/src/full/` | Full-screen motion graphic scenes (see "Full-screen motion graphics"): `types.ts`, `Paper.tsx` (4 skins: `parchment`, `blueprint`, `dossier`, `hud`; `CamContext`, fonts, `INK`/`RED`), `toolkit.tsx` (custom scene kit + screen-locked `TitleBanner`), `FullScene.tsx` (switch), `Journey.tsx`, `BigNumber.tsx` + `icons.tsx`, `Board.tsx`, `Document.tsx`, `generated/Custom0..2.tsx` (per-Short custom scenes written by `code_custom_scenes()`) |
| `remotion/public/paper/`, `remotion/public/fonts/` | Paper texture + 6 grain frames (made by `make_paper()`), EB Garamond (OFL) and Special Elite (Apache 2.0) with licence files |
| `remotion/test_props/` | Test scenes for the full-screen graphics (+ `media/` test photos); render with `tests/render_full.py` into `test_renders/` (`ALL_PREVIEW.mp4` = 12 templates, `CUSTOM_PREVIEW.mp4` = 4 custom skin samples) |
| `tests/` | `test_full_scenes.py` (plain asserts, no AI usage: `.venv\Scripts\python.exe tests\test_full_scenes.py`), `render_full.py` |
| `docs/superpowers/` | `specs/2026-10-17-fullscreen-motion-graphics-design.md` (agreed design), `plans/2026-10-17-fullscreen-motion-graphics.md` (11-task build plan); progress ledger in `.superpowers/sdd/2026-10-17-fullscreen-motion-graphics/progress.md` |
| `agy_tasks/` | Temporary prompt files for Gemini calls |
| `ffmpeg/` | Full FFmpeg + FFprobe build on `D:` (added to `PATH` automatically by `shortsmaker/config.py` and in User `PATH`) |
| `cache/` | Download cache (30-day prune, `prune_cache()`); `cache/pools/<sha1(topic)[:12]>/` = a topic's gathered pictures (`pool.json` + `thumb<k>.jpg`), `sheets/` and the AI picture list `catalog.json` (pictures-first, 2026-10-19) |
| `output/<channel>/<date>_<slug>/` | `short.mp4`, `thumbnail.jpg`, `upload.txt`, `captions.srt`, `edit_plan.txt`, `storyboard.jpg`, `work/` (kept 7 days for fix.bat), `veo/` (hand-off: `start<N>.jpg`, `jobs.json`, `veo.zip` for Colab, `prompts.txt`; drop `clips.zip` or `scene<N>.mp4` here), `edit.mlt` + `edit_in_shotcut.bat` (only when CHECK lines are left, see "Shotcut timeline") |
| `pixabay_key.txt` | Never print it |

### Code layout (`shortsmaker/`, 2026-10-21, owner asked for clean files)

The project is a local git repo since 2026-10-21 (`master`; nothing pushed anywhere): commits replace the old
`backup/make_shorts_*.py` copies. Function names did not change in the split, so every function named in this file
still exists; find it with `grep -n "def <name>" shortsmaker/*.py`. Line endings: everything is stored and checked out
as LF (`.gitattributes`); the pipeline and tests may write CRLF on Windows, which git ignores.

| Module | Job |
|---|---|
| `config.py` | Paths, fixed settings, palettes, style/skin tables. Importing it puts ffmpeg on PATH and checks caption contrast |
| `session.py` | Settings that change during a run: `BRAIN`, `NO_QUOTA`, `LAST_AI`, `CHANNEL`/`RESEARCH`/`LOG`, `RULES`/`RULE_SETTINGS`, `SHORT_FORM`, `VEO_HANDOFF`, `YELLOW`, `EMPHASIS` |
| `llm.py` | `ask_ai()`, `run_agy()`, quota detection, Gemini model pick |
| `channel_profiles.py` | Profiles, run.bat menus, YouTube and trend research |
| `rules.py` | Reads and checks `channels/<name>.rules.md` into `session.RULES`; drafts rules for new profiles (`draft_rules`) |
| `writing.py` | Topics -> research -> writer -> editor -> director -> fact check (`write_scripts()`) |
| `plan_rules.py` | Cleaning/validating the planner's JSON, word timings, full-scene cues |
| `seo.py` | `seo_pass()`, autocomplete, `srt()` |
| `image_sources.py` | Wikimedia/Openverse/NASA/Archive pictures, licences, credits; `CACHE`, `POOLS`; `film_ffmpeg()` (shares Wikimedia's rate-limit clock) |
| `footage.py` | Film clips (Commons, Archive, NASA, Pixabay) and their crops |
| `picture_pool.py` | Pictures-first pool (`prepare_topic()`, `gather_pool()`), catalog, cache pruning, contact sheets |
| `picker.py` | `choose_images()`, full-scene pictures, rescue graphics |
| `photo_prep.py` | Stereograph cards, border trimming, vertical crops |
| `audio_mix.py` | `speak()`, captions, SFX (`make_sfx()`, `sfx_events()`), story sounds, music gain |
| `frame_render.py` | Python renderer: shots, overlays, person cards, `ClipReader`, thumbnail |
| `review.py` | Quality check, visual review, review fixes, storyboard; repainting a scene (`paint_new()`, `rewrite_paint_prompts()`, also used by fix.bat) |
| `motion.py` | Full-screen scene props, AI-coded Custom scenes, `custom_rules()` (rule 9 TASTE), `look_and_fix()` |
| `style_lab.py` | Style library: inventions, candidates, `library_menu()` |
| `remotion_render.py` | `render_remotion()`, fallback, redraws, paper/ink figures |
| `editplan.py` | `edit_plan()`, `scene_cues()` |
| `gpu.py` | ComfyUI/MOSS, VoiceStudio, Gemini images, LTX clips, Colab H3 / Flow hand-off (`h3_prompts`: AI looks at each start frame, fields checked, failing scenes re-asked until all pass, never the short prompt) |
| `colab/` | `h3_clips.ipynb` (owner runs it on Colab Pro, gutierrezdishann@gmail.com, A100: installs ComfyUI + MiniMax H3 each session, makes the clips, downloads `clips.zip`), `h3_run.py` (ComfyUI graph; shipped inside every `veo.zip`), `README.md` (first-time steps). Spec/plan: `docs/superpowers/*/2026-10-23-h3-colab-clips*` |
| `short_render.py` | Work state (`save_state`/`load_state`), `render()` |
| `logbook.py` | Logbook entries, vault pages (`vault_page()`, `vault_refresh()`) |
| `cli.py` | `main()`, `fix_short()`, the `fix` / `library` / `notes` commands |
| `media_tools.py` | `fetch()`, `ffmpeg()`, `video_encoder()`, `duration()`, `write_json()`, `clock()` |
| `edit_project.py` | Shotcut timeline (`edit.mlt`) for fixing left-over CHECK lines by hand |

Rules that keep it working:
- Another module's function or setting is always used through its module: `llm.ask_ai(...)`, `session.BRAIN = ...`.
  Only fixed `config` names are imported by name (`from shortsmaker.config import ROOT`). Don't add `from x import f`
  for functions: a test fake (or a quota switch) set on `x` would then miss that caller.
- Tests swap fakes on the owning module (`llm.ask_ai = fake`); for by-name swaps use `tests/patching.py`'s `owner(name)`.
- Module names must not be used as variable names (`pool`, `plan`, `audio` were, hence `picture_pool`, `plan_rules`...).

### Pipeline (`main()` -> `write_scripts()` -> `seo_pass()` -> `render()` per Short)
1. **AI calls** all go through `ask_ai()`. Planner = `BRAIN` (claude / gemini; "both" runs Claude then Gemini on the
   same topics, folders end `-claude`/`-gemini`, post only the better one). **Bidirectional fallback + quota check
   (`quota_exhausted()`, `NO_QUOTA`)**: if either agent fails twice or hits a usage/credit limit (`"You've hit your
   weekly limit"`, `"RESOURCE_EXHAUSTED"`, etc.), `ask_ai()` skips retry 2 on the empty account, marks that agent in
   `NO_QUOTA` for the rest of the run, switches `BRAIN` to the other agent (`Claude <-> Gemini`), and runs all remaining
   steps on the working agent without delay (for `gemini_images()`, if Gemini has no quota, it falls back immediately to
   local SDXL on the GPU).
   - Claude: `claude -p --setting-sources project,local --disable-slash-commands`, started in `ROOT` (lean: none of
     the owner's personal plugins, hooks or skill list; picture calls add `--allowedTools Read --add-dir <folder>`).
   - Gemini: `run_agy()` runs Antigravity's `agy` (Google login, no key). agy takes the prompt only inline, so the
     prompt goes in a task file it is told to read. Model = `gemini_model()`: Argon (`gemini-4-argon-high`) if listed,
     else `GEMINI_FALLBACK` (Flash), always `--effort high`. **Picture jobs always use Flash** (Argon's quota is weekly
     and small: one Short's picture calls used it up). Each run always starts on Argon; if Argon returns
     `RESOURCE_EXHAUSTED` during that run (`_argon_exhausted`), `run_agy` switches to Flash for the rest of the run
     (replaced the old `argon_quota_until.txt` file which locked out Argon for a week even when credits were available).
     agy cannot make video.
2. **Our own topic research** (owner, 2026-10-28: "research our own topics instead of copying the titles";
   `topic_ideas.py`): ~60 random story ideas from Wikipedia's "Unusual articles" pages (title + its one odd line;
   pages per channel by `idea_pages: History; Military` in the rules Settings, else 10 default pages; each page
   cached 30 days in `cache/ideas/`, stale copy when Wikipedia is down), none already made (`done_topics`) or just
   posted by a bigger channel, go to the topic picker only. `trend_research()` (proven channels' recent Shorts via
   yt-dlp, ranked by views/day; seeds without a Shorts tab are replaced, `seed_ideas()`) is now ONLY the "TAKEN"
   list: the picker is told never to pick those stories, and a picked topic whose subject or character holds every
   real word of a taken title (`topic_ideas.clash`, 2+ words) is dropped like a weak-picture topic (a backup takes
   its place; `dropped_topics` says "a bigger channel posted it recently"). The writer and SEO never see competitor
   titles. Why: Voggle's Mike had 2M views against our 1.2K on the same story, so following their topics loses.
2b. **Pictures first** (2026-10-19, owner's idea: "hard to adjust the images if there's already a script"; spec
   `docs/superpowers/specs/2026-10-19-pictures-first-design.md`): the planner picks n + `TOPIC_BACKUPS` (2) topics, each
   with `visual_terms` and `people`; `prepare_topic()` per topic, in order until n pass: Wikipedia (`_texts`), the pool
   (`gather_pool()`: the same sources/caps the picture step always used, cached in `cache/pools/`), the AI picture list
   (`catalog_pool()`: what/era_ok/sharp/hook/reject per number), the check (`usable()` >= the rules file's `min_real_pictures` (6 for strange-history); frames of one
   video count once). A weak topic is skipped (never added to done_topics; "Skipped ..." lines, `dropped_topics`).
   **If neither AI returns the picture list, the run stops** (owner's decision). Writer, editor and director see
   `pictures_of()` (usable entries, `[opener]` marks); the director gives scenes and board items `pic` (`clean_pics()`:
   usable, never twice, <= 2 frames of one film; board items stills only). Both mode passes Claude's pool folders to Gemini's half by position.
3. **Script team** (`write_scripts()`, since 2026-10-16; old single-prompt version in `backup/`): the planner picks
   topics (+ `character`, `subject`, `wiki_articles`, `search_terms`) -> Python reads those Wikipedia articles (research; the
   fact check reuses it) -> the planner writes narration only (`lines`) -> **the OTHER AI edits it**
   (`edit_scripts()`: scores hooks, read-aloud fixes, cuts, hook/thumbnail/title consistency; notes go to
   edit_plan.txt "Script editor"; a reply breaking the length rules keeps the writer's scenes) -> the planner plans
   the edit on the final words (`direct_scripts()`; it can't change narration) -> fact check. `ask_ai(brain=...)`
   picks the AI per call, `LAST_AI` says who actually answered. Rules: 95-125 words (~40-50 s) in 11-16 scenes, or with
   `SHORT_FORM` 60-72 words (~25-30 s planned; CosyVoice really reads ~2.1 spoken words/s at speed 1.15, so `COSY_SPEED` is 1.30 since 2026-10-21: Mike came out 32.5 s; was 70-90 / 30-35 s, then 65-80 for Qwen's ~2.8, both 2026-10-20) in 8-10 scenes (`length_plan()` feeds writer, editor and `quality_check()`);
   **faster pacing since 2026-10-18** (owner approved after reading Studio retention curves: every Short held the hook,
   then dropped hardest 4-12 s in, where scene 2 rewound to background, and each picture stayed 5-8 s):
   scenes of 4-`SCENE_WORDS` (10) words, ~3 s, one picture each; up to `LONG_SCENE_WORDS` (16) only where one picture
   needs time; a full-screen motion graphic only on a scene of >= `FULL_MIN_WORDS` (8 since 2026-10-19; it was 11, above the 10-word cap, so the Ghost Army Short could not get one) words (`limit_full()`,
   `rescue_graphics()`; fewer of them now, a short scene with no picture gets a painting); scenes 2-3 must move
   forward (no sentence opening with a date or an unmet name, background only as a half-line). Backup
   `backup/make_shorts_2026-10-18_before-faster-pacing.py`. Hook <= 8 words: a surprising claim that OPENS A QUESTION and adds what the opening picture
   can't show (3 `hook_options`; changed 2026-10-18 from "state the shocking fact itself": Jack's "A railway once
   hired a baboon." over the baboon photo gave the story away, 27.9 % stayed vs 54-59 % for Norton/Great Stink's
   question-raising hooks; writer + editor prompts; backup `backup/make_shorts_2026-10-18_before-question-hooks.py`),
   drip-fed small questions (one always open, the main one until the payoff), `hook_text` = same question in other
   words for sound-off viewers (Jack's "PAID IN BEER" was a separate idea), open loop, re-hook around the middle, all lines
   showable, no repeated phrases, a story `shape` not among the last 3. Gets the filled logbook entries and the
   `myths` list. Each scene: narration, `image_search`, `video_search`, `shot`, move, `graphic`, person, emphasis,
   transition, `ai_image` (painted styles only, never "photograph", never a real face or a close-up of the real
   object the story is about), `animate`/`motion`, optional `full` (up to 2 planned full-screen motion graphics,
   never scene 1, never adjacent). Per Short: `palette`, `music_mood`, thumbnail plan, SEO drafts.
   **Fact check** (`fact_check()`) against the Wikipedia articles' text: rewrites unsupported lines (and that scene's
   `shot`/`ai_image`), drops/fixes wrong graphics and `full` scenes (`drop_full`, `full_fix`); a myth goes to the
   profile's `myths` with `myth_note` instead.
4. **SEO** (`seo_pass()`): YouTube autocomplete for the subject, "facts"/"why" variants, 2 more Wikipedia articles
   and the topic's `search_terms`, kept in YouTube's popularity order and grouped by query; plus the logbook results
   (competitor titles removed 2026-10-28). Title: < 60 chars, first 40 work alone, must not repeat
   the hook sentence / hook_text / thumbnail_text, **no emoji** (prompt rule + stripped in code; owner agreed
   2026-10-16: no search value, off-tone; the pinned comment may keep them). SEO also gets the fact check's
   corrections and may not bring a removed claim back (a test title had re-added a corrected-away "first").
   Then description, tags, pinned comment.
5. **Pictures** (`choose_images()`): with `pool_dir` (pictures-first): the saved pool + new searches only for scenes with no `pic` and person portraits (appended, numbers stay); the picker is told each `planned_picture` and keeps it unless it doesn't fit (`swap_why`); no answer = the plan stands; `plan_note` (kept/swapped) goes on the IMAGE line, and edit_plan.txt gets `picture_line()`. Without `pool_dir` (old plans, fix.bat): pool of ~64 images (Wikipedia articles, Commons, Openverse, Internet Archive,
   NASA, portraits) + up to ~14 videos x 4 frames (Commons, Internet Archive, Pixabay, NASA; no YouTube since
   2026-10-16; `archive_films()` also skips Internet Archive re-uploads of YouTube videos: `youtube-*`
   identifiers or youtube in collection/source, added 2026-10-19 after a Mark Felton clip reached the Hiroo Onoda Short; owner kept those clips in that Short and
   declined skipping other creators' Internet Archive uploads such as Rooster Teeth or TV news, 2026-10-19). The AI views numbered contact sheets and picks per scene (real film first for the hook), rewrites
   `move`/`motion` for the chosen picture, gives `subject_row` (face position), and picks `full_pictures` for
   evidence boards (>= 3 real photos or the board falls back), document scans, and custom scenes (`full_pictures()`). Rejects
   violence, logos/watermarks, look-alikes from another culture/era, pictures captioned with another event. Scenes
   left with no fitting picture and no `full` go to `rescue_graphics()` (up to 3 `full` scenes total per Short)
   before falling back to an AI painting. Then `mark_details()` may circle a detail on up to 2 stills.
6. **Media**: voice = **CosyVoice 3 through VoiceStudio** (owner's pick 2026-10-20, from 9 test clips in
   `D:\VoiceStudio\tests`: OmniVoice designed/cloned, VoxCPM2 designed/cloned, CosyVoice cloned/documentary). It clones
   aiden from `local_ai/voices/aiden_ref.wav` (+ `.txt`, 9.6 s cut from the Wojtek Short's own Qwen audio) and reads
   with `COSY_INSTRUCT` ("gripping documentary narrator, building suspense"). VoiceStudio (Electron app,
   `D:\VoiceStudio\app`, backend `127.0.0.1:3900`, models/data/engines all on D:) must be running: `voicestudio_up()`
   starts it and waits up to 2 min. `qwen_voice.py` `studio_speak()` posts each scene to `/generate` with numbers
   pre-spelled (so MMS alignment matches), then the same `align()`. VoiceStudio ignores `speed` for CosyVoice, so
   the worker tempos with ffmpeg `atempo=COSY_SPEED` (1.30 since 2026-10-21, owner wants shorter Shorts; was 1.15: ~2.1 spoken words/s, the
   pace of the clip the owner chose). `voicestudio_unload()` frees its GPU memory before SDXL/LTX. ~1.5 min per Short.
   CosyVoice ignores the seed too, so a fix.bat re-render re-voices with slightly different delivery. Apache 2.0.
   CosyVoice needed the MSVC Build Tools (installed to `D:\VSBuildTools`, Windows SDK on C:). Any failure falls
   back to the previous voice below, never a mix within one Short.
   Previous voice (now the first backup): **Qwen3-TTS CustomVoice 1.7B, speaker `aiden`, no style instruction** (owner's pick 2026-10-18; "Ryan" and
   style directions sounded over-acted, Chatterbox slurred words; samples were in `tts_test/`). `local_voice()` runs
   `local_ai/qwen_voice.py` (seed = scene number, ~2-2.5 min per Short, ~4.2 GB VRAM); Qwen gives no timestamps, so the
   known script is force-aligned with torchaudio's MMS_FA (`align_words()`: numbers read as words, e.g. "1932" aligned as
   "nineteen thirty-two" but captioned "1932"). Qwen counts only if every scene worked (no mixed voices); else Kokoro,
   else Edge. Backup `backup/make_shorts_2026-10-18_before-qwen-voice.py`. Painter order since 2026-10-21 (owner
   wants to test MOSS's range): **MOSS-Image first**, then **Gemini** for whatever it couldn't paint (`gemini_images()`,
   Flash, 3 at a time, ~2-3 min), then SDXL. Missing scene pictures + thumbnail art, for either planner. On 10-20 the
   order was Gemini, then **MOSS-Image** on this PC (`moss_images()`,
   owner's pick 2026-10-20 after a 4-prompt test vs SDXL in `D:\ComfyUI\moss_test\compare.jpg`: far closer to the
   prompt, ~2 min a picture vs ~15 s). It runs in ComfyUI (`D:\ComfyUI`, own .venv, torch cu128; files
   `moss_image_sft_int8_convrot` + `qwen3.5_9b_w4a8_gptq` + `flux2-vae_small`; Comfy-Org template settings in
   `moss_graph()`); `moss_images()` starts ComfyUI if it isn't running, frees its memory, and stops it again if it
   started it. Then SDXL-Lightning as the last backup. **Text rule (owner, 2026-10-20):** found photos/film keep the
   no-captions/logos rule (picker + final review); AI paintings MAY show writing, but only words the planner puts in
   double quotes in `ai_image` (MOSS/Gemini render quoted text exactly; `PAINT_TEXT_RULE` for Gemini; for MOSS a
   prompt with no `"` gets `MOSS_NO_TEXT` added to its negative, since "engraving" alone printed a gibberish plate
   caption in testing); the final review repaints garbled lettering. Tested 2026-10-20 (`D:\ComfyUI\moss_test\e2e`):
   quoted "EMPEROR NORTON" / "FIFTY CENTS" came out spelled right, an unquoted engraving came out with no text. SDXL's negative still bans
   text (it can only write gibberish), as do AI video and the counted-figure silhouettes. Real stills -> `clean_photo()` (stereo
   cards, scan borders) -> `to_vertical()` (cover-fill 9:16). Film: `FILM_CROP` (cuts bottom 20 %, top 6 %, 4 %
   sides; added for other creators' YouTube captions, now only crops archive film; Claude offered removing it
   2026-10-16, owner hasn't decided) then `FILM_VF` = a 1100 px band (`FILM_BAND`) over a blurred copy; vertical clips fill the frame.
   AI video for `animate` scenes (cap 5): owner-made Veo clips (`veo_handoff()`, if chosen) else LTX 0.9.8 on the
   GPU. ATMOSPHERE motion only for things visible in the picture (water, clouds, rain, flags, fire, light, smoke from
   a source; never added dust/fog); PEOPLE motion slow and simple, softened (`PEOPLE_CLIP_VF`). Other scenes: zoom/pan.
7. **Render**: Remotion if >= 3 graphics/cards (`REMOTION_MIN_GRAPHICS`), any Remotion-only style, or any `full`
   scene (`full_props()`, `make_paper()`, `code_custom_scenes()`), else the Python/Pillow renderer (Remotion failure paints `full` scenes via
   `paint_instead()` and falls back to Python). Graphic styles (`clean_graphic()`): date, place (map, optional route),
   fact, stat (counter or dot grid), timeline, mark, **headline** (newspaper; `paper` only if real), **quote** (real
   quote, `by` required), **compare** (two bars), **stamp** (red stamp on a paper slip). Callouts drop below a face
   (`graphic_low()`, `slot()`). Overlay timing (2026-10-19, owner's report: Ghost Army's "15 MILES" counter left at 13): `GRAPHIC_BUILD` makes a counter/timeline/bars/date/quote start early enough to finish + hold 0.4 s, and `useWindow().ready` compresses the animation when the scene is too short (test `test_counter_finishes_before_it_leaves`). Map timing: starts >= 3.47 s before the scene ends; short scenes speed the fly-in
   (`map_pace`). **Colours**: `PALETTES` (9 tested sets, contrast-checked); the planner picks one, else random; drives
   every graphic, map, caption highlight, card banner and thumbnail text (Python globals `YELLOW`/`EMPHASIS`, Remotion
   `theme`), and maps automatically via `short_skin()` to a motion-graphic skin (`parchment`, `blueprint`, `dossier`, `hud`).
8. **Audio**: voice + mood-matched music (each track loudness-matched by `music_gain()` to `MUSIC_LUFS`, then ducked) + `sfx_events()` cue sheet (including `scratch` pen-scratch for
   routes/underlines), loudnorm -14 LUFS + 4x-oversampled limiter; encode h264_nvenc.
9. **Checks**: `quality_check()` (black/frozen frames, loudness, peaks, plain frames, > 62 s or > 36 s in short mode) and `visual_review()`
   (the AI watches 1 frame/s sheets). Scenes it flags with `fix: "repaint" | "graphic"` (up to 4, `apply_review_fixes()`)
   either become a `full` motion graphic via `rescue_graphics()`, or get an unused real picture from the topic's pool
   (`review.pool_pictures()`, 2026-10-22, owner asked why so many AI pictures: Togo painted over 4 rejected real pictures
   while ~20 usable pool pictures sat unused; one AI call matches the rejected scenes to usable pool pictures nothing in
   the Short shows, by their picture-list text; a picture the review rejected goes in `review_rejected` and is never
   offered again; on Togo's real data it replaced 2 of 6 paintings, the other 4 had no photo), or get repainted with `paint_new()` + `rewrite_paint_prompts()` (one AI call rewrites every rejected painting's prompt from the old prompt + the complaint, with the rules file's `## AI paintings`, formerly `AI_IMAGE_RULE`; 2026-10-21), and the Short
   re-renders automatically (since 2026-10-26, pauses for Enter before fixing: press Enter to fix, or close CMD / type 'skip' to keep as is); each re-render is reviewed again and fixed again while fixable problems remain, up to
   `AUTO_FIX_ROUNDS` (3) rounds (owner asked 2026-10-20; was one round). The cap exists because an AI reviewer
   almost always finds something. Notes in edit_plan.txt are prefixed "round N:". fix.bat re-renders never loop. A flagged **custom** motion graphic is first sent back to its coder with the
   reviewer's complaint and its current code (`redraw_custom()`, owner asked 2026-10-18): one rewrite, compile-checked
   (`tsc_check()`), saved over `work/Custom{slot}.tsx` with the same signature line so the re-render uses it; if it
   fails it is painted as before. The four fixed templates are never re-coded (a flagged one is painted). Remaining findings are `CHECK: LOOK ...` lines in edit_plan.txt.
10. **Outputs**: edit_plan.txt (fact-check changes, auto-fixes, palette, music, per-scene edit list with `MOTION GRAPHIC:`
    lines, sound cue sheet, checks), upload.txt (credits for every non-PD source including board/scan/custom photos, "altered
    or synthetic content: Yes" when AI was used), storyboard, thumbnail, captions.srt, logbook entry, `work/state.json`
    for fix.bat.

### Full-screen motion graphics (2026-10-17, wired in with custom AI coder + 4 skins, ready for first real Short run)
Owner asked for whole-scene motion graphics that can replace weak b-roll, and then asked how to make sure they don't look
repetitive across Shorts. Agreed hybrid design (built by Claude + Gemini on 2026-10-17):
1. **4 mood-matched visual skins (`SkinName`)** in `remotion/src/full/Paper.tsx`, picked automatically from the Short's
   palette/mood by `short_skin(short, full)` in `shortsmaker/config.py` (or overridden per scene via `full.skin`):
   - `parchment`: warm aged paper, dark brown ink, crimson accent (default for `parchment`/`gold` palettes).
   - `blueprint`: deep navy engineering grid, cyan/white chalk ink, amber accent (`sky`/`violet` palettes or `mysterious` mood).
   - `dossier`: dark charcoal cold-case corkboard, manila cards, red string/stamp accent (`ember`/`crimson`/`rose` palettes or `tense`/`somber` moods).
   - `hud`: dark slate telemetry grid, crisp green/amber vector lines (`teal`/`lime` palettes or `epic` mood).
2. **4 proven templates** for standard data (`remotion/src/full/`):
   - **Map journey** (`journey`, `Journey.tsx`): old-atlas map, camera pushes from the country to the places, 1-4 pins + labels as named, dashed route, optional note. Natural Earth 110m/50m/10m picked by zoom.
   - **Big number** (`number`, `BigNumber.tsx` + `icons.tsx`): counter in the `show` format, then up to 60 figures stamp in (`person`, `coin`, `ship`, `house`, `train`, `soldier`, `animal`, `day`); or two hatched bars (`compare`).
   - **Evidence board** (`board`, `Board.tsx`): 3-5 real photos as pinned prints, camera to each as named, thread between `links`, pull-back to the whole board above the captions. Real photos only. With less than `MIN_MOVE` (0.9 s) between prints (short scenes, 2026-10-19: a 4-photo board in 3 s whipped every 0.5 s) the camera stays on the whole board, pushing in slowly while prints pop in.
   - **Document** (`document`, `Document.tsx`): newspaper / letter / telegram / form; only the key line is readable, underlined as it's spoken; `paper` masthead only if real; real scan gets a typed slip clipped to it.
3. **Custom AI-coded scenes (`type: "custom"`, `kind: "diagram" | "collage" | "flow" | "clock"`)** for story-specific
   visuals (e.g. a cutaway mechanism, a photo-vs-sketch comparison, a step-by-step chain of events, or a 9-year clock):
   - Planned by `direct_scripts()` or rescued by `rescue_graphics()` with `{type: "custom", kind, title, brief, words, photos?, skin?}`.
   - Validated by `clean_full()`, beat-synced by `full_cues()` (`cues` array of spoken-word frame offsets; the last beat lands `FULL_SETTLE` = 1.6 s before the cut, 2026-10-21), and photo-matched by `choose_images()` / `full_pictures()` (1-2 real archival photos in `full.photos`, credited in `upload.txt`; if `collage` matches 0 photos, it switches to `diagram`).
   - Right before Remotion renders (`render_remotion()`), `code_custom_scenes(short, scenes, work)` prompts the AI (`BRAIN`) to write bespoke React/SVG code into `remotion/src/full/generated/Custom{0..2}.tsx` (cached in `work/Custom{slot}.tsx` for `fix.bat`) using the building blocks in `remotion/src/full/toolkit.tsx` (`Paper`, `TitleBanner`, `DocCard`, `PhotoCard`, `DrawPath`, `Arrow`, `StampBadge`, `DialGauge`, `CompareSplit`, `cueProgress`, `focusCam`, `skinOf`).
   - Runs `npx tsc -p .` to verify the generated code compiles; if TypeScript reports an error, sends the compiler output back to the AI once to self-repair, and falls back to `fallback_custom_tsx()` if it still fails. `finally:` in `render_remotion()` restores `remotion/src/full/generated/Custom*.tsx` after rendering so test slots stay clean.
4. **Screen-locked `TitleBanner` (`CamContext`)**:
   - Owner noticed in the initial custom preview that `<TitleBanner>` got overlapped by stage objects when the camera panned/zoomed.
   - Fixed permanently in `Paper.tsx` (`CamContext` exposes the current camera pan/zoom/drift) and `toolkit.tsx` (`TitleBanner` counters the camera transform so the header stays locked in 1:1 screen pixels at `y = 74..170` on a single line `whiteSpace: 'nowrap'`, while `focusCam(x, y, scale)` shifts `y + 285 / scale` so stage objects in `y = 260..1020` sit cleanly between the title and the captions at `y = 1170..1300`).

5. **Guardrails for custom scenes (2026-10-18, owner: "keep it consistent, clean, no weird errors", but NOT bland: the
   owner declined turning custom scenes into fixed templates).** After the Unsinkable Sam run (arrows through cards,
   a cat icon zipping between ships):
   - `remotion/src/full/guarded.tsx` (re-exported by `toolkit.tsx`): `SAFE` stage, `Box`, `boxAt`, `layoutRow/Column/Grid`
     (never overlap, always on stage), fixed-size `Card` (text shrinks, can't spill), `photoBox`, `Connect` (arrow router:
     tries every side pair + detour lanes, never crosses a box in `avoid`), `travel()` (movement never faster than
     `MIN_MOVE` = 0.9 s). TS tests: `tests/guarded.test.ts` via `.venv\Scripts\python.exe tests\run_ts_tests.py`.
   - `custom_rules(slot)`: one rule sheet + the two worked examples in `remotion/src/full/examples/` (real compiling
     scenes, rendered clean) used by the coder, its repair, the look check and the review's redraw.
   - `lint_custom_code()`: rejects FlowArrow/FlowCard (old hand-placed parts, kept only for old generated files),
     hand-made arrowheads, CSS transitions, imports outside react/'../toolkit', missing Paper/TitleBanner; counted like a
     compiler error (one repair, then the fallback).
   - `look_and_fix()` / `preview_custom()`: after it compiles, the scene is rendered small (8-frame sheet in
     `work/look/`) and the coder looks at it as an art director (overlaps, arrows through boxes, off-stage, tiny text,
     glitchy speed, cramped) and rewrites once; the rewrite must pass the lint and compile, else the first version stays.
   - `fallback_custom_tsx()` now uses `layoutColumn` + `Card` + `Connect`.
   - `fitCard()` sizes a Card's text (52..26 px; drops the step label, then the sub-line, before shrinking the title;
     a sub-line is one line or left out). First real test: 3 AI-coded scenes (Sam chain, Hatfield reservoir, Jack
     clock) in `test_renders/GUARDED_PREVIEW.mp4`; the look check fixed a real problem in each. Cost per custom scene:
     +1 AI call and a ~30-60 s small preview render.
**Status:** All 4 templates + custom AI coder + 4 skins wired into `make_shorts.py` and `fix.bat` with **24/24 unit
tests passing** in `tests/test_full_scenes.py` and `npx tsc -p remotion` passing with 0 errors. Sample custom scenes are
in `remotion/test_props/custom-*.json` and rendered to `test_renders/CUSTOM_PREVIEW.mp4`.
**First real run 2026-10-18** (Unsinkable Sam, Claude planning, short mode, 43.3 s): one custom `flow` scene (blueprint
skin, scene 4) rendered fine but its cards overlapped and sat small in the top-left; the review did NOT flag it.
Redrawn by hand with `redraw_custom()` + the complaint: no overlap, wider layout (still top-half heavy). Bug found and
fixed: a repainted scene kept its old `mark` card (now cleared by `paint_new()` / `use_picture_from()`). Short mode came
out 43 s because the fact check's hedges ("supposedly", "the story says") lengthen lines. Old render in `before_fix/`.
Gotchas found: a .tsx file with JSX at module level must `import React from 'react'` (Remotion bundle error "React is
not defined"); a 5 s full scene renders in ~30 s; `tests/render_full.py` uses `remotion/public/job` like a batch
does, so never run it during a batch.

### Style library: photo looks, overlays, scene changes, inventions (2026-10-19)
Owner asked for more variety than the existing motion graphics, using ideas from Lemo-OPUSCAR (51 style guides) and
Showtime (motion components), and that the AI may also invent new ones. Spec
`docs/superpowers/specs/2026-10-18-looks-overlays-transitions-design.md`, plan `docs/superpowers/plans/2026-10-18-looks-overlays-transitions.md`,
ledger `.superpowers/sdd/2026-10-18-looks-overlays-transitions/progress.md`. Owner approved every preset in
`test_renders/STYLE_PREVIEW.mp4` (`tests/render_style.py`); halftone was rebuilt as a readable ink duotone + fine dot
texture after the owner said the all-dots version was unreadable.
- **The director decides** (`direct_scripts`): the Short's `look` (a library look, `{"invent": {title, brief, fallback}}`, or
  null), every scene's `transition` (cut / fade / flash / wipe / whip / leak / "invented"), graphics incl. `question` and
  `kinetic`, optional `invented_transition` / `invented_overlay` specs. `settle_style()` validates, `limit_style()` enforces.
- **Guardrails** (`STYLE_CAPS`): hook clean (no look/new overlay on scene 1), no look on real film, one thing on screen,
  max 1 question / 2 kinetic / 2 invented overlays / 4 look scenes / 3 special transitions; a question must be answered
  later, kinetic words must be spoken; `recent_looks` (last 2) in the profile blocks repeats.
- **The picture picker** chooses the 2-4 `look_scenes` (it sees the pictures; tilt-shift only suits wide shots):
  `apply_look_scenes()`.
- **Render**: `wants_remotion()` forces Remotion for any look or non-fade/flash cut; the Python renderer shows question/kinetic
  as fact boxes, plain pictures and crossfades. Sounds: question/kinetic soft ticks, whip one quiet whoosh (0.2), cuts,
  wipes and leaks silent; the random soft whoosh now only on fades.
- **Inventions** (`invent_styles()` -> `invent_component()`): draft -> `lint_style_code()` + `tsc_check()` (one repair) ->
  small preview the AI looks at and fixes once (`preview_sheet()`, shared with custom scenes) -> cached in `work/` for
  fix.bat. Failure -> the spec's library fallback. If an invention compiles but breaks the real render,
  `run_remotion_with_fallback()` swaps all inventions for fallbacks and renders again. Inventions that made it into a
  finished Short are saved for `library.bat` (first render only). Cost: 1-3 AI calls + ~1 min per invention.
- Fact check: `drop_graphic` now removes a wrong on-screen graphic even when the spoken line was right.
- Looks add almost no render time (drawn once per scene: 4 s clip 11 s plain vs 11-12 s with a look).
- **First real run 2026-10-19** ("The Titanic Baker Saved by One Drink", 42.8 s, Claude wrote, Gemini edited; Claude ran
  out of quota at the edit plan, so Gemini directed, picked pictures and reviewed): library look `silent` on 4 scenes,
  hard cuts, flash cuts, a whip, a light leak, 2 kinetic titles; no inventions (nothing for `library.bat`). The review
  timed out once, answered on try 2 with no findings. Bug found and fixed: a look picked for an AI-animated scene was
  never drawn (`Short.tsx` skips looks on any clip) but used up a look slot and was listed in edit_plan.txt;
  `apply_look_scenes()` now refuses `animate` scenes too (backup `backup/make_shorts_2026-10-19_before-look-clip-fix.py`).
  Not yet seen in a real run: question beats, wipes, any invention.
- **Code review fixes 2026-10-19** (backup `backup/make_shorts_2026-10-19_before-review-fixes.py`): a failed invention
  now empties only its own slot (before, it also wiped a look invented moments earlier); `approve_candidate()` rolls
  back if the compile check crashes or times out; `render_remotion()` also empties the slots at the start (a run
  closed mid-invention); candidate names are unique across kinds (index.ts imports by name); no second compile
  after the art check says ok; `clean_look()` reuses `clean_invention()`. test_style 29.
- **Open (2026-10-19):** the owner approved the Titanic Baker Short (voice fine). The invention path (AI-coded look,
  overlay or cut) has never run in a real Short.

### fix.bat
Pick a recent Short (made in the last 7 days), a scene, and: 1) no AI motion, 2) use another scene's picture
(`use_picture_from()`, also copies AI paintings and clears any motion graphic), 3) remove its text graphic, map or
motion graphic, 4) paint a new picture (`paint_new()`, clears any motion graphic; asks what's wrong, then `rewrite_paint_prompts()` writes a better prompt), 5) turn it into a motion graphic
(`rescue_graphics()`). `render(..., state)` reuses pictures, music and palette; voice/clips/video are re-made (a few
minutes); no automatic repaint, logbook untouched.

### Logbook
`vault/Logbook/<channel>.md` (in the Obsidian vault since 2026-10-21): one entry per Short ("Written by" Claude/Gemini). Numbers come from YouTube Studio; Claude
can read them with the Claude in Chrome extension (Content -> Shorts -> each Short's Analytics overview; read-only,
own tab, close it after) and fill Views, Comments (from the Content -> Shorts list), Subscribers gained, Stayed to watch, Average % viewed
and a note (traffic sources, last-48h views). **Likes + exact Average % viewed**: channel Analytics overview
(`studio.youtube.com/channel/<id>/analytics/tab-overview/period-default`), "Latest content" card on the right; click
its right arrow through all Shorts and zoom-screenshot the card (its text isn't in the page text; the card lags one
click behind). The newest Short's likes are on the Dashboard's "Latest Short performance" card. The
Analytics overview's view count is newer than the Content list's. Retention appears ~2 days after posting. Entries with Views
filled feed the planner. Studio's video IDs so far: Cardiff UgYjLUeEBdE, Byron Oy_CEoedafY, Violet pYZi6r30aRo,
Moon Hoax h94mVnaAAJU, Great Stink RiUuo_RjVDM, Emperor Norton FxizDDhnd70, Jack the Baboon XIXXJqXRmZ0, Emu War
CFHPBn7fXfk, Hiroo Onoda fWEVCJO6Q8g, Ghost Army UJ5pmA5qOVU. Channel id UCMVMdmkpRb1a7EjBaSOQ4cQ. Direct page per Short:
`studio.youtube.com/video/<id>/analytics/tab-overview/period-default` (wait ~5 s before reading the text).
State 2026-10-20 (fifth read): 10 posted, ~7,800 views total, 7 subscribers. Jack 1,353 (28.6 % stayed, 43 % viewed),
Violet 1,316, Byron 1,302, Norton 1,223 (58.5 % stayed, 89 % viewed), Hiroo Onoda 1,207 (317 -> 1,207 in its first day,
48 % viewed, +3 subscribers, the most of any Short), Emu War 971 (923 in its first 5 hours, then slowed; 32.5 % stayed,
44 % viewed), Great Stink 346, Moon Hoax 52, Cardiff 28, Ghost Army 23 (feed passed on it, 42 % viewed). Every Short older than 2 days has stopped getting feed views; each one's
push lasted about 1-2 days. Hunch, not proven: the 1,000+ Shorts stall near 1,300. Audience (10-16): worldwide
(Philippines 17.7 % largest), ages 25-44. Posted 2026-10-21: Mike the Headless Chicken (video ID not recorded yet). Not posted yet: Hatfield, Vasa, Voigt, Unsinkable Sam, Titanic Baker,
Frank Hayes, 1904 Marathon, Molasses Flood.

### Hard-won lessons
- **How Shorts get pushed (researched 2026-10-16):** YouTube shows each new Short to a small "seed audience", then widens
  or stops (YouTube's Shorts lead). Posting time doesn't matter; never delete and re-upload a flop (spam risk); thumbnails
  are mostly unseen in the feed. Since 2026-08-24 a view counts from the first frame, so "Stayed to watch" is the real
  hook signal. Unconfirmed blog claims: 70-90 % stayed and ~50 % watched for 30-60 s Shorts do best.
- **Monetization bar (reported by vidIQ/TechTimes, YouTube page not opened):** now 1,000 subs + 10M Shorts views in
  90 days; from 2027-02-01 20M (or 8,000 watch hours), and Shorts revenue pauses in months under 10M per 90 days.
- **Wikimedia** serves only thumbnail widths 330/500/960/1280/1920; other sizes/originals get 429 Retry-After 600.
  Use `thumb_url()`, strip `?utm_` query strings, space requests, never wait > 30 s. `WM_UA` carries the owner's
  email (approved), sent to Wikimedia only.
- **LTX on 8 GB**: two-stage load (text encoder, then transformer); fp8 layerwise casting; T5 on the GPU from the
  bf16 copy with `.wo$` layers kept bf16. Wan 2.2 5B tested and rejected (~50 min per 2 s clip).
- **agy quirks**: `-p=` must hold the prompt inline (no stdin); `--mode auto` isn't available on the account.
- **Argon quota** is weekly ("Resets in 165h"): keep it for text.
- Remotion flags: `--gl=angle --concurrency=4 --x264-preset=ultrafast --crf=14`. Don't render tests while a batch
  runs (shared `remotion/public/job`, RAM/VRAM); check for a running `make_shorts.py` first.
- Edge TTS 403 = update edge-tts with `uv pip install -U edge-tts --python .venv\Scripts\python.exe` (no pip in
  .venv). Kokoro runs offline: every mapped voice must already be in `local_ai/hf`.
- Qwen voice: `Qwen3TTSModel.from_pretrained(<repo id>)` calls the Hub API and fails with `HF_HUB_OFFLINE=1`; load the
  `snapshot_download(..., local_files_only=True)` folder instead. qwen-tts pins transformers 4.57.3 (keep it out of
  gen.py's venv). MMS aligner weights are in `local_ai/hf/torch` (`TORCH_HOME`). Chatterbox (tested, not used) needs
  `setuptools<81` for its watermarker and pins torch 2.6, which has no RTX 50-series support.
- PowerShell-written JSON has a BOM: read profiles with utf-8-sig.
- AI painting quality: SDXL (PC) produced a US flag on a 1906 German town hall and faceless soldiers; Gemini's
  paintings fit period details. Painter order is now MOSS, then Gemini, then SDXL (see Media).
- The automatic review catches burned-in subtitles, watermarks, wrong eras, blank frames and other channels' AI art
  reliably; trust its CHECK lines.

### Status (2026-10-16 / 2026-10-17)
- Verified 2026-10-16 in a dry run (no render): the script team with Claude writing and Gemini editing (Emperor
  Norton), the SEO changes, the fact-check corrections reaching SEO; shorter-Shorts length rules via a fake-AI test.
- Verified in full runs: shorter scripts (Vasa 50 s, Voigt 48 s), palettes (teal, gold), music moods, wide-clip band,
  plain zoom instead of parallax, automatic review + repaint, headline + stamp graphics, map route, mark circle,
  counters, Argon -> Flash switch, Gemini painting for a Claude-planned Short (Voigt re-render).
- Verified 2026-10-16 in a full run (Jack the Baboon, 36.4 s): short mode, the script team (Claude writing, Gemini
  editing), fact check rewrites, the footage pool without YouTube (Pixabay + Internet Archive film), a Veo clip the
  owner made in Flow (scene 7), auto-repaint. The review flagged the hook film (a modern snowy European train for
  1880s South Africa); fixed 2026-10-17 by giving scene 1 the real `Jack.signalman.jpg` and repainting scene 6
  (`use_picture_from` + `paint_new` from a scratch script, same as fix.bat); re-review clean. Old version kept in
  the Short's `before_fix/`. Lesson: when the story has one famous real photo, it belongs on the hook.
- Not yet seen in a real run: Gemini writing with Claude editing, quote and compare graphics, "Both" compare mode,
  the myths list, full-screen motion graphics in a real Short.
- Postable now: Hatfield, Vasa, Voigt (all re-rendered and checked), Jack the Baboon. The owner posts them; Hatfield and Voigt were made before the
  YouTube-clip removal and still contain other creators' clips (credited), so they may get less reach.
- 2026-10-17: full-screen motion graphic scenes (4 templates + custom AI-coded scenes + 4 mood skins + screen-locked
  `TitleBanner`) built, approved by owner, and wired into `make_shorts.py` and `fix.bat` (24/24 unit tests pass; Task 11
  full Short run remaining for tomorrow).

### Main character + opening picture (2026-10-19, owner approved)
From the logbook: every Short built around one strange person or animal (Jack, Violet, Norton, Byron, emus, Onoda)
was pushed; every one about a thing/event/group (Great Stink, Moon Hoax, Cardiff Giant, Ghost Army) stalled at <= 346
views. Pattern from 10 Shorts, not proof; the unposted event-led Shorts (Vasa, Molasses Flood, 1904 Marathon) test it.
- **Soft rule, the owner's choice** (worried about running out of topics): any topic is allowed, but every Short needs a
  `character` (one named person or animal); events are told through the person at their center (Great Stink ->
  Bazalgette). The topic prompt asks for it, the character is put first in `people` (portrait search), and the writer
  gets `main_character` and writes the hook about them.
- **Opening picture** (picture list `hook` flag, director's scene-1 `pic`, picker's scene 1): from the story's own
  time (no modern museum/replica/tourist photo: Ghost Army opened on a museum's inflatable tank), ideally the main
  character's face, and it must raise the hook's question, not answer it (Jack opened on the baboon at the levers:
  28.6 % stayed). Old cached `catalog.json` picture lists keep their old `hook` flags until pruned.

### Script rules from the short-video-scripter skill (2026-10-20, owner asked)
The owner installed the Claude Code skill `short-video-scripter` (aaron-he-zhu/aaron-marketing-skills,
`~\.claude\skills\short-video-scripter`). It only affects interactive Claude sessions: ShortsMaker's writer often runs
on Gemini (agy), so a skill never reaches the pipeline by itself; its rules must live in the prompts. Most of it was
already here (question hook, hook_options, sound-off hook_text, callback loop ending, no spoken CTA). Added to the
writer prompt (`write_scripts`) and editor prompt: the 3 `hook_options` come from different hook families (curiosity
gap, result first, stakes, contrarian claim, before/after), and scene 2 is a "confirmation" beat (one concrete,
showable detail proving the hook's claim is real, without answering its question). **The confirmation beat and the
"surprising claim" hook were replaced 2026-10-22 by `STORY_RULES`, see "Story rules from the research".**
- The skill belongs to a 120-skill marketing plugin (with hooks); the owner chose NOT to install the plugin or its 9
  sibling skills (product-marketing tools, not needed here). Instead 3 reference files were copied from the repo into
  `~\.claude\skills\short-video-scripter\references\` (`platforms/youtube.md`, `platforms/tiktok.md`,
  `humanizer-slop.md`) and the skill's links to them repointed from `../../../references/` to `references/`. Links to
  the sibling skills and other framework files stay dead on purpose.
- `npx skills update` overwrites SKILL.md and re-breaks those 3 links (the references folder survives). Re-fix with:
  `sed -i -E 's#\.\./\.\./\.\./references/(platforms/tiktok\.md|platforms/youtube\.md|humanizer-slop\.md)#references/\1#g' ~/.claude/skills/short-video-scripter/SKILL.md`

### Test run 2026-10-21: Mike the Headless Chicken (MOSS first, short mode, Claude planning)
`output/strange-history/2026-10-21_mike-the-headless-chicken-died-of-this-not-the-axe`, 36.6 s, 9 scenes, 72 words.
Real Mike photo on the hook, Internet Archive film, map, 2 custom motion graphics; 3 automatic fix rounds used.
- Fixed: the on-screen credit tag showed a raw web address (Commons author field was two links); `short_credit()`
  now shows the first link's domain ("Photo: miketheheadlesschicken.org").
- Fixed: in fix round 3 the LTX worker died without writing results (no Windows crash event; the same job
  worked when run alone). `local_job()` now retries once after a hard crash and prints the exit code.
- Fixed (owner's report): full-screen motion graphics ended abruptly. `full_cues()` let the last beat start 1 s
  before the cut and the AI-coded scenes add their own delay (Mike's "NO SYRINGE" stamp showed 0.3 s). Now the last
  beat comes `FULL_SETTLE` (1.6 s) before the cut and earlier beats are squeezed forward in order (custom, board,
  journey; number capped too). The 2026-10-19 overlay fix (`GRAPHIC_BUILD`) never covered full-screen scenes.
- Fixed: MOSS drew gibberish on the newsstand because a subject made of print can't be painted "without text"
  (no quoted words -> `MOSS_NO_TEXT`). Planner rule now: quote the cover that matters ("LIFE") or pick another subject.
- Re-rendered with both fixes (old version in the Short's `before_fix/`): last beats now hold ~1.2 s before the cut;
  scene 6 repainted by MOSS as a newsboy holding a magazine reading "LIFE" (spelled right). Review left 2 CHECKs:
  the hens in scenes 2 and 9 have heads.
- Decided 2026-10-21: owner wants shorter Shorts and picked a faster voice by ear (`voice_speed_test/`):
  `COSY_SPEED` 1.15 -> 1.30 (Mike narration 36.0 s -> 31.9 s). Word counts unchanged.
- Fixed 2026-10-21 (owner: Mike had "no background audio"): music was mixed at a fixed 0.22, but the tracks range
  -9 to -28 LUFS, so Thinking Music (-22) vanished under the ducking. `music_gain()` measures each track (ebur128,
  first 60 s) and brings it to `MUSIC_LUFS` (-25) before ducking, so the ducked music sits ~21 dB under the voice
  (measured on Mike: old fixed volume 31 dB under = inaudible; -30 gave 26 dB under = still faint).
- Decided (see above): short mode came out 36.6 s, not 25-30. CosyVoice reads ~2.1 spoken words/s (not the
  2.4 measured on one clip; numbers like "$4,500" add spoken words). Owner chose the faster `COSY_SPEED` (1.30).
- Was open, FIXED later 2026-10-21 (see below): `paint_new()` repainted from the scene's same `ai_image` prompt, so a repaint after the review rejected a
  painting brings the same subject back (scene 6's newsstand: graphic -> painting -> graphic -> painting, garbled
  magazine lettering both times). MOSS also wrote gibberish on a text-heavy subject despite `MOSS_NO_TEXT`.
- 2026-10-21: owner posted the Mike Short (re-rendered version: 32.5 s, louder music, "LIFE" newsboy) and said
  no need to fix the repaint problem for that Short. Its Studio video ID is not in the logbook yet.
- FIXED 2026-10-21 (owner asked: change the prompt on every repaint, improving on the first one):
  `rewrite_paint_prompts(short, {scene: complaint})` sends the old prompts, narration, shot notes and complaints in
  one AI call with the channel's `## AI paintings` rules (the planner's ai_image rules; was `AI_IMAGE_RULE`); answers that are empty,
  unchanged or say "photograph" are refused, and an unanswered scene gets "Seen from a different angle, in different
  light." appended so the seed (and picture) still changes. Used by `apply_review_fixes()` and fix.bat option 4.
  Test `test_rewrite_paint_prompts`; not yet seen in a real run.

### Less "AI-looking" paintings + thumbnail concepts (2026-10-21, owner asked)
Owner: the cartoonish AI pictures in Shorts and thumbnails look "way too AI". No skill fixes this (image skills
found were paid APIs, Gemini-website automation or face-cam thumbnails; `101-skills/superpowers` copies have
inflated install counts). Applied Black Forest Labs' own FLUX prompting guides instead (`flux-image-best-practices`,
`flux-3-archival-formats`): name a real medium with its physical marks, not a mood; ask for low fidelity
explicitly; one descriptive sentence; always name the light; prove style words with a control probe.
- Planner `ai_image` rule: subject, setting, named light, then a hand-made medium of the story's era with its
  marks (wood engraving on newsprint, hand-colored etching, 1940s gouache magazine illustration with halftone
  dots, silkscreen poster, oil sketch, charcoal). Banned: "concept art", "digital illustration", "stylized",
  "cinematic", "highly detailed", "8k", "vibrant" (old default "stylized concept art illustration" = the glossy look).
  Artwork fills the whole frame (poster/card wording made MOSS draw a paper border).
- `thumbnail_prompt` rule: same medium rule + information-gap concepts adapted from Higgsfield's thumbnail
  frameworks (MIT): one big focal subject readable at phone size, size contrast, one real element oversized, lone
  figure in a vast setting, map with a route, before/after split, many copies of one object. Truthful to the story.
- `MOSS_AI_LOOK` (MOSS negative: 3d render, cgi, glossy, concept art, cartoon, border...), `PAINT_HANDMADE`
  (same idea in words for Gemini, which has no negative), `PAINT_FALLBACK` (replaces "Oil painting, muted colors").
- Control probe on MOSS: `test_renders/ai_look/compare.jpg` (old vs new: farm, motel, thumbnail) and
  `border_fix.jpg`. New versions show paper grain, brush texture, print colors. MOSS still ignored "small
  silhouette" in the thumbnail test (drew a big chicken with a head).
- Found: MOSS's seed comes from the prompt text, so a repaint with an unchanged `ai_image` gives the identical
  picture. That is why the review's repaint of Mike's newsstand changed nothing (fixed below: `rewrite_paint_prompts()`).

### Emu War review fixes (2026-10-18, built)
All three were built 2026-10-18 at the owner's request, after reviewing the Emu War Short:
  1. DONE: **credit tag** = `short_credit()` ("Photo: E. Mariz · CC BY 2.0", whole words only; full credit stays in
     upload.txt), 22 px, shown `CREDIT_SECONDS` (2.8 s) then fades; since 2026-10-19 (owner: it sat mid-screen) always bottom-left at `CREDIT_Y` = 1500, just above
     YouTube's channel name/title, hidden once the subscribe button shows (`credit_low` removed); same in the Python fallback renderer. Checked on stills of
     the Emu Short.
  2. DONE: **big-number figure** = the director/rescue give `thing` (singular noun); `render()` adds
     `FIGURE_PROMPT` to the same Gemini painting batch, `ink_silhouette()` turns it into a cropped transparent PNG
     (`work/fig<i>.png`, refused if blank or mostly ink), `full_props()` sends it as `full.image`, and `BigNumber.tsx`
     draws it (inverted on dark skins, accent glow on the last). Fallback = built-in icons, now 18 incl. bird, fish,
     insect, rat, horse, car, plane, gun, barrel, dollar. Grid picks the column count with the biggest figures
     (20 figures: 7 x 3 at ~120 px instead of 10 x 2 at 86 px). Test stills: `test_renders/figure-*.png`.
  3. DONE (2026-10-18): **story sounds**. The director gives a scene `sound: {"word", "sound"}` (max
     `MAX_STORY_SOUNDS` = 3, word must be spoken: `clean_sound()` / `limit_sounds()`); `scene_cues()` times it
     (`sound_at`); `render()` resolves it with `story_sound()`: the owner's own `sfx/story/<name>.(wav|mp3|ogg|flac)`
     wins, else `freesound_fetch()` (official API, CC0 only, 0.15-4 s, well-rated first, HQ preview MP3) is trimmed,
     high-passed at 220 Hz, loudness-evened and kept as `sfx/story/<name>.wav` + a `.txt` source note (fetched once).
     In `sfx_events()` it has priority 9, so the graphic's sound within 0.5 s gives way. No match = no sound.
     First fetches: gun_cock, ship_horn, crowd_gasp ("emu call": no CC0 match). Owner can still drop better files in
     sfx/story/ (YouTube Studio Audio Library is the safest source). Old suggestion list kept for reference:
     gun cock, gunshot, machine-gun burst, cannon, explosion, splash, waves, thunder, rain,
     bell, clock tick, typewriter, shutter, crowd gasp, crowd cheer, footsteps, door creak, glass break, horse gallop,
     train whistle, ship horn, coin drop, cash register, paper rustle, bird squawk. Keep the 220 Hz high-pass, under the voice.

### claude-motion skills (2026-10-21, owner asked)
- From github.com/whaleyxbt/claude-motion (MIT): `motion-design` and `review-loop`, rewritten for this repo in
  `.claude/skills/` (license in `.claude/skills/LICENSE-claude-motion.txt`). They load in interactive Claude Code
  sessions in D:\ShortsMaker; pipeline `claude -p` calls run with `--disable-slash-commands` and never see them.
- What reaches the pipeline: rule 9 "TASTE" in `custom_rules()` (easing curves, spring presets, stagger, one focal point,
  reading holds) and three extra questions in the `look_and_fix()` review (competing focal points, text moving while read,
  everything appearing at once). Keep rule 9 and the skill in step.
- Not taken: `sound-design` (its own stdlib synth engine; ours is `sfx_events()` + the SFX library) and `web-sims` (three.js
  simulations, not this niche).

### First-second check + honest logbook lessons (2026-10-21, owner asked after the logbook review)
The 12 posted strange-history Shorts showed: views split ~1,000-1,350 / ~350 / under 60 (one feed test, none broke
past ~1,350); the three flops were hoax/group stories with no main character; pushed Shorts still lost 4-8 of 10
viewers in the first second (stayed to watch 21-59%); the shorter recent Shorts did not hold attention better.
- `review.first_second_check()` (in `render()`, after `visual_review()`): 4 frames of the first 2 s + the storyboard;
  the AI scores 1-10 "would a scroller stop and need to stay?". Below `HOOK_MIN_SCORE` (7) it writes a
  `FIRST SECOND: n/10: why` CHECK line and may name a later scene whose REAL photo/film would open better; the fix
  loop then swaps the two pictures (`swap_pictures()`, never a painting or motion graphic), once per Short
  (`opener_swapped`). The hook words are not rewritten (that would mean a new voice and timings).
- `logbook.logbook_results()`: entries under `JUDGE_MIN_VIEWS` (100) get "Too few views to judge" so the planner
  stops learning from Cardiff's 81% stayed (28 views). The planner's lesson text names the first second as the weak
  spot and asks it to compare hooks/opening pictures of high- vs low-stay Shorts.
- Topic prompt evidence updated (Hiroo, Mike = character-led and pushed; Ghost Army stalled). The rule stays soft.
- Length unchanged: 40-50 s default, 25-30 s stays the owner's optional test.

### AI models and effort per task (2026-10-21, owner: quality first, but high is the highest Claude effort the plan allows)
- Claude: every `ask_ai` call is pinned to `--model opus --effort high` (`llm.CLAUDE_MODEL`, `CLAUDE_EFFORT`). The lean
  call skips the owner's settings, so before this the model/effort were whatever the CLI defaulted to (Opus 5.5 on
  2026-10-21; effort unknown). `test_package.py` fails if either drops below Opus / high. Don't raise effort to
  xhigh/max: the owner's plan doesn't have the usage.
- Gemini: text tasks and the review-type picture jobs (first-second check, visual review, look-and-fix, detail marks,
  style previews) use `gemini_model()` (Argon high, Flash when its weekly quota runs out). Only `bulk=True` picture
  jobs that read dozens of images stay on Flash: `catalog_pool()` and `choose_images()`.

### Shotcut timeline for fixing by hand (2026-10-22, owner asked)
Owner: after the 3 automatic fix rounds (kept unchanged), CHECK lines can remain (Togo vs Balto: scene 4's title cut
off, scene 9's fake book page, first second 6/10); they want an open-source editor to fix those themselves.
- Editor: **Shotcut** (GPL, github.com/mltframework/shotcut), portable v26.9.27 in `D:\Shotcut`, settings in
  `D:\Shotcut\appdata` (`--appdata`, keeps them off C:). Picked over Kdenlive/OpenShot because it opens plain MLT XML
  as a project and ships `melt.exe`, which renders the same file headless (used by the test).
- `edit_project.py`: when `render()` ends with CHECK lines and no further fix round will run (also after fix.bat),
  it writes `edit.mlt` + `edit_in_shotcut.bat` into the Short's folder. Timeline (Remotion Shorts, i.e. all so far):
  V1 pictures = `work/pictures.mp4` (photos/film/AI clips with their zoom, looks, transitions, full-screen motion
  graphics), V2 graphics = `work/graphics.mov` (ProRes 4444 with alpha: callouts, maps, cards, person cards, hook
  title, credit tag, subscribe button, flash), both cut into one clip per scene so the owner can resize one scene's
  picture (Shotcut filter "Size, Position & Rotate") without moving its graphics (owner asked 2026-10-22); a
  Python-rendered Short gets one V1 = `work/clean.mp4` (pictures + graphics, no captions) instead. Top video track =
  `work/captions.mov` (captions alone, transparent qtrle made
  from `captions.ass` by ffmpeg; ASS mirrors the Remotion captions), A1 voice (`work/voice.wav`), A2 music
  (`work/music.wav`, already ducked), A3 sounds (`work/sfx.wav`, all SFX + story sounds summed); on Shotcut's output a
  Gain filter (`master_gain()`: measured so the three together hit -14 LUFS) and a -1.5 dB Limiter (`ladspa.1913`),
  standing in for the final mix's loudnorm + limiter (tested: -14.0 LUFS in Shotcut vs -14.3 automatic). The two
  stems come from the final ffmpeg run itself (`asplit` before the loudness pass; SFX are summed in their own `amix`
  first, which leaves the mix bit-identical, tested). One marker
  per scene; red with the CHECK text when a CHECK names that scene (lines naming no scene go on scene 1).
  A clean render with nothing left removes an old `edit.mlt`.
- Layers: `Short.tsx` prop `layer: 'pictures' | 'graphics'` (unset = the whole Short, unchanged);
  `render_remotion(..., words=[], layers=True)` re-renders twice at the end (pictures h264, graphics ProRes 4444
  `--image-format=png`; each about as long as a normal render, so ~2-3 min per Short, only when CHECK lines are left;
  graphics.mov ~6.5 MB/s, ~330 MB for 50 s; custom scenes and inventions come from their `work/` caches, so no AI
  calls). clean.mp4 (Python renderer) comes from the same ffmpeg run (split before `subtitles`). Captions sit above
  everything in Shotcut, so Remotion's flash no longer whitens them.
- Shotcut format gotchas (from its source): tracks are playlists with `shotcut:video`/`shotcut:audio`; tractor needs
  property `shotcut`=1; every upper video track's `qtblend` has a_track = 1 (V1, the bottom video track; NOT the track
  just below: with 3 video tracks that rendered black), V1's own (onto the background) stays disabled; markers are
  `shotcut:markers` -> numbered `properties` with text/start/end/color(`#RRGGBB`). Verified: opens in Shotcut as a
  multitrack (log `isMultitrack true`, 2-video-track version); a 4 s test Short (callouts, hook, credit, flash, CTA)
  rendered whole vs pictures + graphics layers composited, both by ffmpeg and through melt: PSNR 42-43 dB (encode
  noise only). The Togo Short has no timeline (made before this; already posted). Not yet used on a real Short.
- `work/` is pruned after 7 days, which breaks that Short's `edit.mlt` too.

### Story rules from the research (2026-10-22, owner asked: average % viewed under 50%)
Owner noticed viewers stay past the first second but don't finish. Claude read Studio retention curves (Hiroo,
Emu War, Jack vs Great Stink, Emperor Norton): every Short loses most viewers 4-12 s in, but the two best (~90%
viewed) stop bleeding after ~12 s while the rest slide to 15-20% at the end. The owner then asked for research on
other channels' successful Shorts before any change ("do your homework"). Read via vidIQ transcripts (~50 credits):
Voggle (new strange-history channel like ours; "The True Story of Mike the Headless Chicken" 2M views vs our Mike's
1.2K, "They Brought Slugs Into War" 1.1M, its Emu War 8K) and Zack D. Films (true stories, 25-60 s, millions each);
YouTube's Shorts lead (2023): storytelling over a target length. Vendor blogs given little weight. Findings: hits open
inside the strangest moment (not a summary claim), link beats with but / so / you see (Parker & Stone's rule), bring
background only as "you see" answers, use few dates/names, save the answer for the last line and stop, flow in full
sentences, and have a dry voice; length is not the lever; very famous topics (Emu War) flopped on both channels.
Built (owner approved all 4 points):
- `## Story rules` in `channels/strange-history.rules.md` (was `writing.STORY_RULES`; writer + editor; includes our own example script, Jack retold; never paste
  other channels' scripts) and `SCENE_CUTS`. First sentence up to 12 words (was 8; topic picker still asks for an
  8-word fact). Old rules gone: confirmation beat, separate callback line, "never background".
- Editor reports `payoff_scene` and `list_like`; `story_problems()` flags: answer before the last two scenes, a line
  starting with a date (`DATE_FIRST`), first sentence over 12 words, list-like beats. Failing scripts go back to the
  editor ONCE with the problems (`edit_scripts(..., problems)`); leftovers become `STILL:` editor notes in edit_plan.txt.
- Sentences may run across picture cuts: `gpu.sentence_groups()` voices each run of scenes ending in . ! ? as one take
  (CosyVoice and Qwen; Kokoro/Edge backups stay per scene), `split_takes()` cuts it halfway through the pause between
  scenes using the aligner's word times (`spoken_count()` mirrors `qwen_voice.align_words`; a mismatch = that voice
  failed, next voice). Takes are `work/take<first scene>.wav`. Real CosyVoice test: 2 takes -> 4 scenes, ~same time.
- Profile `tone` (strange-history) rewritten: flowing story, but/so/you see, dry wit, answer last (was "short punchy
  sentences", which drove the fragments). Lessons text in the planner prompt updated.
- Not changed: lengths (40-50 s / 25-30 s), SCENE_WORDS 10 per picture, niche. Not yet seen in a real run: check the
  next Shorts' retention curves (Studio overview -> "Key moments for audience retention"; read by screenshot).

### Rules per channel (2026-10-22, owner asked)
Each channel has its own `channels/<name>.rules.md`, so a new channel never changes another's Shorts (the gaming
profile had silently used strange-history's rules). Plain Markdown, read by `##` heading (case and spaces don't
matter; `###` stays inside a section; a `<!-- tag -->` first line is stripped): `Settings` (`status: draft|ready`,
`visuals: photos|blender`, `min_real_pictures`), `Topic picking`, `Story rules` (was `writing.STORY_RULES`), `Writing
for the picture`, `Lessons from our numbers`, `Opening picture` (picture list), `Picture picking` (the visual editor's scene-1 rule in
`picker.py`), `Directing`, `First-second check`,
`AI paintings` (was `writing.AI_IMAGE_RULE`). `rules.require_rules()` runs at the start of a batch (before `last.txt` changes) and of fix.bat; a channel with no
rules file yet (a failed draft, a profile copied into `channels/` by hand) gets one drafted and the run stops for review; a
missing/empty/repeated section, `status: draft` or a bad `min_real_pictures`
stops the run with the file and heading named. Never a fallback to another channel's rules.
`## Opening picture` must define `- era_ok:`, `- sharp:` and `- hook:` lines (2026-10-26): `catalog_pool()` asks for
those fields with that text, and weird-economics' prose version made every `hook` false (1 `[opener]` in 231
pictures over 4 Shorts; the AAirpass Short opened on a landing DC-10, first second 5/10). Its rewritten section, tried
on that Short's real pool, tags the 1971 lounge film and the 747 first-class cabin as openers and not the plane.
- What stays in the code, shared: lengths, scene cuts, fact rules, reply formats, `story_problems()`, the picture
  `reject:` safety list, the evidence-board/document/graphic format examples in the director prompt.
- New profile (run.bat "+ New channel"): after the profile JSON, `rules.draft_rules()` has the AI copy the sections
  of existing rules files that fit, adapt or write the rest, tagged `copied from` / `adapted from ...: what changed` /
  `new`; Settings are written by the code with `status: draft`; one retry on a bad reply, never overwrites. run.bat
  then stops until the owner sets `status: ready`. `channels/gaming.rules.md` was drafted this way 2026-10-22 and is
  waiting for the owner's review.
- `tests/test_rules.py`: `tests/golden/prompts.json` holds every prompt strange-history sent before the move; the
  golden test proves they are still identical. Re-save it (`--save-golden`) only when a prompt change is intended.
- `visuals: blender` channels: see "Blender channels"; their engineer instructions are the `## Build plan` section.

### Blender channels (2026-10-22, owner asked; first: engineering-failures)
A channel whose rules say `visuals: blender` is drawn entirely in Blender (`D:\Blender\blender.exe`, 5.2.1, run
headless): every scene is a 3D "ink manual" drawing (flat colours, paper sky, ink outlines, the failing part
red); the only real photo is the thumbnail (one archival photo of the real structure). Owner's choices: bridges only
at launch; failures crack / bend / shear / sway, optionally then collapse_span; fasteners rivet / bolt / pin / weld
(never screws); no painting or photo fall-back. Spec/plan: `docs/superpowers/specs|plans/2026-10-22-blender-*`.
- Engineer step (`blender_plan.plan_builds`, end of `write_scripts`): one AI call writes each Short's build plan
  (template, sizes, focus part + label, failure, scale, one beat per scene) from the channel's `## Build plan`
  rules; `clean_build` checks every value (tables at the top of `blender_plan.py`), fills missing beats and always
  puts a zoom before a failure; an unusable plan is asked for once more, then `default_build` (generic truss bridge,
  CHECK line). Scenes get no motion graphics, callouts or person cards.
- Render (`short_render.render`, `drawn = bool(short.get("build"))`): no picture picking or painting; after the
  voice, `blender_render.render_clips` writes `work/build.json` and runs `blender/build_scene.py`; frames go to
  `work/blender_frames/`, one clip per scene `work/blender{i}.mp4` (played like real film). Same build.json + all
  frames present = no redraw (build.json carries a fingerprint of `blender/*.py`, so a code update redraws). Blender failing twice raises `BlenderFailed`: cli skips that Short (its folder is removed; a re-run writes new
  scripts) and goes on. After the clips are cut only each scene's first and last frame stay (~1.5 GB otherwise);
  the cache reuses the clips. fix.bat explains it can't change a drawn Short and stops.
  Scenes hard-cut (Python renderer, `write_frames(..., cuts)`; edit_plan says "hard cut"): the Blender camera is one
  continuous move. `plan_builds` also clears the writer's photo look and special transitions (they'd send the Short to
  Remotion and film effects over the drawings). A failing pier falls with its span (it belongs to no span; once only
  its red copy fell).
  The review is told the drawings are deliberate; its findings stay CHECK lines (no automatic fix rounds).
  Thumbnail: `drawn_thumbnail` tries `blender_plan.thumbnail_order` (usable openers first, film frames never: their
  URL is the video) and uses the first download that opens as an image, else the zoom frame + CHECK.
- Blender side (`blender/`, plain bpy, not imported by the package): `look.py` (colours, flat materials, ink
  outlines from a GPU compositor: Sobel edges of the normal pass + the flat colours; Freestyle was 3-7 s a frame on
  a full bridge), `parts.py` (parts kit; linked-duplicate meshes; labels with leader lines face the camera),
  `templates.py` (truss, girder, suspension, cable-stayed, eyebar-chain; part names like
  `span2_node3_bottom_left_gusset`; `dress` adds rails, cars, a train, tiny people (never with a collapse);
  `focus_object` says whether the named part exists, and the AI's label is drawn only then), `failures.py` (bend = subdivided plate warped in its plane + sag; crack = ink
  segments; shear = fasteners pop + slip; sway = growing twist; collapse = span pivot drops), `build_scene.py`
  (piers stand from the start; the bridge stands finished until the first build scene, which cuts to the empty
  site and drops the parts in; the hook shows the part failing without the collapse, peaking by 1.5 s; the label
  falls with its span and close shots after the failure aim at the fallen part; renders PNG frames).
  Blender 5.2 gotchas: no video file format (render PNG, join with ffmpeg); a new material's node tree needs a fresh
  Output node; `matrix_world` is stale until a depsgraph update (use `.location`); a SimpleDeform needs a subdivided
  mesh. About 0.3 s per 1080x1920 frame on this PC (a 45 s Short: ~7 min of Blender).
- Sample: `output/_blender_sample/i35w/` (hand-written I-35W script, real render path, 2026-10-22). Its review left
  content notes the kit can't show yet (no gravel, crews or equipment on the deck) and a 6/10 first second.
- Tests: `tests/test_blender_plan.py`, `test_blender_render.py` (fake Blender), `test_blender_run.py`,
  `test_blender_scene.py` (real headless Blender, a few minutes).

### Motion graphics & person card early-triggering and tight narration pacing (2026-10-24, owner asked)
Owner: in Douglas Bader (and future Shorts), spoken lines staggered with awkward, prolonged pauses (e.g. after "Douglas Bader", "his captors had good reason", "when he was shot down over France"). This was caused by the earlier hold padding adding up to 1.8s of audio silence after lines when graphics waited for late trigger words near the end of the sentence. Owner asked to start motion graphics earlier so they have enough time during speech without stalling the narrator.
- **Early visual triggers (`shortsmaker/editplan.py`)**:
  - Instead of delaying entrance until an end-of-sentence trigger word (`spoken_at - 0.1`):
    - **Animated maps (`"lat" in g`)**: Start flying on scene entry (`start + 0.2s`) so the camera sweeps across the world during the sentence and drops the pin right as the place name is spoken, with `map_pace` scaling to fit the scene.
    - **Overlay graphics**: Start on trigger word, or shift earlier if the trigger is late in the scene (`latest = end - 0.25 - need_time`), bounded below by `start + 0.2s`. The graphic builds and holds while the idea is spoken.
    - **Person cards**: Trigger on the spoken name or earlier if the name comes late (`latest_on = end - 0.25 - 1.8`), with `off = min(on + 2.5, end - 0.25)`. The photo card pops in promptly with the shutter sound, holds center focus as the name is heard, and exits before the cut.
- **Tight narration pacing (`shortsmaker/short_render.py`)**:
  - Replaced the large 1.8s dead-air silence padding with tight, natural pacing:
    - Full-screen scenes get at most a subtle micro-settle (`max(0.0, 0.25 - tail)`).
    - Very short scenes (< 1.6s) get a micro-breath if needed.
    - Padding is strictly capped at `<= 0.25s` (`min(0.25, needed)`), completely eliminating line staggering, pauses after spoken names, and dead silence.
- **Smooth broadcast exit animations (`remotion/src/Graphics.tsx`, `shortsmaker/frame_render.py`)**:
  - `PersonCard`: 0.32s cubic-in easing exit, scaling down to 0.75 and smoothly dropping `45px` (`translateY`), eliminating abrupt disappearances.
  - `useWindow`: exit window extended to 0.28s finishing at `end - 0.32s`, providing a calm buffer before the cut across all template cards (`Stat`, `Timeline`, `Headline`, `Fact`, `Stamp`, etc.).
  - Python renderer `draw_card()` updated with matching 0.32s smooth exit.

### Solo AI execution mode & flexible AI selection (2026-10-24, owner asked)
Owner: selecting the AI should offer an option where only one AI does the entire thing by itself (Claude alone or Gemini alone), rather than forcing Claude to write and Gemini to edit, or vice-versa.
- **Options in `ask_brain()` (`shortsmaker/channel_profiles.py`, `shortsmaker/cli.py`)**:
  - `1) Claude only`: 100% Claude solo (`session.SOLO = True`, `session.BRAIN = "claude"`). Claude writes drafts, critiques & edits its own script, plans the edit, catalogs/picks pictures, and reviews the finished Short. No Gemini calls or fallbacks. AI gap images are generated locally by MOSS-Image / SDXL without invoking `agy`.
  - `2) Gemini only`: 100% Gemini solo (`session.SOLO = True`, `session.BRAIN = "gemini"`). Gemini writes drafts, edits scripts, plans the edit, catalogs/picks pictures, paints AI gap images (`agy`), and reviews the finished Short. No Claude calls or fallbacks.
  - `3) Claude (Gemini edits)`: Collaborative mode. Claude writes and plans, Gemini edits each script pass.
  - `4) Gemini (Claude edits)`: Collaborative mode. Gemini writes and plans, Claude edits each script pass.
  - `5) Both, to compare`: Generates each topic twice (once with Claude, once with Gemini) for side-by-side comparison.
- **Solo enforcement across pipeline**:
  - `edit_scripts` (`shortsmaker/writing.py`): In solo mode, `editor = session.BRAIN`. The prompt informs the model that it drafted the scripts and is now critiquing and refining its own work.
  - `ask_ai` (`shortsmaker/llm.py`): In solo mode (`session.SOLO=True`), a bad or broken answer is retried by the same AI, never handed to the other. Only running out of credits/quota hands over (owner, 2026-10-27): the other AI becomes `session.BRAIN` and does the rest of the run solo (the empty account is in `NO_QUOTA` and isn't asked again).
  - `picture_pool.py`: In solo mode, empty candidate catalogs retry the same AI instead of asking the other AI.
  - `gpu.gemini_images` (`shortsmaker/short_render.py`, `shortsmaker/remotion_render.py`): Only runs `agy` if Gemini is allowed (`not (session.SOLO and session.BRAIN == "claude")`). Claude-only runs use MOSS-Image / local SDXL.
  - `logbook.py` & `cli.py`: Log entries record `Written by: <Brain> (solo)` when solo mode is active.

### Gemini review timeout & agy tool loop fix (2026-10-23)
- **Root cause**: In `visual_review`, Gemini (`agy`) was launched without `--disable-slash-commands` and without tool boundaries. When it saw discrepancies on contact sheets, it autonomously ran shell commands, wrote inline Python scripts to crop tiles, and explored python source files until hitting the 15-minute subprocess timeout twice, falling back to Claude.
- **Fix (`shortsmaker/llm.py`, `shortsmaker/review.py`)**:
  - Added `--disable-slash-commands` and explicit prompt instructions in `run_agy` and `visual_review` forbidding shell/script execution or codebase exploration, requiring direct image inspection via `read_file` and immediate JSON return.
  - Reduced review timeout to 300s (180s for text).
  - Automatically switches `_argon_exhausted = True` to `gemini-3.8-flash-high` on timeout retry and for the rest of the run.

### `weird-economics` profile, dollar-scale TTS fix, money graphs & seamless loop fixes (2026-10-25, owner asked)
- **New channel profile (`channels/weird-economics.json`, `channels/weird-economics.rules.md`)**:
  - Niche: Obscure Business Autopsies & Weird Economics (counter-intuitive money math, perverse incentives / Cobra Effects, contract loopholes, bizarre B2B monopolies, unit economics, supply-chain dominoes; bans overused clichés like Enron/WeWork/Blockbuster/FTX/Theranos/Costco hot dogs).
  - Requires topics anchored by well-illustrated Wikipedia subjects (`min_real_pictures: 6`), 4+ concrete numbers per script, and a full-scene setup bridge on the final beat (4–7 words, no trailing period) that loops seamlessly into Scene 1.
- **Dollar-scale TTS word order fix (`local_ai/qwen_voice.py`, `tests/test_qwen_voice.py`)**:
  - Previously, `studio_speak` and `align_words` called `say_number()` token-by-token, turning `"$800 million"` into `"eight hundred dollars million"`.
  - Added `spoken_tokens()` and `spoken_sentence()` in `qwen_voice.py` to look ahead for scale words (`hundred`, `thousand`, `million`, `billion`, `trillion`), hold `"dollars"` until after the scale word (`"$800 million"` -> `"eight hundred million dollars"`), handle `"$800M"`/`"$2.5B"`/`"$50k"`, and use singular `"one dollar"` for `"$1"`.
- **Motion-graphics density & money graphs (`shortsmaker/rules.py`, `shortsmaker/plan_rules.py`, `shortsmaker/writing.py`, `shortsmaker/picker.py`, `remotion/src/Cards.tsx`, `remotion/src/full/BigNumber.tsx`)**:
  - Added optional `max_full_planned` and `max_full` settings in `rules.py` (`weird-economics` uses `max_full_planned: 4`, `max_full: 5`, min 6 words per full scene; `strange-history` stays at `2`/`3` and 7 words so golden prompts are unchanged).
  - Added `parse_scene_money()` and `fill_money_graphics()` in `plan_rules.py` so any dollar beat left without a graphic (or stripped by `fact_check`) automatically gets a side-by-side `compare` bar chart when paired with a nearby dollar beat, or a `stat` counter.
  - Capped `document` full-screen scenes at 1 per Short in `limit_full()` and `rescue_graphics()` so rescued slots aren't wasted repeating the same contract clause.
  - Updated `StatCard` (`Cards.tsx`) and `BigNumber`/`Bars` (`BigNumber.tsx`) to format `$` prefixes and compact `M`/`B` suffixes (`$1.5M`, `$17.45M`), and added `direction: "down"` support on `StatCard` (auto-detected on crash/drop words in `clean_graphic()`) so falling numbers count downward instead of upward from zero.
- **Infinite loop timing & prosody (`shortsmaker/gpu.py`, `shortsmaker/short_render.py`, `shortsmaker/plan_rules.py`)**:
  - For loop Shorts (`is_loop_short()`), `local_voice()` appends the first 4 words of Scene 1 to the final TTS take so CosyVoice/Qwen reads the loop bridge with natural mid-sentence continuation pitch instead of a falling period drop; `split_takes()` then slices the audio right after the final scene's last word (`mine[-1][1] + 0.04s`).
  - `short_render.py` trims trailing silence on the final scene, sets `pads[-1] = 0.0` (no `apad`), reduces `total` tail from `0.6s` to `0.04s`, and uses a `0.12s` music micro-fade so audio flows straight into Frame 0 of Scene 1.
- **Portrait-on-portrait prevention (`shortsmaker/plan_rules.py`, `shortsmaker/picker.py`, `shortsmaker/writing.py`)**:
  - Added `is_person_portrait()` so scenes with a floating `PersonCard` never use a solo portrait of that same person as the full-screen background (`bg` automatically swaps to an unused storefront/crowd/context candidate).
- **Whip transition black-bar fix (`remotion/src/style/transitions/Whip.tsx`, `remotion/src/Short.tsx`)**:
  - Fixed `Whip.tsx` where `to` had `opacity: 0` during `p < 0.5` while `from` translated `-35%` left, exposing a 35–40% black vertical bar on the right side of the frame (seen at `00:19` in Piggly Wiggly). `from` and `to` now whip simultaneously edge-to-edge across `0 < p <= 1` with slight scale overscan.
- **Ivar Kreuger Short audit & 5 pipeline improvements (2026-10-25)**:
  1. **Glass-plate negative mount border trimming (`shortsmaker/photo_prep.py`)**: Extended `trim_borders()` so when a noisy outer glass-plate negative edge (`<= 12px` at 400px thumbnail scale, often containing handwritten catalog numbers like `ROL 161 684`) is immediately followed by `>= 2` consecutive 90%-flat mount border lines inside the 15% border limit, both the outer strip and inner mount border are trimmed cleanly.
  2. **Full-resolution Internet Archive image downloads & cleaner pool queries (`shortsmaker/image_sources.py`, `shortsmaker/footage.py`, `shortsmaker/picture_pool.py`)**: Updated `get_image()` so final downloads (`what != "thumbnail"`) of `https://archive.org/services/img/{ident}` resolve `https://archive.org/metadata/{ident}` and download the full-resolution scan (`2000–3000px` from `d1`/`d2`) instead of the 180px icon thumbnail. Also excluded `tv OR television` collections from `archive_films()` and stripped generic leading adjectives (`vintage`, `old`, `historic`) from fallback 2-word pool search queries in `gather_pool()`.
  3. **`QuestionBeat` & `KineticTitle` placement, backing, and exit timing (`remotion/src/style/overlays/QuestionBeat.tsx`, `remotion/src/style/overlays/KineticTitle.tsx`)**: Updated `QuestionBeat` to respect `slot(graphic, 300)` (`low: true` moves it below faces), added a dark translucent card backing (`rgba(8,10,16,0.82)`) to both `QuestionBeat` and `KineticTitle` for legibility over bright archival prints, capped `KineticTitle` letter-drop stagger to `<= 0.42s`, and set `tOut = end - 0.28` so both overlays exit cleanly before flash/whip cuts.
  4. **Eliminate blank opening frames on Custom full-screen scenes (`remotion/src/full/toolkit.tsx`, `shortsmaker/motion.py`)**: Updated `cueAt(full, 0, start, end, total)` to clamp `i === 0` to `Math.min(c0, start + 0.15)` and updated `custom_rules` Rule 7 so the first card, photo, or core diagram frame always lands within `0.15s` of the scene start instead of leaving the paper stage blank while waiting for a late trigger word.
  5. **Cap repeated solo portraits as scene backgrounds (`shortsmaker/picker.py`, `channels/weird-economics.rules.md`)**: Updated `choose_images()` so a solo portrait of the main subject (`is_person_portrait`) is used at most once as a full-screen scene background (`bg`) across the Short (and skipped on later scenes with overlay cards so they use their concrete historical scene illustration instead of putting a `StatCard` or `QuestionBeat` over a repeated headshot).
  6. **Shorts-Feed & Search SEO upgrades (`shortsmaker/seo.py`)**: Expanded autocomplete seed queries to include mechanism/category terms (`search_terms` + channel `research_seeds`), updated `seo_pass()` to lead titles with the scroll-stopping hook/anomaly + broadly famous anchor entity (`NBA`, `Wall Street`, `$800M`) instead of obscure Wikipedia names or pipe suffixes (`| Match King`), placed exact historical proper nouns in Sentence 1 of the description and tags for exact-name search indexing, and replaced dead proper-noun hashtags (`#IvarKreuger`) with active audience-cohort hashtags (`#Economics`, `#WallStreet`, `#SportsBusiness`, `#BusinessHistory`).

### Oxford review fixes (2026-10-26, owner asked after the William Minor Short)
The Oxford/William Minor Short showed six faults; each was checked against the run's files and real searches first
(Gemini's list was right on the opener swap, the false "blank" findings, the newspaper paintings and the pool junk; its
"always keep Veo clips" and "lower FULL_MIN_WORDS / no mid-sentence cuts" were wrong: 2 of 3 clips came from bad start
pictures, 10 of 14 scenes had 8+ words, and mid-sentence cuts are on purpose, see SCENE_CUTS).
- **Owner clips (Flow/Colab)**: `gpu.start_picture_problems()` looks at every start picture before the hand-off
  (wrong place/era, printed or garbled text, AI artifacts, wrong person); flagged scenes get no job and no LTX clip
  (the review replaces their picture). In a live test it flagged the LA station and the fake newspaper page and passed
  the good scriptorium picture. `veo_handoff()` records `scene["owner_clip"]` (the file in `<Short>/veo`);
  `local_clips()` re-cuts it every render (`cut_owner_clip()`), so `review.swap_pictures()` moves a clip WITH its
  picture (owner_clip, motion, motion_people). Repaints and pool swaps still drop the clip (animate False). Older Shorts
  without owner_clip keep reusing `clip{i}_veo.mp4`.
- **Opener swap**: `first_second_check()` lists every candidate scene's line and picture (title + catalog description)
  and the main character, and only swaps when BOTH scenes fit afterwards (never a different named person under a line
  about someone else). Live replay of the pre-swap Oxford state: 6/10, no swap (it had swapped Murray in).
- **Review false "blank" findings**: `visual_review(..., cues=)` adds each scene's graphic and person-card window
  ("on top: question beat ... 0:04.1-0:05.2") and says dimming there is on purpose (`overlay_notes()`).
- **Pool relevance** (`image_sources.on_topic`): one shared word that is only part of a story person's name or a
  `WEAK_WORDS` word ("portrait", "dr") no longer counts; two do. The searches take `names` from `gather_pool`'s people.
  Pixabay results are now filtered at all, `strict` (two words, or the query's only word): it answers anything with
  modern stock; only 2 of 18 Shorts ever used a Pixabay clip (Big Ben, Lubang jungle; both still found). Internet
  Archive films match on their title only (spam stuffs the subject list). Oxford's searches: 18 junk films -> 1 (the
  film's trailer).
- **Paintings**: the rules files' example media no longer say "illustrated newspaper/newsprint", "magazine" or
  "poster" (scene 8 and the thumbnail were whole fake newspaper pages); a line forbids naming the printed carrier.
- **Twist check** (`writing.check_twists()`, after the picture check, before writing): each topic's twist against its
  Wikipedia text; a legend becomes "the famous story says X; in fact Y", and a far stronger true fact the topic left
  out goes in (live: Oxford's topic gained the 1872 killing and the widow who brought Minor books; the visit legend was
  debunked). Shown in edit_plan.txt as "Twist check". The fact check now also fixes every later line that tells a
  "legend says" legend as fact (story_holds false when the ending is the legend). Research: the 402K-view Short on this
  story opened with the murder and ended by debunking the visit legend; other channels' titles all lead with "murderer".
- Not bugs (checked): Minor's missing name card = the one-portrait-per-Short rule (2026-10-25); his only photo was
  scene 1's background. Left-over CHECK lines are printed and get a Shotcut timeline (not silent).

### Graphic card and title hold time fixes (2026-10-26, owner asked after the Digby Tatham-Warter Short)
The Digby Tatham-Warter Short showed cards ("VIEWING SLIT" kinetic title in scene 2, "KNOCKED OUT" stamp card in scene 3,
and "WHY CARRY IT?" question beat in scene 4) disappearing too quickly (~1.1s total on-screen time, with only ~0.25–0.5s
of resting readable time).
- **`GRAPHIC_BUILD` & `need_time` (`shortsmaker/editplan.py`)**: Added build times for `kinetic` (0.6s), `stamp` (0.35s),
  `headline` (0.45s), `question` (0.4s), and `mark` (0.4s). Differentiated full animated card overlays (`kinetic`, `stamp`,
  `headline`, `quote`, `question`, `stat`, `timeline`, `compare`, `mark`, `date`) from plain inline tags (`fact`, `place`).
  For card overlays, `need_time = max(1.8, build + 1.0)`. Late-trigger cards now shift earlier in the scene
  (`latest = end - 0.25 - need_time`), providing >= 1.8s on-screen time (e.g. "KNOCKED OUT" now holds for 1.80s instead of
  1.10s). Plain callouts preserve `need_time = max(1.1, build + 0.7)` so they wait for their spoken word as tested.
- **Short scene hold padding (`shortsmaker/short_render.py`)**: Raised `sc.get("graphic")` pad threshold from `1.4 - dur`
  to `1.6 - dur` (matching person cards), allowing scenes under 1.6s to gain up to 0.25s breathing room without dead air.
- **Crisp Remotion exit envelopes (`remotion/src/Graphics.tsx`, `KineticTitle.tsx`, `QuestionBeat.tsx`)**:
  In `useWindow`, changed `tOut` from `end - 0.32` to `end - 0.18` and `leave` from `[tOut - 0.28, tOut]` to `[tOut - 0.20, tOut]`.
  In `KineticTitle` and `QuestionBeat`, changed `tOut` from `end - 0.28` to `end - 0.18` and `out` from `[tOut - 0.22, tOut]` to
  `[tOut - 0.18, tOut]`. In `PersonCard`, changed exit interpolation to `[card.off - 0.20, card.off]`. Cards now hold solid
  ~0.22s longer before beginning their exit transition and finish crisply before the cut.
- **Tests**: Added `test_graphic_card_hold_duration` in `tests/test_package.py` validating hold time and early shift for
  late triggers on stamp and kinetic cards. All test suites pass (17/17 package, 45/45 full scenes, 11/11 first second, TS tests).

### Blender openers (2026-10-27, owner asked: every Short opens on an animation of its strangest moment)
First-second research (Voggle, How Money Works, Thoughty2, Simple History vs 12 of ours) and a hand-built probe in the
owner's Blender (Mike's chop; the owner's six catches became the checks below). Spec/plan:
`docs/superpowers/specs|plans/2026-10-27-blender-openers*`. Part 2 (people) built: see "People openers" below.
- **Agent rule (owner, 2026-10-28): load the Blender skills before any opener or people work** (`blender/*.py`,
  people clips, props, looks). The owner installed them in `~\.claude\skills` from github.com/EL4CTEO/blender-skills:
  always `blender-core` first, then the one for the job: `blender-character-rigging` (rigs, IK, weights, the people
  bodies), `blender-animation` (clips, NLA, keys, walks), `blender-lighting-lookdev` / `blender-time-of-day` (light,
  sky, mood), `blender-rendering`, `blender-simulation` (physics), `blender-geometry-nodes`. The owner switches between
  Claude and Gemini: Gemini (agy) has the same 8 as a local plugin, `~\.gemini\config\plugins\blender-skills\skills\`
  (copies: after updating the Claude ones, copy them over again; `agy plugin list` shows it). They only reach
  interactive sessions; the pipeline's planner call and the headless render never see them, so whatever they
  teach has to be baked into `blender/*.py`. Check every change by eye (`tests\people_sheet.py`, a render of the job).
- **Blender MCP has to be started each time.** Opener models are fetched through the owner's live Blender (the MCP
  add-on holds the Poly Pizza key). At the start of a run on a channel with `opener: blender`, `cli.blender_note` pings
  localhost:9876 and, if Blender doesn't answer, says: open Blender, press N, click Start MCP Server, Enter to retry or
  S to skip (skip = only models already in the library). Rendering itself is headless and needs no window.
- Rules settings (`## Settings`): `opener: blender` (both strange-history and weird-economics) and `hook: moment |
  money_claim` (the hook-line check: the editor reports `hook_kind`; a summary hook, or a weird-economics first line
  without a money figure, goes back to the editor once, `writing.story_problems`).
- Plan (`opener_plan.py`, after the fact check in `write_scripts`; **replaced 2026-10-28 by shot templates, see below**): one AI call stages every Short as JSON from the
  tables in `blender/opener_tables.json` (grounds, lights, moves, tools, gaits, outcomes, cut-face colours, limits),
  shared with `blender/moves.py`. `clean_opener` rejects anything outside them; `buildable: false` (people) or an
  unusable plan leaves `s["opener_check"]` and today's scene 1. The AI never writes Blender code.
- Models (`blender_link.py`): `D:\ShortsMaker\blender\assets\library\polypizza_<id>.blend + .json` (gitignored;
  credits in the json). Missing ones: search (CC0 / plain CC-BY only), one AI call picks by title
  (`opener_render.pick_model`), fetched in the owner's own scene (owner, 2026-10-28: no scene of ours; it used to be a temporary
  `SM_fetch` scene): the objects there before are noted, the download's new ones saved and removed. Poly Pizza only (Poly
  Haven's photo-real scans clash with the look); never Sketchfab (NC licences, fan art).
- Blender side (plain bpy): `opener_scene.py` (set, brand look: EEVEE, AgX, warm sun, 50 mm, f/2.2 on the subject,
  camera: starts wider and pushes in, arcs 14 deg, cranes up 16 deg, handheld sway, a jolt on the first hit and a lens
  punch-in (62 mm, else 56, else none: the strongest that keeps the subject in frame), always follows the subject
  once it moves (2026-10-27, owner: the locked-off Mike shot was bad); motion blur; the hit plays at half speed
  (`retime`: scene frames 3 before to 9 after, the rest a little faster, same frame count, rendered on subframes);
  a burst of bits in the target's colours where the first piece comes loose (`burst`, added after the checks); actors placed by `stand_on` where the whole footprint clears the
  surface), `moves.py` (roles not objects; physics for fall/topple/roll/fly_off/scatter/cut pieces with launch speed
  handed over from 2 keyed frames; keyframes for walk/hop_off/sink/push and tool strokes), `scene_kit.py` (models as
  one welded mesh, origin at the feet, physics helpers and collision layers), `opener_checks.py`. **`cut` is one move
  for every cut**: strokes (`through` a region, `at_fraction`, `rows`/`cols`, `mince`) split the target along the
  blade's plane (bisect, cut faces filled and coloured), the blade stops at the first thing it isn't cutting, piece
  shares are by surface area (the owner-approved chicken head = 12%), each piece comes loose with the stroke that
  frees it. Tool edge = the thinner side of the blade.
- Checks on every frame: overlap (all pairs; allowed only tool vs the piece it cuts during its stroke, pieces of one
  cut, physics bodies after release), resting (1 cm), in frame, first frame (subject >= 15% + threat), edge leads,
  blade face (>= 35 deg), cut result (planned shares ±50%, counts, >= 3 mm, <= 80 pieces), blade blocked.
- Run (`opener_render.render_opener`, from `short_render.use_opener` after the voice): beats scaled into scene 1,
  headless Blender (10 min, one retry), report, AI review of an 8-frame strip (no fix rounds since the shot
  templates, 2026-10-28), then `work/opener.mp4` plays as scene 1 (no motion graphic over it, no first-second
  picture swap, CC-BY credits in upload.txt) or `CHECK: opener failed: <reason>` and today's scene 1. Unchanged
  plan + code reuse the clip (`work/opener_done.txt`).
- **Motion-graphic opener (owner, 2026-10-28: the Eiffel Short's opener failed 3 times and fell back to a mugshot
  with no word on a motion graphic).** `picker.opener_graphic` (after the rescue, on Shorts with `opener` or
  `opener_check`) asks for a full-screen graphic of the hook's strangest moment (it may not decline: the onion
  Short's AI said "a picture opens stronger"; an unusable pick is asked once more, told why) and puts it on scene 1 up front,
  outside MAX_FULL and the never-scene-1 / never-two-in-a-row rules (owner: two in a row is fine). A Blender opener
  that renders clears it; one that fails leaves it playing. Its spoken-word triggers are dropped and scene 1's
  `full_cues` start at 0 s, so it moves from the first frame. The first-second picture swap is skipped under it.
  The edit plan's `Opening:` line says what played: `Blender opener: ...` or
  `Blender opener failed (<why>) -> motion graphic: <summary> (<AI's reason>)` / `-> no motion graphic (<reason>);
  scene 1 opens on its picture`.
- **Opener consistency (owner, 2026-10-28: "it failed 3 times, how can we make it more consistent?").** 0 of 7 live
  runs had passed: most failures were engine limits, sent back to a planner that could only edit the plan, so the same
  fault came back on tries 2 and 3. Now:
  - `opener_tables.json` `people_moves[*].does` says what each people move really does; `_tables_text` gives it to
    the planner and the fixer. The fixer may replace a move that can't show the moment (it used to "keep the same
    moment" and kept `pick_up` three times).
  - `fix_plan` sees the earlier tries' failures (`short["opener_tries"]`) and can reply `{"fixable": false}`
    (returns the reason as a str): `render_opener` stops at once and the motion-graphic opener plays.
  - Every failed try is kept: `work/opener_tries/try<n>.json` (plan + failures) and `try<n>_strip.jpg` (the review
    strip, when the checks passed).
  - `pick_up` needs `"take"` (a thing of at most 1 m on the ground, or a person after their earlier `drop_prop`;
    `opener_plan._takeable`). `people.pick_up`: probes the PickUp clip for the lowest-hand frame, picks one of 12 ways
    to stand whose bend keeps `BEND_ROOM` from everyone (side-on to the camera, nearest), walks there (`_travel`,
    split out of `move`), turns, bends; the item is frozen from the bend (kinematic) and rides the hand (CHILD_OF
    "picked") from the grab. Failures: the hand misses (`GRAB_GAP`), no room to bend. The person's next move waits
    until they stand up (`st.busy`); pushed past the scene's end, that's a failure the planner fixes.
  - `drop_prop` lets go out to the side (`DROP_OUT`): straight down, the case lay against the dealer's foot.
  - The stand-in people library's PickUp bends and swings the arm down (its hand sits on the hip hinge).
  - From the second live run (its three tries replayed headless on each fix, `opener_tries/*.json`): the taker aims
    at where a dropped item comes to rest (`REST_FRAMES`); the room to bend is judged against everyone's footprint
    over the rest of the scene and includes the hips going back (`BEND_BACK`); the walk ignores the item and goes
    round whoever is in the way (`_detour`, two legs); a missed grab leaves the item on the ground. In
    `opener_scene`: whoever picks something up has their beats built last (so the bend sees the dealer's later
    cheer); a thing to pick up starts `TAKE_GAP` in front of its taker; a dropper and their taker stand
    `PICK_APART` further apart; a prop someone will pick up is dropped toward them (`DROP_TOWARD`).
  - Fixed for every person: a second travel move (a run after a pick_up, a detour's second leg) turned from the
    planned facing instead of the way the person faces now (`people.facing_now`).
  - Result on the replays: the first live plan (which had failed on timing) and the third pass, as does the first
    Eiffel plan with `take` added; the second still fails by 0.01 m of bend room (dealer cheering over the bag).
- **From the onion-futures run (2026-10-28; all 3 tries failed only at the AI review, the motion-graphic AI then
  declined).** Replayed headless from `work/opener_tries/`, each try now fails in seconds before the render:
  - Everyone a beat moves is framed and checked (`opener_scene.beat_actors`, `seen_segments`): the camera framed the
    sack alone and the trader and farmer were never in shot. The frame covers where they go over the whole scene
    (a cheer's arms, a fallen subject), a falling thing down to where it lands, and the camera no longer rides a
    physics body up and down (the sack's fall looked like the ground rising). The camera follows the subject and
    whoever has to be seen at that frame (a second from each of their beats; smoothed only then: alone, the lag lost
    the chopped rooster), and the punch-in keeps all of them in.
  - `opener_checks.moves_visibly`: a thing's beat must move it by a quarter of its size (a "toppled" sack on the
    floor only rocked).
  - Line-up: actors alternate right/left of the first, each side from its own edge (one running edge put the third
    actor past the second's width on the other side: the farmer 2.6 m out, everyone 13% of the frame).
  - `collapse` played `Defeat`, which only hangs the head (head 2.08 -> 1.84 -> 2.08 m); it now plays `Death` and
    `despair` is the head-hang. The stand-in library's `Defeat` had been a fall, so no test saw it. Die/collapse
    say they fall the way the person faces.
  - Groups of three or more stand in depth (9:16 staging: foreground to back, not side by side): everyone after
    the first goes back at a slant (0.8 across, 0.6 back), so silhouettes clear (at the linked pair's 0.5/0.85 the
    farmer stood behind the trader). Everyone who has to be seen is also checked for being hidden. Onion try 2 now
    passes every check and reads by eye (sack topples into the trader, he goes down, the farmer cheers); the empty
    floor below them is where the captions (bottom-aligned, 620 px up) and YouTube's buttons sit.
  - To look at a build in the owner's window: a job with `"save_blend": <path>` saves the built scene. **Owner
    (2026-10-28): keep the window on their one "Scene"; never add or switch to another scene** (each new scene means
    starting the MCP again). Load the build's objects into a temporary collection in "Scene"
    (`bpy.data.libraries.load`; never `setup()` live), set `scene.camera`/frame range to the build's, `look`, then
    restore them and remove the collection, its objects and orphans.
 The add-on registers its Poly Pizza commands per
  scene (`blendermcp_use_polypizza`): with the window on an appended test scene, every model search failed with
  "Unknown command type: search_polypizza_models" (2026-10-28). **Owner, 2026-10-28: never add or switch to another scene in their window** (every opener try used to
  open an `SM_fetch` scene for its downloads, and a new scene means starting the MCP again): downloads, live looks and
  tests all stay in "Scene".
- **`## Opener` in each channel's rules file** (owner, 2026-10-27: "i want the quality to improve on every short"):
  the planner stages from it and the AI review judges by it, including the owner's accepted conventions (unseen hand
  just off-screen, an animal cut where it stands, a blade stops at the first thing it isn't cutting) and staging
  lessons from the live runs. New owner feedback on openers goes there, not into code.
- Live runs on Mike's script (6, 2026-10-27) each found a general fault, now fixed with a test: hop clipping a wider
  rim (glide past the edge first), walk into an obstacle (stops short), a move that can't be built (reported to the
  planner, never a crash), wrong check subject / self-hiding, review frames skipping a 0.3 s chop (key moments
  added), a tilted blade swinging at the lens (strokes move across the frame), stroke angles explained to the planner.
  Each try's failures are printed. No live run produced a passing opener yet; the owner stopped tuning that one
  animation in favour of general fixes.
- **Owner, 2026-10-27: the opener animation is still not at the quality they want** ("keep improving it until I see
  that the animation is decent"). Fixed that day, each seen on the Mike render (`cache/opener_cam/mike_side_walk.mp4`
  = the plan staged by the new rules; `mike_camera.mp4` = the live plan, which walks "away"):
  - Facings and directions are as seen in the shot (`scene_kit.VIEW_YAW`, `view()`): a "side" camera used to see a
    rooster planned to face right head-on. Actors line up and backdrops sit side by side across the shot. Cut pieces
    keep their model's facing. Tools are not turned (their axes come from the mesh).
  - A neck chop follows the neck's lean and is not tilted at the lens (45 degrees over a 6 cm neck took a wedge off the
    back of the head and left the face on); a swung blade is turned about its stroke to show its face instead
    (`moves.show_face`, 50 degrees). Strokes move in the blade's plane, never toward the lens (`n x cam_h`): in
    profile the axe comes down from behind the head. The wind-up raises the edge against the stroke (it dipped
    underground) and swings down over 4 frames (`SWING`; it snapped there in one); chops and slashes take 4 frames.
  - Loose parts within 6% go together when cut (beak and wattle stayed on the neck stump). Cut faces of meat are dark
    red, not pink. No burst of bits at the cut: spheres, then flat feathers, both looked bad to the owner ("a bunch
    of little objects spawning", 2026-10-27), so it was removed. Physics is re-baked after anything added past the
    checks (a ground collider once dropped the cache and the head never flew).
  - Walking creatures get a leg rig (`scene_kit.leg_rig`; `legs`/`leg_zone` per gait in the tables): one bone per
    leg, swung in step with the bob, feet together on the last frame; the walk stops short by the leg's reach.
  - Staging lessons went into both channels' `## Opener`: animals from the side, walks across the frame, the body
    walks away from a head that flew forward.
  - Second round (owner: "the chicken is standing on the edge of the stump and fix the things that were weak"):
    `stand_on` needs the support under every foot and centres the feet, not the origin (the rooster stood on the
    rim); a measured sky (Multiple Scattering) with the sun 135 degrees round from the view, side/back light that
    shapes and rims (lights table `elevation`; night keeps its flat sky); a 400 m ground to the horizon with soft
    light/dark patches (`ground_material`); tufts and stones scattered behind and beside the action, never between
    it and the camera (`dress_set`, after the checks); legs tucked through a hop
    (`moves.legs` caches the rig for hop and walk). About 58 s of Blender for the 3.4 s Mike clip (was 46).
  - Staging check (`opener_checks.staging`, owner: "fix that"): an animal with legs walking or hopping "away" or
    "camera", or walking the way its own cut piece flew, fails and goes back to the planner with the direction to use
    (the live Mike plan walked "away"). Three tries in all; a plan still wrong after them loses the opener.
  Still open: no haze (at a 10 m set real haze is invisible; it would need a dense fog volume). Look at every
  change by eye.
- Reference tests: `tests/fixtures/openers/` (chicken chop, onion slices, onion mince, crate fall + their models);
  every check was also seen to catch a real fault while building them, and the renders were looked at by eye (checks
  alone passed a head blasted out of frame, hollow slices and an exploding mince).

### People openers (Blender openers part 2, 2026-10-27, owner: "make part 2 now")
Spec/plan: `docs/superpowers/specs|plans/2026-10-27-people-openers*`; branch `people-openers`. Owner chose cartoon people
by era and role (no faces), built in Blender from Quaternius rigged people, and one cel-shaded + ink-outlined look for
every opener.
- **Library (not in git, licence):** the owner downloaded the Ultimate Animated Character Pack (FBX) and Universal
  Animation Library [Standard] into `blender\assets\people\src\`; `blender\pack_people.py` packs them into
  `people.blend` + `people.json` (46 bodies on one 32-bone rig, 17 clips; fixes the FBX data: alpha 0 -> 1, emission
  off, near-black skin -> a default tone, each body's front measured). The Universal Animation Library is a different
  65-bone skeleton and is unused (retargeting is out of scope). `config.PEOPLE_*` point at the files.
- **Tables** (`opener_tables.json`): `roles` (25: body, colours by the body's material names, hat find, height) and
  `people_moves` (19: walk/run/carry travel; die, collapse, despair, flinch, sit, stand_up, jump, roll, punch, swing_prop,
  shoot, pick_up, cheer, throw_prop, drop_prop, idle). A plan's person: `{"id", "person": role, "facing", "prop"}`.
- **Blender** (`blender/people.py`): `dress` makes the mesh the root (origin at the feet) with its armature under it,
  colours, a hat on top of the head, the prop in the hand (the fist bone's HEAD: imported bone tails are guesses):
  long props by the handle (a blade up, anything else down and forward, leaning out until clear of the body and the
  ground), compact props carried. Every person plays Idle under their moves; in-place clips end grounded; travel
  moves at the clip's stride, feet pinned to the ground, stopping short of where others end up (prop and a quarter
  stride included; two going at each other meet halfway). Swing turns a blade to show its face (checked); drop/throw
  bake the prop's path and hand it to physics (layer 2: not its owner). People collide as their rest shape (a
  deforming passive collider crashed Blender).
- **All openers:** `toward` may name another actor (linked actors start 1.5 m apart, the target back into the
  depth, backdrops behind them; what someone goes at is the frame-0 threat, framed with them and at least half
  shown); `look_toon.apply` (3 light bands as emission, inverted-hull ink outlines) after the checks; a model no
  library has goes back to the planner (own allowance of 2, every miss named at once); fix rounds read the channel
  rules; first frame counts a wide low subject by width (40%); a vehicle can't "roll".
- **Checks/report additions:** staging covers people; `prop_shown` (frame 0); report `moved`, `highest`, `held`,
  `swings`, `threat`, `gap_start`/`gap_to`, `look`.
- **Tests:** `tests\test_people_tables.py` (3), `tests\people_standin.py` (stand-in library, built by the tests:
  no Quaternius file in git), 15 people/look tests in `test_opener_scene.py`, plan/render/check additions;
  `tests\people_sheet.py` renders `cache\people_sheet\roles.png` + `moves.png` to look at by eye.
- **Status, honestly:** every suite passes; the role and move sheets and a hand-written showcase
  (`cache\people_showcase\officer_umbrella.mp4`: the officer strolls across a street with a closed umbrella) look
  right. The end-to-end planner run on the umbrella Short never passed its AI review in about 8 attempts: the free
  libraries have no WW2 armoured car (a camper van stood in), the planner kept asking for an "umbrella" (Poly Pizza's
  is open), there's no explosion effect for "shells burst", and a person beside a 5 m vehicle can't be 15% of a
  portrait frame. Each run fixed a general fault (see the rulings in the commits); the remaining ones are content.
  Ideas: an explosion/smoke move, the planner told which models the library already has, a closed-umbrella default.

### Shot templates + three.js model graphic (2026-10-28, owner: "add those all 3 of it but make sure they can be useful")
Owner asked whether to drop Blender for three.js openers; the answer given: keep Blender but stop free composition
(0 of ~10 live runs passed; every new combination found a new engine edge), make the motion graphic the default
when no template fits, and add three.js only as a fixed template. All three built:
- **Shot templates** (`blender/shot_templates.json`): `chop` (Mike's rooster: a bird on a block loses its head, the
  body hops off and staggers away), `slice` (a food on a board sliced into 4-6 rings), `falls_on` (a sack/bag
  drops from 2.5 m and crashes down beside a person who flinches and collapses; a second person cheers or despairs;
  it toppled at first, which only rocked the sack sideways), `hand_over` (one person drops
  a small prop, another walks over, picks it up and walks/runs off). Each is a plan that passed the checks with
  `$slot` blanks; the planner (`opener_plan.plan_openers`) only picks one and fills it (roles, models with size
  ranges, a few picks, ground/light/backdrop); `fill_template` validates every value and `clean_opener` the result.
  Proof: `tests\test_shot_templates.py`, 8 variants with the real library + people, all pass every check, strips
  looked at by eye (`cache\shot_templates\`). Seen in the owner's live window the same evening (chop, hand_over, falls_on;
  physics pieces such as the flying head and the dropped sack don't play there, the build's rigid-body world stays
  in its own scene, so judge those from the render). Not through the AI review, and no live run yet.
- Limits found while building them, kept out of the templates: chopping a thing that isn't a bird (the axe left the
  first frame); `falls_on` with a crate (it hid the person once fallen) or with nobody reacting (same);
  `walk_through` (a person strolls on while a blast goes off behind them) was dropped: `scatter` only hops a thing,
  `fly_off` threw one small rock, and the held closed umbrella read as a dark triangle. It needs an explosion/smoke
  move first (the umbrella officer Short's moment).
- **No template fits -> motion graphic, no Blender at all.** `s["opener_check"] = "opener: no template fits (why)"`;
  the edit plan's Opening line reads `no template fits (<why>) -> motion graphic: ...`. Free composition is gone:
  no planner-written beats, no fix rounds (`fix_plan`, `_tables_text`, `FORMAT` removed). `render_opener` builds
  once; a model no library has goes back to the planner (`swap_models`, up to 2) for a more common find in the same
  template; any check or review failure plays the motion graphic and keeps the try in `work/opener_tries/try1.json`.
  New owner feedback on a template's look goes into the template (or the engine), then `test_shot_templates.py`.
- **three.js model graphic** (`remotion/src/full/Model3D.tsx`, `@remotion/three` 4.0.535 + `three` 0.170.0 +
  `@react-three/fiber` 9.1.2, exact versions): a full-screen motion graphic `{"type": "model", "find", "label",
  "note"}` offered to `picker.opener_graphic` only (`clean_full(..., opener=True)`; never a slideshow scene). The
  model must exist before it is planned (`opener_render.model_for`: library, else Poly Pizza through the owner's
  Blender; no model -> the AI is asked once more, told why). Render: the .blend is exported once to a .glb beside it
  (`blender/export_glb.py`, `opener_render.to_glb`) and copied to `job/model<i>.glb`; toon-shaded in 3 bands with
  an inverted-hull outline like the Blender look, drops in from frame 0, lands with a squash, camera cranes round and
  pushes in, framed to the model's size between the headline and the captions; headline at 0.55 s, note 0.5 s later.
  CC-BY model credit goes to upload.txt (scene 1 `full["credit"]`). Test scene: `remotion\test_props\model-coinbag.json`
  (`tests\render_full.py`); the Eiffel Tower model was also checked by eye. Not tried in a real Short yet.
- Not done: the run start still asks for the Blender MCP on `opener: blender` channels even if no template will fit
  (planning happens later, in `write_scripts`). `tests\test_rules.py` `test_strange_history_prompts_unchanged` was failing
  (no fake reply for the opener planner); fixed and the golden re-saved later the same day.

### Opener next steps (2026-10-28, agreed with the owner, in this order; step 2 done the same day, see above)
1. **A live run** of one Short with the onion-run fixes (framing everyone, checks before the render, depth staging,
   collapse, fetching in the owner's scene). Onion try 2 passes every check when replayed; no AI review or owner has
   seen it yet. Read `edit_plan.txt` (Opening + CHECK lines), `work/opener_tries/`, `work/opener_report.json`.
   Also open from that run: the owner says run.bat's "press any key" at the end doesn't close the window. Not found in
   the code (nothing changes the console mode; ComfyUI is stopped, VoiceStudio is a GUI app). Guess: Windows Terminal
   keeps a tab open after a non-zero exit code and then only Enter/Ctrl+D act. Asked the owner for the window's last
   line; not fixed.
2. **Shot templates** (recommended as the real consistency fix; not started): a small set of staged shots built once
   and checked by eye ("a thing falls near a person", "one hands something to another", "a person collapses",
   "a cut", "a crowd cheers"); the planner picks one and fills in roles and models instead of composing moves
   freely (0 of ~10 live runs passed that way, each new combination found a new engine edge). Same reason the
   motion-graphic templates are reliable and custom code needs a fallback.
3. **TRELLIS.2 on Colab for missing models** (owner, 2026-10-28: fine running the Colab step by hand, like the H3
   clips). microsoft/TRELLIS.2-4B, picture -> textured 3D model, **MIT licence** (commercial use, no conditions),
   about 24 GB VRAM: the Colab Pro A100 account (gutierrezdishann@gmail.com; the others are free tier). Plan: when
   no library has a model (`resolve_models`' "no fitting model"), MOSS paints the object on a plain background,
   TRELLIS.2 turns it into a model, saved to `blender/assets/library` with a json like a Poly Pizza model so later
   runs reuse it. Open: the hand-off pauses the run until the owner runs the notebook (or models are made ahead of
   time), fit with the toon look, mesh quality for the physics/overlap checks. Read the repo's LICENSE before building.
- Considered, not chosen: Hyper3D Rodin through the MCP add-on (its "free trial" is a key built into the add-on and
  shared by all its users, about 10 credits, commercial terms unclear; only with the owner's own key on a plan that
  clearly allows commercial use); Hunyuan3D 2.1 (Tencent licence excludes the EU, UK, South Korea; 29 GB with
  texture). Text-to-motion for more people moves, only if templates show the 17 clips aren't enough: HY-Motion 1.0
  (Tencent community licence, reportedly free commercial use under 100M monthly users; 24-26 GB) or NVIDIA Kimodo
  (code Apache-2.0, weights licence per checkpoint, the SMPL-X one non-commercial; 17 GB, under 3 GB with the text
  encoder on CPU); both need retargeting onto the 32-bone Quaternius rig.

### Ideas offered, not built
- Voice cloning (owner's own voice), SFX on the music's beat, YouTube Audio Library tracks for the somber/epic moods.
- Logbook extras from the Reach/Engagement tabs (drop-off times, search terms, shown in feed, likes/shares): offered
  2026-10-16, declined (noise).
- Rejected: MoneyPrinterTurbo, AutoSocial, kie.ai, Wan 2.2, browser-automating Google Flow/Gemini (account ToS risk).

### How to verify changes
- `.venv\Scripts\python.exe -m compileall -q make_shorts.py shortsmaker`; Remotion: `cd remotion && npx tsc -p .`
- Tests (no AI usage, no rendering): `.venv\Scripts\python.exe tests\test_package.py` (16: ROOT, ffmpeg on PATH, shared session, fakes reach callers, Opus/high pin, Gemini bulk vs review models, Argon->Flash on quota, agy flags and boundaries, Gemini timeout switch to Flash, person card hold and exit gap, scene hold padding, solo brain selection options, solo edit scripts, solo ask_ai no fallback, solo hand-over when out of credits, encoder cache, entry point),
  `.venv\Scripts\python.exe tests\test_h3_handoff.py` (19: H3/Flow prompt checks, retries, veo.zip, clips.zip, renamed zips, flow overwrite protection, closeup bypass, start-picture check, owner clip recorded and re-cut), `.venv\Scripts\python.exe tests\test_h3_run.py` (7: frame grid, H3 graph, start-frame crop, notebook, 40GB A100 warning, upload cancel),
  `.venv\Scripts\python.exe tests\test_first_second.py` (10: first-second check, opener swap incl. owner clips and the scene/picture list, review overlay windows, logbook small-sample note),
  `.venv\Scripts\python.exe tests\test_story.py` (9: word counts match the aligner, sentence takes, cutting a take, story_problems, editor second pass, rules in the prompt, twist check),
  `.venv\Scripts\python.exe tests\test_edit_project.py` (2: Shotcut timeline layout (pictures, graphics, captions; 3 sound tracks), output filters, markers; melt renders graphics + captions over the pictures at -14 LUFS),
  `.venv\Scripts\python.exe tests\test_full_scenes.py` (47 on 2026-10-28), `.venv\Scripts\python.exe tests\test_pictures_first.py` (39: pool, picture list, topic check, `pic`, picker, review fixes, relevance filter, Pixabay filter) and
  `.venv\Scripts\python.exe tests\test_style.py` (29: style library, guardrails, inventions, candidates),
  `.venv\Scripts\python.exe tests\run_ts_tests.py` (6 guarded + 13 style: arrow routing, layouts, card fitting, travel speed, registry, transitions) and
  `local_ai\qwen_venv\Scripts\python.exe tests\test_qwen_voice.py` (4: number words, caption words, aligner alphabet, word counts shared with tests/test_story.py).
- Own topic research: `tests\test_topic_ideas.py` (8: page parsing, clash, pages setting, cache, picks, the topic
  prompt, dropping a taken story, SEO without competitor titles).
- Blender openers: `tests\test_opener_plan.py` (21: tables, template fills, model swaps), `tests\test_blender_link.py` (6, fake add-on socket),
  `tests\test_opener_render.py` (28, fake Blender: one build, model swaps, fallback, reuse, credits, scene-1 wiring, the run.bat
  note), `tests\test_shot_templates.py` (real headless Blender + the real library and people: every template
  variant passes every check, about 6 minutes; `--render` writes `cache\shot_templates\<name>.mp4/.jpg` to look at), and with real headless Blender `tests\test_opener_checks.py` (9, about a minute) and
  `tests\test_opener_scene.py` (31 incl. the people tests, about 15 minutes), `tests\test_people_tables.py` (3),
  `tests\people_sheet.py` (people contact sheets, needs the packed library).
- One full-screen scene alone: `.venv\Scripts\python.exe tests\render_full.py remotion\test_props\<name>.json [--still SECONDS]`.
- Prompt changes without spending AI usage: set `llm.ask_ai` (and `writing.article_text`,
  `channel_profiles.trend_research`) to canned JSON and inspect the captured prompts.
- Single steps: in a scratch script `from shortsmaker import channel_profiles, short_render`,
  `channel_profiles.use_channel("strange-history")`, then call the function (e.g. `short_render.render(short,
  channel_profiles.load_channel(), folder, state)` with `short_render.load_state(work)`) to avoid spending AI usage.
- Full run: `.venv\Scripts\python.exe -u make_shorts.py 1 strange-history gemini`, then review 1 frame/s
  (`ffmpeg -i short.mp4 -vf "fps=1,scale=180:-1,tile=11x5" -frames:v 1 sheet.jpg`) and edit_plan.txt's CHECK lines.


2026-10-30: Voice upgraded from synthetic-cloned Qwen aiden to Mark Nelson (local_ai/voices/nelson_ref.wav + .txt, CC0/PD, 10.1 s from Continental Op), an articulate American investigative narrator with crisp diction and natural ~2.8 wps cadence. COSY_SPEED lowered from 1.20 to 1.10 (snappy 35-40s Shorts without metallic ffmpeg atempo time-stretching artifacts). Dynamic delivery arc added (cosy_instruct): urgent curiosity for the hook (take 0), suspenseful investigation for the body, and dramatic payoff for the final reveal.


### 2026-10-31: Part 2 continuation, Codex + Gemini
- Owner asked to continue the audit improvements and push every completed change set. Repository and remote
  were already at beaae733 on master: Parts 1 and 2.1/2.3-2.5 were merged; old handoff branch/wait notes were stale.
- Owner specified Codex + Gemini because Claude has no credits. Gemini modes now pair with Codex. Mode 2
  (the current strange-history and weird-economics defaults) keeps Gemini writing/editing and uses Codex for
  the independent cold read. Mode 4 uses Codex for editing too. Explicit Claude modes remain available.
  configure_brain is shared by normal runs and fix.bat; picture-catalog fallback uses the same pair.
- Part 2.2: cold reads try the partner, fall back to the planner on failure even in solo mode, and skip a partner
  whose quota is exhausted. Other solo calls keep their existing quota-only handover. Reports name the AI that
  actually answered. Menu/startup text explains the subscription quota use.
- Codex CLI 0.166.0 is already installed and logged in using ChatGPT. run_codex uses the local configured
  gpt-6-astra model at high effort, stdin prompts, direct image attachments, read-only sandbox, disabled shell
  tools, ephemeral sessions, and no user config/project instructions. ChatGPT authentication is enforced and
  API-key environment variables are removed from its child environment. No packages installed.
  Integration references: https://learn.chatgpt.com/docs/non-interactive-mode and
  https://learn.chatgpt.com/docs/config-file/config-reference (forced_login_method, features.shell_tool).
- Regression fixes: a failed second cold read clears the old draft's verdict; non-object cold-read replies
  are handled as no review; a failed opener preview clears the previous render's score. Each bug was reproduced
  in a failing regression test before its fix.
- Verification: 17/17 test suites passed (16 Python suites plus run_ts_tests), Python compileall, TypeScript tsc,
  and git diff --check passed. Golden prompts unchanged. Live Codex cold read of the Jack fixture succeeded,
  identifying the open question and answer scene 6; no Claude was called. Local test logs and the live response
  are in .superpowers/part2-verification/ (ignored).
- Still unverified: a complete live Short with the updated pair, including image-based Codex fallback. No claim
  about better audience retention yet. Part 3 and weird-economics' word-length decision remain open.


### 2026-10-31: three solo modes, all six writer/editor pairs, three-AI quota continuation
Owner corrected the earlier fixed Gemini/Codex interpretation: they want to select among Codex, Claude and
Gemini and keep a batch running when any subscription runs out. run.bat now offers exactly nine choices:
Codex solo, Claude solo, Gemini solo, then Codex/Claude, Codex/Gemini, Claude/Codex, Claude/Gemini,
Gemini/Codex and Gemini/Claude (writer/editor). Solo includes the cold read on the same AI. Hybrid routes
editing and the cold read to the selected editor. Saved choices and fix.bat use the same configuration;
legacy claude/gemini aliases are normalized, and the old both command still works from the CLI.
ask_ai now tries all three providers, skips accounts exhausted earlier in this run, and updates the writer
when a substitute answers after quota exhaustion or a missing CLI. If all three quotas are empty it stops
without re-querying them. Solo malformed replies still retry the selected AI rather than switching arbitrarily.
Verification: all nine modes tested for editor/cold-reader routing and batch writer selection; every mode
continues through two exhausted providers to the third and reuses it on the next request. Eight relevant
suites passed (139 tests), including unchanged golden prompts; compileall and diff checks passed. No live
AI quota spent on this change. A full video render was not needed for menu and provider-routing changes.


### 2026-10-31: Codex model changed at owner request
All ShortsMaker Codex modes now explicitly use gpt-6.1-sol with high reasoning effort.


### 2026-10-31: Mary Toft live-run detail-circle alignment
Owner completed output/strange-history/2026-10-31_doctors-believed-her-babies-were-rabbits and reported an
unrelated circle around 20 seconds. Inspected original frames, the saved grid and _raw scan: mark_details
chose coordinates on the untrimmed download, while MarkCard used the cleaned image after border trimming.
The title's old F3 cell consequently landed on ?Perform?d by.? mark_details now builds its grid on clean_photo
output, the same framing as the rendered card (also fixes the coordinate basis for stereo-card extraction).
A regression test fails on the previous code and passes with the fix. test_marks, test_rules, test_full_scenes
and test_pictures_first pass (116 tests); Python compilation passes. Golden prompts unchanged.
Rendered scene 8 frames 562-638 with the circle centred on the printed ?Rabbets? at x=.70/y=.18, inspected a
five-frame strip, and saved short-circle-fixed.mp4 alongside the untouched original. Only the top 1100 pixels
of those frames are replaced, preserving the original captions below; audio is stream-copied and its SHA256
matches exactly. Both copies are 41.533333 seconds. Before/after strips, corrected props and scene render are
in work/circle-fix/ (before strip in work/circle-before.jpg). Original work state and Shotcut timeline still
correspond to original short.mp4. User run profiles/logbook/vault changes are not included in this fix commit.


### 2026-10-31: Part 3.1 retention reader and owner-requested fresh performance baseline
Added retention.bat / make_shorts.py retention [folder] [screenshot] [AI mode]. The owner selects a finished
Short, supplies a Studio graph screenshot, and chooses an existing AI mode. One AI review task (normal retries
and quota fallback) reads only the isolated screenshot. Valid drop intervals are mapped to edit-plan scenes
in code, including narration and visual notes. retention.txt records at most three approximate drops,
+/-1-2s uncertainty, limitations, the reviewer, and a suggested My notes line; screenshot copy in retention/.
Unreadable graphs produce no guessed timings; malformed replies preserve the previous report. Work-state
pruning is irrelevant: the reader needs only edit_plan.txt. No automatic logbook writes or retention ingestion;
that is Part 3.2. Usage documented in docs/retention.md.
Owner asked to remove every old Short's logbook entry so old results do not influence the new baseline.
Archived exact current logbooks (including the latest Mary Toft run) and all four channel rules files under
vault/Archive/Logbooks/2026-10-31_200433/, with SHA256 manifest. Cleared 32 strange-history, 4 weird-economics
and 2 gaming entries. Active logbooks now have no results; verified logbook_results() returns empty for all
three. Archived and reset numerical Lessons from our numbers sections, and removed old measured-viewer claims
from the editor prompt and topic-picking rules. Videos, topic-repeat history and vault Short pages remain. Existing unrelated channel
profile/research edits are excluded from this commit.
Verification: 149 tests pass across 9 suites, including 10 new retention tests; Python compilation and diff
check pass. Golden prompt differences reviewed before re-saving: only topics/writer lessons and editor's old
performance assertions changed. Archived files verified byte-for-byte by hash. No real Studio screenshot was
provided yet, so no live visual-AI retention result is claimed and no test data was put into actual outputs.


### 2026-10-31: reliability follow-up (all four improvements approved by owner)
- Completed scripts are queued atomically in work/progress.json before SEO, then checkpointed after picture
  selection, voice and encoding. Batch errors preserve folders and continue; run.bat offers resume, resume.bat
  resumes directly, and the CLI accepts resume [folder]. Unfinished work is excluded from seven-day pruning.
  New batches choose a non-existing output folder, preserving old results with the same title.
- save_state now commits JSON atomically and writes background/person blobs through temporary files. Encoding
  targets work/rendering.mp4 and replaces short.mp4 only after success. render-context.json stores the data
  needed by finish_render(), with explicit JSON tags for bytes/paths (no pickle/executable serialization).
  A rendered-stage resume goes straight to reports/reviews. Profile/logbook finalization is repeatable and does
  not duplicate an existing folder's logbook entry. An interrupted planning call itself is not checkpointed;
  completed scripts are. Legacy outputs do not retroactively gain batch checkpoints.
- voice_cache stores per-scene audio and word timings, checked against narration, voice settings, speed,
  instruction/reference and audio hashes. Unchanged visuals can be rerendered without another voice job.
  A real FFmpeg render test caught and fixed concat paths for cached audio in a subdirectory.
- Visual and opening AI reviews now record Passed / Problems found / Not reviewed. Preview failure, absent or
  malformed replies produce NOT REVIEWED checks and no guessed image fixes. edit_plan.txt records statuses.
- fix.bat option 6 changes circle/arrow coordinates and label; option 3 can remove a mark with the same preview.
  The fast path renders only that still scene with hard cuts, replaces its upper card area and keeps original
  captions/audio. It produces preview.mp4 and sheet.jpg, asks the owner to apply, backs up the original video,
  state and reports, updates the storyboard/edit plan, and archives a stale Shotcut timeline. Other scenes
  fall back to ordinary repairs with narration caching. Manual edits invalidate the visual-review status.
- Picture downloads retry at most twice (Wikimedia retains its own existing retry/backoff). On selected-background
  failure, one AI selection may choose an unused reviewed, sharp, era-appropriate pool alternative. Failed URLs,
  reused candidates and unsafe portrait substitutions are excluded. Credits survive; old motion is disabled.
- While running the broad suite, long temporary paths exposed an existing drawn-opener diagnostic truncation:
  node_run kept the last 600 characters, losing the actual TypeError. It now keeps the error headline first;
  a new regression covers long paths and the existing real-node test passes.
- Verification: 22/22 suites pass (including 13 reliability regressions, real FFmpeg render/cache/resume smoke,
  real-node drawn openers and TypeScript runtime tests); compileall, tsc and git diff --check pass. Golden prompts
  unchanged. Real scene preview/apply exercised on an isolated copy of Mary Toft in test_renders/reliability-toft,
  with applied-sheet.jpg visually inspected and original audio SHA256 verified identical. No live AI quota spent.
  Owner's output files, profile/research edits and fresh logbooks remain untouched.
Usage/limitations: docs/reliability.md. Tracked checklist: docs/superpowers/plans/2026-10-31-reliability-improvements.md.
Retention Part 3.2 still awaits implementation and fresh results.
