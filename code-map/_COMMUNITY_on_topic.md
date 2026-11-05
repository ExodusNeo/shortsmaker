---
type: community
members: 8
---

# on_topic

**Members:** 8 nodes

## Members
- [[Keep titles that share a meaningful word with the query (including 2-3 letter…]] - rationale - shortsmaker/image_sources.py
- [[Pixabay stock video free to use in videos, no credit needed (Pixabay Content…]] - rationale - shortsmaker/footage.py
- [[The Oxford pool (2026-10-26) got stock videos that only shared a first name or…]] - rationale - tests/test_pictures_first.py
- [[on_topic()]] - code - shortsmaker/image_sources.py
- [[pixabay_films()]] - code - shortsmaker/footage.py
- [[pixabay_images()]] - code - shortsmaker/extra_sources.py
- [[test_on_topic_ignores_a_lone_shared_name()]] - code - tests/test_pictures_first.py
- [[test_pixabay_keeps_only_on_topic_videos()]] - code - tests/test_pictures_first.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/on_topic
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_extra_sources.py]]
- 3 edges to [[_COMMUNITY_fetch]]
- 2 edges to [[_COMMUNITY_gpu.py]]
- 2 edges to [[_COMMUNITY_picture_pool.py]]
- 2 edges to [[_COMMUNITY_test_pictures_first.py]]
- 1 edge to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_settings]]
- 1 edge to [[_COMMUNITY_wm_files]]
- 1 edge to [[_COMMUNITY_gather_pool]]
- 1 edge to [[_COMMUNITY_re]]

## Top bridge nodes
- [[on_topic()]] - degree 11, connects to 6 communities
- [[pixabay_films()]] - degree 8, connects to 4 communities
- [[pixabay_images()]] - degree 6, connects to 1 community
- [[test_on_topic_ignores_a_lone_shared_name()]] - degree 3, connects to 1 community
- [[test_pixabay_keeps_only_on_topic_videos()]] - degree 2, connects to 1 community