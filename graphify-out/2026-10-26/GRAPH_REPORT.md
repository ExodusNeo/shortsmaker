# Graph Report - ShortsMaker  (2026-10-26)

## Corpus Check
- 105 files · ~114,004 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .canvas 1, .ipynb 1)

## Summary
- 1528 nodes · 4128 edges · 73 communities (68 shown, 5 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 101 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3407d195`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- ask_ai
- toolkit.tsx
- json
- split_make_shorts.py
- __init__.py
- test_h3_handoff.py
- scene_cues
- Paper
- subprocess
- h3_run.py
- motion.py
- guarded.tsx
- Shotcut Timeline and Loudness
- test_rules.py
- Journey.tsx
- BigNumber.tsx
- prepare_topic
- test_pictures_first.py
- Local GPU Worker
- style_library
- math
- Blender Scene Tests
- fetch
- test_blender_plan.py
- speak
- frame_maker
- Edit Plan Text
- write_scripts
- render
- parts.py
- drawn_thumbnail
- test_blender_render.py
- templates.py
- invent_component
- test_story.py
- test_first_second.py
- Blender Ink Look
- AI Clip Prompts and Cuts
- trim_borders
- main
- Short.tsx
- visual_review
- blender_plan.py
- ffmpeg
- test_style.py
- Invented Look Canvas Effects
- gpu.py
- pool_of
- default_build
- re
- build_scene.py
- Style Library Caps
- apply_review_fixes
- fix_short
- BlenderFailed
- choose_images
- edit_scripts
- paint_instead
- style_lab.py
- render_remotion
- gather_pool
- Full Graphic Limits
- test_full_scenes.py
- clean_pics
- wm_files
- owner
- captions
- rescue_graphics
- wants_remotion
- gemini_images

## God Nodes (most connected - your core abstractions)
1. `render()` - 61 edges
2. `write_scripts()` - 44 edges
3. `ask_ai()` - 35 edges
4. `skinOf()` - 29 edges
5. `main()` - 26 edges
6. `Paper()` - 25 edges
7. `choose_images()` - 24 edges
8. `words_of()` - 22 edges
9. `clean_full()` - 21 edges
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
- `test_code_custom_scenes_fallback()` --calls--> `code_custom_scenes()`  [EXTRACTED]
  tests/test_full_scenes.py → shortsmaker/motion.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`

## Communities (73 total, 5 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "ask_ai"
Cohesion: 0.10
Nodes (15): seed_ideas(), ask_ai(), gemini_model(), quota_exhausted(), run_agy(), check_twists(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash() (+7 more)

### Community 3 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 4 - "json"
Cohesion: 0.13
Nodes (11): freesound_fetch(), channel_url(), load_channel(), new_channel(), save_channel(), trend_research(), yt_list(), logbook_results() (+3 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "__init__.py"
Cohesion: 0.13
Nodes (4): ask_brain(), ask_number(), test_fake_reaches_callers(), test_solo_brain_selection_options()

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (32): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_closeup_marked_scenes_skip_pause(), test_all_start_pictures_flagged_skips_pause() (+24 more)

### Community 8 - "scene_cues"
Cohesion: 0.06
Nodes (25): sfx_events(), scene_cues(), full_props(), full_summary(), full_pictures(), full_cues(), spoken_at(), spoken_span() (+17 more)

### Community 9 - "Paper"
Cohesion: 0.13
Nodes (28): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+20 more)

### Community 10 - "subprocess"
Cohesion: 0.09
Nodes (8): music_gain(), film_piece(), shot_span(), voicestudio_up(), film_ffmpeg(), main(), props_for(), test_music_gain_evens_out_tracks()

### Community 11 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 12 - "motion.py"
Cohesion: 0.15
Nodes (11): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+3 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 14 - "Shotcut Timeline and Loudness"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (37): draft_rules(), load_rules(), min_real_pictures(), parse_rules(), require_rules(), capture_prompts(), ask(), draft_reply() (+29 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "BigNumber.tsx"
Cohesion: 0.20
Nodes (14): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+6 more)

### Community 18 - "prepare_topic"
Cohesion: 0.20
Nodes (8): write_json(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_pool_roundtrip(), test_pool_rows_without_thumbs()

### Community 19 - "test_pictures_first.py"
Cohesion: 0.18
Nodes (15): passing(), prepare(), planning, test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), test_dropped_topic_pool_removed(), prepare() (+7 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.13
Nodes (12): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), test_invented_look_needs_fallback() (+4 more)

### Community 22 - "math"
Cohesion: 0.13
Nodes (6): radians(), make_sfx(), clamp(), flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 23 - "Blender Scene Tests"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 24 - "fetch"
Cohesion: 0.12
Nodes (13): archive_films(), commons_films(), nasa_films(), pixabay_films(), archive_images(), get_image(), nasa_images(), nasa_search() (+5 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.30
Nodes (12): clean_build(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults(), test_clean_build_keeps_a_good_plan(), test_default_build_shape(), test_label_is_short_and_upper(), test_nan_and_infinity_get_defaults() (+4 more)

### Community 26 - "speak"
Cohesion: 0.20
Nodes (6): speak(), story_sound(), tts(), test_story_sound_library(), fetch(), _tone_wav()

### Community 27 - "frame_maker"
Cohesion: 0.08
Nodes (13): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), frame_maker(), frame(), graphic_overlay() (+5 more)

### Community 28 - "Edit Plan Text"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 29 - "write_scripts"
Cohesion: 0.09
Nodes (25): clean_sound(), limit_sounds(), graphic_low(), clean_full(), word(), clean_graphic(), contains(), coords() (+17 more)

### Community 30 - "render"
Cohesion: 0.12
Nodes (10): short_credit(), graphics_count(), to_vertical(), srt(), drawn_choices(), load_state(), render(), save_state() (+2 more)

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (23): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+15 more)

### Community 32 - "drawn_thumbnail"
Cohesion: 0.23
Nodes (9): scene_frames(), drawn_thumbnail(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 33 - "test_blender_render.py"
Cohesion: 0.22
Nodes (12): peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises(), test_frames_are_trimmed_after_the_clips_are_cut() (+4 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "invent_component"
Cohesion: 0.12
Nodes (16): invent_component(), attempt(), invent_styles(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others() (+8 more)

### Community 36 - "test_story.py"
Cohesion: 0.07
Nodes (25): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+17 more)

### Community 37 - "test_first_second.py"
Cohesion: 0.22
Nodes (12): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once(), test_opener_must_be_a_later_real_picture() (+4 more)

### Community 38 - "Blender Ink Look"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 39 - "AI Clip Prompts and Cuts"
Cohesion: 0.12
Nodes (11): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), motion_prompt(), start_picture_problems(), veo_handoff() (+3 more)

### Community 40 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

### Community 41 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 42 - "Short.tsx"
Cohesion: 0.13
Nodes (19): Captions(), PersonCard(), Root(), Background(), flashAlpha(), GraphicFor(), Move, Scene (+11 more)

### Community 43 - "visual_review"
Cohesion: 0.24
Nodes (7): clock(), overlay_notes(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 44 - "blender_plan.py"
Cohesion: 0.20
Nodes (5): ending(), panels(), pick(), thumbnail_order(), test_thumbnail_order_skips_film_and_puts_openers_first()

### Community 45 - "ffmpeg"
Cohesion: 0.17
Nodes (9): local_voice(), split_takes(), spoken_count(), voicestudio_unload(), duration(), ffmpeg(), is_loop_short(), test_a_take_is_cut_between_the_scenes_words() (+1 more)

### Community 46 - "test_style.py"
Cohesion: 0.15
Nodes (14): candidate_in(), library_snapshot(), plan_with(), ask(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes() (+6 more)

### Community 47 - "Invented Look Canvas Effects"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "gpu.py"
Cohesion: 0.10
Nodes (9): code_version(), crop_film_bytes(), film_frames(), comfy_call(), moss_graph(), moss_images(), clean_photo(), mark_details() (+1 more)

### Community 49 - "pool_of"
Cohesion: 0.15
Nodes (17): catalog_entries(), catalog_pool(), entry(), fake_ai, pool_of(), test_both_mode_reuses_pools(), test_catalog_both_empty_stops_uncached(), test_catalog_empty_pool_no_ai() (+9 more)

### Community 50 - "default_build"
Cohesion: 0.29
Nodes (4): default_build(), plan_builds(), test_plan_builds_retries_then_defaults(), ask()

### Community 51 - "re"
Cohesion: 0.09
Nodes (16): ask_count(), ask_yes(), pick_channel(), use_channel(), main(), sentence_groups(), log_short(), vault_page() (+8 more)

### Community 52 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 54 - "apply_review_fixes"
Cohesion: 0.10
Nodes (12): apply_review_fixes(), rewrite_paint_prompts(), _fake_planning(), ask(), _review_state(), test_auto_fix_graphic(), test_director_prompt_mentions_full(), test_look_check_fixes_code() (+4 more)

### Community 55 - "fix_short"
Cohesion: 0.11
Nodes (10): fix_short(), use_picture_from(), first_second_check(), paint_new(), pool_pictures(), quality_check(), test_fix_bat_explains_a_drawn_short(), test_new_picture_drops_mark() (+2 more)

### Community 57 - "choose_images"
Cohesion: 0.21
Nodes (13): choose_images(), film(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+5 more)

### Community 58 - "edit_scripts"
Cohesion: 0.18
Nodes (6): pictures_of(), direct_scripts(), edit_scripts(), length_plan(), narration_lines(), test_solo_edit_scripts_uses_same_ai()

### Community 59 - "paint_instead"
Cohesion: 0.20
Nodes (4): ink_silhouette(), paint_instead(), test_ink_silhouette(), test_remotion_failure_paints()

### Community 60 - "style_lab.py"
Cohesion: 0.18
Nodes (7): prune_cache(), prune_work(), approve_candidate(), library_menu(), reject_candidate(), save_candidate(), test_prune_cache_handles_pools()

### Community 61 - "render_remotion"
Cohesion: 0.16
Nodes (9): render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain() (+1 more)

### Community 62 - "gather_pool"
Cohesion: 0.18
Nodes (5): openverse_images(), gather_pool(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 64 - "test_full_scenes.py"
Cohesion: 0.11
Nodes (9): hex_rgb(), luminance(), short_skin(), make_paper(), test_clean_full_custom_and_skin(), test_code_custom_scenes_fallback(), test_lint_custom_code(), test_make_paper() (+1 more)

### Community 65 - "clean_pics"
Cohesion: 0.20
Nodes (8): catalog_text(), clean_pics(), is_usable(), usable(), pic_short(), test_board_item_pics_cleaned(), test_board_item_refuses_film(), test_clean_pics()

### Community 66 - "wm_files"
Cohesion: 0.22
Nodes (5): article_images(), commons_search(), thumb_url(), usable_license(), wm_files()

### Community 67 - "owner"
Cohesion: 0.22
Nodes (3): owner(), planning_ai(), reply()

### Community 68 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 69 - "rescue_graphics"
Cohesion: 0.25
Nodes (5): rescue_graphics(), article_text(), fact_check(), test_fact_check_drops_full(), test_rescue_respects_caps()

### Community 70 - "wants_remotion"
Cohesion: 0.27
Nodes (4): wants_remotion(), apply_look_scenes(), test_apply_look_scenes(), test_remotion_forced_by_look()

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `templates.py`, `json`, `Blender Ink Look`, `build_scene.py`, `parts.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12802275960170698 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `scene_cues`, `subprocess`, `Shotcut Timeline and Loudness`, `math`, `speak`, `frame_maker`, `Edit Plan Text`, `write_scripts`, `drawn_thumbnail`, `test_blender_render.py`, `AI Clip Prompts and Cuts`, `visual_review`, `ffmpeg`, `gpu.py`, `re`, `apply_review_fixes`, `fix_short`, `choose_images`, `paint_instead`, `style_lab.py`, `render_remotion`, `test_full_scenes.py`, `captions`, `rescue_graphics`, `wants_remotion`, `gemini_images`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `clean_pics`, `ask_ai`, `json`, `rescue_graphics`, `__init__.py`, `test_style.py`, `test_rules.py`, `pool_of`, `default_build`, `re`, `prepare_topic`, `style_library`, `Style Library Caps`, `apply_review_fixes`, `test_pictures_first.py`, `edit_scripts`, `style_lab.py`, `Full Graphic Limits`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.10144927536231885 - nodes in this community are weakly interconnected._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.1286549707602339 - nodes in this community are weakly interconnected._