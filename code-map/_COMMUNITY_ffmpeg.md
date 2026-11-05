---
type: community
members: 18
---

# ffmpeg

**Members:** 18 nodes

## Members
- [[Cut each take into its scenes halfway through the pause between their words…]] - rationale - shortsmaker/gpu.py
- [[Fast path for a mark card on a still, with hard cuts on both sides. Preserve…]] - rationale - shortsmaker/scene_repair.py
- [[Final H.264 encode NVENC on the GPU when available (frees the CPU), else x264.]] - rationale - shortsmaker/media_tools.py
- [[Path_26]] - code
- [[Path_27]] - code
- [[What a fix re-render needs to reproduce this Short without new AI picks the…]] - rationale - shortsmaker/short_render.py
- [[Write via a temp file, so an interrupted run never leaves a half-written file…]] - rationale - shortsmaker/media_tools.py
- [[apply()]] - code - shortsmaker/scene_repair.py
- [[copy]] - concept
- [[duration()]] - code - shortsmaker/media_tools.py
- [[ffmpeg()]] - code - shortsmaker/media_tools.py
- [[preview()]] - code - shortsmaker/scene_repair.py
- [[save_state()]] - code - shortsmaker/short_render.py
- [[split_takes()]] - code - shortsmaker/gpu.py
- [[test_a_take_is_cut_between_the_scenes_words()]] - code - tests/test_story.py
- [[test_encoder_cache_lives_with_video_encoder()]] - code - tests/test_package.py
- [[video_encoder()]] - code - shortsmaker/media_tools.py
- [[write_json()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ffmpeg
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_subprocess]]
- 8 edges to [[_COMMUNITY_render]]
- 7 edges to [[_COMMUNITY_audio_library.py]]
- 6 edges to [[_COMMUNITY_json]]
- 6 edges to [[_COMMUNITY_local_clips]]
- 5 edges to [[_COMMUNITY_image_sources.py]]
- 4 edges to [[_COMMUNITY_extra_sources.py]]
- 4 edges to [[_COMMUNITY_make]]
- 3 edges to [[_COMMUNITY_media_command]]
- 3 edges to [[_COMMUNITY_test_blender_plan.py]]
- 3 edges to [[_COMMUNITY_fix_short]]
- 2 edges to [[_COMMUNITY_finish_render]]
- 2 edges to [[_COMMUNITY_test_pictures_first.py]]
- 2 edges to [[_COMMUNITY_resume_runs]]
- 2 edges to [[_COMMUNITY_footage.py]]
- 2 edges to [[_COMMUNITY_test_first_second.py]]
- 1 edge to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_story_problems]]
- 1 edge to [[_COMMUNITY_render_remotion]]
- 1 edge to [[_COMMUNITY_log_short]]
- 1 edge to [[_COMMUNITY_code_custom_scenes]]
- 1 edge to [[_COMMUNITY_qwen_voice.py]]
- 1 edge to [[_COMMUNITY_test_drawn_opener.py]]
- 1 edge to [[_COMMUNITY_pack]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_test_story.py]]

## Top bridge nodes
- [[duration()]] - degree 19, connects to 12 communities
- [[ffmpeg()]] - degree 21, connects to 11 communities
- [[write_json()]] - degree 21, connects to 11 communities
- [[apply()]] - degree 13, connects to 5 communities
- [[video_encoder()]] - degree 10, connects to 5 communities