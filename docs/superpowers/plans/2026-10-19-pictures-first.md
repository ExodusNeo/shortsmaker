# Pictures First Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Gather and catalogue each topic's real pictures and footage before the script is written, drop topics with too little to show, and let the writer/editor/director build the Short around numbered pictures.

**Architecture:** The pool-building half of `choose_images()` moves into `gather_pool()`; a new per-topic step `prepare_topic()` (Wikipedia, gather, AI picture list, check) runs inside `write_scripts()` before the writer. The pool and its list are cached per topic in `cache/pools/<hash>/`. `choose_images()` starts from that pool, searches only for scenes without a planned picture, and confirms or swaps the director's `pic` numbers. Old plans (fix.bat, `state.json` without a pool) keep today's path.

**Tech Stack:** Python 3.14 (`.venv`), single module `make_shorts.py`, plain-assert test scripts in `tests/`, AI via `ask_ai()` (Claude CLI / agy Gemini).

**Spec:** `docs/superpowers/specs/2026-10-19-pictures-first-design.md`

## Global Constraints
- `MIN_USABLE = 6`; usable = not `reject`, `era_ok` true, `sharp` >= 2; all frames of one video (same `film["src"]`) count as one.
- The topic planner returns `n + TOPIC_BACKUPS` topics, `TOPIC_BACKUPS = 2`.
- Sources, caps and licence rules unchanged: up to 64 stills, up to 14 videos x 4 frames, same search functions and per-source caps as today's `choose_images()`.
- The picture-list call is `ask_ai(..., fatal=False, read_dir=<sheets folder>)` (both AIs are tried; picture calls already run Gemini on Flash). Only if it returns no usable reply: print which topic failed and `sys.exit(...)` the whole run, before any script is written.
- Dropped topics are never added to `done_topics`.
- AI replies are untrusted: every number from the AI is checked (int, not bool, in range).
- No new dependencies, no paid APIs, no license-rule changes.
- The project is not a git repo: there are no commit steps; each task ends by running the full test suite.
- Comments only for the why; match the module's style (long-line, terse docstrings).
- Never run `tests/render_full.py` while a batch is running.

## Review Focus
1. The 30-day cache prune in `main()` does `old.unlink()` on everything in `cache/`: the new `cache/pools/` folder would crash every run once it is 30 days old. Expected: old pool folders are removed, nothing crashes. (Task 1 test `test_prune_cache_handles_pools`.)
2. A topic whose searches all come back empty (no Wikipedia article, obscure subject): no contact sheets exist. Expected: 0 usable, topic dropped quietly, no AI call and no `sys.exit`. (Task 3 test `test_empty_pool_drops_topic_without_ai`.)
3. A crash or Ctrl+C between gathering and the picture list leaves `pool.json` without `catalog.json`. Expected: the next run reuses the pool and redoes only the list. (Task 2 test `test_catalog_redone_when_missing`.)
4. "Both" mode: Gemini's planner rewords the topics, so a cache keyed by topic text would miss. Expected: Gemini's half reuses Claude's folders by position, with no new downloads. (Task 3 test `test_both_mode_reuses_pools`.)
5. The AI answers the picture list with numbers as strings, bools, or `sharp` outside 1-3. Expected: those entries are ignored, not crashed on, and not counted as usable. (Task 2 test `test_catalog_junk`.)

---

### Task 1: Move pool building into `gather_pool()`, cache pools per topic

**Files:**
- Modify: `make_shorts.py` (`choose_images()` lines ~1942-2010, `main()` cache prune ~4540, constants near `CACHE` ~1440)
- Test: `tests/test_pictures_first.py` (new; same runner footer as `tests/test_full_scenes.py`)

**Interfaces:**
- Produces: `POOLS = CACHE / "pools"`, `MIN_USABLE = 6`, `TOPIC_BACKUPS = 2`;
  `gather_pool(articles: list[str], people: list[str], image_terms: list[str], video_terms: list[str]) -> list[dict]` (candidates with `thumb` bytes, stills first then film frames, exactly today's dict shape);
  `pool_folder(topic: str) -> Path` (`POOLS / sha1(topic)[:12]`);
  `save_pool(folder: Path, cands: list[dict]) -> None` (writes `pool.json` without bytes + `thumb{k}.jpg`, k = list index);
  `load_pool(folder: Path) -> list[dict] | None` (None when `pool.json` is missing; same order, `thumb` restored);
  `prune_cache() -> None` (files older than 30 days as today; pool folders whose `pool.json` is older than 30 days removed with `shutil.rmtree`).

- [ ] **Step 1: Back up** `make_shorts.py` to `backup/make_shorts_2026-10-19_before-pictures-first.py`.
- [ ] **Step 2: Write failing tests** in `tests/test_pictures_first.py`, with all network functions stubbed (`article_images`, `commons_search`, `openverse_images`, `archive_images`, `nasa_images`, `archive_films`, `commons_films`, `pixabay_films`, `nasa_films`, `get_image`, `film_frames`):
  - `test_gather_pool_shape`: stills carry `url,title,credit,thumb`; each stubbed film gives 4 candidates with `film` and `url == f"{src}#t={t:.0f}"`; there are no duplicate urls; there are at most 64 stills.
  - `test_pool_roundtrip`: `save_pool` then `load_pool` returns the same urls in the same order with identical `thumb` bytes; `load_pool(empty_dir) is None`.
  - `test_prune_cache_handles_pools`: with a temp `CACHE`/`POOLS` holding an old file, an old pool folder (mtime set 31 days back via `os.utime`) and a fresh one, `prune_cache()` removes the old file and the old folder, keeps the fresh one, and raises nothing.
- [ ] **Step 3: Run** `.venv\Scripts\python.exe tests\test_pictures_first.py`; expected: FAIL (names not defined).
- [ ] **Step 4: Implement.** Cut the pool code out of `choose_images()` into `gather_pool()` unchanged (only its inputs become parameters); `choose_images()` calls `gather_pool(articles, names, scene_imgs, scene_vids)` for now. Add `pool_folder`, `save_pool`, `load_pool`, `prune_cache`; `main()` calls `prune_cache()` instead of its inline loop.
- [ ] **Step 5: Run** the new tests plus `tests\test_full_scenes.py`, `tests\test_style.py`, `-m py_compile make_shorts.py`; expected: all PASS.

### Task 2: The picture list (`catalog_pool`) and the usable count

**Files:**
- Modify: `make_shorts.py` (new functions after `contact_sheets()`)
- Test: `tests/test_pictures_first.py`

**Interfaces:**
- Consumes: `contact_sheets(cands, folder)`, `save_pool`/`load_pool` (Task 1), `ask_ai`.
- Produces:
  `catalog_pool(s: dict, cands: list[dict], folder: Path) -> list[dict]`: reuses `folder/"catalog.json"` if present; else builds `folder/"sheets"`, one `ask_ai(prompt, fatal=False, read_dir=folder/"sheets")`, keeps valid entries, writes `catalog.json`, returns entries `{"n": int, "what": str, "era_ok": bool, "sharp": int, "hook": bool, "reject": str | None}`. Reply schema: `{"pictures": [{"n": 1, "what": "...", "era_ok": true, "sharp": 3, "hook": false, "reject": null}]}`. If the reply is None or has no `pictures` list: `sys.exit(f'Stopped: no picture list for "{s["topic"]}". Neither Claude nor Gemini gave a usable answer (their messages are above).')`. With `cands == []` it returns `[]` without any AI call.
  `is_usable(entry: dict) -> bool` (not `reject`, `era_ok`, `sharp` >= 2);
  `usable(cands: list[dict], catalog: list[dict]) -> list[dict]` (entries passing `is_usable`, at most one per `film["src"]`, the sharpest frame wins: used for the count only);
  `catalog_text(cands: list[dict], catalog: list[dict]) -> str` (one line per usable entry: `#12 film: <what> [opener]`; `film`/`photo` from the candidate, `[opener]` when `hook`).
- Prompt content: the subject, topic and era; the reject reasons copied from `choose_images()`'s rules (the picker keeps its own copy: it can still swap) (violence/torture/executions/corpses/suffering, watermark or logo, burned-in subtitles or "subscribe" text after the crop, a printed caption naming a different event/place/person, a namesake); "open and look at every sheet"; file titles as a reference, like `choose_images()` does.

- [ ] **Step 1: Write failing tests:**
  - `test_catalog_junk`: a fake `ask_ai` returns entries with `"n": "3"`, `"n": True`, `"n": 99` (out of range), `"sharp": 7`, a duplicate `n`, and one good entry. Only the good entry is kept (bad `sharp` dropped), and `catalog.json` holds exactly it.
  - `test_catalog_failure_stops`: fake `ask_ai` returns None; `catalog_pool` raises `SystemExit` whose message contains the topic text.
  - `test_catalog_redone_when_missing`: with `pool.json` saved and no `catalog.json`, `catalog_pool` calls the AI once; a second call reads the file and calls it 0 times.
  - `test_usable_counts_film_once`: 4 good frames of one `film["src"]` + 2 good stills + 1 still with `reject` + 1 with `era_ok` false + 1 with `sharp` 1 → `len(usable(...)) == 3`.
  - `test_catalog_text`: a line for a film opener reads `#5 film: ... [opener]`; rejected entries are absent.
- [ ] **Step 2: Run** the tests; expected: FAIL.
- [ ] **Step 3: Implement** the three functions as specified above.
- [ ] **Step 4: Run** the full suite (all test files + `py_compile`); expected: PASS.

### Task 3: Topics with backups, `prepare_topic()`, and the check inside `write_scripts()`

**Files:**
- Modify: `make_shorts.py` (`write_scripts()` topic prompt + the Wikipedia loop ~521-575; `main()` Both-mode call ~4560)
- Modify: `tests/test_full_scenes.py` (`_fake_planning` stubs `prepare_topic`)
- Test: `tests/test_pictures_first.py`

**Interfaces:**
- Consumes: Tasks 1-2.
- Produces:
  `prepare_topic(s: dict, folder: Path | None = None) -> bool`: reads Wikipedia into `s["_texts"]` (today's loop); `folder = folder or pool_folder(s["topic"])`; `load_pool(folder)` or `gather_pool(s["wiki_articles"], s["people"], s["visual_terms"], s["visual_terms"])` + `save_pool`; `catalog_pool`; sets `s["pool_dir"] = str(folder)`, `s["catalog"]`, `s["picture_check"] = f"{len(usable)} usable of {len(cands)}"`; returns `len(usable) >= MIN_USABLE`.
  `write_scripts(ch: dict, n: int, topics: list[str] | None = None, pools: list[str] | None = None) -> list[dict]`: the topic prompt asks for `n + TOPIC_BACKUPS` topics (exactly `len(topics)` when `topics` is given) and two new fields per topic: `visual_terms` (4-6 short search phrases for people, places, objects and events a camera could show) and `people` (key people's full names, may be empty), both cleaned like `search_terms`. Topics are prepared in order until `n` pass; with `pools`, topic i uses `Path(pools[i])`. Failures print `  Skipped "<topic>": only <picture_check> real pictures/clips`; every kept short gets `s["dropped_topics"]` (a list of those lines). If none pass: print `No topic had enough real pictures this time; nothing was made.` and return `[]` (instead of the current assert).
  `main()`: Both mode passes `pools=[s["pool_dir"] for s in shorts]` to the second half.

- [ ] **Step 1: Write failing tests** (fake `ask_ai`; `prepare_topic` or its parts stubbed as needed):
  - `test_topic_prompt_asks_backups_and_visuals`: for `n=1`, the topic prompt asks for 3 topics and contains `visual_terms` and `people`.
  - `test_weak_topic_swapped_for_backup`: `prepare_topic` stub returns False for the first topic, True for the second; result is 1 short on topic 2, its `dropped_topics` names topic 1, and topic 1 is not in `ch["done_topics"]`.
  - `test_all_weak_returns_empty`: all False → `write_scripts` returns `[]` and the writer prompt was never sent.
  - `test_empty_pool_drops_topic_without_ai`: with real `prepare_topic`, stubbed `gather_pool` returning `[]` and `article_text` returning "", `prepare_topic` returns False and the fake `ask_ai` was never called.
  - `test_both_mode_reuses_pools`: `pools=[str(dirA)]` with `pool.json` and `catalog.json` in dirA → `gather_pool` and the catalog AI are called 0 times and `pool_dir == str(dirA)`.
- [ ] **Step 2: Update** `_fake_planning` in `tests/test_full_scenes.py` to stub `m.prepare_topic` (sets `pool_dir`, an empty `catalog`, `picture_check`, `_texts`; returns True).
- [ ] **Step 3: Run;** expected: the new tests FAIL, old ones still PASS.
- [ ] **Step 4: Implement** as specified.
- [ ] **Step 5: Run** the full suite; expected: PASS.

### Task 4: The writer, editor and director see the list; the director plans `pic`

**Files:**
- Modify: `make_shorts.py` (writer prompt + `research` list in `write_scripts()`; `edit_scripts()` drafts; `direct_scripts()` prompt and reply schema; the normalisation loop at the end of `write_scripts()`)
- Test: `tests/test_pictures_first.py`

**Interfaces:**
- Consumes: `catalog_text` (Task 2), `s["catalog"]`, `s["pool_dir"]` (Task 3).
- Produces:
  each topic in the writer's research and each editor draft gets `"pictures": catalog_text(...)` (the candidates come from `load_pool(Path(s["pool_dir"]))`);
  writer rule (one bullet, added after "Write for the picture"): build the story where strong pictures in its `pictures` list exist, and write the hook for an `[opener]` picture when one fits; every other rule stays;
  director: each scene may carry `"pic": <list number or null>`; `shot` is written from that picture; board `items` may carry `"pic"`; `image_search`/`video_search` stay required (used only when `pic` is null);
  `clean_pics(s: dict, cands: list[dict]) -> None`: sets every `sc["pic"]` to a valid number or None (int, not bool, 1..len(cands), never twice, at most 2 per `film["src"]`, in scene order; its catalog entry must pass `is_usable`; the per-video grouping of `usable()` does not apply here), and the same for board item `pic`s. It's called in the normalisation loop when `s.get("pool_dir")`; otherwise every `sc["pic"] = None`.

- [ ] **Step 1: Write failing tests:**
  - `test_prompts_carry_picture_list`: with the fake planning flow from Task 3 and a catalog stub, the writer, editor and director prompts all contain the `#N` lines, and the writer prompt contains "[opener]".
  - `test_clean_pics`: scene pics `[3, 3, True, 99, "4", 5, 6, 7]`, with candidates 5, 6 and 7 frames of one film → result `[3, None, None, None, None, 5, 6, None]`; a pic pointing at a rejected entry becomes None.
  - `test_board_item_pics_cleaned`: board items `[{"pic": 2}, {"pic": 2}, {"pic": 0}]` → `[2, None, None]`.
- [ ] **Step 2: Run;** expected: FAIL.
- [ ] **Step 3: Implement** as specified.
- [ ] **Step 4: Run** the full suite; expected: PASS.

### Task 5: `choose_images()` starts from the pool and confirms the plan

**Files:**
- Modify: `make_shorts.py` (`choose_images()`, `full_pictures()`, `render()` where `source` is built ~4280)
- Test: `tests/test_pictures_first.py`

**Interfaces:**
- Consumes: `load_pool`, `gather_pool`, `contact_sheets`, `sc["pic"]`, board item `pic`.
- Produces:
  with `short.get("pool_dir")`: `cands = load_pool(...)` + new candidates from `gather_pool([], person names, image_search of scenes with pic None, video_search of the same scenes)`, appended with url de-duplication so the list numbers stay valid; the contact sheets are rebuilt over the whole list; each scene in the picker prompt gets `"planned_picture": N` (and board `"planned_full_pictures": [..]`), with the rule: keep it unless it clearly doesn't fit the final line, else pick another or null and give `swap_why`. The reply's `picks` gains an optional `"swap_why"`.
  If the visual call and the title fallback both fail, the planned numbers are used as the picks.
  `choices[i]["plan_note"]`: `"planned picture kept"` / `f"planned #{N} swapped: {swap_why}"` (no note when the scene had no plan); `render()` appends `f" | {plan_note}"` to that scene's `source`.
  No `pool_dir`: unchanged behaviour (old plans, fix.bat).

- [ ] **Step 1: Write failing tests** (network and `film_piece`/`get_image` stubbed; fake `ask_ai` captures the prompt):
  - `test_choose_keeps_plan_and_appends`: a pool of 5 saved; scene 1 `pic=2`, scene 2 `pic=None`; the stubbed `gather_pool` returns 2 new candidates for scene 2's search. The prompt contains `"planned_picture": 2`; candidates 1-5 keep their numbers (the 6th is the first new one); the AI's pick of 2 for scene 1 gives `plan_note == "planned picture kept"`.
  - `test_choose_swap_note`: the AI picks 4 for a scene planned with 2, with `swap_why` "wrong ship" → `plan_note == "planned #2 swapped: wrong ship"`.
  - `test_choose_falls_back_to_plan`: fake `ask_ai` returns None for both calls → scene 1 gets candidate 2.
  - `test_choose_old_path_unchanged`: no `pool_dir` → `gather_pool` is called once with the scene-derived queries, and no prompt contains "planned_picture".
- [ ] **Step 2: Run;** expected: FAIL.
- [ ] **Step 3: Implement** as specified.
- [ ] **Step 4: Run** the full suite; expected: PASS.

### Task 6: Report, document, and one real Short

**Files:**
- Modify: `make_shorts.py` (`edit_plan()` header ~3860)
- Modify: `HANDOFF.md` (pipeline steps 1-5, file table entry for `cache/pools/`, test counts)
- Test: `tests/test_pictures_first.py`

**Interfaces:**
- Consumes: `short["picture_check"]`, `short["dropped_topics"]`, `plan_note` (Tasks 3, 5).
- Produces: an edit_plan.txt line after "Renderer:": `Pictures found before writing: <picture_check>` plus `(topics dropped: <a>; <b>)` when any; omitted for old plans.

- [ ] **Step 1: Write failing test** `test_edit_plan_picture_line`: `edit_plan()` output for a short with `picture_check="9 usable of 41"` and one dropped topic contains both; without `picture_check` the line is absent.
- [ ] **Step 2: Run;** expected: FAIL. **Step 3: Implement.** **Step 4: Run** the full suite; expected: PASS.
- [ ] **Step 5: Update HANDOFF.md:** the new pipeline order, `MIN_USABLE`, the stop-on-failure rule, `cache/pools/`, test counts.
- [ ] **Step 6: Real run** (spends AI usage; owner present): `.venv\Scripts\python.exe -u make_shorts.py 1 strange-history`. Check the console for the gather/list/check lines, then edit_plan.txt for the picture line and the kept/swapped notes, then a 1 frame/s sheet (`ffmpeg -i short.mp4 -vf "fps=1,scale=180:-1,tile=11x5" -frames:v 1 sheet.jpg`) and the CHECK lines. Compare with the Ghost Army / Onoda Shorts: count the AI paintings and the review repaints. Report the numbers to the owner.
