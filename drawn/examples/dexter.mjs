// KIT.md's example, rendered by tests/test_drawn_opener.py
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
