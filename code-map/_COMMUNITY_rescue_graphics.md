---
type: community
members: 7
---

# rescue_graphics

**Members:** 7 nodes

## Members
- [[Planned full-screen motion graphics allowed per Short (default MAX_FULL_PLANNED…]] - rationale - shortsmaker/rules.py
- [[Scenes whose picture is missing or weak may become a full-screen motion graphic…]] - rationale - shortsmaker/picker.py
- [[Total full-screen motion graphics (planned + rescued) allowed per Short…]] - rationale - shortsmaker/rules.py
- [[max_full()]] - code - shortsmaker/rules.py
- [[max_full_planned()]] - code - shortsmaker/rules.py
- [[rescue_graphics()]] - code - shortsmaker/picker.py
- [[test_rescue_respects_caps()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/rescue_graphics
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_blender_link.py]]
- 2 edges to [[_COMMUNITY_plan_rules.py]]
- 2 edges to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_test_rules.py]]
- 1 edge to [[_COMMUNITY_code_custom_scenes]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_write_scripts]]

## Top bridge nodes
- [[rescue_graphics()]] - degree 13, connects to 8 communities
- [[max_full_planned()]] - degree 5, connects to 3 communities
- [[max_full()]] - degree 5, connects to 2 communities
- [[test_rescue_respects_caps()]] - degree 2, connects to 1 community