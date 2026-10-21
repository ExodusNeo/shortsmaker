// Kinetic title (ideas: Showtime's kinetic type, Lemo-OPUSCAR's per-glyph pop): a spoken phrase whose letters drop in one
// by one and squash as they land, with an off-register shadow in the Short's accent colour.
import React from 'react';
import {CLAMP, Easing, FONT, interpolate, slot, theme} from '../kit';
import type {Overlay} from '../types';

const STAGGER = 0.05;
const LAND = 0.3;

export const KineticTitle: Overlay = ({graphic, t, start, end}) => {
	if (t < start || t > end) return null;
	const glyphs = [...graphic.text];
	const size = Math.min(130, 1800 / Math.max(8, glyphs.length)); // a long phrase gets smaller letters, never wraps
	const out = interpolate(t, [end - 0.2, end], [1, 0], CLAMP);
	return (
		<div style={{position: 'absolute', ...slot(graphic, 300), left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: out}}>
			<div style={{fontFamily: FONT, fontSize: size, lineHeight: 1, whiteSpace: 'pre', display: 'flex'}}>
				{glyphs.map((g, i) => {
					const local = t - start - i * STAGGER;
					const y = interpolate(local, [0, LAND], [-60, 0], {...CLAMP, easing: Easing.out(Easing.back(2))});
					const squash = interpolate(local, [LAND * 0.6, LAND, LAND * 1.4], [1, 1.15, 1], CLAMP); // lands, squashes, settles
					return (
						<span
							key={i}
							style={{
								display: 'inline-block', color: 'white', opacity: local > 0 ? 1 : 0,
								transform: `translateY(${y}px) scale(${squash}, ${2 - squash})`, transformOrigin: '50% 100%',
								textShadow: `8px 8px 0 ${theme.accent}, 0 0 6px rgba(0,0,0,0.6)`, WebkitTextStroke: '3px #000',
							}}
						>
							{g}
						</span>
					);
				})}
			</div>
		</div>
	);
};
