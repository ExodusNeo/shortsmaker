import React from 'react';
import {
	CalloutTag,
	CustomFull,
	Easing,
	FlowArrow,
	FullProps,
	Paper,
	PhotoCutout,
	StampBadge,
	TitleBanner,
	clamp,
	cueAt,
	focusCam,
	interpolate,
	skinOf,
} from '../toolkit';

/** Custom 1 (Cutout photo collage, dossier skin): Real archival photos sliding in with drawn arrows,
 * callout tags and a rubber-stamp verdict, all staying above the captions (y <= 1060). */
export const Custom1: React.FC<FullProps<CustomFull>> = ({full, t, start, end}) => {
	const sk = skinOf(full.skin ?? 'dossier');
	const c0 = cueAt(full, 0, start, end, 3);
	const c1 = cueAt(full, 1, start, end, 3);
	const c2 = cueAt(full, 2, start, end, 3);
	const p0 = full.photos?.[0];
	const p1 = full.photos?.[1];
	const p2 = full.photos?.[2];

	// Camera glides from print 1 -> print 2 -> pull back to the whole collage centred at screen y=630
	const fx = interpolate(t, [start, c0 + 0.4, c1 + 0.4, c2 + 0.4], [320, 310, 750, 540], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const fy = interpolate(t, [start, c0 + 0.4, c1 + 0.4, c2 + 0.4], [470, 470, 500, 620], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const fScale = interpolate(t, [start, c0 + 0.4, c1 + 0.4, c2 + 0.4], [1.14, 1.2, 1.18, 1.0], {...clamp, easing: Easing.inOut(Easing.cubic)});

	return (
		<Paper t={t} start={start} seed={full.seed} cam={focusCam(fx, fy, fScale)} skin={full.skin ?? 'dossier'}>
			<TitleBanner title={full.title || 'CASE FILE · SIGNALMAN JACK'} sub="ARCHIVAL PHOTO COLLAGE" t={t} at={start + 0.05} skin={full.skin ?? 'dossier'} />

			<PhotoCutout
				photo={p0}
				x={290}
				y={455}
				w={340}
				rot={-5}
				label={p0?.label || '1. CHACMA BABOON'}
				t={t}
				at={c0}
				skin={full.skin ?? 'dossier'}
			/>

			<FlowArrow x1={465} y1={445} x2={595} y2={485} curve={-35} t={t} at={c1 - 0.1} color={sk.accent} />

			<PhotoCutout
				photo={p1}
				x={775}
				y={490}
				w={340}
				rot={4}
				label={p1?.label || '2. UITENHAGE BOX'}
				t={t}
				at={c1}
				skin={full.skin ?? 'dossier'}
				highlight
			/>

			<FlowArrow x1={675} y1={640} x2={525} y2={745} curve={35} t={t} at={c2 - 0.1} color={sk.accent} />

			<PhotoCutout
				photo={p2}
				x={360}
				y={825}
				w={320}
				rot={-2}
				label={p2?.label || '3. AT THE LEVERS'}
				t={t}
				at={c2}
				skin={full.skin ?? 'dossier'}
			/>

			<CalloutTag
				x={785}
				y={785}
				toX={535}
				toY={815}
				text="OFFICIAL PAYROLL"
				sub="20 cents a day + beer"
				t={t}
				at={c2 + 0.2}
				skin={full.skin ?? 'dossier'}
				accent
			/>

			<StampBadge text="VERIFIED RECORD" x={730} y={965} rot={-8} t={t} at={c2 + 0.45} color={sk.accent} />
		</Paper>
	);
};
