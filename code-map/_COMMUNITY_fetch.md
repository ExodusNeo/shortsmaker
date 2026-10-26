---
type: community
members: 23
---

# fetch

**Members:** 23 nodes

## Members
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Keep titles that share a meaningful word with the query (including 2-3 letter…]] - rationale - shortsmaker/image_sources.py
- [[NASA photos (public domain), when the story touches space, flight or science.]] - rationale - shortsmaker/image_sources.py
- [[NASA videos (public domain), as their mediumsmall MP4 renditions.]] - rationale - shortsmaker/footage.py
- [[Pixabay stock video free to use in videos, no credit needed (Pixabay Content…]] - rationale - shortsmaker/footage.py
- [[Still images, magazinemanual scans, art and archival photos from the Internet…]] - rationale - shortsmaker/image_sources.py
- [[Videos across the entire Internet Archive (historical film, retro gaming,…]] - rationale - shortsmaker/footage.py
- [[Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable).]] - rationale - shortsmaker/footage.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[archive_films()]] - code - shortsmaker/footage.py
- [[archive_images()]] - code - shortsmaker/image_sources.py
- [[commons_films()]] - code - shortsmaker/footage.py
- [[fetch()]] - code - shortsmaker/media_tools.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[nasa_films()]] - code - shortsmaker/footage.py
- [[nasa_images()]] - code - shortsmaker/image_sources.py
- [[nasa_search()]] - code - shortsmaker/image_sources.py
- [[on_topic()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[pixabay_films()]] - code - shortsmaker/footage.py
- [[test_pixabay_keeps_only_on_topic_videos()]] - code - tests/test_pictures_first.py
- [[wm_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/fetch
SORT file.name ASC
```

## Connections to other communities
- 13 edges to [[_COMMUNITY_gpu.py]]
- 5 edges to [[_COMMUNITY_json]]
- 3 edges to [[_COMMUNITY_write_scripts]]
- 3 edges to [[_COMMUNITY_gather_pool]]
- 2 edges to [[_COMMUNITY_test_pictures_first.py]]
- 2 edges to [[_COMMUNITY_wm_files]]
- 1 edge to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_ffmpeg]]
- 1 edge to [[_COMMUNITY_style_lab.py]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_scene_cues]]
- 1 edge to [[_COMMUNITY_fix_short]]
- 1 edge to [[_COMMUNITY_drawn_thumbnail]]
- 1 edge to [[_COMMUNITY_rescue_graphics]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]

## Top bridge nodes
- [[get_image()]] - degree 9, connects to 5 communities
- [[archive_films()]] - degree 7, connects to 4 communities
- [[fetch()]] - degree 11, connects to 3 communities
- [[on_topic()]] - degree 10, connects to 3 communities
- [[pixabay_films()]] - degree 8, connects to 3 communities