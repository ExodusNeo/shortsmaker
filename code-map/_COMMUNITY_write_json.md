---
type: community
members: 15
---

# write_json

**Members:** 15 nodes

## Members
- [[Camera-shot samples for short adslocal videos; otherwise spread samples or…]] - rationale - shortsmaker/footage.py
- [[CompletedProcess]] - code
- [[Detect cuts in short adslocal files; bounded work and cached results for…]] - rationale - shortsmaker/footage.py
- [[Download ~14s around the chosen moment with original framing and muted source…]] - rationale - shortsmaker/footage.py
- [[Match FILM_CROP on downloaded thumbnail JPEGs (cut top 6%, bottom 20%, and 4%…]] - rationale - shortsmaker/footage.py
- [[Path_21]] - code
- [[Write via a temp file, so an interrupted run never leaves a half-written file…]] - rationale - shortsmaker/media_tools.py
- [[crop_film_bytes()]] - code - shortsmaker/footage.py
- [[crop_filter()]] - code - shortsmaker/footage.py
- [[ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the…]] - rationale - shortsmaker/image_sources.py
- [[film_ffmpeg()]] - code - shortsmaker/image_sources.py
- [[film_frames()]] - code - shortsmaker/footage.py
- [[film_piece()]] - code - shortsmaker/footage.py
- [[shot_moments()]] - code - shortsmaker/footage.py
- [[write_json()]] - code - shortsmaker/media_tools.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/write_json
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_re]]
- 4 edges to [[_COMMUNITY_json]]
- 3 edges to [[_COMMUNITY_main_1]]
- 3 edges to [[_COMMUNITY_audio_library.py]]
- 2 edges to [[_COMMUNITY_duration]]
- 2 edges to [[_COMMUNITY_test_pictures_first.py]]
- 2 edges to [[_COMMUNITY_source_json]]
- 2 edges to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_fetch]]
- 1 edge to [[_COMMUNITY_test_full_scenes.py]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_logbook.py]]
- 1 edge to [[_COMMUNITY_preview]]

## Top bridge nodes
- [[write_json()]] - degree 21, connects to 10 communities
- [[film_piece()]] - degree 8, connects to 4 communities
- [[shot_moments()]] - degree 8, connects to 2 communities
- [[film_frames()]] - degree 7, connects to 2 communities
- [[crop_film_bytes()]] - degree 4, connects to 2 communities