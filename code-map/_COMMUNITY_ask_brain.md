---
type: community
members: 5
---

# ask_brain

**Members:** 5 nodes

## Members
- [[Ask for a number 1..n (Enter = default, when there is one).]] - rationale - shortsmaker/channel_profiles.py
- [[Who plans this batch (scripts, fact check, SEO, picture choices, AI images)…]] - rationale - shortsmaker/channel_profiles.py
- [[ask_brain()]] - code - shortsmaker/channel_profiles.py
- [[ask_number()]] - code - shortsmaker/channel_profiles.py
- [[test_solo_brain_selection_options()]] - code - tests/test_package.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ask_brain
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_main_1]]
- 1 edge to [[_COMMUNITY_fix_short]]

## Top bridge nodes
- [[ask_brain()]] - degree 5, connects to 2 communities
- [[ask_number()]] - degree 5, connects to 2 communities
- [[test_solo_brain_selection_options()]] - degree 2, connects to 1 community