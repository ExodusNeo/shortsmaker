---
type: community
cohesion: 0.17
members: 12
---

# Voice Pipeline (VoiceStudio)

**Cohesion:** 0.17 - loosely connected
**Members:** 12 nodes

## Members
- [[Free VoiceStudio's GPU memory the 8 GB card is needed next for SDXL, LTX and…]] - rationale - make_shorts.py
- [[Mike the Headless Chicken, fix round 3 the LTX worker died without writing…]] - rationale - tests/test_full_scenes.py
- [[Run a batch on this PC's GPU through a local_ai worker (gen.py, or…]] - rationale - make_shorts.py
- [[Voice every scene on the GPU CosyVoice (aiden, documentary) for the whole…]] - rationale - make_shorts.py
- [[VoiceStudio's backend answers, starting the app (and waiting up to 2 min) if it…]] - rationale - make_shorts.py
- [[fake_run()]] - code - tests/test_full_scenes.py
- [[local_job()]] - code - make_shorts.py
- [[local_voice()]] - code - make_shorts.py
- [[test_local_job_retries_a_hard_crash()]] - code - tests/test_full_scenes.py
- [[up()]] - code - make_shorts.py
- [[voicestudio_unload()]] - code - make_shorts.py
- [[voicestudio_up()]] - code - make_shorts.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Voice_Pipeline_VoiceStudio
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Shared Imports & Downloads]]
- 2 edges to [[_COMMUNITY_Quality Checks & Captions]]
- 2 edges to [[_COMMUNITY_State & Logbook Helpers]]
- 1 edge to [[_COMMUNITY_AI Painters (MOSS & Gemini)]]
- 1 edge to [[_COMMUNITY_AI Video Clips & Encoding]]
- 1 edge to [[_COMMUNITY_Full-Scene Validation]]

## Top bridge nodes
- [[local_job()]] - degree 8, connects to 5 communities
- [[local_voice()]] - degree 7, connects to 3 communities
- [[voicestudio_up()]] - degree 4, connects to 1 community
- [[test_local_job_retries_a_hard_crash()]] - degree 4, connects to 1 community
- [[voicestudio_unload()]] - degree 3, connects to 1 community