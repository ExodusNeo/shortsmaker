# Graph Report - ShortsMaker  (2026-11-01)

## Corpus Check
- 137 files · ~158,640 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .canvas 1, .ipynb 1)

## Summary
- 2157 nodes · 5940 edges · 110 communities (87 shown, 23 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 134 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4fc8ceb6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- catalog_pool
- direct_scripts
- plan_with
- split_make_shorts.py
- scene_repair.py
- code_custom_scenes
- json
- guarded.tsx
- k
- test_h3_handoff.py
- check_twists
- style_library
- render_remotion
- test_rules.py
- Journey.tsx
- toolkit.tsx
- apply_review_fixes
- write_scripts
- Local GPU Worker
- core.mjs
- local_clips
- make
- makeKit
- write_json
- render
- frame_maker
- rewrite_paint_prompts
- h3_run.py
- math
- parts.py
- OpeningRulesTests
- owner
- templates.py
- use
- story_problems
- full/types.ts
- main
- Paper
- drawn_opener.py
- Shots
- Short.tsx
- textures.mjs
- sfx_events
- image_sources.py
- extra_sources.py
- Halftone.tsx
- io
- pick_channel
- fake_ai
- main
- invent_component
- re
- kit.mjs
- RetentionTests
- retention.py
- make_opener
- ReliabilityTests
- gather_pool
- run_agy
- bean.mjs
- story_sound
- popS
- subprocess
- edit_scripts
- finish_render
- dexter.mjs
- kit_parts.mjs
- test_first_second.py
- words_of
- clean_full
- qwen_voice.py
- ask_ai
- test_full_scenes.py
- audio_library.py
- visual_review
- captions
- ref_remotion
- edit_plan
- full_cues
- capture_prompts
- other_ai
- MediaTests
- MetadataTests
- opener_graphic
- test_drawn_opener_renders_and_is_reused
- MarkTests
- StoryPacingTests
- test_pictures_first.py
- cold_read
- make_paper
- test_blender_plan.py
- FeedbackTests
- plan_with
- full_props
- trim_borders
- apply_metadata
- vault_page
- test_style.py
- rescue_graphics
- .render_fixture
- make_sfx
- limit_style
- media_command
- spoken_count
- prune_cache
- test_short_credit
- StopPicker
- ffmpeg

## God Nodes (most connected - your core abstractions)
1. `k` - 81 edges
2. `render()` - 61 edges
3. `write_scripts()` - 52 edges
4. `ask_ai()` - 47 edges
5. `MediaTests` - 33 edges
6. `main()` - 32 edges
7. `skinOf()` - 29 edges
8. `clamp()` - 27 edges
9. `ellPts()` - 26 edges
10. `choose_images()` - 26 edges

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

## Communities (110 total, 23 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (21): InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "catalog_pool"
Cohesion: 0.14
Nodes (21): catalog_entries(), catalog_pool(), clean_pics(), save_pool(), entry(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+13 more)

### Community 3 - "direct_scripts"
Cohesion: 0.14
Nodes (7): catalog_text(), is_usable(), pictures_of(), pool_folder(), preflight_pictures(), usable(), direct_scripts()

### Community 4 - "plan_with"
Cohesion: 0.14
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "scene_repair.py"
Cohesion: 0.12
Nodes (7): review_status(), storyboard(), apply(), preview(), load_state(), save_state(), test_state_roundtrip_full_pics()

### Community 7 - "code_custom_scenes"
Cohesion: 0.13
Nodes (12): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), redraw_custom() (+4 more)

### Community 8 - "json"
Cohesion: 0.07
Nodes (22): main(), code_version(), channel_url(), trend_research(), yt_list(), pixabay_films(), comfy_call(), moss_graph() (+14 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (23): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+15 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "check_twists"
Cohesion: 0.47
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 13 - "style_library"
Cohesion: 0.11
Nodes (15): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), build() (+7 more)

### Community 14 - "render_remotion"
Cohesion: 0.12
Nodes (12): short_skin(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), invent_styles(), style_props(), swap_inventions() (+4 more)

### Community 15 - "test_rules.py"
Cohesion: 0.13
Nodes (30): parse_rules(), draft_reply(), make(), run_draft(), stop_text(), test_bad_min_pictures_stops(), test_blender_needs_a_build_plan_section(), test_bom_and_crlf_load_the_same() (+22 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 18 - "apply_review_fixes"
Cohesion: 0.13
Nodes (10): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full() (+2 more)

### Community 19 - "write_scripts"
Cohesion: 0.11
Nodes (26): prepare_topic(), limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai() (+18 more)

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
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "makeKit"
Cohesion: 0.16
Nodes (9): makeKit(), catmull(), centroid(), densify(), eOut(), INK, noise1(), idHash() (+1 more)

### Community 25 - "write_json"
Cohesion: 0.29
Nodes (11): begin(), context(), pack(), pending(), read(), save_context(), update(), finish_short() (+3 more)

### Community 26 - "render"
Cohesion: 0.09
Nodes (11): gemini_images(), short_credit(), graphics_count(), to_vertical(), paint_instead(), srt(), drawn_choices(), render() (+3 more)

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (14): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+6 more)

### Community 28 - "rewrite_paint_prompts"
Cohesion: 0.18
Nodes (5): rewrite_paint_prompts(), ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 29 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 30 - "math"
Cohesion: 0.16
Nodes (6): collection(), ink_lines(), linear(), material(), setup(), radians()

### Community 31 - "parts.py"
Cohesion: 0.16
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 33 - "owner"
Cohesion: 0.14
Nodes (4): owner(), _fake_planning(), test_director_prompt_mentions_full(), film()

### Community 34 - "templates.py"
Cohesion: 0.17
Nodes (15): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge() (+7 more)

### Community 35 - "use"
Cohesion: 0.33
Nodes (4): fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 36 - "story_problems"
Cohesion: 0.20
Nodes (10): first_sentence(), recheck_final_scripts(), story_problems(), read(), test_cold_read_verdicts(), test_first_sentence_reads_across_the_cut(), test_no_hook_setting_no_hook_check(), test_story_problems() (+2 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (21): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+13 more)

### Community 38 - "main"
Cohesion: 0.18
Nodes (4): keyvis(), main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "drawn_opener.py"
Cohesion: 0.14
Nodes (7): available(), clean_code(), fingerprint(), lint(), node_run(), look(), test_lint()

### Community 41 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.16
Nodes (18): Captions(), HookTitle(), PersonCard(), SubscribeCta(), Background(), flashAlpha(), GraphicFor(), Move (+10 more)

### Community 43 - "textures.mjs"
Cohesion: 0.25
Nodes (19): ellipse(), fibre(), fill(), grainCanvas(), hash(), hatch(), rng(), stroke() (+11 more)

### Community 44 - "sfx_events"
Cohesion: 0.22
Nodes (5): schedule_sounds(), sfx_events(), test_sfx_full(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 45 - "image_sources.py"
Cohesion: 0.09
Nodes (17): commons_films(), nasa_films(), nasa_images(), nasa_search(), on_topic(), usable_license(), clash(), fetch_ideas() (+9 more)

### Community 46 - "extra_sources.py"
Cohesion: 0.07
Nodes (30): brand_films(), brand_images(), brand_page(), BrandImages, candidate(), collection_images(), europeana_images(), loc_images() (+22 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "io"
Cohesion: 0.14
Nodes (7): unpack(), person_card(), clean_photo(), vertical_image(), contact_sheets(), visual_unique(), mark_details()

### Community 49 - "pick_channel"
Cohesion: 0.17
Nodes (7): new_channel(), pick_channel(), save_channel(), use_channel(), draft_rules(), require_rules(), test_new_channel_stops_for_review()

### Community 50 - "fake_ai"
Cohesion: 0.14
Nodes (10): entry_age(), logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_catalog_empty_pool_no_ai(), test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list() (+2 more)

### Community 51 - "main"
Cohesion: 0.12
Nodes (17): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), load_channel(), normalize_brain(), fix_short() (+9 more)

### Community 52 - "invent_component"
Cohesion: 0.13
Nodes (16): invent_component(), attempt(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_candidate_names_unique_across_kinds(), test_failed_invention_keeps_the_others() (+8 more)

### Community 53 - "re"
Cohesion: 0.08
Nodes (17): archive_ad_films(), archive_films(), crop_film_bytes(), crop_filter(), duke_films(), film_frames(), film_piece(), shot_moments() (+9 more)

### Community 54 - "kit.mjs"
Cohesion: 0.15
Nodes (10): C, H, W, args(), exposure(), run(), SKIN, cam (+2 more)

### Community 56 - "retention.py"
Cohesion: 0.25
Nodes (6): retention_observations(), analyze(), normalize_reply(), report_text(), scenes_from_plan(), seconds()

### Community 57 - "make_opener"
Cohesion: 0.24
Nodes (5): make_opener(), review(), sheet_times(), write(), opening_brief()

### Community 59 - "gather_pool"
Cohesion: 0.10
Nodes (11): article_images(), commons_search(), thumb_url(), wm_files(), balanced_candidates(), gather_pool(), load_pool(), stubbed (+3 more)

### Community 60 - "run_agy"
Cohesion: 0.22
Nodes (6): quota_exhausted(), run_agy(), run_codex(), test_codex_failure_is_bounded(), test_codex_uses_subscription_stdin_and_read_only_images(), test_run_agy_flags_and_boundaries()

### Community 61 - "bean.mjs"
Cohesion: 0.40
Nodes (8): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), lightBands()

### Community 62 - "story_sound"
Cohesion: 0.14
Nodes (8): music_gain(), speak(), story_sound(), tts(), test_music_gain_evens_out_tracks(), test_story_sound_library(), fetch(), _tone_wav()

### Community 65 - "edit_scripts"
Cohesion: 0.17
Nodes (7): edit_scripts(), length_plan(), narration_lines(), test_all_modes_route_writer_editor_and_reader(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules(), test_failed_second_read_clears_old_verdict()

### Community 66 - "finish_render"
Cohesion: 0.14
Nodes (8): drawn_answer_problem(), pacing_check(), quality_check(), status_lines(), weak_opener_graphic(), finish_render(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 69 - "test_first_second.py"
Cohesion: 0.18
Nodes (14): first_second_check(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture() (+6 more)

### Community 70 - "words_of"
Cohesion: 0.16
Nodes (9): clean_sound(), limit_sounds(), graphic_low(), archive_images(), fill_money_graphics(), is_person_portrait(), words_of(), test_clean_sound() (+1 more)

### Community 71 - "clean_full"
Cohesion: 0.11
Nodes (17): clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number() (+9 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.14
Nodes (12): align(), align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak(), test_caption_word_counts_match_the_scene_splitter() (+4 more)

### Community 73 - "ask_ai"
Cohesion: 0.12
Nodes (13): seed_ideas(), ask_ai(), gemini_model(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash() (+5 more)

### Community 75 - "audio_library.py"
Cohesion: 0.28
Nodes (14): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+6 more)

### Community 76 - "visual_review"
Cohesion: 0.24
Nodes (7): clock(), overlay_notes(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 77 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 79 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 80 - "full_cues"
Cohesion: 0.12
Nodes (12): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish() (+4 more)

### Community 81 - "capture_prompts"
Cohesion: 0.20
Nodes (6): load_rules(), min_real_pictures(), capture_prompts(), ask(), test_load_rules_sets_session(), test_strange_history_prompts_unchanged()

### Community 82 - "other_ai"
Cohesion: 0.24
Nodes (9): other_ai(), fake_providers(), claude(), reply(), saved_session(), test_batch_uses_selected_codex_writer_and_migrates_saved_aliases(), test_every_mode_can_continue_through_two_exhausted_ais(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty() (+1 more)

### Community 85 - "opener_graphic"
Cohesion: 0.15
Nodes (8): full_summary(), opener_graphic(), fix_drawn_answer(), fix_opener_graphic(), paint_opener_start(), test_full_props_figure(), test_full_summary(), test_weak_opener_graphic_fixes_then_handoff()

### Community 86 - "test_drawn_opener_renders_and_is_reused"
Cohesion: 0.25
Nodes (6): fake_ai(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused(), test_no_verdict_is_not_a_pass(), test_use_opener_plays_the_drawn_opener()

### Community 89 - "test_pictures_first.py"
Cohesion: 0.17
Nodes (16): choose_images(), download_picture(), recover_downloads(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded() (+8 more)

### Community 90 - "cold_read"
Cohesion: 0.25
Nodes (5): cold_read_line(), cold_read(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 91 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 92 - "test_blender_plan.py"
Cohesion: 0.05
Nodes (44): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+36 more)

### Community 94 - "plan_with"
Cohesion: 0.29
Nodes (5): plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 95 - "full_props"
Cohesion: 0.40
Nodes (4): full_props(), _jpg(), test_custom_cues_props_and_pictures(), test_remotion_props_full()

### Community 96 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

### Community 97 - "apply_metadata"
Cohesion: 0.33
Nodes (3): apply_metadata(), clean_tags(), clean_title()

### Community 99 - "test_style.py"
Cohesion: 0.15
Nodes (12): wants_remotion(), apply_look_scenes(), candidate_in(), library_snapshot(), restore_library(), test_apply_look_scenes(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure() (+4 more)

### Community 100 - "rescue_graphics"
Cohesion: 0.40
Nodes (3): full_formats(), rescue_graphics(), test_rescue_respects_caps()

### Community 104 - "media_command"
Cohesion: 0.22
Nodes (8): freesound_fetch(), freesound_preview(), freesound_results(), audition_audio(), download_audio_choices(), media_command(), review_audio_files(), seed_audio_library()

### Community 114 - "ffmpeg"
Cohesion: 0.17
Nodes (10): sentence_groups(), split_takes(), log_short(), duration(), ffmpeg(), is_loop_short(), scenes(), test_a_take_is_cut_between_the_scenes_words() (+2 more)

## Knowledge Gaps
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `scene_repair.py`, `json`, `render_remotion`, `local_clips`, `write_json`, `frame_maker`, `sfx_events`, `io`, `main`, `story_sound`, `subprocess`, `finish_render`, `words_of`, `test_full_scenes.py`, `audio_library.py`, `visual_review`, `captions`, `full_cues`, `opener_graphic`, `test_pictures_first.py`, `make_paper`, `test_blender_plan.py`, `test_style.py`, `rescue_graphics`, `make_sfx`, `ffmpeg`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13086770981507823 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `catalog_pool`, `direct_scripts`, `json`, `check_twists`, `style_library`, `owner`, `story_problems`, `image_sources.py`, `extra_sources.py`, `pick_channel`, `fake_ai`, `main`, `re`, `gather_pool`, `edit_scripts`, `words_of`, `clean_full`, `ask_ai`, `test_full_scenes.py`, `capture_prompts`, `test_blender_plan.py`, `plan_with`, `limit_style`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `catalog_pool` be split into smaller, more focused modules?**
  _Cohesion score 0.13756613756613756 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `json`, `Shots`, `math`, `parts.py`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Should `direct_scripts` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._
- **Should `plan_with` be split into smaller, more focused modules?**
  _Cohesion score 0.14130434782608695 - nodes in this community are weakly interconnected._