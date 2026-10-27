# People Openers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Blender openers can show people (Quaternius rigged, animated characters dressed by era and role), and every opener gets one cel-shaded, ink-outlined look.

**Architecture:** People are a new kind of actor in the existing opener plan. `blender/people.py` dresses and animates them from a packed library (`people.blend` + `people.json`); `opener_scene.py`, `moves.py` and `opener_checks.py` treat them like any actor. The Python side (`opener_plan`, `opener_render`) learns person actors and passes the library to the Blender job. Tests use a stand-in library built at test time, so no Quaternius file is ever in git.

**Tech Stack:** Blender 5.2 headless (`D:\Blender\blender.exe`, plain bpy, EEVEE), Python 3 package `shortsmaker`, plain-assert test scripts run with `.venv\Scripts\python.exe`.

**Spec:** `docs/superpowers/specs/2026-10-27-people-openers-design.md` (Part 1: `2026-10-27-blender-openers-design.md`, HANDOFF "Blender openers").

## Global Constraints

- Quaternius files live only in `D:\ShortsMaker\blender\assets\people\` and never in git (licence forbids redistribution); add `blender/assets/people/` to `.gitignore` in Task 1.
- The AI never writes Blender code; it picks only values from `blender/opener_tables.json`. A new role or move is a new table row.
- A failed opener never stops a run and never ships: scene 1 falls back with `CHECK: opener failed: <reason>`.
- Facings and directions are as seen in the shot (`scene_kit.VIEW_YAW` / `view()`); the staging check applies to people.
- Every cut, release and move keeps Part 1's checks green: `tests\test_opener_scene.py`, `test_opener_checks.py`, `test_opener_render.py`, `test_opener_plan.py`.
- Look at every visual change by eye (render a strip), not only the checks.
- After each code commit: refresh and commit the code map (`C:\Python314\python.exe -m graphify update .`, clear `code-map\*.md` + `graph.canvas`, `-m graphify export obsidian --dir code-map`, commit "docs: refresh code map").
- Commits end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. A role colour names a clothing slot the body's materials don't have: the colour is skipped, the person still builds (Task 3 test `test_missing_slot_is_skipped`).
2. A person standing on a support who then walks: they must not float off the edge; it comes back as a failure, never a crash (Task 4 test `test_walk_off_support_is_reported`).
3. An in-place clip shorter than the time left (a 1 s fall in a 3 s opener): the person holds the clip's last pose, resting on the ground (Task 4 test `test_fall_holds_last_pose`).
4. A plan has people but the people library is missing on D:: `render_opener` returns `opener failed: people library missing` and the run goes on (Task 7 test `test_people_library_missing`).
5. A prop or hat `find` with no model in the library and Blender off: the opener fails with the reason (same path as any model), no crash (Task 7 test `test_missing_prop_model`).

---

### Task 1: People library (download + pack)

**Files:**
- Create: `blender/pack_people.py`
- Modify: `.gitignore` (add `blender/assets/people/`), `shortsmaker/config.py` (add `PEOPLE_DIR = ROOT / "blender" / "assets" / "people"`, `PEOPLE_BLEND = PEOPLE_DIR / "people.blend"`, `PEOPLE_JSON = PEOPLE_DIR / "people.json"`)

**Interfaces:**
- Produces: `people.blend` (every body as one mesh object parented to its armature, named `body:<name>`; every clip as an action named exactly as in Quaternius, fake user on) and `people.json`:
  `{"bodies": {"<name>": {"object": "body:<name>", "armature": "<armature object>", "slots": {"<material name>": "<clothing slot>"}}}, "bones": {"head": "<bone>", "hand_r": "<bone>"}, "clips": {"<action>": {"frames": int, "loop": bool, "stride_m": float | null}}, "height_m": float}`.
  Clothing slots are `skin`, `hair`, `top`, `bottom`, `shoes`, `extra`. `stride_m` = root distance per loop for locomotion clips (null otherwise).

- [ ] **Step 1:** Download the Quaternius Ultimate Animated Character Pack and Universal Animation Library 1 + 2 (free versions) into `D:\ShortsMaker\blender\assets\people\src\`. If a download needs a browser click-through, stop and ask the owner to download them there (give the quaternius.com pack links); continue when the folder has the files.
- [ ] **Step 2:** Write `blender/pack_people.py` (entry: `blender.exe -b --factory-startup --python blender/pack_people.py -- <src dir> <out dir>`): import every body and the animation library, retarget nothing (UAL shares the characters' skeleton; if a body's skeleton differs, skip that body and print it), map material names to clothing slots by keyword (`skin`, `hair`, `shirt|top|jacket|coat` -> top, `pants|trousers|skirt` -> bottom, `shoe|boot` -> shoes, else extra), measure stride from the root/hips travel over one loop for clips whose name contains Walk/Run/Jog/Crawl/Stagger/Drunk, save both files.
- [ ] **Step 3:** Run it; expected: `people.json` lists >= 20 bodies, >= 60 clips, `bones.head` and `bones.hand_r` set.
- [ ] **Step 4:** Commit `blender/pack_people.py`, `.gitignore`, `shortsmaker/config.py` (no files from `assets/people`).

### Task 2: Tables and the stand-in library for tests

**Files:**
- Modify: `blender/opener_tables.json`
- Create: `tests/people_standin.py` (runs inside Blender), `tests/test_people_tables.py`

**Interfaces:**
- Consumes: `people.json` schema (Task 1) — real clip and body names are copied into the tables from the real `people.json` when present.
- Produces in the tables:
  - `"roles": {"<role>": {"body": "<body>", "colours": {"<slot>": [r, g, b]}, "hat": "<find>" | null, "height_m": float}}` with the 19 roles of the spec (`ww2_british_officer`, `ww1_soldier`, `victorian_gentleman`, `victorian_lady`, `sailor`, `pirate`, `farmer`, `scientist`, `medieval_knight`, `roman_soldier`, `cowboy`, `businessman`, `worker`, `king`, `queen`, `monk`, `man`, `woman`, `child`; child 1.2 m, others 1.6-1.8 m).
  - `"people_moves": {"<move>": {"clip": "<action>", "kind": "travel" | "in_place"}}` for walk, run, stagger, crawl (travel) and fall, die, flinch, point, wave, sit, kneel, raise_prop, swing_prop, throw_prop, drop_prop (in place).
- Produces `tests/people_standin.py -- <out dir>`: builds a stand-in library with the same schema: for every body named in `roles` a capsule body (skin/top/bottom/shoes materials) on an armature with bones `root`, `spine`, `head`, `hand_r`, `leg_l`, `leg_r`; for every clip named in `people_moves` an action of that name (travel clips: leg swing + `stride_m` 0.6; fall/die: rotate the spine 90 deg over 20 frames; swing_prop: hand_r arc over 10 frames; others: a small pose over 15 frames).

- [ ] **Step 1: Write `tests/test_people_tables.py`:** `test_every_role_is_complete` (body, colours, height in 1.0-2.1, slots only from the six), `test_every_move_has_a_clip_and_kind`, `test_standin_matches_tables` (run `people_standin.py` headless into a temp dir; its json has every role's body and every move's clip). Run; expect FAIL (no tables).
- [ ] **Step 2:** Add the tables; write `tests/people_standin.py`.
- [ ] **Step 3:** Run `.venv\Scripts\python.exe tests\test_people_tables.py`; expect 3/3.
- [ ] **Step 4:** Commit.

### Task 3: Dressing and placing a person

**Files:**
- Create: `blender/people.py`
- Modify: `blender/opener_scene.py` (`place_actors`: a person actor is built by `people.dress`, `fit` skipped; size from the role), `blender/opener_checks.py` (overlap allows a person with their own hat and prop), `tests/test_opener_scene.py` (job gains `"people": {"blend", "json"}`; `run()` builds the stand-in once per test run)
- Create fixtures: `tests/fixtures/openers/person_stand.json`, `person_on_support.json`

**Interfaces:**
- Consumes: job key `"people": {"blend": str, "json": str}`; job `models["<id>:hat"]`, `models["<id>:prop"]` (.blend paths or absent).
- Produces: `people.dress(actor: dict, lib: dict, models: dict) -> bpy.types.Object` (returns the body mesh; its armature is `obj.parent`; sets `obj["facing"]`, `obj["person"] = role`, `obj["hat"]`/`obj["prop"]` = object names); `people.load_library(job: dict) -> dict` (the parsed json plus the blend path).

- [ ] **Step 1: Write tests:** `test_person_stands` (person_stand: report ok, `lowest[officer]` within 0.01 of 0), `test_person_on_support` (on a crate: ok, lowest = the crate's top), `test_missing_slot_is_skipped` (role colours name `extra` the stand-in body lacks: still ok). Run; expect FAIL.
- [ ] **Step 2:** Implement `people.dress`: append the body and its armature from the blend, apply the role's colours to the materials mapped to each slot (copies, so two people don't share), parent the hat to `bones.head` and the prop to `bones.hand_r` (Child Of, set inverse at rest), scale the armature so the body is `height_m` tall, turn to the facing with `kit.view`, origin at the feet. Wire into `place_actors`; `stand_on` places it.
- [ ] **Step 3:** Run the three tests; expect PASS. Run the whole `test_opener_scene.py`; expect all green.
- [ ] **Step 4:** Commit.

### Task 4: People moves

**Files:**
- Modify: `blender/people.py`, `blender/moves.py` (`apply`: a beat whose actor is a person and whose move is in `people_moves` goes to `people.move(beat, st)`), `tests/test_opener_scene.py`
- Create fixtures: `person_walk.json`, `person_fall.json`, `person_walk_off_support.json`

**Interfaces:**
- Produces: `people.move(beat: dict, st: moves.State) -> None` (keys NLA strips on the person's armature, keys object location/rotation for travel, records `st.moved_from`).

- [ ] **Step 1: Write tests:** `test_person_walks_across` (walk "left": ok; final x moved >= 0.5 m along the view's left; feet speed matches stride within 15%), `test_fall_holds_last_pose` (fall at 0.5 s in a 3 s opener: ok, resting at the end), `test_walk_off_support_is_reported` (on a crate, walk: not ok, a failure starting with `walk:` or `resting`, no crash), `test_person_walk_away_is_staging` (walk "away": a `staging:` failure). Run; expect FAIL.
- [ ] **Step 2:** Implement: in-place = one NLA strip from the beat's frame for the clip's length, then hold (strip `extrapolation = "HOLD"`); travel = the loop clip repeated to the opener's end, the object moved along `moves.toward(beat)` at `stride_m * fps / frames` per second, turned over 8 frames, stopping short of obstacles with `moves.clear_distance` (as `moves.walk`); strips blend 4 frames (`blend_in`/`blend_out`). A person on a support with a travel move: build as asked; the resting/overlap checks report it.
- [ ] **Step 3:** Run; expect PASS; full `test_opener_scene.py` green.
- [ ] **Step 4:** Render `person_walk` and `person_fall` at 25% and look at a strip (`ffmpeg ... tile`); fix what looks wrong.
- [ ] **Step 5:** Commit.

### Task 5: Prop actions and the prop in frame 0

**Files:**
- Modify: `blender/people.py`, `blender/opener_scene.py` (`checks`: first frame must show the person's prop when the plan names one), `blender/opener_checks.py` (`first_frame` takes an optional prop)
- Create fixtures: `person_swing.json` (sword), `person_drop.json` (umbrella)

**Interfaces:**
- Produces: swing_prop registers the prop as a tool contact (`st.contacts.append((prop, edge_axis, target_or_prop, frame))`) only when its find is a blade in `tables.tools`; throw_prop / drop_prop call `moves.release(st, prop, frame, launch=...)` after clearing its Child Of (keyframed influence 1 -> 0 at the release frame, world transform kept).

- [ ] **Step 1: Write tests:** `test_swing_shows_blade` (ok; no `blade:` failure), `test_drop_lands` (prop resting on the ground at the end), `test_prop_hidden_in_first_frame_fails` (prop moved off-frame at frame 1: a `first_frame:` failure naming the prop). Run; expect FAIL.
- [ ] **Step 2:** Implement.
- [ ] **Step 3:** Run; expect PASS; all opener suites green.
- [ ] **Step 4:** Commit.

### Task 6: One cel-shaded, outlined look for every opener

**Files:**
- Create: `blender/look_toon.py`
- Modify: `blender/opener_scene.py` (after `dress_set`, before the render: `look_toon.apply(scene_objects)`), `tests/test_opener_scene.py`

**Interfaces:**
- Produces: `look_toon.apply(objs: list) -> int` (returns the number of meshes outlined). Each material's colour (base colour value or its image texture) goes through Diffuse -> Shader to RGB -> Color Ramp (CONSTANT, 3 stops: 0.0 shade = colour x 0.55, 0.45 mid = colour, 0.85 light = colour x 1.15) -> Emission; one outline per mesh: Solidify (`thickness = -0.012 * object size`, `use_flip_normals`, material offset to an `ink` material: black, backface culling on, `show_backface` off). Instanced and already-outlined objects are skipped.

- [ ] **Step 1: Write test** `test_toon_look_everywhere` (box_fall rendered at 25%: every visible mesh has an `ink` slot and a Solidify named `ink`; render not blank). Run; expect FAIL.
- [ ] **Step 2:** Implement and wire in.
- [ ] **Step 3:** Run; all opener suites green.
- [ ] **Step 4:** Re-render Mike (`cache/opener_cam/job_left.json`) and look at it by eye; tune the band stops and outline width until the rooster, stump and barn read as clean 2D cartoon (no outline gaps, no black blobs on thin parts like the axe handle).
- [ ] **Step 5:** Commit.

### Task 7: Planner and job wiring (Python side)

**Files:**
- Modify: `shortsmaker/opener_plan.py` (`clean_opener`, `_tables_text`, the planner prompt example), `shortsmaker/opener_render.py` (`resolve_models`, `render_opener` job), `tests/test_opener_plan.py`, `tests/test_opener_render.py`

**Interfaces:**
- Consumes: tables `roles`, `people_moves` (Task 2); `config.PEOPLE_BLEND`, `config.PEOPLE_JSON` (Task 1).
- Produces: `clean_opener` accepts an actor with `"person"` in `roles` (no `find`/`size_m` needed; optional `prop` find text), people moves only for person actors, Part 1 moves for the rest; `resolve_models` adds `"<id>:hat"` (from the role) and `"<id>:prop"` and returns `({}, "people library missing")` when a plan has people and `config.PEOPLE_JSON` doesn't exist; the job carries `"people": {"blend": str(config.PEOPLE_BLEND), "json": str(config.PEOPLE_JSON)}`.

- [ ] **Step 1: Write tests:** in `test_opener_plan.py`: `test_person_actor_is_clean` (the spec's umbrella-officer plan passes), `test_unknown_role_rejected`, `test_people_move_on_animal_rejected`; in `test_opener_render.py` (fake Blender): `test_people_library_missing`, `test_missing_prop_model`, `test_person_job_has_library`. Run; expect FAIL.
- [ ] **Step 2:** Implement; the prompt lists roles and people moves and adds the umbrella example: officer (`ww2_british_officer`, prop `umbrella`, facing right) walking left across a street at 0.3 s while explosions go off behind (Part 1's `scatter` on debris).
- [ ] **Step 3:** Run all four opener suites; expect green.
- [ ] **Step 4:** Commit.

### Task 8: Rules, contact sheet, end-to-end, docs

**Files:**
- Modify: `channels/strange-history.rules.md`, `channels/weird-economics.rules.md` (`## Opener`), `HANDOFF.md` ("Blender openers": a "People (part 2)" subsection; "How to verify changes" lists the new tests)
- Create: `tests/people_sheet.py`

**Interfaces:**
- Produces: `tests/people_sheet.py` (skips with a note when `config.PEOPLE_JSON` is missing): renders every role standing (facing right) and every people move once, tiles them into `cache/people_sheet/roles.png` and `moves.png`.

- [ ] **Step 1:** Rules: replace "It can't show people: ..." with: people are shown as cartoon figures by era and role (pick from the roles list; closest role or man/woman/child when none fits); no faces; at most 3 people; a person's prop is in frame 0; side view, crossing the frame. `buildable false` only for crowds or what even people can't show.
- [ ] **Step 2:** Run `tests/people_sheet.py`; look at both sheets; fix any role or move that looks wrong (colours on the wrong part, hats floating, clips that slide).
- [ ] **Step 3:** End to end: from `output/strange-history/2026-10-26_why-a-ww2-officer-carried-an-umbrella`, run the planner for scene 1 (`opener_plan.plan_openers` on that Short only) and `opener_render.render_opener`; look at `work/opener.mp4`; it must pass checks and review.
- [ ] **Step 4:** HANDOFF; full opener suites green; commit; refresh and commit the code map.
