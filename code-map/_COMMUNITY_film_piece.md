---
type: community
members: 12
---

# film_piece

**Members:** 12 nodes

## Members
- [[Camera-shot samples for short adslocal videos; otherwise spread samples or…]] - rationale - shortsmaker/footage.py
- [[CompletedProcess]] - code
- [[Detect cuts in short adslocal files; bounded work and cached results for…]] - rationale - shortsmaker/footage.py
- [[Download ~14s around the chosen moment with original framing and muted source…]] - rationale - shortsmaker/footage.py
- [[Match FILM_CROP on downloaded thumbnail JPEGs (cut top 6%, bottom 20%, and 4%…]] - rationale - shortsmaker/footage.py
- [[crop_film_bytes()]] - code - shortsmaker/footage.py
- [[crop_filter()]] - code - shortsmaker/footage.py
- [[ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the…]] - rationale - shortsmaker/image_sources.py
- [[film_ffmpeg()]] - code - shortsmaker/image_sources.py
- [[film_frames()]] - code - shortsmaker/footage.py
- [[film_piece()]] - code - shortsmaker/footage.py
- [[shot_moments()]] - code - shortsmaker/footage.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/film_piece
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_write_json]]
- 2 edges to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_extra_sources.py]]
- 1 edge to [[_COMMUNITY_test_pictures_first.py]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_subprocess]]
- 1 edge to [[_COMMUNITY_re]]

## Top bridge nodes
- [[film_piece()]] - degree 8, connects to 5 communities
- [[shot_moments()]] - degree 8, connects to 4 communities
- [[film_frames()]] - degree 7, connects to 2 communities
- [[film_ffmpeg()]] - degree 6, connects to 1 community
- [[crop_film_bytes()]] - degree 4, connects to 1 community