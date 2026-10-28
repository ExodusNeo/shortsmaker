---
type: community
members: 13
---

# ClipReader

**Members:** 13 nodes

## Members
- [[dot-at()]] - code - shortsmaker/frame_render.py
- [[dot-close()]] - code - shortsmaker/frame_render.py
- [[Animate the callout in, hold it, fade it out before the scene ends.]] - rationale - shortsmaker/frame_render.py
- [[ClipReader]] - code - shortsmaker/frame_render.py
- [[Frame at fraction p (0..1) of the clip; p never goes backwards within a scene.]] - rationale - shortsmaker/frame_render.py
- [[Image_2]] - code
- [[One frame of slow Ken Burns motion; affine sampling is sub-pixel so it never…]] - rationale - shortsmaker/frame_render.py
- [[Pop the card in with a slight overshoot over a dimmed background, then shrink…]] - rationale - shortsmaker/frame_render.py
- [[Streams a clip's frames in order. Decoding a whole 1080x1920 clip up front…]] - rationale - shortsmaker/frame_render.py
- [[draw_card()]] - code - shortsmaker/frame_render.py
- [[draw_graphic()]] - code - shortsmaker/frame_render.py
- [[frame()]] - code - shortsmaker/frame_render.py
- [[shot()]] - code - shortsmaker/frame_render.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ClipReader
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_frame_maker]]
- 2 edges to [[_COMMUNITY_person_card]]
- 1 edge to [[_COMMUNITY_write_frames]]

## Top bridge nodes
- [[ClipReader]] - degree 6, connects to 2 communities
- [[frame()]] - degree 6, connects to 2 communities
- [[Image_2]] - degree 6, connects to 1 community
- [[draw_card()]] - degree 4, connects to 1 community
- [[draw_graphic()]] - degree 4, connects to 1 community