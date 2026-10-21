---
type: community
cohesion: 0.08
members: 33
---

# Python Frame Renderer

**Cohesion:** 0.08 - loosely connected
**Members:** 33 nodes

## Members
- [[(style, text) for the built-in renderer, which draws only dates, places and…]] - rationale - shortsmaker/plan_rules.py
- [[dot-__init__()_5]] - code - shortsmaker/frame_render.py
- [[dot-at()]] - code - shortsmaker/frame_render.py
- [[dot-close()]] - code - shortsmaker/frame_render.py
- [[Animate the callout in, hold it, fade it out before the scene ends.]] - rationale - shortsmaker/frame_render.py
- [[ClipReader]] - code - shortsmaker/frame_render.py
- [[Frame at fraction p (0..1) of the clip; p never goes backwards within a scene.]] - rationale - shortsmaker/frame_render.py
- [[FreeTypeFont]] - code
- [[Image_1]] - code
- [[Image_2]] - code
- [[One frame of slow Ken Burns motion; affine sampling is sub-pixel so it never…]] - rationale - shortsmaker/frame_render.py
- [[Path_20]] - code
- [[Pop the card in with a slight overshoot over a dimmed background, then shrink…]] - rationale - shortsmaker/frame_render.py
- [[Pre-render a callout as a small transparent image (animated per frame later).]] - rationale - shortsmaker/frame_render.py
- [[Returns frame(i, t) scene i at time t with camera move and graphics applied.…]] - rationale - shortsmaker/frame_render.py
- [[Small credit label (bottom-left, CREDIT_Y) while credited material (YouTube…]] - rationale - shortsmaker/image_sources.py
- [[Streams a clip's frames in order. Decoding a whole 1080x1920 clip up front…]] - rationale - shortsmaker/frame_render.py
- [[Tilted photo card with a white border, drop shadow and a yellow name banner.]] - rationale - shortsmaker/frame_render.py
- [[True only when a video is already vertical (916-ish, 720p+); horizontal videos…]] - rationale - shortsmaker/frame_render.py
- [[True when the picture's subject would land under the top callouts (y ~180-680…]] - rationale - shortsmaker/frame_render.py
- [[credit_tag_image()]] - code - shortsmaker/image_sources.py
- [[draw_card()]] - code - shortsmaker/frame_render.py
- [[draw_graphic()]] - code - shortsmaker/frame_render.py
- [[fallback_graphic()]] - code - shortsmaker/plan_rules.py
- [[fills_frame()]] - code - shortsmaker/frame_render.py
- [[fit_font()]] - code - shortsmaker/frame_render.py
- [[frame()]] - code - shortsmaker/frame_render.py
- [[frame_maker()]] - code - shortsmaker/frame_render.py
- [[graphic_low()]] - code - shortsmaker/frame_render.py
- [[graphic_overlay()]] - code - shortsmaker/frame_render.py
- [[person_card()]] - code - shortsmaker/frame_render.py
- [[shot()]] - code - shortsmaker/frame_render.py
- [[thumbnail()]] - code - shortsmaker/frame_render.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Python_Frame_Renderer
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_Channel Profiles & CLI]]
- 3 edges to [[_COMMUNITY_Story Sounds & Credits]]
- 2 edges to [[_COMMUNITY_Footage Downloads & Crops]]
- 1 edge to [[_COMMUNITY_Local AI Jobs & Clips]]
- 1 edge to [[_COMMUNITY_Scene Cues & Word Timing]]
- 1 edge to [[_COMMUNITY_SFX Synthesis]]
- 1 edge to [[_COMMUNITY_Motion Previews & Render Tests]]

## Top bridge nodes
- [[fills_frame()]] - degree 6, connects to 3 communities
- [[person_card()]] - degree 6, connects to 3 communities
- [[frame_maker()]] - degree 8, connects to 2 communities
- [[graphic_low()]] - degree 5, connects to 2 communities
- [[thumbnail()]] - degree 4, connects to 2 communities