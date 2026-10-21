---
type: community
cohesion: 0.67
members: 3
---

# Story Sound Limits

**Cohesion:** 0.67 - moderately connected
**Members:** 3 nodes

## Members
- [[At most MAX_STORY_SOUNDS story sounds per Short (the first ones), so each one…]] - rationale - shortsmaker/audio_mix.py
- [[limit_sounds()]] - code - shortsmaker/audio_mix.py
- [[test_clean_sound()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Story_Sound_Limits
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Full-Scene Rescue & Plan Cleaning]]
- 1 edge to [[_COMMUNITY_Script Writing Pipeline]]
- 1 edge to [[_COMMUNITY_Entry Point, Logbook & Sounds]]
- 1 edge to [[_COMMUNITY_Music & Freesound]]
- 1 edge to [[_COMMUNITY_Full-Scene Limits & Director Tests]]

## Top bridge nodes
- [[test_clean_sound()]] - degree 4, connects to 3 communities
- [[limit_sounds()]] - degree 4, connects to 2 communities