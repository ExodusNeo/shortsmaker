# Graph Report - ShortsMaker  (2026-10-22)

## Corpus Check
- 11 files · ~89,088 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1133 nodes · 2965 edges · 60 communities (52 shown, 8 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 50 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Channel Profiles & Menus
- Remotion Captions & Cards
- Film Footage Sources
- Package Split Tool
- Edit Plan Text
- Photo Looks Library
- Python Frame Renderer
- Guarded Scene Layout
- Archive Film & Downloads
- Custom Scene Slots
- AI Calls & Trend Seeds
- Word Counts & Test Utils
- Graphics Rescue & Validation
- Style Inventions
- Evidence Board & Documents
- Picture Catalog
- Sound Effects & Story Sounds
- Quality & Visual Review
- Style Candidates
- Big Number Scenes
- Map Journey Scenes
- Transitions & Overlays
- Media Tools & Shot Spans
- Shotcut Timeline
- Picture Picker
- GPU Image Worker
- Full Scene Tests
- Entry Point & Run Menus
- Script Writing Pipeline
- Picture Pool Prep
- Test Patching Helpers
- Local Voice & Clips
- Painting & Renderer Choice
- Style Registry
- Logbook Lessons & First Second
- Qwen/CosyVoice Worker
- Sound Cue Sheet
- Remotion Render & Skins
- Photo Cleanup
- Review Auto Fixes
- Repaint Prompt Rewrites
- Shared Graphics Kit
- Scene & Graphic Timing
- Full Scene Props
- Usable Picture Checks
- SFX & Paper Synthesis
- Caption Lines (ASS)
- Trend Research & New Channel
- Fix.bat Picture Swaps
- Logbook & Vault Pages
- Figure Silhouettes & Redraws
- Sentence Voice Takes
- Planning Test Fakes
- Run Questions
- Style Guardrails
- SRT Captions
- Vertical Crop
- Motion Graphic Limits
- Worker Crash Retry
- Picture List Entries

## God Nodes (most connected - your core abstractions)
1. `skinOf()` - 29 edges
2. `Paper()` - 25 edges
3. `render()` - 25 edges
4. `main()` - 23 edges
5. `choose_images()` - 21 edges
6. `clean_full()` - 20 edges
7. `pool_of()` - 19 edges
8. `ask_ai()` - 19 edges
9. `style_library()` - 19 edges
10. `write_scripts()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `test_rescue_respects_caps()` --calls--> `rescue_graphics()`  [EXTRACTED]
  tests/test_full_scenes.py → shortsmaker/picker.py
- `test_clean_full_board()` --calls--> `clean_full()`  [EXTRACTED]
  tests/test_full_scenes.py → shortsmaker/plan_rules.py
- `test_clean_full_document()` --calls--> `clean_full()`  [EXTRACTED]
  tests/test_full_scenes.py → shortsmaker/plan_rules.py
- `test_clean_full_journey()` --calls--> `clean_full()`  [EXTRACTED]
  tests/test_full_scenes.py → shortsmaker/plan_rules.py
- `test_clean_full_keeps_thing()` --calls--> `clean_full()`  [EXTRACTED]
  tests/test_full_scenes.py → shortsmaker/plan_rules.py

## Import Cycles
- None detected.

## Communities (60 total, 8 thin omitted)

### Community 0 - "Channel Profiles & Menus"
Cohesion: 0.11
Nodes (6): hex_rgb(), luminance(), tsc_check(), approve_candidate(), library_menu(), reject_candidate()

### Community 1 - "Remotion Captions & Cards"
Cohesion: 0.09
Nodes (41): Captions(), card, clamp, DotGrid(), MarkCard(), Props, StatCard(), TimelineCard() (+33 more)

### Community 2 - "Film Footage Sources"
Cohesion: 0.07
Nodes (20): commons_films(), film_piece(), nasa_films(), archive_images(), article_images(), commons_search(), film_ffmpeg(), get_image() (+12 more)

### Community 3 - "Package Split Tool"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 4 - "Edit Plan Text"
Cohesion: 0.05
Nodes (26): cut_text(), edit_plan(), look_text(), picture_line(), clean_invention(), clean_look(), clean_transition(), settle_style() (+18 more)

### Community 5 - "Photo Looks Library"
Cohesion: 0.14
Nodes (30): InventedLook(), clamp01(), drawCover(), FILL, H, luminance(), noise(), stretch() (+22 more)

### Community 6 - "Python Frame Renderer"
Cohesion: 0.06
Nodes (16): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+8 more)

### Community 7 - "Guarded Scene Layout"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 8 - "Archive Film & Downloads"
Cohesion: 0.10
Nodes (11): archive_films(), crop_film_bytes(), film_frames(), pixabay_films(), comfy_call(), moss_graph(), moss_images(), voicestudio_unload() (+3 more)

### Community 9 - "Custom Scene Slots"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 10 - "AI Calls & Trend Seeds"
Cohesion: 0.08
Nodes (17): seed_ideas(), ask_ai(), gemini_model(), quota_exhausted(), run_agy(), clean_tsx_code(), code_custom_scenes(), custom_rules() (+9 more)

### Community 11 - "Word Counts & Test Utils"
Cohesion: 0.07
Nodes (3): spoken_count(), test_argon_out_of_quota_switches_to_flash(), test_word_counts_match_the_aligner()

### Community 12 - "Graphics Rescue & Validation"
Cohesion: 0.13
Nodes (15): rescue_graphics(), clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures() (+7 more)

### Community 13 - "Style Inventions"
Cohesion: 0.10
Nodes (18): invent_component(), attempt(), invent_styles(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), swap_inventions() (+10 more)

### Community 14 - "Evidence Board & Documents"
Cohesion: 0.14
Nodes (24): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+16 more)

### Community 15 - "Picture Catalog"
Cohesion: 0.19
Nodes (20): catalog_pool(), entry(), fake_ai, film(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film() (+12 more)

### Community 16 - "Sound Effects & Story Sounds"
Cohesion: 0.11
Nodes (10): clean_sound(), freesound_fetch(), limit_sounds(), music_gain(), speak(), story_sound(), tts(), mark_details() (+2 more)

### Community 17 - "Quality & Visual Review"
Cohesion: 0.10
Nodes (12): clock(), quality_check(), review_fixes(), storyboard(), visual_review(), edit_scripts(), length_plan(), narration_lines() (+4 more)

### Community 18 - "Style Candidates"
Cohesion: 0.16
Nodes (13): save_candidate(), style_props(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes() (+5 more)

### Community 19 - "Big Number Scenes"
Cohesion: 0.18
Nodes (16): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), gridFor(), InkIcon() (+8 more)

### Community 20 - "Map Journey Scenes"
Cohesion: 0.14
Nodes (18): FullScene(), clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level() (+10 more)

### Community 21 - "Transitions & Overlays"
Cohesion: 0.22
Nodes (11): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, Cut, Fade, Flash, Leak (+3 more)

### Community 22 - "Media Tools & Shot Spans"
Cohesion: 0.14
Nodes (7): shot_span(), duration(), ffmpeg(), video_encoder(), first_second_check(), main(), props_for()

### Community 23 - "Shotcut Timeline"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "Picture Picker"
Cohesion: 0.19
Nodes (14): choose_images(), apply_look_scenes(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+6 more)

### Community 25 - "GPU Image Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 26 - "Full Scene Tests"
Cohesion: 0.12
Nodes (12): test_clean_full_board(), test_clean_full_document(), test_clean_full_journey(), test_clean_full_keeps_thing(), test_clean_full_limits(), test_music_gain_evens_out_tracks(), test_remotion_failure_paints(), test_rescue_respects_caps() (+4 more)

### Community 27 - "Entry Point & Run Menus"
Cohesion: 0.15
Nodes (11): ask_count(), ask_yes(), load_channel(), pick_channel(), use_channel(), fix_short(), main(), prune_cache() (+3 more)

### Community 28 - "Script Writing Pipeline"
Cohesion: 0.21
Nodes (13): write_scripts(), passing(), prepare(), planning, test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), test_dropped_topic_pool_removed() (+5 more)

### Community 29 - "Picture Pool Prep"
Cohesion: 0.17
Nodes (10): write_json(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip() (+2 more)

### Community 30 - "Test Patching Helpers"
Cohesion: 0.14
Nodes (4): owner(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 31 - "Local Voice & Clips"
Cohesion: 0.20
Nodes (7): cover_crop(), local_clips(), local_job(), local_voice(), motion_prompt(), split_takes(), veo_handoff()

### Community 32 - "Painting & Renderer Choice"
Cohesion: 0.17
Nodes (8): gemini_images(), paint_instead(), wants_remotion(), load_state(), render(), save_state(), test_state_roundtrip_full_pics(), test_remotion_forced_by_look()

### Community 33 - "Style Registry"
Cohesion: 0.20
Nodes (8): has(), lookFor(), overlayFor(), transitionFor(), TRANSITIONS, inksOf(), transitionWindow(), INKS

### Community 34 - "Logbook Lessons & First Second"
Cohesion: 0.24
Nodes (10): logbook_results(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once() (+2 more)

### Community 35 - "Qwen/CosyVoice Worker"
Cohesion: 0.23
Nodes (5): align(), align_words(), main(), say_number(), studio_speak()

### Community 36 - "Sound Cue Sheet"
Cohesion: 0.18
Nodes (7): sfx_events(), full_pictures(), _board(), test_board_pictures_attached(), test_sfx_full(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 37 - "Remotion Render & Skins"
Cohesion: 0.22
Nodes (7): short_skin(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), test_clean_full_custom_and_skin(), test_invention_runtime_failure_uses_fallback()

### Community 38 - "Photo Cleanup"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 39 - "Review Auto Fixes"
Cohesion: 0.20
Nodes (6): apply_review_fixes(), swap_pictures(), _review_state(), test_auto_fix_graphic(), test_redraw_failure_paints(), test_review_redraws_custom()

### Community 40 - "Repaint Prompt Rewrites"
Cohesion: 0.18
Nodes (6): rewrite_paint_prompts(), _fake_planning(), ask(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_rewrite_paint_prompts()

### Community 41 - "Shared Graphics Kit"
Cohesion: 0.29
Nodes (5): FONT, outline(), CAPTION_TOP, CLAMP, QuestionBeat()

### Community 42 - "Scene & Graphic Timing"
Cohesion: 0.20
Nodes (6): scene_cues(), full_cues(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish()

### Community 43 - "Full Scene Props"
Cohesion: 0.22
Nodes (7): full_props(), full_summary(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_full_summary(), test_remotion_props_full()

### Community 44 - "Usable Picture Checks"
Cohesion: 0.20
Nodes (5): catalog_text(), clean_pics(), is_usable(), pictures_of(), usable()

### Community 45 - "SFX & Paper Synthesis"
Cohesion: 0.25
Nodes (3): make_sfx(), make_paper(), test_make_paper()

### Community 46 - "Caption Lines (ASS)"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 47 - "Trend Research & New Channel"
Cohesion: 0.25
Nodes (5): channel_url(), new_channel(), save_channel(), trend_research(), yt_list()

### Community 48 - "Fix.bat Picture Swaps"
Cohesion: 0.29
Nodes (4): use_picture_from(), paint_new(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 49 - "Logbook & Vault Pages"
Cohesion: 0.29
Nodes (3): log_short(), vault_page(), vault_refresh()

### Community 50 - "Figure Silhouettes & Redraws"
Cohesion: 0.29
Nodes (3): ink_silhouette(), redraw_custom(), test_ink_silhouette()

### Community 51 - "Sentence Voice Takes"
Cohesion: 0.40
Nodes (4): sentence_groups(), scenes(), test_a_take_is_cut_between_the_scenes_words(), test_sentences_running_across_cuts_are_one_take()

## Knowledge Gaps
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `choose_images()` connect `Picture Picker` to `Channel Profiles & Menus`, `Film Footage Sources`, `Sound Cue Sheet`, `Edit Plan Text`, `Archive Film & Downloads`, `AI Calls & Trend Seeds`, `Entry Point & Run Menus`, `Picture Pool Prep`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Should `Channel Profiles & Menus` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._
- **Why does `is_stereo()` connect `Photo Cleanup` to `Channel Profiles & Menus`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Should `Remotion Captions & Cards` be split into smaller, more focused modules?**
  _Cohesion score 0.08956228956228957 - nodes in this community are weakly interconnected._
- **Why does `ask_ai()` connect `AI Calls & Trend Seeds` to `Channel Profiles & Menus`, `Repaint Prompt Rewrites`, `Graphics Rescue & Validation`, `Style Inventions`, `Picture Catalog`, `Trend Research & New Channel`, `Sound Effects & Story Sounds`, `Quality & Visual Review`, `Media Tools & Shot Spans`, `Picture Picker`, `Entry Point & Run Menus`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Should `Film Footage Sources` be split into smaller, more focused modules?**
  _Cohesion score 0.06767676767676768 - nodes in this community are weakly interconnected._
- **Should `Package Split Tool` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._