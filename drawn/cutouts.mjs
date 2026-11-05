// cutouts.mjs — paints the 3D opener's cut-outs: node cutouts.mjs <job.json>
// job: {"out": "<folder>", "cutouts": [{"name": "amb", "w": 700, "h": 1100, "frames": 4, "module": "<path to .mjs>"}]}
// Each module exports default function draw(k, f): it draws drawing number f (0..frames-1) with the kit on a
// transparent w x h canvas, the thing standing on the bottom centre. Writes <out>/<name>_<f>.png.
// The 3D set lights and shadows them, so the kit's own ground shadow is switched off here, and so is the paper
// grain: in a 3D set the characters read clean and flat, like the "Second Draw" reference (owner, 2026-11-06).
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { createCanvas } from "./lib/core.mjs";
import { makeKit } from "./kit.mjs";

const flat = createCanvas(2, 2), fx = flat.getContext("2d");
fx.fillStyle = "#FFFFFF"; fx.fillRect(0, 0, 2, 2);  // multiplying white changes nothing: a grain-free wash
const FLAT = fx.createPattern(flat, "repeat");
const job = JSON.parse(fs.readFileSync(process.argv[2], "utf-8"));
fs.mkdirSync(job.out, { recursive: true });
for (const c of job.cutouts) {
  const draw = (await import(pathToFileURL(path.resolve(c.module)).href)).default;
  if (typeof draw !== "function") throw new Error(`cut-out ${c.name}: the module must export default function draw(k, f)`);
  for (let f = 0; f < c.frames; f++) {
    const cv = createCanvas(c.w, c.h), k = makeKit(cv.getContext("2d"), f / 7, []);
    k.shadow = () => {};
    k.pen.grain = FLAT;
    draw(k, f);
    fs.writeFileSync(path.join(job.out, `${c.name}_${f}.png`), cv.toBuffer("image/png"));
  }
}
console.log("painted", job.cutouts.length, "cut-outs");
