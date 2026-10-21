---
type: community
cohesion: 0.19
members: 14
---

# Pool Storage & Contact Sheets

**Cohesion:** 0.19 - loosely connected
**Members:** 14 nodes

## Members
- [[Before writing the topic's Wikipedia research (`_texts`; fact_check() reuses…]] - rationale - shortsmaker/picture_pool.py
- [[Numbered thumbnail grids (6x4) so Claude can look at every candidate at once.]] - rationale - shortsmaker/picture_pool.py
- [[Path_5]] - code
- [[Path_6]] - code
- [[The saved pool (None if missing or unreadable it is gathered again);…]] - rationale - shortsmaker/picture_pool.py
- [[Write via a temp file, so an interrupted run never leaves a half-written file…]] - rationale - shortsmaker/media_tools.py
- [[contact_sheets()]] - code - shortsmaker/picture_pool.py
- [[load_pool()]] - code - shortsmaker/picture_pool.py
- [[pool.json (the candidates without bytes) + thumbk.jpg; list positions are the…]] - rationale - shortsmaker/picture_pool.py
- [[pool_folder()]] - code - shortsmaker/picture_pool.py
- [[prepare_topic()]] - code - shortsmaker/picture_pool.py
- [[save_pool()]] - code - shortsmaker/picture_pool.py
- [[test_pool_rows_without_thumbs()]] - code - tests/test_pictures_first.py
- [[write_json()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pool_Storage__Contact_Sheets
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_Picture List Catalog]]
- 9 edges to [[_COMMUNITY_Footage Downloads & Crops]]
- 6 edges to [[_COMMUNITY_Script Writing Pipeline]]
- 3 edges to [[_COMMUNITY_Picture Picker]]
- 3 edges to [[_COMMUNITY_Pool Gathering]]
- 2 edges to [[_COMMUNITY_Style Lab & Edit Plan Text]]
- 2 edges to [[_COMMUNITY_Usable Picture Filter]]
- 1 edge to [[_COMMUNITY_Commons & Archive Sources]]
- 1 edge to [[_COMMUNITY_Story Sounds & Credits]]

## Top bridge nodes
- [[load_pool()]] - degree 11, connects to 7 communities
- [[prepare_topic()]] - degree 13, connects to 6 communities
- [[save_pool()]] - degree 13, connects to 5 communities
- [[write_json()]] - degree 6, connects to 3 communities
- [[contact_sheets()]] - degree 6, connects to 3 communities