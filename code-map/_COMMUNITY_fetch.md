---
type: community
members: 43
---

# fetch

**Members:** 43 nodes

## Members
- [[(ok, credit). Public domainCC0 need no credit; all other WikimediaWikipedia…]] - rationale - shortsmaker/image_sources.py
- [[CompletedProcess]] - code
- [[Download ~14s of film around the chosen moment (cropped with FILM_CROP to…]] - rationale - shortsmaker/footage.py
- [[Downloads the real photos the picker chose for evidence boards, custom scenes…]] - rationale - shortsmaker/picker.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Keep titles that share a meaningful word with the query (including 2-3 letter…]] - rationale - shortsmaker/image_sources.py
- [[Match FILM_CROP on downloaded thumbnail JPEGs (cut top 6%, bottom 20%, and 4%…]] - rationale - shortsmaker/footage.py
- [[NASA photos (public domain), when the story touches space, flight or science.]] - rationale - shortsmaker/image_sources.py
- [[NASA videos (public domain), as their mediumsmall MP4 renditions.]] - rationale - shortsmaker/footage.py
- [[Path_17]] - code
- [[Pixabay stock video free to use in videos, no credit needed (Pixabay Content…]] - rationale - shortsmaker/footage.py
- [[Rejected scenes (index - the review's complaint) that get a real picture from…]] - rationale - shortsmaker/review.py
- [[Start and end of the camera shot containing time `at` (newsreels cut to title…]] - rationale - shortsmaker/footage.py
- [[Videos across the entire Internet Archive (historical film, retro gaming,…]] - rationale - shortsmaker/footage.py
- [[Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable).]] - rationale - shortsmaker/footage.py
- [[What people actually type into YouTube search (free autocomplete endpoint, no…]] - rationale - shortsmaker/seo.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[archive_films()]] - code - shortsmaker/footage.py
- [[commons_films()]] - code - shortsmaker/footage.py
- [[crop_film_bytes()]] - code - shortsmaker/footage.py
- [[fetch()]] - code - shortsmaker/media_tools.py
- [[ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the…]] - rationale - shortsmaker/image_sources.py
- [[film_ffmpeg()]] - code - shortsmaker/image_sources.py
- [[film_frames()]] - code - shortsmaker/footage.py
- [[film_piece()]] - code - shortsmaker/footage.py
- [[full_pictures()]] - code - shortsmaker/picker.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[n moments spread through a film, for the contact sheets (with FILM_CROP applied…]] - rationale - shortsmaker/footage.py
- [[nasa_films()]] - code - shortsmaker/footage.py
- [[nasa_images()]] - code - shortsmaker/image_sources.py
- [[nasa_search()]] - code - shortsmaker/image_sources.py
- [[on_topic()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[pixabay_films()]] - code - shortsmaker/footage.py
- [[pool_pictures()]] - code - shortsmaker/review.py
- [[search_suggestions()]] - code - shortsmaker/seo.py
- [[shot_span()]] - code - shortsmaker/footage.py
- [[test_board_pictures_attached()]] - code - tests/test_full_scenes.py
- [[usable_license()]] - code - shortsmaker/image_sources.py
- [[wm_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/fetch
SORT file.name ASC
```

## Connections to other communities
- 24 edges to [[_COMMUNITY_test_full_scenes.py]]
- 9 edges to [[_COMMUNITY_json]]
- 5 edges to [[_COMMUNITY_test_pictures_first.py]]
- 4 edges to [[_COMMUNITY_clean_full]]
- 4 edges to [[_COMMUNITY_gather_pool]]
- 3 edges to [[_COMMUNITY_render]]
- 2 edges to [[_COMMUNITY_re]]
- 1 edge to [[_COMMUNITY_local_clips]]
- 1 edge to [[_COMMUNITY_pool_of]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_prepare_topic]]
- 1 edge to [[_COMMUNITY_rescue_graphics]]
- 1 edge to [[_COMMUNITY_ask_ai]]
- 1 edge to [[_COMMUNITY_test_blender_plan.py]]
- 1 edge to [[_COMMUNITY_channel_profiles.py]]
- 1 edge to [[_COMMUNITY_full_props]]

## Top bridge nodes
- [[pool_pictures()]] - degree 10, connects to 7 communities
- [[shot_span()]] - degree 7, connects to 5 communities
- [[archive_films()]] - degree 7, connects to 4 communities
- [[on_topic()]] - degree 10, connects to 3 communities
- [[get_image()]] - degree 9, connects to 3 communities