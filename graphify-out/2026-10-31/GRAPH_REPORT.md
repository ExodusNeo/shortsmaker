# Graph Report - ShortsMaker  (2026-10-30)

## Corpus Check
- 108 files · ~118,725 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .canvas 1, .ipynb 1)

## Summary
- 1589 nodes · 4304 edges · 75 communities (70 shown, 5 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 104 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `edc4b5e6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- pool_of
- h3_run.py
- ask_ai
- split_make_shorts.py
- test_full_scenes.py
- code_custom_scenes
- json
- toolkit.tsx
- test_blender_plan.py
- test_h3_handoff.py
- test_blender_scene.py
- approve_candidate
- make
- test_rules.py
- Journey.tsx
- QuestionBeat.tsx
- load_pool
- write_scripts
- Local GPU Worker
- blender_plan.py
- gpu.py
- test_short_credit
- wm_files
- test_blender_render.py
- test_opener_graphic.py
- frame_maker
- full_cues
- captions
- look.py
- parts.py
- clean_full
- render_remotion
- templates.py
- gather_pool
- style_library
- run_draft
- main
- words_of
- default_build
- build_scene.py
- Short.tsx
- look_and_fix
- subprocess
- rescue_graphics
- ref_remotion
- Halftone.tsx
- re
- invent_component
- test_style.py
- main
- edit_plan
- test_first_second.py
- gemini_model
- style_placeholders
- run_agy
- test_pictures_first.py
- redraw_custom
- capture_prompts
- math
- ask_brain
- clean_graphic
- clean_sound
- srt
- BlenderFailed
- pool_pictures
- edit_scripts
- fix_short
- limit_style
- test_story.py
- trend_research
- drawn_thumbnail
- render
- trim_borders

## God Nodes (most connected - your core abstractions)
1. `render()` - 65 edges
2. `write_scripts()` - 48 edges
3. `ask_ai()` - 37 edges
4. `skinOf()` - 29 edges
5. `main()` - 26 edges
6. `Paper()` - 25 edges
7. `choose_images()` - 24 edges
8. `clean_full()` - 23 edges
9. `words_of()` - 22 edges
10. `Bridge` - 20 edges

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

## Communities (75 total, 5 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.14
Nodes (21): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.19
Nodes (26): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+18 more)

### Community 2 - "pool_of"
Cohesion: 0.13
Nodes (21): catalog_entries(), catalog_pool(), clean_pics(), entry(), fake_ai, pic_short(), pool_of(), test_board_item_pics_cleaned() (+13 more)

### Community 3 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 4 - "ask_ai"
Cohesion: 0.17
Nodes (9): ask_ai(), fact_check(), test_fact_check_drops_full(), test_quota_fallback_both_ways(), test_claude_pinned_to_opus_high(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash(), test_session_shared(), test_solo_ask_ai_hands_over_when_out_of_credits() (+1 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "test_full_scenes.py"
Cohesion: 0.11
Nodes (7): hex_rgb(), luminance(), tsc_check(), prune_work(), library_menu(), reject_candidate(), save_candidate()

### Community 7 - "code_custom_scenes"
Cohesion: 0.22
Nodes (7): code_custom_scenes(), fallback_custom_tsx(), lint_custom_code(), test_code_custom_scenes_fallback(), test_fallback_custom_is_clean(), test_lint_custom_code(), test_fake_reaches_callers()

### Community 8 - "json"
Cohesion: 0.07
Nodes (18): code_version(), archive_films(), commons_films(), crop_film_bytes(), film_frames(), nasa_films(), pixabay_films(), fills_frame() (+10 more)

### Community 9 - "toolkit.tsx"
Cohesion: 0.06
Nodes (84): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+76 more)

### Community 10 - "test_blender_plan.py"
Cohesion: 0.30
Nodes (12): clean_build(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults(), test_clean_build_keeps_a_good_plan(), test_default_build_shape(), test_label_is_short_and_upper(), test_nan_and_infinity_get_defaults() (+4 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 13 - "approve_candidate"
Cohesion: 0.23
Nodes (9): approve_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_candidate_names_unique_across_kinds() (+1 more)

### Community 14 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.17
Nodes (23): parse_rules(), make(), stop_text(), StopPicker, test_bad_min_pictures_stops(), test_blender_needs_a_build_plan_section(), test_bom_and_crlf_load_the_same(), test_draft_keeps_ai_headings_inside_their_section() (+15 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.11
Nodes (19): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+11 more)

### Community 17 - "QuestionBeat.tsx"
Cohesion: 0.26
Nodes (6): FONT, theme, Word, CLAMP, KineticTitle(), Overlay

### Community 18 - "load_pool"
Cohesion: 0.20
Nodes (7): write_json(), contact_sheets(), load_pool(), pool_folder(), save_pool(), test_pool_roundtrip(), test_pool_rows_without_thumbs()

### Community 19 - "write_scripts"
Cohesion: 0.10
Nodes (25): prepare_topic(), limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai() (+17 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "blender_plan.py"
Cohesion: 0.20
Nodes (5): ending(), panels(), pick(), thumbnail_order(), test_thumbnail_order_skips_film_and_puts_openers_first()

### Community 22 - "gpu.py"
Cohesion: 0.06
Nodes (24): comfy_call(), cosy_instruct(), cover_crop(), cut_owner_clip(), gemini_images(), h3_prompts(), local_clips(), local_job() (+16 more)

### Community 24 - "wm_files"
Cohesion: 0.22
Nodes (5): article_images(), commons_search(), thumb_url(), usable_license(), wm_files()

### Community 25 - "test_blender_render.py"
Cohesion: 0.22
Nodes (12): peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises(), test_frames_are_trimmed_after_the_clips_are_cut() (+4 more)

### Community 26 - "test_opener_graphic.py"
Cohesion: 0.17
Nodes (6): weak_opener_graphic(), use_opener(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), test_weak_opener_graphic_fixes_then_handoff()

### Community 27 - "frame_maker"
Cohesion: 0.09
Nodes (12): ClipReader, draw_card(), draw_graphic(), fit_font(), frame_maker(), frame(), graphic_overlay(), person_card() (+4 more)

### Community 28 - "full_cues"
Cohesion: 0.07
Nodes (21): sfx_events(), scene_cues(), full_props(), full_cues(), spoken_at(), spoken_span(), _board(), _jpg() (+13 more)

### Community 29 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 30 - "look.py"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (23): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+15 more)

### Community 32 - "clean_full"
Cohesion: 0.15
Nodes (10): clean_full(), number_figures(), show_number(), test_clean_full_board(), test_clean_full_document(), test_clean_full_journey(), test_clean_full_keeps_thing(), test_clean_full_limits() (+2 more)

### Community 33 - "render_remotion"
Cohesion: 0.10
Nodes (13): short_skin(), ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props() (+5 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "gather_pool"
Cohesion: 0.09
Nodes (8): gather_pool(), owner(), _fake_planning(), test_director_prompt_mentions_full(), film(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 36 - "style_library"
Cohesion: 0.13
Nodes (12): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), test_invented_look_needs_fallback() (+4 more)

### Community 37 - "run_draft"
Cohesion: 0.19
Nodes (9): draft_rules(), require_rules(), draft_reply(), run_draft(), test_draft_blender_channel_needs_build_plan(), test_draft_never_overwrites(), test_draft_retries_once_then_stops(), test_draft_settings_come_from_code() (+1 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "words_of"
Cohesion: 0.32
Nodes (5): fill_money_graphics(), is_person_portrait(), words_of(), test_fill_money_graphics_and_caps(), test_clean_full_keeps_board_pic()

### Community 40 - "default_build"
Cohesion: 0.29
Nodes (4): default_build(), plan_builds(), test_plan_builds_retries_then_defaults(), ask()

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), Background(), Card, flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "look_and_fix"
Cohesion: 0.38
Nodes (3): look_and_fix(), preview_custom(), preview_sheet()

### Community 44 - "subprocess"
Cohesion: 0.08
Nodes (17): freesound_fetch(), music_gain(), speak(), story_sound(), tts(), shot_span(), split_takes(), duration() (+9 more)

### Community 45 - "rescue_graphics"
Cohesion: 0.22
Nodes (5): full_formats(), rescue_graphics(), max_full(), max_full_planned(), test_rescue_respects_caps()

### Community 47 - "Halftone.tsx"
Cohesion: 0.19
Nodes (20): drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw(), Engraving() (+12 more)

### Community 48 - "re"
Cohesion: 0.07
Nodes (16): log_short(), vault_page(), vault_refresh(), parse_scene_money(), clean_style_code(), clash(), fetch_ideas(), pages() (+8 more)

### Community 49 - "invent_component"
Cohesion: 0.15
Nodes (9): invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), swap_inventions(), test_invention_lint_failure_uses_fallback(), test_placeholders_match_the_slots() (+1 more)

### Community 50 - "test_style.py"
Cohesion: 0.14
Nodes (10): wants_remotion(), apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics() (+2 more)

### Community 51 - "main"
Cohesion: 0.10
Nodes (15): ask_count(), ask_yes(), load_channel(), new_channel(), pick_channel(), save_channel(), use_channel(), main() (+7 more)

### Community 52 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 53 - "test_first_second.py"
Cohesion: 0.08
Nodes (23): logbook_results(), apply_review_fixes(), swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples() (+15 more)

### Community 54 - "gemini_model"
Cohesion: 0.40
Nodes (4): gemini_model(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_gemini_timeout_switches_to_flash()

### Community 55 - "style_placeholders"
Cohesion: 0.21
Nodes (9): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_slots_restored_after_render() (+1 more)

### Community 56 - "run_agy"
Cohesion: 0.33
Nodes (3): quota_exhausted(), run_agy(), test_run_agy_flags_and_boundaries()

### Community 57 - "test_pictures_first.py"
Cohesion: 0.21
Nodes (14): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+6 more)

### Community 58 - "redraw_custom"
Cohesion: 0.33
Nodes (3): clean_tsx_code(), custom_rules(), redraw_custom()

### Community 59 - "capture_prompts"
Cohesion: 0.20
Nodes (6): load_rules(), min_real_pictures(), capture_prompts(), ask(), test_load_rules_sets_session(), test_strange_history_prompts_unchanged()

### Community 60 - "math"
Cohesion: 0.13
Nodes (6): radians(), make_sfx(), clamp(), flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 61 - "ask_brain"
Cohesion: 0.40
Nodes (3): ask_brain(), ask_number(), test_solo_brain_selection_options()

### Community 62 - "clean_graphic"
Cohesion: 0.50
Nodes (4): clean_graphic(), coords(), is_num(), test_clean_question_and_kinetic()

### Community 63 - "clean_sound"
Cohesion: 0.29
Nodes (5): clean_sound(), limit_sounds(), word(), contains(), test_clean_sound()

### Community 66 - "pool_pictures"
Cohesion: 0.12
Nodes (8): film_piece(), film_ffmpeg(), get_image(), openverse_images(), ov_get(), full_pictures(), pool_pictures(), test_board_pictures_attached()

### Community 69 - "edit_scripts"
Cohesion: 0.12
Nodes (9): catalog_text(), is_usable(), pictures_of(), usable(), direct_scripts(), edit_scripts(), length_plan(), narration_lines() (+1 more)

### Community 70 - "fix_short"
Cohesion: 0.20
Nodes (7): fix_short(), use_picture_from(), paint_new(), test_fix_bat_explains_a_drawn_short(), test_new_picture_drops_mark(), test_paint_new_clears_full(), test_fix_checks_rules_before_asking_for_a_scene()

### Community 72 - "test_story.py"
Cohesion: 0.06
Nodes (33): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+25 more)

### Community 77 - "trend_research"
Cohesion: 0.29
Nodes (4): channel_url(), seed_ideas(), trend_research(), yt_list()

### Community 78 - "drawn_thumbnail"
Cohesion: 0.23
Nodes (9): scene_frames(), drawn_thumbnail(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 85 - "render"
Cohesion: 0.06
Nodes (25): short_credit(), clock(), full_summary(), graphics_count(), clean_photo(), to_vertical(), mark_details(), first_second_check() (+17 more)

### Community 86 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `test_full_scenes.py`, `json`, `make`, `gpu.py`, `test_blender_render.py`, `test_opener_graphic.py`, `frame_maker`, `full_cues`, `captions`, `render_remotion`, `subprocess`, `rescue_graphics`, `re`, `test_style.py`, `main`, `edit_plan`, `test_first_second.py`, `test_pictures_first.py`, `math`, `srt`, `fix_short`, `drawn_thumbnail`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.14204545454545456 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `json`, `build_scene.py`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Should `pool_of` be split into smaller, more focused modules?**
  _Cohesion score 0.13227513227513227 - nodes in this community are weakly interconnected._
- **Why does `choose_images()` connect `test_pictures_first.py` to `pool_pictures`, `gather_pool`, `ask_ai`, `style_library`, `test_full_scenes.py`, `words_of`, `json`, `load_pool`, `main`, `test_style.py`, `render`, `capture_prompts`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Should `h3_run.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11462450592885376 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._