---
type: community
members: 19
---

# gather_pool

**Members:** 19 nodes

## Members
- [[dot-__enter__()]] - code - tests/test_pictures_first.py
- [[dot-__init__()]] - code - tests/test_pictures_first.py
- [[Candidate pictures (with preview `thumb` bytes) and sampled real-film frames…]] - rationale - shortsmaker/picture_pool.py
- [[Downloads the real photos the picker chose for evidence boards, custom scenes…]] - rationale - shortsmaker/picker.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Replaces the network functions for one test; `calls` records the search queries.]] - rationale - tests/test_pictures_first.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[add()]] - code - shortsmaker/picture_pool.py
- [[full_pictures()]] - code - shortsmaker/picker.py
- [[gather_pool()]] - code - shortsmaker/picture_pool.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[load_thumb()]] - code - shortsmaker/picture_pool.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[stubbed]] - code - tests/test_pictures_first.py
- [[test_board_pictures_attached()]] - code - tests/test_full_scenes.py
- [[test_gather_pool_shape()]] - code - tests/test_pictures_first.py
- [[test_gather_pool_skip_and_limits()]] - code - tests/test_pictures_first.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/gather_pool
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_re]]
- 5 edges to [[_COMMUNITY_choose_images]]
- 3 edges to [[_COMMUNITY_prepare_topic]]
- 3 edges to [[_COMMUNITY_test_pictures_first.py]]
- 3 edges to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_owner]]
- 1 edge to [[_COMMUNITY_fake_ai]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_test_blender_render.py]]
- 1 edge to [[_COMMUNITY_clean_full]]
- 1 edge to [[_COMMUNITY_visual_review]]
- 1 edge to [[_COMMUNITY_full_props]]

## Top bridge nodes
- [[gather_pool()]] - degree 17, connects to 6 communities
- [[stubbed]] - degree 9, connects to 4 communities
- [[get_image()]] - degree 9, connects to 4 communities
- [[full_pictures()]] - degree 5, connects to 2 communities
- [[test_board_pictures_attached()]] - degree 3, connects to 2 communities