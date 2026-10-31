# Graph Report - ShortsMaker  (2026-10-31)

## Corpus Check
- 121 files · ~143,000 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 1866 nodes · 5071 edges · 85 communities (75 shown, 10 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 113 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dbf744d7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- shutil
- test_package.py
- split_make_shorts.py
- json
- code_custom_scenes
- pool_pictures
- guarded.tsx
- k
- test_h3_handoff.py
- gather_pool
- test_style.py
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
- render
- frame_maker
- full_cues
- test_blender_scene.py
- build_scene.py
- parts.py
- drawn_opener.py
- test_full_scenes.py
- templates.py
- test_weak_opener_graphic_fixes_then_handoff
- test_story.py
- full/types.ts
- main
- Paper
- visual_review
- Shots
- Short.tsx
- textures.mjs
- music_gain
- test_blender_render.py
- image_sources.py
- Halftone.tsx
- re
- style_placeholders
- limit_style
- main
- clean_pics
- test_first_second.py
- kit.mjs
- fake_ai
- pick_channel
- choose_images
- style_library
- apply_review_fixes
- full_props
- bean.mjs
- ffmpeg
- popS
- fix_short
- configure_brain
- ref_remotion
- dexter.mjs
- kit_parts.mjs
- capture_prompts
- opener_graphic
- clean_full
- qwen_voice.py
- ask_ai
- drawn_thumbnail
- make_paper
- captions
- invent_component
- require_rules
- StopPicker
- gemini_model
- invent_styles
- style_props
- make_sfx

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 65 edges
3. `write_scripts()` - 51 edges
4. `ask_ai()` - 45 edges
5. `skinOf()` - 29 edges
6. `main()` - 28 edges
7. `clamp()` - 27 edges
8. `ellPts()` - 26 edges
9. `Paper()` - 25 edges
10. `choose_images()` - 24 edges

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

## Communities (85 total, 10 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.14
Nodes (24): write_json(), catalog_entries(), catalog_pool(), save_pool(), entry(), film(), pic_short(), pool_of() (+16 more)

### Community 3 - "shutil"
Cohesion: 0.13
Nodes (10): call(), fit_start(), frames(), graph(), main(), saved_file(), voicestudio_up(), prune_work() (+2 more)

### Community 4 - "test_package.py"
Cohesion: 0.18
Nodes (7): scene_cues(), test_counter_finishes_before_it_leaves(), test_graphic_card_hold_duration(), test_independent_review_falls_back_without_changing_solo_mode(), test_person_card_hold_and_exit_gap(), test_scene_hold_padding(), test_solo_ask_ai_hands_over_when_out_of_credits()

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "json"
Cohesion: 0.09
Nodes (11): freesound_fetch(), channel_url(), save_channel(), seed_ideas(), trend_research(), yt_list(), library_menu(), reject_candidate() (+3 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.12
Nodes (13): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+5 more)

### Community 8 - "pool_pictures"
Cohesion: 0.12
Nodes (8): film_piece(), film_ffmpeg(), get_image(), openverse_images(), ov_get(), full_pictures(), pool_pictures(), test_board_pictures_attached()

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "gather_pool"
Cohesion: 0.12
Nodes (8): gather_pool(), owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits(), test_good_look_check_skips_the_extra_compile()

### Community 13 - "test_style.py"
Cohesion: 0.13
Nodes (12): tsc_check(), approve_candidate(), save_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure() (+4 more)

### Community 14 - "render_remotion"
Cohesion: 0.22
Nodes (7): short_skin(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), test_clean_full_custom_and_skin(), test_invention_runtime_failure_uses_fallback()

### Community 15 - "test_rules.py"
Cohesion: 0.14
Nodes (29): parse_rules(), draft_reply(), make(), run_draft(), stop_text(), test_bad_min_pictures_stops(), test_blender_needs_a_build_plan_section(), test_bom_and_crlf_load_the_same() (+21 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 18 - "prepare_topic"
Cohesion: 0.22
Nodes (7): contact_sheets(), load_pool(), pool_folder(), prepare_topic(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip(), test_small_pool_skips_ai()

### Community 19 - "write_scripts"
Cohesion: 0.11
Nodes (24): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+16 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "gpu.py"
Cohesion: 0.07
Nodes (20): comfy_call(), cover_crop(), cut_owner_clip(), gemini_images(), h3_prompts(), local_clips(), local_job(), moss_graph() (+12 more)

### Community 23 - "make"
Cohesion: 0.15
Nodes (8): caption_layer(), make(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers(), videos()

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.10
Nodes (22): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+14 more)

### Community 26 - "render"
Cohesion: 0.09
Nodes (13): short_credit(), graphics_count(), to_vertical(), wants_remotion(), srt(), drawn_choices(), load_state(), render() (+5 more)

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (15): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+7 more)

### Community 28 - "full_cues"
Cohesion: 0.17
Nodes (7): full_cues(), spoken_at(), spoken_span(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish(), test_opener_graphic()

### Community 29 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 30 - "build_scene.py"
Cohesion: 0.16
Nodes (6): collection(), ink_lines(), linear(), material(), setup(), radians()

### Community 31 - "parts.py"
Cohesion: 0.16
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 32 - "drawn_opener.py"
Cohesion: 0.09
Nodes (17): available(), clean_code(), fingerprint(), lint(), make_opener(), node_run(), review(), sheet_times() (+9 more)

### Community 33 - "test_full_scenes.py"
Cohesion: 0.12
Nodes (4): hex_rgb(), luminance(), fills_frame(), test_short_credit()

### Community 34 - "templates.py"
Cohesion: 0.17
Nodes (15): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge() (+7 more)

### Community 35 - "test_weak_opener_graphic_fixes_then_handoff"
Cohesion: 0.17
Nodes (6): weak_opener_graphic(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), test_weak_opener_graphic_fixes_then_handoff(), use()

### Community 36 - "test_story.py"
Cohesion: 0.06
Nodes (33): sentence_groups(), other_ai(), first_sentence(), check_twists(), cold_read(), edit_scripts(), narration_lines(), story_problems() (+25 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 38 - "main"
Cohesion: 0.18
Nodes (4): keyvis(), main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "visual_review"
Cohesion: 0.11
Nodes (12): clock(), overlay_notes(), quality_check(), review_fixes(), storyboard(), visual_review(), length_plan(), max_seconds() (+4 more)

### Community 41 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "textures.mjs"
Cohesion: 0.25
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "music_gain"
Cohesion: 0.14
Nodes (8): music_gain(), speak(), story_sound(), tts(), test_music_gain_evens_out_tracks(), test_story_sound_library(), fetch(), _tone_wav()

### Community 45 - "test_blender_render.py"
Cohesion: 0.13
Nodes (16): BlenderFailed, code_version(), peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short() (+8 more)

### Community 46 - "image_sources.py"
Cohesion: 0.08
Nodes (18): archive_films(), commons_films(), crop_film_bytes(), film_frames(), nasa_films(), pixabay_films(), archive_images(), article_images() (+10 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "re"
Cohesion: 0.08
Nodes (17): master_gain(), shot_span(), parse_scene_money(), max_full(), max_full_planned(), clean_style_code(), clash(), fetch_ideas() (+9 more)

### Community 49 - "style_placeholders"
Cohesion: 0.21
Nodes (9): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_placeholders_match_the_slots(), test_slots_restored_after_render() (+1 more)

### Community 51 - "main"
Cohesion: 0.10
Nodes (14): ask_brain(), ask_count(), ask_yes(), normalize_brain(), main(), log_short(), vault_page(), vault_refresh() (+6 more)

### Community 52 - "clean_pics"
Cohesion: 0.17
Nodes (6): catalog_text(), clean_pics(), is_usable(), pictures_of(), usable(), direct_scripts()

### Community 53 - "test_first_second.py"
Cohesion: 0.18
Nodes (14): first_second_check(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture() (+6 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 55 - "fake_ai"
Cohesion: 0.19
Nodes (8): logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel(), test_seo_never_sees_competitor_titles()

### Community 56 - "pick_channel"
Cohesion: 0.22
Nodes (5): new_channel(), pick_channel(), use_channel(), draft_rules(), test_new_channel_stops_for_review()

### Community 57 - "choose_images"
Cohesion: 0.18
Nodes (15): load_channel(), choose_images(), apply_look_scenes(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded() (+7 more)

### Community 58 - "style_library"
Cohesion: 0.06
Nodes (23): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), clean_invention(), clean_look(), clean_transition() (+15 more)

### Community 59 - "apply_review_fixes"
Cohesion: 0.15
Nodes (8): apply_review_fixes(), ask(), _review_state(), test_auto_fix_graphic(), test_look_check_fixes_code(), test_redraw_failure_paints(), test_review_redraws_custom(), test_review_uses_unused_pool_pictures_before_painting()

### Community 60 - "full_props"
Cohesion: 0.15
Nodes (9): sfx_events(), full_props(), _board(), _jpg(), test_custom_cues_props_and_pictures(), test_remotion_props_full(), test_sfx_full(), test_story_sound_wins_its_moment() (+1 more)

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "ffmpeg"
Cohesion: 0.23
Nodes (7): cosy_instruct(), local_voice(), split_takes(), duration(), ffmpeg(), is_loop_short(), test_a_take_is_cut_between_the_scenes_words()

### Community 64 - "fix_short"
Cohesion: 0.16
Nodes (8): ask_number(), fix_short(), use_picture_from(), paint_new(), test_fix_bat_explains_a_drawn_short(), test_new_picture_drops_mark(), test_paint_new_clears_full(), test_fix_checks_rules_before_asking_for_a_scene()

### Community 65 - "configure_brain"
Cohesion: 0.24
Nodes (9): configure_brain(), fake_providers(), claude(), reply(), saved_session(), test_all_modes_route_writer_editor_and_reader(), test_every_mode_can_continue_through_two_exhausted_ais(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty() (+1 more)

### Community 69 - "capture_prompts"
Cohesion: 0.20
Nodes (5): rewrite_paint_prompts(), test_rewrite_paint_prompts(), capture_prompts(), ask(), test_strange_history_prompts_unchanged()

### Community 70 - "opener_graphic"
Cohesion: 0.22
Nodes (6): full_summary(), full_formats(), opener_graphic(), fix_opener_graphic(), test_full_props_figure(), test_full_summary()

### Community 71 - "clean_full"
Cohesion: 0.05
Nodes (32): clean_sound(), limit_sounds(), graphic_low(), clean_photo(), is_stereo(), trim_borders(), border(), plain() (+24 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.11
Nodes (15): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+7 more)

### Community 73 - "ask_ai"
Cohesion: 0.11
Nodes (13): ask_ai(), quota_exhausted(), run_agy(), run_codex(), mark_details(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_quota_fallback_both_ways() (+5 more)

### Community 75 - "drawn_thumbnail"
Cohesion: 0.31
Nodes (7): drawn_thumbnail(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so(), test_thumbnail_uses_the_real_photo()

### Community 76 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 77 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 78 - "invent_component"
Cohesion: 0.29
Nodes (5): invent_component(), attempt(), lint_style_code(), style_preview(), test_invention_lint_failure_uses_fallback()

### Community 79 - "require_rules"
Cohesion: 0.29
Nodes (4): load_rules(), min_real_pictures(), require_rules(), test_load_rules_sets_session()

### Community 81 - "gemini_model"
Cohesion: 0.40
Nodes (4): gemini_model(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_gemini_timeout_switches_to_flash()

### Community 82 - "invent_styles"
Cohesion: 0.40
Nodes (3): invent_styles(), swap_inventions(), test_swap_inventions()

## Knowledge Gaps
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `shutil`, `test_package.py`, `test_style.py`, `render_remotion`, `gpu.py`, `make`, `frame_maker`, `test_full_scenes.py`, `test_weak_opener_graphic_fixes_then_handoff`, `visual_review`, `music_gain`, `test_blender_render.py`, `re`, `main`, `test_first_second.py`, `choose_images`, `style_library`, `apply_review_fixes`, `full_props`, `ffmpeg`, `fix_short`, `opener_graphic`, `clean_full`, `ask_ai`, `drawn_thumbnail`, `make_paper`, `captions`, `make_sfx`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `json`, `Shots`, `build_scene.py`, `parts.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14112903225806453 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `test_pictures_first.py`, `shutil`, `test_story.py`, `capture_prompts`, `json`, `clean_full`, `visual_review`, `ask_ai`, `gather_pool`, `re`, `prepare_topic`, `main`, `clean_pics`, `limit_style`, `fake_ai`, `test_blender_plan.py`, `style_library`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Should `shutil` be split into smaller, more focused modules?**
  _Cohesion score 0.12681159420289856 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._