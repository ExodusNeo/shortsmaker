import React from 'react';
import {
	ClockDial,
	CustomFull,
	Easing,
	FullProps,
	Paper,
	PhotoCutout,
	SERIF,
	StampBadge,
	TYPE,
	TitleBanner,
	appear,
	clamp,
	cueAt,
	focusCam,
	interpolate,
	skinOf,
} from '../toolkit';

/** Custom 3 (Animated clock & signal levers, parchment skin): Station clock sweeping through the daily
 * train schedule while railway signal levers pull into place on each spoken cue. */
export const Custom3: React.FC<FullProps<CustomFull>> = ({full, t, start, end}) => {
	const sk = skinOf(full.skin ?? 'parchment');
	const c0 = cueAt(full, 0, start, end, 3);
	const c1 = cueAt(full, 1, start, end, 3);
	const c2 = cueAt(full, 2, start, end, 3);

	const cam = focusCam(
		540,
		interpolate(t, [start, end], [600, 630], clamp),
		interpolate(t, [start, c1, end], [1.03, 1.06, 1.0], clamp),
	);

	const levers = [
		{name: 'TRACK 1', at: c0},
		{name: 'MAIN LINE', at: c1},
		{name: 'CROSSING', at: c2},
	];

	return (
		<Paper t={t} start={start} seed={full.seed} cam={cam} skin={full.skin ?? 'parchment'}>
			<TitleBanner title={full.title || 'UITENHAGE SIGNAL BOX · 9 YEARS'} sub="EVERY TRAIN · EVERY LEVER · ZERO ERRORS" t={t} at={start + 0.05} skin={full.skin ?? 'parchment'} />

			{/* Station clock dial on the upper left */}
			<ClockDial
				cx={310}
				cy={445}
				r={145}
				fromHours={6}
				toHours={17.5}
				t={t}
				startAt={c0}
				endAt={c2 + 0.4}
				label="DAILY SCHEDULE"
				skin={full.skin ?? 'parchment'}
			/>

			{/* Photo cutout on the upper right */}
			<PhotoCutout
				photo={full.photos?.[0]}
				x={775}
				y={445}
				w={275}
				rot={3}
				label={full.photos?.[0]?.label || 'SIGNALMAN JACK'}
				t={t}
				at={c0}
				skin={full.skin ?? 'parchment'}
			/>

			{/* Animated railway signal levers along the lower-middle safe zone */}
			<svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', pointerEvents: 'none'}}>
				<rect x={140} y={1000} width={800} height={30} rx={8} fill={sk.ink} />
				{levers.map((lv, i) => {
					const x = 280 + i * 260;
					const pull = interpolate(t, [lv.at, lv.at + 0.45], [-26, 26], {...clamp, easing: Easing.out(Easing.back(1.6))});
					const done = t >= lv.at + 0.2;
					return (
						<g key={i}>
							<g transform={`translate(${x}, 1000) rotate(${pull})`}>
								<line x1={0} y1={0} x2={0} y2={-115} stroke={done ? sk.accent : sk.ink} strokeWidth={13} strokeLinecap="round" />
								<circle cx={0} cy={-125} r={18} fill={done ? sk.accent : sk.card} stroke={sk.ink} strokeWidth={5} />
							</g>
							<circle cx={x} cy={1000} r={17} fill={sk.card} stroke={sk.ink} strokeWidth={6} />
							<text x={x} y={1062} textAnchor="middle" fontFamily={TYPE} fontSize={32} fill={sk.ink}>
								{lv.name}
							</text>
							{appear(t, lv.at + 0.2, 0.25) > 0 ? (
								<text x={x} y={840} textAnchor="middle" fontFamily={SERIF} fontWeight={700} fontSize={32} fill={sk.accent} opacity={appear(t, lv.at + 0.2, 0.25)}>
									LOCKED ✓
								</text>
							) : null}
						</g>
					);
				})}
			</svg>

			<StampBadge text="0 MISTAKES" x={540} y={735} rot={-5} t={t} at={c2 + 0.35} color={sk.accent} />
		</Paper>
	);
};
