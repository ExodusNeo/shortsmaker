# Graph Report - ShortsMaker  (2026-10-27)

## Corpus Check
- 118 files · ~132,528 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 1857 nodes · 4972 edges · 74 communities (66 shown, 8 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 122 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `245ca06a`
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
- cut
- Paper
- travel
- local_clips
- test_blender_link.py
- guarded.tsx
- test_edit_project.py
- test_rules.py
- Journey.tsx
- full/types.ts
- prepare_topic
- write_scripts
- Local GPU Worker
- style_library
- moves.py
- test_blender_scene.py
- render_remotion
- test_blender_plan.py
- music_gain
- frame_maker
- ref_remotion
- words_of
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
- test_opener_plan.py
- Vector
- test_style.py
- Halftone.tsx
- json
- test_pictures_first.py
- edit_plan
- channel_profiles.py
- Shots
- edit_scripts
- rewrite_paint_prompts
- plan_with
- test_full_scenes.py
- choose_images
- test_opener_render.py
- sfx_events
- scene_kit.py
- opener_checks.py
- gather_pool
- opener_scene.py
- paint_instead
- clean_pics
- shutil
- limit_style
- drawn_choices
- catalog_entries
- ffmpeg
- apply_review_fixes
- test_on_topic_ignores_a_lone_shared_name
- film_piece

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
- `test_scene_frames_cover_every_frame_once()` --calls--> `scene_frames()`  [EXTRACTED]
  tests/test_blender_render.py → shortsmaker/blender_render.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`

## Communities (74 total, 8 thin omitted)

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
Cohesion: 0.09
Nodes (17): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), pick_model(), fact_check(), test_fact_check_drops_full(), test_argon_out_of_quota_switches_to_flash() (+9 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.06
Nodes (38): call(), fit_start(), frames(), graph(), main(), saved_file(), h3_problems(), h3_prompt() (+30 more)

### Community 8 - "cut"
Cohesion: 0.11
Nodes (11): bm_area(), cut(), edge_point_local(), handle_end_local(), place_tool(), to_bm(), to_object(), tool_axes() (+3 more)

### Community 9 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 10 - "travel"
Cohesion: 0.25
Nodes (5): clear_distance(), travel(), surface_z(), tree(), world_verts()

### Community 11 - "local_clips"
Cohesion: 0.11
Nodes (12): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt(), start_picture_problems() (+4 more)

### Community 12 - "test_blender_link.py"
Cohesion: 0.08
Nodes (23): allowed_licence(), attribution(), call(), credit(), fetch_model(), in_library(), LinkError, ping() (+15 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 14 - "test_edit_project.py"
Cohesion: 0.12
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (39): draft_rules(), load_rules(), min_real_pictures(), parse_rules(), require_rules(), test_channels_have_opener_rules(), capture_prompts(), ask() (+31 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 18 - "prepare_topic"
Cohesion: 0.17
Nodes (10): write_json(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip() (+2 more)

### Community 19 - "write_scripts"
Cohesion: 0.16
Nodes (14): write_scripts(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare() (+6 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.11
Nodes (14): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), build() (+6 more)

### Community 22 - "moves.py"
Cohesion: 0.17
Nodes (17): apply(), fall(), fly_off(), gait(), hop_off(), push(), release(), roll() (+9 more)

### Community 23 - "test_blender_scene.py"
Cohesion: 0.08
Nodes (29): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+21 more)

### Community 24 - "render_remotion"
Cohesion: 0.13
Nodes (11): make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_make_paper() (+3 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.11
Nodes (22): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+14 more)

### Community 26 - "music_gain"
Cohesion: 0.18
Nodes (5): music_gain(), speak(), story_sound(), tts(), test_music_gain_evens_out_tracks()

### Community 27 - "frame_maker"
Cohesion: 0.06
Nodes (16): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+8 more)

### Community 29 - "words_of"
Cohesion: 0.06
Nodes (31): clean_sound(), limit_sounds(), graphic_low(), clean_photo(), is_stereo(), trim_borders(), border(), plain() (+23 more)

### Community 30 - "render"
Cohesion: 0.16
Nodes (8): short_credit(), graphics_count(), srt(), load_state(), render(), save_state(), use_opener(), test_state_roundtrip_full_pics()

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (23): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+15 more)

### Community 32 - "drawn_thumbnail"
Cohesion: 0.25
Nodes (8): scene_frames(), drawn_thumbnail(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so(), test_thumbnail_uses_the_real_photo()

### Community 33 - "test_blender_render.py"
Cohesion: 0.08
Nodes (25): BlenderFailed, peaks(), render_clips(), _run(), scene_cues(), full_cues(), spoken_at(), spoken_span() (+17 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "invent_component"
Cohesion: 0.12
Nodes (15): clean_style_code(), invent_component(), attempt(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others() (+7 more)

### Community 36 - "test_story.py"
Cohesion: 0.08
Nodes (22): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), check_twists(), story_problems(), test_caption_word_counts_match_the_scene_splitter() (+14 more)

### Community 37 - "test_first_second.py"
Cohesion: 0.17
Nodes (14): logbook_results(), swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples(), test_low_score_opens_on_a_better_real_picture() (+6 more)

### Community 38 - "build_scene.py"
Cohesion: 0.12
Nodes (5): keyvis(), collection(), ink_lines(), linear(), setup()

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
Cohesion: 0.12
Nodes (8): spoken_count(), log_short(), vault_page(), vault_refresh(), is_loop_short(), mark_details(), max_full(), max_full_planned()

### Community 44 - "test_opener_plan.py"
Cohesion: 0.08
Nodes (38): clean_opener(), _expect(), fix_plan(), _num(), plan_openers(), ask(), _size(), _stroke() (+30 more)

### Community 45 - "Vector"
Cohesion: 0.14
Nodes (13): box_of(), centre(), clusters(), half(), islands(), join(), merge_slivers(), pick_island() (+5 more)

### Community 46 - "test_style.py"
Cohesion: 0.14
Nodes (14): wants_remotion(), apply_look_scenes(), candidate_in(), library_snapshot(), restore_library(), test_apply_look_scenes(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure() (+6 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "json"
Cohesion: 0.05
Nodes (29): freesound_fetch(), code_version(), archive_films(), commons_films(), crop_film_bytes(), film_frames(), nasa_films(), pixabay_films() (+21 more)

### Community 49 - "test_pictures_first.py"
Cohesion: 0.15
Nodes (24): catalog_pool(), entry(), fake_ai, film(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film() (+16 more)

### Community 50 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 51 - "channel_profiles.py"
Cohesion: 0.07
Nodes (24): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+16 more)

### Community 52 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 53 - "edit_scripts"
Cohesion: 0.22
Nodes (5): edit_scripts(), length_plan(), narration_lines(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules()

### Community 54 - "rewrite_paint_prompts"
Cohesion: 0.11
Nodes (10): rewrite_paint_prompts(), _fake_planning(), ask(), _review_state(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_redraw_failure_paints(), test_review_redraws_custom() (+2 more)

### Community 55 - "plan_with"
Cohesion: 0.29
Nodes (5): plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 56 - "test_full_scenes.py"
Cohesion: 0.06
Nodes (26): use_picture_from(), short_skin(), full_props(), full_summary(), full_pictures(), limit_full(), paint_new(), _board() (+18 more)

### Community 57 - "choose_images"
Cohesion: 0.23
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.11
Nodes (25): render_opener(), review(), review_frames(), scale_beats(), Env, short(), test_beats_scaled_into_scene(), test_cc_by_credit() (+17 more)

### Community 59 - "sfx_events"
Cohesion: 0.33
Nodes (3): sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 60 - "scene_kit.py"
Cohesion: 0.11
Nodes (16): build_set(), add_body(), ensure_world(), facing_vec(), fcurves(), fit(), interpolation(), layers() (+8 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.13
Nodes (17): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+9 more)

### Community 62 - "gather_pool"
Cohesion: 0.20
Nodes (4): gather_pool(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 63 - "opener_scene.py"
Cohesion: 0.15
Nodes (9): State, camera(), hold_offscreen(), main(), place_actors(), setup(), stand_on(), subject_segments() (+1 more)

### Community 64 - "paint_instead"
Cohesion: 0.12
Nodes (6): gemini_images(), to_vertical(), ink_silhouette(), paint_instead(), test_ink_silhouette(), test_remotion_failure_paints()

### Community 65 - "clean_pics"
Cohesion: 0.17
Nodes (6): catalog_text(), clean_pics(), is_usable(), pictures_of(), usable(), direct_scripts()

### Community 66 - "shutil"
Cohesion: 0.09
Nodes (13): align(), main(), studio_speak(), voicestudio_up(), prune_cache(), prune_work(), approve_candidate(), invent_styles() (+5 more)

### Community 70 - "ffmpeg"
Cohesion: 0.19
Nodes (9): sentence_groups(), split_takes(), duration(), ffmpeg(), first_second_check(), add(), scenes(), test_a_take_is_cut_between_the_scenes_words() (+1 more)

### Community 71 - "apply_review_fixes"
Cohesion: 0.10
Nodes (13): get_image(), clock(), apply_review_fixes(), overlay_notes(), pool_pictures(), quality_check(), review_fixes(), storyboard() (+5 more)

## Knowledge Gaps
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `pathlib`, `local_clips`, `test_edit_project.py`, `moves.py`, `render_remotion`, `music_gain`, `frame_maker`, `words_of`, `drawn_thumbnail`, `test_blender_render.py`, `captions`, `re`, `test_style.py`, `json`, `edit_plan`, `channel_profiles.py`, `test_full_scenes.py`, `choose_images`, `sfx_events`, `paint_instead`, `shutil`, `drawn_choices`, `ffmpeg`, `apply_review_fixes`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `build_scene.py`, `json`, `Shots`, `parts.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Should `motion.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14855072463768115 - nodes in this community are weakly interconnected._
- **Why does `cut()` connect `cut` to `travel`, `Vector`, `moves.py`, `scene_kit.py`, `opener_scene.py`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.09425287356321839 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._