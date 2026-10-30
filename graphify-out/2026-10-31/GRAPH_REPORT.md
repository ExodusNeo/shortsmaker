# Graph Report - ShortsMaker  (2026-10-31)

## Corpus Check
- 119 files · ~139,015 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 1812 nodes · 4918 edges · 79 communities (68 shown, 11 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 107 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `77f3d866`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- pool_of
- h3_run.py
- ask_ai
- split_make_shorts.py
- gpu.py
- code_custom_scenes
- image_sources.py
- guarded.tsx
- k
- test_h3_handoff.py
- test_blender_scene.py
- approve_candidate
- drawn_opener.py
- test_rules.py
- Journey.tsx
- toolkit.tsx
- prepare_topic
- planning
- Local GPU Worker
- core.mjs
- ffmpeg
- test_full_scenes.py
- makeKit
- test_blender_plan.py
- use
- ClipReader
- full_props
- json
- build_scene.py
- parts.py
- plan_rules.py
- render_remotion
- templates.py
- gather_pool
- clean_look
- full/types.ts
- main
- Paper
- scene_cues
- Shots
- Short.tsx
- textures.mjs
- audio_mix.py
- re
- ref_remotion
- Halftone.tsx
- test_topic_ideas.py
- invent_component
- test_style.py
- channel_profiles.py
- style_library
- test_first_second.py
- kit.mjs
- style_placeholders
- short_with
- test_pictures_first.py
- clean_pics
- _fake_planning
- make_sfx
- bean.mjs
- full_cues
- popS
- test_review_redraws_custom
- full_summary
- subprocess
- dexter.mjs
- kit_parts.mjs
- write_scripts
- use_picture_from
- h3_problems
- test_story.py
- h3_prompt
- apply_look_scenes
- test_local_job_retries_a_hard_crash
- test_remotion_failure_paints
- render
- photo_prep.py

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 65 edges
3. `write_scripts()` - 48 edges
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
- `test_pixabay_keeps_only_on_topic_videos()` --calls--> `pixabay_films()`  [EXTRACTED]
  tests/test_pictures_first.py → shortsmaker/footage.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`

## Communities (79 total, 11 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "pool_of"
Cohesion: 0.14
Nodes (18): catalog_entries(), catalog_pool(), entry(), fake_ai, pool_of(), test_both_mode_reuses_pools(), test_catalog_both_empty_stops_uncached(), test_catalog_empty_pool_no_ai() (+10 more)

### Community 3 - "h3_run.py"
Cohesion: 0.22
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 4 - "ask_ai"
Cohesion: 0.11
Nodes (15): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), fact_check(), test_fact_check_drops_full(), test_argon_out_of_quota_switches_to_flash(), fake_run() (+7 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "gpu.py"
Cohesion: 0.10
Nodes (8): hex_rgb(), luminance(), prune_cache(), prune_work(), library_menu(), reject_candidate(), save_candidate(), test_prune_cache_handles_pools()

### Community 7 - "code_custom_scenes"
Cohesion: 0.11
Nodes (14): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+6 more)

### Community 8 - "image_sources.py"
Cohesion: 0.06
Nodes (22): archive_films(), commons_films(), crop_film_bytes(), film_frames(), nasa_films(), pixabay_films(), archive_images(), article_images() (+14 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.21
Nodes (13): unpack_clips(), handoff(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated(), test_flagged_start_picture_is_not_sent(), test_handoff_picks_up_clips_zip(), test_handoff_records_which_file_made_the_clip(), test_handoff_writes_jobs_and_zip() (+5 more)

### Community 12 - "test_blender_scene.py"
Cohesion: 0.06
Nodes (28): caption_layer(), make(), master_gain(), project_xml(), changed(), count(), manifest(), near() (+20 more)

### Community 13 - "approve_candidate"
Cohesion: 0.23
Nodes (9): approve_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_candidate_names_unique_across_kinds() (+1 more)

### Community 14 - "drawn_opener.py"
Cohesion: 0.09
Nodes (17): code_version(), available(), clean_code(), fingerprint(), lint(), make_opener(), node_run(), review() (+9 more)

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
Nodes (9): write_json(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_pool_roundtrip(), test_pool_rows_without_thumbs() (+1 more)

### Community 19 - "planning"
Cohesion: 0.15
Nodes (16): passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare(), reply() (+8 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "ffmpeg"
Cohesion: 0.13
Nodes (13): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), motion_prompt(), split_takes(), start_picture(), start_picture_problems() (+5 more)

### Community 23 - "test_full_scenes.py"
Cohesion: 0.10
Nodes (14): test_auto_fix_graphic(), test_clean_full_board(), test_clean_full_document(), test_clean_full_journey(), test_clean_full_keeps_thing(), test_clean_full_limits(), test_ink_silhouette(), test_music_gain_evens_out_tracks() (+6 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.05
Nodes (44): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+36 more)

### Community 26 - "use"
Cohesion: 0.33
Nodes (4): fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 27 - "ClipReader"
Cohesion: 0.11
Nodes (8): ClipReader, draw_card(), draw_graphic(), flash_alpha(), frame(), shot(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 28 - "full_props"
Cohesion: 0.17
Nodes (9): sfx_events(), full_props(), _board(), _jpg(), test_board_pictures_attached(), test_custom_cues_props_and_pictures(), test_remotion_props_full(), test_sfx_full() (+1 more)

### Community 29 - "json"
Cohesion: 0.09
Nodes (12): comfy_call(), cosy_instruct(), local_job(), local_voice(), moss_graph(), moss_images(), voicestudio_unload(), voicestudio_up() (+4 more)

### Community 30 - "build_scene.py"
Cohesion: 0.16
Nodes (6): collection(), ink_lines(), linear(), material(), setup(), radians()

### Community 31 - "parts.py"
Cohesion: 0.16
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 32 - "plan_rules.py"
Cohesion: 0.10
Nodes (20): clean_full(), word(), clean_graphic(), contains(), coords(), fallback_graphic(), fill_money_graphics(), is_loop_short() (+12 more)

### Community 33 - "render_remotion"
Cohesion: 0.13
Nodes (11): short_skin(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), test_clean_full_custom_and_skin() (+3 more)

### Community 34 - "templates.py"
Cohesion: 0.17
Nodes (15): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge() (+7 more)

### Community 35 - "gather_pool"
Cohesion: 0.10
Nodes (6): gather_pool(), owner(), film(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 36 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 38 - "main"
Cohesion: 0.18
Nodes (4): keyvis(), main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "scene_cues"
Cohesion: 0.09
Nodes (13): scene_cues(), fills_frame(), fit_font(), frame_maker(), graphic_low(), graphic_overlay(), person_card(), thumbnail() (+5 more)

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
Cohesion: 0.12
Nodes (10): ass_time(), caption_lines(), captions(), styled(), freesound_fetch(), music_gain(), speak(), story_sound() (+2 more)

### Community 45 - "re"
Cohesion: 0.10
Nodes (10): log_short(), logbook_results(), vault_page(), vault_refresh(), rescue_graphics(), mark_details(), first_second_check(), max_full() (+2 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "test_topic_ideas.py"
Cohesion: 0.14
Nodes (13): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+5 more)

### Community 49 - "invent_component"
Cohesion: 0.13
Nodes (10): clean_style_code(), invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), swap_inventions(), test_invention_lint_failure_uses_fallback() (+2 more)

### Community 50 - "test_style.py"
Cohesion: 0.12
Nodes (11): wants_remotion(), plan_with(), ask(), test_clean_question_and_kinetic(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics(), test_limit_style_caps() (+3 more)

### Community 51 - "channel_profiles.py"
Cohesion: 0.08
Nodes (23): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+15 more)

### Community 52 - "style_library"
Cohesion: 0.12
Nodes (10): cut_text(), edit_plan(), look_text(), picture_line(), style_library(), style_rules(), write_style_index(), test_edit_plan_picture_line() (+2 more)

### Community 53 - "test_first_second.py"
Cohesion: 0.20
Nodes (13): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once(), test_opener_must_be_a_later_real_picture() (+5 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 55 - "style_placeholders"
Cohesion: 0.21
Nodes (9): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_slots_restored_after_render() (+1 more)

### Community 56 - "short_with"
Cohesion: 0.21
Nodes (14): fake_ai(), short_with(), test_missing_scene_is_asked_again(), run(), test_owner_clip_is_cut_again_for_the_scene_it_now_sits_in(), test_retries_only_failing_scene_with_reason(), run(), test_scene_number_given_as_text_is_accepted() (+6 more)

### Community 57 - "test_pictures_first.py"
Cohesion: 0.21
Nodes (14): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+6 more)

### Community 58 - "clean_pics"
Cohesion: 0.20
Nodes (8): catalog_text(), clean_pics(), is_usable(), usable(), pic_short(), test_board_item_pics_cleaned(), test_board_item_refuses_film(), test_clean_pics()

### Community 59 - "_fake_planning"
Cohesion: 0.17
Nodes (6): _fake_planning(), ask(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "full_cues"
Cohesion: 0.22
Nodes (5): full_cues(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish(), test_opener_graphic()

### Community 64 - "test_review_redraws_custom"
Cohesion: 0.40
Nodes (3): _review_state(), test_redraw_failure_paints(), test_review_redraws_custom()

### Community 65 - "full_summary"
Cohesion: 0.50
Nodes (3): full_summary(), test_full_props_figure(), test_full_summary()

### Community 66 - "subprocess"
Cohesion: 0.14
Nodes (6): remove(), film_piece(), shot_span(), duration(), main(), props_for()

### Community 69 - "write_scripts"
Cohesion: 0.11
Nodes (13): clean_sound(), limit_sounds(), pictures_of(), limit_full(), limit_style(), direct_scripts(), edit_scripts(), length_plan() (+5 more)

### Community 70 - "use_picture_from"
Cohesion: 0.33
Nodes (3): use_picture_from(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 72 - "test_story.py"
Cohesion: 0.06
Nodes (33): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+25 more)

### Community 85 - "render"
Cohesion: 0.05
Nodes (29): gemini_images(), short_credit(), clock(), graphics_count(), ink_silhouette(), paint_instead(), apply_review_fixes(), fix_opener_graphic() (+21 more)

### Community 86 - "photo_prep.py"
Cohesion: 0.17
Nodes (6): clean_photo(), is_stereo(), to_vertical(), trim_borders(), border(), plain()

## Knowledge Gaps
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `gpu.py`, `test_blender_scene.py`, `ffmpeg`, `test_blender_plan.py`, `ClipReader`, `full_props`, `json`, `plan_rules.py`, `render_remotion`, `scene_cues`, `audio_mix.py`, `re`, `test_style.py`, `channel_profiles.py`, `style_library`, `test_pictures_first.py`, `make_sfx`, `full_summary`, `subprocess`, `photo_prep.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `Shots`, `json`, `build_scene.py`, `parts.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `pool_of` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._
- **Why does `ClipReader` connect `ClipReader` to `gpu.py`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.11255411255411256 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._