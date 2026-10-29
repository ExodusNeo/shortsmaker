---
type: community
members: 5
---

# article_text

**Members:** 5 nodes

## Members
- [[Check every line against the story's Wikipedia articles and rewrite what they…]] - rationale - shortsmaker/writing.py
- [[Plain text of an English Wikipedia article ('' when missing or unreachable).]] - rationale - shortsmaker/writing.py
- [[article_text()]] - code - shortsmaker/writing.py
- [[fact_check()]] - code - shortsmaker/writing.py
- [[test_fact_check_drops_full()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/article_text
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_image_sources.py]]
- 1 edge to [[_COMMUNITY_owner]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_gather_pool]]
- 1 edge to [[_COMMUNITY_opener_graphic]]
- 1 edge to [[_COMMUNITY_rescue_graphics]]

## Top bridge nodes
- [[article_text()]] - degree 8, connects to 6 communities
- [[fact_check()]] - degree 8, connects to 5 communities
- [[test_fact_check_drops_full()]] - degree 2, connects to 1 community