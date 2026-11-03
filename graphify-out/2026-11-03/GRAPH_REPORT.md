# Graph Report - ShortsMaker  (2026-11-03)

## Corpus Check
- 140 files · ~161,026 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2187 nodes · 6044 edges · 102 communities (84 shown, 18 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 135 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f1996e26`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Cards.tsx
- test_pictures_first.py
- prepare_topic
- test_blender_scene.py
- split_make_shorts.py
- write_json
- code_custom_scenes
- blender_render.py
- guarded.tsx
- k
- test_h3_handoff.py
- test_style.py
- json
- render_remotion
- test_rules.py
- Journey.tsx
- skinOf
- apply_review_fixes
- write_scripts
- Local GPU Worker
- core.mjs
- local_clips
- make
- makeKit
- MapCard.tsx
- render
- frame_maker
- rewrite_paint_prompts
- h3_run.py
- look.py
- parts.py
- OpeningRulesTests
- owner
- templates.py
- use
- test_story.py
- BigNumber.tsx
- main
- toolkit.tsx
- subprocess
- build_scene.py
- Short.tsx
- textures.mjs
- sfx_events
- test_topic_ideas.py
- extra_sources.py
- kit.ts
- trim_borders
- approve_candidate
- fake_ai
- QuestionBeat.tsx
- invent_component
- re
- kit.mjs
- RetentionTests
- writing.py
- paint_instead
- ReliabilityTests
- gather_pool
- run_agy
- bean.mjs
- clean_look
- popS
- fetch
- style_library
- visual_review
- dexter.mjs
- kit_parts.mjs
- test_first_second.py
- words_of
- clean_full
- time
- ask_ai
- test_full_scenes.py
- audio_library.py
- Custom3.tsx
- captions
- rescue_graphics
- edit_plan
- full_cues
- clean_photo
- main
- MediaTests
- MetadataTests
- finish_render
- PreflightTests
- MarkTests
- StoryPacingTests
- choose_images
- first_second_check
- quality_check
- test_blender_plan.py
- FeedbackTests
- recover_downloads
- full_props
- test_story_sound_library
- catalog_entries
- run_remotion_with_fallback
- style_props
- limit_style
- test_short_credit

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 61 edges
3. `write_scripts()` - 53 edges
4. `ask_ai()` - 48 edges
5. `MediaTests` - 33 edges
6. `main()` - 32 edges
7. `skinOf()` - 31 edges
8. `clamp()` - 27 edges
9. `Paper()` - 27 edges
10. `ellPts()` - 26 edges

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
- 3-file cycle: `shortsmaker/motion.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`
- 4-file cycle: `shortsmaker/motion.py -> shortsmaker/opening_rules.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py`

## Communities (102 total, 18 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.17
Nodes (15): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, clamp01(), H, W, Cut (+7 more)

### Community 1 - "Cards.tsx"
Cohesion: 0.23
Nodes (21): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+13 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.16
Nodes (23): catalog_pool(), clean_pics(), save_pool(), entry(), film(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+15 more)

### Community 3 - "prepare_topic"
Cohesion: 0.14
Nodes (9): catalog_text(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures(), prepare_topic(), usable() (+1 more)

### Community 4 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "write_json"
Cohesion: 0.14
Nodes (12): save_context(), split_takes(), spoken_count(), duration(), ffmpeg(), video_encoder(), write_json(), apply() (+4 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.13
Nodes (14): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), opener_preflight(), preview_custom() (+6 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.14
Nodes (17): Box, boxAt(), clamp, fitCard(), hits(), layoutColumn(), layoutGrid(), layoutRow() (+9 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "test_style.py"
Cohesion: 0.14
Nodes (10): wants_remotion(), apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics() (+2 more)

### Community 13 - "json"
Cohesion: 0.09
Nodes (15): channel_url(), new_channel(), pick_channel(), save_channel(), trend_research(), yt_list(), comfy_call(), moss_graph() (+7 more)

### Community 14 - "render_remotion"
Cohesion: 0.20
Nodes (7): ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), test_ink_silhouette(), test_make_paper()

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (40): load_rules(), min_real_pictures(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft() (+32 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.16
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "skinOf"
Cohesion: 0.21
Nodes (21): CustomScene(), ExampleChain(), ExampleEvidence(), ExampleOpenerAction(), Custom0(), Custom1(), Custom2(), Custom3() (+13 more)

### Community 18 - "apply_review_fixes"
Cohesion: 0.14
Nodes (9): apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full(), test_redraw_failure_paints() (+1 more)

### Community 19 - "write_scripts"
Cohesion: 0.11
Nodes (25): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+17 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "core.mjs"
Cohesion: 0.11
Nodes (21): burst(), clamp(), eBack(), eBounce(), eElastic(), eExpo(), eIn(), eIO() (+13 more)

### Community 22 - "local_clips"
Cohesion: 0.11
Nodes (12): cosy_instruct(), cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt() (+4 more)

### Community 23 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "MapCard.tsx"
Cohesion: 0.16
Nodes (7): Pin(), clamp, interpolateColor(), MapCard(), topo, Root(), ShortProps

### Community 26 - "render"
Cohesion: 0.09
Nodes (13): make_sfx(), short_credit(), graphics_count(), is_loop_short(), srt(), drawn_choices(), render(), save_state() (+5 more)

### Community 27 - "frame_maker"
Cohesion: 0.06
Nodes (16): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), flash_alpha(), frame_maker(), frame() (+8 more)

### Community 28 - "rewrite_paint_prompts"
Cohesion: 0.18
Nodes (5): rewrite_paint_prompts(), ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 29 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 30 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 32 - "OpeningRulesTests"
Cohesion: 0.06
Nodes (13): make_opener(), review(), sheet_times(), write(), fake_ai(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused() (+5 more)

### Community 33 - "owner"
Cohesion: 0.11
Nodes (7): owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits(), test_pool_roundtrip()

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "use"
Cohesion: 0.33
Nodes (4): fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 36 - "test_story.py"
Cohesion: 0.06
Nodes (31): sentence_groups(), log_short(), first_sentence(), check_twists(), cold_read(), edit_scripts(), length_plan(), narration_lines() (+23 more)

### Community 37 - "BigNumber.tsx"
Cohesion: 0.27
Nodes (11): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+3 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "toolkit.tsx"
Cohesion: 0.12
Nodes (30): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+22 more)

### Community 40 - "subprocess"
Cohesion: 0.10
Nodes (6): music_gain(), node_run(), main(), props_for(), look(), test_music_gain_evens_out_tracks()

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.14
Nodes (21): Captions(), clamp, HookTitle(), PersonCard(), SubscribeCta(), Background(), Card, flashAlpha() (+13 more)

### Community 43 - "textures.mjs"
Cohesion: 0.25
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "sfx_events"
Cohesion: 0.25
Nodes (4): schedule_sounds(), sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 45 - "test_topic_ideas.py"
Cohesion: 0.15
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 46 - "extra_sources.py"
Cohesion: 0.17
Nodes (15): brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images(), loc_images() (+7 more)

### Community 47 - "kit.ts"
Cohesion: 0.15
Nodes (27): InventedLook(), CAPTION_TOP, drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas() (+19 more)

### Community 48 - "trim_borders"
Cohesion: 0.20
Nodes (5): is_stereo(), trim_borders(), border(), plain(), vertical_image()

### Community 49 - "approve_candidate"
Cohesion: 0.23
Nodes (9): approve_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_candidate_names_unique_across_kinds() (+1 more)

### Community 50 - "fake_ai"
Cohesion: 0.15
Nodes (9): entry_age(), logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel() (+1 more)

### Community 51 - "QuestionBeat.tsx"
Cohesion: 0.27
Nodes (5): FONT, theme, Word, CLAMP, KineticTitle()

### Community 52 - "invent_component"
Cohesion: 0.11
Nodes (17): clean_style_code(), invent_component(), attempt(), invent_styles(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview() (+9 more)

### Community 53 - "re"
Cohesion: 0.06
Nodes (24): available(), clean_code(), fingerprint(), lint(), archive_ad_films(), archive_films(), crop_film_bytes(), crop_filter() (+16 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "writing.py"
Cohesion: 0.09
Nodes (9): analyze(), normalize_reply(), observations(), report_text(), scenes_from_plan(), seconds(), apply_metadata(), clean_tags() (+1 more)

### Community 57 - "paint_instead"
Cohesion: 0.18
Nodes (4): gemini_images(), to_vertical(), paint_instead(), test_remotion_failure_paints()

### Community 59 - "gather_pool"
Cohesion: 0.12
Nodes (8): commercial_queries(), article_images(), commons_search(), openverse_images(), thumb_url(), wm_files(), balanced_candidates(), gather_pool()

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "clean_look"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 64 - "fetch"
Cohesion: 0.12
Nodes (12): commons_films(), nasa_films(), archive_images(), get_image(), nasa_images(), nasa_search(), on_topic(), ov_get() (+4 more)

### Community 65 - "style_library"
Cohesion: 0.20
Nodes (8): style_library(), style_rules(), write_style_index(), build(), add(), main(), test_library_entries_have_fields(), test_write_style_index_is_deterministic()

### Community 66 - "visual_review"
Cohesion: 0.20
Nodes (8): clock(), overlay_notes(), pacing_check(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 69 - "test_first_second.py"
Cohesion: 0.23
Nodes (11): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once(), test_opener_must_be_a_later_real_picture() (+3 more)

### Community 70 - "words_of"
Cohesion: 0.14
Nodes (13): clean_sound(), limit_sounds(), graphic_low(), word(), clean_graphic(), contains(), fill_money_graphics(), is_person_portrait() (+5 more)

### Community 71 - "clean_full"
Cohesion: 0.12
Nodes (14): short_skin(), clean_full(), coords(), is_num(), number_figures(), show_number(), test_clean_full_board(), test_clean_full_custom_and_skin() (+6 more)

### Community 72 - "time"
Cohesion: 0.11
Nodes (14): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+6 more)

### Community 73 - "ask_ai"
Cohesion: 0.11
Nodes (15): seed_ideas(), ask_ai(), gemini_model(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high(), test_fake_reaches_callers() (+7 more)

### Community 74 - "test_full_scenes.py"
Cohesion: 0.10
Nodes (3): hex_rgb(), luminance(), storyboard()

### Community 75 - "audio_library.py"
Cohesion: 0.13
Nodes (25): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+17 more)

### Community 76 - "Custom3.tsx"
Cohesion: 0.33
Nodes (6): appear(), CalloutTag(), clamp, FlowArrow(), CustomFull, FullProps

### Community 77 - "captions"
Cohesion: 0.16
Nodes (7): ass_time(), caption_lines(), captions(), styled(), speak(), tts(), ass_colour()

### Community 78 - "rescue_graphics"
Cohesion: 0.20
Nodes (6): full_formats(), rescue_graphics(), article_text(), fact_check(), test_fact_check_drops_full(), test_rescue_respects_caps()

### Community 79 - "edit_plan"
Cohesion: 0.17
Nodes (6): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 80 - "full_cues"
Cohesion: 0.12
Nodes (12): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish() (+4 more)

### Community 81 - "clean_photo"
Cohesion: 0.22
Nodes (4): clean_photo(), contact_sheets(), visual_unique(), mark_details()

### Community 82 - "main"
Cohesion: 0.06
Nodes (40): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), load_channel(), normalize_brain(), use_channel() (+32 more)

### Community 85 - "finish_render"
Cohesion: 0.11
Nodes (14): full_summary(), opening_brief(), opener_graphic(), redraw_custom(), drawn_answer_problem(), fix_drawn_answer(), fix_opener_graphic(), paint_opener_start() (+6 more)

### Community 89 - "choose_images"
Cohesion: 0.25
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 90 - "first_second_check"
Cohesion: 0.33
Nodes (4): first_second_check(), review_status(), test_failed_preview_clears_previous_opener_score(), test_opener_prompt_shows_each_scenes_line_and_picture()

### Community 91 - "quality_check"
Cohesion: 0.33
Nodes (3): quality_check(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 92 - "test_blender_plan.py"
Cohesion: 0.05
Nodes (44): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+36 more)

### Community 95 - "full_props"
Cohesion: 0.20
Nodes (8): full_props(), full_pictures(), _board(), _jpg(), test_board_pictures_attached(), test_custom_cues_props_and_pictures(), test_remotion_props_full(), test_sfx_full()

### Community 96 - "test_story_sound_library"
Cohesion: 0.67
Nodes (3): test_story_sound_library(), fetch(), _tone_wav()

### Community 99 - "run_remotion_with_fallback"
Cohesion: 0.29
Nodes (4): run_remotion_with_fallback(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_swap_inventions()

## Knowledge Gaps
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `veo_handoff()` connect `local_clips` to `h3_run.py`, `test_full_scenes.py`, `test_h3_handoff.py`, `json`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `prepare_topic` be split into smaller, more focused modules?**
  _Cohesion score 0.1437908496732026 - nodes in this community are weakly interconnected._
- **Why does `OpeningRulesTests` connect `OpeningRulesTests` to `test_full_scenes.py`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `write_json`, `test_style.py`, `json`, `render_remotion`, `local_clips`, `frame_maker`, `subprocess`, `sfx_events`, `paint_instead`, `visual_review`, `words_of`, `test_full_scenes.py`, `audio_library.py`, `captions`, `rescue_graphics`, `full_cues`, `clean_photo`, `main`, `finish_render`, `choose_images`, `test_blender_plan.py`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Should `write_json` be split into smaller, more focused modules?**
  _Cohesion score 0.14210526315789473 - nodes in this community are weakly interconnected._
- **Should `code_custom_scenes` be split into smaller, more focused modules?**
  _Cohesion score 0.12666666666666668 - nodes in this community are weakly interconnected._