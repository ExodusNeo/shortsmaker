---
type: community
cohesion: 0.29
members: 8
---

# Fix.bat Picture Swaps

**Cohesion:** 0.29 - loosely connected
**Members:** 8 nodes

## Members
- [[A mark card circles a detail of the old picture it must go when the picture…]] - rationale - tests/test_full_scenes.py
- [[Path_17]] - code
- [[fix  auto-fix scene i drops its picture and gets a freshly painted one…]] - rationale - shortsmaker/review.py
- [[fix scene i shows scene k's picture. A real photofilm is a picture choice; an…]] - rationale - shortsmaker/cli.py
- [[paint_new()]] - code - shortsmaker/review.py
- [[test_new_picture_drops_mark()]] - code - tests/test_full_scenes.py
- [[test_paint_new_clears_full()]] - code - tests/test_full_scenes.py
- [[use_picture_from()]] - code - shortsmaker/cli.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Fixbat_Picture_Swaps
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Channel Profiles & Menus]]
- 2 edges to [[_COMMUNITY_Entry Point & Run Menus]]
- 2 edges to [[_COMMUNITY_Full Scene Tests]]
- 1 edge to [[_COMMUNITY_Review Auto Fixes]]
- 1 edge to [[_COMMUNITY_Quality & Visual Review]]

## Top bridge nodes
- [[paint_new()]] - degree 7, connects to 4 communities
- [[use_picture_from()]] - degree 7, connects to 2 communities
- [[test_new_picture_drops_mark()]] - degree 4, connects to 1 community
- [[test_paint_new_clears_full()]] - degree 3, connects to 1 community