# Graph Report - ShortsMaker  (2026-11-05)

## Corpus Check
- 140 files · ~166,443 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2233 nodes · 6173 edges · 99 communities (82 shown, 17 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 135 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cd254160`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- load_pool
- test_blender_scene.py
- split_make_shorts.py
- render_remotion
- code_custom_scenes
- test_blender_render.py
- guarded.tsx
- k
- test_h3_handoff.py
- drawn_opener.py
- h3_run.py
- gather_pool
- test_rules.py
- Journey.tsx
- toolkit.tsx
- json
- write_scripts
- gen.py
- core.mjs
- extra_sources.py
- make
- makeKit
- drawn_thumbnail
- paint_instead
- frame_maker
- captions
- sfx_events
- look.py
- parts.py
- OpeningRulesTests
- owner
- templates.py
- use
- make_paper
- full/types.ts
- main
- Paper
- lint_custom_code
- build_scene.py
- Short.tsx
- textures.mjs
- full_cues
- re
- invent_component
- Halftone.tsx
- trim_borders
- trend_research
- fake_ai
- test_story.py
- audio_mix.py
- fetch
- kit.mjs
- RetentionTests
- retention.py
- render
- ReliabilityTests
- style_library
- run_agy
- bean.mjs
- gpu.py
- main
- brand_images
- media_command
- visual_review
- dexter.mjs
- kit_parts.mjs
- test_first_second.py
- apply_review_fixes
- test_full_scenes.py
- qwen_voice.py
- ask_ai
- pathlib
- audio_library.py
- Custom3.tsx
- speak
- ffmpeg
- edit_plan
- full_props
- test_style.py
- apply_look_scenes
- MediaTests
- MetadataTests
- finish_render
- PreflightTests
- MarkTests
- StoryPacingTests
- choose_images
- quality_check
- test_blender_plan.py
- FeedbackTests
- get_image
- apply_metadata
- test_story_sound_library
- BlenderFailed
- limit_style
- math

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 64 edges
3. `write_scripts()` - 54 edges
4. `ask_ai()` - 48 edges
5. `MediaTests` - 33 edges
6. `main()` - 32 edges
7. `skinOf()` - 31 edges
8. `clamp()` - 29 edges
9. `Paper()` - 27 edges
10. `choose_images()` - 27 edges

## Surprising Connections (you probably didn't know these)
- `test_numbers()` --calls--> `say_number()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_word_counts_match_the_scene_splitter()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_words_keep_what_is_written()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_every_aligned_word_is_in_the_aligner_alphabet()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_solo_brain_selection_options()` --calls--> `ask_brain()`  [EXTRACTED]
  tests/test_package.py → shortsmaker/channel_profiles.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`
- 3-file cycle: `shortsmaker/motion.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`
- 4-file cycle: `shortsmaker/motion.py -> shortsmaker/opening_rules.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`

## Communities (99 total, 17 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.17
Nodes (22): catalog_entries(), catalog_pool(), save_pool(), entry(), film(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+14 more)

### Community 3 - "load_pool"
Cohesion: 0.08
Nodes (13): film_piece(), catalog_text(), clean_pics(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder() (+5 more)

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "render_remotion"
Cohesion: 0.15
Nodes (10): render_remotion(), remotion(), render(), run_remotion_with_fallback(), invent_styles(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback() (+2 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.13
Nodes (15): clean_tsx_code(), code_custom_scenes(), custom_rules(), is_payoff(), look_and_fix(), opener_preflight(), preview_custom(), preview_sheet() (+7 more)

### Community 8 - "test_blender_render.py"
Cohesion: 0.16
Nodes (16): code_version(), peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws() (+8 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.13
Nodes (18): Box, boxAt(), clamp, Connect(), fitCard(), hits(), layoutColumn(), layoutGrid() (+10 more)

### Community 10 - "k"
Cohesion: 0.07
Nodes (3): k, ellPts(), popS()

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.05
Nodes (42): shot_span(), cover_crop(), cut_owner_clip(), h3_problems(), h3_prompt(), h3_prompts(), local_clips(), local_job() (+34 more)

### Community 12 - "drawn_opener.py"
Cohesion: 0.07
Nodes (21): available(), clean_code(), fingerprint(), lint(), make_opener(), missing_parts(), node_run(), review() (+13 more)

### Community 13 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 14 - "gather_pool"
Cohesion: 0.12
Nodes (9): commons_films(), article_images(), commons_search(), thumb_url(), usable_license(), wm_files(), wm_get(), balanced_candidates() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (39): load_rules(), min_real_pictures(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft() (+31 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.21
Nodes (21): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+13 more)

### Community 18 - "json"
Cohesion: 0.12
Nodes (12): local_assets(), media_search_words(), recover_downloads(), approve_candidate(), library_menu(), reject_candidate(), save_candidate(), load() (+4 more)

### Community 19 - "write_scripts"
Cohesion: 0.11
Nodes (26): prepare_topic(), limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai() (+18 more)

### Community 20 - "gen.py"
Cohesion: 0.22
Nodes (5): images(), main(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "extra_sources.py"
Cohesion: 0.37
Nodes (9): candidate(), collection_images(), europeana_images(), loc_images(), pixabay_images(), smithsonian_images(), source_json(), wellcome_images() (+1 more)

### Community 23 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "drawn_thumbnail"
Cohesion: 0.21
Nodes (9): thumbnail_order(), drawn_thumbnail(), test_thumbnail_order_skips_film_and_puts_openers_first(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 26 - "paint_instead"
Cohesion: 0.18
Nodes (4): gemini_images(), to_vertical(), paint_instead(), test_remotion_failure_paints()

### Community 27 - "frame_maker"
Cohesion: 0.09
Nodes (12): ClipReader, draw_card(), draw_graphic(), fit_font(), frame_maker(), frame(), graphic_overlay(), person_card() (+4 more)

### Community 28 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 29 - "sfx_events"
Cohesion: 0.25
Nodes (4): schedule_sounds(), sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 30 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 33 - "owner"
Cohesion: 0.11
Nodes (6): owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "use"
Cohesion: 0.33
Nodes (4): fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 36 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (22): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+14 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "lint_custom_code"
Cohesion: 0.29
Nodes (5): fallback_custom_tsx(), lint_custom_code(), test_custom_code_cannot_load_code_or_use_network(), test_fallback_custom_is_clean(), test_lint_custom_code()

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.13
Nodes (19): Captions(), PersonCard(), Root(), Background(), flashAlpha(), GraphicFor(), Move, Scene (+11 more)

### Community 43 - "textures.mjs"
Cohesion: 0.22
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "full_cues"
Cohesion: 0.12
Nodes (11): scene_cues(), full_cues(), spoken_at(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish(), test_opener_graphic() (+3 more)

### Community 45 - "re"
Cohesion: 0.06
Nodes (24): commercial_queries(), crop_film_bytes(), crop_filter(), film_frames(), shot_moments(), film_ffmpeg(), vault_page(), vault_refresh() (+16 more)

### Community 46 - "invent_component"
Cohesion: 0.13
Nodes (15): invent_component(), attempt(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile() (+7 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "trim_borders"
Cohesion: 0.20
Nodes (5): is_stereo(), trim_borders(), border(), plain(), vertical_image()

### Community 49 - "trend_research"
Cohesion: 0.29
Nodes (4): channel_url(), seed_ideas(), trend_research(), yt_list()

### Community 50 - "fake_ai"
Cohesion: 0.15
Nodes (9): entry_age(), logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel() (+1 more)

### Community 51 - "test_story.py"
Cohesion: 0.05
Nodes (37): sentence_groups(), other_ai(), log_short(), ends_sentence(), first_sentence(), srt(), check_twists(), cold_read() (+29 more)

### Community 53 - "fetch"
Cohesion: 0.11
Nodes (15): archive_ad_films(), archive_films(), duke_films(), nasa_films(), pixabay_films(), archive_images(), nasa_credit(), nasa_images() (+7 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "retention.py"
Cohesion: 0.20
Nodes (11): analyze(), edit_metrics(), load_metrics(), metrics_text(), normalize_metrics(), normalize_reply(), observations(), parse_metric() (+3 more)

### Community 57 - "render"
Cohesion: 0.13
Nodes (11): ducking_filter(), preview_mix(), music_gain(), short_credit(), graphics_count(), drawn_choices(), drawn_payoff(), render() (+3 more)

### Community 59 - "style_library"
Cohesion: 0.11
Nodes (15): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), build() (+7 more)

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "gpu.py"
Cohesion: 0.07
Nodes (14): fills_frame(), graphic_low(), comfy_call(), cosy_instruct(), local_voice(), moss_graph(), moss_images(), spoken_count() (+6 more)

### Community 63 - "main"
Cohesion: 0.05
Nodes (46): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), load_channel(), new_channel(), normalize_brain() (+38 more)

### Community 64 - "brand_images"
Cohesion: 0.19
Nodes (8): brand_films(), brand_images(), brand_page(), BrandImages, settings(), source_enabled(), source_status(), print_source_status()

### Community 65 - "media_command"
Cohesion: 0.17
Nodes (9): freesound_fetch(), freesound_preview(), freesound_results(), import_media(), audition_audio(), download_audio_choices(), media_command(), review_audio_files() (+1 more)

### Community 66 - "visual_review"
Cohesion: 0.14
Nodes (10): clock(), callout_hold(), overlay_notes(), pacing_check(), review_fixes(), visual_review(), drop_unreadable_kinetic(), test_review_is_told_the_drawings_are_deliberate() (+2 more)

### Community 69 - "test_first_second.py"
Cohesion: 0.16
Nodes (15): first_second_check(), review_status(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing() (+7 more)

### Community 70 - "apply_review_fixes"
Cohesion: 0.10
Nodes (12): apply_review_fixes(), rewrite_paint_prompts(), plan_gap_paintings(), ask(), _review_state(), test_auto_fix_graphic(), test_look_check_fixes_code(), test_redraw_failure_paints() (+4 more)

### Community 71 - "test_full_scenes.py"
Cohesion: 0.06
Nodes (34): clean_sound(), short_skin(), rescue_graphics(), clean_full(), word(), clean_graphic(), contains(), coords() (+26 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.14
Nodes (13): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+5 more)

### Community 73 - "ask_ai"
Cohesion: 0.13
Nodes (13): ask_ai(), gemini_model(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash(), test_gemini_timeout_switches_to_flash() (+5 more)

### Community 75 - "audio_library.py"
Cohesion: 0.28
Nodes (13): approved_sound(), audio_metadata(), history_read(), import_audio_file(), record_audio(), select_music(), score(), set_audio_metadata() (+5 more)

### Community 76 - "Custom3.tsx"
Cohesion: 0.39
Nodes (3): clamp, CustomFull, FullProps

### Community 78 - "ffmpeg"
Cohesion: 0.17
Nodes (10): split_takes(), duration(), ffmpeg(), video_encoder(), write_json(), apply(), preview(), save_state() (+2 more)

### Community 79 - "edit_plan"
Cohesion: 0.17
Nodes (6): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 80 - "full_props"
Cohesion: 0.33
Nodes (5): full_props(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_remotion_props_full()

### Community 81 - "test_style.py"
Cohesion: 0.12
Nodes (18): wants_remotion(), candidate_in(), library_snapshot(), plan_with(), ask(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure() (+10 more)

### Community 85 - "finish_render"
Cohesion: 0.11
Nodes (12): full_summary(), full_formats(), opener_graphic(), drawn_answer_problem(), fix_drawn_answer(), fix_opener_graphic(), paint_opener_start(), status_lines() (+4 more)

### Community 89 - "choose_images"
Cohesion: 0.25
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 91 - "quality_check"
Cohesion: 0.25
Nodes (4): quality_check(), length_plan(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 92 - "test_blender_plan.py"
Cohesion: 0.12
Nodes (20): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), plan() (+12 more)

### Community 94 - "get_image"
Cohesion: 0.15
Nodes (8): get_image(), openverse_images(), ov_get(), download_picture(), full_pictures(), _board(), test_board_pictures_attached(), test_sfx_full()

### Community 95 - "apply_metadata"
Cohesion: 0.33
Nodes (3): apply_metadata(), clean_tags(), clean_title()

### Community 96 - "test_story_sound_library"
Cohesion: 0.67
Nodes (3): test_story_sound_library(), fetch(), _tone_wav()

### Community 105 - "math"
Cohesion: 0.17
Nodes (4): make_sfx(), flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

## Knowledge Gaps
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `render_remotion`, `test_blender_render.py`, `test_h3_handoff.py`, `json`, `paint_instead`, `frame_maker`, `captions`, `sfx_events`, `make_paper`, `full_cues`, `test_story.py`, `gpu.py`, `main`, `visual_review`, `apply_review_fixes`, `test_full_scenes.py`, `pathlib`, `audio_library.py`, `speak`, `ffmpeg`, `test_style.py`, `finish_render`, `choose_images`, `math`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12802275960170698 - nodes in this community are weakly interconnected._
- **Why does `MetadataTests` connect `MetadataTests` to `pathlib`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._
- **Why does `gather_pool()` connect `gather_pool` to `brand_images`, `owner`, `visual_review`, `load_pool`, `test_full_scenes.py`, `pathlib`, `re`, `json`, `write_scripts`, `fetch`, `extra_sources.py`, `gpu.py`, `choose_images`, `get_image`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `load_pool` be split into smaller, more focused modules?**
  _Cohesion score 0.08307692307692308 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._