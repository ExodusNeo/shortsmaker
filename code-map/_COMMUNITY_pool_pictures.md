---
type: community
members: 16
---

# pool_pictures

**Members:** 16 nodes

## Members
- [[CompletedProcess]] - code
- [[Download ~14s of film around the chosen moment (cropped with FILM_CROP to…]] - rationale - shortsmaker/footage.py
- [[Downloads the real photos the picker chose for evidence boards, custom scenes…]] - rationale - shortsmaker/picker.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Rejected scenes (index - the review's complaint) that get a real picture from…]] - rationale - shortsmaker/review.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the…]] - rationale - shortsmaker/image_sources.py
- [[film_ffmpeg()]] - code - shortsmaker/image_sources.py
- [[film_piece()]] - code - shortsmaker/footage.py
- [[full_pictures()]] - code - shortsmaker/picker.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[pool_pictures()]] - code - shortsmaker/review.py
- [[test_board_pictures_attached()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/pool_pictures
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_image_sources.py]]
- 4 edges to [[_COMMUNITY_test_full_scenes.py]]
- 3 edges to [[_COMMUNITY_choose_images]]
- 2 edges to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_gather_pool]]
- 1 edge to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_clean_pics]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_full_props]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_drawn_thumbnail]]
- 1 edge to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_visual_review]]

## Top bridge nodes
- [[pool_pictures()]] - degree 10, connects to 7 communities
- [[get_image()]] - degree 9, connects to 3 communities
- [[film_piece()]] - degree 7, connects to 3 communities
- [[full_pictures()]] - degree 5, connects to 2 communities
- [[openverse_images()]] - degree 4, connects to 2 communities