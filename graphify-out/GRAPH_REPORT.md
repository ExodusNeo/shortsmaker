# Graph Report - ShortsMaker  (2026-11-05)

## Corpus Check
- 140 files · ~167,757 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2247 nodes · 6201 edges · 105 communities (87 shown, 18 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 138 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a0bdb7c2`
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
- subprocess
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
- planning
- gen.py
- core.mjs
- extra_sources.py
- make
- makeKit
- image_sources.py
- local_clips
- frame_maker
- opener_graphic
- full_cues
- look.py
- parts.py
- OpeningRulesTests
- gather_pool
- templates.py
- paint_opener_start
- resume_runs
- BigNumber.tsx
- main
- Paper
- ask
- build_scene.py
- Short.tsx
- textures.mjs
- scene_cues
- re
- invent_component
- Halftone.tsx
- clean_photo
- trend_research
- fake_ai
- story_problems
- pick_channel
- make_paper
- kit.mjs
- RetentionTests
- retention.py
- render
- ReliabilityTests
- style_library
- run_agy
- bean.mjs
- footage.py
- main
- rewrite_paint_prompts
- media_command
- log_short
- dexter.mjs
- kit_parts.mjs
- test_first_second.py
- apply_review_fixes
- write_scripts
- qwen_voice.py
- ask_ai
- test_full_scenes.py
- audio_library.py
- ref_remotion
- music_gain
- ffmpeg
- edit_plan
- quality_check
- approve_candidate
- edit_scripts
- MediaTests
- MetadataTests
- paint_instead
- PreflightTests
- MarkTests
- StoryPacingTests
- choose_images
- plan_with
- test_drawn_opener.py
- test_blender_plan.py
- FeedbackTests
- pack
- .render_fixture
- test_story_sound_library
- missing_parts
- cold_read
- fix_short
- test_short_credit
- limit_style
- saved_session
- test_story.py
- lint

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

## Communities (105 total, 18 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.15
Nodes (24): catalog_entries(), catalog_pool(), save_pool(), entry(), film(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+16 more)

### Community 3 - "prepare_topic"
Cohesion: 0.10
Nodes (13): catalog_text(), clean_pics(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures() (+5 more)

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "render_remotion"
Cohesion: 0.15
Nodes (10): render_remotion(), remotion(), render(), run_remotion_with_fallback(), invent_styles(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback() (+2 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.10
Nodes (20): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), is_payoff(), lint_custom_code(), look_and_fix(), opener_preflight() (+12 more)

### Community 8 - "subprocess"
Cohesion: 0.11
Nodes (5): fills_frame(), import_media(), storyboard(), main(), props_for()

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
Cohesion: 0.15
Nodes (7): available(), make_opener(), node_run(), review(), sheet_times(), write(), look()

### Community 13 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 14 - "finish_render"
Cohesion: 0.11
Nodes (13): clock(), drawn_answer_problem(), overlay_notes(), pacing_check(), review_fixes(), sound_masking(), status_lines(), visual_review() (+5 more)

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (38): load_rules(), min_real_pictures(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft() (+30 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.26
Nodes (20): CustomScene(), ExampleOpenerAction(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear() (+12 more)

### Community 18 - "json"
Cohesion: 0.08
Nodes (18): main(), code_version(), fingerprint(), pixabay_films(), comfy_call(), moss_graph(), moss_images(), voicestudio_unload() (+10 more)

### Community 19 - "planning"
Cohesion: 0.13
Nodes (20): passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), reply() (+12 more)

### Community 20 - "gen.py"
Cohesion: 0.22
Nodes (5): images(), main(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "extra_sources.py"
Cohesion: 0.06
Nodes (36): brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images(), loc_images() (+28 more)

### Community 23 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 26 - "local_clips"
Cohesion: 0.11
Nodes (12): cosy_instruct(), cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt() (+4 more)

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (15): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+7 more)

### Community 28 - "opener_graphic"
Cohesion: 0.12
Nodes (11): full_summary(), full_formats(), opener_graphic(), rescue_graphics(), fix_drawn_answer(), fix_opener_graphic(), article_text(), fact_check() (+3 more)

### Community 29 - "full_cues"
Cohesion: 0.07
Nodes (18): schedule_sounds(), sfx_events(), full_props(), full_cues(), spoken_at(), spoken_span(), _board(), _jpg() (+10 more)

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

### Community 35 - "paint_opener_start"
Cohesion: 0.13
Nodes (7): gemini_images(), paint_opener_start(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), test_weak_opener_graphic_fixes_then_handoff(), use()

### Community 36 - "resume_runs"
Cohesion: 0.32
Nodes (9): begin(), context(), pending(), pending_topics(), read(), update(), finish_short(), record_failure() (+1 more)

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
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "textures.mjs"
Cohesion: 0.22
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "scene_cues"
Cohesion: 0.18
Nodes (9): scene_cues(), read_need(), callout_hold(), drop_unreadable_kinetic(), test_counter_finishes_before_it_leaves(), test_short_scene_callout_is_placed_so_the_check_passes(), test_graphic_card_hold_duration(), test_person_card_hold_and_exit_gap() (+1 more)

### Community 45 - "re"
Cohesion: 0.06
Nodes (19): clean_code(), parse_scene_money(), max_full(), max_full_planned(), apply_metadata(), clean_tags(), clean_title(), clean_style_code() (+11 more)

### Community 46 - "invent_component"
Cohesion: 0.13
Nodes (15): invent_component(), attempt(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile() (+7 more)

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
Cohesion: 0.15
Nodes (9): entry_age(), logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel() (+1 more)

### Community 51 - "story_problems"
Cohesion: 0.08
Nodes (23): ass_time(), caption_lines(), captions(), styled(), ass_colour(), sentence_groups(), ends_sentence(), first_sentence() (+15 more)

### Community 52 - "pick_channel"
Cohesion: 0.22
Nodes (5): pick_channel(), use_channel(), draft_rules(), require_rules(), test_new_channel_stops_for_review()

### Community 53 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "retention.py"
Cohesion: 0.20
Nodes (11): analyze(), edit_metrics(), load_metrics(), metrics_text(), normalize_metrics(), normalize_reply(), observations(), parse_metric() (+3 more)

### Community 57 - "render"
Cohesion: 0.10
Nodes (11): make_sfx(), short_credit(), graphics_count(), is_loop_short(), wants_remotion(), drawn_choices(), drawn_payoff(), render() (+3 more)

### Community 59 - "style_library"
Cohesion: 0.13
Nodes (12): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), test_invented_look_needs_fallback() (+4 more)

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "footage.py"
Cohesion: 0.13
Nodes (9): commons_films(), crop_film_bytes(), crop_filter(), film_frames(), film_piece(), shot_moments(), shot_span(), film_ffmpeg() (+1 more)

### Community 63 - "main"
Cohesion: 0.16
Nodes (11): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), normalize_brain(), main(), command() (+3 more)

### Community 64 - "rewrite_paint_prompts"
Cohesion: 0.25
Nodes (4): rewrite_paint_prompts(), plan_gap_paintings(), test_rewrite_paint_prompts(), test_scene_without_picture_or_prompt_gets_painted_not_reused()

### Community 65 - "media_command"
Cohesion: 0.22
Nodes (8): freesound_fetch(), freesound_preview(), freesound_results(), audition_audio(), download_audio_choices(), media_command(), review_audio_files(), seed_audio_library()

### Community 66 - "log_short"
Cohesion: 0.25
Nodes (4): log_short(), vault_page(), vault_refresh(), test_logbook_hook_line_is_the_whole_first_sentence()

### Community 69 - "test_first_second.py"
Cohesion: 0.16
Nodes (15): first_second_check(), review_status(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing() (+7 more)

### Community 70 - "apply_review_fixes"
Cohesion: 0.18
Nodes (7): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 71 - "write_scripts"
Cohesion: 0.07
Nodes (29): clean_sound(), limit_sounds(), graphic_low(), clean_full(), word(), clean_graphic(), contains(), coords() (+21 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.12
Nodes (14): align(), align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak(), spoken_count() (+6 more)

### Community 73 - "ask_ai"
Cohesion: 0.12
Nodes (14): ask_ai(), gemini_model(), test_every_ai_gets_the_pipeline_preamble_once(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash() (+6 more)

### Community 74 - "test_full_scenes.py"
Cohesion: 0.10
Nodes (4): hex_rgb(), luminance(), short_skin(), test_clean_full_custom_and_skin()

### Community 75 - "audio_library.py"
Cohesion: 0.24
Nodes (15): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+7 more)

### Community 77 - "music_gain"
Cohesion: 0.22
Nodes (4): music_gain(), speak(), tts(), test_music_gain_evens_out_tracks()

### Community 78 - "ffmpeg"
Cohesion: 0.17
Nodes (10): split_takes(), duration(), ffmpeg(), video_encoder(), write_json(), apply(), preview(), save_state() (+2 more)

### Community 79 - "edit_plan"
Cohesion: 0.14
Nodes (7): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 80 - "quality_check"
Cohesion: 0.33
Nodes (3): quality_check(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 81 - "approve_candidate"
Cohesion: 0.19
Nodes (10): approve_candidate(), library_menu(), reject_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure() (+2 more)

### Community 82 - "edit_scripts"
Cohesion: 0.15
Nodes (9): edit_scripts(), length_plan(), narration_lines(), test_all_modes_route_writer_editor_and_reader(), ask(), test_only_the_second_edit_pass_gets_the_research(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules() (+1 more)

### Community 85 - "paint_instead"
Cohesion: 0.25
Nodes (3): to_vertical(), paint_instead(), test_remotion_failure_paints()

### Community 89 - "choose_images"
Cohesion: 0.15
Nodes (16): choose_images(), download_picture(), recover_downloads(), apply_look_scenes(), picking, planned_short(), scene(), still() (+8 more)

### Community 90 - "plan_with"
Cohesion: 0.25
Nodes (6): plan_with(), ask(), test_director_character_look_is_kept_short_or_dropped(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 91 - "test_drawn_opener.py"
Cohesion: 0.26
Nodes (7): fake_ai(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused(), test_no_verdict_is_not_a_pass(), test_reveal_scene_is_drawn_with_its_own_rules(), test_use_opener_plays_the_drawn_opener()

### Community 92 - "test_blender_plan.py"
Cohesion: 0.05
Nodes (45): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+37 more)

### Community 94 - "pack"
Cohesion: 0.50
Nodes (3): pack(), save_context(), unpack()

### Community 96 - "test_story_sound_library"
Cohesion: 0.67
Nodes (3): test_story_sound_library(), fetch(), _tone_wav()

### Community 98 - "cold_read"
Cohesion: 0.20
Nodes (7): other_ai(), cold_read(), recheck_final_scripts(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_gemini_modes_choose_codex_and_keep_editor_choice(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers()

### Community 99 - "fix_short"
Cohesion: 0.25
Nodes (7): load_channel(), fix_short(), load_state(), prune_work(), test_fix_bat_explains_a_drawn_short(), test_state_roundtrip_full_pics(), test_fix_checks_rules_before_asking_for_a_scene()

### Community 105 - "saved_session"
Cohesion: 0.47
Nodes (6): fake_providers(), claude(), reply(), saved_session(), test_every_mode_can_continue_through_two_exhausted_ais(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty()

### Community 106 - "test_story.py"
Cohesion: 0.36
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

## Knowledge Gaps
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `render_remotion`, `subprocess`, `finish_render`, `json`, `local_clips`, `frame_maker`, `opener_graphic`, `full_cues`, `paint_opener_start`, `resume_runs`, `scene_cues`, `clean_photo`, `story_problems`, `make_paper`, `main`, `rewrite_paint_prompts`, `write_scripts`, `test_full_scenes.py`, `audio_library.py`, `music_gain`, `ffmpeg`, `paint_instead`, `choose_images`, `test_blender_plan.py`, `pack`, `fix_short`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `MediaTests` connect `MediaTests` to `image_sources.py`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `prepare_topic` be split into smaller, more focused modules?**
  _Cohesion score 0.09666666666666666 - nodes in this community are weakly interconnected._
- **Why does `gather_pool()` connect `gather_pool` to `prepare_topic`, `write_scripts`, `test_full_scenes.py`, `finish_render`, `clean_photo`, `extra_sources.py`, `choose_images`, `image_sources.py`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._
- **Should `code_custom_scenes` be split into smaller, more focused modules?**
  _Cohesion score 0.10037878787878787 - nodes in this community are weakly interconnected._