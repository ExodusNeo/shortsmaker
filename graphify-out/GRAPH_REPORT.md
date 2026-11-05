# Graph Report - ShortsMaker  (2026-11-05)

## Corpus Check
- 140 files · ~168,032 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2250 nodes · 6207 edges · 116 communities (96 shown, 20 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 140 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8ab2a93f`
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
- test_full_scenes.py
- test_blender_render.py
- guarded.tsx
- k
- test_h3_handoff.py
- make_opener
- h3_run.py
- visual_review
- test_rules.py
- Journey.tsx
- toolkit.tsx
- json
- write_scripts
- gen.py
- core.mjs
- extra_sources.py
- edit_project.py
- makeKit
- test_topic_ideas.py
- ffmpeg
- frame_maker
- opener_graphic
- scene_cues
- look.py
- parts.py
- OpeningRulesTests
- gather_pool
- templates.py
- use
- resume_runs
- BigNumber.tsx
- main
- Paper
- apply_review_fixes
- build_scene.py
- Short.tsx
- textures.mjs
- callout_hold
- llm.py
- style_placeholders
- Halftone.tsx
- clean_photo
- trend_research
- fake_ai
- story_problems
- main
- words_of
- kit.mjs
- RetentionTests
- analyze
- render
- ReliabilityTests
- style_library
- run_agy
- bean.mjs
- image_sources.py
- configure_brain
- rewrite_paint_prompts
- write_json
- vault_page
- dexter.mjs
- kit_parts.mjs
- first_second_check
- paint_new
- clean_full
- re
- ask_ai
- pathlib
- audio_library.py
- ref_remotion
- music_gain
- preview
- edit_plan
- quality_check
- test_style.py
- edit_scripts
- MediaTests
- MetadataTests
- paint_instead
- PreflightTests
- MarkTests
- StoryPacingTests
- choose_images
- plan_with
- short
- test_blender_plan.py
- FeedbackTests
- get_image
- .render_fixture
- test_story_sound_library
- invent_component
- cold_read
- drawn_thumbnail
- opening_brief
- duration
- rescue_graphics
- limit_style
- finish_render
- test_ai_modes.py
- sfx_events
- write_frames
- logbook_results
- lint
- gemini_model
- apply_metadata
- BlenderFailed
- wants_remotion
- apply_look_scenes
- test_local_job_retries_a_hard_crash

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 64 edges
3. `write_scripts()` - 54 edges
4. `ask_ai()` - 49 edges
5. `MediaTests` - 35 edges
6. `main()` - 32 edges
7. `skinOf()` - 31 edges
8. `clamp()` - 29 edges
9. `Paper()` - 27 edges
10. `choose_images()` - 27 edges

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

## Communities (116 total, 20 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.15
Nodes (23): catalog_entries(), catalog_pool(), clean_pics(), save_pool(), entry(), film(), pic_short(), pool_of() (+15 more)

### Community 3 - "prepare_topic"
Cohesion: 0.10
Nodes (14): catalog_text(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures(), prepare_topic() (+6 more)

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "render_remotion"
Cohesion: 0.16
Nodes (9): render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain() (+1 more)

### Community 7 - "test_full_scenes.py"
Cohesion: 0.07
Nodes (31): short_skin(), clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), full_props(), is_payoff(), lint_custom_code() (+23 more)

### Community 8 - "test_blender_render.py"
Cohesion: 0.18
Nodes (15): peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises() (+7 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 10 - "k"
Cohesion: 0.07
Nodes (3): k, ellPts(), popS()

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "make_opener"
Cohesion: 0.14
Nodes (7): available(), make_opener(), missing_parts(), node_run(), sheet_times(), look(), test_kit_animals_must_be_used()

### Community 13 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 14 - "visual_review"
Cohesion: 0.24
Nodes (7): clock(), overlay_notes(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

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
Cohesion: 0.06
Nodes (25): main(), code_version(), fingerprint(), comfy_call(), moss_graph(), moss_images(), voicestudio_unload(), voicestudio_up() (+17 more)

### Community 19 - "write_scripts"
Cohesion: 0.08
Nodes (26): limit_full(), write_scripts(), owner(), _fake_planning(), test_director_prompt_mentions_full(), test_limit_full(), passing(), prepare() (+18 more)

### Community 20 - "gen.py"
Cohesion: 0.22
Nodes (5): images(), main(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "extra_sources.py"
Cohesion: 0.08
Nodes (31): brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images(), loc_images() (+23 more)

### Community 23 - "edit_project.py"
Cohesion: 0.12
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "test_topic_ideas.py"
Cohesion: 0.15
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 26 - "ffmpeg"
Cohesion: 0.11
Nodes (15): cosy_instruct(), cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt() (+7 more)

### Community 27 - "frame_maker"
Cohesion: 0.09
Nodes (12): ClipReader, draw_card(), draw_graphic(), fit_font(), frame_maker(), frame(), graphic_overlay(), person_card() (+4 more)

### Community 28 - "opener_graphic"
Cohesion: 0.15
Nodes (8): full_summary(), opener_graphic(), fix_drawn_answer(), fix_opener_graphic(), paint_opener_start(), test_full_summary(), test_opener_graphic(), test_weak_opener_graphic_fixes_then_handoff()

### Community 29 - "scene_cues"
Cohesion: 0.13
Nodes (11): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish() (+3 more)

### Community 30 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 33 - "gather_pool"
Cohesion: 0.10
Nodes (9): article_images(), commons_search(), thumb_url(), wm_files(), balanced_candidates(), gather_pool(), stubbed, test_gather_pool_shape() (+1 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "use"
Cohesion: 0.33
Nodes (4): fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 36 - "resume_runs"
Cohesion: 0.24
Nodes (12): begin(), context(), pack(), pending(), pending_topics(), read(), save_context(), unpack() (+4 more)

### Community 37 - "BigNumber.tsx"
Cohesion: 0.22
Nodes (13): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+5 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.12
Nodes (29): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+21 more)

### Community 40 - "apply_review_fixes"
Cohesion: 0.15
Nodes (8): apply_review_fixes(), ask(), _review_state(), test_auto_fix_graphic(), test_look_check_fixes_code(), test_redraw_failure_paints(), test_review_redraws_custom(), test_review_uses_unused_pool_pictures_before_painting()

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "textures.mjs"
Cohesion: 0.22
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "callout_hold"
Cohesion: 0.25
Nodes (5): read_need(), callout_hold(), pacing_check(), drop_unreadable_kinetic(), test_short_scene_callout_is_placed_so_the_check_passes()

### Community 45 - "llm.py"
Cohesion: 0.11
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 46 - "style_placeholders"
Cohesion: 0.19
Nodes (10): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_placeholders_match_the_slots() (+2 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "clean_photo"
Cohesion: 0.12
Nodes (8): clean_photo(), is_stereo(), trim_borders(), border(), plain(), vertical_image(), visual_unique(), mark_details()

### Community 49 - "trend_research"
Cohesion: 0.20
Nodes (6): channel_url(), new_channel(), save_channel(), seed_ideas(), trend_research(), yt_list()

### Community 50 - "fake_ai"
Cohesion: 0.27
Nodes (6): seo_pass(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel(), test_seo_never_sees_competitor_titles()

### Community 51 - "story_problems"
Cohesion: 0.09
Nodes (19): ass_time(), caption_lines(), captions(), styled(), ass_colour(), sentence_groups(), ends_sentence(), first_sentence() (+11 more)

### Community 52 - "main"
Cohesion: 0.12
Nodes (13): ask_count(), load_channel(), pick_channel(), use_channel(), fix_short(), main(), draft_rules(), require_rules() (+5 more)

### Community 53 - "words_of"
Cohesion: 0.13
Nodes (11): clean_sound(), limit_sounds(), graphic_low(), fill_money_graphics(), is_person_portrait(), parse_scene_money(), shows_person(), words_of() (+3 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "analyze"
Cohesion: 0.18
Nodes (11): analyze(), edit_metrics(), load_metrics(), metrics_text(), normalize_metrics(), normalize_reply(), observations(), parse_metric() (+3 more)

### Community 57 - "render"
Cohesion: 0.13
Nodes (8): make_sfx(), short_credit(), graphics_count(), drawn_choices(), drawn_payoff(), render(), use_opener(), test_drawn_choices_have_no_pictures()

### Community 59 - "style_library"
Cohesion: 0.11
Nodes (15): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), build() (+7 more)

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "image_sources.py"
Cohesion: 0.11
Nodes (8): commons_films(), crop_film_bytes(), crop_filter(), film_frames(), film_piece(), shot_moments(), film_ffmpeg(), usable_license()

### Community 63 - "configure_brain"
Cohesion: 0.27
Nodes (6): ask_brain(), ask_number(), ask_yes(), configure_brain(), normalize_brain(), command()

### Community 64 - "rewrite_paint_prompts"
Cohesion: 0.25
Nodes (4): rewrite_paint_prompts(), plan_gap_paintings(), test_rewrite_paint_prompts(), test_scene_without_picture_or_prompt_gets_painted_not_reused()

### Community 65 - "write_json"
Cohesion: 0.14
Nodes (10): freesound_fetch(), freesound_preview(), freesound_results(), import_media(), audition_audio(), download_audio_choices(), media_command(), review_audio_files() (+2 more)

### Community 69 - "first_second_check"
Cohesion: 0.15
Nodes (14): first_second_check(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture() (+6 more)

### Community 70 - "paint_new"
Cohesion: 0.33
Nodes (4): use_picture_from(), paint_new(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 71 - "clean_full"
Cohesion: 0.12
Nodes (16): clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number() (+8 more)

### Community 72 - "re"
Cohesion: 0.11
Nodes (15): align(), align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak(), commercial_queries() (+7 more)

### Community 73 - "ask_ai"
Cohesion: 0.14
Nodes (10): ask_ai(), test_every_ai_gets_the_pipeline_preamble_once(), test_quota_fallback_both_ways(), test_claude_pinned_to_opus_high(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash(), test_independent_review_falls_back_without_changing_solo_mode(), test_session_shared(), test_solo_ask_ai_hands_over_when_out_of_credits() (+2 more)

### Community 74 - "pathlib"
Cohesion: 0.11
Nodes (4): hex_rgb(), luminance(), fills_frame(), storyboard()

### Community 75 - "audio_library.py"
Cohesion: 0.24
Nodes (15): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+7 more)

### Community 77 - "music_gain"
Cohesion: 0.22
Nodes (4): music_gain(), speak(), tts(), test_music_gain_evens_out_tracks()

### Community 78 - "preview"
Cohesion: 0.29
Nodes (3): video_encoder(), preview(), test_encoder_cache_lives_with_video_encoder()

### Community 79 - "edit_plan"
Cohesion: 0.14
Nodes (7): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 80 - "quality_check"
Cohesion: 0.25
Nodes (4): quality_check(), length_plan(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 81 - "test_style.py"
Cohesion: 0.21
Nodes (10): save_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_candidate_names_unique_across_kinds() (+2 more)

### Community 82 - "edit_scripts"
Cohesion: 0.25
Nodes (5): edit_scripts(), narration_lines(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules(), test_failed_second_read_clears_old_verdict()

### Community 85 - "paint_instead"
Cohesion: 0.12
Nodes (6): gemini_images(), to_vertical(), ink_silhouette(), paint_instead(), test_ink_silhouette(), test_remotion_failure_paints()

### Community 89 - "choose_images"
Cohesion: 0.19
Nodes (14): choose_images(), download_picture(), recover_downloads(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded() (+6 more)

### Community 90 - "plan_with"
Cohesion: 0.25
Nodes (6): plan_with(), ask(), test_director_character_look_is_kept_short_or_dropped(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 91 - "short"
Cohesion: 0.22
Nodes (7): fake_ai(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused(), test_no_verdict_is_not_a_pass(), test_reveal_scene_is_drawn_with_its_own_rules(), test_use_opener_plays_the_drawn_opener()

### Community 92 - "test_blender_plan.py"
Cohesion: 0.12
Nodes (20): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), plan() (+12 more)

### Community 94 - "get_image"
Cohesion: 0.12
Nodes (9): get_image(), openverse_images(), ov_get(), wm_get(), full_pictures(), article_text(), fact_check(), test_board_pictures_attached() (+1 more)

### Community 96 - "test_story_sound_library"
Cohesion: 0.67
Nodes (3): test_story_sound_library(), fetch(), _tone_wav()

### Community 97 - "invent_component"
Cohesion: 0.18
Nodes (7): clean_style_code(), invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), test_invention_lint_failure_uses_fallback()

### Community 98 - "cold_read"
Cohesion: 0.22
Nodes (7): other_ai(), cold_read(), test_every_mode_can_continue_through_two_exhausted_ais(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_gemini_modes_choose_codex_and_keep_editor_choice(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers()

### Community 99 - "drawn_thumbnail"
Cohesion: 0.21
Nodes (9): thumbnail_order(), drawn_thumbnail(), test_thumbnail_order_skips_film_and_puts_openers_first(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 100 - "opening_brief"
Cohesion: 0.22
Nodes (4): clean_code(), review(), write(), opening_brief()

### Community 101 - "duration"
Cohesion: 0.22
Nodes (6): shot_span(), log_short(), duration(), scenes(), test_logbook_hook_line_is_the_whole_first_sentence(), test_sentences_running_across_cuts_are_one_take()

### Community 102 - "rescue_graphics"
Cohesion: 0.22
Nodes (5): full_formats(), rescue_graphics(), max_full(), max_full_planned(), test_rescue_respects_caps()

### Community 104 - "finish_render"
Cohesion: 0.22
Nodes (5): drawn_answer_problem(), sound_masking(), status_lines(), weak_opener_graphic(), finish_render()

### Community 105 - "test_ai_modes.py"
Cohesion: 0.20
Nodes (10): fake_providers(), claude(), reply(), saved_session(), test_all_modes_route_writer_editor_and_reader(), ask(), test_batch_uses_selected_codex_writer_and_migrates_saved_aliases(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty() (+2 more)

### Community 106 - "sfx_events"
Cohesion: 0.25
Nodes (4): schedule_sounds(), sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 107 - "write_frames"
Cohesion: 0.29
Nodes (3): flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 108 - "logbook_results"
Cohesion: 0.33
Nodes (3): entry_age(), logbook_results(), test_logbook_marks_tiny_samples()

### Community 110 - "gemini_model"
Cohesion: 0.40
Nodes (4): gemini_model(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_gemini_timeout_switches_to_flash()

### Community 111 - "apply_metadata"
Cohesion: 0.33
Nodes (3): apply_metadata(), clean_tags(), clean_title()

## Knowledge Gaps
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `render_remotion`, `test_blender_render.py`, `visual_review`, `json`, `ffmpeg`, `frame_maker`, `opener_graphic`, `scene_cues`, `resume_runs`, `callout_hold`, `clean_photo`, `story_problems`, `main`, `words_of`, `rewrite_paint_prompts`, `pathlib`, `audio_library.py`, `music_gain`, `preview`, `test_style.py`, `paint_instead`, `choose_images`, `duration`, `rescue_graphics`, `finish_render`, `sfx_events`, `write_frames`, `wants_remotion`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `MediaTests` connect `MediaTests` to `image_sources.py`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14919354838709678 - nodes in this community are weakly interconnected._
- **Why does `gather_pool()` connect `gather_pool` to `prepare_topic`, `clean_full`, `re`, `visual_review`, `clean_photo`, `json`, `words_of`, `extra_sources.py`, `choose_images`, `get_image`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `prepare_topic` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._