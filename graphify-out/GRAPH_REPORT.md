# Graph Report - ShortsMaker  (2026-10-27)

## Corpus Check
- 118 files · ~132,915 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 1863 nodes · 4989 edges · 82 communities (75 shown, 7 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 122 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `90099ed3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- code_custom_scenes
- toolkit.tsx
- ask_ai
- split_make_shorts.py
- pathlib
- test_h3_handoff.py
- cut
- Paper
- travel
- ffmpeg
- test_blender_link.py
- guarded.tsx
- make
- test_rules.py
- Journey.tsx
- full/types.ts
- catalog_pool
- planning
- Local GPU Worker
- style_library
- moves.py
- test_blender_scene.py
- render_remotion
- test_blender_plan.py
- speak
- frame_maker
- ref_remotion
- test_full_scenes.py
- render
- parts.py
- drawn_thumbnail
- test_blender_render.py
- templates.py
- invent_component
- test_story.py
- test_first_second.py
- build_scene.py
- owner
- captions
- main
- Short.tsx
- re
- test_opener_scene.py
- Vector
- test_style.py
- Halftone.tsx
- image_sources.py
- pool_of
- edit_plan
- json
- Shots
- scene_cues
- rewrite_paint_prompts
- bbox
- full_props
- test_pictures_first.py
- test_opener_render.py
- sfx_events
- scene_kit.py
- opener_checks.py
- fetch_model
- opener_scene.py
- moss_images
- apply_review_fixes
- shutil
- limit_style
- test_opener_checks.py
- fake_ai
- first_second_check
- visual_review
- call
- trim_borders
- use_picture_from
- gemini_model
- run_agy
- Fake
- mark_details
- apply_look_scenes
- test_local_job_retries_a_hard_crash

## God Nodes (most connected - your core abstractions)
1. `render()` - 62 edges
2. `write_scripts()` - 45 edges
3. `ask_ai()` - 39 edges
4. `cut()` - 29 edges
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

## Communities (82 total, 7 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "code_custom_scenes"
Cohesion: 0.13
Nodes (12): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), redraw_custom() (+4 more)

### Community 3 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 4 - "ask_ai"
Cohesion: 0.16
Nodes (9): ask_ai(), test_quota_fallback_both_ways(), test_claude_pinned_to_opus_high(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash(), test_session_shared(), test_solo_ask_ai_hands_over_when_out_of_credits(), test_solo_ask_ai_never_falls_back(), test_solo_brain_selection_options() (+1 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "pathlib"
Cohesion: 0.09
Nodes (5): code_version(), hex_rgb(), luminance(), short_skin(), clean_photo()

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.06
Nodes (38): call(), fit_start(), frames(), graph(), main(), saved_file(), h3_problems(), h3_prompt() (+30 more)

### Community 8 - "cut"
Cohesion: 0.12
Nodes (10): bm_area(), cut(), edge_point_local(), place_tool(), to_bm(), to_object(), tool_axes(), tool_rotation() (+2 more)

### Community 9 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 10 - "travel"
Cohesion: 0.25
Nodes (5): clear_distance(), travel(), surface_z(), tree(), world_verts()

### Community 11 - "ffmpeg"
Cohesion: 0.10
Nodes (17): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt(), split_takes() (+9 more)

### Community 12 - "test_blender_link.py"
Cohesion: 0.24
Nodes (8): search(), _fetch_replies(), execute(), ok(), test_download_error_cleans_up(), test_ping_on_off(), test_search_filters_licences(), with_fake()

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 14 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (40): load_rules(), min_real_pictures(), parse_rules(), test_channels_have_opener_rules(), capture_prompts(), ask(), draft_reply(), make() (+32 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 18 - "catalog_pool"
Cohesion: 0.14
Nodes (14): catalog_entries(), catalog_pool(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_catalog_empty_pool_no_ai() (+6 more)

### Community 19 - "planning"
Cohesion: 0.21
Nodes (12): passing(), prepare(), planning, test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), test_dropped_topic_pool_removed(), prepare() (+4 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.12
Nodes (13): clean_invention(), clean_look(), clean_transition(), settle_style(), approve_candidate(), style_library(), style_rules(), write_style_index() (+5 more)

### Community 22 - "moves.py"
Cohesion: 0.29
Nodes (12): apply(), fall(), fly_off(), hop_off(), push(), release(), roll(), scatter() (+4 more)

### Community 23 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 24 - "render_remotion"
Cohesion: 0.10
Nodes (13): ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions() (+5 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.06
Nodes (30): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+22 more)

### Community 26 - "speak"
Cohesion: 0.20
Nodes (6): speak(), story_sound(), tts(), test_story_sound_library(), fetch(), _tone_wav()

### Community 27 - "frame_maker"
Cohesion: 0.12
Nodes (8): fills_frame(), fit_font(), frame_maker(), graphic_overlay(), person_card(), thumbnail(), credit_tag_image(), fallback_graphic()

### Community 29 - "test_full_scenes.py"
Cohesion: 0.06
Nodes (35): clean_sound(), limit_sounds(), graphic_low(), full_pictures(), rescue_graphics(), clean_full(), word(), clean_graphic() (+27 more)

### Community 30 - "render"
Cohesion: 0.08
Nodes (15): gemini_images(), short_credit(), graphics_count(), to_vertical(), wants_remotion(), srt(), drawn_choices(), load_state() (+7 more)

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (23): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+15 more)

### Community 32 - "drawn_thumbnail"
Cohesion: 0.23
Nodes (9): scene_frames(), drawn_thumbnail(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 33 - "test_blender_render.py"
Cohesion: 0.17
Nodes (13): BlenderFailed, peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises() (+5 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "invent_component"
Cohesion: 0.11
Nodes (17): clean_style_code(), invent_component(), attempt(), invent_styles(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview() (+9 more)

### Community 36 - "test_story.py"
Cohesion: 0.06
Nodes (28): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), sentence_groups(), check_twists(), story_problems() (+20 more)

### Community 37 - "test_first_second.py"
Cohesion: 0.21
Nodes (12): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once() (+4 more)

### Community 38 - "build_scene.py"
Cohesion: 0.12
Nodes (5): keyvis(), collection(), ink_lines(), linear(), setup()

### Community 39 - "owner"
Cohesion: 0.13
Nodes (5): owner(), film(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 40 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 41 - "main"
Cohesion: 0.17
Nodes (4): main(), Failure, key(), focus_object()

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "re"
Cohesion: 0.09
Nodes (12): music_gain(), allowed_licence(), words(), shot_span(), log_short(), vault_page(), vault_refresh(), duration() (+4 more)

### Community 44 - "test_opener_scene.py"
Cohesion: 0.07
Nodes (39): clean_opener(), _expect(), fix_plan(), _num(), plan_openers(), ask(), _size(), _stroke() (+31 more)

### Community 45 - "Vector"
Cohesion: 0.14
Nodes (13): box_of(), centre(), clusters(), half(), islands(), join(), merge_slivers(), pick_island() (+5 more)

### Community 46 - "test_style.py"
Cohesion: 0.13
Nodes (16): save_candidate(), candidate_in(), library_snapshot(), plan_with(), ask(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure() (+8 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "image_sources.py"
Cohesion: 0.06
Nodes (24): archive_films(), commons_films(), crop_film_bytes(), film_frames(), film_piece(), nasa_films(), pixabay_films(), archive_images() (+16 more)

### Community 49 - "pool_of"
Cohesion: 0.16
Nodes (17): catalog_text(), clean_pics(), is_usable(), usable(), entry(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+9 more)

### Community 50 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 51 - "json"
Cohesion: 0.05
Nodes (36): freesound_fetch(), ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel() (+28 more)

### Community 52 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 53 - "scene_cues"
Cohesion: 0.14
Nodes (10): scene_cues(), full_cues(), spoken_at(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish(), test_graphic_card_hold_duration() (+2 more)

### Community 54 - "rewrite_paint_prompts"
Cohesion: 0.18
Nodes (6): rewrite_paint_prompts(), _fake_planning(), ask(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_rewrite_paint_prompts()

### Community 55 - "bbox"
Cohesion: 0.21
Nodes (8): build_set(), place_actors(), stand_on(), bbox(), fit(), load_model(), material(), merge()

### Community 56 - "full_props"
Cohesion: 0.22
Nodes (7): full_props(), full_summary(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_full_summary(), test_remotion_props_full()

### Community 57 - "test_pictures_first.py"
Cohesion: 0.21
Nodes (14): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+6 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.11
Nodes (24): render_opener(), review(), review_frames(), scale_beats(), Env, short(), test_beats_scaled_into_scene(), test_cc_by_credit() (+16 more)

### Community 59 - "sfx_events"
Cohesion: 0.33
Nodes (3): sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 60 - "scene_kit.py"
Cohesion: 0.16
Nodes (13): walk(), add_body(), ensure_world(), facing_vec(), fcurves(), interpolation(), key_rot(), layers() (+5 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.13
Nodes (17): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+9 more)

### Community 62 - "fetch_model"
Cohesion: 0.19
Nodes (8): attribution(), credit(), fetch_model(), in_library(), resolve_models(), test_fetch_saves_pair(), test_in_library(), test_switched_off_reason()

### Community 63 - "opener_scene.py"
Cohesion: 0.10
Nodes (12): gait(), handle_end_local(), State, camera(), first_hit(), hold_offscreen(), main(), punch_in() (+4 more)

### Community 64 - "moss_images"
Cohesion: 0.20
Nodes (5): comfy_call(), moss_graph(), moss_images(), paint_instead(), test_remotion_failure_paints()

### Community 65 - "apply_review_fixes"
Cohesion: 0.18
Nodes (6): apply_review_fixes(), _review_state(), test_auto_fix_graphic(), test_redraw_failure_paints(), test_review_redraws_custom(), test_review_uses_unused_pool_pictures_before_painting()

### Community 66 - "shutil"
Cohesion: 0.09
Nodes (12): align(), main(), studio_speak(), voicestudio_up(), preview_sheet(), tsc_check(), prune_cache(), library_menu() (+4 more)

### Community 68 - "test_opener_checks.py"
Cohesion: 0.33
Nodes (9): results(), test_blade_face(), test_cut_result(), test_edge_leads(), test_first_frame(), test_hidden(), test_in_frame(), test_overlap() (+1 more)

### Community 69 - "fake_ai"
Cohesion: 0.20
Nodes (5): fake_ai, planning_ai(), reply(), test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list()

### Community 70 - "first_second_check"
Cohesion: 0.22
Nodes (4): first_second_check(), quality_check(), storyboard(), test_opener_prompt_shows_each_scenes_line_and_picture()

### Community 71 - "visual_review"
Cohesion: 0.24
Nodes (7): clock(), overlay_notes(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 72 - "call"
Cohesion: 0.20
Nodes (5): call(), LinkError, ping(), blender_note(), test_blender_note()

### Community 74 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

### Community 75 - "use_picture_from"
Cohesion: 0.29
Nodes (4): use_picture_from(), paint_new(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 76 - "gemini_model"
Cohesion: 0.40
Nodes (4): gemini_model(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_gemini_timeout_switches_to_flash()

### Community 77 - "run_agy"
Cohesion: 0.33
Nodes (3): quota_exhausted(), run_agy(), test_run_agy_flags_and_boundaries()

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `templates.py`, `build_scene.py`, `json`, `Shots`, `parts.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `pathlib`, `ffmpeg`, `make`, `render_remotion`, `test_blender_plan.py`, `speak`, `frame_maker`, `test_full_scenes.py`, `drawn_thumbnail`, `test_blender_render.py`, `captions`, `re`, `test_style.py`, `edit_plan`, `json`, `scene_cues`, `full_props`, `test_pictures_first.py`, `sfx_events`, `opener_scene.py`, `moss_images`, `apply_review_fixes`, `shutil`, `first_second_check`, `visual_review`, `mark_details`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Should `code_custom_scenes` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Why does `cut()` connect `cut` to `travel`, `Vector`, `moves.py`, `bbox`, `scene_kit.py`, `opener_scene.py`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._
- **Should `pathlib` be split into smaller, more focused modules?**
  _Cohesion score 0.09473684210526316 - nodes in this community are weakly interconnected._