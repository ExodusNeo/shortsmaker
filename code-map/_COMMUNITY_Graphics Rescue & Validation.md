---
type: community
cohesion: 0.13
members: 28
---

# Graphics Rescue & Validation

**Cohesion:** 0.13 - loosely connected
**Members:** 28 nodes

## Members
- [[(start, end) of the first time `phrase` is spoken, from TTS word timings.]] - rationale - shortsmaker/plan_rules.py
- [[(what one ink figure stands for, how many to draw) the planner's `each` when…]] - rationale - shortsmaker/plan_rules.py
- [[Cleaning and validating the planner's JSON (graphics, full-screen scenes,…]] - rationale - shortsmaker/plan_rules.py
- [[How the big-number scene prints a value 30,000  1.5 MILLION  2 BILLION  0.3.]] - rationale - shortsmaker/plan_rules.py
- [[Lowercase, accent-free word tokens, for matching names against spoken words.]] - rationale - shortsmaker/plan_rules.py
- [[One planned callout, validated (LLM output is untrusted); None drops it.]] - rationale - shortsmaker/plan_rules.py
- [[One planned full-screen motion graphic, validated (AI output is untrusted);…]] - rationale - shortsmaker/plan_rules.py
- [[Plain text of an English Wikipedia article ('' when missing or unreachable).]] - rationale - shortsmaker/writing.py
- [[Scenes whose picture is missing or weak may become a full-screen motion graphic…]] - rationale - shortsmaker/picker.py
- [[Start time of the first time `phrase` is spoken, from TTS word timings.]] - rationale - shortsmaker/plan_rules.py
- [[article_text()]] - code - shortsmaker/writing.py
- [[clean_full()]] - code - shortsmaker/plan_rules.py
- [[clean_graphic()]] - code - shortsmaker/plan_rules.py
- [[contains()]] - code - shortsmaker/plan_rules.py
- [[coords()]] - code - shortsmaker/plan_rules.py
- [[is_num()]] - code - shortsmaker/plan_rules.py
- [[number_figures()]] - code - shortsmaker/plan_rules.py
- [[plan_rules.py]] - code - shortsmaker/plan_rules.py
- [[rescue_graphics()]] - code - shortsmaker/picker.py
- [[show_number()]] - code - shortsmaker/plan_rules.py
- [[spoken_at()]] - code - shortsmaker/plan_rules.py
- [[spoken_span()]] - code - shortsmaker/plan_rules.py
- [[test_clean_full_keeps_board_pic()]] - code - tests/test_pictures_first.py
- [[test_number_scaling()]] - code - tests/test_full_scenes.py
- [[text()]] - code - shortsmaker/plan_rules.py
- [[unicodedata]] - concept
- [[word()]] - code - shortsmaker/plan_rules.py
- [[words_of()]] - code - shortsmaker/plan_rules.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Graphics_Rescue__Validation
SORT file.name ASC
```

## Connections to other communities
- 16 edges to [[_COMMUNITY_Channel Profiles & Menus]]
- 9 edges to [[_COMMUNITY_Sound Effects & Story Sounds]]
- 8 edges to [[_COMMUNITY_Full Scene Tests]]
- 7 edges to [[_COMMUNITY_Archive Film & Downloads]]
- 6 edges to [[_COMMUNITY_Film Footage Sources]]
- 5 edges to [[_COMMUNITY_Edit Plan Text]]
- 4 edges to [[_COMMUNITY_Scene & Graphic Timing]]
- 2 edges to [[_COMMUNITY_Style Candidates]]
- 2 edges to [[_COMMUNITY_Picture Catalog]]
- 2 edges to [[_COMMUNITY_QwenCosyVoice Worker]]
- 1 edge to [[_COMMUNITY_AI Calls & Trend Seeds]]
- 1 edge to [[_COMMUNITY_Word Counts & Test Utils]]
- 1 edge to [[_COMMUNITY_Entry Point & Run Menus]]
- 1 edge to [[_COMMUNITY_Review Auto Fixes]]
- 1 edge to [[_COMMUNITY_Remotion Render & Skins]]
- 1 edge to [[_COMMUNITY_Media Tools & Shot Spans]]
- 1 edge to [[_COMMUNITY_Quality & Visual Review]]
- 1 edge to [[_COMMUNITY_Picture Pool Prep]]
- 1 edge to [[_COMMUNITY_Style Guardrails]]
- 1 edge to [[_COMMUNITY_Motion Graphic Limits]]
- 1 edge to [[_COMMUNITY_Python Frame Renderer]]

## Top bridge nodes
- [[plan_rules.py]] - degree 44, connects to 12 communities
- [[rescue_graphics()]] - degree 10, connects to 6 communities
- [[article_text()]] - degree 6, connects to 4 communities
- [[clean_full()]] - degree 20, connects to 3 communities
- [[words_of()]] - degree 17, connects to 3 communities