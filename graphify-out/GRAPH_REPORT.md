# Graph Report - ShortsMaker  (2026-10-27)

## Corpus Check
- 124 files · ~144,837 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 2039 nodes · 5373 edges · 91 communities (75 shown, 16 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 125 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `868d8c6b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- motion.py
- skinOf
- ask_ai
- split_make_shorts.py
- pathlib
- test_h3_handoff.py
- test_opener_scene.py
- toolkit.tsx
- gpu.py
- local_clips
- short_with
- guarded.tsx
- make
- test_rules.py
- Journey.tsx
- full/types.ts
- test_pictures_first.py
- planning
- Local GPU Worker
- clean_look
- test_blender_plan.py
- paint_instead
- render_remotion
- test_blender_render.py
- style_placeholders
- ClipReader
- look.py
- write_scripts
- render
- parts.py
- people.py
- prepare_topic
- templates.py
- invent_component
- test_story.py
- test_full_scenes.py
- math
- h3_run.py
- audio_mix.py
- main
- Short.tsx
- test_opener_plan.py
- moves.py
- test_style.py
- Halftone.tsx
- fetch
- blender_link.py
- gather_pool
- json
- Shots
- test_first_second.py
- frame_maker
- scene_kit.py
- sfx_events
- choose_images
- test_opener_render.py
- pack_people.py
- test_opener_checks.py
- opener_checks.py
- blender_note
- opener_scene.py
- look_toon.py
- edit_plan
- QuestionBeat.tsx
- test_blender_scene.py
- owner
- style_library
- use_opener
- default_build
- review
- trim_borders
- pick_model
- Fake
- write_frames
- limit_style
- copy
- h3_problems
- h3_prompt
- edit_scripts
- test_on_topic_ignores_a_lone_shared_name
- person_card
- srt
- thumbnail_order
- clamp
- ending
- panels
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
- `test_scene_frames_cover_every_frame_once()` --calls--> `scene_frames()`  [EXTRACTED]
  tests/test_blender_render.py → shortsmaker/blender_render.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`

## Communities (91 total, 16 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.15
Nodes (21): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.14
Nodes (30): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+22 more)

### Community 2 - "motion.py"
Cohesion: 0.15
Nodes (11): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+3 more)

### Community 3 - "skinOf"
Cohesion: 0.25
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 4 - "ask_ai"
Cohesion: 0.07
Nodes (20): ask_brain(), ask_number(), seed_ideas(), ask_ai(), gemini_model(), quota_exhausted(), run_agy(), mark_details() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "pathlib"
Cohesion: 0.08
Nodes (13): code_version(), hex_rgb(), luminance(), crop_film_bytes(), film_frames(), film_piece(), shot_span(), film_ffmpeg() (+5 more)

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.19
Nodes (13): unpack_clips(), handoff(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated(), test_flagged_start_picture_is_not_sent(), test_handoff_picks_up_clips_zip(), test_handoff_records_which_file_made_the_clip(), test_handoff_writes_jobs_and_zip() (+5 more)

### Community 8 - "test_opener_scene.py"
Cohesion: 0.06
Nodes (35): builds(), fixture(), people_lib(), run(), test_bad_plans_fail(), test_box_fall_rests_and_renders(), test_camera_follows_unasked(), test_chicken_chop_reference() (+27 more)

### Community 9 - "toolkit.tsx"
Cohesion: 0.16
Nodes (24): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+16 more)

### Community 10 - "gpu.py"
Cohesion: 0.08
Nodes (14): align(), main(), studio_speak(), comfy_call(), local_job(), local_voice(), moss_graph(), moss_images() (+6 more)

### Community 11 - "local_clips"
Cohesion: 0.12
Nodes (11): cover_crop(), cut_owner_clip(), gemini_images(), h3_prompts(), local_clips(), motion_prompt(), start_picture_problems(), veo_handoff() (+3 more)

### Community 12 - "short_with"
Cohesion: 0.23
Nodes (14): fake_ai(), short_with(), test_all_closeup_marked_scenes_skip_pause(), test_missing_scene_is_asked_again(), run(), test_retries_only_failing_scene_with_reason(), run(), test_scene_number_given_as_text_is_accepted() (+6 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 14 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (37): load_rules(), min_real_pictures(), parse_rules(), test_channels_have_opener_rules(), capture_prompts(), ask(), draft_reply(), make() (+29 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.15
Nodes (17): FullScene(), clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level() (+9 more)

### Community 17 - "full/types.ts"
Cohesion: 0.15
Nodes (18): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+10 more)

### Community 18 - "test_pictures_first.py"
Cohesion: 0.11
Nodes (28): write_json(), catalog_entries(), catalog_pool(), clean_pics(), save_pool(), entry(), fake_ai, film() (+20 more)

### Community 19 - "planning"
Cohesion: 0.15
Nodes (14): passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), reply() (+6 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 22 - "test_blender_plan.py"
Cohesion: 0.29
Nodes (12): clean_build(), pick(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults(), test_clean_build_keeps_a_good_plan(), test_label_is_short_and_upper(), test_nan_and_infinity_get_defaults() (+4 more)

### Community 23 - "paint_instead"
Cohesion: 0.12
Nodes (7): to_vertical(), ink_silhouette(), make_paper(), paint_instead(), test_ink_silhouette(), test_make_paper(), test_remotion_failure_paints()

### Community 24 - "render_remotion"
Cohesion: 0.13
Nodes (11): short_skin(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_clean_full_custom_and_skin() (+3 more)

### Community 25 - "test_blender_render.py"
Cohesion: 0.08
Nodes (25): BlenderFailed, peaks(), render_clips(), _run(), scene_cues(), full_cues(), spoken_at(), spoken_span() (+17 more)

### Community 26 - "style_placeholders"
Cohesion: 0.21
Nodes (9): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_placeholders_match_the_slots(), test_slots_restored_after_render() (+1 more)

### Community 27 - "ClipReader"
Cohesion: 0.19
Nodes (5): ClipReader, draw_card(), draw_graphic(), frame(), shot()

### Community 28 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 29 - "write_scripts"
Cohesion: 0.08
Nodes (27): clean_sound(), limit_sounds(), graphic_low(), clean_full(), word(), clean_graphic(), contains(), coords() (+19 more)

### Community 30 - "render"
Cohesion: 0.07
Nodes (27): story_sound(), scene_frames(), thumbnail(), short_credit(), clock(), ffmpeg(), graphics_count(), first_second_check() (+19 more)

### Community 31 - "parts.py"
Cohesion: 0.16
Nodes (20): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+12 more)

### Community 32 - "people.py"
Cohesion: 0.08
Nodes (18): _append(), _attach(), _bake_free(), base_name(), _colour(), dress(), held(), _hold() (+10 more)

### Community 33 - "prepare_topic"
Cohesion: 0.12
Nodes (11): catalog_text(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), prepare_topic(), usable() (+3 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "invent_component"
Cohesion: 0.18
Nodes (7): invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), style_rules(), test_invention_lint_failure_uses_fallback()

### Community 36 - "test_story.py"
Cohesion: 0.06
Nodes (30): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), sentence_groups(), check_twists(), story_problems() (+22 more)

### Community 37 - "test_full_scenes.py"
Cohesion: 0.05
Nodes (39): fix_short(), use_picture_from(), full_props(), full_summary(), rescue_graphics(), apply_review_fixes(), paint_new(), rewrite_paint_prompts() (+31 more)

### Community 38 - "math"
Cohesion: 0.10
Nodes (6): make_sfx(), body(), clip(), key(), main(), part()

### Community 39 - "h3_run.py"
Cohesion: 0.22
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 40 - "audio_mix.py"
Cohesion: 0.11
Nodes (10): ass_time(), caption_lines(), captions(), styled(), freesound_fetch(), music_gain(), speak(), tts() (+2 more)

### Community 41 - "main"
Cohesion: 0.16
Nodes (5): keyvis(), main(), Failure, key(), focus_object()

### Community 42 - "Short.tsx"
Cohesion: 0.12
Nodes (20): Captions(), PersonCard(), Root(), Background(), Card, flashAlpha(), GraphicFor(), Move (+12 more)

### Community 44 - "test_opener_plan.py"
Cohesion: 0.09
Nodes (33): clean_opener(), _expect(), fix_plan(), _num(), plan_openers(), ask(), _size(), _stroke() (+25 more)

### Community 45 - "moves.py"
Cohesion: 0.06
Nodes (48): apply(), bm_area(), box_of(), centre(), clear_distance(), clear_distance_at_end(), clusters(), cut() (+40 more)

### Community 46 - "test_style.py"
Cohesion: 0.14
Nodes (10): wants_remotion(), apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics() (+2 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.19
Nodes (21): drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw(), Engraving() (+13 more)

### Community 48 - "fetch"
Cohesion: 0.09
Nodes (16): archive_films(), commons_films(), nasa_films(), pixabay_films(), archive_images(), get_image(), nasa_images(), nasa_search() (+8 more)

### Community 49 - "blender_link.py"
Cohesion: 0.10
Nodes (21): allowed_licence(), attribution(), call(), credit(), fetch_model(), in_library(), LinkError, ping() (+13 more)

### Community 50 - "gather_pool"
Cohesion: 0.18
Nodes (6): article_images(), commons_search(), thumb_url(), wm_files(), gather_pool(), test_gather_pool_skip_and_limits()

### Community 51 - "json"
Cohesion: 0.05
Nodes (32): ask_count(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel(), save_channel(), trend_research() (+24 more)

### Community 52 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 53 - "test_first_second.py"
Cohesion: 0.16
Nodes (15): logbook_results(), swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples(), test_low_score_opens_on_a_better_real_picture() (+7 more)

### Community 54 - "frame_maker"
Cohesion: 0.18
Nodes (4): fills_frame(), frame_maker(), credit_tag_image(), fallback_graphic()

### Community 55 - "scene_kit.py"
Cohesion: 0.11
Nodes (16): add_body(), ensure_world(), facing_vec(), fcurves(), fcurves_of(), interpolation(), key_vis(), layers() (+8 more)

### Community 56 - "sfx_events"
Cohesion: 0.33
Nodes (3): sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 57 - "choose_images"
Cohesion: 0.25
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

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
Cohesion: 0.08
Nodes (23): State, in_frame(), build_set(), camera(), checks(), dress_set(), first_hit(), ground_material() (+15 more)

### Community 64 - "look_toon.py"
Cohesion: 0.27
Nodes (4): apply(), ink(), outline(), toon()

### Community 65 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 66 - "QuestionBeat.tsx"
Cohesion: 0.33
Nodes (4): FONT, theme, CLAMP, KineticTitle()

### Community 68 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 69 - "owner"
Cohesion: 0.12
Nodes (6): owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_good_look_check_skips_the_extra_compile()

### Community 70 - "style_library"
Cohesion: 0.16
Nodes (13): approve_candidate(), style_library(), write_style_index(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure() (+5 more)

### Community 71 - "use_opener"
Cohesion: 0.22
Nodes (6): use_opener(), test_use_opener_failure_keeps_scene(), test_use_opener_never_raises(), test_use_opener_on_success(), test_use_opener_planner_check(), _wiring()

### Community 72 - "default_build"
Cohesion: 0.25
Nodes (5): default_build(), plan_builds(), test_default_build_shape(), test_plan_builds_retries_then_defaults(), ask()

### Community 73 - "review"
Cohesion: 0.22
Nodes (4): _cast_note(), review(), review_frames(), test_review_frames_include_key_moments()

### Community 74 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

### Community 77 - "write_frames"
Cohesion: 0.29
Nodes (3): flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 82 - "edit_scripts"
Cohesion: 0.29
Nodes (4): edit_scripts(), length_plan(), narration_lines(), test_solo_edit_scripts_uses_same_ai()

### Community 84 - "person_card"
Cohesion: 0.33
Nodes (3): fit_font(), graphic_overlay(), person_card()

## Knowledge Gaps
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `templates.py`, `math`, `json`, `Shots`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.14583333333333334 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `ask_ai`, `pathlib`, `gpu.py`, `local_clips`, `make`, `paint_instead`, `render_remotion`, `test_blender_render.py`, `write_scripts`, `test_full_scenes.py`, `math`, `audio_mix.py`, `test_style.py`, `json`, `frame_maker`, `sfx_events`, `choose_images`, `opener_scene.py`, `edit_plan`, `use_opener`, `write_frames`, `srt`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.13513513513513514 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `prepare_topic`, `ask_ai`, `test_story.py`, `test_full_scenes.py`, `owner`, `default_build`, `test_opener_plan.py`, `limit_style`, `test_rules.py`, `test_style.py`, `test_pictures_first.py`, `json`, `edit_scripts`, `test_first_second.py`, `clean_look`, `planning`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `motion.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14855072463768115 - nodes in this community are weakly interconnected._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.07207207207207207 - nodes in this community are weakly interconnected._