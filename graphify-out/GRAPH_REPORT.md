# Graph Report - ShortsMaker  (2026-11-07)

## Corpus Check
- 177 files · ~216,843 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .geojson 2, .canvas 1)

## Summary
- 2770 nodes · 7268 edges · 142 communities (110 shown, 32 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 142 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `054580e4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Short.tsx
- test_pictures_first.py
- prepare_topic
- invent_component
- split_make_shorts.py
- render_remotion
- code_custom_scenes
- guarded.tsx
- k
- test_h3_handoff.py
- local_clips
- plan
- visual_review
- test_rules.py
- Journey.tsx
- toolkit.tsx
- ref_react
- write_scripts
- gen.py
- .at
- json
- make
- core.mjs
- Pen
- brand_images
- frame_maker
- finish_render
- scene_cues
- look.py
- parts.py
- OpeningRulesTests
- gather_pool
- templates.py
- trend_research
- main
- full/types.ts
- main
- Paper
- extra_sources.py
- build_scene.py
- style.test.ts
- textures.mjs
- remotion-best-practices/remotion-maps/techniques/maptiler/scripts/prep-geo.mjs
- remotion-markup/remotion-maps/techniques/maptiler/scripts/prep-geo.mjs
- on_topic
- kit.ts
- trim_borders
- test_blender_render.py
- fake_ai
- test_story.py
- remotion-best-practices/remotion-maps/techniques/maptiler/assets/RiverReveal.tsx
- test_opener_crew.py
- kit.mjs
- RetentionTests
- retention.py
- remotion-markup/remotion-maps/techniques/maptiler/assets/RiverReveal.tsx
- ReliabilityTests
- apply_review_fixes
- h3_run.py
- clean
- layout
- remotion-best-practices/remotion-maps/techniques/cesium/scripts/prep-cesium-path.mjs
- .render_fixture
- telegraph_station.mjs
- music_gain
- uprooted_potatoes.mjs
- kit_parts.mjs
- first_second_check
- remotion-markup/remotion-maps/techniques/cesium/scripts/prep-cesium-path.mjs
- clean_full
- qwen_voice.py
- ask_ai
- audio_mix.py
- audio_library.py
- Opener3D.tsx
- test_style.py
- style_library
- test_blender_scene.py
- remotion-best-practices/remotion-maps/techniques/cesium/assets/CesiumFlythrough.tsx
- remotion-markup/remotion-maps/techniques/cesium/assets/CesiumFlythrough.tsx
- test_drawn_opener.py
- MediaTests
- MetadataTests
- bean.mjs
- PreflightTests
- shutil
- StoryPacingTests
- choose_images
- wm_files
- review
- test_blender_plan.py
- FeedbackTests
- quality_check
- save_candidate
- test_full_scenes.py
- opener3d.py
- MarkTests
- potato_pile.mjs
- assemble
- ffmpeg
- limit_style
- render
- edit_scripts
- use
- drawn_thumbnail
- other_ai
- umbrellas.mjs
- battery.mjs
- re
- telegraph_sounder.mjs
- telegraph_register.mjs
- telegraph_workbench.mjs
- cold_read
- edit_plan
- fetch
- QuestionBeat.tsx
- make_opener
- full_props
- download_audio_choices
- write_frames
- story_problems
- sfx_events
- ends_sentence
- remotion-best-practices/remotion-maps/techniques/maptiler/assets/tokens.ts
- remotion-markup/remotion-maps/techniques/maptiler/assets/tokens.ts
- bitten_potato.mjs
- potato_mouthful.mjs
- first_sentence
- drawn_payoff
- remotion-best-practices/remotion-maps/techniques/maptiler/assets/MapTilerVectorElement.ts
- remotion-markup/remotion-maps/techniques/maptiler/assets/MapTilerVectorElement.ts
- archive_films
- article_text
- node_run
- lint_person
- test_owner_score_replaces_the_ai
- BlenderFailed
- wants_remotion
- test_story_sound_library

## God Nodes (most connected - your core abstractions)
1. `k` - 102 edges
2. `render()` - 64 edges
3. `ask_ai()` - 54 edges
4. `write_scripts()` - 54 edges
5. `makeKit()` - 37 edges
6. `clean()` - 36 edges
7. `clamp()` - 35 edges
8. `MediaTests` - 35 edges
9. `main()` - 32 edges
10. `skinOf()` - 31 edges

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

## Communities (142 total, 32 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.14
Nodes (18): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, clamp01(), H, W (+10 more)

### Community 1 - "Short.tsx"
Cohesion: 0.14
Nodes (37): Captions(), card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard() (+29 more)

### Community 2 - "test_pictures_first.py"
Cohesion: 0.14
Nodes (25): catalog_entries(), catalog_pool(), clean_pics(), save_pool(), entry(), film(), pic_short(), pool_of() (+17 more)

### Community 3 - "prepare_topic"
Cohesion: 0.12
Nodes (12): catalog_text(), contact_sheets(), is_usable(), load_pool(), pictures_of(), pool_folder(), preflight_pictures(), prepare_topic() (+4 more)

### Community 4 - "invent_component"
Cohesion: 0.12
Nodes (15): invent_component(), attempt(), invent_styles(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others() (+7 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "render_remotion"
Cohesion: 0.16
Nodes (9): render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain() (+1 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.11
Nodes (17): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), is_payoff(), lint_custom_code(), look_and_fix(), opener_preflight() (+9 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.13
Nodes (18): Box, boxAt(), clamp, Connect(), fitCard(), hits(), layoutColumn(), layoutGrid() (+10 more)

### Community 10 - "k"
Cohesion: 0.10
Nodes (3): makeKit(), k, ellPts()

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "local_clips"
Cohesion: 0.11
Nodes (12): cosy_instruct(), cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), local_voice(), motion_prompt() (+4 more)

### Community 13 - "plan"
Cohesion: 0.08
Nodes (19): minutes(), staging_line(), blends(), part_sheet(), render(), animal_cutout(), crew(), default_cutout() (+11 more)

### Community 14 - "visual_review"
Cohesion: 0.20
Nodes (8): clock(), overlay_notes(), pacing_check(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (39): load_rules(), min_real_pictures(), parse_rules(), capture_prompts(), ask(), draft_reply(), make(), run_draft() (+31 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.21
Nodes (21): CustomScene(), ExampleChain(), ExampleEvidence(), Custom0(), Custom1(), Custom2(), Custom3(), Card() (+13 more)

### Community 18 - "ref_react"
Cohesion: 0.39
Nodes (3): clamp, CustomFull, FullProps

### Community 19 - "write_scripts"
Cohesion: 0.11
Nodes (24): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+16 more)

### Community 20 - "gen.py"
Cohesion: 0.22
Nodes (5): images(), main(), t5_encoder(), tts(), video()

### Community 22 - "json"
Cohesion: 0.08
Nodes (17): code_version(), fingerprint(), crop_film_bytes(), crop_filter(), film_frames(), film_piece(), pixabay_films(), shot_moments() (+9 more)

### Community 23 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 24 - "core.mjs"
Cohesion: 0.08
Nodes (21): burst(), clamp(), eBounce(), eElastic(), eExpo(), eIn(), eIO(), eOut() (+13 more)

### Community 25 - "Pen"
Cohesion: 0.17
Nodes (7): catmull(), centroid(), densify(), INK, noise1(), idHash(), Pen

### Community 26 - "brand_images"
Cohesion: 0.18
Nodes (7): brand_films(), brand_images(), brand_page(), BrandImages, commercial_queries(), settings(), print_source_status()

### Community 27 - "frame_maker"
Cohesion: 0.08
Nodes (13): ClipReader, draw_card(), draw_graphic(), fills_frame(), fit_font(), frame_maker(), frame(), graphic_low() (+5 more)

### Community 28 - "finish_render"
Cohesion: 0.10
Nodes (13): full_summary(), full_formats(), opener_graphic(), drawn_answer_problem(), fix_drawn_answer(), fix_opener_graphic(), paint_opener_start(), sound_masking() (+5 more)

### Community 29 - "scene_cues"
Cohesion: 0.09
Nodes (16): scene_cues(), full_cues(), read_need(), spoken_at(), spoken_span(), callout_hold(), drop_unreadable_kinetic(), test_counter_finishes_before_it_leaves() (+8 more)

### Community 30 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 31 - "parts.py"
Cohesion: 0.15
Nodes (21): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+13 more)

### Community 33 - "gather_pool"
Cohesion: 0.15
Nodes (5): balanced_candidates(), gather_pool(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "trend_research"
Cohesion: 0.20
Nodes (6): channel_url(), new_channel(), save_channel(), seed_ideas(), trend_research(), yt_list()

### Community 36 - "main"
Cohesion: 0.06
Nodes (39): ask_brain(), ask_count(), ask_number(), ask_yes(), configure_brain(), load_channel(), normalize_brain(), pick_channel() (+31 more)

### Community 37 - "full/types.ts"
Cohesion: 0.13
Nodes (22): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+14 more)

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "Paper"
Cohesion: 0.16
Nodes (21): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+13 more)

### Community 40 - "extra_sources.py"
Cohesion: 0.30
Nodes (9): candidate(), collection_images(), europeana_images(), loc_images(), smithsonian_images(), source_json(), wellcome_images(), optional_key() (+1 more)

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "style.test.ts"
Cohesion: 0.20
Nodes (9): Background(), has(), lookFor(), overlayFor(), transitionFor(), TRANSITIONS, inksOf(), transitionWindow() (+1 more)

### Community 43 - "textures.mjs"
Cohesion: 0.19
Nodes (20): ellipse(), fibre(), fill(), grainCanvas(), grainOver(), hash(), hatch(), rng() (+12 more)

### Community 44 - "remotion-best-practices/remotion-maps/techniques/maptiler/scripts/prep-geo.mjs"
Cohesion: 0.08
Nodes (18): ANCHOR_BBOX, biggestPoly(), borders, COUNTRIES, countryMeta, __dir, flowKm, FRAME_BBOX (+10 more)

### Community 45 - "remotion-markup/remotion-maps/techniques/maptiler/scripts/prep-geo.mjs"
Cohesion: 0.08
Nodes (18): ANCHOR_BBOX, biggestPoly(), borders, COUNTRIES, countryMeta, __dir, flowKm, FRAME_BBOX (+10 more)

### Community 46 - "on_topic"
Cohesion: 0.18
Nodes (8): pixabay_images(), nasa_films(), nasa_credit(), nasa_images(), nasa_search(), on_topic(), test_nasa_partner_media_is_credited(), test_on_topic_ignores_a_lone_shared_name()

### Community 47 - "kit.ts"
Cohesion: 0.19
Nodes (23): CAPTION_TOP, drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "trim_borders"
Cohesion: 0.20
Nodes (5): is_stereo(), trim_borders(), border(), plain(), vertical_image()

### Community 49 - "test_blender_render.py"
Cohesion: 0.18
Nodes (15): peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises() (+7 more)

### Community 50 - "fake_ai"
Cohesion: 0.15
Nodes (9): entry_age(), logbook_results(), seo_pass(), test_logbook_marks_tiny_samples(), fake_ai, test_seo_pass_empty_no_ai(), test_seo_pass_research_seeds_dict_and_list(), test_seo_examples_come_from_the_channel() (+1 more)

### Community 51 - "test_story.py"
Cohesion: 0.26
Nodes (8): check_twists(), scenes(), test_rules_accept_opener_setting(), test_sentences_running_across_cuts_are_one_take(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 52 - "remotion-best-practices/remotion-maps/techniques/maptiler/assets/RiverReveal.tsx"
Cohesion: 0.11
Nodes (16): CountryLabel(), clamp01(), Country, countryPolygons, DRAW, EMPTY, END, lerp() (+8 more)

### Community 53 - "test_opener_crew.py"
Cohesion: 0.14
Nodes (18): made3d(), check_staging(), objects3d(), blind_ok(), fake(), short(), staging(), test_a_failed_part_falls_back_to_its_substitute() (+10 more)

### Community 54 - "kit.mjs"
Cohesion: 0.09
Nodes (27): bounds(), EDGE, flat, fx, PAD_TOP, PAD_X, paintAll(), STEPS (+19 more)

### Community 56 - "retention.py"
Cohesion: 0.20
Nodes (11): analyze(), edit_metrics(), load_metrics(), metrics_text(), normalize_metrics(), normalize_reply(), observations(), parse_metric() (+3 more)

### Community 57 - "remotion-markup/remotion-maps/techniques/maptiler/assets/RiverReveal.tsx"
Cohesion: 0.11
Nodes (16): CountryLabel(), clamp01(), Country, countryPolygons, DRAW, EMPTY, END, lerp() (+8 more)

### Community 59 - "apply_review_fixes"
Cohesion: 0.09
Nodes (14): apply_review_fixes(), rewrite_paint_prompts(), plan_gap_paintings(), _fake_planning(), ask(), _review_state(), test_auto_fix_graphic(), test_director_prompt_mentions_full() (+6 more)

### Community 60 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 61 - "clean"
Cohesion: 0.09
Nodes (25): box_of(), clean(), dress(), front_door(), half_width(), nudge(), on_top(), resolve() (+17 more)

### Community 62 - "layout"
Cohesion: 0.22
Nodes (6): word_time(), foot_of(), layout(), place_animal(), put(), lum()

### Community 63 - "remotion-best-practices/remotion-maps/techniques/cesium/scripts/prep-cesium-path.mjs"
Cohesion: 0.12
Nodes (15): A, AB, B, clip, __dir, even, havKm(), hs (+7 more)

### Community 66 - "music_gain"
Cohesion: 0.12
Nodes (8): ass_time(), caption_lines(), caption_size(), captions(), music_gain(), speak(), tts(), test_music_gain_evens_out_tracks()

### Community 69 - "first_second_check"
Cohesion: 0.14
Nodes (15): first_second_check(), review_status(), swap_pictures(), real(), run_check(), state(), test_failed_preview_clears_previous_opener_score(), test_good_opening_or_no_reply_changes_nothing() (+7 more)

### Community 70 - "remotion-markup/remotion-maps/techniques/cesium/scripts/prep-cesium-path.mjs"
Cohesion: 0.12
Nodes (15): A, AB, B, clip, __dir, even, havKm(), hs (+7 more)

### Community 71 - "clean_full"
Cohesion: 0.08
Nodes (26): clean_sound(), limit_sounds(), rescue_graphics(), clean_full(), word(), clean_graphic(), contains(), coords() (+18 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.13
Nodes (13): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+5 more)

### Community 73 - "ask_ai"
Cohesion: 0.07
Nodes (23): argon_out(), ask_ai(), gemini_model(), quota_exhausted(), run_agy(), run_codex(), strong(), test_codex_failure_is_bounded() (+15 more)

### Community 74 - "audio_mix.py"
Cohesion: 0.12
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 75 - "audio_library.py"
Cohesion: 0.21
Nodes (18): approved_sound(), audio_metadata(), ducking_filter(), history_read(), import_audio_file(), preview_mix(), record_audio(), select_music() (+10 more)

### Community 76 - "Opener3D.tsx"
Cohesion: 0.06
Nodes (54): aim(), Assembly(), BOOKS, Box(), Building(), Burst(), calculateOpener3D(), CameraRig() (+46 more)

### Community 77 - "test_style.py"
Cohesion: 0.13
Nodes (10): apply_look_scenes(), owner(), plan_with(), ask(), test_apply_look_scenes(), test_director_character_look_is_kept_short_or_dropped(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library() (+2 more)

### Community 78 - "style_library"
Cohesion: 0.11
Nodes (15): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), build() (+7 more)

### Community 79 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 80 - "remotion-best-practices/remotion-maps/techniques/cesium/assets/CesiumFlythrough.tsx"
Cohesion: 0.20
Nodes (11): bearing(), CesiumFlythrough(), CesiumFlythroughProps, clamp(), FlyoverMode, havKm(), lerp(), loadCesium() (+3 more)

### Community 81 - "remotion-markup/remotion-maps/techniques/cesium/assets/CesiumFlythrough.tsx"
Cohesion: 0.20
Nodes (11): bearing(), CesiumFlythrough(), CesiumFlythroughProps, clamp(), FlyoverMode, havKm(), lerp(), loadCesium() (+3 more)

### Community 82 - "test_drawn_opener.py"
Cohesion: 0.20
Nodes (9): fake_ai(), short(), test_drawn_opener_gives_up_after_fixes(), test_drawn_opener_renders_and_is_reused(), test_drawn_opener_stops_when_a_fix_does_not_help(), test_neither_passes_so_the_best_draft_at_keep_is_used(), test_no_verdict_is_not_a_pass(), test_reveal_scene_is_drawn_with_its_own_rules() (+1 more)

### Community 85 - "bean.mjs"
Cohesion: 0.35
Nodes (9): rad(), rrect(), arm(), bubble(), bust(), hat(), person(), SKIN (+1 more)

### Community 87 - "shutil"
Cohesion: 0.06
Nodes (21): available(), clean_code(), opener_role(), picture(), staged(), voicestudio_up(), preview_sheet(), tsc_check() (+13 more)

### Community 89 - "choose_images"
Cohesion: 0.17
Nodes (15): choose_images(), download_picture(), recover_downloads(), is_person_portrait(), picking, planned_short(), scene(), still() (+7 more)

### Community 90 - "wm_files"
Cohesion: 0.18
Nodes (6): commons_films(), article_images(), commons_search(), thumb_url(), usable_license(), wm_files()

### Community 91 - "review"
Cohesion: 0.23
Nodes (6): ai_review(), blind_read(), look_dir(), owner_check(), review(), write()

### Community 92 - "test_blender_plan.py"
Cohesion: 0.12
Nodes (20): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), plan() (+12 more)

### Community 94 - "quality_check"
Cohesion: 0.25
Nodes (4): quality_check(), length_plan(), max_seconds(), test_quality_check_reads_ffmpeg_and_flags_reused_pictures()

### Community 95 - "save_candidate"
Cohesion: 0.20
Nodes (10): save_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_candidate_names_unique_across_kinds() (+2 more)

### Community 96 - "test_full_scenes.py"
Cohesion: 0.11
Nodes (9): hex_rgb(), luminance(), short_skin(), person_card(), clean_photo(), visual_unique(), mark_details(), test_clean_full_custom_and_skin() (+1 more)

### Community 97 - "opener3d.py"
Cohesion: 0.12
Nodes (11): clean_shapes(), held_of(), in_order(), inside(), load_part(), num(), shapes_foot(), sheet() (+3 more)

### Community 100 - "assemble"
Cohesion: 0.14
Nodes (10): missing_parts(), lint_cutout(), spread_out(), assemble(), owner(), test_kit_animals_must_be_used(), test_a_knock_needs_a_closed_door_and_a_messenger_his_letter(), test_hold_counts_as_drawing_the_letter_and_scenery_stays_3d() (+2 more)

### Community 102 - "ffmpeg"
Cohesion: 0.13
Nodes (11): shot_span(), split_takes(), spoken_count(), duration(), ffmpeg(), video_encoder(), apply(), preview() (+3 more)

### Community 104 - "render"
Cohesion: 0.07
Nodes (13): make_sfx(), gemini_images(), short_credit(), graphics_count(), to_vertical(), is_loop_short(), ink_silhouette(), paint_instead() (+5 more)

### Community 105 - "edit_scripts"
Cohesion: 0.15
Nodes (9): edit_scripts(), narration_lines(), test_all_modes_route_writer_editor_and_reader(), ask(), test_only_the_second_edit_pass_gets_the_research(), test_script_rounds_stop_when_fixed_or_after_three(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules() (+1 more)

### Community 106 - "use"
Cohesion: 0.33
Nodes (4): fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic(), use()

### Community 107 - "drawn_thumbnail"
Cohesion: 0.21
Nodes (9): thumbnail_order(), drawn_thumbnail(), test_thumbnail_order_skips_film_and_puts_openers_first(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so() (+1 more)

### Community 108 - "other_ai"
Cohesion: 0.28
Nodes (8): other_ai(), fake_providers(), claude(), reply(), saved_session(), test_every_mode_can_continue_through_two_exhausted_ais(), test_exhausted_accounts_are_not_retried_when_all_three_are_empty(), test_gemini_modes_choose_codex_and_keep_editor_choice()

### Community 111 - "re"
Cohesion: 0.08
Nodes (13): vault_page(), vault_refresh(), import_media(), local_assets(), media_search_words(), kit_text(), parse_scene_money(), max_full() (+5 more)

### Community 115 - "cold_read"
Cohesion: 0.22
Nodes (6): cold_read(), recheck_final_scripts(), test_codex_cold_reader_and_quota_fallback_never_call_claude(), test_cold_read_handles_malformed_reply(), test_cold_read_keeps_only_valid_answers(), test_cold_read_uses_other_ai_in_solo_and_collaborative_modes()

### Community 116 - "edit_plan"
Cohesion: 0.17
Nodes (6): cold_read_line(), cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 117 - "fetch"
Cohesion: 0.22
Nodes (6): archive_images(), get_image(), openverse_images(), ov_get(), wm_get(), fetch()

### Community 118 - "QuestionBeat.tsx"
Cohesion: 0.27
Nodes (6): FONT, theme, CLAMP, KineticTitle(), QuestionBeat(), Overlay

### Community 119 - "make_opener"
Cohesion: 0.20
Nodes (5): lint(), make_opener(), sheet_times(), spoils(), test_lint()

### Community 120 - "full_props"
Cohesion: 0.18
Nodes (9): full_props(), full_pictures(), _board(), _jpg(), test_board_pictures_attached(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_remotion_props_full() (+1 more)

### Community 121 - "download_audio_choices"
Cohesion: 0.25
Nodes (5): freesound_fetch(), freesound_preview(), freesound_results(), download_audio_choices(), seed_audio_library()

### Community 122 - "write_frames"
Cohesion: 0.29
Nodes (3): flash_alpha(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 123 - "story_problems"
Cohesion: 0.33
Nodes (7): story_problems(), read(), test_cold_read_verdicts(), test_no_hook_setting_no_hook_check(), test_story_problems(), test_story_problems_flags_summary_hook(), test_story_problems_money_claim()

### Community 124 - "sfx_events"
Cohesion: 0.25
Nodes (4): schedule_sounds(), sfx_events(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 125 - "ends_sentence"
Cohesion: 0.29
Nodes (4): sentence_groups(), ends_sentence(), srt(), test_sentence_ends_include_curly_quotes_and_ellipsis()

### Community 126 - "remotion-best-practices/remotion-maps/techniques/maptiler/assets/tokens.ts"
Cohesion: 0.29
Nodes (6): COLORS, COUNTRY, COUNTRY_DARK, DUR, FILL_OPACITY, VIDEO

### Community 127 - "remotion-markup/remotion-maps/techniques/maptiler/assets/tokens.ts"
Cohesion: 0.29
Nodes (6): COLORS, COUNTRY, COUNTRY_DARK, DUR, FILL_OPACITY, VIDEO

### Community 130 - "first_sentence"
Cohesion: 0.29
Nodes (4): log_short(), first_sentence(), test_first_sentence_reads_across_the_cut(), test_logbook_hook_line_is_the_whole_first_sentence()

### Community 131 - "drawn_payoff"
Cohesion: 0.29
Nodes (3): drawn_payoff(), use_opener(), test_use_opener_plays_the_drawn_opener()

### Community 134 - "archive_films"
Cohesion: 0.40
Nodes (4): archive_ad_films(), archive_films(), duke_films(), source_enabled()

### Community 135 - "article_text"
Cohesion: 0.40
Nodes (3): article_text(), fact_check(), test_fact_check_drops_full()

### Community 141 - "test_story_sound_library"
Cohesion: 0.67
Nodes (3): test_story_sound_library(), fetch(), _tone_wav()

## Knowledge Gaps
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `drawn_payoff`, `render_remotion`, `local_clips`, `wants_remotion`, `visual_review`, `json`, `frame_maker`, `finish_render`, `scene_cues`, `main`, `test_blender_render.py`, `apply_review_fixes`, `music_gain`, `clean_full`, `audio_library.py`, `shutil`, `choose_images`, `save_candidate`, `test_full_scenes.py`, `ffmpeg`, `write_frames`, `sfx_events`, `ends_sentence`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.13793103448275862 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `build_scene.py`, `json`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `Short.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.13953488372093023 - nodes in this community are weakly interconnected._
- **Why does `RetentionTests` connect `RetentionTests` to `pathlib`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Should `test_pictures_first.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13825757575757575 - nodes in this community are weakly interconnected._
- **Should `prepare_topic` be split into smaller, more focused modules?**
  _Cohesion score 0.11688311688311688 - nodes in this community are weakly interconnected._