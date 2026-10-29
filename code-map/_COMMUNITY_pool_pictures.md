---
type: community
members: 16
---

# pool_pictures

**Members:** 16 nodes

## Members
- [[CompletedProcess]] - code
- [[Download ~14s of film around the chosen moment (cropped with FILM_CROP to…]] - rationale - shortsmaker/footage.py
- [[Path_29]] - code
- [[Pool indexes to try for the thumbnail's real photo, best first usable pictures…]] - rationale - shortsmaker/blender_plan.py
- [[Rejected scenes (index - the review's complaint) that get a real picture from…]] - rationale - shortsmaker/review.py
- [[The usable pictures as prompt lines 12 film 1944 newsreel of rubber tanks…]] - rationale - shortsmaker/picture_pool.py
- [[Usable list entries for the topic check all frames of one video count once…]] - rationale - shortsmaker/picture_pool.py
- [[catalog_text()]] - code - shortsmaker/picture_pool.py
- [[ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the…]] - rationale - shortsmaker/image_sources.py
- [[film_ffmpeg()]] - code - shortsmaker/image_sources.py
- [[film_piece()]] - code - shortsmaker/footage.py
- [[is_usable()]] - code - shortsmaker/picture_pool.py
- [[pool_pictures()]] - code - shortsmaker/review.py
- [[test_thumbnail_order_skips_film_and_puts_openers_first()]] - code - tests/test_blender_plan.py
- [[thumbnail_order()]] - code - shortsmaker/blender_plan.py
- [[usable()]] - code - shortsmaker/picture_pool.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/pool_pictures
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_test_full_scenes.py]]
- 3 edges to [[_COMMUNITY_test_pictures_first.py]]
- 2 edges to [[_COMMUNITY_prepare_topic]]
- 2 edges to [[_COMMUNITY_image_sources.py]]
- 2 edges to [[_COMMUNITY_subprocess]]
- 2 edges to [[_COMMUNITY_drawn_thumbnail]]
- 1 edge to [[_COMMUNITY_test_first_second.py]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_edit_scripts]]
- 1 edge to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_visual_review]]
- 1 edge to [[_COMMUNITY_test_blender_plan.py]]

## Top bridge nodes
- [[pool_pictures()]] - degree 10, connects to 7 communities
- [[film_piece()]] - degree 7, connects to 3 communities
- [[catalog_text()]] - degree 5, connects to 3 communities
- [[usable()]] - degree 5, connects to 3 communities
- [[is_usable()]] - degree 6, connects to 2 communities