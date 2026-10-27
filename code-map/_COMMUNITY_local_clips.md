---
type: community
members: 23
---

# local_clips

**Members:** 23 nodes

## Members
- [[After an opener swap moved scene 4's clip to scene 1, the re-render cuts it…]] - rationale - tests/test_h3_handoff.py
- [[Detailed prompts for the owner-made clips (Colab H3 or Flow), written by the AI…]] - rationale - shortsmaker/gpu.py
- [[Fill a 916 frame with the picture (centre crop), for the AI video model's…]] - rationale - shortsmaker/gpu.py
- [[Final H.264 encode NVENC on the GPU when available (frees the CPU), else x264.]] - rationale - shortsmaker/media_tools.py
- [[Paint the AI images with Gemini (agy's built-in image generator, ~2 min each, 3…]] - rationale - shortsmaker/gpu.py
- [[Path]] - code
- [[Pause the batch write each animate scene's start picture + detailed prompt to…]] - rationale - shortsmaker/gpu.py
- [[Real motion for every scene with a picture scenes Claude matched to archival…]] - rationale - shortsmaker/gpu.py
- [[Short image-to-video prompt for an animate scene made by LTX on this PC.]] - rationale - shortsmaker/gpu.py
- [[Start pictures (folderstartN.jpg) the owner shouldn't spend a clip on a…]] - rationale - shortsmaker/gpu.py
- [[The owner's clip `src` cut to scene i's length fills the vertical frame, drops…]] - rationale - shortsmaker/gpu.py
- [[cover_crop()]] - code - shortsmaker/gpu.py
- [[cut_owner_clip()]] - code - shortsmaker/gpu.py
- [[gemini_images()]] - code - shortsmaker/gpu.py
- [[h3_prompts()]] - code - shortsmaker/gpu.py
- [[local_clips()]] - code - shortsmaker/gpu.py
- [[motion_prompt()]] - code - shortsmaker/gpu.py
- [[one()]] - code - shortsmaker/gpu.py
- [[start_picture_problems()]] - code - shortsmaker/gpu.py
- [[test_encoder_cache_lives_with_video_encoder()]] - code - tests/test_package.py
- [[test_owner_clip_is_cut_again_for_the_scene_it_now_sits_in()]] - code - tests/test_h3_handoff.py
- [[veo_handoff()]] - code - shortsmaker/gpu.py
- [[video_encoder()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/local_clips
SORT file.name ASC
```

## Connections to other communities
- 13 edges to [[_COMMUNITY_gpu.py]]
- 5 edges to [[_COMMUNITY_render]]
- 4 edges to [[_COMMUNITY_test_h3_handoff.py]]
- 3 edges to [[_COMMUNITY_ask_ai]]
- 3 edges to [[_COMMUNITY_pathlib]]
- 2 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_short_with]]
- 1 edge to [[_COMMUNITY_paint_instead]]
- 1 edge to [[_COMMUNITY_h3_problems]]
- 1 edge to [[_COMMUNITY_h3_prompt]]
- 1 edge to [[_COMMUNITY_frame_maker]]
- 1 edge to [[_COMMUNITY_h3_run.py]]
- 1 edge to [[_COMMUNITY_test_blender_render.py]]
- 1 edge to [[_COMMUNITY_test_opener_render.py]]

## Top bridge nodes
- [[veo_handoff()]] - degree 14, connects to 5 communities
- [[local_clips()]] - degree 14, connects to 4 communities
- [[video_encoder()]] - degree 9, connects to 4 communities
- [[h3_prompts()]] - degree 7, connects to 4 communities
- [[gemini_images()]] - degree 6, connects to 3 communities