---
type: community
members: 8
---

# Story Sound Limits

**Members:** 8 nodes

## Members
- [[A planned story sound {word, sound}, validated the word must be spoken in…]] - rationale - shortsmaker/audio_mix.py
- [[At most MAX_STORY_SOUNDS story sounds per Short (the first ones), so each one…]] - rationale - shortsmaker/audio_mix.py
- [[Lowercase, accent-free word tokens, for matching names against spoken words.]] - rationale - shortsmaker/plan_rules.py
- [[clean_sound()]] - code - shortsmaker/audio_mix.py
- [[limit_sounds()]] - code - shortsmaker/audio_mix.py
- [[test_clean_full_keeps_board_pic()]] - code - tests/test_pictures_first.py
- [[test_clean_sound()]] - code - tests/test_full_scenes.py
- [[words_of()]] - code - shortsmaker/plan_rules.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Story_Sound_Limits
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Full-Scene Rescue & Plan Cleaning]]
- 3 edges to [[_COMMUNITY_Quality Check & Script Editing]]
- 3 edges to [[_COMMUNITY_Footage Downloads & Crops (3)]]
- 2 edges to [[_COMMUNITY_Scene Cues & Word Timing]]
- 2 edges to [[_COMMUNITY_Entry Point, Logbook & Sounds]]
- 2 edges to [[_COMMUNITY_Captions & TTS]]
- 1 edge to [[_COMMUNITY_Commons & Archive Sources]]
- 1 edge to [[_COMMUNITY_Channel Profiles & CLI (2)]]
- 1 edge to [[_COMMUNITY_Pool Gathering]]
- 1 edge to [[_COMMUNITY_Voice Worker (qwen_voice)]]
- 1 edge to [[_COMMUNITY_Channel Profiles & CLI]]
- 1 edge to [[_COMMUNITY_Picture List Catalog]]

## Top bridge nodes
- [[words_of()]] - degree 18, connects to 10 communities
- [[clean_sound()]] - degree 7, connects to 4 communities
- [[limit_sounds()]] - degree 4, connects to 2 communities
- [[test_clean_full_keeps_board_pic()]] - degree 3, connects to 2 communities
- [[test_clean_sound()]] - degree 4, connects to 1 community