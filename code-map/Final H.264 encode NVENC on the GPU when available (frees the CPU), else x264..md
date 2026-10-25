---
source_file: "shortsmaker/media_tools.py"
type: "rationale"
community: "AI Clip Prompts and Cuts"
location: "L31"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/AI_Clip_Prompts_and_Cuts
---

# Final H.264 encode: NVENC on the GPU when available (frees the CPU), else x264.

## Connections
- [[video_encoder()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/AI_Clip_Prompts_and_Cuts