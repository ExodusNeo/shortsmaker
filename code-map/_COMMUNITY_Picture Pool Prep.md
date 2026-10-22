---
type: community
cohesion: 0.17
members: 16
---

# Picture Pool Prep

**Cohesion:** 0.17 - loosely connected
**Members:** 16 nodes

## Members
- [[Before writing the topic's Wikipedia research (`_texts`; fact_check() reuses…]] - rationale - shortsmaker/picture_pool.py
- [[Numbered thumbnail grids (6x4) so Claude can look at every candidate at once.]] - rationale - shortsmaker/picture_pool.py
- [[Path_12]] - code
- [[The saved pool (None if missing or unreadable it is gathered again);…]] - rationale - shortsmaker/picture_pool.py
- [[Write via a temp file, so an interrupted run never leaves a half-written file…]] - rationale - shortsmaker/media_tools.py
- [[contact_sheets()]] - code - shortsmaker/picture_pool.py
- [[load_pool()]] - code - shortsmaker/picture_pool.py
- [[pool.json (the candidates without bytes) + thumbk.jpg; list positions are the…]] - rationale - shortsmaker/picture_pool.py
- [[pool_folder()]] - code - shortsmaker/picture_pool.py
- [[prepare_topic()]] - code - shortsmaker/picture_pool.py
- [[save_pool()]] - code - shortsmaker/picture_pool.py
- [[test_empty_pool_drops_topic_without_ai()]] - code - tests/test_pictures_first.py
- [[test_pool_roundtrip()]] - code - tests/test_pictures_first.py
- [[test_pool_rows_without_thumbs()]] - code - tests/test_pictures_first.py
- [[test_small_pool_skips_ai()]] - code - tests/test_pictures_first.py
- [[write_json()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Picture_Pool_Prep
SORT file.name ASC
```

## Connections to other communities
- 15 edges to [[_COMMUNITY_Picture Catalog]]
- 9 edges to [[_COMMUNITY_Archive Film & Downloads]]
- 3 edges to [[_COMMUNITY_Script Writing Pipeline]]
- 3 edges to [[_COMMUNITY_Picture Picker]]
- 2 edges to [[_COMMUNITY_Film Footage Sources]]
- 2 edges to [[_COMMUNITY_Media Tools & Shot Spans]]
- 2 edges to [[_COMMUNITY_Usable Picture Checks]]
- 1 edge to [[_COMMUNITY_Test Patching Helpers]]
- 1 edge to [[_COMMUNITY_Graphics Rescue & Validation]]

## Top bridge nodes
- [[prepare_topic()]] - degree 12, connects to 5 communities
- [[save_pool()]] - degree 13, connects to 4 communities
- [[load_pool()]] - degree 10, connects to 4 communities
- [[write_json()]] - degree 6, connects to 3 communities
- [[contact_sheets()]] - degree 6, connects to 3 communities