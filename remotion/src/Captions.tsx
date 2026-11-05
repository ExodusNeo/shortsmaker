import {spring, useVideoConfig} from 'remotion';
import {outline} from './Graphics';
import type {Word} from './Short';

// Owner, 2026-11-05: clean captions like the "Second Draw" Short: one word (or two short ones) at a time, white
// with a black outline, as spoken. Same font and sizing as audio_mix.captions (the Python renderer).
const CAPTION_FONT = '"Segoe UI Black", "Arial Black", sans-serif';

/** One caption line at a time (lines come from Python's caption_lines()), springing in slightly. */
export const Captions: React.FC<{words: Word[]; t: number}> = ({words, t}) => {
	const {fps} = useVideoConfig();
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
	const text = chunk.map((w) => w.text).join(' ');
	const lineIn = spring({frame: (t - chunk[0].start) * fps, fps, config: {damping: 14, stiffness: 260}});
	return (
		<div
			style={{
				position: 'absolute', left: 60, right: 60, bottom: 620, textAlign: 'center', whiteSpace: 'nowrap',
				transform: `scale(${0.86 + 0.14 * lineIn})`, fontFamily: CAPTION_FONT, color: 'white',
				fontSize: Math.min(110, 960 / (text.length * 0.62)), lineHeight: 1.05,
				textShadow: `${outline(7)}, 0 4px 10px rgba(0,0,0,0.5)`,
			}}
		>
			{text}
		</div>
	);
};
