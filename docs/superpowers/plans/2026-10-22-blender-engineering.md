# Blender Engineering Channel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Channels with `visuals: blender` get every scene drawn in Blender (ink-manual look, bridges assembling, zoom to the failing part, the failure animated) from an AI build plan, with one real photo of the structure as the thumbnail.

**Architecture:** An "engineer" AI call (instructions in the channel's `## Build plan` rules section) writes a JSON build plan per Short, cleaned by `blender_plan.py`. After the voice sets scene timings, `blender_render.py` writes `work/build.json` and runs headless Blender on `blender/build_scene.py`, which builds the structure from a parts kit and renders every frame; ffmpeg cuts them into one clip per scene, which the existing renderers treat like real film.

**Tech Stack:** Python 3.12 (`D:\ShortsMaker\.venv`), Blender 5.2.1 LTS headless (`D:\Blender\blender.exe`, EEVEE + Freestyle), ffmpeg, existing `llm.ask_ai`; plain-script tests.

**Spec:** `docs/superpowers/specs/2026-10-22-blender-engineering-design.md`

## Global Constraints

- Blender: `config.BLENDER = Path(r"D:\Blender\blender.exe")`; run `[BLENDER, "-b", "--factory-startup", "--python", "blender/build_scene.py", "--", <build.json>]`; timeout 30 minutes; one retry.
- Blender 5.2: render PNG frames (the `FFMPEG` file format no longer exists); look shader nodes up by `type`, never by name; set the render engine in `try/except TypeError` (`BLENDER_EEVEE_NEXT`, then `BLENDER_EEVEE`); a new Freestyle lineset needs `bpy.data.linestyles.new(...)`.
- Output 1080x1920, 30 fps, frames `work/blender_frames/f_0001.png`..., clips `work/blender{i}.mp4`.
- Colours: paper sky `#EEE8DC`, steel `#9EA8B3`, concrete `#E3DCCD`, water `#C3D7E5`, failure red `#D81F1A`, ink `#141419`.
- Allowed build-plan values and defaults: exactly the spec's "Build plan format" section.
- Every scene of a blender channel's video is Blender; no painting or photo fall-back. A Blender failure after the retry raises `blender_render.BlenderFailed`; `cli.main` keeps that Short's folder (work kept) and goes on.
- Photo channels must not change: `tests/golden/prompts.json` stays identical; all existing tests keep passing.
- Cross-module reads through the module (`session.RULES`, `blender_plan.clean_build`), as the code-layout rules require.
- Tests run as `.venv\Scripts\python.exe tests\<file>.py` from `D:\ShortsMaker`.
- Commits end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

- The engineer AI returns scene numbers out of range, duplicated, or as strings: `clean_build` ignores them and fills beats from the previous scene (test in Task 2).
- A Short with very few scenes (3) or many (18): `default_build` and the zoom/failure guarantee still give a valid beat list (test in Task 2).
- A very short scene (under 10 frames) or a scene boundary on a fractional frame: every frame belongs to exactly one clip and clips add up to the full length (test in Task 4).
- The owner re-runs after a crash: frames from a different `build.json` are never reused; identical `build.json` reuses them (test in Task 4).
- A topic pool with zero usable pictures: the thumbnail falls back to the zoom frame with a CHECK line, and the Short is not skipped (`min_real_pictures` 1 only gates topics; test in Task 5).

---

### Task 1: Rules accept Blender channels

**Files:**
- Modify: `shortsmaker/rules.py`
- Test: `tests/test_rules.py`

**Interfaces:**
- Produces: `rules.BLENDER_SECTION = "Build plan"`; `parse_rules` accepts `visuals: blender` and then requires `## Build plan` (same missing-section message); `PURPOSE["Build plan"]`; `draft_rules` asks for `Build plan` only when the reply's `visuals` is `blender` and treats a missing one then as a bad reply.

- [ ] **Step 1: Write the failing tests** — replace `test_blender_stops` with:

```python
def test_blender_needs_a_build_plan_section():
    blender = "status: ready\nvisuals: blender\nmin_real_pictures: 1"
    assert stop_text(make(Settings=blender)) == 'Stopped: channels/x.rules.md has no "## Build plan" section.'
    sections, settings = rules.parse_rules(make(Settings=blender) + "## Build plan\nplan it\n", LABEL)
    assert settings["visuals"] == "blender" and sections["Build plan"] == "plan it"

def test_photo_channels_dont_need_a_build_plan(): ...   # make() parses without "## Build plan"

def test_draft_blender_channel_needs_build_plan(): ...  # reply visuals "blender" without "Build plan": retried, then stop naming "Build plan"; with it: file has "## Build plan" and "visuals: blender"
```

- [ ] **Step 2: Run, expect FAIL** — `.venv\Scripts\python.exe tests\test_rules.py` → the three new tests fail (blender still stops as "not built yet").
- [ ] **Step 3: Implement** in `rules.py`.
- [ ] **Step 4: Run, expect PASS** — all of `tests\test_rules.py` passes.
- [ ] **Step 5: Commit** — `git add shortsmaker/rules.py tests/test_rules.py` / `git commit -m "feat: rules files can ask for Blender visuals (## Build plan)"`

### Task 2: Build plans (`blender_plan.py`) and the engineer step

**Files:**
- Create: `shortsmaker/blender_plan.py`
- Modify: `shortsmaker/writing.py` (end of `write_scripts`: `if session.RULE_SETTINGS.get("visuals") == "blender": blender_plan.plan_builds(kept, ch)`)
- Test: `tests/test_blender_plan.py`

**Interfaces:**
- Consumes: `session.RULES["Build plan"]` (Task 1).
- Produces:
  - `TEMPLATES`, `TRUSSES`, `DECKS`, `SETTINGS`, `FASTENERS`, `FOCUS_PARTS`, `FAILURES`, `THENS`, `SCALES`, `BEATS` (tuples, defaults first) and `RANGES = {"spans": (1, 5, 1), "span_m": (20, 1300, 100), "height_m": (2, 250, 15), "width_m": (4, 60, 15)}` (min, max, default).
  - `clean_build(raw, n_scenes: int) -> dict | None`: `{"structure": {...all keys}, "focus": {"part", "at": {"span", "panel", "chord", "side"}, "label"}, "failure": {"kind", "then", "span"}, "scale": [...], "beats": [beat for scene 0..n-1]}`; `None` when `raw` isn't a dict or `structure` isn't a dict.
  - `default_build(n_scenes: int) -> dict` (same shape; truss_bridge, focus gusset_plate at the middle span/panel, beats: scene 0 `failure_preview`, then `wide`, `build`… with the last third `zoom`, `failure`, `aftermath`, `"generic": True`).
  - `plan_builds(shorts: list[dict], ch: dict) -> None`: one `llm.ask_ai` for all Shorts (prompt = the code's format and allowed values + `session.RULES["Build plan"]` + each Short's index, title, narration lines and `research` text cut to 6000 chars); per Short `clean_build`, one retry call for the Shorts still `None`, then `default_build`; sets `s["build"]`, `s["build_check"]` (`"generic build plan: the engineer's plan was unusable"` or None) and every scene's `full`, `graphic`, `person` to `None`.
  - `thumbnail_photo(short: dict) -> int | None`: index into the pool candidates (`load_pool`) of the first usable catalog entry with `hook`, else the first usable, else None.

- [ ] **Step 1: Write the failing tests** (`tests/test_blender_plan.py`, runner as in `tests/test_story.py`):

```python
def test_clean_build_keeps_a_good_plan(): ...            # the spec's example plan, n_scenes=11 -> beats[0]=="failure_preview", beats[8]=="failure"
def test_bad_values_get_defaults(): ...                  # template "dam" -> "truss_bridge"; span_m 99999 -> 1300; fastener "screw" -> "rivet"; failure kind "melt" -> "bend"
def test_unlisted_and_bad_scenes_copy_the_previous_beat(): ...  # scenes [{"scene": "2", ...}, {"scene": 40, ...}, {"scene": 3, "beat": "dance"}] -> filled from previous; scene 1 -> failure_preview
def test_zoom_and_failure_are_guaranteed(): ...          # all "build" -> last third becomes zoom, failure, aftermath (n=3 and n=18)
def test_unusable_plan_is_none(): ...                    # "x", {}, {"structure": "truss"} -> None
def test_label_is_short_and_upper(): ...                 # 60-char lower label -> <=40 chars upper; non-str -> None
def test_default_build_shape(): ...                      # n in (3, 12, 18): len(beats)==n, "zoom" and "failure" in beats, clean_build(default_build(n), n) == default_build(n) minus "generic"
def test_plan_builds_retries_then_defaults(): ...        # fake ask_ai: first reply has Short 0 good, Short 1 garbage; retry still garbage -> Short 1 gets default + build_check; ask_ai called twice; scenes' full/graphic/person None
def test_thumbnail_photo_prefers_an_opener(): ...        # catalog with usable n=2 hook False, n=5 hook True -> 4; no hook -> 1; none usable -> None
def test_photo_channels_skip_the_engineer(): ...         # tests/test_rules.py golden still passes: run it from here via import and call
```

- [ ] **Step 2: Run, expect FAIL** — `ModuleNotFoundError: blender_plan`.
- [ ] **Step 3: Implement `blender_plan.py` and the `write_scripts` hook.**
- [ ] **Step 4: Run, expect PASS** — `tests\test_blender_plan.py` and `tests\test_rules.py` pass.
- [ ] **Step 5: Commit** — `git commit -m "feat: the engineer step writes a checked build plan per Short"`

### Task 3: Blender look, parts kit and truss bridge with build/zoom beats

**Files:**
- Create: `blender/look.py`, `blender/parts.py`, `blender/templates.py`, `blender/build_scene.py`
- Test: `tests/test_blender_scene.py` (runs the real Blender; skipped with a printed note when `config.BLENDER` is missing)

**Interfaces:**
- `build.json` (written by Task 4, hand-written in this test): `{"plan": <clean_build output>, "scenes": [{"start": 0.0, "end": 2.8, "peak": 1.9}], "fps": 30, "frames_dir": "<abs path>", "only_frames": [1, 40, 80] | null}` (`only_frames` renders just those frame numbers; tests use it).
- `look.setup(scene)`, `look.material(name) -> bpy.types.Material` (names: paper, steel, concrete, water, red, ink).
- `parts.py`: `deck`, `i_girder`, `truss_member`, `gusset_plate`, `fastener(kind)`, `eyebar`, `main_cable`, `hanger`, `tower`, `pier`, `abutment`, `bearing`, `water`, `valley`, `car`, `train`, `person`, `label(text, anchor_obj)`; each returns the created objects.
- `templates.build(structure) -> dict[str, list[obj]]` with keys `piers`, `deck`, `members`, `details` (assembly order) and `templates.focus_object(parts, focus) -> obj` (the named part, e.g. `span2_panel3_bottom_left_gusset`, or the nearest existing one).
- `build_scene.py`: reads build.json, builds, keyframes beats `wide`, `build`, `zoom` (others added in Task 3b), renders frames.

- [ ] **Step 1: Write the failing test** — `test_truss_build_and_zoom_frames`: plan = `default_build(4)` with beats `["wide", "build", "build", "zoom"]`, scenes 1.0 s each, `only_frames` = middle frame of each scene; run Blender; assert 4 PNGs exist, are 1080x1920; the zoom frame has ≥ 400 pixels within 30 of failure red and ≥ 200 near-ink pixels in the label area (bottom-right quarter is not required: anywhere); the first build frame differs from the second (parts arriving).
- [ ] **Step 2: Run, expect FAIL** — `blender/build_scene.py` missing.
- [ ] **Step 3: Implement** look, parts, the `truss_bridge` template (Warren/Pratt/Howe/K, 1-5 spans, named parts), and beats wide/build/zoom (camera keyframes, parts dropping in stage order across build scenes, detail fasteners + red + label fading in on zoom).
- [ ] **Step 4: Run, expect PASS**, then open the 4 frames with Read and check by eye (bridge readable, label legible at phone size). Adjust and re-run until they are.
- [ ] **Step 5: Commit** — `git commit -m "feat: Blender ink look, parts kit and truss bridge (wide, build, zoom)"`

### Task 3b: Failures, remaining beats and templates

**Files:**
- Modify: `blender/build_scene.py`, `blender/templates.py`, `blender/parts.py`
- Test: `tests/test_blender_scene.py`

**Interfaces:**
- Beats added: `orbit`, `failure` (peak at `scenes[i].peak`), `aftermath`, `failure_preview` (failure shown, then a camera cut and the story starts from an empty site).
- Failure kinds: `crack` (red curve grows on the focus), `bend` (simple-deform bend on the focus), `shear` (fastener kind decides: rivet heads/bolts pop out, pin slides out of a cracked eyebar, weld seam opens), `sway` (deck sway/twist with growing amplitude); `then: collapse_span` drops that span's parts into the water after the peak.
- Templates added: `girder_bridge`, `suspension_bridge`, `cable_stayed_bridge`, `eyebar_chain_bridge`.

- [ ] **Step 1: Write the failing tests** — `test_each_failure_changes_the_focus` (for each kind, frames before and after the peak differ around the focus: ≥ 2% of pixels changed); `test_collapse_moves_the_span_down` (aftermath frame has fewer steel pixels above the water line than the wide frame); `test_every_template_renders` (each template's wide frame has ≥ 5% steel/concrete pixels); `test_failure_preview_cuts_to_an_empty_site` (scene 2's first frame has fewer steel pixels than scene 1's last).
- [ ] **Step 2: Run, expect FAIL.**
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run, expect PASS**; check one frame per failure kind and template by eye with Read.
- [ ] **Step 5: Commit** — `git commit -m "feat: failure animations, collapse and the other bridge templates"`

### Task 4: `blender_render.py` (run Blender, cut clips, cache)

**Files:**
- Create: `shortsmaker/blender_render.py`; Modify: `shortsmaker/config.py` (`BLENDER`)
- Test: `tests/test_blender_render.py` (Blender faked by a tiny Python script that writes numbered PNGs)

**Interfaces:**
- Produces: `class BlenderFailed(RuntimeError)`; `scene_frames(bounds: list[float], fps: int = 30) -> list[tuple[int, int]]` (1-based first/last frame per scene, contiguous, covering `round(bounds[-1]*fps)` frames, each scene ≥ 1 frame); `peaks(short, bounds, all_words) -> list[float]` (`plan_rules.spoken_at` of the scene's `emphasis` within the scene, else 70% into the scene); `render_clips(short: dict, bounds: list[float], all_words: list, work: Path, exe: Path | None = None) -> dict[int, Path]` (writes `build.json`; skips Blender when `work/blender_frames/build.json` equals it and all frames exist; runs Blender with timeout 1800 s, one retry; on failure raises `BlenderFailed(reason)`; joins each scene's frames with ffmpeg into `work/blender{i}.mp4` with `-c:v h264_nvenc` falling back to `libx264`).

- [ ] **Step 1: Write the failing tests** — `test_scene_frames_cover_every_frame_once` (bounds with fractional and 0.2 s scenes); `test_peak_on_the_emphasis_word`; `test_render_clips_makes_one_clip_per_scene` (fake exe; clip durations match scenes within 1 frame); `test_same_build_json_reuses_frames` (fake exe counts runs: second call 0 runs; changed plan → runs again); `test_crash_retries_then_raises` (fake exe exits 1 twice → `BlenderFailed`, called twice); `test_missing_blender_raises`.
- [ ] **Step 2: Run, expect FAIL.**
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run, expect PASS.**
- [ ] **Step 5: Commit** — `git commit -m "feat: blender_render runs Blender headless and cuts one clip per scene"`

### Task 5: Wire it into a run

**Files:**
- Modify: `shortsmaker/short_render.py` (`render`), `shortsmaker/cli.py` (`main` failure handling), `shortsmaker/review.py` (`visual_review` note), `shortsmaker/picker.py` (none if not needed)
- Test: `tests/test_blender_run.py`

**Interfaces:**
- Consumes: `blender_plan.thumbnail_photo`, `blender_render.render_clips`, `BlenderFailed`.
- In `render`, when `short.get("build")`: choices are `{"bg": None, "person": None, "film": None}` per scene (no `choose_images`, no AI paintings, no thumbnail art); each scene's still is a plain frame until Blender is done, then `work/{i}.jpg` = the first frame of its clip; `sources[i] = f"drawn in Blender: {beat}"`; `clips = blender_render.render_clips(short, bounds, all_words, work)` instead of `gpu.local_clips`; thumbnail from `work/thumb_photo.jpg` (written from the pool candidate `thumbnail_photo` returns, credit line in `upload.txt`) else the first `zoom` scene's middle frame plus `CHECK: no real photo of the structure, the thumbnail uses a drawing`; `synthetic` ignores Blender clips; `short["build_check"]` becomes a CHECK line; `review.visual_review` gets `drawn=True` (adds "every scene is a deliberate ink drawing made in Blender, not a photo: don't flag drawings, labels or the red part") and its fixes become CHECK lines with no automatic fix rounds.
- `cli.main`: `except blender_render.BlenderFailed as e:` prints `Blender couldn't draw this Short ({e}); its files are kept in <folder>, run again to retry` and does not delete the folder.

- [ ] **Step 1: Write the failing tests** — `test_blender_short_renders_from_clips` (fake `render_clips` returning solid-colour clips, fake voice/TTS like `test_full_scenes.py` does; assert `choose_images` and painting never called, `edit_plan.txt` has "drawn in Blender", thumbnail exists); `test_thumbnail_uses_the_real_photo`; `test_no_photo_uses_a_drawing_and_says_so`; `test_blender_failure_keeps_the_folder` (cli with `render` raising `BlenderFailed`: folder still exists, batch continues to the next Short); `test_photo_channel_render_unchanged` (existing `test_full_scenes.py` passes).
- [ ] **Step 2: Run, expect FAIL.**
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run every test file, expect PASS** (test_qwen_voice's num2words import error is pre-existing).
- [ ] **Step 5: Commit** — `git commit -m "feat: blender channels render every scene in Blender, real photo on the thumbnail"`

### Task 6: Turn on the engineering channel and look at a real Short's frames

**Files:**
- Create: `channels/engineering-failures.json` (moved from `channel_ideas/`), `channels/engineering-failures.rules.md` (drafted by `require_rules`, a real AI call), then edited: `visuals: blender`, `min_real_pictures: 1`, a `## Build plan` section
- Modify: `HANDOFF.md` (new section "Blender channels"), code map refresh (`graphify update .`, `export obsidian --dir code-map`, `export html`)

- [ ] **Step 1: Draft the rules** — `.venv\Scripts\python.exe -c "from shortsmaker import rules; rules.require_rules('engineering-failures')"` → prints the drafted message. Keep `status: draft` (the owner reviews before the first real run).
- [ ] **Step 2: Sample render** — hand-write an I-35W build plan (truss_bridge, deck truss look, rivet fastener, focus gusset_plate U10, failure bend then collapse_span) with 12 scenes of 3 s; run `build_scene.py` with `only_frames` = one frame per scene; look at all 12 with Read; tune look/camera/labels until a stranger would read the bridge, the zoom and the failure at phone size. Save the 12 frames to `D:\ShortsMaker\output\_blender_sample\` for the owner.
- [ ] **Step 3: Docs and code map**; run every test file again.
- [ ] **Step 4: Commit** — `git commit -m "feat: engineering-failures channel (Blender), rules drafted for review; docs"`
