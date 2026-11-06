---
type: community
members: 5
---

# write_frames

**Members:** 5 nodes

## Members
- [[Stream every frame to ffmpeg. Cuts in `flashes` are hard cuts under a white…]] - rationale - shortsmaker/frame_render.py
- [[frame()_2]] - code - tests/test_blender_plan.py
- [[test_hard_cuts_never_blend_scenes()]] - code - tests/test_blender_plan.py
- [[write()_1]] - code - tests/test_blender_plan.py
- [[write_frames()]] - code - shortsmaker/frame_render.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/write_frames
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_ClipReader]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_audio_library.py]]
- 1 edge to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_test_blender_plan.py]]

## Top bridge nodes
- [[write_frames()]] - degree 6, connects to 4 communities
- [[test_hard_cuts_never_blend_scenes()]] - degree 4, connects to 1 community