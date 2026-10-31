# Read a Short's retention graph

Run `retention.bat`, select the finished Short, then drag a PNG/JPG/WebP screenshot of its YouTube Studio
retention graph into the window and press Enter. Include the curve and the full time axis in the screenshot.
Choose the AI mode to use for this review. Existing subscription models and quota fallback apply.

The report is saved in that Short's output folder:

- `retention.txt`: up to three visible drops, matched to the edit plan's scenes, plus limitations.
- `retention/graph.png` (or the screenshot's other supported extension): the screenshot used for the report.

Timings are approximate, normally within 1–2 seconds. The report does not infer exact retention percentages
or establish why viewers left. If the graph cannot be read, it records that rather than guessing timings.
An unusable AI reply leaves any previous report intact.

The last section suggests a short line you may paste into the logbook's existing **My notes** field.
The command does not edit the logbook automatically. Part 3.2 will add automatic use of the reports in future
planning; this command only creates the reports.

For command-line use:

```text
.venv\Scripts\python.exe make_shorts.py retention "D:\ShortsMaker\output\channel\short-folder" "D:\screenshots\graph.png" codex-only
```

Use the screenshot for the same video whose edit plan is in the selected folder. If the uploaded video was
recut, its timestamps may no longer match the saved edit plan.

The old performance baseline was archived on 2026-10-31 under `vault/Archive/Logbooks/` and removed from active
logbooks. Archived files are not read by the pipeline. Output videos and the list of already-covered topics
remain available. Record new results in `vault/Logbook/<channel>.md`.
