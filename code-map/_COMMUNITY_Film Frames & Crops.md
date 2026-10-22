---
type: community
cohesion: 0.20
members: 10
---

# Film Frames & Crops

**Cohesion:** 0.20 - loosely connected
**Members:** 10 nodes

## Members
- [[CompletedProcess]] - code
- [[Download ~14s of film around the chosen moment (cropped with FILM_CROP to…]] - rationale - shortsmaker/footage.py
- [[Match FILM_CROP on downloaded thumbnail JPEGs (cut top 6%, bottom 20%, and 4%…]] - rationale - shortsmaker/footage.py
- [[Path_16]] - code
- [[crop_film_bytes()]] - code - shortsmaker/footage.py
- [[ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the…]] - rationale - shortsmaker/image_sources.py
- [[film_ffmpeg()]] - code - shortsmaker/image_sources.py
- [[film_frames()]] - code - shortsmaker/footage.py
- [[film_piece()]] - code - shortsmaker/footage.py
- [[n moments spread through a film, for the contact sheets (with FILM_CROP applied…]] - rationale - shortsmaker/footage.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Film_Frames__Crops
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_CLI & Pixabay Films]]
- 2 edges to [[_COMMUNITY_Audio Mix & Music Gain]]
- 1 edge to [[_COMMUNITY_Film Archive Sources]]
- 1 edge to [[_COMMUNITY_Picture Picker]]
- 1 edge to [[_COMMUNITY_Detail Marks & Storyboard]]

## Top bridge nodes
- [[film_piece()]] - degree 6, connects to 3 communities
- [[film_frames()]] - degree 5, connects to 2 communities
- [[crop_film_bytes()]] - degree 4, connects to 2 communities
- [[film_ffmpeg()]] - degree 5, connects to 1 community
- [[Path_16]] - degree 2, connects to 1 community