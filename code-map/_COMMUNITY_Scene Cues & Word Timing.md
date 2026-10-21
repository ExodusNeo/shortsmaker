---
type: community
members: 14
---

# Scene Cues & Word Timing

**Members:** 14 nodes

## Members
- [[(start, end) of the first time `phrase` is spoken, from TTS word timings.]] - rationale - shortsmaker/plan_rules.py
- [[Mike's 'WHY MIKE DIED' (2.7 s scene, last word 1 s before the cut) its stamp…]] - rationale - tests/test_full_scenes.py
- [[Start time of the first time `phrase` is spoken, from TTS word timings.]] - rationale - shortsmaker/plan_rules.py
- [[Timed extras for one scene a person card (photo `found`) when their name is…]] - rationale - shortsmaker/editplan.py
- [[When each element of a full-screen motion graphic appears (absolute seconds)…]] - rationale - shortsmaker/plan_rules.py
- [[full_cues()]] - code - shortsmaker/plan_rules.py
- [[scene_cues()]] - code - shortsmaker/editplan.py
- [[spoken_at()]] - code - shortsmaker/plan_rules.py
- [[spoken_span()]] - code - shortsmaker/plan_rules.py
- [[squeeze()]] - code - shortsmaker/plan_rules.py
- [[test_counter_finishes_before_it_leaves()]] - code - tests/test_full_scenes.py
- [[test_full_cues_document()]] - code - tests/test_full_scenes.py
- [[test_full_cues_fallback()]] - code - tests/test_full_scenes.py
- [[test_full_cues_leave_time_to_finish()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Scene_Cues__Word_Timing
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Full-Scene Rescue & Plan Cleaning]]
- 4 edges to [[_COMMUNITY_AI Calls & Quota Fallback (4)]]
- 1 edge to [[_COMMUNITY_Python Frame Renderer]]
- 1 edge to [[_COMMUNITY_Channel Profiles & CLI (2)]]
- 1 edge to [[_COMMUNITY_Channel Profiles & CLI]]
- 1 edge to [[_COMMUNITY_Scene Cues & Word Timing (3)]]

## Top bridge nodes
- [[scene_cues()]] - degree 7, connects to 3 communities
- [[full_cues()]] - degree 10, connects to 2 communities
- [[spoken_at()]] - degree 5, connects to 1 community
- [[spoken_span()]] - degree 5, connects to 1 community
- [[test_full_cues_leave_time_to_finish()]] - degree 3, connects to 1 community