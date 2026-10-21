# Pictures first, then the script: design

Date: 2026-10-19. Status: approved in conversation (4 parts), waiting for the owner's review of this document.

## Goal
Find the real pictures and footage for a topic **before** the script is written, so the script is built around
what really exists. Today the script is finished first and `choose_images()` then hunts for a picture per line;
when nothing fits, the scene gets a painting or a weak match, which is where most review repaints come from.

Success: fewer AI paintings and weak matches per Short, fewer `CHECK: LOOK` repaints, boards that find their 3
real photos, and topics with nothing to show caught before any script is written.

## Decisions (owner)
- A topic with too few good real pictures is **skipped automatically** and a backup topic takes its place
  (not painted around, not asked about).
- Approach **A: a picture list for the writer.** The AI looks at the gathered pictures once and writes a short
  numbered list; writer, editor and director all see it; the director ties scenes to picture numbers. The story
  still comes first. Rejected: B (file titles only: unreliable, the old namesake problem) and C (one line per
  picture: hooks, open questions and forward pacing would bend to the photos).
- Unchanged: the script team (writer, OTHER AI edits, director, fact check), SEO, motion graphics, voice, render,
  review, fix.bat. Old Shorts and their `state.json` keep working.

## New order of steps
| # | Step | Change |
|---|---|---|
| 1 | Pick topics | Planner picks `n` topics **plus 2 backups**; each also gets `visual_terms` (4-6 search phrases for things a camera could show) and `people` (key people's full names). |
| 2 | Read Wikipedia | Same (`_texts`). |
| 3 | Gather pictures and footage | New `gather_pool()`: the pool-building half of today's `choose_images()`, moved out unchanged in its sources and caps. Queries from subject, `wiki_articles`, `visual_terms`, `people`. |
| 4 | Picture list | New `catalog_pool()`: one AI call views the contact sheets and describes every picture. |
| 5 | Topic check | Fewer than `MIN_USABLE` (6) usable: the topic is dropped and the next backup goes through steps 2-4. |
| 6 | Write, edit, direct, fact check | Writer, editor and director get the picture list; the director gives each scene a `pic`. |
| 7 | SEO | Same. |
| 8 | Picture step | `choose_images()` starts from the saved pool, searches only for scenes without a `pic` (and person-card portraits), and confirms or swaps the planned pictures. Then motion graphic rescue, then painting, as now. |
| 9 | Voice, render, review | Same. |

## Gathering (`gather_pool`)
- Same sources and caps as today: Wikipedia article images, Commons, Openverse, Internet Archive, NASA stills
  (up to 64), and up to 14 videos (Internet Archive, Commons, Pixabay, NASA) with 4 sampled frames each.
- Only preview thumbnails are fetched here; full-size files and film pieces still download at pick time.
- Saved per topic in `cache/pools/<hash of topic>/`: `pool.json` (candidates without bytes), thumbnails as files,
  the contact sheets and `catalog.json`. A cached pool is reused by "Both" mode (Gemini writes the same topics)
  and by a re-run, so nothing downloads twice; the 30-day cache prune applies.

## Picture list (`catalog_pool`)
- One AI call (Flash on Gemini, like the other picture jobs) opens the numbered sheets; per picture:
  `what` (<= 12 words), `era_ok` (story's era and place), `sharp` (1-3), `hook` (could open the Short),
  `reject` (violence/suffering, watermark or logo, burned-in subtitles or "subscribe" text, a caption naming a
  different event/place/person; else null). These reject rules move here from the picture step's prompt (the
  picture step keeps a one-line reminder because it can still swap).
- The reply is untrusted: numbers out of range, duplicates and missing fields are dropped; a picture with no
  usable entry counts as not usable.
- **Usable** = not rejected, `era_ok`, `sharp` >= 2. Frames of one video count as **one** usable item.

## Topic check
- `MIN_USABLE` = 6 (with 11-16 scenes, at most about half go to paintings and motion graphics).
- Fewer: drop the topic, try the next backup. Backups run out: the batch makes fewer Shorts and prints which
  topics were dropped and why. Dropped topics are **not** added to `done_topics` (they may return when better
  pictures exist).
- The picture-list call tries **both AIs**: the planner's AI first, then the other one if the first fails for
  any reason (AI error, broken reply, timeout, no credits); `ask_ai()` already does this. Only when **both** fail
  does the program print a clear error (which topic, what each AI said) and **stop the whole run** (owner's
  decision 2026-10-19: no Short made without its picture list). This happens
  before any script is written, so nothing half-made is left behind.
- In "Both" mode the check runs once, in Claude's half; Gemini's half reuses the same topics and lists.

## How the script uses the list
- The writer and editor get the usable pictures as a compact numbered list (`#12 film: 1944 newsreel of rubber
  tanks being inflated [opener]`), with openers marked. Writer rule: build the story where strong pictures
  exist and write the hook for an opener picture; every existing story rule stays (hook opens a question,
  scenes 2-3 move forward, 4-10 word scenes, no repeats). The writer does not assign numbers.
- The director gives every scene `pic` = a list number or null, and writes `shot` from that picture. Checked in
  code: in range, never the same number twice, at most 2 moments from one video (today's rule). For an evidence
  board, items may carry `pic` numbers (filled into `full_pictures`). Scenes with `pic` null still get
  `image_search` / `video_search` for the fill-in search.
- The fact check is unchanged; a rewritten line keeps its `pic`, and the picture step checks it still fits.

## Picture step (`choose_images`)
- Pool = the saved pool, plus new searches only for scenes with `pic` null and for person-card portraits. New
  candidates are appended so the list numbers stay valid.
- Still one AI call over all the sheets. It is told each scene's planned picture and keeps it unless it clearly
  doesn't fit the final line (then it picks another or null). Moves, AI motion, `subject_row`, looks, person
  cards and `full_pictures` work as today.
- No list (an old plan, e.g. fix.bat re-renders): exactly today's behaviour.

## Reporting
- edit_plan.txt: a line near the top, e.g. "Pictures found before writing: 9 usable of 41 (topics dropped: ...)",
  and per scene whether the planned picture was kept or swapped, with the reason.

## Testing
No AI usage (fake `ask_ai` replies, like `tests/test_full_scenes.py`):
- `gather_pool()` builds the same pool shape as the old code for the same queries (network stubbed).
- `catalog_pool()` parsing: bad numbers, missing fields, junk JSON.
- Usable count with frames of one video counted once.
- Topic swap: weak topic -> backup -> fewer Shorts with a message; dropped topics not in `done_topics`; catalog
  failure stops the run with an error message.
- Director `pic` checks: duplicates, out of range, the 2-moments-per-video cap.
- Picture step keeps a planned `pic`, appends new candidates without renumbering, and falls back to the old path
  with no list.
Then one real full Short, checked at 1 frame/s plus its CHECK lines, before calling it done.

## Safety
- Backup `backup/make_shorts_2026-10-19_before-pictures-first.py` before the change.
- HANDOFF.md updated (pipeline steps 1-5).
- fix.bat and the Shorts already made are untouched (they never redo steps 1-8).

## Out of scope
- No change to which sources are allowed, the caps, the story rules, SEO, motion graphics or rendering.
- No new AI provider, no paid API.
