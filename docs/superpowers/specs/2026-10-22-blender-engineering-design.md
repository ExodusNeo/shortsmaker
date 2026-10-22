# Blender visuals for the engineering-failures channel — design

Date: 2026-10-22. Status: approved in chat (sections 1-3), awaiting the owner's review of this file.
Project 2 of 2; project 1 (per-channel rules files) is built and merged.

## Why

The owner wants an engineering-failures channel drawn, not photographed: structures assembling piece by piece
and the camera zooming in to the part that failed. Research (vidIQ, 2026-10-22) found story-style engineering
failure Shorts doing well on small channels (MechDisk 2.4M / 1.1M, Machines That Never Sleep ~48k at 3k subs).
The owner chose Blender 3D (installed at `D:\Blender`, 5.2.1 LTS) as the default renderer for that channel.

## Decisions made in chat

- Look: "ink manual" — dark ink outlines, flat muted colours, paper-coloured sky, the failing part red.
- Model source: a parts kit built in code + an AI-written JSON build plan per Short (the AI never writes Blender
  code).
- Mix: about 70-80% Blender scenes; real archival photos only as evidence scenes (e.g. the real collapse photo).
- Launch scope: bridges only. Dams, buildings, machines later.
- Failure kinds at launch: crack, bend/buckle, fastener shear, sway/twist; any can end in a span collapse.
- Fasteners are era-correct: rivet, bolt (with nut), pin, weld — never screws.

## Feasibility (throwaway probe, 2026-10-22)

Headless `blender.exe -b --factory-startup` with EEVEE, Freestyle lines, emission-only flat materials and a
paper world colour rendered a 1080x1920 truss bridge in the target look at about 0.7 s per frame (30 frames in
21 s) on the owner's PC; parts dropping in by keyframes worked. A 40-second Short's Blender share (~900 frames)
takes about 8-11 minutes. Blender 5.2 no longer writes video directly (`FFMPEG` file format is gone): frames are
rendered as PNG and joined with ffmpeg. `scene.render.engine` reports only `BLENDER_EEVEE`.

## Flow in a run (visuals: blender channels only)

Unchanged: topics, research, writer, editor, director, fact check, voice, captions, music, sound design,
overlays, credits, upload text, review.

1. **Engineer step** — `blender_plan.plan_builds(shorts, ch)`, one AI call per batch, after the fact check
   inside `writing.write_scripts` (only when `session.RULE_SETTINGS["visuals"] == "blender"`). Input: each Short's
   final narration, research text and picture list. Output: a build plan per Short (format below), checked by
   `blender_plan.clean_build(raw, n_scenes) -> dict | None`. Its instructions come from the channel's
   `## Build plan` rules section. Blender scenes get `sc["full"] = None` (no Remotion full-screen graphic on
   them); their director-planned `ai_image` stays as the fallback.
2. **Pictures** — unchanged picker. Photo-beat scenes use what it picks; Blender scenes ignore it.
3. **Rendering** — in `short_render.render`, after the voice sets `bounds`, `blender_render.render_clips(short,
   bounds, work) -> dict[int, Path]` renders the Blender scenes; the result is merged into the `clips` dict from
   `gpu.local_clips`, so Remotion and the Python renderer treat them like real film (captions, overlays,
   subscribe button on top).
4. **Fallback** — no usable build plan, Blender missing, a crash, or a 30-minute timeout: those scenes render as
   today (the director's AI painting or picked photo), and `edit_plan.txt` gets a `CHECK:` line naming the reason.
5. **Review** — `review.visual_review` is told which scenes are drawn on purpose so it doesn't flag them as
   "not a real photo" or "AI-looking".

## Rules file

- `visuals: blender` becomes valid (the "not built yet" stop is removed).
- New section `## Build plan`, required only when `visuals: blender`: the engineer's instructions (templates,
  parts, failure kinds, beats, fastener eras, labels, how many scenes are photos). Missing → the usual
  `has no "## Build plan" section` stop. `draft_rules` lists it for blender channels.
- The engineering channel's profile moves from `channel_ideas/` to `channels/`; its rules are drafted by
  `require_rules`, then the owner sets `visuals: blender`, `min_real_pictures: 2`, `status: ready`.

## Build plan format

```json
{"structure": {"template": "truss_bridge", "truss": "warren", "spans": 3, "span_m": 140, "height_m": 18,
               "width_m": 20, "deck": "road", "setting": "river", "fastener": "rivet"},
 "focus": {"part": "gusset_plate", "at": {"span": 2, "panel": 3, "chord": "bottom", "side": "left"},
           "label": "GUSSET PLATE U10 · 1/2 INCH"},
 "failure": {"kind": "bend", "then": "collapse_span", "span": 2},
 "scale": ["car", "people"],
 "scenes": [{"scene": 1, "beat": "failure_preview"}, {"scene": 2, "beat": "wide"}, {"scene": 3, "beat": "build"}]}
```

Allowed values (anything else is replaced by the default in brackets, or dropped):
- `template`: `truss_bridge` [default], `girder_bridge`, `suspension_bridge`, `cable_stayed_bridge`,
  `eyebar_chain_bridge`.
- `truss`: `warren` [default], `pratt`, `howe`, `k`. `spans` 1-5 [1]. `span_m` 20-1300 [100]. `height_m` 2-250
  [15]. `width_m` 4-60 [15]. `deck`: `road` [default], `rail`. `setting`: `river` [default], `valley`, `bay`.
- `fastener`: `rivet` [default], `bolt`, `pin`, `weld`.
- `focus.part`: `gusset_plate` [default], `chord`, `diagonal`, `vertical`, `eyebar`, `pin_joint`, `hanger`,
  `cable`, `bearing`, `pier`, `fastener_group`. `at` fields clamped to the template's real range.
  `label` ≤ 40 characters, upper-cased, or null.
- `failure.kind`: `crack`, `bend` [default], `shear`, `sway`. `then`: `none` [default], `collapse_span`.
- `scale`: subset of `car`, `train`, `people` (people only small, never shown hurt).
- `scenes[].beat`: `wide`, `orbit`, `build`, `zoom`, `failure`, `aftermath`, `failure_preview`, `photo`.
  Scenes not listed default to `photo`. At least 1 and at most 30% of scenes are `photo`; if fewer than half of
  all scenes are Blender beats the plan is dropped (the Short is made as a photo Short).
- The whole plan is dropped (fallback) when it isn't a dict or has no usable `scenes`.

## Parts kit and scene building (Blender side, `blender/`)

Plain Blender Python run headless; not imported by the package.
- `look.py`: render settings (EEVEE, 1080x1920, 30 fps, Freestyle ink lines), flat emission materials (paper sky
  `#EEE8DC`, steel `#9EA8B3`, concrete `#E3DCCD`, water `#C3D7E5`, failure red `#D81F1A`), label font.
- `parts.py`: one function per part — deck, i_girder, truss_member, gusset_plate, fastener(kind: rivet | bolt |
  pin | weld), eyebar, main_cable, hanger, tower, pier, abutment, bearing, water, valley, car, train, person.
- `templates.py`: one function per template, building named parts with predictable names
  (`span2_panel3_bottom_left_gusset`) and returning them grouped by assembly stage (piers, deck, members,
  details).
- `build_scene.py`: entry point. Reads `build.json` (plan + scene start/end seconds), builds the template, adds
  focus detail (fastener group at the focus, red material, drawn label: leader line + upper-case text),
  keyframes the beats, renders only frames inside Blender scenes as PNG to `work/blender_frames/`.
- Beats: `wide` (whole structure), `orbit` (slow turn), `build` (parts arrive in stage order, spread over all
  build scenes), `zoom` (push in to the focus; detail and label fade in), `failure` (the failure animates, its
  peak on the scene's emphasis word time), `aftermath` (pull back to the result), `failure_preview` (the failure
  for the hook, then the next scene starts the story from the beginning), `photo` (not rendered).
- Failure animations on the focus part: `crack` (a red crack curve grows), `bend` (the part deforms by a bend
  modifier), `shear` (fasteners pop out and the joint slips; pin pulls out of a cracked eyebar; weld seam opens),
  `sway` (deck sways/twists with growing amplitude). `collapse_span` makes that span's parts fall into the water.
- The camera moves continuously within a run of consecutive Blender scenes; a cut happens at photo scenes and
  after `failure_preview`.

## Python side (`shortsmaker/`)

- `blender_plan.py`: `plan_builds(shorts, ch) -> None` (sets `s["build"]`), `clean_build(raw, n_scenes) -> dict |
  None`, the allowed-value tables.
- `blender_render.py`: `render_clips(short, bounds, work) -> dict[int, Path]` (writes `build.json`, runs Blender
  with a 30-minute timeout, joins frames per scene with ffmpeg into `work/blender{i}.mp4`, reuses frames when
  `build.json` is unchanged), `blender_exe() -> Path | None` (`config.BLENDER = Path(r"D:\Blender\blender.exe")`).
- `short_render.render`: merge `render_clips` into `clips`; CHECK line on fallback; sources line per Blender scene
  ("drawn in Blender: <beat>").
- `review.visual_review`: Blender scenes listed as drawn on purpose.
- `rules.py`: `visuals: blender` allowed; `## Build plan` required for it.

## Testing

- Python (no Blender, no AI): `clean_build` (every field: bad values replaced or dropped, photo-share and
  Blender-share limits, missing scenes), beat timing math (frame ranges from bounds, failure peak on the emphasis
  word), clip cutting, cache reuse, fallback with Blender faked to fail / time out / be missing, the
  `## Build plan` requirement, `visuals: blender` accepted.
- Blender (real headless Blender, seconds): a tiny fixed plan renders 3 frames per beat; frames exist; the zoom
  frame contains failure-red pixels and label (dark text) pixels; a `photo` beat renders no frames.
- Visual check before the first real Short: render a sample Short's key frames, look at them, show the owner.
- Existing tests keep passing; strange-history's golden prompts stay identical (photo channels untouched).

## Out of scope

Dams, buildings and machines; non-bridge templates; sound design changes; Remotion scenes on Blender scenes;
automatic uploads.
