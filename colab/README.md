# Making AI clips with MiniMax H3 on Colab

This replaces making the clips in Google Flow. You don't install anything on this PC; the notebook installs H3 on
Colab every session.

## Each Short

1. Run ShortsMaker with "Make the AI video clips yourself" answered **y**. When it pauses, the Short's `veo` folder
   opens. It holds `veo.zip` (start pictures, prompts and the job script) and `prompts.txt`.
2. Go to colab.research.google.com **signed in as gutierrezdishann@gmail.com** (the Pro account; other accounts only
   get free GPUs, too small for H3). File > Upload notebook > `D:\ShortsMaker\colab\h3_clips.ipynb`.
3. Runtime > Change runtime type > **A100 GPU**, **High-RAM** on > Save. (Colab usually gives an 80 GB A100; if it
   ever gives a 40 GB card, Cell 1 warns you: it still works, but runs slower as weights swap with RAM).
4. Run the cells top to bottom:
   - Cell 1 installs ComfyUI and downloads H3 (~70 GB, several minutes; skipped if this session already has it).
   - Cell 2 starts ComfyUI.
   - Cell 3: pick `veo.zip` when it asks (if you cancel, just run the cell again).
   - Cell 4 makes the clips, a few minutes each. Its first lines are the settings: `ONLY` (e.g. `[1]` to make just
     the hook first), `SEED`, `TURBO`.
   - Cell 5 downloads `clips.zip`.
5. Save `clips.zip` (even if your browser names it `clips (1).zip`) into that same `veo` folder and press Enter in
   ShortsMaker's black window. Scenes you skipped are made on this PC as before.

For another Short in the same Colab session, run cells 3, 4 and 5 again.

## Prompting guide for great AI clips

1. **Water, waves, and smoke need a locked-off camera:**
   - Never combine camera panning with moving water, waves, or smoke. Camera panning forces the model to slide the whole 2D photo across the canvas, which completely freezes the water and smoke into a static picture.
   - Use `Camera: Locked-off / static camera, no camera movement.` This forces the AI to spend its entire motion budget simulating genuine fluid dynamics.
2. **Use dynamic physical action words, not "gentle":**
   - AI video models interpret "gentle ripples" or "stationary" as "barely change any pixels", resulting in frozen images.
   - Use active motion verbs: *"rolling ocean swells, crashing white foam, churning wake, water splashing against the hull"* or *"thick dark smoke billowing rapidly from the funnel"*.
3. **Never animate multiple posing faces in archival group photos:**
   - Asking multiple people in a formal studio portrait to "shift posture subtly" causes the uncanny valley: eyes melt, teeth distort, and faces look like rubbery wax.
   - For group portraits, keep people still and use a slow cinematic push-in (or skip the AI clip in ShortsMaker so it uses the original crisp high-res still with camera zoom).
4. **Don't list every clothing item or accessory:**
   - Image-to-video models already see the first frame. An exhaustive inventory of hats, coats, beards, and ties forces the model to redraw them every frame. Keep `subject` to one concise sentence.
5. **Turn off Turbo for complex fluid physics or delicate faces:**
   - In Cell 4, set `TURBO = False` (full 20 steps). 8-step Turbo is fast, but 20 steps provides the sampling depth needed for realistic water physics and sharp facial details.

## Saving compute units

- `TURBO = True` (default) uses 8 steps instead of 20: cheaper and faster, slightly less detail.
- `ONLY = [1]` in cell 4 makes just the hook; check it, then set `ONLY` to the other scenes and run cell 4 again
  (don't re-run cell 3: a new upload starts the Short over). clips.zip keeps every clip made so far.
- Clips are only as long as the Short uses them.
- When you're done, Runtime > Disconnect and delete runtime, so the A100 stops using units.

If a cell shows an error, copy the red text to Claude.
