---
type: community
members: 13
---

# full_cues

**Members:** 13 nodes

## Members
- [[(start, end) of the first time `phrase` is spoken, from TTS word timings.]] - rationale - shortsmaker/plan_rules.py
- [[Mike's 'WHY MIKE DIED' (2.7 s scene, last word 1 s before the cut) its stamp…]] - rationale - tests/test_full_scenes.py
- [[Scene 1's motion-graphic opener set outside the scene-1 and two-in-a-row…]] - rationale - tests/test_full_scenes.py
- [[Start time of the first time `phrase` is spoken, from TTS word timings.]] - rationale - shortsmaker/plan_rules.py
- [[When each element of a full-screen motion graphic appears (absolute seconds)…]] - rationale - shortsmaker/plan_rules.py
- [[full_cues()]] - code - shortsmaker/plan_rules.py
- [[spoken_at()]] - code - shortsmaker/plan_rules.py
- [[spoken_span()]] - code - shortsmaker/plan_rules.py
- [[squeeze()]] - code - shortsmaker/plan_rules.py
- [[test_full_cues_document()]] - code - tests/test_full_scenes.py
- [[test_full_cues_fallback()]] - code - tests/test_full_scenes.py
- [[test_full_cues_leave_time_to_finish()]] - code - tests/test_full_scenes.py
- [[test_opener_graphic()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/full_cues
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_scene_cues]]
- 1 edge to [[_COMMUNITY_opener_graphic]]
- 1 edge to [[_COMMUNITY_full_props]]
- 1 edge to [[_COMMUNITY_peaks]]
- 1 edge to [[_COMMUNITY_clean_full]]

## Top bridge nodes
- [[full_cues()]] - degree 11, connects to 3 communities
- [[spoken_at()]] - degree 6, connects to 3 communities
- [[spoken_span()]] - degree 5, connects to 2 communities
- [[test_opener_graphic()]] - degree 4, connects to 2 communities
- [[test_full_cues_leave_time_to_finish()]] - degree 3, connects to 1 community