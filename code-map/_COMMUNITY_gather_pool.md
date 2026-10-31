---
type: community
members: 8
---

# gather_pool

**Members:** 8 nodes

## Members
- [[Candidate pictures (with preview `thumb` bytes) and sampled real-film frames…]] - rationale - shortsmaker/picture_pool.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[add()_1]] - code - shortsmaker/picture_pool.py
- [[gather_pool()]] - code - shortsmaker/picture_pool.py
- [[load_thumb()]] - code - shortsmaker/picture_pool.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/gather_pool
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_image_sources.py]]
- 3 edges to [[_COMMUNITY_owner]]
- 3 edges to [[_COMMUNITY_fetch]]
- 2 edges to [[_COMMUNITY_picture_pool.py]]
- 2 edges to [[_COMMUNITY_words_of]]
- 1 edge to [[_COMMUNITY_plan_rules.py]]
- 1 edge to [[_COMMUNITY_choose_images]]

## Top bridge nodes
- [[gather_pool()]] - degree 17, connects to 7 communities
- [[ov_get()]] - degree 5, connects to 2 communities
- [[openverse_images()]] - degree 4, connects to 1 community