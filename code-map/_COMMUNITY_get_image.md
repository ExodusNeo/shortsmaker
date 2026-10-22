---
type: community
members: 8
---

# get_image

**Members:** 8 nodes

## Members
- [[Downloads the real photos the picker chose for evidence boards, custom scenes…]] - rationale - shortsmaker/picker.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[full_pictures()]] - code - shortsmaker/picker.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/get_image
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_wm_files]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_gather_pool]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_plan_rules.py]]

## Top bridge nodes
- [[get_image()]] - degree 8, connects to 4 communities
- [[full_pictures()]] - degree 5, connects to 3 communities
- [[openverse_images()]] - degree 4, connects to 2 communities
- [[ov_get()]] - degree 5, connects to 1 community