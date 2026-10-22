---
type: community
cohesion: 0.13
members: 22
---

# Picture Pool & Catalog

**Cohesion:** 0.13 - loosely connected
**Members:** 22 nodes

## Members
- [[Before writing the topic's Wikipedia research (`_texts`; fact_check() reuses…]] - rationale - shortsmaker/picture_pool.py
- [[Numbered thumbnail grids (6x4) so Claude can look at every candidate at once.]] - rationale - shortsmaker/picture_pool.py
- [[Path_5]] - code
- [[The picture list the writer, editor and director plan with the AI looks at the…]] - rationale - shortsmaker/picture_pool.py
- [[The saved pool (None if missing or unreadable it is gathered again);…]] - rationale - shortsmaker/picture_pool.py
- [[The valid entries of a picture-list reply (LLM output is untrusted).]] - rationale - shortsmaker/picture_pool.py
- [[Write via a temp file, so an interrupted run never leaves a half-written file…]] - rationale - shortsmaker/media_tools.py
- [[catalog_entries()]] - code - shortsmaker/picture_pool.py
- [[catalog_pool()]] - code - shortsmaker/picture_pool.py
- [[contact_sheets()]] - code - shortsmaker/picture_pool.py
- [[load_pool()]] - code - shortsmaker/picture_pool.py
- [[pool.json (the candidates without bytes) + thumbk.jpg; list positions are the…]] - rationale - shortsmaker/picture_pool.py
- [[pool_folder()]] - code - shortsmaker/picture_pool.py
- [[prepare_topic()]] - code - shortsmaker/picture_pool.py
- [[save_pool()]] - code - shortsmaker/picture_pool.py
- [[test_catalog_empty_pool_no_ai()]] - code - tests/test_pictures_first.py
- [[test_catalog_failure_stops()]] - code - tests/test_pictures_first.py
- [[test_corrupt_pool_and_catalog_redone()]] - code - tests/test_pictures_first.py
- [[test_pool_roundtrip()]] - code - tests/test_pictures_first.py
- [[test_pool_rows_without_thumbs()]] - code - tests/test_pictures_first.py
- [[test_small_pool_skips_ai()]] - code - tests/test_pictures_first.py
- [[write_json()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Picture_Pool__Catalog
SORT file.name ASC
```

## Connections to other communities
- 19 edges to [[_COMMUNITY_Pictures-First Tests]]
- 9 edges to [[_COMMUNITY_CLI & Pixabay Films]]
- 3 edges to [[_COMMUNITY_Fake AI Helpers]]
- 3 edges to [[_COMMUNITY_Freesound & Picture Swaps]]
- 3 edges to [[_COMMUNITY_Picture Picker]]
- 2 edges to [[_COMMUNITY_Script Writing Pipeline]]
- 2 edges to [[_COMMUNITY_Audio Mix & Music Gain]]
- 2 edges to [[_COMMUNITY_Usable Picture Checks]]
- 2 edges to [[_COMMUNITY_Scene Cues & Image Search]]
- 1 edge to [[_COMMUNITY_Test Patching Helpers]]
- 1 edge to [[_COMMUNITY_AI Calls & Quota]]
- 1 edge to [[_COMMUNITY_Detail Marks & Storyboard]]
- 1 edge to [[_COMMUNITY_Fact Check]]

## Top bridge nodes
- [[prepare_topic()]] - degree 12, connects to 5 communities
- [[catalog_pool()]] - degree 17, connects to 4 communities
- [[load_pool()]] - degree 10, connects to 4 communities
- [[save_pool()]] - degree 13, connects to 3 communities
- [[contact_sheets()]] - degree 6, connects to 3 communities