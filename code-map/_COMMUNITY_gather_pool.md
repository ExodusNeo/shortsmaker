---
type: community
members: 14
---

# gather_pool

**Members:** 14 nodes

## Members
- [[Candidate pictures (with preview `thumb` bytes) and sampled real-film frames…]] - rationale - shortsmaker/picture_pool.py
- [[Images used in an English Wikipedia article chosen by editors, so almost…]] - rationale - shortsmaker/image_sources.py
- [[Round-robin sources rather than letting the first provider consume the whole…]] - rationale - shortsmaker/picture_pool.py
- [[URL of a standard-size Wikimedia thumbnail the largest allowed step that fits…]] - rationale - shortsmaker/image_sources.py
- [[Usable images from a WikimediaWikipedia API query photos, screenshots,…]] - rationale - shortsmaker/image_sources.py
- [[add()]] - code - shortsmaker/picture_pool.py
- [[article_images()]] - code - shortsmaker/image_sources.py
- [[balanced_candidates()]] - code - shortsmaker/picture_pool.py
- [[commons_search()]] - code - shortsmaker/image_sources.py
- [[gather_pool()]] - code - shortsmaker/picture_pool.py
- [[load_thumb()]] - code - shortsmaker/picture_pool.py
- [[test_gather_pool_shape()]] - code - tests/test_pictures_first.py
- [[thumb_url()]] - code - shortsmaker/image_sources.py
- [[wm_files()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/gather_pool
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_writing.py]]
- 4 edges to [[_COMMUNITY_fetch]]
- 3 edges to [[_COMMUNITY_clean_full]]
- 2 edges to [[_COMMUNITY_owner]]
- 2 edges to [[_COMMUNITY_brand_images]]
- 2 edges to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_load_pool]]
- 1 edge to [[_COMMUNITY_clean_photo]]
- 1 edge to [[_COMMUNITY_extra_sources.py]]
- 1 edge to [[_COMMUNITY_footage.py]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_visual_review]]
- 1 edge to [[_COMMUNITY_test_pictures_first.py]]

## Top bridge nodes
- [[gather_pool()]] - degree 23, connects to 12 communities
- [[wm_files()]] - degree 8, connects to 4 communities
- [[test_gather_pool_shape()]] - degree 3, connects to 2 communities
- [[article_images()]] - degree 4, connects to 1 community
- [[commons_search()]] - degree 3, connects to 1 community