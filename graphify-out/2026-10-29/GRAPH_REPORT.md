# Graph Report - ShortsMaker  (2026-10-29)

## Corpus Check
- 129 files · ~154,818 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 2148 nodes · 5665 edges · 98 communities (87 shown, 11 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 128 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7ae9c2cd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_story.py
- toolkit.tsx
- ask_ai
- split_make_shorts.py
- test_full_scenes.py
- code_custom_scenes
- test_opener_scene.py
- Paper
- ffmpeg
- test_h3_handoff.py
- moves.py
- guarded.tsx
- make
- test_rules.py
- Journey.tsx
- BigNumber.tsx
- pool_of
- write_scripts
- Local GPU Worker
- style_library
- local_clips
- clean_full
- resolve_models
- test_blender_render.py
- test_blender_link.py
- ClipReader
- full_cues
- captions
- look.py
- parts.py
- math
- render_remotion
- templates.py
- image_sources.py
- qwen_voice.py
- owner
- build_scene.py
- h3_run.py
- load_model
- main
- Short.tsx
- json
- test_opener_plan.py
- cut
- subprocess
- Halftone.tsx
- re
- LinkError
- gather_pool
- main
- opener_graphic
- apply_review_fixes
- visual_review
- scene_kit.py
- sfx_events
- test_pictures_first.py
- test_opener_render.py
- pack_people.py
- test_blender_scene.py
- opener_checks.py
- Fake
- opener_scene.py
- look_toon.py
- paint_instead
- use_opener
- Shots
- test_blender_plan.py
- edit_scripts
- test_style.py
- limit_style
- words_of
- people_standin.py
- test_opener_checks.py
- review
- QuestionBeat.tsx
- test_short_credit
- frame_render.py
- film_piece
- rewrite_paint_prompts
- capture_prompts
- run_draft
- fix_short
- frame_maker
- render
- trim_borders
- default_build
- state
- write_frames
- draft_rules
- check_twists
- rescue_graphics
- article_text
- clamp
- thumbnail_order
- apply_look_scenes
- StopPicker

## God Nodes (most connected - your core abstractions)
1. `render()` - 62 edges
2. `write_scripts()` - 49 edges
3. `ask_ai()` - 40 edges
4. `render_opener()` - 33 edges
5. `run()` - 33 edges
6. `skinOf()` - 31 edges
7. `fixture()` - 31 edges
8. `cut()` - 29 edges
9. `main()` - 27 edges
10. `Paper()` - 25 edges

## Surprising Connections (you probably didn't know these)
- `test_numbers()` --calls--> `say_number()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_word_counts_match_the_scene_splitter()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_words_keep_what_is_written()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_every_aligned_word_is_in_the_aligner_alphabet()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_pixabay_keeps_only_on_topic_videos()` --calls--> `pixabay_films()`  [EXTRACTED]
  tests/test_pictures_first.py → shortsmaker/footage.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`
- 5-file cycle: `shortsmaker/blender_render.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py -> shortsmaker/opener_render.py -> shortsmaker/blender_render.py`

## Communities (98 total, 11 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.15
Nodes (21): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.14
Nodes (30): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+22 more)

### Community 2 - "test_story.py"
Cohesion: 0.09
Nodes (11): first_second_check(), story_problems(), run_check(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_must_be_a_later_real_picture(), test_opener_prompt_shows_each_scenes_line_and_picture(), test_no_hook_setting_no_hook_check() (+3 more)

### Community 3 - "toolkit.tsx"
Cohesion: 0.24
Nodes (20): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+12 more)

### Community 4 - "ask_ai"
Cohesion: 0.09
Nodes (16): seed_ideas(), ask_ai(), gemini_model(), quota_exhausted(), run_agy(), mark_details(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash() (+8 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.13
Nodes (12): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), redraw_custom() (+4 more)

### Community 8 - "test_opener_scene.py"
Cohesion: 0.06
Nodes (37): builds(), fixture(), people_lib(), run(), test_bad_plans_fail(), test_box_fall_rests_and_renders(), test_camera_follows_unasked(), test_chicken_chop_reference() (+29 more)

### Community 9 - "Paper"
Cohesion: 0.09
Nodes (36): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+28 more)

### Community 10 - "ffmpeg"
Cohesion: 0.36
Nodes (5): split_takes(), duration(), ffmpeg(), is_loop_short(), test_a_take_is_cut_between_the_scenes_words()

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "moves.py"
Cohesion: 0.12
Nodes (21): apply(), clear_distance(), clear_distance_at_end(), fall(), fly_off(), gait(), hop_off(), legs() (+13 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.11
Nodes (21): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+13 more)

### Community 14 - "make"
Cohesion: 0.15
Nodes (8): caption_layer(), make(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers(), videos()

### Community 15 - "test_rules.py"
Cohesion: 0.19
Nodes (21): parse_rules(), make(), stop_text(), test_bad_min_pictures_stops(), test_blender_needs_a_build_plan_section(), test_bom_and_crlf_load_the_same(), test_draft_stops(), test_duplicate_heading_stops() (+13 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.16
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "BigNumber.tsx"
Cohesion: 0.22
Nodes (13): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+5 more)

### Community 18 - "pool_of"
Cohesion: 0.11
Nodes (25): write_json(), catalog_entries(), catalog_pool(), clean_pics(), save_pool(), entry(), fake_ai, pic_short() (+17 more)

### Community 19 - "write_scripts"
Cohesion: 0.12
Nodes (21): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+13 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.06
Nodes (23): cut_text(), edit_plan(), look_text(), picture_line(), sentence_groups(), clean_invention(), clean_look(), clean_transition() (+15 more)

### Community 22 - "local_clips"
Cohesion: 0.11
Nodes (12): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt(), start_picture_problems() (+4 more)

### Community 23 - "clean_full"
Cohesion: 0.14
Nodes (15): clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number() (+7 more)

### Community 24 - "resolve_models"
Cohesion: 0.33
Nodes (3): pick_model(), resolve_models(), test_every_unfound_model_named_at_once()

### Community 25 - "test_blender_render.py"
Cohesion: 0.15
Nodes (15): BlenderFailed, peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws() (+7 more)

### Community 26 - "test_blender_link.py"
Cohesion: 0.11
Nodes (19): attribution(), call(), credit(), fetch_model(), ping(), search(), blender_note(), model_for() (+11 more)

### Community 27 - "ClipReader"
Cohesion: 0.19
Nodes (5): ClipReader, draw_card(), draw_graphic(), frame(), shot()

### Community 28 - "full_cues"
Cohesion: 0.13
Nodes (11): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish() (+3 more)

### Community 29 - "captions"
Cohesion: 0.12
Nodes (11): ass_time(), caption_lines(), captions(), styled(), speak(), story_sound(), tts(), ass_colour() (+3 more)

### Community 30 - "look.py"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (22): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+14 more)

### Community 32 - "math"
Cohesion: 0.08
Nodes (19): _append(), _attach(), _bake_free(), base_name(), _body_tree(), _clearance(), _clip(), _colour() (+11 more)

### Community 33 - "render_remotion"
Cohesion: 0.10
Nodes (13): short_skin(), ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props() (+5 more)

### Community 34 - "templates.py"
Cohesion: 0.16
Nodes (16): member(), Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), focus_object() (+8 more)

### Community 35 - "image_sources.py"
Cohesion: 0.08
Nodes (21): archive_films(), commons_films(), crop_film_bytes(), film_frames(), nasa_films(), pixabay_films(), archive_images(), article_images() (+13 more)

### Community 36 - "qwen_voice.py"
Cohesion: 0.12
Nodes (14): align(), align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak(), spoken_count() (+6 more)

### Community 37 - "owner"
Cohesion: 0.12
Nodes (10): owner(), _fake_planning(), test_director_prompt_mentions_full(), film(), plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library() (+2 more)

### Community 39 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 40 - "load_model"
Cohesion: 0.25
Nodes (4): ground_material(), load_model(), material(), merge()

### Community 41 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 42 - "Short.tsx"
Cohesion: 0.12
Nodes (20): Captions(), PersonCard(), Root(), Background(), Card, flashAlpha(), GraphicFor(), Move (+12 more)

### Community 43 - "json"
Cohesion: 0.07
Nodes (16): main(), freesound_fetch(), code_version(), channel_url(), trend_research(), yt_list(), comfy_call(), moss_graph() (+8 more)

### Community 44 - "test_opener_plan.py"
Cohesion: 0.07
Nodes (38): clean_opener(), _expect(), fill_template(), _keep(), _num(), plan_openers(), ask(), _size() (+30 more)

### Community 45 - "cut"
Cohesion: 0.07
Nodes (27): bm_area(), box_of(), centre(), clusters(), cut(), edge_point_local(), half(), handle_end_local() (+19 more)

### Community 46 - "subprocess"
Cohesion: 0.08
Nodes (11): music_gain(), master_gain(), shot_span(), fills_frame(), preview_sheet(), tsc_check(), storyboard(), main() (+3 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.19
Nodes (21): drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw(), Engraving() (+13 more)

### Community 48 - "re"
Cohesion: 0.07
Nodes (21): allowed_licence(), in_library(), words(), vault_page(), vault_refresh(), is_person_portrait(), parse_scene_money(), max_full() (+13 more)

### Community 50 - "gather_pool"
Cohesion: 0.12
Nodes (11): contact_sheets(), gather_pool(), load_pool(), pool_folder(), prepare_topic(), stubbed, test_empty_pool_drops_topic_without_ai(), test_gather_pool_shape() (+3 more)

### Community 51 - "main"
Cohesion: 0.09
Nodes (17): ask_count(), ask_yes(), load_channel(), new_channel(), pick_channel(), save_channel(), use_channel(), main() (+9 more)

### Community 52 - "opener_graphic"
Cohesion: 0.15
Nodes (10): full_props(), full_summary(), opener_graphic(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_full_summary(), test_model_graphic() (+2 more)

### Community 53 - "apply_review_fixes"
Cohesion: 0.12
Nodes (10): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full() (+2 more)

### Community 54 - "visual_review"
Cohesion: 0.14
Nodes (9): log_short(), clock(), overlay_notes(), quality_check(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose() (+1 more)

### Community 55 - "scene_kit.py"
Cohesion: 0.08
Nodes (25): facing_now(), _footprints(), _ground(), move(), pick_up(), prop_move(), _strip(), _travel() (+17 more)

### Community 56 - "sfx_events"
Cohesion: 0.18
Nodes (7): sfx_events(), full_pictures(), _board(), test_board_pictures_attached(), test_sfx_full(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 57 - "test_pictures_first.py"
Cohesion: 0.21
Nodes (14): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+6 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.17
Nodes (22): render_opener(), Env, _people_files(), short(), test_beats_scaled_into_scene(), test_cc_by_credit(), test_crash_retry_then_fallback(), test_failed_checks_fall_back_and_the_try_is_kept() (+14 more)

### Community 59 - "pack_people.py"
Cohesion: 0.26
Nodes (6): base_name(), clip_name(), front(), height(), main(), stride()

### Community 60 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.11
Nodes (21): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+13 more)

### Community 63 - "opener_scene.py"
Cohesion: 0.08
Nodes (22): State, beat_actors(), build_set(), camera(), dress_set(), first_hit(), main(), oc_moves() (+14 more)

### Community 64 - "look_toon.py"
Cohesion: 0.27
Nodes (4): apply(), ink(), outline(), toon()

### Community 65 - "paint_instead"
Cohesion: 0.18
Nodes (4): gemini_images(), to_vertical(), paint_instead(), test_remotion_failure_paints()

### Community 66 - "use_opener"
Cohesion: 0.13
Nodes (9): use_opener(), test_use_opener_failure_keeps_scene(), test_use_opener_never_raises(), test_use_opener_no_template_ai_clip(), test_use_opener_no_template_note(), test_use_opener_on_success(), test_use_opener_opening_note(), test_use_opener_planner_check() (+1 more)

### Community 67 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 68 - "test_blender_plan.py"
Cohesion: 0.24
Nodes (13): clean_build(), panels(), pick(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults(), test_clean_build_keeps_a_good_plan(), test_label_is_short_and_upper() (+5 more)

### Community 69 - "edit_scripts"
Cohesion: 0.11
Nodes (10): catalog_text(), is_usable(), pictures_of(), usable(), direct_scripts(), edit_scripts(), length_plan(), narration_lines() (+2 more)

### Community 70 - "test_style.py"
Cohesion: 0.07
Nodes (30): approve_candidate(), invent_component(), attempt(), invent_styles(), library_menu(), lint_style_code(), reject_candidate(), restore_style_slots() (+22 more)

### Community 72 - "words_of"
Cohesion: 0.19
Nodes (8): clean_sound(), limit_sounds(), graphic_low(), fill_money_graphics(), words_of(), test_clean_sound(), test_fill_money_graphics_and_caps(), test_clean_full_keeps_board_pic()

### Community 73 - "people_standin.py"
Cohesion: 0.29
Nodes (5): body(), clip(), key(), main(), part()

### Community 74 - "test_opener_checks.py"
Cohesion: 0.30
Nodes (10): results(), test_blade_face(), test_cut_result(), test_edge_leads(), test_first_frame(), test_hidden(), test_in_frame(), test_moves_visibly() (+2 more)

### Community 75 - "review"
Cohesion: 0.18
Nodes (5): _cast_note(), review(), review_frames(), to_glb(), test_review_frames_include_key_moments()

### Community 76 - "QuestionBeat.tsx"
Cohesion: 0.33
Nodes (4): FONT, theme, CLAMP, KineticTitle()

### Community 78 - "frame_render.py"
Cohesion: 0.13
Nodes (12): fit_font(), graphic_overlay(), person_card(), thumbnail(), clean_photo(), drawn_thumbnail(), drawn_short(), jpeg() (+4 more)

### Community 80 - "rewrite_paint_prompts"
Cohesion: 0.18
Nodes (5): rewrite_paint_prompts(), ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 81 - "capture_prompts"
Cohesion: 0.18
Nodes (7): load_rules(), min_real_pictures(), test_channels_have_opener_rules(), capture_prompts(), ask(), test_load_rules_sets_session(), test_strange_history_prompts_unchanged()

### Community 82 - "run_draft"
Cohesion: 0.31
Nodes (8): draft_reply(), run_draft(), test_draft_blender_channel_needs_build_plan(), test_draft_keeps_ai_headings_inside_their_section(), test_draft_never_overwrites(), test_draft_retries_once_then_stops(), test_draft_settings_come_from_code(), test_draft_writes_tagged_draft_file()

### Community 83 - "fix_short"
Cohesion: 0.22
Nodes (6): ask_brain(), ask_number(), fix_short(), test_fix_bat_explains_a_drawn_short(), test_solo_brain_selection_options(), test_fix_checks_rules_before_asking_for_a_scene()

### Community 84 - "frame_maker"
Cohesion: 0.22
Nodes (3): frame_maker(), credit_tag_image(), fallback_graphic()

### Community 85 - "render"
Cohesion: 0.09
Nodes (12): make_sfx(), short_credit(), graphics_count(), wants_remotion(), srt(), drawn_choices(), load_state(), render() (+4 more)

### Community 86 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

### Community 87 - "default_build"
Cohesion: 0.25
Nodes (5): default_build(), plan_builds(), test_default_build_shape(), test_plan_builds_retries_then_defaults(), ask()

### Community 88 - "state"
Cohesion: 0.39
Nodes (7): swap_pictures(), real(), state(), test_opener_fix_swaps_once(), test_swap_ignores_a_clip_already_dropped(), test_swap_moves_the_owners_clip_with_its_picture(), test_swap_pictures_trades_real_pictures()

### Community 89 - "write_frames"
Cohesion: 0.29
Nodes (3): flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 90 - "draft_rules"
Cohesion: 0.33
Nodes (3): draft_rules(), require_rules(), test_missing_rules_file_is_drafted()

### Community 91 - "check_twists"
Cohesion: 0.47
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 92 - "rescue_graphics"
Cohesion: 0.40
Nodes (3): full_formats(), rescue_graphics(), test_rescue_respects_caps()

### Community 93 - "article_text"
Cohesion: 0.40
Nodes (3): article_text(), fact_check(), test_fact_check_drops_full()

## Knowledge Gaps
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `templates.py`, `Shots`, `build_scene.py`, `json`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.14583333333333334 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `test_story.py`, `ask_ai`, `test_full_scenes.py`, `ffmpeg`, `make`, `style_library`, `local_clips`, `test_blender_render.py`, `full_cues`, `captions`, `render_remotion`, `json`, `subprocess`, `re`, `main`, `opener_graphic`, `apply_review_fixes`, `visual_review`, `sfx_events`, `test_pictures_first.py`, `paint_instead`, `use_opener`, `test_style.py`, `words_of`, `frame_render.py`, `fix_short`, `frame_maker`, `write_frames`, `rescue_graphics`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.13513513513513514 - nodes in this community are weakly interconnected._
- **Why does `render_opener()` connect `test_opener_render.py` to `use_opener`, `test_full_scenes.py`, `ffmpeg`, `json`, `test_opener_plan.py`, `review`, `local_clips`, `resolve_models`, `test_blender_render.py`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Should `test_story.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08602150537634409 - nodes in this community are weakly interconnected._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.09230769230769231 - nodes in this community are weakly interconnected._