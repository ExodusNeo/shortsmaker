# Graph Report - ShortsMaker  (2026-11-06)

## Corpus Check
- 155 files · ~202,067 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2534 nodes · 6903 edges · 109 communities (83 shown, 26 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 142 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `caf64ce4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_pictures_first.py
- prepare_topic
- invent_component
- split_make_shorts.py
- render_remotion
- code_custom_scenes
- test_full_scenes.py
- guarded.tsx
- k
- test_h3_handoff.py
- shutil
- opener_crew.py
- visual_review
- test_rules.py
- Journey.tsx
- toolkit.tsx
- run_draft
- write_scripts
- gen.py
- .at
- film_piece
- test_edit_project.py
- core.mjs
- Pen
- resume_runs
- frame_maker
- finish_render
- full_cues
- look.py
- parts.py
- OpeningRulesTests
- gather_pool
- templates.py
- pick_channel
- main
- BigNumber.tsx
- main
- Paper
- gpu.py
- build_scene.py
- Short.tsx
- textures.mjs
- scene_cues
- check_twists
- extra_sources.py
- Halftone.tsx
- trim_borders
- test_blender_render.py
- fake_ai
- story_problems
- capture_prompts
- test_opener_crew.py
- kit.mjs
- RetentionTests
- retention.py
- ReliabilityTests
- rewrite_paint_prompts
- run_agy
- opener3d.py
- layout
- test_story.py
- .render_fixture
- telegraph_station.mjs
- audio_mix.py
- uprooted_potatoes.mjs
- kit_parts.mjs
- test_first_second.py
- apply_review_fixes
- clean_full
- qwen_voice.py
- ask_ai
- time
- render
- Opener3D.tsx
- test_style.py
- style_library
- apply_look_scenes
- test_short_credit
- StopPicker
- MediaTests
- MetadataTests
- bean.mjs
- PreflightTests
- MarkTests
- StoryPacingTests
- choose_images
- rescue_graphics
- drawn_opener.py
- test_blender_scene.py
- FeedbackTests
- quality_check
- render
- edit_plan
- potato_pile.mjs
- lint_cutout
- limit_style
- edit_scripts
- test_weak_opener_graphic_fixes_then_handoff
- saved_session
- umbrellas.mjs
- battery.mjs
- json
- telegraph_sounder.mjs
- telegraph_register.mjs
- telegraph_workbench.mjs

## God Nodes (most connected - your core abstractions)
1. `k` - 102 edges
2. `render()` - 64 edges
3. `write_scripts()` - 54 edges
4. `ask_ai()` - 53 edges
5. `makeKit()` - 37 edges
6. `clamp()` - 35 edges
7. `MediaTests` - 35 edges
8. `main()` - 32 edges
9. `skinOf()` - 31 edges
10. `clean()` - 31 edges

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

## Communities (109 total, 26 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (23): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+15 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (30): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+22 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.15
Nodes (24): catalog_entries(), catalog_pool(), save_pool(), entry(), film(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+16 more)

### Community 3 - "prepare_topic"
Cohesion: 0.10
Nodes (13): catalog_text(), clean_pics(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures() (+5 more)

### Community 4 - "invent_component"
Cohesion: 0.13
Nodes (15): invent_component(), attempt(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile() (+7 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "render_remotion"
Cohesion: 0.10
Nodes (14): ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), invent_styles(), style_props() (+6 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.13
Nodes (16): clean_tsx_code(), code_custom_scenes(), custom_rules(), is_payoff(), lint_custom_code(), look_and_fix(), opener_preflight(), preview_custom() (+8 more)

### Community 8 - "test_full_scenes.py"
Cohesion: 0.08
Nodes (7): hex_rgb(), luminance(), short_skin(), crop_film_bytes(), clean_photo(), visual_unique(), test_clean_full_custom_and_skin()

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 10 - "k"
Cohesion: 0.10
Nodes (3): makeKit(), k, ellPts()

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.10
Nodes (30): h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated(), test_flagged_start_picture_is_not_sent() (+22 more)

### Community 12 - "shutil"
Cohesion: 0.15
Nodes (7): code_version(), pixabay_films(), load(), save(), signature(), main(), props_for()

### Community 13 - "opener_crew.py"
Cohesion: 0.10
Nodes (20): clean_code(), minutes(), staging_line(), animal_cutout(), crew(), default_cutout(), kit_hats(), kit_text() (+12 more)

### Community 14 - "visual_review"
Cohesion: 0.15
Nodes (9): clock(), overlay_notes(), pacing_check(), review_fixes(), sound_masking(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.19
Nodes (22): parse_rules(), make(), stop_text(), test_bad_min_pictures_stops(), test_blender_needs_a_build_plan_section(), test_bom_and_crlf_load_the_same(), test_draft_stops(), test_draft_writes_tagged_draft_file() (+14 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.26
Nodes (20): CustomScene(), ExampleOpenerAction(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear() (+12 more)

### Community 18 - "run_draft"
Cohesion: 0.18
Nodes (10): draft_rules(), require_rules(), draft_reply(), run_draft(), test_draft_blender_channel_needs_build_plan(), test_draft_keeps_ai_headings_inside_their_section(), test_draft_never_overwrites(), test_draft_retries_once_then_stops() (+2 more)

### Community 19 - "write_scripts"
Cohesion: 0.12
Nodes (23): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+15 more)

### Community 20 - "gen.py"
Cohesion: 0.22
Nodes (5): images(), main(), t5_encoder(), tts(), video()

### Community 22 - "film_piece"
Cohesion: 0.22
Nodes (5): crop_filter(), film_frames(), film_piece(), shot_moments(), film_ffmpeg()

### Community 23 - "test_edit_project.py"
Cohesion: 0.13
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "core.mjs"
Cohesion: 0.08
Nodes (21): burst(), clamp(), eBounce(), eElastic(), eExpo(), eIn(), eIO(), eOut() (+13 more)

### Community 25 - "Pen"
Cohesion: 0.17
Nodes (7): catmull(), centroid(), densify(), INK, noise1(), idHash(), Pen

### Community 26 - "resume_runs"
Cohesion: 0.23
Nodes (11): begin(), context(), pending(), pending_topics(), read(), update(), finish_short(), record_failure() (+3 more)

### Community 27 - "frame_maker"
Cohesion: 0.09
Nodes (12): ClipReader, draw_card(), draw_graphic(), fit_font(), frame_maker(), frame(), graphic_overlay(), person_card() (+4 more)

### Community 28 - "finish_render"
Cohesion: 0.16
Nodes (10): full_summary(), opener_graphic(), drawn_answer_problem(), first_second_check(), fix_drawn_answer(), fix_opener_graphic(), review_status(), status_lines() (+2 more)

### Community 29 - "full_cues"
Cohesion: 0.06
Nodes (20): schedule_sounds(), sfx_events(), full_props(), full_pictures(), full_cues(), spoken_at(), spoken_span(), _board() (+12 more)

### Community 30 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 33 - "gather_pool"
Cohesion: 0.07
Nodes (13): article_images(), commons_search(), thumb_url(), usable_license(), wm_files(), balanced_candidates(), gather_pool(), owner() (+5 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "pick_channel"
Cohesion: 0.14
Nodes (9): channel_url(), new_channel(), pick_channel(), save_channel(), seed_ideas(), trend_research(), use_channel(), yt_list() (+1 more)

### Community 36 - "main"
Cohesion: 0.11
Nodes (18): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), load_channel(), normalize_brain(), fix_short() (+10 more)

### Community 37 - "BigNumber.tsx"
Cohesion: 0.22
Nodes (13): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+5 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.12
Nodes (29): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+21 more)

### Community 40 - "gpu.py"
Cohesion: 0.05
Nodes (31): call(), fit_start(), frames(), graph(), main(), saved_file(), comfy_call(), cosy_instruct() (+23 more)

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (17): Captions(), PersonCard(), Background(), Card, flashAlpha(), GraphicFor(), Move, Scene (+9 more)

### Community 43 - "textures.mjs"
Cohesion: 0.19
Nodes (20): ellipse(), fibre(), fill(), grainCanvas(), grainOver(), hash(), hatch(), rng() (+12 more)

### Community 44 - "scene_cues"
Cohesion: 0.22
Nodes (8): scene_cues(), read_need(), callout_hold(), test_counter_finishes_before_it_leaves(), test_short_scene_callout_is_placed_so_the_check_passes(), test_graphic_card_hold_duration(), test_person_card_hold_and_exit_gap(), test_scene_hold_padding()

### Community 45 - "check_twists"
Cohesion: 0.47
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 46 - "extra_sources.py"
Cohesion: 0.07
Nodes (31): brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images(), loc_images() (+23 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "trim_borders"
Cohesion: 0.15
Nodes (6): is_stereo(), to_vertical(), trim_borders(), border(), plain(), vertical_image()

### Community 49 - "test_blender_render.py"
Cohesion: 0.09
Nodes (25): thumbnail_order(), BlenderFailed, peaks(), render_clips(), _run(), scene_frames(), drawn_thumbnail(), test_thumbnail_order_skips_film_and_puts_openers_first() (+17 more)

### Community 50 - "fake_ai"
Cohesion: 0.12
Nodes (11): entry_age(), logbook_results(), apply_metadata(), clean_tags(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai() (+3 more)

### Community 51 - "story_problems"
Cohesion: 0.24
Nodes (9): first_sentence(), story_problems(), read(), test_cold_read_verdicts(), test_first_sentence_reads_across_the_cut(), test_no_hook_setting_no_hook_check(), test_story_problems(), test_story_problems_flags_summary_hook() (+1 more)

### Community 52 - "capture_prompts"
Cohesion: 0.20
Nodes (6): load_rules(), min_real_pictures(), capture_prompts(), ask(), test_load_rules_sets_session(), test_strange_history_prompts_unchanged()

### Community 53 - "test_opener_crew.py"
Cohesion: 0.12
Nodes (18): spread_out(), assemble(), check_staging(), blind_ok(), fake(), short(), staging(), test_a_failed_part_falls_back_to_its_substitute() (+10 more)

### Community 54 - "kit.mjs"
Cohesion: 0.09
Nodes (27): bounds(), EDGE, flat, fx, PAD_TOP, PAD_X, paintAll(), STEPS (+19 more)

### Community 56 - "retention.py"
Cohesion: 0.20
Nodes (11): analyze(), edit_metrics(), load_metrics(), metrics_text(), normalize_metrics(), normalize_reply(), observations(), parse_metric() (+3 more)

### Community 59 - "rewrite_paint_prompts"
Cohesion: 0.14
Nodes (7): rewrite_paint_prompts(), plan_gap_paintings(), ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts(), test_scene_without_picture_or_prompt_gets_painted_not_reused()

### Community 60 - "run_agy"
Cohesion: 0.18
Nodes (7): argon_out(), quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "opener3d.py"
Cohesion: 0.07
Nodes (30): box_of(), clean(), dress(), front_door(), half_width(), in_order(), inside(), nudge() (+22 more)

### Community 62 - "layout"
Cohesion: 0.40
Nodes (4): layout(), place_thing(), put(), lum()

### Community 63 - "test_story.py"
Cohesion: 0.10
Nodes (12): sentence_groups(), log_short(), vault_page(), vault_refresh(), ends_sentence(), srt(), test_sentence_ends_include_curly_quotes_and_ellipsis(), scenes() (+4 more)

### Community 66 - "audio_mix.py"
Cohesion: 0.11
Nodes (10): ass_time(), caption_lines(), caption_size(), captions(), freesound_fetch(), freesound_preview(), freesound_results(), make_sfx() (+2 more)

### Community 69 - "test_first_second.py"
Cohesion: 0.19
Nodes (13): swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once() (+5 more)

### Community 70 - "apply_review_fixes"
Cohesion: 0.15
Nodes (8): apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_redraw_failure_paints(), test_review_redraws_custom()

### Community 71 - "clean_full"
Cohesion: 0.08
Nodes (24): clean_sound(), limit_sounds(), clean_full(), word(), clean_graphic(), contains(), coords(), fill_money_graphics() (+16 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.13
Nodes (13): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+5 more)

### Community 73 - "ask_ai"
Cohesion: 0.10
Nodes (17): ask_ai(), gemini_model(), direct_scripts(), test_every_ai_gets_the_pipeline_preamble_once(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high() (+9 more)

### Community 74 - "time"
Cohesion: 0.15
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 75 - "render"
Cohesion: 0.05
Nodes (48): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+40 more)

### Community 76 - "Opener3D.tsx"
Cohesion: 0.07
Nodes (50): aim(), BOOKS, Box(), Building(), Burst(), calculateOpener3D(), CameraRig(), Card() (+42 more)

### Community 77 - "test_style.py"
Cohesion: 0.12
Nodes (18): wants_remotion(), candidate_in(), library_snapshot(), plan_with(), ask(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure() (+10 more)

### Community 78 - "style_library"
Cohesion: 0.11
Nodes (15): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), build() (+7 more)

### Community 85 - "bean.mjs"
Cohesion: 0.35
Nodes (9): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), SKIN (+1 more)

### Community 89 - "choose_images"
Cohesion: 0.19
Nodes (14): choose_images(), download_picture(), recover_downloads(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded() (+6 more)

### Community 90 - "rescue_graphics"
Cohesion: 0.20
Nodes (6): full_formats(), rescue_graphics(), article_text(), fact_check(), test_fact_check_drops_full(), test_rescue_respects_caps()

### Community 91 - "drawn_opener.py"
Cohesion: 0.06
Nodes (26): available(), blind_read(), fingerprint(), lint(), look_dir(), make_opener(), node_run(), opener_role() (+18 more)

### Community 92 - "test_blender_scene.py"
Cohesion: 0.07
Nodes (41): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), plan() (+33 more)

### Community 94 - "quality_check"
Cohesion: 0.33
Nodes (3): quality_check(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 97 - "render"
Cohesion: 0.15
Nodes (7): sheet_times(), blends(), render(), sheet(), sheet_times(), test_a_cutout_that_melts_into_the_wall_goes_back(), test_the_preview_sees_every_shot()

### Community 98 - "edit_plan"
Cohesion: 0.14
Nodes (7): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 100 - "lint_cutout"
Cohesion: 0.25
Nodes (6): missing_parts(), lint_cutout(), test_kit_animals_must_be_used(), test_a_knock_needs_a_closed_door_and_a_messenger_his_letter(), test_hold_counts_as_drawing_the_letter_and_scenery_stays_3d(), test_lint_needs_draw()

### Community 105 - "edit_scripts"
Cohesion: 0.11
Nodes (13): other_ai(), cold_read(), edit_scripts(), length_plan(), narration_lines(), recheck_final_scripts(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_gemini_modes_choose_codex_and_keep_editor_choice() (+5 more)

### Community 106 - "test_weak_opener_graphic_fixes_then_handoff"
Cohesion: 0.17
Nodes (6): weak_opener_graphic(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), test_weak_opener_graphic_fixes_then_handoff(), use()

### Community 108 - "saved_session"
Cohesion: 0.21
Nodes (10): fake_providers(), claude(), reply(), saved_session(), test_all_modes_route_writer_editor_and_reader(), ask(), test_every_mode_can_continue_through_two_exhausted_ais(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty() (+2 more)

### Community 111 - "json"
Cohesion: 0.06
Nodes (24): commercial_queries(), commons_films(), import_media(), local_assets(), media_search_words(), settings(), audition_audio(), download_audio_choices() (+16 more)

## Knowledge Gaps
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ReliabilityTests` connect `ReliabilityTests` to `test_full_scenes.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12564102564102564 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `render_remotion`, `test_full_scenes.py`, `shutil`, `visual_review`, `resume_runs`, `frame_maker`, `finish_render`, `full_cues`, `main`, `gpu.py`, `scene_cues`, `trim_borders`, `test_blender_render.py`, `rewrite_paint_prompts`, `test_story.py`, `audio_mix.py`, `test_style.py`, `choose_images`, `rescue_graphics`, `json`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Should `prepare_topic` be split into smaller, more focused modules?**
  _Cohesion score 0.10144927536231885 - nodes in this community are weakly interconnected._
- **Why does `ask_ai()` connect `ask_ai` to `test_pictures_first.py`, `invent_component`, `code_custom_scenes`, `test_full_scenes.py`, `opener_crew.py`, `visual_review`, `run_draft`, `write_scripts`, `finish_render`, `pick_channel`, `gpu.py`, `check_twists`, `fake_ai`, `retention.py`, `rewrite_paint_prompts`, `run_agy`, `apply_review_fixes`, `choose_images`, `rescue_graphics`, `drawn_opener.py`, `edit_scripts`, `saved_session`, `json`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Should `invent_component` be split into smaller, more focused modules?**
  _Cohesion score 0.1341991341991342 - nodes in this community are weakly interconnected._
- **Should `split_make_shorts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._