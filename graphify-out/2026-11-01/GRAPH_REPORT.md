# Graph Report - ShortsMaker  (2026-10-31)

## Corpus Check
- 129 files · ~148,014 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 1959 nodes · 5382 edges · 92 communities (80 shown, 12 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 119 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `29fb6c0e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- test_style.py
- test_blender_scene.py
- split_make_shorts.py
- json
- code_custom_scenes
- film_piece
- guarded.tsx
- k
- test_h3_handoff.py
- gather_pool
- style_library
- render_remotion
- test_rules.py
- Journey.tsx
- toolkit.tsx
- prepare_topic
- write_scripts
- Local GPU Worker
- core.mjs
- local_clips
- make
- makeKit
- test_blender_plan.py
- render
- frame_maker
- full_cues
- h3_run.py
- look.py
- parts.py
- make_opener
- pathlib
- templates.py
- test_weak_opener_graphic_fixes_then_handoff
- story_problems
- full/types.ts
- main
- Paper
- quality_check
- build_scene.py
- Short.tsx
- textures.mjs
- get_image
- logbook_results
- image_sources.py
- Halftone.tsx
- test_topic_ideas.py
- invent_component
- limit_style
- main
- paint_instead
- test_first_second.py
- kit.mjs
- RetentionTests
- short_render.py
- choose_images
- ReliabilityTests
- apply_review_fixes
- run_agy
- bean.mjs
- ffmpeg
- popS
- log_short
- edit_scripts
- visual_review
- dexter.mjs
- kit_parts.mjs
- rewrite_paint_prompts
- full_props
- clean_full
- qwen_voice.py
- ask_ai
- re
- speak
- test_full_scenes.py
- captions
- ref_remotion
- edit_plan
- resume_runs
- cold_read_line
- test_ai_modes.py
- owner
- test_story.py
- make_paper
- clean_pics
- MarkTests
- finish_render
- wants_remotion
- command
- test_review_redraws_custom

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 55 edges
3. `write_scripts()` - 51 edges
4. `ask_ai()` - 47 edges
5. `main()` - 31 edges
6. `skinOf()` - 29 edges
7. `clamp()` - 27 edges
8. `ellPts()` - 26 edges
9. `Paper()` - 25 edges
10. `choose_images()` - 25 edges

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

## Communities (92 total, 12 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.13
Nodes (25): catalog_entries(), catalog_pool(), entry(), fake_ai, film(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+17 more)

### Community 3 - "test_style.py"
Cohesion: 0.15
Nodes (14): candidate_in(), library_snapshot(), plan_with(), ask(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes() (+6 more)

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "json"
Cohesion: 0.07
Nodes (20): freesound_fetch(), code_version(), available(), clean_code(), fingerprint(), lint(), node_run(), comfy_call() (+12 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.13
Nodes (12): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), redraw_custom() (+4 more)

### Community 8 - "film_piece"
Cohesion: 0.25
Nodes (3): film_piece(), shot_span(), film_ffmpeg()

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "gather_pool"
Cohesion: 0.22
Nodes (4): gather_pool(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 13 - "style_library"
Cohesion: 0.13
Nodes (12): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), test_invented_look_needs_fallback() (+4 more)

### Community 14 - "render_remotion"
Cohesion: 0.12
Nodes (12): short_skin(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), invent_styles(), style_props(), swap_inventions() (+4 more)

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (37): load_rules(), min_real_pictures(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft() (+29 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 18 - "prepare_topic"
Cohesion: 0.20
Nodes (9): contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip(), test_pool_rows_without_thumbs() (+1 more)

### Community 19 - "write_scripts"
Cohesion: 0.11
Nodes (24): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+16 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "local_clips"
Cohesion: 0.10
Nodes (14): cosy_instruct(), cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt() (+6 more)

### Community 23 - "make"
Cohesion: 0.15
Nodes (8): make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers(), videos()

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.05
Nodes (44): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+36 more)

### Community 26 - "render"
Cohesion: 0.08
Nodes (13): make_sfx(), gemini_images(), short_credit(), full_summary(), graphics_count(), opener_graphic(), fix_opener_graphic(), paint_opener_start() (+5 more)

### Community 27 - "frame_maker"
Cohesion: 0.06
Nodes (17): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+9 more)

### Community 28 - "full_cues"
Cohesion: 0.12
Nodes (12): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish() (+4 more)

### Community 29 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 30 - "look.py"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (23): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+15 more)

### Community 32 - "make_opener"
Cohesion: 0.11
Nodes (11): make_opener(), review(), sheet_times(), write(), fake_ai(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused() (+3 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "test_weak_opener_graphic_fixes_then_handoff"
Cohesion: 0.14
Nodes (7): weak_opener_graphic(), use_opener(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), test_weak_opener_graphic_fixes_then_handoff(), use()

### Community 36 - "story_problems"
Cohesion: 0.24
Nodes (9): first_sentence(), story_problems(), read(), test_cold_read_verdicts(), test_first_sentence_reads_across_the_cut(), test_no_hook_setting_no_hook_check(), test_story_problems(), test_story_problems_flags_summary_hook() (+1 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "quality_check"
Cohesion: 0.25
Nodes (4): quality_check(), length_plan(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "textures.mjs"
Cohesion: 0.25
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "get_image"
Cohesion: 0.12
Nodes (10): sfx_events(), get_image(), openverse_images(), ov_get(), full_pictures(), _board(), test_board_pictures_attached(), test_sfx_full() (+2 more)

### Community 46 - "image_sources.py"
Cohesion: 0.09
Nodes (16): archive_films(), commons_films(), nasa_films(), pixabay_films(), archive_images(), article_images(), commons_search(), nasa_images() (+8 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "test_topic_ideas.py"
Cohesion: 0.15
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 49 - "invent_component"
Cohesion: 0.13
Nodes (15): invent_component(), attempt(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile() (+7 more)

### Community 51 - "main"
Cohesion: 0.10
Nodes (17): ask_count(), ask_yes(), load_channel(), pick_channel(), use_channel(), fix_short(), main(), draft_rules() (+9 more)

### Community 52 - "paint_instead"
Cohesion: 0.25
Nodes (3): to_vertical(), paint_instead(), test_remotion_failure_paints()

### Community 53 - "test_first_second.py"
Cohesion: 0.18
Nodes (14): first_second_check(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture() (+6 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "short_render.py"
Cohesion: 0.08
Nodes (13): music_gain(), hex_rgb(), luminance(), voicestudio_up(), preview_sheet(), tsc_check(), prune_cache(), preview() (+5 more)

### Community 57 - "choose_images"
Cohesion: 0.16
Nodes (15): choose_images(), download_picture(), recover_downloads(), is_person_portrait(), picking, planned_short(), scene(), still() (+7 more)

### Community 59 - "apply_review_fixes"
Cohesion: 0.18
Nodes (7): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "ffmpeg"
Cohesion: 0.13
Nodes (14): caption_layer(), sentence_groups(), split_takes(), duration(), ffmpeg(), review_status(), apply(), build() (+6 more)

### Community 64 - "log_short"
Cohesion: 0.29
Nodes (3): log_short(), vault_page(), vault_refresh()

### Community 65 - "edit_scripts"
Cohesion: 0.13
Nodes (11): other_ai(), cold_read(), edit_scripts(), narration_lines(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_gemini_modes_choose_codex_and_keep_editor_choice(), test_solo_edit_scripts_uses_same_ai(), test_cold_read_handles_malformed_reply() (+3 more)

### Community 66 - "visual_review"
Cohesion: 0.24
Nodes (7): clock(), overlay_notes(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 69 - "rewrite_paint_prompts"
Cohesion: 0.18
Nodes (5): rewrite_paint_prompts(), ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 70 - "full_props"
Cohesion: 0.33
Nodes (5): full_props(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_remotion_props_full()

### Community 71 - "clean_full"
Cohesion: 0.05
Nodes (32): clean_sound(), limit_sounds(), clean_photo(), is_stereo(), trim_borders(), border(), plain(), full_formats() (+24 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.11
Nodes (15): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+7 more)

### Community 73 - "ask_ai"
Cohesion: 0.14
Nodes (12): ask_ai(), gemini_model(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash(), test_gemini_timeout_switches_to_flash() (+4 more)

### Community 74 - "re"
Cohesion: 0.08
Nodes (15): radians(), channel_url(), new_channel(), save_channel(), seed_ideas(), trend_research(), yt_list(), analyze() (+7 more)

### Community 75 - "speak"
Cohesion: 0.20
Nodes (6): speak(), story_sound(), tts(), test_story_sound_library(), fetch(), _tone_wav()

### Community 76 - "test_full_scenes.py"
Cohesion: 0.12
Nodes (6): crop_film_bytes(), film_frames(), parse_scene_money(), storyboard(), test_music_gain_evens_out_tracks(), test_short_credit()

### Community 77 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 79 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 80 - "resume_runs"
Cohesion: 0.24
Nodes (12): begin(), context(), pack(), pending(), read(), save_context(), unpack(), update() (+4 more)

### Community 82 - "test_ai_modes.py"
Cohesion: 0.22
Nodes (10): configure_brain(), normalize_brain(), fake_providers(), claude(), reply(), saved_session(), test_all_modes_route_writer_editor_and_reader(), test_batch_uses_selected_codex_writer_and_migrates_saved_aliases() (+2 more)

### Community 83 - "owner"
Cohesion: 0.17
Nodes (3): owner(), _fake_planning(), test_director_prompt_mentions_full()

### Community 84 - "test_story.py"
Cohesion: 0.36
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 85 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 86 - "clean_pics"
Cohesion: 0.17
Nodes (6): catalog_text(), clean_pics(), is_usable(), pictures_of(), usable(), direct_scripts()

### Community 88 - "finish_render"
Cohesion: 0.36
Nodes (5): status_lines(), finish_render(), load_state(), save_state(), test_state_roundtrip_full_pics()

### Community 89 - "wants_remotion"
Cohesion: 0.27
Nodes (4): wants_remotion(), apply_look_scenes(), test_apply_look_scenes(), test_remotion_forced_by_look()

### Community 90 - "command"
Cohesion: 0.33
Nodes (4): ask_brain(), ask_number(), command(), test_solo_brain_selection_options()

### Community 91 - "test_review_redraws_custom"
Cohesion: 0.40
Nodes (3): _review_state(), test_redraw_failure_paints(), test_review_redraws_custom()

## Knowledge Gaps
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `templates.py`, `json`, `build_scene.py`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `test_pictures_first.py`, `test_style.py`, `json`, `style_library`, `test_rules.py`, `prepare_topic`, `test_blender_plan.py`, `story_problems`, `quality_check`, `logbook_results`, `test_topic_ideas.py`, `limit_style`, `main`, `short_render.py`, `choose_images`, `edit_scripts`, `clean_full`, `ask_ai`, `re`, `owner`, `test_story.py`, `clean_pics`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1319073083778966 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `json`, `render_remotion`, `local_clips`, `test_blender_plan.py`, `frame_maker`, `full_cues`, `test_weak_opener_graphic_fixes_then_handoff`, `get_image`, `main`, `paint_instead`, `short_render.py`, `choose_images`, `ffmpeg`, `visual_review`, `clean_full`, `speak`, `captions`, `resume_runs`, `make_paper`, `finish_render`, `wants_remotion`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.06666666666666667 - nodes in this community are weakly interconnected._