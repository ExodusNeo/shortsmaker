// kit.mjs — the parts a drawn opener is made of (ShortsMaker, 2026-10-30). The AI writes one scene function per
// Short against this kit (KIT.md is its manual); run.mjs renders it. Brush ink + watercolour on paper, the look the
// owner approved in the Dexter test (test_renders/drawn_opener_dexter). Built on lib/ (claude-animation, MIT).
//
// Every part is placed by its GROUND point (x = centre, y = where it stands) and a scale s (1 = normal size), so
// things stand on the ground without arithmetic. Marks are seeded from the call order (k.part names each call), so
// a held drawing keeps its marks and every render of the same code is identical.
import { clamp, lerp, ss, eOut, eBack, popS, ellPts, rrect, noise1, hash } from "./lib/core.mjs";
import { Pen } from "./lib/pen.mjs";
import { star4 } from "./lib/textures.mjs";
import { person as beanPerson, SKIN } from "./lib/rigs/bean.mjs";

export const W = 1080, H = 1920;
export const C = {
  ink: "#2A2420", paper: "#F3EBDA", brass: "#D9A23A", gold: "#E3B64B", wood: "#7A4E2C", plank: "#C49A62",
  sail: "#F4EAD2", sea: "#3FA7A8", deep: "#2C7F8F", sand: "#E8CF92", grass: "#6FA45A", leaf: "#5E9E4E",
  brick: "#B5563C", roof: "#6B3B2A", stone: "#B8B0A0", navy: "#3C4A6B", red: "#D0312D", white: "#FBF7EE",
  sky: "#BFD9E6", snow: "#F4F6F8", molasses: "#4A2A12", water: "#5FB4E0", fire: "#EF7A2A", smoke: "#8C857C",
  money: "#8DB872", skin: SKIN,
};

export function makeKit(ctx, t, words = []) {
  const p = new Pen(ctx);
  let n = 0;
  const k = { ctx, t, W, H, C, SKIN, pen: p };
  // ---- timing ---------------------------------------------------------------------------------------------------
  k.ss = (a, b) => ss(a, b, t);                         // 0 before a, eases to 1 at b
  k.ease = (a, b) => eOut(clamp((t - a) / Math.max(1e-3, b - a)));
  k.pop = (t0, d = .35) => popS(t, t0, d);              // overshooting pop-in starting at t0
  k.lerp = lerp; k.clamp = clamp;
  k.wave = (hz = 1, amp = 1, ph = 0) => Math.sin(t * hz * Math.PI * 2 + ph) * amp;
  k.noise = (x) => noise1(x);
  k.word = (w, fallback = 0) => {                       // when a spoken word starts (seconds into the opener)
    const want = String(w).toLowerCase().replace(/[^a-z0-9']/g, "");
    const hit = words.find(([, , txt]) => String(txt).toLowerCase().replace(/[^a-z0-9']/g, "").startsWith(want));
    return hit ? hit[0] : fallback;
  };
  // ---- drawing primitives ---------------------------------------------------------------------------------------
  const part = (name) => p.begin(name || "part" + ++n, 1, { boil: 8, t });
  k.part = part;
  k.fade = (alpha, fn) => { ctx.save(); ctx.globalAlpha *= clamp(alpha); fn(); ctx.restore(); };
  k.at =(x, y, s, rot, fn) => { ctx.save(); ctx.translate(x, y); if (rot) ctx.rotate(rot); if (s !== 1) ctx.scale(s, s); fn(); ctx.restore(); };
  // opaque paint: solid colour (the library's default alpha is .8: sails showed the sea through), then a thin
  // multiplied wash for the watercolour grain
  k.paint = (pts, color, o = {}) => { p.wash(pts, color, { alpha: 1, ...o, solid: true, over: true }); p.wash(pts, color, { ...o, over: false, alpha: .3 }); };
  k.ink = (pts, o = {}) => p.stroke(pts, { w: 4, ...o });
  k.outline = (pts, o = {}) => p.poly(pts, { w: 4, ...o });
  k.blob = (pts, o = {}) => p.blob(pts, { w: 4, ...o });
  k.ring = (x, y, rx, ry, o = {}) => p.ring(x, y, rx, ry, { w: 4, ...o });
  k.dot = (x, y, r, color = C.ink) => p.dot(x, y, r, color);
  k.oval = (x, y, rx, ry, nPts = 20) => ellPts(x, y, rx, ry, nPts);
  k.rect = (x, y, w, h) => [[x, y], [x + w, y], [x + w, y + h], [x, y + h]];
  k.rrect = (x, y, w, h, r) => rrect(x, y, w, h, r);
  k.text = (str, x, y, o = {}) => p.text(String(str), x, y, { size: 40, font: "sans-serif", color: C.ink, ...o });
  k.shape = (pts, color, o = {}) => { part(); k.paint(pts, color, { sharp: pts.length <= 6, ...o }); p.poly(pts, { w: o.w ?? 4 }); };
  k.disc = (x, y, r, color, o = {}) => { part(); k.paint(ellPts(x, y, r, o.ry ?? r, 24), color); p.ring(x, y, r, o.ry ?? r, { w: o.w ?? 4 }); };

  // ---- backgrounds ----------------------------------------------------------------------------------------------
  const SKIES = { day: ["#CFE3EA", "#EAF1EC"], hot: ["#F2C27A", "#F6DDA8"], dusk: ["#E98A5A", "#F3C98B"],
                  night: ["#1C2458", "#3A4377"], overcast: ["#C9C6BE", "#DAD6CC"], snow: ["#D9DEE3", "#EEF0F2"],
                  storm: ["#6F7480", "#9A9EA6"] };
  k.sky = (kind = "day", horizon = 1000) => {
    const [top, low] = SKIES[kind] || SKIES.day;
    part("sky"); const g = ctx.createLinearGradient(0, 0, 0, horizon); g.addColorStop(0, top); g.addColorStop(.55, top); g.addColorStop(1, low);
    ctx.fillStyle = g; ctx.fillRect(-300, -300, 1680, horizon + 300);
    p.wash(k.rect(-300, -300, 1680, horizon + 300), top, { alpha: .25 });   // the paper's watercolour grain
    if (kind === "night") for (let i = 0; i < 40; i++) {
      const x = hash(i * 3.7) * W, y = hash(i * 9.1) * (horizon - 120), tw = .6 + .4 * Math.sin(t * 3 + i);
      star4(ctx, x, y, (4 + hash(i) * 6) * tw, "#F4F0D8");
    }
  };
  k.sun = (x, y, r = 110, o = {}) => {
    const heat = o.heat ?? 0, rr = r * (1 + .3 * heat) + Math.sin(t * 9) * 3 * heat;
    part("sun"); k.paint(ellPts(x, y, rr, rr, 24), o.color || "#EFA43A"); p.ring(x, y, rr, rr, { w: 5 });
    const rays = o.rays ?? (heat > .05 ? 1 : 0);
    if (rays) for (let i = 0; i < 12; i++) {
      const a = i / 12 * Math.PI * 2 + t * .25, r0 = rr + 18, r1 = rr + 18 + (50 + 40 * heat) * rays;
      p.stroke([[x + Math.cos(a) * r0, y + Math.sin(a) * r0], [x + Math.cos(a) * r1, y + Math.sin(a) * r1]], { w: 6, color: "#D9802A" });
    }
  };
  k.moon = (x, y, r = 70) => { part("moon"); k.paint(ellPts(x, y, r, r, 22), "#EDE7CF"); p.ring(x, y, r, r, { w: 4 });
    p.wash(ellPts(x - r * .3, y - r * .2, r * .18, r * .15, 10), "#C9C2A8", { alpha: .7 }); };
  k.cloud = (x, y, s = 1, color = C.white) => {
    const P = [[-120, 0], [-110, -40], [-60, -70], [-10, -95], [50, -80], [100, -50], [125, 0]].map(([a, b]) => [x + a * s + k.wave(.05, 20, x), y + b * s]);
    part(); k.paint(P, color, { round: true }); p.stroke(P, { w: 3.4 });
  };
  k.hills = (y, color = "#9BBF84", seed = 1) => {
    const P = [[-200, y + 400]]; for (let i = 0; i <= 12; i++) P.push([-200 + i * 125, y - 60 - 70 * Math.abs(noise1(i * .7 + seed))]); P.push([1300, y + 400]);
    part(); k.paint(P, color, { round: true }); p.stroke(P.slice(1, -1), { w: 3 });
  };
  k.sea = (horizon = 960, o = {}) => {
    part("sea"); k.paint(k.rect(-300, horizon, 1680, 1300), o.color || C.sea, { sharp: true });
    p.wash(k.rect(-300, horizon + 420, 1680, 1200), o.deep || C.deep, { solid: true, alpha: .45, over: true });
    for (let r = 0; r < (o.rows ?? 14); r++) for (let i = 0; i < 5; i++) {
      const g = 1 + r * .12, y = horizon + 50 + r * 64, x = ((i * 260 + r * 90 - t * 40 * g) % 1300 + 1300) % 1300 - 110;
      p.stroke([[x, y], [x + 30 * g, y - 10 * g], [x + 60 * g, y]], { w: 3 * Math.sqrt(g), color: r > 5 ? "#17565F" : "#1F6E78", taper: .5 });
    }
    if (o.glare != null) for (let i = 0; i < 11; i++) {      // the sun's reflection under x = o.glare
      const y = horizon + 30 + i * 48, w = 30 + i * 9, x = o.glare + Math.sin(t * 3 + i) * 14 - i * 6;
      p.stroke([[x - w, y], [x + w, y]], { w: 5, color: "#F6C46A", alpha: .7, taper: .6 });
    }
  };
  const GROUNDS = { grass: [C.grass, "#4E8040"], sand: [C.sand, "#C9A96A"], dirt: ["#B8946A", "#8C6A44"],
                    snow: [C.snow, "#B9C4CF"], street: ["#A9A193", "#7D7568"], floor: ["#B98A55", "#8C6A44"] };
  k.ground = (y = 1100, kind = "grass") => {
    const [base, mark] = GROUNDS[kind] || GROUNDS.grass;
    part("ground"); k.paint(k.rect(-300, y, 1680, 1300), base, { sharp: true }); p.stroke([[-20, y], [1100, y]], { w: 4 });
    for (let i = 0; i < 46; i++) {
      const x = hash(i * 7.7) * 1100 - 10, yy = y + 20 + hash(i * 3.1) * 700;
      if (kind === "grass") p.stroke([[x, yy], [x + 4, yy - 16], [x + 9, yy]], { w: 2.4, color: mark });
      else if (kind === "street") { if (i < 40) p.stroke([[x, yy], [x + 60, yy]], { w: 2.4, color: mark }); }
      else if (kind === "floor") { if (i < 12) p.stroke([[-20, y + 30 + i * 60], [1100, y + 30 + i * 60]], { w: 2.4, color: mark }); }
      else p.dot(x, yy, 2 + hash(i) * 2, mark);
    }
  };
  k.room = (floorY = 1150, o = {}) => {                    // an interior: wall, floorboards, optional window
    part("room"); k.paint(k.rect(-300, -300, 1680, floorY + 300), o.wall || "#E4CFA8", { sharp: true });
    for (let i = 0; i < 9; i++) p.stroke([[i * 130, -50], [i * 130 + 6, floorY]], { w: 2, color: "#CDB48A", alpha: .6 });
    k.ground(floorY, "floor");
    if (o.window !== false) { const [wx, wy] = o.window || [760, 420];
      part("window"); k.paint(k.rect(wx - 110, wy - 140, 220, 280), o.outside || "#CFE3EA", { sharp: true });
      p.poly(k.rect(wx - 110, wy - 140, 220, 280), { w: 6, color: C.wood }); p.stroke([[wx, wy - 140], [wx, wy + 140]], { w: 5, color: C.wood }); p.stroke([[wx - 110, wy], [wx + 110, wy]], { w: 5, color: C.wood }); }
  };

  // ---- people ---------------------------------------------------------------------------------------------------
  const HATS = ["tricorn", "top", "bowler", "crown", "bonnet", "cap", "helmet", "pith", "fez", "turban", "peci", "none"];
  k.HATS = HATS;
  // hats the bean rig doesn't have, in the person's local space (head centre at hy)
  const ownHat = (kind, hy, o) => {
    const col = o.hatColor || (kind === "crown" ? C.gold : "#2B2622");
    if (kind === "tricorn") { const P = [[-50, hy - 18], [-30, hy - 50], [0, hy - 40], [30, hy - 50], [50, hy - 18], [0, hy - 28]]; k.paint(P, col, { sharp: false, round: true }); p.stroke([...P, P[0]], { w: 3.6 }); }
    if (kind === "top") { const P = [[-24, hy - 26], [-24, hy - 92], [24, hy - 92], [24, hy - 26]]; k.paint(P, col, { sharp: true }); p.poly(P, { w: 3.4 }); p.stroke([[-42, hy - 24], [42, hy - 24]], { w: 6 }); }
    if (kind === "bowler") { const P = ellPts(0, hy - 34, 30, 26, 16).filter(([, y]) => y <= hy - 30); k.paint([...P, [30, hy - 30], [-30, hy - 30]], col); p.stroke([[-44, hy - 26], [44, hy - 26]], { w: 6 }); }
    if (kind === "crown") { const P = [[-30, hy - 22], [-34, hy - 66], [-17, hy - 46], [0, hy - 72], [17, hy - 46], [34, hy - 66], [30, hy - 22]]; k.paint(P, col, { sharp: true }); p.poly(P, { w: 3.4 }); p.dot(0, hy - 40, 5, C.red); }
    if (kind === "bonnet") { const P = ellPts(0, hy - 6, 42, 40, 16).filter(([, y]) => y <= hy + 6); k.paint([...P], o.hatColor || "#E8D9B0"); p.stroke(P, { w: 3.4 }); p.stroke([[-30, hy + 10], [-8, hy + 34]], { w: 2.6, color: C.red }); }
  };
  k.person = (x, y, s = 1, o = {}) => {
    const flip = o.flip ? -1 : 1, hy = -212 + (o.dip || 0);
    let bob = o.still ? 0 : Math.sin(t * 4.2 + x * .013) * 2.2;
    if (o.walk != null) bob = -Math.abs(Math.cos(o.walk)) * 7;
    const bean = { ...o, shirt: o.coat || o.shirt, hat: HATS.includes(o.hat) && ["cap", "helmet", "pith", "fez", "turban", "peci"].includes(o.hat) ? o.hat : undefined };
    // the rig paints with see-through washes: an opaque paper underlay keeps a coat and face their own colour over
    // a sea or sky (the first live drafts turned people green over the teal sea)
    ctx.save(); ctx.translate(x, y + bob * s); ctx.scale(s * flip, s); ctx.fillStyle = C.paper;
    ctx.beginPath(); ctx.ellipse(0, hy, 31, 30, 0, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); [[-22, -176], [22, -176], [30, -120], [31, -82], [-31, -82], [-30, -120]].forEach(([a, b], i) => i ? ctx.lineTo(a, b) : ctx.moveTo(a, b)); ctx.fill();
    ctx.restore();
    part(); beanPerson(p, x, y, s, bean, t);
    ctx.save(); ctx.translate(x, y + bob * s); ctx.scale(s * flip, s);
    if (o.dress) { const D = [[-26, -120], [26, -120], [52, -20], [-52, -20]]; k.paint(D, o.dress, { sharp: true }); p.poly(D, { w: 4 }); }
    if (o.beard) { const B = [[-26, hy + 8], [26, hy + 8], [16, hy + 44], [0, hy + 54], [-16, hy + 44]]; k.paint(B, o.beard === true ? "#5A4636" : o.beard); p.blob(B, { w: 3 }); }
    ownHat(o.hat, hy, o);
    ctx.restore();
    // world positions of the head and both hands (for held props, bubbles, sweat)
    const [la, ra] = o.arms || [18, 18], [lb, rb] = o.bend || [0, 0];
    const hand = (a, b, sg, sx) => { const d = (ang) => [sg * Math.sin(ang * Math.PI / 180), Math.cos(ang * Math.PI / 180)];
      const [ux, uy] = d(a), [fx, fy] = d(a + b), lx = sx + ux * 42 + fx * 40, ly = -166 + uy * 42 + fy * 40;
      return [x + flip * s * lx, y + bob * s + s * ly]; };
    return { head: [x, y + bob * s + s * hy], top: [x, y + bob * s + s * (hy - 50)], hands: [hand(la, lb, -1, -22), hand(ra, rb, 1, 22)] };
  };
  k.crowd = (x0, x1, y, count = 5, s = .8, o = {}) => {
    const out = [];
    for (let i = 0; i < count; i++) {
      const x = lerp(x0, x1, count > 1 ? i / (count - 1) : .5), h = hash(i * 5.3 + x0);
      out.push(k.person(x, y + (i % 2) * 18, s * (.92 + h * .12), { coat: [C.navy, "#7A5A3A", "#5E7A5A", C.red, "#8A7A9A"][i % 5],
        skin: SKIN[i % SKIN.length], hat: o.hats ? o.hats[i % o.hats.length] : "none", face: o.face, arms: o.arms, still: o.still, flip: o.flip ?? (i % 2 === 1) }));
    }
    return out;
  };

  // ---- animals (bean style: body, stick legs, dot eye; local space faces right, flip faces left) -----------------
  const legs = (pts, walk, len, w = 4.6) => pts.forEach(([lx, ly], i) => {
    const a = walk == null ? 0 : Math.sin(walk + i * Math.PI / 2) * .45;
    p.stroke([[lx, ly], [lx + Math.sin(a) * len, ly + Math.cos(a) * len]], { w, taper: .3 });
  });
  const animal = (x, y, s, o, draw) => { part(); ctx.save(); ctx.translate(x, y); ctx.scale(s * (o.flip ? -1 : 1), s); draw(); ctx.restore(); };
  k.dog = (x, y, s = 1, o = {}) => animal(x, y, s, o, () => {
    const col = o.color || "#B98A55";
    legs([[-50, -40], [-34, -40], [34, -40], [50, -40]], o.walk, 40);
    const B = [[-70, -50], [-60, -82], [40, -86], [62, -60], [50, -40], [-60, -38]]; k.paint(B, col, { round: true }); p.blob(B, { w: 4 });
    const Hd = ellPts(78, -100, 30, 25, 14); k.paint(Hd, col); p.ring(78, -100, 30, 25, { w: 4 });
    p.wash([[96, -98], [124, -92], [120, -80], [98, -84]], col, { solid: true, over: true }); p.stroke([[96, -98], [124, -92], [120, -80], [98, -84]], { w: 3.4 });
    p.wash([[62, -118], [52, -86], [70, -96]], "#7A5A3A", { solid: true, over: true }); p.dot(122, -92, 4.5); p.dot(84, -106, 4);
    p.stroke([[-68, -70], [-96, -96 + Math.sin(t * 12) * 10]], { w: 4.4, taper: .5 });
  });
  k.chicken = (x, y, s = 1, o = {}) => animal(x, y, s, o, () => {
    legs([[-10, -40], [12, -40]], o.walk, 40, 3.6);
    const B = ellPts(0, -80, 52, 42, 18); k.paint(B, o.color || C.white); p.ring(0, -80, 52, 42, { w: 4 });
    const wing = o.flap ? Math.sin(t * 20) * 22 : 0;
    p.stroke([[-20, -86], [10, -92 - wing], [26, -76]], { w: 3.4 });
    p.stroke([[-50, -92], [-74, -126], [-62, -96], [-80, -104]], { w: 3.6 });
    if (!o.headless) { k.paint(ellPts(46, -132, 22, 22, 12), o.color || C.white); p.ring(46, -132, 22, 22, { w: 4 });
      p.wash([[40, -152], [48, -168], [56, -152]], C.red, { solid: true, over: true }); p.wash([[66, -134], [84, -128], [66, -122]], C.gold, { solid: true, over: true }); p.dot(52, -136, 3.6);
      p.stroke([[36, -104], [42, -114]], { w: 3.6 }); }
    else { p.stroke([[34, -110], [44, -130]], { w: 6 }); p.wash(ellPts(44, -130, 8, 5, 8), C.red, { solid: true, over: true }); }
  });
  k.horse = (x, y, s = 1, o = {}) => animal(x, y, s, o, () => {
    const col = o.color || "#8C5A33";
    legs([[-80, -120], [-60, -120], [60, -120], [80, -120]], o.walk, 120, 6);
    const B = [[-110, -130], [-96, -190], [80, -196], [112, -150], [92, -118], [-96, -112]]; k.paint(B, col, { round: true }); p.blob(B, { w: 4.4 });
    const N = [[70, -186], [96, -262], [120, -292], [150, -300], [196, -262], [206, -240], [186, -228], [146, -246], [126, -206], [112, -150]];
    k.paint(N, col, { sharp: true }); p.poly(N, { w: 4.4 });
    p.wash([[118, -300], [126, -326], [136, -298]], col, { solid: true, over: true }); p.stroke([[118, -300], [126, -326], [136, -298]], { w: 3.4 });
    p.stroke([[112, -296], [86, -240], [74, -190]], { w: 9, color: "#3A2A1C" }); p.dot(150, -276, 5.5); p.dot(198, -246, 3);
    p.stroke([[-108, -170], [-140, -120 + Math.sin(t * 6) * 8], [-150, -80]], { w: 8, color: "#3A2A1C", taper: .5 });
  });
  k.bird = (x, y, s = 1, o = {}) => animal(x, y, s, o, () => {
    const f = Math.sin(t * 14 + x) * 18;
    p.stroke([[-40, -f], [-14, 4], [0, 8], [14, 4], [40, -f]], { w: 4.2, color: o.color || C.ink });
  });
  k.pig = (x, y, s = 1, o = {}) => animal(x, y, s, o, () => {
    legs([[-40, -36], [-22, -36], [22, -36], [40, -36]], o.walk, 32, 5);
    const B = ellPts(0, -76, 74, 48, 18); k.paint(B, o.color || "#E9A9A0"); p.ring(0, -76, 74, 48, { w: 4 });
    k.paint(ellPts(78, -84, 18, 16, 10), "#D98A82"); p.ring(78, -84, 18, 16, { w: 3.4 }); p.dot(74, -84, 3); p.dot(84, -84, 3); p.dot(54, -98, 4);
    p.stroke([[-72, -84], [-88, -94], [-80, -104]], { w: 3.4 });
  });
  k.cow = (x, y, s = 1, o = {}) => animal(x, y, s, o, () => {
    legs([[-80, -110], [-60, -110], [60, -110], [80, -110]], o.walk, 100, 6);
    const B = [[-110, -116], [-104, -190], [90, -196], [112, -150], [96, -110]]; k.paint(B, o.color || C.white, { round: true }); p.blob(B, { w: 4.4 });
    p.wash(ellPts(-30, -160, 30, 22, 12), C.ink, { alpha: .85 }); p.wash(ellPts(40, -140, 22, 16, 10), C.ink, { alpha: .85 });
    k.paint(ellPts(130, -186, 34, 30, 14), o.color || C.white); p.ring(130, -186, 34, 30, { w: 4 }); p.dot(140, -192, 4.5);
    p.stroke([[112, -214], [100, -236]], { w: 4 }); p.stroke([[148, -214], [160, -236]], { w: 4 });
  });

  // ---- vehicles and buildings -----------------------------------------------------------------------------------
  k.ship = (x, y, s = 1, o = {}) => {                       // y = waterline; returns the deck's y and ends
    const roll = Math.sin(t * 2.1 + x) * .025 * (o.roll ?? 1), bob = Math.sin(t * 2.6 + x) * 7;
    ctx.save(); ctx.translate(x, y + bob); ctx.rotate(roll); ctx.scale(s * (o.flip ? -1 : 1), s);
    const hull = [[-300, -100], [-240, -55], [240, -55], [300, -105], [255, 15], [-230, 15]];
    part(); k.paint(hull, o.hull || "#8B5A33", { sharp: true }); p.poly(hull, { w: 6 });
    p.stroke([[-252, -22], [262, -24]], { w: 2.6 }); p.stroke([[-238, 0], [254, -2]], { w: 2.2 });
    const masts = o.masts ?? 2, xs = masts === 1 ? [10] : masts === 3 ? [-150, 10, 160] : [-95, 120];
    xs.forEach((mx, i) => { const top = -640 + i * 50, sw = 220 - i * 10;
      part(); p.stroke([[mx, -55], [mx, top]], { w: 7, color: C.wood, taper: .1 });
      if (o.sails !== false) { const b = Math.sin(t * 2.4 + mx) * 6, S = [[mx - sw / 2, top + 50], [mx + sw / 2, top + 50], [mx + sw / 2 + 18 + b, top + 260], [mx - sw / 2 - 18 + b, top + 260]];
        k.paint(S, o.sail || C.sail, { sharp: true }); p.poly(S, { w: 4 }); p.stroke([[mx - sw / 2 - 10, top + 50], [mx + sw / 2 + 10, top + 50]], { w: 5, color: C.wood }); }
    });
    if (o.flag !== false) { part(); const f = Math.sin(t * 7) * 8, fx = xs[0];
      p.wash([[fx, -640], [fx + 70, -628 + f], [fx, -600]], o.flag || C.red, { solid: true, over: true }); }
    ctx.restore();
    return { deck: y + bob - 55 * s, left: x - 240 * s, right: x + 240 * s };
  };
  k.boat = (x, y, s = 1, o = {}) => { const bob = Math.sin(t * 2.6 + x) * 5;
    const P = [[-130, -40], [130, -40], [100, 10], [-100, 10]].map(([a, b]) => [x + a * s, y + bob + b * s]);
    part(); k.paint(P, o.color || "#8B5A33", { sharp: true }); p.poly(P, { w: 4.4 }); return { deck: y + bob - 40 * s }; };
  k.cart = (x, y, s = 1, o = {}) => { const spin = (o.roll ?? 0) * t * 6;
    const B = k.rect(x - 120 * s, y - 130 * s, 240 * s, 70 * s); part(); k.paint(B, o.color || C.plank, { sharp: true }); p.poly(B, { w: 4 });
    for (const wx of [-80, 80]) { const cx = x + wx * s, cy = y - 40 * s; p.ring(cx, cy, 40 * s, 40 * s, { w: 5 });
      for (let i = 0; i < 4; i++) { const a = spin + i * Math.PI / 4; p.stroke([[cx - Math.cos(a) * 36 * s, cy - Math.sin(a) * 36 * s], [cx + Math.cos(a) * 36 * s, cy + Math.sin(a) * 36 * s]], { w: 2.6 }); } }
    p.stroke([[x + 120 * s, y - 100 * s], [x + 210 * s, y - 80 * s]], { w: 5, color: C.wood }); return { bed: y - 130 * s };
  };
  k.house = (x, y, s = 1, o = {}) => {
    const w = 300 * s, h = 220 * s, wall = k.rect(x - w / 2, y - h, w, h), roof = [[x - w / 2 - 20 * s, y - h], [x, y - h - 150 * s], [x + w / 2 + 20 * s, y - h]];
    part(); k.paint(wall, o.wall || "#E4CFA8", { sharp: true }); p.poly(wall, { w: 4.4 });
    k.paint(roof, o.roof || C.roof, { sharp: true }); p.poly(roof, { w: 4.4 });
    const door = k.rect(x - 34 * s, y - 120 * s, 68 * s, 120 * s); k.paint(door, C.wood, { sharp: true }); p.poly(door, { w: 3.6 });
    for (const wx of [-100, 100]) { const win = k.rect(x + wx * s - 34 * s, y - 170 * s, 68 * s, 60 * s); k.paint(win, o.lit ? "#F6D27A" : "#CFE3EA", { sharp: true }); p.poly(win, { w: 3.4 }); }
    return { top: y - h - 150 * s, roof: y - h };
  };
  k.shop = (x, y, s = 1, o = {}) => {
    const w = 360 * s, h = 300 * s, wall = k.rect(x - w / 2, y - h, w, h);
    part(); k.paint(wall, o.wall || C.brick, { sharp: true }); p.poly(wall, { w: 4.4 });
    const board = k.rect(x - w / 2 + 20 * s, y - h + 20 * s, w - 40 * s, 70 * s); k.paint(board, o.board || "#2F4A3A", { sharp: true }); p.poly(board, { w: 3.6 });
    if (o.sign) p.text(o.sign, x, y - h + 70 * s, { size: 40 * s, font: "serif", color: C.gold });
    const win = k.rect(x - w / 2 + 30 * s, y - 170 * s, 160 * s, 130 * s); k.paint(win, "#CFE3EA", { sharp: true }); p.poly(win, { w: 3.6 });
    const door = k.rect(x + 50 * s, y - 180 * s, 80 * s, 180 * s); k.paint(door, C.wood, { sharp: true }); p.poly(door, { w: 3.6 });
    return { top: y - h };
  };
  k.bank = (x, y, s = 1, o = {}) => {
    const w = 420 * s, base = k.rect(x - w / 2, y - 40 * s, w, 40 * s), ped = [[x - w / 2 - 10 * s, y - 300 * s], [x, y - 400 * s], [x + w / 2 + 10 * s, y - 300 * s]];
    part(); k.paint(k.rect(x - w / 2, y - 300 * s, w, 300 * s), o.wall || C.stone, { sharp: true });
    for (let i = 0; i < 5; i++) { const cx = x - w / 2 + 50 * s + i * 80 * s; const col = k.rect(cx - 16 * s, y - 290 * s, 32 * s, 250 * s); k.paint(col, "#E6E0D2", { sharp: true }); p.poly(col, { w: 3 }); }
    k.paint(ped, o.wall || C.stone, { sharp: true }); p.poly(ped, { w: 4.4 }); k.paint(base, "#9C9484", { sharp: true }); p.poly(base, { w: 4 });
    if (o.sign) p.text(o.sign, x, y - 312 * s, { size: 30 * s, font: "serif" });
    return { top: y - 400 * s };
  };
  k.factory = (x, y, s = 1, o = {}) => {
    const body = k.rect(x - 200 * s, y - 200 * s, 400 * s, 200 * s), saw = [[x - 200 * s, y - 200 * s]];
    for (let i = 0; i < 4; i++) saw.push([x - 200 * s + i * 100 * s, y - 270 * s], [x - 100 * s + i * 100 * s, y - 200 * s]);
    const stack = k.rect(x + 120 * s, y - 420 * s, 50 * s, 220 * s);
    part(); k.paint(stack, C.brick, { sharp: true }); p.poly(stack, { w: 4 }); k.paint(body, o.wall || C.brick, { sharp: true }); p.poly(body, { w: 4.4 }); p.stroke(saw, { w: 4, smooth: false });
    if (o.smoke !== false) k.smoke(x + 145 * s, y - 420 * s, s);
    return { top: y - 420 * s };
  };
  k.tank = (x, y, s = 1, o = {}) => {                        // a big storage tank; burst 0..1 splits its side open
    const w = 320 * s, h = 380 * s, body = k.rect(x - w / 2, y - h, w, h);
    part(); k.paint(body, o.color || "#9AA3A8", { sharp: true }); p.poly(body, { w: 4.4 });
    for (let i = 1; i < 5; i++) p.stroke([[x - w / 2, y - h + i * h / 5], [x + w / 2, y - h + i * h / 5]], { w: 2.4 });
    k.paint(ellPts(x, y - h, w / 2, 26 * s, 18), "#B9C1C5"); p.ring(x, y - h, w / 2, 26 * s, { w: 4 });
    if (o.label) p.text(o.label, x, y - h / 2, { size: 38 * s, font: "sans-serif" });
    if (o.burst) { const b = o.burst, crack = [[x + w / 2 - 6, y - h * .8], [x + w / 2 - 30 * s * b, y - h * .6], [x + w / 2 - 10, y - h * .45], [x + w / 2 - 40 * s * b, y - h * .25]];
      p.stroke(crack, { w: 6, smooth: false }); }
    return { top: y - h, right: x + w / 2 };
  };
  k.tower = (x, y, s = 1, o = {}) => {                      // an iron lattice tower
    const lvl = [[0, 230], [260, 150], [520, 80], [820, 30]], P = (side) => lvl.map(([hy, hw]) => [x + side * hw * s, y - hy * s]);
    part(); const L = P(-1), R = P(1);
    p.stroke(L, { w: 6, color: o.color || "#6E5A44", smooth: false }); p.stroke(R, { w: 6, color: o.color || "#6E5A44", smooth: false });
    for (let i = 0; i < lvl.length - 1; i++) { p.stroke([L[i], R[i + 1]], { w: 2.6 }); p.stroke([R[i], L[i + 1]], { w: 2.6 }); p.stroke([L[i], R[i]], { w: 4 }); }
    p.stroke([[x, y - 820 * s], [x, y - 900 * s]], { w: 5 });
    const arch = []; for (let i = 0; i <= 10; i++) { const a = Math.PI + i / 10 * Math.PI; arch.push([x + Math.cos(a) * 150 * s, y - 40 * s + Math.sin(a) * 110 * s]); }
    p.stroke(arch, { w: 4 }); return { top: y - 900 * s };
  };

  // ---- nature ---------------------------------------------------------------------------------------------------
  k.palm = (x, y, s = 1) => { const tx = x - 35 * s, ty = y - 280 * s, sway = Math.sin(t * 1.6 + x) * .06;
    part(); p.stroke([[x, y], [lerp(x, tx, .5) + 18 * s, lerp(y, ty, .5)], [tx, ty]], { w: 14 * s, color: "#8C6A44", taper: .55 });
    for (const a of [-2.7, -2.1, -1.4, -.8, -.2, .5]) { const ex = tx + Math.cos(a + sway) * 130 * s, ey = ty + Math.sin(a + sway) * 75 * s + 42 * s,
      mx = tx + Math.cos(a + sway) * 70 * s, my = ty + Math.sin(a + sway) * 58 * s - 6 * s;
      k.paint([[tx, ty], [mx, my - 15 * s], [ex, ey], [mx, my + 15 * s]], C.leaf, { round: true }); p.stroke([[tx, ty], [mx, my], [ex, ey]], { w: 3.2 }); }
  };
  k.tree = (x, y, s = 1, o = {}) => { part(); p.stroke([[x, y], [x + 4 * s, y - 200 * s]], { w: 22 * s, color: "#7A5A3A", taper: .4 });
    const crown = ellPts(x, y - 290 * s, 130 * s, 120 * s, 22).map(([a, b], i) => [a + Math.sin(i * 2.3) * 12 * s, b + Math.cos(i * 1.7) * 12 * s]);
    k.paint(crown, o.color || C.leaf, { round: true }); p.blob(crown, { w: 4 }); };
  k.pine = (x, y, s = 1, o = {}) => { part(); for (let i = 0; i < 3; i++) { const T = [[x - (120 - i * 25) * s, y - (40 + i * 90) * s], [x, y - (190 + i * 90) * s], [x + (120 - i * 25) * s, y - (40 + i * 90) * s]];
    k.paint(T, o.color || "#3F7A4A", { sharp: true }); p.poly(T, { w: 3.6 }); } p.stroke([[x, y], [x, y - 40 * s]], { w: 14 * s, color: "#7A5A3A" }); };
  k.island = (x, y, w = 420) => { const P = [[x - w / 2, y + 10], [x - w / 2 + 60, y - 50], [x - 60, y - 80], [x + 80, y - 74], [x + w / 2 - 40, y - 40], [x + w / 2 + 20, y + 10]];
    part(); k.paint(P, C.sand, { round: true }); p.blob(P, { w: 4 }); return { top: y - 75 }; };

  // ---- props ----------------------------------------------------------------------------------------------------
  k.crate = (x, y, w = 140, h = 100, o = {}) => { const B = k.rect(x - w / 2, y - h, w, h);
    part(); k.paint(B, o.color || C.plank, { sharp: true }); p.poly(B, { w: 4 });
    if (o.label) { const size = o.size || Math.min(64, (w - 24) / (o.label.length * .74), h * .42); p.text(o.label, x, y - h / 2 + size * .35, { size, font: "sans-serif" }); }
    else p.stroke([[x - w / 2, y - h / 2], [x + w / 2, y - h / 2]], { w: 2.4 }); };
  k.barrel = (x, y, s = 1, o = {}) => { const B = [[-50, 0], [-60, -70], [-50, -140], [50, -140], [60, -70], [50, 0]].map(([a, b]) => [x + a * s, y + b * s]);
    part(); k.paint(B, o.color || "#9A6A3A", { round: true }); p.blob(B, { w: 4 }); for (const yy of [-30, -110]) p.stroke([[x - 56 * s, y + yy * s], [x + 56 * s, y + yy * s]], { w: 4, color: "#4A4A4A" }); };
  k.sack = (x, y, s = 1, o = {}) => { const B = [[-55, 0], [-62, -70], [-30, -120], [-10, -140], [12, -140], [30, -120], [62, -70], [55, 0]].map(([a, b]) => [x + a * s, y + b * s]);
    part(); k.paint(B, o.color || "#C9B48A", { round: true }); p.blob(B, { w: 4 }); p.stroke([[x - 22 * s, y - 118 * s], [x + 22 * s, y - 118 * s]], { w: 3.4 });
    if (o.label) p.text(o.label, x, y - 50 * s, { size: Math.min(40, 170 / (o.label.length * .62)) * s, font: "sans-serif" }); };
  k.coins = (x, y, count = 8, s = 1) => { part(); for (let i = 0; i < count; i++) { const row = Math.floor(Math.sqrt(i * 2)), cx = x + (hash(i * 4.1) - .5) * 120 * s, cy = y - row * 18 * s - hash(i) * 6;
    k.paint(ellPts(cx, cy, 26 * s, 12 * s, 14), C.gold); p.ring(cx, cy, 26 * s, 12 * s, { w: 2.8 }); } };
  k.coin = (x, y, r = 30) => { part(); k.paint(ellPts(x, y, r, r, 18), C.gold); p.ring(x, y, r, r, { w: 3.4 }); p.ring(x, y, r * .7, r * .7, { w: 2, color: "#9A7420" }); };
  k.moneybag = (x, y, s = 1, o = {}) => { const B = [[-60, 0], [-70, -60], [-40, -110], [-18, -126], [18, -126], [40, -110], [70, -60], [60, 0]].map(([a, b]) => [x + a * s, y + b * s]);
    part(); k.paint(B, o.color || "#C9A96A", { round: true }); p.blob(B, { w: 4 }); p.stroke([[x - 20 * s, y - 124 * s], [x - 34 * s, y - 150 * s]], { w: 3.4 }); p.stroke([[x + 20 * s, y - 124 * s], [x + 34 * s, y - 150 * s]], { w: 3.4 });
    p.text(o.label || "$", x, y - 40 * s, { size: 60 * s, font: "serif", color: "#3A6A2A" }); };
  k.banknote = (x, y, s = 1, rot = 0) => k.at(x, y, s, rot, () => { const B = k.rect(-90, -44, 180, 88);
    part(); k.paint(B, C.money, { sharp: true }); p.poly(B, { w: 3.4 }); p.ring(0, 0, 26, 26, { w: 2.6, color: "#3A6A2A" }); p.text("$", 0, 12, { size: 34, font: "serif", color: "#3A6A2A" }); });
  k.paper = (x, y, s = 1, o = {}) => k.at(x, y, s, o.rot || 0, () => { const B = k.rect(-120, -160, 240, 320);
    part(); k.paint(B, "#F2E8CF", { sharp: true }); p.poly(B, { w: 3.6 });
    if (o.title) p.text(o.title, 0, -110, { size: 30, font: "serif" });
    for (let i = 0; i < (o.lines ?? 7); i++) p.stroke([[-90, -60 + i * 30], [90 - hash(i * 7) * 60, -60 + i * 30]], { w: 2.4, color: "#6A5A4A" });
    if (o.seal) { k.paint(ellPts(60, 120, 26, 26, 14), C.red); } });
  k.cup = (x, y, s = 1, o = {}) => { const B = [[-40, 0], [-50, -110], [50, -110], [40, 0]].map(([a, b]) => [x + a * s, y + b * s]);
    part(); k.paint(B, o.color || C.white, { sharp: true }); p.poly(B, { w: 4 }); p.ring(x + 58 * s, y - 60 * s, 18 * s, 26 * s, { w: 4 });
    if (o.drink) k.paint([[x - 46 * s, y - 96 * s], [x + 46 * s, y - 96 * s], [x + 44 * s, y - 86 * s], [x - 44 * s, y - 86 * s]], o.drink, { sharp: true });
    if (o.steam) for (let i = 0; i < 3; i++) { const yy = y - 130 * s - ((t * 60 + i * 30) % 90) * s; p.stroke([[x + (i - 1) * 20 * s, yy], [x + (i - 1) * 20 * s + 10 * s, yy - 30 * s], [x + (i - 1) * 20 * s, yy - 60 * s]], { w: 3, color: C.smoke, alpha: .7 }); } };
  k.bottle = (x, y, s = 1, o = {}) => { const B = [[-30, 0], [-32, -110], [-12, -140], [-12, -190], [12, -190], [12, -140], [32, -110], [30, 0]].map(([a, b]) => [x + a * s, y + b * s]);
    part(); k.paint(B, o.color || "#5E8A5A", { sharp: false }); p.poly(B, { w: 3.6 }); if (o.label) p.text(o.label, x, y - 50 * s, { size: 22 * s }); };
  k.table = (x, y, w = 400, o = {}) => { const top = k.rect(x - w / 2, y - 180, w, 26);
    part(); k.paint(top, o.color || C.wood, { sharp: true }); p.poly(top, { w: 4 }); for (const lx of [-w / 2 + 30, w / 2 - 30]) p.stroke([[x + lx, y - 154], [x + lx, y]], { w: 10, color: C.wood }); return { top: y - 180 }; };
  k.chair = (x, y, s = 1) => { part(); p.stroke([[x - 40 * s, y], [x - 40 * s, y - 220 * s]], { w: 8, color: C.wood }); p.stroke([[x + 40 * s, y], [x + 40 * s, y - 110 * s]], { w: 8, color: C.wood });
    p.stroke([[x - 44 * s, y - 110 * s], [x + 44 * s, y - 110 * s]], { w: 10, color: C.wood }); };
  k.sign = (x, y, str, o = {}) => { const w = Math.max(160, str.length * (o.size || 40) * .62 + 40), Bd = k.rect(x - w / 2, y - 260, w, 90);
    part(); if (o.post !== false) p.stroke([[x, y], [x, y - 170]], { w: 10, color: C.wood }); k.paint(Bd, o.color || C.plank, { sharp: true }); p.poly(Bd, { w: 4 });
    p.text(str, x, y - 202, { size: o.size || 40, font: "sans-serif" }); };
  k.clock = (x, y, r = 80, o = {}) => { part(); k.paint(ellPts(x, y, r, r, 24), C.white); p.ring(x, y, r, r, { w: 5 });
    const hr = (o.hour ?? 3) / 12 * Math.PI * 2, mn = (o.minute ?? (t * 60)) / 60 * Math.PI * 2;
    p.stroke([[x, y], [x + Math.sin(hr) * r * .5, y - Math.cos(hr) * r * .5]], { w: 6 }); p.stroke([[x, y], [x + Math.sin(mn) * r * .8, y - Math.cos(mn) * r * .8]], { w: 4 }); };
  k.fire = (x, y, s = 1) => { part(); for (let i = 0; i < 3; i++) { const h = (130 - i * 30) * s * (1 + .15 * Math.sin(t * 14 + i)), w = (60 - i * 14) * s;
    const F = [[x - w, y], [x - w * .6, y - h * .5], [x + Math.sin(t * 9 + i) * 10, y - h], [x + w * .6, y - h * .5], [x + w, y]];
    k.paint(F, ["#E8552A", C.fire, "#F6C46A"][i], { round: true }); } };

  // ---- effects (t0 = when it starts; they are drawn only while they play) ---------------------------------------
  k.glint = (x, y, size = 40, t0 = 0) => { const g = popS(t, t0, .18, 2.5) * (1 - ss(t0 + .25, t0 + .5, t)); if (g > .01) star4(ctx, x, y, size * g, "#FFF6C8"); };
  k.sweat = (x, y, t0 = 0, s = 1) => { for (let i = 0; i < 3; i++) { const st = t0 + i * .28, a = clamp((t - st) / .5);
    if (a > 0 && a < 1) { part(); p.wash(ellPts(x + (i - 1) * 34 * s + a * 36 * (i - 1) * s, y - a * 26 * s + a * a * 80 * s, 7 * s, 11 * s, 8), "#5FB4E0", { solid: true, over: true, alpha: 1 - a }); } } };
  k.shimmer = (x0, x1, y, strength = 1) => { if (strength <= .01) return; ctx.save(); ctx.globalAlpha = .8 * strength;
    for (let i = 0; i < 7; i++) { const x = lerp(x0, x1, i / 6), y0 = y - ((t * 120 + i * 37) % 160); part(); p.stroke([[x, y0], [x + 12, y0 - 30], [x - 8, y0 - 60], [x + 10, y0 - 90]], { w: 4.5, color: "#E07A2A", taper: .6 }); }
    ctx.restore(); };
  k.speed = (x, y, dir = -1, count = 3, len = 80) => { part(); for (let i = 0; i < count; i++) p.stroke([[x, y + i * 24], [x + dir * len * (1 - i * .2), y + i * 24]], { w: 4, taper: .7 }); };
  k.burst = (x, y, r = 120, t0 = 0) => { const a = clamp((t - t0) / .35); if (a <= 0 || a >= 1) return; part();
    for (let i = 0; i < 12; i++) { const ang = i / 12 * Math.PI * 2, r0 = r * .4 + r * .5 * a, r1 = r0 + r * .5 * (1 - a); p.stroke([[x + Math.cos(ang) * r0, y + Math.sin(ang) * r0], [x + Math.cos(ang) * r1, y + Math.sin(ang) * r1]], { w: 5 }); } };
  k.puff = (x, y, s = 1, t0 = 0, color = C.smoke) => { const a = clamp((t - t0) / .9); if (a <= 0 || a >= 1) return;
    part(); p.wash(ellPts(x, y - a * 80 * s, (30 + 70 * a) * s, (24 + 50 * a) * s, 16), color, { solid: true, over: true, alpha: .8 * (1 - a) }); };
  k.smoke = (x, y, s = 1, color = C.smoke) => { for (let i = 0; i < 4; i++) { const a = ((t * .6 + i / 4) % 1);
    part(); p.wash(ellPts(x + a * 60 * s, y - a * 260 * s, (24 + 50 * a) * s, (20 + 40 * a) * s, 14), color, { solid: true, over: true, alpha: .7 * (1 - a) }); } };
  k.splash = (x, y, t0 = 0, s = 1, color = C.water) => { const a = clamp((t - t0) / .6); if (a <= 0 || a >= 1) return; part();
    for (let i = 0; i < 7; i++) { const ang = Math.PI + (i + .5) / 7 * Math.PI, d = a * 120 * s; p.wash(ellPts(x + Math.cos(ang) * d, y + Math.sin(ang) * d + a * a * 120 * s, 9 * s, 12 * s, 8), color, { solid: true, over: true, alpha: 1 - a }); } };
  k.question = (x, y, size = 90, t0 = 0) => { const g = popS(t, t0); if (g <= 0) return; k.at(x, y, g, Math.sin(t * 3) * .08, () => { part(); p.text("?", 0, size * .35, { size, font: "serif", color: C.red }); }); };
  k.exclaim = (x, y, size = 90, t0 = 0) => { const g = popS(t, t0); if (g <= 0) return; k.at(x, y, g, 0, () => { part(); p.text("!", 0, size * .35, { size, font: "serif", color: C.red }); }); };
  k.bubble = (x, y, str, o = {}) => { const size = o.size || 40, w = String(str).length * size * .58 + 50, h = size * 1.6, g = o.t0 != null ? popS(t, o.t0) : 1; if (g <= 0) return;
    k.at(x, y, g, 0, () => { const B = rrect(-w / 2, -h / 2, w, h, h / 2), tail = o.tail ?? -1, T = [[tail * w * .18 - 12, h / 2 - 3], [tail * w * .3, h / 2 + 26], [tail * w * .18 + 12, h / 2 - 3]];
      part(); p.wash(B, C.white, { solid: true, over: true }); p.wash(T, C.white, { solid: true, over: true }); p.blob(B, { w: 3.6 }); p.stroke(T, { w: 3.2, smooth: false }); p.text(String(str), 0, size * .35, { size, font: "sans-serif" }); }); };
  k.rain = (strength = 1) => { part(); ctx.save(); ctx.globalAlpha = .6 * strength; for (let i = 0; i < 60; i++) { const x = hash(i * 3.3) * 1200 - 60, y = ((hash(i * 7.1) * 2000 + t * 1400) % 2000) - 80;
    p.stroke([[x, y], [x - 12, y + 50]], { w: 2.4, color: "#5A7A9A" }); } ctx.restore(); };
  k.snowfall = (strength = 1) => { for (let i = 0; i < 70 * strength; i++) { const x = (hash(i * 3.3) * 1200 + Math.sin(t + i) * 30) % 1100, y = ((hash(i * 7.1) * 2000 + t * 160) % 2000) - 40;
    ctx.fillStyle = "#FFFFFF"; ctx.beginPath(); ctx.arc(x, y, 4 + hash(i) * 4, 0, Math.PI * 2); ctx.fill(); } };
  k.flood = (front, top, o = {}) => {                       // a liquid mass from the left edge to x = front, its surface at y = top
    const P = [[-300, 2000], [-300, top]]; for (let i = 0; i <= 20; i++) { const x = lerp(-300, front, i / 20); P.push([x, top + Math.sin(i * .9 + t * 5) * 14 - (i === 20 ? 0 : 0)]); }
    P.push([front + 60, top + 120], [front + 30, 2000]);
    part(); k.paint(P, o.color || C.molasses, { round: true }); p.stroke(P.slice(2, -1), { w: 4.4 });
    for (let i = 0; i < 6; i++) p.stroke([[front - 40 - i * 120, top + 60 + (i % 2) * 40], [front - 100 - i * 120, top + 70 + (i % 2) * 40]], { w: 3, color: "#E0B080", alpha: .6 }); };
  k.fall = (y0, y1, t0, dur = .6) => lerp(y0, y1, clamp((t - t0) / dur) ** 2);   // a dropped thing's y, accelerating
  k.arc = (from, to, t0, dur = .8, height = 200) => { const a = clamp((t - t0) / dur); return [lerp(from[0], to[0], a), lerp(from[1], to[1], a) - Math.sin(a * Math.PI) * height]; };
  return k;
}
