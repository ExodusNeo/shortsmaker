---
type: community
members: 12
---

# film_piece

**Members:** 12 nodes

## Members
- [[CompletedProcess]] - code
- [[Download ~14s of film around the chosen moment (cropped with FILM_CROP to…]] - rationale - shortsmaker/footage.py
- [[Match FILM_CROP on downloaded thumbnail JPEGs (cut top 6%, bottom 20%, and 4%…]] - rationale - shortsmaker/footage.py
- [[Path_12]] - code
- [[Start and end of the camera shot containing time `at` (newsreels cut to title…]] - rationale - shortsmaker/footage.py
- [[crop_film_bytes()]] - code - shortsmaker/footage.py
- [[ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the…]] - rationale - shortsmaker/image_sources.py
- [[film_ffmpeg()]] - code - shortsmaker/image_sources.py
- [[film_frames()]] - code - shortsmaker/footage.py
- [[film_piece()]] - code - shortsmaker/footage.py
- [[n moments spread through a film, for the contact sheets (with FILM_CROP applied…]] - rationale - shortsmaker/footage.py
- [[shot_span()]] - code - shortsmaker/footage.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/film_piece
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_pathlib]]
- 2 edges to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_local_clips]]
- 1 edge to [[_COMMUNITY_ffmpeg]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_fetch]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_re]]

## Top bridge nodes
- [[shot_span()]] - degree 7, connects to 5 communities
- [[film_piece()]] - degree 7, connects to 4 communities
- [[film_frames()]] - degree 5, connects to 2 communities
- [[film_ffmpeg()]] - degree 5, connects to 1 community
- [[crop_film_bytes()]] - degree 4, connects to 1 community