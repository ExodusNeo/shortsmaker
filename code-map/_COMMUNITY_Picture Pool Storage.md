---
type: community
cohesion: 0.12
members: 24
---

# Picture Pool Storage

**Cohesion:** 0.12 - loosely connected
**Members:** 24 nodes

## Members
- [[Before writing the topic's Wikipedia research (`_texts`; fact_check() reuses…]] - rationale - shortsmaker/picture_pool.py
- [[Numbered thumbnail grids (6x4) so Claude can look at every candidate at once.]] - rationale - shortsmaker/picture_pool.py
- [[Path_6]] - code
- [[Path_7]] - code
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
- [[test_min_pictures_from_settings()]] - code - tests/test_rules.py
- [[test_pool_roundtrip()]] - code - tests/test_pictures_first.py
- [[test_pool_rows_without_thumbs()]] - code - tests/test_pictures_first.py
- [[test_small_pool_skips_ai()]] - code - tests/test_pictures_first.py
- [[write_json()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Picture_Pool_Storage
SORT file.name ASC
```

## Connections to other communities
- 13 edges to [[_COMMUNITY_Director Picture Cleanup Tests]]
- 9 edges to [[_COMMUNITY_Pictures-First Pool Tests]]
- 8 edges to [[_COMMUNITY_CLI, Config and Footage]]
- 4 edges to [[_COMMUNITY_Local Voice and Freesound]]
- 3 edges to [[_COMMUNITY_Wikimedia Image Search]]
- 3 edges to [[_COMMUNITY_Fake AI Test Helpers]]
- 3 edges to [[_COMMUNITY_Channel Rules Files]]
- 2 edges to [[_COMMUNITY_Topic Planning Tests]]
- 2 edges to [[_COMMUNITY_Audio Mix and Shotcut Export]]
- 2 edges to [[_COMMUNITY_Usable Picture Catalog]]
- 2 edges to [[_COMMUNITY_TTS and Story Sounds]]
- 2 edges to [[_COMMUNITY_Script Sounds and Graphics]]
- 1 edge to [[_COMMUNITY_Headless AI Planner Calls]]
- 1 edge to [[_COMMUNITY_Main Entry and Channel Profiles]]
- 1 edge to [[_COMMUNITY_Review Auto-Fixes]]
- 1 edge to [[_COMMUNITY_Blender Build Planning]]
- 1 edge to [[_COMMUNITY_Stock Video Sources]]

## Top bridge nodes
- [[load_pool()]] - degree 14, connects to 8 communities
- [[prepare_topic()]] - degree 15, connects to 7 communities
- [[catalog_pool()]] - degree 18, connects to 6 communities
- [[save_pool()]] - degree 13, connects to 3 communities
- [[test_corrupt_pool_and_catalog_redone()]] - degree 7, connects to 3 communities