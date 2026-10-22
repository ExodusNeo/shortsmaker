# Per-profile Rules Files Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move every niche-specific prompt rule out of the Python code into `channels/<name>.rules.md`, one per channel, with AI-drafted rules for new profiles, without changing a single word strange-history's AI receives.

**Architecture:** A new `shortsmaker/rules.py` reads and checks a channel's Markdown rules file and puts its sections in `session.RULES` / `session.RULE_SETTINGS`; prompt code reads sections from there instead of module constants. A golden-prompt test, captured from today's code before anything moves, proves strange-history's prompts are unchanged (whitespace-normalized, word for word).

**Tech Stack:** Python 3.12 (D:\ShortsMaker\.venv), existing `llm.ask_ai`, plain-script tests (`tests/test_*.py` with the `__main__` runner used by `tests/test_story.py`).

**Spec:** `docs/superpowers/specs/2026-10-22-per-profile-rules-design.md`

## Global Constraints

- Rules file path: `channels/<name>.rules.md` (`config.CHANNELS / f"{name}.rules.md"`), UTF-8, read with `encoding="utf-8-sig"` (Notepad BOM).
- Required headings, exactly: `Settings`, `Topic picking`, `Story rules`, `Writing for the picture`, `Lessons from our numbers`, `Opening picture`, `Directing`, `First-second check`, `AI paintings`.
- Settings keys: `status` (`draft` | `ready`), `visuals` (`photos` | `blender`), `min_real_pictures` (positive int).
- Stop messages, verbatim: `Stopped: channels/<name>.rules.md has no "## <heading>" section.` and `Stopped: channels/<name>.rules.md is a draft. Read it, edit anything you want, then change "status: draft" to "status: ready".`
- `visuals: blender` stops with: `Stopped: channels/<name>.rules.md asks for Blender visuals, which aren't built yet.`
- No fallback to another channel's rules, ever.
- Section tag comments (`<!-- ... -->` on the section's first line) are stripped before use.
- Cross-module reads go through the module: `session.RULES[...]`, never `from shortsmaker.session import RULES`.
- Strange-history's prompts must stay word for word identical (compare with `" ".join(text.split())`).
- Run tests with `.venv\Scripts\python.exe tests\<file>.py` from `D:\ShortsMaker`.
- Commits end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

- Notepad saves the rules file with a BOM and CRLF line endings: it must load exactly like an LF file (test in Task 2).
- The owner retypes a heading as `## story rules` or `##  Story Rules ` : headings match case-insensitively with spaces trimmed (test in Task 2).
- The owner adds `### Examples` inside a section: only `## ` (level 2) starts a new section (test in Task 2).
- The same `##` heading appears twice: stop with `Stopped: channels/<name>.rules.md has "## <heading>" twice.` (test in Task 2).
- `status: Ready` / `min_real_pictures:  4 ` : settings values are trimmed and case-insensitive; a non-number `min_real_pictures` stops with `Stopped: channels/<name>.rules.md: min_real_pictures must be a whole number.` (test in Task 2).

---

### Task 1: Capture today's prompts as golden files

**Files:**
- Create: `tests/test_rules.py`
- Create: `tests/golden/prompts.json` (generated, committed)

**Interfaces:**
- Produces: `capture_prompts() -> dict[str, str]` in `tests/test_rules.py`, keys `topics`, `writer`, `editor`, `director`, `fact_check`, `picture_list`, `first_second`, `repaint`; values are the prompt strings sent to `llm.ask_ai`. Run as `.venv\Scripts\python.exe tests\test_rules.py --save-golden` it writes `tests/golden/prompts.json`.

- [ ] **Step 1: Write `capture_prompts()`**

Fake everything outside the prompts (restore all in `finally`): `llm.ask_ai` records each prompt and returns a canned reply chosen by the prompt's opening words; `channel_profiles.trend_research` returns one fixed trend row `{"title": "T", "views": 1000, "channel": "C"}`; `logbook.logbook_results` returns `"- Example Short | 1,000 views"`; `picture_pool.prepare_topic` sets `s["_texts"] = {"Jack (baboon)": "text"}`, `s["catalog"] = []`, `s["pool_dir"] = None` and returns `True`; `writing.fact_check` is left real but its prompt is captured by the fake `ask_ai` (reply `{"ok": true}` shaped the way `fact_check` reads it). Drive `writing.write_scripts(ch, 1)` with `ch` = the strange-history profile loaded from `channels/strange-history.json`; call `picture_pool.catalog_pool` with `contact_sheets` faked to return `[Path("<TMP>/sheet1.jpg")]`; call `review.first_second_check` the way `tests/test_first_second.py::run_check` does; call `review.rewrite_paint_prompts(short, {2: "garbled sign"})`. Replace any temp-dir path in captured prompts with `<TMP>`.

- [ ] **Step 2: Generate and inspect the golden file**

Run: `.venv\Scripts\python.exe tests\test_rules.py --save-golden`
Expected: `tests/golden/prompts.json` with all 8 keys; `writer` contains `OPEN INSIDE THE STORY'S STRANGEST MOMENT`, `topics` contains `MAIN CHARACTER`, `picture_list` contains `era_ok:`, `repaint` contains the first line of `writing.AI_IMAGE_RULE`.

- [ ] **Step 3: Add `test_strange_history_prompts_unchanged`**

```python
def test_strange_history_prompts_unchanged():
    golden = json.loads((HERE / "golden" / "prompts.json").read_text(encoding="utf-8"))
    now = capture_prompts()
    for key, text in golden.items():
        assert " ".join(now[key].split()) == " ".join(text.split()), key
```

Run: `.venv\Scripts\python.exe tests\test_rules.py test_strange_history_prompts_unchanged`
Expected: `1/1 passed` (golden was just taken from the same code).

- [ ] **Step 4: Commit**

```bash
git add tests/test_rules.py tests/golden/prompts.json
git commit -m "test: golden capture of strange-history prompts before the rules move"
```

### Task 2: `rules.py` loader and checks

**Files:**
- Create: `shortsmaker/rules.py`
- Modify: `shortsmaker/session.py` (add `RULES: dict[str, str] = {}` and `RULE_SETTINGS: dict[str, str] = {}` with a one-line comment)
- Test: `tests/test_rules.py`

**Interfaces:**
- Produces:
  - `REQUIRED: tuple[str, ...]` = the 9 headings in Global Constraints, in that order.
  - `parse_rules(text: str, label: str) -> tuple[dict[str, str], dict[str, str]]`: `(sections, settings)`. `sections` keys are the canonical heading names from `REQUIRED` (unknown headings kept under their trimmed text); values have the tag comment and outer blank lines stripped. `settings` parsed from the `Settings` section, keys and values lowercased and trimmed. `label` is the `channels/<name>.rules.md` text used in stop messages. Raises `SystemExit(<stop message>)` for: duplicate heading, missing/empty required heading, `status` not `ready` (draft message), `visuals: blender`, bad `min_real_pictures`.
  - `load_rules(name: str) -> None`: reads `CHANNELS / f"{name}.rules.md"` (missing file = the missing `Settings` message), calls `parse_rules`, sets `session.RULES` and `session.RULE_SETTINGS`.
  - `min_real_pictures() -> int`: `int(session.RULE_SETTINGS["min_real_pictures"])`.

- [ ] **Step 1: Write the failing tests**

Build a valid text with a helper `make(**overrides)` that writes all 9 sections (`Settings` = `status: ready\nvisuals: photos\nmin_real_pictures: 6`, others one line each). Tests:

```python
def test_parses_sections_and_settings(): ...      # sections["Story rules"] == "story text"; settings == {"status": "ready", "visuals": "photos", "min_real_pictures": "6"}
def test_strips_tag_comments(): ...               # "<!-- copied from strange-history -->\nX" -> "X"
def test_bom_and_crlf_load_the_same(): ...        # "\ufeff" + text.replace("\n", "\r\n") parses to the same dicts
def test_heading_case_and_spaces(): ...           # "##  story RULES " is "Story rules"
def test_level3_heading_stays_inside(): ...       # "### Examples" line remains in the Story rules text
def test_missing_heading_stops(): ...             # SystemExit text == 'Stopped: channels/x.rules.md has no "## Directing" section.'
def test_empty_heading_stops(): ...               # same message for a heading with only blank lines/tag
def test_duplicate_heading_stops(): ...           # 'Stopped: channels/x.rules.md has "## Directing" twice.'
def test_draft_stops(): ...                       # "status: Draft" -> the draft message, verbatim
def test_blender_stops(): ...                     # "visuals: blender" -> the Blender message
def test_bad_min_pictures_stops(): ...            # "min_real_pictures: six" -> the whole-number message
def test_load_rules_sets_session(): ...           # temp CHANNELS dir: session.RULES["Topic picking"] set, rules.min_real_pictures() == 6
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv\Scripts\python.exe tests\test_rules.py`
Expected: the new tests FAIL with `ModuleNotFoundError`/`AttributeError` for `rules`; the golden test still passes.

- [ ] **Step 3: Implement `shortsmaker/rules.py` and the two `session` attributes**

Split on lines matching `^##\s+(.*?)\s*$` but not `^###`; match headings to `REQUIRED` by `.strip().lower()`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv\Scripts\python.exe tests\test_rules.py`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add shortsmaker/rules.py shortsmaker/session.py tests/test_rules.py
git commit -m "feat: rules.py reads and checks a channel's rules file"
```

### Task 3: Strange-history rules file and prompts read from it

**Files:**
- Create: `channels/strange-history.rules.md`
- Modify: `shortsmaker/writing.py` (topic prompt, writer prompt, `trend_text`, `edit_scripts`, `direct_scripts`; remove `STORY_RULES`, `AI_IMAGE_RULE`)
- Modify: `shortsmaker/picture_pool.py` (`catalog_pool` prompt; `MIN_USABLE` replaced by `rules.min_real_pictures()`)
- Modify: `shortsmaker/review.py` (`first_second_check`, `rewrite_paint_prompts`)
- Modify: `shortsmaker/cli.py` (`main` after `use_channel(name)`, `fix_short` after its `use_channel`: call `rules.load_rules(name)`)
- Modify: tests that build prompts (`tests/test_story.py`, `tests/test_first_second.py`, `tests/test_pictures_first.py`, any other that fails): call `rules.load_rules("strange-history")` in their setup
- Test: `tests/test_rules.py`

**Interfaces:**
- Consumes: `rules.load_rules`, `rules.min_real_pictures`, `session.RULES` (Task 2); `capture_prompts` (Task 1).

Section boundaries (copy the text verbatim from today's code into the file; the code inserts `session.RULES[<heading>]` exactly where the text was):

| Heading | Exact text moved |
|---|---|
| `Settings` | `status: ready` / `visuals: photos` / `min_real_pictures: 6` |
| `Topic picking` | topic prompt, from `Viewers decide in one second whether to swipe` through `only when nothing better is left.` |
| `Story rules` | the whole `STORY_RULES` string (writer and editor both insert it) |
| `Writing for the picture` | the writer's two bullets `- Write for the picture:` and `- Build on the real pictures:` |
| `Lessons from our numbers` | `trend_text`, from `Two weak spots:` through `made every beat stranger than the last.` |
| `Opening picture` | `catalog_pool` prompt, the `- era_ok:`, `- sharp:` and `- hook:` bullets |
| `Directing` | `direct_scripts` prompt, from `- pic = ` through the end of the `shot = ` bullet (`...or pictures from this topic's era and niche could show.`) |
| `First-second check` | `the main character or the strange situation, without giving the twist away.` |
| `AI paintings` | the whole `AI_IMAGE_RULE` string |

The evidence-board / document / graphic format examples later in `direct_scripts` stay in the code (they show reply formats, shared by every channel).

- [ ] **Step 1: Point `capture_prompts()` at the rules file**

Add `rules.load_rules("strange-history")` at the start of `capture_prompts()`. Run: `.venv\Scripts\python.exe tests\test_rules.py test_strange_history_prompts_unchanged`
Expected: FAIL (`channels/strange-history.rules.md` doesn't exist: the missing `Settings` stop message).

- [ ] **Step 2: Write `channels/strange-history.rules.md` and switch the prompts**

Each section starts with `<!-- strange-history's original rules, moved from the code 2026-10-22 -->`.

- [ ] **Step 3: Run the golden test**

Run: `.venv\Scripts\python.exe tests\test_rules.py`
Expected: all pass, including `test_strange_history_prompts_unchanged`.

- [ ] **Step 4: Add `test_min_pictures_from_settings`**

With `session.RULE_SETTINGS["min_real_pictures"] = "2"`, `picture_pool.prepare_topic` on a topic whose faked pool has 2 usable candidates returns `True`; with `"3"` it returns `False`.

- [ ] **Step 5: Run every test file**

Run: `for %f in (tests\test_*.py) do .venv\Scripts\python.exe %f` (or each file by hand)
Expected: every file ends `N/N passed`. Fix any test that now needs `rules.load_rules("strange-history")`.

- [ ] **Step 6: Commit**

```bash
git add channels/strange-history.rules.md shortsmaker tests
git commit -m "feat: strange-history's rules live in channels/strange-history.rules.md"
```

### Task 4: AI-drafted rules for new profiles

**Files:**
- Modify: `shortsmaker/rules.py` (add `draft_rules`)
- Modify: `shortsmaker/channel_profiles.py:39-45` (`pick_channel`: after `new_channel(...)`, call `rules.draft_rules(ch, name)` then `sys.exit(<review message>)`)
- Test: `tests/test_rules.py`

**Interfaces:**
- Consumes: `REQUIRED`, `parse_rules` (Task 2).
- Produces: `draft_rules(ch: dict, name: str) -> Path`: one `llm.ask_ai` call (reply JSON `{"sections": {"<heading>": {"tag": "copied from strange-history" | "adapted from <channel>: <what changed>" | "new", "text": "..."}}}`), checked: every `REQUIRED` heading present with non-empty `text`; one retry on a bad reply, then `SystemExit("Stopped: couldn't draft rules for <name>: <reason>")` with no file written. `Settings` is written by the code, never taken from the AI's text: `status: draft`, `visuals:` from the AI's choice if `photos` or `blender` else `photos`, `min_real_pictures:` from the AI if a positive int else `6`. Writes `CHANNELS / f"{name}.rules.md"` (refuses to overwrite an existing file: `SystemExit("Stopped: channels/<name>.rules.md already exists.")`) and returns its path.
- Review message printed by `pick_channel`: `Rules drafted: channels/<name>.rules.md\nRead it, edit anything you want, then change "status: draft" to "status: ready" and run again.`

Prompt contents: the new profile's niche, audience and tone; the full text of every existing `channels/*.rules.md` with its channel name; each required heading with one line on what it is for (from the spec's table); the rule "copy a section word for word when it fits this niche, otherwise adapt or write it, and say which in `tag`".

- [ ] **Step 1: Write the failing tests**

```python
def test_draft_writes_tagged_draft_file(): ...     # fake ask_ai returns all 9 sections; file exists, "status: draft" in it, "<!-- copied from strange-history -->" in it, parse_rules on it raises the draft stop
def test_draft_settings_come_from_code(): ...      # AI says status "ready", min "lots": file still has status: draft, min_real_pictures: 6
def test_draft_retries_once_then_stops(): ...      # replies missing "## Directing" twice: SystemExit mentions Directing, no file written, ask_ai called twice
def test_draft_never_overwrites(): ...             # existing file: SystemExit "already exists", file unchanged
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv\Scripts\python.exe tests\test_rules.py`
Expected: the 4 new tests FAIL (`draft_rules` missing).

- [ ] **Step 3: Implement `draft_rules` and the `pick_channel` hook**

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv\Scripts\python.exe tests\test_rules.py`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add shortsmaker/rules.py shortsmaker/channel_profiles.py tests/test_rules.py
git commit -m "feat: new profiles get AI-drafted rules for the owner to review"
```

### Task 5: Gaming draft, docs and code map

**Files:**
- Create: `channels/gaming.rules.md` (drafted by `draft_rules`, a real AI call)
- Modify: `HANDOFF.md` (new section "Rules per channel": file location, headings, draft gate, what stays shared; update the file table row for `channels/`)
- Modify: `graphify-out/` (refresh, as in commit `b8f45c9`)

- [ ] **Step 1: Draft the gaming rules**

Run: `.venv\Scripts\python.exe -c "from shortsmaker import channel_profiles, rules; channel_profiles.use_channel('gaming'); print(rules.draft_rules(channel_profiles.load_channel(), 'gaming'))"`
Expected: prints `...channels\gaming.rules.md`; the file has all 9 headings, each tagged, and `status: draft`. Then `.venv\Scripts\python.exe make_shorts.py 1 gaming` stops with the draft message.

- [ ] **Step 2: Update HANDOFF.md and refresh the code map**

- [ ] **Step 3: Run every test file once more**

Expected: every file ends `N/N passed`.

- [ ] **Step 4: Commit**

```bash
git add channels/gaming.rules.md HANDOFF.md graphify-out
git commit -m "docs: rules per channel; gaming rules drafted for review"
```
