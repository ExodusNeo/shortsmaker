---
type: community
members: 4
---

# ov_get

**Members:** 4 nodes

## Members
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ov_get
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_gather_pool]]
- 1 edge to [[_COMMUNITY_get_image]]
- 1 edge to [[_COMMUNITY_fetch]]

## Top bridge nodes
- [[ov_get()]] - degree 5, connects to 3 communities
- [[openverse_images()]] - degree 4, connects to 2 communities