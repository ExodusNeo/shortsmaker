---
type: community
members: 16
---

# paint_opener_start

**Members:** 16 nodes

## Members
- [[An AI clip of scene 1 came back (the owner's or LTX's) it plays instead of the…]] - rationale - tests/test_opener_graphic.py
- [[No graphic came back scene 1 opens on its picture and a CHECK line says so; a…]] - rationale - tests/test_opener_graphic.py
- [[Owner, 2026-10-30 a weak motion-graphic opener is fixed OPENER_GRAPHIC_FIXES…]] - rationale - tests/test_opener_graphic.py
- [[Paint the AI images with Gemini (agy's built-in image generator, ~2 min each, 3…]] - rationale - shortsmaker/gpu.py
- [[The start picture for scene 1's AI clip (gpu.OPENER_START) a painting of the…]] - rationale - shortsmaker/review.py
- [[fake_moss()]] - code - tests/test_opener_graphic.py
- [[fake_pick()]] - code - tests/test_opener_graphic.py
- [[fresh()]] - code - tests/test_opener_graphic.py
- [[gemini_images()]] - code - shortsmaker/gpu.py
- [[one()]] - code - shortsmaker/gpu.py
- [[paint_opener_start()]] - code - shortsmaker/review.py
- [[test_use_opener_ai_clip_replaces_graphic()]] - code - tests/test_opener_graphic.py
- [[test_use_opener_without_graphic()]] - code - tests/test_opener_graphic.py
- [[test_weak_opener_graphic_fixes_then_handoff()]] - code - tests/test_opener_graphic.py
- [[use()]] - code - tests/test_opener_graphic.py
- [[use_opener with the drawn opener already failed (drawn_failed it is never…]] - rationale - tests/test_opener_graphic.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/paint_opener_start
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_test_full_scenes.py]]
- 3 edges to [[_COMMUNITY_local_clips]]
- 3 edges to [[_COMMUNITY_render]]
- 2 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_opener_graphic]]
- 1 edge to [[_COMMUNITY_finish_render]]
- 1 edge to [[_COMMUNITY_paint_instead]]
- 1 edge to [[_COMMUNITY_rewrite_paint_prompts]]
- 1 edge to [[_COMMUNITY_code_custom_scenes]]
- 1 edge to [[_COMMUNITY_test_style.py]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]

## Top bridge nodes
- [[paint_opener_start()]] - degree 12, connects to 9 communities
- [[test_weak_opener_graphic_fixes_then_handoff()]] - degree 9, connects to 4 communities
- [[gemini_images()]] - degree 7, connects to 4 communities
- [[use()]] - degree 5, connects to 2 communities
- [[fresh()]] - degree 4, connects to 1 community