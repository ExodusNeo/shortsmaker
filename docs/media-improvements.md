# Media sourcing and audio improvements

Implementation scope approved 2026-11-01:

- Add direct Library of Congress, Wellcome, Smithsonian, Europeana, Pixabay photo, official brand-media and Duke advertising sources; keep missing-key services optional and never acquire new keys automatically.
- Search commercials by brand/product/year; accept owner-supplied files and source notes; sample camera shots; preserve source framing and distinguish original brand marks from uploader overlays.
- Balance source candidates, detect visual duplicates, check full-resolution pictures before writing, and preview/select vertical framing.
- Improve Freesound matching, retain multiple sound variants with approval, align their main impact and prevent duration overlaps.
- Select music by mood/intensity/instrumentation, avoid recent repeats, retain useful start offsets, provide narration previews, and use silence for an empty mood.
- Expand the local music choices from the existing approved free sound service, keeping new downloads pending review.
- Preserve resume/fix behavior, provenance and credit output. No paid APIs, no new logbook columns, no automatic uploads.

Optional source keys belong in ignored local files or environment variables. Unavailable services must be reported honestly by the media-library command; they must not block the other sources.

Verification: fixture tests for external response parsing and selection/fallback behavior; real FFmpeg smoke tests for audio timing, local clips and crop previews; existing picture, render-resume, prompt and package checks; Python compile and TypeScript checks. Update HANDOFF.md/history and refresh the code map after the implementation commit.

Delivered: `media.bat`, expanded adapters and local imports, candidate/crop improvements, audio selection and timing changes, and 20 music / 8 SFX candidates pending review. Verification passed (245 tests across 13 suites, compileall, tsc, diff check). Live provider restrictions and the unavailable Duke Ad*Access print connector are documented in `media-library.md`; local imports cover saved assets. No new keys were acquired.
