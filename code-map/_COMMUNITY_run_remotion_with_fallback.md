---
type: community
members: 7
---

# run_remotion_with_fallback

**Members:** 7 nodes

## Members
- [[Replaces every use of an invention in the Remotion props by its library…]] - rationale - shortsmaker/style_lab.py
- [[render()_4]] - code - tests/test_style.py
- [[render(props); if it fails while AI inventions are in use, they are swapped for…]] - rationale - shortsmaker/remotion_render.py
- [[run_remotion_with_fallback()]] - code - shortsmaker/remotion_render.py
- [[swap_inventions()]] - code - shortsmaker/style_lab.py
- [[test_invention_runtime_failure_uses_fallback()]] - code - tests/test_style.py
- [[test_swap_inventions()]] - code - tests/test_style.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/run_remotion_with_fallback
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_render_remotion]]
- 2 edges to [[_COMMUNITY_invent_component]]
- 2 edges to [[_COMMUNITY_test_style.py]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_json]]

## Top bridge nodes
- [[run_remotion_with_fallback()]] - degree 7, connects to 3 communities
- [[swap_inventions()]] - degree 5, connects to 2 communities
- [[test_invention_runtime_failure_uses_fallback()]] - degree 3, connects to 1 community
- [[test_swap_inventions()]] - degree 2, connects to 1 community