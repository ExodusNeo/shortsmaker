# Graph Report - ShortsMaker  (2026-11-06)

## Corpus Check
- 157 files · ~202,462 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2540 nodes · 6907 edges · 132 communities (104 shown, 28 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 142 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fc7ab3e5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- catalog_pool
- prepare_topic
- style_placeholders
- split_make_shorts.py
- render_remotion
- code_custom_scenes
- guarded.tsx
- k
- test_h3_handoff.py
- local_clips
- opener_crew.py
- visual_review
- test_rules.py
- Journey.tsx
- toolkit.tsx
- pick_channel
- write_scripts
- gen.py
- .at
- footage.py
- make
- core.mjs
- Pen
- write_json
- frame_maker
- opener_graphic
- full_cues
- look.py
- parts.py
- OpeningRulesTests
- gather_pool
- templates.py
- config.py
- main
- BigNumber.tsx
- main
- Paper
- json
- build_scene.py
- Short.tsx
- textures.mjs
- scene_cues
- check_twists
- extra_sources.py
- Halftone.tsx
- test_full_scenes.py
- test_blender_render.py
- fake_ai
- test_story.py
- capture_prompts
- test_opener_crew.py
- kit.mjs
- RetentionTests
- retention.py
- ReliabilityTests
- rewrite_paint_prompts
- run_agy
- opener3d.py
- layout
- ends_sentence
- .render_fixture
- telegraph_station.mjs
- music_gain
- uprooted_potatoes.mjs
- kit_parts.mjs
- test_first_second.py
- apply_review_fixes
- clean_full
- qwen_voice.py
- ask_ai
- test_topic_ideas.py
- audio_library.py
- Opener3D.tsx
- test_style.py
- style_library
- test_blender_scene.py
- words_of
- re
- short
- MediaTests
- MetadataTests
- bean.mjs
- PreflightTests
- approve_candidate
- StoryPacingTests
- test_pictures_first.py
- wm_files
- drawn_opener.py
- test_blender_plan.py
- FeedbackTests
- quality_check
- invent_component
- ffmpeg
- render
- edit_plan
- potato_pile.mjs
- lint_cutout
- finish_render
- limit_style
- render
- edit_scripts
- use_opener
- drawn_thumbnail
- test_ai_modes.py
- umbrellas.mjs
- battery.mjs
- shutil
- telegraph_sounder.mjs
- telegraph_register.mjs
- telegraph_workbench.mjs
- cold_read
- download_audio_choices
- get_image
- log_short
- sfx_events
- full_props
- paint_instead
- write_frames
- lint_custom_code
- apply_metadata
- story_sound
- rescue_graphics
- bitten_potato.mjs
- potato_mouthful.mjs
- unpack
- blind_ok

## God Nodes (most connected - your core abstractions)
1. `k` - 102 edges
2. `render()` - 64 edges
3. `write_scripts()` - 54 edges
4. `ask_ai()` - 53 edges
5. `makeKit()` - 37 edges
6. `clamp()` - 35 edges
7. `MediaTests` - 35 edges
8. `main()` - 32 edges
9. `skinOf()` - 31 edges
10. `clean()` - 31 edges

## Surprising Connections (you probably didn't know these)
- `test_numbers()` --calls--> `say_number()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_word_counts_match_the_scene_splitter()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_words_keep_what_is_written()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_every_aligned_word_is_in_the_aligner_alphabet()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_solo_brain_selection_options()` --calls--> `ask_brain()`  [EXTRACTED]
  tests/test_package.py → shortsmaker/channel_profiles.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`
- 3-file cycle: `shortsmaker/motion.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`
- 4-file cycle: `shortsmaker/motion.py -> shortsmaker/opening_rules.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`

## Communities (132 total, 28 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (23): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+15 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (30): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+22 more)

### Community 2 - "catalog_pool"
Cohesion: 0.14
Nodes (21): catalog_entries(), catalog_pool(), clean_pics(), save_pool(), entry(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+13 more)

### Community 3 - "prepare_topic"
Cohesion: 0.12
Nodes (12): catalog_text(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures(), prepare_topic(), usable() (+4 more)

### Community 4 - "style_placeholders"
Cohesion: 0.21
Nodes (9): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_slots_restored_after_render() (+1 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "render_remotion"
Cohesion: 0.10
Nodes (13): ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions() (+5 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.13
Nodes (15): clean_tsx_code(), code_custom_scenes(), custom_rules(), is_payoff(), look_and_fix(), opener_preflight(), preview_custom(), preview_sheet() (+7 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 10 - "k"
Cohesion: 0.10
Nodes (3): makeKit(), k, ellPts()

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "local_clips"
Cohesion: 0.10
Nodes (14): cosy_instruct(), cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt() (+6 more)

### Community 13 - "opener_crew.py"
Cohesion: 0.10
Nodes (20): clean_code(), minutes(), staging_line(), animal_cutout(), crew(), default_cutout(), kit_hats(), kit_text() (+12 more)

### Community 14 - "visual_review"
Cohesion: 0.18
Nodes (8): clock(), overlay_notes(), review_fixes(), sound_masking(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 15 - "test_rules.py"
Cohesion: 0.13
Nodes (31): parse_rules(), draft_reply(), make(), run_draft(), stop_text(), StopPicker, test_bad_min_pictures_stops(), test_blender_needs_a_build_plan_section() (+23 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.26
Nodes (20): CustomScene(), ExampleOpenerAction(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear() (+12 more)

### Community 18 - "pick_channel"
Cohesion: 0.17
Nodes (7): new_channel(), pick_channel(), save_channel(), use_channel(), draft_rules(), require_rules(), test_new_channel_stops_for_review()

### Community 19 - "write_scripts"
Cohesion: 0.12
Nodes (23): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+15 more)

### Community 20 - "gen.py"
Cohesion: 0.22
Nodes (5): images(), main(), t5_encoder(), tts(), video()

### Community 22 - "footage.py"
Cohesion: 0.21
Nodes (6): crop_film_bytes(), crop_filter(), film_frames(), film_piece(), shot_moments(), film_ffmpeg()

### Community 23 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "core.mjs"
Cohesion: 0.08
Nodes (21): burst(), clamp(), eBounce(), eElastic(), eExpo(), eIn(), eIO(), eOut() (+13 more)

### Community 25 - "Pen"
Cohesion: 0.17
Nodes (7): catmull(), centroid(), densify(), INK, noise1(), idHash(), Pen

### Community 26 - "write_json"
Cohesion: 0.24
Nodes (12): begin(), context(), pack(), pending(), pending_topics(), read(), save_context(), update() (+4 more)

### Community 27 - "frame_maker"
Cohesion: 0.08
Nodes (12): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), frame_maker(), frame(), graphic_overlay() (+4 more)

### Community 28 - "opener_graphic"
Cohesion: 0.12
Nodes (9): gemini_images(), full_summary(), opener_graphic(), fix_drawn_answer(), fix_opener_graphic(), paint_opener_start(), test_full_props_figure(), test_full_summary() (+1 more)

### Community 29 - "full_cues"
Cohesion: 0.17
Nodes (7): full_cues(), spoken_at(), spoken_span(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish(), test_opener_graphic()

### Community 30 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 33 - "gather_pool"
Cohesion: 0.10
Nodes (9): balanced_candidates(), gather_pool(), owner(), _fake_planning(), test_director_prompt_mentions_full(), film(), stubbed, test_gather_pool_shape() (+1 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "config.py"
Cohesion: 0.10
Nodes (10): channel_url(), seed_ideas(), trend_research(), yt_list(), hex_rgb(), luminance(), short_skin(), library_menu() (+2 more)

### Community 36 - "main"
Cohesion: 0.13
Nodes (15): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), load_channel(), normalize_brain(), fix_short() (+7 more)

### Community 37 - "BigNumber.tsx"
Cohesion: 0.22
Nodes (13): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+5 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.12
Nodes (29): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+21 more)

### Community 40 - "json"
Cohesion: 0.07
Nodes (17): call(), fit_start(), frames(), graph(), main(), saved_file(), code_version(), pixabay_films() (+9 more)

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (17): Captions(), PersonCard(), Background(), Card, flashAlpha(), GraphicFor(), Move, Scene (+9 more)

### Community 43 - "textures.mjs"
Cohesion: 0.19
Nodes (20): ellipse(), fibre(), fill(), grainCanvas(), grainOver(), hash(), hatch(), rng() (+12 more)

### Community 44 - "scene_cues"
Cohesion: 0.18
Nodes (9): scene_cues(), read_need(), callout_hold(), drop_unreadable_kinetic(), test_counter_finishes_before_it_leaves(), test_short_scene_callout_is_placed_so_the_check_passes(), test_graphic_card_hold_duration(), test_person_card_hold_and_exit_gap() (+1 more)

### Community 45 - "check_twists"
Cohesion: 0.47
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 46 - "extra_sources.py"
Cohesion: 0.08
Nodes (27): brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images(), loc_images() (+19 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "test_full_scenes.py"
Cohesion: 0.08
Nodes (9): person_card(), clean_photo(), is_stereo(), vertical_image(), contact_sheets(), visual_unique(), mark_details(), test_short_credit() (+1 more)

### Community 49 - "test_blender_render.py"
Cohesion: 0.15
Nodes (16): BlenderFailed, peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws() (+8 more)

### Community 50 - "fake_ai"
Cohesion: 0.24
Nodes (7): seo_pass(), fake_ai, test_catalog_empty_pool_no_ai(), test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel(), test_seo_never_sees_competitor_titles()

### Community 51 - "test_story.py"
Cohesion: 0.22
Nodes (10): first_sentence(), story_problems(), read(), test_cold_read_verdicts(), test_first_sentence_reads_across_the_cut(), test_no_hook_setting_no_hook_check(), test_rules_accept_opener_setting(), test_story_problems() (+2 more)

### Community 52 - "capture_prompts"
Cohesion: 0.20
Nodes (6): load_rules(), min_real_pictures(), capture_prompts(), ask(), test_load_rules_sets_session(), test_strange_history_prompts_unchanged()

### Community 53 - "test_opener_crew.py"
Cohesion: 0.12
Nodes (18): spread_out(), assemble(), check_staging(), blind_ok(), fake(), short(), staging(), test_a_failed_part_falls_back_to_its_substitute() (+10 more)

### Community 54 - "kit.mjs"
Cohesion: 0.09
Nodes (27): bounds(), EDGE, flat, fx, PAD_TOP, PAD_X, paintAll(), STEPS (+19 more)

### Community 56 - "retention.py"
Cohesion: 0.23
Nodes (9): analyze(), edit_metrics(), load_metrics(), metrics_text(), normalize_metrics(), normalize_reply(), parse_metric(), report_text() (+1 more)

### Community 59 - "rewrite_paint_prompts"
Cohesion: 0.14
Nodes (7): rewrite_paint_prompts(), plan_gap_paintings(), ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts(), test_scene_without_picture_or_prompt_gets_painted_not_reused()

### Community 60 - "run_agy"
Cohesion: 0.18
Nodes (7): argon_out(), quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "opener3d.py"
Cohesion: 0.08
Nodes (29): box_of(), clean(), dress(), front_door(), half_width(), in_order(), inside(), nudge() (+21 more)

### Community 62 - "layout"
Cohesion: 0.29
Nodes (5): word_time(), layout(), place_thing(), put(), lum()

### Community 63 - "ends_sentence"
Cohesion: 0.29
Nodes (4): sentence_groups(), ends_sentence(), srt(), test_sentence_ends_include_curly_quotes_and_ellipsis()

### Community 66 - "music_gain"
Cohesion: 0.12
Nodes (8): ass_time(), caption_lines(), caption_size(), captions(), music_gain(), speak(), tts(), test_music_gain_evens_out_tracks()

### Community 69 - "test_first_second.py"
Cohesion: 0.18
Nodes (14): first_second_check(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture() (+6 more)

### Community 70 - "apply_review_fixes"
Cohesion: 0.13
Nodes (10): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full() (+2 more)

### Community 71 - "clean_full"
Cohesion: 0.13
Nodes (15): clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number() (+7 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.11
Nodes (15): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+7 more)

### Community 73 - "ask_ai"
Cohesion: 0.12
Nodes (14): ask_ai(), gemini_model(), test_every_ai_gets_the_pipeline_preamble_once(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash() (+6 more)

### Community 74 - "test_topic_ideas.py"
Cohesion: 0.15
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 75 - "audio_library.py"
Cohesion: 0.23
Nodes (17): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+9 more)

### Community 76 - "Opener3D.tsx"
Cohesion: 0.07
Nodes (50): aim(), BOOKS, Box(), Building(), Burst(), calculateOpener3D(), CameraRig(), Card() (+42 more)

### Community 77 - "test_style.py"
Cohesion: 0.14
Nodes (11): wants_remotion(), apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_clean_question_and_kinetic(), test_director_character_look_is_kept_short_or_dropped(), test_director_inventions_are_kept_with_a_spec() (+3 more)

### Community 78 - "style_library"
Cohesion: 0.13
Nodes (12): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), test_invented_look_needs_fallback() (+4 more)

### Community 79 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 80 - "words_of"
Cohesion: 0.12
Nodes (13): clean_sound(), limit_sounds(), graphic_low(), trim_borders(), border(), plain(), fill_money_graphics(), is_person_portrait() (+5 more)

### Community 81 - "re"
Cohesion: 0.12
Nodes (11): archive_ad_films(), archive_films(), duke_films(), entry_age(), logbook_results(), parse_scene_money(), observations(), scenes_from_plan() (+3 more)

### Community 82 - "short"
Cohesion: 0.14
Nodes (10): fake_ai(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused(), test_drawn_opener_stops_when_a_fix_does_not_help(), test_neither_passes_so_the_best_draft_at_keep_is_used(), test_no_verdict_is_not_a_pass(), test_reveal_scene_is_drawn_with_its_own_rules() (+2 more)

### Community 85 - "bean.mjs"
Cohesion: 0.35
Nodes (9): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), SKIN (+1 more)

### Community 87 - "approve_candidate"
Cohesion: 0.18
Nodes (11): approve_candidate(), save_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes() (+3 more)

### Community 89 - "test_pictures_first.py"
Cohesion: 0.19
Nodes (15): choose_images(), download_picture(), recover_downloads(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded() (+7 more)

### Community 90 - "wm_files"
Cohesion: 0.12
Nodes (10): commons_films(), article_images(), commons_search(), thumb_url(), usable_license(), wm_files(), wm_get(), article_text() (+2 more)

### Community 91 - "drawn_opener.py"
Cohesion: 0.09
Nodes (16): available(), blind_read(), fingerprint(), lint(), look_dir(), make_opener(), node_run(), opener_role() (+8 more)

### Community 92 - "test_blender_plan.py"
Cohesion: 0.12
Nodes (20): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), plan() (+12 more)

### Community 94 - "quality_check"
Cohesion: 0.33
Nodes (3): quality_check(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 95 - "invent_component"
Cohesion: 0.16
Nodes (8): clean_style_code(), invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), test_invention_lint_failure_uses_fallback(), test_placeholders_match_the_slots()

### Community 96 - "ffmpeg"
Cohesion: 0.19
Nodes (7): shot_span(), split_takes(), duration(), ffmpeg(), is_loop_short(), drawn_payoff(), test_a_take_is_cut_between_the_scenes_words()

### Community 97 - "render"
Cohesion: 0.18
Nodes (6): blends(), render(), sheet(), sheet_times(), test_a_cutout_that_melts_into_the_wall_goes_back(), test_the_preview_sees_every_shot()

### Community 98 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 100 - "lint_cutout"
Cohesion: 0.25
Nodes (6): missing_parts(), lint_cutout(), test_kit_animals_must_be_used(), test_a_knock_needs_a_closed_door_and_a_messenger_his_letter(), test_hold_counts_as_drawing_the_letter_and_scenery_stays_3d(), test_lint_needs_draw()

### Community 102 - "finish_render"
Cohesion: 0.19
Nodes (8): drawn_answer_problem(), pacing_check(), status_lines(), weak_opener_graphic(), finish_render(), load_state(), save_state(), test_state_roundtrip_full_pics()

### Community 104 - "render"
Cohesion: 0.17
Nodes (6): make_sfx(), short_credit(), graphics_count(), drawn_choices(), render(), test_drawn_choices_have_no_pictures()

### Community 105 - "edit_scripts"
Cohesion: 0.20
Nodes (6): edit_scripts(), length_plan(), narration_lines(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules(), test_failed_second_read_clears_old_verdict()

### Community 106 - "use_opener"
Cohesion: 0.25
Nodes (5): use_opener(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 107 - "drawn_thumbnail"
Cohesion: 0.21
Nodes (9): thumbnail_order(), drawn_thumbnail(), test_thumbnail_order_skips_film_and_puts_openers_first(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 108 - "test_ai_modes.py"
Cohesion: 0.16
Nodes (13): other_ai(), fake_providers(), claude(), reply(), saved_session(), test_all_modes_route_writer_editor_and_reader(), ask(), test_batch_uses_selected_codex_writer_and_migrates_saved_aliases() (+5 more)

### Community 111 - "shutil"
Cohesion: 0.08
Nodes (13): vault_page(), vault_refresh(), import_media(), local_assets(), media_search_words(), prune_cache(), review_status(), storyboard() (+5 more)

### Community 115 - "cold_read"
Cohesion: 0.18
Nodes (7): cold_read_line(), cold_read(), recheck_final_scripts(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 116 - "download_audio_choices"
Cohesion: 0.25
Nodes (5): freesound_fetch(), freesound_preview(), freesound_results(), download_audio_choices(), seed_audio_library()

### Community 117 - "get_image"
Cohesion: 0.22
Nodes (5): get_image(), openverse_images(), ov_get(), full_pictures(), test_board_pictures_attached()

### Community 118 - "log_short"
Cohesion: 0.22
Nodes (7): log_short(), build(), add(), main(), scenes(), test_logbook_hook_line_is_the_whole_first_sentence(), test_sentences_running_across_cuts_are_one_take()

### Community 119 - "sfx_events"
Cohesion: 0.25
Nodes (4): schedule_sounds(), sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 120 - "full_props"
Cohesion: 0.29
Nodes (6): full_props(), _board(), _jpg(), test_custom_cues_props_and_pictures(), test_remotion_props_full(), test_sfx_full()

### Community 121 - "paint_instead"
Cohesion: 0.25
Nodes (3): to_vertical(), paint_instead(), test_remotion_failure_paints()

### Community 122 - "write_frames"
Cohesion: 0.29
Nodes (3): flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 123 - "lint_custom_code"
Cohesion: 0.29
Nodes (5): fallback_custom_tsx(), lint_custom_code(), test_custom_code_cannot_load_code_or_use_network(), test_fallback_custom_is_clean(), test_lint_custom_code()

### Community 124 - "apply_metadata"
Cohesion: 0.33
Nodes (3): apply_metadata(), clean_tags(), clean_title()

### Community 125 - "story_sound"
Cohesion: 0.40
Nodes (4): story_sound(), test_story_sound_library(), fetch(), _tone_wav()

### Community 126 - "rescue_graphics"
Cohesion: 0.40
Nodes (3): full_formats(), rescue_graphics(), test_rescue_respects_caps()

## Knowledge Gaps
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ReliabilityTests` connect `ReliabilityTests` to `pathlib`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12564102564102564 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `render_remotion`, `pathlib`, `local_clips`, `visual_review`, `write_json`, `frame_maker`, `opener_graphic`, `config.py`, `main`, `json`, `scene_cues`, `test_full_scenes.py`, `test_blender_render.py`, `rewrite_paint_prompts`, `ends_sentence`, `music_gain`, `audio_library.py`, `test_style.py`, `words_of`, `approve_candidate`, `test_pictures_first.py`, `ffmpeg`, `finish_render`, `use_opener`, `shutil`, `sfx_events`, `paint_instead`, `write_frames`, `story_sound`, `rescue_graphics`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Should `catalog_pool` be split into smaller, more focused modules?**
  _Cohesion score 0.13756613756613756 - nodes in this community are weakly interconnected._
- **Why does `RetentionTests` connect `RetentionTests` to `pathlib`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Should `prepare_topic` be split into smaller, more focused modules?**
  _Cohesion score 0.11904761904761904 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._