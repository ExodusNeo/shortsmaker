# Graph Report - ShortsMaker  (2026-10-22)

## Corpus Check
- 2 files · ~89,983 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1138 nodes · 2917 edges · 69 communities (52 shown, 17 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 51 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Style Library Components
- Remotion Captions & Cards
- Scene Cues & Image Search
- Custom Scene Examples
- Entry Point & Channel Menus
- Package Split Tool
- CLI & Pixabay Films
- Freesound & Picture Swaps
- Full Scene Tests
- Evidence Board Scenes
- Audio Mix & Music Gain
- Film Archive Sources
- AI-Coded Motion Scenes
- Guarded Scene Layout
- Shotcut Timeline
- Config & Palettes
- Map Journey Scenes
- Big Number Scenes
- Picture Pool & Catalog
- Pictures-First Tests
- GPU Image Worker
- Style Candidates
- Picture Picker
- Review Fixes & Pool Swaps
- GPU Voice & Painters
- Script Writing Pipeline
- Test Patching Helpers
- Python Frame Renderer
- Style Inventions
- Package & TS Tests
- Gemini Painting & Renderer Choice
- Sentence Voice Takes
- Planning Test Fakes
- Remotion Render & Figures
- Photo Look Scenes
- Invention Slots
- Qwen/CosyVoice Worker
- First-Second Check Tests
- Edit Plan Text
- Local Clips & GPU Jobs
- Photo Cleanup
- Style Validation
- Style Registry
- Script Editor & Story Checks
- Film Frames & Crops
- Usable Picture Checks
- Fake AI Helpers
- Frame Overlays & Fonts
- AI Calls & Quota
- Caption Lines (ASS)
- SFX Synthesis
- Frame Maker & Credit Tags
- Detail Marks & Storyboard
- Subject Position Checks
- Sound Cue Sheet
- Visual Review
- SRT Captions
- Fact Check
- Vertical Crop
- Pool Swap Test
- Worker Crash Retry
- Remotion Failure Test
- Story Sound Test
- Motion Graphic Timing Test
- Credit Tag Test
- Music Gain Test
- Figure Silhouette Test
- Quota Fallback Test

## God Nodes (most connected - your core abstractions)
1. `skinOf()` - 29 edges
2. `Paper()` - 25 edges
3. `render()` - 25 edges
4. `main()` - 23 edges
5. `choose_images()` - 21 edges
6. `pool_of()` - 19 edges
7. `style_library()` - 19 edges
8. `write_scripts()` - 18 edges
9. `invent_component()` - 17 edges
10. `catalog_pool()` - 17 edges

## Surprising Connections (you probably didn't know these)
- `test_clean_question_and_kinetic()` --calls--> `clean_graphic()`  [EXTRACTED]
  tests/test_style.py → shortsmaker/plan_rules.py
- `test_prune_cache_handles_pools()` --calls--> `prune_cache()`  [EXTRACTED]
  tests/test_pictures_first.py → shortsmaker/picture_pool.py
- `test_logbook_marks_tiny_samples()` --calls--> `logbook_results()`  [EXTRACTED]
  tests/test_first_second.py → shortsmaker/logbook.py
- `test_approve_adds_to_library()` --calls--> `approve_candidate()`  [EXTRACTED]
  tests/test_style.py → shortsmaker/style_lab.py
- `test_approve_rolls_back_on_tsc_failure()` --calls--> `approve_candidate()`  [EXTRACTED]
  tests/test_style.py → shortsmaker/style_lab.py

## Import Cycles
- None detected.

## Communities (69 total, 17 thin omitted)

### Community 0 - "Style Library Components"
Cohesion: 0.07
Nodes (53): InventedLook(), InventedOverlay(), InventedTransition, has(), lookFor(), LOOKS, overlayFor(), OVERLAYS (+45 more)

### Community 1 - "Remotion Captions & Cards"
Cohesion: 0.11
Nodes (42): Captions(), card, clamp, DotGrid(), MarkCard(), Props, StatCard(), TimelineCard() (+34 more)

### Community 2 - "Scene Cues & Image Search"
Cohesion: 0.06
Nodes (25): clean_sound(), scene_cues(), article_images(), commons_search(), openverse_images(), thumb_url(), wm_files(), rescue_graphics() (+17 more)

### Community 3 - "Custom Scene Examples"
Cohesion: 0.18
Nodes (23): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+15 more)

### Community 4 - "Entry Point & Channel Menus"
Cohesion: 0.08
Nodes (21): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+13 more)

### Community 5 - "Package Split Tool"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "CLI & Pixabay Films"
Cohesion: 0.14
Nodes (3): pixabay_films(), short_credit(), prune_cache()

### Community 7 - "Freesound & Picture Swaps"
Cohesion: 0.09
Nodes (12): freesound_fetch(), use_picture_from(), tsc_check(), first_second_check(), rewrite_paint_prompts(), approve_candidate(), clean_style_code(), library_menu() (+4 more)

### Community 8 - "Full Scene Tests"
Cohesion: 0.08
Nodes (6): _board(), _jpg(), test_board_pictures_attached(), test_custom_cues_props_and_pictures(), test_remotion_props_full(), test_sfx_full()

### Community 9 - "Evidence Board Scenes"
Cohesion: 0.15
Nodes (25): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+17 more)

### Community 10 - "Audio Mix & Music Gain"
Cohesion: 0.12
Nodes (9): limit_sounds(), music_gain(), speak(), story_sound(), tts(), shot_span(), duration(), ffmpeg() (+1 more)

### Community 11 - "Film Archive Sources"
Cohesion: 0.10
Nodes (14): archive_films(), commons_films(), nasa_films(), archive_images(), get_image(), nasa_images(), nasa_search(), on_topic() (+6 more)

### Community 12 - "AI-Coded Motion Scenes"
Cohesion: 0.13
Nodes (10): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), full_props(), full_summary(), lint_custom_code(), look_and_fix() (+2 more)

### Community 13 - "Guarded Scene Layout"
Cohesion: 0.14
Nodes (17): Box, boxAt(), clamp, fitCard(), hits(), layoutColumn(), layoutGrid(), layoutRow() (+9 more)

### Community 14 - "Shotcut Timeline"
Cohesion: 0.13
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "Config & Palettes"
Cohesion: 0.16
Nodes (4): hex_rgb(), luminance(), short_skin(), make_paper()

### Community 16 - "Map Journey Scenes"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "Big Number Scenes"
Cohesion: 0.16
Nodes (18): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), gridFor(), FullScene() (+10 more)

### Community 18 - "Picture Pool & Catalog"
Cohesion: 0.13
Nodes (14): write_json(), catalog_entries(), catalog_pool(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool() (+6 more)

### Community 19 - "Pictures-First Tests"
Cohesion: 0.24
Nodes (16): entry(), film(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film(), test_both_mode_reuses_pools(), test_catalog_both_empty_stops_uncached() (+8 more)

### Community 20 - "GPU Image Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "Style Candidates"
Cohesion: 0.20
Nodes (11): save_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_candidate_names_unique_across_kinds() (+3 more)

### Community 22 - "Picture Picker"
Cohesion: 0.25
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 23 - "Review Fixes & Pool Swaps"
Cohesion: 0.13
Nodes (8): apply_review_fixes(), paint_new(), pool_pictures(), quality_check(), swap_pictures(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 24 - "GPU Voice & Painters"
Cohesion: 0.16
Nodes (6): comfy_call(), local_voice(), moss_graph(), moss_images(), voicestudio_unload(), voicestudio_up()

### Community 25 - "Script Writing Pipeline"
Cohesion: 0.22
Nodes (13): write_scripts(), passing(), prepare(), planning, test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), test_dropped_topic_pool_removed() (+5 more)

### Community 26 - "Test Patching Helpers"
Cohesion: 0.14
Nodes (4): owner(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 27 - "Python Frame Renderer"
Cohesion: 0.16
Nodes (6): ClipReader, draw_card(), draw_graphic(), frame(), shot(), write_frames()

### Community 28 - "Style Inventions"
Cohesion: 0.15
Nodes (9): invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), swap_inventions(), test_invention_lint_failure_uses_fallback(), test_placeholders_match_the_slots() (+1 more)

### Community 30 - "Gemini Painting & Renderer Choice"
Cohesion: 0.18
Nodes (7): gemini_images(), paint_instead(), wants_remotion(), load_state(), render(), save_state(), test_remotion_forced_by_look()

### Community 31 - "Sentence Voice Takes"
Cohesion: 0.18
Nodes (7): sentence_groups(), split_takes(), spoken_count(), scenes(), test_a_take_is_cut_between_the_scenes_words(), test_sentences_running_across_cuts_are_one_take(), test_word_counts_match_the_aligner()

### Community 32 - "Planning Test Fakes"
Cohesion: 0.14
Nodes (8): _fake_planning(), ask(), _review_state(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_redraw_failure_paints(), test_review_redraws_custom(), test_rewrite_paint_prompts()

### Community 33 - "Remotion Render & Figures"
Cohesion: 0.18
Nodes (7): ink_silhouette(), redraw_custom(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), test_invention_runtime_failure_uses_fallback()

### Community 34 - "Photo Look Scenes"
Cohesion: 0.13
Nodes (9): apply_look_scenes(), style_props(), plan_with(), ask(), test_apply_look_scenes(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics() (+1 more)

### Community 35 - "Invention Slots"
Cohesion: 0.21
Nodes (9): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_slots_restored_after_render() (+1 more)

### Community 36 - "Qwen/CosyVoice Worker"
Cohesion: 0.23
Nodes (5): align(), align_words(), main(), say_number(), studio_speak()

### Community 37 - "First-Second Check Tests"
Cohesion: 0.30
Nodes (9): real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once(), test_opener_must_be_a_later_real_picture() (+1 more)

### Community 38 - "Edit Plan Text"
Cohesion: 0.18
Nodes (6): cut_text(), edit_plan(), look_text(), picture_line(), clock(), test_edit_plan_picture_line()

### Community 39 - "Local Clips & GPU Jobs"
Cohesion: 0.27
Nodes (5): cover_crop(), local_clips(), local_job(), motion_prompt(), veo_handoff()

### Community 40 - "Photo Cleanup"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 41 - "Style Validation"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 42 - "Style Registry"
Cohesion: 0.20
Nodes (7): style_library(), style_rules(), write_style_index(), build(), main(), test_library_entries_have_fields(), test_write_style_index_is_deterministic()

### Community 43 - "Script Editor & Story Checks"
Cohesion: 0.18
Nodes (6): edit_scripts(), length_plan(), narration_lines(), story_problems(), test_editor_gets_one_second_pass_for_broken_rules(), test_story_problems()

### Community 44 - "Film Frames & Crops"
Cohesion: 0.20
Nodes (4): crop_film_bytes(), film_frames(), film_piece(), film_ffmpeg()

### Community 45 - "Usable Picture Checks"
Cohesion: 0.20
Nodes (5): catalog_text(), clean_pics(), is_usable(), pictures_of(), usable()

### Community 46 - "Fake AI Helpers"
Cohesion: 0.22
Nodes (4): fake_ai, planning_ai(), reply(), test_seo_pass_empty_no_ai()

### Community 47 - "Frame Overlays & Fonts"
Cohesion: 0.31
Nodes (4): fit_font(), graphic_overlay(), person_card(), thumbnail()

### Community 48 - "AI Calls & Quota"
Cohesion: 0.28
Nodes (4): ask_ai(), gemini_model(), quota_exhausted(), run_agy()

### Community 49 - "Caption Lines (ASS)"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 51 - "Frame Maker & Credit Tags"
Cohesion: 0.29
Nodes (3): frame_maker(), credit_tag_image(), fallback_graphic()

### Community 56 - "Visual Review"
Cohesion: 0.40
Nodes (3): review_fixes(), visual_review(), test_review_fix_kinds()

### Community 63 - "Story Sound Test"
Cohesion: 0.67
Nodes (3): test_story_sound_library(), fetch(), _tone_wav()

## Knowledge Gaps
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `choose_images()` connect `Picture Picker` to `Scene Cues & Image Search`, `Photo Look Scenes`, `Entry Point & Channel Menus`, `CLI & Pixabay Films`, `Freesound & Picture Swaps`, `Style Registry`, `Film Archive Sources`, `Film Frames & Crops`, `AI Calls & Quota`, `Picture Pool & Catalog`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Should `Style Library Components` be split into smaller, more focused modules?**
  _Cohesion score 0.06993828974434323 - nodes in this community are weakly interconnected._
- **Why does `gather_pool()` connect `Scene Cues & Image Search` to `Edit Plan Text`, `CLI & Pixabay Films`, `Film Archive Sources`, `Picture Pool & Catalog`, `Picture Picker`, `Test Patching Helpers`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Should `Remotion Captions & Cards` be split into smaller, more focused modules?**
  _Cohesion score 0.1085972850678733 - nodes in this community are weakly interconnected._
- **Why does `ClipReader` connect `Python Frame Renderer` to `Subject Position Checks`, `Frame Overlays & Fonts`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Should `Scene Cues & Image Search` be split into smaller, more focused modules?**
  _Cohesion score 0.0596078431372549 - nodes in this community are weakly interconnected._
- **Should `Entry Point & Channel Menus` be split into smaller, more focused modules?**
  _Cohesion score 0.080338266384778 - nodes in this community are weakly interconnected._