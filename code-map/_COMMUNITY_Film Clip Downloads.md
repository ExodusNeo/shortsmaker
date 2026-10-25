---
type: community
cohesion: 0.33
members: 6
---

# Film Clip Downloads

**Cohesion:** 0.33 - loosely connected
**Members:** 6 nodes

## Members
- [[CompletedProcess]] - code
- [[Download ~14s of film around the chosen moment (cropped with FILM_CROP to…]] - rationale - shortsmaker/footage.py
- [[Path_19]] - code
- [[ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the…]] - rationale - shortsmaker/image_sources.py
- [[film_ffmpeg()]] - code - shortsmaker/image_sources.py
- [[film_piece()]] - code - shortsmaker/footage.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Film_Clip_Downloads
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_CLI, Config and Footage]]
- 2 edges to [[_COMMUNITY_Audio Mix and Shotcut Export]]
- 1 edge to [[_COMMUNITY_Pictures-First Pool Tests]]
- 1 edge to [[_COMMUNITY_Review Auto-Fixes]]

## Top bridge nodes
- [[film_piece()]] - degree 7, connects to 4 communities
- [[film_ffmpeg()]] - degree 5, connects to 1 community
- [[Path_19]] - degree 2, connects to 1 community