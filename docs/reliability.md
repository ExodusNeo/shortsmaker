# Resume a run or repair a callout

## Interrupted runs

If a new batch is interrupted, run `run.bat` again and choose **Resume unfinished Shorts**. You can also
use `resume.bat`, or `make_shorts.py resume "D:\ShortsMaker\output\channel\short-folder"` for one Short.

Completed scripts are queued before SEO/rendering. Progress is saved after picture selection, narration
generation and video encoding. A failed Short keeps its folder; the batch can continue with the others.
An interrupted video encode writes to a temporary video and keeps the last successful `short.mp4` intact.
Once encoding is committed, resume can finish the reports and reviews without re-encoding the video.
Finalization checks the output-folder entry so it does not add duplicate logbook rows.

Saved narration is reused when its text, voice settings and reference sample match. Changes to a visual
callout do not require another voice job. Changed narration or voice settings invalidate the voice cache;
missing or altered cached audio is regenerated. Unfinished checkpoints are excluded from the normal
seven-day work-file cleanup. Complete Shorts still follow that cleanup policy.

Checkpoints apply to new batches made with this version. An interruption inside an unfinished planning
call can still require that call again. Pictures and clips whose stages did not finish may be rebuilt.

## Review status

`edit_plan.txt` distinguishes **Passed**, **Problems found**, and **Not reviewed** for the visual and opening
AI reviews. A failed preview, absent reply or malformed verdict produces a `NOT REVIEWED` check. It is not
a clean pass, and it does not request an automatic image repaint without an actual defect finding.

## Circle and arrow repairs

Run `fix.bat`, select the Short and scene, then choose:

- **6:** adjust a circle/arrow position (percent from the left/top) and its label.
- **3:** remove the callout.

For a circle/arrow card on a still with hard cuts on both sides, the program renders that scene and saves
`work/repairs/<timestamp>/preview.mp4` plus `sheet.jpg`. Open the preview, then answer the apply question.
Declining leaves the original Short untouched. Applying keeps the original audio, captions and duration,
and backs up the video, saved state and reports next to the preview. It updates `short.mp4`, the storyboard
and the callout entry in the edit plan. The old Shotcut timeline is archived because its layers would be stale.

The fast repair changes the upper card area while preserving the original captions below. Overlapping
transitions, clips and other full-screen graphics use the ordinary repair path, with cached narration
where available. A manual repair marks the visual review as **Not reviewed** until you inspect/review it.

## Failed picture downloads

Non-Wikimedia picture downloads get at most two attempts. Wikimedia keeps its existing bounded retry and
Retry-After handling. If a selected background still fails, one selection task can choose an unused,
previously reviewed, era-appropriate alternative from the picture pool. Failed URLs are excluded from
that recovery selection. Credits are retained, and motion written for the old picture is disabled.
If no suitable alternative downloads, the existing graphic/painting/reuse fallbacks still apply.
