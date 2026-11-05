# Drawn opener kit

You write ONE JavaScript module that draws scene 1 of a YouTube Short as a hand-drawn brush-ink + watercolour
animation. It is rendered at 1080x1920, 30 fps, for the length of scene 1's voice.

```js
export const light = { mood: "day", from: [880, 260] };          // the scene's one light (see Light and depth)
export const camera = (k) => [                                   // 2-3 shots (see Camera)
  { at: 0, zoom: 1, focus: [540, 1100] },
  { at: k.word("door", 1.2), zoom: 1.7, focus: [620, 950], move: "whip" },
];
export default function scene(k, t) {
  // t = seconds since the opener started. Draw back to front: sky, far things, k.depth(), ground, things, people, effects.
}
```

The look we want is CLEAN (owner, 2026-11-05, after a top cartoon-explainer Short): one big subject, a camera that
keeps moving and cuts closer on the strange detail, one warm or cool light over everything, the background soft and
hazy so the subject pops, and NO words in the picture. Clean beats busy: fewer, bigger things.

Rules for the code:
- Only `k.*` calls, arithmetic, `Math.*`, `const`/`let`, `if`, `for`, arrow functions. No `import`, `require`,
  `process`, `fs`, `fetch`, `eval`, `Function`, `globalThis`, `this`, `Date`, `k.ctx`, `k.pen`, `Math.random`
  (the same frame must always draw the same picture: vary things with `k.noise(x)` or by index instead).
- Everything is a pure function of `t`: never keep state between frames.
- The screen: x 0..1080, y 0..1920, and the picture FILLS it: the main things span roughly **y 300..1650** and
  most of the width (a vertical phone frame with an empty bottom half looks distant and gets rejected). Put the
  ground line low (about y 1500-1650) and build up from it. Faces must stay clear of the captions (y 1170-1300)
  in every shot (a close shot moves things: check where the face lands); limbs, bodies and props may cross them.
  Keep main things at least 40 px inside the left and right edges.
- Frame 0 must already show the subject and what is strange about it (open in the middle of the moment; nothing
  pops in from an empty frame). Lock each beat to its spoken word with `k.word("brass")` (that word's start time).
- Big and few: 1-3 main things, large enough to read on a phone (a person at s 1.6-2.4, about 400-590 px tall;
  a ship at s 1.5-1.7).
- **No labels, signs, captions or speech bubbles.** The captions already say the words; a label naming a thing
  ("WOODEN EAGLE", "AMBASSADOR", "GROCER", "BORROW ROOM?") makes the picture look like a diagram. A thing a stranger
  might not recognise is made clear by drawing it BIG and cutting the camera close to it on its spoken word, by its
  shape and by what the person does with it. Leave out `label`, `title`, `k.sign`, `k.text` and `k.bubble`
  unless the writing itself is the strange thing (a forged letter's one line) and the story says it.
- Animals and people come from the kit (`k.horse`, `k.dog`, `k.person`...), never assembled from your own shapes:
  a hand-built horse of boxes read as a cardboard donkey. Pose them with the part's options (`tap`, `walk`, `arms`).
- Solid things stay solid. A hand that touches something (knocks on a door, shakes a hand, holds what another holds)
  uses `reach` to the point on its surface, never arm angles guessed by eye: the McLean messenger's fist went through
  the door. Knock = move the target out and back: `reach: [null, [doorX - 30 * Math.abs(k.wave(3, 1)), 930]]`.
  Inside and outside in one picture = a cutaway: draw the wall between them (a thick edge with the doorway in it),
  and each person stays on their own side of it.

## Camera
`export const camera = (k) => [shot, ...]`: 2-3 shots for an opener (a new framing every 1-1.5 s, like a real edit).
A shot: `{at: seconds, zoom: 1..2.6, focus: [x, y], move}`. `focus` is the point the camera zooms toward (it stays
put on screen); zoom 1 = the whole picture. `move` says how this shot arrives: "cut" (instant), "whip" (a fast
0.28 s swing with motion blur: the energetic default), "push" (a slow glide until the next shot). Every shot also
creeps in by itself, so the camera never stops. Use `k.word(...)` for `at`, so the cut lands on its word.
The usual pattern: shot 1 wide (zoom 1-1.15) shows who and where; on the strange word, whip in close (zoom 1.6-2.2)
to the strange detail (the face reacting, the object, the hand on the door). Frame 0 is still the subject.

## Light and depth
- `export const light = { mood, from }`: mood "day" | "golden" | "dusk" | "night" | "interior" (lamp-lit room);
  `from` = where the light comes from on screen (the sun, a window, a lamp). The whole frame is graded with it,
  and people and animals cast a soft ground shadow away from it. Pick the mood the story's moment had.
- `k.depth(amount)` (0.5-1.2): call it once, right after the far things (sky, hills, distant buildings, the far
  wall): everything drawn so far goes soft and hazy, so the near subject pops. Never call it after the subject.
- `k.shadow(x, y, w)` a ground shadow under a prop you place (people and animals have their own).
- `k.dust(strength)` slow motes floating in the light (outdoors, dusty rooms, sunbeams): 0.4-1.
- `k.rays(x, y, {angle, count, width, length, strength})` soft light shafts from a window or gap (angle in
  degrees: 90 = straight down, 120 = down to the left). Draw them after the room, before people.

## Timing helpers
- `k.word(w, fallback)` start time of the first spoken word that begins with `w` (seconds), else `fallback`.
- `k.ss(a, b)` 0 before a, smoothly 1 at b. `k.ease(a, b)` the same, fast then slow. `k.pop(t0)` overshooting
  0->1 pop from t0 (scale a thing in with it). `k.wave(hz, amp, phase)` a sine. `k.noise(x)` -1..1 smooth noise.
- `k.lerp(a, b, f)`, `k.clamp(x, a, b)`.
- `k.fall(y0, y1, t0, dur)` y of a dropped thing (accelerating). `k.arc(from, to, t0, dur, height)` [x, y] of a
  thrown thing.

## Backgrounds (draw first)
- `k.sky(kind, horizon)` kind: "day" | "hot" | "dusk" | "night" (stars) | "overcast" | "snow" | "storm".
- `k.sun(x, y, r, {heat: 0..1})` heat swells it and adds rays. `k.moon(x, y, r)`. `k.cloud(x, y, s)`.
- `k.hills(y, color)` far hills. `k.sea(horizon, {glare: sunX})` sea with moving waves (and the sun's reflection).
- `k.ground(y, kind)` kind: "grass" | "sand" | "dirt" | "snow" | "street" | "floor".
- `k.room(floorY, {wall, window: [x, y] | false, outside})` an interior: wall, floorboards, a window.

## People
`const pp = k.person(x, y, s, o)` stands on (x, y); about 245*s px tall. Returns `{head: [x, y], top: [x, y],
hands: [[lx, ly], [rx, ry]]}` in screen space, for held props, sweat and bubbles.
o: `hat` (tricorn | top | bowler | crown | bonnet | cap | helmet | pith | fez | turban | peci | fedora | flatcap |
boater | cowboy | ranger (campaign hat) | kepi | officer (peaked cap) | bobby (police helmet) | bicorne | nurse |
hardhat | none; `hatColor` recolours most, `band` the fedora/boater/officer band), `coat`
(colour), `dress` (colour: a skirt), `skin` (`k.SKIN[0..5]`), `beard` (true | colour), `mustache`, `glasses`
("round" | "sun"), `face` ("smile" | "open" | "sad" | "flat"), `arms: [left, right]` (degrees from hanging
down, outward positive: 160 = raised overhead), `bend: [l, r]` (elbow degrees), `reach: [[x, y] | null, [x, y] | null]`
(left, right: that hand lands exactly on the point, overriding arms/bend; out of reach it points at it), `walk` (phase: `t * 9` walks),
`flip` (face left), `still`, `look` (eye shift px).
Arms that read: one arm doing the action (pointing, knocking, raised while speaking) and the other either on the hip
(`arms: [35, ...], bend: [-75, ...]`: the elbow sticks out, it reads as attitude) or hanging (`[12, ...], [6, ...]`).
Never cross an arm in front of the body (negative arms): on a stick figure it reads as a line drawn on the coat.
`k.crowd(x0, x1, y, count, s, {hats: [...], face, arms})` a row of people; returns their positions.

## Animals (stand on (x, y); face right, `flip: true` faces left; `walk: t * 9` walks)
`k.dog`, `k.chicken` (`headless: true`, `flap: true`), `k.cow`, `k.pig`, `k.cat` (about 120*s tall), `k.rabbit`
(sitting, 175*s with ears), `k.bear` (on all fours, 230*s tall, 340*s long) (x, y, s, o; `color`);
`const h = k.horse(x, y, s, o)` about 350*s px tall, 370*s long; o: `color`, `mane`, `walk`, `tap: [k.word("four"),
...]` (the near forehoof lifts and strikes the ground at each time: a counting horse, a pawing horse). Returns
`{hoof, head}` in screen space: `k.puff(h.hoof[0], h.hoof[1], .6, strikeTime)` for dust where it lands;
`k.bird(x, y, s)` a flying gull shape (move x/y yourself).

## Vehicles and buildings (stand on (x, y))
- `k.ship(x, waterline, s, {masts: 1-3, sails, sail, hull, flag})` about 600*s wide, 700*s tall; returns
  `{deck, left, right}` (draw cargo on `deck` AFTER the ship). `k.boat(x, waterline, s)` a rowboat.
- `k.cart(x, y, s, {roll: 1})` returns `{bed}`. `k.house(x, y, s, {wall, roof, lit})`. `k.shop(x, y, s, {sign})`.
  `k.bank(x, y, s, {sign})` (columns). `k.factory(x, y, s)` (smoking chimney). `k.tank(x, y, s, {label, burst:
  0..1})` a storage tank. `k.tower(x, y, s)` an iron lattice tower (900*s tall). Buildings return `{top}`.

## Nature
`k.palm(x, y, s)`, `k.tree(x, y, s, {color})`, `k.pine(x, y, s)`, `k.island(x, y, width)` (returns `{top}`).

## Rooms and furniture (stand on (x, y) unless said)
`const d = k.door(x, y, s, {open: 0..1, color, inside})` 290*s tall; returns `{knob, top, left, right}` (a knock:
`reach` to `d.knob` or the panel). `const b = k.bed(x, y, s, {canopy: true | colour, sheet, blanket})` 450*s long,
headboard left; returns `{top, pillow}`. `k.rug(cx, cy, width, {color, trim})` flat on the floor.
`k.shelf(x, y, s)` a bookcase (380*s tall). `const l = k.lamp(x, y, s, {kind: "desk" | "oil" | "floor", lit, shade})`
glows when lit; returns `{light}` (use it as `light.from`). `k.window(cx, cy, w, h, {outside, curtains})` and
`k.frame(cx, cy, w, h, {kind: "portrait" | "landscape", color})` on a wall. `k.phone(x, y, s)` a candlestick
telephone (returns `{mouth, ear}`), `k.radio(x, y, s)` a 1930s cathedral radio (returns `{top, speaker}`),
`k.letter(cx, cy, s, rotation)` a sealed envelope.

## Props (stand on (x, y) unless said)
`k.crate(x, y, w, h, {label})`, `k.barrel(x, y, s)`, `k.sack(x, y, s, {label})`, `k.coins(x, y, count, s)` a pile,
`k.coin(cx, cy, r)`, `k.moneybag(x, y, s, {label})`, `k.banknote(cx, cy, s, rotation)`,
`k.paper(cx, cy, s, {title, lines, seal, rot})` a document, `k.cup(x, y, s, {steam, drink: colour})`,
`k.bottle(x, y, s, {label})`, `k.table(x, y, width)` returns `{top}`, `k.chair(x, y, s)`, `k.sign(x, y, text)`,
`k.clock(cx, cy, r, {hour, minute})`, `k.fire(x, y, s)`.

## Effects (t0 = when it starts; each plays briefly, call it every frame)
`k.glint(x, y, size, t0)` a sparkle, `k.sweat(x, y, t0, s)` drops flying off a head, `k.shimmer(x0, x1, y,
strength)` heat haze, `k.speed(x, y, dir, count, len)` motion lines (dir -1 = lines trail to the left),
`k.burst(x, y, r, t0)` an impact, `k.puff(x, y, s, t0)` a dust/smoke puff, `k.smoke(x, y, s)` rising smoke,
`k.splash(x, y, t0, s, colour)`, `k.question(x, y, size, t0)`, `k.exclaim(x, y, size, t0)`,
`k.bubble(x, y, text, {size, t0, tail: -1 | 1})` a speech bubble (only words the narration says),
`k.rain(strength)`, `k.snowfall(strength)`, `k.flood(frontX, surfaceY, {color})` a liquid mass from the left edge.

## Drawing your own thing (when no part fits)
`k.shape(points, colour)` a painted shape with an ink outline (points = [[x, y], ...]; up to 6 points stay
sharp-cornered, more are smoothed). `k.disc(x, y, r, colour)`. `k.ink(points, {w, color})` a brush line.
`k.text(str, x, y, {size, font: "serif" | "sans-serif", color})` (only when the writing itself is the strange thing). `k.oval(x, y, rx, ry)` and
`k.rect(x, y, w, h)` return points. `k.at(x, y, s, rotation, () => { ... })` draws inside a moved, scaled, rotated
frame (for spinning, tipping or growing a group of parts). `k.fade(alpha, () => { ... })` draws them see-through
(0..1: fade things in or out). Colours: `k.C.ink, paper, brass, gold, wood, plank,
sail, sea, deep, sand, grass, leaf, brick, roof, stone, navy, red, white, sky, snow, molasses, water, fire, smoke,
money`, or any "#RRGGBB".

## Example (the approved look: "He shipped brass bed warmers straight to the tropical Caribbean.")
```js
export const light = { mood: "golden", from: [860, 380] };
export const camera = (k) => [
  { at: 0, zoom: 1, focus: [540, 1150] },                                     // wide: the ship in the tropics
  { at: k.word("brass", .7), zoom: 1.8, focus: [560, 1180], move: "whip" },   // close: the brass pans glint
  { at: k.word("tropical", 2.1), zoom: 1.2, focus: [640, 900], move: "push" }, // back out to the blazing sun
];
export default function scene(k, t) {
  const hot = k.word("tropical", 2.1), heat = k.ss(hot - .1, hot + .6);
  k.sky("hot", 900); k.sun(860, 380, 110, { heat });
  k.sea(900, { glare: 860 });
  k.island(930, 905, 300); k.palm(900, 860, .55); k.palm(990, 865, .45);   // far away on the horizon
  k.depth(.8);                                                             // ...and out of focus
  const x = k.lerp(470, 520, t / 3.8), ship = k.ship(x, 1600, 1.6);
  const glint = k.word("brass", .7);
  [-300, -200, -40, 80, 250, 340].forEach((dx, i) => {               // bed warmers: long handles, round brass pans
    const px = x + dx, py = ship.deck - 330 - (i % 2) * 40;
    k.ink([[px, py], [px - 40, ship.deck]], { w: 12, color: k.C.wood });
    k.disc(px, py, 62, k.C.brass); k.ring(px, py, 40, 40, { w: 2.4, color: "#8A5A1A" });
    k.glint(px - 20, py - 22, 60, glint + i * .08);
  });
  const sailor = k.person(x - 330, ship.deck, 1.7, { hat: "tricorn", coat: k.C.navy, face: heat > .4 ? "open" : "smile",
    arms: [20, 150 + k.wave(2.5, 15) * heat], bend: [0, 30] });
  k.sweat(sailor.head[0], sailor.head[1] - 40, hot + .2, 1.6);
  k.crate(x + 60, ship.deck + 6, 330, 170);
  k.shimmer(80, 1000, 890, heat);
  k.dust(.7);
}
```
