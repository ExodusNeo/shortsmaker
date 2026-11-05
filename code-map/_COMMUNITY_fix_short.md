---
type: community
members: 8
---

# fix_short

**Members:** 8 nodes

## Members
- [[fix.bat re-render a recent Short with one scene changed, keeping its pictures,…]] - rationale - shortsmaker/cli.py
- [[fix_short()]] - code - shortsmaker/cli.py
- [[load_channel()]] - code - shortsmaker/channel_profiles.py
- [[load_state()]] - code - shortsmaker/short_render.py
- [[prune_work()]] - code - shortsmaker/short_render.py
- [[test_fix_bat_explains_a_drawn_short()]] - code - tests/test_blender_run.py
- [[test_fix_checks_rules_before_asking_for_a_scene()]] - code - tests/test_rules.py
- [[test_state_roundtrip_full_pics()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/fix_short
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_main_1]]
- 5 edges to [[_COMMUNITY_pathlib]]
- 4 edges to [[_COMMUNITY_render]]
- 3 edges to [[_COMMUNITY_resume_runs]]
- 2 edges to [[_COMMUNITY_test_rules.py]]
- 2 edges to [[_COMMUNITY_pick_channel]]
- 2 edges to [[_COMMUNITY_apply_review_fixes]]
- 2 edges to [[_COMMUNITY_re]]
- 2 edges to [[_COMMUNITY_ffmpeg]]
- 2 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_gpu.py]]
- 1 edge to [[_COMMUNITY_fake_ai]]
- 1 edge to [[_COMMUNITY_choose_images]]

## Top bridge nodes
- [[fix_short()]] - degree 20, connects to 8 communities
- [[load_channel()]] - degree 7, connects to 6 communities
- [[load_state()]] - degree 7, connects to 4 communities
- [[prune_work()]] - degree 6, connects to 4 communities
- [[test_state_roundtrip_full_pics()]] - degree 3, connects to 2 communities