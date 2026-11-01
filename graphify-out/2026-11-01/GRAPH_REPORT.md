# Graph Report - ShortsMaker  (2026-11-01)

## Corpus Check
- 136 files · ~156,413 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2112 nodes · 5857 edges · 96 communities (84 shown, 12 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 134 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9c9d7062`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- prepare_topic
- test_blender_scene.py
- split_make_shorts.py
- on_topic
- code_custom_scenes
- json
- guarded.tsx
- k
- test_h3_handoff.py
- test_story.py
- test_style.py
- render_remotion
- test_rules.py
- Journey.tsx
- toolkit.tsx
- apply_review_fixes
- planning
- Local GPU Worker
- core.mjs
- gpu.py
- edit_project.py
- makeKit
- test_blender_plan.py
- paint_instead
- frame_maker
- rewrite_paint_prompts
- h3_run.py
- look.py
- parts.py
- OpeningRulesTests
- fetch
- templates.py
- test_weak_opener_graphic_fixes_then_handoff
- story_problems
- full/types.ts
- main
- Paper
- wm_files
- build_scene.py
- Short.tsx
- textures.mjs
- sfx_events
- re
- extra_sources.py
- Halftone.tsx
- clean_photo
- invent_component
- fake_ai
- main
- style_placeholders
- film_piece
- kit.mjs
- RetentionTests
- shutil
- trend_research
- ReliabilityTests
- gather_pool
- run_agy
- bean.mjs
- speak
- popS
- pathlib
- edit_scripts
- finish_render
- dexter.mjs
- kit_parts.mjs
- test_first_second.py
- audio_mix.py
- test_full_scenes.py
- qwen_voice.py
- ask_ai
- audio_library.py
- build
- captions
- ref_remotion
- edit_plan
- scene_cues
- gemini_model
- test_every_mode_can_continue_through_two_exhausted_ais
- MediaTests
- opener_graphic
- MarkTests
- drawn_thumbnail
- choose_images
- test_blender_render.py
- trim_borders
- fills_frame
- style_library
- blender_plan.py
- media_menu.py
- BlenderFailed
- render

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 61 edges
3. `write_scripts()` - 51 edges
4. `ask_ai()` - 47 edges
5. `MediaTests` - 33 edges
6. `main()` - 32 edges
7. `skinOf()` - 29 edges
8. `clamp()` - 27 edges
9. `ellPts()` - 26 edges
10. `choose_images()` - 26 edges

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

## Communities (96 total, 12 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.15
Nodes (22): catalog_entries(), catalog_pool(), clean_pics(), entry(), film(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+14 more)

### Community 3 - "prepare_topic"
Cohesion: 0.13
Nodes (13): catalog_text(), contact_sheets(), is_usable(), load_pool(), pool_folder(), preflight_pictures(), prepare_topic(), save_pool() (+5 more)

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "on_topic"
Cohesion: 0.14
Nodes (9): archive_ad_films(), archive_films(), duke_films(), nasa_films(), archive_images(), nasa_images(), nasa_search(), on_topic() (+1 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.13
Nodes (12): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+4 more)

### Community 8 - "json"
Cohesion: 0.11
Nodes (14): code_version(), pixabay_films(), shot_moments(), comfy_call(), moss_graph(), moss_images(), import_media(), write_json() (+6 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.12
Nodes (27): unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated(), test_flagged_start_picture_is_not_sent(), test_handoff_picks_up_clips_zip() (+19 more)

### Community 12 - "test_story.py"
Cohesion: 0.11
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 13 - "test_style.py"
Cohesion: 0.05
Nodes (26): pictures_of(), clean_invention(), clean_look(), clean_transition(), limit_style(), settle_style(), wants_remotion(), reject_candidate() (+18 more)

### Community 14 - "render_remotion"
Cohesion: 0.13
Nodes (11): make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_make_paper() (+3 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (39): load_rules(), min_real_pictures(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft() (+31 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 18 - "apply_review_fixes"
Cohesion: 0.18
Nodes (7): apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_redraw_failure_paints(), test_review_redraws_custom()

### Community 19 - "planning"
Cohesion: 0.14
Nodes (18): passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), reply() (+10 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "gpu.py"
Cohesion: 0.06
Nodes (24): cosy_instruct(), cover_crop(), cut_owner_clip(), h3_problems(), h3_prompt(), h3_prompts(), local_clips(), local_job() (+16 more)

### Community 23 - "edit_project.py"
Cohesion: 0.13
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.25
Nodes (14): clean_build(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults(), test_clean_build_keeps_a_good_plan(), test_default_build_shape(), test_label_is_short_and_upper(), test_nan_and_infinity_get_defaults() (+6 more)

### Community 26 - "paint_instead"
Cohesion: 0.12
Nodes (6): gemini_images(), to_vertical(), ink_silhouette(), paint_instead(), test_ink_silhouette(), test_remotion_failure_paints()

### Community 27 - "frame_maker"
Cohesion: 0.08
Nodes (12): ClipReader, draw_card(), draw_graphic(), flash_alpha(), frame_maker(), frame(), graphic_overlay(), shot() (+4 more)

### Community 28 - "rewrite_paint_prompts"
Cohesion: 0.14
Nodes (7): rewrite_paint_prompts(), _fake_planning(), ask(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 29 - "h3_run.py"
Cohesion: 0.18
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 30 - "look.py"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (23): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+15 more)

### Community 32 - "OpeningRulesTests"
Cohesion: 0.06
Nodes (16): fingerprint(), make_opener(), node_run(), review(), sheet_times(), write(), fake_ai(), look() (+8 more)

### Community 33 - "fetch"
Cohesion: 0.22
Nodes (6): get_image(), openverse_images(), ov_get(), wm_get(), fetch(), search_suggestions()

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "test_weak_opener_graphic_fixes_then_handoff"
Cohesion: 0.17
Nodes (6): weak_opener_graphic(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), test_weak_opener_graphic_fixes_then_handoff(), use()

### Community 36 - "story_problems"
Cohesion: 0.24
Nodes (9): first_sentence(), story_problems(), read(), test_cold_read_verdicts(), test_first_sentence_reads_across_the_cut(), test_no_hook_setting_no_hook_check(), test_story_problems(), test_story_problems_flags_summary_hook() (+1 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "wm_files"
Cohesion: 0.18
Nodes (6): commons_films(), article_images(), commons_search(), thumb_url(), usable_license(), wm_files()

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "textures.mjs"
Cohesion: 0.25
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "sfx_events"
Cohesion: 0.25
Nodes (4): schedule_sounds(), sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 45 - "re"
Cohesion: 0.07
Nodes (22): clean_code(), lint(), logbook_results(), vault_page(), vault_refresh(), max_full(), max_full_planned(), clean_style_code() (+14 more)

### Community 46 - "extra_sources.py"
Cohesion: 0.14
Nodes (18): brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images(), loc_images() (+10 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "clean_photo"
Cohesion: 0.18
Nodes (4): clean_photo(), is_stereo(), visual_unique(), mark_details()

### Community 49 - "invent_component"
Cohesion: 0.16
Nodes (8): invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), style_rules(), test_invention_lint_failure_uses_fallback(), test_placeholders_match_the_slots()

### Community 50 - "fake_ai"
Cohesion: 0.24
Nodes (6): seo_pass(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel(), test_seo_never_sees_competitor_titles()

### Community 51 - "main"
Cohesion: 0.06
Nodes (40): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), load_channel(), new_channel(), normalize_brain() (+32 more)

### Community 52 - "style_placeholders"
Cohesion: 0.23
Nodes (8): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_slots_restored_after_render(), with_fakes()

### Community 53 - "film_piece"
Cohesion: 0.22
Nodes (5): crop_film_bytes(), crop_filter(), film_frames(), film_piece(), film_ffmpeg()

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "shutil"
Cohesion: 0.16
Nodes (8): available(), analyze(), normalize_reply(), report_text(), scenes_from_plan(), seconds(), main(), props_for()

### Community 57 - "trend_research"
Cohesion: 0.40
Nodes (3): channel_url(), trend_research(), yt_list()

### Community 59 - "gather_pool"
Cohesion: 0.14
Nodes (6): commercial_queries(), balanced_candidates(), gather_pool(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 64 - "pathlib"
Cohesion: 0.12
Nodes (6): hex_rgb(), luminance(), short_skin(), tsc_check(), drawn_choices(), test_drawn_choices_have_no_pictures()

### Community 65 - "edit_scripts"
Cohesion: 0.15
Nodes (10): other_ai(), cold_read(), edit_scripts(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_gemini_modes_choose_codex_and_keep_editor_choice(), test_solo_edit_scripts_uses_same_ai(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers() (+2 more)

### Community 66 - "finish_render"
Cohesion: 0.10
Nodes (15): clock(), drawn_answer_problem(), overlay_notes(), quality_check(), review_fixes(), review_status(), status_lines(), storyboard() (+7 more)

### Community 69 - "test_first_second.py"
Cohesion: 0.16
Nodes (15): first_second_check(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples() (+7 more)

### Community 70 - "audio_mix.py"
Cohesion: 0.29
Nodes (3): clean_sound(), limit_sounds(), test_clean_sound()

### Community 71 - "test_full_scenes.py"
Cohesion: 0.05
Nodes (42): graphic_low(), full_props(), full_pictures(), clean_full(), word(), clean_graphic(), contains(), coords() (+34 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.14
Nodes (13): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+5 more)

### Community 73 - "ask_ai"
Cohesion: 0.13
Nodes (11): seed_ideas(), ask_ai(), test_quota_fallback_both_ways(), test_claude_pinned_to_opus_high(), test_encoder_cache_lives_with_video_encoder(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash(), test_independent_review_falls_back_without_changing_solo_mode(), test_session_shared() (+3 more)

### Community 75 - "audio_library.py"
Cohesion: 0.23
Nodes (15): approved_sound(), audio_metadata(), history_read(), import_audio_file(), record_audio(), select_music(), score(), set_audio_metadata() (+7 more)

### Community 76 - "build"
Cohesion: 0.67
Nodes (3): build(), add(), main()

### Community 77 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 79 - "edit_plan"
Cohesion: 0.14
Nodes (7): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 80 - "scene_cues"
Cohesion: 0.33
Nodes (5): scene_cues(), test_counter_finishes_before_it_leaves(), test_graphic_card_hold_duration(), test_person_card_hold_and_exit_gap(), test_scene_hold_padding()

### Community 81 - "gemini_model"
Cohesion: 0.40
Nodes (4): gemini_model(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_gemini_timeout_switches_to_flash()

### Community 82 - "test_every_mode_can_continue_through_two_exhausted_ais"
Cohesion: 0.32
Nodes (7): fake_providers(), claude(), reply(), saved_session(), test_all_modes_route_writer_editor_and_reader(), test_every_mode_can_continue_through_two_exhausted_ais(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty()

### Community 85 - "opener_graphic"
Cohesion: 0.12
Nodes (12): full_summary(), opening_brief(), full_formats(), opener_graphic(), rescue_graphics(), redraw_custom(), fix_drawn_answer(), fix_opener_graphic() (+4 more)

### Community 88 - "drawn_thumbnail"
Cohesion: 0.23
Nodes (9): scene_frames(), drawn_thumbnail(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 89 - "choose_images"
Cohesion: 0.12
Nodes (18): choose_images(), download_picture(), recover_downloads(), apply_look_scenes(), owner(), picking, planned_short(), scene() (+10 more)

### Community 92 - "test_blender_render.py"
Cohesion: 0.22
Nodes (12): peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises(), test_frames_are_trimmed_after_the_clips_are_cut() (+4 more)

### Community 96 - "trim_borders"
Cohesion: 0.33
Nodes (4): trim_borders(), border(), plain(), vertical_image()

### Community 98 - "fills_frame"
Cohesion: 0.25
Nodes (4): fills_frame(), fit_font(), person_card(), thumbnail()

### Community 99 - "style_library"
Cohesion: 0.17
Nodes (12): approve_candidate(), style_library(), write_style_index(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure() (+4 more)

### Community 102 - "blender_plan.py"
Cohesion: 0.12
Nodes (8): clamp(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order(), test_thumbnail_order_skips_film_and_puts_openers_first()

### Community 104 - "media_menu.py"
Cohesion: 0.21
Nodes (9): freesound_fetch(), freesound_preview(), freesound_results(), audition_audio(), download_audio_choices(), media_command(), print_source_status(), review_audio_files() (+1 more)

### Community 114 - "render"
Cohesion: 0.06
Nodes (22): radians(), ducking_filter(), preview_mix(), track_start(), make_sfx(), music_gain(), shot_span(), short_credit() (+14 more)

## Knowledge Gaps
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MediaTests` connect `MediaTests` to `pathlib`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `test_style.py` to `edit_scripts`, `test_pictures_first.py`, `prepare_topic`, `story_problems`, `audio_mix.py`, `blender_plan.py`, `json`, `ask_ai`, `__init__.py`, `test_full_scenes.py`, `test_story.py`, `re`, `test_rules.py`, `main`, `planning`, `shutil`, `trend_research`, `rewrite_paint_prompts`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1471264367816092 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `json`, `test_style.py`, `render_remotion`, `gpu.py`, `paint_instead`, `frame_maker`, `sfx_events`, `clean_photo`, `main`, `shutil`, `speak`, `pathlib`, `finish_render`, `test_full_scenes.py`, `audio_library.py`, `captions`, `scene_cues`, `opener_graphic`, `drawn_thumbnail`, `choose_images`, `test_blender_render.py`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Should `prepare_topic` be split into smaller, more focused modules?**
  _Cohesion score 0.12554112554112554 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._