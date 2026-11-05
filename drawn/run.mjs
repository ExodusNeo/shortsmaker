// run.mjs — renders one drawn opener: node run.mjs <job.json>
// job: {"scene": "<path to the scene .mjs>", "seconds": 3.5, "words": [[start, end, "word"], ...],
//       "mode": "sheet" | "render", "times": [0, 1.2, ...] (sheet only), "out": "<folder>", "name": "opener"}
// The scene module exports default function scene(k, t) and optionally:
//   camera = (k) => [{at, zoom, focus: [x, y], move: "cut" | "whip" | "push"}, ...]   shots (KIT.md, Camera)
//            or the old {zoom: [from, to], focus: [x, y]} slow push
//   light  = {mood: "day" | "golden" | "dusk" | "night" | "interior", from: [x, y]}  the frame's light
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { fibrePaper, filmFinish } from "./lib/textures.mjs";
import { run, exposure } from "./lib/film.mjs";
import { clamp, lerp, createCanvas } from "./lib/core.mjs";
import { makeKit, lightOf, MOODS, W, H } from "./kit.mjs";

const job = JSON.parse(fs.readFileSync(process.argv[2], "utf-8"));
const mod = await import(pathToFileURL(path.resolve(job.scene)).href);
const scene = mod.default;
if (typeof scene !== "function") throw new Error("the scene module must export default function scene(k, t)");
const FPS = 30, DUR = job.seconds, WHIP = .28, DRIFT = .035, light = lightOf(mod.light);
process.argv = [process.argv[0], process.argv[1], job.mode, (job.times || []).join(",")];   // film.mjs reads its mode here

// Camera shots. The camera never stops (owner, 2026-11-05: the "Second Draw" Short): each shot creeps in by DRIFT a
// second; a whip is a fast eased move with motion blur, a push a slow move until the next shot, a cut is instant.
const shots = (() => {
  if (typeof mod.camera !== "function") {
    const c = { zoom: [1, 1.06], focus: [540, 1000], ...(mod.camera || {}) };
    return [{ at: 0, zoom: c.zoom[0], focus: c.focus, end: c.zoom[1] }];
  }
  const list = mod.camera(makeKit(createCanvas(4, 4).getContext("2d"), 0, job.words || [], light));   // k.word for shot times
  if (!Array.isArray(list) || !list.length) throw new Error("camera(k) must return a list of shots");
  return list.map((s) => ({ at: clamp(+s.at || 0, 0, DUR), zoom: clamp(+s.zoom || 1, 1, 2.6),
    focus: [clamp(+(s.focus || [])[0] || 540, 0, W), clamp(+(s.focus || [])[1] || 1000, 0, H)], move: s.move || "cut" }))
    .sort((a, b) => a.at - b.at).map((s, i) => (i ? s : { ...s, at: 0 }));
})();
const held = (s, t) => s.end != null   // the old camera: an eased push from zoom to end over the whole opener
  ? { z: s.zoom + (s.end - s.zoom) * (1 - Math.pow(1 - Math.min(1, t / DUR), 3)), x: s.focus[0], y: s.focus[1] }
  : { z: s.zoom * (1 + DRIFT * (t - s.at)), x: s.focus[0], y: s.focus[1] };
function frameAt(t) {
  let i = 0; while (i + 1 < shots.length && t >= shots[i + 1].at) i++;
  const s = shots[i], to = held(s, t);
  if (!i || s.move === "cut") return { ...to, moving: false };
  const from = held(shots[i - 1], s.at), dur = s.move === "push" ? Math.max(.3, (shots[i + 1]?.at ?? DUR) - s.at) : WHIP;
  const u = clamp((t - s.at) / dur), e = u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
  return { z: lerp(from.z, to.z, e), x: lerp(from.x, to.x, e), y: lerp(from.y, to.y, e), moving: s.move === "whip" && u < 1 };
}

// One light mood over the whole frame: the side away from the light falls into shade, the light side glows.
function grade(ctx) {
  const m = MOODS[light.mood], [lx, ly] = light.from;
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  const sh = ctx.createLinearGradient(lx, ly, W - lx, H - ly + H * .4);
  sh.addColorStop(0, "rgba(0,0,0,0)"); sh.addColorStop(1, m.shade);
  ctx.globalCompositeOperation = "multiply"; ctx.globalAlpha = m.shadeA; ctx.fillStyle = sh; ctx.fillRect(0, 0, W, H);
  const key = ctx.createRadialGradient(lx, ly, 0, lx, ly, 1250);
  key.addColorStop(0, m.key); key.addColorStop(1, "rgba(0,0,0,0)");
  ctx.globalCompositeOperation = "screen"; ctx.globalAlpha = m.keyA; ctx.fillStyle = key; ctx.fillRect(0, 0, W, H);
  ctx.restore();
}

await run({
  name: job.name || "opener", W, H, fps: FPS, dur: DUR, out: job.out, sheetScale: job.scale || .25,
  blur: (t) => (frameAt(t).moving ? 10 : 1),   // motion blur only during a whip (fewer samples showed copies)
  setup() { return { paper: fibrePaper(W, H), finish: filmFinish(W, H, { grain: .08, vignette: .32 }) }; },
  frame(ctx, t, i, S) {
    ctx.drawImage(S.paper, 0, 0);
    const f = frameAt(t);   // camera on ones
    ctx.save(); ctx.translate(f.x, f.y); ctx.scale(f.z, f.z); ctx.translate(-f.x, -f.y);
    const dt = exposure(t, [{ at: 0, on: 2 }], FPS);   // drawings on twos
    scene(makeKit(ctx, dt, job.words || [], light), dt);
    ctx.restore();
    grade(ctx);
    S.finish(ctx, i);
  },
});
