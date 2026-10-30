---
type: community
members: 23
---

# write_scripts

**Members:** 23 nodes

## Members
- [[(min words, max words, min scenes, max scenes, seconds) for this batch's…]] - rationale - shortsmaker/writing.py
- [[A planned story sound {word, sound}, validated the word must be spoken in…]] - rationale - shortsmaker/audio_mix.py
- [[At most MAX_STORY_SOUNDS story sounds per Short (the first ones), so each one…]] - rationale - shortsmaker/audio_mix.py
- [[Guardrails for the style library (STYLE_CAPS) the hook keeps only its title…]] - rationale - shortsmaker/plan_rules.py
- [[Never scene 1 (real footage keeps the hook), never two in a row, never a scene…]] - rationale - shortsmaker/plan_rules.py
- [[Plan n Shorts on new topics, or on exactly `topics` (comparison runs the other…]] - rationale - shortsmaker/writing.py
- [[Scene narrations from an AI reply a list of strings (or of {narration ...}).]] - rationale - shortsmaker/writing.py
- [[The planner plans the edit (footage searches, shots, camera, graphics, person…]] - rationale - shortsmaker/writing.py
- [[The script editor pass strongest hook, read-aloud fixes, cuts,…]] - rationale - shortsmaker/writing.py
- [[The topic's usable pictures as prompt lines ( without a picture list).]] - rationale - shortsmaker/picture_pool.py
- [[clean_sound()]] - code - shortsmaker/audio_mix.py
- [[direct_scripts()]] - code - shortsmaker/writing.py
- [[edit_scripts()]] - code - shortsmaker/writing.py
- [[length_plan()]] - code - shortsmaker/writing.py
- [[limit_full()]] - code - shortsmaker/plan_rules.py
- [[limit_sounds()]] - code - shortsmaker/audio_mix.py
- [[limit_style()]] - code - shortsmaker/plan_rules.py
- [[narration_lines()]] - code - shortsmaker/writing.py
- [[pictures_of()]] - code - shortsmaker/picture_pool.py
- [[test_clean_sound()]] - code - tests/test_full_scenes.py
- [[test_limit_full()]] - code - tests/test_full_scenes.py
- [[test_solo_edit_scripts_uses_same_ai()]] - code - tests/test_package.py
- [[write_scripts()]] - code - shortsmaker/writing.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/write_scripts
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_plan_rules.py]]
- 8 edges to [[_COMMUNITY_gpu.py]]
- 6 edges to [[_COMMUNITY_planning]]
- 4 edges to [[_COMMUNITY_ask_ai]]
- 4 edges to [[_COMMUNITY_re]]
- 3 edges to [[_COMMUNITY_prepare_topic]]
- 3 edges to [[_COMMUNITY_test_topic_ideas.py]]
- 3 edges to [[_COMMUNITY_channel_profiles.py]]
- 3 edges to [[_COMMUNITY_json]]
- 3 edges to [[_COMMUNITY_test_story.py]]
- 2 edges to [[_COMMUNITY_pool_of]]
- 2 edges to [[_COMMUNITY_clean_look]]
- 2 edges to [[_COMMUNITY_test_style.py]]
- 2 edges to [[_COMMUNITY_clean_pics]]
- 2 edges to [[_COMMUNITY_audio_mix.py]]
- 2 edges to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_test_rules.py]]
- 1 edge to [[_COMMUNITY_test_blender_plan.py]]
- 1 edge to [[_COMMUNITY_style_library]]
- 1 edge to [[_COMMUNITY__fake_planning]]
- 1 edge to [[_COMMUNITY_render]]

## Top bridge nodes
- [[write_scripts()]] - degree 48, connects to 17 communities
- [[edit_scripts()]] - degree 13, connects to 4 communities
- [[direct_scripts()]] - degree 7, connects to 4 communities
- [[clean_sound()]] - degree 7, connects to 3 communities
- [[pictures_of()]] - degree 7, connects to 3 communities