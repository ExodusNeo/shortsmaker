---
type: community
members: 6
---

# lint

**Members:** 6 nodes

## Members
- [[Rule breaks in an AI-written cut-out module (the drawn opener's code rules,…]] - rationale - shortsmaker/opener3d.py
- [[Rule breaks in an AI-written scene (KIT.md's code rules). Empty = clean.]] - rationale - shortsmaker/drawn_opener.py
- [[lint()]] - code - shortsmaker/drawn_opener.py
- [[lint_cutout()]] - code - shortsmaker/opener3d.py
- [[test_lint()]] - code - tests/test_drawn_opener.py
- [[test_lint_needs_draw()]] - code - tests/test_opener3d.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/lint
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_re]]
- 2 edges to [[_COMMUNITY_test_opener3d.py]]
- 1 edge to [[_COMMUNITY_make_opener]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]

## Top bridge nodes
- [[lint()]] - degree 6, connects to 2 communities
- [[lint_cutout()]] - degree 5, connects to 2 communities
- [[test_lint()]] - degree 2, connects to 1 community
- [[test_lint_needs_draw()]] - degree 2, connects to 1 community