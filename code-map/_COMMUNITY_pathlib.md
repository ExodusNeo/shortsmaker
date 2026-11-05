---
type: community
members: 64
---

# pathlib

**Members:** 64 nodes

## Members
- [[A Short's saved work state and `render()`, which turns a written Short into the…]] - rationale - shortsmaker/short_render.py
- [[A real FFmpegPython render with fake AI verifies stage saves, voice reuse and…]] - rationale - tests/test_render_resume.py
- [[Atomic progress records for unfinished Shorts; no executable serialized state.]] - rationale - shortsmaker/checkpoints.py
- [[Automatic checks on a finished Short, the AI visual review and its fixes (incl.…]] - rationale - shortsmaker/review.py
- [[Choosing each scene's picture, pictures for full-screen scenes, and rescue…]] - rationale - shortsmaker/picker.py
- [[Cleaning and validating the planner's JSON (graphics, full-screen scenes,…]] - rationale - shortsmaker/plan_rules.py
- [[Cleaning found photos stereograph cards, scanner borders, vertical crops.]] - rationale - shortsmaker/photo_prep.py
- [[Detail coordinates must be chosen on the framing that MarkCard actually…]] - rationale - tests/test_marks.py
- [[Draw a Short in Blender (2026-10-22) after the voice sets every scene's…]] - rationale - shortsmaker/blender_render.py
- [[Drawn openers (owner, 2026-10-30) scene 1 of an `opener animated` Short as a…]] - rationale - shortsmaker/drawn_opener.py
- [[Interruption recovery, narration reuse, honest review failures and bounded…]] - rationale - tests/test_reliability.py
- [[Local AI on the owner's GPU and helpers ComfyUIMOSS, VoiceStudio, Gemini…]] - rationale - shortsmaker/gpu.py
- [[One mid-scene frame per scene from the finished video, labeled with its…]] - rationale - shortsmaker/review.py
- [[Opening answer protection across planning, preview review and final drawn-…]] - rationale - tests/test_opening_rules.py
- [[Paths, fixed settings, palettes and the styleskin tables every module shares.…]] - rationale - shortsmaker/config.py
- [[Plain-language media.bat import, audition, approve and tune local media.]] - rationale - shortsmaker/media_menu.py
- [[Preview and apply a callout repair using existing videoaudio, without new AI…]] - rationale - shortsmaker/scene_repair.py
- [[Rendering a Short with Remotion (with the Python renderer as fallback),…]] - rationale - shortsmaker/remotion_render.py
- [[Shared opening instructions show the hook while protecting what the narration…]] - rationale - shortsmaker/opening_rules.py
- [[ShortsMaker make ready-to-upload YouTube Shorts. Entry point make_shorts.py.]] - rationale - shortsmaker/__init__.py
- [[Small shared helpers downloads, ffmpeg, video encoder choice, durations, JSON…]] - rationale - shortsmaker/media_tools.py
- [[Tests for the drawn opener (drawn_opener.py + drawn, 2026-10-30) the lint on…]] - rationale - tests/test_drawn_opener.py
- [[Tests for the motion-graphic opener on `opener animated` channels…]] - rationale - tests/test_opener_graphic.py
- [[The Python renderer camera moves, graphic overlays, person cards, clip…]] - rationale - shortsmaker/frame_render.py
- [[True only when a video is already vertical (916-ish, 720p+); horizontal videos…]] - rationale - shortsmaker/frame_render.py
- [[Voice, captions, sound effects, story sounds and music levels.]] - rationale - shortsmaker/audio_mix.py
- [[__init__.py]] - code - shortsmaker/__init__.py
- [[array]] - concept
- [[audio_mix.py]] - code - shortsmaker/audio_mix.py
- [[blender_render.py]] - code - shortsmaker/blender_render.py
- [[checkpoints.py]] - code - shortsmaker/checkpoints.py
- [[config.py]] - code - shortsmaker/config.py
- [[drawn_opener.py]] - code - shortsmaker/drawn_opener.py
- [[edit_plan.txt (the timestamped edit list) and per-scene cue timing.]] - rationale - shortsmaker/editplan.py
- [[editplan.py]] - code - shortsmaker/editplan.py
- [[fills_frame()]] - code - shortsmaker/frame_render.py
- [[frame_render.py]] - code - shortsmaker/frame_render.py
- [[gpu.py]] - code - shortsmaker/gpu.py
- [[hex_rgb()]] - code - shortsmaker/config.py
- [[io]] - concept
- [[luminance()_1]] - code - shortsmaker/config.py
- [[media_menu.py]] - code - shortsmaker/media_menu.py
- [[media_tools.py]] - code - shortsmaker/media_tools.py
- [[opening_rules.py]] - code - shortsmaker/opening_rules.py
- [[pathlib]] - concept
- [[photo_prep.py]] - code - shortsmaker/photo_prep.py
- [[picker.py]] - code - shortsmaker/picker.py
- [[pil]] - concept
- [[plan_rules.py]] - code - shortsmaker/plan_rules.py
- [[remotion_render.py]] - code - shortsmaker/remotion_render.py
- [[review.py]] - code - shortsmaker/review.py
- [[scene_repair.py]] - code - shortsmaker/scene_repair.py
- [[short_render.py]] - code - shortsmaker/short_render.py
- [[storyboard()]] - code - shortsmaker/review.py
- [[subprocess]] - concept
- [[test_drawn_opener.py]] - code - tests/test_drawn_opener.py
- [[test_marks.py]] - code - tests/test_marks.py
- [[test_opener_graphic.py]] - code - tests/test_opener_graphic.py
- [[test_opening_rules.py]] - code - tests/test_opening_rules.py
- [[test_reliability.py]] - code - tests/test_reliability.py
- [[test_render_resume.py]] - code - tests/test_render_resume.py
- [[urllib_request]] - concept
- [[warnings]] - concept
- [[wave]] - concept

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/pathlib
SORT file.name ASC
```

## Connections to other communities
- 137 edges to [[_COMMUNITY_llm.py]]
- 84 edges to [[_COMMUNITY_json]]
- 40 edges to [[_COMMUNITY_image_sources.py]]
- 38 edges to [[_COMMUNITY_test_full_scenes.py]]
- 17 edges to [[_COMMUNITY_ffmpeg]]
- 15 edges to [[_COMMUNITY_audio_library.py]]
- 14 edges to [[_COMMUNITY_re]]
- 13 edges to [[_COMMUNITY_edit_project.py]]
- 12 edges to [[_COMMUNITY_frame_maker]]
- 12 edges to [[_COMMUNITY_resume_runs]]
- 9 edges to [[_COMMUNITY_clean_photo]]
- 9 edges to [[_COMMUNITY_words_of]]
- 9 edges to [[_COMMUNITY_write_json]]
- 9 edges to [[_COMMUNITY_test_blender_render.py]]
- 8 edges to [[_COMMUNITY_make_opener]]
- 8 edges to [[_COMMUNITY_story_problems]]
- 8 edges to [[_COMMUNITY_clean_full]]
- 7 edges to [[_COMMUNITY_render]]
- 7 edges to [[_COMMUNITY_short]]
- 7 edges to [[_COMMUNITY_test_topic_ideas.py]]
- 7 edges to [[_COMMUNITY_ask_ai]]
- 6 edges to [[_COMMUNITY_finish_render]]
- 6 edges to [[_COMMUNITY_test_h3_handoff.py]]
- 6 edges to [[_COMMUNITY_opener_graphic]]
- 6 edges to [[_COMMUNITY_music_gain]]
- 6 edges to [[_COMMUNITY_h3_run.py]]
- 6 edges to [[_COMMUNITY_test_rules.py]]
- 6 edges to [[_COMMUNITY_test_pictures_first.py]]
- 6 edges to [[_COMMUNITY_test_style.py]]
- 5 edges to [[_COMMUNITY_visual_review]]
- 5 edges to [[_COMMUNITY_extra_sources.py]]
- 5 edges to [[_COMMUNITY_preview]]
- 5 edges to [[_COMMUNITY_edit_plan]]
- 5 edges to [[_COMMUNITY_test_blender_scene.py]]
- 5 edges to [[_COMMUNITY_test_blender_plan.py]]
- 4 edges to [[_COMMUNITY_opening_brief]]
- 4 edges to [[_COMMUNITY_scene_cues]]
- 4 edges to [[_COMMUNITY_use]]
- 4 edges to [[_COMMUNITY_callout_hold]]
- 4 edges to [[_COMMUNITY_style_library]]
- 4 edges to [[_COMMUNITY_paint_instead]]
- 3 edges to [[_COMMUNITY_duration]]
- 3 edges to [[_COMMUNITY_write_scripts]]
- 3 edges to [[_COMMUNITY_choose_images]]
- 3 edges to [[_COMMUNITY_test_ai_modes.py]]
- 2 edges to [[_COMMUNITY_OpeningRulesTests]]
- 2 edges to [[_COMMUNITY_rescue_graphics]]
- 2 edges to [[_COMMUNITY_sfx_events]]
- 2 edges to [[_COMMUNITY_write_frames]]
- 2 edges to [[_COMMUNITY_lint]]
- 2 edges to [[_COMMUNITY_prepare_topic]]
- 2 edges to [[_COMMUNITY_main_1]]
- 2 edges to [[_COMMUNITY_render_remotion]]
- 2 edges to [[_COMMUNITY_rewrite_paint_prompts]]
- 2 edges to [[_COMMUNITY_first_second_check]]
- 2 edges to [[_COMMUNITY_quality_check]]
- 2 edges to [[_COMMUNITY_drawn_thumbnail]]
- 2 edges to [[_COMMUNITY_gen.py]]
- 2 edges to [[_COMMUNITY_split_make_shorts.py]]
- 1 edge to [[_COMMUNITY_BlenderFailed]]
- 1 edge to [[_COMMUNITY_ReliabilityTests]]
- 1 edge to [[_COMMUNITY_MarkTests]]
- 1 edge to [[_COMMUNITY_dot-render_fixture]]
- 1 edge to [[_COMMUNITY_limit_style]]
- 1 edge to [[_COMMUNITY_wants_remotion]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_paint_new]]
- 1 edge to [[_COMMUNITY_get_image]]
- 1 edge to [[_COMMUNITY_build_scene.py]]

## Top bridge nodes
- [[pathlib]] - degree 71, connects to 22 communities
- [[plan_rules.py]] - degree 65, connects to 19 communities
- [[__init__.py]] - degree 65, connects to 18 communities
- [[subprocess]] - degree 54, connects to 18 communities
- [[review.py]] - degree 61, connects to 17 communities