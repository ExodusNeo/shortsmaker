# Graph Report - ShortsMaker  (2026-10-22)

## Corpus Check
- 91 files · ~90,736 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .canvas 1)

## Summary
- 1181 nodes · 3231 edges · 58 communities (51 shown, 7 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 59 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `940b0d5b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- clean_full
- skinOf
- re
- split_make_shorts.py
- test_full_scenes.py
- subprocess
- full_cues
- toolkit.tsx
- audio_mix.py
- fetch
- ask_ai
- guarded.tsx
- make
- test_rules.py
- Journey.tsx
- full/types.ts
- prepare_topic
- test_pictures_first.py
- gen.py
- style_library
- choose_images
- use_picture_from
- json
- write_scripts
- owner
- frame_maker
- invent_component
- test_package.py
- render
- ffmpeg
- apply_review_fixes
- render_remotion
- test_style.py
- style_placeholders
- qwen_voice.py
- run_check
- edit_plan
- local_clips
- clean_photo
- clean_look
- Short.tsx
- edit_scripts
- film_frames
- clean_pics
- planning_ai
- Halftone.tsx
- wm_files
- captions
- gather_pool
- words_of
- film_piece
- limit_style
- catalog_entries
- srt
- paint_instead
- test_short_credit

## God Nodes (most connected - your core abstractions)
1. `render()` - 56 edges
2. `write_scripts()` - 38 edges
3. `ask_ai()` - 30 edges
4. `skinOf()` - 29 edges
5. `Paper()` - 25 edges
6. `main()` - 24 edges
7. `choose_images()` - 22 edges
8. `clean_full()` - 21 edges
9. `style_library()` - 20 edges
10. `pool_of()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `test_numbers()` --calls--> `say_number()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_word_counts_match_the_scene_splitter()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_words_keep_what_is_written()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_every_aligned_word_is_in_the_aligner_alphabet()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_min_pictures_from_settings()` --calls--> `prepare_topic()`  [EXTRACTED]
  tests/test_rules.py → shortsmaker/picture_pool.py

## Import Cycles
- None detected.

## Communities (58 total, 7 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.17
Nodes (29): card, clamp, DotGrid(), MarkCard(), Props, StatCard(), TimelineCard(), clamp (+21 more)

### Community 2 - "clean_full"
Cohesion: 0.14
Nodes (15): clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number() (+7 more)

### Community 3 - "skinOf"
Cohesion: 0.18
Nodes (23): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+15 more)

### Community 4 - "re"
Cohesion: 0.06
Nodes (27): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+19 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "test_full_scenes.py"
Cohesion: 0.13
Nodes (4): person_card(), tsc_check(), library_menu(), reject_candidate()

### Community 7 - "subprocess"
Cohesion: 0.18
Nodes (5): music_gain(), master_gain(), main(), props_for(), test_music_gain_evens_out_tracks()

### Community 8 - "full_cues"
Cohesion: 0.06
Nodes (22): sfx_events(), scene_cues(), full_props(), full_summary(), full_pictures(), full_cues(), spoken_at(), spoken_span() (+14 more)

### Community 9 - "toolkit.tsx"
Cohesion: 0.15
Nodes (25): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+17 more)

### Community 10 - "audio_mix.py"
Cohesion: 0.11
Nodes (9): clean_sound(), freesound_fetch(), limit_sounds(), make_sfx(), hex_rgb(), luminance(), make_paper(), test_clean_sound() (+1 more)

### Community 11 - "fetch"
Cohesion: 0.32
Nodes (5): nasa_films(), get_image(), nasa_search(), ov_get(), fetch()

### Community 12 - "ask_ai"
Cohesion: 0.05
Nodes (27): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx() (+19 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.14
Nodes (17): Box, boxAt(), clamp, fitCard(), hits(), layoutColumn(), layoutGrid(), layoutRow() (+9 more)

### Community 14 - "make"
Cohesion: 0.15
Nodes (8): caption_layer(), make(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers(), videos()

### Community 15 - "test_rules.py"
Cohesion: 0.10
Nodes (28): rewrite_paint_prompts(), min_real_pictures(), parse_rules(), test_rewrite_paint_prompts(), capture_prompts(), ask(), draft_reply(), make() (+20 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "full/types.ts"
Cohesion: 0.16
Nodes (18): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), gridFor(), FullScene() (+10 more)

### Community 18 - "prepare_topic"
Cohesion: 0.20
Nodes (8): write_json(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_pool_roundtrip(), test_pool_rows_without_thumbs()

### Community 19 - "test_pictures_first.py"
Cohesion: 0.17
Nodes (21): catalog_pool(), entry(), fake_ai, film(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film() (+13 more)

### Community 20 - "gen.py"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.12
Nodes (15): cut_text(), look_text(), approve_candidate(), style_library(), write_style_index(), direct_scripts(), candidate_in(), library_snapshot() (+7 more)

### Community 22 - "choose_images"
Cohesion: 0.25
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 23 - "use_picture_from"
Cohesion: 0.29
Nodes (4): use_picture_from(), paint_new(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 24 - "json"
Cohesion: 0.10
Nodes (9): crop_film_bytes(), pixabay_films(), comfy_call(), moss_graph(), moss_images(), voicestudio_unload(), voicestudio_up(), search_suggestions() (+1 more)

### Community 25 - "write_scripts"
Cohesion: 0.16
Nodes (16): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position() (+8 more)

### Community 26 - "owner"
Cohesion: 0.15
Nodes (6): owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (15): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+7 more)

### Community 28 - "invent_component"
Cohesion: 0.16
Nodes (8): invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), style_rules(), test_invention_lint_failure_uses_fallback(), test_placeholders_match_the_slots()

### Community 29 - "test_package.py"
Cohesion: 0.08
Nodes (8): sentence_groups(), story_problems(), build(), add(), main(), scenes(), test_sentences_running_across_cuts_are_one_take(), test_story_problems()

### Community 30 - "render"
Cohesion: 0.12
Nodes (13): short_credit(), clock(), graphics_count(), first_second_check(), quality_check(), review_fixes(), storyboard(), visual_review() (+5 more)

### Community 31 - "ffmpeg"
Cohesion: 0.24
Nodes (8): story_sound(), split_takes(), duration(), ffmpeg(), test_story_sound_library(), fetch(), _tone_wav(), test_a_take_is_cut_between_the_scenes_words()

### Community 32 - "apply_review_fixes"
Cohesion: 0.11
Nodes (11): rescue_graphics(), apply_review_fixes(), pool_pictures(), ask(), _review_state(), test_auto_fix_graphic(), test_look_check_fixes_code(), test_redraw_failure_paints() (+3 more)

### Community 33 - "render_remotion"
Cohesion: 0.13
Nodes (11): short_skin(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_clean_full_custom_and_skin() (+3 more)

### Community 34 - "test_style.py"
Cohesion: 0.14
Nodes (10): wants_remotion(), apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics() (+2 more)

### Community 35 - "style_placeholders"
Cohesion: 0.19
Nodes (10): restore_style_slots(), style_placeholders(), test_candidate_names_unique_across_kinds(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run() (+2 more)

### Community 36 - "qwen_voice.py"
Cohesion: 0.13
Nodes (11): align(), align_words(), main(), say_number(), studio_speak(), spoken_count(), test_caption_word_counts_match_the_scene_splitter(), test_caption_words_keep_what_is_written() (+3 more)

### Community 37 - "run_check"
Cohesion: 0.22
Nodes (9): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once(), test_opener_must_be_a_later_real_picture() (+1 more)

### Community 38 - "edit_plan"
Cohesion: 0.33
Nodes (3): edit_plan(), picture_line(), test_edit_plan_picture_line()

### Community 39 - "local_clips"
Cohesion: 0.15
Nodes (9): cover_crop(), local_clips(), local_job(), local_voice(), motion_prompt(), veo_handoff(), video_encoder(), test_local_job_retries_a_hard_crash() (+1 more)

### Community 40 - "clean_photo"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 41 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 42 - "Short.tsx"
Cohesion: 0.12
Nodes (21): Captions(), HookTitle(), PersonCard(), Root(), Background(), Card, flashAlpha(), GraphicFor() (+13 more)

### Community 43 - "edit_scripts"
Cohesion: 0.25
Nodes (4): edit_scripts(), length_plan(), narration_lines(), test_editor_gets_one_second_pass_for_broken_rules()

### Community 45 - "clean_pics"
Cohesion: 0.20
Nodes (5): catalog_text(), clean_pics(), is_usable(), pictures_of(), usable()

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "wm_files"
Cohesion: 0.20
Nodes (6): commons_films(), commons_search(), thumb_url(), usable_license(), wm_files(), wm_get()

### Community 49 - "captions"
Cohesion: 0.16
Nodes (7): ass_time(), caption_lines(), captions(), styled(), speak(), tts(), ass_colour()

### Community 50 - "gather_pool"
Cohesion: 0.20
Nodes (4): article_images(), nasa_images(), openverse_images(), gather_pool()

### Community 51 - "words_of"
Cohesion: 0.28
Nodes (5): archive_films(), archive_images(), on_topic(), words_of(), test_clean_full_keeps_board_pic()

### Community 59 - "paint_instead"
Cohesion: 0.12
Nodes (6): gemini_images(), to_vertical(), ink_silhouette(), paint_instead(), test_ink_silhouette(), test_remotion_failure_paints()

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `re`, `test_full_scenes.py`, `subprocess`, `full_cues`, `audio_mix.py`, `ask_ai`, `make`, `choose_images`, `json`, `frame_maker`, `ffmpeg`, `apply_review_fixes`, `render_remotion`, `test_style.py`, `edit_plan`, `local_clips`, `clean_photo`, `captions`, `srt`, `paint_instead`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.1282051282051282 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `clean_full`, `test_style.py`, `re`, `test_full_scenes.py`, `clean_look`, `audio_mix.py`, `edit_scripts`, `ask_ai`, `clean_pics`, `test_rules.py`, `prepare_topic`, `words_of`, `test_pictures_first.py`, `limit_style`, `style_library`, `json`, `owner`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Should `clean_full` be split into smaller, more focused modules?**
  _Cohesion score 0.1368421052631579 - nodes in this community are weakly interconnected._
- **Why does `clean_photo()` connect `clean_photo` to `test_full_scenes.py`, `render`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Should `re` be split into smaller, more focused modules?**
  _Cohesion score 0.06274509803921569 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._