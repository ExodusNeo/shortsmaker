# Graph Report - ShortsMaker  (2026-10-31)

## Corpus Check
- 119 files · ~141,478 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 1833 nodes · 4979 edges · 87 communities (74 shown, 13 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 109 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `189c3057`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- h3_run.py
- ask_ai
- split_make_shorts.py
- re
- code_custom_scenes
- film_piece
- guarded.tsx
- k
- test_h3_handoff.py
- test_blender_scene.py
- approve_candidate
- render_remotion
- test_rules.py
- Journey.tsx
- toolkit.tsx
- prepare_topic
- write_scripts
- Local GPU Worker
- core.mjs
- local_clips
- ffmpeg
- makeKit
- test_blender_plan.py
- opener_graphic
- frame_maker
- full_cues
- json
- look.py
- parts.py
- clean_full
- test_full_scenes.py
- templates.py
- gather_pool
- local_voice
- full/types.ts
- main
- Paper
- visual_review
- build_scene.py
- Short.tsx
- textures.mjs
- captions
- test_blender_render.py
- image_sources.py
- Halftone.tsx
- test_topic_ideas.py
- invent_component
- limit_style
- channel_profiles.py
- style_library
- first_second_check
- kit.mjs
- make_opener
- test_blender_run.py
- choose_images
- edit_plan
- clean_pics
- sfx_events
- bean.mjs
- graphic_low
- popS
- apply_review_fixes
- edit_scripts
- ref_remotion
- dexter.mjs
- kit_parts.mjs
- story_problems
- scene_cues
- look_and_fix
- time
- run_agy
- gemini_model
- test_style.py
- paint_instead
- full_props
- limit_full
- check_twists
- music_gain
- BlenderFailed
- peaks
- _run
- mark_details
- render
- test_short_credit

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 65 edges
3. `write_scripts()` - 51 edges
4. `ask_ai()` - 40 edges
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
- `test_fix_bat_explains_a_drawn_short()` --calls--> `fix_short()`  [EXTRACTED]
  tests/test_blender_run.py → shortsmaker/cli.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`

## Communities (87 total, 13 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.15
Nodes (23): catalog_entries(), catalog_pool(), entry(), fake_ai, film(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+15 more)

### Community 3 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 4 - "ask_ai"
Cohesion: 0.17
Nodes (9): ask_ai(), cold_read(), test_quota_fallback_both_ways(), test_claude_pinned_to_opus_high(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash(), test_session_shared(), test_solo_ask_ai_hands_over_when_out_of_credits(), test_solo_ask_ai_never_falls_back() (+1 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "re"
Cohesion: 0.10
Nodes (11): logbook_results(), vault_page(), vault_refresh(), parse_scene_money(), max_full(), max_full_planned(), clean_style_code(), library_menu() (+3 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.15
Nodes (10): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), redraw_custom(), test_code_custom_scenes_fallback(), test_fallback_custom_is_clean() (+2 more)

### Community 8 - "film_piece"
Cohesion: 0.17
Nodes (5): crop_film_bytes(), film_frames(), film_piece(), shot_span(), film_ffmpeg()

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 13 - "approve_candidate"
Cohesion: 0.23
Nodes (9): approve_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_candidate_names_unique_across_kinds() (+1 more)

### Community 14 - "render_remotion"
Cohesion: 0.10
Nodes (13): ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions() (+5 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (39): draft_rules(), load_rules(), min_real_pictures(), parse_rules(), require_rules(), capture_prompts(), ask(), draft_reply() (+31 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 18 - "prepare_topic"
Cohesion: 0.14
Nodes (11): write_json(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_both_mode_reuses_pools(), test_empty_pool_drops_topic_without_ai() (+3 more)

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

### Community 23 - "ffmpeg"
Cohesion: 0.13
Nodes (10): caption_layer(), make(), master_gain(), project_xml(), remove(), ffmpeg(), short_folder(), test_melt_plays_it_with_the_captions_on_top() (+2 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.10
Nodes (22): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+14 more)

### Community 26 - "opener_graphic"
Cohesion: 0.12
Nodes (9): gemini_images(), full_summary(), opener_graphic(), fix_opener_graphic(), paint_opener_start(), weak_opener_graphic(), test_full_props_figure(), test_full_summary() (+1 more)

### Community 27 - "frame_maker"
Cohesion: 0.08
Nodes (12): ClipReader, draw_card(), draw_graphic(), flash_alpha(), frame_maker(), frame(), graphic_overlay(), shot() (+4 more)

### Community 28 - "full_cues"
Cohesion: 0.17
Nodes (7): full_cues(), spoken_at(), spoken_span(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish(), test_opener_graphic()

### Community 29 - "json"
Cohesion: 0.07
Nodes (19): freesound_fetch(), code_version(), available(), clean_code(), fingerprint(), lint(), comfy_call(), moss_graph() (+11 more)

### Community 30 - "look.py"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (22): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+14 more)

### Community 32 - "clean_full"
Cohesion: 0.05
Nodes (32): clean_sound(), limit_sounds(), short_skin(), is_stereo(), trim_borders(), border(), plain(), full_formats() (+24 more)

### Community 33 - "test_full_scenes.py"
Cohesion: 0.09
Nodes (4): hex_rgb(), luminance(), tsc_check(), clean_photo()

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "gather_pool"
Cohesion: 0.09
Nodes (8): gather_pool(), owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits(), test_good_look_check_skips_the_extra_compile()

### Community 36 - "local_voice"
Cohesion: 0.10
Nodes (16): cosy_instruct(), local_voice(), sentence_groups(), split_takes(), spoken_count(), log_short(), duration(), is_loop_short() (+8 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 38 - "main"
Cohesion: 0.17
Nodes (4): main(), Failure, key(), focus_object()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "visual_review"
Cohesion: 0.12
Nodes (11): clock(), overlay_notes(), quality_check(), review_fixes(), storyboard(), visual_review(), max_seconds(), test_review_is_told_the_drawings_are_deliberate() (+3 more)

### Community 41 - "build_scene.py"
Cohesion: 0.15
Nodes (5): direction(), keyloc(), keyvis(), Shots, radians()

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "textures.mjs"
Cohesion: 0.25
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "captions"
Cohesion: 0.12
Nodes (11): ass_time(), caption_lines(), captions(), styled(), speak(), story_sound(), tts(), ass_colour() (+3 more)

### Community 45 - "test_blender_render.py"
Cohesion: 0.28
Nodes (11): render_clips(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises(), test_frames_are_trimmed_after_the_clips_are_cut(), test_missing_blender_raises() (+3 more)

### Community 46 - "image_sources.py"
Cohesion: 0.09
Nodes (18): archive_films(), commons_films(), nasa_films(), pixabay_films(), archive_images(), article_images(), commons_search(), get_image() (+10 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "test_topic_ideas.py"
Cohesion: 0.10
Nodes (15): search_suggestions(), seo_pass(), clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words() (+7 more)

### Community 49 - "invent_component"
Cohesion: 0.12
Nodes (15): invent_component(), attempt(), invent_styles(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others() (+7 more)

### Community 51 - "channel_profiles.py"
Cohesion: 0.09
Nodes (20): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+12 more)

### Community 52 - "style_library"
Cohesion: 0.13
Nodes (12): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), test_invented_look_needs_fallback() (+4 more)

### Community 53 - "first_second_check"
Cohesion: 0.17
Nodes (13): first_second_check(), swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once() (+5 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 55 - "make_opener"
Cohesion: 0.08
Nodes (17): make_opener(), node_run(), review(), sheet_times(), write(), use_opener(), fake_ai(), look() (+9 more)

### Community 56 - "test_blender_run.py"
Cohesion: 0.22
Nodes (9): drawn_thumbnail(), drawn_short(), jpeg(), test_blender_failure_is_reported_and_the_batch_goes_on(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_fix_bat_explains_a_drawn_short(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 57 - "choose_images"
Cohesion: 0.25
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 58 - "edit_plan"
Cohesion: 0.17
Nodes (6): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 59 - "clean_pics"
Cohesion: 0.17
Nodes (6): catalog_text(), clean_pics(), is_usable(), pictures_of(), usable(), direct_scripts()

### Community 60 - "sfx_events"
Cohesion: 0.18
Nodes (7): sfx_events(), full_pictures(), _board(), test_board_pictures_attached(), test_sfx_full(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "graphic_low"
Cohesion: 0.22
Nodes (5): fills_frame(), fit_font(), graphic_low(), person_card(), thumbnail()

### Community 64 - "apply_review_fixes"
Cohesion: 0.08
Nodes (15): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), rewrite_paint_prompts(), ask(), _review_state(), test_auto_fix_graphic() (+7 more)

### Community 65 - "edit_scripts"
Cohesion: 0.22
Nodes (5): edit_scripts(), length_plan(), narration_lines(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules()

### Community 69 - "story_problems"
Cohesion: 0.24
Nodes (9): first_sentence(), story_problems(), read(), test_cold_read_verdicts(), test_first_sentence_reads_across_the_cut(), test_no_hook_setting_no_hook_check(), test_story_problems(), test_story_problems_flags_summary_hook() (+1 more)

### Community 70 - "scene_cues"
Cohesion: 0.33
Nodes (5): scene_cues(), test_counter_finishes_before_it_leaves(), test_graphic_card_hold_duration(), test_person_card_hold_and_exit_gap(), test_scene_hold_padding()

### Community 71 - "look_and_fix"
Cohesion: 0.38
Nodes (3): look_and_fix(), preview_custom(), preview_sheet()

### Community 72 - "time"
Cohesion: 0.10
Nodes (16): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+8 more)

### Community 73 - "run_agy"
Cohesion: 0.33
Nodes (3): quota_exhausted(), run_agy(), test_run_agy_flags_and_boundaries()

### Community 74 - "gemini_model"
Cohesion: 0.40
Nodes (4): gemini_model(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_gemini_timeout_switches_to_flash()

### Community 75 - "test_style.py"
Cohesion: 0.16
Nodes (9): apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_clean_question_and_kinetic(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics() (+1 more)

### Community 76 - "paint_instead"
Cohesion: 0.25
Nodes (3): to_vertical(), paint_instead(), test_remotion_failure_paints()

### Community 77 - "full_props"
Cohesion: 0.40
Nodes (4): full_props(), _jpg(), test_custom_cues_props_and_pictures(), test_remotion_props_full()

### Community 79 - "check_twists"
Cohesion: 0.47
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 85 - "render"
Cohesion: 0.11
Nodes (9): make_sfx(), short_credit(), graphics_count(), wants_remotion(), srt(), drawn_choices(), render(), test_drawn_choices_have_no_pictures() (+1 more)

## Knowledge Gaps
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `re`, `render_remotion`, `local_clips`, `ffmpeg`, `opener_graphic`, `frame_maker`, `json`, `clean_full`, `test_full_scenes.py`, `local_voice`, `visual_review`, `captions`, `test_blender_render.py`, `channel_profiles.py`, `first_second_check`, `make_opener`, `test_blender_run.py`, `choose_images`, `edit_plan`, `sfx_events`, `graphic_low`, `apply_review_fixes`, `scene_cues`, `paint_instead`, `music_gain`, `mark_details`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `build_scene.py`, `json`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14838709677419354 - nodes in this community are weakly interconnected._
- **Why does `scene_cues()` connect `scene_cues` to `test_full_scenes.py`, `full_cues`, `render`, `graphic_low`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Should `h3_run.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11462450592885376 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._