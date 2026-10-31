---
type: community
members: 8
---

# quality_check

**Members:** 8 nodes

## Members
- [[(min words, max words, min scenes, max scenes, seconds) for this batch's…]] - rationale - shortsmaker/writing.py
- [[Automatic checks on the finished Short, using ffmpeg's own detectors in one…]] - rationale - shortsmaker/review.py
- [[Past this, review.quality_check says the Short ran long (the planned seconds of…]] - rationale - shortsmaker/writing.py
- [[length_plan()]] - code - shortsmaker/writing.py
- [[max_seconds()]] - code - shortsmaker/writing.py
- [[quality_check()]] - code - shortsmaker/review.py
- [[test_quality_check_reads_ffmpeg_and_flags_reused_pictures()]] - code - tests/test_first_second.py
- [[where()]] - code - shortsmaker/review.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/quality_check
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_visual_review]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_edit_scripts]]
- 1 edge to [[_COMMUNITY_test_first_second.py]]

## Top bridge nodes
- [[quality_check()]] - degree 11, connects to 5 communities
- [[length_plan()]] - degree 5, connects to 3 communities
- [[max_seconds()]] - degree 3, connects to 1 community
- [[test_quality_check_reads_ffmpeg_and_flags_reused_pictures()]] - degree 2, connects to 1 community