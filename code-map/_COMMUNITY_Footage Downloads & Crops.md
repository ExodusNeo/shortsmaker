---
type: community
members: 16
---

# Footage Downloads & Crops

**Members:** 16 nodes

## Members
- [[Before writing the topic's Wikipedia research (`_texts`; fact_check() reuses…]] - rationale - shortsmaker/picture_pool.py
- [[Numbered thumbnail grids (6x4) so Claude can look at every candidate at once.]] - rationale - shortsmaker/picture_pool.py
- [[Path_8]] - code
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
TABLE source_file, type FROM #community/Footage_Downloads__Crops
SORT file.name ASC
```

## Connections to other communities
- 14 edges to [[_COMMUNITY_Picture List Catalog (2)]]
- 6 edges to [[_COMMUNITY_Picture List Catalog]]
- 6 edges to [[_COMMUNITY_Channel Profiles & CLI]]
- 3 edges to [[_COMMUNITY_Picture List Catalog (3)]]
- 2 edges to [[_COMMUNITY_Local AI Jobs & Clips]]
- 2 edges to [[_COMMUNITY_Invention Slots]]
- 2 edges to [[_COMMUNITY_Footage Downloads & Crops (2)]]
- 2 edges to [[_COMMUNITY_Footage Downloads & Crops (2)_1]]
- 1 edge to [[_COMMUNITY_Pool Gathering]]
- 1 edge to [[_COMMUNITY_AI Calls & Quota Fallback]]
- 1 edge to [[_COMMUNITY_Footage Downloads & Crops (2) (3)]]

## Top bridge nodes
- [[prepare_topic()]] - degree 13, connects to 6 communities
- [[load_pool()]] - degree 11, connects to 6 communities
- [[save_pool()]] - degree 13, connects to 4 communities
- [[write_json()]] - degree 6, connects to 4 communities
- [[contact_sheets()]] - degree 6, connects to 4 communities