---
type: community
members: 9
---

# words_of

**Members:** 9 nodes

## Members
- [[Keep titles that share at least one meaningful word (including 2-3 letter terms…]] - rationale - shortsmaker/image_sources.py
- [[Lowercase, accent-free word tokens, for matching names against spoken words.]] - rationale - shortsmaker/plan_rules.py
- [[Still images, magazinemanual scans, art and archival photos from the Internet…]] - rationale - shortsmaker/image_sources.py
- [[Videos across the entire Internet Archive (historical film, retro gaming,…]] - rationale - shortsmaker/footage.py
- [[archive_films()]] - code - shortsmaker/footage.py
- [[archive_images()]] - code - shortsmaker/image_sources.py
- [[on_topic()]] - code - shortsmaker/image_sources.py
- [[test_clean_full_keeps_board_pic()]] - code - tests/test_pictures_first.py
- [[words_of()]] - code - shortsmaker/plan_rules.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/words_of
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_clean_full]]
- 4 edges to [[_COMMUNITY_json]]
- 3 edges to [[_COMMUNITY_fetch]]
- 3 edges to [[_COMMUNITY_gather_pool]]
- 2 edges to [[_COMMUNITY_audio_mix.py]]
- 2 edges to [[_COMMUNITY_wm_files]]
- 2 edges to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_write_scripts]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_full_cues]]
- 1 edge to [[_COMMUNITY_qwen_voice.py]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_test_pictures_first.py]]

## Top bridge nodes
- [[words_of()]] - degree 18, connects to 10 communities
- [[on_topic()]] - degree 8, connects to 4 communities
- [[archive_films()]] - degree 7, connects to 3 communities
- [[archive_images()]] - degree 6, connects to 3 communities
- [[test_clean_full_keeps_board_pic()]] - degree 3, connects to 2 communities