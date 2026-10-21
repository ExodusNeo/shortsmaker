// Tests for remotion/src/full/guarded.tsx (arrow routing, layouts, travel speed). No rendering.
// Run: .venv\Scripts\python.exe tests\run_ts_tests.py  (bundles with Remotion's esbuild, runs with node)
import {MIN_MOVE, SAFE, boxAt, fitCard, layoutColumn, layoutGrid, layoutRow, routeArrow, travel} from '../remotion/src/full/guarded';
import type {Box} from '../remotion/src/full/guarded';

let failed = 0;
const test = (name: string, fn: () => void) => {
	try {
		fn();
		console.log(`PASS ${name}`);
	} catch (e) {
		failed++;
		console.log(`FAIL ${name}: ${(e as Error).message}`);
	}
};
const ok = (cond: boolean, msg: string) => {
	if (!cond) throw new Error(msg);
};

// does the polyline cross the inside of box b? (sampled every 2 px)
const crosses = (pts: [number, number][], b: Box) => {
	for (let i = 1; i < pts.length; i++) {
		const [p, q] = [pts[i - 1], pts[i]];
		const n = Math.ceil(Math.hypot(q[0] - p[0], q[1] - p[1]) / 2) + 1;
		for (let k = 0; k <= n; k++) {
			const x = p[0] + ((q[0] - p[0]) * k) / n;
			const y = p[1] + ((q[1] - p[1]) * k) / n;
			if (Math.abs(x - b.x) < b.w / 2 && Math.abs(y - b.y) < b.h / 2) return true;
		}
	}
	return false;
};
const inside = (b: Box) =>
	b.x - b.w / 2 >= SAFE.left - 0.01 && b.x + b.w / 2 <= SAFE.right + 0.01 && b.y - b.h / 2 >= SAFE.top - 0.01 && b.y + b.h / 2 <= SAFE.bottom + 0.01;

test('the Unsinkable Sam layout: no arrow crosses a card', () => {
	// two cards side by side on top, the third below the first: the arrow 2 -> 3 used to cut through card 3
	const c1 = boxAt(300, 330, 340, 130);
	const c2 = boxAt(760, 330, 340, 130);
	const c3 = boxAt(400, 560, 420, 150);
	const photo = boxAt(800, 560, 220, 260);
	for (const [a, b] of [[c1, c2], [c2, c3], [c3, photo]] as Box[][]) {
		const pts = routeArrow(a, b, [c1, c2, c3, photo]);
		for (const box of [c1, c2, c3, photo]) ok(!crosses(pts, box), `arrow crosses a box at ${JSON.stringify(box)}`);
	}
});

test('a column of cards gets straight vertical arrows', () => {
	const [a, b] = layoutColumn(2);
	const pts = routeArrow(a, b);
	ok(pts.length === 2 && pts[0][0] === pts[1][0], `expected a straight line, got ${JSON.stringify(pts)}`);
	ok(pts[0][1] > a.y + a.h / 2 && pts[1][1] < b.y - b.h / 2, 'arrow must start below a and end above b');
});

test('an arrow around a box sitting in the way', () => {
	const [a, mid, b] = layoutRow(3);
	const pts = routeArrow(a, b, [mid]);
	ok(!crosses(pts, mid), `arrow goes through the middle box: ${JSON.stringify(pts)}`);
});

test('layouts stay inside the stage and never overlap', () => {
	for (const boxes of [layoutRow(4), layoutColumn(5), layoutGrid(6, 3), layoutGrid(5, 2)]) {
		boxes.forEach((b, i) => {
			ok(inside(b), `box ${i} leaves the stage: ${JSON.stringify(b)}`);
			boxes.slice(i + 1).forEach((c) =>
				ok(Math.abs(b.x - c.x) >= (b.w + c.w) / 2 || Math.abs(b.y - c.y) >= (b.h + c.h) / 2, 'two boxes overlap'));
		});
	}
	ok(inside(boxAt(1050, 1300, 2000, 400)), 'boxAt must pull a box back inside the stage');
});

test('nothing travels faster than MIN_MOVE', () => {
	const short = travel(10.0 + MIN_MOVE / 2, 10.0, [100, 400], [160, 400]);
	ok(short.k < 0.9, `a 60 px hop is already ${short.k} done halfway through MIN_MOVE`);
	ok(short.end - 10.0 >= MIN_MOVE, 'trip shorter than MIN_MOVE');
	const long = travel(10.0, 10.0, [100, 300], [900, 1000]);
	ok(long.end - 10.0 > MIN_MOVE, 'a long trip should take longer than the minimum');
});

test('card text always fits its box (Hatfield cards were cut off)', () => {
	const cases: [Box, string, string | undefined, string | undefined][] = [
		[boxAt(540, 400, 300, 110), '$10,000', 'promised by the city', 'The deal'], // small card: label + title + sub
		[boxAt(540, 400, 300, 110), 'Dam breaks', 'Feb 1916', 'Then'],
		[boxAt(540, 400, 640, 200), 'Ark Royal torpedoed', 'November 1941', 'Ship 3'],
		[boxAt(540, 400, 220, 90), 'A very long title that cannot possibly fit', 'and a sub line', 'step'],
	];
	for (const [box, title, sub, step] of cases) {
		const f = fitCard(box, title, sub, step);
		ok(f.height <= box.h - 8, `"${title}" needs ${f.height}px in a ${box.h}px card`);
		ok(f.titleSize >= 26, `"${title}" title shrank to ${f.titleSize}px (unreadable)`);
	}
	const big = fitCard(boxAt(540, 400, 640, 200), 'Ark Royal torpedoed', 'November 1941', 'Ship 3');
	ok(big.showSub && big.showStep, 'a roomy card keeps its label and sub-line');
});

console.log(failed ? `${failed} failed` : 'all passed');
process.exit(failed ? 1 : 0);
