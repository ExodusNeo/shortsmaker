# Graph Report - ShortsMaker  (2026-10-27)

## Corpus Check
- 118 files · ~135,617 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .blend 9, (none) 3, .canvas 1)

## Summary
- 1891 nodes · 5057 edges · 70 communities (62 shown, 8 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 122 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7578a064`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- code_custom_scenes
- toolkit.tsx
- ask_ai
- split_make_shorts.py
- test_full_scenes.py
- test_h3_handoff.py
- frame_maker
- Paper
- build_set
- local_clips
- rewrite_paint_prompts
- guarded.tsx
- subprocess
- test_rules.py
- Journey.tsx
- BigNumber.tsx
- test_pictures_first.py
- write_scripts
- Local GPU Worker
- style_library
- gather_pool
- film_piece
- render_remotion
- test_blender_plan.py
- short_with
- ClipReader
- look.py
- words_of
- render
- parts.py
- test_package.py
- prepare_topic
- templates.py
- invent_component
- test_story.py
- apply_review_fixes
- math
- h3_run.py
- audio_mix.py
- main
- Short.tsx
- gpu.py
- test_opener_scene.py
- moves.py
- test_style.py
- Halftone.tsx
- footage.py
- clean_pics
- edit_plan
- json
- Shots
- test_first_second.py
- h3_problems
- scene_kit.py
- full_cues
- choose_images
- test_opener_render.py
- h3_prompt
- test_short_credit
- opener_checks.py
- test_blender_link.py
- opener_scene.py
- test_owner_clip_is_cut_again_for_the_scene_it_now_sits_in
- limit_style
- test_blender_scene.py
- owner
- approve_candidate
- trim_borders

## God Nodes (most connected - your core abstractions)
1. `render()` - 62 edges
2. `write_scripts()` - 45 edges
3. `ask_ai()` - 39 edges
4. `cut()` - 30 edges
5. `skinOf()` - 29 edges
6. `main()` - 27 edges
7. `render_opener()` - 27 edges
8. `Paper()` - 25 edges
9. `choose_images()` - 24 edges
10. `words_of()` - 22 edges

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

## Communities (70 total, 8 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "code_custom_scenes"
Cohesion: 0.13
Nodes (12): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), redraw_custom() (+4 more)

### Community 3 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 4 - "ask_ai"
Cohesion: 0.12
Nodes (14): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high() (+6 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 7 - "test_h3_handoff.py"
Cohesion: 0.19
Nodes (13): unpack_clips(), handoff(), test_all_start_pictures_flagged_skips_pause(), test_duplicate_clip_names_deduplicated(), test_flagged_start_picture_is_not_sent(), test_handoff_picks_up_clips_zip(), test_handoff_records_which_file_made_the_clip(), test_handoff_writes_jobs_and_zip() (+5 more)

### Community 8 - "frame_maker"
Cohesion: 0.12
Nodes (8): fills_frame(), fit_font(), frame_maker(), graphic_overlay(), person_card(), thumbnail(), credit_tag_image(), fallback_graphic()

### Community 9 - "Paper"
Cohesion: 0.13
Nodes (28): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+20 more)

### Community 10 - "build_set"
Cohesion: 0.12
Nodes (9): clear_distance(), build_set(), ground_material(), stand_on(), load_model(), material(), merge(), surface_z() (+1 more)

### Community 11 - "local_clips"
Cohesion: 0.16
Nodes (9): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), motion_prompt(), start_picture_problems(), veo_handoff(), video_encoder() (+1 more)

### Community 12 - "rewrite_paint_prompts"
Cohesion: 0.18
Nodes (5): rewrite_paint_prompts(), ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 13 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 14 - "subprocess"
Cohesion: 0.06
Nodes (19): studio_speak(), caption_layer(), make(), master_gain(), project_xml(), remove(), shot_span(), split_takes() (+11 more)

### Community 15 - "test_rules.py"
Cohesion: 0.09
Nodes (37): load_rules(), min_real_pictures(), parse_rules(), test_channels_have_opener_rules(), capture_prompts(), ask(), draft_reply(), make() (+29 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "BigNumber.tsx"
Cohesion: 0.20
Nodes (14): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+6 more)

### Community 18 - "test_pictures_first.py"
Cohesion: 0.12
Nodes (28): catalog_entries(), catalog_pool(), save_pool(), entry(), fake_ai, film(), pic_short(), pool_of() (+20 more)

### Community 19 - "write_scripts"
Cohesion: 0.11
Nodes (19): pictures_of(), limit_full(), edit_scripts(), length_plan(), narration_lines(), write_scripts(), test_limit_full(), test_solo_edit_scripts_uses_same_ai() (+11 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "style_library"
Cohesion: 0.11
Nodes (13): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), style_rules(), write_style_index(), direct_scripts() (+5 more)

### Community 22 - "gather_pool"
Cohesion: 0.12
Nodes (8): article_images(), commons_search(), thumb_url(), wm_files(), gather_pool(), stubbed, test_gather_pool_shape(), test_gather_pool_skip_and_limits()

### Community 24 - "render_remotion"
Cohesion: 0.10
Nodes (13): short_skin(), ink_silhouette(), make_paper(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props() (+5 more)

### Community 25 - "test_blender_plan.py"
Cohesion: 0.05
Nodes (44): clamp(), clean_build(), default_build(), ending(), panels(), pick(), plan_builds(), thumbnail_order() (+36 more)

### Community 26 - "short_with"
Cohesion: 0.23
Nodes (14): fake_ai(), short_with(), test_all_closeup_marked_scenes_skip_pause(), test_missing_scene_is_asked_again(), run(), test_retries_only_failing_scene_with_reason(), run(), test_scene_number_given_as_text_is_accepted() (+6 more)

### Community 27 - "ClipReader"
Cohesion: 0.11
Nodes (8): ClipReader, draw_card(), draw_graphic(), flash_alpha(), frame(), shot(), write_frames(), test_hard_cuts_never_blend_scenes()

### Community 28 - "look.py"
Cohesion: 0.21
Nodes (7): collection(), ink_lines(), linear(), material(), setup(), _mesh(), _obj()

### Community 29 - "words_of"
Cohesion: 0.08
Nodes (26): clean_sound(), limit_sounds(), graphic_low(), rescue_graphics(), clean_full(), word(), clean_graphic(), contains() (+18 more)

### Community 30 - "render"
Cohesion: 0.05
Nodes (27): gemini_images(), short_credit(), clock(), full_summary(), graphics_count(), to_vertical(), is_loop_short(), paint_instead() (+19 more)

### Community 31 - "parts.py"
Cohesion: 0.16
Nodes (20): bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener(), gusset_plate() (+12 more)

### Community 32 - "test_package.py"
Cohesion: 0.22
Nodes (5): scene_cues(), test_counter_finishes_before_it_leaves(), test_graphic_card_hold_duration(), test_person_card_hold_and_exit_gap(), test_scene_hold_padding()

### Community 33 - "prepare_topic"
Cohesion: 0.22
Nodes (7): contact_sheets(), load_pool(), pool_folder(), prepare_topic(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip(), test_small_pool_skips_ai()

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), dress(), _edge_girders(), eyebar_chain_bridge(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "invent_component"
Cohesion: 0.10
Nodes (18): invent_component(), attempt(), invent_styles(), lint_style_code(), restore_style_slots(), style_placeholders(), style_preview(), swap_inventions() (+10 more)

### Community 36 - "test_story.py"
Cohesion: 0.06
Nodes (29): align_words(), say_number(), speak(), spoken_sentence(), spoken_tokens(), sentence_groups(), check_twists(), story_problems() (+21 more)

### Community 37 - "apply_review_fixes"
Cohesion: 0.12
Nodes (10): use_picture_from(), apply_review_fixes(), paint_new(), pool_pictures(), _review_state(), test_auto_fix_graphic(), test_new_picture_drops_mark(), test_paint_new_clears_full() (+2 more)

### Community 39 - "h3_run.py"
Cohesion: 0.22
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 40 - "audio_mix.py"
Cohesion: 0.10
Nodes (13): ass_time(), caption_lines(), captions(), styled(), music_gain(), speak(), story_sound(), tts() (+5 more)

### Community 41 - "main"
Cohesion: 0.16
Nodes (5): keyvis(), main(), Failure, key(), focus_object()

### Community 42 - "Short.tsx"
Cohesion: 0.13
Nodes (19): Captions(), PersonCard(), Root(), Background(), flashAlpha(), GraphicFor(), Move, Scene (+11 more)

### Community 43 - "gpu.py"
Cohesion: 0.08
Nodes (13): align(), main(), code_version(), comfy_call(), local_job(), local_voice(), moss_graph(), moss_images() (+5 more)

### Community 44 - "test_opener_scene.py"
Cohesion: 0.07
Nodes (41): clean_opener(), _expect(), fix_plan(), _num(), plan_openers(), ask(), _size(), _stroke() (+33 more)

### Community 45 - "moves.py"
Cohesion: 0.07
Nodes (32): apply(), bm_area(), box_of(), centre(), clusters(), edge_point_local(), fall(), fly_off() (+24 more)

### Community 46 - "test_style.py"
Cohesion: 0.15
Nodes (9): wants_remotion(), apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics() (+1 more)

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "footage.py"
Cohesion: 0.07
Nodes (18): archive_films(), commons_films(), crop_film_bytes(), film_frames(), nasa_films(), pixabay_films(), archive_images(), nasa_images() (+10 more)

### Community 49 - "clean_pics"
Cohesion: 0.25
Nodes (4): catalog_text(), clean_pics(), is_usable(), usable()

### Community 50 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 51 - "json"
Cohesion: 0.04
Nodes (39): freesound_fetch(), ask_brain(), ask_count(), ask_number(), ask_yes(), channel_url(), load_channel(), new_channel() (+31 more)

### Community 52 - "Shots"
Cohesion: 0.24
Nodes (3): direction(), keyloc(), Shots

### Community 53 - "test_first_second.py"
Cohesion: 0.16
Nodes (15): logbook_results(), swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_logbook_marks_tiny_samples(), test_low_score_opens_on_a_better_real_picture() (+7 more)

### Community 55 - "scene_kit.py"
Cohesion: 0.10
Nodes (28): cut(), gait(), hop_off(), legs(), sink(), walk(), place_actors(), add_body() (+20 more)

### Community 56 - "full_cues"
Cohesion: 0.06
Nodes (20): sfx_events(), get_image(), openverse_images(), ov_get(), full_props(), full_pictures(), full_cues(), spoken_at() (+12 more)

### Community 57 - "choose_images"
Cohesion: 0.27
Nodes (11): choose_images(), picking, planned_short(), scene(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends(), test_choose_old_path_unchanged() (+3 more)

### Community 58 - "test_opener_render.py"
Cohesion: 0.11
Nodes (25): render_opener(), review(), review_frames(), scale_beats(), Env, short(), test_beats_scaled_into_scene(), test_cc_by_credit() (+17 more)

### Community 61 - "opener_checks.py"
Cohesion: 0.12
Nodes (15): area(), at(), blade_face(), cut_result(), edge_leads(), edge_point(), first_frame(), hidden() (+7 more)

### Community 62 - "test_blender_link.py"
Cohesion: 0.08
Nodes (23): allowed_licence(), attribution(), call(), credit(), fetch_model(), in_library(), LinkError, ping() (+15 more)

### Community 63 - "opener_scene.py"
Cohesion: 0.11
Nodes (17): State, in_frame(), burst(), camera(), checks(), dress_set(), feather(), feather_colours() (+9 more)

### Community 68 - "test_blender_scene.py"
Cohesion: 0.08
Nodes (29): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+21 more)

### Community 69 - "owner"
Cohesion: 0.12
Nodes (6): owner(), _fake_planning(), test_director_prompt_mentions_full(), planning_ai(), still(), reply()

### Community 70 - "approve_candidate"
Cohesion: 0.15
Nodes (13): approve_candidate(), library_menu(), reject_candidate(), save_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library() (+5 more)

### Community 74 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

## Knowledge Gaps
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `test_full_scenes.py`, `frame_maker`, `local_clips`, `subprocess`, `render_remotion`, `test_blender_plan.py`, `ClipReader`, `words_of`, `test_package.py`, `apply_review_fixes`, `math`, `audio_mix.py`, `gpu.py`, `test_style.py`, `footage.py`, `edit_plan`, `json`, `full_cues`, `choose_images`, `opener_scene.py`, `approve_candidate`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12802275960170698 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `math`, `json`, `Shots`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `prepare_topic`, `limit_style`, `ask_ai`, `test_story.py`, `test_full_scenes.py`, `owner`, `test_opener_scene.py`, `test_style.py`, `test_rules.py`, `footage.py`, `clean_pics`, `test_pictures_first.py`, `json`, `test_first_second.py`, `style_library`, `test_blender_plan.py`, `words_of`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Should `code_custom_scenes` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `ask_ai` be split into smaller, more focused modules?**
  _Cohesion score 0.11904761904761904 - nodes in this community are weakly interconnected._