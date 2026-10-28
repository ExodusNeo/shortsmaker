---
type: community
members: 14
---

# prepare_topic

**Members:** 14 nodes

## Members
- [[Before writing the topic's Wikipedia research (`_texts`; fact_check() reuses…]] - rationale - shortsmaker/picture_pool.py
- [[Numbered thumbnail grids (6x4) so Claude can look at every candidate at once.]] - rationale - shortsmaker/picture_pool.py
- [[Path_17]] - code
- [[The saved pool (None if missing or unreadable it is gathered again);…]] - rationale - shortsmaker/picture_pool.py
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

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/prepare_topic
SORT file.name ASC
```

## Connections to other communities
- 15 edges to [[_COMMUNITY_test_pictures_first.py]]
- 5 edges to [[_COMMUNITY_test_full_scenes.py]]
- 3 edges to [[_COMMUNITY_gather_pool]]
- 3 edges to [[_COMMUNITY_choose_images]]
- 3 edges to [[_COMMUNITY_write_scripts]]
- 2 edges to [[_COMMUNITY_planning]]
- 2 edges to [[_COMMUNITY_test_rules.py]]
- 2 edges to [[_COMMUNITY_pool_pictures]]
- 1 edge to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_test_blender_render.py]]
- 1 edge to [[_COMMUNITY_frame_render.py]]
- 1 edge to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_test_first_second.py]]
- 1 edge to [[_COMMUNITY_subprocess]]
- 1 edge to [[_COMMUNITY_blender_link.py]]

## Top bridge nodes
- [[load_pool()]] - degree 14, connects to 8 communities
- [[prepare_topic()]] - degree 15, connects to 7 communities
- [[save_pool()]] - degree 13, connects to 4 communities
- [[contact_sheets()]] - degree 6, connects to 4 communities
- [[test_pool_roundtrip()]] - degree 5, connects to 2 communities