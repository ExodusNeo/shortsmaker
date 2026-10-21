# Split make_shorts.py into a package (design)

Date: 2026-10-21. Owner approved option 1 and the verification plan in chat.

## Goal

`make_shorts.py` is 5,294 lines doing ~20 jobs. Split it into a `shortsmaker/` package of focused modules with clean
imports, **behavior unchanged**, then rebuild the Obsidian code map (`code-map/`).

Out of scope: renaming functions, changing logic or prompts, new dependencies (linters, type checkers), new features.

## Constraints

- `run.bat`, `fix.bat`, `library.bat` keep calling `.venv\Scripts\python.exe make_shorts.py [fix|library]`; the
  `notes` command keeps working.
- Tests replace functions and settings with fakes so they spend no AI usage (`m.ask_ai = ...`, `m.POOLS = ...`, ~25
  names). After the split a fake must reach every caller.
- Run settings change during a run (`global` today): `BRAIN`, `NO_QUOTA`, `LAST_AI`, `CHANNEL`, `RESEARCH`, `LOG`,
  `SHORT_FORM`, `VEO_HANDOFF`, `YELLOW`, `EMPHASIS`, and private caches `_gemini_model`, `_argon_exhausted`,
  `_last_wm`, `_last_ov`. Each must have exactly one owner.
- The project was not in git; it becomes a local git repo first (owner's choice), nothing pushed anywhere.

## Layout

`make_shorts.py` stays as a ~5-line entry point that calls `shortsmaker.cli.main()`.

| Module | Job |
|---|---|
| `config.py` | paths, fixed constants, palettes, style/skin tables, prompt constants |
| `session.py` | run settings that change mid-run (the `global` names above) |
| `ai.py` | Claude/Gemini calls (`ask_ai`, `run_agy`, quota detection, Gemini model pick) |
| `channels.py` | channel profiles, menus (`ask_*`), YouTube research, trend research |
| `writing.py` | topic -> research -> writer -> editor -> director -> fact check |
| `plan.py` | cleaning/validating planner JSON, word timings, full-scene cues |
| `seo.py` | SEO pass, autocomplete, srt |
| `sources.py` | Wikimedia/Openverse/NASA/Archive pictures, licenses, credits |
| `footage.py` | film clips (Commons, Archive, Pixabay) and their ffmpeg crops |
| `pool.py` | picture pool, catalog, cache pruning, contact sheets |
| `picker.py` | choosing pictures, full-scene pictures, rescue graphics |
| `photo.py` | stereo cards, border trimming, vertical crop |
| `audio.py` | voice (`speak`), captions, SFX, story sounds, music gain |
| `frames.py` | Python renderer: shots, overlays, person cards, `ClipReader`, thumbnail |
| `review.py` | quality check, visual review, review fixes, storyboard |
| `motion.py` | full-screen scene props, AI-coded Custom scenes, `custom_rules` |
| `styles.py` | style-library inventions, candidates, library menu |
| `remotion.py` | Remotion render with fallback, redraw, paper/ink figures |
| `editplan.py` | `edit_plan.txt`, scene cues |
| `gpu.py` | local AI: ComfyUI/MOSS, VoiceStudio, Gemini images, LTX clips, Veo hand-off |
| `render.py` | work-state save/load, `render()` |
| `logbook.py` | logbook entries, vault pages |
| `cli.py` | `main()`, `fix_short()` and its helpers, command dispatch |

Exact function-to-module assignment follows the old file's order and section boundaries; the implementation plan
lists it.

## Import rules

- Fixed constants: `from shortsmaker.config import NAME` (they never change at run time).
- Functions from another module and anything in `session`: called through the module (`ai.ask_ai(...)`,
  `session.BRAIN`), imported as `from shortsmaker import ai, session`. This is what lets one fake reach all callers
  and keeps a single copy of each run setting.
- Constants tests overwrite (`POOLS`, `CACHE`, `CANDIDATES`) are read through their module too.
- `global X` statements for session names become `session.X = ...`.

## How the move is done

A one-off script (kept in `tools/split_make_shorts.py`) parses the old file with `ast`, assigns each top-level
statement to a module, rewrites cross-module references to `module.name`, writes the modules with their imports,
and runs the checks below. Function bodies are not edited by hand.

## Verification

1. Baseline: commit the current tree; run all suites and record counts (test_full_scenes 43, test_pictures_first 36,
   test_style 29, run_ts_tests 19, test_qwen_voice 3).
2. Automatic proofs from the split script:
   - every top-level name of the old file is defined in exactly one module;
   - no undefined names in any module (every load resolves to a local, import, builtin or module attribute);
   - each function/class is AST-identical to the original after removing the added `module.` qualifiers and
     `session.` rewrites.
3. Tests updated to patch the owning module; all suites pass with the baseline counts.
4. Smoke runs with no AI usage: `tests/render_full.py` on one test-props scene; `make_shorts.py notes`; `run.bat`
   started to the channel question and quit; `python -c "import make_shorts"`.
5. Commit after each stage (baseline, split, tests, docs).

## Docs

- HANDOFF.md: layout table and "How to verify changes" point at the package; function references stay valid by name.
- `.graphifyignore` comment updated (the new `shortsmaker/` folder is already in scope).
- Rebuild the code map: graphify into `code-map/`; `vault/Home.md` link unchanged.
- Memory: ShortsMaker entry notes the package layout.

## Risks

- Hidden import-time side effects in the old file (top-level code beyond constants): the script lists every
  non-def/non-constant top-level statement for a manual decision.
- Circular imports: avoided by module-qualified access at call time; no module uses another at import time except
  `config`.
- Another agent (Gemini/agy) editing the old single file afterwards: HANDOFF says where code lives now.
