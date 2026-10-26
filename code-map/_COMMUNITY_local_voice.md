---
type: community
members: 9
---

# local_voice

**Members:** 9 nodes

## Members
- [[Free VoiceStudio's GPU memory the 8 GB card is needed next for SDXL, LTX and…]] - rationale - shortsmaker/gpu.py
- [[Runs of scenes that together make whole sentences. A sentence may run across…]] - rationale - shortsmaker/gpu.py
- [[True when the Short's final scene is an open grammatical loop bridge into scene…]] - rationale - shortsmaker/plan_rules.py
- [[Voice every scene on the GPU CosyVoice (aiden, documentary) for the whole…]] - rationale - shortsmaker/gpu.py
- [[is_loop_short()]] - code - shortsmaker/plan_rules.py
- [[local_voice()]] - code - shortsmaker/gpu.py
- [[sentence_groups()]] - code - shortsmaker/gpu.py
- [[test_sentences_running_across_cuts_are_one_take()]] - code - tests/test_story.py
- [[voicestudio_unload()]] - code - shortsmaker/gpu.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/local_voice
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_re]]
- 3 edges to [[_COMMUNITY_ffmpeg]]
- 3 edges to [[_COMMUNITY_gpu.py]]
- 2 edges to [[_COMMUNITY_render]]
- 2 edges to [[_COMMUNITY_time]]
- 2 edges to [[_COMMUNITY_AI Clip Prompts and Cuts]]
- 2 edges to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_json]]

## Top bridge nodes
- [[local_voice()]] - degree 12, connects to 6 communities
- [[is_loop_short()]] - degree 7, connects to 5 communities
- [[sentence_groups()]] - degree 5, connects to 2 communities
- [[voicestudio_unload()]] - degree 4, connects to 2 communities
- [[test_sentences_running_across_cuts_are_one_take()]] - degree 3, connects to 2 communities