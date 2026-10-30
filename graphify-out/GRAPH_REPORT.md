# Graph Report - ShortsMaker  (2026-10-30)

## Corpus Check
- 129 files · ~156,209 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 2162 nodes · 5698 edges · 82 communities (76 shown, 6 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 129 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e9553c57`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- re
- write_scripts
- ask_ai
- split_make_shorts.py
- pathlib
- shutil
- test_opener_scene.py
- guarded.tsx
- Paper
- test_h3_handoff.py
- moves.py
- test_style.py
- ffmpeg
- test_rules.py
- Journey.tsx
- toolkit.tsx
- test_pictures_first.py
- planning
- Local GPU Worker
- clean_look
- local_clips
- plan_rules.py
- full/types.ts
- test_blender_render.py
- blender_plan.py
- scene_cues
- test_full_scenes.py
- captions
- look.py
- parts.py
- scene_kit.py
- render_remotion
- templates.py
- gather_pool
- align_words
- test_blender_plan.py
- fetch
- local_voice
- load_model
- main
- Short.tsx
- sys
- test_opener_plan.py
- cut
- prepare_topic
- Halftone.tsx
- json
- blender_link.py
- owner
- channel_profiles.py
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
- story_sound
- opener_scene.py
- bpy
- BlenderFailed
- full_cues
- build_scene.py
- gemini_images
- pool_pictures
- edit_scripts
- limit_style
- test_story.py
- people_standin.py
- test_opener_checks.py
- wants_remotion
- test_on_topic_ignores_a_lone_shared_name
- drawn_thumbnail
- ref_remotion
- render
- trim_borders
- rescue_graphics

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

## Communities (82 total, 6 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "re"
Cohesion: 0.09
Nodes (13): shot_span(), log_short(), logbook_results(), vault_page(), vault_refresh(), duration(), mark_details(), parse_scene_money() (+5 more)

### Community 3 - "write_scripts"
Cohesion: 0.13
Nodes (12): clean_sound(), limit_sounds(), fills_frame(), graphic_low(), fill_money_graphics(), is_person_portrait(), limit_full(), words_of() (+4 more)

### Community 4 - "ask_ai"
Cohesion: 0.12
Nodes (14): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high(), test_fake_reaches_callers() (+6 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "pathlib"
Cohesion: 0.09
Nodes (12): code_version(), hex_rgb(), luminance(), crop_film_bytes(), pixabay_films(), comfy_call(), local_job(), moss_graph() (+4 more)

### Community 7 - "shutil"
Cohesion: 0.09
Nodes (17): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), full_props(), lint_custom_code(), look_and_fix(), preview_custom() (+9 more)

### Community 8 - "test_opener_scene.py"
Cohesion: 0.06
Nodes (37): builds(), fixture(), people_lib(), run(), test_bad_plans_fail(), test_box_fall_rests_and_renders(), test_camera_follows_unasked(), test_chicken_chop_reference() (+29 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 10 - "Paper"
Cohesion: 0.10
Nodes (31): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+23 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "moves.py"
Cohesion: 0.13
Nodes (22): apply(), clear_distance_at_end(), fall(), fly_off(), gait(), hop_off(), legs(), push() (+14 more)

### Community 13 - "test_style.py"
Cohesion: 0.04
Nodes (50): cut_text(), look_text(), approve_candidate(), clean_style_code(), invent_component(), attempt(), invent_styles(), library_menu() (+42 more)

### Community 14 - "ffmpeg"
Cohesion: 0.13
Nodes (10): caption_layer(), make(), master_gain(), project_xml(), remove(), ffmpeg(), short_folder(), test_melt_plays_it_with_the_captions_on_top() (+2 more)

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (37): load_rules(), min_real_pictures(), parse_rules(), test_channels_have_opener_rules(), capture_prompts(), ask(), draft_reply(), make() (+29 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 18 - "test_pictures_first.py"
Cohesion: 0.12
Nodes (27): write_json(), catalog_entries(), catalog_pool(), save_pool(), entry(), fake_ai, film(), pic_short() (+19 more)

### Community 19 - "planning"
Cohesion: 0.14
Nodes (17): passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), reply() (+9 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 22 - "local_clips"
Cohesion: 0.16
Nodes (9): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), motion_prompt(), start_picture_problems(), veo_handoff(), video_encoder() (+1 more)

### Community 23 - "plan_rules.py"
Cohesion: 0.14
Nodes (16): clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number() (+8 more)

### Community 24 - "full/types.ts"
Cohesion: 0.16
Nodes (17): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+9 more)

### Community 25 - "test_blender_render.py"
Cohesion: 0.22
Nodes (12): peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises(), test_frames_are_trimmed_after_the_clips_are_cut() (+4 more)

### Community 26 - "blender_plan.py"
Cohesion: 0.12
Nodes (8): clamp(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order(), test_thumbnail_order_skips_film_and_puts_openers_first()

### Community 27 - "scene_cues"
Cohesion: 0.05
Nodes (20): scene_cues(), ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame() (+12 more)

### Community 28 - "test_full_scenes.py"
Cohesion: 0.06
Nodes (23): sfx_events(), full_summary(), full_formats(), opener_graphic(), fix_opener_graphic(), article_text(), fact_check(), _board() (+15 more)

### Community 29 - "captions"
Cohesion: 0.14
Nodes (8): ass_time(), captions(), styled(), music_gain(), speak(), tts(), ass_colour(), test_music_gain_evens_out_tracks()

### Community 30 - "look.py"
Cohesion: 0.27
Nodes (5): collection(), ink_lines(), linear(), material(), setup()

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (23): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+15 more)

### Community 32 - "scene_kit.py"
Cohesion: 0.14
Nodes (12): add_body(), ensure_world(), fcurves(), fcurves_of(), interpolation(), layers(), leg_rig(), loc_at() (+4 more)

### Community 33 - "render_remotion"
Cohesion: 0.09
Nodes (14): caption_lines(), short_skin(), ink_silhouette(), make_paper(), paint_instead(), render_remotion(), remotion(), render() (+6 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "gather_pool"
Cohesion: 0.08
Nodes (14): commons_films(), article_images(), commons_search(), get_image(), openverse_images(), ov_get(), thumb_url(), usable_license() (+6 more)

### Community 36 - "align_words"
Cohesion: 0.15
Nodes (10): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), test_caption_word_counts_match_the_scene_splitter(), test_caption_words_keep_what_is_written(), test_dollar_scale_word_order() (+2 more)

### Community 37 - "test_blender_plan.py"
Cohesion: 0.25
Nodes (14): clean_build(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults(), test_clean_build_keeps_a_good_plan(), test_default_build_shape(), test_label_is_short_and_upper(), test_nan_and_infinity_get_defaults() (+6 more)

### Community 38 - "fetch"
Cohesion: 0.23
Nodes (7): archive_films(), nasa_films(), archive_images(), nasa_images(), nasa_search(), on_topic(), fetch()

### Community 39 - "local_voice"
Cohesion: 0.20
Nodes (6): cosy_instruct(), local_voice(), split_takes(), spoken_count(), is_loop_short(), test_word_counts_match_the_aligner()

### Community 40 - "load_model"
Cohesion: 0.25
Nodes (4): ground_material(), load_model(), material(), merge()

### Community 41 - "main"
Cohesion: 0.18
Nodes (3): main(), Failure, key()

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "sys"
Cohesion: 0.08
Nodes (3): scale_beats(), main(), build()

### Community 44 - "test_opener_plan.py"
Cohesion: 0.07
Nodes (38): clean_opener(), _expect(), fill_template(), _keep(), _num(), plan_openers(), ask(), _size() (+30 more)

### Community 45 - "cut"
Cohesion: 0.07
Nodes (25): bm_area(), box_of(), centre(), clusters(), cut(), edge_point_local(), half(), handle_end_local() (+17 more)

### Community 46 - "prepare_topic"
Cohesion: 0.22
Nodes (7): contact_sheets(), load_pool(), pool_folder(), prepare_topic(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip(), test_small_pool_skips_ai()

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "json"
Cohesion: 0.06
Nodes (21): call(), fit_start(), frames(), graph(), main(), saved_file(), align(), main() (+13 more)

### Community 49 - "blender_link.py"
Cohesion: 0.08
Nodes (25): allowed_licence(), attribution(), call(), credit(), fetch_model(), in_library(), LinkError, ping() (+17 more)

### Community 50 - "owner"
Cohesion: 0.22
Nodes (3): owner(), stubbed, test_gather_pool_skip_and_limits()

### Community 51 - "channel_profiles.py"
Cohesion: 0.05
Nodes (33): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+25 more)

### Community 52 - "edit_plan"
Cohesion: 0.33
Nodes (3): edit_plan(), picture_line(), test_edit_plan_picture_line()

### Community 53 - "test_first_second.py"
Cohesion: 0.06
Nodes (28): use_picture_from(), apply_review_fixes(), paint_new(), rewrite_paint_prompts(), swap_pictures(), real(), run_check(), state() (+20 more)

### Community 54 - "visual_review"
Cohesion: 0.24
Nodes (7): clock(), overlay_notes(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 55 - "math"
Cohesion: 0.06
Nodes (29): _append(), _attach(), _bake_free(), base_name(), _body_tree(), _clearance(), _clip(), _colour() (+21 more)

### Community 56 - "tree"
Cohesion: 0.25
Nodes (4): clear_distance(), travel(), surface_z(), tree()

### Community 57 - "choose_images"
Cohesion: 0.19
Nodes (14): choose_images(), apply_look_scenes(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+6 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.07
Nodes (36): render_opener(), weak_opener_graphic(), use_opener(), Env, _people_files(), short(), test_beats_scaled_into_scene(), test_cc_by_credit() (+28 more)

### Community 59 - "pack_people.py"
Cohesion: 0.26
Nodes (6): base_name(), clip_name(), front(), height(), main(), stride()

### Community 60 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.08
Nodes (21): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+13 more)

### Community 62 - "story_sound"
Cohesion: 0.40
Nodes (4): story_sound(), test_story_sound_library(), fetch(), _tone_wav()

### Community 63 - "opener_scene.py"
Cohesion: 0.08
Nodes (23): State, beat_actors(), build_set(), camera(), dress_set(), first_hit(), hold_offscreen(), main() (+15 more)

### Community 64 - "bpy"
Cohesion: 0.19
Nodes (4): apply(), ink(), outline(), toon()

### Community 66 - "full_cues"
Cohesion: 0.17
Nodes (7): full_cues(), spoken_at(), spoken_span(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish(), test_model_graphic()

### Community 67 - "build_scene.py"
Cohesion: 0.20
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 69 - "pool_pictures"
Cohesion: 0.10
Nodes (9): film_frames(), film_piece(), film_ffmpeg(), catalog_text(), clean_pics(), is_usable(), pictures_of(), usable() (+1 more)

### Community 70 - "edit_scripts"
Cohesion: 0.17
Nodes (6): quality_check(), edit_scripts(), length_plan(), narration_lines(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules()

### Community 72 - "test_story.py"
Cohesion: 0.14
Nodes (15): sentence_groups(), check_twists(), story_problems(), scenes(), test_a_take_is_cut_between_the_scenes_words(), test_no_hook_setting_no_hook_check(), test_rules_accept_opener_setting(), test_sentences_running_across_cuts_are_one_take() (+7 more)

### Community 73 - "people_standin.py"
Cohesion: 0.25
Nodes (5): body(), clip(), key(), main(), part()

### Community 74 - "test_opener_checks.py"
Cohesion: 0.30
Nodes (10): results(), test_blade_face(), test_cut_result(), test_edge_leads(), test_first_frame(), test_hidden(), test_in_frame(), test_moves_visibly() (+2 more)

### Community 78 - "drawn_thumbnail"
Cohesion: 0.23
Nodes (9): scene_frames(), drawn_thumbnail(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 85 - "render"
Cohesion: 0.10
Nodes (9): make_sfx(), short_credit(), graphics_count(), to_vertical(), srt(), drawn_choices(), render(), save_state() (+1 more)

### Community 86 - "trim_borders"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 92 - "rescue_graphics"
Cohesion: 0.29
Nodes (4): rescue_graphics(), max_full(), max_full_planned(), test_rescue_respects_caps()

## Knowledge Gaps
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `re`, `write_scripts`, `pathlib`, `shutil`, `test_style.py`, `ffmpeg`, `local_clips`, `test_blender_render.py`, `scene_cues`, `test_full_scenes.py`, `captions`, `render_remotion`, `local_voice`, `channel_profiles.py`, `edit_plan`, `test_first_second.py`, `visual_review`, `choose_images`, `test_opener_render.py`, `story_sound`, `gemini_images`, `edit_scripts`, `wants_remotion`, `drawn_thumbnail`, `trim_borders`, `rescue_graphics`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `build_scene.py`, `json`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `re` be split into smaller, more focused modules?**
  _Cohesion score 0.09 - nodes in this community are weakly interconnected._
- **Should `write_scripts` be split into smaller, more focused modules?**
  _Cohesion score 0.12987012987012986 - nodes in this community are weakly interconnected._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._