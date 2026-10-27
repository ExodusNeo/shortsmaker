---
type: community
members: 21
---

# catalog_pool

**Members:** 21 nodes

## Members
- [[Before writing the topic's Wikipedia research (`_texts`; fact_check() reuses…]] - rationale - shortsmaker/picture_pool.py
- [[Numbered thumbnail grids (6x4) so Claude can look at every candidate at once.]] - rationale - shortsmaker/picture_pool.py
- [[Path_12]] - code
- [[The picture list the writer, editor and director plan with the AI looks at the…]] - rationale - shortsmaker/picture_pool.py
- [[The saved pool (None if missing or unreadable it is gathered again);…]] - rationale - shortsmaker/picture_pool.py
- [[The valid entries of a picture-list reply (LLM output is untrusted).]] - rationale - shortsmaker/picture_pool.py
- [[Write via a temp file, so an interrupted run never leaves a half-written file…]] - rationale - shortsmaker/media_tools.py
- [[catalog_entries()]] - code - shortsmaker/picture_pool.py
- [[catalog_pool()]] - code - shortsmaker/picture_pool.py
- [[contact_sheets()]] - code - shortsmaker/picture_pool.py
- [[load_pool()]] - code - shortsmaker/picture_pool.py
- [[pool.json (the candidates without bytes) + thumbk.jpg; list positions are the…]] - rationale - shortsmaker/picture_pool.py
- [[pool_folder()]] - code - shortsmaker/picture_pool.py
- [[prepare_topic()]] - code - shortsmaker/picture_pool.py
- [[save_pool()]] - code - shortsmaker/picture_pool.py
- [[test_catalog_empty_pool_no_ai()]] - code - tests/test_pictures_first.py
- [[test_catalog_failure_stops()]] - code - tests/test_pictures_first.py
- [[test_empty_pool_drops_topic_without_ai()]] - code - tests/test_pictures_first.py
- [[test_pool_roundtrip()]] - code - tests/test_pictures_first.py
- [[test_pool_rows_without_thumbs()]] - code - tests/test_pictures_first.py
- [[write_json()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/catalog_pool
SORT file.name ASC
```

## Connections to other communities
- 18 edges to [[_COMMUNITY_test_pictures_first.py]]
- 10 edges to [[_COMMUNITY_test_full_scenes.py]]
- 4 edges to [[_COMMUNITY_write_scripts]]
- 3 edges to [[_COMMUNITY_test_rules.py]]
- 3 edges to [[_COMMUNITY_json]]
- 3 edges to [[_COMMUNITY_choose_images]]
- 2 edges to [[_COMMUNITY_fake_ai]]
- 2 edges to [[_COMMUNITY_pictures_of]]
- 2 edges to [[_COMMUNITY_gather_pool]]
- 1 edge to [[_COMMUNITY_owner]]
- 1 edge to [[_COMMUNITY_test_blender_run.py]]
- 1 edge to [[_COMMUNITY_first_second_check]]
- 1 edge to [[_COMMUNITY_ffmpeg]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_sys]]
- 1 edge to [[_COMMUNITY_fetch]]
- 1 edge to [[_COMMUNITY_wm_get]]

## Top bridge nodes
- [[load_pool()]] - degree 14, connects to 9 communities
- [[prepare_topic()]] - degree 15, connects to 7 communities
- [[catalog_pool()]] - degree 18, connects to 6 communities
- [[save_pool()]] - degree 13, connects to 4 communities
- [[write_json()]] - degree 6, connects to 3 communities