// partsheet.mjs — a made part's preview for the opener crew's part checker: node partsheet.mjs <job.json>
// job: {"kind": "hat" | "thing", "name": "pickelhaube", "module": "<path to the candidate .mjs>", "out": "<png path>"}
// Draws the candidate (not yet in drawn/parts) big on its own and in use: a hat on two people of different sizes,
// a thing standing on a table and held in a hand. Clean flat paper, no grain, like the 3D cut-outs.
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { createCanvas } from "./lib/core.mjs";
import { makeKit, MADE } from "./kit.mjs";

const job = JSON.parse(fs.readFileSync(process.argv[2], "utf-8"));
const m = await import(pathToFileURL(path.resolve(job.module)).href);
if (typeof m.default !== "function") throw new Error("the part must export default function draw(...)");
MADE[job.kind][job.name] = { draw: m.default, grip: Array.isArray(m.grip) ? m.grip : [0, -40] };
const W = 1440, H = 720, cv = createCanvas(W, H), ctx = cv.getContext("2d"), k = makeKit(ctx, 0, []);
ctx.fillStyle = "#F3EBDA"; ctx.fillRect(0, 0, W, H);
k.shadow = () => {};
if (job.kind === "hat") {
  k.person(260, 700, 2.0, { hat: job.name, coat: k.C.navy, skin: k.SKIN[1], still: true, arms: [12, 12], bend: [6, 6] });
  k.person(720, 690, 1.6, { hat: job.name, coat: k.C.red, skin: k.SKIN[3], still: true, arms: [35, 12], bend: [-75, 6] });
  k.person(1140, 690, 1.6, { hat: job.name, coat: "#5E7A5A", skin: k.SKIN[0], still: true, flip: true, arms: [12, 35], bend: [6, -75] });
} else {
  k.thing(job.name, 300, 600, 3);
  const tb = k.table(800, 690, 360); k.thing(job.name, 800, tb.top, 1.4);
  k.person(1180, 690, 2.2, { hold: [null, job.name], coat: k.C.navy, skin: k.SKIN[1], still: true, arms: [12, 40], bend: [6, 70] });
}
fs.writeFileSync(job.out, cv.toBuffer("image/png"));
console.log("wrote", job.out);
