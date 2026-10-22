---
type: community
members: 5
---

# film_frames

**Members:** 5 nodes

## Members
- [[CompletedProcess]] - code
- [[ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the…]] - rationale - shortsmaker/image_sources.py
- [[film_ffmpeg()]] - code - shortsmaker/image_sources.py
- [[film_frames()]] - code - shortsmaker/footage.py
- [[n moments spread through a film, for the contact sheets (with FILM_CROP applied…]] - rationale - shortsmaker/footage.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/film_frames
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_json]]
- 1 edge to [[_COMMUNITY_fetch]]
- 1 edge to [[_COMMUNITY_film_piece]]

## Top bridge nodes
- [[film_frames()]] - degree 5, connects to 2 communities
- [[film_ffmpeg()]] - degree 5, connects to 2 communities