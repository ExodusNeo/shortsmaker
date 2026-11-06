---
type: community
members: 37
---

# render

**Members:** 37 nodes

## Members
- [[Cut each take into its scenes halfway through the pause between their words…]] - rationale - shortsmaker/gpu.py
- [[Fast path for a mark card on a still, with hard cuts on both sides. Preserve…]] - rationale - shortsmaker/scene_repair.py
- [[Final H.264 encode NVENC on the GPU when available (frees the CPU), else x264.]] - rationale - shortsmaker/media_tools.py
- [[Make one Short. With `state` (fix.bat or an automatic fix round), reuse its…]] - rationale - shortsmaker/short_render.py
- [[On `opener animated` channels, a reveal scene (motion.is_payoff) planned as a…]] - rationale - shortsmaker/short_render.py
- [[Paint the AI images with Gemini (agy's built-in image generator, ~2 min each, 3…]] - rationale - shortsmaker/gpu.py
- [[Path_15]] - code
- [[Path_16]] - code
- [[Path_17]] - code
- [[Scenes after the first with no picture, no graphic and no planned painting get…]] - rationale - shortsmaker/short_render.py
- [[Synthesize the sound-effect library once (no downloads, no copyright). Hits,…]] - rationale - shortsmaker/audio_mix.py
- [[The on-screen credit tag kind, a short name and the licence (Photo E. Mariz…]] - rationale - shortsmaker/image_sources.py
- [[What a fix re-render needs to reproduce this Short without new AI picks the…]] - rationale - shortsmaker/short_render.py
- [[Write via a temp file, so an interrupted run never leaves a half-written file…]] - rationale - shortsmaker/media_tools.py
- [[apply()]] - code - shortsmaker/scene_repair.py
- [[copy]] - concept
- [[drawn_payoff()]] - code - shortsmaker/short_render.py
- [[duration()]] - code - shortsmaker/media_tools.py
- [[ffmpeg()]] - code - shortsmaker/media_tools.py
- [[gemini_images()]] - code - shortsmaker/gpu.py
- [[graphics_count()]] - code - shortsmaker/motion.py
- [[make_sfx()]] - code - shortsmaker/audio_mix.py
- [[noise()]] - code - shortsmaker/audio_mix.py
- [[one()]] - code - shortsmaker/gpu.py
- [[plan_gap_paintings()]] - code - shortsmaker/short_render.py
- [[preview()]] - code - shortsmaker/scene_repair.py
- [[render()]] - code - shortsmaker/short_render.py
- [[save()]] - code - shortsmaker/audio_mix.py
- [[save_context()]] - code - shortsmaker/checkpoints.py
- [[save_state()]] - code - shortsmaker/short_render.py
- [[short_credit()]] - code - shortsmaker/image_sources.py
- [[split_takes()]] - code - shortsmaker/gpu.py
- [[test_a_take_is_cut_between_the_scenes_words()]] - code - tests/test_story.py
- [[test_encoder_cache_lives_with_video_encoder()]] - code - tests/test_package.py
- [[test_scene_without_picture_or_prompt_gets_painted_not_reused()]] - code - tests/test_pictures_first.py
- [[video_encoder()]] - code - shortsmaker/media_tools.py
- [[write_json()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/render
SORT file.name ASC
```

## Connections to other communities
- 15 edges to [[_COMMUNITY_audio_library.py]]
- 14 edges to [[_COMMUNITY_plan_rules.py]]
- 11 edges to [[_COMMUNITY_short_render.py]]
- 10 edges to [[_COMMUNITY_local_clips]]
- 9 edges to [[_COMMUNITY_finish_render]]
- 6 edges to [[_COMMUNITY_hashlib]]
- 6 edges to [[_COMMUNITY_test_drawn_opener.py]]
- 5 edges to [[_COMMUNITY_re]]
- 5 edges to [[_COMMUNITY_resume_runs]]
- 5 edges to [[_COMMUNITY_audio_mix.py]]
- 5 edges to [[_COMMUNITY_checkpoints.py]]
- 5 edges to [[_COMMUNITY_test_blender_render.py]]
- 5 edges to [[_COMMUNITY_fix_short]]
- 4 edges to [[_COMMUNITY_make]]
- 4 edges to [[_COMMUNITY_json]]
- 3 edges to [[_COMMUNITY_test_first_second.py]]
- 3 edges to [[_COMMUNITY_test_pictures_first.py]]
- 3 edges to [[_COMMUNITY_extra_sources.py]]
- 3 edges to [[_COMMUNITY_test_story.py]]
- 3 edges to [[_COMMUNITY_media_menu.py]]
- 2 edges to [[_COMMUNITY_frame_maker]]
- 2 edges to [[_COMMUNITY_render_remotion]]
- 2 edges to [[_COMMUNITY_code_custom_scenes]]
- 2 edges to [[_COMMUNITY_test_blender_run.py]]
- 2 edges to [[_COMMUNITY_clean_full]]
- 2 edges to [[_COMMUNITY_clean_photo]]
- 2 edges to [[_COMMUNITY_scene_cues]]
- 1 edge to [[_COMMUNITY_fetch]]
- 1 edge to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_qwen_voice.py]]
- 1 edge to [[_COMMUNITY_render_1]]
- 1 edge to [[_COMMUNITY_main_1]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_make_paper]]
- 1 edge to [[_COMMUNITY_ends_sentence]]
- 1 edge to [[_COMMUNITY_test_style.py]]
- 1 edge to [[_COMMUNITY_save_candidate]]
- 1 edge to [[_COMMUNITY_ask_ai]]

## Top bridge nodes
- [[render()]] - degree 64, connects to 25 communities
- [[ffmpeg()]] - degree 22, connects to 11 communities
- [[duration()]] - degree 19, connects to 11 communities
- [[write_json()]] - degree 21, connects to 10 communities
- [[apply()]] - degree 13, connects to 7 communities