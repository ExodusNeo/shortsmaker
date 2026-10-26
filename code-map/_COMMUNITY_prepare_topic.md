---
type: community
members: 11
---

# prepare_topic

**Members:** 11 nodes

## Members
- [[Before writing the topic's Wikipedia research (`_texts`; fact_check() reuses…]] - rationale - shortsmaker/picture_pool.py
- [[Numbered thumbnail grids (6x4) so Claude can look at every candidate at once.]] - rationale - shortsmaker/picture_pool.py
- [[Path_4]] - code
- [[The saved pool (None if missing or unreadable it is gathered again);…]] - rationale - shortsmaker/picture_pool.py
- [[contact_sheets()]] - code - shortsmaker/picture_pool.py
- [[load_pool()]] - code - shortsmaker/picture_pool.py
- [[pool_folder()]] - code - shortsmaker/picture_pool.py
- [[prepare_topic()]] - code - shortsmaker/picture_pool.py
- [[test_empty_pool_drops_topic_without_ai()]] - code - tests/test_pictures_first.py
- [[test_pool_roundtrip()]] - code - tests/test_pictures_first.py
- [[test_small_pool_skips_ai()]] - code - tests/test_pictures_first.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/prepare_topic
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_test_pictures_first.py]]
- 7 edges to [[_COMMUNITY_json]]
- 5 edges to [[_COMMUNITY_write_scripts]]
- 3 edges to [[_COMMUNITY_gather_pool]]
- 2 edges to [[_COMMUNITY_choose_images]]
- 2 edges to [[_COMMUNITY_pool_pictures]]
- 1 edge to [[_COMMUNITY_test_first_second.py]]
- 1 edge to [[_COMMUNITY_drawn_thumbnail]]
- 1 edge to [[_COMMUNITY_fact_check]]
- 1 edge to [[_COMMUNITY_capture_prompts]]
- 1 edge to [[_COMMUNITY_test_rules.py]]

## Top bridge nodes
- [[prepare_topic()]] - degree 15, connects to 8 communities
- [[load_pool()]] - degree 14, connects to 7 communities
- [[contact_sheets()]] - degree 6, connects to 3 communities
- [[test_pool_roundtrip()]] - degree 5, connects to 2 communities
- [[test_small_pool_skips_ai()]] - degree 4, connects to 2 communities