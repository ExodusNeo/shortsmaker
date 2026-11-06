---
type: community
members: 18
---

# wm_files

**Members:** 18 nodes

## Members
- [[(ok, credit). Public domainCC0 need no credit; all other WikimediaWikipedia…]] - rationale - shortsmaker/image_sources.py
- [[Check every line against the story's Wikipedia articles and rewrite what they…]] - rationale - shortsmaker/writing.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Images used in an English Wikipedia article chosen by editors, so almost…]] - rationale - shortsmaker/image_sources.py
- [[Plain text of an English Wikipedia article ('' when missing or unreachable).]] - rationale - shortsmaker/writing.py
- [[URL of a standard-size Wikimedia thumbnail the largest allowed step that fits…]] - rationale - shortsmaker/image_sources.py
- [[Usable images from a WikimediaWikipedia API query photos, screenshots,…]] - rationale - shortsmaker/image_sources.py
- [[Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable).]] - rationale - shortsmaker/footage.py
- [[article_images()]] - code - shortsmaker/image_sources.py
- [[article_text()]] - code - shortsmaker/writing.py
- [[commons_films()]] - code - shortsmaker/footage.py
- [[commons_search()]] - code - shortsmaker/image_sources.py
- [[fact_check()_1]] - code - shortsmaker/writing.py
- [[test_fact_check_drops_full()]] - code - tests/test_full_scenes.py
- [[thumb_url()]] - code - shortsmaker/image_sources.py
- [[usable_license()]] - code - shortsmaker/image_sources.py
- [[wm_files()]] - code - shortsmaker/image_sources.py
- [[wm_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/wm_files
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_test_full_scenes.py]]
- 3 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_gather_pool]]
- 2 edges to [[_COMMUNITY_extra_sources.py]]
- 2 edges to [[_COMMUNITY_config.py]]
- 1 edge to [[_COMMUNITY_get_image]]
- 1 edge to [[_COMMUNITY_rescue_graphics]]
- 1 edge to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_opener_graphic]]
- 1 edge to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_test_topic_ideas.py]]
- 1 edge to [[_COMMUNITY_test_style.py]]
- 1 edge to [[_COMMUNITY_words_of]]
- 1 edge to [[_COMMUNITY_footage.py]]

## Top bridge nodes
- [[article_text()]] - degree 8, connects to 5 communities
- [[fact_check()_1]] - degree 8, connects to 5 communities
- [[wm_get()]] - degree 8, connects to 4 communities
- [[commons_films()]] - degree 6, connects to 3 communities
- [[wm_files()]] - degree 8, connects to 2 communities