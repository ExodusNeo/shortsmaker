---
type: community
cohesion: 0.29
members: 7
---

# Logbook & Vault Pages

**Cohesion:** 0.29 - loosely connected
**Members:** 7 nodes

## Members
- [[Add a finished Short to this channel's logbook, with empty lines for its…]] - rationale - shortsmaker/logbook.py
- [[Path_18]] - code
- [[The Short's page in the Obsidian vault thumbnail, storyboard, its logbook…]] - rationale - shortsmaker/logbook.py
- [[log_short()]] - code - shortsmaker/logbook.py
- [[make_shorts.py notes rebuild every Short's vault page from the logbooks (each…]] - rationale - shortsmaker/logbook.py
- [[vault_page()]] - code - shortsmaker/logbook.py
- [[vault_refresh()]] - code - shortsmaker/logbook.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Logbook__Vault_Pages
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Channel Profiles & Menus]]
- 3 edges to [[_COMMUNITY_Entry Point & Run Menus]]
- 3 edges to [[_COMMUNITY_Sound Effects & Story Sounds]]
- 1 edge to [[_COMMUNITY_Quality & Visual Review]]
- 1 edge to [[_COMMUNITY_Media Tools & Shot Spans]]

## Top bridge nodes
- [[log_short()]] - degree 7, connects to 5 communities
- [[vault_page()]] - degree 7, connects to 3 communities
- [[vault_refresh()]] - degree 5, connects to 3 communities