---
type: community
members: 6
---

# pacing_check

**Members:** 6 nodes

## Members
- [[(seconds a callout can be read after its entrance, seconds it needs) the…]] - rationale - shortsmaker/review.py
- [[A kinetic title repeats the spoken words the captions already show; with too…]] - rationale - shortsmaker/short_render.py
- [[Measured reading holds and final-script detours. Editorial defaults, not…]] - rationale - shortsmaker/review.py
- [[callout_hold()]] - code - shortsmaker/review.py
- [[drop_unreadable_kinetic()]] - code - shortsmaker/short_render.py
- [[pacing_check()]] - code - shortsmaker/review.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/pacing_check
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_visual_review]]
- 1 edge to [[_COMMUNITY_finish_render]]

## Top bridge nodes
- [[pacing_check()]] - degree 5, connects to 3 communities
- [[drop_unreadable_kinetic()]] - degree 4, connects to 2 communities
- [[callout_hold()]] - degree 4, connects to 1 community