---
type: community
members: 13
---

# on_topic

**Members:** 13 nodes

## Members
- [[Keep titles that share a meaningful word with the query (including 2-3 letter…]] - rationale - shortsmaker/image_sources.py
- [[NASA photos (public domain), when the story touches space, flight or science.]] - rationale - shortsmaker/image_sources.py
- [[NASA videos (public domain), as their mediumsmall MP4 renditions.]] - rationale - shortsmaker/footage.py
- [[NASA's own media is public domain, but its library also holds partner and…]] - rationale - shortsmaker/image_sources.py
- [[The Oxford pool (2026-10-26) got stock videos that only shared a first name or…]] - rationale - tests/test_pictures_first.py
- [[nasa_credit()]] - code - shortsmaker/image_sources.py
- [[nasa_films()]] - code - shortsmaker/footage.py
- [[nasa_images()]] - code - shortsmaker/image_sources.py
- [[nasa_search()]] - code - shortsmaker/image_sources.py
- [[on_topic()]] - code - shortsmaker/image_sources.py
- [[pixabay_images()]] - code - shortsmaker/extra_sources.py
- [[test_nasa_partner_media_is_credited()]] - code - tests/test_full_scenes.py
- [[test_on_topic_ignores_a_lone_shared_name()]] - code - tests/test_pictures_first.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/on_topic
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_extra_sources.py]]
- 5 edges to [[_COMMUNITY_test_full_scenes.py]]
- 3 edges to [[_COMMUNITY_fetch]]
- 3 edges to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_ffmpeg]]
- 1 edge to [[_COMMUNITY_archive_films]]
- 1 edge to [[_COMMUNITY_gather_pool]]
- 1 edge to [[_COMMUNITY_wm_files]]
- 1 edge to [[_COMMUNITY_clean_full]]
- 1 edge to [[_COMMUNITY_test_pictures_first.py]]

## Top bridge nodes
- [[on_topic()]] - degree 11, connects to 6 communities
- [[nasa_films()]] - degree 8, connects to 3 communities
- [[nasa_images()]] - degree 6, connects to 2 communities
- [[nasa_search()]] - degree 4, connects to 2 communities
- [[pixabay_images()]] - degree 6, connects to 1 community