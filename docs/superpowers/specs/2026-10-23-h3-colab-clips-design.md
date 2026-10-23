# MiniMax H3 on Colab replaces Google Flow for AI clips (design)

Date: 2026-10-23. Owner approved option 1 (frame-aware prompt writer) and hand upload/download in chat.

## Goal

The owner makes the `animate` scenes' AI clips with MiniMax H3 (image-to-video) in a Colab Pro notebook on an
A100 80 GB instead of in Google Flow. Every generation costs compute units, so prompts must be detailed and match
the exact start frame, and clips must be only as long as the scene uses.

Out of scope: running H3 from the batch without a pause (tunnels), Drive sync, automating the notebook from the
pipeline, any change to LTX or to how clips are cut into the Short.

## Constraints

- The pause in `veo_handoff()` stays: the owner runs the notebook, then presses Enter. Scripted runs never pause.
- Fallbacks unchanged: a scene without `scene<N>.mp4` gets LTX; fix.bat reuses `clip<i>_veo.mp4`.
- `prompts.txt` keeps working for Flow (same names, same folder), now with the detailed prompts.
- The Colab account with Pro is gutierrezdishann@gmail.com; other Google accounts only get free-tier GPUs. The
  notebook says so in its first cell.
- No real Colab run in this task (owner: "don't test for now"). Local unit tests only.

## A. Prompt writer (`gpu.py`)

`h3_prompts(short, folder, jobs)` makes one AI call per Short (`llm.ask_ai(..., fatal=False, read_dir=folder)`,
current brain) after the start pictures are cropped. The AI opens each `start<N>.jpg`, reads the scene's narration
and the picker's `motion` idea, and replies JSON per scene:

- `prompt`: subject and setting as seen in the frame; ONE main motion; camera (locked-off or one slow move);
  look matching the photo (black-and-white archival, grain, period light); "continues exactly from the first frame".
  `motion_people` rules carry over (false = people, animals, machines stay still).
- `negative`: morphing faces, extra limbs or fingers, text/captions/watermarks, modern objects, camera shake,
  colour if the photo is black-and-white.

Any scene the reply misses or garbles falls back to `motion_prompt(sc)` with a default negative. A failed call never
stops the run.

## B. Hand-off folder (`<Short>/veo/`)

- `start<N>.jpg` (as today).
- `jobs.json`: `[{"scene": N, "image": "start<N>.jpg", "prompt", "negative", "seconds", "out": "scene<N>.mp4"}]`,
  hook first. `seconds` = the span the Short uses + `XFADE`.
- `veo.zip`: `jobs.json` + the start pictures, for uploading to Colab.
- `prompts.txt`: Colab steps first, then the Flow steps, each scene's prompt and "avoid" line.
- On Enter, a `clips.zip` in `veo/` is unpacked there (only `scene*.mp4|mov|webm`, no paths outside the folder),
  then the existing `scene<N>.*` pickup runs unchanged.
- run.bat question becomes "Make the AI clips yourself (Colab H3 or Google Flow)?"; profile key stays `veo`.

## C. Notebook (`colab/h3_clips.ipynb`)

1. Notes: Pro account, choose A100 + High-RAM.
2. Install ComfyUI and download the int8 H3 transformer + text encoder + VAE to local scratch (skipped when present).
   No nvfp4/fp8 builds (A100 has no hardware support).
3. Start ComfyUI headless; wait until its API answers.
4. Upload `veo.zip`; unzip.
5. For each job (or only scenes listed in `ONLY = []`): ComfyUI API graph with `MiniMaxH3ImageToVideo`,
   `first_frame` = start picture, 768x1344, frames from `seconds` snapped up to H3's frame grid at 24 fps, fixed
   `SEED`; save `scene<N>.mp4`. Print each clip's time.
6. Zip the clips into `clips.zip` and download it.

Exact node names, weight file names and the frame grid are checked against docs.comfy.org while building; anything
unverifiable is marked in the notebook as a CHECK line rather than guessed silently.

## D. Testing

- `h3_prompts`: stubbed `ask_ai` returning good JSON, partial JSON, and None -> every scene gets a prompt and negative.
- `veo_handoff` with stubbed AI + `input`: `jobs.json` fields, hook first, `veo.zip` contents.
- `clips.zip` unpack: picks scene clips, ignores other files and `../` paths, then pickup returns them.
- Notebook: JSON valid, cells in order. No Colab run.
