---
type: community
members: 6
---

# person_card

**Members:** 6 nodes

## Members
- [[FreeTypeFont]] - code
- [[Pre-render a callout as a small transparent image (animated per frame later).]] - rationale - shortsmaker/frame_render.py
- [[Tilted photo card with a white border, drop shadow and a yellow name banner.]] - rationale - shortsmaker/frame_render.py
- [[fit_font()]] - code - shortsmaker/frame_render.py
- [[graphic_overlay()]] - code - shortsmaker/frame_render.py
- [[person_card()]] - code - shortsmaker/frame_render.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/person_card
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_ClipReader]]
- 1 edge to [[_COMMUNITY_frame_maker]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_scene_cues]]

## Top bridge nodes
- [[person_card()]] - degree 6, connects to 3 communities
- [[graphic_overlay()]] - degree 5, connects to 3 communities
- [[fit_font()]] - degree 5, connects to 2 communities