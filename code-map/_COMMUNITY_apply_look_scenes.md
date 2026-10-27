---
type: community
members: 3
---

# apply_look_scenes

**Members:** 3 nodes

## Members
- [[Puts the Short's photo look on the scenes the picker chose for it (it saw the…]] - rationale - shortsmaker/style_lab.py
- [[apply_look_scenes()]] - code - shortsmaker/style_lab.py
- [[test_apply_look_scenes()]] - code - tests/test_style.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/apply_look_scenes
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_shutil]]
- 1 edge to [[_COMMUNITY_test_style.py]]

## Top bridge nodes
- [[apply_look_scenes()]] - degree 4, connects to 2 communities
- [[test_apply_look_scenes()]] - degree 2, connects to 1 community