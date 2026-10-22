---
type: community
cohesion: 0.29
members: 7
---

# Frame Maker & Credit Tags

**Cohesion:** 0.29 - loosely connected
**Members:** 7 nodes

## Members
- [[(style, text) for the built-in renderer, which draws only dates, places and…]] - rationale - shortsmaker/plan_rules.py
- [[Image_2]] - code
- [[Returns frame(i, t) scene i at time t with camera move and graphics applied.…]] - rationale - shortsmaker/frame_render.py
- [[Small credit label (bottom-left, CREDIT_Y) while credited material (YouTube…]] - rationale - shortsmaker/image_sources.py
- [[credit_tag_image()]] - code - shortsmaker/image_sources.py
- [[fallback_graphic()]] - code - shortsmaker/plan_rules.py
- [[frame_maker()]] - code - shortsmaker/frame_render.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Frame_Maker__Credit_Tags
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Frame Overlays & Fonts]]
- 1 edge to [[_COMMUNITY_Python Frame Renderer]]
- 1 edge to [[_COMMUNITY_Subject Position Checks]]
- 1 edge to [[_COMMUNITY_CLI & Pixabay Films]]
- 1 edge to [[_COMMUNITY_Scene Cues & Image Search]]

## Top bridge nodes
- [[frame_maker()]] - degree 7, connects to 3 communities
- [[credit_tag_image()]] - degree 4, connects to 1 community
- [[fallback_graphic()]] - degree 3, connects to 1 community