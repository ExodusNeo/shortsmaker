---
type: community
members: 8
---

# rewrite_paint_prompts

**Members:** 8 nodes

## Members
- [[Mike's newsstand a repaint from the unchanged prompt painted the identical…]] - rationale - tests/test_full_scenes.py
- [[Scenes after the first with no picture, no graphic and no planned painting get…]] - rationale - shortsmaker/short_render.py
- [[Scenes being repainted (scene index - what was wrong) get a better ai_image,…]] - rationale - shortsmaker/review.py
- [[ask()_8]] - code - tests/test_full_scenes.py
- [[plan_gap_paintings()]] - code - shortsmaker/short_render.py
- [[rewrite_paint_prompts()]] - code - shortsmaker/review.py
- [[test_rewrite_paint_prompts()]] - code - tests/test_full_scenes.py
- [[test_scene_without_picture_or_prompt_gets_painted_not_reused()]] - code - tests/test_pictures_first.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/rewrite_paint_prompts
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_test_rules.py]]
- 1 edge to [[_COMMUNITY_paint_opener_start]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_main_1]]
- 1 edge to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_test_pictures_first.py]]

## Top bridge nodes
- [[rewrite_paint_prompts()]] - degree 10, connects to 7 communities
- [[plan_gap_paintings()]] - degree 6, connects to 3 communities
- [[test_rewrite_paint_prompts()]] - degree 5, connects to 2 communities
- [[test_scene_without_picture_or_prompt_gets_painted_not_reused()]] - degree 2, connects to 1 community