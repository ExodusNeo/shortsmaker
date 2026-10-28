---
type: community
members: 8
---

# unpack_clips

**Members:** 8 nodes

## Members
- [[Path_22]] - code
- [[Unpack sceneN.mp4.mov.webm from folderclips.zip (the Colab notebook's…]] - rationale - shortsmaker/gpu.py
- [[test_duplicate_clip_names_deduplicated()]] - code - tests/test_h3_handoff.py
- [[test_old_zip_does_not_overwrite_newer_clip()]] - code - tests/test_h3_handoff.py
- [[test_renamed_zip_is_picked_up()]] - code - tests/test_h3_handoff.py
- [[test_unpack_clips()]] - code - tests/test_h3_handoff.py
- [[unpack_clips()]] - code - shortsmaker/gpu.py
- [[zip_of()]] - code - tests/test_h3_handoff.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/unpack_clips
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_test_h3_handoff.py]]
- 2 edges to [[_COMMUNITY_local_clips]]
- 1 edge to [[_COMMUNITY_h3_run.py]]
- 1 edge to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_pathlib]]

## Top bridge nodes
- [[unpack_clips()]] - degree 10, connects to 4 communities
- [[zip_of()]] - degree 7, connects to 1 community
- [[test_duplicate_clip_names_deduplicated()]] - degree 3, connects to 1 community
- [[test_old_zip_does_not_overwrite_newer_clip()]] - degree 3, connects to 1 community
- [[test_renamed_zip_is_picked_up()]] - degree 3, connects to 1 community