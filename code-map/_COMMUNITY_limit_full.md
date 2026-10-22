---
type: community
members: 3
---

# limit_full

**Members:** 3 nodes

## Members
- [[Never scene 1 (real footage keeps the hook), never two in a row, never a scene…]] - rationale - shortsmaker/plan_rules.py
- [[limit_full()]] - code - shortsmaker/plan_rules.py
- [[test_limit_full()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/limit_full
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_plan_rules.py]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]

## Top bridge nodes
- [[limit_full()]] - degree 4, connects to 2 communities
- [[test_limit_full()]] - degree 2, connects to 1 community