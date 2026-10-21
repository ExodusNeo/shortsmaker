# Graph Report - ShortsMaker  (2026-10-21)

## Corpus Check
- 86 files · ~85,232 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .canvas 1)

## Summary
- 1083 nodes · 2954 edges · 52 communities (45 shown, 7 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 51 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Style Library Inventions (TS)
- Remotion Short Composition
- AI Calls & Quota Fallback
- Custom Scene Toolkit & Examples
- Split Script (tools)
- Channel Profiles & CLI
- Footage Downloads & Crops (2)
- Channel Profiles & CLI (2)
- Entry Point, Logbook & Sounds
- AI Calls & Quota Fallback (4)
- Captions & TTS
- Paper & Evidence Board Scenes
- Local AI Jobs & Clips
- Full-Scene Rescue & Plan Cleaning
- Picture List Catalog (2)
- Python Frame Renderer
- Guarded Layout (cards, arrows)
- Footage Downloads & Crops
- Story Sounds & Credits (2)
- Local AI Jobs & Clips (2)
- Map Journey Scene
- Big Number Scene
- Picture List Catalog
- Look & Transition Cleaning
- GPU Worker (gen.py)
- Library Candidate Tests
- Invention Slots
- Invention Slots (2)
- Picture List Catalog (3)
- Voice Worker (qwen_voice)
- Skins & Remotion Render
- Entry Point, Logbook & Sounds (2)
- Pool Gathering
- Picture List Catalog (2) (2)
- Scene Cues & Word Timing
- Scene Cues & Word Timing (2)
- Python Frame Renderer (2)
- Photo Cleanup
- Picture List Catalog (5)
- Story Sounds & Credits (4)
- Scene Cues & Word Timing (3)
- Commons & Archive Sources
- Gemini Image Painting
- Style Tests
- AI Calls & Quota Fallback (2)
- Full-Scene Rescue & Plan Cleaning (2)
- Style Guardrails
- Story Sounds & Credits (3)
- Picture List Catalog (2)
- Story Sounds & Credits
- Style Tests (2)
- Scene Cues & Word Timing (3)

## God Nodes (most connected - your core abstractions)
1. `render()` - 54 edges
2. `write_scripts()` - 37 edges
3. `skinOf()` - 29 edges
4. `Paper()` - 25 edges
5. `ask_ai()` - 25 edges
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
- `test_rescue_respects_caps()` --calls--> `rescue_graphics()`  [EXTRACTED]
  tests/test_full_scenes.py → shortsmaker/picker.py

## Import Cycles
- None detected.

## Communities (52 total, 7 thin omitted)

### Community 0 - "Style Library Inventions (TS)"
Cohesion: 0.09
Nodes (45): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01() (+37 more)

### Community 1 - "Remotion Short Composition"
Cohesion: 0.09
Nodes (50): Captions(), card, clamp, DotGrid(), MarkCard(), Props, StatCard(), TimelineCard() (+42 more)

### Community 2 - "AI Calls & Quota Fallback"
Cohesion: 0.05
Nodes (26): seed_ideas(), ask_ai(), gemini_model(), quota_exhausted(), run_agy(), clean_tsx_code(), code_custom_scenes(), custom_rules() (+18 more)

### Community 3 - "Custom Scene Toolkit & Examples"
Cohesion: 0.18
Nodes (23): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+15 more)

### Community 4 - "Split Script (tools)"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "Footage Downloads & Crops (2)"
Cohesion: 0.11
Nodes (14): shot_span(), cover_crop(), local_clips(), local_job(), local_voice(), motion_prompt(), veo_handoff(), voicestudio_unload() (+6 more)

### Community 7 - "Channel Profiles & CLI (2)"
Cohesion: 0.10
Nodes (12): fix_short(), hex_rgb(), luminance(), gemini_images(), to_vertical(), paint_instead(), first_second_check(), load_state() (+4 more)

### Community 8 - "Entry Point, Logbook & Sounds"
Cohesion: 0.09
Nodes (17): studio_speak(), ask_count(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel(), save_channel() (+9 more)

### Community 9 - "AI Calls & Quota Fallback (4)"
Cohesion: 0.08
Nodes (17): _fake_planning(), ask(), _review_state(), test_auto_fix_graphic(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_music_gain_evens_out_tracks(), test_redraw_failure_paints() (+9 more)

### Community 10 - "Captions & TTS"
Cohesion: 0.10
Nodes (11): ass_time(), caption_lines(), captions(), styled(), freesound_fetch(), make_sfx(), music_gain(), speak() (+3 more)

### Community 11 - "Paper & Evidence Board Scenes"
Cohesion: 0.15
Nodes (25): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+17 more)

### Community 12 - "Local AI Jobs & Clips"
Cohesion: 0.11
Nodes (13): archive_films(), commons_films(), nasa_films(), archive_images(), get_image(), nasa_images(), nasa_search(), on_topic() (+5 more)

### Community 13 - "Full-Scene Rescue & Plan Cleaning"
Cohesion: 0.12
Nodes (18): clean_full(), word(), clean_graphic(), contains(), coords(), fallback_graphic(), is_num(), number_figures() (+10 more)

### Community 14 - "Picture List Catalog (2)"
Cohesion: 0.19
Nodes (19): clean_pics(), save_pool(), entry(), film(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film() (+11 more)

### Community 15 - "Python Frame Renderer"
Cohesion: 0.10
Nodes (10): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame(), graphic_overlay(), person_card() (+2 more)

### Community 16 - "Guarded Layout (cards, arrows)"
Cohesion: 0.14
Nodes (17): Box, boxAt(), clamp, fitCard(), hits(), layoutColumn(), layoutGrid(), layoutRow() (+9 more)

### Community 17 - "Footage Downloads & Crops"
Cohesion: 0.12
Nodes (12): catalog_text(), is_usable(), load_pool(), pictures_of(), pool_folder(), prepare_topic(), prune_cache(), usable() (+4 more)

### Community 18 - "Story Sounds & Credits (2)"
Cohesion: 0.10
Nodes (11): clock(), rescue_graphics(), apply_review_fixes(), paint_new(), quality_check(), review_fixes(), rewrite_paint_prompts(), storyboard() (+3 more)

### Community 19 - "Local AI Jobs & Clips (2)"
Cohesion: 0.12
Nodes (8): crop_film_bytes(), film_frames(), film_piece(), pixabay_films(), comfy_call(), moss_graph(), moss_images(), film_ffmpeg()

### Community 20 - "Map Journey Scene"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 21 - "Big Number Scene"
Cohesion: 0.16
Nodes (18): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), gridFor(), FullScene() (+10 more)

### Community 22 - "Picture List Catalog"
Cohesion: 0.15
Nodes (16): edit_scripts(), length_plan(), narration_lines(), write_scripts(), passing(), prepare(), planning, test_all_weak_returns_empty() (+8 more)

### Community 23 - "Look & Transition Cleaning"
Cohesion: 0.12
Nodes (13): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), write_style_index(), build(), main() (+5 more)

### Community 24 - "GPU Worker (gen.py)"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 25 - "Library Candidate Tests"
Cohesion: 0.20
Nodes (11): save_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_candidate_names_unique_across_kinds() (+3 more)

### Community 26 - "Invention Slots"
Cohesion: 0.17
Nodes (8): approve_candidate(), clean_style_code(), invent_component(), invent_styles(), library_menu(), reject_candidate(), style_preview(), style_rules()

### Community 27 - "Invention Slots (2)"
Cohesion: 0.14
Nodes (13): attempt(), lint_style_code(), restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback(), test_invention_lint_failure_uses_fallback() (+5 more)

### Community 28 - "Picture List Catalog (3)"
Cohesion: 0.25
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 29 - "Voice Worker (qwen_voice)"
Cohesion: 0.19
Nodes (7): align(), align_words(), main(), say_number(), test_caption_words_keep_what_is_written(), test_every_aligned_word_is_in_the_aligner_alphabet(), test_numbers()

### Community 30 - "Skins & Remotion Render"
Cohesion: 0.14
Nodes (9): short_skin(), render_remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain() (+1 more)

### Community 31 - "Entry Point, Logbook & Sounds (2)"
Cohesion: 0.22
Nodes (10): logbook_results(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once() (+2 more)

### Community 32 - "Pool Gathering"
Cohesion: 0.15
Nodes (5): gather_pool(), owner(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 33 - "Picture List Catalog (2) (2)"
Cohesion: 0.14
Nodes (5): write_json(), catalog_entries(), catalog_pool(), contact_sheets(), test_catalog_failure_stops()

### Community 34 - "Scene Cues & Word Timing"
Cohesion: 0.16
Nodes (8): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish()

### Community 35 - "Scene Cues & Word Timing (2)"
Cohesion: 0.18
Nodes (7): sfx_events(), full_pictures(), _board(), test_board_pictures_attached(), test_sfx_full(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 36 - "Python Frame Renderer (2)"
Cohesion: 0.20
Nodes (5): fills_frame(), frame_maker(), graphic_low(), thumbnail(), credit_tag_image()

### Community 37 - "Photo Cleanup"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 38 - "Picture List Catalog (5)"
Cohesion: 0.20
Nodes (5): fake_ai, planning_ai(), reply(), test_catalog_empty_pool_no_ai(), test_seo_pass_empty_no_ai()

### Community 39 - "Story Sounds & Credits (4)"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 40 - "Scene Cues & Word Timing (3)"
Cohesion: 0.22
Nodes (7): full_props(), full_summary(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_full_summary(), test_remotion_props_full()

### Community 41 - "Commons & Archive Sources"
Cohesion: 0.22
Nodes (5): article_images(), commons_search(), thumb_url(), usable_license(), wm_files()

### Community 42 - "Gemini Image Painting"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 43 - "Style Tests"
Cohesion: 0.29
Nodes (5): plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 44 - "AI Calls & Quota Fallback (2)"
Cohesion: 0.33
Nodes (3): use_picture_from(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 45 - "Full-Scene Rescue & Plan Cleaning (2)"
Cohesion: 0.40
Nodes (3): clean_sound(), limit_sounds(), test_clean_sound()

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `Channel Profiles & CLI (2)` to `AI Calls & Quota Fallback`, `Footage Downloads & Crops (2)`, `Entry Point, Logbook & Sounds`, `Captions & TTS`, `Local AI Jobs & Clips`, `Python Frame Renderer`, `Story Sounds & Credits (2)`, `Local AI Jobs & Clips (2)`, `Library Candidate Tests`, `Picture List Catalog (3)`, `Skins & Remotion Render`, `Scene Cues & Word Timing`, `Scene Cues & Word Timing (2)`, `Python Frame Renderer (2)`, `Photo Cleanup`, `Story Sounds & Credits (4)`, `Scene Cues & Word Timing (3)`, `Gemini Image Painting`, `Story Sounds & Credits (3)`, `Story Sounds & Credits`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Should `Style Library Inventions (TS)` be split into smaller, more focused modules?**
  _Cohesion score 0.08951406649616368 - nodes in this community are weakly interconnected._
- **Why does `owner()` connect `Pool Gathering` to `Picture List Catalog (2) (2)`, `Picture List Catalog (5)`, `AI Calls & Quota Fallback (4)`, `Style Tests`, `Picture List Catalog (2)`, `Library Candidate Tests`, `Invention Slots (2)`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Should `Remotion Short Composition` be split into smaller, more focused modules?**
  _Cohesion score 0.08764568764568764 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `Picture List Catalog` to `AI Calls & Quota Fallback`, `Channel Profiles & CLI`, `Channel Profiles & CLI (2)`, `Entry Point, Logbook & Sounds`, `AI Calls & Quota Fallback (4)`, `Style Tests`, `Full-Scene Rescue & Plan Cleaning (2)`, `Picture List Catalog (2)`, `Full-Scene Rescue & Plan Cleaning`, `Picture List Catalog (2)`, `Footage Downloads & Crops`, `Style Guardrails`, `Look & Transition Cleaning`, `Entry Point, Logbook & Sounds (2)`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Should `AI Calls & Quota Fallback` be split into smaller, more focused modules?**
  _Cohesion score 0.052525252525252523 - nodes in this community are weakly interconnected._
- **Should `Split Script (tools)` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._