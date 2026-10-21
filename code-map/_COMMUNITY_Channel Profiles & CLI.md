---
type: community
members: 50
---

# Channel Profiles & CLI

**Members:** 50 nodes

## Members
- [[A Short's saved work state and `render()`, which turns a written Short into the…]] - rationale - shortsmaker/short_render.py
- [[A planned story sound {word, sound}, validated the word must be spoken in…]] - rationale - shortsmaker/audio_mix.py
- [[Automatic checks on a finished Short, the AI visual review and its fixes (incl.…]] - rationale - shortsmaker/review.py
- [[Choosing each scene's picture, pictures for full-screen scenes, and rescue…]] - rationale - shortsmaker/picker.py
- [[Cleaning and validating the planner's JSON (graphics, full-screen scenes,…]] - rationale - shortsmaker/plan_rules.py
- [[Command-line entry making a batch (`main`), fix.bat's one-scene re-render,…]] - rationale - shortsmaker/cli.py
- [[Headless Claude Code  Gemini (agy) calls that return JSON, with automatic…]] - rationale - shortsmaker/llm.py
- [[Paths, fixed settings, palettes and the styleskin tables every module shares.…]] - rationale - shortsmaker/config.py
- [[Real film clips (Commons, Internet Archive, NASA, Pixabay) and their ffmpeg…]] - rationale - shortsmaker/footage.py
- [[Rendering a Short with Remotion (with the Python renderer as fallback),…]] - rationale - shortsmaker/remotion_render.py
- [[Settings that change during a run (who plans, quota-out agents, the channel's…]] - rationale - shortsmaker/session.py
- [[ShortsMaker make ready-to-upload YouTube Shorts. Entry point make_shorts.py.]] - rationale - shortsmaker/__init__.py
- [[Small shared helpers downloads, ffmpeg, video encoder choice, durations, JSON…]] - rationale - shortsmaker/media_tools.py
- [[The owner's logbook and the Obsidian vault pages.]] - rationale - shortsmaker/logbook.py
- [[The pictures gathered for a topic before writing, their catalog, cache and…]] - rationale - shortsmaker/picture_pool.py
- [[Titles, descriptions and tags from YouTube autocomplete; the .srt captions file.]] - rationale - shortsmaker/seo.py
- [[Topics - Wikipedia research - writer - editor - director - fact check.]] - rationale - shortsmaker/writing.py
- [[Voice, captions, sound effects, story sounds and music levels.]] - rationale - shortsmaker/audio_mix.py
- [[Would a stranger scrolling the Shorts feed stop here Stayed-to-watch is…]] - rationale - shortsmaker/review.py
- [[__init__.py]] - code - shortsmaker/__init__.py
- [[audio_mix.py]] - code - shortsmaker/audio_mix.py
- [[clean_sound()]] - code - shortsmaker/audio_mix.py
- [[cli.py]] - code - shortsmaker/cli.py
- [[config.py]] - code - shortsmaker/config.py
- [[edit_plan.txt (the timestamped edit list) and per-scene cue timing.]] - rationale - shortsmaker/editplan.py
- [[editplan.py]] - code - shortsmaker/editplan.py
- [[first_second_check()]] - code - shortsmaker/review.py
- [[footage.py]] - code - shortsmaker/footage.py
- [[hex_rgb()]] - code - shortsmaker/config.py
- [[llm.py]] - code - shortsmaker/llm.py
- [[logbook.py]] - code - shortsmaker/logbook.py
- [[luminance()_1]] - code - shortsmaker/config.py
- [[media_tools.py]] - code - shortsmaker/media_tools.py
- [[pathlib]] - concept
- [[picker.py]] - code - shortsmaker/picker.py
- [[picture_pool.py]] - code - shortsmaker/picture_pool.py
- [[pil]] - concept
- [[plan_rules.py]] - code - shortsmaker/plan_rules.py
- [[random]] - concept
- [[re]] - concept
- [[remotion_render.py]] - code - shortsmaker/remotion_render.py
- [[review.py]] - code - shortsmaker/review.py
- [[seo.py]] - code - shortsmaker/seo.py
- [[session.py]] - code - shortsmaker/session.py
- [[short_render.py]] - code - shortsmaker/short_render.py
- [[urllib_parse]] - concept
- [[urllib_request]] - concept
- [[warnings]] - concept
- [[wave]] - concept
- [[writing.py]] - code - shortsmaker/writing.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Channel_Profiles__CLI
SORT file.name ASC
```

## Connections to other communities
- 32 edges to [[_COMMUNITY_Invention Slots]]
- 28 edges to [[_COMMUNITY_Entry Point, Logbook & Sounds]]
- 26 edges to [[_COMMUNITY_Local AI Jobs & Clips]]
- 21 edges to [[_COMMUNITY_Footage Downloads & Crops (2)]]
- 20 edges to [[_COMMUNITY_AI Calls & Quota Fallback (4)]]
- 20 edges to [[_COMMUNITY_Footage Downloads & Crops (2) (2)]]
- 20 edges to [[_COMMUNITY_Voice Worker (qwen_voice)]]
- 16 edges to [[_COMMUNITY_Story Sounds & Credits (2)]]
- 15 edges to [[_COMMUNITY_AI Calls & Quota Fallback]]
- 14 edges to [[_COMMUNITY_Picture List Catalog (2)]]
- 13 edges to [[_COMMUNITY_Full-Scene Rescue & Plan Cleaning]]
- 13 edges to [[_COMMUNITY_AI Calls & Quota Fallback (2)]]
- 13 edges to [[_COMMUNITY_Footage Downloads & Crops (2) (3)]]
- 12 edges to [[_COMMUNITY_Style Tests]]
- 11 edges to [[_COMMUNITY_Python Frame Renderer]]
- 8 edges to [[_COMMUNITY_Captions & TTS]]
- 6 edges to [[_COMMUNITY_Footage Downloads & Crops]]
- 5 edges to [[_COMMUNITY_Footage Downloads & Crops (2)_1]]
- 5 edges to [[_COMMUNITY_Captions & TTS (2)]]
- 5 edges to [[_COMMUNITY_Photo Cleanup]]
- 4 edges to [[_COMMUNITY_Scene Cues & Word Timing]]
- 4 edges to [[_COMMUNITY_Gemini Image Painting]]
- 3 edges to [[_COMMUNITY_Picture List Catalog (2)_1]]
- 3 edges to [[_COMMUNITY_GPU Worker (gen.py)]]
- 2 edges to [[_COMMUNITY_Picture List Catalog]]
- 2 edges to [[_COMMUNITY_Skins & Remotion Render]]
- 2 edges to [[_COMMUNITY_AI Calls & Quota Fallback (4) (2)]]
- 2 edges to [[_COMMUNITY_AI Calls & Quota Fallback (2)_1]]
- 2 edges to [[_COMMUNITY_Look & Transition Cleaning]]
- 2 edges to [[_COMMUNITY_Captions & TTS (3)]]
- 2 edges to [[_COMMUNITY_Look & Transition Cleaning (2)]]
- 2 edges to [[_COMMUNITY_Picture List Catalog (2) (2)]]
- 2 edges to [[_COMMUNITY_Split Script (tools)]]
- 1 edge to [[_COMMUNITY_Invention Slots (2)]]
- 1 edge to [[_COMMUNITY_Picture List Catalog (3)]]
- 1 edge to [[_COMMUNITY_Channel Profiles & CLI (2)]]
- 1 edge to [[_COMMUNITY_Style Guardrails]]
- 1 edge to [[_COMMUNITY_Story Sounds & Credits (3)]]
- 1 edge to [[_COMMUNITY_Story Sounds & Credits (4)]]
- 1 edge to [[_COMMUNITY_Picture List Catalog (2) (2)_1]]
- 1 edge to [[_COMMUNITY_Story Sounds & Credits (2) (2)]]

## Top bridge nodes
- [[plan_rules.py]] - degree 44, connects to 16 communities
- [[pathlib]] - degree 35, connects to 14 communities
- [[re]] - degree 43, connects to 13 communities
- [[config.py]] - degree 32, connects to 13 communities
- [[__init__.py]] - degree 28, connects to 13 communities