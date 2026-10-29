# Graph Report - ShortsMaker  (2026-10-29)

## Corpus Check
- 129 files · ~154,544 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 2147 nodes · 5664 edges · 81 communities (73 shown, 8 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 128 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `87f1f30b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- test_first_second.py
- toolkit.tsx
- ask_ai
- split_make_shorts.py
- test_full_scenes.py
- motion.py
- test_opener_scene.py
- Paper
- local_voice
- test_h3_handoff.py
- moves.py
- guarded.tsx
- make
- test_rules.py
- Journey.tsx
- BigNumber.tsx
- test_pictures_first.py
- write_scripts
- Local GPU Worker
- style_library
- local_clips
- clean_full
- resolve_models
- test_blender_render.py
- test_blender_link.py
- frame_maker
- full_cues
- captions
- look.py
- parts.py
- math
- prepare_topic
- templates.py
- image_sources.py
- test_story.py
- plan_with
- build_scene.py
- time
- load_model
- main
- Short.tsx
- json
- test_opener_plan.py
- cut
- subprocess
- Halftone.tsx
- test_topic_ideas.py
- blender_link.py
- gather_pool
- re
- opener_graphic
- use_picture_from
- visual_review
- scene_kit.py
- sfx_events
- choose_images
- test_opener_render.py
- pack_people.py
- test_blender_scene.py
- opener_checks.py
- Fake
- opener_scene.py
- look_toon.py
- paint_instead
- test_style.py
- Shots
- test_blender_plan.py
- edit_scripts
- render_remotion
- limit_style
- make_sfx
- people_standin.py
- test_local_job_retries_a_hard_crash
- ffmpeg
- QuestionBeat.tsx
- test_short_credit
- drawn_thumbnail
- pool_pictures
- render

## God Nodes (most connected - your core abstractions)
1. `render()` - 62 edges
2. `write_scripts()` - 49 edges
3. `ask_ai()` - 40 edges
4. `render_opener()` - 33 edges
5. `run()` - 33 edges
6. `skinOf()` - 31 edges
7. `fixture()` - 31 edges
8. `cut()` - 29 edges
9. `main()` - 27 edges
10. `Paper()` - 25 edges

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
- 5-file cycle: `shortsmaker/blender_render.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py -> shortsmaker/opener_render.py -> shortsmaker/blender_render.py`

## Communities (81 total, 8 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.15
Nodes (21): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.14
Nodes (30): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+22 more)

### Community 2 - "test_first_second.py"
Cohesion: 0.07
Nodes (24): logbook_results(), apply_review_fixes(), swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples() (+16 more)

### Community 3 - "toolkit.tsx"
Cohesion: 0.24
Nodes (20): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+12 more)

### Community 4 - "ask_ai"
Cohesion: 0.08
Nodes (22): scene_cues(), ask_ai(), gemini_model(), quota_exhausted(), run_agy(), mark_details(), test_counter_finishes_before_it_leaves(), test_quota_fallback_both_ways() (+14 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.08
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 7 - "motion.py"
Cohesion: 0.13
Nodes (13): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+5 more)

### Community 8 - "test_opener_scene.py"
Cohesion: 0.06
Nodes (37): builds(), fixture(), people_lib(), run(), test_bad_plans_fail(), test_box_fall_rests_and_renders(), test_camera_follows_unasked(), test_chicken_chop_reference() (+29 more)

### Community 9 - "Paper"
Cohesion: 0.09
Nodes (36): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+28 more)

### Community 10 - "local_voice"
Cohesion: 0.28
Nodes (5): local_voice(), split_takes(), spoken_count(), is_loop_short(), test_word_counts_match_the_aligner()

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.09
Nodes (31): h3_problems(), h3_prompt(), unpack_clips(), fake_ai(), handoff(), short_with(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated() (+23 more)

### Community 12 - "moves.py"
Cohesion: 0.12
Nodes (22): apply(), clear_distance(), clear_distance_at_end(), fall(), fly_off(), gait(), hop_off(), legs() (+14 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.11
Nodes (21): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+13 more)

### Community 14 - "make"
Cohesion: 0.15
Nodes (8): caption_layer(), make(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers(), videos()

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (40): load_rules(), min_real_pictures(), parse_rules(), test_channels_have_opener_rules(), capture_prompts(), ask(), draft_reply(), make() (+32 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.16
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "BigNumber.tsx"
Cohesion: 0.22
Nodes (13): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+5 more)

### Community 18 - "test_pictures_first.py"
Cohesion: 0.13
Nodes (24): catalog_entries(), catalog_pool(), clean_pics(), entry(), fake_ai, pic_short(), pool_of(), test_board_item_pics_cleaned() (+16 more)

### Community 19 - "write_scripts"
Cohesion: 0.11
Nodes (22): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty() (+14 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.08
Nodes (17): cut_text(), edit_plan(), look_text(), picture_line(), clean_invention(), clean_look(), clean_transition(), settle_style() (+9 more)

### Community 22 - "local_clips"
Cohesion: 0.15
Nodes (10): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), motion_prompt(), start_picture_problems(), veo_handoff() (+2 more)

### Community 23 - "clean_full"
Cohesion: 0.05
Nodes (32): clean_sound(), limit_sounds(), graphic_low(), clean_photo(), is_stereo(), trim_borders(), border(), plain() (+24 more)

### Community 24 - "resolve_models"
Cohesion: 0.15
Nodes (7): allowed_licence(), search(), model_for(), pick_model(), resolve_models(), to_glb(), test_search_filters_licences()

### Community 25 - "test_blender_render.py"
Cohesion: 0.15
Nodes (15): BlenderFailed, peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws() (+7 more)

### Community 26 - "test_blender_link.py"
Cohesion: 0.30
Nodes (8): ping(), _fetch_replies(), execute(), ok(), test_download_error_cleans_up(), test_ping_on_off(), test_switched_off_reason(), with_fake()

### Community 27 - "frame_maker"
Cohesion: 0.07
Nodes (15): ClipReader, draw_card(), draw_graphic(), fit_font(), flash_alpha(), frame_maker(), frame(), graphic_overlay() (+7 more)

### Community 28 - "full_cues"
Cohesion: 0.20
Nodes (6): full_cues(), spoken_at(), spoken_span(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish()

### Community 29 - "captions"
Cohesion: 0.16
Nodes (7): ass_time(), caption_lines(), captions(), styled(), speak(), tts(), ass_colour()

### Community 30 - "look.py"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (22): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+14 more)

### Community 32 - "math"
Cohesion: 0.07
Nodes (20): _append(), _attach(), _bake_free(), base_name(), _body_tree(), _clearance(), _colour(), _detour() (+12 more)

### Community 33 - "prepare_topic"
Cohesion: 0.16
Nodes (9): write_json(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_empty_pool_drops_topic_without_ai(), test_pool_rows_without_thumbs() (+1 more)

### Community 34 - "templates.py"
Cohesion: 0.16
Nodes (16): member(), Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), focus_object() (+8 more)

### Community 35 - "image_sources.py"
Cohesion: 0.08
Nodes (18): archive_films(), commons_films(), crop_film_bytes(), film_frames(), nasa_films(), pixabay_films(), archive_images(), article_images() (+10 more)

### Community 36 - "test_story.py"
Cohesion: 0.07
Nodes (28): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), sentence_groups(), check_twists(), story_problems() (+20 more)

### Community 37 - "plan_with"
Cohesion: 0.29
Nodes (5): plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 39 - "time"
Cohesion: 0.10
Nodes (11): call(), fit_start(), frames(), graph(), main(), saved_file(), align(), main() (+3 more)

### Community 40 - "load_model"
Cohesion: 0.25
Nodes (4): ground_material(), load_model(), material(), merge()

### Community 41 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 42 - "Short.tsx"
Cohesion: 0.12
Nodes (20): Captions(), PersonCard(), Root(), Background(), Card, flashAlpha(), GraphicFor(), Move (+12 more)

### Community 43 - "json"
Cohesion: 0.07
Nodes (19): freesound_fetch(), code_version(), comfy_call(), moss_graph(), moss_images(), voicestudio_unload(), _cast_note(), fingerprint() (+11 more)

### Community 44 - "test_opener_plan.py"
Cohesion: 0.07
Nodes (38): clean_opener(), _expect(), fill_template(), _keep(), _num(), plan_openers(), ask(), _size() (+30 more)

### Community 45 - "cut"
Cohesion: 0.07
Nodes (27): bm_area(), box_of(), centre(), clusters(), cut(), edge_point_local(), half(), handle_end_local() (+19 more)

### Community 46 - "subprocess"
Cohesion: 0.07
Nodes (9): music_gain(), master_gain(), shot_span(), fills_frame(), duration(), main(), main(), props_for() (+1 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.19
Nodes (21): drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw(), Engraving() (+13 more)

### Community 48 - "test_topic_ideas.py"
Cohesion: 0.15
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 49 - "blender_link.py"
Cohesion: 0.15
Nodes (9): attribution(), call(), credit(), fetch_model(), in_library(), LinkError, words(), test_fetch_saves_pair() (+1 more)

### Community 50 - "gather_pool"
Cohesion: 0.11
Nodes (10): gather_pool(), owner(), _fake_planning(), test_director_prompt_mentions_full(), film(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits() (+2 more)

### Community 51 - "re"
Cohesion: 0.05
Nodes (29): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+21 more)

### Community 52 - "opener_graphic"
Cohesion: 0.15
Nodes (10): full_props(), full_summary(), opener_graphic(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_full_summary(), test_model_graphic() (+2 more)

### Community 53 - "use_picture_from"
Cohesion: 0.29
Nodes (4): use_picture_from(), paint_new(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 54 - "visual_review"
Cohesion: 0.17
Nodes (8): clock(), overlay_notes(), quality_check(), review_fixes(), storyboard(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_fix_kinds()

### Community 55 - "scene_kit.py"
Cohesion: 0.08
Nodes (24): _clip(), facing_now(), _ground(), move(), pick_up(), _strip(), _travel(), add_body() (+16 more)

### Community 56 - "sfx_events"
Cohesion: 0.29
Nodes (4): sfx_events(), test_sfx_full(), test_story_sound_wins_its_moment(), test_style_sounds()

### Community 57 - "choose_images"
Cohesion: 0.19
Nodes (14): choose_images(), apply_look_scenes(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+6 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.08
Nodes (34): render_opener(), use_opener(), Env, _people_files(), short(), test_beats_scaled_into_scene(), test_blender_note(), test_cc_by_credit() (+26 more)

### Community 59 - "pack_people.py"
Cohesion: 0.26
Nodes (6): base_name(), clip_name(), front(), height(), main(), stride()

### Community 60 - "test_blender_scene.py"
Cohesion: 0.08
Nodes (30): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+22 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.10
Nodes (22): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+14 more)

### Community 63 - "opener_scene.py"
Cohesion: 0.09
Nodes (20): State, beat_actors(), build_set(), camera(), dress_set(), first_hit(), main(), place_actors() (+12 more)

### Community 64 - "look_toon.py"
Cohesion: 0.27
Nodes (4): apply(), ink(), outline(), toon()

### Community 66 - "test_style.py"
Cohesion: 0.11
Nodes (15): first_second_check(), approve_candidate(), clean_style_code(), library_menu(), reject_candidate(), save_candidate(), candidate_in(), library_snapshot() (+7 more)

### Community 67 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 68 - "test_blender_plan.py"
Cohesion: 0.12
Nodes (20): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), plan() (+12 more)

### Community 69 - "edit_scripts"
Cohesion: 0.15
Nodes (7): pictures_of(), direct_scripts(), edit_scripts(), length_plan(), narration_lines(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules()

### Community 70 - "render_remotion"
Cohesion: 0.05
Nodes (30): short_skin(), ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), invent_component() (+22 more)

### Community 73 - "people_standin.py"
Cohesion: 0.29
Nodes (5): body(), clip(), key(), main(), part()

### Community 75 - "ffmpeg"
Cohesion: 0.33
Nodes (5): story_sound(), ffmpeg(), test_story_sound_library(), fetch(), _tone_wav()

### Community 76 - "QuestionBeat.tsx"
Cohesion: 0.33
Nodes (4): FONT, theme, CLAMP, KineticTitle()

### Community 78 - "drawn_thumbnail"
Cohesion: 0.12
Nodes (13): get_image(), openverse_images(), ov_get(), full_pictures(), drawn_thumbnail(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back() (+5 more)

### Community 79 - "pool_pictures"
Cohesion: 0.12
Nodes (8): thumbnail_order(), film_piece(), film_ffmpeg(), catalog_text(), is_usable(), usable(), pool_pictures(), test_thumbnail_order_skips_film_and_puts_openers_first()

### Community 85 - "render"
Cohesion: 0.09
Nodes (11): gemini_images(), short_credit(), graphics_count(), to_vertical(), wants_remotion(), srt(), drawn_choices(), render() (+3 more)

## Knowledge Gaps
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `templates.py`, `Shots`, `build_scene.py`, `json`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.14583333333333334 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `render` to `test_first_second.py`, `ask_ai`, `test_full_scenes.py`, `local_voice`, `make`, `style_library`, `local_clips`, `clean_full`, `test_blender_render.py`, `frame_maker`, `captions`, `json`, `subprocess`, `re`, `opener_graphic`, `visual_review`, `sfx_events`, `choose_images`, `test_opener_render.py`, `paint_instead`, `test_style.py`, `render_remotion`, `make_sfx`, `ffmpeg`, `drawn_thumbnail`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.13513513513513514 - nodes in this community are weakly interconnected._
- **Why does `catalog_pool()` connect `test_pictures_first.py` to `prepare_topic`, `ask_ai`, `test_full_scenes.py`, `json`, `subprocess`, `test_rules.py`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Should `test_first_second.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07422402159244265 - nodes in this community are weakly interconnected._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.07507507507507508 - nodes in this community are weakly interconnected._