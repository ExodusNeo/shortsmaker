// Question beat (idea: Showtime's question-beat): at a cliffhanger the picture dims and a big question pops up and holds,
// so the viewer stops to wonder. The script answers it later.
import React from 'react';
import {AbsoluteFill, CAPTION_TOP, CLAMP, Easing, FONT, interpolate, outline, theme} from '../kit';
import type {Overlay} from '../types';

const TOP = 430;

export const QuestionBeat: Overlay = ({graphic, t, start, end}) => {
	if (t < start || t > end) return null;
	const tin = t - start;
	const out = interpolate(t, [end - 0.2, end], [1, 0], CLAMP);
	const dim = interpolate(tin, [0, 0.25], [0, 0.3], CLAMP) * out;
	const scale = interpolate(tin, [0, 0.35], [0.6, 1], {...CLAMP, easing: Easing.out(Easing.back(1.7))});
	const pulse = 1 + 0.02 * Math.sin(Math.max(0, tin - 0.35) * Math.PI * 1.6); // a gentle breath while it holds
	const text = graphic.text.replace(/\?+$/, '');
	const size = graphic.text.length <= 12 ? 150 : graphic.text.length <= 22 ? 120 : 96;
	return (
		<AbsoluteFill>
			<AbsoluteFill style={{backgroundColor: '#000', opacity: dim}} />
			<div
				style={{
					position: 'absolute', left: 70, right: 70, top: TOP, height: CAPTION_TOP - 60 - TOP, display: 'flex',
					alignItems: 'center', justifyContent: 'center', opacity: interpolate(tin, [0, 0.12], [0, 1], CLAMP) * out,
				}}
			>
				<div
					style={{
						fontFamily: FONT, fontSize: size, lineHeight: 1.05, color: 'white', textAlign: 'center',
						textShadow: outline(7), transform: `scale(${scale * pulse})`,
						...({textWrap: 'balance'} as React.CSSProperties), // even lines, no lonely last word
					}}
				>
					{text}
					<span style={{color: theme.accent}}>?</span>
				</div>
			</div>
		</AbsoluteFill>
	);
};
