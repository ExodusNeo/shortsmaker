---
type: community
cohesion: 0.33
members: 7
---

# Repaint & Scene Swap

**Cohesion:** 0.33 - loosely connected
**Members:** 7 nodes

## Members
- [[A mark card circles a detail of the old picture it must go when the picture…]] - rationale - tests/test_full_scenes.py
- [[fix  auto-fix scene i drops its picture and gets a freshly painted one…]] - rationale - make_shorts.py
- [[fix scene i shows scene k's picture. A real photofilm is a picture choice; an…]] - rationale - make_shorts.py
- [[paint_new()]] - code - make_shorts.py
- [[test_new_picture_drops_mark()]] - code - tests/test_full_scenes.py
- [[test_paint_new_clears_full()]] - code - tests/test_full_scenes.py
- [[use_picture_from()]] - code - make_shorts.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Repaint__Scene_Swap
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Run Menu & Channel Setup]]
- 2 edges to [[_COMMUNITY_State & Logbook Helpers]]
- 2 edges to [[_COMMUNITY_Shared Imports & Downloads]]
- 2 edges to [[_COMMUNITY_Full-Scene Validation]]
- 1 edge to [[_COMMUNITY_Automatic Review Fixes]]

## Top bridge nodes
- [[paint_new()]] - degree 7, connects to 4 communities
- [[use_picture_from()]] - degree 6, connects to 3 communities
- [[test_new_picture_drops_mark()]] - degree 4, connects to 1 community
- [[test_paint_new_clears_full()]] - degree 3, connects to 1 community