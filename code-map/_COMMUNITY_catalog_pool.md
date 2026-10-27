---
type: community
members: 22
---

# catalog_pool

**Members:** 22 nodes

## Members
- [[Before writing the topic's Wikipedia research (`_texts`; fact_check() reuses…]] - rationale - shortsmaker/picture_pool.py
- [[Numbered thumbnail grids (6x4) so Claude can look at every candidate at once.]] - rationale - shortsmaker/picture_pool.py
- [[Path_4]] - code
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
- [[test_corrupt_pool_and_catalog_redone()]] - code - tests/test_pictures_first.py
- [[test_pool_roundtrip()]] - code - tests/test_pictures_first.py
- [[test_pool_rows_without_thumbs()]] - code - tests/test_pictures_first.py
- [[test_small_pool_skips_ai()]] - code - tests/test_pictures_first.py
- [[write_json()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/catalog_pool
SORT file.name ASC
```

## Connections to other communities
- 18 edges to [[_COMMUNITY_test_pictures_first.py]]
- 8 edges to [[_COMMUNITY_pathlib]]
- 6 edges to [[_COMMUNITY_json]]
- 3 edges to [[_COMMUNITY_planning]]
- 3 edges to [[_COMMUNITY_gather_pool]]
- 3 edges to [[_COMMUNITY_fake_ai]]
- 3 edges to [[_COMMUNITY_test_rules.py]]
- 3 edges to [[_COMMUNITY_choose_images]]
- 3 edges to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_ffmpeg]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_gpu.py]]
- 1 edge to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_drawn_thumbnail]]
- 1 edge to [[_COMMUNITY_is_usable]]

## Top bridge nodes
- [[prepare_topic()]] - degree 15, connects to 7 communities
- [[load_pool()]] - degree 14, connects to 7 communities
- [[catalog_pool()]] - degree 18, connects to 5 communities
- [[save_pool()]] - degree 13, connects to 4 communities
- [[contact_sheets()]] - degree 6, connects to 3 communities