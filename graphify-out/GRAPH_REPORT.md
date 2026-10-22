# Graph Report - ShortsMaker  (2026-10-22)

## Corpus Check
- 91 files · ~91,201 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .canvas 1)

## Summary
- 1192 nodes · 3264 edges · 61 communities (53 shown, 8 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 59 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1f987d44`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- clean_full
- skinOf
- re
- split_make_shorts.py
- plan_rules.py
- ask_ai
- full_cues
- toolkit.tsx
- audio_mix.py
- get_image
- motion.py
- guarded.tsx
- test_edit_project.py
- test_rules.py
- Journey.tsx
- full/types.ts
- prepare_topic
- test_pictures_first.py
- gen.py
- approve_candidate
- choose_images
- ClipReader
- json
- write_scripts
- gather_pool
- frame_maker
- style_library
- local_job
- render
- test_full_scenes.py
- apply_review_fixes
- render_remotion
- test_style.py
- invent_component
- qwen_voice.py
- test_first_second.py
- edit_plan
- ffmpeg
- clean_photo
- clean_look
- Short.tsx
- test_story.py
- film_piece
- clean_pics
- planning_ai
- Halftone.tsx
- wm_files
- captions
- _fake_planning
- random
- full_props
- limit_style
- catalog_entries
- limit_sounds
- short_skin
- srt
- limit_full
- paint_instead
- review_fixes

## God Nodes (most connected - your core abstractions)
1. `render()` - 56 edges
2. `write_scripts()` - 38 edges
3. `ask_ai()` - 30 edges
4. `skinOf()` - 29 edges
5. `Paper()` - 25 edges
6. `main()` - 25 edges
7. `choose_images()` - 23 edges
8. `clean_full()` - 21 edges
9. `style_library()` - 20 edges
10. `pool_of()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `test_numbers()` --calls--> `say_number()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_word_counts_match_the_scene_splitter()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_words_keep_what_is_written()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_every_aligned_word_is_in_the_aligner_alphabet()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_new_channel_stops_for_review()` --calls--> `pick_channel()`  [EXTRACTED]
  tests/test_rules.py → shortsmaker/channel_profiles.py

## Import Cycles
- None detected.

## Communities (61 total, 8 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.17
Nodes (29): card, clamp, DotGrid(), MarkCard(), Props, StatCard(), TimelineCard(), clamp (+21 more)

### Community 2 - "clean_full"
Cohesion: 0.11
Nodes (19): rescue_graphics(), clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures() (+11 more)

### Community 3 - "skinOf"
Cohesion: 0.18
Nodes (23): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+15 more)

### Community 4 - "re"
Cohesion: 0.07
Nodes (24): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+16 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "plan_rules.py"
Cohesion: 0.15
Nodes (4): hex_rgb(), luminance(), library_menu(), reject_candidate()

### Community 7 - "ask_ai"
Cohesion: 0.11
Nodes (10): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), mark_details(), rewrite_paint_prompts(), test_argon_out_of_quota_switches_to_flash(), test_claude_pinned_to_opus_high() (+2 more)

### Community 8 - "full_cues"
Cohesion: 0.14
Nodes (9): scene_cues(), person_card(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback() (+1 more)

### Community 9 - "toolkit.tsx"
Cohesion: 0.15
Nodes (25): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+17 more)

### Community 10 - "audio_mix.py"
Cohesion: 0.10
Nodes (6): clean_sound(), freesound_fetch(), music_gain(), flash_alpha(), main(), props_for()

### Community 11 - "get_image"
Cohesion: 0.25
Nodes (4): get_image(), openverse_images(), ov_get(), full_pictures()

### Community 12 - "motion.py"
Cohesion: 0.13
Nodes (13): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), graphics_count(), lint_custom_code(), look_and_fix(), preview_custom() (+5 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.14
Nodes (17): Box, boxAt(), clamp, fitCard(), hits(), layoutColumn(), layoutGrid(), layoutRow() (+9 more)

### Community 14 - "test_edit_project.py"
Cohesion: 0.12
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (36): load_rules(), min_real_pictures(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft() (+28 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "full/types.ts"
Cohesion: 0.16
Nodes (18): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), gridFor(), FullScene() (+10 more)

### Community 18 - "prepare_topic"
Cohesion: 0.20
Nodes (8): write_json(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_pool_roundtrip(), test_pool_rows_without_thumbs()

### Community 19 - "test_pictures_first.py"
Cohesion: 0.19
Nodes (20): catalog_pool(), entry(), fake_ai, film(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film() (+12 more)

### Community 20 - "gen.py"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "approve_candidate"
Cohesion: 0.23
Nodes (9): approve_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_candidate_names_unique_across_kinds() (+1 more)

### Community 22 - "choose_images"
Cohesion: 0.25
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 23 - "ClipReader"
Cohesion: 0.16
Nodes (6): ClipReader, draw_card(), draw_graphic(), frame(), shot(), write_frames()

### Community 24 - "json"
Cohesion: 0.08
Nodes (16): archive_films(), nasa_films(), pixabay_films(), comfy_call(), moss_graph(), moss_images(), voicestudio_unload(), voicestudio_up() (+8 more)

### Community 25 - "write_scripts"
Cohesion: 0.16
Nodes (16): write_scripts(), passing(), prepare(), planning, test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), test_both_mode_reuses_pools() (+8 more)

### Community 26 - "gather_pool"
Cohesion: 0.12
Nodes (5): gather_pool(), owner(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 27 - "frame_maker"
Cohesion: 0.12
Nodes (8): fills_frame(), fit_font(), frame_maker(), graphic_low(), graphic_overlay(), thumbnail(), credit_tag_image(), fallback_graphic()

### Community 28 - "style_library"
Cohesion: 0.18
Nodes (7): cut_text(), look_text(), style_library(), style_rules(), write_style_index(), test_library_entries_have_fields(), test_write_style_index_is_deterministic()

### Community 29 - "local_job"
Cohesion: 0.14
Nodes (9): local_job(), local_voice(), sentence_groups(), build(), add(), main(), test_local_job_retries_a_hard_crash(), scenes() (+1 more)

### Community 30 - "render"
Cohesion: 0.14
Nodes (10): story_sound(), short_credit(), clock(), first_second_check(), storyboard(), visual_review(), load_state(), render() (+2 more)

### Community 31 - "test_full_scenes.py"
Cohesion: 0.10
Nodes (17): sfx_events(), _board(), _jpg(), test_board_pictures_attached(), test_code_custom_scenes_fallback(), test_custom_cues_props_and_pictures(), test_ink_silhouette(), test_lint_custom_code() (+9 more)

### Community 32 - "apply_review_fixes"
Cohesion: 0.12
Nodes (10): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full() (+2 more)

### Community 33 - "render_remotion"
Cohesion: 0.16
Nodes (9): render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain() (+1 more)

### Community 34 - "test_style.py"
Cohesion: 0.12
Nodes (11): wants_remotion(), apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics() (+3 more)

### Community 35 - "invent_component"
Cohesion: 0.12
Nodes (16): invent_component(), attempt(), invent_styles(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others() (+8 more)

### Community 36 - "qwen_voice.py"
Cohesion: 0.13
Nodes (11): align(), align_words(), main(), say_number(), studio_speak(), spoken_count(), test_caption_word_counts_match_the_scene_splitter(), test_caption_words_keep_what_is_written() (+3 more)

### Community 37 - "test_first_second.py"
Cohesion: 0.22
Nodes (10): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once() (+2 more)

### Community 38 - "edit_plan"
Cohesion: 0.33
Nodes (3): edit_plan(), picture_line(), test_edit_plan_picture_line()

### Community 39 - "ffmpeg"
Cohesion: 0.16
Nodes (11): shot_span(), cover_crop(), local_clips(), motion_prompt(), split_takes(), veo_handoff(), duration(), ffmpeg() (+3 more)

### Community 40 - "clean_photo"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 41 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 42 - "Short.tsx"
Cohesion: 0.12
Nodes (21): Captions(), HookTitle(), PersonCard(), Root(), Background(), Card, flashAlpha(), GraphicFor() (+13 more)

### Community 43 - "test_story.py"
Cohesion: 0.10
Nodes (9): pictures_of(), quality_check(), direct_scripts(), edit_scripts(), length_plan(), narration_lines(), story_problems(), test_editor_gets_one_second_pass_for_broken_rules() (+1 more)

### Community 44 - "film_piece"
Cohesion: 0.20
Nodes (4): crop_film_bytes(), film_frames(), film_piece(), film_ffmpeg()

### Community 45 - "clean_pics"
Cohesion: 0.25
Nodes (4): catalog_text(), clean_pics(), is_usable(), usable()

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "wm_files"
Cohesion: 0.12
Nodes (10): commons_films(), article_images(), commons_search(), thumb_url(), usable_license(), wm_files(), wm_get(), article_text() (+2 more)

### Community 49 - "captions"
Cohesion: 0.16
Nodes (7): ass_time(), caption_lines(), captions(), styled(), speak(), tts(), ass_colour()

### Community 50 - "_fake_planning"
Cohesion: 0.17
Nodes (6): _fake_planning(), ask(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 51 - "random"
Cohesion: 0.18
Nodes (4): make_sfx(), ink_silhouette(), make_paper(), test_make_paper()

### Community 52 - "full_props"
Cohesion: 0.29
Nodes (4): full_props(), full_summary(), test_full_props_figure(), test_full_summary()

### Community 59 - "paint_instead"
Cohesion: 0.18
Nodes (4): gemini_images(), to_vertical(), paint_instead(), test_remotion_failure_paints()

## Knowledge Gaps
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `clean_full`, `re`, `plan_rules.py`, `ask_ai`, `full_cues`, `audio_mix.py`, `motion.py`, `test_edit_project.py`, `choose_images`, `ClipReader`, `json`, `frame_maker`, `local_job`, `test_full_scenes.py`, `apply_review_fixes`, `render_remotion`, `test_style.py`, `edit_plan`, `ffmpeg`, `clean_photo`, `test_story.py`, `captions`, `random`, `full_props`, `srt`, `paint_instead`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.1282051282051282 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `clean_full`, `test_style.py`, `re`, `plan_rules.py`, `ask_ai`, `clean_look`, `audio_mix.py`, `test_story.py`, `clean_pics`, `test_rules.py`, `wm_files`, `prepare_topic`, `_fake_planning`, `limit_style`, `limit_sounds`, `json`, `limit_full`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Should `clean_full` be split into smaller, more focused modules?**
  _Cohesion score 0.11076923076923077 - nodes in this community are weakly interconnected._
- **Why does `save_candidate()` connect `json` to `test_style.py`, `invent_component`, `re`, `plan_rules.py`, `approve_candidate`, `style_library`, `render`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Should `re` be split into smaller, more focused modules?**
  _Cohesion score 0.06802721088435375 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._