---
type: community
members: 75
---

# test_full_scenes.py

**Members:** 75 nodes

## Members
- [[A Short's saved work state and `render()`, which turns a written Short into the…]] - rationale - shortsmaker/short_render.py
- [[A real FFmpegPython render with fake AI verifies stage saves, voice reuse and…]] - rationale - tests/test_render_resume.py
- [[Atomic progress records for unfinished Shorts; no executable serialized state.]] - rationale - shortsmaker/checkpoints.py
- [[Automatic checks on a finished Short, the AI visual review and its fixes (incl.…]] - rationale - shortsmaker/review.py
- [[Choosing each scene's picture, pictures for full-screen scenes, and rescue…]] - rationale - shortsmaker/picker.py
- [[Cleaning and validating the planner's JSON (graphics, full-screen scenes,…]] - rationale - shortsmaker/plan_rules.py
- [[Cleaning found photos stereograph cards, scanner borders, vertical crops.]] - rationale - shortsmaker/photo_prep.py
- [[Detail coordinates must be chosen on the framing that MarkCard actually…]] - rationale - tests/test_marks.py
- [[Drawn openers (owner, 2026-10-30) scene 1 of an `opener animated` Short as a…]] - rationale - shortsmaker/drawn_opener.py
- [[For tests that swap shortsmaker functions by name which module owns each one.]] - rationale - tests/patching.py
- [[Full-screen motion-graphic scenes and the AI-coded Custom scenes (with their…]] - rationale - shortsmaker/motion.py
- [[Headless Codex  Claude Code  Gemini (agy) calls that return JSON, with…]] - rationale - shortsmaker/llm.py
- [[Interruption recovery, narration reuse, honest review failures and bounded…]] - rationale - tests/test_reliability.py
- [[Opener preview repairs must be seen, archived and compared before adoption. No…]] - rationale - tests/test_opener_preflight.py
- [[Opening answer protection across planning, preview review and final drawn-…]] - rationale - tests/test_opening_rules.py
- [[Paths, fixed settings, palettes and the styleskin tables every module shares.…]] - rationale - shortsmaker/config.py
- [[Preview of every style-library preset for the owner each look on two real…]] - rationale - tests/render_style.py
- [[Render the opener composition study with the real hookcaptions; restore the…]] - rationale - tests/render_opener_preview.py
- [[Rendering a Short with Remotion (with the Python renderer as fallback),…]] - rationale - shortsmaker/remotion_render.py
- [[Retention screenshot handling, grounded scene timing, and no automatic logbook…]] - rationale - tests/test_retention.py
- [[Shared opening instructions show the hook while protecting what the narration…]] - rationale - shortsmaker/opening_rules.py
- [[ShortsMaker make ready-to-upload YouTube Shorts. Entry point make_shorts.py.]] - rationale - shortsmaker/__init__.py
- [[Tests for the full-screen motion graphic scenes. No AI usage, no rendering.…]] - rationale - tests/test_full_scenes.py
- [[Tests for the motion-graphic opener on `opener animated` channels…]] - rationale - tests/test_opener_graphic.py
- [[Tests for the style library looks, overlays, transitions, inventions (plain…]] - rationale - tests/test_style.py
- [[The Python renderer camera moves, graphic overlays, person cards, clip…]] - rationale - shortsmaker/frame_render.py
- [[The pictures gathered for a topic before writing, their catalog, cache and…]] - rationale - shortsmaker/picture_pool.py
- [[The style library invented looks, overlays and scene changes, candidates and…]] - rationale - shortsmaker/style_lab.py
- [[Visual skin for a Short's full-screen motion graphics (parchment, blueprint,…]] - rationale - shortsmaker/config.py
- [[__init__.py]] - code - shortsmaker/__init__.py
- [[array]] - concept
- [[checkpoints.py]] - code - shortsmaker/checkpoints.py
- [[config.py]] - code - shortsmaker/config.py
- [[drawn_opener.py]] - code - shortsmaker/drawn_opener.py
- [[edit_plan.txt (the timestamped edit list) and per-scene cue timing.]] - rationale - shortsmaker/editplan.py
- [[editplan.py]] - code - shortsmaker/editplan.py
- [[frame_render.py]] - code - shortsmaker/frame_render.py
- [[hex_rgb()]] - code - shortsmaker/config.py
- [[importlib]] - concept
- [[inspect]] - concept
- [[io]] - concept
- [[llm.py]] - code - shortsmaker/llm.py
- [[luminance()_1]] - code - shortsmaker/config.py
- [[motion.py]] - code - shortsmaker/motion.py
- [[opening_rules.py]] - code - shortsmaker/opening_rules.py
- [[patching.py]] - code - tests/patching.py
- [[pathlib]] - concept
- [[photo_prep.py]] - code - shortsmaker/photo_prep.py
- [[picker.py]] - code - shortsmaker/picker.py
- [[picture_pool.py]] - code - shortsmaker/picture_pool.py
- [[pil]] - concept
- [[pkgutil]] - concept
- [[plan_rules.py]] - code - shortsmaker/plan_rules.py
- [[remotion_render.py]] - code - shortsmaker/remotion_render.py
- [[render_opener_preview.py]] - code - tests/render_opener_preview.py
- [[render_style.py]] - code - tests/render_style.py
- [[review.py]] - code - shortsmaker/review.py
- [[short_render.py]] - code - shortsmaker/short_render.py
- [[short_skin()]] - code - shortsmaker/config.py
- [[style_lab.py]] - code - shortsmaker/style_lab.py
- [[sys]] - concept
- [[tempfile]] - concept
- [[test_clean_full_custom_and_skin()]] - code - tests/test_full_scenes.py
- [[test_full_scenes.py]] - code - tests/test_full_scenes.py
- [[test_marks.py]] - code - tests/test_marks.py
- [[test_opener_graphic.py]] - code - tests/test_opener_graphic.py
- [[test_opener_preflight.py]] - code - tests/test_opener_preflight.py
- [[test_opening_rules.py]] - code - tests/test_opening_rules.py
- [[test_reliability.py]] - code - tests/test_reliability.py
- [[test_render_resume.py]] - code - tests/test_render_resume.py
- [[test_retention.py]] - code - tests/test_retention.py
- [[test_style.py]] - code - tests/test_style.py
- [[unittest]] - concept
- [[unittest_mock]] - concept
- [[warnings]] - concept

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/test_full_scenespy
SORT file.name ASC
```

## Connections to other communities
- 132 edges to [[_COMMUNITY_re]]
- 57 edges to [[_COMMUNITY_json]]
- 55 edges to [[_COMMUNITY_image_sources.py]]
- 44 edges to [[_COMMUNITY_subprocess]]
- 25 edges to [[_COMMUNITY_write_scripts]]
- 19 edges to [[_COMMUNITY_code_custom_scenes]]
- 16 edges to [[_COMMUNITY_full_cues]]
- 15 edges to [[_COMMUNITY_test_pictures_first.py]]
- 13 edges to [[_COMMUNITY_frame_maker]]
- 13 edges to [[_COMMUNITY_invent_component]]
- 12 edges to [[_COMMUNITY_style_library]]
- 12 edges to [[_COMMUNITY_ask_ai]]
- 11 edges to [[_COMMUNITY_prepare_topic]]
- 11 edges to [[_COMMUNITY_footage.py]]
- 11 edges to [[_COMMUNITY_test_blender_plan.py]]
- 10 edges to [[_COMMUNITY_finish_render]]
- 10 edges to [[_COMMUNITY_clean_photo]]
- 10 edges to [[_COMMUNITY_test_first_second.py]]
- 10 edges to [[_COMMUNITY_approve_candidate]]
- 10 edges to [[_COMMUNITY_test_rules.py]]
- 9 edges to [[_COMMUNITY_opener_graphic]]
- 9 edges to [[_COMMUNITY_render]]
- 9 edges to [[_COMMUNITY_render_remotion]]
- 9 edges to [[_COMMUNITY_test_drawn_opener.py]]
- 8 edges to [[_COMMUNITY_retention.py]]
- 8 edges to [[_COMMUNITY_test_story.py]]
- 7 edges to [[_COMMUNITY_gather_pool]]
- 7 edges to [[_COMMUNITY_audio_library.py]]
- 6 edges to [[_COMMUNITY_make_opener]]
- 6 edges to [[_COMMUNITY_paint_opener_start]]
- 6 edges to [[_COMMUNITY_resume_runs]]
- 6 edges to [[_COMMUNITY_scene_cues]]
- 6 edges to [[_COMMUNITY_story_problems]]
- 6 edges to [[_COMMUNITY_apply_review_fixes]]
- 6 edges to [[_COMMUNITY_pack]]
- 6 edges to [[_COMMUNITY_h3_run.py]]
- 6 edges to [[_COMMUNITY_test_blender_scene.py]]
- 5 edges to [[_COMMUNITY_extra_sources.py]]
- 5 edges to [[_COMMUNITY_ask]]
- 5 edges to [[_COMMUNITY_make_paper]]
- 5 edges to [[_COMMUNITY_edit_plan]]
- 5 edges to [[_COMMUNITY_choose_images]]
- 5 edges to [[_COMMUNITY_plan_with]]
- 5 edges to [[_COMMUNITY_test_h3_handoff.py]]
- 5 edges to [[_COMMUNITY_qwen_voice.py]]
- 3 edges to [[_COMMUNITY_run_agy]]
- 3 edges to [[_COMMUNITY_rewrite_paint_prompts]]
- 3 edges to [[_COMMUNITY_paint_instead]]
- 3 edges to [[_COMMUNITY_fix_short]]
- 3 edges to [[_COMMUNITY_gen.py]]
- 2 edges to [[_COMMUNITY_OpeningRulesTests]]
- 2 edges to [[_COMMUNITY_PreflightTests]]
- 2 edges to [[_COMMUNITY_limit_style]]
- 2 edges to [[_COMMUNITY_test_story_sound_library]]
- 2 edges to [[_COMMUNITY_build_scene.py]]
- 2 edges to [[_COMMUNITY_split_make_shorts.py]]
- 1 edge to [[_COMMUNITY_RetentionTests]]
- 1 edge to [[_COMMUNITY_ReliabilityTests]]
- 1 edge to [[_COMMUNITY_MarkTests]]
- 1 edge to [[_COMMUNITY_dot-render_fixture]]
- 1 edge to [[_COMMUNITY_test_short_credit]]
- 1 edge to [[_COMMUNITY_lint]]
- 1 edge to [[_COMMUNITY_local_clips]]
- 1 edge to [[_COMMUNITY_pick_channel]]
- 1 edge to [[_COMMUNITY_music_gain]]
- 1 edge to [[_COMMUNITY_ffmpeg]]
- 1 edge to [[_COMMUNITY_quality_check]]
- 1 edge to [[_COMMUNITY_missing_parts]]
- 1 edge to [[_COMMUNITY_cold_read]]

## Top bridge nodes
- [[test_full_scenes.py]] - degree 91, connects to 24 communities
- [[pathlib]] - degree 71, connects to 21 communities
- [[sys]] - degree 43, connects to 18 communities
- [[__init__.py]] - degree 65, connects to 17 communities
- [[plan_rules.py]] - degree 65, connects to 17 communities