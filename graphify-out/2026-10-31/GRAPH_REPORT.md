# Graph Report - ShortsMaker  (2026-10-31)

## Corpus Check
- 122 files · ~143,171 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 1872 nodes · 5088 edges · 88 communities (73 shown, 15 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 114 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d4503664`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- test_style.py
- words_of
- split_make_shorts.py
- audio_mix.py
- shutil
- footage.py
- guarded.tsx
- k
- test_h3_handoff.py
- owner
- candidate_in
- render_remotion
- test_rules.py
- Journey.tsx
- skinOf
- picture_pool.py
- write_scripts
- Local GPU Worker
- core.mjs
- local_clips
- edit_project.py
- makeKit
- test_blender_scene.py
- render
- frame_render.py
- full_cues
- fetch
- look.py
- parts.py
- drawn_opener.py
- plan_rules.py
- templates.py
- use
- test_story.py
- BigNumber.tsx
- main
- toolkit.tsx
- quality_check
- build_scene.py
- Short.tsx
- textures.mjs
- clean_look
- test_blender_render.py
- image_sources.py
- Halftone.tsx
- test_topic_ideas.py
- with_fakes
- limit_style
- main
- local_job
- test_first_second.py
- kit.mjs
- sfx_events
- trim_borders
- choose_images
- json
- apply_review_fixes
- full_props
- bean.mjs
- gpu.py
- popS
- gather_pool
- test_ai_modes.py
- clean_graphic
- dexter.mjs
- kit_parts.mjs
- _fake_planning
- paint_opener_start
- test_full_scenes.py
- re
- ask_ai
- moss_images
- drawn_thumbnail
- make_paper
- captions
- srt
- picture_line
- h3_problems
- h3_prompt
- write_json
- limit_full
- wants_remotion
- test_local_job_retries_a_hard_crash
- test_remotion_failure_paints
- MarkTests

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 65 edges
3. `write_scripts()` - 51 edges
4. `ask_ai()` - 45 edges
5. `skinOf()` - 29 edges
6. `main()` - 28 edges
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
- `test_new_channel_stops_for_review()` --calls--> `pick_channel()`  [EXTRACTED]
  tests/test_rules.py → shortsmaker/channel_profiles.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`

## Communities (88 total, 15 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.13
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.15
Nodes (25): catalog_pool(), save_pool(), entry(), fake_ai, film(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+17 more)

### Community 3 - "test_style.py"
Cohesion: 0.14
Nodes (10): apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics(), test_library_entries_have_fields() (+2 more)

### Community 4 - "words_of"
Cohesion: 0.16
Nodes (10): clean_sound(), limit_sounds(), word(), contains(), fill_money_graphics(), is_person_portrait(), parse_scene_money(), words_of() (+2 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "audio_mix.py"
Cohesion: 0.11
Nodes (9): freesound_fetch(), music_gain(), speak(), tts(), channel_url(), seed_ideas(), trend_research(), yt_list() (+1 more)

### Community 7 - "shutil"
Cohesion: 0.14
Nodes (12): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+4 more)

### Community 8 - "footage.py"
Cohesion: 0.13
Nodes (8): crop_film_bytes(), film_frames(), film_piece(), pixabay_films(), shot_span(), film_ffmpeg(), duration(), test_pixabay_keeps_only_on_topic_videos()

### Community 9 - "guarded.tsx"
Cohesion: 0.13
Nodes (18): Box, boxAt(), clamp, fitCard(), hits(), layoutColumn(), layoutGrid(), layoutRow() (+10 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.06
Nodes (33): call(), fit_start(), frames(), graph(), main(), saved_file(), unpack_clips(), fake_ai() (+25 more)

### Community 12 - "owner"
Cohesion: 0.14
Nodes (5): owner(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits(), test_pool_roundtrip()

### Community 13 - "candidate_in"
Cohesion: 0.25
Nodes (8): candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_candidate_names_unique_across_kinds(), test_reject_deletes()

### Community 14 - "render_remotion"
Cohesion: 0.12
Nodes (13): short_skin(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), restore_style_slots(), style_props(), swap_inventions() (+5 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (39): load_rules(), min_real_pictures(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft() (+31 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.16
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "skinOf"
Cohesion: 0.18
Nodes (24): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+16 more)

### Community 18 - "picture_pool.py"
Cohesion: 0.12
Nodes (12): catalog_entries(), catalog_text(), clean_pics(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder() (+4 more)

### Community 19 - "write_scripts"
Cohesion: 0.14
Nodes (21): write_scripts(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare() (+13 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "local_clips"
Cohesion: 0.18
Nodes (9): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), start_picture(), start_picture_problems(), veo_handoff(), video_encoder() (+1 more)

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
Cohesion: 0.13
Nodes (11): make_sfx(), story_sound(), ffmpeg(), graphics_count(), drawn_choices(), load_state(), render(), save_state() (+3 more)

### Community 27 - "frame_render.py"
Cohesion: 0.07
Nodes (17): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+9 more)

### Community 28 - "full_cues"
Cohesion: 0.12
Nodes (12): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish() (+4 more)

### Community 29 - "fetch"
Cohesion: 0.19
Nodes (8): archive_films(), nasa_films(), archive_images(), nasa_images(), nasa_search(), on_topic(), fetch(), test_on_topic_ignores_a_lone_shared_name()

### Community 30 - "look.py"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (22): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+14 more)

### Community 32 - "drawn_opener.py"
Cohesion: 0.09
Nodes (17): available(), clean_code(), fingerprint(), lint(), make_opener(), node_run(), review(), sheet_times() (+9 more)

### Community 33 - "plan_rules.py"
Cohesion: 0.08
Nodes (8): hex_rgb(), luminance(), clock(), clean_photo(), overlay_notes(), storyboard(), library_menu(), reject_candidate()

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "use"
Cohesion: 0.33
Nodes (4): fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 36 - "test_story.py"
Cohesion: 0.07
Nodes (31): cold_read_line(), sentence_groups(), log_short(), first_sentence(), check_twists(), cold_read(), edit_scripts(), narration_lines() (+23 more)

### Community 37 - "BigNumber.tsx"
Cohesion: 0.27
Nodes (11): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+3 more)

### Community 38 - "main"
Cohesion: 0.17
Nodes (4): main(), Failure, key(), focus_object()

### Community 39 - "toolkit.tsx"
Cohesion: 0.12
Nodes (31): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+23 more)

### Community 40 - "quality_check"
Cohesion: 0.25
Nodes (4): quality_check(), length_plan(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 41 - "build_scene.py"
Cohesion: 0.15
Nodes (5): direction(), keyloc(), keyvis(), Shots, radians()

### Community 42 - "Short.tsx"
Cohesion: 0.13
Nodes (20): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Root(), Background(), flashAlpha(), GraphicFor() (+12 more)

### Community 43 - "textures.mjs"
Cohesion: 0.25
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 45 - "test_blender_render.py"
Cohesion: 0.14
Nodes (16): BlenderFailed, code_version(), peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short() (+8 more)

### Community 46 - "image_sources.py"
Cohesion: 0.14
Nodes (9): commons_films(), article_images(), commons_search(), get_image(), short_credit(), thumb_url(), usable_license(), wm_files() (+1 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "test_topic_ideas.py"
Cohesion: 0.15
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 49 - "with_fakes"
Cohesion: 0.18
Nodes (8): attempt(), lint_style_code(), test_failed_invention_keeps_the_others(), test_invention_compile_failure_uses_fallback(), test_invention_lint_failure_uses_fallback(), run(), test_placeholders_match_the_slots(), with_fakes()

### Community 51 - "main"
Cohesion: 0.07
Nodes (22): ask_count(), ask_yes(), load_channel(), new_channel(), pick_channel(), save_channel(), use_channel(), fix_short() (+14 more)

### Community 52 - "local_job"
Cohesion: 0.20
Nodes (4): gemini_images(), local_job(), to_vertical(), paint_instead()

### Community 53 - "test_first_second.py"
Cohesion: 0.16
Nodes (15): first_second_check(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples() (+7 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 55 - "sfx_events"
Cohesion: 0.22
Nodes (6): sfx_events(), full_pictures(), _board(), test_board_pictures_attached(), test_sfx_full(), test_story_sound_wins_its_moment()

### Community 56 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

### Community 57 - "choose_images"
Cohesion: 0.21
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 58 - "json"
Cohesion: 0.06
Nodes (26): cut_text(), edit_plan(), look_text(), full_formats(), opener_graphic(), rescue_graphics(), approve_candidate(), invent_component() (+18 more)

### Community 59 - "apply_review_fixes"
Cohesion: 0.12
Nodes (10): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full() (+2 more)

### Community 60 - "full_props"
Cohesion: 0.22
Nodes (7): full_props(), full_summary(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_full_summary(), test_remotion_props_full()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "gpu.py"
Cohesion: 0.13
Nodes (9): cosy_instruct(), local_voice(), motion_prompt(), split_takes(), spoken_count(), voicestudio_unload(), voicestudio_up(), is_loop_short() (+1 more)

### Community 64 - "gather_pool"
Cohesion: 0.25
Nodes (3): openverse_images(), ov_get(), gather_pool()

### Community 65 - "test_ai_modes.py"
Cohesion: 0.12
Nodes (16): ask_brain(), ask_number(), configure_brain(), normalize_brain(), other_ai(), fake_providers(), claude(), reply() (+8 more)

### Community 66 - "clean_graphic"
Cohesion: 0.29
Nodes (6): clean_graphic(), coords(), is_num(), review_fixes(), test_review_fix_kinds(), test_clean_question_and_kinetic()

### Community 69 - "_fake_planning"
Cohesion: 0.17
Nodes (6): _fake_planning(), ask(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 70 - "paint_opener_start"
Cohesion: 0.22
Nodes (4): fix_opener_graphic(), paint_opener_start(), weak_opener_graphic(), test_weak_opener_graphic_fixes_then_handoff()

### Community 71 - "test_full_scenes.py"
Cohesion: 0.09
Nodes (20): clean_full(), number_figures(), show_number(), test_clean_full_board(), test_clean_full_custom_and_skin(), test_clean_full_document(), test_clean_full_journey(), test_clean_full_keeps_thing() (+12 more)

### Community 72 - "re"
Cohesion: 0.09
Nodes (17): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+9 more)

### Community 73 - "ask_ai"
Cohesion: 0.09
Nodes (21): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), run_codex(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_codex_failure_is_bounded() (+13 more)

### Community 74 - "moss_images"
Cohesion: 0.40
Nodes (3): comfy_call(), moss_graph(), moss_images()

### Community 75 - "drawn_thumbnail"
Cohesion: 0.31
Nodes (7): drawn_thumbnail(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so(), test_thumbnail_uses_the_real_photo()

### Community 76 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 77 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

## Knowledge Gaps
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `audio_mix.py`, `shutil`, `footage.py`, `render_remotion`, `local_clips`, `edit_project.py`, `frame_render.py`, `full_cues`, `plan_rules.py`, `quality_check`, `test_blender_render.py`, `image_sources.py`, `main`, `local_job`, `test_first_second.py`, `sfx_events`, `choose_images`, `json`, `apply_review_fixes`, `full_props`, `gpu.py`, `paint_opener_start`, `re`, `ask_ai`, `moss_images`, `drawn_thumbnail`, `make_paper`, `captions`, `srt`, `wants_remotion`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `build_scene.py`, `json`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.12682926829268293 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `test_pictures_first.py`, `test_style.py`, `words_of`, `audio_mix.py`, `shutil`, `test_rules.py`, `picture_pool.py`, `test_blender_scene.py`, `plan_rules.py`, `test_story.py`, `quality_check`, `clean_look`, `test_topic_ideas.py`, `limit_style`, `main`, `json`, `clean_graphic`, `_fake_planning`, `test_full_scenes.py`, `re`, `ask_ai`, `limit_full`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14616755793226383 - nodes in this community are weakly interconnected._
- **Should `test_style.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13970588235294118 - nodes in this community are weakly interconnected._