---
type: community
members: 10
---

# film_piece

**Members:** 10 nodes

## Members
- [[CompletedProcess]] - code
- [[Download ~14s of film around the chosen moment (cropped with FILM_CROP to…]] - rationale - shortsmaker/footage.py
- [[Match FILM_CROP on downloaded thumbnail JPEGs (cut top 6%, bottom 20%, and 4%…]] - rationale - shortsmaker/footage.py
- [[Path_17]] - code
- [[crop_film_bytes()]] - code - shortsmaker/footage.py
- [[ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the…]] - rationale - shortsmaker/image_sources.py
- [[film_ffmpeg()]] - code - shortsmaker/image_sources.py
- [[film_frames()]] - code - shortsmaker/footage.py
- [[film_piece()]] - code - shortsmaker/footage.py
- [[n moments spread through a film, for the contact sheets (with FILM_CROP applied…]] - rationale - shortsmaker/footage.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/film_piece
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_ffmpeg]]
- 1 edge to [[_COMMUNITY_audio_mix.py]]

## Top bridge nodes
- [[film_piece()]] - degree 7, connects to 4 communities
- [[film_frames()]] - degree 5, connects to 1 community
- [[film_ffmpeg()]] - degree 5, connects to 1 community
- [[crop_film_bytes()]] - degree 4, connects to 1 community
- [[Path_17]] - degree 2, connects to 1 community