---
type: community
cohesion: 0.07
members: 45
---

# Film Footage Sources

**Cohesion:** 0.07 - loosely connected
**Members:** 45 nodes

## Members
- [[(ok, credit). Public domainCC0 need no credit; all other WikimediaWikipedia…]] - rationale - shortsmaker/image_sources.py
- [[Candidate pictures (with preview `thumb` bytes) and sampled real-film frames…]] - rationale - shortsmaker/picture_pool.py
- [[CompletedProcess]] - code
- [[Download ~14s of film around the chosen moment (cropped with FILM_CROP to…]] - rationale - shortsmaker/footage.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Images used in an English Wikipedia article chosen by editors, so almost…]] - rationale - shortsmaker/image_sources.py
- [[Keep titles that share at least one meaningful word (including 2-3 letter terms…]] - rationale - shortsmaker/image_sources.py
- [[NASA photos (public domain), when the story touches space, flight or science.]] - rationale - shortsmaker/image_sources.py
- [[NASA videos (public domain), as their mediumsmall MP4 renditions.]] - rationale - shortsmaker/footage.py
- [[Path_7]] - code
- [[Pictures from Wikimedia Commons, Openverse, NASA and the Internet Archive, with…]] - rationale - shortsmaker/image_sources.py
- [[Still images, magazinemanual scans, art and archival photos from the Internet…]] - rationale - shortsmaker/image_sources.py
- [[The on-screen credit tag kind, a short name and the licence (Photo E. Mariz…]] - rationale - shortsmaker/image_sources.py
- [[URL of a standard-size Wikimedia thumbnail the largest allowed step that fits…]] - rationale - shortsmaker/image_sources.py
- [[Usable images from a WikimediaWikipedia API query photos, screenshots,…]] - rationale - shortsmaker/image_sources.py
- [[Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable).]] - rationale - shortsmaker/footage.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[add()]] - code - shortsmaker/picture_pool.py
- [[archive_images()]] - code - shortsmaker/image_sources.py
- [[article_images()]] - code - shortsmaker/image_sources.py
- [[commons_films()]] - code - shortsmaker/footage.py
- [[commons_search()]] - code - shortsmaker/image_sources.py
- [[fetch()]] - code - shortsmaker/media_tools.py
- [[ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the…]] - rationale - shortsmaker/image_sources.py
- [[film_ffmpeg()]] - code - shortsmaker/image_sources.py
- [[film_piece()]] - code - shortsmaker/footage.py
- [[gather_pool()]] - code - shortsmaker/picture_pool.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[image_sources.py]] - code - shortsmaker/image_sources.py
- [[load_thumb()]] - code - shortsmaker/picture_pool.py
- [[nasa_films()]] - code - shortsmaker/footage.py
- [[nasa_images()]] - code - shortsmaker/image_sources.py
- [[nasa_search()]] - code - shortsmaker/image_sources.py
- [[on_topic()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[short_credit()]] - code - shortsmaker/image_sources.py
- [[threading]] - concept
- [[thumb_url()]] - code - shortsmaker/image_sources.py
- [[urllib_error]] - concept
- [[usable_license()]] - code - shortsmaker/image_sources.py
- [[wm_files()]] - code - shortsmaker/image_sources.py
- [[wm_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Film_Footage_Sources
SORT file.name ASC
```

## Connections to other communities
- 19 edges to [[_COMMUNITY_Archive Film & Downloads]]
- 7 edges to [[_COMMUNITY_Channel Profiles & Menus]]
- 6 edges to [[_COMMUNITY_Graphics Rescue & Validation]]
- 6 edges to [[_COMMUNITY_Media Tools & Shot Spans]]
- 3 edges to [[_COMMUNITY_Picture Picker]]
- 2 edges to [[_COMMUNITY_Picture Pool Prep]]
- 2 edges to [[_COMMUNITY_Test Patching Helpers]]
- 1 edge to [[_COMMUNITY_Quality & Visual Review]]
- 1 edge to [[_COMMUNITY_Sound Cue Sheet]]
- 1 edge to [[_COMMUNITY_Python Frame Renderer]]
- 1 edge to [[_COMMUNITY_Picture Catalog]]
- 1 edge to [[_COMMUNITY_Sound Effects & Story Sounds]]
- 1 edge to [[_COMMUNITY_Full Scene Tests]]

## Top bridge nodes
- [[image_sources.py]] - degree 38, connects to 8 communities
- [[gather_pool()]] - degree 17, connects to 6 communities
- [[film_piece()]] - degree 6, connects to 3 communities
- [[fetch()]] - degree 11, connects to 2 communities
- [[on_topic()]] - degree 8, connects to 2 communities