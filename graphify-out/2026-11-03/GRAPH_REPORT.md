# Graph Report - ShortsMaker  (2026-11-03)

## Corpus Check
- 140 files · ~162,157 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2203 nodes · 6083 edges · 106 communities (86 shown, 20 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 135 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c1eb534a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- load_pool
- test_blender_scene.py
- split_make_shorts.py
- ffmpeg
- code_custom_scenes
- render_clips
- guarded.tsx
- k
- test_h3_handoff.py
- test_style.py
- json
- drawn_opener.py
- test_rules.py
- Journey.tsx
- toolkit.tsx
- apply_review_fixes
- write_scripts
- Local GPU Worker
- core.mjs
- local_clips
- edit_project.py
- makeKit
- drawn_thumbnail
- render
- frame_maker
- rewrite_paint_prompts
- h3_run.py
- math
- parts.py
- OpeningRulesTests
- owner
- templates.py
- paint_opener_start
- edit_scripts
- full/types.ts
- main
- Paper
- test_story.py
- Shots
- Short.tsx
- textures.mjs
- sfx_events
- writing.py
- brand_images
- Halftone.tsx
- clean_photo
- extra_sources.py
- fake_ai
- story_problems
- invent_component
- footage.py
- kit.mjs
- RetentionTests
- re
- finish_render
- ReliabilityTests
- gather_pool
- run_agy
- bean.mjs
- style_library
- popS
- fetch
- download_audio_choices
- visual_review
- dexter.mjs
- kit_parts.mjs
- test_first_second.py
- review
- clean_full
- qwen_voice.py
- ask_ai
- test_full_scenes.py
- audio_library.py
- Custom3.tsx
- captions
- article_text
- edit_plan
- full_cues
- test_drawn_opener_renders_and_is_reused
- main
- MediaTests
- MetadataTests
- opener_graphic
- PreflightTests
- MarkTests
- StoryPacingTests
- choose_images
- first_second_check
- quality_check
- test_blender_plan.py
- FeedbackTests
- default_build
- full_props
- test_story_sound_library
- wants_remotion
- test_review_redraws_custom
- render_remotion
- make_sfx
- max_full
- BlenderFailed
- limit_style
- min_real_pictures
- test_short_credit

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 61 edges
3. `write_scripts()` - 53 edges
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
- `test_new_channel_stops_for_review()` --calls--> `pick_channel()`  [EXTRACTED]
  tests/test_rules.py → shortsmaker/channel_profiles.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`
- 3-file cycle: `shortsmaker/motion.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`
- 4-file cycle: `shortsmaker/motion.py -> shortsmaker/opening_rules.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`

## Communities (106 total, 20 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.14
Nodes (24): catalog_entries(), catalog_pool(), clean_pics(), save_pool(), entry(), film(), pic_short(), pool_of() (+16 more)

### Community 3 - "load_pool"
Cohesion: 0.12
Nodes (9): catalog_text(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures(), usable() (+1 more)

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "ffmpeg"
Cohesion: 0.12
Nodes (13): cosy_instruct(), local_voice(), sentence_groups(), split_takes(), log_short(), duration(), ffmpeg(), is_loop_short() (+5 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.15
Nodes (13): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), opener_preflight(), preview_custom() (+5 more)

### Community 8 - "render_clips"
Cohesion: 0.17
Nodes (13): code_version(), peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises() (+5 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.13
Nodes (18): Box, boxAt(), clamp, Connect(), fitCard(), hits(), layoutColumn(), layoutGrid() (+10 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "test_style.py"
Cohesion: 0.14
Nodes (15): save_candidate(), candidate_in(), library_snapshot(), plan_with(), ask(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure() (+7 more)

### Community 13 - "json"
Cohesion: 0.06
Nodes (26): main(), pixabay_films(), comfy_call(), moss_graph(), moss_images(), voicestudio_unload(), voicestudio_up(), import_media() (+18 more)

### Community 14 - "drawn_opener.py"
Cohesion: 0.13
Nodes (10): available(), clean_code(), fingerprint(), lint(), make_opener(), node_run(), sheet_times(), write() (+2 more)

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (39): load_rules(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft(), stop_text() (+31 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.21
Nodes (21): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+13 more)

### Community 18 - "apply_review_fixes"
Cohesion: 0.18
Nodes (7): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 19 - "write_scripts"
Cohesion: 0.11
Nodes (26): prepare_topic(), limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai() (+18 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "local_clips"
Cohesion: 0.12
Nodes (12): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), motion_prompt(), start_picture(), start_picture_problems() (+4 more)

### Community 23 - "edit_project.py"
Cohesion: 0.13
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "drawn_thumbnail"
Cohesion: 0.17
Nodes (11): thumbnail_order(), scene_frames(), drawn_thumbnail(), test_thumbnail_order_skips_film_and_puts_openers_first(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back() (+3 more)

### Community 26 - "render"
Cohesion: 0.09
Nodes (11): short_credit(), graphics_count(), to_vertical(), ink_silhouette(), paint_instead(), srt(), drawn_choices(), render() (+3 more)

### Community 27 - "frame_maker"
Cohesion: 0.06
Nodes (17): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+9 more)

### Community 28 - "rewrite_paint_prompts"
Cohesion: 0.18
Nodes (5): rewrite_paint_prompts(), ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

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
Cohesion: 0.12
Nodes (5): owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_skip_and_limits()

### Community 34 - "templates.py"
Cohesion: 0.17
Nodes (15): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge() (+7 more)

### Community 35 - "paint_opener_start"
Cohesion: 0.13
Nodes (7): gemini_images(), paint_opener_start(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), test_weak_opener_graphic_fixes_then_handoff(), use()

### Community 36 - "edit_scripts"
Cohesion: 0.12
Nodes (12): other_ai(), cold_read(), edit_scripts(), narration_lines(), recheck_final_scripts(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_gemini_modes_choose_codex_and_keep_editor_choice(), test_solo_edit_scripts_uses_same_ai() (+4 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (22): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+14 more)

### Community 38 - "main"
Cohesion: 0.18
Nodes (4): keyvis(), main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "test_story.py"
Cohesion: 0.18
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

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
Cohesion: 0.15
Nodes (8): schedule_sounds(), sfx_events(), full_pictures(), _board(), test_board_pictures_attached(), test_sfx_full(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 45 - "writing.py"
Cohesion: 0.07
Nodes (19): channel_url(), new_channel(), save_channel(), trend_research(), yt_list(), apply_metadata(), clean_tags(), clean_title() (+11 more)

### Community 46 - "brand_images"
Cohesion: 0.15
Nodes (10): brand_films(), brand_images(), brand_page(), BrandImages, commercial_queries(), duke_films(), settings(), source_enabled() (+2 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "clean_photo"
Cohesion: 0.12
Nodes (8): clean_photo(), is_stereo(), trim_borders(), border(), plain(), vertical_image(), visual_unique(), mark_details()

### Community 49 - "extra_sources.py"
Cohesion: 0.37
Nodes (9): candidate(), collection_images(), europeana_images(), loc_images(), pixabay_images(), smithsonian_images(), source_json(), wellcome_images() (+1 more)

### Community 50 - "fake_ai"
Cohesion: 0.15
Nodes (9): entry_age(), logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel() (+1 more)

### Community 51 - "story_problems"
Cohesion: 0.24
Nodes (9): first_sentence(), story_problems(), read(), test_cold_read_verdicts(), test_first_sentence_reads_across_the_cut(), test_no_hook_setting_no_hook_check(), test_story_problems(), test_story_problems_flags_summary_hook() (+1 more)

### Community 52 - "invent_component"
Cohesion: 0.13
Nodes (15): invent_component(), attempt(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile() (+7 more)

### Community 53 - "footage.py"
Cohesion: 0.13
Nodes (9): commons_films(), crop_film_bytes(), crop_filter(), film_frames(), film_piece(), shot_moments(), shot_span(), film_ffmpeg() (+1 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "re"
Cohesion: 0.12
Nodes (15): pick_channel(), parse_scene_money(), analyze(), edit_metrics(), load_metrics(), metrics_text(), normalize_metrics(), normalize_reply() (+7 more)

### Community 57 - "finish_render"
Cohesion: 0.24
Nodes (7): drawn_answer_problem(), status_lines(), weak_opener_graphic(), finish_render(), load_state(), save_state(), test_state_roundtrip_full_pics()

### Community 59 - "gather_pool"
Cohesion: 0.15
Nodes (7): article_images(), commons_search(), thumb_url(), wm_files(), balanced_candidates(), gather_pool(), test_gather_pool_shape()

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "style_library"
Cohesion: 0.11
Nodes (15): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), build() (+7 more)

### Community 64 - "fetch"
Cohesion: 0.11
Nodes (13): archive_ad_films(), archive_films(), nasa_films(), archive_images(), get_image(), nasa_images(), nasa_search(), on_topic() (+5 more)

### Community 65 - "download_audio_choices"
Cohesion: 0.25
Nodes (5): freesound_fetch(), freesound_preview(), freesound_results(), download_audio_choices(), seed_audio_library()

### Community 66 - "visual_review"
Cohesion: 0.20
Nodes (8): clock(), overlay_notes(), pacing_check(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 69 - "test_first_second.py"
Cohesion: 0.23
Nodes (11): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once(), test_opener_must_be_a_later_real_picture() (+3 more)

### Community 70 - "review"
Cohesion: 0.32
Nodes (3): review(), test_no_verdict_is_not_a_pass(), RenderResumeTests

### Community 71 - "clean_full"
Cohesion: 0.07
Nodes (28): clean_sound(), limit_sounds(), short_skin(), full_formats(), rescue_graphics(), clean_full(), word(), clean_graphic() (+20 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.12
Nodes (14): align(), align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak(), spoken_count() (+6 more)

### Community 73 - "ask_ai"
Cohesion: 0.12
Nodes (14): seed_ideas(), ask_ai(), gemini_model(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high(), test_fake_reaches_callers() (+6 more)

### Community 75 - "audio_library.py"
Cohesion: 0.21
Nodes (18): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+10 more)

### Community 76 - "Custom3.tsx"
Cohesion: 0.39
Nodes (3): clamp, CustomFull, FullProps

### Community 77 - "captions"
Cohesion: 0.12
Nodes (9): ass_time(), caption_lines(), captions(), styled(), music_gain(), speak(), tts(), ass_colour() (+1 more)

### Community 78 - "article_text"
Cohesion: 0.40
Nodes (3): article_text(), fact_check(), test_fact_check_drops_full()

### Community 79 - "edit_plan"
Cohesion: 0.14
Nodes (7): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 80 - "full_cues"
Cohesion: 0.13
Nodes (11): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish() (+3 more)

### Community 81 - "test_drawn_opener_renders_and_is_reused"
Cohesion: 0.29
Nodes (5): fake_ai(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused(), test_use_opener_plays_the_drawn_opener()

### Community 82 - "main"
Cohesion: 0.06
Nodes (42): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), load_channel(), normalize_brain(), use_channel() (+34 more)

### Community 85 - "opener_graphic"
Cohesion: 0.20
Nodes (7): full_summary(), opener_graphic(), fix_drawn_answer(), fix_opener_graphic(), test_full_props_figure(), test_full_summary(), test_opener_graphic()

### Community 89 - "choose_images"
Cohesion: 0.17
Nodes (15): choose_images(), download_picture(), recover_downloads(), is_person_portrait(), picking, planned_short(), scene(), still() (+7 more)

### Community 90 - "first_second_check"
Cohesion: 0.33
Nodes (4): first_second_check(), review_status(), test_failed_preview_clears_previous_opener_score(), test_opener_prompt_shows_each_scenes_line_and_picture()

### Community 91 - "quality_check"
Cohesion: 0.25
Nodes (4): quality_check(), length_plan(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 92 - "test_blender_plan.py"
Cohesion: 0.16
Nodes (16): clamp(), clean_build(), ending(), panels(), pick(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults() (+8 more)

### Community 94 - "default_build"
Cohesion: 0.29
Nodes (4): default_build(), plan_builds(), test_plan_builds_retries_then_defaults(), ask()

### Community 95 - "full_props"
Cohesion: 0.40
Nodes (4): full_props(), _jpg(), test_custom_cues_props_and_pictures(), test_remotion_props_full()

### Community 96 - "test_story_sound_library"
Cohesion: 0.67
Nodes (3): test_story_sound_library(), fetch(), _tone_wav()

### Community 97 - "wants_remotion"
Cohesion: 0.27
Nodes (4): wants_remotion(), apply_look_scenes(), test_apply_look_scenes(), test_remotion_forced_by_look()

### Community 98 - "test_review_redraws_custom"
Cohesion: 0.40
Nodes (3): _review_state(), test_redraw_failure_paints(), test_review_redraws_custom()

### Community 99 - "render_remotion"
Cohesion: 0.14
Nodes (10): render_remotion(), remotion(), render(), run_remotion_with_fallback(), invent_styles(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback() (+2 more)

## Knowledge Gaps
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `ffmpeg`, `render_clips`, `test_style.py`, `json`, `local_clips`, `drawn_thumbnail`, `frame_maker`, `paint_opener_start`, `sfx_events`, `clean_photo`, `finish_render`, `visual_review`, `clean_full`, `test_full_scenes.py`, `audio_library.py`, `captions`, `full_cues`, `main`, `opener_graphic`, `choose_images`, `wants_remotion`, `render_remotion`, `make_sfx`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12802275960170698 - nodes in this community are weakly interconnected._
- **Why does `FeedbackTests` connect `FeedbackTests` to `writing.py`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `Shots`, `json`, `math`, `parts.py`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14204545454545456 - nodes in this community are weakly interconnected._
- **Should `load_pool` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._