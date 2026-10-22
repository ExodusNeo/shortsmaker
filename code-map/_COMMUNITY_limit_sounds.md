---
type: community
members: 3
---

# limit_sounds

**Members:** 3 nodes

## Members
- [[At most MAX_STORY_SOUNDS story sounds per Short (the first ones), so each one…]] - rationale - shortsmaker/audio_mix.py
- [[limit_sounds()]] - code - shortsmaker/audio_mix.py
- [[test_clean_sound()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/limit_sounds
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_audio_mix.py]]
- 1 edge to [[_COMMUNITY_clean_full]]
- 1 edge to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]

## Top bridge nodes
- [[test_clean_sound()]] - degree 4, connects to 3 communities
- [[limit_sounds()]] - degree 4, connects to 2 communities