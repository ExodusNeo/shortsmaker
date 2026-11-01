# Pictures, commercials, music and sound effects

Double-click **media.bat** to manage the library. **run.bat** automatically uses these improvements on new Shorts.

## Import a commercial or picture

Choose **1**, drag a saved picture/video file into the window, then enter its title, search tags, original source link and credit/rights note. Include the brand, product, year and country when known. The original file is copied, never moved. Imported files live in `media_library/images/` or `media_library/videos/` and participate in the same picture selection as online sources.

Files dropped directly into `media_library/` also work: their filenames are searchable. A sidecar named `clip.mp4.json` or `picture.jpg.json` can supply `title`, `tags`, `source_url` and `credit`. Missing rights are reported as unspecified, never assumed to be public domain.

## Find and approve audio

- **2** lists music; **3** lists story sound effects. Pick a file number, then **P** plays it, **A** approves it, **R** rejects it, and **E** changes its timing/tags.
- **4** searches the existing Freesound account for music choices in all five moods. New downloads are CC0 previews and stay **pending** until you approve them. Search results can include unsuitable material: listen before approval. Existing music remains available.
- **5** searches for several versions of a named story sound. Name the sound precisely, e.g. `single ship bell` or `mechanical cash register`. New variants wait for approval; existing automatic story-sound fetching remains a fallback.
- **6** makes a 12-second music preview with the most recent saved narration. A normal render also writes `music_preview.wav` beside the finished video.
- **9** copies in your own music or sound effect, retaining its credit note and source link, for the same preview/approval workflow.

Music stays in `music/<mood>/`. Selection avoids the most recent five tracks when the mood has enough choices; a smaller library reuses its least recent track. An empty/unrecognized mood stays silent and is explained in the edit plan. Intensity and instrument tags help choose among fitting tracks. An optional start time skips an intro; it is saved with the Short for fixes/resume.

For a story sound, **E** can adjust its main impact time (seconds into the file) and search aliases. The strongest measured 10-ms window supplies the initial impact; this is a timing aid, not a guarantee that it is the perceptually right moment. The effect is offset so that impact meets the spoken word, trimming its beginning when necessary. Effects compete over their actual durations; a single quiet texture may remain underneath a more important effect. Every mixed effect is high-passed at 220 Hz.

## Online sources

New searches include Wellcome Collection, Library of Congress photographs, Smithsonian Open Access images, Europeana, Pixabay photographs, official brand pages and Duke AdViews commercials through Internet Archive. They supplement the existing Wikimedia, Openverse, Archive, NASA and stock-video sources. Duke's separate Ad*Access print-ad site does not currently provide a working automated connector here; saved print ads can be imported locally.

Commercial searches retain brand/product/year/country details supplied by the planner. Short ads and local clips up to ten minutes are scanned for camera cuts, with at most twelve preview moments. Other videos keep spread-out sampling. Network ads are copied once into the cache for local sampling; failed/slow scans fall back to ordinary previews. The existing YouTube-reupload exclusions remain in place.

New film downloads retain the complete source frame, with a fitted foreground over a blurred background. Original commercial audio is removed. The visual editor rejects uploader overlays while allowing genuine brand marks, prices, packaging and campaign text. Source availability and credit are not a determination of permission or fair use.

Stills are balanced across providers before the candidate limit, visually deduplicated before numbering, and checked as full-size downloads before writing. Contact sheets show the cleaned original and three vertical crop previews. The picker can place the crop around an off-centre subject; exact selected crops are saved as `work/crop_preview_<scene>.jpg`.

## Source settings and unavailable services

**7** reports the last source status. **8** adds another brand's public official media page and search aliases. The adapter reads ordinary image tags and direct downloadable video links; interactive/logged-in players are not supported. Sites may block automated requests. Save an asset yourself and use **1** when that happens.

`media_sources.json` controls providers, configured brand pages and music ducking. No accounts were created. Pixabay/Freesound reuse the owner's existing keys. Smithsonian initially uses its documented public `DEMO_KEY`, which is heavily rate-limited. The owner supplied a Europeana key on 2026-11-01; it is configured in ignored `europeana_key.txt`, and a live image search succeeded. Optional keys can also use `SHORTSMAKER_EUROPEANA_KEY` / `SHORTSMAKER_SMITHSONIAN_KEY` environment variables. Keys are never printed or committed.

Initial live checks: Wellcome pictures, Duke/Archive commercial files and Freesound search/downloads worked. Library of Congress and McDonald's pages returned HTTP 403 from this machine; Smithsonian's demo allowance reached HTTP 429 during verification. Their adapters are implemented and fail without blocking the remaining sources. These limitations are visible in source status.

The owner clarified that the intended improvement is more sources for downloads as needed, rather than bulk library downloads. Do not run the bulk music/SFX discovery commands without an explicit request. All current media was approved at the owner's request on 2026-11-01: 28 music tracks and 61 sound effects, including the initial 20 music candidates and eight sound variants. Nothing is pending.

No paid API, automatic upload or logbook-column change is involved. Source files and runtime library metadata stay local and ignored by Git.
