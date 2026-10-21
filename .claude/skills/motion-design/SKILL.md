---
name: motion-design
description: Taste rules for ShortsMaker's Remotion motion graphics (remotion/src/full templates, skins, toolkit, AI-coded Custom scenes) — easing, springs, timing, holds, type, color, focal points, with concrete numbers. Use when creating, animating, retiming or polishing any Remotion scene, template, overlay or transition in this repo.
---

# Motion design

Adapted from whaleyxbt/claude-motion (MIT, see ../LICENSE-claude-motion.txt) for 1080x1920 Shorts. Remotion's own
skills (remotion/.agents/skills) teach the API; this is the taste. Treat the numbers as defaults you leave on purpose.

The pipeline's AI coder gets a condensed copy of these rules as rule 9 of `custom_rules()` in shortsmaker/motion.py. Keep
the two in step when you change one.

## Time

- Everything is a pure function of `t` (seconds). No CSS transition/animation/@keyframes, no `Math.random()` (use
  `rng`), no `Date`: they flicker or drift at render time.
- Elements appear on spoken beats (`cueAt(full, i, start, end, n)`, word timings in `cue`), never on typed numbers.
  Offsets from a beat (`at + 0.05`) are fine.

## Easing (Remotion `Easing.bezier`)

| Curve | Use |
|---|---|
| `bezier(0.16, 1, 0.3, 1)` | arrivals, reveals |
| `bezier(0.6, 0, 0.9, 0.35)` | exits: leave fast, don't linger |
| `bezier(0.65, 0, 0.35, 1)` | moves between two states (camera push, dock, morph) |
| `bezier(0.55, 0, 0.2, 1.12)` | a value that lands with a small overshoot (counter, gauge) |

Linear only for continuous motion: drift, rotation, grain, ticking hands.

## Springs

| Feel | damping / stiffness / mass | For |
|---|---|---|
| settle | 14 / 140 / 0.8 | cards, panels entering |
| heavy, calm | 15–20 / 140–240 / 0.6–1 | big documents, maps |
| notch | 12 / 190 / 0.75 | a dial or pin snapping into place |
| pop | 9–11 / 200–230 / 0.7 | stamps, callouts, badges |
| elastic accent | 8 / 200 | one hero moment per Short, not more |

Springs for physical things (cards, photos, stamps). Bezier tweens for type and camera moves.

## Timing

- Stagger words ~0.09 s, list items/cards ~0.2–0.25 s, dots/pins ~0.06 s.
- Exits take about half an entrance and use the exit curve.
- Overlap: the next element starts before the last one fully settles. Hard gaps read as "loading".
- Reading holds: text must settle, then hold >= 1 s for a short phrase, +0.25 s per word past three. Scenes are ~3 s,
  so a scene carries one idea and few words; when in doubt, hold longer and animate less.
- Movement across the stage uses `travel()` (never faster than MIN_MOVE, 0.9 s).

## Type and color

- Display type big with tight tracking; one accent word per line carries the point.
- Small mono/uppercase labels are decoration; anything the viewer must read goes big. Phone test on the contact sheet.
- Colors come from the skin (`skinOf(full.skin)`); don't add hex values. The accent means something (the answer, the
  twist, the number); if everything is accent, nothing is.

## Texture and continuity

- Nothing dead-still: `Paper` grain/drift, a ticking clock, slow breathing on idle elements. Text being read stays put.
- Prefer one persistent object that changes role over cuts; a transition is motivated by something on screen.
- One hero moment per Short. Build to it; don't spend it in scene 1.

## Anti-patterns

- Everything fading in at once, or everything with the same duration.
- Linear easing on anything that starts or stops.
- Text moving while it's meant to be read.
- More than one focal point per frame.
- Anything outside the stage (x 110..970, y 260..1020 for full scenes) or under the captions/title banner.
- A weak or empty first frame: Shorts autoplay and frame 0 is the first impression.

When done, run the `review-loop` skill.
