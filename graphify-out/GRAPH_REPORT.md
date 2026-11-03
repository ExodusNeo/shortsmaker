# Graph Report - ShortsMaker  (2026-11-03)

## Corpus Check
- 140 files · ~165,765 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2223 nodes · 6135 edges · 111 communities (88 shown, 23 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 135 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `215455ce`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- gather_pool
- test_blender_scene.py
- split_make_shorts.py
- duration
- code_custom_scenes
- test_blender_render.py
- guarded.tsx
- k
- test_h3_handoff.py
- re
- json
- subprocess
- test_rules.py
- Journey.tsx
- toolkit.tsx
- shutil
- write_scripts
- Local GPU Worker
- core.mjs
- local_clips
- make
- makeKit
- test_blender_run.py
- paint_instead
- frame_maker
- apply_review_fixes
- look.py
- parts.py
- test_drawn_opener.py
- owner
- templates.py
- paint_opener_start
- edit_scripts
- full/types.ts
- main
- Paper
- test_story.py
- build_scene.py
- Short.tsx
- textures.mjs
- sfx_events
- writing.py
- invent_component
- Halftone.tsx
- trim_borders
- style_library
- fake_ai
- story_problems
- style_placeholders
- footage.py
- kit.mjs
- RetentionTests
- retention.py
- render
- ReliabilityTests
- approve_candidate
- ask_ai
- bean.mjs
- clean_look
- make_paper
- extra_sources.py
- media_command
- visual_review
- dexter.mjs
- kit_parts.mjs
- test_first_second.py
- rewrite_paint_prompts
- clean_full
- qwen_voice.py
- test_package.py
- test_full_scenes.py
- audio_library.py
- Custom3.tsx
- captions
- test_every_mode_can_continue_through_two_exhausted_ais
- edit_plan
- full_cues
- plan_with
- main
- MediaTests
- MetadataTests
- finish_render
- PreflightTests
- MarkTests
- StoryPacingTests
- choose_images
- write_frames
- quality_check
- test_blender_plan.py
- FeedbackTests
- speak
- full_props
- test_story_sound_library
- gemini_model
- pacing_check
- render_remotion
- make_sfx
- rescue_graphics
- BlenderFailed
- limit_style
- cold_read_line
- srt
- peaks
- test_short_credit
- _run
- swap_inventions
- style_props

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 64 edges
3. `write_scripts()` - 53 edges
4. `ask_ai()` - 48 edges
5. `MediaTests` - 33 edges
6. `main()` - 32 edges
7. `skinOf()` - 31 edges
8. `clamp()` - 28 edges
9. `Paper()` - 27 edges
10. `ellPts()` - 26 edges

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

## Communities (111 total, 23 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.13
Nodes (26): catalog_entries(), catalog_pool(), clean_pics(), save_pool(), entry(), film(), pic_short(), pool_of() (+18 more)

### Community 3 - "gather_pool"
Cohesion: 0.08
Nodes (16): balanced_candidates(), catalog_text(), contact_sheets(), gather_pool(), is_usable(), load_pool(), pictures_of(), pool_folder() (+8 more)

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "duration"
Cohesion: 0.12
Nodes (12): shot_span(), cosy_instruct(), local_voice(), sentence_groups(), split_takes(), log_short(), duration(), is_loop_short() (+4 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.12
Nodes (16): clean_tsx_code(), code_custom_scenes(), custom_rules(), is_payoff(), lint_custom_code(), look_and_fix(), opener_preflight(), preview_custom() (+8 more)

### Community 8 - "test_blender_render.py"
Cohesion: 0.28
Nodes (11): render_clips(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises(), test_frames_are_trimmed_after_the_clips_are_cut(), test_missing_blender_raises() (+3 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.13
Nodes (18): Box, boxAt(), clamp, Connect(), fitCard(), hits(), layoutColumn(), layoutGrid() (+10 more)

### Community 10 - "k"
Cohesion: 0.07
Nodes (3): k, ellPts(), popS()

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "re"
Cohesion: 0.08
Nodes (13): clean_code(), node_run(), fallback_custom_tsx(), mark_details(), parse_scene_money(), clean_style_code(), reject_candidate(), save_candidate() (+5 more)

### Community 13 - "json"
Cohesion: 0.07
Nodes (19): call(), fit_start(), frames(), graph(), main(), saved_file(), channel_url(), trend_research() (+11 more)

### Community 14 - "subprocess"
Cohesion: 0.10
Nodes (5): hex_rgb(), luminance(), local_assets(), media_search_words(), storyboard()

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (37): load_rules(), min_real_pictures(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft() (+29 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.21
Nodes (21): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+13 more)

### Community 18 - "shutil"
Cohesion: 0.10
Nodes (14): code_version(), use_picture_from(), available(), fingerprint(), import_media(), prune_cache(), paint_new(), load() (+6 more)

### Community 19 - "write_scripts"
Cohesion: 0.12
Nodes (23): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+15 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "local_clips"
Cohesion: 0.13
Nodes (10): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), motion_prompt(), start_picture(), start_picture_problems() (+2 more)

### Community 23 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "test_blender_run.py"
Cohesion: 0.31
Nodes (7): drawn_thumbnail(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so(), test_thumbnail_uses_the_real_photo()

### Community 26 - "paint_instead"
Cohesion: 0.25
Nodes (3): to_vertical(), paint_instead(), test_remotion_failure_paints()

### Community 27 - "frame_maker"
Cohesion: 0.08
Nodes (14): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), frame_maker(), frame(), graphic_low() (+6 more)

### Community 28 - "apply_review_fixes"
Cohesion: 0.13
Nodes (9): apply_review_fixes(), pool_pictures(), ask(), _review_state(), test_auto_fix_graphic(), test_look_check_fixes_code(), test_redraw_failure_paints(), test_review_redraws_custom() (+1 more)

### Community 30 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 32 - "test_drawn_opener.py"
Cohesion: 0.05
Nodes (19): lint(), make_opener(), missing_parts(), review(), sheet_times(), write(), fake_ai(), look() (+11 more)

### Community 33 - "owner"
Cohesion: 0.22
Nodes (4): owner(), _fake_planning(), test_director_prompt_mentions_full(), test_good_look_check_skips_the_extra_compile()

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "paint_opener_start"
Cohesion: 0.13
Nodes (7): gemini_images(), paint_opener_start(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), test_weak_opener_graphic_fixes_then_handoff(), use()

### Community 36 - "edit_scripts"
Cohesion: 0.13
Nodes (11): other_ai(), cold_read(), edit_scripts(), narration_lines(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_gemini_modes_choose_codex_and_keep_editor_choice(), test_solo_edit_scripts_uses_same_ai(), test_cold_read_handles_malformed_reply() (+3 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (22): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+14 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "test_story.py"
Cohesion: 0.36
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.13
Nodes (19): Captions(), PersonCard(), Root(), Background(), flashAlpha(), GraphicFor(), Move, Scene (+11 more)

### Community 43 - "textures.mjs"
Cohesion: 0.22
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "sfx_events"
Cohesion: 0.15
Nodes (8): schedule_sounds(), sfx_events(), full_pictures(), _board(), test_board_pictures_attached(), test_sfx_full(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 45 - "writing.py"
Cohesion: 0.07
Nodes (14): apply_metadata(), clean_tags(), clean_title(), clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas() (+6 more)

### Community 46 - "invent_component"
Cohesion: 0.20
Nodes (7): invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), test_invention_lint_failure_uses_fallback(), test_placeholders_match_the_slots()

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "trim_borders"
Cohesion: 0.20
Nodes (5): is_stereo(), trim_borders(), border(), plain(), vertical_image()

### Community 49 - "style_library"
Cohesion: 0.20
Nodes (8): style_library(), style_rules(), write_style_index(), build(), add(), main(), test_library_entries_have_fields(), test_write_style_index_is_deterministic()

### Community 50 - "fake_ai"
Cohesion: 0.15
Nodes (9): entry_age(), logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel() (+1 more)

### Community 51 - "story_problems"
Cohesion: 0.20
Nodes (10): first_sentence(), recheck_final_scripts(), story_problems(), read(), test_cold_read_verdicts(), test_first_sentence_reads_across_the_cut(), test_no_hook_setting_no_hook_check(), test_story_problems() (+2 more)

### Community 52 - "style_placeholders"
Cohesion: 0.23
Nodes (8): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_slots_restored_after_render(), with_fakes()

### Community 53 - "footage.py"
Cohesion: 0.16
Nodes (9): archive_ad_films(), archive_films(), crop_film_bytes(), crop_filter(), duke_films(), film_frames(), film_piece(), shot_moments() (+1 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "retention.py"
Cohesion: 0.20
Nodes (11): analyze(), edit_metrics(), load_metrics(), metrics_text(), normalize_metrics(), normalize_reply(), observations(), parse_metric() (+3 more)

### Community 57 - "render"
Cohesion: 0.08
Nodes (19): ducking_filter(), preview_mix(), music_gain(), short_credit(), ffmpeg(), video_encoder(), graphics_count(), wants_remotion() (+11 more)

### Community 59 - "approve_candidate"
Cohesion: 0.33
Nodes (6): approve_candidate(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes()

### Community 60 - "ask_ai"
Cohesion: 0.11
Nodes (13): seed_ideas(), ask_ai(), quota_exhausted(), run_agy(), run_codex(), direct_scripts(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images() (+5 more)

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 63 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 64 - "extra_sources.py"
Cohesion: 0.06
Nodes (35): brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images(), loc_images() (+27 more)

### Community 65 - "media_command"
Cohesion: 0.22
Nodes (8): freesound_fetch(), freesound_preview(), freesound_results(), audition_audio(), download_audio_choices(), media_command(), review_audio_files(), seed_audio_library()

### Community 66 - "visual_review"
Cohesion: 0.24
Nodes (7): clock(), overlay_notes(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 69 - "test_first_second.py"
Cohesion: 0.16
Nodes (15): first_second_check(), review_status(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing() (+7 more)

### Community 70 - "rewrite_paint_prompts"
Cohesion: 0.25
Nodes (4): rewrite_paint_prompts(), plan_gap_paintings(), test_rewrite_paint_prompts(), test_scene_without_picture_or_prompt_gets_painted_not_reused()

### Community 71 - "clean_full"
Cohesion: 0.08
Nodes (24): clean_sound(), limit_sounds(), clean_full(), word(), clean_graphic(), contains(), coords(), fill_money_graphics() (+16 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.11
Nodes (15): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+7 more)

### Community 73 - "test_package.py"
Cohesion: 0.14
Nodes (10): scene_cues(), test_counter_finishes_before_it_leaves(), test_claude_pinned_to_opus_high(), test_fake_reaches_callers(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash(), test_graphic_card_hold_duration(), test_independent_review_falls_back_without_changing_solo_mode(), test_person_card_hold_and_exit_gap() (+2 more)

### Community 75 - "audio_library.py"
Cohesion: 0.27
Nodes (13): approved_sound(), audio_metadata(), history_read(), import_audio_file(), record_audio(), select_music(), score(), set_audio_metadata() (+5 more)

### Community 76 - "Custom3.tsx"
Cohesion: 0.39
Nodes (3): clamp, CustomFull, FullProps

### Community 77 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 78 - "test_every_mode_can_continue_through_two_exhausted_ais"
Cohesion: 0.32
Nodes (7): fake_providers(), claude(), reply(), saved_session(), test_all_modes_route_writer_editor_and_reader(), test_every_mode_can_continue_through_two_exhausted_ais(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty()

### Community 79 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 80 - "full_cues"
Cohesion: 0.17
Nodes (7): full_cues(), spoken_at(), spoken_span(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish(), test_opener_graphic()

### Community 81 - "plan_with"
Cohesion: 0.25
Nodes (6): plan_with(), ask(), test_director_character_look_is_kept_short_or_dropped(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 82 - "main"
Cohesion: 0.06
Nodes (40): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), load_channel(), new_channel(), normalize_brain() (+32 more)

### Community 85 - "finish_render"
Cohesion: 0.14
Nodes (10): full_summary(), full_formats(), opener_graphic(), drawn_answer_problem(), fix_drawn_answer(), fix_opener_graphic(), status_lines(), weak_opener_graphic() (+2 more)

### Community 89 - "choose_images"
Cohesion: 0.14
Nodes (16): choose_images(), download_picture(), recover_downloads(), apply_look_scenes(), picking, planned_short(), scene(), still() (+8 more)

### Community 90 - "write_frames"
Cohesion: 0.29
Nodes (3): flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 91 - "quality_check"
Cohesion: 0.25
Nodes (4): quality_check(), length_plan(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 92 - "test_blender_plan.py"
Cohesion: 0.10
Nodes (22): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+14 more)

### Community 95 - "full_props"
Cohesion: 0.33
Nodes (5): full_props(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_remotion_props_full()

### Community 96 - "test_story_sound_library"
Cohesion: 0.67
Nodes (3): test_story_sound_library(), fetch(), _tone_wav()

### Community 97 - "gemini_model"
Cohesion: 0.40
Nodes (4): gemini_model(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_gemini_timeout_switches_to_flash()

### Community 98 - "pacing_check"
Cohesion: 0.33
Nodes (3): callout_hold(), pacing_check(), drop_unreadable_kinetic()

### Community 99 - "render_remotion"
Cohesion: 0.22
Nodes (7): short_skin(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), test_clean_full_custom_and_skin(), test_invention_runtime_failure_uses_fallback()

### Community 101 - "rescue_graphics"
Cohesion: 0.29
Nodes (4): rescue_graphics(), max_full(), max_full_planned(), test_rescue_respects_caps()

## Knowledge Gaps
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PreflightTests` connect `PreflightTests` to `test_full_scenes.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12802275960170698 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `duration`, `test_blender_render.py`, `re`, `json`, `subprocess`, `shutil`, `local_clips`, `paint_instead`, `frame_maker`, `paint_opener_start`, `sfx_events`, `make_paper`, `visual_review`, `rewrite_paint_prompts`, `test_package.py`, `test_full_scenes.py`, `audio_library.py`, `captions`, `main`, `finish_render`, `choose_images`, `write_frames`, `speak`, `pacing_check`, `render_remotion`, `make_sfx`, `rescue_graphics`, `srt`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._
- **Why does `MetadataTests` connect `MetadataTests` to `writing.py`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13109243697478992 - nodes in this community are weakly interconnected._
- **Should `gather_pool` be split into smaller, more focused modules?**
  _Cohesion score 0.07862903225806452 - nodes in this community are weakly interconnected._