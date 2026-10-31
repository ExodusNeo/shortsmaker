---
source_file: "shortsmaker/media_tools.py"
type: "rationale"
community: "local_clips"
location: "L31"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/local_clips
---

# Final H.264 encode: NVENC on the GPU when available (frees the CPU), else x264.

## Connections
- [[video_encoder()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/local_clips