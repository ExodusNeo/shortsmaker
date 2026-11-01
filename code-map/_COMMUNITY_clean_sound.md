---
type: community
members: 5
---

# clean_sound

**Members:** 5 nodes

## Members
- [[A planned story sound {word, sound}, validated the word must be spoken in…]] - rationale - shortsmaker/audio_mix.py
- [[At most MAX_STORY_SOUNDS story sounds per Short (the first ones), so each one…]] - rationale - shortsmaker/audio_mix.py
- [[clean_sound()]] - code - shortsmaker/audio_mix.py
- [[limit_sounds()]] - code - shortsmaker/audio_mix.py
- [[test_clean_sound()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/clean_sound
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_plan_rules.py]]
- 3 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_re]]

## Top bridge nodes
- [[clean_sound()]] - degree 7, connects to 4 communities
- [[limit_sounds()]] - degree 4, connects to 2 communities
- [[test_clean_sound()]] - degree 4, connects to 2 communities