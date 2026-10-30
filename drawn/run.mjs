// run.mjs — renders one drawn opener: node run.mjs <job.json>
// job: {"scene": "<path to the scene .mjs>", "seconds": 3.5, "words": [[start, end, "word"], ...],
//       "mode": "sheet" | "render", "times": [0, 1.2, ...] (sheet only), "out": "<folder>", "name": "opener"}
// The scene module exports default function scene(k, t) and optionally `camera` = {zoom: [from, to], focus: [x, y]}.
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { fibrePaper, filmFinish } from "./lib/textures.mjs";
import { run, exposure } from "./lib/film.mjs";
import { makeKit, W, H } from "./kit.mjs";

const job = JSON.parse(fs.readFileSync(process.argv[2], "utf-8"));
const mod = await import(pathToFileURL(path.resolve(job.scene)).href);
const scene = mod.default, cam = { zoom: [1, 1.06], focus: [540, 1000], ...(mod.camera || {}) };
if (typeof scene !== "function") throw new Error("the scene module must export default function scene(k, t)");
const FPS = 30, DUR = job.seconds;
process.argv = [process.argv[0], process.argv[1], job.mode, (job.times || []).join(",")];   // film.mjs reads its mode here

await run({
  name: job.name || "opener", W, H, fps: FPS, dur: DUR, out: job.out, sheetScale: job.scale || .25,
  setup() { return { paper: fibrePaper(W, H), finish: filmFinish(W, H, { grain: .1, vignette: .2 }) }; },
  frame(ctx, t, i, S) {
    ctx.drawImage(S.paper, 0, 0);
    const z = cam.zoom[0] + (cam.zoom[1] - cam.zoom[0]) * (1 - Math.pow(1 - Math.min(1, t / DUR), 3));   // camera on ones
    ctx.save(); ctx.translate(cam.focus[0], cam.focus[1]); ctx.scale(z, z); ctx.translate(-cam.focus[0], -cam.focus[1]);
    scene(makeKit(ctx, exposure(t, [{ at: 0, on: 2 }], FPS), job.words || []), exposure(t, [{ at: 0, on: 2 }], FPS));   // drawings on twos
    ctx.restore();
    S.finish(ctx, i);
  },
});
