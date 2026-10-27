---
type: community
members: 12
---

# gather_pool

**Members:** 12 nodes

## Members
- [[Candidate pictures (with preview `thumb` bytes) and sampled real-film frames…]] - rationale - shortsmaker/picture_pool.py
- [[Images used in an English Wikipedia article chosen by editors, so almost…]] - rationale - shortsmaker/image_sources.py
- [[URL of a standard-size Wikimedia thumbnail the largest allowed step that fits…]] - rationale - shortsmaker/image_sources.py
- [[Usable images from a WikimediaWikipedia API query photos, screenshots,…]] - rationale - shortsmaker/image_sources.py
- [[add()_1]] - code - shortsmaker/picture_pool.py
- [[article_images()]] - code - shortsmaker/image_sources.py
- [[commons_search()]] - code - shortsmaker/image_sources.py
- [[gather_pool()]] - code - shortsmaker/picture_pool.py
- [[load_thumb()]] - code - shortsmaker/picture_pool.py
- [[test_gather_pool_skip_and_limits()]] - code - tests/test_pictures_first.py
- [[thumb_url()]] - code - shortsmaker/image_sources.py
- [[wm_files()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/gather_pool
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_fetch]]
- 4 edges to [[_COMMUNITY_pathlib]]
- 3 edges to [[_COMMUNITY_write_scripts]]
- 2 edges to [[_COMMUNITY_owner]]
- 2 edges to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_test_pictures_first.py]]

## Top bridge nodes
- [[gather_pool()]] - degree 17, connects to 7 communities
- [[wm_files()]] - degree 8, connects to 3 communities
- [[test_gather_pool_skip_and_limits()]] - degree 3, connects to 2 communities
- [[article_images()]] - degree 4, connects to 1 community
- [[commons_search()]] - degree 3, connects to 1 community