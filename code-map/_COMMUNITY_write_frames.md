---
type: community
members: 7
---

# write_frames

**Members:** 7 nodes

## Members
- [[Stream every frame to ffmpeg. Cuts in `flashes` are hard cuts under a white…]] - rationale - shortsmaker/frame_render.py
- [[White camera-flash curve snaps up over the 2 frames before the cut, then…]] - rationale - shortsmaker/frame_render.py
- [[flash_alpha()]] - code - shortsmaker/frame_render.py
- [[frame()_1]] - code - tests/test_blender_plan.py
- [[test_hard_cuts_never_blend_scenes()]] - code - tests/test_blender_plan.py
- [[write()]] - code - tests/test_blender_plan.py
- [[write_frames()]] - code - shortsmaker/frame_render.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/write_frames
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_frame_render.py]]
- 1 edge to [[_COMMUNITY_ClipReader]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_math]]
- 1 edge to [[_COMMUNITY_test_blender_plan.py]]

## Top bridge nodes
- [[write_frames()]] - degree 6, connects to 3 communities
- [[flash_alpha()]] - degree 4, connects to 2 communities
- [[test_hard_cuts_never_blend_scenes()]] - degree 4, connects to 1 community