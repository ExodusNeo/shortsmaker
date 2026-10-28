# Graph Report - ShortsMaker  (2026-10-28)

## Corpus Check
- 124 files · ~149,422 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 2082 nodes · 5477 edges · 77 communities (72 shown, 5 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 126 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0c03249e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- re
- toolkit.tsx
- ask_ai
- split_make_shorts.py
- pathlib
- test_h3_handoff.py
- test_opener_scene.py
- Paper
- local_voice
- local_clips
- tree
- guarded.tsx
- ffmpeg
- test_rules.py
- Journey.tsx
- full/types.ts
- test_pictures_first.py
- write_scripts
- Local GPU Worker
- style_library
- test_style.py
- apply_review_fixes
- render_remotion
- test_blender_render.py
- planning_ai
- frame_maker
- film_piece
- clean_full
- visual_review
- parts.py
- math
- prepare_topic
- templates.py
- _fake_planning
- test_story.py
- test_full_scenes.py
- build_scene.py
- h3_run.py
- captions
- main
- Short.tsx
- json
- test_opener_plan.py
- moves.py
- use_picture_from
- Halftone.tsx
- fetch
- test_blender_link.py
- gather_pool
- channel_profiles.py
- Shots
- test_first_second.py
- people_standin.py
- scene_kit.py
- unpack_clips
- choose_images
- test_opener_render.py
- pack_people.py
- test_opener_checks.py
- opener_checks.py
- ref_remotion
- opener_scene.py
- look_toon.py
- edit_plan
- sfx_events
- pictures_of
- test_blender_scene.py
- owner
- invent_component
- load_state
- make_sfx
- h3_problems
- trim_borders
- limit_style
- render

## God Nodes (most connected - your core abstractions)
1. `render()` - 63 edges
2. `write_scripts()` - 45 edges
3. `ask_ai()` - 40 edges
4. `render_opener()` - 36 edges
5. `run()` - 32 edges
6. `cut()` - 30 edges
7. `fixture()` - 30 edges
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

## Communities (77 total, 5 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "re"
Cohesion: 0.07
Nodes (20): log_short(), vault_page(), vault_refresh(), clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), full_props() (+12 more)

### Community 3 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 4 - "ask_ai"
Cohesion: 0.08
Nodes (21): scene_cues(), ask_ai(), gemini_model(), quota_exhausted(), run_agy(), mark_details(), test_counter_finishes_before_it_leaves(), test_quota_fallback_both_ways() (+13 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "pathlib"
Cohesion: 0.10
Nodes (11): code_version(), hex_rgb(), luminance(), person_card(), drawn_thumbnail(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back() (+3 more)

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.14
Nodes (22): fake_ai(), handoff(), short_with(), test_all_closeup_marked_scenes_skip_pause(), test_all_start_pictures_flagged_skips_pause(), test_flagged_start_picture_is_not_sent(), test_handoff_picks_up_clips_zip(), test_handoff_records_which_file_made_the_clip() (+14 more)

### Community 8 - "test_opener_scene.py"
Cohesion: 0.06
Nodes (36): builds(), fixture(), people_lib(), run(), test_bad_plans_fail(), test_box_fall_rests_and_renders(), test_camera_follows_unasked(), test_chicken_chop_reference() (+28 more)

### Community 9 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 10 - "local_voice"
Cohesion: 0.14
Nodes (12): local_voice(), sentence_groups(), split_takes(), spoken_count(), is_loop_short(), build(), add(), main() (+4 more)

### Community 11 - "local_clips"
Cohesion: 0.10
Nodes (13): cover_crop(), cut_owner_clip(), h3_prompt(), h3_prompts(), local_clips(), local_job(), motion_prompt(), start_picture_problems() (+5 more)

### Community 12 - "tree"
Cohesion: 0.25
Nodes (4): clear_distance(), clear_distance_at_end(), surface_z(), tree()

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 14 - "ffmpeg"
Cohesion: 0.13
Nodes (10): caption_layer(), make(), project_xml(), remove(), duration(), ffmpeg(), short_folder(), test_melt_plays_it_with_the_captions_on_top() (+2 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (40): load_rules(), min_real_pictures(), parse_rules(), test_channels_have_opener_rules(), capture_prompts(), ask(), draft_reply(), make() (+32 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 18 - "test_pictures_first.py"
Cohesion: 0.11
Nodes (28): catalog_entries(), catalog_pool(), clean_pics(), entry(), fake_ai, film(), pic_short(), pool_of() (+20 more)

### Community 19 - "write_scripts"
Cohesion: 0.12
Nodes (19): limit_full(), edit_scripts(), length_plan(), narration_lines(), write_scripts(), test_limit_full(), test_solo_edit_scripts_uses_same_ai(), passing() (+11 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.12
Nodes (13): clean_invention(), clean_look(), clean_transition(), settle_style(), approve_candidate(), style_library(), style_rules(), write_style_index() (+5 more)

### Community 22 - "test_style.py"
Cohesion: 0.18
Nodes (11): apply_look_scenes(), candidate_in(), library_snapshot(), restore_library(), test_apply_look_scenes(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes() (+3 more)

### Community 23 - "apply_review_fixes"
Cohesion: 0.18
Nodes (7): apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_redraw_failure_paints(), test_review_redraws_custom()

### Community 24 - "render_remotion"
Cohesion: 0.16
Nodes (9): render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain() (+1 more)

### Community 25 - "test_blender_render.py"
Cohesion: 0.15
Nodes (15): BlenderFailed, peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws() (+7 more)

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (14): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+6 more)

### Community 28 - "film_piece"
Cohesion: 0.17
Nodes (5): crop_film_bytes(), film_frames(), film_piece(), shot_span(), film_ffmpeg()

### Community 29 - "clean_full"
Cohesion: 0.08
Nodes (24): clean_sound(), limit_sounds(), graphic_low(), clean_full(), word(), clean_graphic(), contains(), coords() (+16 more)

### Community 30 - "visual_review"
Cohesion: 0.18
Nodes (8): clock(), overlay_notes(), quality_check(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (23): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+15 more)

### Community 32 - "math"
Cohesion: 0.06
Nodes (26): _append(), _attach(), _bake_free(), base_name(), _body_tree(), _clearance(), _clip(), _colour() (+18 more)

### Community 33 - "prepare_topic"
Cohesion: 0.19
Nodes (8): write_json(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip()

### Community 34 - "templates.py"
Cohesion: 0.17
Nodes (15): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge() (+7 more)

### Community 35 - "_fake_planning"
Cohesion: 0.17
Nodes (6): _fake_planning(), ask(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 36 - "test_story.py"
Cohesion: 0.07
Nodes (25): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+17 more)

### Community 37 - "test_full_scenes.py"
Cohesion: 0.05
Nodes (34): music_gain(), short_skin(), full_summary(), full_formats(), opener_graphic(), rescue_graphics(), full_cues(), spoken_at() (+26 more)

### Community 38 - "build_scene.py"
Cohesion: 0.12
Nodes (5): keyvis(), collection(), ink_lines(), linear(), setup()

### Community 39 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 40 - "captions"
Cohesion: 0.12
Nodes (11): ass_time(), caption_lines(), captions(), styled(), speak(), story_sound(), tts(), ass_colour() (+3 more)

### Community 41 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "json"
Cohesion: 0.07
Nodes (12): freesound_fetch(), master_gain(), fills_frame(), comfy_call(), moss_graph(), moss_images(), voicestudio_unload(), fingerprint() (+4 more)

### Community 44 - "test_opener_plan.py"
Cohesion: 0.08
Nodes (36): clean_opener(), _expect(), fix_plan(), _num(), plan_openers(), ask(), _size(), _stroke() (+28 more)

### Community 45 - "moves.py"
Cohesion: 0.06
Nodes (33): apply(), bm_area(), box_of(), centre(), clusters(), edge_point_local(), fall(), fly_off() (+25 more)

### Community 46 - "use_picture_from"
Cohesion: 0.33
Nodes (3): use_picture_from(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "fetch"
Cohesion: 0.09
Nodes (16): archive_films(), commons_films(), nasa_films(), pixabay_films(), archive_images(), get_image(), nasa_images(), nasa_search() (+8 more)

### Community 49 - "test_blender_link.py"
Cohesion: 0.07
Nodes (26): allowed_licence(), attribution(), call(), credit(), fetch_model(), in_library(), LinkError, ping() (+18 more)

### Community 50 - "gather_pool"
Cohesion: 0.12
Nodes (8): article_images(), commons_search(), thumb_url(), wm_files(), gather_pool(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 51 - "channel_profiles.py"
Cohesion: 0.06
Nodes (27): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+19 more)

### Community 52 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 53 - "test_first_second.py"
Cohesion: 0.19
Nodes (13): first_second_check(), swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once() (+5 more)

### Community 54 - "people_standin.py"
Cohesion: 0.29
Nodes (5): body(), clip(), key(), main(), part()

### Community 55 - "scene_kit.py"
Cohesion: 0.10
Nodes (28): cut(), gait(), hop_off(), legs(), sink(), walk(), _ground(), add_body() (+20 more)

### Community 56 - "unpack_clips"
Cohesion: 0.36
Nodes (6): unpack_clips(), test_duplicate_clip_names_deduplicated(), test_old_zip_does_not_overwrite_newer_clip(), test_renamed_zip_is_picked_up(), test_unpack_clips(), zip_of()

### Community 57 - "choose_images"
Cohesion: 0.25
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.07
Nodes (39): _cast_note(), render_opener(), review(), review_frames(), save_try(), scale_beats(), use_opener(), Env (+31 more)

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
Cohesion: 0.07
Nodes (24): State, in_frame(), build_set(), camera(), checks(), dress_set(), first_hit(), ground_material() (+16 more)

### Community 64 - "look_toon.py"
Cohesion: 0.27
Nodes (4): apply(), ink(), outline(), toon()

### Community 65 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 66 - "sfx_events"
Cohesion: 0.33
Nodes (3): sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 67 - "pictures_of"
Cohesion: 0.22
Nodes (5): catalog_text(), is_usable(), pictures_of(), usable(), direct_scripts()

### Community 68 - "test_blender_scene.py"
Cohesion: 0.07
Nodes (42): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+34 more)

### Community 69 - "owner"
Cohesion: 0.14
Nodes (6): owner(), plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 70 - "invent_component"
Cohesion: 0.12
Nodes (16): invent_component(), attempt(), invent_styles(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others() (+8 more)

### Community 71 - "load_state"
Cohesion: 0.50
Nodes (3): load_state(), save_state(), test_state_roundtrip_full_pics()

### Community 74 - "trim_borders"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 85 - "render"
Cohesion: 0.07
Nodes (14): gemini_images(), short_credit(), graphics_count(), to_vertical(), ink_silhouette(), paint_instead(), wants_remotion(), srt() (+6 more)

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `templates.py`, `build_scene.py`, `json`, `Shots`, `parts.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `re`, `ask_ai`, `pathlib`, `local_voice`, `local_clips`, `ffmpeg`, `apply_review_fixes`, `render_remotion`, `test_blender_render.py`, `frame_maker`, `clean_full`, `visual_review`, `test_full_scenes.py`, `captions`, `json`, `channel_profiles.py`, `test_first_second.py`, `choose_images`, `test_opener_render.py`, `opener_scene.py`, `edit_plan`, `sfx_events`, `load_state`, `make_sfx`, `trim_borders`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `re` be split into smaller, more focused modules?**
  _Cohesion score 0.07446808510638298 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `prepare_topic`, `re`, `pictures_of`, `test_blender_scene.py`, `ask_ai`, `pathlib`, `test_full_scenes.py`, `test_story.py`, `_fake_planning`, `owner`, `json`, `test_opener_plan.py`, `limit_style`, `test_rules.py`, `test_pictures_first.py`, `channel_profiles.py`, `style_library`, `clean_full`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.07777777777777778 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._