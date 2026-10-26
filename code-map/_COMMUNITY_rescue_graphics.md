---
type: community
members: 8
---

# rescue_graphics

**Members:** 8 nodes

## Members
- [[Check every line against the story's Wikipedia articles and rewrite what they…]] - rationale - shortsmaker/writing.py
- [[Plain text of an English Wikipedia article ('' when missing or unreachable).]] - rationale - shortsmaker/writing.py
- [[Scenes whose picture is missing or weak may become a full-screen motion graphic…]] - rationale - shortsmaker/picker.py
- [[article_text()]] - code - shortsmaker/writing.py
- [[fact_check()]] - code - shortsmaker/writing.py
- [[rescue_graphics()]] - code - shortsmaker/picker.py
- [[test_fact_check_drops_full()]] - code - tests/test_full_scenes.py
- [[test_rescue_respects_caps()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/rescue_graphics
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_json]]
- 3 edges to [[_COMMUNITY_re]]
- 3 edges to [[_COMMUNITY_gpu.py]]
- 2 edges to [[_COMMUNITY_test_package.py]]
- 2 edges to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_catalog_pool]]
- 1 edge to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_clean_full]]
- 1 edge to [[_COMMUNITY_words_of]]
- 1 edge to [[_COMMUNITY_image_sources.py]]
- 1 edge to [[_COMMUNITY_test_style.py]]

## Top bridge nodes
- [[rescue_graphics()]] - degree 12, connects to 6 communities
- [[fact_check()]] - degree 8, connects to 5 communities
- [[article_text()]] - degree 7, connects to 4 communities
- [[test_fact_check_drops_full()]] - degree 2, connects to 1 community
- [[test_rescue_respects_caps()]] - degree 2, connects to 1 community