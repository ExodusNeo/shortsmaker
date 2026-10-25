import React, {useContext} from 'react';
import {Easing, Img, interpolate, spring, staticFile, useVideoConfig} from 'remotion';
import {CamContext, INK, Paper, SERIF, TYPE, rng, skinOf} from './Paper';
import type {Cam, Skin} from './Paper';
import type {CustomFull, CustomPhoto, FullProps, SkinName} from './types';

export {Easing, Img, Paper, SERIF, TYPE, interpolate, rng, skinOf, spring, staticFile, useVideoConfig};
export type {Cam, CustomFull, CustomPhoto, FullProps, Skin, SkinName};

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/** Smooth 0..1 progress from `at` to `at + dur`. */
export const appear = (t: number, at: number, dur = 0.45) =>
	interpolate(t, [at, at + Math.max(0.1, dur)], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});

/** Spring bounce 0..1 starting at `at`. */
export const popIn = (t: number, at: number, fps = 30) =>
	t < at ? 0 : spring({frame: (t - at) * fps, fps, config: {damping: 13, stiffness: 180}});

/** Safe cue lookup: returns `full.cues[i]` or an evenly spaced time in the scene (clamping cue 0 so the stage never opens blank). */
export const cueAt = (full: CustomFull, i: number, start: number, end: number, total = 3) => {
	if (i === 0) {
		const c0 = full.cues && full.cues[0] !== undefined ? full.cues[0] : start + 0.1;
		return Math.min(c0, start + 0.15);
	}
	if (full.cues && full.cues[i] !== undefined) return full.cues[i];
	const span = Math.max(0.8, end - start - 1.2);
	return start + 0.35 + (span * i) / Math.max(1, total);
};

/** Camera helper: places world point (x, y = 630) at the centre of the stage (screen y = 675),
 * leaving screen y = 70..180 clear for TitleBanner at the top and screen y = 1170+ clear for captions at the bottom. */
export const focusCam = (x = 540, y = 630, scale = 1): Cam => ({
	x,
	y: y + 285 / scale,
	scale,
});

/** Documentary header locked to the top of the screen (screen y = 74..170) regardless of camera pan/zoom. */
export const TitleBanner: React.FC<{title: string; sub?: string; t: number; at: number; skin?: SkinName}> = ({title, sub, t, at, skin}) => {
	const sk = skinOf(skin);
	const cam = useContext(CamContext);
	const k = appear(t, at, 0.4);
	if (k <= 0) return null;
	const fontSize = Math.min(48, Math.max(28, Math.floor(1120 / Math.max(12, title.length))));
	return (
		<div
			style={{
				position: 'absolute',
				left: cam.x - 540 / cam.scale,
				top: cam.y - 960 / cam.scale,
				width: 1080,
				height: 220,
				transformOrigin: '0 0',
				transform: `scale(${1 / cam.scale})`,
				pointerEvents: 'none',
				zIndex: 50,
			}}
		>
			<div
				style={{
					position: 'absolute', top: 74, left: 48, right: 48, textAlign: 'center',
					opacity: k, transform: `translateY(${18 * (1 - k)}px)`,
				}}
			>
				<div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 18}}>
					<div style={{height: 3, width: 54, flexShrink: 0, background: sk.accent}} />
					<div
						style={{
							fontFamily: SERIF, fontWeight: 700, fontSize, letterSpacing: 4, color: sk.ink,
							whiteSpace: 'nowrap',
						}}
					>
						{title.toUpperCase()}
					</div>
					<div style={{height: 3, width: 54, flexShrink: 0, background: sk.accent}} />
				</div>
				{sub ? (
					<div style={{fontFamily: TYPE, fontSize: 28, color: sk.ink, opacity: 0.82, marginTop: 8, letterSpacing: 2, whiteSpace: 'nowrap'}}>
						{sub.toUpperCase()}
					</div>
				) : null}
			</div>
		</div>
	);
};

/** Framed archival photo print from `full.photos` (centred at x, y) with pin, shadow and typed label. */
export const PhotoCutout: React.FC<{
	photo?: CustomPhoto;
	x: number;
	y: number;
	w?: number;
	rot?: number;
	label?: string;
	t: number;
	at: number;
	skin?: SkinName;
	highlight?: boolean;
}> = ({photo, x, y, w = 360, rot = -3, label, t, at, skin, highlight}) => {
	const {fps} = useVideoConfig();
	const sk = skinOf(skin);
	if (t < at) return null;
	const land = popIn(t, at, fps);
	const aspect = photo?.aspect || 1.25;
	const h = Math.min(w * 1.25, Math.max(w * 0.65, w / aspect));
	const text = (label ?? photo?.label ?? '').toUpperCase();
	return (
		<div
			style={{
				position: 'absolute', left: x - w / 2, top: y - h / 2, width: w,
				transform: `rotate(${rot + 6 * (1 - land)}deg) scale(${1.16 - 0.16 * land})`,
				opacity: Math.min(1, land * 2.5),
			}}
		>
			<div
				style={{
					background: '#f3ead6', padding: 12,
					border: highlight ? `5px solid ${sk.accent}` : 'none',
					boxShadow: `0 ${16 * land}px ${34 * land}px rgba(0,0,0,0.55)`,
				}}
			>
				{photo?.image ? (
					<Img
						src={staticFile(photo.image)}
						style={{display: 'block', width: w - 24, height: h - 24, objectFit: 'cover', filter: 'sepia(0.28) contrast(1.06)'}}
					/>
				) : (
					<div style={{width: w - 24, height: h - 24, background: sk.card, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: SERIF, fontSize: 42, color: sk.ink}}>
						{text}
					</div>
				)}
			</div>
			{/* Top pin */}
			<div
				style={{
					position: 'absolute', left: w / 2 - 13, top: -10, width: 26, height: 26, borderRadius: 13,
					background: sk.accent, boxShadow: '0 4px 8px rgba(0,0,0,0.45)',
				}}
			/>
			{text ? (
				<div
					style={{
						margin: '-6px auto 0', width: 'fit-content', maxWidth: w + 30, background: '#efe3c8', padding: '7px 18px',
						fontFamily: TYPE, fontSize: 34, color: INK, transform: `rotate(${-rot * 0.5}deg)`,
						boxShadow: '0 6px 12px rgba(0,0,0,0.4)', textAlign: 'center',
					}}
				>
					{text}
				</div>
			) : null}
		</div>
	);
};

/** Step card for a cause-and-effect or flow chain (centred at x, y). */
export const FlowCard: React.FC<{
	step?: string;
	title: string;
	sub?: string;
	x: number;
	y: number;
	w?: number;
	h?: number;
	t: number;
	at: number;
	skin?: SkinName;
	highlight?: boolean;
}> = ({step, title, sub, x, y, w = 420, h = 170, t, at, skin, highlight}) => {
	const {fps} = useVideoConfig();
	const sk = skinOf(skin);
	if (t < at) return null;
	const land = popIn(t, at, fps);
	const border = highlight ? sk.accent : sk.ink;
	return (
		<div
			style={{
				position: 'absolute', left: x - w / 2, top: y - h / 2, width: w, minHeight: h,
				background: sk.card, border: `4px solid ${border}`, borderRadius: 10,
				padding: '18px 24px', boxSizing: 'border-box',
				boxShadow: highlight ? `0 14px 32px rgba(0,0,0,0.45), 0 0 0 4px ${sk.accent}44` : '0 10px 24px rgba(0,0,0,0.3)',
				transform: `scale(${0.85 + 0.15 * land}) translateY(${20 * (1 - land)}px)`,
				opacity: Math.min(1, land * 2.5),
				display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', textAlign: 'center',
			}}
		>
			{step ? (
				<div style={{fontFamily: TYPE, fontSize: 28, color: sk.accent, letterSpacing: 3, marginBottom: 4}}>
					{step.toUpperCase()}
				</div>
			) : null}
			<div style={{fontFamily: SERIF, fontWeight: 700, fontSize: Math.min(46, Math.floor((w * 1.45) / Math.max(8, title.length))), lineHeight: 1.1, color: sk.cardInk}}>
				{title.toUpperCase()}
			</div>
			{sub ? (
				<div style={{fontFamily: TYPE, fontSize: 30, color: sk.cardInk, opacity: 0.82, marginTop: 8, lineHeight: 1.15}}>
					{sub}
				</div>
			) : null}
		</div>
	);
};

/** Self-drawing SVG arrow between (x1, y1) and (x2, y2), with optional curve bend `curve` (px). */
export const FlowArrow: React.FC<{
	x1: number;
	y1: number;
	x2: number;
	y2: number;
	curve?: number;
	t: number;
	at: number;
	dur?: number;
	color?: string;
	dashed?: boolean;
}> = ({x1, y1, x2, y2, curve = 0, t, at, dur = 0.4, color = '#e63946', dashed}) => {
	const k = appear(t, at, dur);
	if (k <= 0) return null;
	const dx = x2 - x1;
	const dy = y2 - y1;
	const len = Math.hypot(dx, dy) || 1;
	const nx = -dy / len;
	const ny = dx / len;
	const cx = (x1 + x2) / 2 + nx * curve;
	const cy = (y1 + y2) / 2 + ny * curve;
	const angle = (Math.atan2(y2 - cy, x2 - cx) * 180) / Math.PI;
	return (
		<svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', pointerEvents: 'none'}}>
			<path
				d={`M ${x1} ${y1} Q ${cx} ${cy} ${x2} ${y2}`}
				fill="none" stroke={color} strokeWidth={6} strokeLinecap="round"
				strokeDasharray={dashed ? '16 10' : 1} pathLength={dashed ? undefined : 1}
				strokeDashoffset={dashed ? undefined : 1 - k}
				opacity={dashed ? k : 1}
			/>
			{k > 0.8 ? (
				<g transform={`translate(${x2}, ${y2}) rotate(${angle})`} opacity={(k - 0.8) * 5}>
					<path d="M -22 -11 L 2 0 L -22 11 Z" fill={color} />
				</g>
			) : null}
		</svg>
	);
};

/** Pointer callout line + label for diagrams & cross-sections. */
export const CalloutTag: React.FC<{
	x: number;
	y: number;
	toX: number;
	toY: number;
	text: string;
	sub?: string;
	t: number;
	at: number;
	skin?: SkinName;
	accent?: boolean;
}> = ({x, y, toX, toY, text, sub, t, at, skin, accent}) => {
	const sk = skinOf(skin);
	const k = appear(t, at, 0.35);
	if (k <= 0) return null;
	const col = accent ? sk.accent : sk.ink;
	return (
		<>
			<svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', pointerEvents: 'none'}}>
				<line x1={x} y1={y} x2={x + (toX - x) * k} y2={y + (toY - y) * k} stroke={col} strokeWidth={4} strokeDasharray="8 6" />
				<circle cx={toX} cy={toY} r={9 * k} fill={sk.accent} stroke={sk.halo} strokeWidth={3} />
			</svg>
			<div
				style={{
					position: 'absolute', left: x, top: y, transform: 'translate(-50%, -50%)',
					background: sk.card, border: `3px solid ${col}`, borderRadius: 8, padding: '8px 18px',
					boxShadow: '0 8px 18px rgba(0,0,0,0.35)', opacity: k, textAlign: 'center', whiteSpace: 'nowrap',
				}}
			>
				<div style={{fontFamily: TYPE, fontSize: 34, fontWeight: 700, color: accent ? sk.accent : sk.cardInk}}>{text.toUpperCase()}</div>
				{sub ? <div style={{fontFamily: SERIF, fontSize: 28, color: sk.cardInk, opacity: 0.85}}>{sub}</div> : null}
			</div>
		</>
	);
};

/** Rubber-stamp verdict badge that slams onto the scene at `at`. */
export const StampBadge: React.FC<{
	text: string;
	x: number;
	y: number;
	rot?: number;
	t: number;
	at: number;
	color?: string;
}> = ({text, x, y, rot = -10, t, at, color = '#d62828'}) => {
	const {fps} = useVideoConfig();
	if (t < at) return null;
	const s = spring({frame: (t - at) * fps, fps, config: {damping: 11, stiffness: 240}});
	const fs = Math.min(56, Math.floor(620 / Math.max(8, text.length)));
	return (
		<div
			style={{
				position: 'absolute', left: x, top: y, width: 'max-content',
				transform: `translate(-50%, -50%) rotate(${rot}deg) scale(${1.6 - 0.6 * s})`,
				opacity: Math.min(1, s * 3),
				border: `7px double ${color}`, borderRadius: 10, padding: '10px 24px',
				fontFamily: TYPE, fontSize: fs, fontWeight: 700, letterSpacing: 5, color,
				background: 'rgba(0,0,0,0.18)', boxShadow: '0 10px 24px rgba(0,0,0,0.35)',
				whiteSpace: 'nowrap',
			}}
		>
			{text.toUpperCase()}
		</div>
	);
};

/** Animated clock / countdown dial with sweeping hour & minute hands and a progress arc. */
export const ClockDial: React.FC<{
	cx: number;
	cy: number;
	r?: number;
	fromHours: number;
	toHours: number;
	t: number;
	startAt: number;
	endAt: number;
	label?: string;
	skin?: SkinName;
}> = ({cx, cy, r = 210, fromHours, toHours, t, startAt, endAt, label, skin}) => {
	const sk = skinOf(skin);
	const k = interpolate(t, [startAt, Math.max(startAt + 0.4, endAt)], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const hrs = fromHours + (toHours - fromHours) * k;
	const hAngle = ((hrs % 12) / 12) * 360 - 90;
	const mAngle = ((hrs * 60) % 60) * 6 - 90;
	const sweep = Math.min(359.9, Math.abs(toHours - fromHours) * 30 * k);
	const a0 = ((fromHours % 12) / 12) * Math.PI * 2 - Math.PI / 2;
	const a1 = a0 + (sweep * Math.PI) / 180;
	const arcR = r - 24;
	const x0 = cx + Math.cos(a0) * arcR;
	const y0 = cy + Math.sin(a0) * arcR;
	const x1 = cx + Math.cos(a1) * arcR;
	const y1 = cy + Math.sin(a1) * arcR;
	const large = sweep > 180 ? 1 : 0;
	return (
		<svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', pointerEvents: 'none'}}>
			<circle cx={cx} cy={cy} r={r + 12} fill={sk.card} stroke={sk.ink} strokeWidth={6} />
			<circle cx={cx} cy={cy} r={r} fill="none" stroke={sk.ink} strokeWidth={2.5} strokeOpacity={0.5} />
			{sweep > 2 ? (
				<path
					d={`M ${cx} ${cy} L ${x0} ${y0} A ${arcR} ${arcR} 0 ${large} 1 ${x1} ${y1} Z`}
					fill={sk.accent} fillOpacity={0.22} stroke={sk.accent} strokeWidth={3}
				/>
			) : null}
			{Array.from({length: 12}, (_, i) => {
				const a = (i / 12) * Math.PI * 2 - Math.PI / 2;
				const major = i % 3 === 0;
				return (
					<g key={i}>
						<line
							x1={cx + Math.cos(a) * (r - (major ? 26 : 16))}
							y1={cy + Math.sin(a) * (r - (major ? 26 : 16))}
							x2={cx + Math.cos(a) * (r - 4)}
							y2={cy + Math.sin(a) * (r - 4)}
							stroke={sk.ink} strokeWidth={major ? 5 : 2.5}
						/>
						{major ? (
							<text
								x={cx + Math.cos(a) * (r - 54)}
								y={cy + Math.sin(a) * (r - 54) + 14}
								textAnchor="middle" fontFamily={SERIF} fontWeight={700} fontSize={40} fill={sk.ink}
							>
								{i === 0 ? 12 : i}
							</text>
						) : null}
					</g>
				);
			})}
			{/* Minute hand */}
			<line
				x1={cx} y1={cy}
				x2={cx + Math.cos((mAngle * Math.PI) / 180) * (r * 0.72)}
				y2={cy + Math.sin((mAngle * Math.PI) / 180) * (r * 0.72)}
				stroke={sk.ink} strokeWidth={6} strokeLinecap="round"
			/>
			{/* Hour hand */}
			<line
				x1={cx} y1={cy}
				x2={cx + Math.cos((hAngle * Math.PI) / 180) * (r * 0.5)}
				y2={cy + Math.sin((hAngle * Math.PI) / 180) * (r * 0.5)}
				stroke={sk.accent} strokeWidth={10} strokeLinecap="round"
			/>
			<circle cx={cx} cy={cy} r={12} fill={sk.accent} stroke={sk.card} strokeWidth={4} />
			{label ? (
				<text x={cx} y={cy + r + 68} textAnchor="middle" fontFamily={TYPE} fontSize={44} fill={sk.ink}>
					{label.toUpperCase()}
				</text>
			) : null}
		</svg>
	);
};

export * from './guarded';
