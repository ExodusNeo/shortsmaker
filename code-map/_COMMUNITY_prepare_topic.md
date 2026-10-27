---
type: community
members: 16
---

# prepare_topic

**Members:** 16 nodes

## Members
- [[Before writing the topic's Wikipedia research (`_texts`; fact_check() reuses…]] - rationale - shortsmaker/picture_pool.py
- [[Numbered thumbnail grids (6x4) so Claude can look at every candidate at once.]] - rationale - shortsmaker/picture_pool.py
- [[Path_3]] - code
- [[The saved pool (None if missing or unreadable it is gathered again);…]] - rationale - shortsmaker/picture_pool.py
- [[The usable pictures as prompt lines 12 film 1944 newsreel of rubber tanks…]] - rationale - shortsmaker/picture_pool.py
- [[Usable list entries for the topic check all frames of one video count once…]] - rationale - shortsmaker/picture_pool.py
- [[catalog_text()]] - code - shortsmaker/picture_pool.py
- [[contact_sheets()]] - code - shortsmaker/picture_pool.py
- [[is_usable()]] - code - shortsmaker/picture_pool.py
- [[load_pool()]] - code - shortsmaker/picture_pool.py
- [[pool_folder()]] - code - shortsmaker/picture_pool.py
- [[prepare_topic()]] - code - shortsmaker/picture_pool.py
- [[test_empty_pool_drops_topic_without_ai()]] - code - tests/test_pictures_first.py
- [[test_pool_roundtrip()]] - code - tests/test_pictures_first.py
- [[test_small_pool_skips_ai()]] - code - tests/test_pictures_first.py
- [[usable()]] - code - shortsmaker/picture_pool.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/prepare_topic
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_pool_of]]
- 8 edges to [[_COMMUNITY_pathlib]]
- 6 edges to [[_COMMUNITY_write_scripts]]
- 5 edges to [[_COMMUNITY_test_pictures_first.py]]
- 3 edges to [[_COMMUNITY_gather_pool]]
- 3 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_test_rules.py]]
- 2 edges to [[_COMMUNITY_test_first_second.py]]
- 1 edge to [[_COMMUNITY_test_blender_scene.py]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_drawn_thumbnail]]

## Top bridge nodes
- [[load_pool()]] - degree 14, connects to 8 communities
- [[prepare_topic()]] - degree 15, connects to 6 communities
- [[is_usable()]] - degree 6, connects to 4 communities
- [[contact_sheets()]] - degree 6, connects to 3 communities
- [[catalog_text()]] - degree 5, connects to 3 communities