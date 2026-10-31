# Reliability improvements, authorized 2026-10-31

The owner approved all four engineering improvements while new retention results accumulate.
These do not change the storytelling strategy or the fresh performance baseline.

- [x] Preserve failed runs and queue completed scripts before SEO/rendering; checkpoint pictures, narration
  and video; offer resume in run.bat and a separate resume.bat. Keep unfinished work during pruning.
- [x] Reuse verified narration when text/voice settings match. Commit final videos only after encoding succeeds.
  Resume post-render work without a new encode. Make logbook finalization idempotent.
- [x] Record Passed / Problems found / Not reviewed for opening and visual AI review. Missing previews and
  malformed replies must produce a check, never an implicit pass.
- [x] Add a scene preview/apply path for circle/arrow position, label and removal, with original audio and
  captions retained. Restrict the fast path to stills with hard cuts; use ordinary repair otherwise.
- [x] Bound picture retries and try a suitable unused reviewed pool image before existing fallbacks.
- [x] Regression tests, a real render/cache/resume smoke test, real isolated callout repair, visual inspection,
  updated HANDOFF/history and separate code-map refresh.

Additional defect found during verification: long temporary paths could truncate the actual Node error
headline from drawn-opener feedback. Preserve that headline first; covered by a regression test.

Usage and limitations: `docs/reliability.md`. Retention Part 3.2 remains the next data-learning task.
