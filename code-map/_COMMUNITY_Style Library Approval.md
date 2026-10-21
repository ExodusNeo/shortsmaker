---
type: community
cohesion: 0.17
members: 17
---

# Style Library Approval

**Cohesion:** 0.17 - loosely connected
**Members:** 17 nodes

## Members
- [[Adds a candidate to the library (component file, library.json entry,…]] - rationale - make_shorts.py
- [[Regenerates remotionsrcstyleindex.ts from library.json Remotion's bundle…]] - rationale - make_shorts.py
- [[The library files a candidate test may touch, to put back afterwards.]] - rationale - tests/test_style.py
- [[The rules every invented component of `kind` follows, with the library's…]] - rationale - make_shorts.py
- [[The style library (remotionsrcstylelibrary.json) {name, kind, description,…]] - rationale - make_shorts.py
- [[approve_candidate()]] - code - make_shorts.py
- [[library_snapshot()]] - code - tests/test_style.py
- [[restore_library()]] - code - tests/test_style.py
- [[style_library()]] - code - make_shorts.py
- [[style_rules()]] - code - make_shorts.py
- [[test_approve_adds_to_library()]] - code - tests/test_style.py
- [[test_approve_rolls_back_on_tsc_failure()]] - code - tests/test_style.py
- [[test_approve_rolls_back_when_the_check_crashes()]] - code - tests/test_style.py
- [[test_library_entries_have_fields()]] - code - tests/test_style.py
- [[test_write_style_index_is_deterministic()]] - code - tests/test_style.py
- [[timeout()]] - code - tests/test_style.py
- [[write_style_index()]] - code - make_shorts.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Style_Library_Approval
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_Look Scene Picking]]
- 5 edges to [[_COMMUNITY_Library Menu & Candidates]]
- 4 edges to [[_COMMUNITY_Shared Imports & Downloads]]
- 3 edges to [[_COMMUNITY_Style Plan Validation]]
- 2 edges to [[_COMMUNITY_Edit Plan Writer]]
- 1 edge to [[_COMMUNITY_Style Invention Coding]]
- 1 edge to [[_COMMUNITY_Image Choosing]]
- 1 edge to [[_COMMUNITY_TypeScript Checks]]
- 1 edge to [[_COMMUNITY_State & Logbook Helpers]]
- 1 edge to [[_COMMUNITY_Director Picture Context]]
- 1 edge to [[_COMMUNITY_Run Menu & Channel Setup]]
- 1 edge to [[_COMMUNITY_Local GPU Workers]]

## Top bridge nodes
- [[style_library()]] - degree 19, connects to 9 communities
- [[approve_candidate()]] - degree 10, connects to 4 communities
- [[test_approve_adds_to_library()]] - degree 6, connects to 2 communities
- [[test_approve_rolls_back_when_the_check_crashes()]] - degree 6, connects to 2 communities
- [[test_approve_rolls_back_on_tsc_failure()]] - degree 5, connects to 2 communities