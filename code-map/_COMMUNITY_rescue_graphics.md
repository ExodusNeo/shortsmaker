---
type: community
members: 10
---

# rescue_graphics

**Members:** 10 nodes

## Members
- [[Check every line against the story's Wikipedia articles and rewrite what they…]] - rationale - shortsmaker/writing.py
- [[Plain text of an English Wikipedia article ('' when missing or unreachable).]] - rationale - shortsmaker/writing.py
- [[Scenes whose picture is missing or weak may become a full-screen motion graphic…]] - rationale - shortsmaker/picker.py
- [[The full-screen motion graphic formats the AI may pick from (rescue_graphics,…]] - rationale - shortsmaker/picker.py
- [[article_text()]] - code - shortsmaker/writing.py
- [[fact_check()_1]] - code - shortsmaker/writing.py
- [[full_formats()]] - code - shortsmaker/picker.py
- [[rescue_graphics()]] - code - shortsmaker/picker.py
- [[test_fact_check_drops_full()]] - code - tests/test_full_scenes.py
- [[test_rescue_respects_caps()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/rescue_graphics
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_test_full_scenes.py]]
- 4 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_finish_render]]
- 2 edges to [[_COMMUNITY_clean_full]]
- 2 edges to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_main_1]]
- 1 edge to [[_COMMUNITY_extra_sources.py]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_test_style.py]]

## Top bridge nodes
- [[rescue_graphics()]] - degree 13, connects to 7 communities
- [[article_text()]] - degree 8, connects to 5 communities
- [[fact_check()_1]] - degree 8, connects to 5 communities
- [[full_formats()]] - degree 4, connects to 2 communities
- [[test_fact_check_drops_full()]] - degree 2, connects to 1 community