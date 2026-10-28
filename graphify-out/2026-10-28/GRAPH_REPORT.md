# Graph Report - ShortsMaker  (2026-10-28)

## Corpus Check
- 124 files · ~150,628 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 2097 nodes · 5510 edges · 80 communities (71 shown, 9 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 129 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `39d84665`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- motion.py
- toolkit.tsx
- ask_ai
- split_make_shorts.py
- test_full_scenes.py
- short_with
- test_opener_scene.py
- Paper
- test_story.py
- local_clips
- moves.py
- guarded.tsx
- re
- test_rules.py
- Journey.tsx
- full/types.ts
- pool_of
- write_scripts
- Local GPU Worker
- style_library
- test_blender_scene.py
- apply_review_fixes
- local_job
- frame_maker
- fake_ai
- ClipReader
- full_cues
- clean_full
- look.py
- parts.py
- people.py
- prepare_topic
- templates.py
- ask
- align_words
- rescue_graphics
- bpy
- h3_run.py
- load_model
- main
- Short.tsx
- json
- test_opener_plan.py
- cut
- Halftone.tsx
- fetch
- test_blender_link.py
- gather_pool
- channel_profiles.py
- full_props
- test_first_second.py
- write_frames
- scene_kit.py
- test_h3_handoff.py
- test_pictures_first.py
- test_opener_render.py
- pack_people.py
- test_opener_checks.py
- opener_checks.py
- ref_remotion
- opener_scene.py
- look_toon.py
- person_card
- sfx_events
- scene_cues
- test_blender_plan.py
- owner
- render_remotion
- gemini_images
- make_sfx
- h3_problems
- trim_borders
- h3_prompt
- test_short_credit
- test_owner_clip_is_cut_again_for_the_scene_it_now_sits_in
- limit_style
- render

## God Nodes (most connected - your core abstractions)
1. `render()` - 63 edges
2. `write_scripts()` - 45 edges
3. `ask_ai()` - 40 edges
4. `render_opener()` - 36 edges
5. `run()` - 33 edges
6. `fixture()` - 31 edges
7. `cut()` - 30 edges
8. `skinOf()` - 29 edges
9. `main()` - 27 edges
10. `Env` - 27 edges

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

## Communities (80 total, 9 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "motion.py"
Cohesion: 0.13
Nodes (13): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+5 more)

### Community 3 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 4 - "ask_ai"
Cohesion: 0.09
Nodes (16): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), mark_details(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run() (+8 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "test_full_scenes.py"
Cohesion: 0.11
Nodes (4): code_version(), hex_rgb(), luminance(), fingerprint()

### Community 7 - "short_with"
Cohesion: 0.23
Nodes (14): fake_ai(), short_with(), test_all_closeup_marked_scenes_skip_pause(), test_missing_scene_is_asked_again(), run(), test_retries_only_failing_scene_with_reason(), run(), test_scene_number_given_as_text_is_accepted() (+6 more)

### Community 8 - "test_opener_scene.py"
Cohesion: 0.06
Nodes (37): builds(), fixture(), people_lib(), run(), test_bad_plans_fail(), test_box_fall_rests_and_renders(), test_camera_follows_unasked(), test_chicken_chop_reference() (+29 more)

### Community 9 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 10 - "test_story.py"
Cohesion: 0.08
Nodes (21): local_voice(), sentence_groups(), split_takes(), spoken_count(), voicestudio_unload(), voicestudio_up(), is_loop_short(), check_twists() (+13 more)

### Community 11 - "local_clips"
Cohesion: 0.16
Nodes (9): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), motion_prompt(), start_picture_problems(), veo_handoff(), video_encoder() (+1 more)

### Community 12 - "moves.py"
Cohesion: 0.12
Nodes (21): apply(), clear_distance_at_end(), fall(), fly_off(), gait(), hop_off(), legs(), push() (+13 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 14 - "re"
Cohesion: 0.06
Nodes (20): allowed_licence(), in_library(), words(), caption_layer(), make(), master_gain(), project_xml(), remove() (+12 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (41): load_rules(), min_real_pictures(), parse_rules(), test_channels_have_opener_rules(), capture_prompts(), ask(), draft_reply(), make() (+33 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 18 - "pool_of"
Cohesion: 0.11
Nodes (24): write_json(), catalog_entries(), catalog_pool(), catalog_text(), clean_pics(), is_usable(), save_pool(), usable() (+16 more)

### Community 19 - "write_scripts"
Cohesion: 0.09
Nodes (22): pictures_of(), limit_full(), direct_scripts(), edit_scripts(), length_plan(), narration_lines(), write_scripts(), test_limit_full() (+14 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.06
Nodes (26): cut_text(), edit_plan(), look_text(), picture_line(), clean_invention(), clean_look(), clean_transition(), settle_style() (+18 more)

### Community 22 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 23 - "apply_review_fixes"
Cohesion: 0.15
Nodes (7): use_picture_from(), apply_review_fixes(), paint_new(), rewrite_paint_prompts(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 24 - "local_job"
Cohesion: 0.10
Nodes (9): local_job(), to_vertical(), ink_silhouette(), make_paper(), paint_instead(), test_ink_silhouette(), test_local_job_retries_a_hard_crash(), test_make_paper() (+1 more)

### Community 25 - "frame_maker"
Cohesion: 0.18
Nodes (4): fills_frame(), frame_maker(), credit_tag_image(), fallback_graphic()

### Community 26 - "fake_ai"
Cohesion: 0.18
Nodes (6): fake_ai, planning_ai(), reply(), test_catalog_empty_pool_no_ai(), test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list()

### Community 27 - "ClipReader"
Cohesion: 0.19
Nodes (5): ClipReader, draw_card(), draw_graphic(), frame(), shot()

### Community 28 - "full_cues"
Cohesion: 0.20
Nodes (6): full_cues(), spoken_at(), spoken_span(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish()

### Community 29 - "clean_full"
Cohesion: 0.08
Nodes (25): clean_sound(), limit_sounds(), graphic_low(), archive_images(), clean_full(), word(), clean_graphic(), contains() (+17 more)

### Community 30 - "look.py"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (23): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+15 more)

### Community 32 - "people.py"
Cohesion: 0.07
Nodes (21): _append(), _attach(), _bake_free(), base_name(), _body_tree(), _clearance(), _colour(), _detour() (+13 more)

### Community 33 - "prepare_topic"
Cohesion: 0.22
Nodes (7): contact_sheets(), load_pool(), pool_folder(), prepare_topic(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip(), test_small_pool_skips_ai()

### Community 34 - "templates.py"
Cohesion: 0.17
Nodes (15): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge() (+7 more)

### Community 35 - "ask"
Cohesion: 0.14
Nodes (7): ask(), _review_state(), test_look_check_fixes_code(), test_redraw_failure_paints(), test_review_redraws_custom(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 36 - "align_words"
Cohesion: 0.15
Nodes (10): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), test_caption_word_counts_match_the_scene_splitter(), test_caption_words_keep_what_is_written(), test_dollar_scale_word_order() (+2 more)

### Community 37 - "rescue_graphics"
Cohesion: 0.10
Nodes (13): full_summary(), full_formats(), opener_graphic(), rescue_graphics(), article_text(), fact_check(), test_fact_check_drops_full(), test_full_props_figure() (+5 more)

### Community 38 - "bpy"
Cohesion: 0.12
Nodes (5): body(), clip(), key(), main(), part()

### Community 39 - "h3_run.py"
Cohesion: 0.22
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 40 - "load_model"
Cohesion: 0.25
Nodes (4): ground_material(), load_model(), material(), merge()

### Community 41 - "main"
Cohesion: 0.11
Nodes (7): direction(), keyloc(), keyvis(), main(), Shots, Failure, key()

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "json"
Cohesion: 0.07
Nodes (16): align(), main(), studio_speak(), freesound_fetch(), comfy_call(), moss_graph(), moss_images(), prune_cache() (+8 more)

### Community 44 - "test_opener_plan.py"
Cohesion: 0.08
Nodes (36): clean_opener(), _expect(), fix_plan(), _num(), plan_openers(), ask(), _size(), _stroke() (+28 more)

### Community 45 - "cut"
Cohesion: 0.08
Nodes (23): bm_area(), box_of(), centre(), clusters(), cut(), edge_point_local(), half(), handle_end_local() (+15 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "fetch"
Cohesion: 0.06
Nodes (22): archive_films(), commons_films(), crop_film_bytes(), film_frames(), film_piece(), nasa_films(), pixabay_films(), shot_span() (+14 more)

### Community 49 - "test_blender_link.py"
Cohesion: 0.10
Nodes (18): attribution(), call(), credit(), fetch_model(), LinkError, search(), Fake, _fetch_replies() (+10 more)

### Community 50 - "gather_pool"
Cohesion: 0.13
Nodes (8): article_images(), commons_search(), thumb_url(), wm_files(), gather_pool(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 51 - "channel_profiles.py"
Cohesion: 0.07
Nodes (23): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+15 more)

### Community 52 - "full_props"
Cohesion: 0.29
Nodes (6): full_props(), _board(), _jpg(), test_custom_cues_props_and_pictures(), test_remotion_props_full(), test_sfx_full()

### Community 53 - "test_first_second.py"
Cohesion: 0.19
Nodes (14): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once() (+6 more)

### Community 54 - "write_frames"
Cohesion: 0.29
Nodes (3): flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 55 - "scene_kit.py"
Cohesion: 0.07
Nodes (26): clear_distance(), travel(), _clip(), _footprints(), _ground(), move(), pick_up(), _strip() (+18 more)

### Community 56 - "test_h3_handoff.py"
Cohesion: 0.21
Nodes (13): unpack_clips(), handoff(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated(), test_flagged_start_picture_is_not_sent(), test_handoff_picks_up_clips_zip(), test_handoff_records_which_file_made_the_clip(), test_handoff_writes_jobs_and_zip() (+5 more)

### Community 57 - "test_pictures_first.py"
Cohesion: 0.16
Nodes (17): choose_images(), apply_look_scenes(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+9 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.06
Nodes (44): ping(), blender_note(), _cast_note(), pick_model(), render_opener(), resolve_models(), review(), review_frames() (+36 more)

### Community 59 - "pack_people.py"
Cohesion: 0.26
Nodes (6): base_name(), clip_name(), front(), height(), main(), stride()

### Community 60 - "test_opener_checks.py"
Cohesion: 0.30
Nodes (10): results(), test_blade_face(), test_cut_result(), test_edge_leads(), test_first_frame(), test_hidden(), test_in_frame(), test_moves_visibly() (+2 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.09
Nodes (19): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+11 more)

### Community 63 - "opener_scene.py"
Cohesion: 0.08
Nodes (25): State, in_frame(), beat_actors(), build_set(), camera(), checks(), dress_set(), first_hit() (+17 more)

### Community 64 - "look_toon.py"
Cohesion: 0.27
Nodes (4): apply(), ink(), outline(), toon()

### Community 65 - "person_card"
Cohesion: 0.33
Nodes (3): fit_font(), graphic_overlay(), person_card()

### Community 66 - "sfx_events"
Cohesion: 0.33
Nodes (3): sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 67 - "scene_cues"
Cohesion: 0.33
Nodes (5): scene_cues(), test_counter_finishes_before_it_leaves(), test_graphic_card_hold_duration(), test_person_card_hold_and_exit_gap(), test_scene_hold_padding()

### Community 68 - "test_blender_plan.py"
Cohesion: 0.05
Nodes (44): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+36 more)

### Community 69 - "owner"
Cohesion: 0.14
Nodes (8): owner(), _fake_planning(), test_director_prompt_mentions_full(), film(), plan_with(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_good_look_check_skips_the_extra_compile()

### Community 70 - "render_remotion"
Cohesion: 0.05
Nodes (32): ass_time(), caption_lines(), captions(), styled(), ass_colour(), short_skin(), render_remotion(), remotion() (+24 more)

### Community 74 - "trim_borders"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 85 - "render"
Cohesion: 0.05
Nodes (31): music_gain(), speak(), story_sound(), tts(), thumbnail(), short_credit(), clock(), duration() (+23 more)

## Knowledge Gaps
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `ask_ai`, `test_full_scenes.py`, `test_story.py`, `local_clips`, `re`, `style_library`, `apply_review_fixes`, `local_job`, `frame_maker`, `clean_full`, `rescue_graphics`, `json`, `channel_profiles.py`, `write_frames`, `test_pictures_first.py`, `test_opener_render.py`, `opener_scene.py`, `sfx_events`, `scene_cues`, `test_blender_plan.py`, `render_remotion`, `gemini_images`, `make_sfx`, `trim_borders`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `prepare_topic`, `test_blender_plan.py`, `ask_ai`, `test_full_scenes.py`, `rescue_graphics`, `owner`, `test_story.py`, `json`, `test_opener_plan.py`, `re`, `limit_style`, `test_rules.py`, `pool_of`, `channel_profiles.py`, `style_library`, `clean_full`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Should `motion.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13230769230769232 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `json`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.09425287356321839 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._