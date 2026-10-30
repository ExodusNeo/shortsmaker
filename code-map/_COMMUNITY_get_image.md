---
type: community
members: 6
---

# get_image

**Members:** 6 nodes

## Members
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/get_image
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_image_sources.py]]
- 2 edges to [[_COMMUNITY_fetch]]
- 1 edge to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_gather_pool]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_render]]

## Top bridge nodes
- [[get_image()]] - degree 9, connects to 6 communities
- [[ov_get()]] - degree 5, connects to 2 communities
- [[openverse_images()]] - degree 4, connects to 2 communities