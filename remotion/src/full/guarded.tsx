import React, {useId} from 'react';
import {Easing, interpolate, spring, useVideoConfig} from 'remotion';
import {SERIF, TYPE, skinOf} from './Paper';
import type {SkinName} from './types';

// Guard-railed building blocks for AI-coded custom scenes. The AI chooses what to show and where; these pieces
// make the classic mistakes impossible: arrows route between box edges and never cross a box, cards keep a fixed
// size so text can't spill out, everything stays inside the stage, and nothing travels faster than MIN_MOVE.

/** Stage every custom scene stays inside (world px): below the title banner, above the captions. */
export const SAFE = {left: 110, right: 970, top: 260, bottom: 1020} as const;
/** A rectangle by its centre point and size (world px). */
export type Box = {x: number; y: number; w: number; h: number};
/** Seconds: nothing moves across the stage faster than this, however short the trip. */
export const MIN_MOVE = 0.9;

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const range = (n: number) => Array.from({length: Math.max(0, Math.floor(n))}, (_, i) => i);

/** A box moved (and shrunk if needed) so it sits fully inside the stage. */
export const boxAt = (x: number, y: number, w: number, h: number): Box => {
	const bw = Math.min(w, SAFE.right - SAFE.left);
	const bh = Math.min(h, SAFE.bottom - SAFE.top);
	return {
		x: Math.min(SAFE.right - bw / 2, Math.max(SAFE.left + bw / 2, x)),
		y: Math.min(SAFE.bottom - bh / 2, Math.max(SAFE.top + bh / 2, y)),
		w: bw,
		h: bh,
	};
};

/** The box a <PhotoCutout x y w photo label> covers (frame + label), for <Connect> and its `avoid` list. */
export const photoBox = (aspect: number | undefined, x: number, y: number, w = 360, label = true): Box => {
	const h = Math.min(w * 1.25, Math.max(w * 0.65, w / (aspect || 1.25)));
	return {x, y: y + (label ? 22 : 0), w: w + 24, h: h + (label ? 64 : 20)};
};

/** n boxes side by side across the stage, evenly spaced. */
export const layoutRow = (n: number, o: {y?: number; h?: number; gap?: number} = {}): Box[] => {
	const gap = o.gap ?? 60;
	const w = (SAFE.right - SAFE.left - gap * (n - 1)) / Math.max(1, n);
	const h = o.h ?? Math.min(240, w * 0.8);
	return range(n).map((i) => boxAt(SAFE.left + w / 2 + i * (w + gap), o.y ?? 640, w, h));
};

/** n boxes stacked top to bottom, centred in the stage, with room between them for arrows. */
export const layoutColumn = (n: number, o: {x?: number; w?: number; gap?: number; top?: number; bottom?: number} = {}): Box[] => {
	const top = Math.max(SAFE.top, o.top ?? SAFE.top);
	const bottom = Math.min(SAFE.bottom, o.bottom ?? SAFE.bottom);
	const gap = o.gap ?? 70;
	const h = Math.min(200, (bottom - top - gap * (n - 1)) / Math.max(1, n));
	const first = top + (bottom - top - (n * h + gap * (n - 1))) / 2 + h / 2;
	return range(n).map((i) => boxAt(o.x ?? 540, first + i * (h + gap), o.w ?? 720, h));
};

/** n boxes in a grid of `cols` columns filling the stage. */
export const layoutGrid = (n: number, cols: number, o: {gap?: number; top?: number; bottom?: number} = {}): Box[] => {
	const c = Math.max(1, Math.min(cols, n));
	const rows = Math.ceil(n / c);
	const gap = o.gap ?? 60;
	const top = Math.max(SAFE.top, o.top ?? SAFE.top);
	const bottom = Math.min(SAFE.bottom, o.bottom ?? SAFE.bottom);
	const w = (SAFE.right - SAFE.left - gap * (c - 1)) / c;
	const h = Math.min(260, (bottom - top - gap * (rows - 1)) / rows);
	const first = top + (bottom - top - (rows * h + gap * (rows - 1))) / 2 + h / 2;
	return range(n).map((i) => boxAt(SAFE.left + w / 2 + (i % c) * (w + gap), first + Math.floor(i / c) * (h + gap), w, h));
};

/** How a card's text fits its box: the biggest title size (52..26 px) that fits with the step label and sub-line;
 * if they can't all fit, the step label goes first, then the sub-line; a title too long even at 26 px is cut to
 * the lines that fit. `height` is what the content needs. Exported for tests. */
export const fitCard = (box: Box, title: string, sub?: string, step?: string) => {
	const inner = box.w - 52;
	const room = box.h - 8 - 24; // border + padding
	const linesAt = (size: number) => {
		const perLine = Math.max(1, Math.floor(inner / (size * 0.72))); // bold serif capitals run ~0.72 em wide
		let lines = 1;
		let cur = 0; // letters on the current line
		for (const w of title.toUpperCase().split(/\s+/).filter(Boolean)) {
			if (cur && cur + 1 + w.length <= perLine) {
				cur += 1 + w.length;
				continue;
			}
			if (cur) lines++;
			lines += Math.ceil(w.length / perLine) - 1; // a word longer than a line breaks across lines
			cur = w.length % perLine || perLine;
		}
		return lines;
	};
	const need = (size: number, st: boolean, sb: boolean) => (st ? 32 : 0) + linesAt(size) * size * 1.08 + (sb ? 36 : 0);
	const subFits = !!sub && sub.length * 28 * 0.62 <= inner; // the sub-line is one line of 28 px type, or it's left out
	const configs: [boolean, boolean, number][] = [[!!step, subFits, 34], [false, subFits, 34], [!!step, false, 34], [false, false, 26]];
	for (const [st, sb, min] of configs) {
		for (let size = 52; size >= min; size -= 2) {
			if (need(size, st, sb) <= room) return {titleSize: size, showStep: st, showSub: sb, maxLines: linesAt(size), height: need(size, st, sb) + 24};
		}
	}
	const maxLines = Math.max(1, Math.floor(room / (26 * 1.08)));
	return {titleSize: 26, showStep: false, showSub: false, maxLines, height: maxLines * 26 * 1.08 + 24};
};

/** A fixed-size card: the text shrinks to fit (never below a phone-readable size) and can never spill out. */
export const Card: React.FC<{
	box: Box;
	title: string;
	sub?: string;
	step?: string;
	t: number;
	at: number;
	skin?: SkinName;
	highlight?: boolean;
}> = ({box, title, sub, step, t, at, skin, highlight}) => {
	const {fps} = useVideoConfig();
	const sk = skinOf(skin);
	if (t < at) return null;
	const land = spring({frame: (t - at) * fps, fps, config: {damping: 15, stiffness: 140}});
	const fit = fitCard(box, title, sub, step);
	return (
		<div
			style={{
				position: 'absolute', left: box.x - box.w / 2, top: box.y - box.h / 2, width: box.w, height: box.h, overflow: 'hidden',
				background: sk.card, border: `4px solid ${highlight ? sk.accent : sk.ink}`, borderRadius: 10, boxSizing: 'border-box',
				padding: '12px 22px', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center',
				textAlign: 'center', boxShadow: '0 10px 24px rgba(0,0,0,0.3)',
				scale: String(0.88 + 0.12 * Math.min(1, land)), translate: `0px ${18 * (1 - Math.min(1, land))}px`, opacity: Math.min(1, land * 2.5),
			}}
		>
			{step && fit.showStep ? <div style={{fontFamily: TYPE, fontSize: 26, lineHeight: '32px', color: sk.accent, letterSpacing: 3}}>{step.toUpperCase()}</div> : null}
			<div
				style={{
					fontFamily: SERIF, fontWeight: 700, fontSize: fit.titleSize, lineHeight: 1.08, color: sk.cardInk,
					display: '-webkit-box', WebkitBoxOrient: 'vertical', WebkitLineClamp: fit.maxLines, overflow: 'hidden',
				}}
			>
				{title.toUpperCase()}
			</div>
			{sub && fit.showSub ? (
				<div style={{fontFamily: TYPE, fontSize: 28, color: sk.cardInk, opacity: 0.85, marginTop: 6, lineHeight: 1.1, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '100%'}}>
					{sub}
				</div>
			) : null}
		</div>
	);
};

type Pt = [number, number];
const GAP = 16; // arrows start and end this far outside their boxes

/** Does segment p-q pass through box b (grown by `pad`)? Liang-Barsky clipping. */
const hits = (p: Pt, q: Pt, b: Box, pad = 6): boolean => {
	const [x0, x1, y0, y1] = [b.x - b.w / 2 - pad, b.x + b.w / 2 + pad, b.y - b.h / 2 - pad, b.y + b.h / 2 + pad];
	const dx = q[0] - p[0];
	const dy = q[1] - p[1];
	let lo = 0;
	let hi = 1;
	for (const [pp, qq] of [[-dx, p[0] - x0], [dx, x1 - p[0]], [-dy, p[1] - y0], [dy, y1 - p[1]]] as Pt[]) {
		if (pp === 0) {
			if (qq < 0) return false;
		} else {
			const r = qq / pp;
			if (pp < 0) lo = Math.max(lo, r);
			else hi = Math.min(hi, r);
			if (lo > hi) return false;
		}
	}
	return true;
};

type Side = 'left' | 'right' | 'top' | 'bottom';
const SIDES: Side[] = ['left', 'right', 'top', 'bottom'];
const NORMAL: Record<Side, Pt> = {left: [-1, 0], right: [1, 0], top: [0, -1], bottom: [0, 1]};
/** Where an arrow leaves/enters a box side: the side's middle, GAP outside the box. */
const port = (b: Box, s: Side): Pt => [b.x + NORMAL[s][0] * (b.w / 2 + GAP), b.y + NORMAL[s][1] * (b.h / 2 + GAP)];

/** The arrow's path from box a to box b: every combination of exit side, entry side and detour lane (straight,
 * elbow, or around all boxes) is scored, and the winner crosses no box (a and b included) whenever any route can,
 * then has the fewest bends and the shortest length. It always leaves a outwards and points into b. Exported for tests. */
export const routeArrow = (a: Box, b: Box, avoid: Box[] = []): Pt[] => {
	const blocks = [a, b, ...avoid];
	const lo = Math.min(...blocks.map((x) => x.x - x.w / 2)) - 2 * GAP;
	const hi = Math.max(...blocks.map((x) => x.x + x.w / 2)) + 2 * GAP;
	const top = Math.min(...blocks.map((x) => x.y - x.h / 2)) - 2 * GAP;
	const bottom = Math.max(...blocks.map((x) => x.y + x.h / 2)) + 2 * GAP;
	const cands: Pt[][] = [];
	for (const sa of SIDES) {
		for (const sb of SIDES) {
			const p = port(a, sa);
			const q = port(b, sb);
			const hA = sa === 'left' || sa === 'right';
			const hB = sb === 'left' || sb === 'right';
			if (hA && hB) {
				for (const x of [(p[0] + q[0]) / 2, lo, hi]) cands.push([p, [x, p[1]], [x, q[1]], q]);
			} else if (!hA && !hB) {
				for (const y of [(p[1] + q[1]) / 2, top, bottom]) cands.push([p, [p[0], y], [q[0], y], q]);
			} else {
				cands.push(hA ? [p, [q[0], p[1]], q] : [p, [p[0], q[1]], q]);
			}
			// facing sides that line up: one straight segment at the overlap
			if (hA && hB && sa !== sb) {
				const y = (Math.max(a.y - a.h / 2, b.y - b.h / 2) + Math.min(a.y + a.h / 2, b.y + b.h / 2)) / 2;
				cands.push([[p[0], y], [q[0], y]]);
			}
			if (!hA && !hB && sa !== sb) {
				const x = (Math.max(a.x - a.w / 2, b.x - b.w / 2) + Math.min(a.x + a.w / 2, b.x + b.w / 2)) / 2;
				cands.push([[x, p[1]], [x, q[1]]]);
			}
		}
	}
	const clean = (pts: Pt[]) => pts.filter((pt, i) => i === 0 || Math.hypot(pt[0] - pts[i - 1][0], pt[1] - pts[i - 1][1]) > 0.5);
	const score = (raw: Pt[]) => {
		const pts = clean(raw);
		if (pts.length < 2) return Infinity;
		const out = (b0: Box, pt: Pt, dir: Pt) => // the segment must point away from b0 (exit) / toward it (entry)
			(pt[0] - b0.x) * dir[0] + (pt[1] - b0.y) * dir[1];
		const d0: Pt = [pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]];
		const n = pts.length;
		const d1: Pt = [pts[n - 1][0] - pts[n - 2][0], pts[n - 1][1] - pts[n - 2][1]];
		if (out(a, pts[0], d0) <= 0 || out(b, pts[n - 1], d1) >= 0) return Infinity;
		let crossings = 0;
		let len = 0;
		for (let i = 1; i < n; i++) {
			crossings += blocks.filter((bx) => hits(pts[i - 1], pts[i], bx)).length;
			len += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
		}
		return crossings * 100000 + (n - 2) * 120 + len;
	};
	const best = cands.reduce((x, c) => (score(c) < score(x) ? c : x), cands[0]);
	return clean(best);
};

/** A self-drawing arrow from one box to another that never crosses a box: list every other box on the stage in
 * `avoid`. Draws in `dur` seconds from `at`; the head appears when the line arrives. */
export const Connect: React.FC<{
	from: Box;
	to: Box;
	avoid?: Box[];
	t: number;
	at: number;
	dur?: number;
	color?: string;
	dashed?: boolean;
	skin?: SkinName;
}> = ({from, to, avoid = [], t, at, dur = 0.5, color, dashed, skin}) => {
	const id = useId().replace(/:/g, '');
	const pts = routeArrow(from, to, avoid);
	const k = interpolate(t, [at, at + Math.max(0.35, dur)], [0, 1], {...clamp, easing: Easing.inOut(Easing.quad)});
	if (k <= 0) return null;
	const c = color ?? skinOf(skin).accent;
	const d = pts.map((p, i) => `${i ? 'L' : 'M'} ${p[0]} ${p[1]}`).join(' ');
	const [p, q] = [pts[pts.length - 2], pts[pts.length - 1]];
	const ang = (Math.atan2(q[1] - p[1], q[0] - p[0]) * 180) / Math.PI;
	return (
		<svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', pointerEvents: 'none'}}>
			<defs>
				<mask id={`m${id}`} maskUnits="userSpaceOnUse" x={-200} y={-200} width={1480} height={2320}>
					<path d={d} fill="none" stroke="white" strokeWidth={24} strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - k} />
				</mask>
			</defs>
			<path d={d} fill="none" stroke={c} strokeWidth={6} strokeLinejoin="round" strokeLinecap="round" strokeDasharray={dashed ? '16 12' : undefined} mask={`url(#m${id})`} />
			{k >= 0.98 ? <path d="M 0 0 L -22 -12 L -22 12 Z" fill={c} transform={`translate(${q[0]} ${q[1]}) rotate(${ang})`} /> : null}
		</svg>
	);
};

/** Where something travelling from `from` to `to` is at time t, starting at `at`. The trip takes at least MIN_MOVE
 * seconds (longer for long trips: `speed` px/s), eases in and out, and lifts in an arc of `arc` px. */
export const travel = (t: number, at: number, from: Pt, to: Pt, o: {speed?: number; arc?: number} = {}) => {
	const dist = Math.hypot(to[0] - from[0], to[1] - from[1]);
	const dur = Math.max(MIN_MOVE, dist / (o.speed ?? 600));
	const k = interpolate(t, [at, at + dur], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const arc = o.arc ?? Math.min(110, dist * 0.22);
	return {x: from[0] + (to[0] - from[0]) * k, y: from[1] + (to[1] - from[1]) * k - Math.sin(Math.PI * k) * arc, k, end: at + dur};
};
