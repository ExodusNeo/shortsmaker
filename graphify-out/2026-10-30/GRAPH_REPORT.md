# Graph Report - ShortsMaker  (2026-10-30)

## Corpus Check
- 129 files · ~156,361 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 2164 nodes · 5701 edges · 85 communities (79 shown, 6 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 129 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9a94bd18`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- fake_ai
- h3_run.py
- ask_ai
- split_make_shorts.py
- pathlib
- test_package.py
- test_opener_scene.py
- guarded.tsx
- toolkit.tsx
- test_h3_handoff.py
- moves.py
- test_style.py
- make
- make
- Journey.tsx
- Custom3.tsx
- test_pictures_first.py
- write_scripts
- Local GPU Worker
- re
- local_clips
- skinOf
- BigNumber.tsx
- test_blender_render.py
- use_opener
- frame_maker
- test_full_scenes.py
- captions
- look.py
- parts.py
- scene_kit.py
- render_remotion
- templates.py
- json
- test_blender_link.py
- test_rules.py
- review
- ffmpeg
- load_model
- main
- Short.tsx
- subprocess
- test_opener_plan.py
- cut
- catalog_pool
- Halftone.tsx
- test_topic_ideas.py
- blender_link.py
- owner
- main
- edit_plan
- test_first_second.py
- visual_review
- math
- tree
- choose_images
- test_opener_render.py
- pack_people.py
- test_blender_scene.py
- opener_checks.py
- capture_prompts
- opener_scene.py
- bpy
- ask
- film_piece
- sfx_events
- use_picture_from
- edit_scripts
- apply_review_fixes
- limit_style
- test_story.py
- people_standin.py
- test_opener_checks.py
- test_weak_opener_graphic_fixes_then_handoff
- ask_brain
- trend_research
- drawn_thumbnail
- paint_instead
- draft_rules
- test_review_redraws_custom
- test_every_unfound_model_named_at_once
- render
- trim_borders

## God Nodes (most connected - your core abstractions)
1. `render()` - 64 edges
2. `write_scripts()` - 49 edges
3. `ask_ai()` - 40 edges
4. `render_opener()` - 33 edges
5. `run()` - 33 edges
6. `skinOf()` - 31 edges
7. `fixture()` - 31 edges
8. `cut()` - 29 edges
9. `main()` - 27 edges
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
- 5-file cycle: `shortsmaker/blender_render.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py -> shortsmaker/opener_render.py -> shortsmaker/blender_render.py`

## Communities (85 total, 6 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "fake_ai"
Cohesion: 0.20
Nodes (7): logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_never_sees_competitor_titles()

### Community 3 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 4 - "ask_ai"
Cohesion: 0.09
Nodes (16): seed_ideas(), ask_ai(), gemini_model(), quota_exhausted(), run_agy(), mark_details(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash() (+8 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "pathlib"
Cohesion: 0.12
Nodes (3): hex_rgb(), luminance(), short_skin()

### Community 7 - "test_package.py"
Cohesion: 0.08
Nodes (18): scene_cues(), clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom() (+10 more)

### Community 8 - "test_opener_scene.py"
Cohesion: 0.06
Nodes (37): builds(), fixture(), people_lib(), run(), test_bad_plans_fail(), test_box_fall_rests_and_renders(), test_camera_follows_unasked(), test_chicken_chop_reference() (+29 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.15
Nodes (15): Box, boxAt(), clamp, fitCard(), hits(), layoutColumn(), layoutGrid(), layoutRow() (+7 more)

### Community 10 - "toolkit.tsx"
Cohesion: 0.09
Nodes (36): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+28 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "moves.py"
Cohesion: 0.13
Nodes (22): apply(), clear_distance_at_end(), fall(), fly_off(), gait(), hop_off(), legs(), push() (+14 more)

### Community 13 - "test_style.py"
Cohesion: 0.06
Nodes (29): cut_text(), look_text(), tsc_check(), save_try(), prune_cache(), approve_candidate(), clean_style_code(), library_menu() (+21 more)

### Community 14 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "make"
Cohesion: 0.17
Nodes (19): parse_rules(), make(), stop_text(), test_bad_min_pictures_stops(), test_blender_needs_a_build_plan_section(), test_bom_and_crlf_load_the_same(), test_draft_stops(), test_duplicate_heading_stops() (+11 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "Custom3.tsx"
Cohesion: 0.28
Nodes (15): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), appear(), CalloutTag(), clamp (+7 more)

### Community 18 - "test_pictures_first.py"
Cohesion: 0.17
Nodes (20): entry(), film(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film(), test_both_mode_reuses_pools(), test_catalog_both_empty_stops_uncached() (+12 more)

### Community 19 - "write_scripts"
Cohesion: 0.12
Nodes (21): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+13 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "re"
Cohesion: 0.06
Nodes (27): clean_sound(), freesound_fetch(), limit_sounds(), vault_page(), vault_refresh(), word(), clean_graphic(), clean_invention() (+19 more)

### Community 22 - "local_clips"
Cohesion: 0.10
Nodes (13): cosy_instruct(), cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt() (+5 more)

### Community 23 - "skinOf"
Cohesion: 0.21
Nodes (11): ExampleChain(), ExampleEvidence(), Card(), Connect(), photoBox(), travel(), Paper(), skinOf() (+3 more)

### Community 24 - "BigNumber.tsx"
Cohesion: 0.24
Nodes (12): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+4 more)

### Community 25 - "test_blender_render.py"
Cohesion: 0.15
Nodes (14): BlenderFailed, code_version(), peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws() (+6 more)

### Community 26 - "use_opener"
Cohesion: 0.11
Nodes (11): use_opener(), test_use_opener_clip_after_blender_failed(), test_use_opener_failure_keeps_scene(), test_use_opener_failure_not_rebuilt(), test_use_opener_never_raises(), test_use_opener_no_template_ai_clip(), test_use_opener_no_template_note(), test_use_opener_on_success() (+3 more)

### Community 27 - "frame_maker"
Cohesion: 0.06
Nodes (17): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+9 more)

### Community 28 - "test_full_scenes.py"
Cohesion: 0.06
Nodes (33): full_props(), full_summary(), full_formats(), full_pictures(), opener_graphic(), rescue_graphics(), clean_full(), full_cues() (+25 more)

### Community 29 - "captions"
Cohesion: 0.09
Nodes (13): ass_time(), caption_lines(), captions(), styled(), music_gain(), speak(), story_sound(), tts() (+5 more)

### Community 30 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 32 - "scene_kit.py"
Cohesion: 0.14
Nodes (12): add_body(), ensure_world(), fcurves(), fcurves_of(), interpolation(), layers(), leg_rig(), loc_at() (+4 more)

### Community 33 - "render_remotion"
Cohesion: 0.06
Nodes (28): ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), invent_component(), attempt() (+20 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "json"
Cohesion: 0.05
Nodes (32): archive_films(), commons_films(), crop_film_bytes(), film_frames(), nasa_films(), pixabay_films(), comfy_call(), moss_graph() (+24 more)

### Community 36 - "test_blender_link.py"
Cohesion: 0.18
Nodes (12): Fake, _fetch_replies(), execute(), ok(), test_download_error_cleans_up(), test_fetch_saves_pair(), test_in_library(), test_ping_on_off() (+4 more)

### Community 37 - "test_rules.py"
Cohesion: 0.23
Nodes (11): draft_reply(), run_draft(), StopPicker, test_draft_blender_channel_needs_build_plan(), test_draft_keeps_ai_headings_inside_their_section(), test_draft_never_overwrites(), test_draft_retries_once_then_stops(), test_draft_settings_come_from_code() (+3 more)

### Community 38 - "review"
Cohesion: 0.18
Nodes (5): _cast_note(), review(), review_frames(), to_glb(), test_review_frames_include_key_moments()

### Community 39 - "ffmpeg"
Cohesion: 0.19
Nodes (8): split_takes(), spoken_count(), duration(), ffmpeg(), is_loop_short(), first_second_check(), test_a_take_is_cut_between_the_scenes_words(), test_word_counts_match_the_aligner()

### Community 40 - "load_model"
Cohesion: 0.25
Nodes (4): ground_material(), load_model(), material(), merge()

### Community 41 - "main"
Cohesion: 0.10
Nodes (7): direction(), keyloc(), keyvis(), main(), Shots, Failure, key()

### Community 42 - "Short.tsx"
Cohesion: 0.13
Nodes (19): Captions(), PersonCard(), Root(), Background(), flashAlpha(), GraphicFor(), Move, Scene (+11 more)

### Community 43 - "subprocess"
Cohesion: 0.07
Nodes (10): align(), main(), studio_speak(), shot_span(), scale_beats(), storyboard(), main(), main() (+2 more)

### Community 44 - "test_opener_plan.py"
Cohesion: 0.07
Nodes (38): clean_opener(), _expect(), fill_template(), _keep(), _num(), plan_openers(), ask(), _size() (+30 more)

### Community 45 - "cut"
Cohesion: 0.07
Nodes (25): bm_area(), box_of(), centre(), clusters(), cut(), edge_point_local(), half(), handle_end_local() (+17 more)

### Community 46 - "catalog_pool"
Cohesion: 0.15
Nodes (12): write_json(), catalog_entries(), catalog_pool(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool() (+4 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "test_topic_ideas.py"
Cohesion: 0.15
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 49 - "blender_link.py"
Cohesion: 0.11
Nodes (13): allowed_licence(), attribution(), call(), credit(), fetch_model(), in_library(), LinkError, ping() (+5 more)

### Community 50 - "owner"
Cohesion: 0.10
Nodes (11): owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits(), plan_with(), ask() (+3 more)

### Community 51 - "main"
Cohesion: 0.10
Nodes (17): ask_count(), ask_yes(), load_channel(), new_channel(), pick_channel(), save_channel(), use_channel(), blender_note() (+9 more)

### Community 52 - "edit_plan"
Cohesion: 0.33
Nodes (3): edit_plan(), picture_line(), test_edit_plan_picture_line()

### Community 53 - "test_first_second.py"
Cohesion: 0.22
Nodes (12): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once(), test_opener_must_be_a_later_real_picture() (+4 more)

### Community 54 - "visual_review"
Cohesion: 0.18
Nodes (8): log_short(), clock(), overlay_notes(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 55 - "math"
Cohesion: 0.06
Nodes (29): _append(), _attach(), _bake_free(), base_name(), _body_tree(), _clearance(), _clip(), _colour() (+21 more)

### Community 56 - "tree"
Cohesion: 0.25
Nodes (4): clear_distance(), travel(), surface_z(), tree()

### Community 57 - "choose_images"
Cohesion: 0.17
Nodes (15): choose_images(), is_person_portrait(), apply_look_scenes(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded() (+7 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.17
Nodes (22): render_opener(), Env, _people_files(), short(), test_beats_scaled_into_scene(), test_cc_by_credit(), test_crash_retry_then_fallback(), test_failed_checks_fall_back_and_the_try_is_kept() (+14 more)

### Community 59 - "pack_people.py"
Cohesion: 0.26
Nodes (6): base_name(), clip_name(), front(), height(), main(), stride()

### Community 60 - "test_blender_scene.py"
Cohesion: 0.07
Nodes (42): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+34 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.08
Nodes (21): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+13 more)

### Community 62 - "capture_prompts"
Cohesion: 0.18
Nodes (7): load_rules(), min_real_pictures(), test_channels_have_opener_rules(), capture_prompts(), ask(), test_load_rules_sets_session(), test_strange_history_prompts_unchanged()

### Community 63 - "opener_scene.py"
Cohesion: 0.08
Nodes (23): State, beat_actors(), build_set(), camera(), dress_set(), first_hit(), hold_offscreen(), main() (+15 more)

### Community 64 - "bpy"
Cohesion: 0.19
Nodes (4): apply(), ink(), outline(), toon()

### Community 65 - "ask"
Cohesion: 0.22
Nodes (4): ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 67 - "sfx_events"
Cohesion: 0.33
Nodes (3): sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 68 - "use_picture_from"
Cohesion: 0.33
Nodes (3): use_picture_from(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 69 - "edit_scripts"
Cohesion: 0.12
Nodes (9): catalog_text(), clean_pics(), is_usable(), pictures_of(), usable(), edit_scripts(), length_plan(), narration_lines() (+1 more)

### Community 70 - "apply_review_fixes"
Cohesion: 0.20
Nodes (5): apply_review_fixes(), paint_new(), pool_pictures(), quality_check(), test_auto_fix_graphic()

### Community 72 - "test_story.py"
Cohesion: 0.07
Nodes (26): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), sentence_groups(), check_twists(), story_problems() (+18 more)

### Community 73 - "people_standin.py"
Cohesion: 0.29
Nodes (5): body(), clip(), key(), main(), part()

### Community 74 - "test_opener_checks.py"
Cohesion: 0.30
Nodes (10): results(), test_blade_face(), test_cut_result(), test_edge_leads(), test_first_frame(), test_hidden(), test_in_frame(), test_moves_visibly() (+2 more)

### Community 76 - "ask_brain"
Cohesion: 0.40
Nodes (3): ask_brain(), ask_number(), test_solo_brain_selection_options()

### Community 77 - "trend_research"
Cohesion: 0.40
Nodes (3): channel_url(), trend_research(), yt_list()

### Community 78 - "drawn_thumbnail"
Cohesion: 0.23
Nodes (9): scene_frames(), drawn_thumbnail(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 81 - "test_review_redraws_custom"
Cohesion: 0.40
Nodes (3): _review_state(), test_redraw_failure_paints(), test_review_redraws_custom()

### Community 85 - "render"
Cohesion: 0.07
Nodes (14): make_sfx(), gemini_images(), short_credit(), graphics_count(), to_vertical(), wants_remotion(), srt(), drawn_choices() (+6 more)

### Community 86 - "trim_borders"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

## Knowledge Gaps
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `ask_ai`, `pathlib`, `test_package.py`, `test_style.py`, `make`, `re`, `local_clips`, `test_blender_render.py`, `use_opener`, `frame_maker`, `test_full_scenes.py`, `captions`, `render_remotion`, `json`, `ffmpeg`, `subprocess`, `main`, `edit_plan`, `visual_review`, `choose_images`, `sfx_events`, `apply_review_fixes`, `test_weak_opener_graphic_fixes_then_handoff`, `drawn_thumbnail`, `paint_instead`, `trim_borders`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12802275960170698 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `json`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._
- **Why does `choose_images()` connect `choose_images` to `film_piece`, `json`, `ask_ai`, `pathlib`, `test_style.py`, `catalog_pool`, `main`, `render`, `test_full_scenes.py`, `capture_prompts`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Should `h3_run.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11462450592885376 - nodes in this community are weakly interconnected._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.09230769230769231 - nodes in this community are weakly interconnected._