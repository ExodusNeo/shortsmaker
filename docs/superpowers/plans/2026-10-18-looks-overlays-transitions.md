# Photo Looks, Overlays, Transitions and Inventions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Each Short gets an AI-chosen (or AI-invented) photo look, question beats, kinetic titles and per-cut transitions, built in Remotion, with owner-approved inventions growing a reusable library.

**Architecture:** A new `remotion/src/style/` folder holds three kinds of interchangeable components (look, overlay, transition) behind fixed interfaces, registered in `library.json`, with a Python-generated `index.ts` of static imports. `make_shorts.py` validates the planner's choices against six guardrails, passes them to Remotion through the existing props, and reuses the custom-scene machinery (lint, `tsc`, preview, look-and-fix, fallback) to invent new components into per-Short slots.

**Tech Stack:** Python 3.12 (`.venv`, Pillow, no numpy), Remotion 4 + React + TypeScript (`remotion/`), esbuild-bundled TS tests, ffmpeg.

**Spec:** `docs/superpowers/specs/2026-10-18-looks-overlays-transitions-design.md`

## Global Constraints

- The project is not a git repository: before editing an existing file, copy it to `backup/<name>_<YYYY-MM-DD>_before-<task-slug>.<ext>`; "commit" steps below mean "make that backup first".
- Run everything from `D:\ShortsMaker`. Python tests: `.venv\Scripts\python.exe tests\<file>.py` (plain asserts, no pytest). TS tests: `.venv\Scripts\python.exe tests\run_ts_tests.py` (runs every `tests\*.test.ts`). Type check: `cd remotion; npx tsc -p .` must print nothing.
- Existing suites must stay green after every task: `tests\test_full_scenes.py` (38), `tests\run_ts_tests.py`, `tests\test_qwen_voice.py` (via `local_ai\qwen_venv`).
- No test may call a real AI (`ask_ai`, `run_agy`) or the network: monkeypatch them.
- Never render while a batch runs (shared `remotion/public/job`): check for a running `make_shorts.py` first.
- Remotion code: animate only from `t` (interpolate/spring/math); no CSS `transition`/`animation`/`@keyframes`, no `setTimeout`/`setInterval`, no `fetch`. Canvas work once per scene via `delayRender`/`continueRender`.
- Guardrail caps (spec): question beat 1, kinetic titles 2, look scenes 4, special transitions (`wipe`, `whip`, `leak`, `invented`) 3, inventions 1 look + 1 overlay + 1 transition per Short; `recent_looks` keeps the last 2.
- Sound: everything high-passed at 220 Hz (existing library); no new loud whooshes: `whip` uses an existing `whoosh*.wav` at gain 0.2.
- Credits: `remotion/src/style/THIRD_PARTY.md` carries the MIT notices of Lemo-OPUSCAR (Copyright (c) 2026 LemoLab) and Showtime (Copyright (c) 2026 Favio Vazquez), saying ideas/style rules were adapted and no code copied.
- The owner is not a programmer: every user-facing printout (`library.bat`, edit_plan lines) is plain English.

## Review Focus

- A Short planned with a library name that no longer exists (renamed/rejected) must render with no look / a fade, never crash Remotion: covered in Task 7 (`test_unknown_names_fall_back`) and Task 1 (`index.ts` default-null lookups).
- A look on a scene whose picture fails to load in the browser (canvas error, CORS) must still show the plain picture: Task 4 (`Look` fallback on `onerror`, checked in the preview).
- `fix.bat` re-renders a Short whose state was saved before this feature (no `look`, old `transition` values): must render exactly as before: Task 8 (`test_old_state_renders_plain`).
- An invention that compiles but throws at render time must not lose the Short: Remotion failure already falls back to the Python renderer; Task 9 adds `test_invention_runtime_failure_uses_fallback` (slot restored, fallback preset used on retry).
- Approving a candidate whose code no longer compiles (library changed since) must leave the library unchanged: Task 10 (`test_approve_rolls_back_on_tsc_failure`).

---

## Phase 1: the library (ends at owner gate 1)

### Task 1: Style folder, interfaces, registry and generated index

**Files:**
- Create: `remotion/src/style/types.ts`, `remotion/src/style/kit.ts`, `remotion/src/style/library.json`, `remotion/src/style/index.ts` (generated), `remotion/src/style/generated/InventedLook.tsx`, `InventedOverlay.tsx`, `InventedTransition.tsx`, `remotion/src/style/THIRD_PARTY.md`, `tests/test_style.py`, `tests/style.test.ts`
- Modify: `make_shorts.py` (constants near `REMOTION`, new `style_library()`, `write_style_index()`)

**Interfaces:**
- Produces (TS, `types.ts`):
  - `type Inks = {paper: string; ink: string; accent: string; alarm: string}`
  - `type LookProps = {src: string; t: number; start: number; end: number; inks: Inks; seed: number}`; `type Look = React.FC<LookProps>`
  - `type OverlayProps = {graphic: Graphic; t: number; start: number; end: number; variant: number}` (Graphic from `../Short`); `type Overlay = React.FC<OverlayProps>`
  - `type TransitionFrame = {from?: React.CSSProperties; to?: React.CSSProperties; cover?: React.ReactNode}`; `type Transition = {duration: number; render: (p: number, inks: Inks, seed: number) => TransitionFrame}` (`p` 0..1 across the transition, centred on the cut)
- Produces (TS, `kit.ts`): `inksOf(theme: {accent: string; emphasis: string; panel: string}): Inks` (paper `#EFE6D2`, ink = `panel`, accent = `accent`, alarm = `emphasis`); `noise(seed: number, x: number): number` (deterministic 0..1); `clamp01(x)`; `useOnceCanvas(src: string, draw: (ctx: CanvasRenderingContext2D, img: HTMLImageElement, w: number, h: number) => void): string | null` (loads the image, draws once inside `delayRender`/`continueRender`, returns a data URL, `null` on error).
- Produces (TS, `index.ts`, generated): `LOOKS: Record<string, Look>`, `OVERLAYS: Record<string, Overlay>`, `TRANSITIONS: Record<string, Transition>`; each map always contains `invented` (the slot); `lookFor(name?: string | null): Look | null`, `overlayFor(style: string): Overlay | null`, `transitionFor(name?: string | null): Transition` (unknown -> `fade`).
- Produces (Python): `STYLE_DIR = REMOTION / "src" / "style"`, `STYLE_LIBRARY = STYLE_DIR / "library.json"`; `style_library(kind: str | None = None) -> list[dict]` (entries `{name, kind, description, fits, file, origin}`); `write_style_index() -> None` (rewrites `index.ts` from `library.json` + the three slots, sorted, deterministic).

- [ ] **Step 1: Write failing tests.** `tests/test_style.py::test_write_style_index_is_deterministic` (write twice, identical text; every library `file` appears as an `import`; `invented` entries for all three kinds present) and `test_library_entries_have_fields` (every entry has the 6 fields, `kind` in look/overlay/transition, names unique, lowercase `[a-z0-9-]`). `tests/style.test.ts`: `transitionFor('nope') === TRANSITIONS.fade`, `lookFor(null) === null`, `inksOf({accent:'#FFD400', emphasis:'#FF7A1A', panel:'#0d1320'}).ink === '#0d1320'`, `noise(3, 0.5) === noise(3, 0.5)`.
- [ ] **Step 2: Run both; expect FAIL** (missing module / function).
- [ ] **Step 3: Implement.** `library.json` starts with the three transitions that exist today as components in `style/transitions/`: `cut` (duration 0, `to` opaque from p≥0.5), `fade` (duration = 0.3, today's crossfade), `flash` (duration 0, hard cut; the white flash stays drawn by `Short.tsx`'s existing flash layer). Slots export placeholders: `InventedLook` renders the plain picture, `InventedOverlay` returns `null`, `InventedTransition` equals `fade`. `THIRD_PARTY.md` per Global Constraints.
- [ ] **Step 4: Run the two test files and `npx tsc -p .`; expect PASS / no output.**
- [ ] **Step 5: Backup `make_shorts.py` first (`backup/make_shorts_2026-10-19_before-style-library.py`).**

### Task 2: Short.tsx plumbing (no visible change yet)

**Files:**
- Modify: `remotion/src/Short.tsx` (`Scene`, `Graphic`, `ShortProps`, `Background`, the scenes map, `GraphicFor`)
- Test: `tests/style.test.ts` (pure helpers only), visual regression via existing preview

**Interfaces:**
- Consumes: Task 1 `lookFor`, `overlayFor`, `transitionFor`, `inksOf`.
- Produces: `Scene.look?: string | null`, `Scene.lookSeed?: number`, `Scene.transition: string` (was `'fade' | 'flash'`), `Graphic.style` adds `'question' | 'kinetic' | 'invented'`, `Graphic.trigger?: string`; exported pure helper `transitionWindow(scene: Scene, prev: Scene | undefined, xfade: number): {lead: number; p: (t: number) => number}` used by the scenes map (replaces the hard-coded `lead`/opacity).

- [ ] **Step 1: Failing TS test** `transitionWindow` for `fade` gives `lead = 0.15` and `p(scene.start) === 0.5`; for `cut` and `flash` `lead = 0`; for an unknown name it behaves like `fade`.
- [ ] **Step 2: Run; FAIL.**
- [ ] **Step 3: Implement.** `Background` draws `lookFor(scene.look)` in place of `<Img>` when set (same zoom/pan transform on a wrapper), else today's `<Img>`; incoming scene layer gets `transition.render(p).to`, the outgoing (previous) layer `from`, and `cover` is drawn above both scene layers and below graphics. `GraphicFor` checks `overlayFor(style)` first. Behaviour for `fade`/`flash` must be pixel-identical to today.
- [ ] **Step 4: TS tests + `tsc` pass; render `remotion\test_props\custom-flow.json` with `tests\render_full.py ... --still 2` before and after; the two stills match (same pixels by `ffmpeg -i a -i b -lavfi psnr` ≥ 40 dB).**
- [ ] **Step 5: Backup `Short.tsx` first.**

### Task 3: Transitions wipe, whip, leak

**Files:** Create `remotion/src/style/transitions/Wipe.tsx`, `Whip.tsx`, `Leak.tsx`; modify `library.json`; regenerate `index.ts`; test `tests/style.test.ts`.

**Interfaces:** each `export const <Name>: Transition`. Durations: wipe 0.44, whip 0.25, leak 0.5. Wipe: grid of circles (step 72 px, diagonal delay 0.12 s across the frame) in `inks.ink`, radius grows to full cover by p=0.5 and shrinks after; `to` invisible until p≥0.5. Whip: `from` translates 0→-35% with `filter: blur(0→18px)`, `to` from +35%→0 with blur 18→0, switch at 0.5. Leak: `cover` = radial warm gradient (`#FFB347`→transparent) whose opacity peaks 0.85 at p=0.5, `to` opacity crosses at 0.5.

- [ ] **Step 1: Failing TS tests:** each transition's `render(0).to?.opacity` is 0 (or undefined `to` hidden), `render(1).to` fully visible, `render(0.5).cover` exists for wipe and leak, durations match.
- [ ] **Step 2: FAIL. Step 3: implement. Step 4: tests + tsc pass. Step 5: backup `library.json`.**

### Task 4: Five preset looks

**Files:** Create `remotion/src/style/looks/Halftone.tsx`, `Engraving.tsx`, `Riso.tsx`, `Miniature.tsx`, `Silent.tsx`; modify `library.json` (+ `description`, `fits` from the spec's presets table); regenerate `index.ts`.

**Interfaces:** each `export const <Name>: Look`. All use `useOnceCanvas` at 1080x1920 for the still treatment and fall back to a plain `<Img src>` when it returns `null` (Review Focus). Per-frame layers only where the spec says (Silent: flicker `opacity 0.9..1` from `noise(seed, t*24)`, grain specks reseeded every 2 frames, 1-2 vertical scratches; nothing else animates).
- Halftone: cream paper; dot screen step 22 px at 15° in `inks.ink` with radius ∝ darkness (k = 0.7), second screen at 75° in `inks.accent` for mid-tones, offset +6/+6 px, multiply.
- Engraving: parallel lines (spacing 7 px, 30°) whose thickness follows darkness; cross-hatch at -30° where luminance < 0.35; sepia ink `#3B2A1A` on paper.
- Riso: two inks (`inks.ink`, `inks.accent`) by luminance bands with per-pixel grain, accent layer offset 4 px.
- Miniature: blur bands top 0-35% and bottom 70-100% (Gaussian-ish via canvas `filter: blur(14px)` composited with a vertical gradient mask), saturation 1.35, contrast 1.15.
- Silent: grayscale → sepia (`#704214` tint 0.35), vignette, plus the per-frame layers above.

- [ ] **Step 1: Test props.** Create `remotion/test_props/look-<name>.json` (one scene, 4 s, a real past photo copied into `remotion/test_props/media/`, `look: "<name>"`).
- [ ] **Step 2: Render each with `tests\render_full.py remotion\test_props\look-<name>.json --still 1` and `--still 3` before implementing: expect the plain picture (no look yet).**
- [ ] **Step 3: Implement the five looks.**
- [ ] **Step 4: Re-render the stills; view each; the look is visible, the subject still readable, no blank or black frame; note render time per 4 s scene (target ≤ 1.5x the plain scene).** `tsc` passes.
- [ ] **Step 5: Backup `library.json`.**

### Task 5: Overlays question and kinetic

**Files:** Create `remotion/src/style/overlays/QuestionBeat.tsx`, `KineticTitle.tsx`; modify `library.json`, regenerate `index.ts`; test props `remotion/test_props/overlay-question.json`, `overlay-kinetic.json`.

**Interfaces:** `export const QuestionBeat: Overlay`, `export const KineticTitle: Overlay` (library names `question`, `kinetic` = the graphic `style`).
- QuestionBeat: dims the frame (black, opacity 0 → 0.3 over 0.25 s from `start`), centred text (FONT, 110 px max, wraps to ≤ 3 lines, `outline(7)`), pops in with a back-ease scale 0.6→1 over 0.35 s, a gentle 2 % pulse while held, holds to `end`, never below y 1150 (captions).
- KineticTitle: one glyph per span, each drops 60 px and squashes in (`scale(1.15, 0.85)` → 1) over 0.3 s with 0.05 s stagger from `start`; offset shadow +8/+8 in `theme.accent`; sits in the graphic slot (`slot(graphic, 300)`).

- [ ] **Step 1: Render the two test props as stills at 0.2 s and 1.5 s after the graphic's `at` (expect the fallback `Callout`).**
- [ ] **Step 2: Implement. Step 3: re-render; question readable and centred, above the captions; kinetic letters land in order. `tsc` passes. Step 4: backup.**

### Task 6: Preview video for the owner (gate 1)

**Files:** Create `tests/render_style.py`; output `test_renders/STYLE_PREVIEW.mp4`.

**Interfaces:** `render_style.py` builds one props file: for each look 2 real photos from past Shorts' `work/keep_*_bg.bin` (decoded to jpg, ≥ 2 different Shorts), each 3 s with a title card naming it; then the two overlays; then the six transitions between two photos, each labelled. Renders with the same flags as `render_remotion` and prints the total render time.

- [ ] **Step 1: Run it; open the video; check every item is labelled and plays.**
- [ ] **Step 2: Show the owner. Record each preset's verdict in `.superpowers/sdd/2026-10-18-looks-overlays-transitions/progress.md`. Rejected presets are removed from `library.json` (and `index.ts` regenerated) before Phase 2. STOP until the owner has answered.**

## Phase 2: planning

### Task 7: Validation and guardrails

**Files:** Modify `make_shorts.py` (`GRAPHIC_STYLES`, `PLANNED_STYLES`, `REMOTION_ONLY`, `clean_graphic`, the per-scene plan loop at the `sc["transition"] = ...` line, new functions); test `tests/test_style.py`.

**Interfaces:**
- `STYLE_CAPS = {"question": 1, "kinetic": 2, "invented": 2, "look_scenes": 4, "special": 3}`; `SPECIAL_TRANSITIONS = {"wipe", "whip", "leak", "invented"}`.
- `clean_graphic` accepts `question` (text ≤ 6 words, ends with `?`, upper-cased ≤ 40 chars), `kinetic` (1-4 words, ≤ 20 letters, every word spoken in the scene; `trigger` required and spoken), `invented` (text ≤ 6 words; `trigger` optional). All three join `PLANNED_STYLES` and `REMOTION_ONLY`.
- `clean_look(v, ch: dict) -> dict | None`: `{"name": <library look>}` unless the name is in `ch.get("recent_looks", [])[-2:]`; or `{"name": "invented", "title": str[:40], "brief": str[:400], "fallback": <library look>}` from `{"invent": {...}}` (fallback must be a library look); else `None`.
- `clean_transition(v) -> str`: a library transition name or `"invented"`, else `"fade"`.
- `limit_style(scenes: list[dict]) -> None`: scene 0 keeps `graphic` only for non-new styles and `transition` irrelevant; keeps the first `STYLE_CAPS[...]` question/kinetic/invented graphics, drops the rest; at most `STYLE_CAPS["special"]` special transitions (later ones become `"fade"`).

- [ ] **Step 1: Failing tests:** `test_clean_question_and_kinetic` (a question without `?` → None; a kinetic word not spoken → None; 5-word kinetic → None), `test_unknown_names_fall_back` (`clean_transition("dissolve") == "fade"`, `clean_look({"name": "nope"}, {}) is None`), `test_recent_looks_blocked`, `test_invented_look_needs_fallback`, `test_limit_style_caps` (2 questions → 1; 4 wipes → 3 then fade; question on scene 0 → dropped).
- [ ] **Step 2: FAIL. Step 3: implement; the plan loop calls `clean_transition` and, after `limit_full`, `limit_style`. Step 4: new tests + the 38 existing pass. Step 5: backup.**

### Task 8: Director, picker, props, sounds, edit plan, profile

**Files:** Modify `make_shorts.py`: `direct_scripts` prompt + parsing, `choose_images` prompt + parsing, `render_remotion` scene props, the renderer choice (the `n_graphics >= REMOTION_MIN_GRAPHICS or any(...)` condition), `sfx_events`, `edit_plan`, the profile update next to `recent_shapes`, the Python renderer's graphic fallback; test `tests/test_style.py`.

**Interfaces:**
- Director prompt adds: the library list (`style_library()` as `name — kind — description — fits`), the Short-level `look` field (library name, `{"invent": {"title", "brief", "fallback"}}`, or null; "null is a good answer"), per-scene `transition` (any library transition or `"invented"`, plus a Short-level `invented_transition: {"title", "brief", "fallback"}` when used), the new graphic styles and an optional Short-level `invented_overlay: {"title", "brief", "fallback"}`, the six guardrails and caps as plain rules. Parsed into `short["look"]`, `short["invented_transition"]`, `short["invented_overlay"]` (validated like `clean_look`).
- Picker: when `short["look"]`, its prompt names the look (name + description; for an invention its brief) and asks for `look_scenes: [scene numbers]` (still pictures that suit it, never scene 1, never film); parsed by `apply_look_scenes(short: dict, choices: list[dict], look_scenes) -> None` which sets `sc["look"] = short["look"]["name"]` on ≤ 4 valid scenes (no film, no `full`, not scene 0) and `sc["look_seed"] = i`.
- `render_remotion` scene props add `"look": sc.get("look")`, `"lookSeed": sc.get("look_seed", i)`; graphics pass `trigger`. Remotion is forced when any scene has a `look`, a new-style graphic or a transition not in {fade, flash}.
- `sfx_events`: `question` → `ticks` gain 0.25 prio 5; `kinetic` → `ticks` gain 0.3 prio 5; transition `whip` → `pick("whoosh", 4)` gain 0.2 prio 4 at the cut; others silent.
- `edit_plan`: `LOOK: <name> on scenes a, b` (or `none`), per scene `CUT IN: <transition>`, graphics lines name `question beat` / `kinetic title`.
- Profile: after a Short is made, `ch["recent_looks"] = (ch.get("recent_looks", []) + [name])[-2:]` for a library look.
- Python renderer: `question`/`kinetic`/`invented` draw as the `fact` box; looks ignored; non-fade/flash transitions play as `fade`.

- [ ] **Step 1: Failing tests:** `test_director_prompt_lists_library` (fake `ask_ai` captures the director prompt; every library name appears; `look` parsed), `test_apply_look_scenes` (scene 1, film and full scenes refused; > 4 trimmed), `test_remotion_forced_by_look`, `test_style_sounds` (whip gets a whoosh at gain 0.2; wipe silent), `test_fact_check_sees_new_graphics` (with a fake `ask_ai`, a scene's `question`/`kinetic` text appears in the fact-check prompt and `drop_graphic: true` removes it), `test_old_state_renders_plain` (a `state.json`-shaped short without `look` and with `transition: "fade"` produces props identical to today's for those keys).
- [ ] **Step 2: FAIL. Step 3: implement. Step 4: all Python tests pass; a fake-AI dry run of `write_scripts` (as in the 2026-10-18 pacing check) shows a look and transitions in the plan. Step 5: backup.**

## Phase 3: inventions and the library

### Task 9: Invent a component on the spot

**Files:** Modify `make_shorts.py` (new `invent_component`, `lint_style_code`, `style_rules`, wiring in `render_remotion` next to `code_custom_scenes`); test `tests/test_style.py`.

**Interfaces:**
- `style_rules(kind: str) -> str`: the kind's interface text, the Remotion rules (Global Constraints), "import only from 'react' and '../kit' (and '../types')", and the kind's preset files as worked examples.
- `lint_style_code(code: str, kind: str) -> list[str]`: like `lint_custom_code`: allowed imports only (`react`, `../kit`, `../types`); no CSS `transition`/`animation`/`@keyframes`; no `setTimeout`/`setInterval`/`fetch`/`XMLHttpRequest`/`eval`; must `export const Invented{Look|Overlay|Transition}` with the kind's type.
- `invent_component(kind: str, spec: dict, short: dict, work: Path) -> str`: returns the library name to use (`"invented"` on success, else `spec["fallback"]`). Steps: prompt (`ask_ai`, brief + scene narration + inks + `style_rules`), `clean_tsx_code`, lint, write slot, `tsc_check` (one repair), small preview of one scene using it (reuse `preview_custom`'s render pattern with `--scale=0.4`), one look-and-fix pass (rewrite must lint + compile), cache to `work/Invented<Kind>.tsx` with a signature first line (`// Invented<Kind>: <title> | <brief[:80]>`) so `fix.bat` reuses it, then `save_candidate(...)` (Task 10). The slot files are restored to their placeholders in `render_remotion`'s existing `finally:`.

- [ ] **Step 1: Failing tests with fake `ask_ai` and a fake `tsc_check`:** `test_invention_passes_into_slot` (slot written, returns `"invented"`, cache file starts with the signature), `test_invention_lint_failure_uses_fallback` (code importing `fs` → fallback name, slot back to placeholder), `test_invention_runtime_failure_uses_fallback` (the Remotion render raises: second attempt uses the fallback name and the Short renders), `test_slots_restored_after_render`.
- [ ] **Step 2: FAIL. Step 3: implement. Step 4: pass + existing suites. Step 5: backup.**

### Task 10: Candidates and `library.bat`

**Files:** Create `library.bat` (`.venv\Scripts\python.exe make_shorts.py library` + `pause`); modify `make_shorts.py` (`save_candidate`, `approve_candidate`, `reject_candidate`, `library_menu`, `main()` dispatch for `library`); test `tests/test_style.py`.

**Interfaces:**
- `CANDIDATES = STYLE_DIR / "candidates"`.
- `save_candidate(kind: str, title: str, brief: str, fits: str, code: str, preview: Path | None, short_title: str) -> Path`: folder `candidates/<kind>-<slug>/` with `Component.tsx` (export renamed from `Invented<Kind>` to a PascalCase name from the slug), `meta.json` `{name, kind, description, fits, brief, from_short, made}`, `preview.mp4` if given. Slug unique (`-2`, `-3`...).
- `approve_candidate(folder: Path) -> bool`: copies `Component.tsx` to `style/<kind>s/<Pascal>.tsx`, appends to `library.json` (`origin: "approved"`), `write_style_index()`, `tsc_check()`; on failure restores `library.json`, `index.ts` and removes the copied file, returns False; on success deletes the candidate folder.
- `reject_candidate(folder: Path) -> None`: deletes the folder.
- `library_menu() -> None`: lists candidates (kind, name, description, from which Short), opens `preview.mp4` with the default player (`os.startfile`), asks `1) Add to library 2) Throw away 3) Decide later` per candidate; prints plain-English results.

- [ ] **Step 1: Failing tests:** `test_save_candidate_unique_slug`, `test_approve_adds_to_library` (with `tsc_check` faked to None: file present, entry in `library.json`, import in `index.ts`, candidate gone), `test_approve_rolls_back_on_tsc_failure` (faked error: `library.json`/`index.ts` byte-identical to before, no leftover file, candidate kept), `test_reject_deletes`.
- [ ] **Step 2: FAIL. Step 3: implement. Step 4: pass. Step 5: backup.**

### Task 11: One real Short (owner gate 2) and handoff

**Files:** Modify `HANDOFF.md` (layout table: `remotion/src/style/`, `library.bat`; pipeline steps 3, 7 and 8; "How to verify" adds `tests\test_style.py`), `channels/strange-history.json` gets `recent_looks` automatically.

- [ ] **Step 1: Check no batch is running; run `.venv\Scripts\python.exe -u make_shorts.py 1 strange-history claude`.**
- [ ] **Step 2: Review: 1 frame/s sheet, `edit_plan.txt` (LOOK, CUT IN, QUESTION/KINETIC, INVENTED lines), render time vs. the Emu War run; list any CHECK lines.**
- [ ] **Step 3: Show the owner the Short and any candidate (`library.bat`). Update `HANDOFF.md` and the progress ledger. Backup `HANDOFF.md` first.**
