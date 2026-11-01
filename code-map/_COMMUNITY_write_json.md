---
type: community
members: 19
---

# write_json

**Members:** 19 nodes

## Members
- [[Caption words the aligner gives for `text` (qwen_voice.align_words a token…]] - rationale - shortsmaker/gpu.py
- [[Cut each take into its scenes halfway through the pause between their words…]] - rationale - shortsmaker/gpu.py
- [[Fast path for a mark card on a still, with hard cuts on both sides. Preserve…]] - rationale - shortsmaker/scene_repair.py
- [[Path_18]] - code
- [[Path_19]] - code
- [[Path_20]] - code
- [[Start and end of the camera shot containing time `at` (newsreels cut to title…]] - rationale - shortsmaker/footage.py
- [[Write via a temp file, so an interrupted run never leaves a half-written file…]] - rationale - shortsmaker/media_tools.py
- [[apply()]] - code - shortsmaker/scene_repair.py
- [[copy]] - concept
- [[duration()]] - code - shortsmaker/media_tools.py
- [[ffmpeg()]] - code - shortsmaker/media_tools.py
- [[preview()]] - code - shortsmaker/scene_repair.py
- [[shot_span()]] - code - shortsmaker/footage.py
- [[split_takes()]] - code - shortsmaker/gpu.py
- [[spoken_count()]] - code - shortsmaker/gpu.py
- [[test_a_take_is_cut_between_the_scenes_words()]] - code - tests/test_story.py
- [[test_word_counts_match_the_aligner()]] - code - tests/test_story.py
- [[write_json()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/write_json
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_local_clips]]
- 8 edges to [[_COMMUNITY_media_command]]
- 6 edges to [[_COMMUNITY_test_full_scenes.py]]
- 5 edges to [[_COMMUNITY_subprocess]]
- 5 edges to [[_COMMUNITY_test_style.py]]
- 4 edges to [[_COMMUNITY_make]]
- 4 edges to [[_COMMUNITY_test_story.py]]
- 4 edges to [[_COMMUNITY_extra_sources.py]]
- 4 edges to [[_COMMUNITY_json]]
- 4 edges to [[_COMMUNITY_re]]
- 3 edges to [[_COMMUNITY_render]]
- 3 edges to [[_COMMUNITY_resume_runs]]
- 2 edges to [[_COMMUNITY_first_second_check]]
- 2 edges to [[_COMMUNITY_prepare_topic]]
- 2 edges to [[_COMMUNITY_main_1]]
- 2 edges to [[_COMMUNITY_test_blender_render.py]]
- 2 edges to [[_COMMUNITY_film_piece]]
- 2 edges to [[_COMMUNITY_finish_render]]
- 1 edge to [[_COMMUNITY_render_remotion]]
- 1 edge to [[_COMMUNITY_catalog_pool]]
- 1 edge to [[_COMMUNITY_make_opener]]
- 1 edge to [[_COMMUNITY_use_opener]]
- 1 edge to [[_COMMUNITY_qwen_voice.py]]
- 1 edge to [[_COMMUNITY_code_custom_scenes]]
- 1 edge to [[_COMMUNITY_visual_review]]
- 1 edge to [[_COMMUNITY_retention.py]]

## Top bridge nodes
- [[ffmpeg()]] - degree 20, connects to 11 communities
- [[duration()]] - degree 18, connects to 11 communities
- [[write_json()]] - degree 21, connects to 10 communities
- [[apply()]] - degree 13, connects to 8 communities
- [[preview()]] - degree 12, connects to 6 communities