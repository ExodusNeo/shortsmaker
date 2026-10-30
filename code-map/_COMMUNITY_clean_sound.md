---
type: community
members: 7
---

# clean_sound

**Members:** 7 nodes

## Members
- [[A planned story sound {word, sound}, validated the word must be spoken in…]] - rationale - shortsmaker/audio_mix.py
- [[At most MAX_STORY_SOUNDS story sounds per Short (the first ones), so each one…]] - rationale - shortsmaker/audio_mix.py
- [[clean_sound()]] - code - shortsmaker/audio_mix.py
- [[contains()]] - code - shortsmaker/plan_rules.py
- [[limit_sounds()]] - code - shortsmaker/audio_mix.py
- [[test_clean_sound()]] - code - tests/test_full_scenes.py
- [[word()]] - code - shortsmaker/plan_rules.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/clean_sound
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_write_scripts]]
- 3 edges to [[_COMMUNITY_words_of]]
- 2 edges to [[_COMMUNITY_clean_full]]
- 2 edges to [[_COMMUNITY_subprocess]]
- 2 edges to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_gather_pool]]
- 1 edge to [[_COMMUNITY_clean_graphic]]
- 1 edge to [[_COMMUNITY_re]]

## Top bridge nodes
- [[contains()]] - degree 7, connects to 5 communities
- [[clean_sound()]] - degree 7, connects to 4 communities
- [[limit_sounds()]] - degree 4, connects to 2 communities
- [[test_clean_sound()]] - degree 4, connects to 2 communities
- [[word()]] - degree 3, connects to 2 communities