---
type: community
cohesion: 0.22
members: 11
---

# Photo Cleanup

**Cohesion:** 0.22 - loosely connected
**Members:** 11 nodes

## Members
- [[A stereograph card two near-identical photos side by side. Compares the…]] - rationale - shortsmaker/photo_prep.py
- [[Archive scans look broken on screen with their extras a stereograph card keeps…]] - rationale - shortsmaker/photo_prep.py
- [[Cut plain strips (white mounts, black plate edges) off the sides, at most 15%…]] - rationale - shortsmaker/photo_prep.py
- [[Image_1]] - code
- [[border()]] - code - shortsmaker/photo_prep.py
- [[clean_photo()]] - code - shortsmaker/photo_prep.py
- [[detail()]] - code - shortsmaker/photo_prep.py
- [[is_stereo()]] - code - shortsmaker/photo_prep.py
- [[plain()]] - code - shortsmaker/photo_prep.py
- [[statistics]] - concept
- [[trim_borders()]] - code - shortsmaker/photo_prep.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Photo_Cleanup
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Config & Palettes]]
- 1 edge to [[_COMMUNITY_Detail Marks & Storyboard]]

## Top bridge nodes
- [[clean_photo()]] - degree 5, connects to 2 communities
- [[is_stereo()]] - degree 6, connects to 1 community
- [[trim_borders()]] - degree 6, connects to 1 community
- [[statistics]] - degree 2, connects to 1 community