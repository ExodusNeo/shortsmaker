---
type: community
cohesion: 0.25
members: 9
---

# Archive Photo Cleanup

**Cohesion:** 0.25 - loosely connected
**Members:** 9 nodes

## Members
- [[A stereograph card two near-identical photos side by side. Compares the…]] - rationale - make_shorts.py
- [[Archive scans look broken on screen with their extras a stereograph card keeps…]] - rationale - make_shorts.py
- [[Cut plain strips (white mounts, black plate edges) off the sides, at most 15%…]] - rationale - make_shorts.py
- [[border()]] - code - make_shorts.py
- [[clean_photo()]] - code - make_shorts.py
- [[detail()]] - code - make_shorts.py
- [[is_stereo()]] - code - make_shorts.py
- [[plain()]] - code - make_shorts.py
- [[trim_borders()]] - code - make_shorts.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Archive_Photo_Cleanup
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Shared Imports & Downloads]]
- 2 edges to [[_COMMUNITY_Python Frame Renderer]]
- 1 edge to [[_COMMUNITY_Quality Checks & Captions]]

## Top bridge nodes
- [[trim_borders()]] - degree 6, connects to 2 communities
- [[clean_photo()]] - degree 5, connects to 2 communities
- [[is_stereo()]] - degree 5, connects to 2 communities