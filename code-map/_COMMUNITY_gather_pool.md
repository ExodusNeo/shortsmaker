---
type: community
members: 15
---

# gather_pool

**Members:** 15 nodes

## Members
- [[Candidate pictures (with preview `thumb` bytes) and sampled real-film frames…]] - rationale - shortsmaker/picture_pool.py
- [[Images used in an English Wikipedia article chosen by editors, so almost…]] - rationale - shortsmaker/image_sources.py
- [[Retain productyearcountry details from the director; also search the…]] - rationale - shortsmaker/footage.py
- [[Round-robin sources rather than letting the first provider consume the whole…]] - rationale - shortsmaker/picture_pool.py
- [[URL of a standard-size Wikimedia thumbnail the largest allowed step that fits…]] - rationale - shortsmaker/image_sources.py
- [[Usable images from a WikimediaWikipedia API query photos, screenshots,…]] - rationale - shortsmaker/image_sources.py
- [[add()_1]] - code - shortsmaker/picture_pool.py
- [[article_images()]] - code - shortsmaker/image_sources.py
- [[balanced_candidates()]] - code - shortsmaker/picture_pool.py
- [[commercial_queries()]] - code - shortsmaker/footage.py
- [[commons_search()]] - code - shortsmaker/image_sources.py
- [[gather_pool()]] - code - shortsmaker/picture_pool.py
- [[load_thumb()]] - code - shortsmaker/picture_pool.py
- [[thumb_url()]] - code - shortsmaker/image_sources.py
- [[wm_files()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/gather_pool
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY___init__.py]]
- 5 edges to [[_COMMUNITY_fetch]]
- 4 edges to [[_COMMUNITY_extra_sources.py]]
- 2 edges to [[_COMMUNITY_owner]]
- 2 edges to [[_COMMUNITY_prepare_topic]]
- 2 edges to [[_COMMUNITY_words_of]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_clean_full]]
- 1 edge to [[_COMMUNITY_visual_review]]

## Top bridge nodes
- [[gather_pool()]] - degree 23, connects to 9 communities
- [[wm_files()]] - degree 8, connects to 3 communities
- [[commercial_queries()]] - degree 5, connects to 3 communities
- [[article_images()]] - degree 4, connects to 1 community
- [[commons_search()]] - degree 3, connects to 1 community