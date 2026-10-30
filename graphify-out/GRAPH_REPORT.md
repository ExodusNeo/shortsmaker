# Graph Report - ShortsMaker  (2026-10-30)

## Corpus Check
- 108 files · ~118,335 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .canvas 1, .ipynb 1)

## Summary
- 1584 nodes · 4283 edges · 79 communities (74 shown, 5 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 103 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `11ad5320`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- style/index.ts
- Graphics.tsx
- catalog_pool
- h3_run.py
- ask_ai
- split_make_shorts.py
- code_custom_scenes
- words_of
- guarded.tsx
- Paper
- test_h3_handoff.py
- test_blender_scene.py
- approve_candidate
- make
- test_rules.py
- Journey.tsx
- toolkit.tsx
- pool_of
- write_scripts
- Local GPU Worker
- re
- local_clips
- test_full_scenes.py
- BigNumber.tsx
- test_blender_render.py
- use_opener
- frame_maker
- full_cues
- captions
- look.py
- parts.py
- clean_full
- render_remotion
- templates.py
- image_sources.py
- style_library
- run_draft
- main
- ffmpeg
- json
- build_scene.py
- Short.tsx
- gpu.py
- audio_mix.py
- rescue_graphics
- prepare_topic
- Halftone.tsx
- topic_ideas.py
- invent_component
- owner
- main
- edit_plan
- state
- visual_review
- style_placeholders
- test_story.py
- picking
- make_paper
- capture_prompts
- test_blender_plan.py
- check_twists
- require_rules
- clean_sound
- story_sound
- ask
- choose_images
- limit_full
- StopPicker
- edit_scripts
- fix_short
- limit_style
- qwen_voice.py
- first_second_check
- trend_research
- drawn_thumbnail
- paint_instead
- render
- trim_borders

## God Nodes (most connected - your core abstractions)
1. `render()` - 64 edges
2. `write_scripts()` - 48 edges
3. `ask_ai()` - 37 edges
4. `skinOf()` - 29 edges
5. `main()` - 26 edges
6. `Paper()` - 25 edges
7. `choose_images()` - 24 edges
8. `clean_full()` - 23 edges
9. `words_of()` - 22 edges
10. `Bridge` - 20 edges

## Surprising Connections (you probably didn't know these)
- `test_numbers()` --calls--> `say_number()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_word_counts_match_the_scene_splitter()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_caption_words_keep_what_is_written()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_every_aligned_word_is_in_the_aligner_alphabet()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_a_stopped_run_keeps_the_default_channel()` --calls--> `main()`  [EXTRACTED]
  tests/test_rules.py → shortsmaker/cli.py

## Import Cycles
- 3-file cycle: `shortsmaker/blender_plan.py -> shortsmaker/picture_pool.py -> shortsmaker/writing.py -> shortsmaker/blender_plan.py`

## Communities (79 total, 5 thin omitted)

### Community 0 - "style/index.ts"
Cohesion: 0.13
Nodes (22): FONT, theme, InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP (+14 more)

### Community 1 - "Graphics.tsx"
Cohesion: 0.15
Nodes (32): card, clamp, DotGrid(), formatStat(), MarkCard(), Props, StatCard(), TimelineCard() (+24 more)

### Community 2 - "catalog_pool"
Cohesion: 0.12
Nodes (12): write_json(), catalog_entries(), catalog_pool(), fake_ai, test_catalog_both_empty_stops_uncached(), test_catalog_empty_pool_no_ai(), test_catalog_empty_reply_asks_other_ai(), test_catalog_failure_stops() (+4 more)

### Community 3 - "h3_run.py"
Cohesion: 0.11
Nodes (6): call(), fit_start(), frames(), graph(), main(), saved_file()

### Community 4 - "ask_ai"
Cohesion: 0.12
Nodes (14): ask_ai(), gemini_model(), quota_exhausted(), run_agy(), test_quota_fallback_both_ways(), test_argon_out_of_quota_switches_to_flash(), fake_run(), test_claude_pinned_to_opus_high() (+6 more)

### Community 5 - "split_make_shorts.py"
Cohesion: 0.09
Nodes (20): arg_names(), chunks_of(), defined_names(), global_names(), visit(), identifiers(), import_lines(), is_main_guard() (+12 more)

### Community 7 - "code_custom_scenes"
Cohesion: 0.12
Nodes (13): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), preview_custom(), preview_sheet() (+5 more)

### Community 8 - "words_of"
Cohesion: 0.10
Nodes (16): archive_films(), film_frames(), nasa_films(), pixabay_films(), graphic_low(), archive_images(), nasa_images(), nasa_search() (+8 more)

### Community 9 - "guarded.tsx"
Cohesion: 0.10
Nodes (22): ExampleChain(), ExampleEvidence(), Box, boxAt(), Card(), clamp, Connect(), fitCard() (+14 more)

### Community 10 - "Paper"
Cohesion: 0.13
Nodes (28): Board(), clamp, layout(), LAYOUTS, lerp(), Print, clamp, DocumentScene() (+20 more)

### Community 11 - "test_h3_handoff.py"
Cohesion: 0.07
Nodes (37): h3_problems(), h3_prompt(), sentence_groups(), unpack_clips(), build(), add(), main(), fake_ai() (+29 more)

### Community 12 - "test_blender_scene.py"
Cohesion: 0.18
Nodes (20): changed(), count(), manifest(), near(), plan_with(), render(), test_a_failing_pier_falls_with_its_red_copy(), test_bridge_stands_until_the_build_starts_over() (+12 more)

### Community 13 - "approve_candidate"
Cohesion: 0.20
Nodes (10): approve_candidate(), save_candidate(), candidate_in(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure(), test_approve_rolls_back_when_the_check_crashes() (+2 more)

### Community 14 - "make"
Cohesion: 0.14
Nodes (9): caption_layer(), make(), master_gain(), project_xml(), remove(), short_folder(), test_melt_plays_it_with_the_captions_on_top(), test_timeline_has_scenes_captions_sound_and_markers() (+1 more)

### Community 15 - "test_rules.py"
Cohesion: 0.18
Nodes (22): parse_rules(), make(), stop_text(), test_a_stopped_run_keeps_the_default_channel(), test_bad_min_pictures_stops(), test_blender_needs_a_build_plan_section(), test_bom_and_crlf_load_the_same(), test_draft_stops() (+14 more)

### Community 16 - "Journey.tsx"
Cohesion: 0.12
Nodes (17): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+9 more)

### Community 17 - "toolkit.tsx"
Cohesion: 0.27
Nodes (19): CustomScene(), Custom0(), Custom1(), Custom2(), Custom3(), skinOf(), appear(), CalloutTag() (+11 more)

### Community 18 - "pool_of"
Cohesion: 0.15
Nodes (17): catalog_text(), clean_pics(), is_usable(), save_pool(), usable(), entry(), pic_short(), pool_of() (+9 more)

### Community 19 - "write_scripts"
Cohesion: 0.14
Nodes (19): write_scripts(), passing(), prepare(), planning, planning_ai(), test_all_weak_returns_empty(), test_both_mode_pools_follow_reply_position(), prepare() (+11 more)

### Community 20 - "Local GPU Worker"
Cohesion: 0.14
Nodes (7): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video()

### Community 21 - "re"
Cohesion: 0.09
Nodes (11): logbook_results(), vault_page(), vault_refresh(), mark_details(), parse_scene_money(), max_full(), max_full_planned(), clean_style_code() (+3 more)

### Community 22 - "local_clips"
Cohesion: 0.12
Nodes (11): cover_crop(), cut_owner_clip(), h3_prompts(), local_clips(), local_job(), motion_prompt(), start_picture_problems(), veo_handoff() (+3 more)

### Community 23 - "test_full_scenes.py"
Cohesion: 0.18
Nodes (5): hex_rgb(), luminance(), tsc_check(), prune_work(), test_short_credit()

### Community 24 - "BigNumber.tsx"
Cohesion: 0.20
Nodes (14): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), fmtBar(), gridFor() (+6 more)

### Community 25 - "test_blender_render.py"
Cohesion: 0.15
Nodes (15): BlenderFailed, peaks(), render_clips(), _run(), scene_frames(), fake_blender(), short(), test_changed_blender_code_redraws() (+7 more)

### Community 26 - "use_opener"
Cohesion: 0.33
Nodes (4): use_opener(), fresh(), test_use_opener_ai_clip_replaces_graphic(), test_use_opener_without_graphic()

### Community 27 - "frame_maker"
Cohesion: 0.09
Nodes (12): ClipReader, draw_card(), draw_graphic(), fit_font(), frame_maker(), frame(), graphic_overlay(), person_card() (+4 more)

### Community 28 - "full_cues"
Cohesion: 0.06
Nodes (22): sfx_events(), scene_cues(), full_props(), full_cues(), spoken_at(), spoken_span(), _board(), _jpg() (+14 more)

### Community 29 - "captions"
Cohesion: 0.16
Nodes (7): ass_time(), caption_lines(), captions(), styled(), speak(), tts(), ass_colour()

### Community 30 - "look.py"
Cohesion: 0.33
Nodes (4): collection(), ink_lines(), linear(), setup()

### Community 31 - "parts.py"
Cohesion: 0.14
Nodes (23): material(), bbox_size(), box(), car(), cylinder(), deck(), eyebar(), fastener() (+15 more)

### Community 32 - "clean_full"
Cohesion: 0.11
Nodes (17): clean_full(), word(), clean_graphic(), contains(), coords(), is_num(), number_figures(), show_number() (+9 more)

### Community 33 - "render_remotion"
Cohesion: 0.13
Nodes (11): short_skin(), render_remotion(), remotion(), render(), run_remotion_with_fallback(), style_props(), swap_inventions(), test_clean_full_custom_and_skin() (+3 more)

### Community 34 - "templates.py"
Cohesion: 0.19
Nodes (14): Bridge, build(), cable_stayed_bridge(), _edge_girders(), eyebar_chain_bridge(), focus_object(), girder_bridge(), _hung_deck() (+6 more)

### Community 35 - "image_sources.py"
Cohesion: 0.11
Nodes (11): article_images(), commons_search(), openverse_images(), thumb_url(), usable_license(), wm_files(), gather_pool(), stubbed (+3 more)

### Community 36 - "style_library"
Cohesion: 0.15
Nodes (11): clean_invention(), clean_look(), clean_transition(), settle_style(), style_library(), write_style_index(), test_invented_look_needs_fallback(), test_library_entries_have_fields() (+3 more)

### Community 37 - "run_draft"
Cohesion: 0.33
Nodes (7): draft_reply(), run_draft(), test_draft_blender_channel_needs_build_plan(), test_draft_keeps_ai_headings_inside_their_section(), test_draft_never_overwrites(), test_draft_retries_once_then_stops(), test_draft_settings_come_from_code()

### Community 38 - "main"
Cohesion: 0.20
Nodes (3): main(), Failure, key()

### Community 39 - "ffmpeg"
Cohesion: 0.19
Nodes (8): cosy_instruct(), local_voice(), split_takes(), voicestudio_unload(), duration(), ffmpeg(), is_loop_short(), test_a_take_is_cut_between_the_scenes_words()

### Community 40 - "json"
Cohesion: 0.16
Nodes (8): freesound_fetch(), load_channel(), load_pool(), pictures_of(), pool_pictures(), search_suggestions(), seo_pass(), direct_scripts()

### Community 41 - "build_scene.py"
Cohesion: 0.16
Nodes (4): direction(), keyloc(), keyvis(), Shots

### Community 42 - "Short.tsx"
Cohesion: 0.13
Nodes (19): Captions(), PersonCard(), Root(), Background(), flashAlpha(), GraphicFor(), Move, Scene (+11 more)

### Community 43 - "gpu.py"
Cohesion: 0.07
Nodes (15): code_version(), crop_film_bytes(), shot_span(), fills_frame(), comfy_call(), moss_graph(), moss_images(), voicestudio_up() (+7 more)

### Community 45 - "rescue_graphics"
Cohesion: 0.13
Nodes (9): commons_films(), wm_get(), full_formats(), opener_graphic(), rescue_graphics(), article_text(), fact_check(), test_fact_check_drops_full() (+1 more)

### Community 46 - "prepare_topic"
Cohesion: 0.33
Nodes (5): pool_folder(), prepare_topic(), test_empty_pool_drops_topic_without_ai(), test_small_pool_skips_ai(), test_min_pictures_from_settings()

### Community 47 - "Halftone.tsx"
Cohesion: 0.17
Nodes (23): InventedLook(), drawCover(), FILL, luminance(), noise(), stretch(), useOnceCanvas(), draw() (+15 more)

### Community 48 - "topic_ideas.py"
Cohesion: 0.13
Nodes (11): clash(), fetch_ideas(), pages(), parse_ideas(), pick_ideas(), _words(), test_clash_needs_every_name_word(), test_fetch_is_cached() (+3 more)

### Community 49 - "invent_component"
Cohesion: 0.16
Nodes (8): invent_component(), attempt(), invent_styles(), lint_style_code(), style_preview(), style_rules(), test_invention_lint_failure_uses_fallback(), test_placeholders_match_the_slots()

### Community 50 - "owner"
Cohesion: 0.12
Nodes (9): owner(), _fake_planning(), test_director_prompt_mentions_full(), film(), plan_with(), ask(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library() (+1 more)

### Community 51 - "main"
Cohesion: 0.09
Nodes (14): ask_brain(), ask_count(), ask_number(), ask_yes(), new_channel(), pick_channel(), save_channel(), use_channel() (+6 more)

### Community 52 - "edit_plan"
Cohesion: 0.20
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 53 - "state"
Cohesion: 0.21
Nodes (11): swap_pictures(), real(), run_check(), state(), test_good_opening_or_no_reply_changes_nothing(), test_low_score_opens_on_a_better_real_picture(), test_opener_fix_swaps_once(), test_opener_must_be_a_later_real_picture() (+3 more)

### Community 54 - "visual_review"
Cohesion: 0.18
Nodes (8): log_short(), clock(), overlay_notes(), review_fixes(), visual_review(), test_review_is_told_the_drawings_are_deliberate(), test_review_knows_what_dims_a_picture_on_purpose(), test_review_fix_kinds()

### Community 55 - "style_placeholders"
Cohesion: 0.21
Nodes (9): restore_style_slots(), style_placeholders(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback(), test_invention_passes_into_slot(), run(), test_slots_restored_after_render() (+1 more)

### Community 56 - "test_story.py"
Cohesion: 0.31
Nodes (5): story_problems(), test_no_hook_setting_no_hook_check(), test_story_problems(), test_story_problems_flags_summary_hook(), test_story_problems_money_claim()

### Community 57 - "picking"
Cohesion: 0.27
Nodes (11): picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends(), test_choose_old_path_unchanged() (+3 more)

### Community 58 - "make_paper"
Cohesion: 0.25
Nodes (4): ink_silhouette(), make_paper(), test_ink_silhouette(), test_make_paper()

### Community 59 - "capture_prompts"
Cohesion: 0.29
Nodes (4): rewrite_paint_prompts(), capture_prompts(), ask(), test_strange_history_prompts_unchanged()

### Community 60 - "test_blender_plan.py"
Cohesion: 0.07
Nodes (27): radians(), make_sfx(), clamp(), clean_build(), default_build(), ending(), panels(), pick() (+19 more)

### Community 61 - "check_twists"
Cohesion: 0.47
Nodes (5): check_twists(), test_twist_check_keeps_topics_on_null_or_bad_replies(), test_twist_check_needs_wikipedia_text(), test_twist_check_rewrites_a_legend_before_writing(), twist_short()

### Community 62 - "require_rules"
Cohesion: 0.25
Nodes (5): load_rules(), min_real_pictures(), require_rules(), test_load_rules_sets_session(), test_missing_rules_file_is_drafted()

### Community 63 - "clean_sound"
Cohesion: 0.40
Nodes (3): clean_sound(), limit_sounds(), test_clean_sound()

### Community 64 - "story_sound"
Cohesion: 0.40
Nodes (4): story_sound(), test_story_sound_library(), fetch(), _tone_wav()

### Community 65 - "ask"
Cohesion: 0.22
Nodes (4): ask(), test_look_check_fixes_code(), test_review_uses_unused_pool_pictures_before_painting(), test_rewrite_paint_prompts()

### Community 66 - "choose_images"
Cohesion: 0.11
Nodes (9): film_piece(), film_ffmpeg(), get_image(), ov_get(), choose_images(), full_pictures(), apply_look_scenes(), test_board_pictures_attached() (+1 more)

### Community 69 - "edit_scripts"
Cohesion: 0.17
Nodes (6): quality_check(), edit_scripts(), length_plan(), narration_lines(), test_solo_edit_scripts_uses_same_ai(), test_editor_gets_one_second_pass_for_broken_rules()

### Community 70 - "fix_short"
Cohesion: 0.11
Nodes (12): fix_short(), use_picture_from(), apply_review_fixes(), paint_new(), test_fix_bat_explains_a_drawn_short(), _review_state(), test_auto_fix_graphic(), test_new_picture_drops_mark() (+4 more)

### Community 72 - "qwen_voice.py"
Cohesion: 0.11
Nodes (15): align(), align_words(), main(), say_number(), speak(), spoken_sentence(), spoken_tokens(), studio_speak() (+7 more)

### Community 75 - "first_second_check"
Cohesion: 0.15
Nodes (7): full_summary(), first_second_check(), fix_opener_graphic(), weak_opener_graphic(), test_opener_prompt_shows_each_scenes_line_and_picture(), test_full_summary(), test_weak_opener_graphic_fixes_then_handoff()

### Community 77 - "trend_research"
Cohesion: 0.29
Nodes (4): channel_url(), seed_ideas(), trend_research(), yt_list()

### Community 78 - "drawn_thumbnail"
Cohesion: 0.31
Nodes (7): drawn_thumbnail(), drawn_short(), jpeg(), test_film_opener_is_skipped_and_bad_bytes_fall_back(), get(), test_no_photo_uses_a_drawing_and_says_so(), test_thumbnail_uses_the_real_photo()

### Community 79 - "paint_instead"
Cohesion: 0.18
Nodes (4): gemini_images(), to_vertical(), paint_instead(), test_remotion_failure_paints()

### Community 85 - "render"
Cohesion: 0.12
Nodes (11): short_credit(), graphics_count(), wants_remotion(), srt(), drawn_choices(), load_state(), render(), save_state() (+3 more)

### Community 86 - "trim_borders"
Cohesion: 0.25
Nodes (4): is_stereo(), trim_borders(), border(), plain()

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render()` connect `render` to `words_of`, `approve_candidate`, `make`, `re`, `local_clips`, `test_full_scenes.py`, `test_blender_render.py`, `use_opener`, `frame_maker`, `full_cues`, `captions`, `render_remotion`, `ffmpeg`, `gpu.py`, `audio_mix.py`, `rescue_graphics`, `main`, `edit_plan`, `visual_review`, `make_paper`, `test_blender_plan.py`, `story_sound`, `choose_images`, `edit_scripts`, `fix_short`, `first_second_check`, `drawn_thumbnail`, `paint_instead`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Should `style/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.12802275960170698 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `main` to `templates.py`, `json`, `build_scene.py`, `look.py`, `parts.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Should `Graphics.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._
- **Why does `write_scripts()` connect `write_scripts` to `ask_ai`, `test_pictures_first.py`, `words_of`, `pool_of`, `re`, `test_full_scenes.py`, `clean_full`, `style_library`, `json`, `rescue_graphics`, `prepare_topic`, `topic_ideas.py`, `owner`, `main`, `capture_prompts`, `test_blender_plan.py`, `check_twists`, `clean_sound`, `limit_full`, `edit_scripts`, `limit_style`, `trend_research`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `catalog_pool` be split into smaller, more focused modules?**
  _Cohesion score 0.12280701754385964 - nodes in this community are weakly interconnected._
- **Should `h3_run.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11462450592885376 - nodes in this community are weakly interconnected._