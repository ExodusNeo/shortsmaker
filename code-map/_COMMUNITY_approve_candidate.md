---
type: community
members: 9
---

# approve_candidate

**Members:** 9 nodes

## Members
- [[Adds a candidate to the library (component file, library.json entry,…]] - rationale - shortsmaker/style_lab.py
- [[The library files a candidate test may touch, to put back afterwards.]] - rationale - tests/test_style.py
- [[approve_candidate()]] - code - shortsmaker/style_lab.py
- [[library_snapshot()]] - code - tests/test_style.py
- [[restore_library()]] - code - tests/test_style.py
- [[test_approve_adds_to_library()]] - code - tests/test_style.py
- [[test_approve_rolls_back_on_tsc_failure()]] - code - tests/test_style.py
- [[test_approve_rolls_back_when_the_check_crashes()]] - code - tests/test_style.py
- [[timeout()]] - code - tests/test_style.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/approve_candidate
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_re]]
- 3 edges to [[_COMMUNITY_style_library]]
- 1 edge to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_shutil]]
- 1 edge to [[_COMMUNITY_code_custom_scenes]]
- 1 edge to [[_COMMUNITY_main_1]]
- 1 edge to [[_COMMUNITY_invent_component]]

## Top bridge nodes
- [[approve_candidate()]] - degree 12, connects to 7 communities
- [[test_approve_adds_to_library()]] - degree 6, connects to 2 communities
- [[test_approve_rolls_back_when_the_check_crashes()]] - degree 6, connects to 1 community
- [[library_snapshot()]] - degree 5, connects to 1 community
- [[test_approve_rolls_back_on_tsc_failure()]] - degree 5, connects to 1 community