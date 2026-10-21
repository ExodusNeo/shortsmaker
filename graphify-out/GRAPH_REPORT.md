# Graph Report - ShortsMaker  (2026-10-21)

## Corpus Check
- 57 files · ~79,020 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 940 nodes · 2334 edges · 50 communities (44 shown, 6 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 52 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Full-Screen Motion Graphics
- Style Library Looks & Transitions
- Remotion Cards & Captions
- Local GPU Workers
- Shared Imports & Downloads
- Archive Picture & Film Sources
- Run Menu & Channel Setup
- Python Frame Renderer
- Script Team (Write/Edit/Direct)
- Quality Checks & Captions
- Map Journey Scene
- Full-Scene Validation
- Usable Picture Catalog
- Style Invention Coding
- Wikipedia & Wikimedia Research
- Picture List & Contact Sheets
- Image Choosing
- State & Logbook Helpers
- Style Library Approval
- Custom Scene Coder
- Look Scene Picking
- AI Painters (MOSS & Gemini)
- Spoken-Word Cue Timing
- Planning Test Fakes
- Callout & Sound Validation
- Voice Pipeline (VoiceStudio)
- AI Planner Calls & Quota
- Style Plan Validation
- SFX & Preview Sheets
- Pictures-First Pool
- AI Video Clips & Encoding
- Motion Graphics Tests
- Remotion Render Prep
- Library Menu & Candidates
- Director Picture Context
- Archive Photo Cleanup
- Edit Plan Writer
- Full-Scene Props
- YouTube Trend Research
- Callout Validation
- TypeScript Checks
- Repaint & Scene Swap
- Invention Fallback Render
- Automatic Review Fixes
- Film Clip Download
- Figure Silhouettes
- Style Guardrails
- Music Loudness
- Motion Graphic Limits
- Style Props for Remotion

## God Nodes (most connected - your core abstractions)
1. `render()` - 50 edges
2. `write_scripts()` - 35 edges
3. `skinOf()` - 29 edges
4. `Paper()` - 25 edges
5. `ask_ai()` - 23 edges
6. `gather_pool()` - 22 edges
7. `choose_images()` - 21 edges
8. `clean_full()` - 20 edges
9. `main()` - 20 edges
10. `pool_of()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `test_caption_words_keep_what_is_written()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_every_aligned_word_is_in_the_aligner_alphabet()` --calls--> `align_words()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_numbers()` --calls--> `say_number()`  [INFERRED]
  tests/test_qwen_voice.py → local_ai/qwen_voice.py
- `test_catalog_junk()` --calls--> `catalog_pool()`  [EXTRACTED]
  tests/test_pictures_first.py → make_shorts.py
- `test_seo_pass_empty_no_ai()` --calls--> `seo_pass()`  [EXTRACTED]
  tests/test_pictures_first.py → make_shorts.py

## Import Cycles
- None detected.

## Communities (50 total, 6 thin omitted)

### Community 0 - "Full-Screen Motion Graphics"
Cohesion: 0.06
Nodes (83): Bars(), BigNumber(), clamp, counter(), Figure(), fmt(), gridFor(), Board() (+75 more)

### Community 1 - "Style Library Looks & Transitions"
Cohesion: 0.09
Nodes (45): InventedLook(), InventedOverlay(), InventedTransition, LOOKS, OVERLAYS, CAPTION_TOP, CLAMP, clamp01() (+37 more)

### Community 2 - "Remotion Cards & Captions"
Cohesion: 0.09
Nodes (50): Captions(), card, clamp, DotGrid(), MarkCard(), Props, StatCard(), TimelineCard() (+42 more)

### Community 3 - "Local GPU Workers"
Cohesion: 0.06
Nodes (19): encoder_args(), images(), main(), parallax(), t5_encoder(), tts(), video(), align() (+11 more)

### Community 4 - "Shared Imports & Downloads"
Cohesion: 0.06
Nodes (11): ass_colour(), ass_time(), caption_lines(), captions(), styled(), catalog_entries(), flash_alpha(), freesound_fetch() (+3 more)

### Community 5 - "Archive Picture & Film Sources"
Cohesion: 0.08
Nodes (18): archive_films(), archive_images(), crop_film_bytes(), fetch(), film_frames(), gather_pool(), load_thumb(), get_image() (+10 more)

### Community 6 - "Run Menu & Channel Setup"
Cohesion: 0.08
Nodes (20): ask_brain(), ask_count(), ask_number(), ask_yes(), fix_short(), gemini_model(), load_channel(), logbook_results() (+12 more)

### Community 7 - "Python Frame Renderer"
Cohesion: 0.09
Nodes (12): ClipReader, credit_tag_image(), draw_card(), draw_graphic(), fallback_graphic(), fit_font(), frame_maker(), frame() (+4 more)

### Community 8 - "Script Team (Write/Edit/Direct)"
Cohesion: 0.14
Nodes (16): edit_scripts(), length_plan(), narration_lines(), write_scripts(), passing(), prepare(), planning, test_all_weak_returns_empty() (+8 more)

### Community 9 - "Quality Checks & Captions"
Cohesion: 0.11
Nodes (13): clock(), graphics_count(), quality_check(), where(), render(), review_fixes(), short_credit(), srt() (+5 more)

### Community 10 - "Map Journey Scene"
Cohesion: 0.13
Nodes (16): clamp, fitPoints(), FOCUS, graticule, INNER, Journey(), level(), LEVELS (+8 more)

### Community 11 - "Full-Scene Validation"
Cohesion: 0.14
Nodes (13): clean_full(), show_number(), test_clean_full_board(), test_clean_full_custom_and_skin(), test_clean_full_document(), test_clean_full_journey(), test_clean_full_keeps_thing(), test_clean_full_limits() (+5 more)

### Community 12 - "Usable Picture Catalog"
Cohesion: 0.24
Nodes (15): clean_pics(), entry(), film(), pic_short(), pool_of(), test_board_item_pics_cleaned(), test_board_item_refuses_film(), test_both_mode_reuses_pools() (+7 more)

### Community 13 - "Style Invention Coding"
Cohesion: 0.15
Nodes (12): clean_style_code(), invent_component(), restore_style_slots(), style_placeholders(), style_preview(), test_failed_invention_keeps_the_others(), test_good_look_check_skips_the_extra_compile(), test_invention_compile_failure_uses_fallback() (+4 more)

### Community 14 - "Wikipedia & Wikimedia Research"
Cohesion: 0.12
Nodes (10): article_images(), article_text(), commons_films(), commons_search(), fact_check(), thumb_url(), usable_license(), wm_files() (+2 more)

### Community 15 - "Picture List & Contact Sheets"
Cohesion: 0.12
Nodes (9): catalog_pool(), contact_sheets(), write_json(), fake_ai, planning_ai(), reply(), test_catalog_empty_pool_no_ai(), test_catalog_failure_stops() (+1 more)

### Community 16 - "Image Choosing"
Cohesion: 0.23
Nodes (12): choose_images(), picking, planned_short(), scene(), still(), test_choose_extra_gather_is_bounded(), test_choose_falls_back_to_plan(), test_choose_keeps_plan_and_appends() (+4 more)

### Community 17 - "State & Logbook Helpers"
Cohesion: 0.14
Nodes (11): duration(), fills_frame(), graphic_low(), load_state(), log_short(), pool_folder(), save_state(), shot_span() (+3 more)

### Community 18 - "Style Library Approval"
Cohesion: 0.17
Nodes (11): approve_candidate(), style_library(), style_rules(), write_style_index(), library_snapshot(), restore_library(), test_approve_adds_to_library(), test_approve_rolls_back_on_tsc_failure() (+3 more)

### Community 19 - "Custom Scene Coder"
Cohesion: 0.16
Nodes (10): clean_tsx_code(), code_custom_scenes(), custom_rules(), fallback_custom_tsx(), lint_custom_code(), look_and_fix(), redraw_custom(), test_code_custom_scenes_fallback() (+2 more)

### Community 20 - "Look Scene Picking"
Cohesion: 0.18
Nodes (8): apply_look_scenes(), plan_with(), ask(), test_apply_look_scenes(), test_director_inventions_are_kept_with_a_spec(), test_director_prompt_lists_library(), test_fact_check_sees_new_graphics(), test_style_sounds()

### Community 21 - "AI Painters (MOSS & Gemini)"
Cohesion: 0.14
Nodes (7): comfy_call(), gemini_images(), moss_graph(), moss_images(), paint_instead(), to_vertical(), test_remotion_failure_paints()

### Community 22 - "Spoken-Word Cue Timing"
Cohesion: 0.16
Nodes (8): full_cues(), scene_cues(), spoken_at(), spoken_span(), test_counter_finishes_before_it_leaves(), test_full_cues_document(), test_full_cues_fallback(), test_full_cues_leave_time_to_finish()

### Community 23 - "Planning Test Fakes"
Cohesion: 0.14
Nodes (8): _fake_planning(), ask(), _review_state(), test_director_prompt_mentions_full(), test_look_check_fixes_code(), test_redraw_failure_paints(), test_review_redraws_custom(), test_rewrite_paint_prompts()

### Community 24 - "Callout & Sound Validation"
Cohesion: 0.18
Nodes (9): word(), clean_sound(), contains(), limit_sounds(), rescue_graphics(), words_of(), test_clean_sound(), test_rescue_respects_caps() (+1 more)

### Community 25 - "Voice Pipeline (VoiceStudio)"
Cohesion: 0.17
Nodes (5): local_job(), local_voice(), voicestudio_unload(), voicestudio_up(), test_local_job_retries_a_hard_crash()

### Community 26 - "AI Planner Calls & Quota"
Cohesion: 0.22
Nodes (6): ask_ai(), one(), mark_details(), quota_exhausted(), run_agy(), test_quota_fallback_both_ways()

### Community 27 - "Style Plan Validation"
Cohesion: 0.20
Nodes (7): clean_invention(), clean_look(), clean_transition(), settle_style(), test_invented_look_needs_fallback(), test_recent_looks_blocked(), test_unknown_names_fall_back()

### Community 28 - "SFX & Preview Sheets"
Cohesion: 0.18
Nodes (6): ffmpeg(), make_sfx(), save(), preview_custom(), preview_sheet(), story_sound()

### Community 29 - "Pictures-First Pool"
Cohesion: 0.24
Nodes (8): load_pool(), prepare_topic(), save_pool(), test_corrupt_pool_and_catalog_redone(), test_empty_pool_drops_topic_without_ai(), test_pool_roundtrip(), test_pool_rows_without_thumbs(), test_small_pool_skips_ai()

### Community 30 - "AI Video Clips & Encoding"
Cohesion: 0.27
Nodes (5): cover_crop(), local_clips(), motion_prompt(), veo_handoff(), video_encoder()

### Community 31 - "Motion Graphics Tests"
Cohesion: 0.20
Nodes (7): full_pictures(), sfx_events(), _board(), test_board_pictures_attached(), test_remotion_props_full(), test_sfx_full(), test_story_sound_wins_its_moment()

### Community 32 - "Remotion Render Prep"
Cohesion: 0.20
Nodes (5): invent_styles(), make_paper(), render_remotion(), short_skin(), test_make_paper()

### Community 33 - "Library Menu & Candidates"
Cohesion: 0.22
Nodes (7): library_menu(), reject_candidate(), save_candidate(), candidate_in(), test_candidate_names_unique_across_kinds(), test_reject_deletes(), test_save_candidate_unique_slug()

### Community 34 - "Director Picture Context"
Cohesion: 0.22
Nodes (5): catalog_text(), direct_scripts(), is_usable(), pictures_of(), usable()

### Community 35 - "Archive Photo Cleanup"
Cohesion: 0.25
Nodes (5): clean_photo(), is_stereo(), trim_borders(), border(), plain()

### Community 36 - "Edit Plan Writer"
Cohesion: 0.22
Nodes (5): cut_text(), edit_plan(), look_text(), picture_line(), test_edit_plan_picture_line()

### Community 37 - "Full-Scene Props"
Cohesion: 0.22
Nodes (6): full_props(), full_summary(), _jpg(), test_custom_cues_props_and_pictures(), test_full_props_figure(), test_full_summary()

### Community 38 - "YouTube Trend Research"
Cohesion: 0.29
Nodes (4): channel_url(), seed_ideas(), trend_research(), yt_list()

### Community 39 - "Callout Validation"
Cohesion: 0.33
Nodes (5): clean_graphic(), coords(), is_num(), number_figures(), test_clean_question_and_kinetic()

### Community 40 - "TypeScript Checks"
Cohesion: 0.29
Nodes (5): attempt(), lint_style_code(), tsc_check(), test_invention_lint_failure_uses_fallback(), test_placeholders_match_the_slots()

### Community 41 - "Repaint & Scene Swap"
Cohesion: 0.33
Nodes (4): paint_new(), use_picture_from(), test_new_picture_drops_mark(), test_paint_new_clears_full()

### Community 42 - "Invention Fallback Render"
Cohesion: 0.29
Nodes (4): run_remotion_with_fallback(), swap_inventions(), test_invention_runtime_failure_uses_fallback(), test_swap_inventions()

### Community 43 - "Automatic Review Fixes"
Cohesion: 0.33
Nodes (3): apply_review_fixes(), rewrite_paint_prompts(), test_auto_fix_graphic()

## Knowledge Gaps
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `write_scripts()` connect `Script Team (Write/Edit/Direct)` to `Director Picture Context`, `Shared Imports & Downloads`, `Run Menu & Channel Setup`, `Callout Validation`, `YouTube Trend Research`, `Full-Scene Validation`, `Usable Picture Catalog`, `Wikipedia & Wikimedia Research`, `Style Guardrails`, `Motion Graphic Limits`, `Look Scene Picking`, `Planning Test Fakes`, `Callout & Sound Validation`, `AI Planner Calls & Quota`, `Style Plan Validation`, `Pictures-First Pool`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Should `Full-Screen Motion Graphics` be split into smaller, more focused modules?**
  _Cohesion score 0.05853994490358127 - nodes in this community are weakly interconnected._
- **Why does `clean_full()` connect `Full-Scene Validation` to `Callout & Sound Validation`, `Script Team (Write/Edit/Direct)`, `Shared Imports & Downloads`, `Callout Validation`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **Should `Style Library Looks & Transitions` be split into smaller, more focused modules?**
  _Cohesion score 0.08691834942932397 - nodes in this community are weakly interconnected._
- **Why does `render()` connect `Quality Checks & Captions` to `Shared Imports & Downloads`, `Run Menu & Channel Setup`, `Python Frame Renderer`, `Image Choosing`, `State & Logbook Helpers`, `AI Painters (MOSS & Gemini)`, `Spoken-Word Cue Timing`, `Callout & Sound Validation`, `Voice Pipeline (VoiceStudio)`, `AI Planner Calls & Quota`, `SFX & Preview Sheets`, `AI Video Clips & Encoding`, `Motion Graphics Tests`, `Remotion Render Prep`, `Library Menu & Candidates`, `Archive Photo Cleanup`, `Edit Plan Writer`, `Full-Scene Props`, `Invention Fallback Render`, `Automatic Review Fixes`, `Figure Silhouettes`, `Music Loudness`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **Should `Remotion Cards & Captions` be split into smaller, more focused modules?**
  _Cohesion score 0.08764568764568764 - nodes in this community are weakly interconnected._
- **Should `Local GPU Workers` be split into smaller, more focused modules?**
  _Cohesion score 0.05928614640048397 - nodes in this community are weakly interconnected._