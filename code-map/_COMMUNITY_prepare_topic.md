---
type: community
members: 23
---

# prepare_topic

**Members:** 23 nodes

## Members
- [[Before writing the topic's Wikipedia research (`_texts`; fact_check() reuses…]] - rationale - shortsmaker/picture_pool.py
- [[Download ~14s of film around the chosen moment (cropped with FILM_CROP to…]] - rationale - shortsmaker/footage.py
- [[Numbered thumbnail grids (6x4) so Claude can look at every candidate at once.]] - rationale - shortsmaker/picture_pool.py
- [[Path_4]] - code
- [[Path_5]] - code
- [[Rejected scenes (index - the review's complaint) that get a real picture from…]] - rationale - shortsmaker/review.py
- [[The planner plans the edit (footage searches, shots, camera, graphics, person…]] - rationale - shortsmaker/writing.py
- [[The saved pool (None if missing or unreadable it is gathered again);…]] - rationale - shortsmaker/picture_pool.py
- [[The topic's usable pictures as prompt lines ( without a picture list).]] - rationale - shortsmaker/picture_pool.py
- [[The usable pictures as prompt lines 12 film 1944 newsreel of rubber tanks…]] - rationale - shortsmaker/picture_pool.py
- [[Usable list entries for the topic check all frames of one video count once…]] - rationale - shortsmaker/picture_pool.py
- [[catalog_text()]] - code - shortsmaker/picture_pool.py
- [[contact_sheets()]] - code - shortsmaker/picture_pool.py
- [[direct_scripts()]] - code - shortsmaker/writing.py
- [[film_piece()]] - code - shortsmaker/footage.py
- [[is_usable()]] - code - shortsmaker/picture_pool.py
- [[load_pool()]] - code - shortsmaker/picture_pool.py
- [[pictures_of()]] - code - shortsmaker/picture_pool.py
- [[pool_folder()]] - code - shortsmaker/picture_pool.py
- [[pool_pictures()]] - code - shortsmaker/review.py
- [[prepare_topic()]] - code - shortsmaker/picture_pool.py
- [[test_empty_pool_drops_topic_without_ai()]] - code - tests/test_pictures_first.py
- [[usable()]] - code - shortsmaker/picture_pool.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/prepare_topic
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_test_pictures_first.py]]
- 9 edges to [[_COMMUNITY___init__.py]]
- 8 edges to [[_COMMUNITY_json]]
- 5 edges to [[_COMMUNITY_write_scripts]]
- 3 edges to [[_COMMUNITY_choose_images]]
- 2 edges to [[_COMMUNITY_test_rules.py]]
- 2 edges to [[_COMMUNITY_gather_pool]]
- 2 edges to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_fetch]]
- 1 edge to [[_COMMUNITY_subprocess]]
- 1 edge to [[_COMMUNITY_test_blender_plan.py]]
- 1 edge to [[_COMMUNITY_test_first_second.py]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_test_story.py]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_get_image]]
- 1 edge to [[_COMMUNITY_style_library]]
- 1 edge to [[_COMMUNITY_ffmpeg]]

## Top bridge nodes
- [[load_pool()]] - degree 14, connects to 8 communities
- [[prepare_topic()]] - degree 15, connects to 6 communities
- [[direct_scripts()]] - degree 7, connects to 5 communities
- [[pool_pictures()]] - degree 10, connects to 4 communities
- [[film_piece()]] - degree 7, connects to 4 communities