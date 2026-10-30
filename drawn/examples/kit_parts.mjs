// Every kit part, one page per second (tests/test_drawn_opener.py --look renders a sheet of it).
export const camera = { zoom: [1, 1] };
export default function scene(k, t) {
  const page = Math.floor(t);
  if (page === 0) {            // people and hats
    k.sky("day"); k.ground(1500, "grass");
    k.HATS.forEach((hat, i) => k.person(140 + (i % 4) * 270, 600 + Math.floor(i / 4) * 450, .8, { hat, coat: [k.C.navy, k.C.red, "#5E7A5A", "#7A5A3A"][i % 4], skin: k.SKIN[i % 6], still: true }));
    k.text("hats", 540, 120, { size: 50 });
  } else if (page === 1) {     // more people options and a crowd
    k.room(1350);
    k.person(200, 900, 1, { hat: "bonnet", dress: "#8A5A9A", face: "open", arms: [150, 20], bend: [30, 0] });
    k.person(520, 900, 1, { hat: "top", beard: true, coat: "#2B2622", mustache: true, arms: [20, 160], bend: [0, -40] });
    const p = k.person(850, 900, 1, { hat: "crown", coat: k.C.red, walk: t * 9, flip: true }); k.cup(p.hands[1][0], p.hands[1][1] + 40, .5, { steam: true });
    k.crowd(120, 960, 1300, 6, .7, { hats: ["bowler", "cap", "none"] });
  } else if (page === 2) {     // animals
    k.sky("day"); k.ground(1400, "dirt");
    k.dog(220, 650, 1, { walk: t * 10 }); k.chicken(640, 650, 1.2, {}); k.chicken(900, 650, 1.2, { headless: true, flip: true, walk: t * 10 });
    k.horse(300, 1100, 1, { walk: t * 8 }); k.cow(780, 1100, .9, { flip: true });
    k.pig(300, 1400, 1, {}); k.bird(700, 1300, 1.2); k.bird(850, 1250, .8);
  } else if (page === 3) {     // buildings
    k.sky("dusk"); k.hills(1200); k.ground(1500, "street");
    k.house(250, 800, .9, { lit: true }); k.shop(760, 800, .9, { sign: "GROCER" });
    k.bank(260, 1450, .9, { sign: "BANK" }); k.factory(780, 1450, .8); k.moon(900, 250);
  } else if (page === 4) {     // sea, ships, nature
    k.sky("hot"); k.sun(820, 330, 100, { heat: 1 }); k.sea(1000, { glare: 820 });
    k.island(830, 1000, 380); k.palm(800, 960, .9); k.ship(380, 1160, 1, { masts: 2 }); k.boat(800, 1400, 1);
    k.tank(180, 700, .5, { label: "MOLASSES" }); k.tower(520, 950, .5); k.cloud(300, 240, 1);
  } else {                     // props and effects
    k.room(1500, { window: false });
    k.table(540, 1500, 700); k.coins(300, 1300, 10); k.moneybag(540, 1310, .9); k.cup(740, 1320, 1, { steam: true, drink: k.C.molasses });
    k.crate(160, 900, 180, 130, { label: "TEA" }); k.barrel(400, 900); k.sack(600, 900, 1, { label: "FLOUR" }); k.bottle(800, 900); k.banknote(940, 820, .8, .3);
    k.paper(200, 500, .8, { title: "DEED", seal: true, rot: -.1 }); k.clock(480, 450, 90); k.sign(800, 650, "FOR SALE"); k.fire(980, 1100, .8);
    k.bubble(540, 220, "WHAT?!", { size: 50 }); k.question(900, 260, 100); k.exclaim(140, 230, 100);
    k.glint(400, 1250, 50, page + .1); k.burst(540, 700, 120, page + .1); k.puff(940, 1060, 1, page); k.splash(300, 1150, page + .1); k.sweat(560, 380, page + .05);
  }
}
