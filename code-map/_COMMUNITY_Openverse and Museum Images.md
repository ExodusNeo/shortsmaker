---
type: community
cohesion: 0.22
members: 9
---

# Openverse and Museum Images

**Cohesion:** 0.22 - loosely connected
**Members:** 9 nodes

## Members
- [[Downloads the real photos the picker chose for evidence boards, custom scenes…]] - rationale - shortsmaker/picker.py
- [[GET from Openverse, spaced to its anonymous limit (20 requests a minute). None…]] - rationale - shortsmaker/image_sources.py
- [[Images from museums, archives and photographers through Openverse (no key),…]] - rationale - shortsmaker/image_sources.py
- [[Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse…]] - rationale - shortsmaker/image_sources.py
- [[full_pictures()]] - code - shortsmaker/picker.py
- [[get_image()]] - code - shortsmaker/image_sources.py
- [[openverse_images()]] - code - shortsmaker/image_sources.py
- [[ov_get()]] - code - shortsmaker/image_sources.py
- [[test_board_pictures_attached()]] - code - tests/test_full_scenes.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Openverse_and_Museum_Images
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_CLI, Config and Footage]]
- 3 edges to [[_COMMUNITY_Stock Video Sources]]
- 2 edges to [[_COMMUNITY_Pictures-First Pool Tests]]
- 1 edge to [[_COMMUNITY_Review Auto-Fixes]]
- 1 edge to [[_COMMUNITY_Blender Build Planning]]
- 1 edge to [[_COMMUNITY_Wikimedia Image Search]]
- 1 edge to [[_COMMUNITY_Sound Design and Scene Cues]]

## Top bridge nodes
- [[get_image()]] - degree 9, connects to 5 communities
- [[ov_get()]] - degree 5, connects to 2 communities
- [[full_pictures()]] - degree 5, connects to 2 communities
- [[openverse_images()]] - degree 4, connects to 2 communities
- [[test_board_pictures_attached()]] - degree 3, connects to 2 communities