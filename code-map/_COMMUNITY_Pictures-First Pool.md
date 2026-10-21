---
type: community
cohesion: 0.24
members: 11
---

# Pictures-First Pool

**Cohesion:** 0.24 - loosely connected
**Members:** 11 nodes

## Members
- [[Before writing the topic's Wikipedia research (`_texts`; fact_check() reuses…]] - rationale - make_shorts.py
- [[The saved pool (None if missing or unreadable it is gathered again);…]] - rationale - make_shorts.py
- [[load_pool()]] - code - make_shorts.py
- [[pool.json (the candidates without bytes) + thumbk.jpg; list positions are the…]] - rationale - make_shorts.py
- [[prepare_topic()]] - code - make_shorts.py
- [[save_pool()]] - code - make_shorts.py
- [[test_corrupt_pool_and_catalog_redone()]] - code - tests/test_pictures_first.py
- [[test_empty_pool_drops_topic_without_ai()]] - code - tests/test_pictures_first.py
- [[test_pool_roundtrip()]] - code - tests/test_pictures_first.py
- [[test_pool_rows_without_thumbs()]] - code - tests/test_pictures_first.py
- [[test_small_pool_skips_ai()]] - code - tests/test_pictures_first.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pictures-First_Pool
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_Usable Picture Catalog]]
- 5 edges to [[_COMMUNITY_Script Team (WriteEditDirect)]]
- 4 edges to [[_COMMUNITY_Picture List & Contact Sheets]]
- 4 edges to [[_COMMUNITY_State & Logbook Helpers]]
- 3 edges to [[_COMMUNITY_Archive Picture & Film Sources]]
- 3 edges to [[_COMMUNITY_Shared Imports & Downloads]]
- 2 edges to [[_COMMUNITY_Image Choosing]]
- 2 edges to [[_COMMUNITY_Director Picture Context]]
- 1 edge to [[_COMMUNITY_Wikipedia & Wikimedia Research]]

## Top bridge nodes
- [[prepare_topic()]] - degree 13, connects to 7 communities
- [[save_pool()]] - degree 13, connects to 6 communities
- [[load_pool()]] - degree 10, connects to 5 communities
- [[test_corrupt_pool_and_catalog_redone()]] - degree 7, connects to 2 communities
- [[test_pool_roundtrip()]] - degree 5, connects to 2 communities