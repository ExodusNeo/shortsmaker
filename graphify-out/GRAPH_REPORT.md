# Graph Report - ShortsMaker  (2026-10-27)

## Corpus Check
- 124 files · ~145,539 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 2046 nodes · 5386 edges · 83 communities (75 shown, 8 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 125 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b89cd969`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- shutil
- toolkit.tsx
- ask_ai
- split_make_shorts.py
- test_full_scenes.py
- test_h3_handoff.py
- test_opener_scene.py
- Paper
- ffmpeg
- gpu.py
- moves.py
- guarded.tsx
- make
- test_rules.py
- Journey.tsx
- BigNumber.tsx
- test_pictures_first.py
- write_scripts
- Local GPU Worker
- words_of
- test_blender_run.py
- paint_instead
- render_remotion
- test_blender_render.py
- fake_ai
- frame_render.py
- look.py
- clean_full
- first_second_check
- parts.py
- people.py
- catalog_pool
- templates.py
- captions
- test_story.py
- scene_cues
- math
- h3_run.py
- music_gain
- main
- Short.tsx
- sys
- test_opener_plan.py
- cut
- use_picture_from
- Halftone.tsx
- fetch
- blender_link.py
- gather_pool
- json
- Shots
- test_first_second.py
- wm_get
- scene_kit.py
- log_short
- choose_images
- test_opener_render.py
- pack_people.py
- test_opener_checks.py
- opener_checks.py
- blender_note
- opener_scene.py
- look_toon.py
- edit_plan
- rescue_graphics
- pictures_of
- test_blender_scene.py
- owner
- test_style.py
- use_opener
- test_local_job_retries_a_hard_crash
- review
- trim_borders
- pick_model
- Fake
- test_short_credit
- limit_style
- copy
- on_topic
- render
- test_every_unfound_model_named_at_once

## God Nodes (most connected - your core abstractions)
1. `render()` - 62 edges
2. `write_scripts()` - 45 edges
3. `ask_ai()` - 39 edges
4. `render_opener()` - 34 edges
5. `run()` - 31 edges
6. `cut()` - 30 edges
7. `skinOf()` - 29 edges
8. `fixture()` - 29 edges
9. `main()` - 27 edges
10. `Env` - 26 edges

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

## Communities (83 total, 8 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "shutil"
Cohesion: 0.11
Nodes (15): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+7 more)

### Community 3 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 4 - "ask_ai"
Cohesion: 0.08
Nodes (19): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), mark_details(), direct_scripts(), fact_check(), test_fact_check_drops_full() (+11 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "test_full_scenes.py"
Cohesion: 0.11
Nodes (4): code_version(), short_skin(), fingerprint(), test_clean_full_custom_and_skin()

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.11
Nodes (27): fake_ai(), handoff(), short_with(), test_all_closeup_marked_scenes_skip_pause(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated(), test_flagged_start_picture_is_not_sent(), test_handoff_picks_up_clips_zip() (+19 more)

### Community 8 - "test_opener_scene.py"
Cohesion: 0.06
Nodes (35): builds(), fixture(), people_lib(), run(), test_bad_plans_fail(), test_box_fall_rests_and_renders(), test_camera_follows_unasked(), test_chicken_chop_reference() (+27 more)

### Community 9 - "Paper"
Cohesion: 0.13
Nodes (28): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+20 more)

### Community 10 - "ffmpeg"
Cohesion: 0.11
Nodes (12): shot_span(), local_voice(), sentence_groups(), split_takes(), spoken_count(), voicestudio_unload(), voicestudio_up(), duration() (+4 more)

### Community 11 - "gpu.py"
Cohesion: 0.10
Nodes (16): comfy_call(), cover_crop(), cut_owner_clip(), h3_problems(), h3_prompt(), h3_prompts(), local_clips(), local_job() (+8 more)

### Community 12 - "moves.py"
Cohesion: 0.11
Nodes (24): apply(), clear_distance_at_end(), fall(), fly_off(), gait(), hop_off(), legs(), push() (+16 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 14 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (40): load_rules(), min_real_pictures(), parse_rules(), test_channels_have_opener_rules(), capture_prompts(), ask(), draft_reply(), make() (+32 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "BigNumber.tsx"
Cohesion: 0.20
Nodes (14): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+6 more)

### Community 18 - "test_pictures_first.py"
Cohesion: 0.19
Nodes (19): clean_pics(), entry(), film(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film(), test_both_mode_reuses_pools() (+11 more)

### Community 19 - "write_scripts"
Cohesion: 0.12
Nodes (19): limit_full(), edit_scripts(), length_plan(), narration_lines(), write_scripts(), test_limit_full(), test_solo_edit_scripts_uses_same_ai(), passing() (+11 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "words_of"
Cohesion: 0.16
Nodes (9): clean_sound(), limit_sounds(), fill_money_graphics(), is_person_portrait(), parse_scene_money(), words_of(), test_clean_sound(), test_fill_money_graphics_and_caps() (+1 more)

### Community 22 - "test_blender_run.py"
Cohesion: 0.24
Nodes (8): drawn_thumbnail(), drawn_short(), jpeg(), test_blender_failure_is_reported_and_the_batch_goes_on(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so(), test_thumbnail_uses_the_real_photo()

### Community 23 - "paint_instead"
Cohesion: 0.18
Nodes (4): gemini_images(), to_vertical(), paint_instead(), test_remotion_failure_paints()

### Community 24 - "render_remotion"
Cohesion: 0.11
Nodes (13): hex_rgb(), luminance(), ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback() (+5 more)

### Community 25 - "test_blender_render.py"
Cohesion: 0.15
Nodes (15): BlenderFailed, peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws() (+7 more)

### Community 26 - "fake_ai"
Cohesion: 0.20
Nodes (5): fake_ai, planning_ai(), reply(), test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list()

### Community 27 - "frame_render.py"
Cohesion: 0.07
Nodes (17): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+9 more)

### Community 28 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 29 - "clean_full"
Cohesion: 0.14
Nodes (15): clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number() (+7 more)

### Community 30 - "first_second_check"
Cohesion: 0.14
Nodes (10): clock(), first_second_check(), overlay_notes(), quality_check(), review_fixes(), storyboard(), visual_review(), test_review_is_told_the_drawings_are_deliberate() (+2 more)

### Community 31 - "parts.py"
Cohesion: 0.16
Nodes (20): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+12 more)

### Community 32 - "people.py"
Cohesion: 0.08
Nodes (20): _append(), _attach(), _bake_free(), base_name(), _body_tree(), _clip(), _colour(), dress() (+12 more)

### Community 33 - "catalog_pool"
Cohesion: 0.13
Nodes (13): write_json(), catalog_entries(), catalog_pool(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool() (+5 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 36 - "test_story.py"
Cohesion: 0.07
Nodes (26): align(), align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak(), check_twists() (+18 more)

### Community 37 - "scene_cues"
Cohesion: 0.06
Nodes (25): sfx_events(), scene_cues(), full_props(), full_summary(), full_pictures(), full_cues(), spoken_at(), spoken_span() (+17 more)

### Community 38 - "math"
Cohesion: 0.10
Nodes (6): make_sfx(), body(), clip(), key(), main(), part()

### Community 39 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 40 - "music_gain"
Cohesion: 0.14
Nodes (8): music_gain(), speak(), story_sound(), tts(), test_music_gain_evens_out_tracks(), test_story_sound_library(), fetch(), _tone_wav()

### Community 41 - "main"
Cohesion: 0.16
Nodes (5): keyvis(), main(), Failure, key(), focus_object()

### Community 42 - "Short.tsx"
Cohesion: 0.13
Nodes (19): Captions(), PersonCard(), Root(), Background(), flashAlpha(), GraphicFor(), Move, Scene (+11 more)

### Community 43 - "sys"
Cohesion: 0.09
Nodes (4): main(), build(), add(), main()

### Community 44 - "test_opener_plan.py"
Cohesion: 0.09
Nodes (33): clean_opener(), _expect(), fix_plan(), _num(), plan_openers(), ask(), _size(), _stroke() (+25 more)

### Community 45 - "cut"
Cohesion: 0.07
Nodes (27): bm_area(), box_of(), centre(), clear_distance(), clusters(), cut(), edge_point_local(), half() (+19 more)

### Community 46 - "use_picture_from"
Cohesion: 0.29
Nodes (4): use_picture_from(), paint_new(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "fetch"
Cohesion: 0.09
Nodes (12): crop_film_bytes(), film_frames(), film_piece(), nasa_films(), film_ffmpeg(), get_image(), nasa_images(), nasa_search() (+4 more)

### Community 49 - "blender_link.py"
Cohesion: 0.10
Nodes (21): allowed_licence(), attribution(), call(), credit(), fetch_model(), in_library(), LinkError, ping() (+13 more)

### Community 50 - "gather_pool"
Cohesion: 0.20
Nodes (5): article_images(), commons_search(), thumb_url(), wm_files(), gather_pool()

### Community 51 - "json"
Cohesion: 0.06
Nodes (30): main(), freesound_fetch(), ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel() (+22 more)

### Community 52 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 53 - "test_first_second.py"
Cohesion: 0.08
Nodes (23): logbook_results(), apply_review_fixes(), swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples() (+15 more)

### Community 54 - "wm_get"
Cohesion: 0.25
Nodes (4): commons_films(), usable_license(), wm_get(), article_text()

### Community 55 - "scene_kit.py"
Cohesion: 0.09
Nodes (16): add_body(), ensure_world(), fcurves(), fcurves_of(), interpolation(), key_vis(), layers(), leg_rig() (+8 more)

### Community 56 - "log_short"
Cohesion: 0.29
Nodes (3): log_short(), vault_page(), vault_refresh()

### Community 57 - "choose_images"
Cohesion: 0.19
Nodes (14): choose_images(), apply_look_scenes(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+6 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.17
Nodes (24): render_opener(), Env, _people_files(), short(), test_beats_scaled_into_scene(), test_cc_by_credit(), test_crash_retry_then_fallback(), test_failed_checks_fix_then_fallback() (+16 more)

### Community 59 - "pack_people.py"
Cohesion: 0.26
Nodes (6): base_name(), clip_name(), front(), height(), main(), stride()

### Community 60 - "test_opener_checks.py"
Cohesion: 0.33
Nodes (9): results(), test_blade_face(), test_cut_result(), test_edge_leads(), test_first_frame(), test_hidden(), test_in_frame(), test_overlap() (+1 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.11
Nodes (17): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+9 more)

### Community 63 - "opener_scene.py"
Cohesion: 0.09
Nodes (21): State, in_frame(), build_set(), camera(), checks(), dress_set(), first_hit(), ground_material() (+13 more)

### Community 64 - "look_toon.py"
Cohesion: 0.27
Nodes (4): apply(), ink(), outline(), toon()

### Community 65 - "edit_plan"
Cohesion: 0.33
Nodes (3): edit_plan(), picture_line(), test_edit_plan_picture_line()

### Community 66 - "rescue_graphics"
Cohesion: 0.29
Nodes (4): rescue_graphics(), max_full(), max_full_planned(), test_rescue_respects_caps()

### Community 67 - "pictures_of"
Cohesion: 0.29
Nodes (4): catalog_text(), is_usable(), pictures_of(), usable()

### Community 68 - "test_blender_scene.py"
Cohesion: 0.07
Nodes (42): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+34 more)

### Community 69 - "owner"
Cohesion: 0.11
Nodes (10): owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits(), plan_with(), ask() (+2 more)

### Community 70 - "test_style.py"
Cohesion: 0.05
Nodes (47): cut_text(), look_text(), clean_invention(), clean_look(), clean_transition(), settle_style(), approve_candidate(), clean_style_code() (+39 more)

### Community 71 - "use_opener"
Cohesion: 0.22
Nodes (6): use_opener(), test_use_opener_failure_keeps_scene(), test_use_opener_never_raises(), test_use_opener_on_success(), test_use_opener_planner_check(), _wiring()

### Community 73 - "review"
Cohesion: 0.22
Nodes (4): _cast_note(), review(), review_frames(), test_review_frames_include_key_moments()

### Community 74 - "trim_borders"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 83 - "on_topic"
Cohesion: 0.25
Nodes (4): archive_films(), archive_images(), on_topic(), test_on_topic_ignores_a_lone_shared_name()

### Community 85 - "render"
Cohesion: 0.11
Nodes (10): short_credit(), video_encoder(), graphics_count(), wants_remotion(), srt(), drawn_choices(), render(), test_drawn_choices_have_no_pictures() (+2 more)

## Knowledge Gaps
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `templates.py`, `math`, `json`, `Shots`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12802275960170698 - nodes in this community are weakly interconnected._
- **Why does `fake_ai` connect `fake_ai` to `catalog_pool`, `test_pictures_first.py`, `owner`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `shutil`, `ask_ai`, `test_full_scenes.py`, `ffmpeg`, `gpu.py`, `make`, `test_blender_run.py`, `paint_instead`, `render_remotion`, `test_blender_render.py`, `frame_render.py`, `first_second_check`, `captions`, `scene_cues`, `math`, `music_gain`, `json`, `test_first_second.py`, `choose_images`, `opener_scene.py`, `edit_plan`, `rescue_graphics`, `test_style.py`, `use_opener`, `trim_borders`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `shutil` be split into smaller, more focused modules?**
  _Cohesion score 0.11397849462365592 - nodes in this community are weakly interconnected._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.0773109243697479 - nodes in this community are weakly interconnected._