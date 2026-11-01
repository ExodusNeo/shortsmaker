---
type: community
members: 6
---

# freesound_results

**Members:** 6 nodes

## Members
- [[Official API, CC0 only; collect metadata before choosing a preview.]] - rationale - shortsmaker/audio_mix.py
- [[One CC0 (no credit, any use) sound for `name` from Freesound's official API…]] - rationale - shortsmaker/audio_mix.py
- [[freesound_fetch()]] - code - shortsmaker/audio_mix.py
- [[freesound_preview()]] - code - shortsmaker/audio_mix.py
- [[freesound_results()]] - code - shortsmaker/audio_mix.py
- [[rank()]] - code - shortsmaker/audio_mix.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/freesound_results
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_re]]
- 2 edges to [[_COMMUNITY_media_command]]
- 1 edge to [[_COMMUNITY_extra_sources.py]]
- 1 edge to [[_COMMUNITY_json]]

## Top bridge nodes
- [[freesound_results()]] - degree 6, connects to 3 communities
- [[freesound_preview()]] - degree 4, connects to 3 communities
- [[freesound_fetch()]] - degree 4, connects to 1 community