---
type: community
members: 74
---

# re

**Members:** 74 nodes

## Members
- [[(min words, max words, min scenes, max scenes, seconds) for this batch's…]] - rationale - shortsmaker/writing.py
- [[Add a finished Short to this channel's logbook, with empty lines for its…]] - rationale - shortsmaker/logbook.py
- [[Automatic checks on the finished Short, using ffmpeg's own detectors in one…]] - rationale - shortsmaker/review.py
- [[Caption words the aligner gives for `text` (qwen_voice.align_words a token…]] - rationale - shortsmaker/gpu.py
- [[Cut each take into its scenes halfway through the pause between their words…]] - rationale - shortsmaker/gpu.py
- [[Download ~14s of film around the chosen moment (cropped with FILM_CROP to…]] - rationale - shortsmaker/footage.py
- [[Extract (numeric_value, compact_display, short_label, trigger_phrase) from a…]] - rationale - shortsmaker/plan_rules.py
- [[Fill the 916 frame with the picture (centre crop) for the slow zoompan. This…]] - rationale - shortsmaker/photo_prep.py
- [[Make one Short. With `state` (fix.bat or an automatic fix round), reuse its…]] - rationale - shortsmaker/short_render.py
- [[One mid-scene frame per scene from the finished video, labeled with its…]] - rationale - shortsmaker/review.py
- [[Path_14]] - code
- [[Path_15]] - code
- [[Path_16]] - code
- [[Path_17]] - code
- [[Path_18]] - code
- [[Planned full-screen motion graphics allowed per Short (default MAX_FULL_PLANNED…]] - rationale - shortsmaker/rules.py
- [[Rejected scenes (index - the review's complaint) that get a real picture from…]] - rationale - shortsmaker/review.py
- [[Remotion failed the full-screen motion graphic scenes get a painted picture…]] - rationale - shortsmaker/remotion_render.py
- [[Run a batch on this PC's GPU through a local_ai worker (gen.py, or…]] - rationale - shortsmaker/gpu.py
- [[Runs of scenes that together make whole sentences. A sentence may run across…]] - rationale - shortsmaker/gpu.py
- [[Saves an invention that made it into a finished Short as a candidate for the…]] - rationale - shortsmaker/style_lab.py
- [[Start and end of the camera shot containing time `at` (newsreels cut to title…]] - rationale - shortsmaker/footage.py
- [[The AI watches the finished Short as sheets of one frame per second and reports…]] - rationale - shortsmaker/review.py
- [[The automatic fixes after a render's review (up to AUTO_REPAINT_MAX scenes per…]] - rationale - shortsmaker/review.py
- [[The code from an AI reply (code fences removed); None unless it exports the…]] - rationale - shortsmaker/style_lab.py
- [[The review's reply - (CHECK lines, scene - (repaint  graphic, why)).…]] - rationale - shortsmaker/review.py
- [[The sound file for a story sound the owner's own file in…]] - rationale - shortsmaker/audio_mix.py
- [[Total full-screen motion graphics (planned + rescued) allowed per Short…]] - rationale - shortsmaker/rules.py
- [[True when the Short's final scene is an open grammatical loop bridge into scene…]] - rationale - shortsmaker/plan_rules.py
- [[Voice every scene on the GPU CosyVoice (aiden, documentary) for the whole…]] - rationale - shortsmaker/gpu.py
- [[VoiceStudio's backend answers, starting the app (and waiting up to 2 min) if it…]] - rationale - shortsmaker/gpu.py
- [[Volume factor that brings this track's loudness (first 60 s) to MUSIC_LUFS;…]] - rationale - shortsmaker/audio_mix.py
- [[What covers or dims scene's picture on purpose, with its times (as…]] - rationale - shortsmaker/review.py
- [[Would a stranger scrolling the Shorts feed stop here Stayed-to-watch is…]] - rationale - shortsmaker/review.py
- [[apply_review_fixes()]] - code - shortsmaker/review.py
- [[clean_style_code()]] - code - shortsmaker/style_lab.py
- [[clock()_1]] - code - shortsmaker/media_tools.py
- [[duration()]] - code - shortsmaker/media_tools.py
- [[ffmpeg()]] - code - shortsmaker/media_tools.py
- [[film_piece()]] - code - shortsmaker/footage.py
- [[first_second_check()]] - code - shortsmaker/review.py
- [[fix  auto-fix scene i drops its picture and gets a freshly painted one…]] - rationale - shortsmaker/review.py
- [[is_loop_short()]] - code - shortsmaker/plan_rules.py
- [[length_plan()]] - code - shortsmaker/writing.py
- [[local_job()]] - code - shortsmaker/gpu.py
- [[local_voice()]] - code - shortsmaker/gpu.py
- [[log_short()]] - code - shortsmaker/logbook.py
- [[max_full()]] - code - shortsmaker/rules.py
- [[max_full_planned()]] - code - shortsmaker/rules.py
- [[music_gain()]] - code - shortsmaker/audio_mix.py
- [[overlay_notes()]] - code - shortsmaker/review.py
- [[paint_instead()]] - code - shortsmaker/remotion_render.py
- [[paint_new()]] - code - shortsmaker/review.py
- [[parse_scene_money()]] - code - shortsmaker/plan_rules.py
- [[pool_pictures()]] - code - shortsmaker/review.py
- [[quality_check()]] - code - shortsmaker/review.py
- [[re]] - concept
- [[render()_3]] - code - shortsmaker/short_render.py
- [[review_fixes()]] - code - shortsmaker/review.py
- [[save_candidate()]] - code - shortsmaker/style_lab.py
- [[sentence_groups()]] - code - shortsmaker/gpu.py
- [[shot_span()]] - code - shortsmaker/footage.py
- [[split_takes()]] - code - shortsmaker/gpu.py
- [[spoken_count()]] - code - shortsmaker/gpu.py
- [[story_sound()]] - code - shortsmaker/audio_mix.py
- [[storyboard()]] - code - shortsmaker/review.py
- [[subprocess]] - concept
- [[test_a_take_is_cut_between_the_scenes_words()]] - code - tests/test_story.py
- [[test_review_is_told_the_drawings_are_deliberate()]] - code - tests/test_blender_run.py
- [[to_vertical()]] - code - shortsmaker/photo_prep.py
- [[up()]] - code - shortsmaker/gpu.py
- [[visual_review()]] - code - shortsmaker/review.py
- [[voicestudio_up()]] - code - shortsmaker/gpu.py
- [[where()]] - code - shortsmaker/review.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/re
SORT file.name ASC
```

## Connections to other communities
- 58 edges to [[_COMMUNITY_gpu.py]]
- 17 edges to [[_COMMUNITY_json]]
- 16 edges to [[_COMMUNITY_shutil]]
- 15 edges to [[_COMMUNITY_local_clips]]
- 13 edges to [[_COMMUNITY_audio_mix.py]]
- 8 edges to [[_COMMUNITY_Shotcut Timeline and Loudness]]
- 8 edges to [[_COMMUNITY_test_full_scenes.py]]
- 7 edges to [[_COMMUNITY_test_blender_scene.py]]
- 7 edges to [[_COMMUNITY_image_sources.py]]
- 6 edges to [[_COMMUNITY_test_first_second.py]]
- 5 edges to [[_COMMUNITY_drawn_thumbnail]]
- 5 edges to [[_COMMUNITY_test_blender_render.py]]
- 5 edges to [[_COMMUNITY_test_package.py]]
- 5 edges to [[_COMMUNITY_words_of]]
- 4 edges to [[_COMMUNITY_frame_render.py]]
- 4 edges to [[_COMMUNITY_clean_full]]
- 4 edges to [[_COMMUNITY_align_words]]
- 4 edges to [[_COMMUNITY_random]]
- 3 edges to [[_COMMUNITY_catalog_pool]]
- 3 edges to [[_COMMUNITY_write_scripts]]
- 3 edges to [[_COMMUNITY_vault_page]]
- 3 edges to [[_COMMUNITY_rescue_graphics]]
- 3 edges to [[_COMMUNITY_test_style.py]]
- 3 edges to [[_COMMUNITY_style_library]]
- 2 edges to [[_COMMUNITY_test_rules.py]]
- 2 edges to [[_COMMUNITY_render_remotion]]
- 2 edges to [[_COMMUNITY_invent_component]]
- 2 edges to [[_COMMUNITY_choose_images]]
- 2 edges to [[_COMMUNITY_edit_plan]]
- 2 edges to [[_COMMUNITY_use_picture_from]]
- 2 edges to [[_COMMUNITY_captions]]
- 2 edges to [[_COMMUNITY_split_make_shorts.py]]
- 1 edge to [[_COMMUNITY_math]]
- 1 edge to [[_COMMUNITY_srt]]
- 1 edge to [[_COMMUNITY_style_placeholders]]
- 1 edge to [[_COMMUNITY_test_local_job_retries_a_hard_crash]]
- 1 edge to [[_COMMUNITY__fake_planning]]
- 1 edge to [[_COMMUNITY_clean_pics]]
- 1 edge to [[_COMMUNITY_drawn_choices]]
- 1 edge to [[_COMMUNITY_full_props]]
- 1 edge to [[_COMMUNITY_scene_cues]]
- 1 edge to [[_COMMUNITY_sfx_events]]
- 1 edge to [[_COMMUNITY_write_frames]]
- 1 edge to [[_COMMUNITY_test_h3_handoff.py]]
- 1 edge to [[_COMMUNITY_Local GPU Worker]]

## Top bridge nodes
- [[render()_3]] - degree 61, connects to 26 communities
- [[re]] - degree 65, connects to 21 communities
- [[subprocess]] - degree 40, connects to 13 communities
- [[apply_review_fixes()]] - degree 15, connects to 7 communities
- [[first_second_check()]] - degree 13, connects to 7 communities