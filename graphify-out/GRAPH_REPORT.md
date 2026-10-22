# Graph Report - ShortsMaker  (2026-10-22)

## Corpus Check
- 102 files · ~100,986 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .canvas 1)

## Summary
- 1394 nodes · 3789 edges · 62 communities (56 shown, 6 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 87 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `36855729`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- clean_full
- skinOf
- main
- split_make_shorts.py
- test_full_scenes.py
- ask_ai
- full_cues
- toolkit.tsx
- audio_mix.py
- drawn_thumbnail
- code_custom_scenes
- guarded.tsx
- make
- test_rules.py
- Journey.tsx
- full/types.ts
- prepare_topic
- test_pictures_first.py
- gen.py
- test_style.py
- choose_images
- test_blender_scene.py
- image_sources.py
- write_scripts
- gather_pool
- frame_maker
- style_library
- sentence_groups
- render
- parts.py
- apply_review_fixes
- test_blender_render.py
- templates.py
- render_remotion
- re
- run_check
- build_scene.py
- local_clips
- clean_photo
- main
- Short.tsx
- first_second_check
- pool_pictures
- ffmpeg
- planning_ai
- Halftone.tsx
- json
- speak
- rewrite_paint_prompts
- plan_rules.py
- Shots
- limit_style
- trend_research
- capture_prompts
- run_draft
- use_picture_from
- draft_rules
- paint_instead
- make_sfx
- StopPicker

## God Nodes (most connected - your core abstractions)
1. `render()` - 60 edges
2. `write_scripts()` - 39 edges
3. `ask_ai()` - 30 edges
4. `skinOf()` - 29 edges
5. `main()` - 26 edges
6. `Paper()` - 25 edges
7. `choose_images()` - 23 edges
8. `clean_full()` - 21 edges
9. `style_library()` - 20 edges
10. `Bridge` - 19 edges

## Surprising Connections (you probably didn't know these)
- `test_numbers()` --calls--> `say_number()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_word_counts_match_the_scene_splitter()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_words_keep_what_is_written()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_every_aligned_word_is_in_the_aligner_alphabet()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_min_pictures_from_settings()` --calls--> `prepare_topic()`  [EXTRACTED]
  tests/test_rules.py → shortsmaker/picture_pool.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`

## Communities (62 total, 6 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.17
Nodes (29): card, clamp, DotGrid(), MarkCard(), Props, StatCard(), TimelineCard(), clamp (+21 more)

### Community 2 - "clean_full"
Cohesion: 0.09
Nodes (22): clean_sound(), limit_sounds(), rescue_graphics(), clean_full(), word(), clean_graphic(), contains(), coords() (+14 more)

### Community 3 - "skinOf"
Cohesion: 0.18
Nodes (23): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+15 more)

### Community 4 - "main"
Cohesion: 0.08
Nodes (18): ask_brain(), ask_count(), ask_number(), ask_yes(), load_channel(), pick_channel(), use_channel(), fix_short() (+10 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 7 - "ask_ai"
Cohesion: 0.12
Nodes (10): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), mark_details(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), test_claude_pinned_to_opus_high() (+2 more)

### Community 8 - "full_cues"
Cohesion: 0.07
Nodes (20): sfx_events(), scene_cues(), full_props(), full_summary(), full_cues(), spoken_at(), spoken_span(), _board() (+12 more)

### Community 9 - "toolkit.tsx"
Cohesion: 0.15
Nodes (25): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+17 more)

### Community 10 - "audio_mix.py"
Cohesion: 0.12
Nodes (3): freesound_fetch(), music_gain(), test_music_gain_evens_out_tracks()

### Community 11 - "drawn_thumbnail"
Cohesion: 0.18
Nodes (6): get_image(), openverse_images(), ov_get(), full_pictures(), drawn_thumbnail(), test_board_pictures_attached()

### Community 12 - "code_custom_scenes"
Cohesion: 0.12
Nodes (13): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+5 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.14
Nodes (17): Box, boxAt(), clamp, fitCard(), hits(), layoutColumn(), layoutGrid(), layoutRow() (+9 more)

### Community 14 - "make"
Cohesion: 0.17
Nodes (6): caption_layer(), make(), master_gain(), project_xml(), remove(), test_timeline_has_scenes_captions_sound_and_markers()

### Community 15 - "test_rules.py"
Cohesion: 0.20
Nodes (20): parse_rules(), make(), stop_text(), test_bad_min_pictures_stops(), test_blender_needs_a_build_plan_section(), test_bom_and_crlf_load_the_same(), test_draft_stops(), test_draft_writes_tagged_draft_file() (+12 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "full/types.ts"
Cohesion: 0.16
Nodes (18): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), gridFor(), FullScene() (+10 more)

### Community 18 - "prepare_topic"
Cohesion: 0.22
Nodes (7): contact_sheets(), load_pool(), pool_folder(), prepare_topic(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip(), test_small_pool_skips_ai()

### Community 19 - "test_pictures_first.py"
Cohesion: 0.12
Nodes (26): write_json(), catalog_entries(), catalog_pool(), clean_pics(), save_pool(), entry(), fake_ai, film() (+18 more)

### Community 20 - "gen.py"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "test_style.py"
Cohesion: 0.13
Nodes (14): approve_candidate(), clean_style_code(), library_menu(), reject_candidate(), save_candidate(), candidate_in(), library_snapshot(), restore_library() (+6 more)

### Community 22 - "choose_images"
Cohesion: 0.19
Nodes (14): choose_images(), apply_look_scenes(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+6 more)

### Community 23 - "test_blender_scene.py"
Cohesion: 0.08
Nodes (35): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_photo() (+27 more)

### Community 24 - "image_sources.py"
Cohesion: 0.08
Nodes (18): archive_films(), commons_films(), crop_film_bytes(), film_frames(), nasa_films(), pixabay_films(), archive_images(), article_images() (+10 more)

### Community 25 - "write_scripts"
Cohesion: 0.09
Nodes (22): pictures_of(), limit_full(), direct_scripts(), edit_scripts(), length_plan(), narration_lines(), story_problems(), write_scripts() (+14 more)

### Community 26 - "gather_pool"
Cohesion: 0.12
Nodes (7): gather_pool(), owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (16): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+8 more)

### Community 28 - "style_library"
Cohesion: 0.06
Nodes (22): cut_text(), edit_plan(), look_text(), picture_line(), clean_invention(), clean_look(), clean_transition(), settle_style() (+14 more)

### Community 29 - "sentence_groups"
Cohesion: 0.29
Nodes (6): sentence_groups(), build(), add(), main(), scenes(), test_sentences_running_across_cuts_are_one_take()

### Community 30 - "render"
Cohesion: 0.12
Nodes (9): short_credit(), graphics_count(), wants_remotion(), srt(), drawn_choices(), render(), save_state(), test_drawn_choices_have_no_pictures() (+1 more)

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (22): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+14 more)

### Community 32 - "apply_review_fixes"
Cohesion: 0.15
Nodes (8): apply_review_fixes(), ask(), _review_state(), test_auto_fix_graphic(), test_look_check_fixes_code(), test_redraw_failure_paints(), test_review_redraws_custom(), test_review_uses_unused_pool_pictures_before_painting()

### Community 33 - "test_blender_render.py"
Cohesion: 0.11
Nodes (18): BlenderFailed, peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws() (+10 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "render_remotion"
Cohesion: 0.06
Nodes (30): ass_time(), caption_lines(), captions(), styled(), ass_colour(), render_remotion(), remotion(), render() (+22 more)

### Community 36 - "re"
Cohesion: 0.09
Nodes (14): align(), align_words(), main(), say_number(), studio_speak(), spoken_count(), voicestudio_up(), vault_page() (+6 more)

### Community 37 - "run_check"
Cohesion: 0.22
Nodes (9): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once(), test_opener_must_be_a_later_real_picture() (+1 more)

### Community 38 - "build_scene.py"
Cohesion: 0.18
Nodes (5): collection(), ink_lines(), linear(), setup(), radians()

### Community 39 - "local_clips"
Cohesion: 0.15
Nodes (9): cover_crop(), local_clips(), local_job(), local_voice(), motion_prompt(), veo_handoff(), video_encoder(), test_local_job_retries_a_hard_crash() (+1 more)

### Community 40 - "clean_photo"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 41 - "main"
Cohesion: 0.18
Nodes (4): keyvis(), main(), Failure, key()

### Community 42 - "Short.tsx"
Cohesion: 0.12
Nodes (21): Captions(), HookTitle(), PersonCard(), Root(), Background(), Card, flashAlpha(), GraphicFor() (+13 more)

### Community 43 - "first_second_check"
Cohesion: 0.13
Nodes (9): log_short(), clock(), first_second_check(), quality_check(), review_fixes(), storyboard(), visual_review(), test_review_is_told_the_drawings_are_deliberate() (+1 more)

### Community 44 - "pool_pictures"
Cohesion: 0.15
Nodes (6): film_piece(), film_ffmpeg(), catalog_text(), is_usable(), usable(), pool_pictures()

### Community 45 - "ffmpeg"
Cohesion: 0.22
Nodes (8): shot_span(), split_takes(), duration(), ffmpeg(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), videos(), test_a_take_is_cut_between_the_scenes_words()

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "json"
Cohesion: 0.10
Nodes (12): code_version(), comfy_call(), moss_graph(), moss_images(), voicestudio_unload(), load_state(), article_text(), fact_check() (+4 more)

### Community 49 - "speak"
Cohesion: 0.20
Nodes (6): speak(), story_sound(), tts(), test_story_sound_library(), fetch(), _tone_wav()

### Community 51 - "plan_rules.py"
Cohesion: 0.12
Nodes (8): hex_rgb(), luminance(), short_skin(), tsc_check(), make_paper(), prune_work(), test_clean_full_custom_and_skin(), test_make_paper()

### Community 52 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 54 - "trend_research"
Cohesion: 0.20
Nodes (6): channel_url(), new_channel(), save_channel(), seed_ideas(), trend_research(), yt_list()

### Community 55 - "capture_prompts"
Cohesion: 0.20
Nodes (6): load_rules(), min_real_pictures(), capture_prompts(), ask(), test_load_rules_sets_session(), test_strange_history_prompts_unchanged()

### Community 56 - "run_draft"
Cohesion: 0.33
Nodes (7): draft_reply(), run_draft(), test_draft_blender_channel_needs_build_plan(), test_draft_keeps_ai_headings_inside_their_section(), test_draft_never_overwrites(), test_draft_retries_once_then_stops(), test_draft_settings_come_from_code()

### Community 57 - "use_picture_from"
Cohesion: 0.29
Nodes (4): use_picture_from(), paint_new(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 58 - "draft_rules"
Cohesion: 0.33
Nodes (3): draft_rules(), require_rules(), test_missing_rules_file_is_drafted()

### Community 59 - "paint_instead"
Cohesion: 0.12
Nodes (6): gemini_images(), to_vertical(), ink_silhouette(), paint_instead(), test_ink_silhouette(), test_remotion_failure_paints()

## Knowledge Gaps
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `clean_full`, `main`, `ask_ai`, `full_cues`, `audio_mix.py`, `drawn_thumbnail`, `make`, `test_style.py`, `choose_images`, `frame_maker`, `style_library`, `apply_review_fixes`, `test_blender_render.py`, `render_remotion`, `re`, `local_clips`, `clean_photo`, `first_second_check`, `ffmpeg`, `json`, `speak`, `plan_rules.py`, `paint_instead`, `make_sfx`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.1282051282051282 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `build_scene.py`, `json`, `Shots`, `parts.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Should `clean_full` be split into smaller, more focused modules?**
  _Cohesion score 0.09247311827956989 - nodes in this community are weakly interconnected._
- **Why does `mark_details()` connect `ask_ai` to `image_sources.py`, `plan_rules.py`, `re`, `render`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `main` be split into smaller, more focused modules?**
  _Cohesion score 0.08465608465608465 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._