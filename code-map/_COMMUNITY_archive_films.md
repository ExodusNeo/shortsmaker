---
type: community
members: 5
---

# archive_films

**Members:** 5 nodes

## Members
- [[Videos across the entire Internet Archive (historical film, retro gaming,…]] - rationale - shortsmaker/footage.py
- [[archive_ad_films()]] - code - shortsmaker/footage.py
- [[archive_films()]] - code - shortsmaker/footage.py
- [[duke_films()]] - code - shortsmaker/footage.py
- [[source_enabled()]] - code - shortsmaker/media_library.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/archive_films
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_json]]
- 3 edges to [[_COMMUNITY_brand_images]]
- 2 edges to [[_COMMUNITY_re]]
- 2 edges to [[_COMMUNITY_extra_sources.py]]
- 1 edge to [[_COMMUNITY_fetch]]
- 1 edge to [[_COMMUNITY_clean_full]]
- 1 edge to [[_COMMUNITY_on_topic]]
- 1 edge to [[_COMMUNITY_gather_pool]]

## Top bridge nodes
- [[archive_films()]] - degree 9, connects to 5 communities
- [[source_enabled()]] - degree 8, connects to 4 communities
- [[duke_films()]] - degree 3, connects to 1 community
- [[archive_ad_films()]] - degree 2, connects to 1 community