---
type: community
members: 20
---

# ffmpeg

**Members:** 20 nodes

## Members
- [[Cut each take into its scenes halfway through the pause between their words…]] - rationale - shortsmaker/gpu.py
- [[Fill a 916 frame with the picture (centre crop), for the AI video model's…]] - rationale - shortsmaker/gpu.py
- [[Final H.264 encode NVENC on the GPU when available (frees the CPU), else x264.]] - rationale - shortsmaker/media_tools.py
- [[Image-to-video prompt for an animate scene (LTX on this PC, or Veo in Flow by…]] - rationale - shortsmaker/gpu.py
- [[Path_13]] - code
- [[Path_14]] - code
- [[Pause the batch write each animate scene's start picture + Veo prompt to…]] - rationale - shortsmaker/gpu.py
- [[Real motion for every scene with a picture scenes Claude matched to archival…]] - rationale - shortsmaker/gpu.py
- [[Start and end of the camera shot containing time `at` (newsreels cut to title…]] - rationale - shortsmaker/footage.py
- [[cover_crop()]] - code - shortsmaker/gpu.py
- [[duration()]] - code - shortsmaker/media_tools.py
- [[ffmpeg()]] - code - shortsmaker/media_tools.py
- [[local_clips()]] - code - shortsmaker/gpu.py
- [[motion_prompt()]] - code - shortsmaker/gpu.py
- [[shot_span()]] - code - shortsmaker/footage.py
- [[split_takes()]] - code - shortsmaker/gpu.py
- [[test_a_take_is_cut_between_the_scenes_words()]] - code - tests/test_story.py
- [[test_encoder_cache_lives_with_video_encoder()]] - code - tests/test_package.py
- [[veo_handoff()]] - code - shortsmaker/gpu.py
- [[video_encoder()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ffmpeg
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_json]]
- 7 edges to [[_COMMUNITY_render]]
- 7 edges to [[_COMMUNITY_audio_mix.py]]
- 5 edges to [[_COMMUNITY_local_job]]
- 3 edges to [[_COMMUNITY_test_edit_project.py]]
- 2 edges to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_motion.py]]
- 1 edge to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_frame_maker]]
- 1 edge to [[_COMMUNITY_render_remotion]]
- 1 edge to [[_COMMUNITY_qwen_voice.py]]
- 1 edge to [[_COMMUNITY_film_piece]]
- 1 edge to [[_COMMUNITY_plan_rules.py]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_test_story.py]]
- 1 edge to [[_COMMUNITY_paint_instead]]

## Top bridge nodes
- [[duration()]] - degree 11, connects to 6 communities
- [[ffmpeg()]] - degree 14, connects to 4 communities
- [[local_clips()]] - degree 12, connects to 4 communities
- [[shot_span()]] - degree 7, connects to 4 communities
- [[split_takes()]] - degree 8, connects to 3 communities