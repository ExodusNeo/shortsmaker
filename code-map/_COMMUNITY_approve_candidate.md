---
type: community
members: 13
---

# approve_candidate

**Members:** 13 nodes

## Members
- [[Adds a candidate to the library (component file, library.json entry,…]] - rationale - shortsmaker/style_lab.py
- [[Path_4]] - code
- [[The library files a candidate test may touch, to put back afterwards.]] - rationale - tests/test_style.py
- [[approve_candidate()]] - code - shortsmaker/style_lab.py
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
TABLE source_file, type FROM #community/approve_candidate
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_test_style.py]]
- 4 edges to [[_COMMUNITY_plan_rules.py]]
- 3 edges to [[_COMMUNITY_json]]
- 3 edges to [[_COMMUNITY_style_library]]
- 2 edges to [[_COMMUNITY_invent_component]]
- 1 edge to [[_COMMUNITY_motion.py]]

## Top bridge nodes
- [[approve_candidate()]] - degree 12, connects to 5 communities
- [[test_candidate_names_unique_across_kinds()]] - degree 4, connects to 3 communities
- [[candidate_in()]] - degree 8, connects to 2 communities
- [[test_approve_adds_to_library()]] - degree 6, connects to 2 communities
- [[test_reject_deletes()]] - degree 3, connects to 2 communities