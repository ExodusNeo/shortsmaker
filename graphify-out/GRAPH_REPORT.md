# Graph Report - ShortsMaker  (2026-11-06)

## Corpus Check
- 144 files · ~182,160 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2371 nodes · 6529 edges · 117 communities (92 shown, 25 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 140 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cf5a4d94`
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
- guarded.tsx
- k
- test_h3_handoff.py
- drawn_opener.py
- h3_run.py
- visual_review
- test_rules.py
- Journey.tsx
- toolkit.tsx
- gpu.py
- write_scripts
- gen.py
- clamp
- extra_sources.py
- test_edit_project.py
- makeKit
- test_topic_ideas.py
- resume_runs
- frame_maker
- finish_render
- full_cues
- look.py
- parts.py
- OpeningRulesTests
- gather_pool
- templates.py
- paint_opener_start
- main
- BigNumber.tsx
- main
- Paper
- _fake_planning
- build_scene.py
- Short.tsx
- core.mjs
- scene_cues
- check_twists
- shutil
- Halftone.tsx
- paint_instead
- logbook_results
- test_story.py
- invent_component
- words_of
- kit.mjs
- RetentionTests
- json
- render
- ReliabilityTests
- edit_plan
- run_agy
- test_opener3d.py
- clean_pics
- ends_sentence
- rewrite_paint_prompts
- media_command
- style_placeholders
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
- captions
- clean_look
- first_sentence
- quality_check
- style_library
- full_props
- MediaTests
- MetadataTests
- bean.mjs
- PreflightTests
- MarkTests
- StoryPacingTests
- choose_images
- test_style.py
- test_drawn_opener.py
- test_blender_plan.py
- FeedbackTests
- make_paper
- review
- test_story_sound_library
- plan
- cold_read
- configure_brain
- missing_parts
- clean_sound
- lint_custom_code
- limit_style
- owner
- edit_scripts
- use
- clean_graphic
- test_short_credit
- lint_cutout
- make_sfx
- re
- short_skin
- limit_full
- drawn_choices
- front_door
- inside

## God Nodes (most connected - your core abstractions)
1. `k` - 99 edges
2. `render()` - 64 edges
3. `write_scripts()` - 54 edges
4. `ask_ai()` - 50 edges
5. `makeKit()` - 35 edges
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
- `test_pixabay_keeps_only_on_topic_videos()` --calls--> `pixabay_films()`  [EXTRACTED]
  tests/test_pictures_first.py → shortsmaker/footage.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`
- 3-file cycle: `shortsmaker/motion.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`
- 4-file cycle: `shortsmaker/motion.py -> shortsmaker/opening_rules.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`

## Communities (117 total, 25 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (23): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+15 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (30): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+22 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.16
Nodes (23): catalog_entries(), catalog_pool(), save_pool(), entry(), film(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+15 more)

### Community 3 - "prepare_topic"
Cohesion: 0.14
Nodes (9): contact_sheets(), pool_folder(), preflight_pictures(), prepare_topic(), article_text(), fact_check(), test_fact_check_drops_full(), test_empty_pool_drops_topic_without_ai() (+1 more)

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "render_remotion"
Cohesion: 0.16
Nodes (9): render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain() (+1 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.13
Nodes (15): clean_tsx_code(), code_custom_scenes(), custom_rules(), is_payoff(), look_and_fix(), opener_preflight(), preview_custom(), preview_sheet() (+7 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.05
Nodes (45): cosy_instruct(), cover_crop(), cut_owner_clip(), h3_problems(), h3_prompt(), h3_prompts(), local_clips(), local_job() (+37 more)

### Community 12 - "drawn_opener.py"
Cohesion: 0.10
Nodes (11): available(), clean_code(), fingerprint(), make_opener(), node_run(), opener_role(), sheet_times(), write() (+3 more)

### Community 13 - "h3_run.py"
Cohesion: 0.10
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 14 - "visual_review"
Cohesion: 0.18
Nodes (8): clock(), overlay_notes(), review_fixes(), sound_masking(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (37): load_rules(), min_real_pictures(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft() (+29 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.26
Nodes (20): CustomScene(), ExampleOpenerAction(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear() (+12 more)

### Community 18 - "gpu.py"
Cohesion: 0.07
Nodes (19): code_version(), crop_film_bytes(), crop_filter(), film_frames(), film_piece(), pixabay_films(), shot_moments(), shot_span() (+11 more)

### Community 19 - "write_scripts"
Cohesion: 0.15
Nodes (20): write_scripts(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare() (+12 more)

### Community 20 - "gen.py"
Cohesion: 0.22
Nodes (5): images(), main(), t5_encoder(), tts(), video()

### Community 21 - "clamp"
Cohesion: 0.10
Nodes (9): clamp(), eExpo(), eIn(), eIO(), eOut(), ik(), lerp(), lerpColor() (+1 more)

### Community 22 - "extra_sources.py"
Cohesion: 0.05
Nodes (38): brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images(), loc_images() (+30 more)

### Community 23 - "test_edit_project.py"
Cohesion: 0.13
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.13
Nodes (10): makeKit(), catmull(), centroid(), densify(), eBack(), INK, noise1(), popS() (+2 more)

### Community 25 - "test_topic_ideas.py"
Cohesion: 0.11
Nodes (14): seo_pass(), clash(), pages(), pick_ideas(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_clash_needs_every_name_word() (+6 more)

### Community 26 - "resume_runs"
Cohesion: 0.24
Nodes (12): begin(), context(), pack(), pending(), pending_topics(), read(), save_context(), unpack() (+4 more)

### Community 27 - "frame_maker"
Cohesion: 0.06
Nodes (17): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+9 more)

### Community 28 - "finish_render"
Cohesion: 0.14
Nodes (11): full_summary(), full_formats(), opener_graphic(), drawn_answer_problem(), first_second_check(), fix_drawn_answer(), fix_opener_graphic(), review_status() (+3 more)

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
Cohesion: 0.13
Nodes (7): balanced_candidates(), gather_pool(), load_pool(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits(), test_pool_roundtrip()

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "paint_opener_start"
Cohesion: 0.18
Nodes (4): gemini_images(), paint_opener_start(), weak_opener_graphic(), test_weak_opener_graphic_fixes_then_handoff()

### Community 36 - "main"
Cohesion: 0.08
Nodes (21): ask_brain(), ask_count(), ask_number(), ask_yes(), load_channel(), new_channel(), normalize_brain(), pick_channel() (+13 more)

### Community 37 - "BigNumber.tsx"
Cohesion: 0.22
Nodes (13): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+5 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.12
Nodes (29): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+21 more)

### Community 40 - "_fake_planning"
Cohesion: 0.22
Nodes (5): _fake_planning(), ask(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting()

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (17): Captions(), PersonCard(), Background(), Card, flashAlpha(), GraphicFor(), Move, Scene (+9 more)

### Community 43 - "core.mjs"
Cohesion: 0.13
Nodes (32): burst(), eBounce(), eElastic(), ellipse(), fibre(), fill(), _grain, grainCanvas() (+24 more)

### Community 44 - "scene_cues"
Cohesion: 0.15
Nodes (10): scene_cues(), read_need(), callout_hold(), pacing_check(), drop_unreadable_kinetic(), test_counter_finishes_before_it_leaves(), test_short_scene_callout_is_placed_so_the_check_passes(), test_graphic_card_hold_duration() (+2 more)

### Community 45 - "check_twists"
Cohesion: 0.47
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 46 - "shutil"
Cohesion: 0.18
Nodes (7): prune_cache(), library_menu(), reject_candidate(), save_candidate(), main(), props_for(), test_prune_cache_handles_pools()

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "paint_instead"
Cohesion: 0.09
Nodes (10): clean_photo(), is_stereo(), to_vertical(), trim_borders(), border(), plain(), vertical_image(), mark_details() (+2 more)

### Community 50 - "logbook_results"
Cohesion: 0.33
Nodes (3): entry_age(), logbook_results(), test_logbook_marks_tiny_samples()

### Community 51 - "test_story.py"
Cohesion: 0.27
Nodes (8): story_problems(), read(), test_cold_read_verdicts(), test_no_hook_setting_no_hook_check(), test_rules_accept_opener_setting(), test_story_problems(), test_story_problems_flags_summary_hook(), test_story_problems_money_claim()

### Community 52 - "invent_component"
Cohesion: 0.16
Nodes (8): invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), style_rules(), test_invention_lint_failure_uses_fallback(), test_placeholders_match_the_slots()

### Community 53 - "words_of"
Cohesion: 0.22
Nodes (7): rescue_graphics(), fill_money_graphics(), shows_person(), words_of(), test_fill_money_graphics_and_caps(), test_rescue_respects_caps(), test_clean_full_keeps_board_pic()

### Community 54 - "kit.mjs"
Cohesion: 0.11
Nodes (20): flat, fx, job, C, H, lightOf(), MOODS, W (+12 more)

### Community 56 - "json"
Cohesion: 0.11
Nodes (17): channel_url(), save_channel(), trend_research(), yt_list(), analyze(), command(), edit_metrics(), load_metrics() (+9 more)

### Community 57 - "render"
Cohesion: 0.10
Nodes (18): split_takes(), short_credit(), duration(), ffmpeg(), video_encoder(), write_json(), graphics_count(), is_loop_short() (+10 more)

### Community 59 - "edit_plan"
Cohesion: 0.17
Nodes (6): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "test_opener3d.py"
Cohesion: 0.26
Nodes (12): clean(), num(), xz(), example(), look(), test_a_shot_can_frame_several_things(), test_against_puts_a_cutout_at_the_house_door_and_inside_is_rejected(), test_bad_parts_go_back_to_the_coder() (+4 more)

### Community 62 - "clean_pics"
Cohesion: 0.17
Nodes (6): catalog_text(), clean_pics(), is_usable(), pictures_of(), usable(), direct_scripts()

### Community 63 - "ends_sentence"
Cohesion: 0.25
Nodes (5): sentence_groups(), ends_sentence(), srt(), test_sentence_ends_include_curly_quotes_and_ellipsis(), test_sentences_running_across_cuts_are_one_take()

### Community 64 - "rewrite_paint_prompts"
Cohesion: 0.25
Nodes (4): rewrite_paint_prompts(), plan_gap_paintings(), test_rewrite_paint_prompts(), test_scene_without_picture_or_prompt_gets_painted_not_reused()

### Community 65 - "media_command"
Cohesion: 0.16
Nodes (11): freesound_fetch(), freesound_preview(), freesound_results(), commercial_queries(), settings(), audition_audio(), download_audio_choices(), media_command() (+3 more)

### Community 66 - "style_placeholders"
Cohesion: 0.23
Nodes (8): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_slots_restored_after_render(), with_fakes()

### Community 69 - "test_first_second.py"
Cohesion: 0.19
Nodes (13): swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once() (+5 more)

### Community 70 - "apply_review_fixes"
Cohesion: 0.13
Nodes (10): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full() (+2 more)

### Community 71 - "clean_full"
Cohesion: 0.15
Nodes (10): clean_full(), number_figures(), show_number(), test_clean_full_board(), test_clean_full_document(), test_clean_full_journey(), test_clean_full_keeps_thing(), test_clean_full_limits() (+2 more)

### Community 72 - "time"
Cohesion: 0.13
Nodes (13): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+5 more)

### Community 73 - "ask_ai"
Cohesion: 0.11
Nodes (14): seed_ideas(), ask_ai(), gemini_model(), test_every_ai_gets_the_pipeline_preamble_once(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high() (+6 more)

### Community 75 - "audio_library.py"
Cohesion: 0.24
Nodes (15): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+7 more)

### Community 76 - "Opener3D.tsx"
Cohesion: 0.08
Nodes (41): aim(), BOOKS, Box(), Building(), Burst(), calculateOpener3D(), CameraRig(), Card() (+33 more)

### Community 77 - "captions"
Cohesion: 0.17
Nodes (6): ass_time(), caption_lines(), caption_size(), captions(), speak(), tts()

### Community 78 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 79 - "first_sentence"
Cohesion: 0.18
Nodes (8): log_short(), first_sentence(), build(), add(), main(), scenes(), test_first_sentence_reads_across_the_cut(), test_logbook_hook_line_is_the_whole_first_sentence()

### Community 80 - "quality_check"
Cohesion: 0.25
Nodes (4): quality_check(), length_plan(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 81 - "style_library"
Cohesion: 0.16
Nodes (13): approve_candidate(), style_library(), write_style_index(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure() (+5 more)

### Community 82 - "full_props"
Cohesion: 0.11
Nodes (13): schedule_sounds(), sfx_events(), full_props(), full_pictures(), _board(), _jpg(), test_board_pictures_attached(), test_custom_cues_props_and_pictures() (+5 more)

### Community 85 - "bean.mjs"
Cohesion: 0.46
Nodes (6): rrect(), arm(), bubble(), bust(), hat(), person()

### Community 89 - "choose_images"
Cohesion: 0.25
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 90 - "test_style.py"
Cohesion: 0.14
Nodes (11): wants_remotion(), apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_director_character_look_is_kept_short_or_dropped(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library() (+3 more)

### Community 91 - "test_drawn_opener.py"
Cohesion: 0.21
Nodes (8): fake_ai(), look(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused(), test_no_verdict_is_not_a_pass(), test_reveal_scene_is_drawn_with_its_own_rules(), test_use_opener_plays_the_drawn_opener()

### Community 92 - "test_blender_plan.py"
Cohesion: 0.05
Nodes (45): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+37 more)

### Community 94 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 96 - "test_story_sound_library"
Cohesion: 0.67
Nodes (3): test_story_sound_library(), fetch(), _tone_wav()

### Community 97 - "plan"
Cohesion: 0.19
Nodes (7): blends(), plan(), sheet(), sheet_times(), write(), test_a_cutout_that_melts_into_the_wall_goes_back(), test_the_preview_sees_every_shot()

### Community 98 - "cold_read"
Cohesion: 0.25
Nodes (5): cold_read(), recheck_final_scripts(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 99 - "configure_brain"
Cohesion: 0.21
Nodes (10): configure_brain(), other_ai(), fake_providers(), claude(), reply(), saved_session(), test_every_mode_can_continue_through_two_exhausted_ais(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty() (+2 more)

### Community 100 - "missing_parts"
Cohesion: 0.33
Nodes (4): missing_parts(), test_kit_animals_must_be_used(), test_a_knock_needs_a_closed_door_and_a_messenger_his_letter(), test_hold_counts_as_drawing_the_letter_and_scenery_stays_3d()

### Community 101 - "clean_sound"
Cohesion: 0.29
Nodes (5): clean_sound(), limit_sounds(), word(), contains(), test_clean_sound()

### Community 102 - "lint_custom_code"
Cohesion: 0.29
Nodes (5): fallback_custom_tsx(), lint_custom_code(), test_custom_code_cannot_load_code_or_use_network(), test_fallback_custom_is_clean(), test_lint_custom_code()

### Community 105 - "edit_scripts"
Cohesion: 0.15
Nodes (9): edit_scripts(), narration_lines(), test_all_modes_route_writer_editor_and_reader(), ask(), test_only_the_second_edit_pass_gets_the_research(), test_script_rounds_stop_when_fixed_or_after_three(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules() (+1 more)

### Community 106 - "use"
Cohesion: 0.33
Nodes (4): fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 107 - "clean_graphic"
Cohesion: 0.50
Nodes (4): clean_graphic(), coords(), is_num(), test_clean_question_and_kinetic()

### Community 109 - "lint_cutout"
Cohesion: 0.33
Nodes (4): lint(), lint_cutout(), test_lint(), test_lint_needs_draw()

### Community 111 - "re"
Cohesion: 0.06
Nodes (20): music_gain(), vault_page(), vault_refresh(), import_media(), local_assets(), media_search_words(), recover_downloads(), is_person_portrait() (+12 more)

## Knowledge Gaps
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `render_remotion`, `pathlib`, `test_h3_handoff.py`, `visual_review`, `gpu.py`, `resume_runs`, `frame_maker`, `finish_render`, `paint_opener_start`, `main`, `scene_cues`, `shutil`, `paint_instead`, `words_of`, `ends_sentence`, `rewrite_paint_prompts`, `test_full_scenes.py`, `audio_library.py`, `captions`, `full_props`, `choose_images`, `test_style.py`, `test_blender_plan.py`, `make_paper`, `make_sfx`, `re`, `drawn_choices`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12564102564102564 - nodes in this community are weakly interconnected._
- **Why does `trim_borders()` connect `paint_instead` to `test_full_scenes.py`, `words_of`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Should `prepare_topic` be split into smaller, more focused modules?**
  _Cohesion score 0.14166666666666666 - nodes in this community are weakly interconnected._
- **Why does `ReliabilityTests` connect `ReliabilityTests` to `pathlib`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._
- **Should `code_custom_scenes` be split into smaller, more focused modules?**
  _Cohesion score 0.12923076923076923 - nodes in this community are weakly interconnected._