# Graph Report - ShortsMaker  (2026-10-27)

## Corpus Check
- 118 files · ~134,889 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 1884 nodes · 5037 edges · 76 communities (72 shown, 4 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 122 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1f538675`
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
- align_words
- Paper
- travel
- local_clips
- json
- guarded.tsx
- make
- test_rules.py
- Journey.tsx
- full/types.ts
- catalog_pool
- test_pictures_first.py
- Local GPU Worker
- clean_look
- gather_pool
- ffmpeg
- render_remotion
- test_blender_plan.py
- story_sound
- frame_maker
- ref_remotion
- plan_rules.py
- render
- parts.py
- cut
- words_of
- templates.py
- invent_component
- test_story.py
- test_first_second.py
- build_scene.py
- h3_run.py
- captions
- main
- Short.tsx
- gpu.py
- test_opener_scene.py
- Vector
- test_style.py
- Halftone.tsx
- image_sources.py
- pool_of
- style_library
- channel_profiles.py
- Shots
- re
- make_paper
- scene_kit.py
- test_full_scenes.py
- choose_images
- test_opener_render.py
- test_edit_project.py
- moves.py
- opener_checks.py
- test_blender_link.py
- opener_scene.py
- random
- full_cues
- shutil
- write_scripts
- test_blender_scene.py
- owner
- candidate_in
- visual_review
- rescue_graphics
- srt
- trim_borders
- apply_look_scenes

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

## Communities (76 total, 4 thin omitted)

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
Nodes (19): scene_cues(), ask_ai(), gemini_model(), quota_exhausted(), run_agy(), test_counter_finishes_before_it_leaves(), test_argon_out_of_quota_switches_to_flash(), fake_run() (+11 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "pathlib"
Cohesion: 0.10
Nodes (7): hex_rgb(), luminance(), crop_film_bytes(), person_card(), clean_photo(), contact_sheets(), storyboard()

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (32): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_closeup_marked_scenes_skip_pause(), test_all_start_pictures_flagged_skips_pause() (+24 more)

### Community 8 - "align_words"
Cohesion: 0.14
Nodes (10): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), test_caption_word_counts_match_the_scene_splitter(), test_caption_words_keep_what_is_written(), test_dollar_scale_word_order() (+2 more)

### Community 9 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 10 - "travel"
Cohesion: 0.25
Nodes (5): clear_distance(), travel(), surface_z(), tree(), world_verts()

### Community 11 - "local_clips"
Cohesion: 0.16
Nodes (9): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), motion_prompt(), start_picture_problems(), veo_handoff(), video_encoder() (+1 more)

### Community 12 - "json"
Cohesion: 0.11
Nodes (10): freesound_fetch(), code_version(), pixabay_films(), fingerprint(), pick_model(), rewrite_paint_prompts(), article_text(), direct_scripts() (+2 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 14 - "make"
Cohesion: 0.21
Nodes (4): caption_layer(), make(), master_gain(), project_xml()

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
Cohesion: 0.11
Nodes (18): write_json(), catalog_entries(), catalog_pool(), load_pool(), pool_folder(), prepare_topic(), save_pool(), fake_ai (+10 more)

### Community 19 - "test_pictures_first.py"
Cohesion: 0.19
Nodes (14): passing(), prepare(), planning, test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), test_dropped_topic_pool_removed(), prepare() (+6 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 22 - "gather_pool"
Cohesion: 0.20
Nodes (6): commons_search(), gather_pool(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits(), test_pool_roundtrip()

### Community 23 - "ffmpeg"
Cohesion: 0.17
Nodes (8): shot_span(), local_voice(), sentence_groups(), split_takes(), spoken_count(), duration(), ffmpeg(), test_a_take_is_cut_between_the_scenes_words()

### Community 24 - "render_remotion"
Cohesion: 0.15
Nodes (10): render_remotion(), remotion(), render(), run_remotion_with_fallback(), invent_styles(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback() (+2 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.05
Nodes (44): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+36 more)

### Community 26 - "story_sound"
Cohesion: 0.40
Nodes (4): story_sound(), test_story_sound_library(), fetch(), _tone_wav()

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (14): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+6 more)

### Community 29 - "plan_rules.py"
Cohesion: 0.16
Nodes (13): clean_full(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number(), test_clean_full_board() (+5 more)

### Community 30 - "render"
Cohesion: 0.12
Nodes (10): gemini_images(), short_credit(), graphics_count(), to_vertical(), drawn_choices(), load_state(), render(), save_state() (+2 more)

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (23): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+15 more)

### Community 32 - "cut"
Cohesion: 0.11
Nodes (11): bm_area(), cut(), handle_end_local(), place_tool(), show_face(), to_bm(), to_object(), tool_axes() (+3 more)

### Community 33 - "words_of"
Cohesion: 0.13
Nodes (11): archive_films(), graphic_low(), archive_images(), on_topic(), word(), fill_money_graphics(), is_person_portrait(), words_of() (+3 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "invent_component"
Cohesion: 0.12
Nodes (16): clean_style_code(), invent_component(), attempt(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others() (+8 more)

### Community 36 - "test_story.py"
Cohesion: 0.09
Nodes (21): check_twists(), edit_scripts(), narration_lines(), story_problems(), build(), add(), main(), test_solo_edit_scripts_uses_same_ai() (+13 more)

### Community 37 - "test_first_second.py"
Cohesion: 0.05
Nodes (30): use_picture_from(), film_piece(), film_ffmpeg(), apply_review_fixes(), paint_new(), pool_pictures(), swap_pictures(), real() (+22 more)

### Community 38 - "build_scene.py"
Cohesion: 0.12
Nodes (5): keyvis(), collection(), ink_lines(), linear(), setup()

### Community 39 - "h3_run.py"
Cohesion: 0.20
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 40 - "captions"
Cohesion: 0.12
Nodes (9): ass_time(), caption_lines(), captions(), styled(), music_gain(), speak(), tts(), ass_colour() (+1 more)

### Community 41 - "main"
Cohesion: 0.17
Nodes (4): main(), Failure, key(), focus_object()

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "gpu.py"
Cohesion: 0.09
Nodes (11): studio_speak(), fills_frame(), comfy_call(), local_job(), moss_graph(), moss_images(), voicestudio_unload(), voicestudio_up() (+3 more)

### Community 44 - "test_opener_scene.py"
Cohesion: 0.07
Nodes (41): clean_opener(), _expect(), fix_plan(), _num(), plan_openers(), ask(), _size(), _stroke() (+33 more)

### Community 45 - "Vector"
Cohesion: 0.13
Nodes (13): box_of(), centre(), clusters(), half(), islands(), join(), merge_slivers(), pick_island() (+5 more)

### Community 46 - "test_style.py"
Cohesion: 0.12
Nodes (11): wants_remotion(), plan_with(), ask(), test_clean_question_and_kinetic(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics(), test_limit_style_caps() (+3 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "image_sources.py"
Cohesion: 0.09
Nodes (16): commons_films(), film_frames(), nasa_films(), article_images(), get_image(), nasa_images(), nasa_search(), openverse_images() (+8 more)

### Community 49 - "pool_of"
Cohesion: 0.13
Nodes (18): catalog_text(), clean_pics(), is_usable(), pictures_of(), usable(), entry(), film(), pic_short() (+10 more)

### Community 50 - "style_library"
Cohesion: 0.12
Nodes (10): cut_text(), edit_plan(), look_text(), picture_line(), style_library(), style_rules(), write_style_index(), test_edit_plan_picture_line() (+2 more)

### Community 51 - "channel_profiles.py"
Cohesion: 0.07
Nodes (24): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+16 more)

### Community 52 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 53 - "re"
Cohesion: 0.15
Nodes (6): logbook_results(), is_loop_short(), mark_details(), parse_scene_money(), first_second_check(), test_logbook_marks_tiny_samples()

### Community 54 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 55 - "scene_kit.py"
Cohesion: 0.09
Nodes (19): build_set(), feather(), add_body(), ensure_world(), facing_vec(), fcurves(), fit(), interpolation() (+11 more)

### Community 56 - "test_full_scenes.py"
Cohesion: 0.08
Nodes (18): sfx_events(), short_skin(), full_props(), full_summary(), _board(), _jpg(), test_board_pictures_attached(), test_clean_full_custom_and_skin() (+10 more)

### Community 57 - "choose_images"
Cohesion: 0.27
Nodes (11): choose_images(), picking, planned_short(), scene(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends(), test_choose_old_path_unchanged() (+3 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.11
Nodes (26): render_opener(), review(), review_frames(), scale_beats(), use_opener(), Env, short(), test_beats_scaled_into_scene() (+18 more)

### Community 59 - "test_edit_project.py"
Cohesion: 0.27
Nodes (5): remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers(), videos()

### Community 60 - "moves.py"
Cohesion: 0.23
Nodes (16): apply(), fall(), fly_off(), gait(), hop_off(), push(), release(), roll() (+8 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.13
Nodes (17): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+9 more)

### Community 62 - "test_blender_link.py"
Cohesion: 0.08
Nodes (25): allowed_licence(), attribution(), call(), credit(), fetch_model(), in_library(), LinkError, ping() (+17 more)

### Community 63 - "opener_scene.py"
Cohesion: 0.11
Nodes (17): edge_point_local(), State, burst(), camera(), feather_colours(), first_hit(), hold_offscreen(), main() (+9 more)

### Community 65 - "full_cues"
Cohesion: 0.20
Nodes (6): full_cues(), spoken_at(), spoken_span(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish()

### Community 66 - "shutil"
Cohesion: 0.12
Nodes (9): align(), main(), prune_cache(), approve_candidate(), library_menu(), reject_candidate(), save_candidate(), main() (+1 more)

### Community 67 - "write_scripts"
Cohesion: 0.18
Nodes (7): clean_sound(), limit_sounds(), limit_full(), limit_style(), write_scripts(), test_clean_sound(), test_limit_full()

### Community 68 - "test_blender_scene.py"
Cohesion: 0.08
Nodes (29): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+21 more)

### Community 69 - "owner"
Cohesion: 0.22
Nodes (3): owner(), planning_ai(), reply()

### Community 70 - "candidate_in"
Cohesion: 0.25
Nodes (8): candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_candidate_names_unique_across_kinds(), test_reject_deletes()

### Community 71 - "visual_review"
Cohesion: 0.12
Nodes (10): log_short(), clock(), overlay_notes(), quality_check(), review_fixes(), visual_review(), length_plan(), test_review_is_told_the_drawings_are_deliberate() (+2 more)

### Community 72 - "rescue_graphics"
Cohesion: 0.29
Nodes (4): rescue_graphics(), max_full(), max_full_planned(), test_rescue_respects_caps()

### Community 74 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

## Knowledge Gaps
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `ask_ai`, `pathlib`, `local_clips`, `make`, `ffmpeg`, `render_remotion`, `test_blender_plan.py`, `story_sound`, `frame_maker`, `words_of`, `test_first_second.py`, `captions`, `gpu.py`, `test_style.py`, `style_library`, `channel_profiles.py`, `re`, `make_paper`, `test_full_scenes.py`, `choose_images`, `test_opener_render.py`, `test_edit_project.py`, `random`, `shutil`, `visual_review`, `rescue_graphics`, `srt`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `build_scene.py`, `json`, `Shots`, `parts.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Should `motion.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14855072463768115 - nodes in this community are weakly interconnected._
- **Why does `render_opener()` connect `test_opener_render.py` to `shutil`, `local_clips`, `json`, `test_opener_scene.py`, `ffmpeg`, `test_blender_plan.py`, `test_blender_link.py`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.09462365591397849 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._