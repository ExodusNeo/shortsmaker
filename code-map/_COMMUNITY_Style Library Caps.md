---
type: community
members: 4
---

# Style Library Caps

**Members:** 4 nodes

## Members
- [[Guardrails for the style library (STYLE_CAPS) the hook keeps only its title…]] - rationale - shortsmaker/plan_rules.py
- [[limit_style()]] - code - shortsmaker/plan_rules.py
- [[scene()]] - code - tests/test_style.py
- [[test_limit_style_caps()]] - code - tests/test_style.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Style_Library_Caps
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_gpu.py]]
- 1 edge to [[_COMMUNITY_test_style.py]]

## Top bridge nodes
- [[limit_style()]] - degree 4, connects to 2 communities
- [[test_limit_style_caps()]] - degree 3, connects to 1 community