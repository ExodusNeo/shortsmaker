# Graph Report - ShortsMaker  (2026-10-27)

## Corpus Check
- 118 files · ~135,371 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 1891 nodes · 5052 edges · 72 communities (66 shown, 6 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 122 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a38b7561`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- motion.py
- toolkit.tsx
- ask_ai
- split_make_shorts.py
- pathlib
- test_h3_handoff.py
- test_opener_scene.py
- Paper
- moves.py
- ffmpeg
- rewrite_paint_prompts
- guarded.tsx
- make
- test_rules.py
- Journey.tsx
- full/types.ts
- pool_of
- test_pictures_first.py
- Local GPU Worker
- style_library
- align_words
- paint_instead
- render_remotion
- test_blender_plan.py
- catalog_pool
- frame_maker
- look.py
- test_full_scenes.py
- render
- parts.py
- hold_offscreen
- gather_pool
- templates.py
- style_placeholders
- test_story.py
- apply_review_fixes
- test_opener_checks.py
- captions
- main
- Short.tsx
- gpu.py
- test_opener_plan.py
- Vector
- test_style.py
- Halftone.tsx
- image_sources.py
- clean_look
- visual_review
- json
- Shots
- test_first_second.py
- ref_remotion
- scene_kit.py
- scene_cues
- choose_images
- test_opener_render.py
- story_sound
- lint_style_code
- opener_checks.py
- test_blender_link.py
- opener_scene.py
- make_sfx
- wants_remotion
- apply_look_scenes
- swap_inventions
- test_blender_scene.py
- owner
- candidate_in
- trim_borders

## God Nodes (most connected - your core abstractions)
1. `render()` - 62 edges
2. `write_scripts()` - 45 edges
3. `ask_ai()` - 39 edges
4. `cut()` - 30 edges
5. `skinOf()` - 29 edges
6. `main()` - 27 edges
7. `render_opener()` - 27 edges
8. `Paper()` - 25 edges
9. `choose_images()` - 24 edges
10. `words_of()` - 22 edges

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

## Communities (72 total, 6 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "motion.py"
Cohesion: 0.15
Nodes (11): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+3 more)

### Community 3 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 4 - "ask_ai"
Cohesion: 0.07
Nodes (22): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), pick_model(), pictures_of(), direct_scripts(), edit_scripts() (+14 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "pathlib"
Cohesion: 0.09
Nodes (12): code_version(), main(), hex_rgb(), luminance(), vault_page(), vault_refresh(), fingerprint(), prune_cache() (+4 more)

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (32): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_closeup_marked_scenes_skip_pause(), test_all_start_pictures_flagged_skips_pause() (+24 more)

### Community 8 - "test_opener_scene.py"
Cohesion: 0.13
Nodes (17): builds(), fixture(), run(), test_bad_plans_fail(), test_box_fall_rests_and_renders(), test_camera_follows_unasked(), test_chicken_chop_reference(), test_chicken_live_plan() (+9 more)

### Community 9 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 10 - "moves.py"
Cohesion: 0.17
Nodes (20): apply(), clear_distance(), fall(), fly_off(), gait(), hop_off(), legs(), push() (+12 more)

### Community 11 - "ffmpeg"
Cohesion: 0.12
Nodes (12): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), motion_prompt(), start_picture_problems(), veo_handoff() (+4 more)

### Community 12 - "rewrite_paint_prompts"
Cohesion: 0.14
Nodes (7): rewrite_paint_prompts(), _fake_planning(), ask(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 14 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

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
Cohesion: 0.13
Nodes (20): catalog_text(), clean_pics(), is_usable(), save_pool(), usable(), entry(), pic_short(), pool_of() (+12 more)

### Community 19 - "test_pictures_first.py"
Cohesion: 0.18
Nodes (14): passing(), prepare(), planning, test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), test_dropped_topic_pool_removed(), prepare() (+6 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.10
Nodes (12): cut_text(), look_text(), approve_candidate(), clean_style_code(), invent_component(), invent_styles(), save_candidate(), style_library() (+4 more)

### Community 22 - "align_words"
Cohesion: 0.15
Nodes (10): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), test_caption_word_counts_match_the_scene_splitter(), test_caption_words_keep_what_is_written(), test_dollar_scale_word_order() (+2 more)

### Community 23 - "paint_instead"
Cohesion: 0.12
Nodes (6): gemini_images(), to_vertical(), ink_silhouette(), paint_instead(), test_ink_silhouette(), test_remotion_failure_paints()

### Community 24 - "render_remotion"
Cohesion: 0.13
Nodes (11): short_skin(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), test_clean_full_custom_and_skin() (+3 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.05
Nodes (44): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+36 more)

### Community 26 - "catalog_pool"
Cohesion: 0.14
Nodes (9): write_json(), catalog_entries(), catalog_pool(), fake_ai, test_catalog_both_empty_stops_uncached(), test_catalog_empty_pool_no_ai(), test_catalog_failure_stops(), test_seo_pass_empty_no_ai() (+1 more)

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (15): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+7 more)

### Community 28 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 29 - "test_full_scenes.py"
Cohesion: 0.05
Nodes (41): clean_sound(), limit_sounds(), graphic_low(), local_voice(), spoken_count(), logbook_results(), clean_full(), word() (+33 more)

### Community 30 - "render"
Cohesion: 0.10
Nodes (14): fix_short(), short_credit(), graphics_count(), rescue_graphics(), srt(), drawn_choices(), load_state(), render() (+6 more)

### Community 31 - "parts.py"
Cohesion: 0.16
Nodes (20): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+12 more)

### Community 32 - "hold_offscreen"
Cohesion: 0.22
Nodes (5): edge_point_local(), handle_end_local(), tool_axes(), tool_rotation(), hold_offscreen()

### Community 33 - "gather_pool"
Cohesion: 0.12
Nodes (11): contact_sheets(), gather_pool(), load_pool(), pool_folder(), prepare_topic(), stubbed, test_empty_pool_drops_topic_without_ai(), test_gather_pool_shape() (+3 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "style_placeholders"
Cohesion: 0.21
Nodes (9): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_slots_restored_after_render() (+1 more)

### Community 36 - "test_story.py"
Cohesion: 0.08
Nodes (22): sentence_groups(), split_takes(), log_short(), duration(), check_twists(), story_problems(), build(), add() (+14 more)

### Community 37 - "apply_review_fixes"
Cohesion: 0.12
Nodes (10): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full() (+2 more)

### Community 39 - "test_opener_checks.py"
Cohesion: 0.08
Nodes (15): call(), fit_start(), frames(), graph(), main(), saved_file(), results(), test_blade_face() (+7 more)

### Community 40 - "captions"
Cohesion: 0.16
Nodes (7): ass_time(), caption_lines(), captions(), styled(), speak(), tts(), ass_colour()

### Community 41 - "main"
Cohesion: 0.16
Nodes (5): keyvis(), main(), Failure, key(), focus_object()

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "gpu.py"
Cohesion: 0.06
Nodes (15): align(), main(), studio_speak(), freesound_fetch(), music_gain(), fills_frame(), comfy_call(), moss_graph() (+7 more)

### Community 44 - "test_opener_plan.py"
Cohesion: 0.12
Nodes (26): clean_opener(), _expect(), fix_plan(), _num(), plan_openers(), ask(), _size(), _stroke() (+18 more)

### Community 45 - "Vector"
Cohesion: 0.10
Nodes (16): bm_area(), box_of(), centre(), clusters(), half(), islands(), join(), merge_slivers() (+8 more)

### Community 46 - "test_style.py"
Cohesion: 0.18
Nodes (8): plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics(), test_library_entries_have_fields(), test_limit_style_caps(), test_save_candidate_unique_slug()

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "image_sources.py"
Cohesion: 0.07
Nodes (20): archive_films(), commons_films(), crop_film_bytes(), film_frames(), film_piece(), nasa_films(), pixabay_films(), shot_span() (+12 more)

### Community 49 - "clean_look"
Cohesion: 0.29
Nodes (5): clean_look(), clean_transition(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 50 - "visual_review"
Cohesion: 0.12
Nodes (11): edit_plan(), picture_line(), clock(), overlay_notes(), quality_check(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate() (+3 more)

### Community 51 - "json"
Cohesion: 0.07
Nodes (21): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+13 more)

### Community 52 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 53 - "test_first_second.py"
Cohesion: 0.18
Nodes (14): first_second_check(), swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples(), test_low_score_opens_on_a_better_real_picture() (+6 more)

### Community 55 - "scene_kit.py"
Cohesion: 0.09
Nodes (22): cut(), to_bm(), to_object(), travel(), add_body(), ensure_world(), facing_vec(), fcurves() (+14 more)

### Community 56 - "scene_cues"
Cohesion: 0.05
Nodes (28): sfx_events(), scene_cues(), get_image(), openverse_images(), ov_get(), full_props(), full_summary(), full_pictures() (+20 more)

### Community 57 - "choose_images"
Cohesion: 0.21
Nodes (13): choose_images(), film(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+5 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.11
Nodes (25): render_opener(), review(), review_frames(), scale_beats(), Env, short(), test_beats_scaled_into_scene(), test_cc_by_credit() (+17 more)

### Community 59 - "story_sound"
Cohesion: 0.40
Nodes (4): story_sound(), test_story_sound_library(), fetch(), _tone_wav()

### Community 60 - "lint_style_code"
Cohesion: 0.40
Nodes (4): attempt(), lint_style_code(), test_invention_lint_failure_uses_fallback(), test_placeholders_match_the_slots()

### Community 61 - "opener_checks.py"
Cohesion: 0.12
Nodes (18): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+10 more)

### Community 62 - "test_blender_link.py"
Cohesion: 0.08
Nodes (25): allowed_licence(), attribution(), call(), credit(), fetch_model(), in_library(), LinkError, ping() (+17 more)

### Community 63 - "opener_scene.py"
Cohesion: 0.09
Nodes (18): State, build_set(), camera(), dress_set(), first_hit(), ground_material(), main(), place_actors() (+10 more)

### Community 68 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 69 - "owner"
Cohesion: 0.15
Nodes (3): owner(), planning_ai(), reply()

### Community 70 - "candidate_in"
Cohesion: 0.25
Nodes (8): candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_candidate_names_unique_across_kinds(), test_reject_deletes()

### Community 74 - "trim_borders"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

## Knowledge Gaps
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `templates.py`, `build_scene.py`, `json`, `Shots`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `pathlib`, `ffmpeg`, `make`, `style_library`, `paint_instead`, `render_remotion`, `test_blender_plan.py`, `frame_maker`, `test_full_scenes.py`, `test_story.py`, `apply_review_fixes`, `captions`, `gpu.py`, `visual_review`, `test_first_second.py`, `scene_cues`, `choose_images`, `story_sound`, `opener_scene.py`, `make_sfx`, `wants_remotion`, `trim_borders`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Should `motion.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14855072463768115 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `test_full_scenes.py` to `gather_pool`, `ask_ai`, `test_story.py`, `pathlib`, `test_opener_plan.py`, `rewrite_paint_prompts`, `test_style.py`, `test_rules.py`, `clean_look`, `pool_of`, `json`, `test_pictures_first.py`, `test_blender_plan.py`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.06794871794871794 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._