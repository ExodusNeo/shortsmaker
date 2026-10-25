# Graph Report - ShortsMaker  (2026-10-26)

## Corpus Check
- 105 files · ~113,611 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .canvas 1, .ipynb 1)

## Summary
- 1526 nodes · 4124 edges · 66 communities (58 shown, 8 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 101 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f156b366`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- clean_full
- toolkit.tsx
- channel_profiles.py
- split_make_shorts.py
- test_full_scenes.py
- test_h3_handoff.py
- full_cues
- Paper
- subprocess
- get_image
- ask_ai
- guarded.tsx
- make
- test_rules.py
- Journey.tsx
- full/types.ts
- catalog_pool
- pool_of
- gen.py
- test_style.py
- test_pictures_first.py
- test_blender_scene.py
- fetch
- planning
- gather_pool
- frame_maker
- edit_plan
- write_scripts
- render
- parts.py
- _fake_planning
- test_blender_plan.py
- templates.py
- render_remotion
- test_story.py
- test_first_second.py
- look.py
- local_clips
- trim_borders
- main
- Short.tsx
- visual_review
- film_piece
- local_voice
- fake_ai
- Halftone.tsx
- json
- ffmpeg
- rewrite_paint_prompts
- re
- build_scene.py
- limit_style
- clean_look
- apply_review_fixes
- rescue_graphics
- use_picture_from
- pictures_of
- paint_instead
- ref_remotion
- test_review_redraws_custom
- logbook_results
- limit_full
- apply_look_scenes
- test_short_credit

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

## Communities (66 total, 8 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "clean_full"
Cohesion: 0.16
Nodes (12): clean_full(), coords(), is_num(), number_figures(), show_number(), test_clean_full_board(), test_clean_full_document(), test_clean_full_journey() (+4 more)

### Community 3 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 4 - "channel_profiles.py"
Cohesion: 0.07
Nodes (26): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+18 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "test_full_scenes.py"
Cohesion: 0.14
Nodes (3): crop_film_bytes(), film_frames(), storyboard()

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.05
Nodes (38): call(), fit_start(), frames(), graph(), main(), saved_file(), h3_problems(), h3_prompt() (+30 more)

### Community 8 - "full_cues"
Cohesion: 0.07
Nodes (21): sfx_events(), scene_cues(), full_props(), full_summary(), full_cues(), spoken_at(), _board(), _jpg() (+13 more)

### Community 9 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 10 - "subprocess"
Cohesion: 0.08
Nodes (9): music_gain(), hex_rgb(), luminance(), shot_span(), fills_frame(), duration(), make_paper(), test_make_paper() (+1 more)

### Community 11 - "get_image"
Cohesion: 0.22
Nodes (5): get_image(), openverse_images(), ov_get(), full_pictures(), test_board_pictures_attached()

### Community 12 - "ask_ai"
Cohesion: 0.06
Nodes (27): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx() (+19 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 14 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (36): draft_rules(), load_rules(), min_real_pictures(), parse_rules(), require_rules(), capture_prompts(), ask(), draft_reply() (+28 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 18 - "catalog_pool"
Cohesion: 0.12
Nodes (15): write_json(), catalog_entries(), catalog_pool(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool() (+7 more)

### Community 19 - "pool_of"
Cohesion: 0.19
Nodes (15): clean_pics(), entry(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film(), test_both_mode_reuses_pools(), test_catalog_both_empty_stops_uncached() (+7 more)

### Community 20 - "gen.py"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "test_style.py"
Cohesion: 0.06
Nodes (28): tsc_check(), approve_candidate(), library_menu(), reject_candidate(), save_candidate(), style_library(), style_rules(), write_style_index() (+20 more)

### Community 22 - "test_pictures_first.py"
Cohesion: 0.21
Nodes (14): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+6 more)

### Community 23 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 24 - "fetch"
Cohesion: 0.09
Nodes (15): archive_films(), commons_films(), nasa_films(), pixabay_films(), archive_images(), nasa_images(), nasa_search(), on_topic() (+7 more)

### Community 25 - "planning"
Cohesion: 0.22
Nodes (12): passing(), prepare(), planning, test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), test_dropped_topic_pool_removed(), prepare() (+4 more)

### Community 26 - "gather_pool"
Cohesion: 0.10
Nodes (10): article_images(), commons_search(), thumb_url(), wm_files(), gather_pool(), owner(), film(), stubbed (+2 more)

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (15): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+7 more)

### Community 28 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 29 - "write_scripts"
Cohesion: 0.14
Nodes (14): clean_sound(), limit_sounds(), graphic_low(), word(), clean_graphic(), contains(), fill_money_graphics(), is_person_portrait() (+6 more)

### Community 30 - "render"
Cohesion: 0.10
Nodes (10): make_sfx(), short_credit(), graphics_count(), wants_remotion(), srt(), drawn_choices(), render(), save_state() (+2 more)

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (22): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+14 more)

### Community 32 - "_fake_planning"
Cohesion: 0.22
Nodes (5): _fake_planning(), ask(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting()

### Community 33 - "test_blender_plan.py"
Cohesion: 0.05
Nodes (44): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+36 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "render_remotion"
Cohesion: 0.05
Nodes (32): ass_time(), caption_lines(), captions(), styled(), ass_colour(), short_skin(), render_remotion(), remotion() (+24 more)

### Community 36 - "test_story.py"
Cohesion: 0.06
Nodes (25): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), sentence_groups(), check_twists(), edit_scripts() (+17 more)

### Community 37 - "test_first_second.py"
Cohesion: 0.24
Nodes (12): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once(), test_opener_must_be_a_later_real_picture() (+4 more)

### Community 38 - "look.py"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 39 - "local_clips"
Cohesion: 0.12
Nodes (11): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), motion_prompt(), start_picture_problems(), veo_handoff() (+3 more)

### Community 40 - "trim_borders"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 41 - "main"
Cohesion: 0.17
Nodes (4): main(), Failure, key(), focus_object()

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "visual_review"
Cohesion: 0.15
Nodes (9): clock(), overlay_notes(), quality_check(), review_fixes(), visual_review(), length_plan(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose() (+1 more)

### Community 45 - "local_voice"
Cohesion: 0.28
Nodes (5): local_voice(), split_takes(), spoken_count(), is_loop_short(), test_word_counts_match_the_aligner()

### Community 46 - "fake_ai"
Cohesion: 0.22
Nodes (4): fake_ai, planning_ai(), reply(), test_seo_pass_research_seeds_dict_and_list()

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "json"
Cohesion: 0.08
Nodes (14): align(), main(), studio_speak(), freesound_fetch(), code_version(), comfy_call(), moss_graph(), moss_images() (+6 more)

### Community 49 - "ffmpeg"
Cohesion: 0.15
Nodes (8): speak(), story_sound(), tts(), ffmpeg(), first_second_check(), test_story_sound_library(), fetch(), _tone_wav()

### Community 51 - "re"
Cohesion: 0.20
Nodes (5): log_short(), vault_page(), vault_refresh(), parse_scene_money(), clean_style_code()

### Community 52 - "build_scene.py"
Cohesion: 0.15
Nodes (5): direction(), keyloc(), keyvis(), Shots, radians()

### Community 54 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 55 - "apply_review_fixes"
Cohesion: 0.28
Nodes (4): apply_review_fixes(), paint_new(), pool_pictures(), test_auto_fix_graphic()

### Community 56 - "rescue_graphics"
Cohesion: 0.29
Nodes (4): rescue_graphics(), max_full(), max_full_planned(), test_rescue_respects_caps()

### Community 57 - "use_picture_from"
Cohesion: 0.33
Nodes (3): use_picture_from(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 58 - "pictures_of"
Cohesion: 0.29
Nodes (4): catalog_text(), is_usable(), pictures_of(), usable()

### Community 59 - "paint_instead"
Cohesion: 0.12
Nodes (6): gemini_images(), to_vertical(), ink_silhouette(), paint_instead(), test_ink_silhouette(), test_remotion_failure_paints()

### Community 61 - "test_review_redraws_custom"
Cohesion: 0.40
Nodes (3): _review_state(), test_redraw_failure_paints(), test_review_redraws_custom()

## Knowledge Gaps
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `templates.py`, `look.py`, `json`, `build_scene.py`, `parts.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `channel_profiles.py`, `test_full_scenes.py`, `full_cues`, `subprocess`, `ask_ai`, `make`, `test_style.py`, `test_pictures_first.py`, `frame_maker`, `edit_plan`, `write_scripts`, `test_blender_plan.py`, `render_remotion`, `local_clips`, `trim_borders`, `visual_review`, `local_voice`, `json`, `ffmpeg`, `re`, `apply_review_fixes`, `rescue_graphics`, `paint_instead`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Should `channel_profiles.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06868686868686869 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `clean_full`, `channel_profiles.py`, `test_full_scenes.py`, `ask_ai`, `test_rules.py`, `catalog_pool`, `pool_of`, `test_style.py`, `fetch`, `planning`, `_fake_planning`, `test_blender_plan.py`, `test_story.py`, `visual_review`, `json`, `re`, `limit_style`, `clean_look`, `rescue_graphics`, `pictures_of`, `logbook_results`, `limit_full`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._
- **Should `test_full_scenes.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13836477987421383 - nodes in this community are weakly interconnected._