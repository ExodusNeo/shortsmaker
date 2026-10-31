# Graph Report - ShortsMaker  (2026-10-31)

## Corpus Check
- 119 files · ~139,941 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 1825 nodes · 4960 edges · 81 communities (72 shown, 9 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 109 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2515ca28`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- h3_run.py
- ask_ai
- split_make_shorts.py
- __init__.py
- code_custom_scenes
- fetch
- guarded.tsx
- k
- test_h3_handoff.py
- test_blender_scene.py
- test_style.py
- make_opener
- test_rules.py
- Journey.tsx
- toolkit.tsx
- prepare_topic
- write_scripts
- Local GPU Worker
- core.mjs
- local_clips
- test_edit_project.py
- makeKit
- test_blender_plan.py
- test_weak_opener_graphic_fixes_then_handoff
- frame_maker
- test_full_scenes.py
- json
- build_scene.py
- parts.py
- clean_full
- plan_rules.py
- templates.py
- gather_pool
- ffmpeg
- BigNumber.tsx
- main
- Paper
- visual_review
- Shots
- Short.tsx
- textures.mjs
- music_gain
- fake_ai
- image_sources.py
- Halftone.tsx
- test_topic_ideas.py
- render_remotion
- limit_style
- re
- style_library
- test_first_second.py
- kit.mjs
- review
- trend_research
- choose_images
- words_of
- ask
- make_sfx
- bean.mjs
- state
- popS
- apply_review_fixes
- clean_sound
- subprocess
- dexter.mjs
- kit_parts.mjs
- test_story.py
- use_picture_from
- look_and_fix
- qwen_voice.py
- get_image
- gemini_model
- clean_graphic
- paint_instead
- write
- limit_full
- render
- trim_borders

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 65 edges
3. `write_scripts()` - 51 edges
4. `ask_ai()` - 39 edges
5. `skinOf()` - 29 edges
6. `clamp()` - 27 edges
7. `ellPts()` - 26 edges
8. `main()` - 26 edges
9. `Paper()` - 25 edges
10. `choose_images()` - 24 edges

## Surprising Connections (you probably didn't know these)
- `test_numbers()` --calls--> `say_number()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_word_counts_match_the_scene_splitter()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_words_keep_what_is_written()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_every_aligned_word_is_in_the_aligner_alphabet()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_new_channel_stops_for_review()` --calls--> `pick_channel()`  [EXTRACTED]
  tests/test_rules.py → shortsmaker/channel_profiles.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`

## Communities (81 total, 9 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.13
Nodes (26): write_json(), catalog_entries(), catalog_pool(), clean_pics(), save_pool(), entry(), film(), pic_short() (+18 more)

### Community 3 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 4 - "ask_ai"
Cohesion: 0.15
Nodes (10): ask_ai(), quota_exhausted(), run_agy(), test_quota_fallback_both_ways(), test_claude_pinned_to_opus_high(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash(), test_run_agy_flags_and_boundaries(), test_session_shared() (+2 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.15
Nodes (10): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), redraw_custom(), test_code_custom_scenes_fallback(), test_fallback_custom_is_clean() (+2 more)

### Community 8 - "fetch"
Cohesion: 0.13
Nodes (10): archive_films(), film_frames(), nasa_films(), archive_images(), film_ffmpeg(), nasa_images(), nasa_search(), on_topic() (+2 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 13 - "test_style.py"
Cohesion: 0.13
Nodes (12): approve_candidate(), save_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes() (+4 more)

### Community 14 - "make_opener"
Cohesion: 0.17
Nodes (6): lint(), make_opener(), node_run(), sheet_times(), look(), test_lint()

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (40): draft_rules(), load_rules(), min_real_pictures(), parse_rules(), require_rules(), capture_prompts(), ask(), draft_reply() (+32 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 18 - "prepare_topic"
Cohesion: 0.10
Nodes (12): film_piece(), catalog_text(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), prepare_topic() (+4 more)

### Community 19 - "write_scripts"
Cohesion: 0.13
Nodes (22): write_scripts(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare() (+14 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "local_clips"
Cohesion: 0.12
Nodes (12): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), motion_prompt(), start_picture(), start_picture_problems() (+4 more)

### Community 23 - "test_edit_project.py"
Cohesion: 0.13
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.05
Nodes (43): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+35 more)

### Community 26 - "test_weak_opener_graphic_fixes_then_handoff"
Cohesion: 0.17
Nodes (6): weak_opener_graphic(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), test_weak_opener_graphic_fixes_then_handoff(), use()

### Community 27 - "frame_maker"
Cohesion: 0.06
Nodes (17): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+9 more)

### Community 28 - "test_full_scenes.py"
Cohesion: 0.05
Nodes (33): sfx_events(), scene_cues(), full_props(), full_summary(), full_formats(), full_pictures(), opener_graphic(), rescue_graphics() (+25 more)

### Community 29 - "json"
Cohesion: 0.08
Nodes (16): freesound_fetch(), code_version(), commons_films(), crop_film_bytes(), pixabay_films(), comfy_call(), moss_graph(), moss_images() (+8 more)

### Community 30 - "build_scene.py"
Cohesion: 0.16
Nodes (6): collection(), ink_lines(), linear(), material(), setup(), radians()

### Community 31 - "parts.py"
Cohesion: 0.16
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 32 - "clean_full"
Cohesion: 0.15
Nodes (10): clean_full(), number_figures(), show_number(), test_clean_full_board(), test_clean_full_document(), test_clean_full_journey(), test_clean_full_keeps_thing(), test_clean_full_limits() (+2 more)

### Community 33 - "plan_rules.py"
Cohesion: 0.11
Nodes (6): hex_rgb(), luminance(), short_skin(), make_paper(), test_clean_full_custom_and_skin(), test_make_paper()

### Community 34 - "templates.py"
Cohesion: 0.17
Nodes (15): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge() (+7 more)

### Community 35 - "gather_pool"
Cohesion: 0.12
Nodes (8): gather_pool(), owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits(), test_pool_roundtrip()

### Community 36 - "ffmpeg"
Cohesion: 0.12
Nodes (14): shot_span(), cosy_instruct(), local_voice(), sentence_groups(), split_takes(), spoken_count(), duration(), ffmpeg() (+6 more)

### Community 37 - "BigNumber.tsx"
Cohesion: 0.20
Nodes (14): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+6 more)

### Community 38 - "main"
Cohesion: 0.18
Nodes (4): keyvis(), main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.13
Nodes (28): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+20 more)

### Community 40 - "visual_review"
Cohesion: 0.14
Nodes (10): clock(), overlay_notes(), quality_check(), review_fixes(), visual_review(), max_seconds(), test_review_is_told_the_drawings_are_deliberate(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures() (+2 more)

### Community 41 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.13
Nodes (19): Captions(), PersonCard(), Root(), Background(), flashAlpha(), GraphicFor(), Move, Scene (+11 more)

### Community 43 - "textures.mjs"
Cohesion: 0.25
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "music_gain"
Cohesion: 0.14
Nodes (8): music_gain(), speak(), story_sound(), tts(), test_music_gain_evens_out_tracks(), test_story_sound_library(), fetch(), _tone_wav()

### Community 45 - "fake_ai"
Cohesion: 0.19
Nodes (8): logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel(), test_seo_never_sees_competitor_titles()

### Community 46 - "image_sources.py"
Cohesion: 0.18
Nodes (6): article_images(), commons_search(), thumb_url(), usable_license(), wm_files(), wm_get()

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "test_topic_ideas.py"
Cohesion: 0.15
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 49 - "render_remotion"
Cohesion: 0.05
Nodes (32): ass_time(), caption_lines(), captions(), styled(), ass_colour(), render_remotion(), remotion(), render() (+24 more)

### Community 51 - "re"
Cohesion: 0.08
Nodes (18): ask_brain(), ask_count(), ask_number(), ask_yes(), load_channel(), pick_channel(), use_channel(), fix_short() (+10 more)

### Community 52 - "style_library"
Cohesion: 0.06
Nodes (24): cut_text(), edit_plan(), look_text(), picture_line(), clean_invention(), clean_look(), clean_transition(), settle_style() (+16 more)

### Community 53 - "test_first_second.py"
Cohesion: 0.25
Nodes (6): first_second_check(), run_check(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_must_be_a_later_real_picture(), test_opener_prompt_shows_each_scenes_line_and_picture()

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 55 - "review"
Cohesion: 0.20
Nodes (7): review(), fake_ai(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused(), test_no_verdict_is_not_a_pass(), test_use_opener_plays_the_drawn_opener()

### Community 56 - "trend_research"
Cohesion: 0.20
Nodes (6): channel_url(), new_channel(), save_channel(), seed_ideas(), trend_research(), yt_list()

### Community 57 - "choose_images"
Cohesion: 0.19
Nodes (14): choose_images(), apply_look_scenes(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+6 more)

### Community 58 - "words_of"
Cohesion: 0.24
Nodes (6): fill_money_graphics(), is_person_portrait(), parse_scene_money(), words_of(), test_fill_money_graphics_and_caps(), test_clean_full_keeps_board_pic()

### Community 59 - "ask"
Cohesion: 0.33
Nodes (3): ask(), test_look_check_fixes_code(), test_rewrite_paint_prompts()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "state"
Cohesion: 0.39
Nodes (7): swap_pictures(), real(), state(), test_opener_fix_swaps_once(), test_swap_ignores_a_clip_already_dropped(), test_swap_moves_the_owners_clip_with_its_picture(), test_swap_pictures_trades_real_pictures()

### Community 64 - "apply_review_fixes"
Cohesion: 0.18
Nodes (6): apply_review_fixes(), _review_state(), test_auto_fix_graphic(), test_redraw_failure_paints(), test_review_redraws_custom(), test_review_uses_unused_pool_pictures_before_painting()

### Community 65 - "clean_sound"
Cohesion: 0.29
Nodes (5): clean_sound(), limit_sounds(), word(), contains(), test_clean_sound()

### Community 66 - "subprocess"
Cohesion: 0.13
Nodes (7): available(), fingerprint(), tsc_check(), prune_cache(), prune_work(), main(), props_for()

### Community 69 - "test_story.py"
Cohesion: 0.10
Nodes (18): first_sentence(), check_twists(), edit_scripts(), length_plan(), narration_lines(), story_problems(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules() (+10 more)

### Community 70 - "use_picture_from"
Cohesion: 0.29
Nodes (4): use_picture_from(), paint_new(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 71 - "look_and_fix"
Cohesion: 0.38
Nodes (3): look_and_fix(), preview_custom(), preview_sheet()

### Community 72 - "qwen_voice.py"
Cohesion: 0.13
Nodes (13): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+5 more)

### Community 73 - "get_image"
Cohesion: 0.33
Nodes (3): get_image(), openverse_images(), ov_get()

### Community 74 - "gemini_model"
Cohesion: 0.40
Nodes (4): gemini_model(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_gemini_timeout_switches_to_flash()

### Community 75 - "clean_graphic"
Cohesion: 0.50
Nodes (4): clean_graphic(), coords(), is_num(), test_clean_question_and_kinetic()

### Community 76 - "paint_instead"
Cohesion: 0.12
Nodes (6): gemini_images(), to_vertical(), ink_silhouette(), paint_instead(), test_ink_silhouette(), test_remotion_failure_paints()

### Community 85 - "render"
Cohesion: 0.09
Nodes (14): short_credit(), graphics_count(), mark_details(), wants_remotion(), srt(), drawn_choices(), drawn_thumbnail(), load_state() (+6 more)

### Community 86 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

## Knowledge Gaps
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `test_style.py`, `local_clips`, `test_edit_project.py`, `test_blender_plan.py`, `test_weak_opener_graphic_fixes_then_handoff`, `frame_maker`, `test_full_scenes.py`, `json`, `plan_rules.py`, `ffmpeg`, `visual_review`, `music_gain`, `render_remotion`, `re`, `style_library`, `test_first_second.py`, `choose_images`, `make_sfx`, `apply_review_fixes`, `subprocess`, `paint_instead`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12802275960170698 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `Shots`, `json`, `build_scene.py`, `parts.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._
- **Why does `ClipReader` connect `frame_maker` to `plan_rules.py`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12773109243697478 - nodes in this community are weakly interconnected._
- **Should `h3_run.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11462450592885376 - nodes in this community are weakly interconnected._