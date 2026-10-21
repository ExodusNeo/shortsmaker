---
type: community
cohesion: 0.50
members: 4
---

# Music Loudness

**Cohesion:** 0.50 - moderately connected
**Members:** 4 nodes

## Members
- [[Mike's Thinking Music (-22 LUFS) vanished under the voice with the old fixed…]] - rationale - tests/test_full_scenes.py
- [[Volume factor that brings this track's loudness (first 60 s) to MUSIC_LUFS;…]] - rationale - make_shorts.py
- [[music_gain()]] - code - make_shorts.py
- [[test_music_gain_evens_out_tracks()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Music_Loudness
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Quality Checks & Captions]]
- 1 edge to [[_COMMUNITY_State & Logbook Helpers]]
- 1 edge to [[_COMMUNITY_Shared Imports & Downloads]]
- 1 edge to [[_COMMUNITY_Full-Scene Validation]]

## Top bridge nodes
- [[music_gain()]] - degree 5, connects to 3 communities
- [[test_music_gain_evens_out_tracks()]] - degree 3, connects to 1 community