---
type: community
members: 10
---

# get_image

**Members:** 10 nodes

## Members
- [[Bounded retry; Wikimedia already handles its own rate limits and retries.]] - rationale - shortsmaker/picker.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[One text selection from already-reviewed pool entries before missing scenes…]] - rationale - shortsmaker/picker.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[download_picture()]] - code - shortsmaker/picker.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[recover_downloads()]] - code - shortsmaker/picker.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/get_image
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_re]]
- 2 edges to [[_COMMUNITY_gather_pool]]
- 2 edges to [[_COMMUNITY_fetch]]
- 2 edges to [[_COMMUNITY_choose_images]]
- 2 edges to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_drawn_thumbnail]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_full_cues]]
- 1 edge to [[_COMMUNITY_words_of]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_json]]

## Top bridge nodes
- [[get_image()]] - degree 9, connects to 6 communities
- [[recover_downloads()]] - degree 7, connects to 5 communities
- [[ov_get()]] - degree 5, connects to 2 communities
- [[download_picture()]] - degree 5, connects to 2 communities
- [[openverse_images()]] - degree 4, connects to 2 communities