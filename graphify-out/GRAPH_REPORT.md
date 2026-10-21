# Graph Report - ShortsMaker  (2026-10-21)

## Corpus Check
- 85 files · ~83,825 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .canvas 1)

## Summary
- 1066 nodes · 2916 edges · 59 communities (46 shown, 13 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 51 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Style Library Inventions (TS)
- Remotion Short Composition
- Footage Downloads & Crops
- Custom Scene Toolkit & Examples
- Split Script (tools)
- Entry Point, Logbook & Sounds
- Channel Profiles & CLI
- Style Lab & Edit Plan Text
- AI Calls & Quota Fallback
- Python Frame Renderer
- Paper & Evidence Board Scenes
- Picture List Catalog
- Motion Previews & Render Tests
- Full-Scene Rescue & Plan Cleaning
- Guarded Layout (cards, arrows)
- Commons & Archive Sources
- Map Journey Scene
- Big Number Scene
- Script Writing Pipeline
- GPU Worker (gen.py)
- Voice Worker (qwen_voice)
- Picture Picker
- Full-Scene Limits & Director Tests
- Skins & Remotion Render
- Local AI Jobs & Clips
- Review Fixes
- Captions & TTS
- Style Tests
- Scene Cues & Word Timing
- Pool Storage & Contact Sheets
- SFX Events & Full Pictures
- Story Sounds & Credits
- Photo Cleanup
- Pool Gathering
- Invention Slots
- Gemini Image Painting
- Full-Scene Props
- Library Candidate Tests
- SFX Synthesis
- Visual Review Sheets
- Quality Check & Script Editing
- Test Patching Helper
- Music & Freesound
- fix.bat Picture Swaps
- YouTube Research
- Usable Picture Filter
- Look & Transition Cleaning
- Edit Plan
- Ink Silhouettes
- Invention Lint
- Planning Fakes (tests)
- Invention Validation
- Style Guardrails
- SRT Captions File
- Story Sound Limits
- Remotion Decision
- Look Scenes
- LTX Crash Retry Test
- Picture List Parsing

## God Nodes (most connected - your core abstractions)
1. `render()` - 53 edges
2. `write_scripts()` - 37 edges
3. `skinOf()` - 29 edges
4. `Paper()` - 25 edges
5. `ask_ai()` - 24 edges
6. `main()` - 23 edges
7. `choose_images()` - 22 edges
8. `clean_full()` - 21 edges
9. `style_library()` - 20 edges
10. `pool_of()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `test_numbers()` --calls--> `say_number()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_words_keep_what_is_written()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_every_aligned_word_is_in_the_aligner_alphabet()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_prune_cache_handles_pools()` --calls--> `prune_cache()`  [EXTRACTED]
  tests/test_pictures_first.py → shortsmaker/picture_pool.py
- `test_library_entries_have_fields()` --calls--> `style_library()`  [EXTRACTED]
  tests/test_style.py → shortsmaker/style_lab.py

## Import Cycles
- None detected.

## Communities (59 total, 13 thin omitted)

### Community 0 - "Style Library Inventions (TS)"
Cohesion: 0.09
Nodes (45): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01() (+37 more)

### Community 1 - "Remotion Short Composition"
Cohesion: 0.09
Nodes (50): Captions(), card, clamp, DotGrid(), MarkCard(), Props, StatCard(), TimelineCard() (+42 more)

### Community 2 - "Footage Downloads & Crops"
Cohesion: 0.07
Nodes (19): archive_films(), crop_film_bytes(), film_frames(), film_piece(), nasa_films(), pixabay_films(), shot_span(), comfy_call() (+11 more)

### Community 3 - "Custom Scene Toolkit & Examples"
Cohesion: 0.18
Nodes (23): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+15 more)

### Community 4 - "Split Script (tools)"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 5 - "Entry Point, Logbook & Sounds"
Cohesion: 0.07
Nodes (21): clean_sound(), ask_brain(), ask_count(), ask_number(), ask_yes(), load_channel(), new_channel(), pick_channel() (+13 more)

### Community 7 - "Style Lab & Edit Plan Text"
Cohesion: 0.10
Nodes (16): cut_text(), look_text(), voicestudio_unload(), approve_candidate(), clean_style_code(), invent_component(), invent_styles(), library_menu() (+8 more)

### Community 8 - "AI Calls & Quota Fallback"
Cohesion: 0.08
Nodes (18): ask_ai(), quota_exhausted(), run_agy(), clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code() (+10 more)

### Community 9 - "Python Frame Renderer"
Cohesion: 0.08
Nodes (14): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), frame_maker(), frame(), graphic_low() (+6 more)

### Community 10 - "Paper & Evidence Board Scenes"
Cohesion: 0.15
Nodes (25): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+17 more)

### Community 11 - "Picture List Catalog"
Cohesion: 0.17
Nodes (21): catalog_pool(), clean_pics(), entry(), fake_ai, film(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+13 more)

### Community 12 - "Motion Previews & Render Tests"
Cohesion: 0.12
Nodes (6): preview_sheet(), tsc_check(), main(), props_for(), build(), main()

### Community 13 - "Full-Scene Rescue & Plan Cleaning"
Cohesion: 0.11
Nodes (20): rescue_graphics(), clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures() (+12 more)

### Community 14 - "Guarded Layout (cards, arrows)"
Cohesion: 0.14
Nodes (17): Box, boxAt(), clamp, fitCard(), hits(), layoutColumn(), layoutGrid(), layoutRow() (+9 more)

### Community 15 - "Commons & Archive Sources"
Cohesion: 0.09
Nodes (13): commons_films(), article_images(), commons_search(), get_image(), openverse_images(), ov_get(), thumb_url(), usable_license() (+5 more)

### Community 16 - "Map Journey Scene"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "Big Number Scene"
Cohesion: 0.16
Nodes (18): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), gridFor(), FullScene() (+10 more)

### Community 18 - "Script Writing Pipeline"
Cohesion: 0.16
Nodes (16): write_scripts(), passing(), prepare(), planning, test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), test_both_mode_reuses_pools() (+8 more)

### Community 19 - "GPU Worker (gen.py)"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 20 - "Voice Worker (qwen_voice)"
Cohesion: 0.16
Nodes (8): align(), align_words(), main(), say_number(), studio_speak(), test_caption_words_keep_what_is_written(), test_every_aligned_word_is_in_the_aligner_alphabet(), test_numbers()

### Community 21 - "Picture Picker"
Cohesion: 0.25
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 22 - "Full-Scene Limits & Director Tests"
Cohesion: 0.14
Nodes (9): limit_full(), _fake_planning(), test_director_prompt_mentions_full(), test_limit_full(), test_music_gain_evens_out_tracks(), test_short_credit(), test_story_sound_library(), fetch() (+1 more)

### Community 23 - "Skins & Remotion Render"
Cohesion: 0.14
Nodes (9): short_skin(), render_remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain() (+1 more)

### Community 24 - "Local AI Jobs & Clips"
Cohesion: 0.20
Nodes (7): cover_crop(), local_clips(), local_job(), local_voice(), motion_prompt(), veo_handoff(), video_encoder()

### Community 25 - "Review Fixes"
Cohesion: 0.14
Nodes (8): apply_review_fixes(), ask(), _review_state(), test_auto_fix_graphic(), test_look_check_fixes_code(), test_redraw_failure_paints(), test_review_redraws_custom(), test_rewrite_paint_prompts()

### Community 26 - "Captions & TTS"
Cohesion: 0.16
Nodes (7): ass_time(), caption_lines(), captions(), styled(), speak(), tts(), ass_colour()

### Community 27 - "Style Tests"
Cohesion: 0.18
Nodes (8): plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics(), test_library_entries_have_fields(), test_save_candidate_unique_slug(), test_style_sounds()

### Community 28 - "Scene Cues & Word Timing"
Cohesion: 0.16
Nodes (8): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish()

### Community 29 - "Pool Storage & Contact Sheets"
Cohesion: 0.19
Nodes (7): write_json(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_pool_rows_without_thumbs()

### Community 30 - "SFX Events & Full Pictures"
Cohesion: 0.15
Nodes (8): sfx_events(), full_pictures(), make_paper(), _board(), test_board_pictures_attached(), test_make_paper(), test_sfx_full(), test_story_sound_wins_its_moment()

### Community 31 - "Story Sounds & Credits"
Cohesion: 0.21
Nodes (8): story_sound(), short_credit(), ffmpeg(), graphics_count(), load_state(), render(), save_state(), test_state_roundtrip_full_pics()

### Community 32 - "Photo Cleanup"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 33 - "Pool Gathering"
Cohesion: 0.18
Nodes (5): gather_pool(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits(), test_pool_roundtrip()

### Community 34 - "Invention Slots"
Cohesion: 0.21
Nodes (9): restore_style_slots(), style_placeholders(), test_candidate_names_unique_across_kinds(), test_failed_invention_keeps_the_others(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_slots_restored_after_render() (+1 more)

### Community 35 - "Gemini Image Painting"
Cohesion: 0.18
Nodes (4): gemini_images(), to_vertical(), paint_instead(), test_remotion_failure_paints()

### Community 36 - "Full-Scene Props"
Cohesion: 0.22
Nodes (7): full_props(), full_summary(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_full_summary(), test_remotion_props_full()

### Community 37 - "Library Candidate Tests"
Cohesion: 0.29
Nodes (7): candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_reject_deletes()

### Community 38 - "SFX Synthesis"
Cohesion: 0.22
Nodes (3): make_sfx(), flash_alpha(), write_frames()

### Community 39 - "Visual Review Sheets"
Cohesion: 0.28
Nodes (5): clock(), review_fixes(), storyboard(), visual_review(), test_review_fix_kinds()

### Community 40 - "Quality Check & Script Editing"
Cohesion: 0.22
Nodes (4): quality_check(), edit_scripts(), length_plan(), narration_lines()

### Community 43 - "fix.bat Picture Swaps"
Cohesion: 0.32
Nodes (4): paint_new(), use_picture_from(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 44 - "YouTube Research"
Cohesion: 0.29
Nodes (4): channel_url(), seed_ideas(), trend_research(), yt_list()

### Community 45 - "Usable Picture Filter"
Cohesion: 0.29
Nodes (4): catalog_text(), is_usable(), pictures_of(), usable()

### Community 46 - "Look & Transition Cleaning"
Cohesion: 0.29
Nodes (5): clean_look(), clean_transition(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 47 - "Edit Plan"
Cohesion: 0.33
Nodes (3): edit_plan(), picture_line(), test_edit_plan_picture_line()

### Community 49 - "Invention Lint"
Cohesion: 0.40
Nodes (4): attempt(), lint_style_code(), test_invention_lint_failure_uses_fallback(), test_placeholders_match_the_slots()

## Knowledge Gaps
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `Story Sounds & Credits` to `Footage Downloads & Crops`, `Entry Point, Logbook & Sounds`, `Channel Profiles & CLI`, `Style Lab & Edit Plan Text`, `AI Calls & Quota Fallback`, `Python Frame Renderer`, `Motion Previews & Render Tests`, `Full-Scene Rescue & Plan Cleaning`, `Picture Picker`, `Skins & Remotion Render`, `Local AI Jobs & Clips`, `Review Fixes`, `Captions & TTS`, `Scene Cues & Word Timing`, `SFX Events & Full Pictures`, `Photo Cleanup`, `Gemini Image Painting`, `Full-Scene Props`, `SFX Synthesis`, `Visual Review Sheets`, `Quality Check & Script Editing`, `Music & Freesound`, `Edit Plan`, `Ink Silhouettes`, `SRT Captions File`, `Remotion Decision`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Should `Style Library Inventions (TS)` be split into smaller, more focused modules?**
  _Cohesion score 0.08951406649616368 - nodes in this community are weakly interconnected._
- **Why does `to_vertical()` connect `Gemini Image Painting` to `Photo Cleanup`, `Story Sounds & Credits`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Should `Remotion Short Composition` be split into smaller, more focused modules?**
  _Cohesion score 0.08764568764568764 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `Script Writing Pipeline` to `Entry Point, Logbook & Sounds`, `Channel Profiles & CLI`, `Style Lab & Edit Plan Text`, `AI Calls & Quota Fallback`, `Quality Check & Script Editing`, `Picture List Catalog`, `YouTube Research`, `Usable Picture Filter`, `Full-Scene Rescue & Plan Cleaning`, `Look & Transition Cleaning`, `Commons & Archive Sources`, `Motion Previews & Render Tests`, `Invention Validation`, `Style Guardrails`, `Story Sound Limits`, `Full-Scene Limits & Director Tests`, `Style Tests`, `Pool Storage & Contact Sheets`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Should `Footage Downloads & Crops` be split into smaller, more focused modules?**
  _Cohesion score 0.06801346801346801 - nodes in this community are weakly interconnected._
- **Should `Split Script (tools)` be split into smaller, more focused modules?**
  _Cohesion score 0.09291521486643438 - nodes in this community are weakly interconnected._