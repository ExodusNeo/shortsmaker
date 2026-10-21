# Graph Report - ShortsMaker  (2026-10-21)

## Corpus Check
- 85 files · ~84,000 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .canvas 1)

## Summary
- 1067 nodes · 2908 edges · 49 communities (42 shown, 7 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 51 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Style Library Inventions (TS)
- Remotion Short Composition
- Entry Point, Logbook & Sounds
- Custom Scene Toolkit & Examples
- Channel Profiles & CLI
- Split Script (tools)
- Local AI Jobs & Clips
- Commons & Archive Sources
- Python Frame Renderer
- Scene Cues & Word Timing
- Full-Scene Rescue & Plan Cleaning
- Footage Downloads & Crops (2)
- Paper & Evidence Board Scenes
- Picture List Catalog
- AI Calls & Quota Fallback
- Invention Slots
- Guarded Layout (cards, arrows)
- Map Journey Scene
- Big Number Scene
- Picture List Catalog (2)
- Picture List Catalog (3)
- GPU Worker (gen.py)
- Library Candidate Tests
- Voice Worker (qwen_voice)
- Skins & Remotion Render
- Local AI Jobs & Clips (2)
- Story Sounds & Credits
- Style Lab & Edit Plan Text
- Captions & TTS
- AI Calls & Quota Fallback (2)
- Picture List Catalog (4)
- Style Tests
- Gemini Image Painting
- Story Sounds & Credits (2)
- AI Calls & Quota Fallback (3)
- Pool Gathering
- Photo Cleanup
- Look & Transition Cleaning
- AI Calls & Quota Fallback (4)
- Picture List Catalog (5)
- Motion Previews & Render Tests
- Footage Downloads & Crops
- Test Patching Helper
- Story Sounds & Credits (3)
- Story Sounds & Credits (4)
- Scene Cues & Word Timing (2)
- Style Guardrails
- Scene Cues & Word Timing (3)
- Scene Cues & Word Timing (4)

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
- `test_fake_reaches_callers()` --calls--> `code_custom_scenes()`  [EXTRACTED]
  tests/test_package.py → shortsmaker/motion.py
- `test_prune_cache_handles_pools()` --calls--> `prune_cache()`  [EXTRACTED]
  tests/test_pictures_first.py → shortsmaker/picture_pool.py

## Import Cycles
- None detected.

## Communities (49 total, 7 thin omitted)

### Community 0 - "Style Library Inventions (TS)"
Cohesion: 0.09
Nodes (45): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01() (+37 more)

### Community 1 - "Remotion Short Composition"
Cohesion: 0.09
Nodes (50): Captions(), card, clamp, DotGrid(), MarkCard(), Props, StatCard(), TimelineCard() (+42 more)

### Community 2 - "Entry Point, Logbook & Sounds"
Cohesion: 0.07
Nodes (21): ask_count(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel(), save_channel(), seed_ideas() (+13 more)

### Community 3 - "Custom Scene Toolkit & Examples"
Cohesion: 0.18
Nodes (23): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+15 more)

### Community 5 - "Split Script (tools)"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "Local AI Jobs & Clips"
Cohesion: 0.09
Nodes (14): archive_films(), crop_film_bytes(), film_frames(), nasa_films(), pixabay_films(), comfy_call(), local_job(), local_voice() (+6 more)

### Community 7 - "Commons & Archive Sources"
Cohesion: 0.06
Nodes (20): commons_films(), article_images(), commons_search(), get_image(), openverse_images(), ov_get(), thumb_url(), usable_license() (+12 more)

### Community 8 - "Python Frame Renderer"
Cohesion: 0.07
Nodes (15): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), frame_maker(), frame(), graphic_low() (+7 more)

### Community 9 - "Scene Cues & Word Timing"
Cohesion: 0.06
Nodes (22): sfx_events(), scene_cues(), full_props(), full_summary(), full_pictures(), full_cues(), spoken_at(), spoken_span() (+14 more)

### Community 10 - "Full-Scene Rescue & Plan Cleaning"
Cohesion: 0.08
Nodes (23): clean_sound(), limit_sounds(), archive_images(), nasa_images(), on_topic(), clean_full(), word(), clean_graphic() (+15 more)

### Community 11 - "Footage Downloads & Crops (2)"
Cohesion: 0.08
Nodes (11): freesound_fetch(), music_gain(), film_piece(), shot_span(), flash_alpha(), film_ffmpeg(), duration(), write_json() (+3 more)

### Community 12 - "Paper & Evidence Board Scenes"
Cohesion: 0.15
Nodes (25): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+17 more)

### Community 13 - "Picture List Catalog"
Cohesion: 0.11
Nodes (19): limit_full(), edit_scripts(), length_plan(), narration_lines(), write_scripts(), test_limit_full(), passing(), prepare() (+11 more)

### Community 14 - "AI Calls & Quota Fallback"
Cohesion: 0.13
Nodes (13): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+5 more)

### Community 15 - "Invention Slots"
Cohesion: 0.12
Nodes (16): invent_component(), attempt(), invent_styles(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others() (+8 more)

### Community 16 - "Guarded Layout (cards, arrows)"
Cohesion: 0.14
Nodes (17): Box, boxAt(), clamp, fitCard(), hits(), layoutColumn(), layoutGrid(), layoutRow() (+9 more)

### Community 17 - "Map Journey Scene"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 18 - "Big Number Scene"
Cohesion: 0.16
Nodes (18): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), gridFor(), FullScene() (+10 more)

### Community 19 - "Picture List Catalog (2)"
Cohesion: 0.18
Nodes (17): catalog_entries(), catalog_pool(), clean_pics(), entry(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film() (+9 more)

### Community 20 - "Picture List Catalog (3)"
Cohesion: 0.25
Nodes (13): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+5 more)

### Community 21 - "GPU Worker (gen.py)"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 22 - "Library Candidate Tests"
Cohesion: 0.15
Nodes (13): approve_candidate(), library_menu(), reject_candidate(), save_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library() (+5 more)

### Community 23 - "Voice Worker (qwen_voice)"
Cohesion: 0.16
Nodes (8): align(), align_words(), main(), say_number(), studio_speak(), test_caption_words_keep_what_is_written(), test_every_aligned_word_is_in_the_aligner_alphabet(), test_numbers()

### Community 24 - "Skins & Remotion Render"
Cohesion: 0.13
Nodes (10): short_skin(), render_remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_clean_full_custom_and_skin(), test_invention_runtime_failure_uses_fallback() (+2 more)

### Community 25 - "Local AI Jobs & Clips (2)"
Cohesion: 0.17
Nodes (8): cover_crop(), gemini_images(), local_clips(), motion_prompt(), veo_handoff(), ffmpeg(), video_encoder(), test_encoder_cache_lives_with_video_encoder()

### Community 26 - "Story Sounds & Credits"
Cohesion: 0.15
Nodes (9): short_credit(), graphics_count(), to_vertical(), wants_remotion(), load_state(), render(), save_state(), test_state_roundtrip_full_pics() (+1 more)

### Community 27 - "Style Lab & Edit Plan Text"
Cohesion: 0.14
Nodes (9): cut_text(), look_text(), style_library(), style_rules(), write_style_index(), build(), main(), test_library_entries_have_fields() (+1 more)

### Community 28 - "Captions & TTS"
Cohesion: 0.16
Nodes (7): ass_time(), caption_lines(), captions(), styled(), speak(), tts(), ass_colour()

### Community 29 - "AI Calls & Quota Fallback (2)"
Cohesion: 0.16
Nodes (7): ask_brain(), ask_number(), fix_short(), use_picture_from(), paint_new(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 30 - "Picture List Catalog (4)"
Cohesion: 0.20
Nodes (9): contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip(), test_pool_rows_without_thumbs() (+1 more)

### Community 31 - "Style Tests"
Cohesion: 0.19
Nodes (7): apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 32 - "Gemini Image Painting"
Cohesion: 0.15
Nodes (6): ink_silhouette(), make_paper(), paint_instead(), test_ink_silhouette(), test_make_paper(), test_remotion_failure_paints()

### Community 33 - "Story Sounds & Credits (2)"
Cohesion: 0.21
Nodes (6): clock(), quality_check(), review_fixes(), storyboard(), visual_review(), test_review_fix_kinds()

### Community 34 - "AI Calls & Quota Fallback (3)"
Cohesion: 0.18
Nodes (7): rescue_graphics(), apply_review_fixes(), _review_state(), test_auto_fix_graphic(), test_redraw_failure_paints(), test_rescue_respects_caps(), test_review_redraws_custom()

### Community 35 - "Pool Gathering"
Cohesion: 0.18
Nodes (5): gather_pool(), film(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 36 - "Photo Cleanup"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 37 - "Look & Transition Cleaning"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 38 - "AI Calls & Quota Fallback (4)"
Cohesion: 0.18
Nodes (6): rewrite_paint_prompts(), _fake_planning(), ask(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_rewrite_paint_prompts()

### Community 39 - "Picture List Catalog (5)"
Cohesion: 0.20
Nodes (5): fake_ai, planning_ai(), reply(), test_catalog_empty_pool_no_ai(), test_seo_pass_empty_no_ai()

### Community 41 - "Footage Downloads & Crops"
Cohesion: 0.22
Nodes (5): catalog_text(), is_usable(), pictures_of(), usable(), direct_scripts()

### Community 44 - "Story Sounds & Credits (4)"
Cohesion: 0.33
Nodes (3): edit_plan(), picture_line(), test_edit_plan_picture_line()

### Community 45 - "Scene Cues & Word Timing (2)"
Cohesion: 0.40
Nodes (4): story_sound(), test_story_sound_library(), fetch(), _tone_wav()

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `Story Sounds & Credits` to `Entry Point, Logbook & Sounds`, `Channel Profiles & CLI`, `Local AI Jobs & Clips`, `Commons & Archive Sources`, `Python Frame Renderer`, `Scene Cues & Word Timing`, `Footage Downloads & Crops (2)`, `Picture List Catalog (3)`, `Library Candidate Tests`, `Skins & Remotion Render`, `Local AI Jobs & Clips (2)`, `Captions & TTS`, `AI Calls & Quota Fallback (2)`, `Gemini Image Painting`, `Story Sounds & Credits (2)`, `AI Calls & Quota Fallback (3)`, `Photo Cleanup`, `Story Sounds & Credits (3)`, `Story Sounds & Credits (4)`, `Scene Cues & Word Timing (2)`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Should `Style Library Inventions (TS)` be split into smaller, more focused modules?**
  _Cohesion score 0.08951406649616368 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `Picture List Catalog` to `Entry Point, Logbook & Sounds`, `Channel Profiles & CLI`, `Look & Transition Cleaning`, `Local AI Jobs & Clips`, `Commons & Archive Sources`, `AI Calls & Quota Fallback (4)`, `Footage Downloads & Crops`, `Full-Scene Rescue & Plan Cleaning`, `Style Guardrails`, `Picture List Catalog (2)`, `Picture List Catalog (4)`, `Style Tests`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Should `Remotion Short Composition` be split into smaller, more focused modules?**
  _Cohesion score 0.08764568764568764 - nodes in this community are weakly interconnected._
- **Why does `owner()` connect `Test Patching Helper` to `Pool Gathering`, `Channel Profiles & CLI`, `AI Calls & Quota Fallback (4)`, `Picture List Catalog (5)`, `Invention Slots`, `Picture List Catalog (3)`, `Style Tests`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Should `Entry Point, Logbook & Sounds` be split into smaller, more focused modules?**
  _Cohesion score 0.07493061979648474 - nodes in this community are weakly interconnected._
- **Should `Split Script (tools)` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._