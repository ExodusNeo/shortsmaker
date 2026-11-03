# Read a Short's retention graph

Run `retention.bat`, select the finished Short, then drag a PNG/JPG/WebP screenshot of its YouTube Studio
retention graph into the window and press Enter. Include the curve and the full time axis in the screenshot.
Choose **1) Review a retention graph**. You can add optional Studio details after choosing the screenshot,
then choose the AI mode for the review. Existing subscription models and quota fallback apply.

To add or change details later without another AI call, run `retention.bat`, choose the Short, then choose
**2) Add/update optional Studio details (no AI)**. This also works before you have a graph.

All fields are optional:

- Views; stayed to watch (%); average percentage viewed (including values over 100%).
- Average view duration, entered as seconds or M:SS (for example `24.5` or `0:24.5`).
- Posted on and numbers collected on, using YYYY-MM-DD; the reporting period shown in Studio.
- Likes, comments, subscribers gained, and your own notes.

Press Enter to skip an unknown value or keep a previous value. Type `-` to clear a previous value.
Counts accept commas (`1,234`), and percentages accept a `%` sign. Use details from the same video and
reporting period as the graph. Unknown fields stay unknown; a blank is not treated as zero.

The report is saved in that Short's output folder:

- `retention.txt`: up to three visible drops, matched to the edit plan's scenes, plus limitations.
- `retention/graph.png` (or the screenshot's other supported extension): the screenshot used for the report.
- `retention/metrics.json`: your optional manual details, editable later through the helper's option 2.

New graph reviews include the manual details in their AI input and report. A report is a snapshot from
review time; future planning always reads the latest optional details, including updates made without
another graph review. Details can also be used before a graph is added.

Timings are approximate, normally within 1–2 seconds. The report does not infer exact retention percentages
or establish why viewers left. If the graph cannot be read, it records that rather than guessing timings.
An unusable AI reply leaves any previous report intact.

Retention reviews are independent of the logbook. You choose which videos to submit (the owner's workflow:
submit graphs once a video has at least 100 views). You do not need to record views, dates or notes in the
logbook for retention reviews or future planning to use them. No logbook entry or view-count check is required.

Future planning reads saved `retention.txt` reports directly from the active channel's output folders,
even when its logbook is missing or empty. Only approximate drop timings are matched to saved scene types;
patterns are reported when they repeat across at least three distinct Shorts. Other channels' reports are
excluded. Overlap counts do not establish causes or failure rates. No reliable repeated observation means
no inferred lesson. Optional manual details are passed to future planning as context, with the saved video
length; when both dates are entered, the report also shows age when the numbers were collected. No minimum
view count is enforced. Compare similar ages, exposure, lengths and reporting periods before changing strategy.
Notes are observations or hypotheses, not proven causes. Older reports without manual details still work.

For command-line use:

```text
.venv\Scripts\python.exe make_shorts.py retention "D:\ShortsMaker\output\channel\short-folder" "D:\screenshots\graph.png" codex-only
```

Providing both folder and screenshot on the command line skips the interactive details prompts; any details
already saved for that Short are still used. Use the normal `retention.bat` menu to add or update them.

Use the screenshot for the same video whose edit plan is in the selected folder. If the uploaded video was
recut, its timestamps may no longer match the saved edit plan.

The old performance baseline was archived on 2026-10-31 under `vault/Archive/Logbooks/` and removed from active
logbooks. Archived files are not read by the pipeline. Output videos and the list of already-covered topics
remain available. The separate, optional numbers log is `vault/Logbook/<channel>.md`; retention does not use it.
