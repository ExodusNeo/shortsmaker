---
type: community
cohesion: 0.20
members: 10
---

# Scene & Graphic Timing

**Cohesion:** 0.20 - loosely connected
**Members:** 10 nodes

## Members
- [[Mike's 'WHY MIKE DIED' (2.7 s scene, last word 1 s before the cut) its stamp…]] - rationale - tests/test_full_scenes.py
- [[Timed extras for one scene a person card (photo `found`) when their name is…]] - rationale - shortsmaker/editplan.py
- [[When each element of a full-screen motion graphic appears (absolute seconds)…]] - rationale - shortsmaker/plan_rules.py
- [[full_cues()]] - code - shortsmaker/plan_rules.py
- [[scene_cues()]] - code - shortsmaker/editplan.py
- [[squeeze()]] - code - shortsmaker/plan_rules.py
- [[test_counter_finishes_before_it_leaves()]] - code - tests/test_full_scenes.py
- [[test_full_cues_document()]] - code - tests/test_full_scenes.py
- [[test_full_cues_fallback()]] - code - tests/test_full_scenes.py
- [[test_full_cues_leave_time_to_finish()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Scene__Graphic_Timing
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Graphics Rescue & Validation]]
- 4 edges to [[_COMMUNITY_Full Scene Tests]]
- 1 edge to [[_COMMUNITY_Python Frame Renderer]]
- 1 edge to [[_COMMUNITY_Channel Profiles & Menus]]
- 1 edge to [[_COMMUNITY_Full Scene Props]]

## Top bridge nodes
- [[scene_cues()]] - degree 6, connects to 3 communities
- [[full_cues()]] - degree 10, connects to 2 communities
- [[test_full_cues_leave_time_to_finish()]] - degree 3, connects to 1 community
- [[test_counter_finishes_before_it_leaves()]] - degree 2, connects to 1 community
- [[test_full_cues_document()]] - degree 2, connects to 1 community