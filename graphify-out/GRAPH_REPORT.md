# Graph Report - ShortsMaker  (2026-10-27)

## Corpus Check
- 105 files · ~114,305 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .canvas 1, .ipynb 1)

## Summary
- 1530 nodes · 4133 edges · 72 communities (63 shown, 9 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 101 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c6e00880`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Short.tsx
- shutil
- skinOf
- test_package.py
- split_make_shorts.py
- gpu.py
- test_h3_handoff.py
- scene_cues
- toolkit.tsx
- frame_render.py
- local_clips
- blender_plan.py
- guarded.tsx
- Shotcut Timeline and Loudness
- test_rules.py
- Journey.tsx
- full/types.ts
- catalog_pool
- write_scripts
- Local GPU Worker
- clean_look
- math
- test_blender_scene.py
- render_remotion
- test_blender_plan.py
- audio_mix.py
- ClipReader
- Root.tsx
- clean_full
- srt
- parts.py
- drawn_thumbnail
- test_blender_render.py
- templates.py
- style_placeholders
- align_words
- test_first_second.py
- Blender Ink Look
- invent_component
- trim_borders
- main
- style.test.ts
- re
- words_of
- test_local_job_retries_a_hard_crash
- style_library
- kit.ts
- image_sources.py
- test_pictures_first.py
- edit_plan
- json
- build_scene.py
- Style Library Caps
- _fake_planning
- use_picture_from
- full_props
- choose_images
- sfx_events
- test_full_scenes.py
- write_frames
- test_style.py
- owner
- vault_page
- random
- clean_pics
- credit_tag_image
- fake_ai
- captions
- rescue_graphics
- limit_full
- drawn_choices

## God Nodes (most connected - your core abstractions)
1. `render()` - 61 edges
2. `write_scripts()` - 44 edges
3. `ask_ai()` - 36 edges
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

## Communities (72 total, 9 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.11
Nodes (22): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CLAMP, clamp01(), H (+14 more)

### Community 1 - "Short.tsx"
Cohesion: 0.12
Nodes (37): Captions(), card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard() (+29 more)

### Community 2 - "shutil"
Cohesion: 0.11
Nodes (14): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), graphics_count(), lint_custom_code(), look_and_fix(), preview_custom() (+6 more)

### Community 3 - "skinOf"
Cohesion: 0.25
Nodes (20): CustomScene(), ExampleChain(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear() (+12 more)

### Community 4 - "test_package.py"
Cohesion: 0.10
Nodes (15): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), mark_details(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high() (+7 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.06
Nodes (38): call(), fit_start(), frames(), graph(), main(), saved_file(), h3_problems(), h3_prompt() (+30 more)

### Community 8 - "scene_cues"
Cohesion: 0.13
Nodes (11): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish() (+3 more)

### Community 9 - "toolkit.tsx"
Cohesion: 0.13
Nodes (28): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+20 more)

### Community 10 - "frame_render.py"
Cohesion: 0.17
Nodes (7): fills_frame(), fit_font(), frame_maker(), graphic_overlay(), person_card(), thumbnail(), fallback_graphic()

### Community 11 - "local_clips"
Cohesion: 0.10
Nodes (13): comfy_call(), cover_crop(), cut_owner_clip(), gemini_images(), h3_prompts(), local_clips(), moss_graph(), moss_images() (+5 more)

### Community 12 - "blender_plan.py"
Cohesion: 0.14
Nodes (7): default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order(), test_thumbnail_order_skips_film_and_puts_openers_first()

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (20): ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard(), hits() (+12 more)

### Community 14 - "Shotcut Timeline and Loudness"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (37): load_rules(), min_real_pictures(), parse_rules(), require_rules(), capture_prompts(), ask(), draft_reply(), make() (+29 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.16
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "full/types.ts"
Cohesion: 0.18
Nodes (16): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+8 more)

### Community 18 - "catalog_pool"
Cohesion: 0.14
Nodes (13): write_json(), catalog_entries(), catalog_pool(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool() (+5 more)

### Community 19 - "write_scripts"
Cohesion: 0.20
Nodes (14): write_scripts(), passing(), prepare(), planning, test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), test_dropped_topic_pool_removed() (+6 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 22 - "math"
Cohesion: 0.25
Nodes (3): radians(), make_sfx(), clamp()

### Community 23 - "test_blender_scene.py"
Cohesion: 0.05
Nodes (37): check_twists(), edit_scripts(), narration_lines(), story_problems(), build(), add(), main(), changed() (+29 more)

### Community 24 - "render_remotion"
Cohesion: 0.18
Nodes (8): short_skin(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain()

### Community 25 - "test_blender_plan.py"
Cohesion: 0.25
Nodes (14): clean_build(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults(), test_clean_build_keeps_a_good_plan(), test_default_build_shape(), test_label_is_short_and_upper(), test_nan_and_infinity_get_defaults() (+6 more)

### Community 26 - "audio_mix.py"
Cohesion: 0.11
Nodes (9): align(), main(), clean_sound(), freesound_fetch(), speak(), tts(), pixabay_films(), prune_cache() (+1 more)

### Community 27 - "ClipReader"
Cohesion: 0.18
Nodes (5): ClipReader, draw_card(), draw_graphic(), frame(), shot()

### Community 29 - "clean_full"
Cohesion: 0.13
Nodes (16): clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number() (+8 more)

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (23): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+15 more)

### Community 32 - "drawn_thumbnail"
Cohesion: 0.19
Nodes (10): drawn_thumbnail(), load_state(), save_state(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+2 more)

### Community 33 - "test_blender_render.py"
Cohesion: 0.13
Nodes (16): BlenderFailed, code_version(), peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short() (+8 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "style_placeholders"
Cohesion: 0.15
Nodes (12): attempt(), lint_style_code(), restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_lint_failure_uses_fallback(), test_invention_passes_into_slot() (+4 more)

### Community 36 - "align_words"
Cohesion: 0.13
Nodes (11): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak(), test_caption_word_counts_match_the_scene_splitter(), test_caption_words_keep_what_is_written() (+3 more)

### Community 37 - "test_first_second.py"
Cohesion: 0.16
Nodes (15): logbook_results(), swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples(), test_low_score_opens_on_a_better_real_picture() (+7 more)

### Community 38 - "Blender Ink Look"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 39 - "invent_component"
Cohesion: 0.17
Nodes (7): invent_component(), invent_styles(), style_preview(), style_rules(), swap_inventions(), test_invention_compile_failure_uses_fallback(), test_swap_inventions()

### Community 40 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

### Community 41 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 42 - "style.test.ts"
Cohesion: 0.18
Nodes (12): Background(), flashAlpha(), GraphicFor(), Short(), has(), lookFor(), overlayFor(), transitionFor() (+4 more)

### Community 43 - "re"
Cohesion: 0.05
Nodes (35): music_gain(), story_sound(), film_piece(), shot_span(), local_job(), local_voice(), sentence_groups(), split_takes() (+27 more)

### Community 44 - "words_of"
Cohesion: 0.19
Nodes (8): limit_sounds(), graphic_low(), fill_money_graphics(), is_person_portrait(), words_of(), test_clean_sound(), test_fill_money_graphics_and_caps(), test_clean_full_keeps_board_pic()

### Community 46 - "style_library"
Cohesion: 0.13
Nodes (15): approve_candidate(), library_menu(), reject_candidate(), style_library(), write_style_index(), candidate_in(), library_snapshot(), restore_library() (+7 more)

### Community 47 - "kit.ts"
Cohesion: 0.19
Nodes (23): CAPTION_TOP, drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "image_sources.py"
Cohesion: 0.07
Nodes (21): commons_films(), film_frames(), nasa_films(), archive_images(), article_images(), commons_search(), film_ffmpeg(), get_image() (+13 more)

### Community 49 - "test_pictures_first.py"
Cohesion: 0.25
Nodes (16): entry(), film(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film(), test_both_mode_reuses_pools(), test_catalog_both_empty_stops_uncached() (+8 more)

### Community 50 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 51 - "json"
Cohesion: 0.06
Nodes (30): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+22 more)

### Community 52 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 54 - "_fake_planning"
Cohesion: 0.17
Nodes (6): _fake_planning(), ask(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 55 - "use_picture_from"
Cohesion: 0.33
Nodes (3): use_picture_from(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 56 - "full_props"
Cohesion: 0.22
Nodes (7): full_props(), full_summary(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_full_summary(), test_remotion_props_full()

### Community 57 - "choose_images"
Cohesion: 0.23
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 58 - "sfx_events"
Cohesion: 0.22
Nodes (6): sfx_events(), full_pictures(), _board(), test_board_pictures_attached(), test_sfx_full(), test_story_sound_wins_its_moment()

### Community 59 - "test_full_scenes.py"
Cohesion: 0.09
Nodes (14): _review_state(), test_auto_fix_graphic(), test_ink_silhouette(), test_make_paper(), test_music_gain_evens_out_tracks(), test_quota_fallback_both_ways(), test_redraw_failure_paints(), test_remotion_failure_paints() (+6 more)

### Community 60 - "write_frames"
Cohesion: 0.29
Nodes (3): flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 61 - "test_style.py"
Cohesion: 0.12
Nodes (11): wants_remotion(), apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics() (+3 more)

### Community 62 - "owner"
Cohesion: 0.14
Nodes (4): owner(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 64 - "random"
Cohesion: 0.25
Nodes (4): hex_rgb(), luminance(), ink_silhouette(), make_paper()

### Community 65 - "clean_pics"
Cohesion: 0.17
Nodes (6): catalog_text(), clean_pics(), is_usable(), pictures_of(), usable(), direct_scripts()

### Community 67 - "fake_ai"
Cohesion: 0.20
Nodes (5): fake_ai, planning_ai(), reply(), test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list()

### Community 68 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 69 - "rescue_graphics"
Cohesion: 0.25
Nodes (5): rescue_graphics(), article_text(), fact_check(), test_fact_check_drops_full(), test_rescue_respects_caps()

## Knowledge Gaps
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `templates.py`, `Blender Ink Look`, `json`, `build_scene.py`, `parts.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.10960960960960961 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `re` to `shutil`, `test_package.py`, `gpu.py`, `scene_cues`, `frame_render.py`, `local_clips`, `Shotcut Timeline and Loudness`, `math`, `render_remotion`, `audio_mix.py`, `srt`, `drawn_thumbnail`, `test_blender_render.py`, `words_of`, `image_sources.py`, `edit_plan`, `json`, `full_props`, `choose_images`, `sfx_events`, `write_frames`, `test_style.py`, `random`, `captions`, `rescue_graphics`, `drawn_choices`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Should `Short.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `shutil`, `test_package.py`, `gpu.py`, `blender_plan.py`, `test_rules.py`, `catalog_pool`, `clean_look`, `test_blender_scene.py`, `audio_mix.py`, `clean_full`, `test_first_second.py`, `re`, `words_of`, `test_pictures_first.py`, `json`, `Style Library Caps`, `_fake_planning`, `test_style.py`, `clean_pics`, `rescue_graphics`, `limit_full`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Should `shutil` be split into smaller, more focused modules?**
  _Cohesion score 0.11494252873563218 - nodes in this community are weakly interconnected._
- **Should `test_package.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10317460317460317 - nodes in this community are weakly interconnected._