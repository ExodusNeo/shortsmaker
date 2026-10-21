---
type: community
cohesion: 0.67
members: 3
---

# LTX Crash Retry Test

**Cohesion:** 0.67 - moderately connected
**Members:** 3 nodes

## Members
- [[Mike the Headless Chicken, fix round 3 the LTX worker died without writing…]] - rationale - tests/test_full_scenes.py
- [[fake_run()]] - code - tests/test_full_scenes.py
- [[test_local_job_retries_a_hard_crash()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LTX_Crash_Retry_Test
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Local AI Jobs & Clips]]
- 1 edge to [[_COMMUNITY_Full-Scene Limits & Director Tests]]

## Top bridge nodes
- [[test_local_job_retries_a_hard_crash()]] - degree 4, connects to 2 communities