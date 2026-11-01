---
type: community
members: 10
---

# film_piece

**Members:** 10 nodes

## Members
- [[Camera-shot samples for short adslocal videos; otherwise spread samples or…]] - rationale - shortsmaker/footage.py
- [[CompletedProcess]] - code
- [[Download ~14s around the chosen moment with original framing and muted source…]] - rationale - shortsmaker/footage.py
- [[Match FILM_CROP on downloaded thumbnail JPEGs (cut top 6%, bottom 20%, and 4%…]] - rationale - shortsmaker/footage.py
- [[crop_film_bytes()]] - code - shortsmaker/footage.py
- [[crop_filter()]] - code - shortsmaker/footage.py
- [[ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the…]] - rationale - shortsmaker/image_sources.py
- [[film_ffmpeg()]] - code - shortsmaker/image_sources.py
- [[film_frames()]] - code - shortsmaker/footage.py
- [[film_piece()]] - code - shortsmaker/footage.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/film_piece
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_pathlib]]
- 2 edges to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_fetch]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_render]]

## Top bridge nodes
- [[film_piece()]] - degree 8, connects to 4 communities
- [[film_frames()]] - degree 7, connects to 3 communities
- [[film_ffmpeg()]] - degree 6, connects to 2 communities
- [[crop_film_bytes()]] - degree 4, connects to 1 community
- [[crop_filter()]] - degree 3, connects to 1 community