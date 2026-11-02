import React from 'react';
import {CustomFull, Easing, FullProps, Paper, interpolate, skinOf} from '../toolkit';

// Composition study, not a factual reconstruction: one large subject, one braking action, no explanation.
// Keep the camera in portrait coordinates; the headline and captions are supplied by the Short composition.
export const ExampleOpenerAction: React.FC<FullProps<CustomFull>> = ({full, t, start}) => {
	const sk = skinOf(full.skin);
	const light = sk.dark ? sk.ink : sk.card;
	const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
	const stop = interpolate(t - start, [0, 0.65], [-100, 0], {...clamp, easing: Easing.bezier(0.16, 1, 0.3, 1)});
	const spray = interpolate(t - start, [0.45, 0.8, 1.5], [0, 1, 0.8], clamp);
	return <Paper t={t} start={start} seed={full.seed} cam={{x: 540, y: 960, scale: 1}} skin={full.skin}>
		<svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
			<path d="M0 1030H1080 M0 1060H1080" stroke={sk.ink} strokeWidth={12} opacity={0.6} />
			<g transform={`translate(${stop} 0)`}>
				<path d="M160 880L270 790H660L890 910L840 990H210Z" fill={sk.accent} stroke={sk.ink} strokeWidth={9} />
				<path d="M220 990H840L800 1035H260Z" fill={sk.ink} />
				<g transform="translate(0 100)">
				<path d="M380 790L395 650Q475 595 560 675L605 790Z" fill={sk.ink} />
				<ellipse cx={470} cy={565} rx={82} ry={100} fill={light} stroke={sk.ink} strokeWidth={10} />
				<path d="M388 545Q395 430 480 455Q555 465 554 550Z" fill={sk.accent} stroke={sk.ink} strokeWidth={9} />
				<path d="M435 575H475 M500 575H530" stroke={sk.ink} strokeWidth={12} strokeLinecap="round" />
				<path d="M408 665L550 787 M540 670L415 787" stroke={light} strokeWidth={20} />
				</g>
			</g>
			<g opacity={spray} transform={`translate(860 980) scale(${0.25 + spray * 0.75})`}>
				<path d="M0 0Q-90-140-155-265Q-75-260-45-160Q-35-370 15-410Q55-300 40-180Q130-310 180-300Q135-140 0 0Z"
					fill={light} stroke={sk.ink} strokeWidth={5} />
				{[[-120, -330], [-25, -450], [100, -370], [160, -240]].map(([x, y], i) =>
					<ellipse key={i} cx={x} cy={y} rx={10} ry={22} fill={light} />)}
			</g>
		</svg>
	</Paper>;
};
