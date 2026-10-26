# Blender openers (animated scene 1) — design

Date: 2026-10-27. Status: approved in chat, awaiting the owner's review of this file.
Part 1 of 2. Part 2 (motion-graphic openers for stories Part 1 can't build) gets its own spec later.

## Why

Stayed-to-watch (the first second) is the channels' weakest number: strange-history 21-58%, weird-economics
Match King 29.7%. Research on 2026-10-27 (Chrome, no vidIQ credits) compared the first second of 9 hits with 12 of
ours. Voggle's "True Story of Mike the Headless Chicken" (2.7M) opens on an animated chicken on the chopping block
while the axe falls; ours (1.4K) opened on a still photo with a summary line. Our three lowest-stay Shorts opened on
calm portraits, and nothing in our first second moves (frames at 0.1 s and 1.0 s look the same).

The owner wants every Short to open on an animation of the story's strangest moment, for the channel brand, made
in Blender or as a motion graphic. This spec covers Blender. Part 2 covers motion graphics for the rest (people
stories, and anything the model libraries can't show).

## Decisions made in chat

- Every Short gets an animated opener (brand), not only the ones with weak pictures.
- Approach: the AI writes a staging plan; our own code animates it from a fixed list of tested moves and checks
  the result. The AI never writes Blender code (same rule as the bridge channel).
- Models come from the free libraries through the owner's live Blender (the MCP add-on holds the Poly Pizza key)
  and are saved on D: so later runs reuse them without Blender.
- run.bat reminds the owner to start the Blender MCP server, because it has to be switched on each time.
- A failed opener never stops a run and never ships: scene 1 falls back to today's opener plus a CHECK line.
- Everything is stored on D: (the model library and the add-on's download temp folder).

## Feasibility (throwaway probe, 2026-10-27)

Built by hand in the owner's Blender through the MCP (scene `OpenerTest_Mike`, kept for reference): a Poly Pizza
rooster (CC-BY, Poly by Google), Quaternius stump, axe and barn (CC0). 90 frames at 540x960 rendered in about
14 s with EEVEE (about a minute at full size). Library coverage: good for animals, vehicles, props and buildings;
none for people in period clothes, and Sketchfab results included non-commercial licences and fan art of
copyrighted characters.

The owner's review found these faults, in order, each now a rule or a check below:
1. The axe swung in from the side, its edge facing away from the bird.
2. The headless body's legs went through the stump when it hopped off.
3. The axe went through the bird's breast; then, stopped early, it didn't cut through the neck.
4. The cut-off piece was half the bird.
5. A dark seam showed on the neck before the axe hit (the model was split into two pieces from the start).
6. In the three-quarter view, the bird walked out of frame.

Also learned:
- A blade seen edge-on is invisible: the camera must see the tool's flat side.
- A single upright model limits a cut. A blade that kept going through this rooster's neck would hit its breast,
  so the chop stops at the cut. The owner accepted this.

## Flow in a run

1. **Start of run.** `cli.main` asks the Blender add-on for a ping over localhost:9876. If there's no answer, it
   prints the note below and waits: Enter retries, S skips. Skipping means openers only use models already in the
   library; Shorts that would need a new model fall back. Runs started with arguments (no questions) only print
   the note.
   > Blender MCP is off: new opener models can't be fetched. Open Blender, press N, click Start MCP Server, then
   > press Enter to retry (or S to skip).
2. **Opener plan, when the scripts are written.** `opener_plan.plan_openers(shorts, ch)` makes one AI call per
   batch, after the fact check. Input: each Short's final narration, the scene 1 line, and the research text.
   Output: one plan per Short (format below), checked by `opener_plan.clean_opener(raw)`. An unusable reply is
   asked for once more; still unusable, or `buildable: false`, means no Blender opener for that Short (Part 2
   will pick these up).
3. **Models.** `blender_link.fetch(plan)` resolves every `find` to a library model:
   - The library is searched first by the find text and the model's saved tags.
   - If nothing matches and Blender is on, the add-on searches Poly Pizza (CC0 / CC-BY) and Poly Haven models
     (CC0). One small AI call per missing model picks the best result from up to 10 titles (with Poly Haven
     preview images when there are any); "none fits" makes that Short fall back.
   - The download happens in a temporary scene, so the owner's open scene is never touched. The objects are
     saved to `D:\ShortsMaker\blender\assets\library\<source>_<id>.blend` with `<source>_<id>.json` (title,
     author, licence, attribution line, real-world size, tags), and the temporary scene is deleted.
   - Before downloading, the add-on's Python temp folder is pointed at `D:\ShortsMaker\cache\blender_tmp`.
   - Sketchfab is not used: its licences vary (NC/ND) and it has fan art of copyrighted characters.
   - A model that can't be found or fetched makes that Short fall back.
4. **Render, after the voice.** In `short_render.render`, scene 1's length is known from `bounds`. Then
   `opener_render.render_opener(short, bounds, work)` does the following:
   - writes `work/opener.json`;
   - runs headless `D:\Blender\blender.exe -b --factory-startup --python blender/opener_scene.py`, which builds
     the scene, applies the moves, runs the checks, renders PNG frames and writes `work/opener_report.json`;
   - joins the frames into `work/opener.mp4`.

   Scene 1 then plays that clip like real film, the same way owner clips and Blender clips are played. Captions,
   the title banner and the subscribe button stay on top.
5. **Fix rounds.** The checks fail, or the AI review fails: it looks at an 8-frame strip plus the plan and
   answers whether the action makes sense and whether frame 0 shows the subject and the threat. Either way, the
   failures go back to the AI to fix the plan, up to 2 rounds.
6. **Fallback.** Still failing: scene 1 stays as it is today (picture, film or graphic), with a
   `CHECK: opener failed: <reason>` line in edit_plan.txt. Blender missing, a crash, or a 10-minute timeout is
   retried once, then falls back the same way. The run goes on.
7. **First-second check.** `review.first_second_check` still scores a Short with a Blender opener. It never swaps
   in another scene's picture; a low score adds a CHECK line.
8. **Credits.** CC-BY models add their attribution line to upload.txt; CC0 models need none. Low-poly 3D is not
   realistic synthetic media, so it doesn't set the upload's "altered or synthetic" flag (same as the bridge
   channel).

## Opener plan format

```json
{
  "buildable": true,
  "moment": "an axe chops a rooster's head off on a stump; the headless body hops off and staggers away",
  "set": {"ground": "dirt", "backdrop": [{"find": "red barn", "size_m": 8}], "light": "day"},
  "actors": [
    {"id": "rooster", "find": "rooster", "size_m": 0.55, "on": "stump", "facing": "right"},
    {"id": "stump", "find": "tree stump", "size_m": 1.2},
    {"id": "axe", "find": "axe", "size_m": 0.8}
  ],
  "beats": [
    {"move": "cut", "tool": "axe", "target": "rooster", "at": 0.55,
     "strokes": [{"through": "neck", "angle": "level"}],
     "expect": [{"piece": "head", "share": 0.15, "then": "fly_off"}, {"piece": "rest", "then": "stay"}]},
    {"move": "hop_off", "actor": "rooster", "at": 1.3, "style": "stagger"},
    {"move": "walk", "actor": "rooster", "at": 1.8, "toward": "left", "style": "stagger"}
  ],
  "camera": {"angle": "three_quarter", "follow": "rooster"}
}
```

- `clean_opener` checks every value against tables at the top of `opener_plan.py`:
  - grounds, lights, facings, angles and moves must be in their tables;
  - `at` is in seconds and must fit inside scene 1;
  - every id a beat names must exist;
  - sizes must be 0.05-30 m.
- A `cut` beat's tool must be in the tool table, each stroke must cross the target, and `expect` must name every
  piece the strokes make (or give a count range for many small ones, e.g. `{"pieces": "40-60", "then": "scatter"}`).
- At least one beat must happen by 1.0 s. Frame 0 must show the subject and the beat's threat (tool, edge, drop,
  wave): that's the stop-the-scroll frame.

## Moves (blender/moves.py)

Each move is written once and tested; the AI only chooses moves and their timing.

| Move | What it does |
|---|---|
| `cut` | Any cut: one or many tool strokes through a target (details below). |
| `fall` | Drops under gravity onto whatever is below, with a small bounce, and comes to rest touching it. |
| `topple` | Tips over around its base edge and comes to rest lying on the ground. |
| `hop_off` | Jumps clear of what it stands on and lands beside it. |
| `walk` | Moves along the ground with a step bob; `style` is `normal` or `stagger`. |
| `fly_off` | A cut or knocked part flies off on an arc and lands resting on something. |
| `sink` | Sinks into water or mud, tilting as it goes. |
| `roll` | Rolls along the ground. |

**`cut`: one general move for every kind of cut** (owner, 2026-10-27: "be prepared for anything"). A chop, a
split, slices, dice, a mince or a shaving are all the same move with different strokes; there are no built-in
kinds and no fixed size limits.
- **Strokes.** A cut is a list of strokes; each one says where it crosses the target (a named region such as
  `neck`, or a fraction along the target's long axis) and at what angle. Many strokes can be given as a pattern:
  `{"rows": 8}` (slices), `{"rows": 6, "cols": 6}` (dice), `{"mince": 50}` (repeated strokes moving across).
- **Tool table.** The tool sets the motion and the shape it cuts:
  - axe: a chop swing, edge leading;
  - knife or cleaver: a press or slice down, or quick repeated strokes for a mince;
  - saw: back and forth, cutting a slot as wide as its blade;
  - sword: a level slash;
  - guillotine: a straight drop;
  - drill, scoop or cookie cutter: they cut their own shape out instead of a flat plane.
  The cut always follows the path the viewer sees the blade take. New tools are added as table rows.
- **How the model is split.** Straight blades split it with Blender's bisect along the stroke plane; shaped tools
  use a boolean with the tool's shape. Every cut face is filled and coloured from a small table by what the target
  is (pale for onion, light for wood, red for meat, a default otherwise), so no open holes show.
- **Stopping.** Each stroke stops at the first thing it isn't meant to cut: the rest of the body, a board, a
  block, the ground. Then it recoils or moves to the next stroke.
- **Expectations come from the plan.** The `expect` list says what the cut should produce: named pieces with
  their rough share of the target (`head` about 0.15) or a count range for many small pieces, and what each does
  afterwards (`stay`, `fall`, `tip_over`, `fly_off`, `scatter`). The check compares the real pieces with that list.
  Today's half-chicken cut fails because it doesn't match "head about 0.15"; a mince passes as long as it really
  is 40-60 small bits.
- **Two limits always apply:** every piece at least 3 mm (visible, and sane geometry) and at most 80 pieces per
  opener (render time).
- **The blade must be long enough** to cut the target in one stroke. Otherwise the plan must pick a bigger tool
  or more strokes.
- **Seam.** The untouched model is shown until the first stroke reaches it, then the pieces are swapped in.
  Splitting can leave seam lines, so pieces never appear before the cut.
- **Not cuts:** shattering, crushing, melting and tearing are separate moves, added to the move list when a story
  needs one.

## Checks (blender/opener_checks.py), run on every frame

| Check | Rule |
|---|---|
| Overlap | No two objects overlap (mesh against mesh, BVH tree); the only allowed overlap is a tool and the piece it is cutting, on the frames of that stroke |
| Resting | Anything resting or landed touches what it rests on, within 1 cm (no floating, no sinking) |
| In frame | The subject stays within 4-96% of the frame width and 3-97% of the height on every frame |
| First frame | At frame 0 the subject and the threat are both in frame, the subject at least 15% of the frame height |
| Edge leads | At contact, the tool's edge faces the way it's moving and points at the target |
| Blade face | At contact, the camera sees the blade's flat side (at least 35 degrees off edge-on) |
| Cut result | The pieces match the plan's `expect`: each named piece's share is within ±50% of planned (so 0.15 allows 0.075-0.225), counts are within the planned range, every piece is at least 3 mm, and there are at most 80 pieces |

`opener_report.json` lists every failure with its frame numbers, and those go straight into the fix-round prompt.

## Brand look (fixed in code, not chosen by the AI)

EEVEE at 1080x1920, 30 fps. AgX colour, a warm sun, a soft sky colour, depth of field on the subject (f/2.2),
50 mm lens, three-quarter camera with a slow push-in, and the camera following the subject when it moves. Models
keep their low-poly library colours. Every opener looks like part of the same channel.

## Hook-line check (small, independent)

The script editor reports `hook_kind`:
- `moment`: the first line happens inside the strangest moment;
- `summary`: it states the whole story;
- `money_claim`: weird-economics; a specific money figure tied to a person or thing the viewer can picture.

`writing.story_problems` flags `summary` on strange-history, and anything but `money_claim` on weird-economics,
so the script goes back to the editor once (the existing second pass). Both rules files' `## Story rules` get one
line each with the research examples (Voggle's Mike; How Money Works' "This man effectively created a free money
machine...").

## Files

- `shortsmaker/opener_plan.py`: plan prompt, `clean_opener`, tables.
- `shortsmaker/opener_render.py`: fetch, headless run, report, review, fix rounds, fallback.
- `shortsmaker/blender_link.py`: add-on socket client (ping, search, download to library, temp folder on D:).
- `blender/opener_scene.py`, `blender/moves.py` and `blender/opener_checks.py`: plain bpy, not imported by the
  package.
- `blender/assets/library/`: the model library (gitignored).
- `cli.py`: the Blender ping and the note at the start of a run.
- `HANDOFF.md`: a "Blender openers" section, and the note that the MCP server has to be started for new models.
- Rules files: the hook-line lines.

## Tests

- `tests/test_opener_plan.py`: `clean_opener` accepts the example and rejects bad moves, ids, timing and sizes;
  `buildable: false` falls back.
- `tests/test_blender_link.py`: a fake socket covers ping on and off, search, and download writing the
  `.blend`/`.json` pair to the library; the start-of-run note and Enter/S handling.
- `tests/test_opener_render.py`: a fake Blender covers success (scene 1 uses `opener.mp4`), check failure (fix
  round, then fallback plus CHECK line), crash (retry, then fallback), and CC-BY credits in upload.txt.
- `tests/test_opener_scene.py`: real headless Blender, a few minutes. The reference plan `chicken_chop.json`
  (today's opener) must pass every check, as must `onion_slices.json` and `onion_mince.json` (with a knife on a
  board); plus one deliberately bad plan per check, which must fail that check.
  Re-run on every change to `blender/opener_*.py` or `blender/moves.py`.
- `tests/test_story.py`: `hook_kind` flags summary hooks and missing money claims.

## Limits and open points

- People can't be shown (there are no animated period people in the libraries): Part 2.
- Moves outside the list can't be shown; the plan says `buildable: false`.
- New kinds of mistakes will appear. Each one the owner spots becomes a new check, the way this spec's checks
  came from the probe.
- Cost per opener: one planning call per batch, plus 1-3 review calls per Short; about a minute of rendering per
  try.
