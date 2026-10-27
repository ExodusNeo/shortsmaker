# Graph Report - ShortsMaker  (2026-10-27)

## Corpus Check
- 124 files · ~144,302 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 2029 nodes · 5351 edges · 84 communities (73 shown, 11 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 125 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1c711fc9`
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
- test_opener_scene.py
- Paper
- json
- ffmpeg
- ask
- guarded.tsx
- make
- test_rules.py
- Journey.tsx
- BigNumber.tsx
- test_pictures_first.py
- write_scripts
- Local GPU Worker
- style_library
- qwen_voice.py
- paint_instead
- render_remotion
- test_blender_plan.py
- catalog_entries
- frame_maker
- look.py
- test_full_scenes.py
- render
- parts.py
- people.py
- prepare_topic
- templates.py
- invent_component
- test_story.py
- apply_review_fixes
- math
- h3_run.py
- captions
- main
- Short.tsx
- subprocess
- test_opener_plan.py
- moves.py
- plan_with
- Halftone.tsx
- image_sources.py
- fetch_model
- visual_review
- re
- Shots
- test_first_second.py
- audio_mix.py
- scene_kit.py
- sfx_events
- choose_images
- test_opener_render.py
- pack_people.py
- test_opener_checks.py
- opener_checks.py
- blender_link.py
- opener_scene.py
- look_toon.py
- edit_plan
- apply_look_scenes
- load_model
- test_blender_scene.py
- owner
- test_style.py
- use_opener
- clean_pics
- review
- photo_prep.py
- resolve_models
- Fake
- planning_ai
- limit_style
- copy
- h3_problems
- h3_prompt
- logbook_results
- test_on_topic_ignores_a_lone_shared_name

## God Nodes (most connected - your core abstractions)
1. `render()` - 62 edges
2. `write_scripts()` - 45 edges
3. `ask_ai()` - 39 edges
4. `render_opener()` - 32 edges
5. `cut()` - 30 edges
6. `run()` - 30 edges
7. `skinOf()` - 29 edges
8. `fixture()` - 28 edges
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

## Communities (84 total, 11 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "code_custom_scenes"
Cohesion: 0.12
Nodes (13): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+5 more)

### Community 3 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 4 - "ask_ai"
Cohesion: 0.10
Nodes (15): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), mark_details(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run() (+7 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "pathlib"
Cohesion: 0.12
Nodes (3): hex_rgb(), luminance(), short_skin()

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.11
Nodes (28): unpack_clips(), fake_ai(), handoff(), short_with(), test_all_closeup_marked_scenes_skip_pause(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated(), test_flagged_start_picture_is_not_sent() (+20 more)

### Community 8 - "test_opener_scene.py"
Cohesion: 0.06
Nodes (34): builds(), fixture(), people_lib(), run(), test_bad_plans_fail(), test_box_fall_rests_and_renders(), test_camera_follows_unasked(), test_chicken_chop_reference() (+26 more)

### Community 9 - "Paper"
Cohesion: 0.13
Nodes (28): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+20 more)

### Community 10 - "json"
Cohesion: 0.07
Nodes (17): code_version(), archive_films(), commons_films(), crop_film_bytes(), film_frames(), pixabay_films(), comfy_call(), moss_graph() (+9 more)

### Community 11 - "ffmpeg"
Cohesion: 0.09
Nodes (18): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt(), split_takes() (+10 more)

### Community 12 - "ask"
Cohesion: 0.22
Nodes (4): ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 14 - "make"
Cohesion: 0.15
Nodes (8): caption_layer(), make(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers(), videos()

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (40): load_rules(), min_real_pictures(), parse_rules(), test_channels_have_opener_rules(), capture_prompts(), ask(), draft_reply(), make() (+32 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "BigNumber.tsx"
Cohesion: 0.20
Nodes (14): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+6 more)

### Community 18 - "test_pictures_first.py"
Cohesion: 0.16
Nodes (23): catalog_pool(), entry(), fake_ai, film(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film() (+15 more)

### Community 19 - "write_scripts"
Cohesion: 0.10
Nodes (21): pictures_of(), limit_full(), direct_scripts(), edit_scripts(), length_plan(), narration_lines(), write_scripts(), test_limit_full() (+13 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.13
Nodes (12): clean_invention(), clean_look(), clean_transition(), settle_style(), approve_candidate(), style_library(), write_style_index(), test_invented_look_needs_fallback() (+4 more)

### Community 22 - "qwen_voice.py"
Cohesion: 0.14
Nodes (13): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+5 more)

### Community 24 - "render_remotion"
Cohesion: 0.10
Nodes (13): ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions() (+5 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.05
Nodes (44): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+36 more)

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (14): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+6 more)

### Community 28 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 29 - "test_full_scenes.py"
Cohesion: 0.05
Nodes (47): scene_cues(), graphic_low(), person_card(), full_props(), full_summary(), full_pictures(), rescue_graphics(), clean_full() (+39 more)

### Community 30 - "render"
Cohesion: 0.09
Nodes (13): gemini_images(), short_credit(), graphics_count(), to_vertical(), wants_remotion(), srt(), drawn_choices(), load_state() (+5 more)

### Community 31 - "parts.py"
Cohesion: 0.16
Nodes (20): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+12 more)

### Community 32 - "people.py"
Cohesion: 0.08
Nodes (16): _append(), _attach(), _bake_free(), base_name(), _colour(), dress(), held(), _hold() (+8 more)

### Community 33 - "prepare_topic"
Cohesion: 0.15
Nodes (10): write_json(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip() (+2 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "invent_component"
Cohesion: 0.10
Nodes (18): invent_component(), attempt(), invent_styles(), lint_style_code(), reject_candidate(), restore_style_slots(), style_placeholders(), style_preview() (+10 more)

### Community 36 - "test_story.py"
Cohesion: 0.11
Nodes (18): sentence_groups(), check_twists(), story_problems(), build(), add(), main(), scenes(), test_editor_gets_one_second_pass_for_broken_rules() (+10 more)

### Community 37 - "apply_review_fixes"
Cohesion: 0.12
Nodes (10): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full() (+2 more)

### Community 38 - "math"
Cohesion: 0.10
Nodes (6): make_sfx(), body(), clip(), key(), main(), part()

### Community 39 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 40 - "captions"
Cohesion: 0.12
Nodes (11): ass_time(), caption_lines(), captions(), styled(), speak(), story_sound(), tts(), ass_colour() (+3 more)

### Community 41 - "main"
Cohesion: 0.16
Nodes (5): keyvis(), main(), Failure, key(), focus_object()

### Community 42 - "Short.tsx"
Cohesion: 0.13
Nodes (19): Captions(), PersonCard(), Root(), Background(), flashAlpha(), GraphicFor(), Move, Scene (+11 more)

### Community 43 - "subprocess"
Cohesion: 0.06
Nodes (11): master_gain(), film_piece(), shot_span(), fills_frame(), film_ffmpeg(), duration(), tsc_check(), storyboard() (+3 more)

### Community 44 - "test_opener_plan.py"
Cohesion: 0.09
Nodes (33): clean_opener(), _expect(), fix_plan(), _num(), plan_openers(), ask(), _size(), _stroke() (+25 more)

### Community 45 - "moves.py"
Cohesion: 0.07
Nodes (25): bm_area(), box_of(), centre(), clear_distance(), clear_distance_at_end(), clusters(), edge_point_local(), half() (+17 more)

### Community 46 - "plan_with"
Cohesion: 0.29
Nodes (5): plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "image_sources.py"
Cohesion: 0.09
Nodes (17): nasa_films(), archive_images(), article_images(), commons_search(), get_image(), nasa_images(), nasa_search(), on_topic() (+9 more)

### Community 49 - "fetch_model"
Cohesion: 0.20
Nodes (12): credit(), fetch_model(), in_library(), words(), _fetch_replies(), execute(), ok(), test_download_error_cleans_up() (+4 more)

### Community 50 - "visual_review"
Cohesion: 0.18
Nodes (8): clock(), overlay_notes(), quality_check(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 51 - "re"
Cohesion: 0.06
Nodes (29): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+21 more)

### Community 52 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 53 - "test_first_second.py"
Cohesion: 0.19
Nodes (13): first_second_check(), swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once() (+5 more)

### Community 54 - "audio_mix.py"
Cohesion: 0.14
Nodes (6): clean_sound(), freesound_fetch(), limit_sounds(), music_gain(), test_clean_sound(), test_music_gain_evens_out_tracks()

### Community 55 - "scene_kit.py"
Cohesion: 0.08
Nodes (38): apply(), cut(), fall(), fly_off(), gait(), hop_off(), legs(), push() (+30 more)

### Community 56 - "sfx_events"
Cohesion: 0.33
Nodes (3): sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 57 - "choose_images"
Cohesion: 0.21
Nodes (13): choose_images(), is_person_portrait(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+5 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.19
Nodes (22): render_opener(), Env, _people_files(), short(), test_beats_scaled_into_scene(), test_cc_by_credit(), test_crash_retry_then_fallback(), test_failed_checks_fix_then_fallback() (+14 more)

### Community 59 - "pack_people.py"
Cohesion: 0.26
Nodes (6): base_name(), clip_name(), front(), height(), main(), stride()

### Community 60 - "test_opener_checks.py"
Cohesion: 0.33
Nodes (9): results(), test_blade_face(), test_cut_result(), test_edge_leads(), test_first_frame(), test_hidden(), test_in_frame(), test_overlap() (+1 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.11
Nodes (17): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+9 more)

### Community 62 - "blender_link.py"
Cohesion: 0.13
Nodes (10): allowed_licence(), attribution(), call(), LinkError, ping(), search(), blender_note(), test_ping_on_off() (+2 more)

### Community 63 - "opener_scene.py"
Cohesion: 0.09
Nodes (21): State, in_frame(), build_set(), camera(), checks(), dress_set(), first_hit(), hold_offscreen() (+13 more)

### Community 64 - "look_toon.py"
Cohesion: 0.27
Nodes (4): apply(), ink(), outline(), toon()

### Community 65 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 67 - "load_model"
Cohesion: 0.25
Nodes (4): ground_material(), load_model(), material(), merge()

### Community 68 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 69 - "owner"
Cohesion: 0.12
Nodes (6): owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 70 - "test_style.py"
Cohesion: 0.20
Nodes (11): save_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_candidate_names_unique_across_kinds() (+3 more)

### Community 71 - "use_opener"
Cohesion: 0.22
Nodes (6): use_opener(), test_use_opener_failure_keeps_scene(), test_use_opener_never_raises(), test_use_opener_on_success(), test_use_opener_planner_check(), _wiring()

### Community 72 - "clean_pics"
Cohesion: 0.25
Nodes (4): catalog_text(), clean_pics(), is_usable(), usable()

### Community 73 - "review"
Cohesion: 0.29
Nodes (3): review(), review_frames(), test_review_frames_include_key_moments()

### Community 74 - "photo_prep.py"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 75 - "resolve_models"
Cohesion: 0.33
Nodes (3): pick_model(), resolve_models(), test_every_unfound_model_named_at_once()

## Knowledge Gaps
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `ask_ai`, `pathlib`, `json`, `ffmpeg`, `make`, `paint_instead`, `render_remotion`, `test_blender_plan.py`, `frame_maker`, `test_full_scenes.py`, `apply_review_fixes`, `math`, `captions`, `subprocess`, `visual_review`, `re`, `test_first_second.py`, `audio_mix.py`, `sfx_events`, `choose_images`, `opener_scene.py`, `edit_plan`, `test_style.py`, `use_opener`, `photo_prep.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12802275960170698 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `math`, `json`, `Shots`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `ask_ai`, `pathlib`, `json`, `test_rules.py`, `test_pictures_first.py`, `style_library`, `test_blender_plan.py`, `test_full_scenes.py`, `prepare_topic`, `test_story.py`, `test_opener_plan.py`, `plan_with`, `re`, `audio_mix.py`, `choose_images`, `owner`, `clean_pics`, `limit_style`, `logbook_results`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `code_custom_scenes` be split into smaller, more focused modules?**
  _Cohesion score 0.1225296442687747 - nodes in this community are weakly interconnected._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.10144927536231885 - nodes in this community are weakly interconnected._