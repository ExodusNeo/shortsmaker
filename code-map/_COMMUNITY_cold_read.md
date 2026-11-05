---
type: community
members: 9
---

# cold_read

**Members:** 9 nodes

## Members
- [[How a stranger hears each final script (audit 2026-10-31) the editor used to…]] - rationale - shortsmaker/writing.py
- [[Preferred alternative, keeping the configured hybrid partner when possible.]] - rationale - shortsmaker/llm.py
- [[cold_read()]] - code - shortsmaker/writing.py
- [[other_ai()]] - code - shortsmaker/llm.py
- [[test_codex_cold_reader_and_quota_fallback_never_call_claude()]] - code - tests/test_codex.py
- [[test_cold_read_handles_malformed_reply()]] - code - tests/test_story.py
- [[test_cold_read_keeps_only_valid_answers()]] - code - tests/test_story.py
- [[test_every_mode_can_continue_through_two_exhausted_ais()]] - code - tests/test_ai_modes.py
- [[test_gemini_modes_choose_codex_and_keep_editor_choice()]] - code - tests/test_codex.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/cold_read
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_llm.py]]
- 3 edges to [[_COMMUNITY_test_ai_modes.py]]
- 3 edges to [[_COMMUNITY_configure_brain]]
- 3 edges to [[_COMMUNITY_ask_ai]]
- 2 edges to [[_COMMUNITY_edit_scripts]]
- 1 edge to [[_COMMUNITY_test_pictures_first.py]]
- 1 edge to [[_COMMUNITY_story_problems]]
- 1 edge to [[_COMMUNITY_edit_plan]]
- 1 edge to [[_COMMUNITY_json]]

## Top bridge nodes
- [[cold_read()]] - degree 11, connects to 6 communities
- [[other_ai()]] - degree 8, connects to 4 communities
- [[test_every_mode_can_continue_through_two_exhausted_ais()]] - degree 6, connects to 3 communities
- [[test_codex_cold_reader_and_quota_fallback_never_call_claude()]] - degree 3, connects to 2 communities
- [[test_gemini_modes_choose_codex_and_keep_editor_choice()]] - degree 3, connects to 2 communities