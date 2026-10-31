---
type: community
members: 17
---

# get_image

**Members:** 17 nodes

## Members
- [[Downloads the real photos the picker chose for evidence boards, custom scenes…]] - rationale - shortsmaker/picker.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Sound design each timed visual gets a matching sound. Candidates are kept by…]] - rationale - shortsmaker/audio_mix.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[_board()]] - code - tests/test_full_scenes.py
- [[full_pictures()]] - code - shortsmaker/picker.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[pick()_1]] - code - shortsmaker/audio_mix.py
- [[sc()]] - code - tests/test_style.py
- [[sfx_events()]] - code - shortsmaker/audio_mix.py
- [[test_board_pictures_attached()]] - code - tests/test_full_scenes.py
- [[test_sfx_full()]] - code - tests/test_full_scenes.py
- [[test_story_sound_wins_its_moment()]] - code - tests/test_full_scenes.py
- [[test_style_sounds()]] - code - tests/test_style.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/get_image
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_image_sources.py]]
- 4 edges to [[_COMMUNITY_test_full_scenes.py]]
- 2 edges to [[_COMMUNITY_choose_images]]
- 1 edge to [[_COMMUNITY_gather_pool]]
- 1 edge to [[_COMMUNITY_test_blender_plan.py]]
- 1 edge to [[_COMMUNITY_render]]
- 1 edge to [[_COMMUNITY_short_render.py]]
- 1 edge to [[_COMMUNITY_apply_review_fixes]]
- 1 edge to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_full_props]]
- 1 edge to [[_COMMUNITY_test_style.py]]

## Top bridge nodes
- [[get_image()]] - degree 9, connects to 4 communities
- [[sfx_events()]] - degree 7, connects to 2 communities
- [[full_pictures()]] - degree 5, connects to 2 communities
- [[openverse_images()]] - degree 4, connects to 2 communities
- [[_board()]] - degree 4, connects to 2 communities