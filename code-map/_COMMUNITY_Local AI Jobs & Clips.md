---
type: community
members: 58
---

# Local AI Jobs & Clips

**Members:** 58 nodes

## Members
- [[(ok, credit). Public domainCC0 need no credit; all other WikimediaWikipedia…]] - rationale - shortsmaker/image_sources.py
- [[At most MAX_STORY_SOUNDS story sounds per Short (the first ones), so each one…]] - rationale - shortsmaker/audio_mix.py
- [[Candidate pictures (with preview `thumb` bytes) and sampled real-film frames…]] - rationale - shortsmaker/picture_pool.py
- [[CompletedProcess]] - code
- [[Downloads the real photos the picker chose for evidence boards, custom scenes…]] - rationale - shortsmaker/picker.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Image]] - code
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Images used in an English Wikipedia article chosen by editors, so almost…]] - rationale - shortsmaker/image_sources.py
- [[Keep titles that share at least one meaningful word (including 2-3 letter terms…]] - rationale - shortsmaker/image_sources.py
- [[Lowercase, accent-free word tokens, for matching names against spoken words.]] - rationale - shortsmaker/plan_rules.py
- [[Match FILM_CROP on downloaded thumbnail JPEGs (cut top 6%, bottom 20%, and 4%…]] - rationale - shortsmaker/footage.py
- [[NASA photos (public domain), when the story touches space, flight or science.]] - rationale - shortsmaker/image_sources.py
- [[NASA videos (public domain), as their mediumsmall MP4 renditions.]] - rationale - shortsmaker/footage.py
- [[Pictures from Wikimedia Commons, Openverse, NASA and the Internet Archive, with…]] - rationale - shortsmaker/image_sources.py
- [[Small credit label (bottom-left, CREDIT_Y) while credited material (YouTube…]] - rationale - shortsmaker/image_sources.py
- [[Still images, magazinemanual scans, art and archival photos from the Internet…]] - rationale - shortsmaker/image_sources.py
- [[The on-screen credit tag kind, a short name and the licence (Photo E. Mariz…]] - rationale - shortsmaker/image_sources.py
- [[URL of a standard-size Wikimedia thumbnail the largest allowed step that fits…]] - rationale - shortsmaker/image_sources.py
- [[Usable images from a WikimediaWikipedia API query photos, screenshots,…]] - rationale - shortsmaker/image_sources.py
- [[Videos across the entire Internet Archive (historical film, retro gaming,…]] - rationale - shortsmaker/footage.py
- [[Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable).]] - rationale - shortsmaker/footage.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[add()]] - code - shortsmaker/picture_pool.py
- [[archive_films()]] - code - shortsmaker/footage.py
- [[archive_images()]] - code - shortsmaker/image_sources.py
- [[article_images()]] - code - shortsmaker/image_sources.py
- [[commons_films()]] - code - shortsmaker/footage.py
- [[commons_search()]] - code - shortsmaker/image_sources.py
- [[credit_tag_image()]] - code - shortsmaker/image_sources.py
- [[crop_film_bytes()]] - code - shortsmaker/footage.py
- [[fetch()_1]] - code - shortsmaker/media_tools.py
- [[ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the…]] - rationale - shortsmaker/image_sources.py
- [[film_ffmpeg()]] - code - shortsmaker/image_sources.py
- [[film_frames()]] - code - shortsmaker/footage.py
- [[full_pictures()]] - code - shortsmaker/picker.py
- [[gather_pool()]] - code - shortsmaker/picture_pool.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[image_sources.py]] - code - shortsmaker/image_sources.py
- [[limit_sounds()]] - code - shortsmaker/audio_mix.py
- [[load_thumb()]] - code - shortsmaker/picture_pool.py
- [[n moments spread through a film, for the contact sheets (with FILM_CROP applied…]] - rationale - shortsmaker/footage.py
- [[nasa_films()]] - code - shortsmaker/footage.py
- [[nasa_images()]] - code - shortsmaker/image_sources.py
- [[nasa_search()]] - code - shortsmaker/image_sources.py
- [[on_topic()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[short_credit()]] - code - shortsmaker/image_sources.py
- [[test_clean_sound()]] - code - tests/test_full_scenes.py
- [[threading]] - concept
- [[thumb_url()]] - code - shortsmaker/image_sources.py
- [[urllib_error]] - concept
- [[usable_license()]] - code - shortsmaker/image_sources.py
- [[wm_files()]] - code - shortsmaker/image_sources.py
- [[wm_get()]] - code - shortsmaker/image_sources.py
- [[words_of()]] - code - shortsmaker/plan_rules.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Local_AI_Jobs__Clips
SORT file.name ASC
```

## Connections to other communities
- 26 edges to [[_COMMUNITY_Channel Profiles & CLI]]
- 5 edges to [[_COMMUNITY_Full-Scene Rescue & Plan Cleaning]]
- 4 edges to [[_COMMUNITY_Invention Slots]]
- 3 edges to [[_COMMUNITY_AI Calls & Quota Fallback (4)]]
- 3 edges to [[_COMMUNITY_Footage Downloads & Crops (2)]]
- 3 edges to [[_COMMUNITY_Footage Downloads & Crops (2) (3)]]
- 3 edges to [[_COMMUNITY_Picture List Catalog (3)]]
- 2 edges to [[_COMMUNITY_AI Calls & Quota Fallback]]
- 2 edges to [[_COMMUNITY_Story Sounds & Credits (2)]]
- 2 edges to [[_COMMUNITY_Picture List Catalog]]
- 2 edges to [[_COMMUNITY_Python Frame Renderer]]
- 2 edges to [[_COMMUNITY_Footage Downloads & Crops (2) (2)]]
- 2 edges to [[_COMMUNITY_Footage Downloads & Crops]]
- 2 edges to [[_COMMUNITY_Pool Gathering]]
- 1 edge to [[_COMMUNITY_Entry Point, Logbook & Sounds]]
- 1 edge to [[_COMMUNITY_Scene Cues & Word Timing]]
- 1 edge to [[_COMMUNITY_Voice Worker (qwen_voice)]]
- 1 edge to [[_COMMUNITY_Picture List Catalog (2)]]

## Top bridge nodes
- [[image_sources.py]] - degree 38, connects to 8 communities
- [[words_of()]] - degree 18, connects to 6 communities
- [[gather_pool()]] - degree 17, connects to 6 communities
- [[fetch()_1]] - degree 11, connects to 3 communities
- [[nasa_films()]] - degree 7, connects to 3 communities