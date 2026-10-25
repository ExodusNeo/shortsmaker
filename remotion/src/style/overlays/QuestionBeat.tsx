// Question beat (idea: Showtime's question-beat): at a cliffhanger the picture dims and a big question pops up and holds,
// so the viewer stops to wonder. The script answers it later.
import React from 'react';
import {AbsoluteFill, CLAMP, Easing, FONT, interpolate, outline, slot, theme} from '../kit';
import type {Overlay} from '../types';

export const QuestionBeat: Overlay = ({graphic, t, start, end}) => {
	const tOut = end - 0.28;
	if (t < start || t > tOut) return null;
	const tin = t - start;
	const out = interpolate(t, [tOut - 0.22, tOut], [1, 0], CLAMP);
	const dim = interpolate(tin, [0, 0.25], [0, 0.22], CLAMP) * out;
	const scale = interpolate(tin, [0, 0.32], [0.68, 1], {...CLAMP, easing: Easing.out(Easing.back(1.7))});
	const pulse = 1 + 0.02 * Math.sin(Math.max(0, tin - 0.32) * Math.PI * 1.6); // a gentle breath while it holds
	const text = graphic.text.replace(/\?+$/, '');
	const size = graphic.text.length <= 12 ? 140 : graphic.text.length <= 22 ? 110 : 90;
	return (
		<AbsoluteFill>
			<AbsoluteFill style={{backgroundColor: '#000', opacity: dim}} />
			<div
				style={{
					position: 'absolute', ...slot(graphic, 300), left: 60, right: 60, display: 'flex',
					alignItems: 'center', justifyContent: 'center', opacity: interpolate(tin, [0, 0.12], [0, 1], CLAMP) * out,
				}}
			>
				<div
					style={{
						background: 'rgba(8,10,16,0.82)', border: '4px solid rgba(255,255,255,0.82)', borderRadius: 28,
						padding: '20px 38px 24px', boxShadow: '0 22px 50px rgba(0,0,0,0.58)',
						fontFamily: FONT, fontSize: size, lineHeight: 1.05, color: 'white', textAlign: 'center',
						textShadow: outline(7), transform: `scale(${scale * pulse})`, maxWidth: 920,
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
