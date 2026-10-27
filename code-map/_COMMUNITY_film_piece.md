---
type: community
members: 6
---

# film_piece

**Members:** 6 nodes

## Members
- [[CompletedProcess]] - code
- [[Download ~14s of film around the chosen moment (cropped with FILM_CROP to…]] - rationale - shortsmaker/footage.py
- [[Path_31]] - code
- [[ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the…]] - rationale - shortsmaker/image_sources.py
- [[film_ffmpeg()]] - code - shortsmaker/image_sources.py
- [[film_piece()]] - code - shortsmaker/footage.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/film_piece
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_gpu.py]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_ffmpeg]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_shutil]]
- 1 edge to [[_COMMUNITY_image_sources.py]]

## Top bridge nodes
- [[film_piece()]] - degree 7, connects to 4 communities
- [[film_ffmpeg()]] - degree 5, connects to 2 communities
- [[Path_31]] - degree 2, connects to 1 community