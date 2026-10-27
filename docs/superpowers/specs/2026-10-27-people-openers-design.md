# People openers (Blender openers, part 2) — design

Date: 2026-10-27. Status: approved in chat section by section, awaiting the owner's review of this file.
Part 2 of 2. Part 1: `2026-10-27-blender-openers-design.md` (built; polished on Mike the Headless Chicken).

## Why

Every Short should open on an animation of its strangest moment (Part 1's brief). Part 1 can't show people: the
model libraries have no animated people, so the planner answers `buildable: false` and those Shorts keep today's
scene 1. Many strange-history and weird-economics stories are about a person (Digby Tatham-Warter walking into
fire with an umbrella), so most Shorts get no opener yet.

## Decisions made in chat (owner, 2026-10-27)

- Look: 2D cartoon people acting out the moment (Simple History was the reference), not an animated photo or an
  AI-coded one-off scene.
- Identity: era + role costume from a fixed wardrobe plus a signature prop. No faces or likenesses.
- Build: approach A, in Blender: Quaternius rigged, animated low-poly people with their real animation clips,
  cel-shaded with ink outlines so they read as 2D. Chosen over hand-made 2D puppets (Kenney parts in Remotion)
  because the hard part is motion, and hand-keyed motion is what made the first rooster stiff.
- The cel-shaded, outlined look applies to every opener (people, animals, props, set): one brand look.
- Everything else from Part 1 stays: the AI only writes a plan from tables, our code builds it, the checks and
  fix rounds catch bad plans, the AI review judges 8 frames, a failed opener never ships.

## Assets and licence

- Bodies: Quaternius Ultimate Animated Character Pack (50+ rigged characters). Clips: Quaternius Universal
  Animation Library (1 and 2), one shared skeleton. Licence: older releases CC0, newer the Quaternius Asset
  Licence: free commercial use, no attribution required, but the files may not be redistributed as a pack. So they
  live only in `D:\ShortsMaker\blender\assets\people\` (gitignored) and never in git, tests included.
- Getting them: the build tries to download them itself; if the site needs a click-through, the owner downloads
  the two packs once into that folder (links given then).
- `blender/pack_people.py` (one-time, headless) packs them into `people.blend` (every body; every clip as a named
  action) and `people.json` (bodies, material slots per body, bone names for head and right hand, clips with
  lengths and whether they loop, stride length per locomotion clip). A run never needs the internet or the
  owner's Blender window for people.
- Hats, helmets and props: Poly Pizza through the existing `blender_link` fetch (CC0 / CC-BY, credits in
  upload.txt as today). A wardrobe item that is only a colour needs no model.

## Tables (`blender/opener_tables.json`)

- `roles`: about 20 to start, e.g. `ww2_british_officer`, `ww1_soldier`, `victorian_gentleman`, `victorian_lady`,
  `sailor`, `pirate`, `farmer`, `scientist`, `medieval_knight`, `roman_soldier`, `cowboy`, `businessman`,
  `worker`, `king`, `queen`, `monk`, plus generic `man`, `woman`, `child`. Each: base body, colours by clothing
  slot (tunic, trousers, boots, hair), optional `hat` find text, height in metres. A new role is a new row.
- `people_moves`: move name -> Quaternius clip name, kind (`in_place` or `travel`), and for travel the clip's
  stride. Moves: walk, run, stagger, crawl (travel); fall, die, flinch, point, wave, sit, kneel, raise_prop,
  swing_prop, throw_prop, drop_prop (in place).
- The AI picks only from these lists; a person who fits no role gets the closest one or a generic role.

## Plan format (additions)

An actor may be a person: `{"id": "officer", "person": "ww2_british_officer", "prop": "umbrella",
"facing": "right"}` (`prop` is a find text; `size_m` comes from the role's height). Beats use the people moves
with the same fields as Part 1 (`actor`, `at`, `toward`, `ends`). `clean_opener` accepts a person actor only with a
role from the table and moves from `people_moves` for people (Part 1's moves stay for everything else);
`buildable: false` is left only for moments even people can't show (crowds, a building falling on a city).

## Building a person (`blender/people.py`, beside `moves.py`)

- Dress: copy the role's body and skeleton from `people.blend`; set the clothing colours per material slot; fix
  the hat to the head bone and the prop to the right-hand bone (child-of, transforms applied). Scale to the
  role's height; place with `stand_on` like any actor (a person on a stage or a cart needs no extra code).
- In-place moves play their clip from the beat's time (NLA strip). Travel moves play the looping clip while the
  person is moved across the ground at the clip's stride speed (feet don't slide), turning to the way it walks and
  stopping short of obstacles like Part 1's walk. Clips blend over 4 frames; a person holds the last pose of their
  last clip.
- Prop actions: swing_prop = the clip with the prop in the hand; the prop counts as a tool for the blade-face and
  edge checks when it is a blade. throw_prop / drop_prop release the prop to physics with Part 1's `release`.
- Facings and directions are as seen in the shot (Part 1's `VIEW_YAW`), the camera follows the subject, the
  staging check applies to people (no walking "away" or "camera").

## Checks (`opener_checks.py`)

Part 1's checks apply to people unchanged: overlap (a person may overlap only their own hat and prop), resting
(feet on the ground or support at the end), in frame, hidden, first frame (subject >= 15% + the threat), staging,
blade face / edge leads for swung blades. The first frame must show the person's prop when the plan names one.

## Brand look (all openers)

- One cel shader for every material: the model's colour or texture in 2-3 flat light bands (Shader to RGB +
  constant colour ramp, EEVEE).
- Ink outlines: an inverted-hull shell (Solidify, flipped normals, back faces only, dark material) per mesh, its
  thickness scaled to the object's size; nothing added after the checks gets one twice.
- Sky and sun stay as now; the ground is banded too. The rooster openers are re-rendered and looked at by eye.

## Planner, rules, review

- `opener_plan.py`: the prompt lists the roles, the people moves and one people example (the umbrella officer
  walking calmly across the frame while explosions go off behind him).
- Both channels' `## Opener` rules: drop "it can't show people"; add people staging (side view, cross the frame,
  the prop visible in frame 0, no more than 3 people).
- The existing AI review of 8 frames judges by those rules. No new review step.

## Rollout

Both `opener: blender` channels (strange-history, weird-economics) get people openers automatically.
engineering-failures (`visuals: blender`) is untouched. A failed opener falls back to today's scene 1 with a CHECK
line, as now.

## Testing

1. Committed fixtures with a stand-in person (primitive shapes on a small skeleton, built by the test, so no
   Quaternius file is in git): a walk across, a fall, a prop swing, a person on a support. Each passes the checks.
2. When the people library is present on D: (skipped with a note otherwise): a contact sheet of every role
   standing, and every move, looked at by eye.
3. End to end: an opener for the umbrella Short (`output/strange-history/2026-10-26_why-a-ww2-officer-carried-an-umbrella`).
4. The Mike opener re-rendered in the new look, looked at by eye.
5. Existing opener suites stay green.

## Out of scope

Faces and likenesses, crowds (more than 3 people), lip-sync and dialogue, people in engineering-failures.
