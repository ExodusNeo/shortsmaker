---
type: community
cohesion: 0.18
members: 11
---

# Sound Cue Sheet

**Cohesion:** 0.18 - loosely connected
**Members:** 11 nodes

## Members
- [[Downloads the real photos the picker chose for evidence boards, custom scenes…]] - rationale - shortsmaker/picker.py
- [[Sound design each timed visual gets a matching sound. Candidates are kept by…]] - rationale - shortsmaker/audio_mix.py
- [[_board()]] - code - tests/test_full_scenes.py
- [[full_pictures()]] - code - shortsmaker/picker.py
- [[pick()]] - code - shortsmaker/audio_mix.py
- [[sc()]] - code - tests/test_style.py
- [[sfx_events()]] - code - shortsmaker/audio_mix.py
- [[test_board_pictures_attached()]] - code - tests/test_full_scenes.py
- [[test_sfx_full()]] - code - tests/test_full_scenes.py
- [[test_story_sound_wins_its_moment()]] - code - tests/test_full_scenes.py
- [[test_style_sounds()]] - code - tests/test_style.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Sound_Cue_Sheet
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Full Scene Tests]]
- 1 edge to [[_COMMUNITY_Film Footage Sources]]
- 1 edge to [[_COMMUNITY_Picture Picker]]
- 1 edge to [[_COMMUNITY_SFX & Paper Synthesis]]
- 1 edge to [[_COMMUNITY_Sound Effects & Story Sounds]]
- 1 edge to [[_COMMUNITY_Channel Profiles & Menus]]
- 1 edge to [[_COMMUNITY_Full Scene Props]]
- 1 edge to [[_COMMUNITY_Style Candidates]]

## Top bridge nodes
- [[full_pictures()]] - degree 5, connects to 3 communities
- [[sfx_events()]] - degree 7, connects to 2 communities
- [[_board()]] - degree 4, connects to 2 communities
- [[test_board_pictures_attached()]] - degree 3, connects to 1 community
- [[test_sfx_full()]] - degree 3, connects to 1 community