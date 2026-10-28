# Graph Report - ShortsMaker  (2026-10-28)

## Corpus Check
- 129 files · ~154,314 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 2146 nodes · 5664 edges · 85 communities (79 shown, 6 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 128 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c679eae9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- code_custom_scenes
- toolkit.tsx
- ask_ai
- split_make_shorts.py
- test_full_scenes.py
- frame_render.py
- test_opener_scene.py
- Paper
- gpu.py
- test_h3_handoff.py
- moves.py
- guarded.tsx
- re
- test_rules.py
- Journey.tsx
- BigNumber.tsx
- test_pictures_first.py
- planning
- Local GPU Worker
- clean_look
- rescue_graphics
- plan_rules.py
- make_paper
- test_blender_render.py
- style_placeholders
- frame_maker
- full_cues
- music_gain
- look.py
- parts.py
- math
- prepare_topic
- templates.py
- on_topic
- time
- test_style.py
- build_scene.py
- h3_run.py
- load_model
- main
- Short.tsx
- subprocess
- test_opener_plan.py
- cut
- test_first_second.py
- Halftone.tsx
- image_sources.py
- blender_link.py
- gather_pool
- json
- full_props
- style_library
- visual_review
- scene_kit.py
- sfx_events
- choose_images
- test_opener_render.py
- pack_people.py
- test_opener_checks.py
- opener_checks.py
- check_twists
- opener_scene.py
- look_toon.py
- render_remotion
- approve_candidate
- Shots
- test_blender_scene.py
- write_scripts
- invent_component
- edit_plan
- make_sfx
- people_standin.py
- trim_borders
- story_sound
- QuestionBeat.tsx
- captions
- full_pictures
- pool_pictures
- gemini_images
- to_vertical
- wants_remotion
- render
- srt

## God Nodes (most connected - your core abstractions)
1. `render()` - 62 edges
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
Cohesion: 0.15
Nodes (21): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.14
Nodes (30): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+22 more)

### Community 2 - "code_custom_scenes"
Cohesion: 0.05
Nodes (31): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), redraw_custom() (+23 more)

### Community 3 - "toolkit.tsx"
Cohesion: 0.24
Nodes (20): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+12 more)

### Community 4 - "ask_ai"
Cohesion: 0.11
Nodes (14): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high() (+6 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "test_full_scenes.py"
Cohesion: 0.10
Nodes (10): hex_rgb(), luminance(), library_menu(), reject_candidate(), story_problems(), test_short_credit(), test_no_hook_setting_no_hook_check(), test_story_problems() (+2 more)

### Community 7 - "frame_render.py"
Cohesion: 0.17
Nodes (5): crop_film_bytes(), film_frames(), pixabay_films(), fills_frame(), person_card()

### Community 8 - "test_opener_scene.py"
Cohesion: 0.06
Nodes (37): builds(), fixture(), people_lib(), run(), test_bad_plans_fail(), test_box_fall_rests_and_renders(), test_camera_follows_unasked(), test_chicken_chop_reference() (+29 more)

### Community 9 - "Paper"
Cohesion: 0.09
Nodes (36): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+28 more)

### Community 10 - "gpu.py"
Cohesion: 0.07
Nodes (18): comfy_call(), local_job(), local_voice(), moss_graph(), moss_images(), sentence_groups(), split_takes(), spoken_count() (+10 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.06
Nodes (41): cover_crop(), cut_owner_clip(), h3_problems(), h3_prompt(), h3_prompts(), local_clips(), motion_prompt(), start_picture_problems() (+33 more)

### Community 12 - "moves.py"
Cohesion: 0.12
Nodes (22): apply(), clear_distance(), clear_distance_at_end(), fall(), fly_off(), gait(), hop_off(), legs() (+14 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.11
Nodes (21): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+13 more)

### Community 14 - "re"
Cohesion: 0.07
Nodes (17): caption_layer(), make(), master_gain(), project_xml(), remove(), shot_span(), log_short(), vault_page() (+9 more)

### Community 15 - "test_rules.py"
Cohesion: 0.05
Nodes (50): ask_brain(), ask_number(), fix_short(), use_picture_from(), paint_new(), draft_rules(), load_rules(), min_real_pictures() (+42 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.16
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "BigNumber.tsx"
Cohesion: 0.22
Nodes (13): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+5 more)

### Community 18 - "test_pictures_first.py"
Cohesion: 0.14
Nodes (25): catalog_entries(), catalog_pool(), entry(), fake_ai, film(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+17 more)

### Community 19 - "planning"
Cohesion: 0.14
Nodes (17): passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), reply() (+9 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 22 - "rescue_graphics"
Cohesion: 0.29
Nodes (4): rescue_graphics(), max_full(), max_full_planned(), test_rescue_respects_caps()

### Community 23 - "plan_rules.py"
Cohesion: 0.10
Nodes (22): graphic_low(), clean_full(), word(), clean_graphic(), contains(), coords(), fill_money_graphics(), is_loop_short() (+14 more)

### Community 24 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 25 - "test_blender_render.py"
Cohesion: 0.09
Nodes (23): BlenderFailed, peaks(), render_clips(), _run(), scene_frames(), to_glb(), drawn_thumbnail(), fake_blender() (+15 more)

### Community 26 - "style_placeholders"
Cohesion: 0.23
Nodes (8): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_slots_restored_after_render(), with_fakes()

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (14): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+6 more)

### Community 28 - "full_cues"
Cohesion: 0.13
Nodes (11): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish() (+3 more)

### Community 29 - "music_gain"
Cohesion: 0.22
Nodes (4): music_gain(), speak(), tts(), test_music_gain_evens_out_tracks()

### Community 30 - "look.py"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (22): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+14 more)

### Community 32 - "math"
Cohesion: 0.07
Nodes (20): _append(), _attach(), _bake_free(), base_name(), _body_tree(), _clearance(), _colour(), _detour() (+12 more)

### Community 33 - "prepare_topic"
Cohesion: 0.20
Nodes (9): contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip(), test_pool_rows_without_thumbs() (+1 more)

### Community 34 - "templates.py"
Cohesion: 0.16
Nodes (16): member(), Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), focus_object() (+8 more)

### Community 35 - "on_topic"
Cohesion: 0.20
Nodes (5): archive_films(), archive_images(), nasa_images(), on_topic(), test_on_topic_ignores_a_lone_shared_name()

### Community 36 - "time"
Cohesion: 0.12
Nodes (14): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+6 more)

### Community 37 - "test_style.py"
Cohesion: 0.11
Nodes (11): apply_look_scenes(), owner(), plan_with(), ask(), test_apply_look_scenes(), test_clean_question_and_kinetic(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library() (+3 more)

### Community 39 - "h3_run.py"
Cohesion: 0.20
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 40 - "load_model"
Cohesion: 0.25
Nodes (4): ground_material(), load_model(), material(), merge()

### Community 41 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 42 - "Short.tsx"
Cohesion: 0.12
Nodes (20): Captions(), PersonCard(), Root(), Background(), Card, flashAlpha(), GraphicFor(), Move (+12 more)

### Community 43 - "subprocess"
Cohesion: 0.08
Nodes (15): code_version(), preview_sheet(), tsc_check(), _cast_note(), fingerprint(), review(), review_frames(), save_try() (+7 more)

### Community 44 - "test_opener_plan.py"
Cohesion: 0.07
Nodes (38): clean_opener(), _expect(), fill_template(), _keep(), _num(), plan_openers(), ask(), _size() (+30 more)

### Community 45 - "cut"
Cohesion: 0.07
Nodes (27): bm_area(), box_of(), centre(), clusters(), cut(), edge_point_local(), half(), handle_end_local() (+19 more)

### Community 46 - "test_first_second.py"
Cohesion: 0.08
Nodes (8): logbook_results(), first_second_check(), run_check(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples(), test_low_score_opens_on_a_better_real_picture(), test_opener_must_be_a_later_real_picture(), test_opener_prompt_shows_each_scenes_line_and_picture()

### Community 47 - "Halftone.tsx"
Cohesion: 0.19
Nodes (21): drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw(), Engraving() (+13 more)

### Community 48 - "image_sources.py"
Cohesion: 0.07
Nodes (25): commons_films(), nasa_films(), article_images(), commons_search(), get_image(), nasa_search(), openverse_images(), ov_get() (+17 more)

### Community 49 - "blender_link.py"
Cohesion: 0.06
Nodes (29): allowed_licence(), attribution(), call(), credit(), fetch_model(), in_library(), LinkError, ping() (+21 more)

### Community 50 - "gather_pool"
Cohesion: 0.18
Nodes (4): gather_pool(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 51 - "json"
Cohesion: 0.07
Nodes (23): freesound_fetch(), ask_count(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel(), save_channel() (+15 more)

### Community 52 - "full_props"
Cohesion: 0.20
Nodes (8): full_props(), full_summary(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_full_summary(), test_model_graphic(), test_remotion_props_full()

### Community 53 - "style_library"
Cohesion: 0.29
Nodes (5): style_library(), style_rules(), write_style_index(), test_library_entries_have_fields(), test_write_style_index_is_deterministic()

### Community 54 - "visual_review"
Cohesion: 0.14
Nodes (10): clock(), overlay_notes(), quality_check(), review_fixes(), storyboard(), visual_review(), length_plan(), test_review_is_told_the_drawings_are_deliberate() (+2 more)

### Community 55 - "scene_kit.py"
Cohesion: 0.08
Nodes (24): _clip(), facing_now(), _ground(), move(), pick_up(), _strip(), _travel(), add_body() (+16 more)

### Community 56 - "sfx_events"
Cohesion: 0.33
Nodes (3): sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 57 - "choose_images"
Cohesion: 0.25
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.09
Nodes (32): render_opener(), use_opener(), Env, _people_files(), short(), test_beats_scaled_into_scene(), test_cc_by_credit(), test_crash_retry_then_fallback() (+24 more)

### Community 59 - "pack_people.py"
Cohesion: 0.26
Nodes (6): base_name(), clip_name(), front(), height(), main(), stride()

### Community 60 - "test_opener_checks.py"
Cohesion: 0.30
Nodes (10): results(), test_blade_face(), test_cut_result(), test_edge_leads(), test_first_frame(), test_hidden(), test_in_frame(), test_moves_visibly() (+2 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.10
Nodes (22): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+14 more)

### Community 62 - "check_twists"
Cohesion: 0.47
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 63 - "opener_scene.py"
Cohesion: 0.09
Nodes (20): State, beat_actors(), build_set(), camera(), dress_set(), first_hit(), main(), place_actors() (+12 more)

### Community 64 - "look_toon.py"
Cohesion: 0.27
Nodes (4): apply(), ink(), outline(), toon()

### Community 65 - "render_remotion"
Cohesion: 0.14
Nodes (10): caption_lines(), short_skin(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), test_clean_full_custom_and_skin() (+2 more)

### Community 66 - "approve_candidate"
Cohesion: 0.18
Nodes (11): approve_candidate(), save_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes() (+3 more)

### Community 67 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 68 - "test_blender_scene.py"
Cohesion: 0.07
Nodes (42): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+34 more)

### Community 69 - "write_scripts"
Cohesion: 0.09
Nodes (15): clean_sound(), limit_sounds(), pictures_of(), limit_full(), limit_style(), direct_scripts(), edit_scripts(), fact_check() (+7 more)

### Community 70 - "invent_component"
Cohesion: 0.15
Nodes (9): invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), swap_inventions(), test_invention_lint_failure_uses_fallback(), test_placeholders_match_the_slots() (+1 more)

### Community 71 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 73 - "people_standin.py"
Cohesion: 0.29
Nodes (5): body(), clip(), key(), main(), part()

### Community 74 - "trim_borders"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 75 - "story_sound"
Cohesion: 0.40
Nodes (4): story_sound(), test_story_sound_library(), fetch(), _tone_wav()

### Community 76 - "QuestionBeat.tsx"
Cohesion: 0.33
Nodes (4): FONT, theme, CLAMP, KineticTitle()

### Community 77 - "captions"
Cohesion: 0.40
Nodes (4): ass_time(), captions(), styled(), ass_colour()

### Community 78 - "full_pictures"
Cohesion: 0.40
Nodes (4): full_pictures(), _board(), test_board_pictures_attached(), test_sfx_full()

### Community 79 - "pool_pictures"
Cohesion: 0.12
Nodes (7): film_piece(), film_ffmpeg(), catalog_text(), clean_pics(), is_usable(), usable(), pool_pictures()

### Community 85 - "render"
Cohesion: 0.15
Nodes (7): short_credit(), graphics_count(), mark_details(), drawn_choices(), render(), save_state(), test_drawn_choices_have_no_pictures()

## Knowledge Gaps
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `templates.py`, `Shots`, `build_scene.py`, `json`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.14583333333333334 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `code_custom_scenes`, `test_full_scenes.py`, `gpu.py`, `test_h3_handoff.py`, `re`, `test_rules.py`, `rescue_graphics`, `plan_rules.py`, `make_paper`, `test_blender_render.py`, `frame_maker`, `full_cues`, `music_gain`, `subprocess`, `test_first_second.py`, `blender_link.py`, `json`, `full_props`, `visual_review`, `sfx_events`, `choose_images`, `test_opener_render.py`, `render_remotion`, `approve_candidate`, `edit_plan`, `make_sfx`, `trim_borders`, `story_sound`, `captions`, `gemini_images`, `to_vertical`, `wants_remotion`, `srt`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.13513513513513514 - nodes in this community are weakly interconnected._
- **Why does `catalog_pool()` connect `test_pictures_first.py` to `prepare_topic`, `ask_ai`, `test_full_scenes.py`, `re`, `test_rules.py`, `json`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Should `code_custom_scenes` be split into smaller, more focused modules?**
  _Cohesion score 0.05128205128205128 - nodes in this community are weakly interconnected._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.11384615384615385 - nodes in this community are weakly interconnected._