---
type: community
members: 4
---

# recover_downloads

**Members:** 4 nodes

## Members
- [[Bounded retry; Wikimedia already handles its own rate limits and retries.]] - rationale - shortsmaker/picker.py
- [[One text selection from already-reviewed pool entries before missing scenes…]] - rationale - shortsmaker/picker.py
- [[download_picture()]] - code - shortsmaker/picker.py
- [[recover_downloads()]] - code - shortsmaker/picker.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/recover_downloads
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_choose_images]]
- 2 edges to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_fetch]]
- 1 edge to [[_COMMUNITY_words_of]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_json]]

## Top bridge nodes
- [[recover_downloads()]] - degree 7, connects to 5 communities
- [[download_picture()]] - degree 5, connects to 3 communities