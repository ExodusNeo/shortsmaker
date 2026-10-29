---
source_file: "shortsmaker/media_tools.py"
type: "rationale"
community: "render"
location: "L31"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/render
---

# Final H.264 encode: NVENC on the GPU when available (frees the CPU), else x264.

## Connections
- [[video_encoder()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/render