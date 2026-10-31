---
type: community
members: 18
---

# prepare_topic

**Members:** 18 nodes

## Members
- [[Before writing the topic's Wikipedia research (`_texts`; fact_check() reuses…]] - rationale - shortsmaker/picture_pool.py
- [[Numbered thumbnail grids (6x4) so Claude can look at every candidate at once.]] - rationale - shortsmaker/picture_pool.py
- [[Path_4]] - code
- [[The saved pool (None if missing or unreadable it is gathered again);…]] - rationale - shortsmaker/picture_pool.py
- [[Write via a temp file, so an interrupted run never leaves a half-written file…]] - rationale - shortsmaker/media_tools.py
- [[contact_sheets()]] - code - shortsmaker/picture_pool.py
- [[load_pool()]] - code - shortsmaker/picture_pool.py
- [[no_gather()]] - code - tests/test_pictures_first.py
- [[pool.json (the candidates without bytes) + thumbk.jpg; list positions are the…]] - rationale - shortsmaker/picture_pool.py
- [[pool_folder()]] - code - shortsmaker/picture_pool.py
- [[prepare_topic()]] - code - shortsmaker/picture_pool.py
- [[save_pool()]] - code - shortsmaker/picture_pool.py
- [[test_both_mode_reuses_pools()]] - code - tests/test_pictures_first.py
- [[test_empty_pool_drops_topic_without_ai()]] - code - tests/test_pictures_first.py
- [[test_pool_roundtrip()]] - code - tests/test_pictures_first.py
- [[test_pool_rows_without_thumbs()]] - code - tests/test_pictures_first.py
- [[test_small_pool_skips_ai()]] - code - tests/test_pictures_first.py
- [[write_json()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/prepare_topic
SORT file.name ASC
```

## Connections to other communities
- 17 edges to [[_COMMUNITY_test_pictures_first.py]]
- 7 edges to [[_COMMUNITY_write_scripts]]
- 7 edges to [[_COMMUNITY_test_full_scenes.py]]
- 4 edges to [[_COMMUNITY_json]]
- 3 edges to [[_COMMUNITY_gather_pool]]
- 3 edges to [[_COMMUNITY_choose_images]]
- 2 edges to [[_COMMUNITY_test_rules.py]]
- 2 edges to [[_COMMUNITY_clean_pics]]
- 1 edge to [[_COMMUNITY_local_voice]]
- 1 edge to [[_COMMUNITY_first_second_check]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_test_blender_run.py]]

## Top bridge nodes
- [[load_pool()]] - degree 14, connects to 9 communities
- [[prepare_topic()]] - degree 15, connects to 7 communities
- [[save_pool()]] - degree 13, connects to 4 communities
- [[write_json()]] - degree 6, connects to 4 communities
- [[contact_sheets()]] - degree 6, connects to 3 communities