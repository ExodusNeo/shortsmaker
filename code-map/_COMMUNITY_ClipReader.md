---
type: community
members: 21
---

# ClipReader

**Members:** 21 nodes

## Members
- [[dot-__init__()_3]] - code - shortsmaker/frame_render.py
- [[dot-at()]] - code - shortsmaker/frame_render.py
- [[dot-close()]] - code - shortsmaker/frame_render.py
- [[Animate the callout in, hold it, fade it out before the scene ends.]] - rationale - shortsmaker/frame_render.py
- [[ClipReader]] - code - shortsmaker/frame_render.py
- [[Frame at fraction p (0..1) of the clip; p never goes backwards within a scene.]] - rationale - shortsmaker/frame_render.py
- [[Image]] - code
- [[One frame of slow Ken Burns motion; affine sampling is sub-pixel so it never…]] - rationale - shortsmaker/frame_render.py
- [[Pop the card in with a slight overshoot over a dimmed background, then shrink…]] - rationale - shortsmaker/frame_render.py
- [[Stream every frame to ffmpeg. Cuts in `flashes` are hard cuts under a white…]] - rationale - shortsmaker/frame_render.py
- [[Streams a clip's frames in order. Decoding a whole 1080x1920 clip up front…]] - rationale - shortsmaker/frame_render.py
- [[White camera-flash curve snaps up over the 2 frames before the cut, then…]] - rationale - shortsmaker/frame_render.py
- [[draw_card()]] - code - shortsmaker/frame_render.py
- [[draw_graphic()]] - code - shortsmaker/frame_render.py
- [[flash_alpha()]] - code - shortsmaker/frame_render.py
- [[frame()]] - code - shortsmaker/frame_render.py
- [[frame()_1]] - code - tests/test_blender_plan.py
- [[shot()]] - code - shortsmaker/frame_render.py
- [[test_hard_cuts_never_blend_scenes()]] - code - tests/test_blender_plan.py
- [[write()]] - code - tests/test_blender_plan.py
- [[write_frames()]] - code - shortsmaker/frame_render.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ClipReader
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_test_full_scenes.py]]
- 4 edges to [[_COMMUNITY_frame_maker]]
- 1 edge to [[_COMMUNITY_math]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_test_blender_plan.py]]

## Top bridge nodes
- [[write_frames()]] - degree 6, connects to 2 communities
- [[flash_alpha()]] - degree 4, connects to 2 communities
- [[ClipReader]] - degree 6, connects to 1 community
- [[frame()]] - degree 6, connects to 1 community
- [[Image]] - degree 6, connects to 1 community