---
type: community
members: 10
---

# on_topic

**Members:** 10 nodes

## Members
- [[Keep titles that share a meaningful word with the query (including 2-3 letter…]] - rationale - shortsmaker/image_sources.py
- [[NASA photos (public domain), when the story touches space, flight or science.]] - rationale - shortsmaker/image_sources.py
- [[Still images, magazinemanual scans, art and archival photos from the Internet…]] - rationale - shortsmaker/image_sources.py
- [[The Oxford pool (2026-10-26) got stock videos that only shared a first name or…]] - rationale - tests/test_pictures_first.py
- [[Videos across the entire Internet Archive (historical film, retro gaming,…]] - rationale - shortsmaker/footage.py
- [[archive_films()]] - code - shortsmaker/footage.py
- [[archive_images()]] - code - shortsmaker/image_sources.py
- [[nasa_images()]] - code - shortsmaker/image_sources.py
- [[on_topic()]] - code - shortsmaker/image_sources.py
- [[test_on_topic_ignores_a_lone_shared_name()]] - code - tests/test_pictures_first.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/on_topic
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_image_sources.py]]
- 3 edges to [[_COMMUNITY_plan_rules.py]]
- 2 edges to [[_COMMUNITY_frame_render.py]]
- 2 edges to [[_COMMUNITY_gather_pool]]
- 1 edge to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_test_pictures_first.py]]

## Top bridge nodes
- [[archive_films()]] - degree 7, connects to 5 communities
- [[on_topic()]] - degree 10, connects to 3 communities
- [[archive_images()]] - degree 6, connects to 3 communities
- [[nasa_images()]] - degree 5, connects to 2 communities
- [[test_on_topic_ignores_a_lone_shared_name()]] - degree 3, connects to 1 community