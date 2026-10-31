# Graph Report - ShortsMaker  (2026-10-31)

## Corpus Check
- 120 files · ~142,709 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 1853 nodes · 5032 edges · 85 communities (70 shown, 15 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 111 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `19d098f6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- json
- ask_ai
- split_make_shorts.py
- rescue_graphics
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
- gpu.py
- edit_project.py
- makeKit
- test_blender_scene.py
- render
- frame_maker
- full_cues
- drawn_opener.py
- build_scene.py
- parts.py
- clean_full
- test_full_scenes.py
- templates.py
- owner
- test_story.py
- full/types.ts
- main
- Paper
- visual_review
- Shots
- Short.tsx
- textures.mjs
- audio_mix.py
- test_blender_render.py
- re
- Halftone.tsx
- topic_ideas.py
- invent_component
- limit_style
- main
- clean_look
- test_first_second.py
- kit.mjs
- fake_ai
- fix_short
- choose_images
- edit_plan
- ask
- full_props
- bean.mjs
- subprocess
- popS
- apply_review_fixes
- quality_check
- ref_remotion
- dexter.mjs
- kit_parts.mjs
- capture_prompts
- run_draft
- trim_borders
- align_words
- run_agy
- test_style.py
- make_paper
- trend_research
- rewrite_paint_prompts
- srt
- StopPicker
- catalog_entries
- test_on_topic_ignores_a_lone_shared_name
- make_sfx
- test_short_credit

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 65 edges
3. `write_scripts()` - 51 edges
4. `ask_ai()` - 43 edges
5. `skinOf()` - 29 edges
6. `clamp()` - 27 edges
7. `main()` - 27 edges
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

## Communities (85 total, 15 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.14
Nodes (24): write_json(), catalog_pool(), clean_pics(), save_pool(), entry(), film(), pic_short(), pool_of() (+16 more)

### Community 3 - "json"
Cohesion: 0.11
Nodes (13): call(), fit_start(), frames(), graph(), main(), saved_file(), align(), main() (+5 more)

### Community 4 - "ask_ai"
Cohesion: 0.13
Nodes (13): ask_ai(), gemini_model(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high(), test_encoder_cache_lives_with_video_encoder(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash() (+5 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "rescue_graphics"
Cohesion: 0.14
Nodes (8): full_formats(), rescue_graphics(), max_full(), max_full_planned(), article_text(), fact_check(), test_fact_check_drops_full(), test_rescue_respects_caps()

### Community 7 - "code_custom_scenes"
Cohesion: 0.13
Nodes (12): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), redraw_custom() (+4 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "gather_pool"
Cohesion: 0.11
Nodes (9): get_image(), openverse_images(), ov_get(), full_pictures(), gather_pool(), test_board_pictures_attached(), stubbed, test_gather_pool_shape() (+1 more)

### Community 13 - "style_library"
Cohesion: 0.16
Nodes (13): approve_candidate(), style_library(), write_style_index(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure() (+5 more)

### Community 14 - "render_remotion"
Cohesion: 0.13
Nodes (11): short_skin(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_clean_full_custom_and_skin() (+3 more)

### Community 15 - "test_rules.py"
Cohesion: 0.20
Nodes (20): parse_rules(), make(), stop_text(), test_bad_min_pictures_stops(), test_blender_needs_a_build_plan_section(), test_bom_and_crlf_load_the_same(), test_draft_stops(), test_duplicate_heading_stops() (+12 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 18 - "prepare_topic"
Cohesion: 0.13
Nodes (11): catalog_text(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), prepare_topic(), usable() (+3 more)

### Community 19 - "write_scripts"
Cohesion: 0.12
Nodes (23): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+15 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "gpu.py"
Cohesion: 0.08
Nodes (17): comfy_call(), cover_crop(), cut_owner_clip(), gemini_images(), h3_prompts(), local_clips(), local_job(), moss_graph() (+9 more)

### Community 23 - "edit_project.py"
Cohesion: 0.13
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "test_blender_scene.py"
Cohesion: 0.07
Nodes (42): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+34 more)

### Community 26 - "render"
Cohesion: 0.06
Nodes (23): full_summary(), graphics_count(), to_vertical(), opener_graphic(), mark_details(), fix_opener_graphic(), storyboard(), weak_opener_graphic() (+15 more)

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (15): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+7 more)

### Community 28 - "full_cues"
Cohesion: 0.13
Nodes (11): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish() (+3 more)

### Community 29 - "drawn_opener.py"
Cohesion: 0.20
Nodes (5): code_version(), available(), clean_code(), fingerprint(), write()

### Community 30 - "build_scene.py"
Cohesion: 0.16
Nodes (6): collection(), ink_lines(), linear(), material(), setup(), radians()

### Community 31 - "parts.py"
Cohesion: 0.16
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 32 - "clean_full"
Cohesion: 0.05
Nodes (30): lint(), make_opener(), node_run(), review(), sheet_times(), clean_full(), word(), clean_graphic() (+22 more)

### Community 33 - "test_full_scenes.py"
Cohesion: 0.09
Nodes (9): ask_number(), hex_rgb(), luminance(), crop_film_bytes(), film_frames(), clean_photo(), library_menu(), reject_candidate() (+1 more)

### Community 34 - "templates.py"
Cohesion: 0.17
Nodes (15): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge() (+7 more)

### Community 35 - "owner"
Cohesion: 0.15
Nodes (4): owner(), _fake_planning(), test_director_prompt_mentions_full(), test_good_look_check_skips_the_extra_compile()

### Community 36 - "test_story.py"
Cohesion: 0.06
Nodes (35): sentence_groups(), other_ai(), log_short(), first_sentence(), check_twists(), cold_read(), edit_scripts(), narration_lines() (+27 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 38 - "main"
Cohesion: 0.18
Nodes (4): keyvis(), main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "visual_review"
Cohesion: 0.24
Nodes (7): clock(), overlay_notes(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 41 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "textures.mjs"
Cohesion: 0.25
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "audio_mix.py"
Cohesion: 0.09
Nodes (15): ass_time(), caption_lines(), captions(), styled(), freesound_fetch(), limit_sounds(), music_gain(), speak() (+7 more)

### Community 45 - "test_blender_render.py"
Cohesion: 0.10
Nodes (22): BlenderFailed, peaks(), render_clips(), _run(), scene_frames(), drawn_thumbnail(), fake_blender(), short() (+14 more)

### Community 46 - "re"
Cohesion: 0.05
Nodes (28): clean_sound(), archive_films(), commons_films(), nasa_films(), graphic_low(), cosy_instruct(), local_voice(), spoken_count() (+20 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "topic_ideas.py"
Cohesion: 0.13
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 49 - "invent_component"
Cohesion: 0.11
Nodes (16): invent_component(), attempt(), invent_styles(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), style_rules() (+8 more)

### Community 51 - "main"
Cohesion: 0.09
Nodes (16): ask_brain(), ask_count(), ask_yes(), new_channel(), pick_channel(), save_channel(), use_channel(), main() (+8 more)

### Community 52 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 53 - "test_first_second.py"
Cohesion: 0.18
Nodes (14): first_second_check(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture() (+6 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 55 - "fake_ai"
Cohesion: 0.19
Nodes (8): logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel(), test_seo_never_sees_competitor_titles()

### Community 56 - "fix_short"
Cohesion: 0.15
Nodes (8): configure_brain(), fix_short(), draft_rules(), require_rules(), test_fix_bat_explains_a_drawn_short(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_fix_checks_rules_before_asking_for_a_scene(), test_missing_rules_file_is_drafted()

### Community 57 - "choose_images"
Cohesion: 0.21
Nodes (13): load_channel(), choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+5 more)

### Community 58 - "edit_plan"
Cohesion: 0.17
Nodes (6): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 59 - "ask"
Cohesion: 0.18
Nodes (6): ask(), _review_state(), test_look_check_fixes_code(), test_redraw_failure_paints(), test_review_redraws_custom(), test_review_uses_unused_pool_pictures_before_painting()

### Community 60 - "full_props"
Cohesion: 0.15
Nodes (9): sfx_events(), full_props(), _board(), _jpg(), test_custom_cues_props_and_pictures(), test_remotion_props_full(), test_sfx_full(), test_story_sound_wins_its_moment() (+1 more)

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "subprocess"
Cohesion: 0.09
Nodes (12): shot_span(), fills_frame(), split_takes(), voicestudio_up(), duration(), ffmpeg(), video_encoder(), preview_sheet() (+4 more)

### Community 64 - "apply_review_fixes"
Cohesion: 0.16
Nodes (7): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 65 - "quality_check"
Cohesion: 0.25
Nodes (4): quality_check(), length_plan(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 69 - "capture_prompts"
Cohesion: 0.20
Nodes (6): load_rules(), min_real_pictures(), capture_prompts(), ask(), test_load_rules_sets_session(), test_strange_history_prompts_unchanged()

### Community 70 - "run_draft"
Cohesion: 0.31
Nodes (8): draft_reply(), run_draft(), test_draft_blender_channel_needs_build_plan(), test_draft_keeps_ai_headings_inside_their_section(), test_draft_never_overwrites(), test_draft_retries_once_then_stops(), test_draft_settings_come_from_code(), test_draft_writes_tagged_draft_file()

### Community 71 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

### Community 72 - "align_words"
Cohesion: 0.13
Nodes (11): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak(), test_caption_word_counts_match_the_scene_splitter(), test_caption_words_keep_what_is_written() (+3 more)

### Community 73 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 75 - "test_style.py"
Cohesion: 0.14
Nodes (10): wants_remotion(), apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics() (+2 more)

### Community 76 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 77 - "trend_research"
Cohesion: 0.29
Nodes (4): channel_url(), seed_ideas(), trend_research(), yt_list()

## Knowledge Gaps
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `templates.py`, `json`, `Shots`, `build_scene.py`, `parts.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `rescue_graphics`, `render_remotion`, `gpu.py`, `edit_project.py`, `frame_maker`, `full_cues`, `test_full_scenes.py`, `visual_review`, `audio_mix.py`, `test_blender_render.py`, `re`, `main`, `test_first_second.py`, `fix_short`, `choose_images`, `edit_plan`, `full_props`, `subprocess`, `apply_review_fixes`, `quality_check`, `test_style.py`, `make_paper`, `srt`, `make_sfx`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14393939393939395 - nodes in this community are weakly interconnected._
- **Why does `cold_read()` connect `test_story.py` to `fix_short`, `test_full_scenes.py`, `json`, `ask_ai`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.10591133004926108 - nodes in this community are weakly interconnected._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.12987012987012986 - nodes in this community are weakly interconnected._