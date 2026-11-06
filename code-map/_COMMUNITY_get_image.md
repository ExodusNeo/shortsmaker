---
type: community
members: 15
---

# get_image

**Members:** 15 nodes

## Members
- [[(ok, credit). Public domainCC0 need no credit; all other WikimediaWikipedia…]] - rationale - shortsmaker/image_sources.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Images used in an English Wikipedia article chosen by editors, so almost…]] - rationale - shortsmaker/image_sources.py
- [[URL of a standard-size Wikimedia thumbnail the largest allowed step that fits…]] - rationale - shortsmaker/image_sources.py
- [[Usable images from a WikimediaWikipedia API query photos, screenshots,…]] - rationale - shortsmaker/image_sources.py
- [[Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable).]] - rationale - shortsmaker/footage.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[article_images()]] - code - shortsmaker/image_sources.py
- [[commons_films()]] - code - shortsmaker/footage.py
- [[commons_search()]] - code - shortsmaker/image_sources.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[thumb_url()]] - code - shortsmaker/image_sources.py
- [[usable_license()]] - code - shortsmaker/image_sources.py
- [[wm_files()]] - code - shortsmaker/image_sources.py
- [[wm_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/get_image
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_test_full_scenes.py]]
- 3 edges to [[_COMMUNITY_fetch]]
- 2 edges to [[_COMMUNITY_gather_pool]]
- 1 edge to [[_COMMUNITY_drawn_thumbnail]]
- 1 edge to [[_COMMUNITY_ov_get]]
- 1 edge to [[_COMMUNITY_opener_graphic]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_clean_full]]
- 1 edge to [[_COMMUNITY_test_topic_ideas.py]]
- 1 edge to [[_COMMUNITY_audio_library.py]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_json]]

## Top bridge nodes
- [[get_image()]] - degree 9, connects to 7 communities
- [[wm_get()]] - degree 8, connects to 4 communities
- [[commons_films()]] - degree 6, connects to 3 communities
- [[wm_files()]] - degree 8, connects to 2 communities
- [[article_images()]] - degree 4, connects to 2 communities