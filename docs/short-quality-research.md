# Shorts quality audit — 2026-11-01

The largest opportunity is a tighter story and clearer visual explanation. The project already has a
capable production pipeline. More effects, tags or model calls alone will not establish better results.
The changes below repair specific gaps; increased audience retention remains a hypothesis to measure.

## Evidence and limits

Reviewed `writing`, `seo`, `logbook`, `retention`, `review`, `editplan`, `short_render`, caption rendering,
channel rules, the previous audit, existing tests and the latest Bobby Leach edit plan/storyboard.
Used the local `motion-design` and `review-loop` skills for readable holds and visual assessment.

YouTube describes Shorts ranking signals as choosing to watch, average view duration, average percentage
viewed and satisfaction. Search also considers metadata relevance and whether people click and watch.
This supports giving hook clarity and story delivery priority over metadata padding.
[YouTube Shorts discovery](https://support.google.com/youtube/answer/11914225?hl=en).

YouTube's interview with creator Jenny Hoyos emphasizes an immediate hook and a satisfying mini-story.
It does not establish a universal optimal duration or cut frequency.
[Creator/product-lead interview](https://blog.youtube/creator-and-artist-stories/youtube-shorts-deep-dive/).

Previous project research recorded transcripts and view counts for Voggle, Zack D. Films, Squire Explains
and Boupai. Examples in the 2026-10-31 audit include Squire's pilot story (recorded 1.8M, 74s) and Boupai's
eBay story (recorded 1.6M, 28s): both establish a clear question, advance consequences and deliver a concrete
ending. Those are historical observations, not freshly verified counts or causal proof. Direct retrieval
of the two YouTube pages failed in this session. Competitor captions/topics were not put into production
prompts. The current active logbook has no filled performance numbers, so it cannot establish an uplift.

## Findings and implemented changes

| Area | Actual gap | Change |
|---|---|---|
| Script momentum | A predicted swipe after scene 4 did not trigger the existing editorial retry. Three separated filler scenes also passed. | Apply the existing bounded retry to swipe points before the final two scenes and to 3+ scenes marked as adding nothing. An unanswered opening question is a problem. |
| Final script | Fact checking could change narration after the cold reader's verdict. | Re-read only changed scripts, batched in one conditional call. Replace the old verdict; flag a missing review. Never rewrite verified facts during this step. |
| Truthful checks | A malformed fact-check object could be reported as “every line held up.” | Require an explicit boolean verdict and a fixes list; surface unreviewed facts in CHECK lines. |
| Rendered pacing | Scene counts concealed how much runtime was spent on detours; callouts lacked a deterministic reading-time check. | Report actual seconds in scenes the cold reader marked as empty and the predicted swipe timestamp. Flag short callout holds using the existing skill's reading guidance. These are review prompts, not automatic cuts. |
| SEO | Autocomplete order was described as search-volume ranking. Tags were claimed to assign an audience. Forced controversy and generic descriptions weakened packaging. | Treat predictions as wording ideas, require relevance to the narration, emphasize accurate title/description, avoid generic hype and manufactured dilemmas. |
| Metadata reliability | Malformed rows/fields could crash or corrupt metadata; a good title was ignored without tags. | Validate fields independently; preserve usable drafts, reject invalid/overlong replacement titles, deduplicate whole tags within a conservative budget, record fallback notes. |
| Upload captions | Every seven words became one SRT block regardless of sentence, pause or line length. | Break on sentence endings, pauses, width, duration and word count while preserving the narration and its word timings. Burned-in caption styling is unchanged. |
| Learning | Retention reports never reached future planning, and posting age was absent. | Read reports only for current-channel active-logbook entries with 100+ views. Match approximate drops to saved scene types and report repeated overlaps across at least 3 distinct Shorts. Add posting age; explicitly distinguish it from the unknown metrics capture date. No logbook edits. |

The latest saved Bobby Leach Short provides a concrete regression example: its cold reader marked scenes
7, 9 and 12 as adding nothing. Actual scene timing makes that **7.6 seconds**, with a predicted swipe at
**22.7 seconds**. This is an AI editorial assessment, not measured viewer behavior. The new checks surface
both findings. Its existing storyboard also shows tiny diagram labels competing with large captions;
future graphics should communicate their point at phone size. The orange-peel spoiler in that older render
is already addressed by the preceding opener-protection change; this audit did not repair that saved video.

YouTube states that tags generally have a minimal discovery role beyond misspellings.
[Official tag guidance](https://support.google.com/youtube/answer/146402?hl=en).
Google describes autocomplete as contextual predictions, influenced by several factors; it is not a
volume dataset. This is Google Search documentation, not documentation of the unofficial YouTube endpoint.
The endpoint used here returns phrases, without volume measurements.
[Autocomplete explanation](https://support.google.com/websearch/answer/7368877?hl=en).

Retention dips identify places to investigate. They do not prove that a map, person card or other visual
caused the decline. Overlap counts have no exposure denominator: three drops during graphics are not a
graphics failure rate. [YouTube retention guidance](https://support.google.com/youtube/answer/9314415?hl=en).

## GitHub projects worth using

These are focused options for this codebase, not replacements for its existing pipeline. No new runtime
packages, models, keys or paid services were installed during the audit.

| Repository | Fit for ShortsMaker | Decision |
|---|---|---|
| [remotion-dev/skills](https://github.com/remotion-dev/skills) | Official rendering, timing, captions and typography guidance. | Already present under `remotion/.agents/skills`. Use the relevant skill for visual work; installing a duplicate adds little. Pipeline prompts still need their own condensed rules because interactive skills are excluded from pipeline calls. |
| [remotion-dev/template-tiktok](https://github.com/remotion-dev/template-tiktok) | Reference implementation of local Whisper.cpp captions in Remotion. | Useful for phrase-page experiments. Keep the current known narration and aligner; do not retranscribe every generated voice by default. Remotion's licensing terms apply. |
| [m-bain/whisperX](https://github.com/m-bain/whisperX) | Independent transcription/forced alignment for detecting missing, repeated or mispronounced speech. BSD-2-Clause repository. | Good future optional QA worker, isolated on D:. Existing MMS alignment already handles timing, so install only for a measured speech-check need. Evaluate model licences separately and benchmark CPU/VRAM use. |
| [snakers4/silero-vad](https://github.com/snakers4/silero-vad) | Speech detection can distinguish soft narration from actual silence. MIT; supports ONNX. | Consider if FFmpeg's current fixed silence threshold produces false positives. CPU/ONNX is attractive on this 8GB GPU machine. It does not judge script quality or pronunciation. |
| [WyattBlue/auto-editor](https://github.com/WyattBlue/auto-editor) | Silence-based cuts with margins; supports Shotcut export. Unlicense. | Useful reference for a future pre-timeline voice trim pass. Do not apply it to a finished Short: that would invalidate word cues, overlays, captions and retention timestamps unless all timings are remapped. |
| [whaleyxbt/claude-motion](https://github.com/whaleyxbt/claude-motion) | Motion hierarchy, readable holds, easing and visual review. MIT. | Already adapted by the local motion-design/review-loop skills. Improve those existing tools instead of importing another style system. |

No repository's popularity is evidence that its defaults improve this channel's retention. Test the
specific behavior being borrowed. Full generators would duplicate sourcing, rendering and review systems
already implemented here.

## Next improvements, in priority order

1. **Reliable factual research.** Save claim-to-source references and verify the hook and payoff against a
   second independent source when historical accounts disagree. Today's Wikipedia/AI-confidence path can
   still accept an unsupported statement; the new validation makes missing reviews visible, not infallible.
2. **Phone-readable explanation.** Sample full-screen graphics at each spoken cue, check large text and
   reading holds, simplify crowded diagrams, and preserve the strongest visual for the actual payoff.
   Current contact sheets show selected moments; they cannot prove continuous motion quality.
3. **Speech QA before final timing.** Detect omitted/repeated words and pronunciation problems, then regenerate
   only affected takes. Verify any silence trim before propagating all word/cut times. Do not speed narration
   globally just to meet a duration target.
4. **Length based on story beats.** Fixed minimum word/scene counts can encourage padding. First collect fresh
   retention by comparable duration; then evaluate a wider length range and the weird-economics length-rule
   conflict. The first patch preserves existing length targets and opener branding.
5. **Competitor structure research.** Fetch a small sample of captions and current view counts, save abstract
   structure observations separately from the taken-topic list, and keep original titles/scripts out of the
   writer. Failure to obtain transcripts should leave this input absent, never fabricate a pattern.

## Measurement and validation

Compare Shorts at the same age where possible (for example 7 days), with enough views and similar lengths.
Use stayed-to-watch for the opening and average duration/percentage plus retention curves for delivery.
Look for repeated patterns across at least three Shorts; a larger sample is preferable. Fill the existing
Posted on field using YYYY-MM-DD. Save new screenshots with `retention.bat`; future planning now uses the
reports automatically when matching active entries have sufficient views.

The new checks are covered by `tests/test_quality.py`, with existing story, rules, SEO/pictures-first,
retention and real FFmpeg render/resume regressions. Final verification results are recorded in
`HANDOFF_history.md`. No full new AI-generated Short or audience experiment has been completed by this patch.
