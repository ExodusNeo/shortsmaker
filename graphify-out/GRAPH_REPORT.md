# Graph Report - ShortsMaker  (2026-11-06)

## Corpus Check
- 151 files · ~196,990 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2490 nodes · 6817 edges · 113 communities (92 shown, 21 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 141 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `df0b8556`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- prepare_topic
- json
- split_make_shorts.py
- render_remotion
- code_custom_scenes
- plan_rules.py
- guarded.tsx
- k
- test_h3_handoff.py
- review
- opener_crew.py
- test_first_second.py
- test_rules.py
- Journey.tsx
- toolkit.tsx
- short_render.py
- write_scripts
- gen.py
- style_placeholders
- fetch
- make
- core.mjs
- topic_ideas.py
- resume_runs
- frame_maker
- finish_render
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
- textures.mjs
- scene_cues
- check_twists
- extra_sources.py
- Halftone.tsx
- clean_photo
- test_blender_render.py
- logbook_results
- test_story.py
- invent_component
- test_opener_crew.py
- kit.mjs
- RetentionTests
- retention.py
- checkpoints.py
- ReliabilityTests
- edit_plan
- run_agy
- opener3d.py
- test_blender_run.py
- ends_sentence
- hashlib
- media_menu.py
- audio_mix.py
- capture_prompts
- kit_parts.mjs
- state
- apply_review_fixes
- clean_full
- qwen_voice.py
- ask_ai
- audio_library.py
- Opener3D.tsx
- save_candidate
- clean_look
- make_paper
- style_library
- trend_research
- MediaTests
- MetadataTests
- bean.mjs
- PreflightTests
- MarkTests
- StoryPacingTests
- choose_images
- test_style.py
- test_drawn_opener.py
- test_blender_scene.py
- FeedbackTests
- fix_short
- pick_channel
- article_text
- render
- cold_read
- potato_pile.mjs
- lint_cutout
- vault_page
- limit_style
- test_full_scenes.py
- edit_scripts
- test_weak_opener_graphic_fixes_then_handoff
- apply_metadata
- umbrellas.mjs
- battery.mjs
- re
- telegraph_sounder.mjs
- run_draft

## God Nodes (most connected - your core abstractions)
1. `k` - 100 edges
2. `render()` - 64 edges
3. `write_scripts()` - 54 edges
4. `ask_ai()` - 53 edges
5. `makeKit()` - 37 edges
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
- `test_fake_reaches_callers()` --calls--> `code_custom_scenes()`  [EXTRACTED]
  tests/test_package.py → shortsmaker/motion.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`
- 3-file cycle: `shortsmaker/motion.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`
- 4-file cycle: `shortsmaker/motion.py -> shortsmaker/opening_rules.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`

## Communities (113 total, 21 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (23): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+15 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (30): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+22 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.11
Nodes (31): catalog_entries(), catalog_pool(), save_pool(), seo_pass(), entry(), fake_ai, film(), pic_short() (+23 more)

### Community 3 - "prepare_topic"
Cohesion: 0.10
Nodes (12): catalog_text(), clean_pics(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures() (+4 more)

### Community 4 - "json"
Cohesion: 0.11
Nodes (12): call(), fit_start(), frames(), graph(), main(), saved_file(), node_run(), staged() (+4 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "render_remotion"
Cohesion: 0.16
Nodes (9): render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain() (+1 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.11
Nodes (18): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), is_payoff(), lint_custom_code(), look_and_fix(), opener_preflight() (+10 more)

### Community 8 - "plan_rules.py"
Cohesion: 0.10
Nodes (9): crop_film_bytes(), fills_frame(), person_card(), comfy_call(), moss_graph(), moss_images(), voicestudio_up(), visual_unique() (+1 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "review"
Cohesion: 0.19
Nodes (5): clean_code(), look_dir(), review(), write(), RenderResumeTests

### Community 13 - "opener_crew.py"
Cohesion: 0.09
Nodes (20): minutes(), opener_role(), staging_line(), animal_cutout(), check_staging(), default_cutout(), kit_hats(), kit_text() (+12 more)

### Community 14 - "test_first_second.py"
Cohesion: 0.09
Nodes (16): clock(), overlay_notes(), pacing_check(), quality_check(), review_fixes(), review_status(), visual_review(), max_seconds() (+8 more)

### Community 15 - "test_rules.py"
Cohesion: 0.17
Nodes (23): parse_rules(), make(), stop_text(), StopPicker, test_bad_min_pictures_stops(), test_blender_needs_a_build_plan_section(), test_bom_and_crlf_load_the_same(), test_draft_stops() (+15 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.26
Nodes (20): CustomScene(), ExampleOpenerAction(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear() (+12 more)

### Community 18 - "short_render.py"
Cohesion: 0.10
Nodes (9): hex_rgb(), luminance(), short_skin(), available(), available(), prune_cache(), paint_instead(), prune_work() (+1 more)

### Community 19 - "write_scripts"
Cohesion: 0.12
Nodes (23): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+15 more)

### Community 20 - "gen.py"
Cohesion: 0.22
Nodes (5): images(), main(), t5_encoder(), tts(), video()

### Community 21 - "style_placeholders"
Cohesion: 0.21
Nodes (9): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_slots_restored_after_render() (+1 more)

### Community 22 - "fetch"
Cohesion: 0.06
Nodes (25): archive_ad_films(), archive_films(), commons_films(), crop_filter(), duke_films(), film_frames(), film_piece(), nasa_films() (+17 more)

### Community 23 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "core.mjs"
Cohesion: 0.07
Nodes (31): makeKit(), burst(), catmull(), centroid(), clamp(), densify(), eBack(), eBounce() (+23 more)

### Community 25 - "topic_ideas.py"
Cohesion: 0.14
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 26 - "resume_runs"
Cohesion: 0.32
Nodes (9): begin(), context(), pending(), pending_topics(), read(), update(), finish_short(), record_failure() (+1 more)

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (14): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+6 more)

### Community 28 - "finish_render"
Cohesion: 0.10
Nodes (16): full_summary(), opening_brief(), full_formats(), opener_graphic(), drawn_answer_problem(), first_second_check(), fix_drawn_answer(), fix_opener_graphic() (+8 more)

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
Cohesion: 0.08
Nodes (12): article_images(), commons_search(), thumb_url(), wm_files(), balanced_candidates(), gather_pool(), owner(), _fake_planning() (+4 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "render"
Cohesion: 0.08
Nodes (19): make_sfx(), save_context(), gemini_images(), split_takes(), short_credit(), duration(), ffmpeg(), video_encoder() (+11 more)

### Community 36 - "main"
Cohesion: 0.14
Nodes (13): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), normalize_brain(), main(), command() (+5 more)

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
Cohesion: 0.11
Nodes (12): cosy_instruct(), cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt() (+4 more)

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
Cohesion: 0.17
Nodes (16): brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images(), loc_images() (+8 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "clean_photo"
Cohesion: 0.14
Nodes (7): clean_photo(), is_stereo(), to_vertical(), trim_borders(), border(), plain(), vertical_image()

### Community 49 - "test_blender_render.py"
Cohesion: 0.13
Nodes (17): BlenderFailed, code_version(), peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short() (+9 more)

### Community 50 - "logbook_results"
Cohesion: 0.33
Nodes (3): entry_age(), logbook_results(), test_logbook_marks_tiny_samples()

### Community 51 - "test_story.py"
Cohesion: 0.13
Nodes (17): log_short(), first_sentence(), story_problems(), build(), add(), main(), read(), scenes() (+9 more)

### Community 52 - "invent_component"
Cohesion: 0.14
Nodes (9): clean_style_code(), invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), style_rules(), test_invention_lint_failure_uses_fallback() (+1 more)

### Community 53 - "test_opener_crew.py"
Cohesion: 0.26
Nodes (9): fake(), short(), staging(), test_a_failed_part_falls_back_to_its_substitute(), test_a_made_part_is_kept_and_reused_with_no_ai(), test_a_painter_with_unusable_code_gets_the_plain_kit_cutout(), test_parallel_calls_are_capped(), test_staging_is_checked_against_the_kit() (+1 more)

### Community 54 - "kit.mjs"
Cohesion: 0.09
Nodes (27): bounds(), EDGE, flat, fx, PAD_TOP, PAD_X, paintAll(), STEPS (+19 more)

### Community 56 - "retention.py"
Cohesion: 0.20
Nodes (11): analyze(), edit_metrics(), load_metrics(), metrics_text(), normalize_metrics(), normalize_reply(), observations(), parse_metric() (+3 more)

### Community 59 - "edit_plan"
Cohesion: 0.17
Nodes (6): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 60 - "run_agy"
Cohesion: 0.18
Nodes (7): argon_out(), quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "opener3d.py"
Cohesion: 0.07
Nodes (30): box_of(), clean(), dress(), front_door(), half_width(), in_order(), inside(), nudge() (+22 more)

### Community 62 - "test_blender_run.py"
Cohesion: 0.18
Nodes (9): drawn_choices(), drawn_thumbnail(), drawn_short(), jpeg(), test_drawn_choices_have_no_pictures(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 63 - "ends_sentence"
Cohesion: 0.29
Nodes (4): sentence_groups(), ends_sentence(), srt(), test_sentence_ends_include_curly_quotes_and_ellipsis()

### Community 64 - "hashlib"
Cohesion: 0.31
Nodes (5): shot_moments(), is_loop_short(), load(), save(), signature()

### Community 65 - "media_menu.py"
Cohesion: 0.40
Nodes (6): audition_audio(), download_audio_choices(), media_command(), print_source_status(), review_audio_files(), seed_audio_library()

### Community 66 - "audio_mix.py"
Cohesion: 0.09
Nodes (14): ass_time(), caption_lines(), caption_size(), captions(), freesound_fetch(), freesound_preview(), freesound_results(), music_gain() (+6 more)

### Community 67 - "capture_prompts"
Cohesion: 0.20
Nodes (6): load_rules(), min_real_pictures(), capture_prompts(), ask(), test_load_rules_sets_session(), test_strange_history_prompts_unchanged()

### Community 69 - "state"
Cohesion: 0.29
Nodes (8): swap_pictures(), real(), state(), test_failed_preview_clears_previous_opener_score(), test_opener_fix_swaps_once(), test_swap_ignores_a_clip_already_dropped(), test_swap_moves_the_owners_clip_with_its_picture(), test_swap_pictures_trades_real_pictures()

### Community 70 - "apply_review_fixes"
Cohesion: 0.12
Nodes (9): apply_review_fixes(), ask(), _review_state(), test_auto_fix_graphic(), test_look_check_fixes_code(), test_redraw_failure_paints(), test_review_redraws_custom(), test_review_uses_unused_pool_pictures_before_painting() (+1 more)

### Community 71 - "clean_full"
Cohesion: 0.07
Nodes (27): clean_sound(), limit_sounds(), graphic_low(), rescue_graphics(), clean_full(), word(), clean_graphic(), contains() (+19 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.11
Nodes (15): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+7 more)

### Community 73 - "ask_ai"
Cohesion: 0.12
Nodes (14): ask_ai(), gemini_model(), test_every_ai_gets_the_pipeline_preamble_once(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high(), test_fake_reaches_callers() (+6 more)

### Community 75 - "audio_library.py"
Cohesion: 0.24
Nodes (15): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+7 more)

### Community 76 - "Opener3D.tsx"
Cohesion: 0.07
Nodes (45): aim(), BOOKS, Box(), Building(), Burst(), calculateOpener3D(), CameraRig(), Card() (+37 more)

### Community 77 - "save_candidate"
Cohesion: 0.22
Nodes (7): library_menu(), reject_candidate(), save_candidate(), candidate_in(), test_candidate_names_unique_across_kinds(), test_reject_deletes(), test_save_candidate_unique_slug()

### Community 78 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 80 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 81 - "style_library"
Cohesion: 0.20
Nodes (10): approve_candidate(), style_library(), write_style_index(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes() (+2 more)

### Community 82 - "trend_research"
Cohesion: 0.29
Nodes (4): channel_url(), seed_ideas(), trend_research(), yt_list()

### Community 85 - "bean.mjs"
Cohesion: 0.35
Nodes (9): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), SKIN (+1 more)

### Community 89 - "choose_images"
Cohesion: 0.17
Nodes (15): choose_images(), download_picture(), recover_downloads(), is_person_portrait(), picking, planned_short(), scene(), still() (+7 more)

### Community 90 - "test_style.py"
Cohesion: 0.12
Nodes (12): wants_remotion(), apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_clean_question_and_kinetic(), test_director_character_look_is_kept_short_or_dropped(), test_director_inventions_are_kept_with_a_spec() (+4 more)

### Community 91 - "test_drawn_opener.py"
Cohesion: 0.10
Nodes (16): fingerprint(), lint(), make_opener(), spoils(), use_opener(), fake_ai(), look(), short() (+8 more)

### Community 92 - "test_blender_scene.py"
Cohesion: 0.07
Nodes (42): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+34 more)

### Community 94 - "fix_short"
Cohesion: 0.16
Nodes (10): load_channel(), fix_short(), use_picture_from(), paint_new(), load_state(), test_fix_bat_explains_a_drawn_short(), test_new_picture_drops_mark(), test_paint_new_clears_full() (+2 more)

### Community 95 - "pick_channel"
Cohesion: 0.29
Nodes (5): new_channel(), pick_channel(), save_channel(), use_channel(), test_new_channel_stops_for_review()

### Community 96 - "article_text"
Cohesion: 0.40
Nodes (3): article_text(), fact_check(), test_fact_check_drops_full()

### Community 97 - "render"
Cohesion: 0.15
Nodes (7): sheet_times(), blends(), render(), sheet(), sheet_times(), test_a_cutout_that_melts_into_the_wall_goes_back(), test_the_preview_sees_every_shot()

### Community 98 - "cold_read"
Cohesion: 0.18
Nodes (7): other_ai(), cold_read(), recheck_final_scripts(), test_gemini_modes_choose_codex_and_keep_editor_choice(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 100 - "lint_cutout"
Cohesion: 0.17
Nodes (9): missing_parts(), lint_cutout(), assemble(), owner(), test_kit_animals_must_be_used(), test_a_knock_needs_a_closed_door_and_a_messenger_his_letter(), test_hold_counts_as_drawing_the_letter_and_scenery_stays_3d(), test_lint_needs_draw() (+1 more)

### Community 104 - "test_full_scenes.py"
Cohesion: 0.10
Nodes (14): full_props(), full_pictures(), _board(), _jpg(), test_board_pictures_attached(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_remotion_failure_paints() (+6 more)

### Community 105 - "edit_scripts"
Cohesion: 0.11
Nodes (16): edit_scripts(), length_plan(), narration_lines(), fake_providers(), claude(), reply(), saved_session(), test_all_modes_route_writer_editor_and_reader() (+8 more)

### Community 106 - "test_weak_opener_graphic_fixes_then_handoff"
Cohesion: 0.17
Nodes (6): weak_opener_graphic(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), test_weak_opener_graphic_fixes_then_handoff(), use()

### Community 108 - "apply_metadata"
Cohesion: 0.33
Nodes (3): apply_metadata(), clean_tags(), clean_title()

### Community 111 - "re"
Cohesion: 0.12
Nodes (8): commercial_queries(), shot_span(), import_media(), local_assets(), media_search_words(), mark_details(), max_full(), max_full_planned()

### Community 114 - "run_draft"
Cohesion: 0.18
Nodes (10): draft_rules(), require_rules(), draft_reply(), run_draft(), test_draft_blender_channel_needs_build_plan(), test_draft_keeps_ai_headings_inside_their_section(), test_draft_never_overwrites(), test_draft_retries_once_then_stops() (+2 more)

## Knowledge Gaps
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `render_remotion`, `plan_rules.py`, `test_first_second.py`, `short_render.py`, `resume_runs`, `frame_maker`, `finish_render`, `main`, `local_clips`, `scene_cues`, `clean_photo`, `test_blender_render.py`, `test_blender_run.py`, `ends_sentence`, `hashlib`, `audio_mix.py`, `clean_full`, `audio_library.py`, `save_candidate`, `make_paper`, `choose_images`, `test_style.py`, `test_drawn_opener.py`, `fix_short`, `re`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12564102564102564 - nodes in this community are weakly interconnected._
- **Why does `MediaTests` connect `MediaTests` to `plan_rules.py`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11033681765389082 - nodes in this community are weakly interconnected._
- **Why does `ReliabilityTests` connect `ReliabilityTests` to `pathlib`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Should `prepare_topic` be split into smaller, more focused modules?**
  _Cohesion score 0.10144927536231885 - nodes in this community are weakly interconnected._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.10541310541310542 - nodes in this community are weakly interconnected._