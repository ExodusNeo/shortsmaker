---
type: community
members: 9
---

# download_audio_choices

**Members:** 9 nodes

## Members
- [[New library downloads wait for the owner's ears; existing approved files are…]] - rationale - shortsmaker/media_menu.py
- [[Official API, CC0 only; collect metadata before choosing a preview.]] - rationale - shortsmaker/audio_mix.py
- [[One CC0 (no credit, any use) sound for `name` from Freesound's official API…]] - rationale - shortsmaker/audio_mix.py
- [[download_audio_choices()]] - code - shortsmaker/media_menu.py
- [[freesound_fetch()]] - code - shortsmaker/audio_mix.py
- [[freesound_preview()]] - code - shortsmaker/audio_mix.py
- [[freesound_results()]] - code - shortsmaker/audio_mix.py
- [[rank()]] - code - shortsmaker/audio_mix.py
- [[seed_audio_library()]] - code - shortsmaker/media_menu.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/download_audio_choices
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_audio_library.py]]
- 3 edges to [[_COMMUNITY_audio_mix.py]]
- 3 edges to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_ffmpeg]]
- 1 edge to [[_COMMUNITY_fetch]]
- 1 edge to [[_COMMUNITY_json]]

## Top bridge nodes
- [[download_audio_choices()]] - degree 10, connects to 3 communities
- [[freesound_results()]] - degree 7, connects to 3 communities
- [[freesound_preview()]] - degree 5, connects to 3 communities
- [[seed_audio_library()]] - degree 3, connects to 2 communities
- [[freesound_fetch()]] - degree 4, connects to 1 community