---
type: community
cohesion: 0.28
members: 9
---

# Local Voice Alignment

**Cohesion:** 0.28 - loosely connected
**Members:** 9 nodes

## Members
- [[Caption words the aligner gives for `text` (qwen_voice.align_words a token…]] - rationale - shortsmaker/gpu.py
- [[Cut each take into its scenes halfway through the pause between their words…]] - rationale - shortsmaker/gpu.py
- [[True when the Short's final scene is an open grammatical loop bridge into scene…]] - rationale - shortsmaker/plan_rules.py
- [[Voice every scene on the GPU CosyVoice (aiden, documentary) for the whole…]] - rationale - shortsmaker/gpu.py
- [[is_loop_short()]] - code - shortsmaker/plan_rules.py
- [[local_voice()]] - code - shortsmaker/gpu.py
- [[split_takes()]] - code - shortsmaker/gpu.py
- [[spoken_count()]] - code - shortsmaker/gpu.py
- [[test_word_counts_match_the_aligner()]] - code - tests/test_story.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Local_Voice_Alignment
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Local Voice and Freesound]]
- 3 edges to [[_COMMUNITY_Narration Number Speech]]
- 3 edges to [[_COMMUNITY_AI Clip Prompts and Cuts]]
- 3 edges to [[_COMMUNITY_Obsidian Vault Logbook]]
- 2 edges to [[_COMMUNITY_Sound Effects and Credits]]
- 1 edge to [[_COMMUNITY_Audio Mix and Shotcut Export]]
- 1 edge to [[_COMMUNITY_Script Sounds and Graphics]]
- 1 edge to [[_COMMUNITY_TTS and Story Sounds]]
- 1 edge to [[_COMMUNITY_CLI, Config and Footage]]

## Top bridge nodes
- [[local_voice()]] - degree 12, connects to 5 communities
- [[split_takes()]] - degree 9, connects to 5 communities
- [[is_loop_short()]] - degree 7, connects to 4 communities
- [[spoken_count()]] - degree 7, connects to 2 communities
- [[test_word_counts_match_the_aligner()]] - degree 2, connects to 1 community