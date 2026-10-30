---
type: community
members: 12
---

# edit_scripts

**Members:** 12 nodes

## Members
- [[(min words, max words, min scenes, max scenes, seconds) for this batch's…]] - rationale - shortsmaker/writing.py
- [[Automatic checks on the finished Short, using ffmpeg's own detectors in one…]] - rationale - shortsmaker/review.py
- [[Scene narrations from an AI reply a list of strings (or of {narration ...}).]] - rationale - shortsmaker/writing.py
- [[The script editor pass strongest hook, read-aloud fixes, cuts,…]] - rationale - shortsmaker/writing.py
- [[edit_scripts()]] - code - shortsmaker/writing.py
- [[fake()]] - code - tests/test_story.py
- [[length_plan()]] - code - shortsmaker/writing.py
- [[narration_lines()]] - code - shortsmaker/writing.py
- [[quality_check()]] - code - shortsmaker/review.py
- [[test_editor_gets_one_second_pass_for_broken_rules()]] - code - tests/test_story.py
- [[test_solo_edit_scripts_uses_same_ai()]] - code - tests/test_package.py
- [[where()]] - code - shortsmaker/review.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/edit_scripts
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_test_pictures_first.py]]
- 3 edges to [[_COMMUNITY_write_scripts]]
- 2 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_test_story.py]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_visual_review]]
- 1 edge to [[_COMMUNITY_gpu.py]]
- 1 edge to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_fix_short]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]

## Top bridge nodes
- [[quality_check()]] - degree 9, connects to 6 communities
- [[edit_scripts()]] - degree 13, connects to 5 communities
- [[length_plan()]] - degree 5, connects to 2 communities
- [[narration_lines()]] - degree 4, connects to 2 communities
- [[test_editor_gets_one_second_pass_for_broken_rules()]] - degree 3, connects to 1 community