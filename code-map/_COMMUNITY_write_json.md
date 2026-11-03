---
type: community
members: 20
---

# write_json

**Members:** 20 nodes

## Members
- [[Caption words the aligner gives for `text` (qwen_voice.align_words a token…]] - rationale - shortsmaker/gpu.py
- [[Cut each take into its scenes halfway through the pause between their words…]] - rationale - shortsmaker/gpu.py
- [[Fast path for a mark card on a still, with hard cuts on both sides. Preserve…]] - rationale - shortsmaker/scene_repair.py
- [[Final H.264 encode NVENC on the GPU when available (frees the CPU), else x264.]] - rationale - shortsmaker/media_tools.py
- [[Path_22]] - code
- [[Path_23]] - code
- [[Write via a temp file, so an interrupted run never leaves a half-written file…]] - rationale - shortsmaker/media_tools.py
- [[apply()]] - code - shortsmaker/scene_repair.py
- [[copy]] - concept
- [[duration()]] - code - shortsmaker/media_tools.py
- [[ffmpeg()]] - code - shortsmaker/media_tools.py
- [[preview()]] - code - shortsmaker/scene_repair.py
- [[save_context()]] - code - shortsmaker/checkpoints.py
- [[split_takes()]] - code - shortsmaker/gpu.py
- [[spoken_count()]] - code - shortsmaker/gpu.py
- [[test_a_take_is_cut_between_the_scenes_words()]] - code - tests/test_story.py
- [[test_encoder_cache_lives_with_video_encoder()]] - code - tests/test_package.py
- [[test_word_counts_match_the_aligner()]] - code - tests/test_story.py
- [[video_encoder()]] - code - shortsmaker/media_tools.py
- [[write_json()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/write_json
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_test_full_scenes.py]]
- 10 edges to [[_COMMUNITY_audio_library.py]]
- 9 edges to [[_COMMUNITY_render]]
- 7 edges to [[_COMMUNITY_local_clips]]
- 6 edges to [[_COMMUNITY_main_1]]
- 6 edges to [[_COMMUNITY_subprocess]]
- 5 edges to [[_COMMUNITY_re]]
- 4 edges to [[_COMMUNITY_make]]
- 4 edges to [[_COMMUNITY_test_story.py]]
- 3 edges to [[_COMMUNITY_extra_sources.py]]
- 3 edges to [[_COMMUNITY_test_blender_plan.py]]
- 3 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_test_pictures_first.py]]
- 2 edges to [[_COMMUNITY_first_second_check]]
- 1 edge to [[_COMMUNITY_render_remotion]]
- 1 edge to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_OpeningRulesTests]]
- 1 edge to [[_COMMUNITY_time]]
- 1 edge to [[_COMMUNITY_fetch]]
- 1 edge to [[_COMMUNITY_code_custom_scenes]]
- 1 edge to [[_COMMUNITY_visual_review]]
- 1 edge to [[_COMMUNITY_ask_ai]]

## Top bridge nodes
- [[duration()]] - degree 19, connects to 12 communities
- [[ffmpeg()]] - degree 20, connects to 10 communities
- [[write_json()]] - degree 21, connects to 9 communities
- [[apply()]] - degree 13, connects to 7 communities
- [[preview()]] - degree 12, connects to 5 communities