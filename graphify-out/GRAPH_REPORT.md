# Graph Report - ShortsMaker  (2026-11-06)

## Corpus Check
- 153 files · ~200,326 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2516 nodes · 6867 edges · 117 communities (94 shown, 23 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 142 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fa87d94e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- prepare_topic
- test_blender_scene.py
- split_make_shorts.py
- render_remotion
- code_custom_scenes
- pathlib
- guarded.tsx
- k
- test_h3_handoff.py
- drawn_opener.py
- opener_crew.py
- finish_render
- test_rules.py
- Journey.tsx
- toolkit.tsx
- paint_instead
- write_scripts
- gen.py
- .at
- footage.py
- make
- core.mjs
- Pen
- main
- ClipReader
- opener_graphic
- full_cues
- look.py
- parts.py
- OpeningRulesTests
- gather_pool
- templates.py
- ffmpeg
- test_ai_modes.py
- BigNumber.tsx
- main
- Paper
- local_clips
- build_scene.py
- Short.tsx
- textures.mjs
- scene_cues
- test_story.py
- extra_sources.py
- Halftone.tsx
- clean_photo
- test_blender_render.py
- logbook_results
- story_problems
- test_opener3d.py
- test_opener_crew.py
- kit.mjs
- RetentionTests
- json
- render
- ReliabilityTests
- rewrite_paint_prompts
- run_agy
- opener3d.py
- drawn_thumbnail
- ends_sentence
- words_of
- media_command
- captions
- sfx_events
- kit_parts.mjs
- test_first_second.py
- apply_review_fixes
- clean_full
- align_words
- ask_ai
- test_full_scenes.py
- audio_library.py
- Opener3D.tsx
- shutil
- style_library
- person_card
- frame_maker
- lint_custom_code
- graphic_low
- MediaTests
- MetadataTests
- bean.mjs
- PreflightTests
- MarkTests
- StoryPacingTests
- choose_images
- owner
- test_drawn_opener.py
- test_blender_plan.py
- FeedbackTests
- quality_check
- write_frames
- rescue_graphics
- render
- cold_read
- potato_pile.mjs
- lint_cutout
- first_sentence
- limit_style
- full_props
- edit_scripts
- use
- make_sfx
- fake_providers
- umbrellas.mjs
- battery.mjs
- re
- telegraph_sounder.mjs
- telegraph_register.mjs
- telegraph_workbench.mjs
- BlenderFailed
- test_story_sound_library

## God Nodes (most connected - your core abstractions)
1. `k` - 102 edges
2. `render()` - 64 edges
3. `ask_ai()` - 54 edges
4. `write_scripts()` - 54 edges
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
- `test_new_channel_stops_for_review()` --calls--> `pick_channel()`  [EXTRACTED]
  tests/test_rules.py → shortsmaker/channel_profiles.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`
- 3-file cycle: `shortsmaker/motion.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`
- 4-file cycle: `shortsmaker/motion.py -> shortsmaker/opening_rules.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`

## Communities (117 total, 23 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (23): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+15 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (30): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+22 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.13
Nodes (26): catalog_entries(), catalog_pool(), seo_pass(), entry(), fake_ai, pic_short(), pool_of(), test_board_item_pics_cleaned() (+18 more)

### Community 3 - "prepare_topic"
Cohesion: 0.10
Nodes (15): catalog_text(), clean_pics(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures() (+7 more)

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "render_remotion"
Cohesion: 0.05
Nodes (31): short_skin(), ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), invent_component() (+23 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.12
Nodes (16): clean_tsx_code(), code_custom_scenes(), custom_rules(), is_payoff(), look_and_fix(), opener_preflight(), preview_custom(), preview_sheet() (+8 more)

### Community 8 - "pathlib"
Cohesion: 0.07
Nodes (8): hex_rgb(), luminance(), master_gain(), visual_unique(), storyboard(), apply(), preview(), save_state()

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 10 - "k"
Cohesion: 0.10
Nodes (3): makeKit(), k, ellPts()

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.05
Nodes (37): call(), fit_start(), frames(), graph(), main(), saved_file(), h3_problems(), h3_prompt() (+29 more)

### Community 12 - "drawn_opener.py"
Cohesion: 0.09
Nodes (13): align(), main(), studio_speak(), clean_code(), look_dir(), minutes(), opener_role(), staged() (+5 more)

### Community 13 - "opener_crew.py"
Cohesion: 0.13
Nodes (14): animal_cutout(), default_cutout(), kit_hats(), kit_text(), made(), made_note(), make_parts(), paint() (+6 more)

### Community 14 - "finish_render"
Cohesion: 0.13
Nodes (12): clock(), drawn_answer_problem(), overlay_notes(), pacing_check(), review_fixes(), sound_masking(), status_lines(), visual_review() (+4 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (40): load_rules(), min_real_pictures(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft() (+32 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.26
Nodes (20): CustomScene(), ExampleOpenerAction(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear() (+12 more)

### Community 18 - "paint_instead"
Cohesion: 0.25
Nodes (3): gemini_images(), paint_instead(), test_remotion_failure_paints()

### Community 19 - "write_scripts"
Cohesion: 0.11
Nodes (24): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+16 more)

### Community 20 - "gen.py"
Cohesion: 0.22
Nodes (5): images(), main(), t5_encoder(), tts(), video()

### Community 22 - "footage.py"
Cohesion: 0.14
Nodes (10): crop_film_bytes(), crop_filter(), film_frames(), film_piece(), pixabay_films(), shot_moments(), film_ffmpeg(), load() (+2 more)

### Community 23 - "make"
Cohesion: 0.15
Nodes (8): caption_layer(), make(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers(), videos()

### Community 24 - "core.mjs"
Cohesion: 0.08
Nodes (21): burst(), clamp(), eBounce(), eElastic(), eExpo(), eIn(), eIO(), eOut() (+13 more)

### Community 25 - "Pen"
Cohesion: 0.17
Nodes (7): catmull(), centroid(), densify(), INK, noise1(), idHash(), Pen

### Community 26 - "main"
Cohesion: 0.08
Nodes (31): ask_count(), ask_yes(), load_channel(), new_channel(), pick_channel(), save_channel(), use_channel(), begin() (+23 more)

### Community 27 - "ClipReader"
Cohesion: 0.19
Nodes (5): ClipReader, draw_card(), draw_graphic(), frame(), shot()

### Community 28 - "opener_graphic"
Cohesion: 0.13
Nodes (9): full_summary(), opener_graphic(), fix_drawn_answer(), fix_opener_graphic(), paint_opener_start(), weak_opener_graphic(), test_full_props_figure(), test_full_summary() (+1 more)

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
Cohesion: 0.06
Nodes (18): commons_films(), article_images(), commons_search(), get_image(), openverse_images(), ov_get(), thumb_url(), usable_license() (+10 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "ffmpeg"
Cohesion: 0.14
Nodes (10): shot_span(), cosy_instruct(), local_voice(), split_takes(), spoken_count(), duration(), ffmpeg(), is_loop_short() (+2 more)

### Community 36 - "test_ai_modes.py"
Cohesion: 0.21
Nodes (7): configure_brain(), saved_session(), test_all_modes_route_writer_editor_and_reader(), test_batch_uses_selected_codex_writer_and_migrates_saved_aliases(), test_every_mode_can_continue_through_two_exhausted_ais(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_gemini_modes_choose_codex_and_keep_editor_choice()

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
Cohesion: 0.12
Nodes (12): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), motion_prompt(), start_picture(), start_picture_problems() (+4 more)

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

### Community 45 - "test_story.py"
Cohesion: 0.24
Nodes (9): check_twists(), scenes(), test_logbook_hook_line_is_the_whole_first_sentence(), test_rules_accept_opener_setting(), test_sentences_running_across_cuts_are_one_take(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing() (+1 more)

### Community 46 - "extra_sources.py"
Cohesion: 0.08
Nodes (30): brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images(), loc_images() (+22 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "clean_photo"
Cohesion: 0.12
Nodes (8): clean_photo(), is_stereo(), to_vertical(), trim_borders(), border(), plain(), vertical_image(), mark_details()

### Community 49 - "test_blender_render.py"
Cohesion: 0.16
Nodes (16): code_version(), peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws() (+8 more)

### Community 50 - "logbook_results"
Cohesion: 0.33
Nodes (3): entry_age(), logbook_results(), test_logbook_marks_tiny_samples()

### Community 51 - "story_problems"
Cohesion: 0.33
Nodes (7): story_problems(), read(), test_cold_read_verdicts(), test_no_hook_setting_no_hook_check(), test_story_problems(), test_story_problems_flags_summary_hook(), test_story_problems_money_claim()

### Community 52 - "test_opener3d.py"
Cohesion: 0.14
Nodes (14): example(), look(), room(), test_a_cabin_has_its_own_door(), test_a_close_shot_on_people_far_apart_goes_back_to_the_placer(), test_a_walk_goes_from_mark_to_mark(), test_an_arm_past_the_canvas_edge_is_kept(), test_bad_parts_go_back() (+6 more)

### Community 53 - "test_opener_crew.py"
Cohesion: 0.19
Nodes (12): check_staging(), blind_ok(), fake(), short(), staging(), test_a_failed_part_falls_back_to_its_substitute(), test_a_made_part_is_kept_and_reused_with_no_ai(), test_a_painter_with_unusable_code_gets_the_plain_kit_cutout() (+4 more)

### Community 54 - "kit.mjs"
Cohesion: 0.09
Nodes (27): bounds(), EDGE, flat, fx, PAD_TOP, PAD_X, paintAll(), STEPS (+19 more)

### Community 56 - "json"
Cohesion: 0.11
Nodes (19): ask_brain(), ask_number(), normalize_brain(), comfy_call(), moss_graph(), moss_images(), voicestudio_unload(), analyze() (+11 more)

### Community 57 - "render"
Cohesion: 0.13
Nodes (11): ducking_filter(), preview_mix(), music_gain(), short_credit(), graphics_count(), wants_remotion(), drawn_choices(), render() (+3 more)

### Community 59 - "rewrite_paint_prompts"
Cohesion: 0.14
Nodes (7): rewrite_paint_prompts(), plan_gap_paintings(), ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts(), test_scene_without_picture_or_prompt_gets_painted_not_reused()

### Community 60 - "run_agy"
Cohesion: 0.18
Nodes (7): argon_out(), quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "opener3d.py"
Cohesion: 0.10
Nodes (17): box_of(), clean(), dress(), front_door(), half_width(), in_order(), inside(), nudge() (+9 more)

### Community 62 - "drawn_thumbnail"
Cohesion: 0.21
Nodes (9): thumbnail_order(), drawn_thumbnail(), test_thumbnail_order_skips_film_and_puts_openers_first(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 63 - "ends_sentence"
Cohesion: 0.29
Nodes (4): sentence_groups(), ends_sentence(), srt(), test_sentence_ends_include_curly_quotes_and_ellipsis()

### Community 64 - "words_of"
Cohesion: 0.19
Nodes (8): clean_sound(), limit_sounds(), fill_money_graphics(), shows_person(), words_of(), test_clean_sound(), test_fill_money_graphics_and_caps(), test_clean_full_keeps_board_pic()

### Community 65 - "media_command"
Cohesion: 0.22
Nodes (8): freesound_fetch(), freesound_preview(), freesound_results(), audition_audio(), download_audio_choices(), media_command(), review_audio_files(), seed_audio_library()

### Community 66 - "captions"
Cohesion: 0.17
Nodes (6): ass_time(), caption_lines(), caption_size(), captions(), speak(), tts()

### Community 67 - "sfx_events"
Cohesion: 0.25
Nodes (4): schedule_sounds(), sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 69 - "test_first_second.py"
Cohesion: 0.16
Nodes (15): first_second_check(), review_status(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing() (+7 more)

### Community 70 - "apply_review_fixes"
Cohesion: 0.15
Nodes (8): apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_redraw_failure_paints(), test_review_redraws_custom()

### Community 71 - "clean_full"
Cohesion: 0.12
Nodes (16): clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number() (+8 more)

### Community 72 - "align_words"
Cohesion: 0.15
Nodes (10): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), test_caption_word_counts_match_the_scene_splitter(), test_caption_words_keep_what_is_written(), test_dollar_scale_word_order() (+2 more)

### Community 73 - "ask_ai"
Cohesion: 0.12
Nodes (14): ask_ai(), gemini_model(), test_every_ai_gets_the_pipeline_preamble_once(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash() (+6 more)

### Community 74 - "test_full_scenes.py"
Cohesion: 0.07
Nodes (19): channel_url(), seed_ideas(), trend_research(), yt_list(), apply_metadata(), clean_tags(), clean_title(), clash() (+11 more)

### Community 75 - "audio_library.py"
Cohesion: 0.23
Nodes (14): approved_sound(), audio_metadata(), history_read(), import_audio_file(), record_audio(), select_music(), score(), set_audio_metadata() (+6 more)

### Community 76 - "Opener3D.tsx"
Cohesion: 0.07
Nodes (50): aim(), BOOKS, Box(), Building(), Burst(), calculateOpener3D(), CameraRig(), Card() (+42 more)

### Community 77 - "shutil"
Cohesion: 0.09
Nodes (17): available(), available(), approve_candidate(), library_menu(), reject_candidate(), save_candidate(), main(), props_for() (+9 more)

### Community 78 - "style_library"
Cohesion: 0.07
Nodes (21): cut_text(), edit_plan(), look_text(), picture_line(), staging_line(), clean_invention(), clean_look(), clean_transition() (+13 more)

### Community 79 - "person_card"
Cohesion: 0.29
Nodes (4): fit_font(), graphic_overlay(), person_card(), thumbnail()

### Community 80 - "frame_maker"
Cohesion: 0.29
Nodes (3): frame_maker(), credit_tag_image(), fallback_graphic()

### Community 81 - "lint_custom_code"
Cohesion: 0.29
Nodes (5): fallback_custom_tsx(), lint_custom_code(), test_custom_code_cannot_load_code_or_use_network(), test_fallback_custom_is_clean(), test_lint_custom_code()

### Community 85 - "bean.mjs"
Cohesion: 0.35
Nodes (9): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), SKIN (+1 more)

### Community 89 - "choose_images"
Cohesion: 0.17
Nodes (15): choose_images(), apply_look_scenes(), film(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded() (+7 more)

### Community 90 - "owner"
Cohesion: 0.10
Nodes (12): article_text(), fact_check(), owner(), _fake_planning(), test_director_prompt_mentions_full(), test_fact_check_drops_full(), plan_with(), ask() (+4 more)

### Community 91 - "test_drawn_opener.py"
Cohesion: 0.06
Nodes (23): blind_read(), fingerprint(), lint(), make_opener(), review(), sheet_times(), spoils(), drawn_payoff() (+15 more)

### Community 92 - "test_blender_plan.py"
Cohesion: 0.12
Nodes (20): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), plan() (+12 more)

### Community 94 - "quality_check"
Cohesion: 0.33
Nodes (3): quality_check(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 96 - "rescue_graphics"
Cohesion: 0.40
Nodes (3): full_formats(), rescue_graphics(), test_rescue_respects_caps()

### Community 97 - "render"
Cohesion: 0.18
Nodes (6): blends(), render(), sheet(), sheet_times(), test_a_cutout_that_melts_into_the_wall_goes_back(), test_the_preview_sees_every_shot()

### Community 98 - "cold_read"
Cohesion: 0.17
Nodes (7): cold_read_line(), other_ai(), cold_read(), recheck_final_scripts(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 100 - "lint_cutout"
Cohesion: 0.17
Nodes (9): missing_parts(), lint_cutout(), assemble(), owner(), test_kit_animals_must_be_used(), test_a_knock_needs_a_closed_door_and_a_messenger_his_letter(), test_hold_counts_as_drawing_the_letter_and_scenery_stays_3d(), test_lint_needs_draw() (+1 more)

### Community 102 - "first_sentence"
Cohesion: 0.33
Nodes (3): log_short(), first_sentence(), test_first_sentence_reads_across_the_cut()

### Community 104 - "full_props"
Cohesion: 0.29
Nodes (6): full_props(), _board(), _jpg(), test_custom_cues_props_and_pictures(), test_remotion_props_full(), test_sfx_full()

### Community 105 - "edit_scripts"
Cohesion: 0.13
Nodes (9): edit_scripts(), length_plan(), narration_lines(), ask(), test_only_the_second_edit_pass_gets_the_research(), test_script_rounds_stop_when_fixed_or_after_three(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules() (+1 more)

### Community 106 - "use"
Cohesion: 0.33
Nodes (4): fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 108 - "fake_providers"
Cohesion: 0.67
Nodes (4): fake_providers(), claude(), reply(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty()

### Community 111 - "re"
Cohesion: 0.08
Nodes (13): node_run(), commercial_queries(), vault_page(), vault_refresh(), import_media(), local_assets(), media_search_words(), recover_downloads() (+5 more)

### Community 116 - "test_story_sound_library"
Cohesion: 0.67
Nodes (3): test_story_sound_library(), fetch(), _tone_wav()

## Knowledge Gaps
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RetentionTests` connect `RetentionTests` to `pathlib`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12564102564102564 - nodes in this community are weakly interconnected._
- **Why does `ask_ai()` connect `ask_ai` to `test_pictures_first.py`, `render_remotion`, `code_custom_scenes`, `pathlib`, `drawn_opener.py`, `opener_crew.py`, `finish_render`, `write_scripts`, `main`, `opener_graphic`, `test_ai_modes.py`, `local_clips`, `test_story.py`, `clean_photo`, `json`, `rewrite_paint_prompts`, `run_agy`, `test_first_second.py`, `apply_review_fixes`, `test_full_scenes.py`, `choose_images`, `owner`, `test_drawn_opener.py`, `rescue_graphics`, `cold_read`, `edit_scripts`, `fake_providers`, `re`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12941176470588237 - nodes in this community are weakly interconnected._
- **Why does `ReliabilityTests` connect `ReliabilityTests` to `pathlib`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Should `prepare_topic` be split into smaller, more focused modules?**
  _Cohesion score 0.09686609686609686 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._