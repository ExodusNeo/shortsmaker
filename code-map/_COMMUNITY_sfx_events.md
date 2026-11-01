---
type: community
members: 9
---

# sfx_events

**Members:** 9 nodes

## Members
- [[Main story impacts land on their word; effects compete over their whole…]] - rationale - shortsmaker/audio_mix.py
- [[Sound design each timed visual gets a matching sound. Candidates are kept by…]] - rationale - shortsmaker/audio_mix.py
- [[pick()]] - code - shortsmaker/audio_mix.py
- [[sc()]] - code - tests/test_style.py
- [[schedule_sounds()]] - code - shortsmaker/audio_mix.py
- [[sfx_events()]] - code - shortsmaker/audio_mix.py
- [[test_sfx_full()]] - code - tests/test_full_scenes.py
- [[test_story_sound_wins_its_moment()]] - code - tests/test_full_scenes.py
- [[test_style_sounds()]] - code - tests/test_style.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/sfx_events
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_subprocess]]
- 2 edges to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_audio_library.py]]
- 1 edge to [[_COMMUNITY_extra_sources.py]]
- 1 edge to [[_COMMUNITY_test_style.py]]

## Top bridge nodes
- [[sfx_events()]] - degree 8, connects to 2 communities
- [[schedule_sounds()]] - degree 4, connects to 2 communities
- [[test_sfx_full()]] - degree 3, connects to 2 communities
- [[test_style_sounds()]] - degree 3, connects to 1 community
- [[test_story_sound_wins_its_moment()]] - degree 2, connects to 1 community