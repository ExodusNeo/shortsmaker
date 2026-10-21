---
type: community
cohesion: 0.09
members: 24
---

# Commons & Archive Sources

**Cohesion:** 0.09 - loosely connected
**Members:** 24 nodes

## Members
- [[(ok, credit). Public domainCC0 need no credit; all other WikimediaWikipedia…]] - rationale - shortsmaker/image_sources.py
- [[Check every line against the story's Wikipedia articles and rewrite what they…]] - rationale - shortsmaker/writing.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Images used in an English Wikipedia article chosen by editors, so almost…]] - rationale - shortsmaker/image_sources.py
- [[Plain text of an English Wikipedia article ('' when missing or unreachable).]] - rationale - shortsmaker/writing.py
- [[URL of a standard-size Wikimedia thumbnail the largest allowed step that fits…]] - rationale - shortsmaker/image_sources.py
- [[Usable images from a WikimediaWikipedia API query photos, screenshots,…]] - rationale - shortsmaker/image_sources.py
- [[Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable).]] - rationale - shortsmaker/footage.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[article_images()]] - code - shortsmaker/image_sources.py
- [[article_text()]] - code - shortsmaker/writing.py
- [[commons_films()]] - code - shortsmaker/footage.py
- [[commons_search()]] - code - shortsmaker/image_sources.py
- [[fact_check()]] - code - shortsmaker/writing.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[test_fact_check_drops_full()]] - code - tests/test_full_scenes.py
- [[thumb_url()]] - code - shortsmaker/image_sources.py
- [[usable_license()]] - code - shortsmaker/image_sources.py
- [[wm_files()]] - code - shortsmaker/image_sources.py
- [[wm_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Commons__Archive_Sources
SORT file.name ASC
```

## Connections to other communities
- 14 edges to [[_COMMUNITY_Footage Downloads & Crops]]
- 3 edges to [[_COMMUNITY_Style Lab & Edit Plan Text]]
- 3 edges to [[_COMMUNITY_Pool Gathering]]
- 2 edges to [[_COMMUNITY_Full-Scene Rescue & Plan Cleaning]]
- 2 edges to [[_COMMUNITY_Channel Profiles & CLI]]
- 1 edge to [[_COMMUNITY_Picture Picker]]
- 1 edge to [[_COMMUNITY_SFX Events & Full Pictures]]
- 1 edge to [[_COMMUNITY_Pool Storage & Contact Sheets]]
- 1 edge to [[_COMMUNITY_AI Calls & Quota Fallback]]
- 1 edge to [[_COMMUNITY_Script Writing Pipeline]]
- 1 edge to [[_COMMUNITY_Style Tests]]
- 1 edge to [[_COMMUNITY_Full-Scene Limits & Director Tests]]

## Top bridge nodes
- [[fact_check()]] - degree 8, connects to 5 communities
- [[article_text()]] - degree 7, connects to 4 communities
- [[get_image()]] - degree 7, connects to 3 communities
- [[wm_files()]] - degree 8, connects to 2 communities
- [[commons_films()]] - degree 6, connects to 2 communities