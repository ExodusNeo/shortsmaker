---
type: community
members: 11
---

# fetch

**Members:** 11 nodes

## Members
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Still images, magazinemanual scans, art and archival photos from the Internet…]] - rationale - shortsmaker/image_sources.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[archive_images()]] - code - shortsmaker/image_sources.py
- [[fetch()]] - code - shortsmaker/media_tools.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[wm_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/fetch
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_test_full_scenes.py]]
- 3 edges to [[_COMMUNITY_on_topic]]
- 3 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_gather_pool]]
- 2 edges to [[_COMMUNITY_wm_files]]
- 1 edge to [[_COMMUNITY_drawn_thumbnail]]
- 1 edge to [[_COMMUNITY_clean_full]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_full_props]]
- 1 edge to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_audio_mix.py]]
- 1 edge to [[_COMMUNITY_article_text]]
- 1 edge to [[_COMMUNITY_download_audio_choices]]
- 1 edge to [[_COMMUNITY_brand_images]]
- 1 edge to [[_COMMUNITY_extra_sources.py]]
- 1 edge to [[_COMMUNITY_archive_films]]
- 1 edge to [[_COMMUNITY_pathlib]]

## Top bridge nodes
- [[fetch()]] - degree 14, connects to 7 communities
- [[get_image()]] - degree 9, connects to 5 communities
- [[wm_get()]] - degree 8, connects to 4 communities
- [[archive_images()]] - degree 6, connects to 4 communities
- [[openverse_images()]] - degree 4, connects to 2 communities