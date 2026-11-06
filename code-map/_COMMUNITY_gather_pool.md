---
type: community
members: 36
---

# gather_pool

**Members:** 36 nodes

## Members
- [[(ok, credit). Public domainCC0 need no credit; all other WikimediaWikipedia…]] - rationale - shortsmaker/image_sources.py
- [[dot-__enter__()_1]] - code - tests/test_pictures_first.py
- [[dot-__init__()_2]] - code - tests/test_pictures_first.py
- [[Bounded retry; Wikimedia already handles its own rate limits and retries.]] - rationale - shortsmaker/picker.py
- [[Candidate pictures (with preview `thumb` bytes) and sampled real-film frames…]] - rationale - shortsmaker/picture_pool.py
- [[Downloads the real photos the picker chose for evidence boards, custom scenes…]] - rationale - shortsmaker/picker.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Images used in an English Wikipedia article chosen by editors, so almost…]] - rationale - shortsmaker/image_sources.py
- [[Replaces the network functions for one test; `calls` records the search queries.]] - rationale - tests/test_pictures_first.py
- [[Round-robin sources rather than letting the first provider consume the whole…]] - rationale - shortsmaker/picture_pool.py
- [[URL of a standard-size Wikimedia thumbnail the largest allowed step that fits…]] - rationale - shortsmaker/image_sources.py
- [[Usable images from a WikimediaWikipedia API query photos, screenshots,…]] - rationale - shortsmaker/image_sources.py
- [[Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable).]] - rationale - shortsmaker/footage.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[add()]] - code - shortsmaker/picture_pool.py
- [[article_images()]] - code - shortsmaker/image_sources.py
- [[balanced_candidates()]] - code - shortsmaker/picture_pool.py
- [[commons_films()]] - code - shortsmaker/footage.py
- [[commons_search()]] - code - shortsmaker/image_sources.py
- [[download_picture()]] - code - shortsmaker/picker.py
- [[full_pictures()]] - code - shortsmaker/picker.py
- [[gather_pool()]] - code - shortsmaker/picture_pool.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[load_thumb()]] - code - shortsmaker/picture_pool.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[stubbed]] - code - tests/test_pictures_first.py
- [[test_board_pictures_attached()]] - code - tests/test_full_scenes.py
- [[test_gather_pool_shape()]] - code - tests/test_pictures_first.py
- [[test_gather_pool_skip_and_limits()]] - code - tests/test_pictures_first.py
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
- 8 edges to [[_COMMUNITY_extra_sources.py]]
- 5 edges to [[_COMMUNITY_choose_images]]
- 4 edges to [[_COMMUNITY_test_pictures_first.py]]
- 4 edges to [[_COMMUNITY_test_full_scenes.py]]
- 3 edges to [[_COMMUNITY_prepare_topic]]
- 3 edges to [[_COMMUNITY_re]]
- 2 edges to [[_COMMUNITY_owner]]
- 2 edges to [[_COMMUNITY_words_of]]
- 1 edge to [[_COMMUNITY_full_props]]
- 1 edge to [[_COMMUNITY_finish_render]]
- 1 edge to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_footage.py]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_drawn_thumbnail]]
- 1 edge to [[_COMMUNITY_clean_full]]

## Top bridge nodes
- [[gather_pool()]] - degree 23, connects to 8 communities
- [[stubbed]] - degree 9, connects to 4 communities
- [[get_image()]] - degree 9, connects to 4 communities
- [[wm_get()]] - degree 8, connects to 4 communities
- [[commons_films()]] - degree 6, connects to 3 communities