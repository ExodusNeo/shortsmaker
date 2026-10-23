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

## Saving compute units

- `TURBO = True` (default) uses 8 steps instead of 20: cheaper and faster, slightly less detail.
- `ONLY = [1]` in cell 4 makes just the hook; check it, then set `ONLY` to the other scenes and run cell 4 again
  (don't re-run cell 3: a new upload starts the Short over). clips.zip keeps every clip made so far.
- Clips are only as long as the Short uses them.
- When you're done, Runtime > Disconnect and delete runtime, so the A100 stops using units.

If a cell shows an error, copy the red text to Claude.
