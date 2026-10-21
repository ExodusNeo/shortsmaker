---
type: community
cohesion: 0.07
members: 55
---

# Footage Downloads & Crops

**Cohesion:** 0.07 - loosely connected
**Members:** 55 nodes

## Members
- [[Comfy-Org's official MOSS-Image text-to-image template (25 steps, CFG 2.5,…]] - rationale - shortsmaker/gpu.py
- [[CompletedProcess]] - code
- [[Download ~14s of film around the chosen moment (cropped with FILM_CROP to…]] - rationale - shortsmaker/footage.py
- [[Drop cached downloads and topic pools older than 30 days.]] - rationale - shortsmaker/picture_pool.py
- [[Keep titles that share at least one meaningful word (including 2-3 letter terms…]] - rationale - shortsmaker/image_sources.py
- [[Local AI on the owner's GPU and helpers ComfyUIMOSS, VoiceStudio, Gemini…]] - rationale - shortsmaker/gpu.py
- [[Match FILM_CROP on downloaded thumbnail JPEGs (cut top 6%, bottom 20%, and 4%…]] - rationale - shortsmaker/footage.py
- [[NASA photos (public domain), when the story touches space, flight or science.]] - rationale - shortsmaker/image_sources.py
- [[NASA videos (public domain), as their mediumsmall MP4 renditions.]] - rationale - shortsmaker/footage.py
- [[Paint on this PC with MOSS-Image in ComfyUI (owner's pick 2026-10-20 over SDXL-…]] - rationale - shortsmaker/gpu.py
- [[Path]] - code
- [[Pictures from Wikimedia Commons, Openverse, NASA and the Internet Archive, with…]] - rationale - shortsmaker/image_sources.py
- [[Pixabay stock video free to use in videos, no credit needed (Pixabay Content…]] - rationale - shortsmaker/footage.py
- [[Real film clips (Commons, Internet Archive, NASA, Pixabay) and their ffmpeg…]] - rationale - shortsmaker/footage.py
- [[Small shared helpers downloads, ffmpeg, video encoder choice, durations, JSON…]] - rationale - shortsmaker/media_tools.py
- [[Start and end of the camera shot containing time `at` (newsreels cut to title…]] - rationale - shortsmaker/footage.py
- [[Still images, magazinemanual scans, art and archival photos from the Internet…]] - rationale - shortsmaker/image_sources.py
- [[The pictures gathered for a topic before writing, their catalog, cache and…]] - rationale - shortsmaker/picture_pool.py
- [[Videos across the entire Internet Archive (historical film, retro gaming,…]] - rationale - shortsmaker/footage.py
- [[VoiceStudio's backend answers, starting the app (and waiting up to 2 min) if it…]] - rationale - shortsmaker/gpu.py
- [[archive_films()]] - code - shortsmaker/footage.py
- [[archive_images()]] - code - shortsmaker/image_sources.py
- [[comfy_call()]] - code - shortsmaker/gpu.py
- [[concurrent_futures]] - concept
- [[crop_film_bytes()]] - code - shortsmaker/footage.py
- [[duration()]] - code - shortsmaker/media_tools.py
- [[fetch()]] - code - shortsmaker/media_tools.py
- [[ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the…]] - rationale - shortsmaker/image_sources.py
- [[film_ffmpeg()]] - code - shortsmaker/image_sources.py
- [[film_frames()]] - code - shortsmaker/footage.py
- [[film_piece()]] - code - shortsmaker/footage.py
- [[footage.py]] - code - shortsmaker/footage.py
- [[gpu.py]] - code - shortsmaker/gpu.py
- [[hashlib]] - concept
- [[image_sources.py]] - code - shortsmaker/image_sources.py
- [[io]] - concept
- [[media_tools.py]] - code - shortsmaker/media_tools.py
- [[moss_graph()]] - code - shortsmaker/gpu.py
- [[moss_images()]] - code - shortsmaker/gpu.py
- [[n moments spread through a film, for the contact sheets (with FILM_CROP applied…]] - rationale - shortsmaker/footage.py
- [[nasa_films()]] - code - shortsmaker/footage.py
- [[nasa_images()]] - code - shortsmaker/image_sources.py
- [[nasa_search()]] - code - shortsmaker/image_sources.py
- [[on_topic()]] - code - shortsmaker/image_sources.py
- [[picture_pool.py]] - code - shortsmaker/picture_pool.py
- [[pil]] - concept
- [[pixabay_films()]] - code - shortsmaker/footage.py
- [[prune_cache()]] - code - shortsmaker/picture_pool.py
- [[shot_span()]] - code - shortsmaker/footage.py
- [[threading]] - concept
- [[time]] - concept
- [[up()]] - code - shortsmaker/gpu.py
- [[urllib_error]] - concept
- [[urllib_parse]] - concept
- [[voicestudio_up()]] - code - shortsmaker/gpu.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Footage_Downloads__Crops
SORT file.name ASC
```

## Connections to other communities
- 49 edges to [[_COMMUNITY_Channel Profiles & CLI]]
- 19 edges to [[_COMMUNITY_Motion Previews & Render Tests]]
- 14 edges to [[_COMMUNITY_Commons & Archive Sources]]
- 14 edges to [[_COMMUNITY_Style Lab & Edit Plan Text]]
- 10 edges to [[_COMMUNITY_Local AI Jobs & Clips]]
- 9 edges to [[_COMMUNITY_Pool Storage & Contact Sheets]]
- 8 edges to [[_COMMUNITY_Entry Point, Logbook & Sounds]]
- 7 edges to [[_COMMUNITY_Picture List Catalog]]
- 5 edges to [[_COMMUNITY_Music & Freesound]]
- 4 edges to [[_COMMUNITY_Story Sounds & Credits]]
- 4 edges to [[_COMMUNITY_Usable Picture Filter]]
- 4 edges to [[_COMMUNITY_Full-Scene Limits & Director Tests]]
- 3 edges to [[_COMMUNITY_Full-Scene Rescue & Plan Cleaning]]
- 3 edges to [[_COMMUNITY_Pool Gathering]]
- 3 edges to [[_COMMUNITY_Photo Cleanup]]
- 2 edges to [[_COMMUNITY_Gemini Image Painting]]
- 2 edges to [[_COMMUNITY_Voice Worker (qwen_voice)]]
- 2 edges to [[_COMMUNITY_Visual Review Sheets]]
- 2 edges to [[_COMMUNITY_Python Frame Renderer]]
- 2 edges to [[_COMMUNITY_GPU Worker (gen.py)]]
- 1 edge to [[_COMMUNITY_Picture Picker]]
- 1 edge to [[_COMMUNITY_Skins & Remotion Render]]
- 1 edge to [[_COMMUNITY_Captions & TTS]]
- 1 edge to [[_COMMUNITY_YouTube Research]]
- 1 edge to [[_COMMUNITY_Picture List Parsing]]
- 1 edge to [[_COMMUNITY_AI Calls & Quota Fallback]]
- 1 edge to [[_COMMUNITY_Style Tests]]

## Top bridge nodes
- [[picture_pool.py]] - degree 38, connects to 10 communities
- [[time]] - degree 22, connects to 10 communities
- [[image_sources.py]] - degree 38, connects to 9 communities
- [[media_tools.py]] - degree 24, connects to 8 communities
- [[gpu.py]] - degree 37, connects to 7 communities