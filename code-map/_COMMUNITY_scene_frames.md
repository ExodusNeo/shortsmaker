---
type: community
members: 10
---

# scene_frames

**Members:** 10 nodes

## Members
- [[(first, last) frame of every scene, 1-based and back to back; even a very short…]] - rationale - shortsmaker/blender_render.py
- [[Path_30]] - code
- [[drawn_short()]] - code - tests/test_blender_run.py
- [[get()]] - code - tests/test_blender_run.py
- [[jpeg()]] - code - tests/test_blender_run.py
- [[scene_frames()]] - code - shortsmaker/blender_render.py
- [[test_film_opener_is_skipped_and_bad_bytes_fall_back()]] - code - tests/test_blender_run.py
- [[test_no_photo_uses_a_drawing_and_says_so()]] - code - tests/test_blender_run.py
- [[test_scene_frames_cover_every_frame_once()]] - code - tests/test_blender_render.py
- [[test_thumbnail_uses_the_real_photo()]] - code - tests/test_blender_run.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/scene_frames
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY___init__.py]]
- 4 edges to [[_COMMUNITY_finish_render]]
- 3 edges to [[_COMMUNITY_test_blender_render.py]]
- 1 edge to [[_COMMUNITY_default_build]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_pathlib]]

## Top bridge nodes
- [[scene_frames()]] - degree 8, connects to 4 communities
- [[drawn_short()]] - degree 6, connects to 2 communities
- [[test_film_opener_is_skipped_and_bad_bytes_fall_back()]] - degree 4, connects to 2 communities
- [[test_no_photo_uses_a_drawing_and_says_so()]] - degree 4, connects to 2 communities
- [[test_thumbnail_uses_the_real_photo()]] - degree 4, connects to 2 communities