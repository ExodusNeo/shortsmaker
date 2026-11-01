# Graph Report - ShortsMaker  (2026-11-01)

## Corpus Check
- 134 files · ~153,932 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2072 nodes · 5750 edges · 118 communities (94 shown, 24 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 128 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f01d7d35`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- catalog_pool
- article_text
- test_blender_scene.py
- split_make_shorts.py
- json
- code_custom_scenes
- film_piece
- guarded.tsx
- k
- test_h3_handoff.py
- gather_pool
- clean_look
- render_remotion
- test_rules.py
- Journey.tsx
- toolkit.tsx
- prepare_topic
- write_scripts
- Local GPU Worker
- core.mjs
- local_clips
- make
- makeKit
- test_blender_plan.py
- render
- frame_render.py
- full_cues
- time
- look.py
- parts.py
- make_opener
- templates.py
- use_opener
- test_story.py
- full/types.ts
- main
- Paper
- quality_check
- build_scene.py
- Short.tsx
- textures.mjs
- sfx_events
- fake_ai
- extra_sources.py
- Halftone.tsx
- test_topic_ideas.py
- style_placeholders
- limit_style
- main
- is_stereo
- test_first_second.py
- kit.mjs
- RetentionTests
- subprocess
- test_pictures_first.py
- ReliabilityTests
- apply_review_fixes
- run_agy
- bean.mjs
- write_json
- popS
- re
- edit_scripts
- visual_review
- dexter.mjs
- kit_parts.mjs
- rewrite_paint_prompts
- full_props
- clean_full
- qwen_voice.py
- ask_ai
- test_style.py
- media_command
- test_short_credit
- captions
- ref_remotion
- edit_plan
- resume_runs
- cold_read_line
- test_every_mode_can_continue_through_two_exhausted_ais
- MediaTests
- check_twists
- opener_graphic
- prune_cache
- MarkTests
- finish_render
- apply_look_scenes
- retention.py
- test_review_redraws_custom
- test_blender_render.py
- drawn_opener.py
- invent_component
- ClipReader
- clean_photo
- style_library
- words_of
- approve_candidate
- redraw_custom
- clean_sound
- default_build
- write_frames
- freesound_results
- scene_cues
- gemini_model
- first_second_check
- rescue_graphics
- clean_graphic
- BlenderFailed
- thumbnail_order
- peaks
- _run
- short_skin
- limit_full
- ending
- panels

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 60 edges
3. `write_scripts()` - 51 edges
4. `ask_ai()` - 47 edges
5. `main()` - 32 edges
6. `skinOf()` - 29 edges
7. `clamp()` - 27 edges
8. `ellPts()` - 26 edges
9. `Paper()` - 25 edges
10. `choose_images()` - 25 edges

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

## Communities (118 total, 24 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "catalog_pool"
Cohesion: 0.15
Nodes (18): catalog_entries(), catalog_pool(), clean_pics(), entry(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film() (+10 more)

### Community 3 - "article_text"
Cohesion: 0.17
Nodes (8): article_text(), fact_check(), test_fact_check_drops_full(), plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "json"
Cohesion: 0.09
Nodes (16): code_version(), channel_url(), new_channel(), pick_channel(), save_channel(), trend_research(), yt_list(), pixabay_films() (+8 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.18
Nodes (8): clean_tsx_code(), code_custom_scenes(), custom_rules(), look_and_fix(), preview_custom(), preview_sheet(), test_code_custom_scenes_fallback(), test_fake_reaches_callers()

### Community 8 - "film_piece"
Cohesion: 0.20
Nodes (6): crop_film_bytes(), crop_filter(), film_frames(), film_piece(), shot_moments(), film_ffmpeg()

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "gather_pool"
Cohesion: 0.10
Nodes (9): balanced_candidates(), gather_pool(), owner(), _fake_planning(), test_director_prompt_mentions_full(), film(), stubbed, test_gather_pool_shape() (+1 more)

### Community 13 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 14 - "render_remotion"
Cohesion: 0.12
Nodes (11): ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), test_ink_silhouette() (+3 more)

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (37): load_rules(), min_real_pictures(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft() (+29 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 18 - "prepare_topic"
Cohesion: 0.10
Nodes (16): catalog_text(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures(), prepare_topic() (+8 more)

### Community 19 - "write_scripts"
Cohesion: 0.13
Nodes (22): write_scripts(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare() (+14 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "local_clips"
Cohesion: 0.10
Nodes (13): cosy_instruct(), cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt() (+5 more)

### Community 23 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.27
Nodes (13): clean_build(), pick(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults(), test_clean_build_keeps_a_good_plan(), test_default_build_shape(), test_label_is_short_and_upper() (+5 more)

### Community 26 - "render"
Cohesion: 0.07
Nodes (13): make_sfx(), short_credit(), graphics_count(), to_vertical(), is_loop_short(), paint_instead(), wants_remotion(), srt() (+5 more)

### Community 27 - "frame_render.py"
Cohesion: 0.13
Nodes (8): fills_frame(), fit_font(), frame_maker(), graphic_overlay(), person_card(), thumbnail(), credit_tag_image(), fallback_graphic()

### Community 28 - "full_cues"
Cohesion: 0.17
Nodes (7): full_cues(), spoken_at(), spoken_span(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish(), test_opener_graphic()

### Community 29 - "time"
Cohesion: 0.16
Nodes (7): call(), fit_start(), frames(), graph(), main(), saved_file(), voicestudio_up()

### Community 30 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 32 - "make_opener"
Cohesion: 0.11
Nodes (11): make_opener(), review(), sheet_times(), write(), fake_ai(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused() (+3 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "use_opener"
Cohesion: 0.25
Nodes (5): use_opener(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 36 - "test_story.py"
Cohesion: 0.13
Nodes (15): sentence_groups(), log_short(), first_sentence(), story_problems(), read(), scenes(), test_cold_read_verdicts(), test_first_sentence_reads_across_the_cut() (+7 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "quality_check"
Cohesion: 0.25
Nodes (4): quality_check(), length_plan(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

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

### Community 45 - "fake_ai"
Cohesion: 0.19
Nodes (8): logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel(), test_seo_never_sees_competitor_titles()

### Community 46 - "extra_sources.py"
Cohesion: 0.05
Nodes (39): ducking_filter(), brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images() (+31 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "test_topic_ideas.py"
Cohesion: 0.15
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 49 - "style_placeholders"
Cohesion: 0.19
Nodes (10): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_placeholders_match_the_slots() (+2 more)

### Community 51 - "main"
Cohesion: 0.12
Nodes (17): ask_brain(), ask_count(), ask_yes(), configure_brain(), load_channel(), normalize_brain(), use_channel(), fix_short() (+9 more)

### Community 53 - "test_first_second.py"
Cohesion: 0.23
Nodes (11): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once(), test_opener_must_be_a_later_real_picture() (+3 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "subprocess"
Cohesion: 0.07
Nodes (4): tsc_check(), storyboard(), main(), props_for()

### Community 57 - "test_pictures_first.py"
Cohesion: 0.19
Nodes (15): choose_images(), download_picture(), recover_downloads(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded() (+7 more)

### Community 59 - "apply_review_fixes"
Cohesion: 0.18
Nodes (7): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "write_json"
Cohesion: 0.15
Nodes (10): shot_span(), split_takes(), spoken_count(), duration(), ffmpeg(), write_json(), apply(), preview() (+2 more)

### Community 64 - "re"
Cohesion: 0.08
Nodes (12): music_gain(), commercial_queries(), vault_page(), vault_refresh(), import_media(), local_assets(), media_search_words(), parse_scene_money() (+4 more)

### Community 65 - "edit_scripts"
Cohesion: 0.13
Nodes (11): other_ai(), cold_read(), edit_scripts(), narration_lines(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_gemini_modes_choose_codex_and_keep_editor_choice(), test_solo_edit_scripts_uses_same_ai(), test_cold_read_handles_malformed_reply() (+3 more)

### Community 66 - "visual_review"
Cohesion: 0.24
Nodes (7): clock(), overlay_notes(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 69 - "rewrite_paint_prompts"
Cohesion: 0.18
Nodes (5): rewrite_paint_prompts(), ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 70 - "full_props"
Cohesion: 0.20
Nodes (8): full_props(), full_pictures(), _board(), _jpg(), test_board_pictures_attached(), test_custom_cues_props_and_pictures(), test_remotion_props_full(), test_sfx_full()

### Community 71 - "clean_full"
Cohesion: 0.15
Nodes (10): clean_full(), number_figures(), show_number(), test_clean_full_board(), test_clean_full_document(), test_clean_full_journey(), test_clean_full_keeps_thing(), test_clean_full_limits() (+2 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.13
Nodes (13): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+5 more)

### Community 73 - "ask_ai"
Cohesion: 0.14
Nodes (10): seed_ideas(), ask_ai(), test_quota_fallback_both_ways(), test_claude_pinned_to_opus_high(), test_encoder_cache_lives_with_video_encoder(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash(), test_independent_review_falls_back_without_changing_solo_mode(), test_session_shared() (+2 more)

### Community 74 - "test_style.py"
Cohesion: 0.10
Nodes (10): ask_number(), hex_rgb(), luminance(), library_menu(), reject_candidate(), save_candidate(), candidate_in(), test_candidate_names_unique_across_kinds() (+2 more)

### Community 75 - "media_command"
Cohesion: 0.15
Nodes (21): approved_sound(), audio_metadata(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music(), score() (+13 more)

### Community 77 - "captions"
Cohesion: 0.16
Nodes (7): ass_time(), caption_lines(), captions(), styled(), speak(), tts(), ass_colour()

### Community 79 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 80 - "resume_runs"
Cohesion: 0.28
Nodes (11): begin(), context(), pack(), pending(), read(), save_context(), unpack(), update() (+3 more)

### Community 82 - "test_every_mode_can_continue_through_two_exhausted_ais"
Cohesion: 0.32
Nodes (7): fake_providers(), claude(), reply(), saved_session(), test_all_modes_route_writer_editor_and_reader(), test_every_mode_can_continue_through_two_exhausted_ais(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty()

### Community 84 - "check_twists"
Cohesion: 0.47
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 85 - "opener_graphic"
Cohesion: 0.12
Nodes (9): gemini_images(), full_summary(), opener_graphic(), fix_opener_graphic(), paint_opener_start(), weak_opener_graphic(), test_full_props_figure(), test_full_summary() (+1 more)

### Community 88 - "finish_render"
Cohesion: 0.17
Nodes (12): status_lines(), drawn_thumbnail(), finish_render(), load_state(), save_state(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back() (+4 more)

### Community 90 - "retention.py"
Cohesion: 0.21
Nodes (7): clamp(), analyze(), command(), normalize_reply(), report_text(), scenes_from_plan(), seconds()

### Community 91 - "test_review_redraws_custom"
Cohesion: 0.40
Nodes (3): _review_state(), test_redraw_failure_paints(), test_review_redraws_custom()

### Community 92 - "test_blender_render.py"
Cohesion: 0.28
Nodes (11): render_clips(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises(), test_frames_are_trimmed_after_the_clips_are_cut(), test_missing_blender_raises() (+3 more)

### Community 93 - "drawn_opener.py"
Cohesion: 0.14
Nodes (7): available(), clean_code(), fingerprint(), lint(), node_run(), look(), test_lint()

### Community 94 - "invent_component"
Cohesion: 0.16
Nodes (8): invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), swap_inventions(), test_invention_lint_failure_uses_fallback(), test_swap_inventions()

### Community 95 - "ClipReader"
Cohesion: 0.19
Nodes (5): ClipReader, draw_card(), draw_graphic(), frame(), shot()

### Community 96 - "clean_photo"
Cohesion: 0.20
Nodes (6): clean_photo(), trim_borders(), border(), plain(), visual_unique(), mark_details()

### Community 97 - "style_library"
Cohesion: 0.20
Nodes (8): style_library(), style_rules(), write_style_index(), build(), add(), main(), test_library_entries_have_fields(), test_write_style_index_is_deterministic()

### Community 98 - "words_of"
Cohesion: 0.27
Nodes (6): graphic_low(), fill_money_graphics(), is_person_portrait(), words_of(), test_fill_money_graphics_and_caps(), test_clean_full_keeps_board_pic()

### Community 99 - "approve_candidate"
Cohesion: 0.33
Nodes (6): approve_candidate(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes()

### Community 100 - "redraw_custom"
Cohesion: 0.25
Nodes (5): fallback_custom_tsx(), lint_custom_code(), redraw_custom(), test_fallback_custom_is_clean(), test_lint_custom_code()

### Community 101 - "clean_sound"
Cohesion: 0.29
Nodes (5): clean_sound(), limit_sounds(), word(), contains(), test_clean_sound()

### Community 102 - "default_build"
Cohesion: 0.29
Nodes (4): default_build(), plan_builds(), test_plan_builds_retries_then_defaults(), ask()

### Community 103 - "write_frames"
Cohesion: 0.29
Nodes (3): flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 104 - "freesound_results"
Cohesion: 0.33
Nodes (3): freesound_fetch(), freesound_preview(), freesound_results()

### Community 105 - "scene_cues"
Cohesion: 0.33
Nodes (5): scene_cues(), test_counter_finishes_before_it_leaves(), test_graphic_card_hold_duration(), test_person_card_hold_and_exit_gap(), test_scene_hold_padding()

### Community 106 - "gemini_model"
Cohesion: 0.40
Nodes (4): gemini_model(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_gemini_timeout_switches_to_flash()

### Community 107 - "first_second_check"
Cohesion: 0.33
Nodes (4): first_second_check(), review_status(), test_failed_preview_clears_previous_opener_score(), test_opener_prompt_shows_each_scenes_line_and_picture()

### Community 108 - "rescue_graphics"
Cohesion: 0.40
Nodes (3): full_formats(), rescue_graphics(), test_rescue_respects_caps()

### Community 109 - "clean_graphic"
Cohesion: 0.50
Nodes (4): clean_graphic(), coords(), is_num(), test_clean_question_and_kinetic()

## Knowledge Gaps
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MediaTests` connect `MediaTests` to `test_full_scenes.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `catalog_pool`, `article_text`, `json`, `gather_pool`, `clean_look`, `test_rules.py`, `prepare_topic`, `test_story.py`, `quality_check`, `fake_ai`, `test_topic_ideas.py`, `limit_style`, `main`, `re`, `edit_scripts`, `clean_full`, `ask_ai`, `test_style.py`, `check_twists`, `words_of`, `clean_sound`, `default_build`, `clean_graphic`, `limit_full`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `json`, `build_scene.py`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.0907258064516129 - nodes in this community are weakly interconnected._
- **Should `guarded.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.09986504723346828 - nodes in this community are weakly interconnected._