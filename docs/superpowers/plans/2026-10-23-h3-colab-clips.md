# MiniMax H3 on Colab (replaces Flow clips) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** The animate scenes' AI clips are made by the owner with MiniMax H3 in a Colab Pro notebook, from detailed, frame-checked prompts and a `veo.zip`/`clips.zip` hand-off.

**Architecture:** `gpu.veo_handoff()` keeps its pause. Before pausing it gets field-structured prompts from the AI
(retrying failing scenes until all pass, never the short prompt), writes `jobs.json`, `prompts.txt`, `veo.zip`
(with `colab/h3_run.py` inside). The notebook installs ComfyUI + H3 and runs `h3_run.py`, which builds ComfyUI API
graphs and saves `scene<N>.mp4`; the owner downloads `clips.zip` into `veo/`; Enter unpacks it into the existing
pickup.

**Tech Stack:** Python 3 stdlib (`zipfile`, `json`, `urllib`), Pillow, ComfyUI API on Colab, plain-assert test files.

**Spec:** `docs/superpowers/specs/2026-10-23-h3-colab-clips-design.md`

## Global Constraints

- No fallback to `motion_prompt()` for hand-off prompts (owner's rule); retry until every scene passes.
- Scripted runs never pause; LTX fallback and fix.bat's `clip<i>_veo.mp4` reuse unchanged.
- Colab Pro account is gutierrezdishann@gmail.com; other accounts are free-tier. Notebook + README say so.
- H3 output canvas 768x1344 (portrait), 24 fps, frames = `n + (5 - n % 17) % 17` with `n = max(5, round(s * 24))`.
- Weights from `Comfy-Org/MiniMax-H3` (not gated): `diffusion_models/minimax_h3_fl2va_pruned_bf16.safetensors`,
  `text_encoders/qwen3vl_32b_minimax_h3_int8_convrot.safetensors`, `vae/minimax_h3_video_vae_fp16.safetensors`,
  `vae/minimax_h3_audio_vae_fp32.safetensors`; turbo LoRA `lightx2v/Minimax-h3-Turbo`
  `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors`. No nvfp4/fp8.
- No real Colab run in this task. Tests: `.venv\Scripts\python.exe tests\<file>.py`, plain asserts, no AI usage.

## Review Focus

- AI reply missing a scene entirely (not just a short field) -> that scene is re-asked, not silently dropped.
- `clips.zip` containing folders (`clips/scene3.mp4`) or Windows-style names -> still found by basename.
- `clips.zip` with `../evil.mp4` or `scene1.mp4.exe` -> ignored, nothing written outside `veo/`.
- A CLOSE-UP scene in `marked` -> no job, no start picture (as today), and no prompt asked for it.
- Both AIs return None -> the batch waits for Enter and asks again instead of exiting or looping silently.

---

### Task 1: Prompt fields, checks and the retry loop (`gpu.py`)

**Files:**
- Modify: `shortsmaker/gpu.py` (next to `motion_prompt`, ~line 323)
- Test: `tests/test_h3_handoff.py` (new, same header/fake style as `tests/test_first_second.py`)

**Interfaces:**
- Produces: `h3_problems(entry: dict | None) -> list[str]`, `h3_prompt(sc: dict, entry: dict) -> str`,
  `h3_prompts(short: dict, folder: Path, scenes: list[int]) -> dict[int, str]` (scene index -> final prompt).

- [ ] **Step 1: Write failing tests**

```python
GOOD = {"subject": "A wooden tower with open pans stands on a hill under dark clouds, men in coats at its base",
        "motion": "White vapour rises slowly from the pans", "camera": "Locked-off, no camera movement",
        "look": "Black-and-white 1910s photograph, film grain, soft overcast light",
        "avoid": ["morphing faces", "extra fingers", "text", "colour", "camera shake"]}

def test_problems():
    assert h3_problems(GOOD) == []
    assert any("camera" in p for p in h3_problems({**GOOD, "camera": ""}))
    assert any("subject" in p for p in h3_problems({**GOOD, "subject": "a tower"}))   # < 40 chars
    assert any("avoid" in p for p in h3_problems({**GOOD, "avoid": ["text"]}))        # < 3 items
    assert h3_problems(None) == ["no entry for this scene"]

def test_prompt_joins_fields():
    p = h3_prompt({"motion_people": False}, GOOD)
    for part in (GOOD["subject"], GOOD["motion"], "Locked-off", "film grain", "first frame",
                 "stay completely still", "Avoid: morphing faces, extra fingers, text, colour, camera shake."):
        assert part in p

def test_retries_only_failing_scene_with_reason():
    asked = []
    replies = [{"scenes": [{"scene": 1, **GOOD}, {"scene": 3, **GOOD, "camera": ""}]},
               {"scenes": [{"scene": 3, **GOOD}]}]
    llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: (asked.append(prompt), replies.pop(0))[1]
    out = gpu.h3_prompts(short_with(4), folder, [0, 2])
    assert set(out) == {0, 2} and "no camera" in asked[1] and "SCENE 1" not in asked[1]
    assert all(gpu.motion_prompt(short_with(4)["scenes"][i]) not in out[i] for i in out)

def test_waits_for_enter_when_no_ai_answers():
    replies, waits = [None, {"scenes": [{"scene": 1, **GOOD}]}], []
    llm.ask_ai = lambda *a, **k: replies.pop(0)
    builtins.input = lambda msg="": waits.append(msg) or ""
    assert set(gpu.h3_prompts(short_with(2), folder, [0])) == {0} and len(waits) == 1
```
Also a test that a reply missing scene 3 entirely re-asks scene 3 (Review Focus 1).

- [ ] **Step 2: Run** `.venv\Scripts\python.exe tests\test_h3_handoff.py` — Expected: FAIL (`h3_problems` not defined).

- [ ] **Step 3: Implement in `shortsmaker/gpu.py`**

- `h3_problems`: messages exactly `"no entry for this scene"`, `"no <field> line"` for empty fields,
  `"<field> too short"` under minimums subject 40, motion 20, camera 10, look 15 chars; avoid needs >= 3 items.
- `h3_prompt`: `f"{subject}. {motion}. Camera: {camera}. Look: {look}. The video starts exactly on the given first
  frame and stays consistent with it. {people_rule} Vertical 9:16. No text, captions or watermarks. Avoid: {', '.join(avoid)}."`
  with `people_rule` = the same two sentences `motion_prompt` uses for `motion_people` (move them to a module
  constant both functions share). Strip trailing periods from fields before joining.
- `h3_prompts`: one `llm.ask_ai(prompt, fatal=False, read_dir=folder)` per round over the still-failing scenes. The
  prompt tells the AI to open `start<N>.jpg` for each listed SCENE N, gives the scene's narration and the picker's
  `motion` idea and `motion_people`, the rules (describe only what is in the frame; ONE main motion; locked-off or one
  slow camera move; look matches the photo; avoid list incl. colour when the photo is black-and-white), and on later
  rounds each scene's problems from `h3_problems`. Reply schema:
  `{"scenes": [{"scene": N, "subject", "motion", "camera", "look", "avoid": [..]}]}`.
  `None` reply -> `input("  >> Neither Claude nor Gemini answered (quota or network). Press Enter to try again. ")`.
  Loop until no scene fails; print `"  video prompts: round R, K scene(s) to fix"` per retry.

- [ ] **Step 4: Run tests** — Expected: all PASS.

- [ ] **Step 5: Commit** `feat: frame-checked H3/Veo prompts, retried until every scene passes`

### Task 2: `h3_run.py` (graph, frames, crop) for Colab

**Files:**
- Create: `colab/h3_run.py` (stdlib + Pillow only; runs on Colab next to `jobs.json`)
- Test: `tests/test_h3_run.py`

**Interfaces:**
- Produces: `frames(seconds: float) -> int`, `fit_start(src: Path, dst: Path) -> None` (centre-crop + resize to
  768x1344), `graph(prompt: str, image: str, length: int, seed: int, turbo: bool, prefix: str) -> dict`,
  `REQUIRED: tuple[str, ...]` (node classes), `main(only: list[int], seed: int, turbo: bool) -> None`.

- [ ] **Step 1: Write failing tests**

```python
def test_frames_snap_to_17k_plus_5():
    assert [h3_run.frames(s) for s in (0, 1, 2, 3.04, 8)] == [5, 39, 56, 73, 192]
    assert all(h3_run.frames(s) % 17 == 5 for s in (0.3, 4.7, 9.9))

def test_graph_wiring():
    g = h3_run.graph("p", "start1.jpg", 73, 7, turbo=True, prefix="h3/scene1")
    by = {n["class_type"]: n for n in g.values()}
    assert set(h3_run.REQUIRED) <= set(by)
    i2v = by["MiniMaxH3ImageToVideo"]["inputs"]
    assert (i2v["width"], i2v["height"], i2v["length"], i2v["prompt"]) == (768, 1344, 73, "p")
    assert by["BasicScheduler"]["inputs"]["steps"] == 8 and by["RandomNoise"]["inputs"]["noise_seed"] == 7
    plain = {n["class_type"]: n for n in h3_run.graph("p", "s", 73, 7, False, "x").values()}
    assert "LoraLoaderModelOnly" not in plain and plain["BasicScheduler"]["inputs"]["steps"] == 20
    assert plain["BasicScheduler"]["inputs"]["model"][0] == next(k for k, n in h3_run.graph("p", "s", 73, 7, False, "x").items()
                                                                  if n["class_type"] == "UNETLoader")

def test_fit_start_is_768x1344():
    # 1080x1920 image whose left half is red, right half blue -> 768x1344, centre column still split red/blue
    # (centre crop, not a stretch: the colour boundary stays at x=384 +/- 2)
```

- [ ] **Step 2: Run** `.venv\Scripts\python.exe tests\test_h3_run.py` — Expected: FAIL (no module).

- [ ] **Step 3: Implement `colab/h3_run.py`**

Graph (ComfyUI API format, string ids), mirroring the official template `video_minimax_h3_i2v.json`:
`UNETLoader(unet_name=pruned_bf16, weight_dtype="default")`; `CLIPLoader(clip_name=int8_convrot, type="minimax",
device="default")`; `VAELoader` video fp16 and audio fp32; `LoadImage(image)`; `MiniMaxH3ImageToVideo(clip, vae,
first_frame, prompt, width=768, height=1344, length)`; turbo only: `LoraLoaderModelOnly(model, lora_name,
strength_model=1.0)`; `BasicScheduler(model, scheduler="simple", steps=8 if turbo else 20, denoise=1.0)`;
`KSamplerSelect(sampler_name="res_multistep")`; `RandomNoise(noise_seed)`; `BasicGuider(model,
conditioning=i2v[0])`; `SamplerCustomAdvanced(noise, guider, sampler, sigmas, latent_image=i2v[1])`;
`VAEDecode(samples, vae)`; `VAEDecodeAudio(samples, audio_vae)`; `CreateVideo(images, audio, fps=24)`;
`SaveVideo(video, filename_prefix=prefix, format="auto", codec="auto")`.
`main`: read `jobs.json`; GET `http://127.0.0.1:8188/object_info`, stop with `"ComfyUI is missing node X: run the
setup cell again (it updates ComfyUI)"` if any `REQUIRED` is absent; for each job (filtered by `only` scene numbers):
`fit_start` into `/content/ComfyUI/input/`, POST `/prompt`, poll `/history/<id>` every 5 s, copy the saved file to
`clips/scene<N>.mp4`, print scene, frames, minutes taken; on a ComfyUI error print it and continue with the next job.
Finally write `clips.zip` of `clips/`.

- [ ] **Step 4: Run tests** — Expected: PASS.

- [ ] **Step 5: Commit** `feat: h3_run.py builds the MiniMax H3 image-to-video graph for Colab`

### Task 3: Hand-off files and `clips.zip` pickup (`veo_handoff`)

**Files:**
- Modify: `shortsmaker/gpu.py:331-368` (`veo_handoff`), `shortsmaker/cli.py:36` (question text)
- Test: `tests/test_h3_handoff.py`

**Interfaces:**
- Consumes: `h3_prompts` (Task 1); `colab/h3_run.py` file (Task 2).
- Produces: `unpack_clips(folder: Path) -> list[str]` (names written); `veo_handoff` signature unchanged.

- [ ] **Step 1: Write failing tests**

- `test_handoff_writes_jobs_and_zip`: stub `h3_prompts`, `cover_crop`, `os.startfile`, `input`, two marked
  scenes + one CLOSE-UP. Assert `jobs.json` == `[{"scene": 1, "image": "start1.jpg", "prompt": ..., "seconds":
  round(bounds[1]-bounds[0]+XFADE, 2), "out": "scene1.mp4"}, ...]` (no CLOSE-UP entry, ascending), `veo.zip` names
  == `{"jobs.json", "start1.jpg", "start3.jpg", "h3_run.py"}`, `prompts.txt` contains "Colab" and "Google Flow"
  and each prompt.
- `test_unpack_clips`: zip with `clips/scene3.mp4`, `scene1.MP4`, `../evil.mp4`, `scene1.mp4.exe`, `notes.txt` ->
  returns `["scene1.MP4", "scene3.mp4"]`, only those exist in `veo/`, nothing outside it.
- `test_handoff_picks_up_clips_zip`: the stubbed `input` drops a `clips.zip` with `scene1.mp4`; fake
  `media_tools.ffmpeg` -> result `{0: work/"clip0_veo.mp4"}`.

- [ ] **Step 2: Run** — Expected: FAIL.

- [ ] **Step 3: Implement**

- `veo_handoff`: build the non-CLOSE-UP list first, crop its start pictures, call `h3_prompts` for those, then write
  `jobs.json`, `veo.zip` (`zipfile.ZIP_DEFLATED`, includes `ROOT / "colab" / "h3_run.py"`), `prompts.txt`. Notes
  text: Colab steps first ("Open colab/h3_clips.ipynb in Colab with gutierrezdishann@gmail.com (Pro), A100, run the
  cells, upload veo.zip when asked, download clips.zip into this folder"), then the existing Flow lines; each scene
  lists `Start picture`, `Save as`, seconds and the full prompt. After `input`, call `unpack_clips(folder)`, then the
  existing pickup loop unchanged. Update the docstring and the printed line ("AI clip(s) to make in Colab (H3) or
  Google Flow").
- `unpack_clips`: for each zip member take `PurePosixPath(name.replace("\\", "/")).name`; keep only
  `re.fullmatch(r"scene\d+\.(mp4|mov|webm)", base, re.I)`; write to `folder / base`. Missing zip -> `[]`;
  bad zip -> print `"    clips.zip couldn't be opened, using the loose scene files"` and return `[]`.
- `cli.py`: question -> `"Make the AI video clips yourself (Colab H3 or Google Flow)? The batch pauses at each Short until you've saved them"`.

- [ ] **Step 4: Run** both test files and `tests\test_package.py` — Expected: all PASS.

- [ ] **Step 5: Commit** `feat: veo.zip/jobs.json hand-off for Colab H3, clips.zip picked up on Enter`

### Task 4: Notebook, first-time guide, HANDOFF

**Files:**
- Create: `colab/h3_clips.ipynb`, `colab/README.md`
- Modify: `HANDOFF.md` (rows for `run.bat` question, `veo/` contents, `gpu.py`, new `colab/` row, tests list)
- Test: `tests/test_h3_run.py` (notebook check)

- [ ] **Step 1: Failing test** `test_notebook_cells`: `json.load` the ipynb; nbformat 4; code cells in order contain
  `"gutierrezdishann@gmail.com"` (markdown 1), `"Comfy-Org/MiniMax-H3"` and every Global-Constraints weight file
  name, `"main.py"` + `"8188"`, `"files.upload"`, `"h3_run.main("`, `"files.download('clips.zip')"`.

- [ ] **Step 2: Run** — Expected: FAIL (no notebook).

- [ ] **Step 3: Write the notebook** (nbformat 4, `accelerator: GPU`), cells:
  1. Markdown: what it is; use the Pro account; Runtime > Change runtime type > A100 + High-RAM; run top to bottom;
     first run downloads ~70 GB (several minutes), again in each new session.
  2. Setup: `nvidia-smi` check that warns if the GPU isn't an A100; clone/`git pull` ComfyUI into `/content/ComfyUI`,
     `pip install -r requirements.txt`; `huggingface_hub.hf_hub_download` each weight (with `HF_HUB_ENABLE_HF_TRANSFER=1`
     + `hf_transfer` installed) into the right `models/` subfolder, skipping files already present.
  3. Start ComfyUI headless (`subprocess.Popen([... "main.py", "--listen", "127.0.0.1", "--port", "8188"])`, log to
     file), poll until `/object_info` answers (timeout 10 min, print the log tail on failure).
  4. Settings + upload: `ONLY = []`, `SEED = 1`, `TURBO = True` with one comment line each; `files.upload()` the
     `veo.zip`, unzip into `/content/job`.
  5. `sys.path` -> `/content/job`; `import h3_run; h3_run.main(ONLY, SEED, TURBO)`.
  6. `files.download('clips.zip')`.
  `colab/README.md`: the same first-time steps in plain words, plus "if a cell fails, copy its error to Claude".

- [ ] **Step 4: Run** all tests — Expected: PASS.

- [ ] **Step 5: Commit** `feat: Colab notebook and guide for MiniMax H3 clips; HANDOFF`
