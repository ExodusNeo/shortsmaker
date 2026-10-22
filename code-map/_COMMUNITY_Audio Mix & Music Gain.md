---
type: community
cohesion: 0.12
members: 26
---

# Audio Mix & Music Gain

**Cohesion:** 0.12 - loosely connected
**Members:** 26 nodes

## Members
- [[At most MAX_STORY_SOUNDS story sounds per Short (the first ones), so each one…]] - rationale - shortsmaker/audio_mix.py
- [[Final H.264 encode NVENC on the GPU when available (frees the CPU), else x264.]] - rationale - shortsmaker/media_tools.py
- [[Path]] - code
- [[Path_1]] - code
- [[Small shared helpers downloads, ffmpeg, video encoder choice, durations, JSON…]] - rationale - shortsmaker/media_tools.py
- [[Start and end of the camera shot containing time `at` (newsreels cut to title…]] - rationale - shortsmaker/footage.py
- [[TTS with retries Microsoft's free Edge voice service drops a request now and…]] - rationale - shortsmaker/audio_mix.py
- [[The sound file for a story sound the owner's own file in…]] - rationale - shortsmaker/audio_mix.py
- [[Voice, captions, sound effects, story sounds and music levels.]] - rationale - shortsmaker/audio_mix.py
- [[Volume factor that brings this track's loudness (first 60 s) to MUSIC_LUFS;…]] - rationale - shortsmaker/audio_mix.py
- [[asyncio]] - concept
- [[audio_mix.py]] - code - shortsmaker/audio_mix.py
- [[duration()]] - code - shortsmaker/media_tools.py
- [[edge_tts]] - concept
- [[ffmpeg()]] - code - shortsmaker/media_tools.py
- [[limit_sounds()]] - code - shortsmaker/audio_mix.py
- [[media_tools.py]] - code - shortsmaker/media_tools.py
- [[music_gain()]] - code - shortsmaker/audio_mix.py
- [[shot_span()]] - code - shortsmaker/footage.py
- [[speak()]] - code - shortsmaker/audio_mix.py
- [[story_sound()]] - code - shortsmaker/audio_mix.py
- [[subprocess]] - concept
- [[tts()]] - code - shortsmaker/audio_mix.py
- [[urllib_request]] - concept
- [[video_encoder()]] - code - shortsmaker/media_tools.py
- [[wave]] - concept

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Audio_Mix__Music_Gain
SORT file.name ASC
```

## Connections to other communities
- 16 edges to [[_COMMUNITY_CLI & Pixabay Films]]
- 13 edges to [[_COMMUNITY_Config & Palettes]]
- 7 edges to [[_COMMUNITY_Freesound & Picture Swaps]]
- 6 edges to [[_COMMUNITY_Entry Point & Channel Menus]]
- 5 edges to [[_COMMUNITY_GPU Voice & Painters]]
- 5 edges to [[_COMMUNITY_Caption Lines (ASS)]]
- 4 edges to [[_COMMUNITY_AI-Coded Motion Scenes]]
- 3 edges to [[_COMMUNITY_Shotcut Timeline]]
- 3 edges to [[_COMMUNITY_Package & TS Tests]]
- 2 edges to [[_COMMUNITY_Film Frames & Crops]]
- 2 edges to [[_COMMUNITY_Film Archive Sources]]
- 2 edges to [[_COMMUNITY_Picture Pool & Catalog]]
- 2 edges to [[_COMMUNITY_Scene Cues & Image Search]]
- 2 edges to [[_COMMUNITY_QwenCosyVoice Worker]]
- 2 edges to [[_COMMUNITY_SFX Synthesis]]
- 2 edges to [[_COMMUNITY_Full Scene Tests]]
- 1 edge to [[_COMMUNITY_Review Fixes & Pool Swaps]]
- 1 edge to [[_COMMUNITY_Gemini Painting & Renderer Choice]]
- 1 edge to [[_COMMUNITY_Edit Plan Text]]
- 1 edge to [[_COMMUNITY_Local Clips & GPU Jobs]]
- 1 edge to [[_COMMUNITY_Detail Marks & Storyboard]]
- 1 edge to [[_COMMUNITY_Subject Position Checks]]
- 1 edge to [[_COMMUNITY_Sound Cue Sheet]]
- 1 edge to [[_COMMUNITY_Style Candidates]]
- 1 edge to [[_COMMUNITY_First-Second Check Tests]]
- 1 edge to [[_COMMUNITY_Sentence Voice Takes]]
- 1 edge to [[_COMMUNITY_Frame Overlays & Fonts]]
- 1 edge to [[_COMMUNITY_Package Split Tool]]

## Top bridge nodes
- [[subprocess]] - degree 37, connects to 17 communities
- [[media_tools.py]] - degree 28, connects to 13 communities
- [[audio_mix.py]] - degree 37, connects to 11 communities
- [[shot_span()]] - degree 6, connects to 3 communities
- [[duration()]] - degree 6, connects to 2 communities