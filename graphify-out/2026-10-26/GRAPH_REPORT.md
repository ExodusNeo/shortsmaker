# Graph Report - ShortsMaker  (2026-10-26)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1526 nodes · 4124 edges · 66 communities (58 shown, 8 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 101 edges (avg confidence: 0.85)
- Token cost: 69,368 input · 935 output

## Graph Freshness
- Built from commit: `f156b366`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Invented Overlays and Looks
- Remotion Caption Cards
- Full-Screen Graphic Validation
- Custom Remotion Scenes
- Main Entry and Channel Profiles
- Script Splitting AST Tools
- CLI, Config and Footage
- MiniMax H3 Video Jobs
- Sound Design and Scene Cues
- Board and Document Scenes
- Audio Mix and Shotcut Export
- Openverse and Museum Images
- Headless AI Planner Calls
- Example Chain and Evidence
- Shotcut Timeline and Loudness
- Channel Rules Files
- Map Journey Scene
- Big Number Full Scenes
- Picture Pool Storage
- Director Picture Cleanup Tests
- Local GPU Worker
- Motion Scenes and Style Library
- Pictures-First Pool Tests
- Blender Scene Tests
- Stock Video Sources
- Topic Planning Tests
- Wikimedia Image Search
- Frame Drawing and Graphics
- Edit Plan Text
- Script Sounds and Graphics
- Sound Effects and Credits
- Blender Bridge Parts
- Write Scripts Review Tests
- Blender Build Planning
- Bridge Templates
- ASS Captions and Skins
- Narration Number Speech
- First-Second Opener Check
- Blender Ink Look
- AI Clip Prompts and Cuts
- Archive Photo Cleanup
- Bridge Collapse Simulation
- Short Composition Root
- Quality and Visual Review
- Film Clip Downloads
- Local Voice Alignment
- Fake AI Test Helpers
- Invented Look Canvas Effects
- Local Voice and Freesound
- TTS and Story Sounds
- Repaint Prompt Rewrites
- Obsidian Vault Logbook
- Blender Camera Shots
- Style Library Caps
- Style Plan Validation
- Review Auto-Fixes
- Graphics Rescue Caps
- Picture Swap Fixes
- Usable Picture Catalog
- Gemini Image Painting
- Remotion Root Entry
- Custom Scene Redraw Tests
- Logbook Results
- Full Graphic Limits
- Photo Look Application
- Short Credit Tags

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
- `test_pixabay_keeps_only_on_topic_videos()` --calls--> `pixabay_films()`  [EXTRACTED]
  tests/test_pictures_first.py → shortsmaker/footage.py
- `test_caption_word_counts_match_the_scene_splitter()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_words_keep_what_is_written()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_every_aligned_word_is_in_the_aligner_alphabet()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_numbers()` --calls--> `say_number()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`

## Communities (66 total, 8 thin omitted)

### Community 0 - "Invented Overlays and Looks"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Remotion Caption Cards"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "Full-Screen Graphic Validation"
Cohesion: 0.16
Nodes (12): clean_full(), coords(), is_num(), number_figures(), show_number(), test_clean_full_board(), test_clean_full_document(), test_clean_full_journey() (+4 more)

### Community 3 - "Custom Remotion Scenes"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 4 - "Main Entry and Channel Profiles"
Cohesion: 0.07
Nodes (26): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+18 more)

### Community 5 - "Script Splitting AST Tools"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "CLI, Config and Footage"
Cohesion: 0.14
Nodes (3): crop_film_bytes(), film_frames(), storyboard()

### Community 7 - "MiniMax H3 Video Jobs"
Cohesion: 0.05
Nodes (38): call(), fit_start(), frames(), graph(), main(), saved_file(), h3_problems(), h3_prompt() (+30 more)

### Community 8 - "Sound Design and Scene Cues"
Cohesion: 0.07
Nodes (21): sfx_events(), scene_cues(), full_props(), full_summary(), full_cues(), spoken_at(), _board(), _jpg() (+13 more)

### Community 9 - "Board and Document Scenes"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 10 - "Audio Mix and Shotcut Export"
Cohesion: 0.08
Nodes (9): music_gain(), hex_rgb(), luminance(), shot_span(), fills_frame(), duration(), make_paper(), test_make_paper() (+1 more)

### Community 11 - "Openverse and Museum Images"
Cohesion: 0.22
Nodes (5): get_image(), openverse_images(), ov_get(), full_pictures(), test_board_pictures_attached()

### Community 12 - "Headless AI Planner Calls"
Cohesion: 0.06
Nodes (27): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx() (+19 more)

### Community 13 - "Example Chain and Evidence"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 14 - "Shotcut Timeline and Loudness"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "Channel Rules Files"
Cohesion: 0.08
Nodes (36): draft_rules(), load_rules(), min_real_pictures(), parse_rules(), require_rules(), capture_prompts(), ask(), draft_reply() (+28 more)

### Community 16 - "Map Journey Scene"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "Big Number Full Scenes"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 18 - "Picture Pool Storage"
Cohesion: 0.12
Nodes (15): write_json(), catalog_entries(), catalog_pool(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool() (+7 more)

### Community 19 - "Director Picture Cleanup Tests"
Cohesion: 0.19
Nodes (15): clean_pics(), entry(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film(), test_both_mode_reuses_pools(), test_catalog_both_empty_stops_uncached() (+7 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "Motion Scenes and Style Library"
Cohesion: 0.06
Nodes (28): tsc_check(), approve_candidate(), library_menu(), reject_candidate(), save_candidate(), style_library(), style_rules(), write_style_index() (+20 more)

### Community 22 - "Pictures-First Pool Tests"
Cohesion: 0.21
Nodes (14): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+6 more)

### Community 23 - "Blender Scene Tests"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 24 - "Stock Video Sources"
Cohesion: 0.09
Nodes (15): archive_films(), commons_films(), nasa_films(), pixabay_films(), archive_images(), nasa_images(), nasa_search(), on_topic() (+7 more)

### Community 25 - "Topic Planning Tests"
Cohesion: 0.22
Nodes (12): passing(), prepare(), planning, test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), test_dropped_topic_pool_removed(), prepare() (+4 more)

### Community 26 - "Wikimedia Image Search"
Cohesion: 0.10
Nodes (10): article_images(), commons_search(), thumb_url(), wm_files(), gather_pool(), owner(), film(), stubbed (+2 more)

### Community 27 - "Frame Drawing and Graphics"
Cohesion: 0.07
Nodes (15): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+7 more)

### Community 28 - "Edit Plan Text"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 29 - "Script Sounds and Graphics"
Cohesion: 0.14
Nodes (14): clean_sound(), limit_sounds(), graphic_low(), word(), clean_graphic(), contains(), fill_money_graphics(), is_person_portrait() (+6 more)

### Community 30 - "Sound Effects and Credits"
Cohesion: 0.10
Nodes (10): make_sfx(), short_credit(), graphics_count(), wants_remotion(), srt(), drawn_choices(), render(), save_state() (+2 more)

### Community 31 - "Blender Bridge Parts"
Cohesion: 0.15
Nodes (22): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+14 more)

### Community 32 - "Write Scripts Review Tests"
Cohesion: 0.22
Nodes (5): _fake_planning(), ask(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting()

### Community 33 - "Blender Build Planning"
Cohesion: 0.05
Nodes (44): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+36 more)

### Community 34 - "Bridge Templates"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "ASS Captions and Skins"
Cohesion: 0.05
Nodes (32): ass_time(), caption_lines(), captions(), styled(), ass_colour(), short_skin(), render_remotion(), remotion() (+24 more)

### Community 36 - "Narration Number Speech"
Cohesion: 0.06
Nodes (25): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), sentence_groups(), check_twists(), edit_scripts() (+17 more)

### Community 37 - "First-Second Opener Check"
Cohesion: 0.24
Nodes (12): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once(), test_opener_must_be_a_later_real_picture() (+4 more)

### Community 38 - "Blender Ink Look"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 39 - "AI Clip Prompts and Cuts"
Cohesion: 0.12
Nodes (11): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), motion_prompt(), start_picture_problems(), veo_handoff() (+3 more)

### Community 40 - "Archive Photo Cleanup"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 41 - "Bridge Collapse Simulation"
Cohesion: 0.17
Nodes (4): main(), Failure, key(), focus_object()

### Community 42 - "Short Composition Root"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "Quality and Visual Review"
Cohesion: 0.15
Nodes (9): clock(), overlay_notes(), quality_check(), review_fixes(), visual_review(), length_plan(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose() (+1 more)

### Community 45 - "Local Voice Alignment"
Cohesion: 0.28
Nodes (5): local_voice(), split_takes(), spoken_count(), is_loop_short(), test_word_counts_match_the_aligner()

### Community 46 - "Fake AI Test Helpers"
Cohesion: 0.22
Nodes (4): fake_ai, planning_ai(), reply(), test_seo_pass_research_seeds_dict_and_list()

### Community 47 - "Invented Look Canvas Effects"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "Local Voice and Freesound"
Cohesion: 0.08
Nodes (14): align(), main(), studio_speak(), freesound_fetch(), code_version(), comfy_call(), moss_graph(), moss_images() (+6 more)

### Community 49 - "TTS and Story Sounds"
Cohesion: 0.15
Nodes (8): speak(), story_sound(), tts(), ffmpeg(), first_second_check(), test_story_sound_library(), fetch(), _tone_wav()

### Community 51 - "Obsidian Vault Logbook"
Cohesion: 0.20
Nodes (5): log_short(), vault_page(), vault_refresh(), parse_scene_money(), clean_style_code()

### Community 52 - "Blender Camera Shots"
Cohesion: 0.15
Nodes (5): direction(), keyloc(), keyvis(), Shots, radians()

### Community 54 - "Style Plan Validation"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 55 - "Review Auto-Fixes"
Cohesion: 0.28
Nodes (4): apply_review_fixes(), paint_new(), pool_pictures(), test_auto_fix_graphic()

### Community 56 - "Graphics Rescue Caps"
Cohesion: 0.29
Nodes (4): rescue_graphics(), max_full(), max_full_planned(), test_rescue_respects_caps()

### Community 57 - "Picture Swap Fixes"
Cohesion: 0.33
Nodes (3): use_picture_from(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 58 - "Usable Picture Catalog"
Cohesion: 0.29
Nodes (4): catalog_text(), is_usable(), pictures_of(), usable()

### Community 59 - "Gemini Image Painting"
Cohesion: 0.12
Nodes (6): gemini_images(), to_vertical(), ink_silhouette(), paint_instead(), test_ink_silhouette(), test_remotion_failure_paints()

### Community 61 - "Custom Scene Redraw Tests"
Cohesion: 0.40
Nodes (3): _review_state(), test_redraw_failure_paints(), test_review_redraws_custom()

## Knowledge Gaps
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `Bridge Collapse Simulation` to `Bridge Templates`, `Blender Ink Look`, `Local Voice and Freesound`, `Blender Camera Shots`, `Blender Bridge Parts`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Should `Invented Overlays and Looks` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `Sound Effects and Credits` to `Main Entry and Channel Profiles`, `CLI, Config and Footage`, `Sound Design and Scene Cues`, `Audio Mix and Shotcut Export`, `Headless AI Planner Calls`, `Shotcut Timeline and Loudness`, `Motion Scenes and Style Library`, `Pictures-First Pool Tests`, `Frame Drawing and Graphics`, `Edit Plan Text`, `Script Sounds and Graphics`, `Blender Build Planning`, `ASS Captions and Skins`, `AI Clip Prompts and Cuts`, `Archive Photo Cleanup`, `Quality and Visual Review`, `Local Voice Alignment`, `Local Voice and Freesound`, `TTS and Story Sounds`, `Obsidian Vault Logbook`, `Review Auto-Fixes`, `Graphics Rescue Caps`, `Gemini Image Painting`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Should `Main Entry and Channel Profiles` be split into smaller, more focused modules?**
  _Cohesion score 0.06868686868686869 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `Script Sounds and Graphics` to `Full-Screen Graphic Validation`, `Main Entry and Channel Profiles`, `CLI, Config and Footage`, `Headless AI Planner Calls`, `Channel Rules Files`, `Picture Pool Storage`, `Director Picture Cleanup Tests`, `Motion Scenes and Style Library`, `Stock Video Sources`, `Topic Planning Tests`, `Write Scripts Review Tests`, `Blender Build Planning`, `Narration Number Speech`, `Quality and Visual Review`, `Local Voice and Freesound`, `Obsidian Vault Logbook`, `Style Library Caps`, `Style Plan Validation`, `Graphics Rescue Caps`, `Usable Picture Catalog`, `Logbook Results`, `Full Graphic Limits`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Should `Script Splitting AST Tools` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._
- **Should `CLI, Config and Footage` be split into smaller, more focused modules?**
  _Cohesion score 0.13836477987421383 - nodes in this community are weakly interconnected._