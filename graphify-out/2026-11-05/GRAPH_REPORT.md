# Graph Report - ShortsMaker  (2026-11-05)

## Corpus Check
- 140 files · ~166,625 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2235 nodes · 6176 edges · 113 communities (92 shown, 21 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 136 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `60f9b324`
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
- test_blender_render.py
- guarded.tsx
- k
- test_h3_handoff.py
- make_opener
- h3_run.py
- wm_files
- test_rules.py
- Journey.tsx
- toolkit.tsx
- gpu.py
- write_scripts
- gen.py
- core.mjs
- extra_sources.py
- make
- makeKit
- drawn_thumbnail
- local_clips
- frame_maker
- captions
- sfx_events
- look.py
- parts.py
- OpeningRulesTests
- owner
- templates.py
- use
- resume_runs
- full/types.ts
- main
- Paper
- lint_custom_code
- build_scene.py
- Short.tsx
- textures.mjs
- full_cues
- test_topic_ideas.py
- invent_component
- Halftone.tsx
- trim_borders
- trend_research
- fake_ai
- test_story.py
- pick_channel
- fetch
- kit.mjs
- RetentionTests
- json
- render
- ReliabilityTests
- clean_look
- run_agy
- bean.mjs
- picture_pool.py
- main
- brand_images
- download_audio_choices
- first_sentence
- dexter.mjs
- kit_parts.mjs
- test_first_second.py
- apply_review_fixes
- re
- align_words
- ask_ai
- pathlib
- audio_library.py
- Custom3.tsx
- speak
- ffmpeg
- edit_plan
- full_props
- style_library
- edit_scripts
- MediaTests
- MetadataTests
- paint_opener_start
- PreflightTests
- MarkTests
- StoryPacingTests
- choose_images
- fact_check
- short
- test_blender_plan.py
- FeedbackTests
- get_image
- review
- test_story_sound_library
- settings
- cold_read
- fix_short
- on_topic
- gather_pool
- BlenderFailed
- limit_style
- invent_styles
- test_every_mode_can_continue_through_two_exhausted_ais
- check_twists
- srt
- lint
- prune_cache
- limit_full
- build

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 64 edges
3. `write_scripts()` - 54 edges
4. `ask_ai()` - 49 edges
5. `MediaTests` - 33 edges
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

## Communities (113 total, 21 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.15
Nodes (23): catalog_entries(), catalog_pool(), clean_pics(), save_pool(), entry(), film(), pic_short(), pool_of() (+15 more)

### Community 3 - "prepare_topic"
Cohesion: 0.13
Nodes (11): catalog_text(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures(), prepare_topic(), usable() (+3 more)

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "render_remotion"
Cohesion: 0.12
Nodes (11): ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), test_ink_silhouette() (+3 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.12
Nodes (16): clean_tsx_code(), code_custom_scenes(), custom_rules(), is_payoff(), look_and_fix(), opener_preflight(), preview_custom(), preview_sheet() (+8 more)

### Community 8 - "test_blender_render.py"
Cohesion: 0.16
Nodes (16): code_version(), peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws() (+8 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.13
Nodes (18): Box, boxAt(), clamp, Connect(), fitCard(), hits(), layoutColumn(), layoutGrid() (+10 more)

### Community 10 - "k"
Cohesion: 0.07
Nodes (3): k, ellPts(), popS()

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "make_opener"
Cohesion: 0.13
Nodes (8): available(), make_opener(), missing_parts(), node_run(), sheet_times(), write(), look(), test_kit_animals_must_be_used()

### Community 13 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 14 - "wm_files"
Cohesion: 0.17
Nodes (7): commons_films(), article_images(), commons_search(), thumb_url(), usable_license(), wm_files(), wm_get()

### Community 15 - "test_rules.py"
Cohesion: 0.06
Nodes (44): rewrite_paint_prompts(), load_rules(), min_real_pictures(), parse_rules(), plan_gap_paintings(), ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting() (+36 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.21
Nodes (21): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+13 more)

### Community 18 - "gpu.py"
Cohesion: 0.07
Nodes (19): align(), main(), studio_speak(), fingerprint(), comfy_call(), moss_graph(), moss_images(), voicestudio_unload() (+11 more)

### Community 19 - "write_scripts"
Cohesion: 0.14
Nodes (21): write_scripts(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare() (+13 more)

### Community 20 - "gen.py"
Cohesion: 0.22
Nodes (5): images(), main(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "extra_sources.py"
Cohesion: 0.36
Nodes (8): candidate(), collection_images(), europeana_images(), loc_images(), smithsonian_images(), source_json(), wellcome_images(), optional_key()

### Community 23 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "drawn_thumbnail"
Cohesion: 0.21
Nodes (9): thumbnail_order(), drawn_thumbnail(), test_thumbnail_order_skips_film_and_puts_openers_first(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 26 - "local_clips"
Cohesion: 0.10
Nodes (13): cosy_instruct(), cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt() (+5 more)

### Community 27 - "frame_maker"
Cohesion: 0.08
Nodes (12): ClipReader, draw_card(), draw_graphic(), flash_alpha(), frame_maker(), frame(), graphic_overlay(), shot() (+4 more)

### Community 28 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 29 - "sfx_events"
Cohesion: 0.15
Nodes (8): schedule_sounds(), sfx_events(), full_pictures(), _board(), test_board_pictures_attached(), test_sfx_full(), test_story_sound_wins_its_moment(), test_style_sounds()

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

### Community 35 - "use"
Cohesion: 0.33
Nodes (4): fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 36 - "resume_runs"
Cohesion: 0.25
Nodes (11): begin(), context(), pack(), pending(), pending_topics(), read(), unpack(), update() (+3 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (22): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+14 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "lint_custom_code"
Cohesion: 0.29
Nodes (5): fallback_custom_tsx(), lint_custom_code(), test_custom_code_cannot_load_code_or_use_network(), test_fallback_custom_is_clean(), test_lint_custom_code()

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.13
Nodes (19): Captions(), PersonCard(), Root(), Background(), flashAlpha(), GraphicFor(), Move, Scene (+11 more)

### Community 43 - "textures.mjs"
Cohesion: 0.22
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "full_cues"
Cohesion: 0.14
Nodes (10): scene_cues(), full_cues(), spoken_at(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish(), test_graphic_card_hold_duration() (+2 more)

### Community 45 - "test_topic_ideas.py"
Cohesion: 0.14
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 46 - "invent_component"
Cohesion: 0.13
Nodes (15): invent_component(), attempt(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile() (+7 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "trim_borders"
Cohesion: 0.20
Nodes (5): is_stereo(), trim_borders(), border(), plain(), vertical_image()

### Community 49 - "trend_research"
Cohesion: 0.29
Nodes (4): channel_url(), seed_ideas(), trend_research(), yt_list()

### Community 50 - "fake_ai"
Cohesion: 0.12
Nodes (11): entry_age(), logbook_results(), apply_metadata(), clean_tags(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai() (+3 more)

### Community 51 - "test_story.py"
Cohesion: 0.25
Nodes (9): story_problems(), read(), test_cold_read_verdicts(), test_first_sentence_reads_across_the_cut(), test_no_hook_setting_no_hook_check(), test_rules_accept_opener_setting(), test_story_problems(), test_story_problems_flags_summary_hook() (+1 more)

### Community 52 - "pick_channel"
Cohesion: 0.17
Nodes (7): new_channel(), pick_channel(), save_channel(), use_channel(), draft_rules(), require_rules(), test_new_channel_stops_for_review()

### Community 53 - "fetch"
Cohesion: 0.22
Nodes (7): nasa_films(), nasa_credit(), nasa_images(), nasa_search(), fetch(), search_suggestions(), test_nasa_partner_media_is_credited()

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "json"
Cohesion: 0.16
Nodes (12): recover_downloads(), analyze(), edit_metrics(), load_metrics(), metrics_text(), normalize_metrics(), normalize_reply(), observations() (+4 more)

### Community 57 - "render"
Cohesion: 0.07
Nodes (17): make_sfx(), short_credit(), graphics_count(), wants_remotion(), callout_hold(), drawn_answer_problem(), pacing_check(), status_lines() (+9 more)

### Community 59 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "picture_pool.py"
Cohesion: 0.07
Nodes (15): crop_film_bytes(), crop_filter(), film_frames(), film_piece(), shot_moments(), fills_frame(), fit_font(), graphic_low() (+7 more)

### Community 63 - "main"
Cohesion: 0.15
Nodes (12): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), normalize_brain(), main(), command() (+4 more)

### Community 64 - "brand_images"
Cohesion: 0.21
Nodes (5): brand_films(), brand_images(), brand_page(), BrandImages, source_status()

### Community 65 - "download_audio_choices"
Cohesion: 0.25
Nodes (5): freesound_fetch(), freesound_preview(), freesound_results(), download_audio_choices(), seed_audio_library()

### Community 66 - "first_sentence"
Cohesion: 0.20
Nodes (8): sentence_groups(), log_short(), ends_sentence(), first_sentence(), test_sentence_ends_include_curly_quotes_and_ellipsis(), scenes(), test_logbook_hook_line_is_the_whole_first_sentence(), test_sentences_running_across_cuts_are_one_take()

### Community 69 - "test_first_second.py"
Cohesion: 0.08
Nodes (26): clock(), first_second_check(), overlay_notes(), quality_check(), review_fixes(), review_status(), swap_pictures(), visual_review() (+18 more)

### Community 70 - "apply_review_fixes"
Cohesion: 0.09
Nodes (13): use_picture_from(), full_formats(), opener_graphic(), apply_review_fixes(), fix_drawn_answer(), paint_new(), pool_pictures(), storyboard() (+5 more)

### Community 71 - "re"
Cohesion: 0.04
Nodes (44): clean_sound(), limit_sounds(), music_gain(), short_skin(), clean_code(), vault_page(), vault_refresh(), rescue_graphics() (+36 more)

### Community 72 - "align_words"
Cohesion: 0.15
Nodes (10): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), test_caption_word_counts_match_the_scene_splitter(), test_caption_words_keep_what_is_written(), test_dollar_scale_word_order() (+2 more)

### Community 73 - "ask_ai"
Cohesion: 0.12
Nodes (14): ask_ai(), gemini_model(), test_every_ai_gets_the_pipeline_preamble_once(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash() (+6 more)

### Community 75 - "audio_library.py"
Cohesion: 0.21
Nodes (18): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+10 more)

### Community 76 - "Custom3.tsx"
Cohesion: 0.39
Nodes (3): clamp, CustomFull, FullProps

### Community 78 - "ffmpeg"
Cohesion: 0.12
Nodes (13): save_context(), shot_span(), split_takes(), spoken_count(), duration(), ffmpeg(), video_encoder(), write_json() (+5 more)

### Community 79 - "edit_plan"
Cohesion: 0.17
Nodes (6): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 80 - "full_props"
Cohesion: 0.33
Nodes (5): full_props(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_remotion_props_full()

### Community 81 - "style_library"
Cohesion: 0.15
Nodes (13): approve_candidate(), style_library(), style_rules(), write_style_index(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library() (+5 more)

### Community 82 - "edit_scripts"
Cohesion: 0.18
Nodes (7): other_ai(), edit_scripts(), narration_lines(), test_gemini_modes_choose_codex_and_keep_editor_choice(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules(), test_failed_second_read_clears_old_verdict()

### Community 85 - "paint_opener_start"
Cohesion: 0.09
Nodes (10): gemini_images(), full_summary(), to_vertical(), paint_instead(), fix_opener_graphic(), paint_opener_start(), weak_opener_graphic(), test_full_summary() (+2 more)

### Community 89 - "choose_images"
Cohesion: 0.19
Nodes (14): choose_images(), apply_look_scenes(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+6 more)

### Community 90 - "fact_check"
Cohesion: 0.18
Nodes (8): fact_check(), test_fact_check_drops_full(), plan_with(), ask(), test_director_character_look_is_kept_short_or_dropped(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 91 - "short"
Cohesion: 0.22
Nodes (7): fake_ai(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused(), test_no_verdict_is_not_a_pass(), test_reveal_scene_is_drawn_with_its_own_rules(), test_use_opener_plays_the_drawn_opener()

### Community 92 - "test_blender_plan.py"
Cohesion: 0.12
Nodes (20): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), plan() (+12 more)

### Community 94 - "get_image"
Cohesion: 0.25
Nodes (4): get_image(), openverse_images(), ov_get(), download_picture()

### Community 96 - "test_story_sound_library"
Cohesion: 0.67
Nodes (3): test_story_sound_library(), fetch(), _tone_wav()

### Community 97 - "settings"
Cohesion: 0.22
Nodes (7): archive_ad_films(), archive_films(), commercial_queries(), duke_films(), settings(), source_enabled(), print_source_status()

### Community 98 - "cold_read"
Cohesion: 0.22
Nodes (6): cold_read(), recheck_final_scripts(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 99 - "fix_short"
Cohesion: 0.25
Nodes (7): load_channel(), fix_short(), load_state(), prune_work(), test_fix_bat_explains_a_drawn_short(), test_state_roundtrip_full_pics(), test_fix_checks_rules_before_asking_for_a_scene()

### Community 100 - "on_topic"
Cohesion: 0.25
Nodes (5): pixabay_images(), pixabay_films(), on_topic(), test_on_topic_ignores_a_lone_shared_name(), test_pixabay_keeps_only_on_topic_videos()

### Community 101 - "gather_pool"
Cohesion: 0.25
Nodes (3): archive_images(), balanced_candidates(), gather_pool()

### Community 104 - "invent_styles"
Cohesion: 0.25
Nodes (5): invent_styles(), reject_candidate(), swap_inventions(), test_reject_deletes(), test_swap_inventions()

### Community 105 - "test_every_mode_can_continue_through_two_exhausted_ais"
Cohesion: 0.32
Nodes (7): fake_providers(), claude(), reply(), saved_session(), test_all_modes_route_writer_editor_and_reader(), test_every_mode_can_continue_through_two_exhausted_ais(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty()

### Community 106 - "check_twists"
Cohesion: 0.47
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 112 - "build"
Cohesion: 0.67
Nodes (3): build(), add(), main()

## Knowledge Gaps
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `render_remotion`, `test_blender_render.py`, `test_rules.py`, `gpu.py`, `local_clips`, `frame_maker`, `captions`, `sfx_events`, `resume_runs`, `full_cues`, `picture_pool.py`, `main`, `test_first_second.py`, `apply_review_fixes`, `re`, `pathlib`, `audio_library.py`, `speak`, `ffmpeg`, `paint_opener_start`, `choose_images`, `fix_short`, `srt`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12802275960170698 - nodes in this community are weakly interconnected._
- **Why does `gather_pool()` connect `gather_pool` to `settings`, `owner`, `prepare_topic`, `test_first_second.py`, `re`, `wm_files`, `gpu.py`, `fetch`, `extra_sources.py`, `get_image`, `choose_images`, `picture_pool.py`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `test_pictures_first.py`, `prepare_topic`, `code_custom_scenes`, `test_rules.py`, `gpu.py`, `owner`, `resume_runs`, `test_topic_ideas.py`, `trend_research`, `fake_ai`, `test_story.py`, `pick_channel`, `json`, `clean_look`, `main`, `test_first_second.py`, `re`, `ask_ai`, `pathlib`, `edit_scripts`, `fact_check`, `test_blender_plan.py`, `cold_read`, `limit_style`, `check_twists`, `limit_full`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14919354838709678 - nodes in this community are weakly interconnected._
- **Should `prepare_topic` be split into smaller, more focused modules?**
  _Cohesion score 0.13450292397660818 - nodes in this community are weakly interconnected._