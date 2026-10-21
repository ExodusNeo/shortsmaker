---
source_file: "local_ai/gen.py"
type: "rationale"
community: "GPU Worker (gen.py)"
location: "L132"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/GPU_Worker_genpy
---

# NVENC (the GPU's video encoder) when ffmpeg has it, else CPU x264.

## Connections
- [[encoder_args()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/GPU_Worker_genpy