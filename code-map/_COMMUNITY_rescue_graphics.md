---
type: community
members: 16
---

# rescue_graphics

**Members:** 16 nodes

## Members
- [[Check every line against the story's Wikipedia articles and rewrite what they…]] - rationale - shortsmaker/writing.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Plain text of an English Wikipedia article ('' when missing or unreachable).]] - rationale - shortsmaker/writing.py
- [[Scenes whose picture is missing or weak may become a full-screen motion graphic…]] - rationale - shortsmaker/picker.py
- [[The full-screen motion graphic formats the AI may pick from (rescue_graphics,…]] - rationale - shortsmaker/picker.py
- [[The motion-graphic opener (owner, 2026-10-28) on a channel with `opener…]] - rationale - shortsmaker/picker.py
- [[Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable).]] - rationale - shortsmaker/footage.py
- [[article_text()]] - code - shortsmaker/writing.py
- [[commons_films()]] - code - shortsmaker/footage.py
- [[fact_check()]] - code - shortsmaker/writing.py
- [[full_formats()]] - code - shortsmaker/picker.py
- [[opener_graphic()]] - code - shortsmaker/picker.py
- [[rescue_graphics()]] - code - shortsmaker/picker.py
- [[test_fact_check_drops_full()]] - code - tests/test_full_scenes.py
- [[test_rescue_respects_caps()]] - code - tests/test_full_scenes.py
- [[wm_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/rescue_graphics
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_json]]
- 5 edges to [[_COMMUNITY_test_pictures_first.py]]
- 3 edges to [[_COMMUNITY_image_sources.py]]
- 3 edges to [[_COMMUNITY_ask_ai]]
- 3 edges to [[_COMMUNITY_words_of]]
- 2 edges to [[_COMMUNITY_clean_full]]
- 2 edges to [[_COMMUNITY_first_second_check]]
- 2 edges to [[_COMMUNITY_render]]
- 2 edges to [[_COMMUNITY_fix_short]]
- 2 edges to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_full_cues]]
- 1 edge to [[_COMMUNITY_gpu.py]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_topic_ideas.py]]
- 1 edge to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_owner]]

## Top bridge nodes
- [[rescue_graphics()]] - degree 13, connects to 8 communities
- [[opener_graphic()]] - degree 11, connects to 7 communities
- [[fact_check()]] - degree 8, connects to 5 communities
- [[wm_get()]] - degree 8, connects to 4 communities
- [[commons_films()]] - degree 6, connects to 4 communities