// cutouts.mjs — paints the 3D opener's cut-outs: node cutouts.mjs <job.json>
// job: {"out": "<folder>", "cutouts": [{"name": "amb", "w": 700, "h": 1100, "frames": 4, "fps": 7, "module": "<path to .mjs>"}]}
// Each module exports default function draw(k, f, u): it draws the moment u (0..1 through one cycle of `frames`
// drawings; f = Math.floor(u * frames)) with the kit on a transparent w x h canvas, the thing standing on the bottom
// centre. A cycle is painted as `steps` (12+) drawings so limbs move smoothly (2026-11-06: 4 drawings at 7 fps read
// as jerky); code that only uses f still works, each drawing just repeats. Writes <out>/<name>_<step>.png and
// <out>/sizes.json = {name: {wide, tall, steps}}.
// The canvas is painted with room to spare (PAD_X each side, PAD_TOP above) and cropped to what was drawn, the same
// distance either side of the centre line and the bottom where it was, so feet, spot and knock contact don't move:
// a fixed w x h canvas cut off a waving arm at its widest (owner, 2026-11-06: "like there's an invisible wall").
// `wide`/`tall` = the cropped board / the painter's w x h.
// The 3D set lights and shadows them, so the kit's own ground shadow is switched off here, and so is the paper
// grain: in a 3D set the characters read clean and flat, like the "Second Draw" reference (owner, 2026-11-06).
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { createCanvas } from "./lib/core.mjs";
import { makeKit } from "./kit.mjs";

export const PAD_X = .5, PAD_TOP = .4, STEPS = 12, EDGE = 6;  // EDGE: px of clear margin kept round the drawing

const flat = createCanvas(2, 2), fx = flat.getContext("2d");
fx.fillStyle = "#FFFFFF"; fx.fillRect(0, 0, 2, 2);  // multiplying white changes nothing: a grain-free wash
const FLAT = fx.createPattern(flat, "repeat");

/** The opaque bounds [minX, minY, maxX, maxY] of a canvas, or null when nothing was drawn. */
function bounds(cv) {
  const { width: w, height: h } = cv, d = cv.getContext("2d").getImageData(0, 0, w, h).data;
  let x0 = w, y0 = h, x1 = -1, y1 = -1;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (d[(y * w + x) * 4 + 3] > 8) {
    if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
  }
  return x1 < 0 ? null : [x0, y0, x1, y1];
}

export async function paintAll(job) {
  fs.mkdirSync(job.out, { recursive: true });
  const sizes = {};
  for (const c of job.cutouts) {
    const draw = (await import(pathToFileURL(path.resolve(c.module)).href)).default;
    if (typeof draw !== "function") throw new Error(`cut-out ${c.name}: the module must export default function draw(k, f, u)`);
    const px = Math.round(c.w * PAD_X), pt = Math.round(c.h * PAD_TOP), W = c.w + 2 * px, H = c.h + pt;
    const steps = c.frames > 1 ? Math.max(STEPS, c.frames) : 1, cycle = c.frames / (c.fps || 7);
    const drawn = [], hands = [];
    let box = null;
    for (let j = 0; j < steps; j++) {
      const u = j / steps, f = Math.floor(u * c.frames);
      const cv = createCanvas(W, H), ctx = cv.getContext("2d");
      ctx.translate(px, pt);  // the painter's own coordinates: (0, 0) is still its canvas's top left
      const k = makeKit(ctx, u * cycle, []);
      k.shadow = () => {};
      k.pen.grain = FLAT;
      // the person's hands in this drawing (the outermost k.person call: a dance calls it again inside), for a 3D
      // object held in the hand (owner, 2026-11-06: objects are 3D)
      const person = k.person;
      let depth = 0, hand = null;
      k.person = (...a) => { depth++; const r = person(...a); depth--; if (!depth && !hand && r && r.hands) hand = r.hands; return r; };
      draw(k, f, u);
      hands.push(hand);
      drawn.push(cv);
      const b = bounds(cv);
      if (b) box = box ? [Math.min(box[0], b[0]), Math.min(box[1], b[1]), Math.max(box[2], b[2]), Math.max(box[3], b[3])] : b;
    }
    const mid = px + c.w / 2, bottom = pt + c.h;  // crop round the centre line, down to the painter's own bottom
    const half = box ? Math.ceil(Math.max(mid - box[0], box[2] + 1 - mid) + EDGE) : c.w / 2;
    const top = box ? Math.max(0, box[1] - EDGE) : pt;
    const cw = Math.max(2, Math.round(2 * half)), ch = Math.max(2, Math.round(bottom - top));
    drawn.forEach((cv, j) => {
      const out = createCanvas(cw, ch);
      out.getContext("2d").drawImage(cv, Math.round(mid - half), top, cw, ch, 0, 0, cw, ch);
      fs.writeFileSync(path.join(job.out, `${c.name}_${j}.png`), out.toBuffer("image/png"));
    });
    sizes[c.name] = { wide: +(cw / c.w).toFixed(4), tall: +(ch / c.h).toFixed(4), steps };
    if (hands.every(Boolean))  // on the cropped board: 0..1 across from its left edge, 0..1 up from its bottom
      sizes[c.name].hands = hands.map((hs) => hs.map(([hx, hy]) => [+((hx + px - (mid - half)) / cw).toFixed(4), +((bottom - (hy + pt)) / ch).toFixed(4)]));
  }
  fs.writeFileSync(path.join(job.out, "sizes.json"), JSON.stringify(sizes));
  return sizes;
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  await paintAll(JSON.parse(fs.readFileSync(process.argv[2], "utf-8")));
  console.log("painted cut-outs");
}
