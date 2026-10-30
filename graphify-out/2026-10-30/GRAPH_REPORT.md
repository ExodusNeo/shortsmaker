# Graph Report - ShortsMaker  (2026-10-29)

## Corpus Check
- 129 files · ~155,348 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 2150 nodes · 5672 edges · 89 communities (79 shown, 10 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 128 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3c41f561`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_first_second.py
- test_style.py
- ask_ai
- split_make_shorts.py
- test_full_scenes.py
- code_custom_scenes
- test_opener_scene.py
- toolkit.tsx
- ffmpeg
- test_h3_handoff.py
- walk
- style_library
- make
- test_rules.py
- Journey.tsx
- style_placeholders
- pool_of
- write_scripts
- Local GPU Worker
- clean_look
- gpu.py
- clean_full
- resolve_models
- test_blender_render.py
- fetch_model
- frame_maker
- full_cues
- captions
- look.py
- parts.py
- _hold
- render_remotion
- templates.py
- fetch
- test_story.py
- owner
- fake_ai
- h3_run.py
- dress
- main
- Short.tsx
- json
- test_opener_plan.py
- moves.py
- edit_plan
- Halftone.tsx
- re
- call
- gather_pool
- sys
- apply_review_fixes
- visual_review
- scene_kit.py
- tree
- test_pictures_first.py
- test_opener_render.py
- pack_people.py
- test_blender_scene.py
- opener_checks.py
- Fake
- opener_scene.py
- look_toon.py
- paint_instead
- use_opener
- Shots
- test_blender_plan.py
- pictures_of
- invent_component
- limit_style
- sentence_groups
- math
- test_opener_checks.py
- test_review_frames_include_key_moments
- QuestionBeat.tsx
- test_short_credit
- drawn_thumbnail
- qwen_voice.py
- ref_remotion
- BlenderFailed
- wants_remotion
- test_local_job_retries_a_hard_crash
- render
- trim_borders
- blender_plan.py
- opener_graphic
- apply_look_scenes

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
- `test_new_channel_stops_for_review()` --calls--> `pick_channel()`  [EXTRACTED]
  tests/test_rules.py → shortsmaker/channel_profiles.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`
- 5-file cycle: `shortsmaker/blender_render.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py -> shortsmaker/opener_render.py -> shortsmaker/blender_render.py`

## Communities (89 total, 10 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.14
Nodes (21): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.19
Nodes (26): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+18 more)

### Community 2 - "test_first_second.py"
Cohesion: 0.19
Nodes (13): first_second_check(), swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once() (+5 more)

### Community 3 - "test_style.py"
Cohesion: 0.18
Nodes (9): candidate_in(), plan_with(), ask(), test_candidate_names_unique_across_kinds(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics(), test_reject_deletes() (+1 more)

### Community 4 - "ask_ai"
Cohesion: 0.09
Nodes (16): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), mark_details(), direct_scripts(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash() (+8 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "test_full_scenes.py"
Cohesion: 0.09
Nodes (9): code_version(), hex_rgb(), luminance(), crop_film_bytes(), film_frames(), pixabay_films(), fills_frame(), clean_photo() (+1 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.11
Nodes (14): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+6 more)

### Community 8 - "test_opener_scene.py"
Cohesion: 0.06
Nodes (37): builds(), fixture(), people_lib(), run(), test_bad_plans_fail(), test_box_fall_rests_and_renders(), test_camera_follows_unasked(), test_chicken_chop_reference() (+29 more)

### Community 9 - "toolkit.tsx"
Cohesion: 0.05
Nodes (90): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+82 more)

### Community 10 - "ffmpeg"
Cohesion: 0.16
Nodes (10): story_sound(), shot_span(), split_takes(), duration(), ffmpeg(), is_loop_short(), test_story_sound_library(), fetch() (+2 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.12
Nodes (27): unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated(), test_flagged_start_picture_is_not_sent(), test_handoff_picks_up_clips_zip() (+19 more)

### Community 12 - "walk"
Cohesion: 0.22
Nodes (7): gait(), legs(), share_of_gap(), walk(), facing_vec(), key_swing(), leg_rig()

### Community 13 - "style_library"
Cohesion: 0.20
Nodes (10): approve_candidate(), style_library(), write_style_index(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes() (+2 more)

### Community 14 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (40): load_rules(), min_real_pictures(), parse_rules(), test_channels_have_opener_rules(), capture_prompts(), ask(), draft_reply(), make() (+32 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.11
Nodes (19): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+11 more)

### Community 17 - "style_placeholders"
Cohesion: 0.23
Nodes (8): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_slots_restored_after_render(), with_fakes()

### Community 18 - "pool_of"
Cohesion: 0.11
Nodes (24): write_json(), catalog_entries(), catalog_pool(), clean_pics(), contact_sheets(), pool_folder(), save_pool(), entry() (+16 more)

### Community 19 - "write_scripts"
Cohesion: 0.13
Nodes (21): prepare_topic(), limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, test_all_weak_returns_empty() (+13 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 22 - "gpu.py"
Cohesion: 0.08
Nodes (20): comfy_call(), cover_crop(), cut_owner_clip(), h3_problems(), h3_prompt(), h3_prompts(), local_clips(), local_job() (+12 more)

### Community 23 - "clean_full"
Cohesion: 0.08
Nodes (24): clean_sound(), limit_sounds(), graphic_low(), clean_full(), word(), clean_graphic(), contains(), coords() (+16 more)

### Community 24 - "resolve_models"
Cohesion: 0.33
Nodes (3): pick_model(), resolve_models(), test_every_unfound_model_named_at_once()

### Community 25 - "test_blender_render.py"
Cohesion: 0.22
Nodes (12): peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises(), test_frames_are_trimmed_after_the_clips_are_cut() (+4 more)

### Community 26 - "fetch_model"
Cohesion: 0.14
Nodes (17): attribution(), credit(), fetch_model(), in_library(), search(), words(), model_for(), _fetch_replies() (+9 more)

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (15): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+7 more)

### Community 28 - "full_cues"
Cohesion: 0.05
Nodes (27): sfx_events(), scene_cues(), full_props(), full_summary(), to_glb(), full_pictures(), full_cues(), spoken_at() (+19 more)

### Community 29 - "captions"
Cohesion: 0.12
Nodes (9): ass_time(), caption_lines(), captions(), styled(), music_gain(), speak(), tts(), ass_colour() (+1 more)

### Community 30 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 31 - "parts.py"
Cohesion: 0.16
Nodes (20): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+12 more)

### Community 32 - "_hold"
Cohesion: 0.10
Nodes (10): _bake_free(), _body_tree(), _handle_first(), held(), _hold(), prop_move(), _show_blade(), _through() (+2 more)

### Community 33 - "render_remotion"
Cohesion: 0.11
Nodes (13): short_skin(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions() (+5 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "fetch"
Cohesion: 0.10
Nodes (14): archive_films(), commons_films(), nasa_films(), archive_images(), get_image(), nasa_images(), nasa_search(), on_topic() (+6 more)

### Community 36 - "test_story.py"
Cohesion: 0.07
Nodes (25): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), check_twists(), edit_scripts(), narration_lines() (+17 more)

### Community 37 - "owner"
Cohesion: 0.15
Nodes (4): owner(), _fake_planning(), test_director_prompt_mentions_full(), film()

### Community 38 - "fake_ai"
Cohesion: 0.18
Nodes (6): fake_ai, planning_ai(), reply(), test_catalog_empty_pool_no_ai(), test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list()

### Community 39 - "h3_run.py"
Cohesion: 0.18
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 40 - "dress"
Cohesion: 0.11
Nodes (10): ground_material(), _append(), _attach(), base_name(), _colour(), dress(), _is_blade(), load_model() (+2 more)

### Community 41 - "main"
Cohesion: 0.16
Nodes (5): keyvis(), main(), Failure, key(), focus_object()

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), Background(), Card, flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "json"
Cohesion: 0.08
Nodes (11): freesound_fetch(), _cast_note(), fingerprint(), review(), review_frames(), save_try(), scale_beats(), save_candidate() (+3 more)

### Community 44 - "test_opener_plan.py"
Cohesion: 0.07
Nodes (38): clean_opener(), _expect(), fill_template(), _keep(), _num(), plan_openers(), ask(), _size() (+30 more)

### Community 45 - "moves.py"
Cohesion: 0.07
Nodes (36): apply(), bm_area(), box_of(), centre(), clusters(), cut(), edge_point_local(), fall() (+28 more)

### Community 46 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 47 - "Halftone.tsx"
Cohesion: 0.19
Nodes (20): drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw(), Engraving() (+12 more)

### Community 48 - "re"
Cohesion: 0.07
Nodes (19): allowed_licence(), log_short(), logbook_results(), vault_page(), vault_refresh(), parse_scene_money(), clean_style_code(), clash() (+11 more)

### Community 49 - "call"
Cohesion: 0.20
Nodes (5): call(), LinkError, ping(), blender_note(), test_blender_note()

### Community 50 - "gather_pool"
Cohesion: 0.12
Nodes (10): article_images(), commons_search(), thumb_url(), wm_files(), gather_pool(), load_pool(), stubbed, test_gather_pool_shape() (+2 more)

### Community 51 - "sys"
Cohesion: 0.06
Nodes (26): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+18 more)

### Community 53 - "apply_review_fixes"
Cohesion: 0.08
Nodes (13): film_piece(), film_ffmpeg(), apply_review_fixes(), pool_pictures(), rewrite_paint_prompts(), ask(), _review_state(), test_auto_fix_graphic() (+5 more)

### Community 54 - "visual_review"
Cohesion: 0.09
Nodes (14): use_picture_from(), clock(), overlay_notes(), paint_new(), quality_check(), review_fixes(), storyboard(), visual_review() (+6 more)

### Community 55 - "scene_kit.py"
Cohesion: 0.08
Nodes (28): hop_off(), sink(), _clearance(), _clip(), _detour(), drink(), facing_now(), _footprints() (+20 more)

### Community 56 - "tree"
Cohesion: 0.25
Nodes (4): clear_distance(), clear_distance_at_end(), surface_z(), tree()

### Community 57 - "test_pictures_first.py"
Cohesion: 0.20
Nodes (15): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+7 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.17
Nodes (22): render_opener(), Env, _people_files(), short(), test_beats_scaled_into_scene(), test_cc_by_credit(), test_crash_retry_then_fallback(), test_failed_checks_fall_back_and_the_try_is_kept() (+14 more)

### Community 59 - "pack_people.py"
Cohesion: 0.26
Nodes (6): base_name(), clip_name(), front(), height(), main(), stride()

### Community 60 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.08
Nodes (21): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+13 more)

### Community 63 - "opener_scene.py"
Cohesion: 0.07
Nodes (24): State, beat_actors(), build_set(), camera(), dress_set(), first_hit(), hold_offscreen(), main() (+16 more)

### Community 64 - "look_toon.py"
Cohesion: 0.27
Nodes (4): apply(), ink(), outline(), toon()

### Community 65 - "paint_instead"
Cohesion: 0.12
Nodes (6): gemini_images(), to_vertical(), ink_silhouette(), paint_instead(), test_ink_silhouette(), test_remotion_failure_paints()

### Community 66 - "use_opener"
Cohesion: 0.13
Nodes (9): use_opener(), test_use_opener_failure_keeps_scene(), test_use_opener_never_raises(), test_use_opener_no_template_ai_clip(), test_use_opener_no_template_note(), test_use_opener_on_success(), test_use_opener_opening_note(), test_use_opener_planner_check() (+1 more)

### Community 67 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 68 - "test_blender_plan.py"
Cohesion: 0.25
Nodes (14): clean_build(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults(), test_clean_build_keeps_a_good_plan(), test_default_build_shape(), test_label_is_short_and_upper(), test_nan_and_infinity_get_defaults() (+6 more)

### Community 69 - "pictures_of"
Cohesion: 0.29
Nodes (4): catalog_text(), is_usable(), pictures_of(), usable()

### Community 70 - "invent_component"
Cohesion: 0.15
Nodes (9): invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), style_rules(), test_good_look_check_skips_the_extra_compile(), test_invention_lint_failure_uses_fallback() (+1 more)

### Community 72 - "sentence_groups"
Cohesion: 0.29
Nodes (6): sentence_groups(), build(), add(), main(), scenes(), test_sentences_running_across_cuts_are_one_take()

### Community 73 - "math"
Cohesion: 0.16
Nodes (5): body(), clip(), key(), main(), part()

### Community 74 - "test_opener_checks.py"
Cohesion: 0.30
Nodes (10): results(), test_blade_face(), test_cut_result(), test_edge_leads(), test_first_frame(), test_hidden(), test_in_frame(), test_moves_visibly() (+2 more)

### Community 76 - "QuestionBeat.tsx"
Cohesion: 0.26
Nodes (6): FONT, theme, Word, CLAMP, KineticTitle(), Overlay

### Community 78 - "drawn_thumbnail"
Cohesion: 0.23
Nodes (9): scene_frames(), drawn_thumbnail(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 79 - "qwen_voice.py"
Cohesion: 0.40
Nodes (3): align(), main(), studio_speak()

### Community 85 - "render"
Cohesion: 0.09
Nodes (12): make_sfx(), short_credit(), video_encoder(), graphics_count(), srt(), drawn_choices(), load_state(), render() (+4 more)

### Community 86 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

### Community 87 - "blender_plan.py"
Cohesion: 0.12
Nodes (8): clamp(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order(), test_thumbnail_order_skips_film_and_puts_openers_first()

### Community 92 - "opener_graphic"
Cohesion: 0.12
Nodes (10): full_formats(), opener_graphic(), rescue_graphics(), max_full(), max_full_planned(), article_text(), fact_check(), test_fact_check_drops_full() (+2 more)

## Knowledge Gaps
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `test_first_second.py`, `ask_ai`, `test_full_scenes.py`, `ffmpeg`, `make`, `gpu.py`, `clean_full`, `test_blender_render.py`, `frame_maker`, `full_cues`, `captions`, `render_remotion`, `json`, `edit_plan`, `re`, `sys`, `apply_review_fixes`, `visual_review`, `test_pictures_first.py`, `paint_instead`, `use_opener`, `drawn_thumbnail`, `wants_remotion`, `opener_graphic`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.14204545454545456 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `Shots`, `math`, `json`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.09032258064516129 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `test_style.py`, `ask_ai`, `pictures_of`, `test_story.py`, `limit_style`, `owner`, `json`, `test_opener_plan.py`, `test_rules.py`, `re`, `pool_of`, `sys`, `clean_full`, `gather_pool`, `clean_look`, `blender_plan.py`, `visual_review`, `opener_graphic`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._
- **Should `test_full_scenes.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08765432098765433 - nodes in this community are weakly interconnected._