# Graph Report - ShortsMaker  (2026-11-06)

## Corpus Check
- 149 files · ~192,839 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2460 nodes · 6765 edges · 115 communities (95 shown, 20 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 141 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5b9a1015`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- catalog_pool
- prepare_topic
- test_blender_scene.py
- split_make_shorts.py
- render_remotion
- test_full_scenes.py
- short_render.py
- guarded.tsx
- k
- test_h3_handoff.py
- drawn_opener.py
- opener_crew.py
- finish_render
- test_rules.py
- Journey.tsx
- toolkit.tsx
- gpu.py
- write_scripts
- gen.py
- clamp
- footage.py
- edit_project.py
- Pen
- test_topic_ideas.py
- checkpoints.py
- frame_maker
- json
- full_cues
- look.py
- parts.py
- OpeningRulesTests
- gather_pool
- templates.py
- render
- main
- BigNumber.tsx
- main
- Paper
- local_clips
- build_scene.py
- Short.tsx
- core.mjs
- scene_cues
- check_twists
- extra_sources.py
- Halftone.tsx
- clean_photo
- test_blender_render.py
- fake_ai
- test_story.py
- invent_component
- test_opener_crew.py
- kit.mjs
- RetentionTests
- retention.py
- ffmpeg
- ReliabilityTests
- edit_plan
- run_agy
- opener3d.py
- drawn_thumbnail
- ends_sentence
- hashlib
- media_menu.py
- music_gain
- film_piece
- kit_parts.mjs
- test_first_second.py
- apply_review_fixes
- clean_full
- qwen_voice.py
- ask_ai
- pathlib
- audio_library.py
- Opener3D.tsx
- captions
- style_library
- scenes
- popS
- approve_candidate
- sfx_events
- MediaTests
- MetadataTests
- makeKit
- PreflightTests
- MarkTests
- StoryPacingTests
- test_pictures_first.py
- test_style.py
- short
- test_blender_plan.py
- FeedbackTests
- paint_new
- .render_fixture
- test_story_sound_library
- render
- cold_read
- other_ai
- lint_cutout
- write_frames
- log_short
- limit_style
- owner
- edit_scripts
- test_weak_opener_graphic_fixes_then_handoff
- gemini_model
- apply_metadata
- umbrellas.mjs
- battery.mjs
- re
- telegraph_sounder.mjs
- BlenderFailed
- draft_rules

## God Nodes (most connected - your core abstractions)
1. `k` - 100 edges
2. `render()` - 64 edges
3. `write_scripts()` - 54 edges
4. `ask_ai()` - 53 edges
5. `makeKit()` - 36 edges
6. `clamp()` - 35 edges
7. `MediaTests` - 35 edges
8. `main()` - 32 edges
9. `skinOf()` - 31 edges
10. `ellPts()` - 30 edges

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
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`
- 3-file cycle: `shortsmaker/motion.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`
- 4-file cycle: `shortsmaker/motion.py -> shortsmaker/opening_rules.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`

## Communities (115 total, 20 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (23): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+15 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (30): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+22 more)

### Community 2 - "catalog_pool"
Cohesion: 0.18
Nodes (17): catalog_entries(), catalog_pool(), clean_pics(), entry(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film() (+9 more)

### Community 3 - "prepare_topic"
Cohesion: 0.11
Nodes (15): catalog_text(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures(), prepare_topic(), save_pool() (+7 more)

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "render_remotion"
Cohesion: 0.16
Nodes (9): render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain() (+1 more)

### Community 7 - "test_full_scenes.py"
Cohesion: 0.07
Nodes (32): short_skin(), clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), full_props(), full_summary(), is_payoff() (+24 more)

### Community 8 - "short_render.py"
Cohesion: 0.12
Nodes (4): hex_rgb(), luminance(), make_paper(), test_make_paper()

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.05
Nodes (37): call(), fit_start(), frames(), graph(), main(), saved_file(), h3_problems(), h3_prompt() (+29 more)

### Community 12 - "drawn_opener.py"
Cohesion: 0.10
Nodes (13): available(), clean_code(), fingerprint(), lint(), look_dir(), make_opener(), node_run(), review() (+5 more)

### Community 13 - "opener_crew.py"
Cohesion: 0.11
Nodes (18): minutes(), opener_role(), staging_line(), animal_cutout(), default_cutout(), kit_hats(), kit_text(), lint_part() (+10 more)

### Community 14 - "finish_render"
Cohesion: 0.08
Nodes (19): clock(), drawn_answer_problem(), overlay_notes(), pacing_check(), quality_check(), review_status(), sound_masking(), status_lines() (+11 more)

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (39): load_rules(), min_real_pictures(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft() (+31 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.26
Nodes (20): CustomScene(), ExampleOpenerAction(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear() (+12 more)

### Community 18 - "gpu.py"
Cohesion: 0.10
Nodes (10): main(), comfy_call(), moss_graph(), moss_images(), voicestudio_unload(), voicestudio_up(), prune_cache(), library_menu() (+2 more)

### Community 19 - "write_scripts"
Cohesion: 0.11
Nodes (25): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+17 more)

### Community 20 - "gen.py"
Cohesion: 0.22
Nodes (5): images(), main(), t5_encoder(), tts(), video()

### Community 21 - "clamp"
Cohesion: 0.10
Nodes (9): clamp(), eBounce(), eElastic(), eExpo(), eIn(), eIO(), ik(), lerp() (+1 more)

### Community 22 - "footage.py"
Cohesion: 0.06
Nodes (23): archive_ad_films(), archive_films(), commons_films(), duke_films(), nasa_films(), pixabay_films(), archive_images(), get_image() (+15 more)

### Community 23 - "edit_project.py"
Cohesion: 0.13
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "Pen"
Cohesion: 0.14
Nodes (9): catmull(), centroid(), densify(), eOut(), INK, noise1(), pathOf(), idHash() (+1 more)

### Community 25 - "test_topic_ideas.py"
Cohesion: 0.14
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 26 - "checkpoints.py"
Cohesion: 0.25
Nodes (12): begin(), context(), pack(), pending(), pending_topics(), read(), save_context(), unpack() (+4 more)

### Community 27 - "frame_maker"
Cohesion: 0.08
Nodes (14): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), frame_maker(), frame(), graphic_low() (+6 more)

### Community 28 - "json"
Cohesion: 0.07
Nodes (20): channel_url(), new_channel(), pick_channel(), save_channel(), seed_ideas(), trend_research(), yt_list(), opening_brief() (+12 more)

### Community 29 - "full_cues"
Cohesion: 0.20
Nodes (6): full_cues(), spoken_at(), spoken_span(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish()

### Community 30 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 33 - "gather_pool"
Cohesion: 0.11
Nodes (9): article_images(), commons_search(), thumb_url(), wm_files(), balanced_candidates(), gather_pool(), stubbed, test_gather_pool_shape() (+1 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "render"
Cohesion: 0.06
Nodes (19): make_sfx(), gemini_images(), short_credit(), graphics_count(), to_vertical(), is_loop_short(), ink_silhouette(), paint_instead() (+11 more)

### Community 36 - "main"
Cohesion: 0.13
Nodes (16): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), load_channel(), normalize_brain(), use_channel() (+8 more)

### Community 37 - "BigNumber.tsx"
Cohesion: 0.22
Nodes (13): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+5 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.12
Nodes (29): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+21 more)

### Community 40 - "local_clips"
Cohesion: 0.10
Nodes (13): cosy_instruct(), cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt() (+5 more)

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (17): Captions(), PersonCard(), Background(), Card, flashAlpha(), GraphicFor(), Move, Scene (+9 more)

### Community 43 - "core.mjs"
Cohesion: 0.14
Nodes (30): burst(), ellipse(), fibre(), fill(), _grain, grainCanvas(), grainOver(), hash() (+22 more)

### Community 44 - "scene_cues"
Cohesion: 0.18
Nodes (9): scene_cues(), read_need(), callout_hold(), drop_unreadable_kinetic(), test_counter_finishes_before_it_leaves(), test_short_scene_callout_is_placed_so_the_check_passes(), test_graphic_card_hold_duration(), test_person_card_hold_and_exit_gap() (+1 more)

### Community 45 - "check_twists"
Cohesion: 0.47
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 46 - "extra_sources.py"
Cohesion: 0.17
Nodes (15): brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images(), loc_images() (+7 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "clean_photo"
Cohesion: 0.16
Nodes (7): clean_photo(), is_stereo(), trim_borders(), border(), plain(), vertical_image(), contact_sheets()

### Community 49 - "test_blender_render.py"
Cohesion: 0.18
Nodes (15): peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises() (+7 more)

### Community 50 - "fake_ai"
Cohesion: 0.14
Nodes (10): entry_age(), logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_catalog_empty_pool_no_ai(), test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list() (+2 more)

### Community 51 - "test_story.py"
Cohesion: 0.22
Nodes (10): first_sentence(), story_problems(), read(), test_cold_read_verdicts(), test_first_sentence_reads_across_the_cut(), test_no_hook_setting_no_hook_check(), test_rules_accept_opener_setting(), test_story_problems() (+2 more)

### Community 52 - "invent_component"
Cohesion: 0.11
Nodes (16): clean_style_code(), invent_component(), attempt(), invent_styles(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview() (+8 more)

### Community 53 - "test_opener_crew.py"
Cohesion: 0.24
Nodes (10): check_staging(), fake(), short(), staging(), test_a_failed_part_falls_back_to_its_substitute(), test_a_made_part_is_kept_and_reused_with_no_ai(), test_a_painter_with_unusable_code_gets_the_plain_kit_cutout(), test_parallel_calls_are_capped() (+2 more)

### Community 54 - "kit.mjs"
Cohesion: 0.10
Nodes (23): flat, fx, job, C, H, lightOf(), MADE, MOODS (+15 more)

### Community 56 - "retention.py"
Cohesion: 0.20
Nodes (11): analyze(), edit_metrics(), load_metrics(), metrics_text(), normalize_metrics(), normalize_reply(), observations(), parse_metric() (+3 more)

### Community 57 - "ffmpeg"
Cohesion: 0.21
Nodes (8): split_takes(), duration(), ffmpeg(), write_json(), apply(), preview(), save_state(), test_a_take_is_cut_between_the_scenes_words()

### Community 59 - "edit_plan"
Cohesion: 0.17
Nodes (6): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 60 - "run_agy"
Cohesion: 0.18
Nodes (7): argon_out(), quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "opener3d.py"
Cohesion: 0.10
Nodes (24): box_of(), clean(), front_door(), half_width(), in_order(), inside(), nudge(), num() (+16 more)

### Community 62 - "drawn_thumbnail"
Cohesion: 0.21
Nodes (9): thumbnail_order(), drawn_thumbnail(), test_thumbnail_order_skips_film_and_puts_openers_first(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 63 - "ends_sentence"
Cohesion: 0.25
Nodes (5): sentence_groups(), ends_sentence(), srt(), test_sentence_ends_include_curly_quotes_and_ellipsis(), test_sentences_running_across_cuts_are_one_take()

### Community 64 - "hashlib"
Cohesion: 0.31
Nodes (4): code_version(), load(), save(), signature()

### Community 65 - "media_menu.py"
Cohesion: 0.20
Nodes (10): freesound_fetch(), freesound_preview(), freesound_results(), settings(), audition_audio(), download_audio_choices(), media_command(), print_source_status() (+2 more)

### Community 66 - "music_gain"
Cohesion: 0.22
Nodes (4): music_gain(), speak(), tts(), test_music_gain_evens_out_tracks()

### Community 67 - "film_piece"
Cohesion: 0.22
Nodes (5): crop_film_bytes(), crop_filter(), film_frames(), film_piece(), film_ffmpeg()

### Community 69 - "test_first_second.py"
Cohesion: 0.18
Nodes (14): first_second_check(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture() (+6 more)

### Community 70 - "apply_review_fixes"
Cohesion: 0.12
Nodes (9): apply_review_fixes(), ask(), _review_state(), test_auto_fix_graphic(), test_look_check_fixes_code(), test_redraw_failure_paints(), test_review_redraws_custom(), test_review_uses_unused_pool_pictures_before_painting() (+1 more)

### Community 71 - "clean_full"
Cohesion: 0.07
Nodes (27): clean_sound(), limit_sounds(), clean_full(), word(), clean_graphic(), contains(), coords(), fill_money_graphics() (+19 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.12
Nodes (14): align(), align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak(), spoken_count() (+6 more)

### Community 73 - "ask_ai"
Cohesion: 0.13
Nodes (12): ask_ai(), test_every_ai_gets_the_pipeline_preamble_once(), test_quota_fallback_both_ways(), test_claude_pinned_to_opus_high(), test_encoder_cache_lives_with_video_encoder(), test_fake_reaches_callers(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash(), test_independent_review_falls_back_without_changing_solo_mode() (+4 more)

### Community 75 - "audio_library.py"
Cohesion: 0.24
Nodes (15): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+7 more)

### Community 76 - "Opener3D.tsx"
Cohesion: 0.07
Nodes (43): aim(), BOOKS, Box(), Building(), Burst(), calculateOpener3D(), CameraRig(), Card() (+35 more)

### Community 77 - "captions"
Cohesion: 0.29
Nodes (4): ass_time(), caption_lines(), caption_size(), captions()

### Community 78 - "style_library"
Cohesion: 0.13
Nodes (12): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), test_invented_look_needs_fallback() (+4 more)

### Community 79 - "scenes"
Cohesion: 0.40
Nodes (5): build(), add(), main(), scenes(), test_logbook_hook_line_is_the_whole_first_sentence()

### Community 81 - "approve_candidate"
Cohesion: 0.18
Nodes (11): approve_candidate(), save_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes() (+3 more)

### Community 82 - "sfx_events"
Cohesion: 0.25
Nodes (4): schedule_sounds(), sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 85 - "makeKit"
Cohesion: 0.26
Nodes (9): makeKit(), rrect(), ss(), arm(), bubble(), bust(), hat(), person() (+1 more)

### Community 89 - "test_pictures_first.py"
Cohesion: 0.19
Nodes (15): choose_images(), film(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+7 more)

### Community 90 - "test_style.py"
Cohesion: 0.15
Nodes (10): wants_remotion(), apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_director_character_look_is_kept_short_or_dropped(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library() (+2 more)

### Community 91 - "short"
Cohesion: 0.19
Nodes (8): fake_ai(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused(), test_drawn_opener_stops_when_a_fix_does_not_help(), test_no_verdict_is_not_a_pass(), test_reveal_scene_is_drawn_with_its_own_rules(), test_use_opener_plays_the_drawn_opener()

### Community 92 - "test_blender_plan.py"
Cohesion: 0.12
Nodes (20): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), plan() (+12 more)

### Community 94 - "paint_new"
Cohesion: 0.33
Nodes (4): use_picture_from(), paint_new(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 96 - "test_story_sound_library"
Cohesion: 0.67
Nodes (3): test_story_sound_library(), fetch(), _tone_wav()

### Community 97 - "render"
Cohesion: 0.15
Nodes (7): sheet_times(), blends(), render(), sheet(), sheet_times(), test_a_cutout_that_melts_into_the_wall_goes_back(), test_the_preview_sees_every_shot()

### Community 98 - "cold_read"
Cohesion: 0.22
Nodes (6): cold_read(), recheck_final_scripts(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 99 - "other_ai"
Cohesion: 0.33
Nodes (6): other_ai(), fake_providers(), claude(), reply(), test_every_mode_can_continue_through_two_exhausted_ais(), test_gemini_modes_choose_codex_and_keep_editor_choice()

### Community 100 - "lint_cutout"
Cohesion: 0.17
Nodes (9): missing_parts(), lint_cutout(), assemble(), owner(), test_kit_animals_must_be_used(), test_a_knock_needs_a_closed_door_and_a_messenger_his_letter(), test_hold_counts_as_drawing_the_letter_and_scenery_stays_3d(), test_lint_needs_draw() (+1 more)

### Community 101 - "write_frames"
Cohesion: 0.29
Nodes (3): flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 102 - "log_short"
Cohesion: 0.29
Nodes (3): log_short(), vault_page(), vault_refresh()

### Community 104 - "owner"
Cohesion: 0.17
Nodes (4): owner(), _fake_planning(), test_director_prompt_mentions_full(), test_good_look_check_skips_the_extra_compile()

### Community 105 - "edit_scripts"
Cohesion: 0.15
Nodes (11): edit_scripts(), narration_lines(), saved_session(), test_all_modes_route_writer_editor_and_reader(), ask(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty(), test_only_the_second_edit_pass_gets_the_research(), test_script_rounds_stop_when_fixed_or_after_three() (+3 more)

### Community 106 - "test_weak_opener_graphic_fixes_then_handoff"
Cohesion: 0.20
Nodes (5): fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), test_weak_opener_graphic_fixes_then_handoff(), use()

### Community 107 - "gemini_model"
Cohesion: 0.40
Nodes (4): gemini_model(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_gemini_timeout_switches_to_flash()

### Community 108 - "apply_metadata"
Cohesion: 0.33
Nodes (3): apply_metadata(), clean_tags(), clean_title()

### Community 111 - "re"
Cohesion: 0.11
Nodes (9): commercial_queries(), shot_moments(), shot_span(), import_media(), local_assets(), media_search_words(), mark_details(), max_full() (+1 more)

## Knowledge Gaps
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MediaTests` connect `MediaTests` to `short_render.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12564102564102564 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `render_remotion`, `test_full_scenes.py`, `short_render.py`, `finish_render`, `gpu.py`, `checkpoints.py`, `frame_maker`, `json`, `main`, `local_clips`, `scene_cues`, `clean_photo`, `test_blender_render.py`, `ffmpeg`, `ends_sentence`, `hashlib`, `music_gain`, `audio_library.py`, `captions`, `approve_candidate`, `sfx_events`, `test_pictures_first.py`, `test_style.py`, `write_frames`, `re`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `prepare_topic` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `catalog_pool`, `prepare_topic`, `test_full_scenes.py`, `finish_render`, `test_rules.py`, `footage.py`, `test_topic_ideas.py`, `checkpoints.py`, `json`, `main`, `check_twists`, `fake_ai`, `test_story.py`, `retention.py`, `clean_full`, `ask_ai`, `pathlib`, `style_library`, `test_style.py`, `test_blender_plan.py`, `cold_read`, `limit_style`, `owner`, `edit_scripts`, `re`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._
- **Should `test_full_scenes.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06883116883116883 - nodes in this community are weakly interconnected._