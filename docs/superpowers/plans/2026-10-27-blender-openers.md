# Blender Openers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every Short on a channel with `opener: blender` opens on a checked Blender animation of its strangest moment.
The opener is built from an AI staging plan and tested moves. Any failure falls back to today's scene 1. The plan
also adds the hook-line check.

**Architecture:**
- The AI writes a JSON staging plan per Short (`opener_plan.py`).
- Models come from a library on D:, filled through the owner's live Blender MCP add-on (`blender_link.py`).
- Headless Blender builds, animates, checks and renders scene 1 (`blender/opener_scene.py`, `moves.py`,
  `opener_checks.py`).
- `opener_render.py` runs it, reviews it, does up to 2 fix rounds, and hands `short_render.render` a clip for
  scene 1, or a CHECK line.

**Tech Stack:** Python 3.12 (.venv), Blender 5.2.1 headless (`D:\Blender\blender.exe`, plain bpy), the MCP add-on
socket (localhost:9876, JSON), ffmpeg, the existing `llm.ask_ai`.

**Spec:** `docs/superpowers/specs/2026-10-27-blender-openers-design.md`

## Global Constraints

- **Storage on D:.**
  - Library: `D:\ShortsMaker\blender\assets\library\<source>_<id>.blend` plus `.json`, gitignored.
  - Add-on temp folder: `D:\ShortsMaker\cache\blender_tmp`.
- **The AI never writes Blender code.** It only fills the plan format; `clean_opener` rejects anything outside the
  tables.
- **Model sources:** Poly Pizza (licences CC0 and CC-BY only) and Poly Haven models (CC0). Never Sketchfab.
- **An opener never stops a run.**
  - Failure: scene 1 stays as today, plus `CHECK: opener failed: <reason>` in the quality check.
  - At most 2 fix rounds.
  - Headless Blender: 10-minute timeout, retried once.
- **Fetching never touches the owner's open scene.** Downloads happen in a temporary scene that copies every
  `blendermcp_*` property from the owner's scene (the add-on's on/off switches are per scene), and the owner's
  scene is made active again afterwards.
- **Brand look (fixed):**
  - EEVEE, 1080x1920, 30 fps, AgX colour;
  - warm sun (energy 4.5, colour (1.0, 0.9, 0.75));
  - soft sky colour (0.55, 0.72, 0.92);
  - 50 mm lens, depth of field f/2.2 on the subject;
  - three-quarter camera (40 degrees around from the front) with a slow push-in, and a follow target when the
    subject moves.
- **Plan rules:**
  - at least one beat at or before 1.0 s;
  - sizes 0.05-30 m;
  - every id a beat names must exist;
  - moves, tools, gaits, grounds, lights, facings, angles and piece outcomes must be from the tables.
- **Check thresholds:**

  | Check | Threshold |
  |---|---|
  | In frame | 4-96% of the width, 3-97% of the height, every frame |
  | First frame | Subject at least 15% of the frame height at frame 0 |
  | Resting | Within 1 cm |
  | Blade face | At least 35 degrees off edge-on |
  | Cut share | ±50% of the planned share |
  | Pieces | At least 3 mm each, at most 80 per opener |
- **Repo conventions:**
  - Tests are plain functions plus the `__main__` runner used in `tests/test_blender_render.py`, run with
    `.venv\Scripts\python.exe tests\<file>.py`.
  - Cross-module calls go through the module (`llm.ask_ai`, `session.X`), so tests can swap fakes.
  - Module docstrings carry the date.
- **Commits** end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. After the last code commit,
  refresh the code map as its own "docs: refresh code map" commit (HANDOFF.md `code-map/` row).

## Review Focus

1. **Poly Pizza looks switched off in the temporary scene** (the probe hit this). `fetch_model` must report
   "Poly Pizza is switched off in Blender" as its failure reason, never crash or silently save nothing. Test in
   Task 3.
2. **The voice makes scene 1 shorter than the plan's beat times.** Beat times are scaled into the real scene
   length, so the last beat ends before the cut. Test in Task 6.
3. **A search result has a licence outside CC0 / CC-BY** (CC-BY-NC, unknown). It's never offered to the AI or
   saved. Test in Task 3.
4. **The fix round returns the same failing plan.** After 2 rounds it falls back with the last failure as the
   reason, with no endless loop. Test in Task 6.
5. **fix.bat or an automatic fix round re-renders the Short.** An unchanged opener plan plus code reuses
   `work/opener.mp4` without running Blender again. Test in Task 6.

---

### Task 1: Rules settings and the hook-line check

**Files:**
- Modify: `shortsmaker/rules.py` (settings accepted and validated), `shortsmaker/writing.py:286-340` (editor JSON
  plus `story_problems`)
- Modify: `channels/strange-history.rules.md`, `channels/weird-economics.rules.md` (`## Settings` plus one
  `## Story rules` line each)
- Test: `tests/test_story.py`

**Interfaces:**
- Produces:
  - settings `opener: blender | none` (missing = none) and `hook: moment | money_claim` (missing = no hook check);
  - `writing.story_problems(lines, payoff, list_like, hook_kind=None) -> list[str]`.

- [ ] **Step 1: Write the failing tests** in `tests/test_story.py`:
  - `test_story_problems_flags_summary_hook`:
    - with `session.RULE_SETTINGS = {"hook": "moment"}`, `story_problems(lines, None, None, "summary")` contains a
      problem with "inside the strangest moment";
    - with `"moment"` it has no hook problem.
  - `test_story_problems_money_claim`:
    - with `{"hook": "money_claim"}`, `hook_kind="moment"` gives a problem with "money figure";
    - `"money_claim"` gives none.
  - `test_no_hook_setting_no_hook_check`: `{}` with `"summary"` gives no hook problem.
  - `test_rules_accept_opener_setting`: `rules.parse_rules` on a Settings block with `opener: blender` and
    `hook: moment` returns them; `opener: maybe` raises SystemExit naming "opener".
- [ ] **Step 2: Run them.** `.venv\Scripts\python.exe tests\test_story.py` should FAIL (the extra argument and the
  settings don't exist yet).
- [ ] **Step 3: Implement.**
  - **Editor prompt:** add the line
    `hook_kind: "moment" if your first line happens inside the strangest moment, "summary" if it states the whole story, "money_claim" if it is a specific money figure tied to someone or something the viewer can picture.`
    and add `"hook_kind": "moment"` to the reply example.
  - **Passing it through:** `verdict` becomes a 3-tuple. A broken length rule resets it to `(None, None, None)`.
  - **Messages in `story_problems`:**
    - moment: `'the first line sums up the story: open inside the strangest moment, told as it happens (Voggle: "The axe cut off the rooster\'s head, but...")'`
    - money_claim: `'the first line needs a specific money figure tied to a person or thing the viewer can picture ("This man effectively created a free money machine...")'`
  - **rules.py:** validate the two settings the way `visuals` is validated.
  - **Rules files:** both get `opener: blender`; strange-history gets `hook: moment`, weird-economics gets
    `hook: money_claim`. Each gets the matching sentence under `## Story rules`.
- [ ] **Step 4: Run** `tests\test_story.py` and `tests\test_package.py`. Both should PASS.
- [ ] **Step 5: Commit** `feat: hook-line check and opener/hook rule settings`.

### Task 2: Opener plan (`shortsmaker/opener_plan.py`)

**Files:**
- Create: `shortsmaker/opener_plan.py`, `blender/opener_tables.json` (every table, read by both
  `opener_plan.py` and `blender/moves.py`, so there's one copy)
- Test: `tests/test_opener_plan.py`

**Interfaces:**
- Consumes: `llm.ask_ai(prompt, fatal=False)`, `session.RULES`.
- Produces:
  - tables loaded from `blender/opener_tables.json`: `GROUNDS`, `LIGHTS`, `FACINGS`, `ANGLES`, `MOVES`, `TOOLS`
    (dict name to stroke: `chop`, `press`,
    `saw`, `slash`, `drop`, `shape`), `GAITS`, `OUTCOMES` (`stay`, `fall`, `tip_over`, `fly_off`, `scatter`), and
    `CUT_FACE` (target word to RGB);
  - `clean_opener(raw) -> dict | None`;
  - `plan_openers(shorts: list[dict], ch: dict) -> None` (sets `s["opener"]` or `s["opener_check"]`);
  - `fix_plan(short: dict, failures: list[str]) -> dict | None`.

**Plan format:** exactly the spec's JSON. `MOVES` = `cut fall topple hop_off walk fly_off scatter sink roll push`.

- [ ] **Step 1: Write the failing tests:**
  - `test_spec_example_is_clean`: the spec's rooster plan passes unchanged.
  - `test_rejects_unknown_move_tool_and_id`: a beat with `move: "explode"` gives None; a cut with `tool: "laser"`
    gives None; a beat naming `actor: "dog"` that isn't in `actors` gives None.
  - `test_first_beat_by_one_second`: every `at` > 1.0 gives None.
  - `test_sizes_bounded`: `size_m` of 0.01 or 50 gives None.
  - `test_cut_needs_expect`: a cut without `expect` gives None; with `{"pieces": "40-60", "then": "scatter"}` it's
    clean.
  - `test_unbuildable`: `buildable: false` makes `plan_openers` set `opener_check` to
    "opener: not buildable (...)" and no `opener`.
  - `test_plan_retry_then_none`: a fake `llm.ask_ai` returns junk twice, so the Short gets `opener_check`
    "opener: no usable plan" and `ask_ai` was called exactly twice.
- [ ] **Step 2: Run.** `.venv\Scripts\python.exe tests\test_opener_plan.py` should FAIL (no module).
- [ ] **Step 3: Implement.**
  - `plan_openers` makes one batch call. The prompt holds each Short's scene 1 line, its narration and the
    research, plus the tables and the plan format. The section `## Opener` comes from `session.RULES` when the
    channel has one, otherwise a built-in default.
  - `fix_plan` makes one call with the plan and the failures and returns `clean_opener(reply)`.
- [ ] **Step 4: Run.** It should PASS.
- [ ] **Step 5: Commit** `feat: opener staging plans`.

### Task 3: Model library and Blender link (`shortsmaker/blender_link.py`)

**Files:**
- Create: `shortsmaker/blender_link.py`
- Modify: `shortsmaker/config.py` (`LIBRARY = ROOT / "blender" / "assets" / "library"`, `BLENDER_TMP = ROOT / "cache" / "blender_tmp"`, `MCP_PORT = 9876`), `.gitignore` (`blender/assets/library/`)
- Test: `tests/test_blender_link.py`

**Interfaces:**
- Produces:
  - `ping(timeout=2.0) -> bool`;
  - `call(cmd: str, params: dict, timeout=120) -> dict` (raises `LinkError(msg)`);
  - `in_library(find: str) -> Path | None` (matches the find words against each `.json`'s title and tags);
  - `search(find: str) -> list[dict]` (`{"source", "id", "title", "licence", "author"}`, only CC0 / CC-BY);
  - `fetch_model(hit: dict, find: str, size_m: float) -> tuple[Path | None, str]` (the `.blend` path, or None and
    the reason);
  - `credit(blend: Path) -> str | None` (the attribution line for CC-BY, else None).
- Socket protocol: send `{"type": cmd, "params": {...}}`; receive `{"status": "success", "result": ...}` or an
  error. The add-on's commands:
  - `ping`;
  - `search_polypizza_models(query, licence)` and `download_polypizza_model(model_id, normalize_size, target_size)`;
  - `search_polyhaven_assets(asset_type="models", ...)` and `download_polyhaven_asset(asset_id, asset_type)`;
  - `execute_code(code)`.

- [ ] **Step 1: Write the failing tests.** A fake server (a `socketserver` thread on a free port, with
  `config.MCP_PORT` patched) answers with canned replies.
  - `test_ping_on_off`: ping is True with the fake running and False with it stopped.
  - `test_search_filters_licences`: CC0, CC-BY 3.0 and CC-BY-NC results come back as only the first two.
  - `test_fetch_saves_pair`: the fake answers download success, then `execute_code` writes a dummy `.blend`.
    `fetch_model` returns that path, its `.json` has `title`, `author`, `licence`, `attribution`, `size_m`, and
    the find words in `tags`, and `credit()` returns the attribution for CC-BY and None for CC0.
  - `test_switched_off_reason`: the fake returns `"Poly Pizza is switched off..."`, so the result is
    `(None, ...)` with "switched off in Blender" in the reason.
  - `test_in_library`: a saved pair is found by `in_library("rooster")` and not by `in_library("baboon")`.
- [ ] **Step 2: Run.** `tests\test_blender_link.py` should FAIL.
- [ ] **Step 3: Implement.** `fetch_model` sends one `execute_code` that does all of the following before the
  download command:
  1. sets `tempfile.tempdir` to `BLENDER_TMP`;
  2. remembers the active scene;
  3. creates scene `SM_fetch`;
  4. copies every `blendermcp_*` property from the active scene into it;
  5. makes it active.

  After the download, a second `execute_code`:
  1. writes the new objects with `bpy.data.libraries.write(path, set(objects), fake_user=True)`;
  2. removes `SM_fetch` and its objects;
  3. restores the remembered scene.

  The `.json` is written by Python.
- [ ] **Step 4: Run.** It should PASS.
- [ ] **Step 5: Manual check with Blender open.** Fetch "tree stump" with
  `.venv\Scripts\python.exe -c "from shortsmaker import blender_link as b; h=b.search('tree stump')[0]; print(b.fetch_model(h,'tree stump',1.2))"`.
  The `.blend` and `.json` should appear in the library, and the owner's scene list should be unchanged
  afterwards (`OpenerTest_Mike` and `Scene` only).
- [ ] **Step 6: Commit** `feat: model library fetched through the Blender MCP add-on`.

### Task 4: Checks (`blender/opener_checks.py`)

**Files:**
- Create: `blender/opener_checks.py`, `tests/opener_check_cases.py` (a bpy script that builds tiny cases with
  primitives)
- Test: `tests/test_opener_checks.py` (runs real headless Blender on the cases script, about 1 min)

**Interfaces:**
- Produces (plain bpy; every function returns a list of failure strings like `"overlap: axe/rooster frames 21-23"`):
  - `overlaps(objs, frames, allowed: dict[frozenset, set[int]])`;
  - `resting(pairs: list[tuple[obj, support]], frames, tol=0.01)`;
  - `in_frame(subject, cam, frames)`;
  - `first_frame(subject, threat, cam, min_height=0.15)`;
  - `edge_leads(tool, edge_axis, target, frame)`;
  - `blade_face(tool, edge_axis, cam, frame, min_deg=35)`;
  - `cut_result(pieces, target_volume, expect)`.

  These use BVH trees built from evaluated meshes, plus `world_to_camera_view`, as in the probe.

- [ ] **Step 1: Write the failing tests.** For each check, one passing case and one failing case built from cubes,
  planes and a flat "blade" box:
  - two cubes intersecting on frames 5-6 fail `overlaps`, and pass when frames 5-6 are allowed;
  - a cube 3 cm above a plane fails `resting`;
  - a cube animated out of frame fails `in_frame` on exactly those frames;
  - a cube under 15% of the frame height fails `first_frame`;
  - a blade moving +x with its edge toward -x fails `edge_leads`;
  - a blade seen edge-on fails `blade_face`;
  - pieces with shares 0.5 against expect 0.15 fail `cut_result`; 0.15 passes; 81 pieces fail; a 2 mm piece
    fails.

  The cases script writes `{case: failures}` JSON, and the test asserts on it.
- [ ] **Step 2: Run.** `tests\test_opener_checks.py` should FAIL.
- [ ] **Step 3: Implement** each check.
- [ ] **Step 4: Run.** It should PASS.
- [ ] **Step 5: Commit** `feat: per-frame opener checks`.

### Task 5: Scene, look and moves (`blender/opener_scene.py`, `blender/moves.py`)

**Files:**
- Create: `blender/opener_scene.py` (entry point:
  `blender.exe -b --factory-startup --python blender/opener_scene.py -- <opener_job.json>`), `blender/moves.py`
- Create: `tests/fixtures/openers/` holding the model `.blend` and `.json` pairs used by the reference plans:
  rooster, stump, axe, barn, onion, knife, cutting board. Fetch them with Task 3 while Blender is open; these are
  committed, since they're small with their credits in the `.json`. Also
  `chicken_chop.json`, `onion_slices.json`, `onion_mince.json`, `box_fall.json` (primitive-only, no models).
- Test: `tests/test_opener_scene.py` (real headless Blender, a few minutes)

**Interfaces:**
- Consumes: `opener_checks.*`, the plan from `opener_plan.clean_opener`.
- Job JSON: `{"plan", "library": [dirs], "seconds": float, "fps": 30, "frames_dir": str, "report": str, "size": [w, h]}`.
- Produces: PNG frames `f_0001.png...`, plus a report JSON
  `{"ok": bool, "failures": [str], "subject_box": [...], "pieces": int}`.
- Exit code 0 even when checks fail (failures go in the report); non-zero only on a crash.

- [ ] **Step 1: Write the failing tests:**
  - `test_box_fall_rests`: `box_fall.json` (a cube falls by physics onto the ground) gives a report `ok`, and the
    last frame's cube touches the ground within 1 cm.
  - `test_chicken_chop_reference`: report `ok`. The head piece's share is within ±50% of 0.15. There's no overlap
    outside the cut frames, and frame 0 shows the rooster and the axe.
  - `test_onion_slices`: `ok`, with the planned slice count of pieces.
  - `test_onion_mince`: `ok`, with 40-60 pieces, each at least 3 mm.
  - `test_bad_plans_fail`: four broken variants of `chicken_chop.json` each give the matching failure:
    - the tool path moved into the breast: "overlap";
    - expect head 0.5: "cut";
    - the camera turned edge-on: "blade";
    - the walk long enough to leave the frame: "in_frame".
- [ ] **Step 2: Run.** `tests\test_opener_scene.py` should FAIL.
- [ ] **Step 3: Implement `opener_scene.py`.**
  - Load each actor's `.blend` from the library dirs.
  - Scale to `size_m`, place by `on`/`facing`, and build the set (ground colour from a table, backdrop models).
  - Apply the brand look from Global Constraints.
  - Run the beats via `moves.apply(beat, scene_state)`.
  - Bake rigid-body physics.
  - Run the checks.
  - Render to `frames_dir`, unless the checks failed and the job's `"render_failed"` is false (saves time on fix
    rounds).
- [ ] **Step 4: Implement `moves.py`.**
  - One function per move: `cut`, `fall`, `topple`, `hop_off`, `walk`, `fly_off`, `scatter`, `sink`, `roll`,
    `push`.
  - Passive ones add rigid bodies (convex hull; mesh shape for supports) with the plan's push or spin.
  - Driven ones are keyframed from the `GAITS` and `TOOLS` tables, read from `blender/opener_tables.json`.
  - A beat's `ends` (e.g. `{"on": "board"}`) and every cut piece with `then` other than `fly_off` and `scatter`
    become `opener_checks.resting` pairs on the last frame.
  - **`cut`** follows the spec:
    - the strokes come from the tool's motion;
    - bisect with fill for straight blades, a boolean with the tool's shape for shaped tools;
    - the cut faces are coloured from `CUT_FACE`;
    - each stroke stops at the first object that isn't the piece being cut (BVH test along the stroke, as in the
      probe);
    - the untouched model is shown until the first stroke, then the pieces are swapped in;
    - the pieces get the `then` outcomes;
    - a blade too short for the target's thickness along the stroke is a failure "blade too short".
- [ ] **Step 5: Run.** It should PASS. Then render `chicken_chop.json` to an mp4 in `test_renders/` and look at
  it next to the owner-approved `mike_opener_test8.mp4` behaviour: wind-up behind, head off, body hops off,
  camera follows.
- [ ] **Step 6: Commit** `feat: opener scenes, moves and reference plans`.

### Task 6: Running it from a Short (`shortsmaker/opener_render.py`)

**Files:**
- Create: `shortsmaker/opener_render.py`
- Modify: `shortsmaker/blender_render.py` (`_run(exe, job_path, script=SCRIPT, timeout=TIMEOUT)`, so both
  callers share it)
- Test: `tests/test_opener_render.py` (a fake Blender `.cmd`, as in `tests/test_blender_render.py`)

**Interfaces:**
- Consumes:
  - `blender_render._run`;
  - `blender_link.in_library`, `search`, `fetch_model`, `ping`, `credit`;
  - `opener_plan.fix_plan`;
  - `llm.ask_ai(..., read_dir=...)`.
- Produces:
  - `render_opener(short: dict, seconds: float, work: Path, exe: Path | None = None) -> tuple[Path | None, str | None]`,
    returning `(work/opener.mp4, None)` or `(None, "opener failed: <reason>")`;
  - `pick_model(find: str, hits: list[dict]) -> dict | None`: one `llm.ask_ai` call shows at most 10 hit titles
    and answers `{"pick": n}` or `{"pick": null}` ("none fits");
  - `short["opener_credits"]: list[str]`.

- [ ] **Step 1: Write the failing tests:**
  - `test_success_returns_clip`: the fake writes frames plus an ok report, so the result is `opener.mp4` with
    90 frames at 3.0 s.
  - `test_beats_scaled_into_scene`: a plan with its last beat at 2.5 s and `seconds=1.8` gives a job whose beat
    times are all at most 1.8 minus 1 frame, in the same order.
  - `test_failed_checks_fix_then_fallback`:
    - the fake always reports `failures: ["overlap: a/b frames 3-4"]`;
    - `fix_plan` is faked to return the same plan;
    - so the fake Blender runs 3 times (first try plus 2 fix rounds) and the result is
      `(None, "opener failed: overlap: a/b frames 3-4")`.
  - `test_crash_retry_then_fallback`: the fake exits 1 twice, so the result is None with "Blender" in the reason.
  - `test_reuse_unchanged`: the second call with the same plan and the same code version doesn't run Blender
    (the run log has 1 line).
  - `test_missing_model_blender_off`: the model isn't in the library and `ping` is False, so the result is
    `(None, "opener failed: model 'rooster' not in the library and Blender is off")`.
  - `test_review_rejects`: `llm.ask_ai` (the review) returns `{"ok": false, "problems": ["the axe hits the breast"]}`,
    so a fix round is started with that problem.
  - `test_cc_by_credit`: a CC-BY library model puts its attribution in `short["opener_credits"]`.
  - `test_pick_model`: a fake `ask_ai` answers `{"pick": 2}`, so the second hit is returned; `{"pick": null}`
    makes `render_opener` fall back with "no fitting model for '<find>'".
- [ ] **Step 2: Run.** `tests\test_opener_render.py` should FAIL.
- [ ] **Step 3: Implement.**
  - Scale every `at` by `min(1, (seconds - 1/30) / max_at)`.
  - The job fingerprint is the job JSON plus `blender_render.code_version()` (which covers `blender/*.py`).
  - The review uses an 8-frame strip (`fps`, `tile=8x1`) in `work/opener_look/`, with this prompt:
    "Does the action make physical sense, and does frame 0 show the subject and the threat? Reply
    {ok, problems}".
  - A Blender timeout of 600 s.
- [ ] **Step 4: Run.** It should PASS, along with `tests\test_blender_render.py` (the shared `_run`).
- [ ] **Step 5: Commit** `feat: render, review and fix openers`.

### Task 7: Wiring into the run

**Files:**
- Modify:
  - `shortsmaker/writing.py:233` (after `plan_builds`: `if kept and session.RULE_SETTINGS.get("opener") == "blender": opener_plan.plan_openers(kept, ch)`);
  - `shortsmaker/short_render.py:260-266` (after `clips = gpu.local_clips(...)`);
  - `shortsmaker/short_render.py:383-386` (no swap when an opener clip is used);
  - `shortsmaker/short_render.py:396-412` (credits);
  - `shortsmaker/cli.py` (start note);
  - `HANDOFF.md`.
- Test: `tests/test_opener_render.py` (wiring tests) and `tests/test_package.py`

**Interfaces:**
- Consumes: `opener_render.render_opener`, `blender_link.ping`.
- Produces:
  - `short_render.render` sets `clips[0] = work/"opener.mp4"`, `images[0]` to its first frame,
    `short["scenes"][0]["full"] = None`, and `sources[0] = "drawn in Blender (opener): <moment>"`;
  - on failure, adds the reason (and any `short["opener_check"]`) to `issues`;
  - `cli.blender_note(interactive: bool) -> None`.

- [ ] **Step 1: Write the failing tests:**
  - `test_render_uses_opener_clip`: with `render_opener` faked to return a clip, scene 0's clip and source are
    the opener, `first_second_check`'s swap is ignored, and upload.txt has the opener credits but no
    "ALTERED OR SYNTHETIC" line.
  - `test_render_falls_back_with_check`: faked to fail, so scene 0 is untouched and the issues include the
    reason.
  - `test_blender_note`:
    - with `ping` False and interactive, the inputs `["", "s"]` give 2 pings, and the printed note matches the
      spec's wording;
    - non-interactive prints once without asking.
- [ ] **Step 2: Run.** It should FAIL.
- [ ] **Step 3: Implement.**
  - Call `cli.blender_note(len(sys.argv) < 2)` after the channel's rules load, only when its settings have
    `opener: blender`.
  - **HANDOFF.md** gets a "Blender openers (2026-10-27)" section: the flow, files, tests, the library on D:, and
    the note that the MCP server has to be started for new models. Add the new test files to "How to verify
    changes".
- [ ] **Step 4: Run every suite.** All should PASS:
  - `tests\test_package.py`
  - `test_story.py`
  - `test_opener_plan.py`
  - `test_blender_link.py`
  - `test_opener_render.py`
  - `test_blender_render.py`
  - `test_first_second.py`
  - `test_opener_checks.py`
  - `test_opener_scene.py`
- [ ] **Step 5: Live run with Blender open.** Run one real strange-history Short with run.bat.
  - edit_plan.txt shows either an opener source line or a CHECK line with a reason.
  - `short.mp4` starts with the opener when it passed.
  - Show the owner the first 3 seconds.
- [ ] **Step 6: Commit** `feat: Blender openers in the run`. Then refresh the code map and commit
  `docs: refresh code map`.
