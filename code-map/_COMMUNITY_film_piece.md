---
type: community
members: 11
---

# film_piece

**Members:** 11 nodes

## Members
- [[Camera-shot samples for short adslocal videos; otherwise spread samples or…]] - rationale - shortsmaker/footage.py
- [[CompletedProcess]] - code
- [[Detect cuts in short adslocal files; bounded work and cached results for…]] - rationale - shortsmaker/footage.py
- [[Download ~14s around the chosen moment with original framing and muted source…]] - rationale - shortsmaker/footage.py
- [[Path_8]] - code
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
- 6 edges to [[_COMMUNITY_test_full_scenes.py]]
- 3 edges to [[_COMMUNITY_render]]
- 2 edges to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_extra_sources.py]]
- 1 edge to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_shutil]]

## Top bridge nodes
- [[film_piece()]] - degree 8, connects to 4 communities
- [[shot_moments()]] - degree 8, connects to 4 communities
- [[film_frames()]] - degree 7, connects to 2 communities
- [[film_ffmpeg()]] - degree 6, connects to 1 community
- [[crop_filter()]] - degree 3, connects to 1 community