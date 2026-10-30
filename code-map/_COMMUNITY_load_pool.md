---
type: community
members: 12
---

# load_pool

**Members:** 12 nodes

## Members
- [[Numbered thumbnail grids (6x4) so Claude can look at every candidate at once.]] - rationale - shortsmaker/picture_pool.py
- [[Path_4]] - code
- [[The saved pool (None if missing or unreadable it is gathered again);…]] - rationale - shortsmaker/picture_pool.py
- [[Write via a temp file, so an interrupted run never leaves a half-written file…]] - rationale - shortsmaker/media_tools.py
- [[contact_sheets()]] - code - shortsmaker/picture_pool.py
- [[load_pool()]] - code - shortsmaker/picture_pool.py
- [[pool.json (the candidates without bytes) + thumbk.jpg; list positions are the…]] - rationale - shortsmaker/picture_pool.py
- [[pool_folder()]] - code - shortsmaker/picture_pool.py
- [[save_pool()]] - code - shortsmaker/picture_pool.py
- [[test_pool_roundtrip()]] - code - tests/test_pictures_first.py
- [[test_pool_rows_without_thumbs()]] - code - tests/test_pictures_first.py
- [[write_json()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/load_pool
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_pool_of]]
- 7 edges to [[_COMMUNITY_write_scripts]]
- 5 edges to [[_COMMUNITY_test_pictures_first.py]]
- 4 edges to [[_COMMUNITY_json]]
- 4 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_gather_pool]]
- 2 edges to [[_COMMUNITY_subprocess]]
- 1 edge to [[_COMMUNITY_edit_scripts]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_pool_pictures]]
- 1 edge to [[_COMMUNITY_drawn_thumbnail]]

## Top bridge nodes
- [[load_pool()]] - degree 14, connects to 9 communities
- [[save_pool()]] - degree 13, connects to 4 communities
- [[contact_sheets()]] - degree 6, connects to 4 communities
- [[write_json()]] - degree 6, connects to 3 communities
- [[pool_folder()]] - degree 4, connects to 3 communities