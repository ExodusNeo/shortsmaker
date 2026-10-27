---
type: community
members: 10
---

# moss_images

**Members:** 10 nodes

## Members
- [[Comfy-Org's official MOSS-Image text-to-image template (25 steps, CFG 2.5,…]] - rationale - shortsmaker/gpu.py
- [[Paint on this PC with MOSS-Image in ComfyUI (owner's pick 2026-10-20 over SDXL-…]] - rationale - shortsmaker/gpu.py
- [[Remotion failed the full-screen motion graphic scenes get a painted picture…]] - rationale - shortsmaker/remotion_render.py
- [[comfy_call()]] - code - shortsmaker/gpu.py
- [[fake_gemini()]] - code - tests/test_full_scenes.py
- [[fake_moss()]] - code - tests/test_full_scenes.py
- [[moss_graph()]] - code - shortsmaker/gpu.py
- [[moss_images()]] - code - shortsmaker/gpu.py
- [[paint_instead()]] - code - shortsmaker/remotion_render.py
- [[test_remotion_failure_paints()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/moss_images
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_pathlib]]
- 4 edges to [[_COMMUNITY_render]]
- 2 edges to [[_COMMUNITY_ffmpeg]]
- 2 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_shutil]]
- 1 edge to [[_COMMUNITY_render_remotion]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]

## Top bridge nodes
- [[moss_images()]] - degree 12, connects to 5 communities
- [[paint_instead()]] - degree 10, connects to 5 communities
- [[comfy_call()]] - degree 3, connects to 2 communities
- [[test_remotion_failure_paints()]] - degree 4, connects to 1 community
- [[moss_graph()]] - degree 3, connects to 1 community