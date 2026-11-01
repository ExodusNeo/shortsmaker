# Graph Report - ShortsMaker  (2026-11-01)

## Corpus Check
- 134 files · ~154,777 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2082 nodes · 5772 edges · 107 communities (81 shown, 26 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 128 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4d9f417a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- plan_with
- test_blender_scene.py
- split_make_shorts.py
- fetch
- motion.py
- hashlib
- guarded.tsx
- k
- test_h3_handoff.py
- owner
- style_library
- render_remotion
- test_rules.py
- Journey.tsx
- toolkit.tsx
- prepare_topic
- write_scripts
- Local GPU Worker
- core.mjs
- gpu.py
- make
- makeKit
- test_blender_plan.py
- paint_instead
- frame_render.py
- full_cues
- json
- look.py
- parts.py
- drawn_opener.py
- __init__.py
- templates.py
- use
- story_problems
- full/types.ts
- main
- Paper
- render
- build_scene.py
- Short.tsx
- textures.mjs
- sfx_events
- fake_ai
- extra_sources.py
- Halftone.tsx
- fetch_ideas
- invent_component
- limit_style
- main
- short_with
- test_first_second.py
- kit.mjs
- RetentionTests
- tempfile
- choose_images
- ReliabilityTests
- gather_pool
- run_agy
- bean.mjs
- re
- popS
- pathlib
- edit_scripts
- visual_review
- dexter.mjs
- kit_parts.mjs
- apply_review_fixes
- full_props
- clean_full
- qwen_voice.py
- ask_ai
- llm.py
- audio_library.py
- duration
- captions
- ref_remotion
- edit_plan
- speak
- ink_silhouette
- test_every_mode_can_continue_through_two_exhausted_ais
- MediaTests
- test_story.py
- finish_render
- make_sfx
- MarkTests
- scene_frames
- apply_look_scenes
- srt
- wants_remotion
- test_blender_render.py
- drawn_choices
- test_local_job_retries_a_hard_crash
- code_version
- clean_photo
- words_of
- test_style.py
- default_build
- test_hard_cuts_never_blend_scenes
- media_command
- BlenderFailed
- thumbnail_order
- test_full_scenes.py
- ending
- panels

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 61 edges
3. `write_scripts()` - 51 edges
4. `ask_ai()` - 47 edges
5. `MediaTests` - 33 edges
6. `main()` - 32 edges
7. `skinOf()` - 29 edges
8. `clamp()` - 27 edges
9. `ellPts()` - 26 edges
10. `Paper()` - 25 edges

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

## Communities (107 total, 26 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.15
Nodes (22): catalog_entries(), catalog_pool(), clean_pics(), entry(), film(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+14 more)

### Community 3 - "plan_with"
Cohesion: 0.29
Nodes (5): plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "fetch"
Cohesion: 0.08
Nodes (18): archive_ad_films(), archive_films(), commons_films(), duke_films(), nasa_films(), pixabay_films(), archive_images(), get_image() (+10 more)

### Community 7 - "motion.py"
Cohesion: 0.13
Nodes (14): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), graphics_count(), lint_custom_code(), look_and_fix(), preview_custom() (+6 more)

### Community 8 - "hashlib"
Cohesion: 0.14
Nodes (10): crop_filter(), film_frames(), film_piece(), shot_moments(), film_ffmpeg(), import_media(), write_json(), load() (+2 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.21
Nodes (13): unpack_clips(), handoff(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated(), test_flagged_start_picture_is_not_sent(), test_handoff_picks_up_clips_zip(), test_handoff_records_which_file_made_the_clip(), test_handoff_writes_jobs_and_zip() (+5 more)

### Community 12 - "owner"
Cohesion: 0.13
Nodes (7): owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits(), test_good_look_check_skips_the_extra_compile()

### Community 13 - "style_library"
Cohesion: 0.11
Nodes (15): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), build() (+7 more)

### Community 14 - "render_remotion"
Cohesion: 0.16
Nodes (9): render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (40): draft_rules(), load_rules(), min_real_pictures(), parse_rules(), require_rules(), capture_prompts(), ask(), draft_reply() (+32 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 18 - "prepare_topic"
Cohesion: 0.11
Nodes (13): catalog_text(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures(), prepare_topic() (+5 more)

### Community 19 - "write_scripts"
Cohesion: 0.14
Nodes (22): write_scripts(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare() (+14 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "gpu.py"
Cohesion: 0.11
Nodes (16): comfy_call(), cover_crop(), cut_owner_clip(), h3_problems(), h3_prompt(), h3_prompts(), local_clips(), local_job() (+8 more)

### Community 23 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.22
Nodes (14): clamp(), clean_build(), pick(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults(), test_clean_build_keeps_a_good_plan(), test_default_build_shape() (+6 more)

### Community 26 - "paint_instead"
Cohesion: 0.25
Nodes (3): gemini_images(), paint_instead(), test_remotion_failure_paints()

### Community 27 - "frame_render.py"
Cohesion: 0.08
Nodes (16): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+8 more)

### Community 28 - "full_cues"
Cohesion: 0.13
Nodes (11): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish() (+3 more)

### Community 29 - "json"
Cohesion: 0.11
Nodes (11): call(), fit_start(), frames(), graph(), main(), saved_file(), prune_cache(), search_suggestions() (+3 more)

### Community 30 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 32 - "drawn_opener.py"
Cohesion: 0.08
Nodes (18): available(), clean_code(), fingerprint(), lint(), make_opener(), node_run(), review(), sheet_times() (+10 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "use"
Cohesion: 0.33
Nodes (4): fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 36 - "story_problems"
Cohesion: 0.24
Nodes (9): first_sentence(), story_problems(), read(), test_cold_read_verdicts(), test_first_sentence_reads_across_the_cut(), test_no_hook_setting_no_hook_check(), test_story_problems(), test_story_problems_flags_summary_hook() (+1 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "render"
Cohesion: 0.12
Nodes (14): ducking_filter(), preview_mix(), music_gain(), short_credit(), ffmpeg(), video_encoder(), apply(), preview() (+6 more)

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "textures.mjs"
Cohesion: 0.25
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "sfx_events"
Cohesion: 0.15
Nodes (8): schedule_sounds(), sfx_events(), full_pictures(), _board(), test_board_pictures_attached(), test_sfx_full(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 45 - "fake_ai"
Cohesion: 0.19
Nodes (8): logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel(), test_seo_never_sees_competitor_titles()

### Community 46 - "extra_sources.py"
Cohesion: 0.13
Nodes (19): brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images(), loc_images() (+11 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "fetch_ideas"
Cohesion: 0.12
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 49 - "invent_component"
Cohesion: 0.11
Nodes (16): clean_style_code(), invent_component(), attempt(), invent_styles(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview() (+8 more)

### Community 51 - "main"
Cohesion: 0.07
Nodes (35): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), load_channel(), normalize_brain(), use_channel() (+27 more)

### Community 52 - "short_with"
Cohesion: 0.21
Nodes (14): fake_ai(), short_with(), test_missing_scene_is_asked_again(), run(), test_owner_clip_is_cut_again_for_the_scene_it_now_sits_in(), test_retries_only_failing_scene_with_reason(), run(), test_scene_number_given_as_text_is_accepted() (+6 more)

### Community 53 - "test_first_second.py"
Cohesion: 0.19
Nodes (13): swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once() (+5 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "tempfile"
Cohesion: 0.12
Nodes (5): analyze(), normalize_reply(), report_text(), scenes_from_plan(), seconds()

### Community 57 - "choose_images"
Cohesion: 0.17
Nodes (15): choose_images(), download_picture(), recover_downloads(), is_person_portrait(), picking, planned_short(), scene(), still() (+7 more)

### Community 59 - "gather_pool"
Cohesion: 0.14
Nodes (7): commercial_queries(), article_images(), commons_search(), thumb_url(), wm_files(), balanced_candidates(), gather_pool()

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "re"
Cohesion: 0.09
Nodes (12): shot_span(), cosy_instruct(), local_voice(), sentence_groups(), split_takes(), spoken_count(), voicestudio_unload(), voicestudio_up() (+4 more)

### Community 65 - "edit_scripts"
Cohesion: 0.12
Nodes (11): other_ai(), cold_read(), edit_scripts(), length_plan(), narration_lines(), test_gemini_modes_choose_codex_and_keep_editor_choice(), test_solo_edit_scripts_uses_same_ai(), test_cold_read_handles_malformed_reply() (+3 more)

### Community 66 - "visual_review"
Cohesion: 0.12
Nodes (11): clock(), overlay_notes(), quality_check(), review_fixes(), storyboard(), visual_review(), max_seconds(), test_review_is_told_the_drawings_are_deliberate() (+3 more)

### Community 69 - "apply_review_fixes"
Cohesion: 0.10
Nodes (12): apply_review_fixes(), paint_new(), pool_pictures(), rewrite_paint_prompts(), ask(), _review_state(), test_auto_fix_graphic(), test_look_check_fixes_code() (+4 more)

### Community 70 - "full_props"
Cohesion: 0.40
Nodes (4): full_props(), _jpg(), test_custom_cues_props_and_pictures(), test_remotion_props_full()

### Community 71 - "clean_full"
Cohesion: 0.12
Nodes (16): clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number() (+8 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.14
Nodes (13): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+5 more)

### Community 73 - "ask_ai"
Cohesion: 0.12
Nodes (14): ask_ai(), gemini_model(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high(), test_encoder_cache_lives_with_video_encoder(), test_fake_reaches_callers() (+6 more)

### Community 74 - "llm.py"
Cohesion: 0.09
Nodes (9): channel_url(), new_channel(), pick_channel(), save_channel(), seed_ideas(), trend_research(), yt_list(), library_menu() (+1 more)

### Community 75 - "audio_library.py"
Cohesion: 0.27
Nodes (13): approved_sound(), audio_metadata(), history_read(), import_audio_file(), record_audio(), select_music(), score(), set_audio_metadata() (+5 more)

### Community 76 - "duration"
Cohesion: 0.29
Nodes (6): log_short(), duration(), scenes(), test_a_take_is_cut_between_the_scenes_words(), test_logbook_hook_line_is_the_whole_first_sentence(), test_sentences_running_across_cuts_are_one_take()

### Community 77 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 79 - "edit_plan"
Cohesion: 0.14
Nodes (7): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 82 - "test_every_mode_can_continue_through_two_exhausted_ais"
Cohesion: 0.32
Nodes (7): fake_providers(), claude(), reply(), saved_session(), test_all_modes_route_writer_editor_and_reader(), test_every_mode_can_continue_through_two_exhausted_ais(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty()

### Community 84 - "test_story.py"
Cohesion: 0.36
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 85 - "finish_render"
Cohesion: 0.10
Nodes (12): full_summary(), first_second_check(), fix_opener_graphic(), paint_opener_start(), review_status(), status_lines(), weak_opener_graphic(), drawn_thumbnail() (+4 more)

### Community 88 - "scene_frames"
Cohesion: 0.22
Nodes (8): scene_frames(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so(), test_thumbnail_uses_the_real_photo()

### Community 92 - "test_blender_render.py"
Cohesion: 0.22
Nodes (12): peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises(), test_frames_are_trimmed_after_the_clips_are_cut() (+4 more)

### Community 96 - "clean_photo"
Cohesion: 0.12
Nodes (8): clean_photo(), is_stereo(), to_vertical(), trim_borders(), border(), plain(), vertical_image(), mark_details()

### Community 98 - "words_of"
Cohesion: 0.14
Nodes (10): clean_sound(), limit_sounds(), rescue_graphics(), fill_money_graphics(), parse_scene_money(), words_of(), test_clean_sound(), test_fill_money_graphics_and_caps() (+2 more)

### Community 99 - "test_style.py"
Cohesion: 0.19
Nodes (11): approve_candidate(), save_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes() (+3 more)

### Community 102 - "default_build"
Cohesion: 0.29
Nodes (4): default_build(), plan_builds(), test_plan_builds_retries_then_defaults(), ask()

### Community 104 - "media_command"
Cohesion: 0.22
Nodes (8): freesound_fetch(), freesound_preview(), freesound_results(), audition_audio(), download_audio_choices(), media_command(), review_audio_files(), seed_audio_library()

### Community 114 - "test_full_scenes.py"
Cohesion: 0.07
Nodes (16): short_skin(), full_formats(), opener_graphic(), limit_full(), make_paper(), article_text(), fact_check(), test_clean_full_custom_and_skin() (+8 more)

## Knowledge Gaps
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MediaTests` connect `MediaTests` to `__init__.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `motion.py`, `hashlib`, `render_remotion`, `gpu.py`, `paint_instead`, `frame_render.py`, `full_cues`, `json`, `sfx_events`, `main`, `choose_images`, `re`, `pathlib`, `visual_review`, `audio_library.py`, `duration`, `captions`, `speak`, `ink_silhouette`, `finish_render`, `make_sfx`, `scene_frames`, `srt`, `wants_remotion`, `test_blender_render.py`, `drawn_choices`, `clean_photo`, `words_of`, `test_style.py`, `test_full_scenes.py`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `test_pictures_first.py`, `plan_with`, `owner`, `style_library`, `test_rules.py`, `prepare_topic`, `json`, `__init__.py`, `story_problems`, `fake_ai`, `fetch_ideas`, `limit_style`, `main`, `choose_images`, `re`, `edit_scripts`, `clean_full`, `ask_ai`, `llm.py`, `test_story.py`, `words_of`, `default_build`, `test_full_scenes.py`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `fetch` be split into smaller, more focused modules?**
  _Cohesion score 0.08172043010752689 - nodes in this community are weakly interconnected._
- **Should `motion.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12535612535612536 - nodes in this community are weakly interconnected._