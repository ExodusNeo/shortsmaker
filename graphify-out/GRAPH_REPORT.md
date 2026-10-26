# Graph Report - ShortsMaker  (2026-10-26)

## Corpus Check
- 105 files · ~113,746 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .canvas 1, .ipynb 1)

## Summary
- 1527 nodes · 4126 edges · 62 communities (57 shown, 5 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 101 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1cee3720`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- ask_ai
- toolkit.tsx
- json
- split_make_shorts.py
- test_h3_handoff.py
- full_cues
- Paper
- subprocess
- h3_run.py
- code_custom_scenes
- guarded.tsx
- Shotcut Timeline and Loudness
- test_rules.py
- Journey.tsx
- BigNumber.tsx
- choose_images
- test_pictures_first.py
- Local GPU Worker
- style_library
- math
- Blender Scene Tests
- gather_pool
- test_blender_plan.py
- audio_mix.py
- frame_maker
- Edit Plan Text
- write_scripts
- render
- parts.py
- drawn_thumbnail
- test_blender_render.py
- templates.py
- render_remotion
- time
- test_first_second.py
- Blender Ink Look
- AI Clip Prompts and Cuts
- trim_borders
- main
- Short.tsx
- visual_review
- blender_plan.py
- local_voice
- fact_check
- Invented Look Canvas Effects
- gpu.py
- ffmpeg
- default_build
- re
- build_scene.py
- Style Library Caps
- check_twists
- fix_short
- BlenderFailed
- edit_scripts
- Gemini Image Painting
- Full Graphic Limits
- short_render.py
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

## Communities (62 total, 5 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "ask_ai"
Cohesion: 0.10
Nodes (15): new_channel(), seed_ideas(), ask_ai(), gemini_model(), quota_exhausted(), run_agy(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash() (+7 more)

### Community 3 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 4 - "json"
Cohesion: 0.13
Nodes (11): freesound_fetch(), channel_url(), load_channel(), save_channel(), trend_research(), yt_list(), logbook_results(), write_json() (+3 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (32): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_closeup_marked_scenes_skip_pause(), test_all_start_pictures_flagged_skips_pause() (+24 more)

### Community 8 - "full_cues"
Cohesion: 0.06
Nodes (22): sfx_events(), scene_cues(), full_props(), full_summary(), full_cues(), spoken_at(), spoken_span(), _board() (+14 more)

### Community 9 - "Paper"
Cohesion: 0.13
Nodes (28): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+20 more)

### Community 10 - "subprocess"
Cohesion: 0.12
Nodes (6): tsc_check(), storyboard(), reject_candidate(), main(), props_for(), test_reject_deletes()

### Community 11 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 12 - "code_custom_scenes"
Cohesion: 0.06
Nodes (21): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+13 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 14 - "Shotcut Timeline and Loudness"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.05
Nodes (49): ask_brain(), ask_count(), ask_yes(), pick_channel(), use_channel(), main(), log_short(), vault_page() (+41 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "BigNumber.tsx"
Cohesion: 0.20
Nodes (14): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+6 more)

### Community 18 - "choose_images"
Cohesion: 0.10
Nodes (13): get_image(), choose_images(), full_pictures(), catalog_entries(), catalog_pool(), contact_sheets(), load_pool(), pool_folder() (+5 more)

### Community 19 - "test_pictures_first.py"
Cohesion: 0.05
Nodes (60): catalog_text(), clean_pics(), is_usable(), save_pool(), usable(), owner(), entry(), fake_ai (+52 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.09
Nodes (21): clean_invention(), clean_look(), clean_transition(), settle_style(), approve_candidate(), save_candidate(), style_library(), write_style_index() (+13 more)

### Community 22 - "math"
Cohesion: 0.13
Nodes (6): radians(), make_sfx(), clamp(), flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 23 - "Blender Scene Tests"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 24 - "gather_pool"
Cohesion: 0.08
Nodes (18): archive_films(), commons_films(), nasa_films(), pixabay_films(), archive_images(), article_images(), commons_search(), nasa_images() (+10 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.30
Nodes (12): clean_build(), plan(), test_a_failure_in_scene_one_becomes_the_hook(), test_bad_values_get_defaults(), test_clean_build_keeps_a_good_plan(), test_default_build_shape(), test_label_is_short_and_upper(), test_nan_and_infinity_get_defaults() (+4 more)

### Community 26 - "audio_mix.py"
Cohesion: 0.22
Nodes (4): music_gain(), speak(), tts(), test_music_gain_evens_out_tracks()

### Community 27 - "frame_maker"
Cohesion: 0.08
Nodes (13): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), frame_maker(), frame(), graphic_overlay() (+5 more)

### Community 28 - "Edit Plan Text"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 29 - "write_scripts"
Cohesion: 0.09
Nodes (25): clean_sound(), limit_sounds(), graphic_low(), clean_full(), word(), clean_graphic(), contains(), coords() (+17 more)

### Community 30 - "render"
Cohesion: 0.12
Nodes (11): short_credit(), graphics_count(), wants_remotion(), srt(), drawn_choices(), load_state(), render(), save_state() (+3 more)

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (23): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+15 more)

### Community 32 - "drawn_thumbnail"
Cohesion: 0.23
Nodes (9): scene_frames(), drawn_thumbnail(), test_scene_frames_cover_every_frame_once(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 33 - "test_blender_render.py"
Cohesion: 0.22
Nodes (12): peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises(), test_frames_are_trimmed_after_the_clips_are_cut() (+4 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "render_remotion"
Cohesion: 0.06
Nodes (31): ass_time(), caption_lines(), captions(), styled(), ass_colour(), render_remotion(), remotion(), render() (+23 more)

### Community 36 - "time"
Cohesion: 0.08
Nodes (19): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+11 more)

### Community 37 - "test_first_second.py"
Cohesion: 0.22
Nodes (12): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once(), test_opener_must_be_a_later_real_picture() (+4 more)

### Community 38 - "Blender Ink Look"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 39 - "AI Clip Prompts and Cuts"
Cohesion: 0.12
Nodes (11): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), motion_prompt(), start_picture_problems(), veo_handoff() (+3 more)

### Community 40 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

### Community 41 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 42 - "Short.tsx"
Cohesion: 0.13
Nodes (19): Captions(), PersonCard(), Root(), Background(), flashAlpha(), GraphicFor(), Move, Scene (+11 more)

### Community 43 - "visual_review"
Cohesion: 0.18
Nodes (8): clock(), overlay_notes(), quality_check(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 44 - "blender_plan.py"
Cohesion: 0.20
Nodes (5): ending(), panels(), pick(), thumbnail_order(), test_thumbnail_order_skips_film_and_puts_openers_first()

### Community 45 - "local_voice"
Cohesion: 0.22
Nodes (5): local_voice(), sentence_groups(), voicestudio_unload(), is_loop_short(), test_sentences_running_across_cuts_are_one_take()

### Community 46 - "fact_check"
Cohesion: 0.20
Nodes (7): fact_check(), test_fact_check_drops_full(), plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 47 - "Invented Look Canvas Effects"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "gpu.py"
Cohesion: 0.08
Nodes (10): code_version(), crop_film_bytes(), film_frames(), film_piece(), shot_span(), comfy_call(), moss_graph(), moss_images() (+2 more)

### Community 49 - "ffmpeg"
Cohesion: 0.16
Nodes (12): story_sound(), split_takes(), duration(), ffmpeg(), build(), add(), main(), test_story_sound_library() (+4 more)

### Community 50 - "default_build"
Cohesion: 0.29
Nodes (4): default_build(), plan_builds(), test_plan_builds_retries_then_defaults(), ask()

### Community 51 - "re"
Cohesion: 0.14
Nodes (7): mark_details(), parse_scene_money(), max_full(), max_full_planned(), clean_style_code(), story_problems(), test_story_problems()

### Community 52 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 54 - "check_twists"
Cohesion: 0.47
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 55 - "fix_short"
Cohesion: 0.08
Nodes (16): ask_number(), fix_short(), use_picture_from(), rescue_graphics(), redraw_custom(), apply_review_fixes(), paint_new(), rewrite_paint_prompts() (+8 more)

### Community 58 - "edit_scripts"
Cohesion: 0.15
Nodes (7): pictures_of(), direct_scripts(), edit_scripts(), length_plan(), narration_lines(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules()

### Community 59 - "Gemini Image Painting"
Cohesion: 0.12
Nodes (6): gemini_images(), to_vertical(), ink_silhouette(), paint_instead(), test_ink_silhouette(), test_remotion_failure_paints()

### Community 64 - "short_render.py"
Cohesion: 0.12
Nodes (8): hex_rgb(), luminance(), short_skin(), make_paper(), apply_look_scenes(), test_clean_full_custom_and_skin(), test_make_paper(), test_apply_look_scenes()

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `templates.py`, `json`, `Blender Ink Look`, `build_scene.py`, `parts.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12802275960170698 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `full_cues`, `subprocess`, `Shotcut Timeline and Loudness`, `test_rules.py`, `choose_images`, `style_library`, `math`, `audio_mix.py`, `frame_maker`, `Edit Plan Text`, `write_scripts`, `drawn_thumbnail`, `test_blender_render.py`, `render_remotion`, `AI Clip Prompts and Cuts`, `visual_review`, `local_voice`, `gpu.py`, `ffmpeg`, `re`, `fix_short`, `Gemini Image Painting`, `short_render.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `ask_ai`, `json`, `test_full_scenes.py`, `subprocess`, `code_custom_scenes`, `fact_check`, `test_rules.py`, `default_build`, `re`, `test_pictures_first.py`, `choose_images`, `style_library`, `Style Library Caps`, `check_twists`, `edit_scripts`, `Full Graphic Limits`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.10144927536231885 - nodes in this community are weakly interconnected._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.1286549707602339 - nodes in this community are weakly interconnected._