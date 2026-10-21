import {Easing, Img, interpolate, spring, staticFile, useVideoConfig} from 'remotion';
import {Cam, INK, Paper, TYPE, rng, skinOf} from './Paper';
import {MIN_MOVE} from './guarded';
import type {BoardFull, FullProps} from './types';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// Where the prints sit (centre points, world pixels), per item count; mirrored and jittered per scene.
const LAYOUTS: Record<number, [number, number][]> = {
	3: [[290, 380], [800, 600], [400, 1060]],
	4: [[280, 360], [810, 420], [300, 1000], [800, 1080]],
	5: [[270, 340], [820, 380], [540, 760], [260, 1160], [820, 1200]],
};

type Print = {x: number; y: number; w: number; h: number; rot: number};

const layout = (full: BoardFull): Print[] => {
	const r = rng(full.seed);
	const n = full.items.length;
	const base = LAYOUTS[Math.min(5, Math.max(3, n))];
	const flip = r() < 0.5;
	const w = n <= 3 ? 420 : n === 4 ? 370 : 330;
	return full.items.map((it, i) => {
		const [bx, by] = base[i % base.length];
		const h = Math.min(w * 1.3, Math.max(w * 0.62, w / (it.aspect || 1.33)));
		return {x: (flip ? 1080 - bx : bx) + (r() - 0.5) * 70, y: by + (r() - 0.5) * 50, w, h, rot: (r() - 0.5) * 12};
	});
};

const lerp = (a: Cam, b: Cam, k: number): Cam => ({x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, scale: a.scale + (b.scale - a.scale) * k});

/** Real photos pinned to a dark board as aged prints. Each pops in as it is named while the camera
 * glides to it; red thread pulls tight between linked prints; at the end the camera pulls back to
 * show the whole board. With less than MIN_MOVE between prints (a short scene) the camera would whip, so it
 * stays on the whole board instead, pushing in slowly while the prints pop into place. */
export const Board: React.FC<FullProps<BoardFull>> = ({full, t, start, end}) => {
	const {fps} = useVideoConfig();
	const prints = layout(full);
	const latest = end - 1.1;
	const ats = full.items.map((it) => Math.max(start + 0.15, Math.min(it.at, latest)));
	// Camera: close on each new print as it lands, then pull back to the whole board.
	const xs = prints.flatMap((p) => [p.x - p.w / 2, p.x + p.w / 2]);
	const ys = prints.flatMap((p) => [p.y - p.h / 2 - 30, p.y + p.h / 2 + 90]);
	const all: Cam = {
		x: (Math.min(...xs) + Math.max(...xs)) / 2,
		y: 0,
		scale: Math.min(1, 980 / (Math.max(...xs) - Math.min(...xs)), 880 / (Math.max(...ys) - Math.min(...ys))),
	};
	all.y = (Math.min(...ys) + Math.max(...ys)) / 2 + 330 / all.scale; // the whole board sits at screen y ~630, above the captions
	const keys: {t: number; cam: Cam}[] = [
		...prints.map((p, i) => ({t: ats[i] + 0.2, cam: {x: p.x, y: p.y + 210, scale: 1.6}})),
		{t: Math.min(end - 0.25, Math.max(ats[ats.length - 1] + 0.9, end - 0.9)), cam: all},
	];
	const closeUps = keys.every((key, i) => i === 0 || key.t - keys[i - 1].t >= MIN_MOVE);
	let cam: Cam = closeUps ? {...keys[0].cam, scale: 1.12} : lerp(all, {...all, scale: all.scale * 1.06}, interpolate(t, [start, end], [0, 1], clamp));
	for (const key of closeUps ? keys : []) {
		const k = interpolate(t, [key.t - 0.6, key.t], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
		cam = lerp(cam, key.cam, k);
	}
	const pinOf = (i: number) => {
		const p = prints[i];
		const a = (p.rot * Math.PI) / 180;
		return [p.x + Math.sin(a) * (p.h / 2), p.y - Math.cos(a) * (p.h / 2) + 6];
	};

	const sk = skinOf(full.skin);

	return (
		<Paper t={t} start={start} seed={full.seed} cam={cam} dark skin={full.skin}>
			{(!full.skin || full.skin === 'parchment') ? (
				<Img
					src={staticFile('paper/paper.jpg')}
					style={{position: 'absolute', left: -1400, top: -1400, width: 3880, height: 4800, filter: 'brightness(0.34) sepia(0.5) saturate(1.4)'}}
				/>
			) : null}
			{full.items.map((it, i) => {
				const p = prints[i];
				if (t < ats[i]) return null;
				const land = spring({frame: (t - ats[i]) * fps, fps, config: {damping: 13, stiffness: 190}});
				return (
					<div
						key={i}
						style={{
							position: 'absolute', left: p.x - p.w / 2, top: p.y - p.h / 2, width: p.w,
							transform: `rotate(${p.rot + 7 * (1 - land)}deg) scale(${1.18 - 0.18 * land})`, opacity: Math.min(1, land * 2.5),
						}}
					>
						<div style={{background: '#f3ead6', padding: 14, boxShadow: `0 ${18 * land}px ${36 * land}px rgba(0,0,0,0.6)`}}>
							<Img src={staticFile(it.image)} style={{display: 'block', width: p.w - 28, height: p.h - 28, objectFit: 'cover', filter: 'sepia(0.35) contrast(1.05)'}} />
						</div>
						<div
							style={{
								margin: '-6px auto 0', width: 'fit-content', maxWidth: p.w + 40, background: '#efe3c8', padding: '8px 20px',
								fontFamily: TYPE, fontSize: 38, color: INK, transform: `rotate(${-p.rot * 0.6}deg)`, boxShadow: '0 6px 12px rgba(0,0,0,0.45)',
							}}
						>
							{it.label}
						</div>
					</div>
				);
			})}
			<svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
				{full.links.map(([a, b], i) => {
					const from = Math.max(ats[a], ats[b]) + 0.35;
					const k = interpolate(t, [from, from + 0.5], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
					if (k <= 0) return null;
					const [x1, y1] = pinOf(a);
					const [x2, y2] = pinOf(b);
					const sag = 70 * (1 - 0.6 * k);
					return (
						<path
							key={i} d={`M${x1} ${y1} Q${(x1 + x2) / 2} ${(y1 + y2) / 2 + sag} ${x2} ${y2}`} fill="none" stroke={sk.accent} strokeWidth={5}
							strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - k} style={{filter: 'drop-shadow(0 4px 3px rgba(0,0,0,0.5))'}}
						/>
					);
				})}
				{full.items.map((_, i) => {
					if (t < ats[i]) return null;
					const [x, y] = pinOf(i);
					return (
						<g key={i}>
							<circle cx={x + 3} cy={y + 5} r={15} fill="rgba(0,0,0,0.45)" />
							<circle cx={x} cy={y} r={15} fill={sk.accent} />
							<circle cx={x - 5} cy={y - 5} r={5} fill="rgba(255,255,255,0.45)" />
						</g>
					);
				})}
			</svg>
		</Paper>
	);
};
