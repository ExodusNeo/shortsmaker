// Tests for remotion/src/style (registry lookups, kit helpers, transitions). No rendering.
// Run: .venv\Scripts\python.exe tests\run_ts_tests.py
import {TRANSITIONS, lookFor, overlayFor, transitionFor} from '../remotion/src/style/index';
import {inksOf, noise} from '../remotion/src/style/kit';
import {transitionWindow} from '../remotion/src/style/window';

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

test('unknown transition falls back to fade', () => ok(transitionFor('nope') === TRANSITIONS.fade, 'not fade'));
test('missing transition falls back to fade', () => ok(transitionFor(undefined) === TRANSITIONS.fade, 'not fade'));
test('no look for null or unknown', () => ok(lookFor(null) === null && lookFor('nope') === null, 'got a look'));
test('no overlay for a built-in style', () => ok(overlayFor('fact') === null, 'got an overlay'));
test('inks come from the palette', () => {
	const k = inksOf({accent: '#FFD400', emphasis: '#FF7A1A', panel: '#0d1320'});
	ok(k.ink === '#0d1320' && k.accent === '#FFD400' && k.alarm === '#FF7A1A' && k.paper === '#EFE6D2', JSON.stringify(k));
});
test('noise is deterministic and in 0..1', () => {
	ok(noise(3, 0.5) === noise(3, 0.5), 'not deterministic');
	for (let i = 0; i < 50; i++) {
		const v = noise(i, i * 0.37);
		ok(v >= 0 && v < 1, `out of range ${v}`);
	}
	ok(noise(1, 0.5) !== noise(2, 0.5), 'seed ignored');
});
test('fade lasts 0.3 s, cut and flash are instant', () => {
	ok(TRANSITIONS.fade.duration === 0.3, `fade ${TRANSITIONS.fade.duration}`);
	ok(TRANSITIONS.cut.duration === 0 && TRANSITIONS.flash.duration === 0, 'cut/flash not instant');
});

test('fade window: lead 0.15 s, half way at the cut', () => {
	const w = transitionWindow({start: 4, transition: 'fade'});
	ok(Math.abs(w.lead - 0.15) < 1e-9, `lead ${w.lead}`);
	ok(Math.abs(w.p(4) - 0.5) < 1e-9 && w.p(3.8) === 0 && w.p(4.2) === 1, `p ${w.p(3.8)} ${w.p(4)} ${w.p(4.2)}`);
});
test('cut and flash windows are instant', () => {
	for (const transition of ['cut', 'flash']) {
		const w = transitionWindow({start: 4, transition});
		ok(w.lead === 0 && w.p(3.99) === 0 && w.p(4) === 1, transition);
	}
});
test('unknown transition window behaves like fade', () => {
	const w = transitionWindow({start: 4, transition: 'dissolve'});
	ok(Math.abs(w.lead - 0.15) < 1e-9 && Math.abs(w.p(4) - 0.5) < 1e-9, 'not fade');
});

const INKS = inksOf({accent: '#FFD400', emphasis: '#FF7A1A', panel: '#0d1320'});
const hidden = (s?: {opacity?: unknown}) => !!s && s.opacity === 0;
const shown = (s?: {opacity?: unknown}) => !s || s.opacity === undefined || s.opacity === 1;
for (const [name, duration, covers] of [['wipe', 0.44, true], ['whip', 0.25, false], ['leak', 0.5, true]] as const) {
	test(`${name}: ${duration}s, hides the new scene at the start and shows it at the end`, () => {
		const tr = TRANSITIONS[name];
		ok(!!tr, 'missing from the library');
		ok(tr.duration === duration, `duration ${tr.duration}`);
		ok(hidden(tr.render(0, INKS, 1).to), `start ${JSON.stringify(tr.render(0, INKS, 1).to)}`);
		ok(shown(tr.render(1, INKS, 1).to), `end ${JSON.stringify(tr.render(1, INKS, 1).to)}`);
		ok(!!tr.render(0.5, INKS, 1).cover === covers, `cover at the cut: ${!!tr.render(0.5, INKS, 1).cover}`);
	});
}

process.exit(failed ? 1 : 0);
