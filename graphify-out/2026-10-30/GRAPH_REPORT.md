# Graph Report - ShortsMaker  (2026-10-30)

## Corpus Check
- 129 files · ~155,410 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 2152 nodes · 5675 edges · 83 communities (77 shown, 6 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 128 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b96206f1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- first_second_check
- plan_with
- ask_ai
- split_make_shorts.py
- gpu.py
- code_custom_scenes
- test_opener_scene.py
- guarded.tsx
- Paper
- test_h3_handoff.py
- walk
- test_style.py
- make
- test_rules.py
- Journey.tsx
- toolkit.tsx
- test_pictures_first.py
- write_scripts
- Local GPU Worker
- style_library
- ffmpeg
- clean_full
- full/types.ts
- test_blender_render.py
- fetch_model
- frame_maker
- opener_graphic
- captions
- look.py
- parts.py
- _hold
- render_remotion
- templates.py
- image_sources.py
- time
- test_full_scenes.py
- test_blender_link.py
- h3_run.py
- dress
- main
- Short.tsx
- opener_render.py
- test_opener_plan.py
- moves.py
- sfx_events
- Halftone.tsx
- re
- blender_link.py
- gather_pool
- channel_profiles.py
- test_edit_project.py
- apply_review_fixes
- visual_review
- scene_kit.py
- tree
- choose_images
- test_opener_render.py
- pack_people.py
- test_blender_scene.py
- opener_checks.py
- Fake
- opener_scene.py
- look_toon.py
- test_package.py
- full_cues
- Shots
- rewrite_paint_prompts
- prepare_topic
- edit_scripts
- limit_style
- test_story.py
- math
- test_opener_checks.py
- film_piece
- check_twists
- drawn_thumbnail
- ref_remotion
- test_local_job_retries_a_hard_crash
- render
- trim_borders
- json

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

## Communities (83 total, 6 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "first_second_check"
Cohesion: 0.17
Nodes (13): first_second_check(), swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once() (+5 more)

### Community 3 - "plan_with"
Cohesion: 0.29
Nodes (5): plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 4 - "ask_ai"
Cohesion: 0.09
Nodes (16): seed_ideas(), ask_ai(), gemini_model(), quota_exhausted(), run_agy(), mark_details(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash() (+8 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "gpu.py"
Cohesion: 0.08
Nodes (11): hex_rgb(), luminance(), crop_film_bytes(), film_frames(), shot_span(), fills_frame(), person_card(), duration() (+3 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.12
Nodes (13): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+5 more)

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

### Community 12 - "walk"
Cohesion: 0.22
Nodes (7): gait(), legs(), share_of_gap(), walk(), facing_vec(), key_swing(), leg_rig()

### Community 13 - "test_style.py"
Cohesion: 0.11
Nodes (17): tsc_check(), approve_candidate(), invent_styles(), library_menu(), reject_candidate(), save_candidate(), swap_inventions(), candidate_in() (+9 more)

### Community 14 - "make"
Cohesion: 0.21
Nodes (4): caption_layer(), make(), master_gain(), project_xml()

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (41): load_rules(), min_real_pictures(), parse_rules(), test_channels_have_opener_rules(), capture_prompts(), ask(), draft_reply(), make() (+33 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 18 - "test_pictures_first.py"
Cohesion: 0.10
Nodes (30): write_json(), catalog_entries(), catalog_pool(), save_pool(), entry(), fake_ai, film(), pic_short() (+22 more)

### Community 19 - "write_scripts"
Cohesion: 0.13
Nodes (20): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+12 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.07
Nodes (21): cut_text(), edit_plan(), look_text(), picture_line(), clean_invention(), clean_look(), clean_transition(), settle_style() (+13 more)

### Community 22 - "ffmpeg"
Cohesion: 0.09
Nodes (18): cosy_instruct(), cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt() (+10 more)

### Community 23 - "clean_full"
Cohesion: 0.08
Nodes (24): clean_sound(), limit_sounds(), graphic_low(), clean_full(), word(), clean_graphic(), contains(), coords() (+16 more)

### Community 24 - "full/types.ts"
Cohesion: 0.16
Nodes (17): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+9 more)

### Community 25 - "test_blender_render.py"
Cohesion: 0.17
Nodes (13): BlenderFailed, peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises() (+5 more)

### Community 26 - "fetch_model"
Cohesion: 0.20
Nodes (7): fetch_model(), in_library(), words(), model_for(), pick_model(), resolve_models(), test_in_library()

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (14): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+6 more)

### Community 28 - "opener_graphic"
Cohesion: 0.11
Nodes (12): full_props(), full_summary(), to_glb(), full_formats(), opener_graphic(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure() (+4 more)

### Community 29 - "captions"
Cohesion: 0.10
Nodes (12): ass_time(), captions(), styled(), music_gain(), speak(), story_sound(), tts(), ass_colour() (+4 more)

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
Cohesion: 0.06
Nodes (29): caption_lines(), short_skin(), ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback() (+21 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "image_sources.py"
Cohesion: 0.09
Nodes (18): archive_films(), commons_films(), nasa_films(), pixabay_films(), archive_images(), article_images(), commons_search(), get_image() (+10 more)

### Community 36 - "time"
Cohesion: 0.10
Nodes (15): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+7 more)

### Community 38 - "test_blender_link.py"
Cohesion: 0.27
Nodes (8): credit(), _fetch_replies(), execute(), ok(), test_download_error_cleans_up(), test_fetch_saves_pair(), test_switched_off_reason(), with_fake()

### Community 39 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 40 - "dress"
Cohesion: 0.11
Nodes (10): ground_material(), _append(), _attach(), base_name(), _colour(), dress(), _is_blade(), load_model() (+2 more)

### Community 41 - "main"
Cohesion: 0.16
Nodes (5): keyvis(), main(), Failure, key(), focus_object()

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "opener_render.py"
Cohesion: 0.13
Nodes (7): code_version(), _cast_note(), fingerprint(), review(), review_frames(), scale_beats(), build()

### Community 44 - "test_opener_plan.py"
Cohesion: 0.07
Nodes (38): clean_opener(), _expect(), fill_template(), _keep(), _num(), plan_openers(), ask(), _size() (+30 more)

### Community 45 - "moves.py"
Cohesion: 0.07
Nodes (36): apply(), bm_area(), box_of(), centre(), clusters(), cut(), edge_point_local(), fall() (+28 more)

### Community 46 - "sfx_events"
Cohesion: 0.18
Nodes (7): sfx_events(), full_pictures(), _board(), test_board_pictures_attached(), test_sfx_full(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "re"
Cohesion: 0.08
Nodes (18): log_short(), logbook_results(), vault_page(), vault_refresh(), parse_scene_money(), clean_style_code(), clash(), fetch_ideas() (+10 more)

### Community 49 - "blender_link.py"
Cohesion: 0.13
Nodes (10): allowed_licence(), attribution(), call(), LinkError, ping(), search(), blender_note(), test_ping_on_off() (+2 more)

### Community 50 - "gather_pool"
Cohesion: 0.12
Nodes (7): gather_pool(), owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 51 - "channel_profiles.py"
Cohesion: 0.08
Nodes (22): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+14 more)

### Community 52 - "test_edit_project.py"
Cohesion: 0.27
Nodes (5): remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers(), videos()

### Community 53 - "apply_review_fixes"
Cohesion: 0.12
Nodes (10): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full() (+2 more)

### Community 54 - "visual_review"
Cohesion: 0.18
Nodes (8): clock(), overlay_notes(), quality_check(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 55 - "scene_kit.py"
Cohesion: 0.08
Nodes (28): hop_off(), sink(), _clearance(), _clip(), _detour(), drink(), facing_now(), _footprints() (+20 more)

### Community 56 - "tree"
Cohesion: 0.25
Nodes (4): clear_distance(), clear_distance_at_end(), surface_z(), tree()

### Community 57 - "choose_images"
Cohesion: 0.19
Nodes (14): choose_images(), apply_look_scenes(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+6 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.09
Nodes (33): render_opener(), use_opener(), Env, _people_files(), short(), test_beats_scaled_into_scene(), test_cc_by_credit(), test_crash_retry_then_fallback() (+25 more)

### Community 59 - "pack_people.py"
Cohesion: 0.26
Nodes (6): base_name(), clip_name(), front(), height(), main(), stride()

### Community 60 - "test_blender_scene.py"
Cohesion: 0.07
Nodes (42): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+34 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.08
Nodes (21): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+13 more)

### Community 63 - "opener_scene.py"
Cohesion: 0.07
Nodes (24): State, beat_actors(), build_set(), camera(), dress_set(), first_hit(), hold_offscreen(), main() (+16 more)

### Community 64 - "look_toon.py"
Cohesion: 0.27
Nodes (4): apply(), ink(), outline(), toon()

### Community 65 - "test_package.py"
Cohesion: 0.22
Nodes (5): scene_cues(), test_counter_finishes_before_it_leaves(), test_graphic_card_hold_duration(), test_person_card_hold_and_exit_gap(), test_scene_hold_padding()

### Community 66 - "full_cues"
Cohesion: 0.20
Nodes (6): full_cues(), spoken_at(), spoken_span(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish()

### Community 67 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 68 - "rewrite_paint_prompts"
Cohesion: 0.18
Nodes (5): rewrite_paint_prompts(), ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 69 - "prepare_topic"
Cohesion: 0.10
Nodes (12): catalog_text(), clean_pics(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), prepare_topic() (+4 more)

### Community 70 - "edit_scripts"
Cohesion: 0.22
Nodes (5): edit_scripts(), length_plan(), narration_lines(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules()

### Community 72 - "test_story.py"
Cohesion: 0.21
Nodes (7): sentence_groups(), story_problems(), test_no_hook_setting_no_hook_check(), test_sentences_running_across_cuts_are_one_take(), test_story_problems(), test_story_problems_flags_summary_hook(), test_story_problems_money_claim()

### Community 73 - "math"
Cohesion: 0.16
Nodes (5): body(), clip(), key(), main(), part()

### Community 74 - "test_opener_checks.py"
Cohesion: 0.30
Nodes (10): results(), test_blade_face(), test_cut_result(), test_edge_leads(), test_first_frame(), test_hidden(), test_in_frame(), test_moves_visibly() (+2 more)

### Community 76 - "check_twists"
Cohesion: 0.47
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 78 - "drawn_thumbnail"
Cohesion: 0.23
Nodes (9): scene_frames(), drawn_thumbnail(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 85 - "render"
Cohesion: 0.07
Nodes (14): make_sfx(), gemini_images(), short_credit(), graphics_count(), to_vertical(), wants_remotion(), srt(), drawn_choices() (+6 more)

### Community 86 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

### Community 92 - "json"
Cohesion: 0.07
Nodes (18): freesound_fetch(), comfy_call(), moss_graph(), moss_images(), voicestudio_unload(), save_try(), rescue_graphics(), paint_instead() (+10 more)

## Knowledge Gaps
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `first_second_check`, `ask_ai`, `gpu.py`, `test_style.py`, `make`, `style_library`, `ffmpeg`, `clean_full`, `test_blender_render.py`, `frame_maker`, `opener_graphic`, `captions`, `render_remotion`, `sfx_events`, `re`, `channel_profiles.py`, `test_edit_project.py`, `apply_review_fixes`, `visual_review`, `choose_images`, `test_opener_render.py`, `test_package.py`, `drawn_thumbnail`, `json`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `Shots`, `math`, `json`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.09230769230769231 - nodes in this community are weakly interconnected._
- **Why does `choose_images()` connect `choose_images` to `image_sources.py`, `ask_ai`, `test_full_scenes.py`, `prepare_topic`, `film_piece`, `sfx_events`, `test_rules.py`, `gather_pool`, `channel_profiles.py`, `style_library`, `render`, `clean_full`, `json`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._
- **Should `gpu.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07597895967270601 - nodes in this community are weakly interconnected._