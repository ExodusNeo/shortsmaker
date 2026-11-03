---
type: community
members: 22
---

# fetch

**Members:** 22 nodes

## Members
- [[(ok, credit). Public domainCC0 need no credit; all other WikimediaWikipedia…]] - rationale - shortsmaker/image_sources.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Keep titles that share a meaningful word with the query (including 2-3 letter…]] - rationale - shortsmaker/image_sources.py
- [[NASA photos (public domain), when the story touches space, flight or science.]] - rationale - shortsmaker/image_sources.py
- [[NASA videos (public domain), as their mediumsmall MP4 renditions.]] - rationale - shortsmaker/footage.py
- [[Still images, magazinemanual scans, art and archival photos from the Internet…]] - rationale - shortsmaker/image_sources.py
- [[The Oxford pool (2026-10-26) got stock videos that only shared a first name or…]] - rationale - tests/test_pictures_first.py
- [[Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable).]] - rationale - shortsmaker/footage.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[archive_images()]] - code - shortsmaker/image_sources.py
- [[commons_films()]] - code - shortsmaker/footage.py
- [[fetch()]] - code - shortsmaker/media_tools.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[nasa_films()]] - code - shortsmaker/footage.py
- [[nasa_images()]] - code - shortsmaker/image_sources.py
- [[nasa_search()]] - code - shortsmaker/image_sources.py
- [[on_topic()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[test_on_topic_ignores_a_lone_shared_name()]] - code - tests/test_pictures_first.py
- [[usable_license()]] - code - shortsmaker/image_sources.py
- [[wm_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/fetch
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_test_full_scenes.py]]
- 7 edges to [[_COMMUNITY_re]]
- 5 edges to [[_COMMUNITY_gather_pool]]
- 3 edges to [[_COMMUNITY_json]]
- 3 edges to [[_COMMUNITY_extra_sources.py]]
- 2 edges to [[_COMMUNITY_words_of]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_test_topic_ideas.py]]
- 1 edge to [[_COMMUNITY_write_json]]
- 1 edge to [[_COMMUNITY_recover_downloads]]
- 1 edge to [[_COMMUNITY_full_props]]
- 1 edge to [[_COMMUNITY_test_blender_plan.py]]
- 1 edge to [[_COMMUNITY_rescue_graphics]]
- 1 edge to [[_COMMUNITY_audio_library.py]]
- 1 edge to [[_COMMUNITY_test_pictures_first.py]]

## Top bridge nodes
- [[fetch()]] - degree 14, connects to 5 communities
- [[get_image()]] - degree 9, connects to 5 communities
- [[on_topic()]] - degree 11, connects to 4 communities
- [[wm_get()]] - degree 8, connects to 4 communities
- [[nasa_films()]] - degree 7, connects to 3 communities