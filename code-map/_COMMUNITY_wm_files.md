---
type: community
members: 11
---

# wm_files

**Members:** 11 nodes

## Members
- [[(ok, credit). Public domainCC0 need no credit; all other WikimediaWikipedia…]] - rationale - shortsmaker/image_sources.py
- [[Images used in an English Wikipedia article chosen by editors, so almost…]] - rationale - shortsmaker/image_sources.py
- [[URL of a standard-size Wikimedia thumbnail the largest allowed step that fits…]] - rationale - shortsmaker/image_sources.py
- [[Usable images from a WikimediaWikipedia API query photos, screenshots,…]] - rationale - shortsmaker/image_sources.py
- [[Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable).]] - rationale - shortsmaker/footage.py
- [[article_images()]] - code - shortsmaker/image_sources.py
- [[commons_films()]] - code - shortsmaker/footage.py
- [[commons_search()]] - code - shortsmaker/image_sources.py
- [[thumb_url()]] - code - shortsmaker/image_sources.py
- [[usable_license()]] - code - shortsmaker/image_sources.py
- [[wm_files()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/wm_files
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_fetch]]
- 2 edges to [[_COMMUNITY_gather_pool]]
- 2 edges to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_on_topic]]
- 1 edge to [[_COMMUNITY_clean_full]]

## Top bridge nodes
- [[wm_files()]] - degree 8, connects to 3 communities
- [[commons_films()]] - degree 6, connects to 3 communities
- [[article_images()]] - degree 4, connects to 2 communities
- [[commons_search()]] - degree 3, connects to 2 communities
- [[usable_license()]] - degree 4, connects to 1 community