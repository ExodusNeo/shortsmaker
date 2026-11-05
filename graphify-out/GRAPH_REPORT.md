# Graph Report - ShortsMaker  (2026-11-05)

## Corpus Check
- 140 files · ~166,489 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2229 nodes · 6152 edges · 107 communities (90 shown, 17 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 135 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `417f5b60`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- prepare_topic
- test_blender_scene.py
- split_make_shorts.py
- render_style.py
- json
- test_blender_render.py
- guarded.tsx
- k
- test_h3_handoff.py
- drawn_opener.py
- h3_run.py
- gather_pool
- test_rules.py
- Journey.tsx
- toolkit.tsx
- test_full_scenes.py
- write_scripts
- Local GPU Worker
- core.mjs
- local_clips
- make
- makeKit
- drawn_thumbnail
- paint_instead
- frame_maker
- apply_review_fixes
- blender_plan.py
- look.py
- parts.py
- OpeningRulesTests
- owner
- templates.py
- use
- cold_read
- full/types.ts
- main
- Paper
- check_twists
- build_scene.py
- Short.tsx
- textures.mjs
- full_cues
- re
- render_remotion
- Halftone.tsx
- clean_photo
- pick_channel
- logbook_results
- test_story.py
- words_of
- fetch
- kit.mjs
- RetentionTests
- retention.py
- render
- ReliabilityTests
- test_style.py
- run_agy
- bean.mjs
- local_voice
- write_json
- extra_sources.py
- download_audio_choices
- visual_review
- dexter.mjs
- kit_parts.mjs
- test_first_second.py
- rewrite_paint_prompts
- clean_full
- qwen_voice.py
- ask_ai
- pathlib
- audio_library.py
- Custom3.tsx
- music_gain
- duration
- edit_plan
- edit_scripts
- article_text
- main
- MediaTests
- MetadataTests
- finish_render
- PreflightTests
- MarkTests
- StoryPacingTests
- choose_images
- .render_fixture
- quality_check
- test_blender_plan.py
- FeedbackTests
- get_image
- seo_pass
- test_story_sound_library
- gemini_model
- pacing_check
- fix_short
- test_every_mode_can_continue_through_two_exhausted_ais
- rescue_graphics
- BlenderFailed
- limit_style
- finish_short
- make_sfx
- limit_full

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 64 edges
3. `write_scripts()` - 54 edges
4. `ask_ai()` - 48 edges
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
- `test_pixabay_keeps_only_on_topic_videos()` --calls--> `pixabay_films()`  [EXTRACTED]
  tests/test_pictures_first.py → shortsmaker/footage.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`
- 3-file cycle: `shortsmaker/motion.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`
- 4-file cycle: `shortsmaker/motion.py -> shortsmaker/opening_rules.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`

## Communities (107 total, 17 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.14
Nodes (24): catalog_entries(), catalog_pool(), clean_pics(), entry(), fake_ai, film(), pic_short(), pool_of() (+16 more)

### Community 3 - "prepare_topic"
Cohesion: 0.12
Nodes (13): catalog_text(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures(), prepare_topic() (+5 more)

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "render_style.py"
Cohesion: 0.50
Nodes (3): build(), add(), main()

### Community 7 - "json"
Cohesion: 0.06
Nodes (31): code_version(), pixabay_films(), comfy_call(), moss_images(), clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx() (+23 more)

### Community 8 - "test_blender_render.py"
Cohesion: 0.22
Nodes (12): peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises(), test_frames_are_trimmed_after_the_clips_are_cut() (+4 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.13
Nodes (18): Box, boxAt(), clamp, Connect(), fitCard(), hits(), layoutColumn(), layoutGrid() (+10 more)

### Community 10 - "k"
Cohesion: 0.07
Nodes (3): k, ellPts(), popS()

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "drawn_opener.py"
Cohesion: 0.10
Nodes (14): available(), clean_code(), fingerprint(), lint(), make_opener(), missing_parts(), node_run(), review() (+6 more)

### Community 13 - "h3_run.py"
Cohesion: 0.10
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 14 - "gather_pool"
Cohesion: 0.12
Nodes (9): commons_films(), article_images(), commons_search(), thumb_url(), usable_license(), wm_files(), wm_get(), balanced_candidates() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (39): draft_rules(), load_rules(), min_real_pictures(), parse_rules(), require_rules(), capture_prompts(), ask(), draft_reply() (+31 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.21
Nodes (21): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+13 more)

### Community 18 - "test_full_scenes.py"
Cohesion: 0.10
Nodes (10): hex_rgb(), luminance(), moss_graph(), make_paper(), load_state(), library_menu(), reject_candidate(), test_make_paper() (+2 more)

### Community 19 - "write_scripts"
Cohesion: 0.12
Nodes (23): write_scripts(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare() (+15 more)

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

### Community 25 - "drawn_thumbnail"
Cohesion: 0.23
Nodes (9): scene_frames(), drawn_thumbnail(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 26 - "paint_instead"
Cohesion: 0.12
Nodes (6): gemini_images(), to_vertical(), ink_silhouette(), paint_instead(), test_ink_silhouette(), test_remotion_failure_paints()

### Community 27 - "frame_maker"
Cohesion: 0.06
Nodes (16): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+8 more)

### Community 28 - "apply_review_fixes"
Cohesion: 0.13
Nodes (10): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full() (+2 more)

### Community 29 - "blender_plan.py"
Cohesion: 0.12
Nodes (8): clamp(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order(), test_thumbnail_order_skips_film_and_puts_openers_first()

### Community 30 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 33 - "owner"
Cohesion: 0.14
Nodes (7): owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits(), test_good_look_check_skips_the_extra_compile()

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "use"
Cohesion: 0.33
Nodes (4): fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 36 - "cold_read"
Cohesion: 0.20
Nodes (6): other_ai(), cold_read(), recheck_final_scripts(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (22): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+14 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "check_twists"
Cohesion: 0.47
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

### Community 44 - "full_cues"
Cohesion: 0.07
Nodes (19): schedule_sounds(), sfx_events(), full_props(), full_pictures(), full_cues(), spoken_at(), spoken_span(), _board() (+11 more)

### Community 45 - "re"
Cohesion: 0.05
Nodes (28): main(), commercial_queries(), crop_film_bytes(), crop_filter(), film_frames(), film_piece(), shot_moments(), voicestudio_up() (+20 more)

### Community 46 - "render_remotion"
Cohesion: 0.05
Nodes (32): ass_time(), caption_lines(), captions(), styled(), ass_colour(), short_skin(), render_remotion(), remotion() (+24 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "clean_photo"
Cohesion: 0.12
Nodes (8): clean_photo(), is_stereo(), trim_borders(), border(), plain(), vertical_image(), visual_unique(), mark_details()

### Community 49 - "pick_channel"
Cohesion: 0.14
Nodes (9): channel_url(), new_channel(), pick_channel(), save_channel(), seed_ideas(), trend_research(), use_channel(), yt_list() (+1 more)

### Community 50 - "logbook_results"
Cohesion: 0.33
Nodes (3): entry_age(), logbook_results(), test_logbook_marks_tiny_samples()

### Community 51 - "test_story.py"
Cohesion: 0.13
Nodes (17): sentence_groups(), log_short(), first_sentence(), story_problems(), read(), scenes(), test_a_take_is_cut_between_the_scenes_words(), test_cold_read_verdicts() (+9 more)

### Community 52 - "words_of"
Cohesion: 0.15
Nodes (10): clean_sound(), limit_sounds(), graphic_low(), fill_money_graphics(), is_person_portrait(), shows_person(), words_of(), test_clean_sound() (+2 more)

### Community 53 - "fetch"
Cohesion: 0.16
Nodes (10): archive_ad_films(), archive_films(), duke_films(), nasa_films(), archive_images(), nasa_images(), nasa_search(), on_topic() (+2 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "retention.py"
Cohesion: 0.20
Nodes (11): analyze(), edit_metrics(), load_metrics(), metrics_text(), normalize_metrics(), normalize_reply(), observations(), parse_metric() (+3 more)

### Community 57 - "render"
Cohesion: 0.08
Nodes (16): short_credit(), ffmpeg(), video_encoder(), graphics_count(), wants_remotion(), apply(), preview(), srt() (+8 more)

### Community 59 - "test_style.py"
Cohesion: 0.08
Nodes (22): clean_invention(), clean_look(), clean_transition(), settle_style(), approve_candidate(), save_candidate(), style_library(), write_style_index() (+14 more)

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "local_voice"
Cohesion: 0.20
Nodes (6): cosy_instruct(), local_voice(), split_takes(), spoken_count(), voicestudio_unload(), is_loop_short()

### Community 63 - "write_json"
Cohesion: 0.20
Nodes (12): begin(), context(), pack(), pending(), pending_topics(), read(), save_context(), unpack() (+4 more)

### Community 64 - "extra_sources.py"
Cohesion: 0.16
Nodes (17): brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images(), loc_images() (+9 more)

### Community 65 - "download_audio_choices"
Cohesion: 0.25
Nodes (5): freesound_fetch(), freesound_preview(), freesound_results(), download_audio_choices(), seed_audio_library()

### Community 66 - "visual_review"
Cohesion: 0.24
Nodes (7): clock(), overlay_notes(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 69 - "test_first_second.py"
Cohesion: 0.16
Nodes (15): first_second_check(), review_status(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing() (+7 more)

### Community 70 - "rewrite_paint_prompts"
Cohesion: 0.14
Nodes (7): rewrite_paint_prompts(), plan_gap_paintings(), ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts(), test_scene_without_picture_or_prompt_gets_painted_not_reused()

### Community 71 - "clean_full"
Cohesion: 0.12
Nodes (16): clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number() (+8 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.14
Nodes (12): align(), align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak(), test_caption_word_counts_match_the_scene_splitter() (+4 more)

### Community 73 - "ask_ai"
Cohesion: 0.12
Nodes (14): scene_cues(), ask_ai(), test_counter_finishes_before_it_leaves(), test_quota_fallback_both_ways(), test_claude_pinned_to_opus_high(), test_fake_reaches_callers(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash(), test_graphic_card_hold_duration() (+6 more)

### Community 75 - "audio_library.py"
Cohesion: 0.21
Nodes (18): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+10 more)

### Community 76 - "Custom3.tsx"
Cohesion: 0.39
Nodes (3): clamp, CustomFull, FullProps

### Community 77 - "music_gain"
Cohesion: 0.22
Nodes (4): music_gain(), speak(), tts(), test_music_gain_evens_out_tracks()

### Community 78 - "duration"
Cohesion: 0.16
Nodes (8): shot_span(), duration(), fake_ai(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused(), test_reveal_scene_is_drawn_with_its_own_rules(), test_use_opener_plays_the_drawn_opener()

### Community 79 - "edit_plan"
Cohesion: 0.17
Nodes (6): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 80 - "edit_scripts"
Cohesion: 0.20
Nodes (6): edit_scripts(), length_plan(), narration_lines(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules(), test_failed_second_read_clears_old_verdict()

### Community 81 - "article_text"
Cohesion: 0.15
Nodes (9): article_text(), fact_check(), test_fact_check_drops_full(), plan_with(), ask(), test_director_character_look_is_kept_short_or_dropped(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library() (+1 more)

### Community 82 - "main"
Cohesion: 0.13
Nodes (13): ask_brain(), ask_count(), ask_number(), ask_yes(), normalize_brain(), main(), prune_cache(), command() (+5 more)

### Community 85 - "finish_render"
Cohesion: 0.12
Nodes (11): full_summary(), opener_graphic(), drawn_answer_problem(), fix_drawn_answer(), fix_opener_graphic(), status_lines(), weak_opener_graphic(), finish_render() (+3 more)

### Community 89 - "choose_images"
Cohesion: 0.19
Nodes (14): choose_images(), apply_look_scenes(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+6 more)

### Community 91 - "quality_check"
Cohesion: 0.33
Nodes (3): quality_check(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 92 - "test_blender_plan.py"
Cohesion: 0.25
Nodes (14): clean_build(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults(), test_clean_build_keeps_a_good_plan(), test_default_build_shape(), test_label_is_short_and_upper(), test_nan_and_infinity_get_defaults() (+6 more)

### Community 94 - "get_image"
Cohesion: 0.20
Nodes (5): get_image(), openverse_images(), ov_get(), download_picture(), recover_downloads()

### Community 95 - "seo_pass"
Cohesion: 0.22
Nodes (6): load_channel(), apply_metadata(), clean_tags(), seo_pass(), test_seo_examples_come_from_the_channel(), test_seo_never_sees_competitor_titles()

### Community 96 - "test_story_sound_library"
Cohesion: 0.67
Nodes (3): test_story_sound_library(), fetch(), _tone_wav()

### Community 97 - "gemini_model"
Cohesion: 0.40
Nodes (4): gemini_model(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_gemini_timeout_switches_to_flash()

### Community 98 - "pacing_check"
Cohesion: 0.33
Nodes (3): callout_hold(), pacing_check(), drop_unreadable_kinetic()

### Community 99 - "fix_short"
Cohesion: 0.25
Nodes (6): configure_brain(), fix_short(), test_fix_bat_explains_a_drawn_short(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_gemini_modes_choose_codex_and_keep_editor_choice(), test_fix_checks_rules_before_asking_for_a_scene()

### Community 100 - "test_every_mode_can_continue_through_two_exhausted_ais"
Cohesion: 0.32
Nodes (7): fake_providers(), claude(), reply(), saved_session(), test_all_modes_route_writer_editor_and_reader(), test_every_mode_can_continue_through_two_exhausted_ais(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty()

### Community 101 - "rescue_graphics"
Cohesion: 0.40
Nodes (3): full_formats(), rescue_graphics(), test_rescue_respects_caps()

### Community 104 - "finish_short"
Cohesion: 0.33
Nodes (3): finish_short(), vault_page(), vault_refresh()

## Knowledge Gaps
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MetadataTests` connect `MetadataTests` to `pathlib`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12802275960170698 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `json`, `test_blender_render.py`, `test_full_scenes.py`, `local_clips`, `drawn_thumbnail`, `paint_instead`, `frame_maker`, `full_cues`, `render_remotion`, `clean_photo`, `words_of`, `test_style.py`, `local_voice`, `write_json`, `visual_review`, `rewrite_paint_prompts`, `ask_ai`, `pathlib`, `audio_library.py`, `music_gain`, `duration`, `main`, `finish_render`, `choose_images`, `pacing_check`, `fix_short`, `rescue_graphics`, `make_sfx`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `test_pictures_first.py`, `prepare_topic`, `json`, `test_rules.py`, `blender_plan.py`, `owner`, `cold_read`, `check_twists`, `re`, `pick_channel`, `logbook_results`, `test_story.py`, `words_of`, `retention.py`, `test_style.py`, `write_json`, `clean_full`, `ask_ai`, `pathlib`, `edit_scripts`, `article_text`, `main`, `limit_style`, `limit_full`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14015151515151514 - nodes in this community are weakly interconnected._
- **Should `prepare_topic` be split into smaller, more focused modules?**
  _Cohesion score 0.11857707509881422 - nodes in this community are weakly interconnected._