# Split make_shorts.py Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the 5,294-line `make_shorts.py` into a `shortsmaker/` package of focused modules with identical behavior, then rebuild the Obsidian code map.

**Architecture:** A one-off `ast`-based script moves every top-level statement, unchanged, to its module by line range, rewrites cross-module references to `module.name` (fixed constants from `config` stay bare via `from shortsmaker.config import ...`), and proves the result (no lost/duplicate names, no undefined names, each function AST-identical to the original modulo the rewrites). The same script rewrites the tests' `m.name` to `owner.name`.

**Tech Stack:** Python 3.12 (`.venv`), stdlib `ast`; existing test runners (plain-script tests, `run_ts_tests.py`); graphify for the code map.

**Spec:** `docs/superpowers/specs/2026-10-21-split-make-shorts-design.md`

## Global Constraints

- Behavior unchanged; no renamed functions, no logic or prompt edits, no new dependencies.
- `run.bat`, `fix.bat`, `library.bat` unchanged: `.venv\Scripts\python.exe make_shorts.py [fix|library|notes]`.
- Local git only; nothing pushed.
- Baseline test counts: test_full_scenes 43, test_pictures_first 36, test_style 29, run_ts_tests 6 guarded + 13 style, test_qwen_voice 3.
- Module names must not equal any identifier used in the old file (checked by the script). Spec names are refined to clash-free names: `llm` (spec `ai`), `channel_profiles` (`channels`), `planning` (`plan`), `image_sources` (`sources`), `picture_pool` (`pool`), `photo_prep` (`photo`), `audio_mix` (`audio`), `frame_render` (`frames`), `remotion_render` (`remotion`), `short_render` (`render`), plus `media_tools` for shared ffmpeg/file helpers.
- Private caches used by one module (`_gemini_model`, `_argon_exhausted`, `_last_wm`, `_last_ov`) stay in that module; `session` owns `BRAIN`, `NO_QUOTA`, `LAST_AI`, `CHANNEL`, `RESEARCH`, `LOG`, `SHORT_FORM`, `VEO_HANDOFF`, `YELLOW`, `EMPHASIS`.

## Review Focus

- Import-time side effects (ffmpeg added to PATH, PIL warning filter, palette contrast assert, `GRAPHIC_STYLES.update`) must still run when started via `make_shorts.py` → they live in `config`, imported by every module. Pinned by `test_package.py::test_ffmpeg_on_path`.
- `ROOT` must still be `D:\ShortsMaker` after moving into `shortsmaker/` (channels, remotion, vault paths). Pinned by `test_package.py::test_root`.
- A quota switch (`session.BRAIN = "gemini"`) made in `llm` must be seen by every module. Pinned by `test_package.py::test_session_shared`.
- A fake installed on the owning module must reach callers in other modules (tests rely on it to spend no AI usage). Pinned by `test_package.py::test_fake_reaches_callers`.
- `fix` / `library` / `notes` commands still dispatch. Pinned by Task 5 smoke runs.

---

### Task 1: Git baseline

**Files:**
- Create: `D:\ShortsMaker\.gitignore`

- [ ] **Step 1: Write `.gitignore`** with: `.venv/`, `__pycache__/`, `.npm-cache/`, `output/`, `cache/`, `backup/`, `agy_tasks/`, `test_renders/`, `ltx_compare/`, `voice_speed_test/`, `ffmpeg/`, `music/`, `local_ai/hf/`, `local_ai/models/`, `local_ai/python/`, `local_ai/qwen_venv/`, `local_ai/voices/`, `remotion/node_modules/`, `remotion/public/job/`, `graphify-out/cache/`, `*.mp4`, `*.mp3`, `*.wav`, `freesound_key.txt`, `pixabay_key.txt`, `.superpowers/`.
- [ ] **Step 2: Check what would be committed:** `git init` then `git add -A --dry-run | wc -l` and `du` of the listed files. Expected: no keys, no media, total under ~50 MB; add any big offender to `.gitignore`.
- [ ] **Step 3: Record baseline:** run the five suites (commands in HANDOFF "How to verify changes"). Expected: the counts in Global Constraints.
- [ ] **Step 4: Commit** `git add -A && git commit -m "chore: baseline before splitting make_shorts.py"` (with the attribution line).

### Task 2: Split script with self-test and proofs

**Files:**
- Create: `tools/split_make_shorts.py`

**Interfaces:**
- Produces: `python tools/split_make_shorts.py split` (writes `shortsmaker/*.py` and the new `make_shorts.py`, runs proofs, exits non-zero on any failure); `python tools/split_make_shorts.py tests` (rewrites test files); `python tools/split_make_shorts.py selftest`.
- Reads the original from `git show HEAD:make_shorts.py` so reruns are idempotent.

Module assignment (by the start line of each top-level statement in the original; overrides win):

| Lines | Module |
|---|---|
| 35-150 | `config` (incl. PATH side effect, `GRAPHIC_STYLES.update`, palette helpers + assert, `short_skin`, `ass_colour`) |
| 151-291 | `llm` |
| 292-490 | `channel_profiles` (warnings filter at 393 → `config`) |
| 491-518 | `styles` |
| 519-759, 809-1142 | `writing` |
| 760-808 | `picture_pool` |
| 1143-1506 | `planning` |
| 1507-1577 | `seo` |
| 1578-1695, 1716-1782, 1834-1873, 1943-1975 | `image_sources` (`fetch` → `media_tools`; `POOLS`, `MIN_USABLE`, `TOPIC_BACKUPS` → `picture_pool`) |
| 1696-1715, 1783-1833, 1874-1942, 1976-2068 | `footage` |
| 2069-2284 | `picture_pool` (`write_json` → `media_tools`) |
| 2285-2454, 2488-2577 | `picker` |
| 2455-2462 | `remotion_render` |
| 2463-2487 | `styles` |
| 2578-2656 | `photo_prep` |
| 2657-2931 | `audio_mix` (`duration`, `video_encoder`, `ffmpeg` → `media_tools`; `fills_frame` → `frame_render`) |
| 2932-3215 | `frame_render` |
| 3216-3341 | `review` (`clock` → `media_tools`) |
| 3342-3432 | `audio_mix` |
| 3433-3732 | `motion` |
| 3733-3986 | `styles` |
| 3987-4174 | `remotion_render` |
| 4175-4343 | `editplan` |
| 4344-4701 | `gpu` |
| 4702-5016 | `short_render` (`MUSIC_LUFS`, `music_gain` → `audio_mix`) |
| 5017-5106 | `logbook` |
| 5107-5292 | `cli` (the `if __name__` block is dropped) |
| name overrides | `CHANNEL`, `RESEARCH`, `LOG`, `YELLOW`, `EMPHASIS`, `BRAIN`, `NO_QUOTA`, `LAST_AI`, `SHORT_FORM`, `VEO_HANDOFF` → `session` |

Rewrite rules: a load of a top-level name owned by another module becomes `owner.name`, except names owned by `config`, which are imported by name. `global X` for a session name is removed and `X = ...` becomes `session.X = ...`. `config.ROOT` becomes `Path(__file__).parent.parent` (the only intended code change). Each module gets only the stdlib/third-party imports it uses, `from shortsmaker.config import <used names>`, and `from shortsmaker import <used modules>`. Rewrites are applied to source text by AST node positions so comments and formatting survive.

- [ ] **Step 1: Write `selftest`**: a toy source with two top-level functions in different modules, a session global with `global` + assignment, a config constant, a local variable shadowing a top-level name. Assert: cross-module call rewritten, shadowed local left alone, `global` replaced by `session.` assignment, config constant imported bare.
- [ ] **Step 2: Run** `.venv\Scripts\python.exe tools\split_make_shorts.py selftest`. Expected: FAIL (not implemented).
- [ ] **Step 3: Implement** assignment, rewriting, module writing, and the proofs:
  - every original top-level name defined in exactly one module;
  - no module name equals an identifier in the original or in the tests (hard fail, lists clashes);
  - no undefined name in any module (walk loads; resolve to local scope, import, builtin, or `module.attr` that exists);
  - each function/class AST-dumps equal to the original after reversing `owner.name` → `name` and `session.X` → `X` (`global` lines and `ROOT` excepted);
  - import-time cross-module references (module-level statements and default arguments) only to `config`, else list them.
- [ ] **Step 4: Run selftest.** Expected: PASS.
- [ ] **Step 5: Commit** `tools/split_make_shorts.py`.

### Task 3: Split, package tests

**Files:**
- Create: `shortsmaker/__init__.py` (docstring only), `shortsmaker/<module>.py` ×24, `tests/test_package.py`
- Modify: `make_shorts.py` (becomes docstring + `from shortsmaker.cli import main` + `if __name__ == "__main__": main()`)

- [ ] **Step 1: Write `tests/test_package.py`** (plain-script style like the other tests, PASS/FAIL lines and a count):
  - `test_root`: `config.ROOT == Path(<repo>)` and `(config.ROOT / "remotion").exists()`.
  - `test_ffmpeg_on_path`: after `import shortsmaker.config`, `str(config.ROOT / "ffmpeg")` is in `os.environ["PATH"]`.
  - `test_session_shared`: set `session.BRAIN = "gemini"`; `llm.ask_ai`'s order uses gemini first (fake `llm.run_agy` returning `'{"ok": 1}'`, `shutil.which` patched truthy) → returns `{"ok": 1}` and `session.LAST_AI == "gemini"`; restore.
  - `test_fake_reaches_callers`: set `llm.ask_ai = lambda *a, **k: {"code": None}`; `motion.code_custom_scenes` on one custom scene in a temp work dir falls back to `fallback_custom_tsx` output (proves the motion module calls the fake); restore.
  - `test_entry_point`: `import make_shorts` exposes `main` that is `cli.main`.
- [ ] **Step 2: Run** `.venv\Scripts\python.exe tests\test_package.py`. Expected: FAIL (no package).
- [ ] **Step 3: Run** `.venv\Scripts\python.exe tools\split_make_shorts.py split`. Expected: all proofs print OK; resolve anything listed (import-time references, clashes) by adjusting the table, never by hand-editing generated modules.
- [ ] **Step 4: Run** `py_compile` on every new file and `tests\test_package.py`. Expected: 5/5 passed.
- [ ] **Step 5: Commit** "refactor: split make_shorts.py into shortsmaker package".

### Task 4: Point the existing tests at the owning modules

**Files:**
- Modify: `tests/test_full_scenes.py`, `tests/test_pictures_first.py`, `tests/test_style.py`, `tests/render_style.py`

- [ ] **Step 1: Run** `tools\split_make_shorts.py tests`: replaces `import make_shorts as m` with `from shortsmaker import <used modules>` and every `m.<name>` (only names from the original's top level) with `<owner>.<name>`; fails if a test file uses a module name as a variable.
- [ ] **Step 2: Run all suites.** Expected: exactly the baseline counts, plus test_package 5/5.
- [ ] **Step 3: Commit** "test: patch owning modules after the split".

### Task 5: Smoke runs (no AI usage)

- [ ] **Step 1:** `.venv\Scripts\python.exe tests\render_full.py remotion\test_props\custom-clock.json --still 1`. Expected: a still is written, no traceback.
- [ ] **Step 2:** `.venv\Scripts\python.exe make_shorts.py notes`. Expected: vault pages rebuilt; `git status vault` shows no unexpected content changes beyond timestamps (inspect any diff).
- [ ] **Step 3:** `echo q | .venv\Scripts\python.exe make_shorts.py` up to the channel question. Expected: the channel menu prints, exits cleanly on EOF.
- [ ] **Step 4:** Same for `make_shorts.py fix` and `make_shorts.py library`. Expected: their first menus print.

### Task 6: Docs, skills, memory

**Files:**
- Modify: `HANDOFF.md` (Layout table row for the package, "How to verify changes" adds `tests\test_package.py`, a short "Code layout" section listing modules and their jobs), `.claude/skills/motion-design/SKILL.md` and `.claude/skills/review-loop/SKILL.md` (`make_shorts.py` → `shortsmaker/motion.py`), `.graphifyignore` (comment: code is `make_shorts.py`, `shortsmaker/`, ...), memory `shortsmaker-project.md`.
- [ ] **Step 1:** Make the edits.
- [ ] **Step 2:** `grep -rn "make_shorts.py" HANDOFF.md .claude` and check each remaining mention still means the entry point.
- [ ] **Step 3: Commit** "docs: code layout after the split".

### Task 7: Rebuild the Obsidian code map

- [ ] **Step 1:** Run graphify per HANDOFF: `/graphify D:\ShortsMaker --obsidian --obsidian-dir D:\ShortsMaker\code-map` (structural, no AI tokens).
- [ ] **Step 2:** Check `code-map/` has notes for `shortsmaker/*.py` modules and `graph.canvas` updated; `vault/Home.md` link still correct.
- [ ] **Step 3: Commit** "docs: rebuild code map".
