---
type: community
cohesion: 0.29
members: 7
---

# Graphics Rescue Caps

**Cohesion:** 0.29 - loosely connected
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
TABLE source_file, type FROM #community/Graphics_Rescue_Caps
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_CLI, Config and Footage]]
- 2 edges to [[_COMMUNITY_Script Sounds and Graphics]]
- 2 edges to [[_COMMUNITY_Obsidian Vault Logbook]]
- 1 edge to [[_COMMUNITY_Headless AI Planner Calls]]
- 1 edge to [[_COMMUNITY_Full-Screen Graphic Validation]]
- 1 edge to [[_COMMUNITY_Stock Video Sources]]
- 1 edge to [[_COMMUNITY_Sound Effects and Credits]]
- 1 edge to [[_COMMUNITY_Main Entry and Channel Profiles]]
- 1 edge to [[_COMMUNITY_Review Auto-Fixes]]
- 1 edge to [[_COMMUNITY_Local Voice and Freesound]]

## Top bridge nodes
- [[rescue_graphics()]] - degree 12, connects to 9 communities
- [[max_full_planned()]] - degree 5, connects to 3 communities
- [[max_full()]] - degree 5, connects to 2 communities
- [[test_rescue_respects_caps()]] - degree 2, connects to 1 community