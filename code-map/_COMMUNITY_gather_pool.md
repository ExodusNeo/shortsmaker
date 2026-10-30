---
type: community
members: 27
---

# gather_pool

**Members:** 27 nodes

## Members
- [[(ok, credit). Public domainCC0 need no credit; all other WikimediaWikipedia…]] - rationale - shortsmaker/image_sources.py
- [[Candidate pictures (with preview `thumb` bytes) and sampled real-film frames…]] - rationale - shortsmaker/picture_pool.py
- [[Downloads the real photos the picker chose for evidence boards, custom scenes…]] - rationale - shortsmaker/picker.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Images used in an English Wikipedia article chosen by editors, so almost…]] - rationale - shortsmaker/image_sources.py
- [[URL of a standard-size Wikimedia thumbnail the largest allowed step that fits…]] - rationale - shortsmaker/image_sources.py
- [[Usable images from a WikimediaWikipedia API query photos, screenshots,…]] - rationale - shortsmaker/image_sources.py
- [[Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable).]] - rationale - shortsmaker/footage.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[add()_1]] - code - shortsmaker/picture_pool.py
- [[article_images()]] - code - shortsmaker/image_sources.py
- [[commons_films()]] - code - shortsmaker/footage.py
- [[commons_search()]] - code - shortsmaker/image_sources.py
- [[full_pictures()]] - code - shortsmaker/picker.py
- [[gather_pool()]] - code - shortsmaker/picture_pool.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[load_thumb()]] - code - shortsmaker/picture_pool.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[test_board_pictures_attached()]] - code - tests/test_full_scenes.py
- [[test_gather_pool_shape()]] - code - tests/test_pictures_first.py
- [[thumb_url()]] - code - shortsmaker/image_sources.py
- [[usable_license()]] - code - shortsmaker/image_sources.py
- [[wm_files()]] - code - shortsmaker/image_sources.py
- [[wm_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/gather_pool
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_pathlib]]
- 6 edges to [[_COMMUNITY_fetch]]
- 3 edges to [[_COMMUNITY_test_full_scenes.py]]
- 3 edges to [[_COMMUNITY_choose_images]]
- 2 edges to [[_COMMUNITY_owner]]
- 2 edges to [[_COMMUNITY_write_scripts]]
- 2 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_plan_rules.py]]
- 1 edge to [[_COMMUNITY_pool_pictures]]
- 1 edge to [[_COMMUNITY_drawn_thumbnail]]
- 1 edge to [[_COMMUNITY_visual_review]]
- 1 edge to [[_COMMUNITY_test_pictures_first.py]]

## Top bridge nodes
- [[gather_pool()]] - degree 17, connects to 8 communities
- [[get_image()]] - degree 9, connects to 5 communities
- [[wm_get()]] - degree 8, connects to 4 communities
- [[commons_films()]] - degree 6, connects to 3 communities
- [[wm_files()]] - degree 8, connects to 2 communities