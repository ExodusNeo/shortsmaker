---
name: review-loop
description: Visual self-review for ShortsMaker's Remotion scenes — render a small preview, build a contact sheet, look at it, critique against a checklist, fix, repeat. Use after changing any template, skin, overlay, toolkit component or Custom scene, and before calling a visual change done.
---

# Review loop

Adapted from whaleyxbt/claude-motion (MIT, see ../LICENSE-claude-motion.txt). You can't watch the video, but you can
look at frames. Never report a visual change as done without looking at a contact sheet of the current render.

The pipeline already does this on its own for AI-coded scenes: `look_and_fix()` -> `preview_custom()` ->
`preview_sheet()` in shortsmaker/motion.py (40 % render, 8 frames tiled 4x2, one rewrite if something is wrong). Use the
same helpers by hand.

## Loop

1. Preview: `preview_sheet(props, start, end, work)` renders seconds start..end at 40 % and writes
   `work/look/sheet.jpg`. For one full-screen scene alone:
   `.venv\Scripts\python.exe tests\render_full.py remotion\test_props\<name>.json [--still SECONDS]`.
2. Open the sheet and go through the checklist.
3. Zoom in on anything suspicious: `npx remotion still src/index.ts Short still.png --props=... --frame=N` for one
   full-size frame, or a denser sheet across a transition (ffmpeg `select` + `tile`, as in `preview_sheet`).
4. Fix, `npx tsc -p .` in remotion/, back to step 1. Stop when a full pass finds nothing.
5. Final: a real `fix.bat`/run render, and look at a sheet of the finished mp4.

## Checklist

Composition
- One focal point per frame. If two things compete, one of them waits.
- Nothing overlaps unintentionally, especially mid-transition; no arrow or line crosses a card, photo or text.
- Everything on the stage, clear of the title banner, captions, credits (bottom-left) and the SUBSCRIBE button.
- Frame 0 is a strong real image.

Type
- Nothing clipped by a mask, card or the frame.
- Key message readable with the tile shrunk to phone width.
- Text isn't moving while it's meant to be read.

Timing
- Each readable state holds long enough (`motion-design` Timing). A tile mid-hold that shows text still animating
  means the hold is too short.
- Elements arrive one after another on spoken beats, not all at once.
- Overlays finish animating before they leave.

Consistency
- Only skin colors; the accent marks the point of the frame.
- The same element looks the same in every scene it appears in.

Sound (whole Short)
- Loudness -14 LUFS (`loudnorm` pass), SFX accents land on their word, no sub-bass thumps (owner dislikes them).

## Report

Say what you checked, what you fixed, and which sheet shows it. Don't claim a fix you haven't re-rendered and looked at.
