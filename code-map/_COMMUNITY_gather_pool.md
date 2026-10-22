---
type: community
members: 10
---

# gather_pool

**Members:** 10 nodes

## Members
- [[Candidate pictures (with preview `thumb` bytes) and sampled real-film frames…]] - rationale - shortsmaker/picture_pool.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Images used in an English Wikipedia article chosen by editors, so almost…]] - rationale - shortsmaker/image_sources.py
- [[NASA photos (public domain), when the story touches space, flight or science.]] - rationale - shortsmaker/image_sources.py
- [[add()_1]] - code - shortsmaker/picture_pool.py
- [[article_images()]] - code - shortsmaker/image_sources.py
- [[gather_pool()]] - code - shortsmaker/picture_pool.py
- [[load_thumb()]] - code - shortsmaker/picture_pool.py
- [[nasa_images()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/gather_pool
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_json]]
- 3 edges to [[_COMMUNITY_words_of]]
- 2 edges to [[_COMMUNITY_fetch]]
- 2 edges to [[_COMMUNITY_prepare_topic]]
- 2 edges to [[_COMMUNITY_owner]]
- 2 edges to [[_COMMUNITY_wm_files]]
- 1 edge to [[_COMMUNITY_clean_full]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]

## Top bridge nodes
- [[gather_pool()]] - degree 17, connects to 8 communities
- [[nasa_images()]] - degree 5, connects to 3 communities
- [[article_images()]] - degree 4, connects to 2 communities
- [[openverse_images()]] - degree 4, connects to 2 communities