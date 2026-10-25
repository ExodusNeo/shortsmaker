---
type: community
cohesion: 0.67
members: 3
---

# Full Graphic Limits

**Cohesion:** 0.67 - moderately connected
**Members:** 3 nodes

## Members
- [[Never scene 1 (real footage keeps the hook), never two in a row, never a scene…]] - rationale - shortsmaker/plan_rules.py
- [[limit_full()]] - code - shortsmaker/plan_rules.py
- [[test_limit_full()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Full_Graphic_Limits
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_CLI, Config and Footage]]
- 1 edge to [[_COMMUNITY_Script Sounds and Graphics]]

## Top bridge nodes
- [[limit_full()]] - degree 4, connects to 2 communities
- [[test_limit_full()]] - degree 2, connects to 1 community