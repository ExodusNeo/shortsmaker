---
type: community
members: 9
---

# get_image

**Members:** 9 nodes

## Members
- [[Downloads the real photos the picker chose for evidence boards, custom scenes…]] - rationale - shortsmaker/picker.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[full_pictures()]] - code - shortsmaker/picker.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[test_board_pictures_attached()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/get_image
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_extra_sources.py]]
- 2 edges to [[_COMMUNITY_test_pictures_first.py]]
- 1 edge to [[_COMMUNITY_drawn_thumbnail]]
- 1 edge to [[_COMMUNITY_wm_files]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_gather_pool]]
- 1 edge to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_full_props]]

## Top bridge nodes
- [[get_image()]] - degree 9, connects to 6 communities
- [[ov_get()]] - degree 5, connects to 2 communities
- [[full_pictures()]] - degree 5, connects to 2 communities
- [[openverse_images()]] - degree 4, connects to 2 communities
- [[test_board_pictures_attached()]] - degree 3, connects to 2 communities