# Graph Report - ShortsMaker  (2026-11-01)

## Corpus Check
- 134 files · ~154,951 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2084 nodes · 5781 edges · 98 communities (83 shown, 15 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 128 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b3c60ca1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- config.py
- test_blender_scene.py
- split_make_shorts.py
- fetch
- code_custom_scenes
- json
- guarded.tsx
- k
- test_h3_handoff.py
- owner
- test_style.py
- render_remotion
- test_rules.py
- Journey.tsx
- toolkit.tsx
- style_lab.py
- write_scripts
- Local GPU Worker
- core.mjs
- local_clips
- edit_project.py
- makeKit
- test_blender_plan.py
- paint_instead
- frame_maker
- full_cues
- time
- look.py
- parts.py
- drawn_opener.py
- image_sources.py
- templates.py
- use
- test_story.py
- full/types.ts
- main
- Paper
- finish_render
- build_scene.py
- Short.tsx
- textures.mjs
- full_props
- re
- brand_images
- Halftone.tsx
- pick_ideas
- invent_component
- extra_sources.py
- main
- style_placeholders
- quality_check
- kit.mjs
- RetentionTests
- shutil
- trend_research
- ReliabilityTests
- gather_pool
- run_agy
- bean.mjs
- ffmpeg
- popS
- test_full_scenes.py
- edit_scripts
- visual_review
- dexter.mjs
- kit_parts.mjs
- first_second_check
- clean_sound
- plan_rules.py
- qwen_voice.py
- ask_ai
- audio_library.py
- log_short
- captions
- ref_remotion
- edit_plan
- clean_invention
- limit_full
- test_every_mode_can_continue_through_two_exhausted_ais
- MediaTests
- test_story_sound_library
- paint_opener_start
- MarkTests
- drawn_thumbnail
- apply_look_scenes
- test_blender_render.py
- clean_photo
- is_loop_short
- save_candidate
- default_build
- write_frames
- media_command
- BlenderFailed
- render

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
- `test_pixabay_keeps_only_on_topic_videos()` --calls--> `pixabay_films()`  [EXTRACTED]
  tests/test_pictures_first.py → shortsmaker/footage.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`

## Communities (98 total, 15 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.05
Nodes (57): choose_images(), download_picture(), recover_downloads(), catalog_entries(), catalog_pool(), catalog_text(), clean_pics(), contact_sheets() (+49 more)

### Community 3 - "config.py"
Cohesion: 0.17
Nodes (3): hex_rgb(), luminance(), import_media()

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "fetch"
Cohesion: 0.16
Nodes (10): archive_ad_films(), archive_films(), duke_films(), nasa_films(), archive_images(), nasa_images(), nasa_search(), on_topic() (+2 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.12
Nodes (13): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+5 more)

### Community 8 - "json"
Cohesion: 0.09
Nodes (15): code_version(), crop_film_bytes(), crop_filter(), film_frames(), film_piece(), pixabay_films(), shot_moments(), film_ffmpeg() (+7 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 13 - "test_style.py"
Cohesion: 0.10
Nodes (15): clean_look(), clean_transition(), wants_remotion(), plan_with(), ask(), test_clean_question_and_kinetic(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library() (+7 more)

### Community 14 - "render_remotion"
Cohesion: 0.16
Nodes (9): render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (38): draft_rules(), load_rules(), min_real_pictures(), parse_rules(), require_rules(), capture_prompts(), ask(), draft_reply() (+30 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 18 - "style_lab.py"
Cohesion: 0.18
Nodes (9): approve_candidate(), library_menu(), reject_candidate(), style_library(), style_rules(), write_style_index(), direct_scripts(), test_approve_adds_to_library() (+1 more)

### Community 19 - "write_scripts"
Cohesion: 0.12
Nodes (23): limit_style(), narration_lines(), write_scripts(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+15 more)

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

### Community 25 - "test_blender_plan.py"
Cohesion: 0.16
Nodes (16): clamp(), clean_build(), ending(), panels(), pick(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults() (+8 more)

### Community 26 - "paint_instead"
Cohesion: 0.15
Nodes (6): ink_silhouette(), make_paper(), paint_instead(), test_ink_silhouette(), test_make_paper(), test_remotion_failure_paints()

### Community 27 - "frame_maker"
Cohesion: 0.09
Nodes (11): ClipReader, draw_card(), draw_graphic(), fit_font(), frame_maker(), frame(), graphic_overlay(), shot() (+3 more)

### Community 28 - "full_cues"
Cohesion: 0.20
Nodes (6): full_cues(), spoken_at(), spoken_span(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish()

### Community 29 - "time"
Cohesion: 0.08
Nodes (11): call(), fit_start(), frames(), graph(), main(), saved_file(), voicestudio_up(), fetch_ideas() (+3 more)

### Community 30 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 32 - "drawn_opener.py"
Cohesion: 0.08
Nodes (18): available(), clean_code(), fingerprint(), lint(), make_opener(), node_run(), review(), sheet_times() (+10 more)

### Community 33 - "image_sources.py"
Cohesion: 0.15
Nodes (7): commons_films(), get_image(), openverse_images(), ov_get(), short_credit(), usable_license(), wm_get()

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "use"
Cohesion: 0.33
Nodes (4): fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 36 - "test_story.py"
Cohesion: 0.16
Nodes (15): first_sentence(), check_twists(), story_problems(), read(), test_cold_read_verdicts(), test_first_sentence_reads_across_the_cut(), test_no_hook_setting_no_hook_check(), test_rules_accept_opener_setting() (+7 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "finish_render"
Cohesion: 0.21
Nodes (7): status_lines(), weak_opener_graphic(), finish_render(), load_state(), save_state(), use_opener(), test_state_roundtrip_full_pics()

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "textures.mjs"
Cohesion: 0.25
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "full_props"
Cohesion: 0.11
Nodes (12): schedule_sounds(), sfx_events(), full_props(), full_pictures(), _board(), _jpg(), test_board_pictures_attached(), test_custom_cues_props_and_pictures() (+4 more)

### Community 45 - "re"
Cohesion: 0.15
Nodes (7): logbook_results(), vault_page(), vault_refresh(), mark_details(), max_full(), max_full_planned(), test_logbook_marks_tiny_samples()

### Community 46 - "brand_images"
Cohesion: 0.19
Nodes (8): brand_films(), brand_images(), brand_page(), BrandImages, settings(), source_enabled(), source_status(), print_source_status()

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "pick_ideas"
Cohesion: 0.20
Nodes (7): clash(), pages(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_pages_setting(), test_pick_skips_done_and_taken()

### Community 49 - "invent_component"
Cohesion: 0.16
Nodes (8): clean_style_code(), invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), test_invention_lint_failure_uses_fallback(), test_placeholders_match_the_slots()

### Community 50 - "extra_sources.py"
Cohesion: 0.37
Nodes (9): candidate(), collection_images(), europeana_images(), loc_images(), pixabay_images(), smithsonian_images(), source_json(), wellcome_images() (+1 more)

### Community 51 - "main"
Cohesion: 0.07
Nodes (36): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), load_channel(), new_channel(), normalize_brain() (+28 more)

### Community 52 - "style_placeholders"
Cohesion: 0.21
Nodes (9): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_slots_restored_after_render() (+1 more)

### Community 53 - "quality_check"
Cohesion: 0.25
Nodes (4): quality_check(), length_plan(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "shutil"
Cohesion: 0.11
Nodes (12): prune_cache(), analyze(), normalize_reply(), report_text(), scenes_from_plan(), seconds(), review_status(), apply() (+4 more)

### Community 57 - "trend_research"
Cohesion: 0.29
Nodes (4): channel_url(), seed_ideas(), trend_research(), yt_list()

### Community 59 - "gather_pool"
Cohesion: 0.12
Nodes (9): commercial_queries(), article_images(), commons_search(), thumb_url(), wm_files(), local_assets(), media_search_words(), balanced_candidates() (+1 more)

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "ffmpeg"
Cohesion: 0.12
Nodes (11): shot_span(), cosy_instruct(), local_voice(), sentence_groups(), split_takes(), spoken_count(), voicestudio_unload(), duration() (+3 more)

### Community 64 - "test_full_scenes.py"
Cohesion: 0.08
Nodes (10): short_skin(), person_card(), comfy_call(), moss_graph(), moss_images(), tsc_check(), visual_unique(), storyboard() (+2 more)

### Community 65 - "edit_scripts"
Cohesion: 0.13
Nodes (11): other_ai(), cold_read(), edit_scripts(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_gemini_modes_choose_codex_and_keep_editor_choice(), test_solo_edit_scripts_uses_same_ai(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers() (+3 more)

### Community 66 - "visual_review"
Cohesion: 0.24
Nodes (7): clock(), overlay_notes(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 69 - "first_second_check"
Cohesion: 0.05
Nodes (31): use_picture_from(), apply_review_fixes(), first_second_check(), paint_new(), pool_pictures(), rewrite_paint_prompts(), swap_pictures(), real() (+23 more)

### Community 70 - "clean_sound"
Cohesion: 0.40
Nodes (3): clean_sound(), limit_sounds(), test_clean_sound()

### Community 71 - "plan_rules.py"
Cohesion: 0.11
Nodes (19): rescue_graphics(), clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures() (+11 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.13
Nodes (13): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+5 more)

### Community 73 - "ask_ai"
Cohesion: 0.11
Nodes (17): scene_cues(), ask_ai(), gemini_model(), test_counter_finishes_before_it_leaves(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high() (+9 more)

### Community 75 - "audio_library.py"
Cohesion: 0.24
Nodes (15): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+7 more)

### Community 76 - "log_short"
Cohesion: 0.22
Nodes (7): log_short(), build(), add(), main(), scenes(), test_logbook_hook_line_is_the_whole_first_sentence(), test_sentences_running_across_cuts_are_one_take()

### Community 77 - "captions"
Cohesion: 0.12
Nodes (9): ass_time(), caption_lines(), captions(), styled(), music_gain(), speak(), tts(), ass_colour() (+1 more)

### Community 79 - "edit_plan"
Cohesion: 0.17
Nodes (6): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 82 - "test_every_mode_can_continue_through_two_exhausted_ais"
Cohesion: 0.32
Nodes (7): fake_providers(), claude(), reply(), saved_session(), test_all_modes_route_writer_editor_and_reader(), test_every_mode_can_continue_through_two_exhausted_ais(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty()

### Community 84 - "test_story_sound_library"
Cohesion: 0.67
Nodes (3): test_story_sound_library(), fetch(), _tone_wav()

### Community 85 - "paint_opener_start"
Cohesion: 0.20
Nodes (4): gemini_images(), fix_opener_graphic(), paint_opener_start(), test_weak_opener_graphic_fixes_then_handoff()

### Community 88 - "drawn_thumbnail"
Cohesion: 0.17
Nodes (11): thumbnail_order(), scene_frames(), drawn_thumbnail(), test_thumbnail_order_skips_film_and_puts_openers_first(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back() (+3 more)

### Community 92 - "test_blender_render.py"
Cohesion: 0.22
Nodes (12): peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises(), test_frames_are_trimmed_after_the_clips_are_cut() (+4 more)

### Community 96 - "clean_photo"
Cohesion: 0.14
Nodes (7): clean_photo(), is_stereo(), to_vertical(), trim_borders(), border(), plain(), vertical_image()

### Community 98 - "is_loop_short"
Cohesion: 0.15
Nodes (7): fills_frame(), graphic_low(), fill_money_graphics(), is_loop_short(), is_person_portrait(), parse_scene_money(), test_fill_money_graphics_and_caps()

### Community 99 - "save_candidate"
Cohesion: 0.19
Nodes (9): save_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_candidate_names_unique_across_kinds(), test_reject_deletes() (+1 more)

### Community 102 - "default_build"
Cohesion: 0.29
Nodes (4): default_build(), plan_builds(), test_plan_builds_retries_then_defaults(), ask()

### Community 103 - "write_frames"
Cohesion: 0.29
Nodes (3): flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 104 - "media_command"
Cohesion: 0.22
Nodes (8): freesound_fetch(), freesound_preview(), freesound_results(), audition_audio(), download_audio_choices(), media_command(), review_audio_files(), seed_audio_library()

### Community 114 - "render"
Cohesion: 0.09
Nodes (12): make_sfx(), full_summary(), graphics_count(), full_formats(), opener_graphic(), srt(), drawn_choices(), render() (+4 more)

## Knowledge Gaps
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MediaTests` connect `MediaTests` to `test_full_scenes.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `test_pictures_first.py`, `config.py`, `json`, `test_style.py`, `render_remotion`, `local_clips`, `paint_instead`, `frame_maker`, `image_sources.py`, `finish_render`, `full_props`, `re`, `main`, `shutil`, `ffmpeg`, `test_full_scenes.py`, `visual_review`, `plan_rules.py`, `ask_ai`, `audio_library.py`, `captions`, `paint_opener_start`, `drawn_thumbnail`, `test_blender_render.py`, `clean_photo`, `is_loop_short`, `save_candidate`, `write_frames`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.050187265917602995 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `test_pictures_first.py`, `json`, `test_style.py`, `test_rules.py`, `style_lab.py`, `test_story.py`, `re`, `pick_ideas`, `main`, `quality_check`, `shutil`, `trend_research`, `edit_scripts`, `first_second_check`, `clean_sound`, `plan_rules.py`, `ask_ai`, `pathlib`, `clean_invention`, `limit_full`, `is_loop_short`, `default_build`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._
- **Should `code_custom_scenes` be split into smaller, more focused modules?**
  _Cohesion score 0.1225296442687747 - nodes in this community are weakly interconnected._