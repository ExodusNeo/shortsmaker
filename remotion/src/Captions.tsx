import {spring, useVideoConfig} from 'remotion';
import {FONT, outline, theme} from './Graphics';
import type {Word} from './Short';


/** One caption line at a time; the word being spoken turns yellow and pops, each new line springs in,
 * and the scene's emphasis word glows orange from when it's said until its line ends. */
export const Captions: React.FC<{words: Word[]; t: number}> = ({words, t}) => {
	const {fps} = useVideoConfig();
	// Lines come from Python's caption_lines() (up to 3 words, about 16 letters).
	let chunk: Word[] = [];
	for (let k = 0, e = 0; k < words.length; k = e) {
		for (e = k; e < words.length && words[e].line === words[k].line; e++);
		const end = e < words.length ? words[e].start : words[e - 1].end;
		if (t >= words[k].start && t < end) {
			chunk = words.slice(k, e);
			break;
		}
	}
	if (!chunk.length) return null;
	const lineIn = spring({frame: (t - chunk[0].start) * fps, fps, config: {damping: 14, stiffness: 240}});
	// Always one line: shrink long lines instead of wrapping into the graphics above.
	// Impact's uppercase glyphs average about 0.5em wide; the 0.6 budget leaves room for a word growing 15%.
	const chars = chunk.reduce((n, w) => n + w.text.length, 0) + chunk.length;
	const fontSize = Math.min(120, 980 / (chars * 0.6));
	return (
		<div
			style={{
				position: 'absolute', left: 30, right: 30, bottom: 620, textAlign: 'center', whiteSpace: 'nowrap',
				transform: `scale(${0.8 + 0.2 * lineIn})`, fontFamily: FONT, fontSize, lineHeight: 1.05,
				textTransform: 'uppercase', textShadow: outline(8),
			}}
		>
			{chunk.map((w, k) => {
				const spoken = t >= w.start;
				const active = spoken && (k === chunk.length - 1 || t < chunk[k + 1].start);
				// Emphasis words light up orange with a glow when said and stay lit until the line ends.
				const lit = w.emphasis && spoken;
				const pop = active || lit ? spring({frame: (t - w.start) * fps, fps, config: {damping: 12, stiffness: 300}}) : 0;
				return (
					<span
						key={k}
						style={{
							// Grow via font size (takes up layout space) so neighbours move aside instead of overlapping.
							color: lit ? theme.emphasis : active ? theme.accent : 'white', display: 'inline-block', margin: '0 14px',
							fontSize: `${lit ? 1 + 0.15 * pop : 1 + 0.06 * pop}em`, verticalAlign: 'baseline',
							textShadow: lit
								? `${outline(8)}, 0 0 28px rgba(255,140,0,0.95), 0 0 60px rgba(255,120,0,0.7)`
								: active ? `${outline(8)}, 0 0 24px ${theme.accent}99` : undefined,
						}}
					>
						{w.text}
					</span>
				);
			})}
		</div>
	);
};
