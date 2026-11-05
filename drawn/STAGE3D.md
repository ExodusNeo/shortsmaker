# 3D opener stage

You stage scene 1 of a YouTube Short as a short 3D shot: flat hand-drawn cut-outs (people, animals, the strange
object) standing inside a lit 3D set, filmed by a moving camera. You do not model anything: you pick the place, put
furniture from the prop list in it, draw the cut-outs with the drawing kit, and aim the camera. The look we want is
CLEAN: one big subject, a camera that keeps moving and cuts closer on the strange detail, one light mood, NO words.

Reply with ONE JSON object:
```json
{"moment": "one sentence: what the shot shows",
 "place": "room", "mood": "interior", "colors": {"wall": "#7E5A40", "floor": "#5A3820"},
 "props": [...], "cutouts": [...], "shots": [...], "effects": [...]}
```

**Frame 0 must already show what is strange**, in the middle of the moment: a stranger decides in the first second.
When an effect IS the strange thing (the rings out of the eagle, the shaking, the rain), start it at 0, and let its
spoken word make it stronger (a second effect, a whip in close). Nothing waits for its word to appear.

## Places (units are metres; y is up; the camera looks toward -z)
- `"room"`: an interior 8 m wide (x -4..4), 4.4 m high. The back wall is at z = -4, side walls at x = -4 and 4,
  the open side faces the camera (+z). Put the action between z = -3 and z = 0. `colors`: wall, floor, trim.
- `"street"`: a town street running away from the camera, rows of plain buildings on both sides (x = +-5.2).
  The road is x -3..3. `colors`: ground, sky.
- `"outdoors"`: open ground with far hills and sky. `colors`: ground, sky.
`mood`: "day" | "golden" | "dusk" | "night" | "interior" (a lamp-lit room). It sets the light, shadows, fog and grade.

## Props (`{"type", "at": [x, z], "turn": degrees, "size": 1, "color": "#RRGGBB", "id": "name"}`)
Each stands on the floor at `at`, facing the camera; `turn` spins it (90 = faces +x); `y` lifts it (a lamp on a desk:
`"y": 0.86`). `"wall": true` hangs it on the room's back wall with `at` = [x, height of its centre].
Give a prop an `id` when a shot or effect aims at it.
- room: `desk` (2.3 x 1 m, top at 0.86), `table` (1.6 x 0.9, top 0.8), `chair`, `door` (`open`: 0..1; put it on the
  back wall line: `at: [x, -3.95]`), `window` (use `"wall": true`, e.g. `at: [-2.2, 2.4]`), `frame` (a picture,
  wall), `shelf` (bookcase 1.3 x 2.3 m), `lamp` (desk lamp, `lit`), `bed` (2 m long, headboard at the back),
  `rug`, `cabinet`, `counter` (3 m shop/bar counter), `fireplace` (glowing).
- anywhere: `crate`, `barrel`, `rock`, `tree`, `fence` (`length`), `lamppost` (`lit`).
- street / outdoors: `house` (4 x 4 m, pitched roof; lit windows at night), `shopfront`.
Keep it to the few props the moment needs: a clean set, not a cluttered one.

## Cut-outs (the people, animals and the strange object)
```json
{"name": "amb", "w": 700, "h": 1100, "frames": 4, "height": 1.75, "at": [0, -1.75],
 "talk": ["ambassador", "word"], "code": "export default function draw(k, f) { ... }"}
```
- `code` draws the cut-out with the drawing kit (the manual below) on a transparent `w` x `h` pixel canvas, the
  thing standing on the bottom centre (a person: `k.person(w / 2, h - 20, s, {...})`; s = 4 fills 1100 px).
  `f` = which drawing (0..frames-1). Use only the kit's parts and plain shapes: no backgrounds, sky, ground, room,
  camera, light or depth calls (the 3D set does those), and no words.
- `height` = how tall it stands in the set, in metres (a person 1.75, a dog 0.6, a horse 1.7); its width follows
  the canvas shape. `at` = [x, z] where it stands. `"wall": true` hangs it on the back wall (`at` = [x, centre height]):
  a painting, a carved seal, a clock.
- Moving: `frames` 2-4 drawings that differ (mouth open/shut, arm up/down) cycle at `fps` (default 7) while
  `talk` = [from, to] (a spoken word or seconds); otherwise drawing 0 shows. `path`: [[time, x, z], ...] slides it
  across the set (a walk, a run, a fall forward). `flip: true` mirrors it.
- People: one arm doing the action, the other on the hip (`arms: [35, ...], bend: [-75, ...]`) or hanging.
- **Things that touch go in ONE cut-out.** A thing someone holds (a letter, a cup, a lamp) is drawn inside that
  person's cut-out, at the hand the kit returns (`const pp = k.person(...); k.letter(pp.hands[1][0], pp.hands[1][1], ...)`).
  A hand on something (knocking on a door, a hand on a horse, two people shaking hands) = draw both in the same
  cut-out with the kit's `reach` (`const d = k.door(...); k.person(..., {reach: [null, d.knob]})`): a flat cut-out
  never touches a 3D prop exactly (a live McLean draft's fist went straight through the 3D door). Use 3D props for
  the room around the action, not for what the action touches. A separate cut-out is a board standing on the floor
  or hanging on the wall: never a thing in mid-air (a live draft's sheet of paper floated before the ambassador).
- Nobody stands hidden behind furniture: a desk or counter in front of a person turns half the frame into a dark
  wooden wall (a live draft's wide shot was one third desk front). Put furniture beside or behind people, or have
  them stand in front of it.

## Shots (2-3; a new framing every 1-1.5 s)
`{"at": 0 | "word", "target": "<cut-out name or prop id>", "distance": 3.5, "height": 0.2, "turn": 15, "fov": 55, "move": "whip"}`
The target sits in the middle of the frame. A list (`"target": ["messenger", "grocer"]`) aims between them and
stands back far enough to keep all of them inside the frame: use it whenever a shot must show two things, or one
gets cut off at the edge (a live McLean draft lost the grocer off the right side). `distance` metres from it, `height` above it, `turn` degrees around it
(positive = from the right). `fov` 45-62 (portrait frames need a wide one to show the set). `move` = how this shot
arrives: "cut", "whip" (fast swing: the energetic default), "push" (slow glide). Every shot also creeps in.
Shot 1 (at 0) wide enough to show who and where (distance 3-5); on the strange word, whip in close to the strange
detail (distance 1.2-2.5). Aim at people, not at their feet: the captions sit a little below the middle.
Fill the tall frame: the subject and what is strange about it span most of its height in every shot. A wide shot
taken a little from above (`height` 0.6-1.2) shows floor and tabletops instead of a band of empty front; a
person plus a thing on the wall above them fits when the camera stands back (distance 3.5-4.5, fov 58-62).

## Effects
`{"type": "rings", "at": "broadcasts", "on": "eagle"}` sound/radio rings rolling out of a thing; `"burst"` an
impact flash (`at`, `on`); `"shake"` the camera jolts (`at`); `"dust"` motes in the light; `"shafts"` light beams
from the room's window; `"rain"`, `"snow"`.

## Example: "The ambassador speaks, and his wooden eagle broadcasts every word."
```json
{"moment": "The ambassador talks at his desk while the carved eagle on the wall above him sends out radio rings",
 "place": "room", "mood": "interior", "colors": {"wall": "#7E5A40", "floor": "#5A3820"},
 "props": [{"type": "desk", "at": [1.4, -2.6], "turn": -20}, {"type": "lamp", "at": [2.0, -2.6], "y": 0.86, "lit": true},
   {"type": "window", "wall": true, "at": [-2.2, 2.4]}, {"type": "shelf", "at": [3.2, -3.5], "turn": -90},
   {"type": "rug", "at": [0, -1.4]}],
 "cutouts": [
   {"name": "amb", "w": 700, "h": 1100, "frames": 4, "height": 1.76, "at": [-0.3, -1.6], "talk": ["ambassador", 4.4],
    "code": "export default function draw(k, f) { k.person(350, 1080, 4, { coat: k.C.navy, skin: k.SKIN[1], face: f % 2 ? 'smile' : 'open', arms: [35, [110, 128, 140, 118][f]], bend: [-75, 46], still: true }); }"},
   {"name": "eagle", "w": 760, "h": 640, "frames": 1, "height": 1.47, "wall": true, "at": [0, 2.67],
    "code": "export default function draw(k, f) { k.at(380, 300, 1.15, 0, () => { k.shape([[-42, -18], [-295, -135], [-275, -66], [-230, -20], [-175, 20], [-60, 40]], k.C.wood); k.shape([[42, -18], [295, -135], [275, -66], [230, -20], [175, 20], [60, 40]], k.C.wood); k.shape([[-64, -26], [64, -26], [58, 64], [0, 112], [-58, 64]], k.C.plank); k.shape([[-30, -24], [30, -24], [24, -108], [-16, -122], [-42, -90]], k.C.wood); k.shape([[-32, -104], [-74, -88], [-62, -70], [-30, -76]], k.C.brass); k.disc(-18, -98, 5.5, k.C.ink); }); }"}],
 "shots": [{"at": 0, "target": "amb", "distance": 3.9, "height": 0.9, "turn": 12, "fov": 60},
   {"at": "eagle", "target": "eagle", "distance": 2.6, "height": -0.2, "turn": 8, "fov": 48, "move": "whip"}],
 "effects": [{"type": "rings", "at": 0, "on": "eagle"}, {"type": "rings", "at": "broadcasts", "on": "eagle"}, {"type": "dust"}, {"type": "shafts"}]}
```
