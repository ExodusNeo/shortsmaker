---
type: community
cohesion: 0.25
members: 8
---

# Music & Freesound

**Cohesion:** 0.25 - loosely connected
**Members:** 8 nodes

## Members
- [[One CC0 (no credit, any use) sound for `name` from Freesound's official API…]] - rationale - shortsmaker/audio_mix.py
- [[Voice, captions, sound effects, story sounds and music levels.]] - rationale - shortsmaker/audio_mix.py
- [[Volume factor that brings this track's loudness (first 60 s) to MUSIC_LUFS;…]] - rationale - shortsmaker/audio_mix.py
- [[audio_mix.py]] - code - shortsmaker/audio_mix.py
- [[freesound_fetch()]] - code - shortsmaker/audio_mix.py
- [[music_gain()]] - code - shortsmaker/audio_mix.py
- [[urllib_request]] - concept
- [[wave]] - concept

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Music__Freesound
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_Captions & TTS]]
- 7 edges to [[_COMMUNITY_Channel Profiles & CLI]]
- 5 edges to [[_COMMUNITY_Footage Downloads & Crops]]
- 3 edges to [[_COMMUNITY_Motion Previews & Render Tests]]
- 3 edges to [[_COMMUNITY_Entry Point, Logbook & Sounds]]
- 2 edges to [[_COMMUNITY_Full-Scene Limits & Director Tests]]
- 2 edges to [[_COMMUNITY_SFX Events & Full Pictures]]
- 2 edges to [[_COMMUNITY_Story Sounds & Credits]]
- 2 edges to [[_COMMUNITY_SFX Synthesis]]
- 2 edges to [[_COMMUNITY_Style Lab & Edit Plan Text]]
- 1 edge to [[_COMMUNITY_Story Sound Limits]]
- 1 edge to [[_COMMUNITY_Style Tests]]

## Top bridge nodes
- [[audio_mix.py]] - degree 36, connects to 12 communities
- [[music_gain()]] - degree 7, connects to 5 communities
- [[freesound_fetch()]] - degree 3, connects to 1 community
- [[urllib_request]] - degree 3, connects to 1 community