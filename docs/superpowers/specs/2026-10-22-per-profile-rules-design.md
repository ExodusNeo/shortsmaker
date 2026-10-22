# Per-profile rules files — design

Date: 2026-10-22. Status: approved in chat (sections 1 and 2), awaiting the owner's review of this file.

## Why

Every channel shares one set of story, topic and picture rules, written into the Python prompts and full of
strange-history examples (Jack the baboon, Great Stink, "our posted Shorts"). The gaming profile silently uses
them today. The owner wants each profile to have its own ruleset, so a new channel (next: engineering failures,
drawn in Blender) never changes strange-history, and rules that fit another niche are copied over, not shared.

This is project 1 of 2. Project 2 (Blender renderer for the engineering channel) gets its own design after this
is built; its planning rules will live only in that channel's rules file.

## The rules file

`channels/<name>.rules.md`, next to `channels/<name>.json`. Plain Markdown with fixed `##` headings; the code
reads each section by its heading (text up to the next `##`). The owner can read and edit it in Notepad or
Obsidian. Each section may start with an HTML comment tag (`<!-- copied from strange-history -->`,
`<!-- adapted from strange-history: ... -->`, `<!-- new -->`), which the loader strips before use.

| Heading | Content for strange-history (moved verbatim) | Used by (today's location) |
|---|---|---|
| `## Settings` | `status: ready`, `visuals: photos`, `min_real_pictures: 6` (one `key: value` per line) | `picture_pool.MIN_USABLE`; run start gate |
| `## Topic picking` | "pick stories whose single most shocking fact..." + the MAIN CHARACTER paragraph with its examples | topic prompt in `writing.write_scripts` |
| `## Story rules` | the whole of `STORY_RULES` | writer prompt and `edit_scripts` (both use `STORY_RULES`) |
| `## Writing for the picture` | "Write for the picture" + "Build on the real pictures" bullets | writer prompt |
| `## Lessons from our numbers` | the paragraph after the logbook results (two weak spots, 4-12 s drop, Great Stink / Norton) | `trend_text` in `write_scripts` |
| `## Opening picture` | the picture list's `hook:` and `era_ok:` definitions: story's own time, no museum/replica/reenactment/tourist photo, main character's face or a strange moment, never shows the twist; with the baboon and inflatable-tank examples | picture list prompt (`picture_pool`) |
| `## Directing` | the niche parts of the director prompt: scene 1's opening-picture rule in the `pic` bullet, the shot / image_search / video_search examples, "pictures from this topic's era and niche" | `direct_scripts` |
| `## First-second check` | "the main character or the strange situation, without giving the twist away" | `review.first_second_check` |
| `## AI paintings` | the whole of `AI_IMAGE_RULE` | `direct_scripts`, `review.py` repaint prompt |

The opening-picture idea appears in three prompts with different wording today; each keeps its own wording in
its own section, so strange-history's prompts stay word for word the same. Merging them is a later, separate
choice.

### Stays in the code, shared by every channel

Word counts and lengths (`length_plan`), `SCENE_CUTS`, scene word limits, "every fact must be true", no repeated
3-word phrases, the JSON reply formats, title / thumbnail / hook_text formats, `story_problems()` checks, the
picture `reject:` safety list (violence, watermarks, burned-in captions), all validation of AI replies, the fact
check, SEO, rendering and audio.

## Loading

New `rules.py` module (one job: read and check a channel's rules file):

- `load_rules(name) -> dict[str, str]`: parses headings, strips tag comments, returns `{heading: text}` plus a
  parsed `settings` dict.
- `REQUIRED` = the headings above. A missing or empty required heading stops the run at the start with
  `Stopped: channels/<name>.rules.md has no "## <heading>" section.` No fallback to another channel's rules.
- `status: draft` stops the run with `Stopped: channels/<name>.rules.md is a draft. Read it, edit anything you
  want, then change "status: draft" to "status: ready".`
- `visuals:` accepts `photos` (today's pipeline). `blender` is reserved for project 2 and stops the run with
  "not built yet" until then.
- Loaded once per run in `cli.py` right after the channel is picked, kept in `session.RULES`; prompt code reads
  `session.RULES["Story rules"]` etc. (cross-module access through the module, as the code-layout rules require).
- `picture_pool` reads `min_real_pictures` from the settings instead of the `MIN_USABLE` constant.

## New profiles

`channel_profiles.new_channel()` (run.bat "+ New channel") gains a second step after the profile JSON is saved:
`rules.draft_rules(ch, name)`.

- Input to the AI: the new profile (niche, audience, tone), the full text of every existing `*.rules.md`, the
  list of required headings and what each is for, and the allowed `## Settings` values.
- For each heading the AI either copies an existing channel's section word for word when it fits the new
  niche, or adapts/writes it, and tags it (`copied from <channel>`, `adapted from <channel>: <what changed>`,
  `new`). `status: draft` is always written, whatever the AI returns.
- The reply is checked like any AI reply: every required heading present and non-empty, else the draft is
  retried once, then the run stops with the reason (no half-written file is saved).
- After saving, run.bat prints the file path and stops instead of making Shorts (the draft gate above).
- The same function is run once by hand for the existing gaming profile; the owner reviews that draft too.
- The engineering-failures profile (`channel_ideas/engineering-failures.json`) is drafted the same way when the
  owner copies it into `channels/`; its `visuals:` stays `photos` until project 2.

## Migration

1. `channels/strange-history.rules.md` is written by hand from the current constants and prompt text, verbatim,
   with `status: ready`.
2. The constants and inline prompt text move out of `writing.py`, `picture_pool.py` and `review.py`; prompts
   read `session.RULES`.
3. Gaming gets a drafted file (status draft) for the owner to review.
4. HANDOFF.md: new "Rules per channel" section; code map refreshed.

## Testing

- **Golden prompts (strange-history unchanged):** before the move, capture every prompt the writer, editor,
  director, picture list and first-second check send for a fixed fake topic (fake `llm.ask_ai`, canned
  replies, as in `test_story.py`). After the move, the same capture must match word for word.
- `load_rules`: missing heading, empty heading, `status: draft`, `visuals: blender`, tag comments stripped,
  settings parsed.
- `draft_rules` with a canned AI reply: file written with `status: draft` and tags; a reply missing a heading is
  retried once, then stops without writing a file.
- `min_real_pictures` from settings reaches `prepare_topic`.
- Existing tests (`tests/`) still pass.

## Out of scope

Blender rendering, build plans and the engineering rules themselves (project 2); changing any strange-history
rule's content; per-channel shared-rule overrides (lengths, scene cuts) — they stay shared until a channel
needs otherwise.
