---
type: community
cohesion: 0.16
members: 14
---

# Spoken-Word Cue Timing

**Cohesion:** 0.16 - loosely connected
**Members:** 14 nodes

## Members
- [[(start, end) of the first time `phrase` is spoken, from TTS word timings.]] - rationale - make_shorts.py
- [[Mike's 'WHY MIKE DIED' (2.7 s scene, last word 1 s before the cut) its stamp…]] - rationale - tests/test_full_scenes.py
- [[Start time of the first time `phrase` is spoken, from TTS word timings.]] - rationale - make_shorts.py
- [[Timed extras for one scene a person card (photo `found`) when their name is…]] - rationale - make_shorts.py
- [[When each element of a full-screen motion graphic appears (absolute seconds)…]] - rationale - make_shorts.py
- [[full_cues()]] - code - make_shorts.py
- [[scene_cues()]] - code - make_shorts.py
- [[spoken_at()]] - code - make_shorts.py
- [[spoken_span()]] - code - make_shorts.py
- [[squeeze()]] - code - make_shorts.py
- [[test_counter_finishes_before_it_leaves()]] - code - tests/test_full_scenes.py
- [[test_full_cues_document()]] - code - tests/test_full_scenes.py
- [[test_full_cues_fallback()]] - code - tests/test_full_scenes.py
- [[test_full_cues_leave_time_to_finish()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Spoken-Word_Cue_Timing
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Shared Imports & Downloads]]
- 4 edges to [[_COMMUNITY_Full-Scene Validation]]
- 1 edge to [[_COMMUNITY_Full-Scene Props]]
- 1 edge to [[_COMMUNITY_Quality Checks & Captions]]
- 1 edge to [[_COMMUNITY_Python Frame Renderer]]
- 1 edge to [[_COMMUNITY_Callout & Sound Validation]]

## Top bridge nodes
- [[scene_cues()]] - degree 7, connects to 3 communities
- [[full_cues()]] - degree 10, connects to 2 communities
- [[spoken_span()]] - degree 5, connects to 2 communities
- [[spoken_at()]] - degree 5, connects to 1 community
- [[test_full_cues_leave_time_to_finish()]] - degree 3, connects to 1 community