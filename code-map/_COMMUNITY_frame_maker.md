---
type: community
members: 7
---

# frame_maker

**Members:** 7 nodes

## Members
- [[(style, text) for the built-in renderer, which draws only dates, places and…]] - rationale - shortsmaker/plan_rules.py
- [[Image_3]] - code
- [[Returns frame(i, t) scene i at time t with camera move and graphics applied.…]] - rationale - shortsmaker/frame_render.py
- [[Small credit label (bottom-left, CREDIT_Y) while credited material (YouTube…]] - rationale - shortsmaker/image_sources.py
- [[credit_tag_image()]] - code - shortsmaker/image_sources.py
- [[fallback_graphic()]] - code - shortsmaker/plan_rules.py
- [[frame_maker()]] - code - shortsmaker/frame_render.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/frame_maker
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_ClipReader]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_person_card]]
- 1 edge to [[_COMMUNITY_graphic_low]]

## Top bridge nodes
- [[frame_maker()]] - degree 8, connects to 5 communities
- [[credit_tag_image()]] - degree 4, connects to 1 community
- [[fallback_graphic()]] - degree 3, connects to 1 community