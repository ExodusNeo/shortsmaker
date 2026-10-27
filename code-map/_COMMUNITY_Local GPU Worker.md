---
type: community
members: 19
---

# Local GPU Worker

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
- [[tts()]] - code - local_ai/gen.py
- [[video()]] - code - local_ai/gen.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Local_GPU_Worker
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_json]]
- 2 edges to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_gpu.py]]

## Top bridge nodes
- [[gen.py]] - degree 17, connects to 3 communities