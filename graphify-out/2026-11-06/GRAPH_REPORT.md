# Graph Report - ShortsMaker  (2026-11-05)

## Corpus Check
- 144 files · ~177,978 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2340 nodes · 6456 edges · 111 communities (92 shown, 19 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 140 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c99de969`
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
- re
- guarded.tsx
- k
- test_h3_handoff.py
- make_opener
- h3_run.py
- finish_render
- test_rules.py
- Journey.tsx
- toolkit.tsx
- json
- write_scripts
- gen.py
- clamp
- source_json
- make
- makeKit
- test_topic_ideas.py
- local_clips
- frame_maker
- opener_graphic
- full_cues
- look.py
- parts.py
- OpeningRulesTests
- owner
- templates.py
- paint_opener_start
- main
- BigNumber.tsx
- main
- Paper
- ask
- build_scene.py
- Short.tsx
- core.mjs
- scene_cues
- check_twists
- fetch
- Halftone.tsx
- clean_photo
- .at
- fake_ai
- test_story.py
- wm_files
- words_of
- kit.mjs
- RetentionTests
- retention.py
- render
- ReliabilityTests
- style_library
- run_agy
- test_opener3d.py
- write_json
- ends_sentence
- rewrite_paint_prompts
- download_audio_choices
- logbook.py
- dexter.mjs
- kit_parts.mjs
- test_first_second.py
- apply_review_fixes
- clean_full
- time
- ask_ai
- test_full_scenes.py
- audio_library.py
- Opener3D.tsx
- music_gain
- preview
- first_sentence
- quality_check
- test_style.py
- full_props
- MediaTests
- MetadataTests
- paint_instead
- PreflightTests
- MarkTests
- StoryPacingTests
- choose_images
- fact_check
- short
- test_blender_plan.py
- FeedbackTests
- gather_pool
- review
- test_story_sound_library
- plan
- cold_read
- other_ai
- write
- duration
- rescue_graphics
- limit_style
- edit_scripts
- sfx_events
- write_frames
- test_short_credit
- lint
- apply_metadata

## God Nodes (most connected - your core abstractions)
1. `k` - 98 edges
2. `render()` - 64 edges
3. `write_scripts()` - 54 edges
4. `ask_ai()` - 50 edges
5. `clamp()` - 35 edges
6. `MediaTests` - 35 edges
7. `main()` - 32 edges
8. `skinOf()` - 31 edges
9. `ellPts()` - 30 edges
10. `makeKit()` - 29 edges

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

## Communities (111 total, 19 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (23): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+15 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (30): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+22 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.14
Nodes (24): catalog_entries(), catalog_pool(), clean_pics(), save_pool(), entry(), film(), pic_short(), pool_of() (+16 more)

### Community 3 - "prepare_topic"
Cohesion: 0.11
Nodes (13): catalog_text(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures(), prepare_topic() (+5 more)

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "render_remotion"
Cohesion: 0.05
Nodes (32): short_skin(), ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), invent_component() (+24 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.10
Nodes (19): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), is_payoff(), lint_custom_code(), look_and_fix(), opener_preflight() (+11 more)

### Community 8 - "re"
Cohesion: 0.07
Nodes (11): hex_rgb(), luminance(), node_run(), import_media(), local_assets(), media_search_words(), word_time(), parse_scene_money() (+3 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "make_opener"
Cohesion: 0.18
Nodes (6): available(), make_opener(), missing_parts(), sheet_times(), available(), test_kit_animals_must_be_used()

### Community 13 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 14 - "finish_render"
Cohesion: 0.11
Nodes (13): clock(), drawn_answer_problem(), overlay_notes(), pacing_check(), review_fixes(), sound_masking(), status_lines(), visual_review() (+5 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (40): load_rules(), min_real_pictures(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft() (+32 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.26
Nodes (20): CustomScene(), ExampleOpenerAction(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear() (+12 more)

### Community 18 - "json"
Cohesion: 0.09
Nodes (17): channel_url(), new_channel(), pick_channel(), save_channel(), trend_research(), yt_list(), fingerprint(), pixabay_films() (+9 more)

### Community 19 - "write_scripts"
Cohesion: 0.12
Nodes (23): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+15 more)

### Community 20 - "gen.py"
Cohesion: 0.22
Nodes (5): images(), main(), t5_encoder(), tts(), video()

### Community 21 - "clamp"
Cohesion: 0.09
Nodes (9): clamp(), eElastic(), eIn(), eIO(), eOut(), ik(), lerp(), lerpColor() (+1 more)

### Community 22 - "source_json"
Cohesion: 0.16
Nodes (15): brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images(), loc_images() (+7 more)

### Community 23 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.20
Nodes (8): makeKit(), catmull(), centroid(), densify(), INK, noise1(), idHash(), Pen

### Community 25 - "test_topic_ideas.py"
Cohesion: 0.15
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 26 - "local_clips"
Cohesion: 0.12
Nodes (12): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), motion_prompt(), start_picture(), start_picture_problems() (+4 more)

### Community 27 - "frame_maker"
Cohesion: 0.08
Nodes (14): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), frame_maker(), frame(), graphic_low() (+6 more)

### Community 28 - "opener_graphic"
Cohesion: 0.25
Nodes (6): full_summary(), opener_graphic(), fix_drawn_answer(), fix_opener_graphic(), test_full_props_figure(), test_full_summary()

### Community 29 - "full_cues"
Cohesion: 0.17
Nodes (7): full_cues(), spoken_at(), spoken_span(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish(), test_opener_graphic()

### Community 30 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 33 - "owner"
Cohesion: 0.14
Nodes (6): owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "paint_opener_start"
Cohesion: 0.13
Nodes (7): gemini_images(), paint_opener_start(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), test_weak_opener_graphic_fixes_then_handoff(), use()

### Community 36 - "main"
Cohesion: 0.08
Nodes (31): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), load_channel(), normalize_brain(), use_channel() (+23 more)

### Community 37 - "BigNumber.tsx"
Cohesion: 0.22
Nodes (13): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+5 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.12
Nodes (29): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+21 more)

### Community 40 - "ask"
Cohesion: 0.18
Nodes (6): ask(), _review_state(), test_look_check_fixes_code(), test_redraw_failure_paints(), test_review_redraws_custom(), test_review_uses_unused_pool_pictures_before_painting()

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (17): Captions(), PersonCard(), Background(), Card, flashAlpha(), GraphicFor(), Move, Scene (+9 more)

### Community 43 - "core.mjs"
Cohesion: 0.13
Nodes (30): burst(), eBounce(), eExpo(), ellipse(), fibre(), fill(), _grain, grainCanvas() (+22 more)

### Community 44 - "scene_cues"
Cohesion: 0.18
Nodes (9): scene_cues(), read_need(), callout_hold(), drop_unreadable_kinetic(), test_counter_finishes_before_it_leaves(), test_short_scene_callout_is_placed_so_the_check_passes(), test_graphic_card_hold_duration(), test_person_card_hold_and_exit_gap() (+1 more)

### Community 45 - "check_twists"
Cohesion: 0.47
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 46 - "fetch"
Cohesion: 0.12
Nodes (13): archive_ad_films(), archive_films(), duke_films(), nasa_films(), archive_images(), nasa_credit(), nasa_images(), nasa_search() (+5 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "clean_photo"
Cohesion: 0.14
Nodes (7): clean_photo(), is_stereo(), trim_borders(), border(), plain(), vertical_image(), mark_details()

### Community 50 - "fake_ai"
Cohesion: 0.15
Nodes (9): entry_age(), logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel() (+1 more)

### Community 51 - "test_story.py"
Cohesion: 0.27
Nodes (8): story_problems(), read(), test_cold_read_verdicts(), test_no_hook_setting_no_hook_check(), test_rules_accept_opener_setting(), test_story_problems(), test_story_problems_flags_summary_hook(), test_story_problems_money_claim()

### Community 52 - "wm_files"
Cohesion: 0.14
Nodes (8): commons_films(), article_images(), commons_search(), thumb_url(), usable_license(), wm_files(), wm_get(), article_text()

### Community 53 - "words_of"
Cohesion: 0.19
Nodes (8): clean_sound(), limit_sounds(), fill_money_graphics(), shows_person(), words_of(), test_clean_sound(), test_fill_money_graphics_and_caps(), test_clean_full_keeps_board_pic()

### Community 54 - "kit.mjs"
Cohesion: 0.10
Nodes (26): job, C, H, lightOf(), MOODS, W, rad(), rrect() (+18 more)

### Community 56 - "retention.py"
Cohesion: 0.20
Nodes (11): analyze(), edit_metrics(), load_metrics(), metrics_text(), normalize_metrics(), normalize_reply(), observations(), parse_metric() (+3 more)

### Community 57 - "render"
Cohesion: 0.10
Nodes (13): make_sfx(), short_credit(), ffmpeg(), graphics_count(), wants_remotion(), drawn_choices(), drawn_payoff(), render() (+5 more)

### Community 59 - "style_library"
Cohesion: 0.09
Nodes (15): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), clean_invention(), clean_look(), clean_transition() (+7 more)

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "test_opener3d.py"
Cohesion: 0.28
Nodes (9): clean(), num(), xz(), example(), look(), test_a_shot_can_frame_several_things(), test_bad_parts_go_back_to_the_coder(), test_example_is_clean() (+1 more)

### Community 62 - "write_json"
Cohesion: 0.15
Nodes (7): crop_film_bytes(), crop_filter(), film_frames(), film_piece(), shot_moments(), film_ffmpeg(), write_json()

### Community 63 - "ends_sentence"
Cohesion: 0.20
Nodes (6): caption_lines(), sentence_groups(), ends_sentence(), srt(), test_sentence_ends_include_curly_quotes_and_ellipsis(), test_sentences_running_across_cuts_are_one_take()

### Community 64 - "rewrite_paint_prompts"
Cohesion: 0.25
Nodes (4): rewrite_paint_prompts(), plan_gap_paintings(), test_rewrite_paint_prompts(), test_scene_without_picture_or_prompt_gets_painted_not_reused()

### Community 65 - "download_audio_choices"
Cohesion: 0.25
Nodes (5): freesound_fetch(), freesound_preview(), freesound_results(), download_audio_choices(), seed_audio_library()

### Community 66 - "logbook.py"
Cohesion: 0.17
Nodes (5): vault_page(), vault_refresh(), review_status(), storyboard(), apply()

### Community 69 - "test_first_second.py"
Cohesion: 0.18
Nodes (14): first_second_check(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture() (+6 more)

### Community 70 - "apply_review_fixes"
Cohesion: 0.18
Nodes (7): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 71 - "clean_full"
Cohesion: 0.12
Nodes (16): clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number() (+8 more)

### Community 72 - "time"
Cohesion: 0.11
Nodes (14): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+6 more)

### Community 73 - "ask_ai"
Cohesion: 0.10
Nodes (16): seed_ideas(), ask_ai(), gemini_model(), test_every_ai_gets_the_pipeline_preamble_once(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high() (+8 more)

### Community 75 - "audio_library.py"
Cohesion: 0.19
Nodes (20): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+12 more)

### Community 76 - "Opener3D.tsx"
Cohesion: 0.10
Nodes (30): aim(), BOOKS, Box(), Burst(), calculateOpener3D(), CameraRig(), Card(), clamp() (+22 more)

### Community 77 - "music_gain"
Cohesion: 0.14
Nodes (7): ass_time(), caption_size(), captions(), music_gain(), speak(), tts(), test_music_gain_evens_out_tracks()

### Community 79 - "first_sentence"
Cohesion: 0.18
Nodes (8): log_short(), first_sentence(), build(), add(), main(), scenes(), test_first_sentence_reads_across_the_cut(), test_logbook_hook_line_is_the_whole_first_sentence()

### Community 80 - "quality_check"
Cohesion: 0.25
Nodes (4): quality_check(), length_plan(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 81 - "test_style.py"
Cohesion: 0.09
Nodes (16): approve_candidate(), clean_style_code(), library_menu(), reject_candidate(), save_candidate(), write_style_index(), candidate_in(), library_snapshot() (+8 more)

### Community 82 - "full_props"
Cohesion: 0.20
Nodes (8): full_props(), full_pictures(), _board(), _jpg(), test_board_pictures_attached(), test_custom_cues_props_and_pictures(), test_remotion_props_full(), test_sfx_full()

### Community 85 - "paint_instead"
Cohesion: 0.25
Nodes (3): to_vertical(), paint_instead(), test_remotion_failure_paints()

### Community 89 - "choose_images"
Cohesion: 0.14
Nodes (17): choose_images(), download_picture(), recover_downloads(), is_person_portrait(), apply_look_scenes(), picking, planned_short(), scene() (+9 more)

### Community 90 - "fact_check"
Cohesion: 0.18
Nodes (8): fact_check(), test_fact_check_drops_full(), plan_with(), ask(), test_director_character_look_is_kept_short_or_dropped(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 91 - "short"
Cohesion: 0.22
Nodes (7): fake_ai(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused(), test_no_verdict_is_not_a_pass(), test_reveal_scene_is_drawn_with_its_own_rules(), test_use_opener_plays_the_drawn_opener()

### Community 92 - "test_blender_plan.py"
Cohesion: 0.05
Nodes (46): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+38 more)

### Community 94 - "gather_pool"
Cohesion: 0.14
Nodes (6): commercial_queries(), get_image(), openverse_images(), ov_get(), balanced_candidates(), gather_pool()

### Community 96 - "test_story_sound_library"
Cohesion: 0.67
Nodes (3): test_story_sound_library(), fetch(), _tone_wav()

### Community 97 - "plan"
Cohesion: 0.31
Nodes (4): plan(), render(), sheet(), write()

### Community 98 - "cold_read"
Cohesion: 0.22
Nodes (6): cold_read(), recheck_final_scripts(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 99 - "other_ai"
Cohesion: 0.33
Nodes (6): other_ai(), fake_providers(), claude(), reply(), test_every_mode_can_continue_through_two_exhausted_ais(), test_gemini_modes_choose_codex_and_keep_editor_choice()

### Community 100 - "write"
Cohesion: 0.29
Nodes (3): clean_code(), opener_role(), write()

### Community 101 - "duration"
Cohesion: 0.13
Nodes (10): shot_span(), cosy_instruct(), local_voice(), split_takes(), spoken_count(), voicestudio_unload(), duration(), is_loop_short() (+2 more)

### Community 102 - "rescue_graphics"
Cohesion: 0.40
Nodes (3): full_formats(), rescue_graphics(), test_rescue_respects_caps()

### Community 105 - "edit_scripts"
Cohesion: 0.15
Nodes (11): edit_scripts(), narration_lines(), saved_session(), test_all_modes_route_writer_editor_and_reader(), ask(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty(), test_only_the_second_edit_pass_gets_the_research(), test_script_rounds_stop_when_fixed_or_after_three() (+3 more)

### Community 106 - "sfx_events"
Cohesion: 0.25
Nodes (4): schedule_sounds(), sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 107 - "write_frames"
Cohesion: 0.29
Nodes (3): flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 109 - "lint"
Cohesion: 0.33
Nodes (4): lint(), lint_cutout(), test_lint(), test_lint_needs_draw()

### Community 111 - "apply_metadata"
Cohesion: 0.33
Nodes (3): apply_metadata(), clean_tags(), clean_title()

## Knowledge Gaps
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `render_remotion`, `re`, `finish_render`, `json`, `local_clips`, `frame_maker`, `opener_graphic`, `paint_opener_start`, `main`, `scene_cues`, `clean_photo`, `ends_sentence`, `rewrite_paint_prompts`, `test_full_scenes.py`, `audio_library.py`, `music_gain`, `test_style.py`, `paint_instead`, `choose_images`, `test_blender_plan.py`, `duration`, `rescue_graphics`, `sfx_events`, `write_frames`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12564102564102564 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `test_pictures_first.py`, `prepare_topic`, `re`, `test_rules.py`, `json`, `test_topic_ideas.py`, `owner`, `main`, `check_twists`, `fake_ai`, `test_story.py`, `words_of`, `retention.py`, `style_library`, `clean_full`, `ask_ai`, `test_full_scenes.py`, `quality_check`, `test_style.py`, `choose_images`, `fact_check`, `test_blender_plan.py`, `cold_read`, `limit_style`, `edit_scripts`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14204545454545456 - nodes in this community are weakly interconnected._
- **Should `prepare_topic` be split into smaller, more focused modules?**
  _Cohesion score 0.1067193675889328 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._
- **Should `render_remotion` be split into smaller, more focused modules?**
  _Cohesion score 0.05128205128205128 - nodes in this community are weakly interconnected._