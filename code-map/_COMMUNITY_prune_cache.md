---
type: community
members: 3
---

# prune_cache

**Members:** 3 nodes

## Members
- [[Drop cached downloads and topic pools older than 30 days.]] - rationale - shortsmaker/picture_pool.py
- [[prune_cache()]] - code - shortsmaker/picture_pool.py
- [[test_prune_cache_handles_pools()]] - code - tests/test_pictures_first.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/prune_cache
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_gpu.py]]
- 1 edge to [[_COMMUNITY_main_1]]
- 1 edge to [[_COMMUNITY_picture_pool.py]]
- 1 edge to [[_COMMUNITY_test_pictures_first.py]]

## Top bridge nodes
- [[prune_cache()]] - degree 6, connects to 3 communities
- [[test_prune_cache_handles_pools()]] - degree 2, connects to 1 community