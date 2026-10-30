---
type: community
members: 23
---

# scene_cues

**Members:** 23 nodes

## Members
- [[FreeTypeFont]] - code
- [[Image_2]] - code
- [[Path_14]] - code
- [[Pre-render a callout as a small transparent image (animated per frame later).]] - rationale - shortsmaker/frame_render.py
- [[Returns frame(i, t) scene i at time t with camera move and graphics applied.…]] - rationale - shortsmaker/frame_render.py
- [[Small credit label (bottom-left, CREDIT_Y) while credited material (YouTube…]] - rationale - shortsmaker/image_sources.py
- [[Tilted photo card with a white border, drop shadow and a yellow name banner.]] - rationale - shortsmaker/frame_render.py
- [[Timed extras for one scene a person card (photo `found`) when their name is…]] - rationale - shortsmaker/editplan.py
- [[True only when a video is already vertical (916-ish, 720p+); horizontal videos…]] - rationale - shortsmaker/frame_render.py
- [[True when the picture's subject would land under the top callouts (y ~180-680…]] - rationale - shortsmaker/frame_render.py
- [[credit_tag_image()]] - code - shortsmaker/image_sources.py
- [[fills_frame()]] - code - shortsmaker/frame_render.py
- [[fit_font()]] - code - shortsmaker/frame_render.py
- [[frame_maker()]] - code - shortsmaker/frame_render.py
- [[graphic_low()]] - code - shortsmaker/frame_render.py
- [[graphic_overlay()]] - code - shortsmaker/frame_render.py
- [[person_card()]] - code - shortsmaker/frame_render.py
- [[scene_cues()]] - code - shortsmaker/editplan.py
- [[test_counter_finishes_before_it_leaves()]] - code - tests/test_full_scenes.py
- [[test_graphic_card_hold_duration()]] - code - tests/test_package.py
- [[test_person_card_hold_and_exit_gap()]] - code - tests/test_package.py
- [[test_scene_hold_padding()]] - code - tests/test_package.py
- [[thumbnail()]] - code - shortsmaker/frame_render.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/scene_cues
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_gpu.py]]
- 4 edges to [[_COMMUNITY_ClipReader]]
- 4 edges to [[_COMMUNITY_plan_rules.py]]
- 4 edges to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_ffmpeg]]
- 1 edge to [[_COMMUNITY_full_cues]]
- 1 edge to [[_COMMUNITY_subprocess]]
- 1 edge to [[_COMMUNITY_image_sources.py]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]

## Top bridge nodes
- [[scene_cues()]] - degree 10, connects to 4 communities
- [[frame_maker()]] - degree 8, connects to 4 communities
- [[graphic_low()]] - degree 7, connects to 3 communities
- [[fills_frame()]] - degree 6, connects to 3 communities
- [[person_card()]] - degree 6, connects to 2 communities