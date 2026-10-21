# Graph Report - ShortsMaker  (2026-10-21)

## Corpus Check
- 86 files · ~85,478 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .canvas 1)

## Summary
- 1085 nodes · 2958 edges · 56 communities (45 shown, 11 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 51 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Style Library Inventions (TS)
- Remotion Short Composition
- Local AI Jobs & Clips
- Channel Profiles & CLI
- Entry Point, Logbook & Sounds
- Custom Scene Toolkit & Examples
- Split Script (tools)
- Python Frame Renderer
- Voice Worker (qwen_voice)
- Invention Slots
- Paper & Evidence Board Scenes
- Picture List Catalog (2)
- Footage Downloads & Crops (2)
- AI Calls & Quota Fallback (4)
- Guarded Layout (cards, arrows)
- Full-Scene Rescue & Plan Cleaning
- AI Calls & Quota Fallback
- AI Calls & Quota Fallback (2)
- Story Sounds & Credits (2)
- Map Journey Scene
- Big Number Scene
- GPU Worker (gen.py)
- Invention Slots (2)
- Picture List Catalog
- Style Tests
- Picture List Catalog (3)
- Footage Downloads & Crops
- Footage Downloads & Crops (2) (2)
- Scene Cues & Word Timing
- Photo Cleanup
- Skins & Remotion Render
- Footage Downloads & Crops (2) (3)
- AI Calls & Quota Fallback (4) (2)
- Captions & TTS
- Scene Cues & Word Timing (3)
- Footage Downloads & Crops (2)
- Library Candidate Tests
- AI Calls & Quota Fallback (4) (3)
- Picture List Catalog (2) (2)
- Captions & TTS (2)
- AI Calls & Quota Fallback (2)
- Channel Profiles & CLI (2)
- Gemini Image Painting
- Look & Transition Cleaning
- Pool Gathering
- Picture List Catalog (2)
- Picture List Catalog (5)
- Captions & TTS (3)
- Look & Transition Cleaning (2)
- Style Guardrails
- Story Sounds & Credits (3)
- Story Sounds & Credits (4)
- Picture List Catalog (2) (2)
- Story Sounds & Credits (2) (2)
- Style Tests (2)
- AI Calls & Quota Fallback (4) (4)

## God Nodes (most connected - your core abstractions)
1. `render()` - 54 edges
2. `write_scripts()` - 37 edges
3. `skinOf()` - 29 edges
4. `ask_ai()` - 27 edges
5. `Paper()` - 25 edges
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
- `test_encoder_cache_lives_with_video_encoder()` --calls--> `video_encoder()`  [EXTRACTED]
  tests/test_package.py → shortsmaker/media_tools.py
- `test_code_custom_scenes_fallback()` --calls--> `code_custom_scenes()`  [EXTRACTED]
  tests/test_full_scenes.py → shortsmaker/motion.py

## Import Cycles
- None detected.

## Communities (56 total, 11 thin omitted)

### Community 0 - "Style Library Inventions (TS)"
Cohesion: 0.09
Nodes (45): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01() (+37 more)

### Community 1 - "Remotion Short Composition"
Cohesion: 0.09
Nodes (50): Captions(), card, clamp, DotGrid(), MarkCard(), Props, StatCard(), TimelineCard() (+42 more)

### Community 2 - "Local AI Jobs & Clips"
Cohesion: 0.05
Nodes (27): limit_sounds(), archive_films(), commons_films(), crop_film_bytes(), film_frames(), nasa_films(), archive_images(), article_images() (+19 more)

### Community 3 - "Channel Profiles & CLI"
Cohesion: 0.13
Nodes (4): clean_sound(), hex_rgb(), luminance(), first_second_check()

### Community 4 - "Entry Point, Logbook & Sounds"
Cohesion: 0.07
Nodes (23): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+15 more)

### Community 5 - "Custom Scene Toolkit & Examples"
Cohesion: 0.18
Nodes (23): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+15 more)

### Community 6 - "Split Script (tools)"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 7 - "Python Frame Renderer"
Cohesion: 0.09
Nodes (15): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+7 more)

### Community 8 - "Voice Worker (qwen_voice)"
Cohesion: 0.09
Nodes (18): align(), align_words(), main(), say_number(), studio_speak(), logbook_results(), real(), run_check() (+10 more)

### Community 9 - "Invention Slots"
Cohesion: 0.10
Nodes (16): freesound_fetch(), cut_text(), look_text(), approve_candidate(), clean_style_code(), invent_component(), invent_styles(), library_menu() (+8 more)

### Community 10 - "Paper & Evidence Board Scenes"
Cohesion: 0.15
Nodes (25): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+17 more)

### Community 11 - "Picture List Catalog (2)"
Cohesion: 0.17
Nodes (21): catalog_entries(), catalog_pool(), entry(), fake_ai, film(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+13 more)

### Community 12 - "Footage Downloads & Crops (2)"
Cohesion: 0.13
Nodes (11): comfy_call(), cover_crop(), local_clips(), local_job(), local_voice(), moss_graph(), moss_images(), motion_prompt() (+3 more)

### Community 13 - "AI Calls & Quota Fallback (4)"
Cohesion: 0.09
Nodes (16): sfx_events(), _board(), test_board_pictures_attached(), test_code_custom_scenes_fallback(), test_fact_check_drops_full(), test_lint_custom_code(), test_local_job_retries_a_hard_crash(), test_music_gain_evens_out_tracks() (+8 more)

### Community 14 - "Guarded Layout (cards, arrows)"
Cohesion: 0.14
Nodes (17): Box, boxAt(), clamp, fitCard(), hits(), layoutColumn(), layoutGrid(), layoutRow() (+9 more)

### Community 15 - "Full-Scene Rescue & Plan Cleaning"
Cohesion: 0.11
Nodes (18): short_skin(), clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures() (+10 more)

### Community 16 - "AI Calls & Quota Fallback"
Cohesion: 0.10
Nodes (11): ask_ai(), quota_exhausted(), run_agy(), rescue_graphics(), article_text(), fact_check(), test_claude_pinned_to_opus_high(), test_encoder_cache_lives_with_video_encoder() (+3 more)

### Community 17 - "AI Calls & Quota Fallback (2)"
Cohesion: 0.15
Nodes (11): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+3 more)

### Community 18 - "Story Sounds & Credits (2)"
Cohesion: 0.12
Nodes (11): edit_plan(), clock(), graphics_count(), mark_details(), quality_check(), storyboard(), visual_review(), load_state() (+3 more)

### Community 19 - "Map Journey Scene"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 20 - "Big Number Scene"
Cohesion: 0.16
Nodes (18): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), gridFor(), FullScene() (+10 more)

### Community 21 - "GPU Worker (gen.py)"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 22 - "Invention Slots (2)"
Cohesion: 0.13
Nodes (14): attempt(), lint_style_code(), restore_style_slots(), style_placeholders(), test_candidate_names_unique_across_kinds(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback() (+6 more)

### Community 23 - "Picture List Catalog"
Cohesion: 0.19
Nodes (14): write_scripts(), passing(), prepare(), planning, test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), test_both_mode_reuses_pools() (+6 more)

### Community 24 - "Style Tests"
Cohesion: 0.14
Nodes (10): wants_remotion(), plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics(), test_library_entries_have_fields(), test_remotion_forced_by_look() (+2 more)

### Community 25 - "Picture List Catalog (3)"
Cohesion: 0.25
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 26 - "Footage Downloads & Crops"
Cohesion: 0.17
Nodes (10): write_json(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip() (+2 more)

### Community 27 - "Footage Downloads & Crops (2) (2)"
Cohesion: 0.17
Nodes (6): pixabay_films(), prune_cache(), main(), props_for(), build(), main()

### Community 28 - "Scene Cues & Word Timing"
Cohesion: 0.16
Nodes (8): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish()

### Community 29 - "Photo Cleanup"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 30 - "Skins & Remotion Render"
Cohesion: 0.17
Nodes (8): render_remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain(), test_swap_inventions()

### Community 31 - "Footage Downloads & Crops (2) (3)"
Cohesion: 0.21
Nodes (5): film_piece(), shot_span(), voicestudio_up(), duration(), ffmpeg()

### Community 32 - "AI Calls & Quota Fallback (4) (2)"
Cohesion: 0.20
Nodes (6): apply_review_fixes(), swap_pictures(), _review_state(), test_auto_fix_graphic(), test_redraw_failure_paints(), test_review_redraws_custom()

### Community 33 - "Captions & TTS"
Cohesion: 0.22
Nodes (4): music_gain(), speak(), story_sound(), tts()

### Community 34 - "Scene Cues & Word Timing (3)"
Cohesion: 0.22
Nodes (7): full_props(), full_summary(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_full_summary(), test_remotion_props_full()

### Community 35 - "Footage Downloads & Crops (2)"
Cohesion: 0.20
Nodes (5): catalog_text(), clean_pics(), is_usable(), pictures_of(), usable()

### Community 36 - "Library Candidate Tests"
Cohesion: 0.29
Nodes (7): candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_reject_deletes()

### Community 37 - "AI Calls & Quota Fallback (4) (3)"
Cohesion: 0.22
Nodes (5): _fake_planning(), ask(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_rewrite_paint_prompts()

### Community 39 - "Captions & TTS (2)"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 40 - "AI Calls & Quota Fallback (2)"
Cohesion: 0.29
Nodes (4): use_picture_from(), paint_new(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 41 - "Channel Profiles & CLI (2)"
Cohesion: 0.25
Nodes (3): gemini_images(), to_vertical(), paint_instead()

### Community 42 - "Gemini Image Painting"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 43 - "Look & Transition Cleaning"
Cohesion: 0.29
Nodes (5): clean_look(), clean_transition(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 44 - "Pool Gathering"
Cohesion: 0.29
Nodes (3): stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 45 - "Picture List Catalog (2)"
Cohesion: 0.33
Nodes (3): edit_scripts(), length_plan(), narration_lines()

## Knowledge Gaps
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `Story Sounds & Credits (2)` to `Local AI Jobs & Clips`, `Channel Profiles & CLI`, `Entry Point, Logbook & Sounds`, `Python Frame Renderer`, `Invention Slots`, `Footage Downloads & Crops (2)`, `AI Calls & Quota Fallback (4)`, `AI Calls & Quota Fallback`, `Style Tests`, `Picture List Catalog (3)`, `Footage Downloads & Crops (2) (2)`, `Scene Cues & Word Timing`, `Photo Cleanup`, `Skins & Remotion Render`, `Footage Downloads & Crops (2) (3)`, `AI Calls & Quota Fallback (4) (2)`, `Captions & TTS`, `Scene Cues & Word Timing (3)`, `Captions & TTS (2)`, `Channel Profiles & CLI (2)`, `Gemini Image Painting`, `Captions & TTS (3)`, `Story Sounds & Credits (3)`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Should `Style Library Inventions (TS)` be split into smaller, more focused modules?**
  _Cohesion score 0.08951406649616368 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `Picture List Catalog` to `Local AI Jobs & Clips`, `Channel Profiles & CLI`, `Entry Point, Logbook & Sounds`, `Footage Downloads & Crops (2)`, `AI Calls & Quota Fallback (4) (3)`, `Voice Worker (qwen_voice)`, `Invention Slots`, `Look & Transition Cleaning`, `Picture List Catalog (2)`, `Full-Scene Rescue & Plan Cleaning`, `AI Calls & Quota Fallback`, `Style Guardrails`, `Look & Transition Cleaning (2)`, `Picture List Catalog (2) (2)`, `Style Tests`, `Footage Downloads & Crops`, `Footage Downloads & Crops (2) (2)`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `Remotion Short Composition` be split into smaller, more focused modules?**
  _Cohesion score 0.08764568764568764 - nodes in this community are weakly interconnected._
- **Why does `owner()` connect `Picture List Catalog (2) (2)` to `AI Calls & Quota Fallback (4) (3)`, `Picture List Catalog (2)`, `Pool Gathering`, `AI Calls & Quota Fallback (4)`, `Picture List Catalog (5)`, `Invention Slots (2)`, `Style Tests`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Should `Local AI Jobs & Clips` be split into smaller, more focused modules?**
  _Cohesion score 0.05202661826981246 - nodes in this community are weakly interconnected._
- **Should `Channel Profiles & CLI` be split into smaller, more focused modules?**
  _Cohesion score 0.12979591836734694 - nodes in this community are weakly interconnected._