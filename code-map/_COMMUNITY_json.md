---
type: community
members: 73
---

# json

**Members:** 73 nodes

## Members
- [[(ok, credit). Public domainCC0 need no credit; all other WikimediaWikipedia…]] - rationale - shortsmaker/image_sources.py
- [[Candidate pictures (with preview `thumb` bytes) and sampled real-film frames…]] - rationale - shortsmaker/picture_pool.py
- [[Check every line against the story's Wikipedia articles and rewrite what they…]] - rationale - shortsmaker/writing.py
- [[Comfy-Org's official MOSS-Image text-to-image template (25 steps, CFG 2.5,…]] - rationale - shortsmaker/gpu.py
- [[Free VoiceStudio's GPU memory the 8 GB card is needed next for SDXL, LTX and…]] - rationale - shortsmaker/gpu.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Images used in an English Wikipedia article chosen by editors, so almost…]] - rationale - shortsmaker/image_sources.py
- [[Keep titles that share a meaningful word with the query (including 2-3 letter…]] - rationale - shortsmaker/image_sources.py
- [[Local AI on the owner's GPU and helpers ComfyUIMOSS, VoiceStudio, Gemini…]] - rationale - shortsmaker/gpu.py
- [[Match FILM_CROP on downloaded thumbnail JPEGs (cut top 6%, bottom 20%, and 4%…]] - rationale - shortsmaker/footage.py
- [[NASA photos (public domain), when the story touches space, flight or science.]] - rationale - shortsmaker/image_sources.py
- [[NASA videos (public domain), as their mediumsmall MP4 renditions.]] - rationale - shortsmaker/footage.py
- [[Paint on this PC with MOSS-Image in ComfyUI (owner's pick 2026-10-20 over SDXL-…]] - rationale - shortsmaker/gpu.py
- [[Pictures from Wikimedia Commons, Openverse, NASA and the Internet Archive, with…]] - rationale - shortsmaker/image_sources.py
- [[Pixabay stock video free to use in videos, no credit needed (Pixabay Content…]] - rationale - shortsmaker/footage.py
- [[Plain text of an English Wikipedia article ('' when missing or unreachable).]] - rationale - shortsmaker/writing.py
- [[Real film clips (Commons, Internet Archive, NASA, Pixabay) and their ffmpeg…]] - rationale - shortsmaker/footage.py
- [[Scenes being repainted (scene index - what was wrong) get a better ai_image,…]] - rationale - shortsmaker/review.py
- [[Still images, magazinemanual scans, art and archival photos from the Internet…]] - rationale - shortsmaker/image_sources.py
- [[URL of a standard-size Wikimedia thumbnail the largest allowed step that fits…]] - rationale - shortsmaker/image_sources.py
- [[Usable images from a WikimediaWikipedia API query photos, screenshots,…]] - rationale - shortsmaker/image_sources.py
- [[Videos across the entire Internet Archive (historical film, retro gaming,…]] - rationale - shortsmaker/footage.py
- [[Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable).]] - rationale - shortsmaker/footage.py
- [[VoiceStudio's backend answers, starting the app (and waiting up to 2 min) if it…]] - rationale - shortsmaker/gpu.py
- [[What people actually type into YouTube search (free autocomplete endpoint, no…]] - rationale - shortsmaker/seo.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[add()]] - code - shortsmaker/picture_pool.py
- [[archive_films()]] - code - shortsmaker/footage.py
- [[archive_images()]] - code - shortsmaker/image_sources.py
- [[article_images()]] - code - shortsmaker/image_sources.py
- [[article_text()]] - code - shortsmaker/writing.py
- [[comfy_call()]] - code - shortsmaker/gpu.py
- [[commons_films()]] - code - shortsmaker/footage.py
- [[commons_search()]] - code - shortsmaker/image_sources.py
- [[concurrent_futures]] - concept
- [[crop_film_bytes()]] - code - shortsmaker/footage.py
- [[fact_check()]] - code - shortsmaker/writing.py
- [[fetch()_1]] - code - shortsmaker/media_tools.py
- [[film_frames()]] - code - shortsmaker/footage.py
- [[fingerprint()]] - code - shortsmaker/opener_render.py
- [[footage.py]] - code - shortsmaker/footage.py
- [[gather_pool()]] - code - shortsmaker/picture_pool.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[gpu.py]] - code - shortsmaker/gpu.py
- [[hashlib]] - concept
- [[image_sources.py]] - code - shortsmaker/image_sources.py
- [[json]] - concept
- [[load_thumb()]] - code - shortsmaker/picture_pool.py
- [[moss_graph()]] - code - shortsmaker/gpu.py
- [[moss_images()]] - code - shortsmaker/gpu.py
- [[n moments spread through a film, for the contact sheets (with FILM_CROP applied…]] - rationale - shortsmaker/footage.py
- [[nasa_films()]] - code - shortsmaker/footage.py
- [[nasa_images()]] - code - shortsmaker/image_sources.py
- [[nasa_search()]] - code - shortsmaker/image_sources.py
- [[on_topic()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[pixabay_films()]] - code - shortsmaker/footage.py
- [[rewrite_paint_prompts()]] - code - shortsmaker/review.py
- [[search_suggestions()]] - code - shortsmaker/seo.py
- [[test_fact_check_drops_full()]] - code - tests/test_full_scenes.py
- [[thumb_url()]] - code - shortsmaker/image_sources.py
- [[time]] - concept
- [[up()]] - code - shortsmaker/gpu.py
- [[urllib_error]] - concept
- [[urllib_parse]] - concept
- [[usable_license()]] - code - shortsmaker/image_sources.py
- [[voicestudio_unload()]] - code - shortsmaker/gpu.py
- [[voicestudio_up()]] - code - shortsmaker/gpu.py
- [[wm_files()]] - code - shortsmaker/image_sources.py
- [[wm_get()]] - code - shortsmaker/image_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/json
SORT file.name ASC
```

## Connections to other communities
- 67 edges to [[_COMMUNITY_pathlib]]
- 19 edges to [[_COMMUNITY_re]]
- 16 edges to [[_COMMUNITY_test_style.py]]
- 16 edges to [[_COMMUNITY_subprocess]]
- 15 edges to [[_COMMUNITY_local_clips]]
- 9 edges to [[_COMMUNITY_test_full_scenes.py]]
- 9 edges to [[_COMMUNITY_test_topic_ideas.py]]
- 7 edges to [[_COMMUNITY_h3_run.py]]
- 7 edges to [[_COMMUNITY_catalog_pool]]
- 6 edges to [[_COMMUNITY_test_pictures_first.py]]
- 6 edges to [[_COMMUNITY_blender_link.py]]
- 5 edges to [[_COMMUNITY_render]]
- 5 edges to [[_COMMUNITY_main_1]]
- 4 edges to [[_COMMUNITY_test_h3_handoff.py]]
- 4 edges to [[_COMMUNITY_test_story.py]]
- 3 edges to [[_COMMUNITY_test_blender_render.py]]
- 3 edges to [[_COMMUNITY_film_piece]]
- 3 edges to [[_COMMUNITY_ffmpeg]]
- 3 edges to [[_COMMUNITY_choose_images]]
- 3 edges to [[_COMMUNITY_apply_review_fixes]]
- 3 edges to [[_COMMUNITY_test_opener_render.py]]
- 3 edges to [[_COMMUNITY_owner]]
- 3 edges to [[_COMMUNITY_test_package.py]]
- 3 edges to [[_COMMUNITY_test_blender_scene.py]]
- 2 edges to [[_COMMUNITY_write_scripts]]
- 2 edges to [[_COMMUNITY_fake_ai]]
- 2 edges to [[_COMMUNITY_render_remotion]]
- 2 edges to [[_COMMUNITY_ask_ai]]
- 2 edges to [[_COMMUNITY_main]]
- 2 edges to [[_COMMUNITY_test_opener_plan.py]]
- 2 edges to [[_COMMUNITY_pack_people.py]]
- 2 edges to [[_COMMUNITY_people_standin.py]]
- 2 edges to [[_COMMUNITY_trend_research]]
- 2 edges to [[_COMMUNITY_draft_rules]]
- 2 edges to [[_COMMUNITY_Local GPU Worker]]
- 2 edges to [[_COMMUNITY_test_blender_link.py]]
- 1 edge to [[_COMMUNITY_frame_maker]]
- 1 edge to [[_COMMUNITY_captions]]
- 1 edge to [[_COMMUNITY_paint_instead]]
- 1 edge to [[_COMMUNITY_drawn_thumbnail]]
- 1 edge to [[_COMMUNITY_visual_review]]
- 1 edge to [[_COMMUNITY_ask]]
- 1 edge to [[_COMMUNITY_capture_prompts]]
- 1 edge to [[_COMMUNITY_edit_scripts]]
- 1 edge to [[_COMMUNITY_scene_kit.py]]
- 1 edge to [[_COMMUNITY_test_rules.py]]
- 1 edge to [[_COMMUNITY_math]]
- 1 edge to [[_COMMUNITY_opener_checks.py]]
- 1 edge to [[_COMMUNITY_opener_scene.py]]
- 1 edge to [[_COMMUNITY_test_opener_checks.py]]
- 1 edge to [[_COMMUNITY_test_opener_scene.py]]

## Top bridge nodes
- [[json]] - degree 115, connects to 39 communities
- [[gpu.py]] - degree 53, connects to 11 communities
- [[time]] - degree 26, connects to 11 communities
- [[image_sources.py]] - degree 42, connects to 10 communities
- [[gather_pool()]] - degree 17, connects to 6 communities