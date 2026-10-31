# Graph Report - ShortsMaker  (2026-10-31)

## Corpus Check
- 124 files · ~144,614 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 1898 nodes · 5155 edges · 90 communities (74 shown, 16 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 115 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b76efc1b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- catalog_pool
- plan_with
- test_blender_scene.py
- split_make_shorts.py
- json
- code_custom_scenes
- film_piece
- guarded.tsx
- k
- test_h3_handoff.py
- gather_pool
- test_style.py
- render_remotion
- test_rules.py
- Journey.tsx
- toolkit.tsx
- prepare_topic
- write_scripts
- Local GPU Worker
- core.mjs
- gpu.py
- test_edit_project.py
- makeKit
- test_blender_plan.py
- render
- ClipReader
- full_cues
- h3_run.py
- build_scene.py
- parts.py
- drawn_opener.py
- templates.py
- use
- test_story.py
- full/types.ts
- main
- Paper
- quality_check
- Shots
- Short.tsx
- textures.mjs
- frame_maker
- fake_ai
- image_sources.py
- Halftone.tsx
- re
- style_placeholders
- limit_style
- main
- paint_instead
- test_first_second.py
- kit.mjs
- RetentionTests
- invent_component
- test_pictures_first.py
- rescue_graphics
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
- paint_opener_start
- clean_full
- align_words
- ask_ai
- analyze
- speak
- test_full_scenes.py
- captions
- ref_remotion
- edit_plan
- use_picture_from
- cold_read
- story_sound
- limit_full
- make_sfx
- test_local_job_retries_a_hard_crash
- pictures_of
- MarkTests
- lint_style_code
- apply_look_scenes

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 65 edges
3. `write_scripts()` - 51 edges
4. `ask_ai()` - 46 edges
5. `skinOf()` - 29 edges
6. `main()` - 29 edges
7. `clamp()` - 27 edges
8. `ellPts()` - 26 edges
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
- `test_pixabay_keeps_only_on_topic_videos()` --calls--> `pixabay_films()`  [EXTRACTED]
  tests/test_pictures_first.py → shortsmaker/footage.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`

## Communities (90 total, 16 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "catalog_pool"
Cohesion: 0.13
Nodes (21): catalog_entries(), catalog_pool(), catalog_text(), clean_pics(), is_usable(), usable(), entry(), pic_short() (+13 more)

### Community 3 - "plan_with"
Cohesion: 0.29
Nodes (5): plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "json"
Cohesion: 0.08
Nodes (15): align(), main(), studio_speak(), freesound_fetch(), code_version(), channel_url(), seed_ideas(), trend_research() (+7 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.12
Nodes (13): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+5 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.11
Nodes (27): unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated(), test_flagged_start_picture_is_not_sent(), test_handoff_picks_up_clips_zip() (+19 more)

### Community 12 - "gather_pool"
Cohesion: 0.12
Nodes (8): gather_pool(), owner(), _fake_planning(), test_director_prompt_mentions_full(), film(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 13 - "test_style.py"
Cohesion: 0.08
Nodes (22): clean_invention(), clean_look(), clean_transition(), settle_style(), approve_candidate(), save_candidate(), style_library(), write_style_index() (+14 more)

### Community 14 - "render_remotion"
Cohesion: 0.22
Nodes (7): render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain()

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (38): draft_rules(), load_rules(), min_real_pictures(), parse_rules(), require_rules(), capture_prompts(), ask(), draft_reply() (+30 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 18 - "prepare_topic"
Cohesion: 0.17
Nodes (10): write_json(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip() (+2 more)

### Community 19 - "write_scripts"
Cohesion: 0.13
Nodes (22): write_scripts(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare() (+14 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "gpu.py"
Cohesion: 0.10
Nodes (17): comfy_call(), cover_crop(), cut_owner_clip(), h3_problems(), h3_prompt(), h3_prompts(), local_clips(), local_job() (+9 more)

### Community 23 - "test_edit_project.py"
Cohesion: 0.12
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.05
Nodes (44): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+36 more)

### Community 26 - "render"
Cohesion: 0.11
Nodes (12): short_credit(), graphics_count(), wants_remotion(), srt(), drawn_choices(), load_state(), render(), save_state() (+4 more)

### Community 27 - "ClipReader"
Cohesion: 0.12
Nodes (8): ClipReader, draw_card(), draw_graphic(), flash_alpha(), frame(), shot(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 28 - "full_cues"
Cohesion: 0.08
Nodes (17): sfx_events(), full_props(), full_pictures(), full_cues(), spoken_at(), spoken_span(), _board(), _jpg() (+9 more)

### Community 29 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 30 - "build_scene.py"
Cohesion: 0.16
Nodes (6): collection(), ink_lines(), linear(), material(), setup(), radians()

### Community 31 - "parts.py"
Cohesion: 0.16
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 32 - "drawn_opener.py"
Cohesion: 0.09
Nodes (17): available(), clean_code(), fingerprint(), lint(), make_opener(), node_run(), review(), sheet_times() (+9 more)

### Community 34 - "templates.py"
Cohesion: 0.17
Nodes (15): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge() (+7 more)

### Community 35 - "use"
Cohesion: 0.33
Nodes (4): fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 36 - "test_story.py"
Cohesion: 0.16
Nodes (15): first_sentence(), check_twists(), story_problems(), read(), test_cold_read_verdicts(), test_first_sentence_reads_across_the_cut(), test_no_hook_setting_no_hook_check(), test_rules_accept_opener_setting() (+7 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 38 - "main"
Cohesion: 0.18
Nodes (4): keyvis(), main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "quality_check"
Cohesion: 0.25
Nodes (4): quality_check(), length_plan(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 41 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "textures.mjs"
Cohesion: 0.25
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "frame_maker"
Cohesion: 0.12
Nodes (8): fills_frame(), fit_font(), frame_maker(), graphic_low(), graphic_overlay(), thumbnail(), credit_tag_image(), fallback_graphic()

### Community 45 - "fake_ai"
Cohesion: 0.16
Nodes (10): load_channel(), logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_catalog_empty_pool_no_ai(), test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list() (+2 more)

### Community 46 - "image_sources.py"
Cohesion: 0.08
Nodes (19): archive_films(), commons_films(), film_frames(), nasa_films(), archive_images(), article_images(), commons_search(), get_image() (+11 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "re"
Cohesion: 0.09
Nodes (17): vault_page(), vault_refresh(), parse_scene_money(), max_full(), max_full_planned(), clean_style_code(), clash(), fetch_ideas() (+9 more)

### Community 49 - "style_placeholders"
Cohesion: 0.19
Nodes (10): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback(), test_invention_lint_failure_uses_fallback(), test_invention_passes_into_slot(), run() (+2 more)

### Community 51 - "main"
Cohesion: 0.07
Nodes (26): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), new_channel(), normalize_brain(), pick_channel() (+18 more)

### Community 52 - "paint_instead"
Cohesion: 0.12
Nodes (6): gemini_images(), to_vertical(), ink_silhouette(), paint_instead(), test_ink_silhouette(), test_remotion_failure_paints()

### Community 53 - "test_first_second.py"
Cohesion: 0.18
Nodes (14): first_second_check(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture() (+6 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "invent_component"
Cohesion: 0.18
Nodes (6): invent_component(), invent_styles(), style_preview(), style_rules(), swap_inventions(), test_swap_inventions()

### Community 57 - "test_pictures_first.py"
Cohesion: 0.21
Nodes (14): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+6 more)

### Community 58 - "rescue_graphics"
Cohesion: 0.15
Nodes (8): full_formats(), opener_graphic(), rescue_graphics(), article_text(), fact_check(), test_fact_check_drops_full(), test_opener_graphic(), test_rescue_respects_caps()

### Community 59 - "apply_review_fixes"
Cohesion: 0.18
Nodes (7): apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_redraw_failure_paints(), test_review_redraws_custom()

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "ffmpeg"
Cohesion: 0.11
Nodes (12): shot_span(), cosy_instruct(), local_voice(), split_takes(), spoken_count(), voicestudio_unload(), voicestudio_up(), duration() (+4 more)

### Community 64 - "log_short"
Cohesion: 0.25
Nodes (5): sentence_groups(), log_short(), scenes(), test_logbook_hook_line_is_the_whole_first_sentence(), test_sentences_running_across_cuts_are_one_take()

### Community 65 - "edit_scripts"
Cohesion: 0.13
Nodes (13): other_ai(), edit_scripts(), narration_lines(), fake_providers(), claude(), reply(), saved_session(), test_all_modes_route_writer_editor_and_reader() (+5 more)

### Community 66 - "visual_review"
Cohesion: 0.24
Nodes (7): clock(), overlay_notes(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 69 - "rewrite_paint_prompts"
Cohesion: 0.18
Nodes (5): rewrite_paint_prompts(), ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 70 - "paint_opener_start"
Cohesion: 0.15
Nodes (7): full_summary(), fix_opener_graphic(), paint_opener_start(), weak_opener_graphic(), test_full_props_figure(), test_full_summary(), test_weak_opener_graphic_fixes_then_handoff()

### Community 71 - "clean_full"
Cohesion: 0.06
Nodes (30): clean_sound(), limit_sounds(), clean_photo(), is_stereo(), trim_borders(), border(), plain(), clean_full() (+22 more)

### Community 72 - "align_words"
Cohesion: 0.15
Nodes (10): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), test_caption_word_counts_match_the_scene_splitter(), test_caption_words_keep_what_is_written(), test_dollar_scale_word_order() (+2 more)

### Community 73 - "ask_ai"
Cohesion: 0.10
Nodes (18): scene_cues(), ask_ai(), gemini_model(), test_counter_finishes_before_it_leaves(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high() (+10 more)

### Community 74 - "analyze"
Cohesion: 0.29
Nodes (5): analyze(), normalize_reply(), report_text(), scenes_from_plan(), seconds()

### Community 76 - "test_full_scenes.py"
Cohesion: 0.08
Nodes (14): music_gain(), hex_rgb(), luminance(), short_skin(), crop_film_bytes(), person_card(), tsc_check(), make_paper() (+6 more)

### Community 77 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 79 - "edit_plan"
Cohesion: 0.17
Nodes (6): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 80 - "use_picture_from"
Cohesion: 0.33
Nodes (3): use_picture_from(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 81 - "cold_read"
Cohesion: 0.33
Nodes (4): cold_read(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 82 - "story_sound"
Cohesion: 0.40
Nodes (4): story_sound(), test_story_sound_library(), fetch(), _tone_wav()

### Community 88 - "lint_style_code"
Cohesion: 0.50
Nodes (3): attempt(), lint_style_code(), test_placeholders_match_the_slots()

## Knowledge Gaps
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `test_style.py`, `render_remotion`, `gpu.py`, `test_edit_project.py`, `test_blender_plan.py`, `ClipReader`, `full_cues`, `quality_check`, `frame_maker`, `re`, `main`, `paint_instead`, `test_first_second.py`, `test_pictures_first.py`, `rescue_graphics`, `apply_review_fixes`, `ffmpeg`, `visual_review`, `paint_opener_start`, `clean_full`, `ask_ai`, `speak`, `test_full_scenes.py`, `captions`, `edit_plan`, `story_sound`, `make_sfx`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `json`, `Shots`, `build_scene.py`, `parts.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `catalog_pool` be split into smaller, more focused modules?**
  _Cohesion score 0.12698412698412698 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `catalog_pool`, `plan_with`, `json`, `gather_pool`, `test_style.py`, `test_rules.py`, `prepare_topic`, `test_blender_plan.py`, `pathlib`, `test_story.py`, `quality_check`, `fake_ai`, `re`, `limit_style`, `main`, `rescue_graphics`, `edit_scripts`, `clean_full`, `ask_ai`, `test_full_scenes.py`, `limit_full`, `pictures_of`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.08143939393939394 - nodes in this community are weakly interconnected._