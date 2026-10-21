---
type: community
cohesion: 0.29
members: 10
---

# Library Candidate Tests

**Cohesion:** 0.29 - loosely connected
**Members:** 10 nodes

## Members
- [[Path_9]] - code
- [[The library files a candidate test may touch, to put back afterwards.]] - rationale - tests/test_style.py
- [[candidate_in()]] - code - tests/test_style.py
- [[library_snapshot()]] - code - tests/test_style.py
- [[restore_library()]] - code - tests/test_style.py
- [[test_approve_adds_to_library()]] - code - tests/test_style.py
- [[test_approve_rolls_back_on_tsc_failure()]] - code - tests/test_style.py
- [[test_approve_rolls_back_when_the_check_crashes()]] - code - tests/test_style.py
- [[test_reject_deletes()]] - code - tests/test_style.py
- [[timeout()]] - code - tests/test_style.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Library_Candidate_Tests
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Style Tests]]
- 6 edges to [[_COMMUNITY_Style Lab & Edit Plan Text]]
- 1 edge to [[_COMMUNITY_Invention Slots]]

## Top bridge nodes
- [[candidate_in()]] - degree 8, connects to 3 communities
- [[test_approve_adds_to_library()]] - degree 6, connects to 2 communities
- [[test_approve_rolls_back_when_the_check_crashes()]] - degree 6, connects to 2 communities
- [[test_approve_rolls_back_on_tsc_failure()]] - degree 5, connects to 2 communities
- [[test_reject_deletes()]] - degree 3, connects to 2 communities