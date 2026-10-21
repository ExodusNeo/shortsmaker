# Full-screen Motion Graphic Scenes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Four full-screen, archival-style Remotion scene types (evidence board, map journey, big number, document) that the AI plans or uses to rescue weak footage.

**Architecture:** Each scene may carry a validated `full` object (Python, `make_shorts.py`). Python times it to the spoken words and passes it in `props.json`; `remotion/src/Short.tsx` draws the matching component from `remotion/src/full/` in place of the scene's picture. AI planning lives in the director prompt, the picture chooser, a new `rescue_graphics()` call and the review.

**Tech Stack:** Python 3 (`.venv`), Pillow, Remotion 4 / React 19 / TypeScript, d3-geo + world-atlas (installed), ffmpeg.

**Spec:** `docs/superpowers/specs/2026-10-17-fullscreen-motion-graphics-design.md`

## Global Constraints
- Look: style A "Archival documentary": ink `#2c1f0e`, red ink `#7a1d12`, palette accent (`theme.accent`) for one highlight per scene; aged paper, film grain, vignette, slow camera drift.
- Fonts offline from `remotion/public/fonts/` via `FontFace` + `staticFile`: EB Garamond (OFL) for headings/labels, Special Elite (Apache 2.0) for typed labels and telegrams.
- Caps: `MAX_FULL = 3` per Short; `MAX_FULL_PLANNED = 2`; never scene 1; never two adjacent `full` scenes.
- A `full` scene clears that scene's `graphic` and `person`.
- Board: 3-5 items, labels <= 3 words; needs >= 3 items with real pictures, else the scene falls back to the normal picture path. Real photos only.
- Journey: 1-4 stops, valid `coords()`; map data `world-atlas/countries-10m.json`.
- Number: icons exactly `person, coin, ship, house, train, soldier, animal, day`; at most 60 figures drawn.
- Document kinds exactly `newspaper, letter, telegram, form`; only `key_line` readable, filler lines unreadable; `paper` only if real (same rule as the headline card).
- All SFX high-passed at 220 Hz; new sound `scratch` (pen scratch).
- No git in `D:\ShortsMaker`: before the first change to a file, copy it to `backup/<name>_2026-10-17_before-full-scenes.<ext>`.
- Never render while a batch runs (check no `make_shorts.py` process first).
- Owner is not a programmer: edit_plan.txt and console lines in plain words.

## Review Focus
1. A timing word not spoken (fact check rewrote the line, or TTS split it): element still appears at an evenly spaced fallback time, never dropped or crashing. Test: `test_full_cues_fallback` (Task 7).
2. Journey stops far apart (London -> Sydney) or a single stop: camera fits every stop; one stop = push-in on it. Test: `journey-far.json` and `journey-one.json` renders (Task 2).
3. Huge or fractional numbers (1.5 million, 0.3): counter formats correctly; figures capped at 60 with `each` rescaled. Test: `test_number_scaling` (Task 6) + `number-million.json` render (Task 3).
4. Long text (a 14-word key line, 3-word labels, long place names): wraps inside the frame, never clipped. Test: `document-long.json` render (Task 5), `test_clean_full_limits` (Task 6).
5. Short scene (3 s) or Remotion failure: animations compress to fit; Remotion failure paints the `full` scenes and still finishes. Tests: `board-short.json` render (Task 4), `test_remotion_failure_paints` (Task 9).

---

### Task 1: Paper base, fonts and the `full` hook in Short.tsx

**Files:**
- Create: `remotion/src/full/Paper.tsx`, `remotion/src/full/FullScene.tsx`, `remotion/src/full/types.ts`
- Create: `remotion/public/fonts/EBGaramond-*.ttf`, `remotion/public/fonts/SpecialElite-Regular.ttf` (downloaded from the google/fonts GitHub repo, with their licence files)
- Create: `remotion/test_props/paper.json`, `tests/render_full.py`
- Modify: `make_shorts.py` (new `make_paper()`), `remotion/src/Short.tsx` (`Scene.full`, `Background`)

**Interfaces:**
- Produces (TS, `types.ts`):
  `FullBase = {type: 'board'|'journey'|'number'|'document'; seed: number}`;
  `FullProps<T> = {full: T; t: number; start: number; end: number}` (absolute seconds, like other graphics).
- Produces (TS, `Paper.tsx`): `<Paper t start end seed>{children}</Paper>` draws texture + grain + vignette and gives children a camera transform via render prop `camera: (cam: {x: number; y: number; scale: number}) => ReactNode`; `INK = '#2c1f0e'`, `RED = '#7a1d12'`, `SERIF`, `TYPE` font-family names; `useFonts()` loads both fonts with `delayRender`.
- Produces (TS, `FullScene.tsx`): `FullScene: React.FC<FullProps<FullBase>>` switching on `type` (placeholder `<Paper>` only until Tasks 2-5 fill it).
- Produces (Python): `make_paper() -> None` writes `remotion/public/paper/paper.jpg` (1300x2300, warm off-white with fibre noise and stains) and `grain0..5.png` (1080x1920 transparent noise); skips files that exist.
- Produces (tool): `tests/render_full.py <props.json> [--still SECONDS]` renders `remotion/test_props/<name>.json` through the `Short` composition to `D:\ShortsMaker\test_renders\<name>.mp4` (or a still `.png`) and a 1 frame/s contact sheet `<name>_sheet.jpg`. Copies `remotion/test_props/media/*` into `public/job/` first.

- [ ] **Step 1:** Back up `make_shorts.py`, `remotion/src/Short.tsx` per Global Constraints.
- [ ] **Step 2:** Implement `make_paper()` (Pillow: base colour `#eadcbf`, low-frequency blotches, fibre streaks, 2-3 faint stains; grain = per-frame random noise at alpha <= 0.18).
- [ ] **Step 3:** Add `full?: FullBase | null` to `Scene` in `Short.tsx`; in `Background`, `scene.full` renders `<FullScene full={scene.full} t={t} start={scene.start} end={scene.end} />` instead of `Img`/`OffthreadVideo` (opacity/crossfade logic unchanged).
- [ ] **Step 4:** Implement `Paper.tsx`: texture drifts <= 3% over the scene; grain frame = `Math.floor(t * 12) % 6`; radial vignette to `rgba(59,42,20,0.55)`; camera eased with `Easing.inOut(Easing.cubic)`.
- [ ] **Step 5:** Write `tests/render_full.py` and `remotion/test_props/paper.json` (one 5 s scene, `full: {type: 'board', seed: 1, items: []}` showing only the paper).
- [ ] **Step 6:** Run `cd remotion && npx tsc -p .` -> no errors; run `.venv\Scripts\python.exe tests\render_full.py remotion\test_props\paper.json` -> mp4 + sheet exist; view the sheet: paper fills the frame, grain moves, captions still on top.

### Task 2: Map journey scene

**Files:**
- Create: `remotion/src/full/Journey.tsx`; `remotion/test_props/journey-jack.json`, `journey-far.json`, `journey-one.json`
- Modify: `remotion/src/full/FullScene.tsx`, `remotion/src/full/types.ts`

**Interfaces:**
- Consumes: `Paper`, `INK`, `RED`, `SERIF`, `FullProps` (Task 1).
- Produces: `JourneyFull = FullBase & {type: 'journey'; stops: {name: string; lat: number; lon: number; at: number}[]; note?: string; noteAt?: number}`.

- [ ] **Step 1:** Write the three props files: Jack (Port Elizabeth lat -33.96 lon 25.60 -> Uitenhage lat -33.76 lon 25.40, note "1881 · 32 KM", 5.5 s), far (London -> Cape Town -> Sydney, 6 s), one (Uitenhage only, 4 s).
- [ ] **Step 2:** Implement `Journey.tsx`: `geoMercator().fitExtent` over the country containing the first stop (wide frame) then over the stops' bounding box padded 35% (close frame); camera interpolates wide -> close from `start` to the first stop's `at`; land fill `#cdbb95`, coast/border ink lines 1.2 px, faint graticule; route = dashed `RED` path drawn by `strokeDashoffset` between consecutive stops ending at each `at`; pin = red ink dot with paper ring, drops with `spring`; label = `SERIF` italic, wrapped at 14 chars, kept inside the frame; compass rose + `note` in small caps top area at `noteAt`. Single stop: close frame = 6° box around it.
- [ ] **Step 3:** Wire `type === 'journey'` in `FullScene.tsx`; `npx tsc -p .` -> no errors.
- [ ] **Step 4:** Render all three with `tests/render_full.py`; view sheets: every stop and label visible and inside the frame, route ends at the last pin, nothing cut by captions (labels stay above y = 1450 px).

### Task 3: Big number scene

**Files:**
- Create: `remotion/src/full/BigNumber.tsx`, `remotion/src/full/icons.tsx`; `remotion/test_props/number-norton.json`, `number-million.json`, `number-compare.json`
- Modify: `FullScene.tsx`, `types.ts`

**Interfaces:**
- Produces: `NumberFull = FullBase & {type: 'number'; value: number; show: string; label: string; icon: Icon; each: number; figures: number; at: number; compare?: {a_label: string; a_value: number; b_label: string; b_value: number}}`;
  `Icon = 'person'|'coin'|'ship'|'house'|'train'|'soldier'|'animal'|'day'`; `INK_ICONS: Record<Icon, (size: number, color: string) => JSX.Element>` (hand-drawn style SVG, 1 path each).
- Note: `show` (formatted final text, e.g. "30,000", "1.5 MILLION") and `figures` (<= 60) are computed in Python (Task 6); Remotion only animates.

- [ ] **Step 1:** Props: Norton (30000, show "30,000", label "MOURNERS", person, each 1000, figures 30), million (1500000, "1.5 MILLION", coin, each 50000, figures 30), compare (a "1858" 100 vs b "TODAY" 3, two bars).
- [ ] **Step 2:** Implement: number counts from 0 to `value` over 1.0 s from `at` (eased), displayed with the same unit style as `show` (so "1.5 MILLION" counts as "0.4 MILLION"…); label in `SERIF` small caps with a red ink rule; figures fill row by row in a grid (5-6 per row) after the count, each ink-stamped in with a tiny scale-in; caption "EACH = 1,000" under the grid; `compare` draws two ink-hatched bars growing to scale instead of figures.
- [ ] **Step 3:** Wire in `FullScene.tsx`; `npx tsc -p .` -> no errors.
- [ ] **Step 4:** Render the three; view: counter text never wider than 960 px, figures inside the frame and above the captions, bars proportional.

### Task 4: Evidence board scene

**Files:**
- Create: `remotion/src/full/Board.tsx`; `remotion/test_props/board-jack.json`, `board-short.json`; `remotion/test_props/media/` (4 real photos copied from the Jack and Norton `work/` folders)
- Modify: `FullScene.tsx`, `types.ts`

**Interfaces:**
- Produces: `BoardFull = FullBase & {type: 'board'; items: {image: string; aspect: number; label: string; at: number}[]; links: [number, number][]}` (`image` = `job/...` path).

- [ ] **Step 1:** Props: Jack board (4 items, 6 s, links [[0,1],[1,2],[2,3]]); short board (3 items, 3 s).
- [ ] **Step 2:** Implement: dark cork/board background under the paper texture edge (board = `#3b2c1e` with subtle noise, paper vignette on top); layout = one of 3 seeded arrangements, prints rotated ±6°, white border + slight sepia filter (`sepia(0.35) contrast(1.05)`), drop shadow, a red pin at the top; each print pops in at its `at`; camera centres the newest print (scale 1.25) and pulls back to show all by `end - 0.8`; red thread (`RED`, 3 px, slight sag curve) draws between linked prints after both are visible; label on a typed paper slip (`TYPE`) under each print. Short scenes: all timings compress proportionally, the pull-back still happens.
- [ ] **Step 3:** Wire in `FullScene.tsx`; `npx tsc -p .` -> no errors.
- [ ] **Step 4:** Render both; view: prints never leave the frame on pull-back, labels readable, thread attaches at the pins.

### Task 5: Paper & documents scene

**Files:**
- Create: `remotion/src/full/Document.tsx`; `remotion/test_props/document-telegram.json`, `document-newspaper.json`, `document-long.json`, `document-scan.json`
- Modify: `FullScene.tsx`, `types.ts`

**Interfaces:**
- Produces: `DocumentFull = FullBase & {type: 'document'; kind: 'newspaper'|'letter'|'telegram'|'form'; key_line: string; date?: string; paper?: string; image?: string; aspect?: number; at: number; lineEnd: number}` (`at` = underline starts, `lineEnd` = underline finished).

- [ ] **Step 1:** Props: telegram (Special Elite strips pasted on a form), newspaper (masthead only when `paper` given, else a generic rule; columns of faded filler lines as grey bars), long (14-word key line), scan (real scan image: underline drawn at the vertical centre band, label-free).
- [ ] **Step 2:** Implement: document sheet fills ~90% width, slight rotation, camera pushes in from 1.0 to 1.35 toward the key line; key line typeset large and readable, wrapped to <= 3 lines; filler = blurred grey bars (never text); red ink underline drawn by `strokeDashoffset` from `at` to `lineEnd` with a hand-drawn wobble; `date` in the corner; letter = handwriting-like slant using `SERIF` italic.
- [ ] **Step 3:** Wire in `FullScene.tsx`; `npx tsc -p .` -> no errors.
- [ ] **Step 4:** Render all four; view: key line fully inside the frame at max zoom, nothing readable except the key line, date and real masthead.
- [ ] **Step 5 (owner gate):** Send the owner the 13 test renders' paths (`D:\ShortsMaker\test_renders\`) and a one-line description of each; stop until they approve or ask for changes. Do not start Task 6 before approval; rejected types are removed from `FULL_TYPES` in Task 6.

### Task 6: `clean_full()` validation and caps

**Files:**
- Create: `tests/test_full_scenes.py` (plain asserts; run with `.venv\Scripts\python.exe tests\test_full_scenes.py`)
- Modify: `make_shorts.py`: constants near `PLANNED_STYLES` (~line 57), new `clean_full()` after `clean_graphic()` (~line 845), scene validation loop at the end of `write_scripts()` (~lines 548-569)

**Interfaces:**
- Produces: `FULL_TYPES = ("board", "journey", "number", "document")`, `ICONS`, `DOC_KINDS`, `MAX_FULL = 3`, `MAX_FULL_PLANNED = 2`, `MAX_FIGURES = 60`.
- Produces: `clean_full(f, said: list[str]) -> dict | None` returning the normalized dicts below (strings stripped, labels upper-cased, `word` kept only when `contains(said, words_of(word))`):
  - board `{"type", "items": [{"label" (<=3 words, <=24 chars), "find" (<=120), "word"?}] (3-5), "links": [[a, b]] (valid indexes, a != b)}`
  - journey `{"type", "stops": [{"name" (<=28), "lat", "lon", "word"?}] (1-4, coords()), "note"? (<=24)}`
  - number `{"type", "value" (0 < v < 1e12), "show", "label" (<=24), "icon" in ICONS else "person", "each", "figures" (1..60), "word"?, "compare"? }`
  - document `{"type", "kind" in DOC_KINDS, "key_line" (<=14 words), "date"?, "paper"?, "find"?, "word"?}`
- Produces: `number_figures(value: float, each) -> tuple[float, int]` (if `each` missing/invalid or value/each > 60: smallest "round" each from 1/2/5 x 10^k with value/each <= 60) and `show_number(value: float) -> str` ("30,000", "1.5 MILLION", "2 BILLION", "0.3").
- Produces: `limit_full(scenes: list[dict], planned_max: int) -> None` enforcing: `scenes[0]["full"] = None`; no two adjacent (keep the earlier); at most `planned_max`; a kept `full` sets `graphic` and `person` to None.

- [ ] **Step 1:** Back up `make_shorts.py` if not done. Write tests: `test_clean_full_board` (2 items -> None; 6 items -> first 5; bad link dropped), `test_clean_full_journey` (lat 200 -> stop dropped; 0 stops -> None), `test_clean_full_document` (15-word key line -> None; kind "memo" -> None), `test_clean_full_limits` (28+ char names trimmed, word not spoken -> no `word`), `test_number_scaling` (30000 each 1000 -> 30 figures; 1.5e6 no each -> each 50000, 30 figures; show "1.5 MILLION"; 0.3 -> "0.3"), `test_limit_full` (scene 1 cleared; adjacent pair keeps the first; 3 planned with max 2 -> 2; graphic/person cleared).
- [ ] **Step 2:** Run tests -> FAIL (`clean_full` not defined).
- [ ] **Step 3:** Implement the constants and functions; in the `write_scripts()` validation loop call `sc["full"] = clean_full(sc.get("full"), said) if i else None` before the graphic/person lines, then `limit_full(s["scenes"], MAX_FULL_PLANNED)` after the loop.
- [ ] **Step 4:** Run tests -> PASS; `.venv\Scripts\python.exe -m py_compile make_shorts.py` -> no output.

### Task 7: Director prompt, fact check and word timing

**Files:**
- Modify: `make_shorts.py`: `direct_scripts()` prompt (~line 640-725), `fact_check()` script list and fix loop (~lines 735-790), `scene_cues()` (~line 2507)
- Test: `tests/test_full_scenes.py`

**Interfaces:**
- Consumes: `clean_full()`, `limit_full()` (Task 6).
- Produces: `full_cues(full: dict, words: list[tuple[float, float, str]], start: float, end: float) -> dict` returning the Remotion timing fields for the type: board `items[k].at`; journey `stops[k].at`, `noteAt`; number `at`; document `at`, `lineEnd`. A missing/unspoken `word` gets an evenly spaced fallback in `[start + 0.4, end - 1.0]`; times sorted ascending for board/journey. `scene_cues()` stores it as `cue["full"]`.
- Produces: fact-check fix field `drop_full: bool` and `full_fix: dict | null` (corrected `full` run through `clean_full`).

- [ ] **Step 1:** Tests: `test_full_cues_fallback` (journey with 3 stops, 2nd word unspoken -> 3 ascending times inside the window), `test_full_cues_document` (`lineEnd` = end of the last key-line word when spoken, else `at + 1.2`), `test_director_prompt_mentions_full` (monkeypatch `ask_ai` to capture the prompt and return canned JSON with a `full` on scene 1 and scene 3 -> after `write_scripts` validation scene 1 has none, scene 3 keeps it), `test_fact_check_drops_full` (canned reply `drop_full: true` -> `sc["full"]` None).
- [ ] **Step 2:** Run -> FAIL.
- [ ] **Step 3:** Add to the director prompt: the four types with one JSON example each, "use on at most 2 scenes, only where it shows the moment better than any picture (a trip between places, a hard-to-picture number, a document that matters, several people or things that connect); never scene 1, never two in a row; real facts only; board items describe real photos to find (`find`); `paper` only for a real paper that covered it"; add `"full": null` to the reply schema. Add `full` to the fact-check script items and the rules ("drop_full = true when it shows a wrong fact; full_fix = corrected version"); apply in the fix loop. Implement `full_cues()` with `spoken_at()`.
- [ ] **Step 4:** Run tests -> PASS; `py_compile` clean.

### Task 8: Pictures for boards/documents and `rescue_graphics()`

**Files:**
- Modify: `make_shorts.py`: `choose_images()` scene list, rules and result loop (~lines 1561-1650); new `rescue_graphics()` after `choose_images()`; `save_state()` / `load_state()` (~2719-2745)
- Test: `tests/test_full_scenes.py`

**Interfaces:**
- Consumes: `clean_full()`, `limit_full()`, `MAX_FULL`.
- Produces: picker reply field per scene `full_pictures: [int|null]` (one per board item / one for a document). `choose_images()` result gets `result["full_pics"] = [(bytes, title, credit) | None, ...]`. A board with < 3 pictures sets `short["scenes"][i]["full"] = None`.
- Produces: `rescue_graphics(short: dict, scenes: list[int], why: dict[int, str]) -> list[int]` (one `ask_ai` call with the scenes' narration, the reason, and `short["_texts"]`/Wikipedia text; may return `full` only of type journey/number/document (no pictures needed); runs `clean_full`, respects `MAX_FULL` counting existing `full` scenes and adjacency; returns the scene indexes that got one).
- Produces: `save_state` writes `keep_{i}_full{k}.bin` for each picture in `full_pics`, `load_state` restores them.
- Note: `short["_texts"]` must be kept (not popped) after `fact_check()` for the rescue; store as `short["research"]` and exclude it from `state.json`.

- [ ] **Step 1:** Tests (monkeypatched `ask_ai`, fake `get_image`): `test_board_pictures_attached` (3 of 4 pictures found -> kept, 2 found -> `full` None), `test_rescue_respects_caps` (2 `full` already + rescue for 2 scenes -> only 1 added, never adjacent), `test_state_roundtrip_full_pics` (save then load -> same bytes).
- [ ] **Step 2:** Run -> FAIL.
- [ ] **Step 3:** Implement. In the picker rules add: "For scenes with a board or document, also pick `full_pictures`: for each board item the candidate showing what its `find` describes (real photos only, never the same candidate twice), for a document a real scan of that document or null." In `render()` (first render only, `state` is None), after `choose_images()`: scenes with `bg` None and no `full` go to `rescue_graphics()` with why "no fitting picture"; only the rest are painted.
- [ ] **Step 4:** Run tests -> PASS; `py_compile` clean.

### Task 9: Render integration, sound and edit plan

**Files:**
- Modify: `make_shorts.py`: `render()` renderer choice and fallback (~2840-2860), `render_remotion()` (~2373), `sfx_events()` (~2305), `make_sfx()` + `SFX_FILES` (~1834), `edit_plan()` (~2418), `graphics_count()`; also call `make_paper()` before Remotion renders
- Test: `tests/test_full_scenes.py`

**Interfaces:**
- Consumes: `cue["full"]` (Task 7), `choices[i]["full_pics"]` (Task 8), `make_paper()` (Task 1).
- Produces: props scene field `full` = the plan's `full` merged with `cue["full"]` timings, `seed = i`, `show`/`figures` for numbers, and pictures copied to `job/full{i}_{k}.jpg` with `aspect`.
- Produces: `FULL_NAMES = {"board": "evidence board", "journey": "map journey", "number": "big number", "document": "document"}`; edit_plan line `  MOTION GRAPHIC: <name>: <summary> (planned | rescued: <why>)` replacing IMAGE/CAMERA for that scene; summary = stop names joined " -> " + note / `show label` / item labels / `kind: "key line"`.

- [ ] **Step 1:** Tests: `test_remotion_props_full` (fake scene with journey + cues -> props scene has `full.stops[k].at`, `seed`), `test_remotion_failure_paints` (monkeypatch `render_remotion` to raise -> the `full` scene gets `full = None`, an `ai_image` built from its shot note, and `paint_new`-style painting is requested; edit_plan contains "painted instead of the motion graphic (Remotion failed)"), `test_sfx_full` (board -> one `pin` per item; journey -> `scratch` under the route + `pin` per stop; number -> `ticks`; document -> `stamp` at scene start + `scratch` at `at`; all pass the 0.5 s collision rule).
- [ ] **Step 2:** Run -> FAIL.
- [ ] **Step 3:** Implement: any `full` forces Remotion; on Remotion failure set those scenes' `full` to None, paint them via the existing generation path (`gemini_images`/SDXL), rebuild their `{i}.jpg`, render with Python. Synthesize `scratch` in `make_sfx()` (band-passed noise bursts, 0.6 s, high-passed at 220 Hz like the others) and add to `SFX_FILES`. `graphics_count()` counts `full` scenes.
- [ ] **Step 4:** Run tests -> PASS; `py_compile` clean; `npx tsc -p .` clean.

### Task 10: Review rescue and fix.bat option 5

**Files:**
- Modify: `make_shorts.py`: `visual_review()` prompt and parsing (~2249-2285), auto-repaint block at the end of `render()` (~2943-2950), `fix_short()` (~3081)
- Test: `tests/test_full_scenes.py`

**Interfaces:**
- Consumes: `rescue_graphics()` (Task 8), `paint_new()`.
- Produces: `visual_review()` returns `(found, fixes)` with `fixes: dict[int, tuple[str, str]]` = scene -> (`"repaint"` | `"graphic"`, why). The review prompt asks for `fix: "repaint" | "graphic" | null` ("graphic" when the line is about places, numbers, a document or links between things; never for scene 1).
- Produces: fix.bat menu item `5) Turn it into a motion graphic (map, number or document)`; option 5 calls `rescue_graphics(short, [i], {i: "owner asked"})` and prints "No motion graphic fits this line; nothing changed." when it returns [].

- [ ] **Step 1:** Tests: `test_review_fix_kinds` (canned reply with one repaint and one graphic -> both parsed; `repaint: true` from old-style replies still maps to "repaint"), `test_auto_fix_graphic` (graphic fix -> `rescue_graphics` called; if it returns [] the scene is repainted instead; total fixes <= `AUTO_REPAINT_MAX`).
- [ ] **Step 2:** Run -> FAIL.
- [ ] **Step 3:** Implement; edit_plan "Fixed automatically" lines say "scene N became a motion graphic (why)".
- [ ] **Step 4:** Run all tests -> PASS; `py_compile` clean.

### Task 11: Full run and handoff

**Files:**
- Modify: `HANDOFF.md` (Layout table: `remotion/src/full/`, `tests/`, `test_renders/`; Pipeline steps 3, 5, 7, 9; fix.bat; Status), `C:\Users\ddgut\.claude\projects\C--Users-ddgut\memory\shortsmaker-project.md` (one dated line)

- [ ] **Step 1:** Confirm no `make_shorts.py` is running; run `.venv\Scripts\python.exe -u make_shorts.py 1 strange-history claude`.
- [ ] **Step 2:** Make the 1 frame/s sheet (`ffmpeg -i short.mp4 -vf "fps=1,scale=180:-1,tile=11x5" -frames:v 1 sheet.jpg`), view it, read edit_plan.txt `MOTION GRAPHIC` and `CHECK` lines. Expected: 0-3 motion graphic scenes, none in scene 1, none adjacent, each matching its line.
- [ ] **Step 3:** If the run had no `full` scene, run `fix.bat`'s option 5 path from a scratch script on a scene about a place or number of that Short to see one in a real render.
- [ ] **Step 4:** Update HANDOFF.md and the memory line; tell the owner in plain words what was made, where, and anything that looked off.
