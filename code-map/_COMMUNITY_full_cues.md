---
type: community
members: 16
---

# full_cues

**Members:** 16 nodes

## Members
- [[(start, end) of the first time `phrase` is spoken, from TTS word timings.]] - rationale - shortsmaker/plan_rules.py
- [[Mike's 'WHY MIKE DIED' (2.7 s scene, last word 1 s before the cut) its stamp…]] - rationale - tests/test_full_scenes.py
- [[Start time of the first time `phrase` is spoken, from TTS word timings.]] - rationale - shortsmaker/plan_rules.py
- [[Tilted photo card with a white border, drop shadow and a yellow name banner.]] - rationale - shortsmaker/frame_render.py
- [[Timed extras for one scene a person card (photo `found`) when their name is…]] - rationale - shortsmaker/editplan.py
- [[When each element of a full-screen motion graphic appears (absolute seconds)…]] - rationale - shortsmaker/plan_rules.py
- [[full_cues()]] - code - shortsmaker/plan_rules.py
- [[person_card()]] - code - shortsmaker/frame_render.py
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
TABLE source_file, type FROM #community/full_cues
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_test_full_scenes.py]]
- 4 edges to [[_COMMUNITY_plan_rules.py]]
- 1 edge to [[_COMMUNITY_clean_full]]
- 1 edge to [[_COMMUNITY_frame_maker]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_ClipReader]]
- 1 edge to [[_COMMUNITY_audio_mix.py]]

## Top bridge nodes
- [[person_card()]] - degree 6, connects to 4 communities
- [[full_cues()]] - degree 10, connects to 2 communities
- [[scene_cues()]] - degree 7, connects to 2 communities
- [[spoken_span()]] - degree 5, connects to 2 communities
- [[spoken_at()]] - degree 5, connects to 1 community