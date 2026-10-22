---
type: community
members: 8
---

# fetch

**Members:** 8 nodes

## Members
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[NASA videos (public domain), as their mediumsmall MP4 renditions.]] - rationale - shortsmaker/footage.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[fetch()]] - code - shortsmaker/media_tools.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[nasa_films()]] - code - shortsmaker/footage.py
- [[nasa_search()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/fetch
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_json]]
- 3 edges to [[_COMMUNITY_words_of]]
- 2 edges to [[_COMMUNITY_wm_files]]
- 2 edges to [[_COMMUNITY_gather_pool]]
- 1 edge to [[_COMMUNITY_ffmpeg]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_full_cues]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_film_frames]]

## Top bridge nodes
- [[get_image()]] - degree 8, connects to 5 communities
- [[fetch()]] - degree 11, connects to 4 communities
- [[nasa_films()]] - degree 7, connects to 3 communities
- [[ov_get()]] - degree 5, connects to 2 communities
- [[nasa_search()]] - degree 4, connects to 2 communities