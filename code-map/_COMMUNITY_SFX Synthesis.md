---
type: community
cohesion: 0.22
members: 9
---

# SFX Synthesis

**Cohesion:** 0.22 - loosely connected
**Members:** 9 nodes

## Members
- [[Stream every frame to ffmpeg. Cuts in `flashes` are hard cuts under a white…]] - rationale - shortsmaker/frame_render.py
- [[Synthesize the sound-effect library once (no downloads, no copyright). Hits,…]] - rationale - shortsmaker/audio_mix.py
- [[White camera-flash curve snaps up over the 2 frames before the cut, then…]] - rationale - shortsmaker/frame_render.py
- [[flash_alpha()]] - code - shortsmaker/frame_render.py
- [[make_sfx()]] - code - shortsmaker/audio_mix.py
- [[math]] - concept
- [[noise()_1]] - code - shortsmaker/audio_mix.py
- [[save()]] - code - shortsmaker/audio_mix.py
- [[write_frames()]] - code - shortsmaker/frame_render.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SFX_Synthesis
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Channel Profiles & CLI]]
- 2 edges to [[_COMMUNITY_Story Sounds & Credits]]
- 2 edges to [[_COMMUNITY_Music & Freesound]]
- 1 edge to [[_COMMUNITY_SFX Events & Full Pictures]]
- 1 edge to [[_COMMUNITY_Python Frame Renderer]]

## Top bridge nodes
- [[make_sfx()]] - degree 7, connects to 3 communities
- [[write_frames()]] - degree 5, connects to 3 communities
- [[math]] - degree 4, connects to 2 communities
- [[flash_alpha()]] - degree 4, connects to 1 community