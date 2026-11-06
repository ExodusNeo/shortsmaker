# Graph Report - ShortsMaker  (2026-11-07)

## Corpus Check
- 157 files · ~205,530 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2570 nodes · 6983 edges · 126 communities (95 shown, 31 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 142 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0f0b9e79`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- contact_sheets
- style_placeholders
- split_make_shorts.py
- render_remotion
- code_custom_scenes
- test_full_scenes.py
- guarded.tsx
- k
- test_h3_handoff.py
- ffmpeg
- opener_crew.py
- visual_review
- test_rules.py
- Journey.tsx
- toolkit.tsx
- ref_react
- write_scripts
- gen.py
- .at
- hashlib
- make
- core.mjs
- Pen
- brand_images
- ClipReader
- opener_graphic
- full_cues
- look.py
- parts.py
- OpeningRulesTests
- gather_pool
- templates.py
- channel_profiles.py
- main
- full/types.ts
- main
- Paper
- extra_sources.py
- build_scene.py
- Short.tsx
- textures.mjs
- scene_cues
- default_build
- fetch
- Halftone.tsx
- trim_borders
- test_blender_render.py
- fake_ai
- writing.py
- frame_maker
- test_opener_crew.py
- kit.mjs
- RetentionTests
- json
- person_card
- ReliabilityTests
- apply_review_fixes
- run_agy
- opener3d.py
- layout
- gemini_model
- .render_fixture
- telegraph_station.mjs
- audio_mix.py
- uprooted_potatoes.mjs
- kit_parts.mjs
- test_first_second.py
- make_paper
- clean_full
- qwen_voice.py
- ask_ai
- test_topic_ideas.py
- audio_library.py
- Opener3D.tsx
- owner
- style_library
- test_blender_scene.py
- graphic_low
- thumbnail_order
- test_drawn_opener.py
- MediaTests
- MetadataTests
- bean.mjs
- PreflightTests
- shutil
- StoryPacingTests
- choose_images
- get_image
- time
- test_blender_plan.py
- FeedbackTests
- quality_check
- invent_component
- short_skin
- render
- MarkTests
- potato_pile.mjs
- lint_cutout
- finish_render
- limit_style
- render
- edit_scripts
- test_weak_opener_graphic_fixes_then_handoff
- drawn_thumbnail
- saved_session
- umbrellas.mjs
- battery.mjs
- re
- telegraph_sounder.mjs
- telegraph_register.mjs
- telegraph_workbench.mjs
- cold_read
- clamp
- ov_get
- ending
- panels
- full_props
- test_short_credit
- write_frames
- lint_custom_code
- bitten_potato.mjs
- potato_mouthful.mjs

## God Nodes (most connected - your core abstractions)
1. `k` - 102 edges
2. `render()` - 64 edges
3. `ask_ai()` - 54 edges
4. `write_scripts()` - 54 edges
5. `makeKit()` - 37 edges
6. `clean()` - 36 edges
7. `clamp()` - 35 edges
8. `MediaTests` - 35 edges
9. `main()` - 32 edges
10. `skinOf()` - 31 edges

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

## Communities (126 total, 31 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.16
Nodes (31): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+23 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.15
Nodes (23): catalog_entries(), catalog_pool(), clean_pics(), save_pool(), entry(), film(), pic_short(), pool_of() (+15 more)

### Community 3 - "contact_sheets"
Cohesion: 0.12
Nodes (8): catalog_text(), contact_sheets(), is_usable(), pictures_of(), pool_folder(), preflight_pictures(), usable(), direct_scripts()

### Community 4 - "style_placeholders"
Cohesion: 0.21
Nodes (9): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_placeholders_match_the_slots(), test_slots_restored_after_render() (+1 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "render_remotion"
Cohesion: 0.16
Nodes (9): render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain() (+1 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.13
Nodes (14): clean_tsx_code(), code_custom_scenes(), custom_rules(), is_payoff(), look_and_fix(), opener_preflight(), preview_custom(), preview_sheet() (+6 more)

### Community 8 - "test_full_scenes.py"
Cohesion: 0.09
Nodes (5): hex_rgb(), luminance(), crop_film_bytes(), clean_photo(), visual_unique()

### Community 9 - "guarded.tsx"
Cohesion: 0.13
Nodes (18): Box, boxAt(), clamp, Connect(), fitCard(), hits(), layoutColumn(), layoutGrid() (+10 more)

### Community 10 - "k"
Cohesion: 0.10
Nodes (3): makeKit(), k, ellPts()

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.05
Nodes (37): call(), fit_start(), frames(), graph(), main(), saved_file(), h3_problems(), h3_prompt() (+29 more)

### Community 12 - "ffmpeg"
Cohesion: 0.07
Nodes (21): shot_span(), cosy_instruct(), cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice() (+13 more)

### Community 13 - "opener_crew.py"
Cohesion: 0.09
Nodes (19): staging_line(), made3d(), animal_cutout(), crew(), default_cutout(), kit_hats(), kit_text(), lint_part() (+11 more)

### Community 14 - "visual_review"
Cohesion: 0.11
Nodes (12): log_short(), clock(), overlay_notes(), pacing_check(), review_fixes(), sound_masking(), visual_review(), test_review_is_told_the_drawings_are_deliberate() (+4 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (40): load_rules(), min_real_pictures(), parse_rules(), require_rules(), capture_prompts(), ask(), draft_reply(), make() (+32 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.21
Nodes (21): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+13 more)

### Community 18 - "ref_react"
Cohesion: 0.39
Nodes (3): clamp, CustomFull, FullProps

### Community 19 - "write_scripts"
Cohesion: 0.11
Nodes (26): prepare_topic(), limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai() (+18 more)

### Community 20 - "gen.py"
Cohesion: 0.22
Nodes (5): images(), main(), t5_encoder(), tts(), video()

### Community 22 - "hashlib"
Cohesion: 0.16
Nodes (8): crop_filter(), film_frames(), film_piece(), shot_moments(), film_ffmpeg(), load(), save(), signature()

### Community 23 - "make"
Cohesion: 0.15
Nodes (8): caption_layer(), make(), master_gain(), project_xml(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers(), videos()

### Community 24 - "core.mjs"
Cohesion: 0.08
Nodes (21): burst(), clamp(), eBounce(), eElastic(), eExpo(), eIn(), eIO(), eOut() (+13 more)

### Community 25 - "Pen"
Cohesion: 0.17
Nodes (7): catmull(), centroid(), densify(), INK, noise1(), idHash(), Pen

### Community 26 - "brand_images"
Cohesion: 0.19
Nodes (8): brand_films(), brand_images(), brand_page(), BrandImages, settings(), source_enabled(), source_status(), print_source_status()

### Community 27 - "ClipReader"
Cohesion: 0.18
Nodes (5): ClipReader, draw_card(), draw_graphic(), frame(), shot()

### Community 28 - "opener_graphic"
Cohesion: 0.14
Nodes (10): full_summary(), full_formats(), opener_graphic(), rescue_graphics(), fix_drawn_answer(), fix_opener_graphic(), article_text(), test_full_props_figure() (+2 more)

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
Cohesion: 0.14
Nodes (7): balanced_candidates(), gather_pool(), load_pool(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits(), test_pool_roundtrip()

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "channel_profiles.py"
Cohesion: 0.10
Nodes (10): channel_url(), new_channel(), save_channel(), seed_ideas(), trend_research(), yt_list(), apply_metadata(), clean_tags() (+2 more)

### Community 36 - "main"
Cohesion: 0.07
Nodes (37): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), load_channel(), normalize_brain(), use_channel() (+29 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (22): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+14 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "extra_sources.py"
Cohesion: 0.37
Nodes (9): candidate(), collection_images(), europeana_images(), loc_images(), pixabay_images(), smithsonian_images(), source_json(), wellcome_images() (+1 more)

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.11
Nodes (22): Captions(), PersonCard(), SubscribeCta(), calculateOpener3D(), StageProps, Root(), Background(), flashAlpha() (+14 more)

### Community 43 - "textures.mjs"
Cohesion: 0.19
Nodes (20): ellipse(), fibre(), fill(), grainCanvas(), grainOver(), hash(), hatch(), rng() (+12 more)

### Community 44 - "scene_cues"
Cohesion: 0.18
Nodes (9): scene_cues(), read_need(), callout_hold(), drop_unreadable_kinetic(), test_counter_finishes_before_it_leaves(), test_short_scene_callout_is_placed_so_the_check_passes(), test_graphic_card_hold_duration(), test_person_card_hold_and_exit_gap() (+1 more)

### Community 45 - "default_build"
Cohesion: 0.29
Nodes (4): default_build(), plan_builds(), test_plan_builds_retries_then_defaults(), ask()

### Community 46 - "fetch"
Cohesion: 0.12
Nodes (14): archive_ad_films(), archive_films(), duke_films(), nasa_films(), pixabay_films(), archive_images(), nasa_credit(), nasa_images() (+6 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "trim_borders"
Cohesion: 0.20
Nodes (5): is_stereo(), trim_borders(), border(), plain(), vertical_image()

### Community 49 - "test_blender_render.py"
Cohesion: 0.13
Nodes (17): BlenderFailed, code_version(), peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short() (+9 more)

### Community 50 - "fake_ai"
Cohesion: 0.15
Nodes (9): entry_age(), logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel() (+1 more)

### Community 51 - "writing.py"
Cohesion: 0.09
Nodes (19): sentence_groups(), ends_sentence(), first_sentence(), check_twists(), recheck_final_scripts(), story_problems(), test_sentence_ends_include_curly_quotes_and_ellipsis(), read() (+11 more)

### Community 52 - "frame_maker"
Cohesion: 0.29
Nodes (3): frame_maker(), credit_tag_image(), fallback_graphic()

### Community 53 - "test_opener_crew.py"
Cohesion: 0.11
Nodes (21): spread_out(), assemble(), check_staging(), blind_ok(), fake(), short(), staging(), test_a_failed_part_falls_back_to_its_substitute() (+13 more)

### Community 54 - "kit.mjs"
Cohesion: 0.09
Nodes (27): bounds(), EDGE, flat, fx, PAD_TOP, PAD_X, paintAll(), STEPS (+19 more)

### Community 56 - "json"
Cohesion: 0.17
Nodes (13): comfy_call(), voicestudio_unload(), analyze(), edit_metrics(), load_metrics(), metrics_text(), normalize_metrics(), normalize_reply() (+5 more)

### Community 57 - "person_card"
Cohesion: 0.33
Nodes (3): fit_font(), graphic_overlay(), person_card()

### Community 59 - "apply_review_fixes"
Cohesion: 0.08
Nodes (14): apply_review_fixes(), paint_new(), pool_pictures(), rewrite_paint_prompts(), plan_gap_paintings(), ask(), _review_state(), test_auto_fix_graphic() (+6 more)

### Community 60 - "run_agy"
Cohesion: 0.18
Nodes (7): argon_out(), quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "opener3d.py"
Cohesion: 0.07
Nodes (33): box_of(), clean(), clean_shapes(), dress(), front_door(), half_width(), held_of(), in_order() (+25 more)

### Community 62 - "layout"
Cohesion: 0.22
Nodes (6): word_time(), foot_of(), layout(), place_animal(), put(), lum()

### Community 63 - "gemini_model"
Cohesion: 0.40
Nodes (4): gemini_model(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_gemini_timeout_switches_to_flash()

### Community 66 - "audio_mix.py"
Cohesion: 0.14
Nodes (8): ass_time(), caption_lines(), caption_size(), captions(), music_gain(), speak(), tts(), test_music_gain_evens_out_tracks()

### Community 69 - "test_first_second.py"
Cohesion: 0.16
Nodes (15): first_second_check(), review_status(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing() (+7 more)

### Community 70 - "make_paper"
Cohesion: 0.50
Nodes (3): make_paper(), main(), test_make_paper()

### Community 71 - "clean_full"
Cohesion: 0.08
Nodes (24): clean_sound(), limit_sounds(), clean_full(), word(), clean_graphic(), contains(), coords(), is_num() (+16 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.13
Nodes (13): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+5 more)

### Community 73 - "ask_ai"
Cohesion: 0.14
Nodes (10): ask_ai(), test_every_ai_gets_the_pipeline_preamble_once(), test_quota_fallback_both_ways(), test_claude_pinned_to_opus_high(), test_encoder_cache_lives_with_video_encoder(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash(), test_independent_review_falls_back_without_changing_solo_mode(), test_session_shared() (+2 more)

### Community 74 - "test_topic_ideas.py"
Cohesion: 0.15
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 75 - "audio_library.py"
Cohesion: 0.07
Nodes (35): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+27 more)

### Community 76 - "Opener3D.tsx"
Cohesion: 0.07
Nodes (50): aim(), Assembly(), BOOKS, Box(), Building(), Burst(), CameraRig(), Card() (+42 more)

### Community 77 - "owner"
Cohesion: 0.10
Nodes (12): fact_check(), owner(), _fake_planning(), test_director_prompt_mentions_full(), test_fact_check_drops_full(), plan_with(), ask(), test_director_character_look_is_kept_short_or_dropped() (+4 more)

### Community 78 - "style_library"
Cohesion: 0.07
Nodes (21): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), clean_invention(), clean_look(), clean_transition() (+13 more)

### Community 79 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 80 - "graphic_low"
Cohesion: 0.40
Nodes (3): fills_frame(), graphic_low(), thumbnail()

### Community 82 - "test_drawn_opener.py"
Cohesion: 0.13
Nodes (12): blind_ok(), fake_ai(), look(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused(), test_drawn_opener_stops_when_a_fix_does_not_help(), test_neither_passes_so_the_best_draft_at_keep_is_used() (+4 more)

### Community 85 - "bean.mjs"
Cohesion: 0.35
Nodes (9): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), SKIN (+1 more)

### Community 87 - "shutil"
Cohesion: 0.09
Nodes (15): approve_candidate(), library_menu(), reject_candidate(), save_candidate(), main(), props_for(), candidate_in(), library_snapshot() (+7 more)

### Community 89 - "choose_images"
Cohesion: 0.15
Nodes (16): choose_images(), download_picture(), recover_downloads(), apply_look_scenes(), picking, planned_short(), scene(), still() (+8 more)

### Community 90 - "get_image"
Cohesion: 0.14
Nodes (8): commons_films(), article_images(), commons_search(), get_image(), thumb_url(), usable_license(), wm_files(), wm_get()

### Community 91 - "time"
Cohesion: 0.08
Nodes (19): available(), blind_read(), clean_code(), fingerprint(), look_dir(), make_opener(), minutes(), node_run() (+11 more)

### Community 92 - "test_blender_plan.py"
Cohesion: 0.27
Nodes (13): clean_build(), pick(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults(), test_clean_build_keeps_a_good_plan(), test_default_build_shape(), test_label_is_short_and_upper() (+5 more)

### Community 94 - "quality_check"
Cohesion: 0.33
Nodes (3): quality_check(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 95 - "invent_component"
Cohesion: 0.15
Nodes (8): clean_style_code(), invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), style_rules(), test_invention_lint_failure_uses_fallback()

### Community 97 - "render"
Cohesion: 0.17
Nodes (7): blends(), part_sheet(), render(), sheet(), sheet_times(), test_a_cutout_that_melts_into_the_wall_goes_back(), test_the_preview_sees_every_shot()

### Community 100 - "lint_cutout"
Cohesion: 0.18
Nodes (8): lint(), missing_parts(), lint_cutout(), test_kit_animals_must_be_used(), test_lint(), test_a_knock_needs_a_closed_door_and_a_messenger_his_letter(), test_hold_counts_as_drawing_the_letter_and_scenery_stays_3d(), test_lint_needs_draw()

### Community 102 - "finish_render"
Cohesion: 0.13
Nodes (11): remove(), drawn_answer_problem(), status_lines(), storyboard(), apply(), preview(), drawn_payoff(), finish_render() (+3 more)

### Community 104 - "render"
Cohesion: 0.06
Nodes (17): gemini_images(), moss_graph(), moss_images(), short_credit(), graphics_count(), to_vertical(), ink_silhouette(), paint_instead() (+9 more)

### Community 105 - "edit_scripts"
Cohesion: 0.13
Nodes (10): edit_scripts(), length_plan(), narration_lines(), test_all_modes_route_writer_editor_and_reader(), ask(), test_only_the_second_edit_pass_gets_the_research(), test_script_rounds_stop_when_fixed_or_after_three(), test_solo_edit_scripts_uses_same_ai() (+2 more)

### Community 106 - "test_weak_opener_graphic_fixes_then_handoff"
Cohesion: 0.14
Nodes (7): weak_opener_graphic(), use_opener(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), test_weak_opener_graphic_fixes_then_handoff(), use()

### Community 107 - "drawn_thumbnail"
Cohesion: 0.31
Nodes (7): drawn_thumbnail(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so(), test_thumbnail_uses_the_real_photo()

### Community 108 - "saved_session"
Cohesion: 0.47
Nodes (6): fake_providers(), claude(), reply(), saved_session(), test_every_mode_can_continue_through_two_exhausted_ais(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty()

### Community 111 - "re"
Cohesion: 0.07
Nodes (13): pick_channel(), commercial_queries(), vault_page(), vault_refresh(), import_media(), local_assets(), media_search_words(), fill_money_graphics() (+5 more)

### Community 115 - "cold_read"
Cohesion: 0.29
Nodes (5): other_ai(), cold_read(), test_gemini_modes_choose_codex_and_keep_editor_choice(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers()

### Community 120 - "full_props"
Cohesion: 0.40
Nodes (4): full_props(), _jpg(), test_custom_cues_props_and_pictures(), test_remotion_props_full()

### Community 122 - "write_frames"
Cohesion: 0.29
Nodes (3): flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 123 - "lint_custom_code"
Cohesion: 0.29
Nodes (5): fallback_custom_tsx(), lint_custom_code(), test_custom_code_cannot_load_code_or_use_network(), test_fallback_custom_is_clean(), test_lint_custom_code()

## Knowledge Gaps
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RetentionTests` connect `RetentionTests` to `test_full_scenes.py`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12912912912912913 - nodes in this community are weakly interconnected._
- **Why does `FeedbackTests` connect `FeedbackTests` to `channel_profiles.py`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14919354838709678 - nodes in this community are weakly interconnected._
- **Why does `ReliabilityTests` connect `ReliabilityTests` to `test_full_scenes.py`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Should `contact_sheets` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._