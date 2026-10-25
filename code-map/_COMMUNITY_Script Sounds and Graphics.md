---
type: community
cohesion: 0.14
members: 23
---

# Script Sounds and Graphics

**Cohesion:** 0.14 - loosely connected
**Members:** 23 nodes

## Members
- [[(start, end) of the first time `phrase` is spoken, from TTS word timings.]] - rationale - shortsmaker/plan_rules.py
- [[A planned story sound {word, sound}, validated the word must be spoken in…]] - rationale - shortsmaker/audio_mix.py
- [[At most MAX_STORY_SOUNDS story sounds per Short (the first ones), so each one…]] - rationale - shortsmaker/audio_mix.py
- [[Ensure money beats in economicsfinance Shorts don't go bare when the LLM omits…]] - rationale - shortsmaker/plan_rules.py
- [[Lowercase, accent-free word tokens, for matching names against spoken words.]] - rationale - shortsmaker/plan_rules.py
- [[One planned callout, validated (LLM output is untrusted); None drops it.]] - rationale - shortsmaker/plan_rules.py
- [[Plan n Shorts on new topics, or on exactly `topics` (comparison runs the other…]] - rationale - shortsmaker/writing.py
- [[True when `cand` is a solo portraitheadshot of `person_name` (so a scene that…]] - rationale - shortsmaker/plan_rules.py
- [[True when the picture's subject would land under the top callouts (y ~180-680…]] - rationale - shortsmaker/frame_render.py
- [[clean_graphic()]] - code - shortsmaker/plan_rules.py
- [[clean_sound()]] - code - shortsmaker/audio_mix.py
- [[contains()]] - code - shortsmaker/plan_rules.py
- [[fill_money_graphics()]] - code - shortsmaker/plan_rules.py
- [[graphic_low()]] - code - shortsmaker/frame_render.py
- [[is_person_portrait()]] - code - shortsmaker/plan_rules.py
- [[limit_sounds()]] - code - shortsmaker/audio_mix.py
- [[spoken_span()]] - code - shortsmaker/plan_rules.py
- [[test_clean_question_and_kinetic()]] - code - tests/test_style.py
- [[test_clean_sound()]] - code - tests/test_full_scenes.py
- [[test_fill_money_graphics_and_caps()]] - code - tests/test_full_scenes.py
- [[word()]] - code - shortsmaker/plan_rules.py
- [[words_of()]] - code - shortsmaker/plan_rules.py
- [[write_scripts()]] - code - shortsmaker/writing.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Script_Sounds_and_Graphics
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_CLI, Config and Footage]]
- 7 edges to [[_COMMUNITY_Full-Screen Graphic Validation]]
- 6 edges to [[_COMMUNITY_Obsidian Vault Logbook]]
- 5 edges to [[_COMMUNITY_Topic Planning Tests]]
- 4 edges to [[_COMMUNITY_Motion Scenes and Style Library]]
- 4 edges to [[_COMMUNITY_Stock Video Sources]]
- 3 edges to [[_COMMUNITY_Audio Mix and Shotcut Export]]
- 3 edges to [[_COMMUNITY_Director Picture Cleanup Tests]]
- 3 edges to [[_COMMUNITY_Wikimedia Image Search]]
- 3 edges to [[_COMMUNITY_Main Entry and Channel Profiles]]
- 3 edges to [[_COMMUNITY_Narration Number Speech]]
- 2 edges to [[_COMMUNITY_Picture Pool Storage]]
- 2 edges to [[_COMMUNITY_Sound Design and Scene Cues]]
- 2 edges to [[_COMMUNITY_Graphics Rescue Caps]]
- 2 edges to [[_COMMUNITY_Local Voice and Freesound]]
- 2 edges to [[_COMMUNITY_Style Plan Validation]]
- 1 edge to [[_COMMUNITY_Headless AI Planner Calls]]
- 1 edge to [[_COMMUNITY_Channel Rules Files]]
- 1 edge to [[_COMMUNITY_Pictures-First Pool Tests]]
- 1 edge to [[_COMMUNITY_Sound Effects and Credits]]
- 1 edge to [[_COMMUNITY_Frame Drawing and Graphics]]
- 1 edge to [[_COMMUNITY_Usable Picture Catalog]]
- 1 edge to [[_COMMUNITY_Quality and Visual Review]]
- 1 edge to [[_COMMUNITY_Full Graphic Limits]]
- 1 edge to [[_COMMUNITY_Style Library Caps]]
- 1 edge to [[_COMMUNITY_Blender Build Planning]]
- 1 edge to [[_COMMUNITY_Logbook Results]]
- 1 edge to [[_COMMUNITY_Write Scripts Review Tests]]
- 1 edge to [[_COMMUNITY_Local Voice Alignment]]
- 1 edge to [[_COMMUNITY_Archive Photo Cleanup]]

## Top bridge nodes
- [[write_scripts()]] - degree 44, connects to 22 communities
- [[words_of()]] - degree 22, connects to 7 communities
- [[graphic_low()]] - degree 7, connects to 4 communities
- [[clean_graphic()]] - degree 10, connects to 3 communities
- [[test_fill_money_graphics_and_caps()]] - degree 8, connects to 3 communities