import {Easing, Img, interpolate, spring, staticFile, useVideoConfig} from 'remotion';
import {InkIcon} from './icons';
import {Paper, SERIF, TYPE, skinOf} from './Paper';
import type {Skin} from './Paper';
import type {FullProps, NumberFull} from './types';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/** One counted figure: the thing itself painted as an ink silhouette (full.image), else the closest built-in icon.
 * The silhouette is dark ink; on dark skins it is inverted to light ink. */
const Figure: React.FC<{full: NumberFull; size: number; color: string; dark: boolean; glow?: string}> = ({full, size, color, dark, glow}) =>
	full.image ? (
		<Img
			src={staticFile(full.image)}
			style={{
				display: 'block', width: size, height: size, objectFit: 'contain',
				filter: [dark ? 'invert(0.92)' : '', glow ? `drop-shadow(0 0 5px ${glow}) drop-shadow(0 0 2px ${glow})` : ''].join(' ').trim() || undefined,
			}}
		/>
	) : (
		<InkIcon icon={full.icon} size={size} color={color} />
	);

/** The figure grid: the column count that gives the biggest figures in the space between the key and the captions. */
const gridFor = (n: number, width = 860, height = 360) =>
	Array.from({length: 10}, (_, k) => k + 1)
		.map((cols) => ({cols, rows: Math.ceil(n / cols), cell: Math.floor(Math.min(150, width / cols, height / Math.ceil(n / cols)))}))
		.reduce((best, g) => (g.cell > best.cell ? g : best));

/** "1.5 MILLION" -> 1.5 + " MILLION"; "30,000" -> 30000 with commas. The counter keeps that format. */
const counter = (show: string, k: number) => {
	const m = show.match(/^([\d,]*\.?\d+)(.*)$/);
	if (!m) return show;
	const num = parseFloat(m[1].replace(/,/g, ''));
	const decimals = (m[1].split('.')[1] ?? '').length;
	const v = num * k;
	const text = v.toLocaleString('en-US', {minimumFractionDigits: decimals, maximumFractionDigits: decimals, useGrouping: m[1].includes(',')});
	return text + m[2];
};

const fmt = (v: number) => v.toLocaleString('en-US', {maximumFractionDigits: 2});

const fmtBar = (v: number, grow: number, dollar: boolean) => {
	const prefix = dollar ? '$' : '';
	if (v >= 1_000_000_000 && v % 10_000_000 === 0) {
		const b = v / 1_000_000_000;
		const dec = Number.isInteger(b) ? 0 : b * 10 === Math.floor(b * 10) ? 1 : 2;
		return `${prefix}${(b * grow).toFixed(dec)}B`;
	}
	if (v >= 1_000_000 && v % 10_000 === 0) {
		const m = v / 1_000_000;
		const dec = Number.isInteger(m) ? 0 : m * 10 === Math.floor(m * 10) ? 1 : 2;
		return `${prefix}${(m * grow).toFixed(dec)}M`;
	}
	return `${prefix}${fmt(Math.round(v * grow * 100) / 100)}`;
};

/** A number that is hard to picture: it counts up big, then a field of small ink figures stamps in,
 * each standing for `each` of them. With `compare`, two hatched ink bars grow to scale instead. */
export const BigNumber: React.FC<FullProps<NumberFull>> = ({full, t, start, end}) => {
	const {fps} = useVideoConfig();
	const sk = skinOf(full.skin);
	const at = Math.max(start + 0.2, Math.min(full.at, end - 1.8));
	const k = interpolate(t, [at, at + 1.0], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
	const enter = spring({frame: (t - at) * fps, fps, config: {damping: 14, stiffness: 160}});
	const fillStart = at + 1.05;
	const fillEnd = Math.max(fillStart + 0.4, Math.min(fillStart + 1.6, end - 0.6));
	const cam = {x: 540, y: interpolate(t, [start, fillStart, fillEnd], [800, 820, 900], clamp), scale: interpolate(t, [start, fillStart, fillEnd], [1.12, 1.08, 1], clamp)};
	const n = Math.max(1, Math.min(60, full.figures));
	const {cols, cell} = gridFor(n);
	const shown = Math.floor(interpolate(t, [fillStart, fillEnd], [0, n], clamp));
	const dollar = full.icon === 'dollar' || /\$|DOLLAR/i.test(full.label);
	const rawBig = full.compare ? null : counter(full.show, k);
	const big = rawBig && dollar && !rawBig.startsWith('$') ? `$${rawBig}` : rawBig;
	const bigSize = big ? Math.min(230, Math.floor(1750 / Math.max(4, big.length))) : 0;

	return (
		<Paper t={t} start={start} seed={full.seed} cam={cam} skin={full.skin}>
			<div style={{position: 'absolute', top: 300, left: 60, right: 60, textAlign: 'center', color: sk.ink, opacity: Math.min(1, enter * 2)}}>
				{big ? (
					<div style={{fontFamily: SERIF, fontWeight: 700, fontSize: bigSize, lineHeight: 1, transform: `translateY(${30 * (1 - enter)}px)`}}>{big}</div>
				) : null}
				<div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 24, marginTop: big ? 18 : 0}}>
					<div style={{height: 4, width: 70, background: sk.accent}} />
					<div style={{fontFamily: SERIF, fontSize: Math.min(full.compare ? 76 : 64, Math.floor(1500 / Math.max(8, full.label.length))), letterSpacing: 6, fontWeight: 600, whiteSpace: 'nowrap'}}>{full.label}</div>
					<div style={{height: 4, width: 70, background: sk.accent}} />
				</div>
			</div>
			{full.compare ? (
				<Bars compare={full.compare} t={t} at={at + 0.4} until={fillEnd} sk={sk} dollar={dollar} />
			) : (
				<>
					<div
						style={{
							position: 'absolute', top: 672, left: 0, right: 0, textAlign: 'center', fontFamily: TYPE, fontSize: 40, color: sk.ink,
							opacity: interpolate(t, [fillStart, fillStart + 0.3], [0, 0.85], clamp),
						}}
					>
						<span style={{display: 'inline-flex', alignItems: 'center', gap: 12}}>
							<Figure full={full} size={50} color={sk.ink} dark={sk.dark} /> = {dollar ? `$${fmt(full.each)}` : fmt(full.each)}
						</span>
					</div>
					<div
						style={{
							position: 'absolute', top: 740, left: (1080 - cols * cell) / 2, width: cols * cell,
							display: 'grid', gridTemplateColumns: `repeat(${cols}, ${cell}px)`,
						}}
					>
						{Array.from({length: n}, (_, i) => {
							const on = i < shown;
							const pop = on ? interpolate(t, [fillStart + ((fillEnd - fillStart) * i) / n, fillStart + ((fillEnd - fillStart) * i) / n + 0.12], [1.35, 1], clamp) : 1;
							return (
								<div key={i} style={{width: cell, height: cell, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
									<div style={{transform: `scale(${pop})`, opacity: on ? 1 : 0.13}}>
										<Figure full={full} size={cell * 0.84} color={i === n - 1 && on ? sk.accent : sk.ink} dark={sk.dark} glow={i === n - 1 && on ? sk.accent : undefined} />
									</div>
								</div>
							);
						})}
					</div>
				</>
			)}
		</Paper>
	);
};

const Bars: React.FC<{compare: NonNullable<NumberFull['compare']>; t: number; at: number; until: number; sk: Skin; dollar?: boolean}> = ({compare, t, at, until, sk, dollar = false}) => {
	const max = Math.max(compare.a_value, compare.b_value) || 1;
	const grow = interpolate(t, [at, Math.max(at + 0.6, until)], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
	const H = 330;
	const bar = (label: string, value: number, x: number, red: boolean) => {
		const h = Math.max(8, (H * value) / max) * grow;
		const text = fmtBar(value, grow, dollar);
		const fontSize = text.length > 8 ? 50 : 64;
		return (
			<div style={{position: 'absolute', left: x, top: 560, width: 300, height: H + 120}}>
				<div style={{position: 'absolute', bottom: 120 + h + 10, width: '100%', textAlign: 'center', fontFamily: SERIF, fontWeight: 700, fontSize, color: red ? sk.accent : sk.ink}}>
					{text}
				</div>
				<div
					style={{
						position: 'absolute', bottom: 120, left: 50, width: 200, height: h, border: `4px solid ${sk.ink}`, boxSizing: 'border-box',
						background: `repeating-linear-gradient(135deg, ${red ? sk.accent : sk.ink} 0 3px, transparent 3px 12px)`,
					}}
				/>
				<div style={{position: 'absolute', bottom: 54, width: '100%', textAlign: 'center', fontFamily: TYPE, fontSize: 46, color: sk.ink}}>{label}</div>
			</div>
		);
	};
	return (
		<>
			{bar(compare.a_label, compare.a_value, 170, compare.a_value >= compare.b_value)}
			{bar(compare.b_label, compare.b_value, 610, compare.b_value > compare.a_value)}
			<div style={{position: 'absolute', left: 140, right: 140, top: 560 + H + 4, height: 4, background: sk.ink}} />
		</>
	);
};
