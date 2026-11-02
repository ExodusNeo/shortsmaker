---
type: community
members: 6
---

# is_person_portrait

**Members:** 6 nodes

## Members
- [[Bounded retry; Wikimedia already handles its own rate limits and retries.]] - rationale - shortsmaker/picker.py
- [[One text selection from already-reviewed pool entries before missing scenes…]] - rationale - shortsmaker/picker.py
- [[True when `cand` is a solo portraitheadshot of `person_name` (so a scene that…]] - rationale - shortsmaker/plan_rules.py
- [[download_picture()]] - code - shortsmaker/picker.py
- [[is_person_portrait()]] - code - shortsmaker/plan_rules.py
- [[recover_downloads()]] - code - shortsmaker/picker.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/is_person_portrait
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_choose_images]]
- 3 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_words_of]]
- 1 edge to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_gather_pool]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_re]]

## Top bridge nodes
- [[is_person_portrait()]] - degree 8, connects to 5 communities
- [[recover_downloads()]] - degree 7, connects to 4 communities
- [[download_picture()]] - degree 5, connects to 3 communities