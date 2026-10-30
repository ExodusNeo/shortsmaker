---
type: community
members: 8
---

# require_rules

**Members:** 8 nodes

## Members
- [[Read and check channelsname.rules.md into session.RULES …]] - rationale - shortsmaker/rules.py
- [[Usable real picturesclips a topic needs, else a backup topic replaces it.]] - rationale - shortsmaker/rules.py
- [[load_rules()]] - code - shortsmaker/rules.py
- [[load_rules, but a channel with no rules file yet (a failed draft, a profile…]] - rationale - shortsmaker/rules.py
- [[min_real_pictures()]] - code - shortsmaker/rules.py
- [[require_rules()]] - code - shortsmaker/rules.py
- [[test_load_rules_sets_session()]] - code - tests/test_rules.py
- [[test_missing_rules_file_is_drafted()]] - code - tests/test_rules.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/require_rules
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_test_rules.py]]
- 3 edges to [[_COMMUNITY_test_pictures_first.py]]
- 2 edges to [[_COMMUNITY_main_1]]
- 1 edge to [[_COMMUNITY_run_draft]]
- 1 edge to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_capture_prompts]]
- 1 edge to [[_COMMUNITY_fix_short]]
- 1 edge to [[_COMMUNITY_json]]

## Top bridge nodes
- [[require_rules()]] - degree 8, connects to 4 communities
- [[load_rules()]] - degree 6, connects to 3 communities
- [[min_real_pictures()]] - degree 4, connects to 2 communities
- [[test_missing_rules_file_is_drafted()]] - degree 3, connects to 2 communities
- [[test_load_rules_sets_session()]] - degree 4, connects to 1 community