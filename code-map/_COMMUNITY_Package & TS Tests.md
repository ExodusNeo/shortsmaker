---
type: community
cohesion: 0.13
members: 15
---

# Package & TS Tests

**Cohesion:** 0.13 - loosely connected
**Members:** 15 nodes

## Members
- [[Runs the TypeScript tests (tests.test.ts) bundles each with Remotion's own…]] - rationale - tests/run_ts_tests.py
- [[Tests for the shortsmaker package wiring (one owner per setting, fakes reach…]] - rationale - tests/test_package.py
- [[fake_run()]] - code - tests/test_package.py
- [[run_ts_tests.py]] - code - tests/run_ts_tests.py
- [[tempfile]] - concept
- [[test_argon_out_of_quota_switches_to_flash()]] - code - tests/test_package.py
- [[test_claude_pinned_to_opus_high()]] - code - tests/test_package.py
- [[test_encoder_cache_lives_with_video_encoder()]] - code - tests/test_package.py
- [[test_entry_point()]] - code - tests/test_package.py
- [[test_fake_reaches_callers()]] - code - tests/test_package.py
- [[test_ffmpeg_on_path()]] - code - tests/test_package.py
- [[test_gemini_reviews_get_the_main_model_bulk_pictures_flash()]] - code - tests/test_package.py
- [[test_package.py]] - code - tests/test_package.py
- [[test_root()]] - code - tests/test_package.py
- [[test_session_shared()]] - code - tests/test_package.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Package__TS_Tests
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_CLI & Pixabay Films]]
- 3 edges to [[_COMMUNITY_Audio Mix & Music Gain]]
- 3 edges to [[_COMMUNITY_Config & Palettes]]
- 3 edges to [[_COMMUNITY_Freesound & Picture Swaps]]
- 2 edges to [[_COMMUNITY_Sentence Voice Takes]]
- 1 edge to [[_COMMUNITY_AI-Coded Motion Scenes]]
- 1 edge to [[_COMMUNITY_Shotcut Timeline]]
- 1 edge to [[_COMMUNITY_Pictures-First Tests]]
- 1 edge to [[_COMMUNITY_First-Second Check Tests]]
- 1 edge to [[_COMMUNITY_Full Scene Tests]]

## Top bridge nodes
- [[test_package.py]] - degree 24, connects to 6 communities
- [[tempfile]] - degree 7, connects to 5 communities
- [[run_ts_tests.py]] - degree 6, connects to 4 communities