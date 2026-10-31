---
type: community
members: 6
---

# scene_cues

**Members:** 6 nodes

## Members
- [[Timed extras for one scene a person card (photo `found`) when their name is…]] - rationale - shortsmaker/editplan.py
- [[scene_cues()]] - code - shortsmaker/editplan.py
- [[test_counter_finishes_before_it_leaves()]] - code - tests/test_full_scenes.py
- [[test_graphic_card_hold_duration()]] - code - tests/test_package.py
- [[test_person_card_hold_and_exit_gap()]] - code - tests/test_package.py
- [[test_scene_hold_padding()]] - code - tests/test_package.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/scene_cues
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_full_cues]]
- 1 edge to [[_COMMUNITY_graphic_low]]
- 1 edge to [[_COMMUNITY_render]]

## Top bridge nodes
- [[scene_cues()]] - degree 10, connects to 4 communities
- [[test_counter_finishes_before_it_leaves()]] - degree 2, connects to 1 community
- [[test_graphic_card_hold_duration()]] - degree 2, connects to 1 community
- [[test_person_card_hold_and_exit_gap()]] - degree 2, connects to 1 community
- [[test_scene_hold_padding()]] - degree 2, connects to 1 community