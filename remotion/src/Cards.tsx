import {Easing, Img, interpolate, staticFile} from 'remotion';
import {FONT, moveIn, outline, slot, useWindow, theme} from './Graphics';
import type {Graphic} from './Short';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const card: React.CSSProperties = {
	background: 'rgba(8,10,16,0.84)', border: '4px solid rgba(255,255,255,0.85)', borderRadius: 32,
	boxShadow: '0 22px 50px rgba(0,0,0,0.55)', textAlign: 'center',
};
type Props = {graphic: Graphic; t: number; start: number; end: number; variant: number};

const formatStat = (value: number, k: number, of?: number, dollar?: boolean) => {
	const prefix = dollar ? '$' : '';
	if (!of && value >= 1_000_000_000 && value % 10_000_000 === 0) {
		const b = value / 1_000_000_000;
		const dec = Number.isInteger(b) ? 0 : b * 10 === Math.floor(b * 10) ? 1 : 2;
		return `${prefix}${(b * k).toFixed(dec)}B`;
	}
	if (!of && value >= 1_000_000 && value % 10_000 === 0) {
		const m = value / 1_000_000;
		const dec = Number.isInteger(m) ? 0 : m * 10 === Math.floor(m * 10) ? 1 : 2;
		return `${prefix}${(m * k).toFixed(dec)}M`;
	}
	const num = Number.isInteger(value) ? Math.round(value * k).toLocaleString('en-US') : (value * k).toFixed(1);
	return `${prefix}${num}`;
};

/** A number worth seeing: with `of`, a grid of dots where `value` of them light up one by one;
 * without, a big counter ticking up to `value` (or ticking down to `value` when `direction === 'down'`). */
export const StatCard: React.FC<Props> = ({graphic, t, start, end, variant}) => {
	const {visible, enter, leave, tIn, ready} = useWindow(t, start, end);
	if (!visible) return null;
	const value = graphic.value ?? 0;
	const of = graphic.of;
	const p = interpolate(t, [tIn + 0.25, Math.min(tIn + 1.25, ready)], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
	const startRatio = !of && graphic.direction === 'down'
		? (graphic.from_value && graphic.from_value > value ? graphic.from_value / Math.max(1e-6, value) : 2.5)
		: 0;
	const k = startRatio + (1 - startRatio) * p;
	const dollar = !of && ((graphic.trigger ?? '').trim().startsWith('$') || /\bDOLLARS?\b/i.test(graphic.text) || graphic.text.includes('$'));
	const shown = formatStat(value, k, of, dollar);
	const fontSize = of ? 110 : shown.length > 9 ? 120 : shown.length > 7 ? 145 : 170;
	return (
		<div style={{position: 'absolute', ...slot(graphic, 260), left: 0, right: 0, display: 'flex', justifyContent: 'center', ...moveIn(enter, leave, variant)}}>
			<div style={{...card, padding: '26px 44px 22px', maxWidth: 920}}>
				{of ? <DotGrid of={of} lit={Math.round(value * p)} /> : null}
				<div style={{fontFamily: FONT, fontSize, lineHeight: 1, color: theme.accent, textShadow: outline(6)}}>
					{shown}
					{of ? <span style={{color: 'white', fontSize: 70}}> / {of}</span> : null}
				</div>
				<div style={{fontFamily: FONT, fontSize: 64, color: 'white', marginTop: 8}}>{graphic.text}</div>
			</div>
		</div>
	);
};

const DotGrid: React.FC<{of: number; lit: number}> = ({of, lit}) => {
	const cols = Math.min(20, Math.ceil(Math.sqrt(of * 2)));
	const size = Math.min(48, Math.floor(780 / cols));
	return (
		<div style={{display: 'grid', gridTemplateColumns: `repeat(${cols}, ${size}px)`, justifyContent: 'center', marginBottom: 16}}>
			{Array.from({length: of}, (_, n) => (
				<div key={n} style={{width: size, height: size, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
					<div
						style={{
							width: size * 0.74, height: size * 0.74, borderRadius: '50%',
							background: n < lit ? theme.accent : 'rgba(255,255,255,0.16)', boxShadow: n < lit ? `0 0 ${size * 0.3}px ${theme.accent}99` : 'none',
						}}
					/>
				</div>
			))}
		</div>
	);
};

/** Time passing between two moments: a marker slides along a line from `start` to `end`, the gap
 * ("17 HOURS LATER") above it. */
export const TimelineCard: React.FC<Props> = ({graphic, t, start, end, variant}) => {
	const {visible, enter, leave, tIn, ready} = useWindow(t, start, end);
	if (!visible) return null;
	const p = interpolate(t, [tIn + 0.35, Math.min(tIn + 1.35, ready)], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const L = 720;
	const x = 40 + L * p;
	return (
		<div style={{position: 'absolute', ...slot(graphic, 290), left: 0, right: 0, display: 'flex', justifyContent: 'center', ...moveIn(enter, leave, variant)}}>
			<div style={{...card, padding: '24px 30px 22px', width: 860}}>
				<div style={{fontFamily: FONT, fontSize: 84, color: theme.accent, textShadow: outline(5), lineHeight: 1.05}}>{graphic.text}</div>
				<svg width={800} height={90} style={{display: 'block', margin: '10px auto 0'}}>
					<line x1={40} y1={45} x2={40 + L} y2={45} stroke="rgba(255,255,255,0.35)" strokeWidth={10} strokeLinecap="round" />
					<line x1={40} y1={45} x2={x} y2={45} stroke={theme.accent} strokeWidth={10} strokeLinecap="round" />
					<circle cx={40} cy={45} r={16} fill="white" />
					<circle cx={40 + L} cy={45} r={16} fill={p >= 1 ? theme.accent : 'white'} />
					<circle cx={x} cy={45} r={26} fill={theme.accent} stroke="#000" strokeWidth={5} />
				</svg>
				<div style={{display: 'flex', justifyContent: 'space-between', fontFamily: FONT, fontSize: 48, color: 'white', padding: '0 4px'}}>
					<span>{graphic.start}</span>
					<span>{graphic.end}</span>
				</div>
			</div>
		</div>
	);
};

/** The chosen picture as a framed card: a hand-drawn circle (or arrow) draws itself around one
 * detail, then the card slowly pushes in toward it. The background keeps moving behind, so the mark
 * lives on this still card where its position is exact. */
export const MarkCard: React.FC<Props> = ({graphic, t, start, end, variant}) => {
	const {visible, enter, leave, tIn} = useWindow(t, start, end);
	if (!visible || !graphic.image) return null;
	const a = graphic.aspect ?? 1;
	const bw = a >= 880 / 860 ? 880 : Math.round(860 * a);
	const bh = Math.round(bw / a);
	const x = (graphic.x ?? 0.5) * bw;
	const y = (graphic.y ?? 0.5) * bh;
	const r = Math.max(60, Math.min(bw, bh) * 0.13);
	const draw = interpolate(t, [tIn + 0.35, tIn + 0.95], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const push = interpolate(t, [tIn + 1.0, end], [1, 1.35], {...clamp, easing: Easing.inOut(Easing.sin)});
	// Arrow comes in from the side with more room, aimed at the detail.
	const ux = x > bw / 2 ? -1 : 1;
	const uy = y > bh / 2 ? -0.7 : 0.7;
	const n = Math.hypot(ux, uy);
	const [tx, ty] = [x + (ux / n) * r * 2.6, y + (uy / n) * r * 2.6];
	const [hx, hy] = [x + (ux / n) * r * 0.45, y + (uy / n) * r * 0.45];
	const ang = Math.atan2(hy - ty, hx - tx);
	const head = (s: number) => `${hx + 46 * Math.cos(ang + Math.PI + s)},${hy + 46 * Math.sin(ang + Math.PI + s)}`;
	const stroke = {fill: 'none', stroke: theme.accent, strokeWidth: 11, strokeLinecap: 'round' as const, pathLength: 1, strokeDasharray: 1};
	return (
		<div style={{position: 'absolute', top: 200, left: 0, right: 0, display: 'flex', justifyContent: 'center', ...moveIn(enter, leave, variant)}}>
			<div style={{width: bw, height: bh, position: 'relative', overflow: 'hidden', borderRadius: 28, border: '5px solid white', boxShadow: '0 24px 60px rgba(0,0,0,0.6)', background: '#000'}}>
				<div style={{position: 'absolute', inset: 0, transform: `scale(${push})`, transformOrigin: `${x}px ${y}px`}}>
					<Img src={staticFile(graphic.image)} style={{width: bw, height: bh, display: 'block'}} />
					<svg width={bw} height={bh} style={{position: 'absolute', left: 0, top: 0, filter: 'drop-shadow(0 0 6px rgba(0,0,0,0.8))'}}>
						{graphic.shape === 'arrow' ? (
							<>
								<line x1={tx} y1={ty} x2={hx} y2={hy} {...stroke} strokeDashoffset={1 - draw} />
								{draw > 0.97 ? <polyline points={`${head(0.5)} ${hx},${hy} ${head(-0.5)}`} {...stroke} pathLength={undefined} strokeDasharray={undefined} strokeLinejoin="round" /> : null}
							</>
						) : (
							<ellipse cx={x} cy={y} rx={r * 1.15} ry={r} transform={`rotate(-8 ${x} ${y})`} {...stroke} strokeDashoffset={1 - draw} />
						)}
					</svg>
				</div>
				<div
					style={{
						position: 'absolute', left: 0, right: 0, bottom: 22, display: 'flex', justifyContent: 'center',
						opacity: interpolate(draw, [0.7, 1], [0, 1], clamp), transform: `translateY(${interpolate(draw, [0.7, 1], [24, 0], clamp)}px)`,
					}}
				>
					<div style={{background: theme.accent, border: '5px solid #000', borderRadius: 16, padding: '6px 26px', fontFamily: FONT, fontSize: 58, color: '#000'}}>
						{graphic.text}
					</div>
				</div>
			</div>
		</div>
	);
};
