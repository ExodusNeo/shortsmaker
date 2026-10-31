---
type: community
members: 4
---

# music_gain

**Members:** 4 nodes

## Members
- [[Mike's Thinking Music (-22 LUFS) vanished under the voice with the old fixed…]] - rationale - tests/test_full_scenes.py
- [[Volume factor that brings this track's loudness (first 60 s) to MUSIC_LUFS;…]] - rationale - shortsmaker/audio_mix.py
- [[music_gain()]] - code - shortsmaker/audio_mix.py
- [[test_music_gain_evens_out_tracks()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/music_gain
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_captions]]

## Top bridge nodes
- [[music_gain()]] - degree 7, connects to 4 communities
- [[test_music_gain_evens_out_tracks()]] - degree 3, connects to 1 community