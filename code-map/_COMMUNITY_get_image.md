---
type: community
members: 13
---

# get_image

**Members:** 13 nodes

## Members
- [[Bounded retry; Wikimedia already handles its own rate limits and retries.]] - rationale - shortsmaker/picker.py
- [[Downloads the real photos the picker chose for evidence boards, custom scenes…]] - rationale - shortsmaker/picker.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[_board()]] - code - tests/test_full_scenes.py
- [[download_picture()]] - code - shortsmaker/picker.py
- [[full_pictures()]] - code - shortsmaker/picker.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[test_board_pictures_attached()]] - code - tests/test_full_scenes.py
- [[test_sfx_full()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/get_image
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_re]]
- 3 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_gather_pool]]
- 2 edges to [[_COMMUNITY_fetch]]
- 2 edges to [[_COMMUNITY_choose_images]]
- 2 edges to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_drawn_thumbnail]]
- 1 edge to [[_COMMUNITY_sfx_events]]
- 1 edge to [[_COMMUNITY_load_pool]]
- 1 edge to [[_COMMUNITY_full_props]]

## Top bridge nodes
- [[get_image()]] - degree 9, connects to 5 communities
- [[download_picture()]] - degree 5, connects to 3 communities
- [[ov_get()]] - degree 5, connects to 2 communities
- [[full_pictures()]] - degree 5, connects to 2 communities
- [[openverse_images()]] - degree 4, connects to 2 communities