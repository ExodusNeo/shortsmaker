// KIT.md's worked example (an invented story, 2026-11-06: no posted Short is used as a reference):
// "A captain sailed a whole cargo of umbrellas into a desert port where it never rains."
export const light = { mood: "golden", from: [860, 380] };
export const camera = (k) => [
  { at: 0, zoom: 1, focus: [540, 1150] },                                        // wide: the ship in the scorching port
  { at: k.word("umbrellas", .9), zoom: 1.8, focus: [520, 1180], move: "whip" },  // close: the open umbrellas on deck
  { at: k.word("never", 2.4), zoom: 1.2, focus: [640, 900], move: "push" },      // back out to the blazing sun
];
export default function scene(k, t) {
  const dry = k.word("never", 2.4), heat = k.ss(dry - .1, dry + .6);
  k.sky("hot", 900); k.sun(860, 380, 110, { heat });
  k.sea(900, { glare: 860 });
  k.island(930, 905, 300); k.palm(900, 860, .55);                          // the dry port on the horizon
  k.depth(.8);                                                             // ...and out of focus
  const x = k.lerp(470, 520, t / 3.8), ship = k.ship(x, 1600, 1.6);
  const pop = k.word("umbrellas", .9);
  [-300, -170, -40, 90, 220, 340].forEach((dx, i) => {                     // open umbrellas fill the deck from frame 0...
    const ux = x + dx, uy = ship.deck - 300 - (i % 2) * 50, at = pop + i * .07;
    const g = 1 + .25 * (k.ss(at, at + .12) - k.ss(at + .12, at + .3));    // ...and bounce one by one on their word
    k.ink([[ux, uy], [ux, ship.deck]], { w: 8, color: k.C.ink });
    k.at(ux, uy, g, 0, () => k.shape([[-90, 20], [-70, -30], [0, -60], [70, -30], [90, 20]], [k.C.red, k.C.navy, "#E3B64B"][i % 3]));
  });
  const captain = k.person(x - 330, ship.deck, 1.7, { hat: "tricorn", coat: k.C.navy, face: heat > .4 ? "open" : "smile",
    arms: [35, 150 + k.wave(2.5, 15) * heat], bend: [-75, 30] });
  k.sweat(captain.head[0], captain.head[1] - 40, dry + .2, 1.6);
  k.crate(x + 60, ship.deck + 6, 330, 170);
  k.shimmer(80, 1000, 890, heat);
  k.dust(.7);
}
