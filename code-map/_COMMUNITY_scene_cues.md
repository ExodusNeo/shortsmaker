---
type: community
members: 14
---

# scene_cues

**Members:** 14 nodes

## Members
- [[(seconds a callout can be read after its entrance, seconds it needs) the…]] - rationale - shortsmaker/review.py
- [[A kinetic title repeats the spoken words the captions already show; with too…]] - rationale - shortsmaker/short_render.py
- [[Measured reading holds and final-script detours. Editorial defaults, not…]] - rationale - shortsmaker/review.py
- [[Timed extras for one scene a person card (photo `found`) when their name is…]] - rationale - shortsmaker/editplan.py
- [[callout_hold()]] - code - shortsmaker/review.py
- [[drop_unreadable_kinetic()]] - code - shortsmaker/short_render.py
- [[pacing_check()]] - code - shortsmaker/review.py
- [[read_need()]] - code - shortsmaker/plan_rules.py
- [[scene_cues()]] - code - shortsmaker/editplan.py
- [[test_counter_finishes_before_it_leaves()]] - code - tests/test_full_scenes.py
- [[test_graphic_card_hold_duration()]] - code - tests/test_package.py
- [[test_person_card_hold_and_exit_gap()]] - code - tests/test_package.py
- [[test_scene_hold_padding()]] - code - tests/test_package.py
- [[test_short_scene_callout_is_placed_so_the_check_passes()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/scene_cues
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_test_full_scenes.py]]
- 3 edges to [[_COMMUNITY_ask_ai]]
- 2 edges to [[_COMMUNITY_full_cues]]
- 2 edges to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_visual_review]]
- 1 edge to [[_COMMUNITY_frame_maker]]
- 1 edge to [[_COMMUNITY_finish_render]]

## Top bridge nodes
- [[scene_cues()]] - degree 12, connects to 4 communities
- [[pacing_check()]] - degree 5, connects to 3 communities
- [[drop_unreadable_kinetic()]] - degree 4, connects to 2 communities
- [[callout_hold()]] - degree 6, connects to 1 community
- [[read_need()]] - degree 3, connects to 1 community