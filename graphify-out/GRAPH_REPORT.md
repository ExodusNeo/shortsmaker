# Graph Report - ShortsMaker  (2026-10-21)

## Corpus Check
- 85 files · ~83,964 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .canvas 1)

## Summary
- 1066 nodes · 2905 edges · 43 communities (39 shown, 4 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 51 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Picture List Catalog
- Style Library Inventions (TS)
- Remotion Short Composition
- AI Calls & Quota Fallback
- Scene Cues & Word Timing
- Custom Scene Toolkit & Examples
- Split Script (tools)
- Channel Profiles & CLI
- Story Sounds & Credits
- Python Frame Renderer
- Local AI Jobs & Clips
- Style Lab & Edit Plan Text
- Paper & Evidence Board Scenes
- Captions & TTS
- Entry Point, Logbook & Sounds
- Guarded Layout (cards, arrows)
- Map Journey Scene
- Big Number Scene
- Motion Previews & Render Tests
- Commons & Archive Sources
- Full-Scene Rescue & Plan Cleaning
- GPU Worker (gen.py)
- Entry Point, Logbook & Sounds (2)
- Footage Downloads & Crops
- Invention Slots
- Voice Worker (qwen_voice)
- AI Calls & Quota Fallback (2)
- Style Tests
- Quality Check & Script Editing
- Gemini Image Painting
- Skins & Remotion Render
- Footage Downloads & Crops (2)
- Footage Downloads & Crops (3)
- Channel Profiles & CLI (2)
- Photo Cleanup
- Look & Transition Cleaning
- Pool Gathering
- Library Candidate Tests
- Commons & Archive Sources (2)
- Test Patching Helper
- Story Sound Limits
- Style Guardrails
- Remotion Decision

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
- `test_session_shared()` --calls--> `ask_ai()`  [EXTRACTED]
  tests/test_package.py → shortsmaker/llm.py
- `test_rescue_respects_caps()` --calls--> `rescue_graphics()`  [EXTRACTED]
  tests/test_full_scenes.py → shortsmaker/picker.py

## Import Cycles
- None detected.

## Communities (43 total, 4 thin omitted)

### Community 0 - "Picture List Catalog"
Cohesion: 0.06
Nodes (57): write_json(), catalog_entries(), catalog_pool(), clean_pics(), is_usable(), pool_folder(), prepare_topic(), save_pool() (+49 more)

### Community 1 - "Style Library Inventions (TS)"
Cohesion: 0.09
Nodes (45): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01() (+37 more)

### Community 2 - "Remotion Short Composition"
Cohesion: 0.09
Nodes (50): Captions(), card, clamp, DotGrid(), MarkCard(), Props, StatCard(), TimelineCard() (+42 more)

### Community 3 - "AI Calls & Quota Fallback"
Cohesion: 0.05
Nodes (27): use_picture_from(), clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom() (+19 more)

### Community 4 - "Scene Cues & Word Timing"
Cohesion: 0.05
Nodes (31): sfx_events(), short_skin(), scene_cues(), full_props(), full_summary(), full_cues(), limit_full(), spoken_at() (+23 more)

### Community 5 - "Custom Scene Toolkit & Examples"
Cohesion: 0.18
Nodes (23): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+15 more)

### Community 6 - "Split Script (tools)"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 7 - "Channel Profiles & CLI"
Cohesion: 0.13
Nodes (6): hex_rgb(), luminance(), crop_film_bytes(), film_frames(), mark_details(), make_paper()

### Community 8 - "Story Sounds & Credits"
Cohesion: 0.07
Nodes (20): story_sound(), cut_text(), edit_plan(), look_text(), picture_line(), short_credit(), clock(), ffmpeg() (+12 more)

### Community 9 - "Python Frame Renderer"
Cohesion: 0.09
Nodes (15): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+7 more)

### Community 10 - "Local AI Jobs & Clips"
Cohesion: 0.09
Nodes (14): pixabay_films(), comfy_call(), cover_crop(), gemini_images(), local_clips(), local_job(), local_voice(), moss_graph() (+6 more)

### Community 11 - "Style Lab & Edit Plan Text"
Cohesion: 0.12
Nodes (14): freesound_fetch(), approve_candidate(), clean_style_code(), invent_component(), invent_styles(), library_menu(), reject_candidate(), save_candidate() (+6 more)

### Community 12 - "Paper & Evidence Board Scenes"
Cohesion: 0.15
Nodes (25): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+17 more)

### Community 13 - "Captions & TTS"
Cohesion: 0.10
Nodes (10): ass_time(), caption_lines(), captions(), styled(), make_sfx(), music_gain(), speak(), tts() (+2 more)

### Community 14 - "Entry Point, Logbook & Sounds"
Cohesion: 0.14
Nodes (12): load_channel(), pick_channel(), use_channel(), fix_short(), main(), log_short(), logbook_results(), vault_page() (+4 more)

### Community 15 - "Guarded Layout (cards, arrows)"
Cohesion: 0.14
Nodes (17): Box, boxAt(), clamp, fitCard(), hits(), layoutColumn(), layoutGrid(), layoutRow() (+9 more)

### Community 16 - "Map Journey Scene"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "Big Number Scene"
Cohesion: 0.16
Nodes (18): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), gridFor(), FullScene() (+10 more)

### Community 18 - "Motion Previews & Render Tests"
Cohesion: 0.13
Nodes (5): main(), props_for(), build(), main(), test_session_shared()

### Community 19 - "Commons & Archive Sources"
Cohesion: 0.13
Nodes (8): commons_films(), article_images(), commons_search(), credit_tag_image(), thumb_url(), usable_license(), wm_files(), wm_get()

### Community 20 - "Full-Scene Rescue & Plan Cleaning"
Cohesion: 0.14
Nodes (15): clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number() (+7 more)

### Community 21 - "GPU Worker (gen.py)"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 22 - "Entry Point, Logbook & Sounds (2)"
Cohesion: 0.14
Nodes (10): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), new_channel(), save_channel(), seed_ideas() (+2 more)

### Community 23 - "Footage Downloads & Crops"
Cohesion: 0.13
Nodes (8): choose_images(), catalog_text(), contact_sheets(), load_pool(), pictures_of(), prune_cache(), apply_look_scenes(), test_apply_look_scenes()

### Community 24 - "Invention Slots"
Cohesion: 0.13
Nodes (14): attempt(), lint_style_code(), restore_style_slots(), style_placeholders(), test_candidate_names_unique_across_kinds(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback() (+6 more)

### Community 25 - "Voice Worker (qwen_voice)"
Cohesion: 0.16
Nodes (8): align(), align_words(), main(), say_number(), studio_speak(), test_caption_words_keep_what_is_written(), test_every_aligned_word_is_in_the_aligner_alphabet(), test_numbers()

### Community 26 - "AI Calls & Quota Fallback (2)"
Cohesion: 0.18
Nodes (6): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), rewrite_paint_prompts(), test_quota_fallback_both_ways()

### Community 27 - "Style Tests"
Cohesion: 0.18
Nodes (8): plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics(), test_library_entries_have_fields(), test_save_candidate_unique_slug(), test_style_sounds()

### Community 28 - "Quality Check & Script Editing"
Cohesion: 0.22
Nodes (6): article_text(), edit_scripts(), fact_check(), length_plan(), narration_lines(), write_scripts()

### Community 29 - "Gemini Image Painting"
Cohesion: 0.15
Nodes (5): to_vertical(), ink_silhouette(), paint_instead(), test_ink_silhouette(), test_remotion_failure_paints()

### Community 30 - "Skins & Remotion Render"
Cohesion: 0.17
Nodes (8): render_remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain(), test_swap_inventions()

### Community 31 - "Footage Downloads & Crops (2)"
Cohesion: 0.20
Nodes (5): film_piece(), shot_span(), film_ffmpeg(), duration(), tsc_check()

### Community 32 - "Footage Downloads & Crops (3)"
Cohesion: 0.23
Nodes (7): archive_films(), nasa_films(), archive_images(), nasa_images(), nasa_search(), on_topic(), fetch()

### Community 34 - "Photo Cleanup"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 35 - "Look & Transition Cleaning"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 36 - "Pool Gathering"
Cohesion: 0.24
Nodes (5): gather_pool(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits(), test_pool_roundtrip()

### Community 37 - "Library Candidate Tests"
Cohesion: 0.29
Nodes (7): candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_reject_deletes()

### Community 38 - "Commons & Archive Sources (2)"
Cohesion: 0.22
Nodes (5): get_image(), openverse_images(), ov_get(), full_pictures(), test_board_pictures_attached()

### Community 40 - "Story Sound Limits"
Cohesion: 0.29
Nodes (5): clean_sound(), limit_sounds(), words_of(), test_clean_sound(), test_clean_full_keeps_board_pic()

## Knowledge Gaps
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `Story Sounds & Credits` to `Channel Profiles & CLI (2)`, `Photo Cleanup`, `AI Calls & Quota Fallback`, `Scene Cues & Word Timing`, `Channel Profiles & CLI`, `Python Frame Renderer`, `Local AI Jobs & Clips`, `Remotion Decision`, `Style Lab & Edit Plan Text`, `Captions & TTS`, `Entry Point, Logbook & Sounds`, `Motion Previews & Render Tests`, `Footage Downloads & Crops`, `Gemini Image Painting`, `Skins & Remotion Render`, `Footage Downloads & Crops (2)`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Should `Picture List Catalog` be split into smaller, more focused modules?**
  _Cohesion score 0.055364314400458976 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `Quality Check & Script Editing` to `Picture List Catalog`, `Look & Transition Cleaning`, `Scene Cues & Word Timing`, `AI Calls & Quota Fallback`, `Story Sound Limits`, `Style Guardrails`, `Style Lab & Edit Plan Text`, `Entry Point, Logbook & Sounds`, `Motion Previews & Render Tests`, `Full-Scene Rescue & Plan Cleaning`, `Entry Point, Logbook & Sounds (2)`, `Footage Downloads & Crops`, `AI Calls & Quota Fallback (2)`, `Style Tests`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Should `Style Library Inventions (TS)` be split into smaller, more focused modules?**
  _Cohesion score 0.08951406649616368 - nodes in this community are weakly interconnected._
- **Why does `test_failed_invention_keeps_the_others()` connect `Invention Slots` to `Style Tests`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Should `Remotion Short Composition` be split into smaller, more focused modules?**
  _Cohesion score 0.08764568764568764 - nodes in this community are weakly interconnected._
- **Should `AI Calls & Quota Fallback` be split into smaller, more focused modules?**
  _Cohesion score 0.05061224489795919 - nodes in this community are weakly interconnected._