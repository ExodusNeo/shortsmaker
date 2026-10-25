---
type: community
cohesion: 0.09
members: 27
---

# Stock Video Sources

**Cohesion:** 0.09 - loosely connected
**Members:** 27 nodes

## Members
- [[(ok, credit). Public domainCC0 need no credit; all other WikimediaWikipedia…]] - rationale - shortsmaker/image_sources.py
- [[Check every line against the story's Wikipedia articles and rewrite what they…]] - rationale - shortsmaker/writing.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Keep titles that share a meaningful word with the query (including 2-3 letter…]] - rationale - shortsmaker/image_sources.py
- [[NASA photos (public domain), when the story touches space, flight or science.]] - rationale - shortsmaker/image_sources.py
- [[NASA videos (public domain), as their mediumsmall MP4 renditions.]] - rationale - shortsmaker/footage.py
- [[Pixabay stock video free to use in videos, no credit needed (Pixabay Content…]] - rationale - shortsmaker/footage.py
- [[Plain text of an English Wikipedia article ('' when missing or unreachable).]] - rationale - shortsmaker/writing.py
- [[Still images, magazinemanual scans, art and archival photos from the Internet…]] - rationale - shortsmaker/image_sources.py
- [[Videos across the entire Internet Archive (historical film, retro gaming,…]] - rationale - shortsmaker/footage.py
- [[Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable).]] - rationale - shortsmaker/footage.py
- [[What people actually type into YouTube search (free autocomplete endpoint, no…]] - rationale - shortsmaker/seo.py
- [[archive_films()]] - code - shortsmaker/footage.py
- [[archive_images()]] - code - shortsmaker/image_sources.py
- [[article_text()]] - code - shortsmaker/writing.py
- [[commons_films()]] - code - shortsmaker/footage.py
- [[fact_check()]] - code - shortsmaker/writing.py
- [[fetch()]] - code - shortsmaker/media_tools.py
- [[nasa_films()]] - code - shortsmaker/footage.py
- [[nasa_images()]] - code - shortsmaker/image_sources.py
- [[nasa_search()]] - code - shortsmaker/image_sources.py
- [[on_topic()]] - code - shortsmaker/image_sources.py
- [[pixabay_films()]] - code - shortsmaker/footage.py
- [[search_suggestions()]] - code - shortsmaker/seo.py
- [[test_fact_check_drops_full()]] - code - tests/test_full_scenes.py
- [[usable_license()]] - code - shortsmaker/image_sources.py
- [[wm_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Stock_Video_Sources
SORT file.name ASC
```

## Connections to other communities
- 15 edges to [[_COMMUNITY_CLI, Config and Footage]]
- 8 edges to [[_COMMUNITY_Local Voice and Freesound]]
- 4 edges to [[_COMMUNITY_Script Sounds and Graphics]]
- 4 edges to [[_COMMUNITY_Wikimedia Image Search]]
- 3 edges to [[_COMMUNITY_Openverse and Museum Images]]
- 2 edges to [[_COMMUNITY_Audio Mix and Shotcut Export]]
- 2 edges to [[_COMMUNITY_Pictures-First Pool Tests]]
- 2 edges to [[_COMMUNITY_Main Entry and Channel Profiles]]
- 1 edge to [[_COMMUNITY_Headless AI Planner Calls]]
- 1 edge to [[_COMMUNITY_Picture Pool Storage]]
- 1 edge to [[_COMMUNITY_Motion Scenes and Style Library]]
- 1 edge to [[_COMMUNITY_Obsidian Vault Logbook]]
- 1 edge to [[_COMMUNITY_Graphics Rescue Caps]]

## Top bridge nodes
- [[fact_check()]] - degree 8, connects to 5 communities
- [[pixabay_films()]] - degree 8, connects to 4 communities
- [[archive_films()]] - degree 7, connects to 4 communities
- [[article_text()]] - degree 7, connects to 4 communities
- [[fetch()]] - degree 11, connects to 3 communities