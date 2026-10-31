---
type: community
members: 14
---

# rescue_graphics

**Members:** 14 nodes

## Members
- [[Check every line against the story's Wikipedia articles and rewrite what they…]] - rationale - shortsmaker/writing.py
- [[Plain text of an English Wikipedia article ('' when missing or unreachable).]] - rationale - shortsmaker/writing.py
- [[Planned full-screen motion graphics allowed per Short (default MAX_FULL_PLANNED…]] - rationale - shortsmaker/rules.py
- [[Scenes whose picture is missing or weak may become a full-screen motion graphic…]] - rationale - shortsmaker/picker.py
- [[The full-screen motion graphic formats the AI may pick from (rescue_graphics,…]] - rationale - shortsmaker/picker.py
- [[Total full-screen motion graphics (planned + rescued) allowed per Short…]] - rationale - shortsmaker/rules.py
- [[article_text()]] - code - shortsmaker/writing.py
- [[fact_check()_1]] - code - shortsmaker/writing.py
- [[full_formats()]] - code - shortsmaker/picker.py
- [[max_full()]] - code - shortsmaker/rules.py
- [[max_full_planned()]] - code - shortsmaker/rules.py
- [[rescue_graphics()]] - code - shortsmaker/picker.py
- [[test_fact_check_drops_full()]] - code - tests/test_full_scenes.py
- [[test_rescue_respects_caps()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/rescue_graphics
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_test_full_scenes.py]]
- 4 edges to [[_COMMUNITY_re]]
- 3 edges to [[_COMMUNITY_render]]
- 3 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_write_scripts]]
- 2 edges to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_clean_full]]
- 1 edge to [[_COMMUNITY_fix_short]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_test_style.py]]

## Top bridge nodes
- [[rescue_graphics()]] - degree 13, connects to 8 communities
- [[article_text()]] - degree 8, connects to 5 communities
- [[fact_check()_1]] - degree 8, connects to 5 communities
- [[max_full_planned()]] - degree 5, connects to 3 communities
- [[max_full()]] - degree 5, connects to 2 communities