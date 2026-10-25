---
type: community
cohesion: 0.14
members: 54
---

# CLI, Config and Footage

**Cohesion:** 0.14 - loosely connected
**Members:** 54 nodes

## Members
- [[A Short's saved work state and `render()`, which turns a written Short into the…]] - rationale - shortsmaker/short_render.py
- [[Automatic checks on a finished Short, the AI visual review and its fixes (incl.…]] - rationale - shortsmaker/review.py
- [[Choosing each scene's picture, pictures for full-screen scenes, and rescue…]] - rationale - shortsmaker/picker.py
- [[Cleaning and validating the planner's JSON (graphics, full-screen scenes,…]] - rationale - shortsmaker/plan_rules.py
- [[Cleaning found photos stereograph cards, scanner borders, vertical crops.]] - rationale - shortsmaker/photo_prep.py
- [[Command-line entry making a batch (`main`), fix.bat's one-scene re-render,…]] - rationale - shortsmaker/cli.py
- [[Each channel's own rules (channelsname.rules.md, 2026-10-22) the niche's…]] - rationale - shortsmaker/rules.py
- [[Headless Claude Code  Gemini (agy) calls that return JSON, with automatic…]] - rationale - shortsmaker/llm.py
- [[Match FILM_CROP on downloaded thumbnail JPEGs (cut top 6%, bottom 20%, and 4%…]] - rationale - shortsmaker/footage.py
- [[One mid-scene frame per scene from the finished video, labeled with its…]] - rationale - shortsmaker/review.py
- [[Paths, fixed settings, palettes and the styleskin tables every module shares.…]] - rationale - shortsmaker/config.py
- [[Pictures from Wikimedia Commons, Openverse, NASA and the Internet Archive, with…]] - rationale - shortsmaker/image_sources.py
- [[Real film clips (Commons, Internet Archive, NASA, Pixabay) and their ffmpeg…]] - rationale - shortsmaker/footage.py
- [[Settings that change during a run (who plans, quota-out agents, the channel's…]] - rationale - shortsmaker/session.py
- [[ShortsMaker make ready-to-upload YouTube Shorts. Entry point make_shorts.py.]] - rationale - shortsmaker/__init__.py
- [[Tests for a Blender channel's run (2026-10-22) every scene drawn (no picture…]] - rationale - tests/test_blender_run.py
- [[Tests for the full-screen motion graphic scenes. No AI usage, no rendering.…]] - rationale - tests/test_full_scenes.py
- [[The Python renderer camera moves, graphic overlays, person cards, clip…]] - rationale - shortsmaker/frame_render.py
- [[The owner's logbook and the Obsidian vault pages.]] - rationale - shortsmaker/logbook.py
- [[The pictures gathered for a topic before writing, their catalog, cache and…]] - rationale - shortsmaker/picture_pool.py
- [[Titles, descriptions and tags from YouTube autocomplete; the .srt captions file.]] - rationale - shortsmaker/seo.py
- [[Topics - Wikipedia research - writer - editor - director - fact check.]] - rationale - shortsmaker/writing.py
- [[__init__.py]] - code - shortsmaker/__init__.py
- [[cli.py]] - code - shortsmaker/cli.py
- [[config.py]] - code - shortsmaker/config.py
- [[crop_film_bytes()]] - code - shortsmaker/footage.py
- [[edit_plan.txt (the timestamped edit list) and per-scene cue timing.]] - rationale - shortsmaker/editplan.py
- [[editplan.py]] - code - shortsmaker/editplan.py
- [[film_frames()]] - code - shortsmaker/footage.py
- [[footage.py]] - code - shortsmaker/footage.py
- [[frame_render.py]] - code - shortsmaker/frame_render.py
- [[image_sources.py]] - code - shortsmaker/image_sources.py
- [[io]] - concept
- [[llm.py]] - code - shortsmaker/llm.py
- [[logbook.py]] - code - shortsmaker/logbook.py
- [[n moments spread through a film, for the contact sheets (with FILM_CROP applied…]] - rationale - shortsmaker/footage.py
- [[pathlib]] - concept
- [[photo_prep.py]] - code - shortsmaker/photo_prep.py
- [[picker.py]] - code - shortsmaker/picker.py
- [[picture_pool.py]] - code - shortsmaker/picture_pool.py
- [[pil]] - concept
- [[plan_rules.py]] - code - shortsmaker/plan_rules.py
- [[review.py]] - code - shortsmaker/review.py
- [[rules.py]] - code - shortsmaker/rules.py
- [[seo.py]] - code - shortsmaker/seo.py
- [[session.py]] - code - shortsmaker/session.py
- [[short_render.py]] - code - shortsmaker/short_render.py
- [[storyboard()]] - code - shortsmaker/review.py
- [[test_blender_run.py]] - code - tests/test_blender_run.py
- [[test_full_scenes.py]] - code - tests/test_full_scenes.py
- [[threading]] - concept
- [[urllib_parse]] - concept
- [[warnings]] - concept
- [[writing.py]] - code - shortsmaker/writing.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/CLI_Config_and_Footage
SORT file.name ASC
```

## Connections to other communities
- 65 edges to [[_COMMUNITY_Audio Mix and Shotcut Export]]
- 44 edges to [[_COMMUNITY_Motion Scenes and Style Library]]
- 44 edges to [[_COMMUNITY_Local Voice and Freesound]]
- 31 edges to [[_COMMUNITY_Main Entry and Channel Profiles]]
- 21 edges to [[_COMMUNITY_Blender Build Planning]]
- 17 edges to [[_COMMUNITY_Channel Rules Files]]
- 15 edges to [[_COMMUNITY_Pictures-First Pool Tests]]
- 15 edges to [[_COMMUNITY_Stock Video Sources]]
- 15 edges to [[_COMMUNITY_Sound Design and Scene Cues]]
- 14 edges to [[_COMMUNITY_Frame Drawing and Graphics]]
- 14 edges to [[_COMMUNITY_Obsidian Vault Logbook]]
- 11 edges to [[_COMMUNITY_Full-Screen Graphic Validation]]
- 11 edges to [[_COMMUNITY_Narration Number Speech]]
- 10 edges to [[_COMMUNITY_Headless AI Planner Calls]]
- 10 edges to [[_COMMUNITY_Script Sounds and Graphics]]
- 9 edges to [[_COMMUNITY_MiniMax H3 Video Jobs]]
- 8 edges to [[_COMMUNITY_Picture Pool Storage]]
- 8 edges to [[_COMMUNITY_First-Second Opener Check]]
- 8 edges to [[_COMMUNITY_Quality and Visual Review]]
- 7 edges to [[_COMMUNITY_Sound Effects and Credits]]
- 6 edges to [[_COMMUNITY_Wikimedia Image Search]]
- 5 edges to [[_COMMUNITY_Openverse and Museum Images]]
- 5 edges to [[_COMMUNITY_Archive Photo Cleanup]]
- 5 edges to [[_COMMUNITY_Review Auto-Fixes]]
- 4 edges to [[_COMMUNITY_Edit Plan Text]]
- 4 edges to [[_COMMUNITY_Write Scripts Review Tests]]
- 4 edges to [[_COMMUNITY_Style Plan Validation]]
- 4 edges to [[_COMMUNITY_Graphics Rescue Caps]]
- 4 edges to [[_COMMUNITY_Usable Picture Catalog]]
- 4 edges to [[_COMMUNITY_Blender Scene Tests]]
- 3 edges to [[_COMMUNITY_ASS Captions and Skins]]
- 3 edges to [[_COMMUNITY_Film Clip Downloads]]
- 3 edges to [[_COMMUNITY_TTS and Story Sounds]]
- 3 edges to [[_COMMUNITY_Picture Swap Fixes]]
- 3 edges to [[_COMMUNITY_Gemini Image Painting]]
- 3 edges to [[_COMMUNITY_Custom Scene Redraw Tests]]
- 2 edges to [[_COMMUNITY_Repaint Prompt Rewrites]]
- 2 edges to [[_COMMUNITY_Full Graphic Limits]]
- 2 edges to [[_COMMUNITY_Local GPU Worker]]
- 2 edges to [[_COMMUNITY_Blender Camera Shots]]
- 1 edge to [[_COMMUNITY_Director Picture Cleanup Tests]]
- 1 edge to [[_COMMUNITY_AI Clip Prompts and Cuts]]
- 1 edge to [[_COMMUNITY_Local Voice Alignment]]
- 1 edge to [[_COMMUNITY_Style Library Caps]]
- 1 edge to [[_COMMUNITY_Logbook Results]]
- 1 edge to [[_COMMUNITY_Short Credit Tags]]
- 1 edge to [[_COMMUNITY_Script Splitting AST Tools]]

## Top bridge nodes
- [[test_full_scenes.py]] - degree 84, connects to 25 communities
- [[plan_rules.py]] - degree 51, connects to 15 communities
- [[pathlib]] - degree 49, connects to 13 communities
- [[writing.py]] - degree 38, connects to 12 communities
- [[picture_pool.py]] - degree 44, connects to 11 communities