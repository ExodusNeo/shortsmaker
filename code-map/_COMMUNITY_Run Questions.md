---
type: community
cohesion: 0.50
members: 4
---

# Run Questions

**Cohesion:** 0.50 - moderately connected
**Members:** 4 nodes

## Members
- [[Ask for a number 1..n (Enter = default, when there is one).]] - rationale - shortsmaker/channel_profiles.py
- [[Who plans this batch (scripts, fact check, SEO, picture choices, AI images)…]] - rationale - shortsmaker/channel_profiles.py
- [[ask_brain()]] - code - shortsmaker/channel_profiles.py
- [[ask_number()]] - code - shortsmaker/channel_profiles.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Run_Questions
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Channel Profiles & Menus]]
- 2 edges to [[_COMMUNITY_Entry Point & Run Menus]]

## Top bridge nodes
- [[ask_number()]] - degree 5, connects to 2 communities
- [[ask_brain()]] - degree 4, connects to 2 communities