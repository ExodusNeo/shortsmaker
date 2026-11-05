---
type: community
members: 14
---

# gather_pool

**Members:** 14 nodes

## Members
- [[Candidate pictures (with preview `thumb` bytes) and sampled real-film frames…]] - rationale - shortsmaker/picture_pool.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Retain productyearcountry details from the director; also search the…]] - rationale - shortsmaker/footage.py
- [[Round-robin sources rather than letting the first provider consume the whole…]] - rationale - shortsmaker/picture_pool.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[add()_1]] - code - shortsmaker/picture_pool.py
- [[balanced_candidates()]] - code - shortsmaker/picture_pool.py
- [[commercial_queries()]] - code - shortsmaker/footage.py
- [[gather_pool()]] - code - shortsmaker/picture_pool.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[load_thumb()]] - code - shortsmaker/picture_pool.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/gather_pool
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_re]]
- 4 edges to [[_COMMUNITY_fetch]]
- 3 edges to [[_COMMUNITY_wm_files]]
- 3 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_source_json]]
- 2 edges to [[_COMMUNITY_prepare_topic]]
- 2 edges to [[_COMMUNITY_owner]]
- 2 edges to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_finish_render]]
- 1 edge to [[_COMMUNITY_words_of]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_clean_full]]
- 1 edge to [[_COMMUNITY_audio_library.py]]
- 1 edge to [[_COMMUNITY_full_props]]
- 1 edge to [[_COMMUNITY_test_blender_plan.py]]

## Top bridge nodes
- [[gather_pool()]] - degree 23, connects to 11 communities
- [[get_image()]] - degree 9, connects to 7 communities
- [[commercial_queries()]] - degree 5, connects to 2 communities
- [[ov_get()]] - degree 5, connects to 2 communities
- [[openverse_images()]] - degree 4, connects to 1 community