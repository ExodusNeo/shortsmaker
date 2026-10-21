import React from 'react';
import {Card, Connect, CustomFull, FullProps, Paper, StampBadge, TitleBanner, cueAt, focusCam, layoutColumn, skinOf, travel} from '../toolkit';

// EXAMPLE (shown to the custom-scene coder): a chain of events. Boxes come from a layout helper, arrows from
// <Connect> (they route around every box listed in `avoid`), and the marker moves with travel(), which never
// goes faster than MIN_MOVE. Every element lands on a spoken beat (cueAt) and then holds still to be read.
export const ExampleChain: React.FC<FullProps<CustomFull>> = ({full, t, start, end}) => {
	const sk = skinOf(full.skin);
	const steps = ['Bismarck sinks', 'Cossack torpedoed', 'Ark Royal torpedoed'];
	const subs = ['May 1941', 'October 1941', 'November 1941'];
	const boxes = layoutColumn(3, {w: 640, bottom: 900}); // leaves room under the chain for the stamp
	const c = [0, 1, 2].map((i) => cueAt(full, i, start, end, 3));
	// the marker waits beside card 1, then walks down the left side to each card as it is named
	const side = (i: number): [number, number] => [boxes[i].x - boxes[i].w / 2 - 70, boxes[i].y];
	const leg1 = travel(t, c[1] - 0.2, side(0), side(1), {arc: 40});
	const leg2 = travel(t, c[2] - 0.2, side(1), side(2), {arc: 40});
	const pos = t < c[2] - 0.2 ? leg1 : leg2;
	return (
		<Paper t={t} start={start} seed={full.seed} cam={focusCam(540, 640, 1.0)} skin={full.skin}>
			<TitleBanner title={full.title || 'ONE CAT, THREE SHIPS'} sub="MAY - NOV 1941" t={t} at={start + 0.05} skin={full.skin} />
			{boxes.map((b, i) => (
				<Card key={i} box={b} step={`Ship ${i + 1}`} title={steps[i]} sub={subs[i]} t={t} at={c[i]} skin={full.skin} highlight={i === 2} />
			))}
			<Connect from={boxes[0]} to={boxes[1]} avoid={boxes} t={t} at={c[1] - 0.35} skin={full.skin} />
			<Connect from={boxes[1]} to={boxes[2]} avoid={boxes} t={t} at={c[2] - 0.35} skin={full.skin} />
			{t >= c[0] ? (
				<div
					style={{
						position: 'absolute', left: pos.x - 26, top: pos.y - 26, width: 52, height: 52, borderRadius: 26,
						background: sk.accent, border: `4px solid ${sk.ink}`,
					}}
				/>
			) : null}
			<StampBadge text="SURVIVED" x={540} y={965} rot={-8} t={t} at={c[2] + 0.6} color={sk.accent} />
		</Paper>
	);
};
