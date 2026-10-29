---
type: community
members: 15
---

# style_library

**Members:** 15 nodes

## Members
- [[Adds a candidate to the library (component file, library.json entry,…]] - rationale - shortsmaker/style_lab.py
- [[Regenerates remotionsrcstyleindex.ts from library.json Remotion's bundle…]] - rationale - shortsmaker/style_lab.py
- [[The library files a candidate test may touch, to put back afterwards.]] - rationale - tests/test_style.py
- [[The style library (remotionsrcstylelibrary.json) {name, kind, description,…]] - rationale - shortsmaker/style_lab.py
- [[approve_candidate()]] - code - shortsmaker/style_lab.py
- [[library_snapshot()]] - code - tests/test_style.py
- [[restore_library()]] - code - tests/test_style.py
- [[style_library()]] - code - shortsmaker/style_lab.py
- [[test_approve_adds_to_library()]] - code - tests/test_style.py
- [[test_approve_rolls_back_on_tsc_failure()]] - code - tests/test_style.py
- [[test_approve_rolls_back_when_the_check_crashes()]] - code - tests/test_style.py
- [[test_library_entries_have_fields()]] - code - tests/test_style.py
- [[test_write_style_index_is_deterministic()]] - code - tests/test_style.py
- [[timeout()]] - code - tests/test_style.py
- [[write_style_index()]] - code - shortsmaker/style_lab.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/style_library
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_test_style.py]]
- 5 edges to [[_COMMUNITY_json]]
- 3 edges to [[_COMMUNITY_test_full_scenes.py]]
- 3 edges to [[_COMMUNITY_clean_look]]
- 2 edges to [[_COMMUNITY_sys]]
- 2 edges to [[_COMMUNITY_invent_component]]
- 2 edges to [[_COMMUNITY_edit_plan]]
- 1 edge to [[_COMMUNITY_code_custom_scenes]]
- 1 edge to [[_COMMUNITY_test_pictures_first.py]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_sentence_groups]]

## Top bridge nodes
- [[style_library()]] - degree 20, connects to 10 communities
- [[approve_candidate()]] - degree 12, connects to 5 communities
- [[write_style_index()]] - degree 6, connects to 2 communities
- [[test_approve_adds_to_library()]] - degree 6, connects to 1 community
- [[test_approve_rolls_back_when_the_check_crashes()]] - degree 6, connects to 1 community