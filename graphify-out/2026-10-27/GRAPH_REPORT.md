# Graph Report - ShortsMaker  (2026-10-27)

## Corpus Check
- 118 files · ~130,759 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: .blend 7, (none) 3, .canvas 1)

## Summary
- 1835 nodes · 4916 edges · 77 communities (74 shown, 3 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 122 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b2fa5ca6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Short.tsx
- code_custom_scenes
- skinOf
- ask_ai
- split_make_shorts.py
- pathlib
- test_h3_handoff.py
- scene_cues
- toolkit.tsx
- gpu.py
- local_clips
- test_blender_link.py
- guarded.tsx
- make
- test_rules.py
- Journey.tsx
- full/types.ts
- catalog_pool
- planning
- Local GPU Worker
- clean_look
- moves.py
- test_blender_scene.py
- render_remotion
- test_blender_plan.py
- audio_mix.py
- frame_maker
- Root.tsx
- plan_rules.py
- render
- parts.py
- drawn_thumbnail
- test_blender_render.py
- templates.py
- style_placeholders
- test_story.py
- test_first_second.py
- build_scene.py
- invent_component
- trim_borders
- main
- style.test.ts
- re
- test_opener_plan.py
- cut
- test_style.py
- kit.ts
- image_sources.py
- test_pictures_first.py
- edit_plan
- main
- Shots
- write_scripts
- _fake_planning
- use_picture_from
- test_full_scenes.py
- choose_images
- test_opener_render.py
- test_review_redraws_custom
- scene_kit.py
- opener_checks.py
- gather_pool
- opener_scene.py
- make_paper
- is_usable
- shutil
- fake_ai
- time
- json
- ffmpeg
- visual_review
- apply_review_fixes
- trend_research
- film_piece
- story_sound
- paint_instead

## God Nodes (most connected - your core abstractions)
1. `render()` - 62 edges
2. `write_scripts()` - 45 edges
3. `ask_ai()` - 39 edges
4. `cut()` - 29 edges
5. `skinOf()` - 29 edges
6. `main()` - 27 edges
7. `render_opener()` - 26 edges
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
- `test_a_stopped_run_keeps_the_default_channel()` --calls--> `main()`  [EXTRACTED]
  tests/test_rules.py → shortsmaker/cli.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`

## Communities (77 total, 3 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.11
Nodes (22): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CLAMP, clamp01(), H (+14 more)

### Community 1 - "Short.tsx"
Cohesion: 0.12
Nodes (37): Captions(), card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard() (+29 more)

### Community 2 - "code_custom_scenes"
Cohesion: 0.13
Nodes (12): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), redraw_custom() (+4 more)

### Community 3 - "skinOf"
Cohesion: 0.25
Nodes (20): CustomScene(), ExampleChain(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear() (+12 more)

### Community 4 - "ask_ai"
Cohesion: 0.11
Nodes (14): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high() (+6 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "pathlib"
Cohesion: 0.12
Nodes (4): ask_number(), hex_rgb(), luminance(), library_menu()

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (32): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_closeup_marked_scenes_skip_pause(), test_all_start_pictures_flagged_skips_pause() (+24 more)

### Community 8 - "scene_cues"
Cohesion: 0.13
Nodes (11): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish() (+3 more)

### Community 9 - "toolkit.tsx"
Cohesion: 0.13
Nodes (28): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+20 more)

### Community 10 - "gpu.py"
Cohesion: 0.11
Nodes (7): crop_film_bytes(), film_frames(), person_card(), local_job(), local_voice(), voicestudio_unload(), voicestudio_up()

### Community 11 - "local_clips"
Cohesion: 0.13
Nodes (10): cover_crop(), cut_owner_clip(), gemini_images(), h3_prompts(), local_clips(), motion_prompt(), start_picture_problems(), veo_handoff() (+2 more)

### Community 12 - "test_blender_link.py"
Cohesion: 0.08
Nodes (25): allowed_licence(), attribution(), call(), credit(), fetch_model(), in_library(), LinkError, ping() (+17 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (20): ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard(), hits() (+12 more)

### Community 14 - "make"
Cohesion: 0.17
Nodes (6): caption_layer(), make(), master_gain(), project_xml(), remove(), test_timeline_has_scenes_captions_sound_and_markers()

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (39): draft_rules(), load_rules(), min_real_pictures(), parse_rules(), require_rules(), capture_prompts(), ask(), draft_reply() (+31 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.16
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "full/types.ts"
Cohesion: 0.18
Nodes (16): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+8 more)

### Community 18 - "catalog_pool"
Cohesion: 0.13
Nodes (14): write_json(), catalog_entries(), catalog_pool(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool() (+6 more)

### Community 19 - "planning"
Cohesion: 0.19
Nodes (13): passing(), prepare(), planning, test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), test_dropped_topic_pool_removed(), prepare() (+5 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 22 - "moves.py"
Cohesion: 0.17
Nodes (17): apply(), fall(), fly_off(), gait(), hop_off(), push(), release(), roll() (+9 more)

### Community 23 - "test_blender_scene.py"
Cohesion: 0.08
Nodes (28): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+20 more)

### Community 24 - "render_remotion"
Cohesion: 0.15
Nodes (10): render_remotion(), remotion(), render(), run_remotion_with_fallback(), invent_styles(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback() (+2 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.11
Nodes (22): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+14 more)

### Community 26 - "audio_mix.py"
Cohesion: 0.12
Nodes (10): ass_time(), caption_lines(), captions(), styled(), freesound_fetch(), music_gain(), speak(), tts() (+2 more)

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (15): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+7 more)

### Community 29 - "plan_rules.py"
Cohesion: 0.09
Nodes (24): graphic_low(), rescue_graphics(), clean_full(), word(), clean_graphic(), contains(), coords(), fill_money_graphics() (+16 more)

### Community 30 - "render"
Cohesion: 0.10
Nodes (12): short_credit(), graphics_count(), to_vertical(), wants_remotion(), srt(), drawn_choices(), load_state(), render() (+4 more)

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

### Community 35 - "style_placeholders"
Cohesion: 0.19
Nodes (10): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_placeholders_match_the_slots() (+2 more)

### Community 36 - "test_story.py"
Cohesion: 0.07
Nodes (28): align(), align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak(), sentence_groups() (+20 more)

### Community 37 - "test_first_second.py"
Cohesion: 0.20
Nodes (13): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once() (+5 more)

### Community 38 - "build_scene.py"
Cohesion: 0.12
Nodes (5): keyvis(), collection(), ink_lines(), linear(), setup()

### Community 39 - "invent_component"
Cohesion: 0.18
Nodes (7): clean_style_code(), invent_component(), attempt(), lint_style_code(), style_preview(), style_rules(), test_invention_lint_failure_uses_fallback()

### Community 40 - "trim_borders"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 41 - "main"
Cohesion: 0.17
Nodes (4): main(), Failure, key(), focus_object()

### Community 42 - "style.test.ts"
Cohesion: 0.18
Nodes (12): Background(), flashAlpha(), GraphicFor(), Short(), has(), lookFor(), overlayFor(), transitionFor() (+4 more)

### Community 43 - "re"
Cohesion: 0.09
Nodes (11): spoken_count(), log_short(), logbook_results(), vault_page(), vault_refresh(), mark_details(), parse_scene_money(), first_second_check() (+3 more)

### Community 44 - "test_opener_plan.py"
Cohesion: 0.09
Nodes (33): clean_opener(), _expect(), fix_plan(), _num(), plan_openers(), ask(), _size(), _stroke() (+25 more)

### Community 45 - "cut"
Cohesion: 0.08
Nodes (22): bm_area(), box_of(), centre(), clusters(), cut(), edge_point_local(), half(), handle_end_local() (+14 more)

### Community 46 - "test_style.py"
Cohesion: 0.11
Nodes (20): reject_candidate(), save_candidate(), style_library(), write_style_index(), candidate_in(), library_snapshot(), plan_with(), ask() (+12 more)

### Community 47 - "kit.ts"
Cohesion: 0.19
Nodes (23): CAPTION_TOP, drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "image_sources.py"
Cohesion: 0.09
Nodes (19): archive_films(), commons_films(), nasa_films(), pixabay_films(), archive_images(), article_images(), commons_search(), get_image() (+11 more)

### Community 49 - "test_pictures_first.py"
Cohesion: 0.18
Nodes (18): clean_pics(), entry(), film(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film(), test_both_mode_reuses_pools() (+10 more)

### Community 50 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 51 - "main"
Cohesion: 0.10
Nodes (16): ask_brain(), ask_count(), ask_yes(), load_channel(), new_channel(), pick_channel(), save_channel(), use_channel() (+8 more)

### Community 52 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 53 - "write_scripts"
Cohesion: 0.10
Nodes (14): clean_sound(), limit_sounds(), pictures_of(), limit_full(), limit_style(), direct_scripts(), edit_scripts(), length_plan() (+6 more)

### Community 54 - "_fake_planning"
Cohesion: 0.17
Nodes (6): _fake_planning(), ask(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 55 - "use_picture_from"
Cohesion: 0.33
Nodes (3): use_picture_from(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 56 - "test_full_scenes.py"
Cohesion: 0.07
Nodes (18): sfx_events(), short_skin(), full_props(), full_summary(), full_pictures(), _board(), _jpg(), test_board_pictures_attached() (+10 more)

### Community 57 - "choose_images"
Cohesion: 0.19
Nodes (14): choose_images(), apply_look_scenes(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+6 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.12
Nodes (23): render_opener(), review(), scale_beats(), use_opener(), Env, short(), test_beats_scaled_into_scene(), test_cc_by_credit() (+15 more)

### Community 59 - "test_review_redraws_custom"
Cohesion: 0.40
Nodes (3): _review_state(), test_redraw_failure_paints(), test_review_redraws_custom()

### Community 60 - "scene_kit.py"
Cohesion: 0.08
Nodes (18): to_bm(), add_body(), ensure_world(), facing_vec(), fcurves(), interpolation(), key_vis(), layers() (+10 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.14
Nodes (16): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), in_frame() (+8 more)

### Community 62 - "gather_pool"
Cohesion: 0.15
Nodes (5): gather_pool(), owner(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 63 - "opener_scene.py"
Cohesion: 0.13
Nodes (12): State, build_set(), camera(), main(), place_actors(), setup(), stand_on(), subject_segments() (+4 more)

### Community 64 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 65 - "is_usable"
Cohesion: 0.40
Nodes (3): catalog_text(), is_usable(), usable()

### Community 66 - "shutil"
Cohesion: 0.14
Nodes (8): preview_sheet(), tsc_check(), storyboard(), approve_candidate(), main(), props_for(), build(), main()

### Community 67 - "fake_ai"
Cohesion: 0.20
Nodes (5): fake_ai, planning_ai(), reply(), test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list()

### Community 68 - "time"
Cohesion: 0.14
Nodes (9): call(), fit_start(), frames(), graph(), main(), saved_file(), main(), prune_cache() (+1 more)

### Community 69 - "json"
Cohesion: 0.12
Nodes (10): code_version(), comfy_call(), moss_graph(), moss_images(), fingerprint(), pick_model(), rewrite_paint_prompts(), article_text() (+2 more)

### Community 70 - "ffmpeg"
Cohesion: 0.22
Nodes (8): shot_span(), split_takes(), duration(), ffmpeg(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), videos(), test_a_take_is_cut_between_the_scenes_words()

### Community 71 - "visual_review"
Cohesion: 0.18
Nodes (8): clock(), overlay_notes(), quality_check(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 72 - "apply_review_fixes"
Cohesion: 0.28
Nodes (4): apply_review_fixes(), paint_new(), pool_pictures(), test_auto_fix_graphic()

### Community 73 - "trend_research"
Cohesion: 0.29
Nodes (4): channel_url(), seed_ideas(), trend_research(), yt_list()

### Community 75 - "story_sound"
Cohesion: 0.40
Nodes (4): story_sound(), test_story_sound_library(), fetch(), _tone_wav()

## Knowledge Gaps
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `pathlib`, `scene_cues`, `gpu.py`, `local_clips`, `make`, `moves.py`, `render_remotion`, `audio_mix.py`, `frame_maker`, `plan_rules.py`, `drawn_thumbnail`, `test_blender_render.py`, `trim_borders`, `re`, `test_style.py`, `edit_plan`, `main`, `test_full_scenes.py`, `choose_images`, `test_opener_render.py`, `make_paper`, `shutil`, `json`, `ffmpeg`, `visual_review`, `apply_review_fixes`, `story_sound`, `paint_instead`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.10960960960960961 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `json`, `build_scene.py`, `Shots`, `parts.py`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Should `Short.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `shutil`, `ask_ai`, `json`, `pathlib`, `test_story.py`, `trend_research`, `re`, `test_opener_plan.py`, `test_style.py`, `test_rules.py`, `test_pictures_first.py`, `catalog_pool`, `main`, `planning`, `clean_look`, `_fake_planning`, `test_blender_plan.py`, `plan_rules.py`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Should `code_custom_scenes` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.11384615384615385 - nodes in this community are weakly interconnected._