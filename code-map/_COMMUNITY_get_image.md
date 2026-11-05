---
type: community
members: 16
---

# get_image

**Members:** 16 nodes

## Members
- [[Check every line against the story's Wikipedia articles and rewrite what they…]] - rationale - shortsmaker/writing.py
- [[Downloads the real photos the picker chose for evidence boards, custom scenes…]] - rationale - shortsmaker/picker.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Plain text of an English Wikipedia article ('' when missing or unreachable).]] - rationale - shortsmaker/writing.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[article_text()]] - code - shortsmaker/writing.py
- [[fact_check()_1]] - code - shortsmaker/writing.py
- [[full_pictures()]] - code - shortsmaker/picker.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[test_board_pictures_attached()]] - code - tests/test_full_scenes.py
- [[test_fact_check_drops_full()]] - code - tests/test_full_scenes.py
- [[wm_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/get_image
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_image_sources.py]]
- 3 edges to [[_COMMUNITY_extra_sources.py]]
- 3 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_prepare_topic]]
- 2 edges to [[_COMMUNITY_gather_pool]]
- 2 edges to [[_COMMUNITY_choose_images]]
- 2 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_llm.py]]
- 1 edge to [[_COMMUNITY_rescue_graphics]]
- 1 edge to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_test_topic_ideas.py]]
- 1 edge to [[_COMMUNITY_opener_graphic]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_plan_with]]
- 1 edge to [[_COMMUNITY_drawn_thumbnail]]
- 1 edge to [[_COMMUNITY_pathlib]]

## Top bridge nodes
- [[get_image()]] - degree 9, connects to 5 communities
- [[article_text()]] - degree 8, connects to 5 communities
- [[fact_check()_1]] - degree 8, connects to 5 communities
- [[wm_get()]] - degree 8, connects to 4 communities
- [[ov_get()]] - degree 5, connects to 2 communities