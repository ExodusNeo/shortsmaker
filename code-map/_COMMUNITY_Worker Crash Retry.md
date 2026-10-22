---
type: community
cohesion: 0.67
members: 3
---

# Worker Crash Retry

**Cohesion:** 0.67 - moderately connected
**Members:** 3 nodes

## Members
- [[Mike the Headless Chicken, fix round 3 the LTX worker died without writing…]] - rationale - tests/test_full_scenes.py
- [[fake_run()_1]] - code - tests/test_full_scenes.py
- [[test_local_job_retries_a_hard_crash()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Worker_Crash_Retry
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Full Scene Tests]]

## Top bridge nodes
- [[test_local_job_retries_a_hard_crash()]] - degree 3, connects to 1 community