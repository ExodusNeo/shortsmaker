---
type: community
members: 77
---

# test_full_scenes.py

**Members:** 77 nodes

## Members
- [[A Short's saved work state and `render()`, which turns a written Short into the…]] - rationale - shortsmaker/short_render.py
- [[A real FFmpegPython render with fake AI verifies stage saves, voice reuse and…]] - rationale - tests/test_render_resume.py
- [[Atomic progress records for unfinished Shorts; no executable serialized state.]] - rationale - shortsmaker/checkpoints.py
- [[Automatic checks on a finished Short, the AI visual review and its fixes (incl.…]] - rationale - shortsmaker/review.py
- [[Choosing each scene's picture, pictures for full-screen scenes, and rescue…]] - rationale - shortsmaker/picker.py
- [[Cleaning and validating the planner's JSON (graphics, full-screen scenes,…]] - rationale - shortsmaker/plan_rules.py
- [[Cleaning found photos stereograph cards, scanner borders, vertical crops.]] - rationale - shortsmaker/photo_prep.py
- [[Detail coordinates must be chosen on the framing that MarkCard actually…]] - rationale - tests/test_marks.py
- [[Full-screen motion-graphic scenes and the AI-coded Custom scenes (with their…]] - rationale - shortsmaker/motion.py
- [[Headless Codex  Claude Code  Gemini (agy) calls that return JSON, with…]] - rationale - shortsmaker/llm.py
- [[Interruption recovery, narration reuse, honest review failures and bounded…]] - rationale - tests/test_reliability.py
- [[Local AI on the owner's GPU and helpers ComfyUIMOSS, VoiceStudio, Gemini…]] - rationale - shortsmaker/gpu.py
- [[Media adapters and selection invariants, plus small real FFmpeg checks. No…]] - rationale - tests/test_media.py
- [[One mid-scene frame per scene from the finished video, labeled with its…]] - rationale - shortsmaker/review.py
- [[Opener preview repairs must be seen, archived and compared before adoption. No…]] - rationale - tests/test_opener_preflight.py
- [[Opening answer protection across planning, preview review and final drawn-…]] - rationale - tests/test_opening_rules.py
- [[Paths, fixed settings, palettes and the styleskin tables every module shares.…]] - rationale - shortsmaker/config.py
- [[Pictures from Wikimedia Commons, Openverse, NASA and the Internet Archive, with…]] - rationale - shortsmaker/image_sources.py
- [[Plain-language media.bat import, audition, approve and tune local media.]] - rationale - shortsmaker/media_menu.py
- [[Preview and apply a callout repair using existing videoaudio, without new AI…]] - rationale - shortsmaker/scene_repair.py
- [[Render the opener composition study with the real hookcaptions; restore the…]] - rationale - tests/render_opener_preview.py
- [[Rendering a Short with Remotion (with the Python renderer as fallback),…]] - rationale - shortsmaker/remotion_render.py
- [[Reuse completed narration only when text, voice settings and source files still…]] - rationale - shortsmaker/voice_cache.py
- [[Shared opening instructions show the hook while protecting what the narration…]] - rationale - shortsmaker/opening_rules.py
- [[ShortsMaker make ready-to-upload YouTube Shorts. Entry point make_shorts.py.]] - rationale - shortsmaker/__init__.py
- [[Small shared helpers downloads, ffmpeg, video encoder choice, durations, JSON…]] - rationale - shortsmaker/media_tools.py
- [[Tests for the full-screen motion graphic scenes. No AI usage, no rendering.…]] - rationale - tests/test_full_scenes.py
- [[Tests for the motion-graphic opener on `opener animated` channels…]] - rationale - tests/test_opener_graphic.py
- [[The Python renderer camera moves, graphic overlays, person cards, clip…]] - rationale - shortsmaker/frame_render.py
- [[The pictures gathered for a topic before writing, their catalog, cache and…]] - rationale - shortsmaker/picture_pool.py
- [[Voice, captions, sound effects, story sounds and music levels.]] - rationale - shortsmaker/audio_mix.py
- [[__init__.py]] - code - shortsmaker/__init__.py
- [[audio_mix.py]] - code - shortsmaker/audio_mix.py
- [[checkpoints.py]] - code - shortsmaker/checkpoints.py
- [[concurrent_futures]] - concept
- [[config.py]] - code - shortsmaker/config.py
- [[edit_plan.txt (the timestamped edit list) and per-scene cue timing.]] - rationale - shortsmaker/editplan.py
- [[editplan.py]] - code - shortsmaker/editplan.py
- [[frame_render.py]] - code - shortsmaker/frame_render.py
- [[gpu.py]] - code - shortsmaker/gpu.py
- [[hex_rgb()]] - code - shortsmaker/config.py
- [[image_sources.py]] - code - shortsmaker/image_sources.py
- [[io]] - concept
- [[llm.py]] - code - shortsmaker/llm.py
- [[luminance()_1]] - code - shortsmaker/config.py
- [[media_menu.py]] - code - shortsmaker/media_menu.py
- [[media_tools.py]] - code - shortsmaker/media_tools.py
- [[motion.py]] - code - shortsmaker/motion.py
- [[opening_rules.py]] - code - shortsmaker/opening_rules.py
- [[pathlib]] - concept
- [[photo_prep.py]] - code - shortsmaker/photo_prep.py
- [[picker.py]] - code - shortsmaker/picker.py
- [[picture_pool.py]] - code - shortsmaker/picture_pool.py
- [[pil]] - concept
- [[plan_rules.py]] - code - shortsmaker/plan_rules.py
- [[remotion_render.py]] - code - shortsmaker/remotion_render.py
- [[render_opener_preview.py]] - code - tests/render_opener_preview.py
- [[review.py]] - code - shortsmaker/review.py
- [[scene_repair.py]] - code - shortsmaker/scene_repair.py
- [[short_render.py]] - code - shortsmaker/short_render.py
- [[storyboard()]] - code - shortsmaker/review.py
- [[test_full_scenes.py]] - code - tests/test_full_scenes.py
- [[test_marks.py]] - code - tests/test_marks.py
- [[test_media.py]] - code - tests/test_media.py
- [[test_opener_graphic.py]] - code - tests/test_opener_graphic.py
- [[test_opener_preflight.py]] - code - tests/test_opener_preflight.py
- [[test_opening_rules.py]] - code - tests/test_opening_rules.py
- [[test_reliability.py]] - code - tests/test_reliability.py
- [[test_render_resume.py]] - code - tests/test_render_resume.py
- [[types]] - concept
- [[unittest]] - concept
- [[unittest_mock]] - concept
- [[urllib_error]] - concept
- [[urllib_request]] - concept
- [[voice_cache.py]] - code - shortsmaker/voice_cache.py
- [[warnings]] - concept
- [[wave]] - concept

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/test_full_scenespy
SORT file.name ASC
```

## Connections to other communities
- 111 edges to [[_COMMUNITY_writing.py]]
- 66 edges to [[_COMMUNITY_subprocess]]
- 47 edges to [[_COMMUNITY_re]]
- 46 edges to [[_COMMUNITY_json]]
- 22 edges to [[_COMMUNITY_audio_library.py]]
- 15 edges to [[_COMMUNITY_frame_maker]]
- 15 edges to [[_COMMUNITY_clean_full]]
- 15 edges to [[_COMMUNITY_finish_render]]
- 15 edges to [[_COMMUNITY_main_1]]
- 14 edges to [[_COMMUNITY_code_custom_scenes]]
- 12 edges to [[_COMMUNITY_local_clips]]
- 12 edges to [[_COMMUNITY_render]]
- 12 edges to [[_COMMUNITY_ask_ai]]
- 11 edges to [[_COMMUNITY_test_pictures_first.py]]
- 11 edges to [[_COMMUNITY_write_json]]
- 11 edges to [[_COMMUNITY_time]]
- 11 edges to [[_COMMUNITY_test_topic_ideas.py]]
- 10 edges to [[_COMMUNITY_test_style.py]]
- 10 edges to [[_COMMUNITY_apply_review_fixes]]
- 10 edges to [[_COMMUNITY_test_story.py]]
- 10 edges to [[_COMMUNITY_words_of]]
- 9 edges to [[_COMMUNITY_fetch]]
- 9 edges to [[_COMMUNITY_captions]]
- 9 edges to [[_COMMUNITY_full_cues]]
- 9 edges to [[_COMMUNITY_test_blender_plan.py]]
- 8 edges to [[_COMMUNITY_prepare_topic]]
- 8 edges to [[_COMMUNITY_clean_photo]]
- 8 edges to [[_COMMUNITY_full_props]]
- 8 edges to [[_COMMUNITY_test_rules.py]]
- 7 edges to [[_COMMUNITY_test_h3_handoff.py]]
- 7 edges to [[_COMMUNITY_gather_pool]]
- 7 edges to [[_COMMUNITY_visual_review]]
- 7 edges to [[_COMMUNITY_test_first_second.py]]
- 7 edges to [[_COMMUNITY_h3_run.py]]
- 7 edges to [[_COMMUNITY_extra_sources.py]]
- 6 edges to [[_COMMUNITY_render_remotion]]
- 6 edges to [[_COMMUNITY_owner]]
- 6 edges to [[_COMMUNITY_blender_render.py]]
- 5 edges to [[_COMMUNITY_edit_plan]]
- 4 edges to [[_COMMUNITY_rewrite_paint_prompts]]
- 4 edges to [[_COMMUNITY_use]]
- 4 edges to [[_COMMUNITY_trim_borders]]
- 4 edges to [[_COMMUNITY_paint_instead]]
- 4 edges to [[_COMMUNITY_clean_look]]
- 4 edges to [[_COMMUNITY_rescue_graphics]]
- 4 edges to [[_COMMUNITY_test_blender_scene.py]]
- 3 edges to [[_COMMUNITY_OpeningRulesTests]]
- 3 edges to [[_COMMUNITY_sfx_events]]
- 3 edges to [[_COMMUNITY_run_agy]]
- 2 edges to [[_COMMUNITY_PreflightTests]]
- 2 edges to [[_COMMUNITY_write_scripts]]
- 2 edges to [[_COMMUNITY_first_second_check]]
- 2 edges to [[_COMMUNITY_recover_downloads]]
- 2 edges to [[_COMMUNITY_test_story_sound_library]]
- 2 edges to [[_COMMUNITY_Local GPU Worker]]
- 1 edge to [[_COMMUNITY_ReliabilityTests]]
- 1 edge to [[_COMMUNITY_MediaTests]]
- 1 edge to [[_COMMUNITY_MarkTests]]
- 1 edge to [[_COMMUNITY_limit_style]]
- 1 edge to [[_COMMUNITY_test_short_credit]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_quality_check]]
- 1 edge to [[_COMMUNITY_catalog_entries]]
- 1 edge to [[_COMMUNITY_run_remotion_with_fallback]]
- 1 edge to [[_COMMUNITY_build_scene.py]]
- 1 edge to [[_COMMUNITY_split_make_shorts.py]]

## Top bridge nodes
- [[test_full_scenes.py]] - degree 86, connects to 24 communities
- [[pathlib]] - degree 71, connects to 22 communities
- [[__init__.py]] - degree 65, connects to 18 communities
- [[plan_rules.py]] - degree 62, connects to 18 communities
- [[llm.py]] - degree 54, connects to 15 communities