---
type: community
cohesion: 0.10
members: 26
---

# Film Archive Sources

**Cohesion:** 0.10 - loosely connected
**Members:** 26 nodes

## Members
- [[(ok, credit). Public domainCC0 need no credit; all other WikimediaWikipedia…]] - rationale - shortsmaker/image_sources.py
- [[Downloads the real photos the picker chose for evidence boards, custom scenes…]] - rationale - shortsmaker/picker.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Keep titles that share at least one meaningful word (including 2-3 letter terms…]] - rationale - shortsmaker/image_sources.py
- [[NASA photos (public domain), when the story touches space, flight or science.]] - rationale - shortsmaker/image_sources.py
- [[NASA videos (public domain), as their mediumsmall MP4 renditions.]] - rationale - shortsmaker/footage.py
- [[Still images, magazinemanual scans, art and archival photos from the Internet…]] - rationale - shortsmaker/image_sources.py
- [[Videos across the entire Internet Archive (historical film, retro gaming,…]] - rationale - shortsmaker/footage.py
- [[Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable).]] - rationale - shortsmaker/footage.py
- [[What people actually type into YouTube search (free autocomplete endpoint, no…]] - rationale - shortsmaker/seo.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[archive_films()]] - code - shortsmaker/footage.py
- [[archive_images()]] - code - shortsmaker/image_sources.py
- [[commons_films()]] - code - shortsmaker/footage.py
- [[fetch()]] - code - shortsmaker/media_tools.py
- [[full_pictures()]] - code - shortsmaker/picker.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[nasa_films()]] - code - shortsmaker/footage.py
- [[nasa_images()]] - code - shortsmaker/image_sources.py
- [[nasa_search()]] - code - shortsmaker/image_sources.py
- [[on_topic()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[search_suggestions()]] - code - shortsmaker/seo.py
- [[usable_license()]] - code - shortsmaker/image_sources.py
- [[wm_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Film_Archive_Sources
SORT file.name ASC
```

## Connections to other communities
- 14 edges to [[_COMMUNITY_CLI & Pixabay Films]]
- 8 edges to [[_COMMUNITY_Scene Cues & Image Search]]
- 4 edges to [[_COMMUNITY_Freesound & Picture Swaps]]
- 2 edges to [[_COMMUNITY_Audio Mix & Music Gain]]
- 2 edges to [[_COMMUNITY_Entry Point & Channel Menus]]
- 2 edges to [[_COMMUNITY_Picture Picker]]
- 1 edge to [[_COMMUNITY_Film Frames & Crops]]

## Top bridge nodes
- [[archive_films()]] - degree 7, connects to 4 communities
- [[fetch()]] - degree 11, connects to 3 communities
- [[nasa_films()]] - degree 7, connects to 3 communities
- [[search_suggestions()]] - degree 5, connects to 3 communities
- [[on_topic()]] - degree 8, connects to 2 communities