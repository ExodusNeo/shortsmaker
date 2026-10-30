---
type: community
members: 11
---

# full_cues

**Members:** 11 nodes

## Members
- [[(start, end) of the first time `phrase` is spoken, from TTS word timings.]] - rationale - shortsmaker/plan_rules.py
- [[Mike's 'WHY MIKE DIED' (2.7 s scene, last word 1 s before the cut) its stamp…]] - rationale - tests/test_full_scenes.py
- [[Start time of the first time `phrase` is spoken, from TTS word timings.]] - rationale - shortsmaker/plan_rules.py
- [[When each element of a full-screen motion graphic appears (absolute seconds)…]] - rationale - shortsmaker/plan_rules.py
- [[full_cues()]] - code - shortsmaker/plan_rules.py
- [[spoken_at()]] - code - shortsmaker/plan_rules.py
- [[spoken_span()]] - code - shortsmaker/plan_rules.py
- [[squeeze()]] - code - shortsmaker/plan_rules.py
- [[test_full_cues_document()]] - code - tests/test_full_scenes.py
- [[test_full_cues_fallback()]] - code - tests/test_full_scenes.py
- [[test_full_cues_leave_time_to_finish()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/full_cues
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_opener_graphic]]
- 3 edges to [[_COMMUNITY_gpu.py]]
- 3 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_test_package.py]]
- 1 edge to [[_COMMUNITY_clean_full]]
- 1 edge to [[_COMMUNITY_test_blender_render.py]]

## Top bridge nodes
- [[full_cues()]] - degree 12, connects to 3 communities
- [[spoken_at()]] - degree 6, connects to 3 communities
- [[spoken_span()]] - degree 5, connects to 2 communities
- [[test_full_cues_leave_time_to_finish()]] - degree 3, connects to 1 community
- [[test_full_cues_document()]] - degree 2, connects to 1 community