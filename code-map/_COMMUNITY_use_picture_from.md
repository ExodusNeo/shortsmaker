---
type: community
members: 7
---

# use_picture_from

**Members:** 7 nodes

## Members
- [[A mark card circles a detail of the old picture it must go when the picture…]] - rationale - tests/test_full_scenes.py
- [[fix  auto-fix scene i drops its picture and gets a freshly painted one…]] - rationale - shortsmaker/review.py
- [[fix scene i shows scene k's picture. A real photofilm is a picture choice; an…]] - rationale - shortsmaker/cli.py
- [[paint_new()]] - code - shortsmaker/review.py
- [[test_new_picture_drops_mark()]] - code - tests/test_full_scenes.py
- [[test_paint_new_clears_full()]] - code - tests/test_full_scenes.py
- [[use_picture_from()]] - code - shortsmaker/cli.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/use_picture_from
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_main_1]]
- 1 edge to [[_COMMUNITY_subprocess]]
- 1 edge to [[_COMMUNITY_resume_runs]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_finish_render]]

## Top bridge nodes
- [[use_picture_from()]] - degree 7, connects to 4 communities
- [[paint_new()]] - degree 7, connects to 4 communities
- [[test_new_picture_drops_mark()]] - degree 4, connects to 1 community
- [[test_paint_new_clears_full()]] - degree 3, connects to 1 community