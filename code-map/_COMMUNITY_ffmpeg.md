---
type: community
members: 23
---

# ffmpeg

**Members:** 23 nodes

## Members
- [[Caption words the aligner gives for `text` (qwen_voice.align_words a token…]] - rationale - shortsmaker/gpu.py
- [[Cut each take into its scenes halfway through the pause between their words…]] - rationale - shortsmaker/gpu.py
- [[Fast path for a mark card on a still, with hard cuts on both sides. Preserve…]] - rationale - shortsmaker/scene_repair.py
- [[Final H.264 encode NVENC on the GPU when available (frees the CPU), else x264.]] - rationale - shortsmaker/media_tools.py
- [[Path_28]] - code
- [[Path_29]] - code
- [[Path_30]] - code
- [[Start and end of the camera shot containing time `at` (newsreels cut to title…]] - rationale - shortsmaker/footage.py
- [[Write via a temp file, so an interrupted run never leaves a half-written file…]] - rationale - shortsmaker/media_tools.py
- [[apply()]] - code - shortsmaker/scene_repair.py
- [[copy]] - concept
- [[duration()]] - code - shortsmaker/media_tools.py
- [[ffmpeg()]] - code - shortsmaker/media_tools.py
- [[preview()]] - code - shortsmaker/scene_repair.py
- [[save_context()]] - code - shortsmaker/checkpoints.py
- [[shot_span()]] - code - shortsmaker/footage.py
- [[split_takes()]] - code - shortsmaker/gpu.py
- [[spoken_count()]] - code - shortsmaker/gpu.py
- [[test_a_take_is_cut_between_the_scenes_words()]] - code - tests/test_story.py
- [[test_encoder_cache_lives_with_video_encoder()]] - code - tests/test_package.py
- [[test_word_counts_match_the_aligner()]] - code - tests/test_story.py
- [[video_encoder()]] - code - shortsmaker/media_tools.py
- [[write_json()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ffmpeg
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_gpu.py]]
- 9 edges to [[_COMMUNITY_local_clips]]
- 9 edges to [[_COMMUNITY_audio_library.py]]
- 8 edges to [[_COMMUNITY_render]]
- 8 edges to [[_COMMUNITY_pathlib]]
- 4 edges to [[_COMMUNITY_make]]
- 4 edges to [[_COMMUNITY_resume_runs]]
- 3 edges to [[_COMMUNITY_picture_pool.py]]
- 3 edges to [[_COMMUNITY_test_first_second.py]]
- 3 edges to [[_COMMUNITY_re]]
- 3 edges to [[_COMMUNITY_test_blender_render.py]]
- 3 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_test_pictures_first.py]]
- 2 edges to [[_COMMUNITY_brand_images]]
- 2 edges to [[_COMMUNITY_first_sentence]]
- 2 edges to [[_COMMUNITY_fix_short]]
- 2 edges to [[_COMMUNITY_test_story.py]]
- 1 edge to [[_COMMUNITY_extra_sources.py]]
- 1 edge to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_fetch]]
- 1 edge to [[_COMMUNITY_render_remotion]]
- 1 edge to [[_COMMUNITY_download_audio_choices]]
- 1 edge to [[_COMMUNITY_code_custom_scenes]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_short]]
- 1 edge to [[_COMMUNITY_ask_ai]]

## Top bridge nodes
- [[write_json()]] - degree 21, connects to 11 communities
- [[duration()]] - degree 19, connects to 11 communities
- [[ffmpeg()]] - degree 21, connects to 10 communities
- [[apply()]] - degree 13, connects to 8 communities
- [[preview()]] - degree 12, connects to 5 communities