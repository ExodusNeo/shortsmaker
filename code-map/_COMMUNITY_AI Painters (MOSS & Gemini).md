---
type: community
cohesion: 0.14
members: 14
---

# AI Painters (MOSS & Gemini)

**Cohesion:** 0.14 - loosely connected
**Members:** 14 nodes

## Members
- [[Comfy-Org's official MOSS-Image text-to-image template (25 steps, CFG 2.5,…]] - rationale - make_shorts.py
- [[Fill the 916 frame with the picture (centre crop) for the slow zoompan. This…]] - rationale - make_shorts.py
- [[Paint on this PC with MOSS-Image in ComfyUI (owner's pick 2026-10-20 over SDXL-…]] - rationale - make_shorts.py
- [[Paint the AI images with Gemini (agy's built-in image generator, ~2 min each, 3…]] - rationale - make_shorts.py
- [[Remotion failed the full-screen motion graphic scenes get a painted picture…]] - rationale - make_shorts.py
- [[comfy_call()]] - code - make_shorts.py
- [[fake_gemini()]] - code - tests/test_full_scenes.py
- [[fake_moss()]] - code - tests/test_full_scenes.py
- [[gemini_images()]] - code - make_shorts.py
- [[moss_graph()]] - code - make_shorts.py
- [[moss_images()]] - code - make_shorts.py
- [[paint_instead()]] - code - make_shorts.py
- [[test_remotion_failure_paints()]] - code - tests/test_full_scenes.py
- [[to_vertical()]] - code - make_shorts.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/AI_Painters_MOSS__Gemini
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Shared Imports & Downloads]]
- 4 edges to [[_COMMUNITY_Quality Checks & Captions]]
- 4 edges to [[_COMMUNITY_State & Logbook Helpers]]
- 1 edge to [[_COMMUNITY_AI Planner Calls & Quota]]
- 1 edge to [[_COMMUNITY_Voice Pipeline (VoiceStudio)]]
- 1 edge to [[_COMMUNITY_Full-Scene Validation]]

## Top bridge nodes
- [[paint_instead()]] - degree 9, connects to 4 communities
- [[gemini_images()]] - degree 6, connects to 4 communities
- [[moss_images()]] - degree 7, connects to 3 communities
- [[to_vertical()]] - degree 5, connects to 3 communities
- [[test_remotion_failure_paints()]] - degree 4, connects to 1 community