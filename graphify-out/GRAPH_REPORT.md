# Graph Report - ShortsMaker  (2026-10-26)

## Corpus Check
- 105 files · ~114,143 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .canvas 1, .ipynb 1)

## Summary
- 1529 nodes · 4131 edges · 76 communities (67 shown, 9 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 101 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6781d5db`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Cards.tsx
- ask_ai
- skinOf
- trend_research
- split_make_shorts.py
- re
- test_h3_handoff.py
- scene_cues
- toolkit.tsx
- subprocess
- h3_run.py
- ExampleEvidence.tsx
- guarded.tsx
- Shotcut Timeline and Loudness
- make
- Journey.tsx
- BigNumber.tsx
- prepare_topic
- write_scripts
- Local GPU Worker
- style_library
- make_sfx
- Blender Scene Tests
- test_rules.py
- test_blender_plan.py
- speak
- frame_maker
- MapCard.tsx
- clean_full
- render
- parts.py
- drawn_thumbnail
- test_blender_render.py
- templates.py
- render_remotion
- time
- test_first_second.py
- Blender Ink Look
- QuestionBeat.tsx
- trim_borders
- main
- Short.tsx
- visual_review
- words_of
- local_voice
- style_lab.py
- kit.ts
- json
- test_pictures_first.py
- capture_prompts
- main
- build_scene.py
- Style Library Caps
- rewrite_paint_prompts
- use_picture_from
- BlenderFailed
- choose_images
- edit_scripts
- apply_review_fixes
- clean_sound
- plan_with
- gather_pool
- ask_brain
- test_full_scenes.py
- pool_pictures
- wm_files
- planning_ai
- captions
- fact_check
- clean_graphic
- logbook_results
- write_json
- rescue_graphics
- catalog_entries
- test_on_topic_ignores_a_lone_shared_name

## God Nodes (most connected - your core abstractions)
1. `render()` - 61 edges
2. `write_scripts()` - 44 edges
3. `ask_ai()` - 35 edges
4. `skinOf()` - 29 edges
5. `main()` - 26 edges
6. `Paper()` - 25 edges
7. `choose_images()` - 24 edges
8. `words_of()` - 22 edges
9. `clean_full()` - 21 edges
10. `Bridge` - 20 edges

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

## Communities (76 total, 9 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.17
Nodes (15): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, clamp01(), H, W, Cut (+7 more)

### Community 1 - "Cards.tsx"
Cohesion: 0.23
Nodes (21): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+13 more)

### Community 2 - "ask_ai"
Cohesion: 0.05
Nodes (32): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx() (+24 more)

### Community 3 - "skinOf"
Cohesion: 0.30
Nodes (21): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+13 more)

### Community 4 - "trend_research"
Cohesion: 0.20
Nodes (6): channel_url(), new_channel(), save_channel(), seed_ideas(), trend_research(), yt_list()

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "re"
Cohesion: 0.10
Nodes (7): music_gain(), vault_page(), vault_refresh(), is_loop_short(), parse_scene_money(), max_full(), max_full_planned()

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.06
Nodes (43): cover_crop(), cut_owner_clip(), gemini_images(), h3_problems(), h3_prompt(), h3_prompts(), local_clips(), motion_prompt() (+35 more)

### Community 8 - "scene_cues"
Cohesion: 0.06
Nodes (23): sfx_events(), scene_cues(), full_props(), full_summary(), full_cues(), spoken_at(), spoken_span(), _board() (+15 more)

### Community 9 - "toolkit.tsx"
Cohesion: 0.12
Nodes (31): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+23 more)

### Community 10 - "subprocess"
Cohesion: 0.07
Nodes (13): shot_span(), fills_frame(), sentence_groups(), log_short(), duration(), main(), props_for(), build() (+5 more)

### Community 11 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 12 - "ExampleEvidence.tsx"
Cohesion: 0.23
Nodes (3): clamp, CustomFull, FullProps

### Community 13 - "guarded.tsx"
Cohesion: 0.13
Nodes (18): Box, boxAt(), clamp, fitCard(), hits(), layoutColumn(), layoutGrid(), layoutRow() (+10 more)

### Community 14 - "Shotcut Timeline and Loudness"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "make"
Cohesion: 0.17
Nodes (19): parse_rules(), make(), stop_text(), test_bad_min_pictures_stops(), test_blender_needs_a_build_plan_section(), test_bom_and_crlf_load_the_same(), test_draft_stops(), test_duplicate_heading_stops() (+11 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.16
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "BigNumber.tsx"
Cohesion: 0.27
Nodes (11): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+3 more)

### Community 18 - "prepare_topic"
Cohesion: 0.22
Nodes (7): contact_sheets(), load_pool(), pool_folder(), prepare_topic(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip(), test_small_pool_skips_ai()

### Community 19 - "write_scripts"
Cohesion: 0.14
Nodes (16): pictures_of(), limit_full(), direct_scripts(), write_scripts(), test_limit_full(), passing(), prepare(), planning (+8 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.08
Nodes (17): cut_text(), edit_plan(), look_text(), picture_line(), clean_invention(), clean_look(), clean_transition(), settle_style() (+9 more)

### Community 23 - "Blender Scene Tests"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 24 - "test_rules.py"
Cohesion: 0.23
Nodes (11): draft_reply(), run_draft(), StopPicker, test_draft_blender_channel_needs_build_plan(), test_draft_keeps_ai_headings_inside_their_section(), test_draft_never_overwrites(), test_draft_retries_once_then_stops(), test_draft_settings_come_from_code() (+3 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.11
Nodes (22): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+14 more)

### Community 26 - "speak"
Cohesion: 0.20
Nodes (6): speak(), story_sound(), tts(), test_story_sound_library(), fetch(), _tone_wav()

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (14): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+6 more)

### Community 28 - "MapCard.tsx"
Cohesion: 0.16
Nodes (7): Pin(), clamp, interpolateColor(), MapCard(), topo, Root(), ShortProps

### Community 29 - "clean_full"
Cohesion: 0.18
Nodes (9): clean_full(), number_figures(), show_number(), test_clean_full_board(), test_clean_full_document(), test_clean_full_journey(), test_clean_full_keeps_thing(), test_clean_full_limits() (+1 more)

### Community 30 - "render"
Cohesion: 0.10
Nodes (12): short_credit(), graphics_count(), to_vertical(), wants_remotion(), srt(), drawn_choices(), load_state(), render() (+4 more)

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (22): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+14 more)

### Community 32 - "drawn_thumbnail"
Cohesion: 0.23
Nodes (9): scene_frames(), drawn_thumbnail(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 33 - "test_blender_render.py"
Cohesion: 0.22
Nodes (12): peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises(), test_frames_are_trimmed_after_the_clips_are_cut() (+4 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "render_remotion"
Cohesion: 0.06
Nodes (29): short_skin(), ink_silhouette(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), invent_component(), attempt() (+21 more)

### Community 36 - "time"
Cohesion: 0.13
Nodes (14): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+6 more)

### Community 37 - "test_first_second.py"
Cohesion: 0.19
Nodes (13): first_second_check(), swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once() (+5 more)

### Community 38 - "Blender Ink Look"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 39 - "QuestionBeat.tsx"
Cohesion: 0.27
Nodes (5): FONT, theme, Word, CLAMP, KineticTitle()

### Community 40 - "trim_borders"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 41 - "main"
Cohesion: 0.17
Nodes (4): main(), Failure, key(), focus_object()

### Community 42 - "Short.tsx"
Cohesion: 0.14
Nodes (21): Captions(), clamp, HookTitle(), PersonCard(), SubscribeCta(), Background(), Card, flashAlpha() (+13 more)

### Community 43 - "visual_review"
Cohesion: 0.16
Nodes (9): clock(), overlay_notes(), quality_check(), review_fixes(), storyboard(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose() (+1 more)

### Community 44 - "words_of"
Cohesion: 0.27
Nodes (6): graphic_low(), fill_money_graphics(), is_person_portrait(), words_of(), test_fill_money_graphics_and_caps(), test_clean_full_keeps_board_pic()

### Community 45 - "local_voice"
Cohesion: 0.09
Nodes (10): local_job(), local_voice(), split_takes(), spoken_count(), voicestudio_unload(), voicestudio_up(), paint_instead(), test_local_job_retries_a_hard_crash() (+2 more)

### Community 46 - "style_lab.py"
Cohesion: 0.12
Nodes (15): tsc_check(), approve_candidate(), clean_style_code(), library_menu(), reject_candidate(), save_candidate(), candidate_in(), library_snapshot() (+7 more)

### Community 47 - "kit.ts"
Cohesion: 0.15
Nodes (27): InventedLook(), CAPTION_TOP, drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas() (+19 more)

### Community 48 - "json"
Cohesion: 0.07
Nodes (19): freesound_fetch(), code_version(), archive_films(), commons_films(), crop_film_bytes(), film_frames(), nasa_films(), pixabay_films() (+11 more)

### Community 49 - "test_pictures_first.py"
Cohesion: 0.13
Nodes (26): catalog_pool(), clean_pics(), save_pool(), entry(), fake_ai, film(), pic_short(), pool_of() (+18 more)

### Community 50 - "capture_prompts"
Cohesion: 0.20
Nodes (6): load_rules(), min_real_pictures(), capture_prompts(), ask(), test_load_rules_sets_session(), test_strange_history_prompts_unchanged()

### Community 51 - "main"
Cohesion: 0.09
Nodes (17): ask_count(), ask_yes(), load_channel(), pick_channel(), use_channel(), fix_short(), main(), prune_cache() (+9 more)

### Community 52 - "build_scene.py"
Cohesion: 0.15
Nodes (5): direction(), keyloc(), keyvis(), Shots, radians()

### Community 54 - "rewrite_paint_prompts"
Cohesion: 0.18
Nodes (5): rewrite_paint_prompts(), ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 55 - "use_picture_from"
Cohesion: 0.29
Nodes (4): use_picture_from(), paint_new(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 57 - "choose_images"
Cohesion: 0.14
Nodes (17): get_image(), choose_images(), full_pictures(), apply_look_scenes(), test_board_pictures_attached(), picking, planned_short(), scene() (+9 more)

### Community 58 - "edit_scripts"
Cohesion: 0.17
Nodes (7): edit_scripts(), length_plan(), narration_lines(), story_problems(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules(), test_story_problems()

### Community 59 - "apply_review_fixes"
Cohesion: 0.25
Nodes (5): apply_review_fixes(), _review_state(), test_auto_fix_graphic(), test_redraw_failure_paints(), test_review_redraws_custom()

### Community 60 - "clean_sound"
Cohesion: 0.29
Nodes (5): clean_sound(), limit_sounds(), word(), contains(), test_clean_sound()

### Community 61 - "plan_with"
Cohesion: 0.29
Nodes (5): plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 62 - "gather_pool"
Cohesion: 0.10
Nodes (9): openverse_images(), ov_get(), gather_pool(), owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape() (+1 more)

### Community 63 - "ask_brain"
Cohesion: 0.40
Nodes (3): ask_brain(), ask_number(), test_solo_brain_selection_options()

### Community 64 - "test_full_scenes.py"
Cohesion: 0.12
Nodes (6): hex_rgb(), luminance(), make_paper(), test_make_paper(), test_music_gain_evens_out_tracks(), test_short_credit()

### Community 65 - "pool_pictures"
Cohesion: 0.15
Nodes (6): film_piece(), film_ffmpeg(), catalog_text(), is_usable(), usable(), pool_pictures()

### Community 66 - "wm_files"
Cohesion: 0.22
Nodes (5): article_images(), commons_search(), thumb_url(), usable_license(), wm_files()

### Community 68 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 69 - "fact_check"
Cohesion: 0.40
Nodes (3): article_text(), fact_check(), test_fact_check_drops_full()

### Community 70 - "clean_graphic"
Cohesion: 0.50
Nodes (4): clean_graphic(), coords(), is_num(), test_clean_question_and_kinetic()

## Knowledge Gaps
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `templates.py`, `Blender Ink Look`, `json`, `build_scene.py`, `parts.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.05203619909502263 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `ask_ai`, `re`, `test_h3_handoff.py`, `scene_cues`, `subprocess`, `Shotcut Timeline and Loudness`, `style_library`, `make_sfx`, `speak`, `frame_maker`, `drawn_thumbnail`, `test_blender_render.py`, `render_remotion`, `test_first_second.py`, `trim_borders`, `visual_review`, `words_of`, `local_voice`, `style_lab.py`, `json`, `main`, `choose_images`, `apply_review_fixes`, `test_full_scenes.py`, `captions`, `rescue_graphics`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `ask_ai`, `trend_research`, `re`, `prepare_topic`, `style_library`, `test_blender_plan.py`, `clean_full`, `words_of`, `style_lab.py`, `json`, `test_pictures_first.py`, `capture_prompts`, `main`, `Style Library Caps`, `edit_scripts`, `clean_sound`, `plan_with`, `gather_pool`, `fact_check`, `clean_graphic`, `logbook_results`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Should `re` be split into smaller, more focused modules?**
  _Cohesion score 0.09764309764309764 - nodes in this community are weakly interconnected._
- **Should `test_h3_handoff.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05576923076923077 - nodes in this community are weakly interconnected._