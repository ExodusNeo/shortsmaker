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
- 2 edges to [[_COMMUNITY_write_scripts]]
- 2 edges to [[_COMMUNITY_words_of]]
- 2 edges to [[_COMMUNITY_audio_mix.py]]
- 1 edge to [[_COMMUNITY_clean_full]]
- 1 edge to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]

## Top bridge nodes
- [[clean_sound()]] - degree 7, connects to 5 communities
- [[limit_sounds()]] - degree 4, connects to 2 communities
- [[test_clean_sound()]] - degree 4, connects to 2 communities