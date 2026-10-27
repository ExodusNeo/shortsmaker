# Graph Report - ShortsMaker  (2026-10-27)

## Corpus Check
- 118 files · ~133,575 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 1870 nodes · 5005 edges · 78 communities (68 shown, 10 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 122 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `52dd58ba`
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
- qwen_voice.py
- Paper
- tree
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
- gather_pool
- local_voice
- render_remotion
- test_blender_scene.py
- story_sound
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
- owner
- captions
- main
- Short.tsx
- subprocess
- test_opener_scene.py
- moves.py
- test_style.py
- Halftone.tsx
- json
- pool_of
- edit_plan
- channel_profiles.py
- build_scene.py
- look.py
- make_paper
- build_set
- test_full_scenes.py
- test_pictures_first.py
- test_opener_render.py
- sfx_events
- scene_kit.py
- opener_checks.py
- blender_link.py
- opener_scene.py
- make_sfx
- BlenderFailed
- shutil
- limit_style
- test_opener_checks.py
- fake_ai
- gemini_images
- visual_review
- call
- trim_borders
- to_vertical
- Fake
- apply_look_scenes

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
- `test_pixabay_keeps_only_on_topic_videos()` --calls--> `pixabay_films()`  [EXTRACTED]
  tests/test_pictures_first.py → shortsmaker/footage.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`

## Communities (78 total, 10 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "re"
Cohesion: 0.08
Nodes (19): log_short(), logbook_results(), vault_page(), vault_refresh(), clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx() (+11 more)

### Community 3 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 4 - "ask_ai"
Cohesion: 0.08
Nodes (21): scene_cues(), person_card(), ask_ai(), gemini_model(), quota_exhausted(), run_agy(), mark_details(), test_counter_finishes_before_it_leaves() (+13 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "pathlib"
Cohesion: 0.11
Nodes (3): hex_rgb(), luminance(), clean_photo()

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.06
Nodes (38): call(), fit_start(), frames(), graph(), main(), saved_file(), h3_problems(), h3_prompt() (+30 more)

### Community 8 - "qwen_voice.py"
Cohesion: 0.13
Nodes (13): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+5 more)

### Community 9 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 10 - "tree"
Cohesion: 0.20
Nodes (5): clear_distance(), stand_on(), surface_z(), tree(), world_verts()

### Community 11 - "local_clips"
Cohesion: 0.12
Nodes (11): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), motion_prompt(), start_picture_problems(), veo_handoff() (+3 more)

### Community 12 - "test_blender_link.py"
Cohesion: 0.31
Nodes (10): _fetch_replies(), execute(), ok(), test_download_error_cleans_up(), test_fetch_saves_pair(), test_in_library(), test_ping_on_off(), test_search_filters_licences() (+2 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 14 - "test_edit_project.py"
Cohesion: 0.13
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (37): load_rules(), min_real_pictures(), parse_rules(), test_channels_have_opener_rules(), capture_prompts(), ask(), draft_reply(), make() (+29 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 18 - "prepare_topic"
Cohesion: 0.14
Nodes (10): catalog_text(), contact_sheets(), is_usable(), load_pool(), pool_folder(), prepare_topic(), usable(), test_empty_pool_drops_topic_without_ai() (+2 more)

### Community 19 - "write_scripts"
Cohesion: 0.14
Nodes (16): pictures_of(), limit_full(), direct_scripts(), write_scripts(), test_limit_full(), passing(), prepare(), planning (+8 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.12
Nodes (14): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), write_style_index(), build(), add() (+6 more)

### Community 22 - "gather_pool"
Cohesion: 0.13
Nodes (8): article_images(), commons_search(), thumb_url(), wm_files(), gather_pool(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 23 - "local_voice"
Cohesion: 0.15
Nodes (7): local_voice(), sentence_groups(), split_takes(), spoken_count(), voicestudio_unload(), voicestudio_up(), is_loop_short()

### Community 24 - "render_remotion"
Cohesion: 0.12
Nodes (12): short_skin(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), invent_styles(), style_props(), swap_inventions() (+4 more)

### Community 25 - "test_blender_scene.py"
Cohesion: 0.07
Nodes (42): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+34 more)

### Community 26 - "story_sound"
Cohesion: 0.40
Nodes (4): story_sound(), test_story_sound_library(), fetch(), _tone_wav()

### Community 27 - "frame_maker"
Cohesion: 0.06
Nodes (16): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+8 more)

### Community 29 - "words_of"
Cohesion: 0.09
Nodes (23): clean_sound(), limit_sounds(), clean_full(), word(), clean_graphic(), contains(), coords(), fill_money_graphics() (+15 more)

### Community 30 - "render"
Cohesion: 0.11
Nodes (13): short_credit(), ffmpeg(), graphics_count(), first_second_check(), srt(), drawn_choices(), load_state(), render() (+5 more)

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (23): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+15 more)

### Community 32 - "drawn_thumbnail"
Cohesion: 0.23
Nodes (9): scene_frames(), drawn_thumbnail(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 33 - "test_blender_render.py"
Cohesion: 0.22
Nodes (12): peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises(), test_frames_are_trimmed_after_the_clips_are_cut() (+4 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "invent_component"
Cohesion: 0.11
Nodes (17): invent_component(), attempt(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), style_rules(), test_candidate_names_unique_across_kinds() (+9 more)

### Community 36 - "test_story.py"
Cohesion: 0.11
Nodes (19): check_twists(), edit_scripts(), narration_lines(), story_problems(), test_solo_edit_scripts_uses_same_ai(), scenes(), test_a_take_is_cut_between_the_scenes_words(), test_editor_gets_one_second_pass_for_broken_rules() (+11 more)

### Community 37 - "test_first_second.py"
Cohesion: 0.06
Nodes (27): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), rewrite_paint_prompts(), swap_pictures(), real(), run_check() (+19 more)

### Community 39 - "owner"
Cohesion: 0.15
Nodes (4): owner(), _fake_planning(), test_director_prompt_mentions_full(), film()

### Community 40 - "captions"
Cohesion: 0.16
Nodes (7): ass_time(), caption_lines(), captions(), styled(), speak(), tts(), ass_colour()

### Community 41 - "main"
Cohesion: 0.17
Nodes (4): main(), Failure, key(), focus_object()

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "subprocess"
Cohesion: 0.13
Nodes (8): music_gain(), film_piece(), shot_span(), duration(), storyboard(), main(), props_for(), test_music_gain_evens_out_tracks()

### Community 44 - "test_opener_scene.py"
Cohesion: 0.07
Nodes (40): clean_opener(), _expect(), fix_plan(), _num(), plan_openers(), ask(), _size(), _stroke() (+32 more)

### Community 45 - "moves.py"
Cohesion: 0.09
Nodes (23): bm_area(), box_of(), centre(), clusters(), cut(), edge_point_local(), half(), handle_end_local() (+15 more)

### Community 46 - "test_style.py"
Cohesion: 0.13
Nodes (15): wants_remotion(), candidate_in(), library_snapshot(), plan_with(), ask(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure() (+7 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "json"
Cohesion: 0.05
Nodes (30): freesound_fetch(), code_version(), archive_films(), commons_films(), crop_film_bytes(), film_frames(), nasa_films(), pixabay_films() (+22 more)

### Community 49 - "pool_of"
Cohesion: 0.11
Nodes (23): write_json(), catalog_entries(), catalog_pool(), clean_pics(), save_pool(), entry(), pic_short(), pool_of() (+15 more)

### Community 50 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 51 - "channel_profiles.py"
Cohesion: 0.07
Nodes (24): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+16 more)

### Community 52 - "build_scene.py"
Cohesion: 0.20
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 53 - "look.py"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 54 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 55 - "build_set"
Cohesion: 0.22
Nodes (6): build_set(), layers(), load_model(), make_static(), material(), merge()

### Community 56 - "test_full_scenes.py"
Cohesion: 0.07
Nodes (22): full_props(), full_summary(), full_pictures(), full_cues(), spoken_at(), spoken_span(), _board(), _jpg() (+14 more)

### Community 57 - "test_pictures_first.py"
Cohesion: 0.20
Nodes (15): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+7 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.11
Nodes (24): render_opener(), review(), review_frames(), scale_beats(), Env, short(), test_beats_scaled_into_scene(), test_cc_by_credit() (+16 more)

### Community 59 - "sfx_events"
Cohesion: 0.33
Nodes (3): sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 60 - "scene_kit.py"
Cohesion: 0.12
Nodes (26): apply(), fall(), fly_off(), hop_off(), push(), release(), roll(), scatter() (+18 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.12
Nodes (15): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+7 more)

### Community 62 - "blender_link.py"
Cohesion: 0.16
Nodes (8): allowed_licence(), attribution(), credit(), fetch_model(), in_library(), search(), words(), resolve_models()

### Community 63 - "opener_scene.py"
Cohesion: 0.10
Nodes (17): gait(), State, in_frame(), burst(), camera(), checks(), first_hit(), hold_offscreen() (+9 more)

### Community 66 - "shutil"
Cohesion: 0.15
Nodes (8): prune_cache(), paint_instead(), prune_work(), approve_candidate(), clean_style_code(), library_menu(), reject_candidate(), save_candidate()

### Community 68 - "test_opener_checks.py"
Cohesion: 0.33
Nodes (9): results(), test_blade_face(), test_cut_result(), test_edge_leads(), test_first_frame(), test_hidden(), test_in_frame(), test_overlap() (+1 more)

### Community 69 - "fake_ai"
Cohesion: 0.20
Nodes (5): fake_ai, planning_ai(), reply(), test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list()

### Community 71 - "visual_review"
Cohesion: 0.15
Nodes (9): clock(), overlay_notes(), quality_check(), review_fixes(), visual_review(), length_plan(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose() (+1 more)

### Community 72 - "call"
Cohesion: 0.20
Nodes (5): call(), LinkError, ping(), blender_note(), test_blender_note()

### Community 74 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

## Knowledge Gaps
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `re`, `ask_ai`, `pathlib`, `local_clips`, `test_edit_project.py`, `local_voice`, `render_remotion`, `story_sound`, `frame_maker`, `drawn_thumbnail`, `test_blender_render.py`, `test_first_second.py`, `captions`, `subprocess`, `test_style.py`, `json`, `edit_plan`, `channel_profiles.py`, `make_paper`, `test_full_scenes.py`, `test_pictures_first.py`, `sfx_events`, `opener_scene.py`, `make_sfx`, `shutil`, `gemini_images`, `visual_review`, `to_vertical`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `project_xml()` connect `test_edit_project.py` to `re`, `pathlib`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `re` be split into smaller, more focused modules?**
  _Cohesion score 0.07804878048780488 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `json`, `build_scene.py`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.07777777777777778 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._