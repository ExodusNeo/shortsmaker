# Graph Report - ShortsMaker  (2026-11-02)

## Corpus Check
- 140 files · ~160,927 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2183 nodes · 6030 edges · 108 communities (84 shown, 24 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 135 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `823fb0dd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- prepare_topic
- test_blender_scene.py
- split_make_shorts.py
- ffmpeg
- code_custom_scenes
- json
- guarded.tsx
- k
- test_h3_handoff.py
- check_twists
- channel_profiles.py
- render_remotion
- test_rules.py
- Journey.tsx
- toolkit.tsx
- use_picture_from
- write_scripts
- Local GPU Worker
- core.mjs
- local_clips
- make
- makeKit
- resume_runs
- render
- frame_maker
- apply_review_fixes
- h3_run.py
- math
- parts.py
- OpeningRulesTests
- owner
- templates.py
- use_opener
- test_story.py
- full/types.ts
- main
- Paper
- subprocess
- Shots
- Short.tsx
- textures.mjs
- sfx_events
- test_topic_ideas.py
- extra_sources.py
- Halftone.tsx
- clean_photo
- pick_channel
- fake_ai
- main
- test_style.py
- re
- kit.mjs
- RetentionTests
- retention.py
- make_opener
- ReliabilityTests
- gather_pool
- run_agy
- bean.mjs
- music_gain
- popS
- fetch
- edit_scripts
- visual_review
- dexter.mjs
- kit_parts.mjs
- first_second_check
- words_of
- clean_full
- qwen_voice.py
- ask_ai
- test_full_scenes.py
- audio_library.py
- Custom3.tsx
- captions
- blender_plan.py
- edit_plan
- full_cues
- test_blender_plan.py
- configure_brain
- MediaTests
- MetadataTests
- finish_render
- PreflightTests
- MarkTests
- StoryPacingTests
- choose_images
- drawn_thumbnail
- write_json
- test_blender_render.py
- FeedbackTests
- is_person_portrait
- full_props
- full_pictures
- BrandImages
- BlenderFailed
- swap_inventions
- style_props
- .render_fixture
- make_sfx
- limit_style
- spoken_count
- prune_cache
- test_short_credit
- log_short

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 61 edges
3. `write_scripts()` - 52 edges
4. `ask_ai()` - 48 edges
5. `MediaTests` - 33 edges
6. `main()` - 32 edges
7. `skinOf()` - 31 edges
8. `clamp()` - 27 edges
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
- `test_encoder_cache_lives_with_video_encoder()` --calls--> `video_encoder()`  [EXTRACTED]
  tests/test_package.py → shortsmaker/media_tools.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`
- 3-file cycle: `shortsmaker/motion.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`
- 4-file cycle: `shortsmaker/motion.py -> shortsmaker/opening_rules.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`

## Communities (108 total, 24 thin omitted)

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
Cohesion: 0.12
Nodes (12): catalog_text(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures(), prepare_topic() (+4 more)

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "ffmpeg"
Cohesion: 0.20
Nodes (7): shot_span(), split_takes(), duration(), ffmpeg(), apply(), preview(), test_a_take_is_cut_between_the_scenes_words()

### Community 7 - "code_custom_scenes"
Cohesion: 0.17
Nodes (11): clean_tsx_code(), code_custom_scenes(), custom_rules(), lint_custom_code(), look_and_fix(), opener_preflight(), preview_custom(), opening_brief() (+3 more)

### Community 8 - "json"
Cohesion: 0.11
Nodes (13): code_version(), crop_filter(), film_frames(), film_piece(), shot_moments(), comfy_call(), voicestudio_unload(), film_ffmpeg() (+5 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.13
Nodes (18): Box, boxAt(), clamp, Connect(), fitCard(), hits(), layoutColumn(), layoutGrid() (+10 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.08
Nodes (32): h3_problems(), h3_prompt(), h3_prompts(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause() (+24 more)

### Community 12 - "check_twists"
Cohesion: 0.47
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 13 - "channel_profiles.py"
Cohesion: 0.13
Nodes (9): main(), channel_url(), seed_ideas(), trend_research(), yt_list(), voicestudio_up(), build(), add() (+1 more)

### Community 14 - "render_remotion"
Cohesion: 0.22
Nodes (7): short_skin(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), test_clean_full_custom_and_skin(), test_invention_runtime_failure_uses_fallback()

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (36): load_rules(), min_real_pictures(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft() (+28 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.21
Nodes (21): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+13 more)

### Community 18 - "use_picture_from"
Cohesion: 0.33
Nodes (4): use_picture_from(), paint_new(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 19 - "write_scripts"
Cohesion: 0.12
Nodes (24): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+16 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "local_clips"
Cohesion: 0.11
Nodes (12): cosy_instruct(), cover_crop(), cut_owner_clip(), local_clips(), local_job(), local_voice(), motion_prompt(), start_picture() (+4 more)

### Community 23 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "resume_runs"
Cohesion: 0.44
Nodes (7): context(), pending(), read(), update(), finish_short(), record_failure(), resume_runs()

### Community 26 - "render"
Cohesion: 0.06
Nodes (17): gemini_images(), moss_graph(), moss_images(), short_credit(), graphics_count(), to_vertical(), is_loop_short(), ink_silhouette() (+9 more)

### Community 27 - "frame_maker"
Cohesion: 0.06
Nodes (17): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+9 more)

### Community 28 - "apply_review_fixes"
Cohesion: 0.12
Nodes (10): apply_review_fixes(), rewrite_paint_prompts(), ask(), _review_state(), test_auto_fix_graphic(), test_look_check_fixes_code(), test_redraw_failure_paints(), test_review_redraws_custom() (+2 more)

### Community 29 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 30 - "math"
Cohesion: 0.16
Nodes (6): collection(), ink_lines(), linear(), material(), setup(), radians()

### Community 31 - "parts.py"
Cohesion: 0.16
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 33 - "owner"
Cohesion: 0.08
Nodes (13): article_text(), fact_check(), owner(), _fake_planning(), test_director_prompt_mentions_full(), test_fact_check_drops_full(), stubbed, test_gather_pool_shape() (+5 more)

### Community 34 - "templates.py"
Cohesion: 0.17
Nodes (15): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge() (+7 more)

### Community 35 - "use_opener"
Cohesion: 0.25
Nodes (5): use_opener(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 36 - "test_story.py"
Cohesion: 0.22
Nodes (10): first_sentence(), story_problems(), read(), test_cold_read_verdicts(), test_first_sentence_reads_across_the_cut(), test_no_hook_setting_no_hook_check(), test_rules_accept_opener_setting(), test_story_problems() (+2 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (22): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+14 more)

### Community 38 - "main"
Cohesion: 0.18
Nodes (4): keyvis(), main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "subprocess"
Cohesion: 0.08
Nodes (14): hex_rgb(), luminance(), available(), clean_code(), fingerprint(), node_run(), preview_sheet(), tsc_check() (+6 more)

### Community 41 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.13
Nodes (19): Captions(), PersonCard(), Root(), Background(), flashAlpha(), GraphicFor(), Move, Scene (+11 more)

### Community 43 - "textures.mjs"
Cohesion: 0.25
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "sfx_events"
Cohesion: 0.25
Nodes (4): schedule_sounds(), sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 45 - "test_topic_ideas.py"
Cohesion: 0.15
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 46 - "extra_sources.py"
Cohesion: 0.18
Nodes (17): brand_films(), brand_images(), brand_page(), candidate(), collection_images(), europeana_images(), loc_images(), pixabay_images() (+9 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "clean_photo"
Cohesion: 0.12
Nodes (8): clean_photo(), is_stereo(), trim_borders(), border(), plain(), vertical_image(), visual_unique(), mark_details()

### Community 49 - "pick_channel"
Cohesion: 0.18
Nodes (6): new_channel(), pick_channel(), save_channel(), draft_rules(), require_rules(), test_new_channel_stops_for_review()

### Community 50 - "fake_ai"
Cohesion: 0.12
Nodes (11): entry_age(), logbook_results(), apply_metadata(), clean_tags(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai() (+3 more)

### Community 51 - "main"
Cohesion: 0.17
Nodes (11): ask_count(), ask_yes(), load_channel(), use_channel(), fix_short(), main(), prune_work(), test_blender_failure_is_reported_and_the_batch_goes_on() (+3 more)

### Community 52 - "test_style.py"
Cohesion: 0.05
Nodes (45): cut_text(), look_text(), clean_invention(), clean_look(), clean_transition(), settle_style(), approve_candidate(), clean_style_code() (+37 more)

### Community 53 - "re"
Cohesion: 0.07
Nodes (11): vault_page(), vault_refresh(), import_media(), local_assets(), media_search_words(), fallback_custom_tsx(), parse_scene_money(), max_full() (+3 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "retention.py"
Cohesion: 0.18
Nodes (8): ask_number(), retention_observations(), analyze(), command(), normalize_reply(), report_text(), scenes_from_plan(), seconds()

### Community 57 - "make_opener"
Cohesion: 0.11
Nodes (12): lint(), make_opener(), review(), sheet_times(), write(), fake_ai(), short(), test_drawn_opener_gives_up_after_fixes() (+4 more)

### Community 59 - "gather_pool"
Cohesion: 0.09
Nodes (12): commons_films(), article_images(), commons_search(), get_image(), openverse_images(), ov_get(), thumb_url(), usable_license() (+4 more)

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "music_gain"
Cohesion: 0.22
Nodes (4): music_gain(), speak(), tts(), test_music_gain_evens_out_tracks()

### Community 64 - "fetch"
Cohesion: 0.13
Nodes (12): archive_ad_films(), archive_films(), duke_films(), nasa_films(), pixabay_films(), archive_images(), nasa_images(), nasa_search() (+4 more)

### Community 65 - "edit_scripts"
Cohesion: 0.12
Nodes (11): other_ai(), cold_read(), edit_scripts(), narration_lines(), recheck_final_scripts(), test_gemini_modes_choose_codex_and_keep_editor_choice(), test_solo_edit_scripts_uses_same_ai(), test_cold_read_handles_malformed_reply() (+3 more)

### Community 66 - "visual_review"
Cohesion: 0.10
Nodes (13): clock(), overlay_notes(), pacing_check(), quality_check(), review_fixes(), review_status(), visual_review(), length_plan() (+5 more)

### Community 69 - "first_second_check"
Cohesion: 0.15
Nodes (14): first_second_check(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture() (+6 more)

### Community 70 - "words_of"
Cohesion: 0.14
Nodes (10): clean_sound(), limit_sounds(), full_formats(), rescue_graphics(), fill_money_graphics(), words_of(), test_clean_sound(), test_fill_money_graphics_and_caps() (+2 more)

### Community 71 - "clean_full"
Cohesion: 0.12
Nodes (16): clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number() (+8 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.14
Nodes (12): align(), align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak(), test_caption_word_counts_match_the_scene_splitter() (+4 more)

### Community 73 - "ask_ai"
Cohesion: 0.10
Nodes (19): scene_cues(), ask_ai(), gemini_model(), test_counter_finishes_before_it_leaves(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high() (+11 more)

### Community 75 - "audio_library.py"
Cohesion: 0.12
Nodes (26): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+18 more)

### Community 76 - "Custom3.tsx"
Cohesion: 0.39
Nodes (3): clamp, CustomFull, FullProps

### Community 77 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 78 - "blender_plan.py"
Cohesion: 0.12
Nodes (8): clamp(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order(), test_thumbnail_order_skips_film_and_puts_openers_first()

### Community 79 - "edit_plan"
Cohesion: 0.20
Nodes (5): cold_read_line(), edit_plan(), picture_line(), test_edit_plan_picture_line(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 80 - "full_cues"
Cohesion: 0.17
Nodes (7): full_cues(), spoken_at(), spoken_span(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish(), test_opener_graphic()

### Community 81 - "test_blender_plan.py"
Cohesion: 0.25
Nodes (14): clean_build(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults(), test_clean_build_keeps_a_good_plan(), test_default_build_shape(), test_label_is_short_and_upper(), test_nan_and_infinity_get_defaults() (+6 more)

### Community 82 - "configure_brain"
Cohesion: 0.16
Nodes (13): ask_brain(), configure_brain(), normalize_brain(), fake_providers(), claude(), reply(), saved_session(), test_all_modes_route_writer_editor_and_reader() (+5 more)

### Community 85 - "finish_render"
Cohesion: 0.10
Nodes (14): full_summary(), opener_graphic(), drawn_answer_problem(), fix_drawn_answer(), fix_opener_graphic(), paint_opener_start(), status_lines(), weak_opener_graphic() (+6 more)

### Community 89 - "choose_images"
Cohesion: 0.19
Nodes (14): choose_images(), apply_look_scenes(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+6 more)

### Community 90 - "drawn_thumbnail"
Cohesion: 0.23
Nodes (9): scene_frames(), drawn_thumbnail(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 91 - "write_json"
Cohesion: 0.33
Nodes (5): begin(), pack(), save_context(), unpack(), write_json()

### Community 92 - "test_blender_render.py"
Cohesion: 0.22
Nodes (12): peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises(), test_frames_are_trimmed_after_the_clips_are_cut() (+4 more)

### Community 94 - "is_person_portrait"
Cohesion: 0.33
Nodes (3): download_picture(), recover_downloads(), is_person_portrait()

### Community 95 - "full_props"
Cohesion: 0.33
Nodes (5): full_props(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_remotion_props_full()

### Community 96 - "full_pictures"
Cohesion: 0.40
Nodes (4): full_pictures(), _board(), test_board_pictures_attached(), test_sfx_full()

### Community 114 - "log_short"
Cohesion: 0.25
Nodes (5): sentence_groups(), log_short(), scenes(), test_logbook_hook_line_is_the_whole_first_sentence(), test_sentences_running_across_cuts_are_one_take()

## Knowledge Gaps
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `ffmpeg`, `json`, `render_remotion`, `local_clips`, `resume_runs`, `frame_maker`, `use_opener`, `subprocess`, `sfx_events`, `clean_photo`, `main`, `test_style.py`, `music_gain`, `visual_review`, `words_of`, `ask_ai`, `test_full_scenes.py`, `audio_library.py`, `captions`, `finish_render`, `choose_images`, `drawn_thumbnail`, `write_json`, `test_blender_render.py`, `make_sfx`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12802275960170698 - nodes in this community are weakly interconnected._
- **Why does `veo_handoff()` connect `local_clips` to `json`, `test_full_scenes.py`, `test_h3_handoff.py`, `test_style.py`, `h3_run.py`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._
- **Why does `OpeningRulesTests` connect `OpeningRulesTests` to `test_full_scenes.py`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14919354838709678 - nodes in this community are weakly interconnected._
- **Should `prepare_topic` be split into smaller, more focused modules?**
  _Cohesion score 0.11688311688311688 - nodes in this community are weakly interconnected._