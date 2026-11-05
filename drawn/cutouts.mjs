// cutouts.mjs — paints the 3D opener's cut-outs: node cutouts.mjs <job.json>
// job: {"out": "<folder>", "cutouts": [{"name": "amb", "w": 700, "h": 1100, "frames": 4, "module": "<path to .mjs>"}]}
// Each module exports default function draw(k, f): it draws drawing number f (0..frames-1) with the kit on a
// transparent w x h canvas, the thing standing on the bottom centre. Writes <out>/<name>_<f>.png.
// The 3D set lights and shadows them, so the kit's own ground shadow is switched off here.
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { createCanvas } from "./lib/core.mjs";
import { makeKit } from "./kit.mjs";

const job = JSON.parse(fs.readFileSync(process.argv[2], "utf-8"));
fs.mkdirSync(job.out, { recursive: true });
for (const c of job.cutouts) {
  const draw = (await import(pathToFileURL(path.resolve(c.module)).href)).default;
  if (typeof draw !== "function") throw new Error(`cut-out ${c.name}: the module must export default function draw(k, f)`);
  for (let f = 0; f < c.frames; f++) {
    const cv = createCanvas(c.w, c.h), k = makeKit(cv.getContext("2d"), f / 7, []);
    k.shadow = () => {};
    draw(k, f);
    fs.writeFileSync(path.join(job.out, `${c.name}_${f}.png`), cv.toBuffer("image/png"));
  }
}
console.log("painted", job.cutouts.length, "cut-outs");
