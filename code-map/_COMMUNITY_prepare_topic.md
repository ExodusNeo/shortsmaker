---
type: community
members: 16
---

# prepare_topic

**Members:** 16 nodes

## Members
- [[Before writing the topic's Wikipedia research (`_texts`; fact_check() reuses…]] - rationale - shortsmaker/picture_pool.py
- [[Check every line against the story's Wikipedia articles and rewrite what they…]] - rationale - shortsmaker/writing.py
- [[Numbered thumbnail grids (6x4) so Claude can look at every candidate at once.]] - rationale - shortsmaker/picture_pool.py
- [[Path_12]] - code
- [[Plain text of an English Wikipedia article ('' when missing or unreachable).]] - rationale - shortsmaker/writing.py
- [[Verifydownload usable originals while the writer can still avoid unavailable…]] - rationale - shortsmaker/picture_pool.py
- [[article_text()]] - code - shortsmaker/writing.py
- [[contact_sheets()]] - code - shortsmaker/picture_pool.py
- [[fact_check()_1]] - code - shortsmaker/writing.py
- [[pool_folder()]] - code - shortsmaker/picture_pool.py
- [[preflight_pictures()]] - code - shortsmaker/picture_pool.py
- [[prepare_topic()]] - code - shortsmaker/picture_pool.py
- [[test_empty_pool_drops_topic_without_ai()]] - code - tests/test_pictures_first.py
- [[test_fact_check_drops_full()]] - code - tests/test_full_scenes.py
- [[test_small_pool_skips_ai()]] - code - tests/test_pictures_first.py
- [[verify()]] - code - shortsmaker/picture_pool.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/prepare_topic
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_test_pictures_first.py]]
- 7 edges to [[_COMMUNITY_test_full_scenes.py]]
- 4 edges to [[_COMMUNITY_write_scripts]]
- 3 edges to [[_COMMUNITY_gather_pool]]
- 2 edges to [[_COMMUNITY_test_rules.py]]
- 2 edges to [[_COMMUNITY_paint_instead]]
- 2 edges to [[_COMMUNITY_gpu.py]]
- 2 edges to [[_COMMUNITY_clean_pics]]
- 2 edges to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_extra_sources.py]]
- 1 edge to [[_COMMUNITY_finish_render]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_words_of]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_test_style.py]]

## Top bridge nodes
- [[prepare_topic()]] - degree 16, connects to 6 communities
- [[contact_sheets()]] - degree 8, connects to 5 communities
- [[article_text()]] - degree 8, connects to 5 communities
- [[fact_check()_1]] - degree 8, connects to 5 communities
- [[preflight_pictures()]] - degree 7, connects to 3 communities