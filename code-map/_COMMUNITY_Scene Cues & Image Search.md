---
type: community
cohesion: 0.06
members: 51
---

# Scene Cues & Image Search

**Cohesion:** 0.06 - loosely connected
**Members:** 51 nodes

## Members
- [[(start, end) of the first time `phrase` is spoken, from TTS word timings.]] - rationale - shortsmaker/plan_rules.py
- [[(what one ink figure stands for, how many to draw) the planner's `each` when…]] - rationale - shortsmaker/plan_rules.py
- [[A planned story sound {word, sound}, validated the word must be spoken in…]] - rationale - shortsmaker/audio_mix.py
- [[Candidate pictures (with preview `thumb` bytes) and sampled real-film frames…]] - rationale - shortsmaker/picture_pool.py
- [[Cleaning and validating the planner's JSON (graphics, full-screen scenes,…]] - rationale - shortsmaker/plan_rules.py
- [[Guardrails for the style library (STYLE_CAPS) the hook keeps only its title…]] - rationale - shortsmaker/plan_rules.py
- [[How the big-number scene prints a value 30,000  1.5 MILLION  2 BILLION  0.3.]] - rationale - shortsmaker/plan_rules.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Images used in an English Wikipedia article chosen by editors, so almost…]] - rationale - shortsmaker/image_sources.py
- [[Lowercase, accent-free word tokens, for matching names against spoken words.]] - rationale - shortsmaker/plan_rules.py
- [[Never scene 1 (real footage keeps the hook), never two in a row, never a scene…]] - rationale - shortsmaker/plan_rules.py
- [[One planned callout, validated (LLM output is untrusted); None drops it.]] - rationale - shortsmaker/plan_rules.py
- [[One planned full-screen motion graphic, validated (AI output is untrusted);…]] - rationale - shortsmaker/plan_rules.py
- [[Scenes whose picture is missing or weak may become a full-screen motion graphic…]] - rationale - shortsmaker/picker.py
- [[Start time of the first time `phrase` is spoken, from TTS word timings.]] - rationale - shortsmaker/plan_rules.py
- [[Timed extras for one scene a person card (photo `found`) when their name is…]] - rationale - shortsmaker/editplan.py
- [[URL of a standard-size Wikimedia thumbnail the largest allowed step that fits…]] - rationale - shortsmaker/image_sources.py
- [[Usable images from a WikimediaWikipedia API query photos, screenshots,…]] - rationale - shortsmaker/image_sources.py
- [[When each element of a full-screen motion graphic appears (absolute seconds)…]] - rationale - shortsmaker/plan_rules.py
- [[add()]] - code - shortsmaker/picture_pool.py
- [[article_images()]] - code - shortsmaker/image_sources.py
- [[clean_full()]] - code - shortsmaker/plan_rules.py
- [[clean_graphic()]] - code - shortsmaker/plan_rules.py
- [[clean_sound()]] - code - shortsmaker/audio_mix.py
- [[commons_search()]] - code - shortsmaker/image_sources.py
- [[contains()]] - code - shortsmaker/plan_rules.py
- [[coords()]] - code - shortsmaker/plan_rules.py
- [[full_cues()]] - code - shortsmaker/plan_rules.py
- [[gather_pool()]] - code - shortsmaker/picture_pool.py
- [[is_num()]] - code - shortsmaker/plan_rules.py
- [[limit_full()]] - code - shortsmaker/plan_rules.py
- [[limit_style()]] - code - shortsmaker/plan_rules.py
- [[load_thumb()]] - code - shortsmaker/picture_pool.py
- [[number_figures()]] - code - shortsmaker/plan_rules.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[plan_rules.py]] - code - shortsmaker/plan_rules.py
- [[rescue_graphics()]] - code - shortsmaker/picker.py
- [[scene()]] - code - tests/test_style.py
- [[scene_cues()]] - code - shortsmaker/editplan.py
- [[show_number()]] - code - shortsmaker/plan_rules.py
- [[spoken_at()]] - code - shortsmaker/plan_rules.py
- [[spoken_span()]] - code - shortsmaker/plan_rules.py
- [[squeeze()]] - code - shortsmaker/plan_rules.py
- [[test_clean_full_keeps_board_pic()]] - code - tests/test_pictures_first.py
- [[test_limit_style_caps()]] - code - tests/test_style.py
- [[text()]] - code - shortsmaker/plan_rules.py
- [[thumb_url()]] - code - shortsmaker/image_sources.py
- [[unicodedata]] - concept
- [[wm_files()]] - code - shortsmaker/image_sources.py
- [[word()]] - code - shortsmaker/plan_rules.py
- [[words_of()]] - code - shortsmaker/plan_rules.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Scene_Cues__Image_Search
SORT file.name ASC
```

## Connections to other communities
- 17 edges to [[_COMMUNITY_CLI & Pixabay Films]]
- 8 edges to [[_COMMUNITY_Film Archive Sources]]
- 7 edges to [[_COMMUNITY_Entry Point & Channel Menus]]
- 5 edges to [[_COMMUNITY_Config & Palettes]]
- 4 edges to [[_COMMUNITY_Style Validation]]
- 3 edges to [[_COMMUNITY_Style Candidates]]
- 2 edges to [[_COMMUNITY_Picture Pool & Catalog]]
- 2 edges to [[_COMMUNITY_Audio Mix & Music Gain]]
- 2 edges to [[_COMMUNITY_Frame Overlays & Fonts]]
- 2 edges to [[_COMMUNITY_Freesound & Picture Swaps]]
- 2 edges to [[_COMMUNITY_Test Patching Helpers]]
- 2 edges to [[_COMMUNITY_Pictures-First Tests]]
- 2 edges to [[_COMMUNITY_QwenCosyVoice Worker]]
- 2 edges to [[_COMMUNITY_Detail Marks & Storyboard]]
- 1 edge to [[_COMMUNITY_Fact Check]]
- 1 edge to [[_COMMUNITY_AI Calls & Quota]]
- 1 edge to [[_COMMUNITY_Picture Picker]]
- 1 edge to [[_COMMUNITY_Edit Plan Text]]
- 1 edge to [[_COMMUNITY_Sentence Voice Takes]]
- 1 edge to [[_COMMUNITY_Frame Maker & Credit Tags]]
- 1 edge to [[_COMMUNITY_Full Scene Tests]]
- 1 edge to [[_COMMUNITY_GPU Voice & Painters]]

## Top bridge nodes
- [[plan_rules.py]] - degree 44, connects to 12 communities
- [[gather_pool()]] - degree 17, connects to 6 communities
- [[rescue_graphics()]] - degree 8, connects to 5 communities
- [[unicodedata]] - degree 6, connects to 3 communities
- [[words_of()]] - degree 16, connects to 2 communities