---
type: community
cohesion: 0.14
members: 19
---

# GPU Image Worker

**Cohesion:** 0.14 - loosely connected
**Members:** 19 nodes

## Members
- [[LTX's text encoder on the GPU. The repo ships it as 19GB fp32; a one-time bf16…]] - rationale - local_ai/gen.py
- [[Local GPU worker for ShortsMaker voice (Kokoro), images (SDXL-Lightning),…]] - rationale - local_ai/gen.py
- [[NVENC (the GPU's video encoder) when ffmpeg has it, else CPU x264.]] - rationale - local_ai/gen.py
- [[encoder_args()]] - code - local_ai/gen.py
- [[gc]] - concept
- [[gen.py]] - code - local_ai/gen.py
- [[images()]] - code - local_ai/gen.py
- [[item {image, out (.mp4), seconds, move, fps, width, height} -…]] - rationale - local_ai/gen.py
- [[item {image, prompt, out (.mp4), frames} - image-to-video clip at…]] - rationale - local_ai/gen.py
- [[item {prompt, out, width, height} - 4-step SDXL-Lightning image.]] - rationale - local_ai/gen.py
- [[item {text, voice, out (.wav)} - adds words start, end, word,…]] - rationale - local_ai/gen.py
- [[main()_1]] - code - local_ai/gen.py
- [[numpy]] - concept
- [[parallax()]] - code - local_ai/gen.py
- [[t5_encoder()]] - code - local_ai/gen.py
- [[to_grid()]] - code - local_ai/gen.py
- [[torch]] - concept
- [[tts()_1]] - code - local_ai/gen.py
- [[video()]] - code - local_ai/gen.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/GPU_Image_Worker
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Archive Film & Downloads]]
- 2 edges to [[_COMMUNITY_Channel Profiles & Menus]]
- 1 edge to [[_COMMUNITY_Sound Effects & Story Sounds]]
- 1 edge to [[_COMMUNITY_Word Counts & Test Utils]]

## Top bridge nodes
- [[gen.py]] - degree 17, connects to 4 communities