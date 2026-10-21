import {AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useVideoConfig} from 'remotion';
import type {Card, Graphic} from './Short';

/** This Short's colours: Short sets them from props.palette (shortsmaker/config.py PALETTES) before anything draws. */
export const theme = {accent: '#FFD400', emphasis: '#FF7A1A', panel: '#0d1320', land: '#333843', border: '#4b5871'};
export const FONT = 'Impact, "Arial Black", sans-serif';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// Thick black outline that survives any background (text-stroke alone eats into Impact's letters).
export const outline = (px: number) =>
	[...Array(16)]
		.map((_, k) => `${(Math.cos((k / 16) * 2 * Math.PI) * px).toFixed(1)}px ${(Math.sin((k / 16) * 2 * Math.PI) * px).toFixed(1)}px 0 #000`)
		.join(', ') + `, 0 ${px}px ${px * 2}px rgba(0,0,0,0.6)`;

/** In/out envelope for a callout that lives inside one scene; it appears at `tIn`. The spring lands
 * in ~12 frames with an ~8% overshoot; `leave` (0 -> 1) is a quicker, accelerating exit. */
export const useWindow = (t: number, tIn: number, end: number) => {
	const {fps} = useVideoConfig();
	const tOut = end - 0.25;
	const enter = spring({frame: (t - tIn) * fps, fps, config: {damping: 16.5, stiffness: 170}});
	const leave = interpolate(t, [tOut - 0.22, tOut], [0, 1], {...clamp, easing: Easing.in(Easing.cubic)});
	// a counter, bar or typing must be done by here, 0.4 s before the exit, however short the scene
	const ready = Math.max(tIn + 0.5, tOut - 0.62);
	return {visible: t >= tIn && t <= tOut, enter, leave, exit: 1 - leave, tIn, ready};
};

/** Arrive by moving, not fading: callout number `variant` rises from below, slides in from the left
 * or drops from above (rotating, so back-to-back callouts differ), and leaves the way it was heading.
 * Never grows from zero: scale starts at 0.9. */
export const moveIn = (enter: number, leave: number, variant: number): React.CSSProperties => {
	const [dx, dy] = [[0, 1], [-1, 0], [0, -1]][variant % 3];
	const d = 90 * (1 - enter) - 140 * leave;
	return {
		transform: `translate(${dx * d}px, ${dy * d}px) scale(${0.9 + 0.1 * Math.min(enter, 1)})`,
		opacity: Math.min(1, enter * 4) * (1 - leave),
	};
};

/** Vertical slot of a text callout: its usual place near the top, or, when the picture's subject
 * is up there (`low`), ending at y=1110 just above the captions so it doesn't cover a face. */
export const slot = (graphic: Graphic, top: number): React.CSSProperties => (graphic.low ? {bottom: 1920 - 1110} : {top});

export const HookTitle: React.FC<{text: string; t: number}> = ({text, t}) => {
	if (t > 1.8) return null;
	const opacity = interpolate(t, [1.5, 1.8], [1, 0], clamp); // fully visible on frame 0: thumbnail-ready
	return (
		<div
			style={{
				position: 'absolute', top: 220, left: 70, right: 70, textAlign: 'center', opacity, // high and compact: clear of faces
				transform: `scale(${1 + 0.03 * t})`, fontFamily: FONT, fontSize: 120, lineHeight: 1.12,
				color: theme.accent, textTransform: 'uppercase', textShadow: outline(9),
			}}
		>
			{text}
		</div>
	);
};

/** Silent subscribe reminder for the last seconds, just under the captions (clear of YouTube's buttons). */
export const SubscribeCta: React.FC<{line: string; t: number; start: number; end: number}> = ({line, t, start, end}) => {
	const {visible, enter, exit} = useWindow(t, start, end);
	if (!visible) return null;
	return (
		<div style={{position: 'absolute', top: 1330, left: 0, right: 0, textAlign: 'center', opacity: exit, transform: `translateY(${40 * (1 - enter)}px)`}}>
			<div
				style={{
					display: 'inline-block', background: '#CC0000', border: '5px solid #000', borderRadius: 60, padding: '10px 60px',
					fontFamily: FONT, fontSize: 80, color: 'white', boxShadow: '0 14px 30px rgba(0,0,0,0.5)',
				}}
			>
				SUBSCRIBE
			</div>
			<div style={{fontFamily: FONT, fontSize: 50, color: 'white', textShadow: outline(5), marginTop: 6}}>{line}</div>
		</div>
	);
};

export const Callout: React.FC<{graphic: Graphic; t: number; start: number; end: number; variant: number}> = ({graphic, t, start, end, variant}) => {
	const {visible, enter, leave, tIn, ready} = useWindow(t, start, end);
	if (!visible) return null;
	const m = moveIn(enter, leave, variant);
	const base: React.CSSProperties = {position: 'absolute', ...slot(graphic, 300), left: 0, right: 0, display: 'flex', justifyContent: 'center', ...m};

	if (graphic.style === 'date') {
		// A bare year counts up into place, like a time-travel dial.
		const year = /^\d{3,4}$/.test(graphic.text) ? Number(graphic.text) : null;
		const shown = year
			? Math.round(interpolate(t, [tIn, Math.min(tIn + 0.7, ready)], [year - 40, year], {...clamp, easing: Easing.out(Easing.cubic)}))
			: graphic.text;
		return (
			<div style={base}>
				<div style={{background: 'rgba(0,0,0,0.62)', borderRadius: 36, padding: '18px 54px 30px', textAlign: 'center'}}>
					<div style={{fontFamily: FONT, fontSize: 170, lineHeight: 1, color: 'white', textShadow: outline(7)}}>{shown}</div>
					<div style={{height: 16, borderRadius: 8, background: theme.accent, margin: '14px auto 0', width: `${70 * Math.min(enter, 1)}%`}} />
				</div>
			</div>
		);
	}
	if (graphic.style === 'fact') {
		return (
			<div style={{...base, transform: `${m.transform} rotate(${interpolate(Math.min(enter, 1), [0, 1], [-6, -2])}deg)`}}>
				<div
					style={{
						background: theme.accent, border: '6px solid #000', borderRadius: 24, padding: '14px 40px',
						fontFamily: FONT, fontSize: 84, color: '#000', boxShadow: '0 14px 30px rgba(0,0,0,0.5)', maxWidth: 900, textAlign: 'center',
					}}
				>
					{graphic.text}
				</div>
			</div>
		);
	}
	return ( // place without coordinates: pill with a map pin
		<div style={base}>
			<div style={{display: 'flex', alignItems: 'center', gap: 20, background: 'rgba(0,0,0,0.72)', borderRadius: 60, padding: '18px 44px 18px 30px'}}>
				<Pin size={64} />
				<span style={{fontFamily: FONT, fontSize: 64, color: 'white'}}>{graphic.text}</span>
			</div>
		</div>
	);
};

export const Pin: React.FC<{size: number}> = ({size}) => (
	<svg width={size * 0.75} height={size} viewBox="0 0 30 40">
		<path d="M15 0C6.7 0 0 6.7 0 15c0 11 15 25 15 25s15-14 15-25C30 6.7 23.3 0 15 0z" fill={theme.accent} stroke="#000" strokeWidth={2} />
		<circle cx={15} cy={15} r={5.5} fill="#000" />
	</svg>
);

export const PersonCard: React.FC<{card: Card; t: number}> = ({card, t}) => {
	const {fps} = useVideoConfig();
	if (t < card.on || t > card.off) return null;
	const pop = spring({frame: (t - card.on) * fps, fps, config: {damping: 10, stiffness: 180}}); // overshoots, then settles
	const exit = interpolate(t, [card.off - 0.2, card.off], [1, 0], clamp);
	const scale = (0.6 + 0.4 * pop) * (0.85 + 0.15 * exit);
	return (
		<>
			<AbsoluteFill style={{backgroundColor: `rgba(0,0,0,${0.38 * Math.min(1, pop) * exit})`}} />
			<div
				style={{
					// Centered at y=660: clear of the top callouts and of the captions' line above y~1180.
					position: 'absolute', left: 540 - 282, top: 660 - 370, width: 564, opacity: Math.min(1, pop * 2) * exit,
					transform: `scale(${scale}) rotate(${interpolate(pop, [0, 1], [-9, -3])}deg)`,
				}}
			>
				<div style={{background: 'white', borderRadius: 30, padding: 12, boxShadow: '0 22px 50px rgba(0,0,0,0.6)'}}>
					<Img src={staticFile(card.image)} style={{width: 540, height: 648, objectFit: 'cover', objectPosition: '50% 20%', borderRadius: 22, display: 'block'}} />
				</div>
				<div style={{display: 'flex', justifyContent: 'center', marginTop: -48}}>
					<div style={{background: theme.accent, border: '5px solid #000', borderRadius: 18, padding: '10px 28px', fontFamily: FONT, fontSize: 62, color: '#000', textTransform: 'uppercase', whiteSpace: 'nowrap'}}>
						{card.name}
					</div>
				</div>
			</div>
		</>
	);
};
