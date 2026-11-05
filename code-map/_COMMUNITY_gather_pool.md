---
type: community
members: 8
---

# gather_pool

**Members:** 8 nodes

## Members
- [[Candidate pictures (with preview `thumb` bytes) and sampled real-film frames…]] - rationale - shortsmaker/picture_pool.py
- [[Round-robin sources rather than letting the first provider consume the whole…]] - rationale - shortsmaker/picture_pool.py
- [[Still images, magazinemanual scans, art and archival photos from the Internet…]] - rationale - shortsmaker/image_sources.py
- [[add()]] - code - shortsmaker/picture_pool.py
- [[archive_images()]] - code - shortsmaker/image_sources.py
- [[balanced_candidates()]] - code - shortsmaker/picture_pool.py
- [[gather_pool()]] - code - shortsmaker/picture_pool.py
- [[load_thumb()]] - code - shortsmaker/picture_pool.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/gather_pool
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_picture_pool.py]]
- 3 edges to [[_COMMUNITY_re]]
- 2 edges to [[_COMMUNITY_fetch]]
- 2 edges to [[_COMMUNITY_wm_files]]
- 2 edges to [[_COMMUNITY_settings]]
- 2 edges to [[_COMMUNITY_prepare_topic]]
- 2 edges to [[_COMMUNITY_owner]]
- 1 edge to [[_COMMUNITY_on_topic]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_get_image]]
- 1 edge to [[_COMMUNITY_extra_sources.py]]
- 1 edge to [[_COMMUNITY_gpu.py]]
- 1 edge to [[_COMMUNITY_test_first_second.py]]

## Top bridge nodes
- [[gather_pool()]] - degree 23, connects to 12 communities
- [[archive_images()]] - degree 6, connects to 4 communities
- [[balanced_candidates()]] - degree 3, connects to 1 community