import React from 'react';
import {Card, Connect, CustomFull, FullProps, Paper, PhotoCutout, StampBadge, TitleBanner, boxAt, cueAt, focusCam, layoutRow, photoBox, skinOf} from '../toolkit';

// EXAMPLE (shown to the custom-scene coder): one real photo and two facts that point at it. The photo's outline
// comes from photoBox() so <Connect> can route to it and around it; cards come from layoutRow(); with no photo,
// a big Card takes the photo's place. One idea, few elements, generous spacing.
export const ExampleEvidence: React.FC<FullProps<CustomFull>> = ({full, t, start, end}) => {
	const sk = skinOf(full.skin);
	const photo = full.photos?.[0];
	const c = [0, 1, 2].map((i) => cueAt(full, i, start, end, 3));
	const pb = photo ? photoBox(photo.aspect, 540, 470, 420) : boxAt(540, 430, 560, 260);
	const facts = layoutRow(2, {y: 790, h: 170}); // leaves room under the facts for the stamp
	const all = [pb, ...facts];
	return (
		<Paper t={t} start={start} seed={full.seed} cam={focusCam(540, 620, 1.0)} skin={full.skin}>
			<TitleBanner title={full.title || 'TWO CATS CALLED OSCAR'} sub="WHAT THE PHOTOS SHOW" t={t} at={start + 0.05} skin={full.skin} />
			{photo ? (
				<PhotoCutout photo={photo} x={540} y={470} w={420} rot={-2} label={photo.label} t={t} at={c[0]} skin={full.skin} />
			) : (
				<Card box={pb} title="Oscar" sub="the ship's cat" t={t} at={c[0]} skin={full.skin} />
			)}
			<Card box={facts[0]} title="Black and white" sub="photo, 1941" t={t} at={c[1]} skin={full.skin} />
			<Card box={facts[1]} title="Mostly black" sub="photo, 1942" t={t} at={c[2]} skin={full.skin} highlight />
			<Connect from={pb} to={facts[0]} avoid={all} t={t} at={c[1] + 0.25} skin={full.skin} />
			<Connect from={pb} to={facts[1]} avoid={all} t={t} at={c[2] + 0.25} skin={full.skin} />
			<StampBadge text="NOT THE SAME CAT" x={540} y={965} rot={-6} t={t} at={c[2] + 0.9} color={sk.accent} />
		</Paper>
	);
};
