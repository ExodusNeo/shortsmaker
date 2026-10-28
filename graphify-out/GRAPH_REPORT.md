# Graph Report - ShortsMaker  (2026-10-28)

## Corpus Check
- 127 files · ~152,783 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 2121 nodes · 5586 edges · 89 communities (78 shown, 11 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 127 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6ba8bc10`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- code_custom_scenes
- toolkit.tsx
- ask_ai
- split_make_shorts.py
- pathlib
- short_with
- test_opener_scene.py
- Paper
- ffmpeg
- gpu.py
- share_of_gap
- guarded.tsx
- test_edit_project.py
- test_rules.py
- Journey.tsx
- BigNumber.tsx
- test_pictures_first.py
- write_scripts
- Local GPU Worker
- style_library
- re
- test_full_scenes.py
- make_paper
- test_blender_render.py
- planning_ai
- ClipReader
- full_cues
- audio_mix.py
- look.py
- parts.py
- math
- prepare_topic
- templates.py
- ask
- qwen_voice.py
- fact_check
- build_scene.py
- h3_run.py
- load_model
- main
- Short.tsx
- json
- test_opener_plan.py
- moves.py
- tempfile
- Halftone.tsx
- plan_rules.py
- test_blender_link.py
- gather_pool
- main
- full_props
- test_first_second.py
- first_second_check
- scene_kit.py
- test_h3_handoff.py
- choose_images
- test_opener_render.py
- pack_people.py
- test_opener_checks.py
- opener_checks.py
- test_story.py
- opener_scene.py
- look_toon.py
- render_remotion
- approve_candidate
- Shots
- test_blender_scene.py
- edit_scripts
- invent_component
- edit_plan
- make_sfx
- people_standin.py
- trim_borders
- h3_prompt
- QuestionBeat.tsx
- captions
- limit_style
- clean_pics
- builds
- _clip
- gemini_model
- people_lib
- tree
- render
- srt
- test_local_job_retries_a_hard_crash
- test_slow_motion_keeps_length

## God Nodes (most connected - your core abstractions)
1. `render()` - 63 edges
2. `write_scripts()` - 45 edges
3. `ask_ai()` - 40 edges
4. `render_opener()` - 33 edges
5. `run()` - 33 edges
6. `skinOf()` - 31 edges
7. `fixture()` - 31 edges
8. `cut()` - 30 edges
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
- `test_scene_frames_cover_every_frame_once()` --calls--> `scene_frames()`  [EXTRACTED]
  tests/test_blender_render.py → shortsmaker/blender_render.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`
- 5-file cycle: `shortsmaker/blender_render.py -> shortsmaker/plan_rules.py -> shortsmaker/style_lab.py -> shortsmaker/motion.py -> shortsmaker/opener_render.py -> shortsmaker/blender_render.py`

## Communities (89 total, 11 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.15
Nodes (21): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, clamp01(), H (+13 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.14
Nodes (30): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+22 more)

### Community 2 - "code_custom_scenes"
Cohesion: 0.11
Nodes (14): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+6 more)

### Community 3 - "toolkit.tsx"
Cohesion: 0.24
Nodes (20): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+12 more)

### Community 4 - "ask_ai"
Cohesion: 0.13
Nodes (11): ask_ai(), quota_exhausted(), run_agy(), test_quota_fallback_both_ways(), test_claude_pinned_to_opus_high(), test_gemini_reviews_get_the_main_model_bulk_pictures_flash(), test_run_agy_flags_and_boundaries(), test_session_shared() (+3 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 6 - "pathlib"
Cohesion: 0.09
Nodes (9): hex_rgb(), luminance(), short_skin(), prune_cache(), library_menu(), reject_candidate(), save_candidate(), test_reject_deletes() (+1 more)

### Community 7 - "short_with"
Cohesion: 0.19
Nodes (15): fake_ai(), short_with(), test_all_closeup_marked_scenes_skip_pause(), test_missing_scene_is_asked_again(), run(), test_owner_clip_is_cut_again_for_the_scene_it_now_sits_in(), test_retries_only_failing_scene_with_reason(), run() (+7 more)

### Community 8 - "test_opener_scene.py"
Cohesion: 0.09
Nodes (27): fixture(), run(), test_bad_plans_fail(), test_box_fall_rests_and_renders(), test_camera_follows_unasked(), test_chicken_chop_reference(), test_drop_lands(), test_everyone_with_a_beat_is_framed() (+19 more)

### Community 9 - "Paper"
Cohesion: 0.09
Nodes (36): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+28 more)

### Community 10 - "ffmpeg"
Cohesion: 0.12
Nodes (12): local_voice(), sentence_groups(), split_takes(), spoken_count(), voicestudio_unload(), voicestudio_up(), ffmpeg(), add() (+4 more)

### Community 11 - "gpu.py"
Cohesion: 0.10
Nodes (14): cover_crop(), cut_owner_clip(), gemini_images(), h3_problems(), h3_prompts(), local_clips(), local_job(), moss_graph() (+6 more)

### Community 13 - "guarded.tsx"
Cohesion: 0.11
Nodes (21): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+13 more)

### Community 14 - "test_edit_project.py"
Cohesion: 0.12
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.08
Nodes (39): load_rules(), min_real_pictures(), parse_rules(), test_channels_have_opener_rules(), capture_prompts(), ask(), draft_reply(), make() (+31 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.16
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 17 - "BigNumber.tsx"
Cohesion: 0.22
Nodes (13): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+5 more)

### Community 18 - "test_pictures_first.py"
Cohesion: 0.14
Nodes (24): catalog_entries(), catalog_pool(), entry(), fake_ai, film(), pic_short(), pool_of(), test_board_item_pics_cleaned() (+16 more)

### Community 19 - "write_scripts"
Cohesion: 0.15
Nodes (16): limit_full(), write_scripts(), test_limit_full(), passing(), prepare(), planning, test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position() (+8 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.11
Nodes (14): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), build() (+6 more)

### Community 22 - "re"
Cohesion: 0.09
Nodes (14): allowed_licence(), call(), in_library(), LinkError, ping(), search(), words(), log_short() (+6 more)

### Community 23 - "test_full_scenes.py"
Cohesion: 0.04
Nodes (40): sfx_events(), use_picture_from(), full_summary(), full_formats(), full_pictures(), opener_graphic(), rescue_graphics(), clean_full() (+32 more)

### Community 24 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 25 - "test_blender_render.py"
Cohesion: 0.16
Nodes (14): BlenderFailed, peaks(), render_clips(), _run(), fake_blender(), short(), test_changed_blender_code_redraws(), test_crash_retries_then_raises() (+6 more)

### Community 27 - "ClipReader"
Cohesion: 0.11
Nodes (8): ClipReader, draw_card(), draw_graphic(), flash_alpha(), frame(), shot(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 28 - "full_cues"
Cohesion: 0.13
Nodes (11): scene_cues(), full_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish() (+3 more)

### Community 29 - "audio_mix.py"
Cohesion: 0.15
Nodes (6): freesound_fetch(), music_gain(), speak(), story_sound(), tts(), test_music_gain_evens_out_tracks()

### Community 30 - "look.py"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (22): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+14 more)

### Community 32 - "math"
Cohesion: 0.08
Nodes (18): _append(), _attach(), _bake_free(), base_name(), _body_tree(), _clearance(), _colour(), _detour() (+10 more)

### Community 33 - "prepare_topic"
Cohesion: 0.14
Nodes (11): write_json(), contact_sheets(), load_pool(), pool_folder(), prepare_topic(), save_pool(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip() (+3 more)

### Community 34 - "templates.py"
Cohesion: 0.16
Nodes (16): member(), Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), focus_object() (+8 more)

### Community 35 - "ask"
Cohesion: 0.22
Nodes (4): ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 36 - "qwen_voice.py"
Cohesion: 0.14
Nodes (13): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+5 more)

### Community 37 - "fact_check"
Cohesion: 0.20
Nodes (7): fact_check(), test_fact_check_drops_full(), plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics()

### Community 39 - "h3_run.py"
Cohesion: 0.19
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

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
Nodes (17): code_version(), crop_film_bytes(), film_frames(), film_piece(), pixabay_films(), shot_span(), comfy_call(), moss_images() (+9 more)

### Community 44 - "test_opener_plan.py"
Cohesion: 0.07
Nodes (38): clean_opener(), _expect(), fill_template(), _keep(), _num(), plan_openers(), ask(), _size() (+30 more)

### Community 45 - "moves.py"
Cohesion: 0.07
Nodes (35): apply(), bm_area(), box_of(), centre(), clear_distance(), clear_distance_at_end(), clusters(), cut() (+27 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.19
Nodes (21): drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw(), Engraving() (+13 more)

### Community 48 - "plan_rules.py"
Cohesion: 0.06
Nodes (32): clean_sound(), limit_sounds(), archive_films(), commons_films(), nasa_films(), archive_images(), commons_search(), get_image() (+24 more)

### Community 49 - "test_blender_link.py"
Cohesion: 0.14
Nodes (15): attribution(), credit(), fetch_model(), Fake, _fetch_replies(), execute(), ok(), test_download_error_cleans_up() (+7 more)

### Community 50 - "gather_pool"
Cohesion: 0.11
Nodes (8): article_images(), gather_pool(), owner(), _fake_planning(), test_director_prompt_mentions_full(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 51 - "main"
Cohesion: 0.06
Nodes (24): ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel(), pick_channel() (+16 more)

### Community 52 - "full_props"
Cohesion: 0.40
Nodes (4): full_props(), _jpg(), test_custom_cues_props_and_pictures(), test_remotion_props_full()

### Community 53 - "test_first_second.py"
Cohesion: 0.16
Nodes (15): logbook_results(), swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples(), test_low_score_opens_on_a_better_real_picture() (+7 more)

### Community 54 - "first_second_check"
Cohesion: 0.14
Nodes (9): clock(), first_second_check(), overlay_notes(), quality_check(), review_fixes(), visual_review(), length_plan(), test_review_is_told_the_drawings_are_deliberate() (+1 more)

### Community 55 - "scene_kit.py"
Cohesion: 0.08
Nodes (31): gait(), hop_off(), legs(), sink(), walk(), facing_now(), _footprints(), _ground() (+23 more)

### Community 56 - "test_h3_handoff.py"
Cohesion: 0.19
Nodes (13): unpack_clips(), handoff(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated(), test_flagged_start_picture_is_not_sent(), test_handoff_picks_up_clips_zip(), test_handoff_records_which_file_made_the_clip(), test_handoff_writes_jobs_and_zip() (+5 more)

### Community 57 - "choose_images"
Cohesion: 0.19
Nodes (14): choose_images(), apply_look_scenes(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan() (+6 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.06
Nodes (41): _cast_note(), pick_model(), render_opener(), resolve_models(), review(), review_frames(), scale_beats(), to_glb() (+33 more)

### Community 59 - "pack_people.py"
Cohesion: 0.26
Nodes (6): base_name(), clip_name(), front(), height(), main(), stride()

### Community 60 - "test_opener_checks.py"
Cohesion: 0.30
Nodes (10): results(), test_blade_face(), test_cut_result(), test_edge_leads(), test_first_frame(), test_hidden(), test_in_frame(), test_moves_visibly() (+2 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.10
Nodes (22): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+14 more)

### Community 62 - "test_story.py"
Cohesion: 0.19
Nodes (11): check_twists(), story_problems(), test_no_hook_setting_no_hook_check(), test_rules_accept_opener_setting(), test_story_problems(), test_story_problems_flags_summary_hook(), test_story_problems_money_claim(), test_twist_check_keeps_topics_on_null_or_bad_replies() (+3 more)

### Community 63 - "opener_scene.py"
Cohesion: 0.08
Nodes (23): State, beat_actors(), build_set(), camera(), dress_set(), first_hit(), hold_offscreen(), main() (+15 more)

### Community 64 - "look_toon.py"
Cohesion: 0.27
Nodes (4): apply(), ink(), outline(), toon()

### Community 65 - "render_remotion"
Cohesion: 0.16
Nodes (9): render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_old_state_renders_plain() (+1 more)

### Community 66 - "approve_candidate"
Cohesion: 0.26
Nodes (8): approve_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes(), test_candidate_names_unique_across_kinds()

### Community 67 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 68 - "test_blender_scene.py"
Cohesion: 0.07
Nodes (42): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+34 more)

### Community 69 - "edit_scripts"
Cohesion: 0.18
Nodes (6): pictures_of(), direct_scripts(), edit_scripts(), narration_lines(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules()

### Community 70 - "invent_component"
Cohesion: 0.12
Nodes (16): invent_component(), attempt(), invent_styles(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others() (+8 more)

### Community 71 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 73 - "people_standin.py"
Cohesion: 0.29
Nodes (5): body(), clip(), key(), main(), part()

### Community 74 - "trim_borders"
Cohesion: 0.22
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 76 - "QuestionBeat.tsx"
Cohesion: 0.33
Nodes (4): FONT, theme, CLAMP, KineticTitle()

### Community 77 - "captions"
Cohesion: 0.29
Nodes (5): ass_time(), caption_lines(), captions(), styled(), ass_colour()

### Community 79 - "clean_pics"
Cohesion: 0.25
Nodes (4): catalog_text(), clean_pics(), is_usable(), usable()

### Community 80 - "builds"
Cohesion: 0.25
Nodes (4): builds(), test_chicken_live_plan(), test_subject_without_follow(), test_walk_stops_short_of_obstacles()

### Community 81 - "_clip"
Cohesion: 0.33
Nodes (3): _clip(), idle(), fcurves_of()

### Community 82 - "gemini_model"
Cohesion: 0.40
Nodes (4): gemini_model(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_gemini_timeout_switches_to_flash()

### Community 83 - "people_lib"
Cohesion: 0.33
Nodes (3): people_lib(), test_missing_slot_is_skipped(), test_person_walks_across()

### Community 85 - "render"
Cohesion: 0.04
Nodes (31): scene_frames(), fills_frame(), fit_font(), frame_maker(), graphic_low(), graphic_overlay(), person_card(), thumbnail() (+23 more)

## Knowledge Gaps
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `pathlib`, `ffmpeg`, `gpu.py`, `test_edit_project.py`, `re`, `test_full_scenes.py`, `make_paper`, `test_blender_render.py`, `ClipReader`, `full_cues`, `audio_mix.py`, `json`, `plan_rules.py`, `main`, `first_second_check`, `choose_images`, `test_opener_render.py`, `opener_scene.py`, `render_remotion`, `edit_plan`, `make_sfx`, `trim_borders`, `captions`, `srt`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.14583333333333334 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `Shots`, `build_scene.py`, `json`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.13513513513513514 - nodes in this community are weakly interconnected._
- **Why does `catalog_pool()` connect `test_pictures_first.py` to `prepare_topic`, `ask_ai`, `pathlib`, `json`, `test_rules.py`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Should `code_custom_scenes` be split into smaller, more focused modules?**
  _Cohesion score 0.11333333333333333 - nodes in this community are weakly interconnected._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.12857142857142856 - nodes in this community are weakly interconnected._