---
type: community
members: 17
---

# local_voice

**Members:** 17 nodes

## Members
- [[Caption words the aligner gives for `text` (qwen_voice.align_words a token…]] - rationale - shortsmaker/gpu.py
- [[Cut each take into its scenes halfway through the pause between their words…]] - rationale - shortsmaker/gpu.py
- [[Runs of scenes that together make whole sentences. A sentence may run across…]] - rationale - shortsmaker/gpu.py
- [[True when the Short's final scene is an open grammatical loop bridge into scene…]] - rationale - shortsmaker/plan_rules.py
- [[Voice every scene on the GPU CosyVoice (aiden, documentary) for the whole…]] - rationale - shortsmaker/gpu.py
- [[add()]] - code - tests/render_style.py
- [[build()]] - code - tests/render_style.py
- [[is_loop_short()]] - code - shortsmaker/plan_rules.py
- [[local_voice()]] - code - shortsmaker/gpu.py
- [[main()]] - code - tests/render_style.py
- [[scenes()]] - code - tests/test_story.py
- [[sentence_groups()]] - code - shortsmaker/gpu.py
- [[split_takes()]] - code - shortsmaker/gpu.py
- [[spoken_count()]] - code - shortsmaker/gpu.py
- [[test_a_take_is_cut_between_the_scenes_words()]] - code - tests/test_story.py
- [[test_sentences_running_across_cuts_are_one_take()]] - code - tests/test_story.py
- [[test_word_counts_match_the_aligner()]] - code - tests/test_story.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/local_voice
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_pathlib]]
- 5 edges to [[_COMMUNITY_test_story.py]]
- 4 edges to [[_COMMUNITY_re]]
- 4 edges to [[_COMMUNITY_ffmpeg]]
- 3 edges to [[_COMMUNITY_local_clips]]
- 3 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_channel_profiles.py]]
- 1 edge to [[_COMMUNITY_clean_full]]
- 1 edge to [[_COMMUNITY_style_library]]
- 1 edge to [[_COMMUNITY_test_h3_handoff.py]]

## Top bridge nodes
- [[local_voice()]] - degree 12, connects to 6 communities
- [[is_loop_short()]] - degree 7, connects to 4 communities
- [[split_takes()]] - degree 9, connects to 3 communities
- [[spoken_count()]] - degree 7, connects to 3 communities
- [[sentence_groups()]] - degree 5, connects to 2 communities