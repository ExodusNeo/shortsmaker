# Full-screen motion graphic scenes: design

Date: 2026-10-17. Status: approved in conversation, waiting for the owner's review of this document.

## Goal
Whole-scene motion graphics that can replace weak b-roll, not only the overlays (callouts, cards, small map)
the Shorts already have. They must look good: a documentary feel that sits with real archival footage.

## Decisions (owner)
- Four scene types in the first batch: evidence board, map journey, big number, paper & documents.
- Use: planned by the AI (max 2 per Short) **and** rescue for weak footage; max 3 per Short in total.
- Look: style A "Archival documentary" (aged paper, ink, serif type, film grain, vignette). Applies to
  `strange-history`. The `gaming` channel is out of scope for now (it would get the dark modern style B later).
- Build: hand-built Remotion templates; the AI only fills in data. Not AI-written animation code, not stock packs.

## Shared look (`remotion/src/Paper.tsx`)
- Background: aged-paper texture made once by the program (Pillow noise + fibres, stored in
  `remotion/public/paper/`), drifting slowly; film grain (a few pre-made grain frames cycled), dark-brown vignette.
- Ink: dark brown `#2c1f0e` text and lines, red ink `#7a1d12` for routes, thread and underlines, the Short's
  palette accent for one highlight per scene.
- Type: a free OFL book serif in `remotion/public/fonts`, loaded with `FontFace` from `staticFile` (no network).
- Camera: slow drift/push across the scene; each scene picks one of several camera paths/layouts
  (seeded by scene index) so Shorts don't look identical.
- Timing: elements land on spoken words (the existing word timings), like current graphics.
- Captions, subscribe button, credit tags and the hook title still draw on top.

## The four scenes
Each is a `full` object on the scene: `{"type": ..., ...}`.

1. **Evidence board** (`type: "board"`): 3-5 real photos from the Short's picture pool pinned as aged prints on
   a dark board, each with a typed label (<= 3 words). Camera glides print to print as each is named; a red
   thread draws between linked prints. Data: `items: [{"label": "...", "word": "...", "find": "<what the photo
   should show>"}]`, `links: [[a, b], ...]`. The director plans items before pictures exist; the picture chooser
   fills each item's `picture` from the pool (same contact sheets, same rules). Real photos only (no AI faces).
   Needs >= 3 items with pictures or the scene falls back to the normal picture path.
2. **Map journey** (`type: "journey"`): full-screen old-atlas map from `world-atlas/countries-10m.json` with
   d3-geo. Camera starts on the country, pushes to the region; up to 4 places pinned with ink labels as they are
   named; dashed red route draws between them in order; optional note ("1881 · 32 km").
   Data: `stops: [{"name", "lat", "lon", "word"}]` (1-4), `note`.
3. **Big number** (`type: "number"`): a large number counts up, then a field of small ink figures fills in
   (`each` = what one figure stands for), or two bars for a comparison. Figures drawn in code: person, coin,
   ship, house, train, soldier, animal, day. Data: `value`, `label`, `icon`, `each`, optional
   `compare: {"a_label", "a_value", "b_label", "b_value"}`.
4. **Paper & documents** (`type: "document"`): full-screen newspaper page, letter, telegram or official form;
   camera pushes in and the key line is underlined in red ink as it is spoken. Uses a real scan from the pool
   when the picker found one (`picture`); otherwise typeset: only the key line is readable, the rest are faded
   filler lines (never invented article text). Data: `kind`, `key_line`, `date`, `paper` (only a real paper that
   covered it, same rule as the headline card), optional `find` (the picture chooser may attach a real scan of
   that document as `picture`).

## When they are used
- **Planned:** `direct_scripts()` may give a scene `full` where a graphic shows the moment better than any
  picture (a trip between places, a hard-to-picture number, a document that matters, several things connecting).
  Rules: never scene 1 (real footage keeps the hook), never two in a row, max 2 planned.
- **Rescue 1, picture choosing:** when the picker finds no fitting picture for a scene, a small AI call
  (`rescue_graphics()`) gets those scenes, the Wikipedia research and the pool, and returns `full` for scenes whose
  line suits one; the rest get an AI painting as today. Order: real footage/photo -> motion graphic -> painting.
- **Rescue 2, review:** `visual_review()` answers per flagged scene `fix: "repaint" | "graphic"`. Graphic fixes
  go through `rescue_graphics()`; both kinds share the existing single automatic re-render (`AUTO_REPAINT_MAX`).
- **Caps:** max 3 `full` scenes per Short in total; a `full` scene drops that scene's overlay graphic and
  person card.
- **Fact check:** `fact_check()` also checks `full` data (places, numbers, labels, key line) against the
  Wikipedia text; an unsupported item is removed, and a `full` left without enough data is dropped.
- **Validation:** `clean_scene_graphic()` (like `clean_graphic()`) checks types, ranges, coordinates, word
  limits and that the trigger words are spoken; anything invalid is dropped, never crashes the render.
- **fix.bat option 5:** "Turn this scene into a motion graphic" (calls `rescue_graphics()` for that scene).
- **edit_plan.txt:** `MOTION GRAPHIC: map journey: Port Elizabeth -> Uitenhage, 1881` with planned/rescued.

## Rendering, sound, fallback
- A Short with any `full` scene always renders with Remotion; `render_remotion()` copies board/document pictures
  into `public/job` and passes `full` per scene; `Short.tsx` `Background` draws the scene component instead of
  the picture.
- Sound: `sfx_events()` adds pin (pins/prints), ticks (counting), stamp (document arrives) and a new synthesized
  "pen scratch" (underline, route), high-passed at 220 Hz like all SFX.
- Fallback: if Remotion fails, `full` scenes get an AI painting (existing painting path) and the Python renderer
  runs; edit_plan.txt says so.
- `state.json` keeps `full`, so fix.bat re-renders keep the graphics.

## Out of scope
Gaming channel style B; more scene types; AI-written animation code; stock template packs.

## Testing
1. Each scene type rendered standalone with real data (Jack route, Norton 30,000, a board of real photos, a
   telegram); frames reviewed by Claude and short clips shown to the owner before pipeline work. Owner may
   reject a type.
2. Prompt tests with monkeypatched `ask_ai` (no AI usage): director rules, caps, rescue, fact check, validation.
3. `npx tsc -p .` and `py_compile`.
4. One full real Short, reviewed at 1 frame/s plus edit_plan.txt.
Never test while a batch is running (shared `remotion/public/job`).
