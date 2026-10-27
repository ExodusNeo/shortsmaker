---
type: community
members: 11
---

# candidate_in

**Members:** 11 nodes

## Members
- [[Path_29]] - code
- [[The library files a candidate test may touch, to put back afterwards.]] - rationale - tests/test_style.py
- [[candidate_in()]] - code - tests/test_style.py
- [[library_snapshot()]] - code - tests/test_style.py
- [[restore_library()]] - code - tests/test_style.py
- [[test_approve_adds_to_library()]] - code - tests/test_style.py
- [[test_approve_rolls_back_on_tsc_failure()]] - code - tests/test_style.py
- [[test_approve_rolls_back_when_the_check_crashes()]] - code - tests/test_style.py
- [[test_candidate_names_unique_across_kinds()]] - code - tests/test_style.py
- [[test_reject_deletes()]] - code - tests/test_style.py
- [[timeout()]] - code - tests/test_style.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/candidate_in
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_test_style.py]]
- 6 edges to [[_COMMUNITY_shutil]]
- 1 edge to [[_COMMUNITY_invent_component]]
- 1 edge to [[_COMMUNITY_style_library]]

## Top bridge nodes
- [[test_approve_adds_to_library()]] - degree 6, connects to 3 communities
- [[test_candidate_names_unique_across_kinds()]] - degree 4, connects to 3 communities
- [[candidate_in()]] - degree 8, connects to 2 communities
- [[test_approve_rolls_back_when_the_check_crashes()]] - degree 6, connects to 2 communities
- [[test_approve_rolls_back_on_tsc_failure()]] - degree 5, connects to 2 communities