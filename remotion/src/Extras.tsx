import {Easing, interpolate, spring, useVideoConfig} from 'remotion';
import {FONT, moveIn, outline, slot, useWindow, theme} from './Graphics';
import type {Graphic} from './Short';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const SERIF = 'Georgia, "Times New Roman", serif';
const PAPER = '#efe4c8';
const INK = '#1d1a14';
type Props = {graphic: Graphic; t: number; start: number; end: number; variant: number};

/** Newspaper front page: drops in tilted with a slight overshoot, then settles. */
export const HeadlineCard: React.FC<Props> = ({graphic, t, start, end}) => {
	const {fps} = useVideoConfig();
	const {visible, leave, tIn} = useWindow(t, start, end);
	if (!visible) return null;
	const slam = spring({frame: (t - tIn) * fps, fps, config: {damping: 11, stiffness: 220}});
	return (
		<div style={{position: 'absolute', ...slot(graphic, 250), left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: 1 - leave}}>
			<div
				style={{
					width: 860, background: PAPER, color: INK, padding: '26px 40px 30px', boxShadow: '0 26px 60px rgba(0,0,0,0.6)',
					transform: `scale(${interpolate(slam, [0, 1], [1.5, 1])}) rotate(${interpolate(slam, [0, 1], [-14, -3])}deg) translateY(${-160 * leave}px)`,
					textAlign: 'center', borderTop: `8px double ${INK}`,
				}}
			>
				<div style={{fontFamily: SERIF, fontSize: 46, fontWeight: 700, letterSpacing: 2}}>{graphic.paper || 'EXTRA! EXTRA!'}</div>
				{graphic.date ? <div style={{fontFamily: SERIF, fontSize: 26, borderTop: `2px solid ${INK}`, borderBottom: `2px solid ${INK}`, margin: '10px 0 16px', padding: '4px 0'}}>{graphic.date}</div> : <div style={{height: 14}} />}
				<div style={{fontFamily: FONT, fontSize: graphic.text.length > 26 ? 76 : 96, lineHeight: 1.02}}>{graphic.text}</div>
			</div>
		</div>
	);
};

/** A real quote typed out letter by letter on aged paper, then the speaker's name. */
export const QuoteCard: React.FC<Props> = ({graphic, t, start, end, variant}) => {
	const {visible, enter, leave, tIn, ready} = useWindow(t, start, end);
	if (!visible) return null;
	const typedEnd = Math.max(tIn + 0.3, Math.min(tIn + 0.25 + graphic.text.length * 0.035, ready - 0.25));
	const typed = Math.round(interpolate(t, [tIn + 0.25, typedEnd], [0, graphic.text.length], clamp));
	const byIn = interpolate(t, [typedEnd + 0.1, typedEnd + 0.35], [0, 1], clamp);
	return (
		<div style={{position: 'absolute', ...slot(graphic, 260), left: 0, right: 0, display: 'flex', justifyContent: 'center', ...moveIn(enter, leave, variant)}}>
			<div style={{width: 840, background: PAPER, color: INK, borderRadius: 10, padding: '30px 46px 26px', boxShadow: '0 22px 50px rgba(0,0,0,0.55)', transform: 'rotate(-1.5deg)'}}>
				<div style={{fontFamily: SERIF, fontSize: 110, lineHeight: 0.6, height: 46, color: '#8a6d2f'}}>&ldquo;</div>
				<div style={{fontFamily: '"Courier New", Courier, monospace', fontWeight: 700, fontSize: 50, lineHeight: 1.25, minHeight: 64}}>
					{graphic.text.slice(0, typed)}
					<span style={{opacity: typed < graphic.text.length ? 1 : 0}}>|</span>
				</div>
				<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 40, textAlign: 'right', marginTop: 14, opacity: byIn}}>&mdash; {graphic.by}</div>
			</div>
		</div>
	);
};

/** Two bars grow side by side to their values (bar length relative to the larger one). */
export const CompareCard: React.FC<Props> = ({graphic, t, start, end, variant}) => {
	const {visible, enter, leave, tIn, ready} = useWindow(t, start, end);
	if (!visible) return null;
	const a = graphic.a_value ?? 1;
	const b = graphic.b_value ?? 1;
	const top = Math.max(a, b);
	const s = Math.min(1, (ready - tIn) / 1.55); // both bars grown before the exit
	const grow = (delay: number) => interpolate(t, [tIn + delay * s, tIn + (delay + 0.8) * s], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
	const row = (label: string, show: string, v: number, k: number, color: string) => (
		<div style={{marginTop: 14}}>
			<div style={{display: 'flex', justifyContent: 'space-between', fontFamily: FONT, fontSize: 52, color: 'white'}}>
				<span>{label}</span>
				<span style={{color, opacity: k}}>{show}</span>
			</div>
			<div style={{height: 44, borderRadius: 22, background: 'rgba(255,255,255,0.15)', marginTop: 6}}>
				<div style={{height: 44, borderRadius: 22, background: color, width: `${Math.max(4, (100 * v) / top) * k}%`}} />
			</div>
		</div>
	);
	return (
		<div style={{position: 'absolute', ...slot(graphic, 270), left: 0, right: 0, display: 'flex', justifyContent: 'center', ...moveIn(enter, leave, variant)}}>
			<div style={{width: 860, background: 'rgba(8,10,16,0.84)', border: '4px solid rgba(255,255,255,0.85)', borderRadius: 32, padding: '22px 40px 30px', boxShadow: '0 22px 50px rgba(0,0,0,0.55)'}}>
				<div style={{fontFamily: FONT, fontSize: 64, color: theme.accent, textAlign: 'center', textShadow: outline(4)}}>{graphic.text}</div>
				{row(graphic.a_label ?? '', graphic.a_show ?? '', a, grow(0.25), 'white')}
				{row(graphic.b_label ?? '', graphic.b_show ?? '', b, grow(0.75), theme.accent)}
			</div>
		</div>
	);
};

/** Red rubber stamp: drops from big to its size with a hard landing, slightly crooked, rough ink. */
export const StampCard: React.FC<Props> = ({graphic, t, start, end}) => {
	const {fps} = useVideoConfig();
	const {visible, leave, tIn} = useWindow(t, start, end);
	if (!visible) return null;
	const land = spring({frame: (t - tIn) * fps, fps, config: {damping: 14, stiffness: 320}});
	const red = '#d4231c';
	return (
		<div style={{position: 'absolute', ...slot(graphic, 330), left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: Math.min(1, land * 3) * (1 - leave)}}>
			{/* A paper slip under the ink: red on red brick (Voigt Short, 2026-10-16) was unreadable without it. */}
			<div style={{transform: `scale(${interpolate(land, [0, 1], [2.4, 1])}) rotate(-12deg)`, background: PAPER, padding: '18px 22px', borderRadius: 6, boxShadow: '0 18px 40px rgba(0,0,0,0.55)'}}>
				<div
					style={{
						border: `12px solid ${red}`, borderRadius: 18, padding: '6px 34px', fontFamily: FONT,
						fontSize: graphic.text.length > 8 ? 104 : 150, letterSpacing: 6, color: red, whiteSpace: 'nowrap',
						boxShadow: `inset 0 0 0 6px rgba(212,35,28,0.35)`,
						WebkitMaskImage: 'repeating-linear-gradient(115deg, #000 0 9px, rgba(0,0,0,0.72) 9px 12px)',
					}}
				>
					{graphic.text}
				</div>
			</div>
		</div>
	);
};
