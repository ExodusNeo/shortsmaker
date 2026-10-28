---
type: community
members: 16
---

# approve_candidate

**Members:** 16 nodes

## Members
- [[Adds a candidate to the library (component file, library.json entry,…]] - rationale - shortsmaker/style_lab.py
- [[Path_24]] - code
- [[Saves an invention that made it into a finished Short as a candidate for the…]] - rationale - shortsmaker/style_lab.py
- [[The library files a candidate test may touch, to put back afterwards.]] - rationale - tests/test_style.py
- [[approve_candidate()]] - code - shortsmaker/style_lab.py
- [[candidate_in()]] - code - tests/test_style.py
- [[library_snapshot()]] - code - tests/test_style.py
- [[restore_library()]] - code - tests/test_style.py
- [[save_candidate()]] - code - shortsmaker/style_lab.py
- [[test_approve_adds_to_library()]] - code - tests/test_style.py
- [[test_approve_rolls_back_on_tsc_failure()]] - code - tests/test_style.py
- [[test_approve_rolls_back_when_the_check_crashes()]] - code - tests/test_style.py
- [[test_candidate_names_unique_across_kinds()]] - code - tests/test_style.py
- [[test_reject_deletes()]] - code - tests/test_style.py
- [[test_save_candidate_unique_slug()]] - code - tests/test_style.py
- [[timeout()]] - code - tests/test_style.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/approve_candidate
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_test_style.py]]
- 4 edges to [[_COMMUNITY_style_library]]
- 4 edges to [[_COMMUNITY_test_full_scenes.py]]
- 3 edges to [[_COMMUNITY_subprocess]]
- 2 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_invent_component]]
- 1 edge to [[_COMMUNITY_style_placeholders]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_time]]

## Top bridge nodes
- [[save_candidate()]] - degree 12, connects to 8 communities
- [[approve_candidate()]] - degree 12, connects to 5 communities
- [[test_approve_adds_to_library()]] - degree 6, connects to 2 communities
- [[test_candidate_names_unique_across_kinds()]] - degree 4, connects to 2 communities
- [[test_reject_deletes()]] - degree 3, connects to 2 communities