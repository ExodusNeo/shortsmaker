---
type: community
cohesion: 0.27
members: 10
---

# AI Video Clips & Encoding

**Cohesion:** 0.27 - loosely connected
**Members:** 10 nodes

## Members
- [[Fill a 916 frame with the picture (centre crop), for the AI video model's…]] - rationale - make_shorts.py
- [[Final H.264 encode NVENC on the GPU when available (frees the CPU), else x264.]] - rationale - make_shorts.py
- [[Image-to-video prompt for an animate scene (LTX on this PC, or Veo in Flow by…]] - rationale - make_shorts.py
- [[Pause the batch write each animate scene's start picture + Veo prompt to…]] - rationale - make_shorts.py
- [[Real motion for every scene with a picture scenes Claude matched to archival…]] - rationale - make_shorts.py
- [[cover_crop()]] - code - make_shorts.py
- [[local_clips()]] - code - make_shorts.py
- [[motion_prompt()]] - code - make_shorts.py
- [[veo_handoff()]] - code - make_shorts.py
- [[video_encoder()]] - code - make_shorts.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/AI_Video_Clips__Encoding
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_State & Logbook Helpers]]
- 5 edges to [[_COMMUNITY_Shared Imports & Downloads]]
- 2 edges to [[_COMMUNITY_SFX & Preview Sheets]]
- 2 edges to [[_COMMUNITY_Quality Checks & Captions]]
- 1 edge to [[_COMMUNITY_Voice Pipeline (VoiceStudio)]]

## Top bridge nodes
- [[local_clips()]] - degree 12, connects to 5 communities
- [[veo_handoff()]] - degree 8, connects to 3 communities
- [[cover_crop()]] - degree 5, connects to 2 communities
- [[video_encoder()]] - degree 5, connects to 2 communities
- [[motion_prompt()]] - degree 4, connects to 1 community