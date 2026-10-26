// Kinetic title (ideas: Showtime's kinetic type, Lemo-OPUSCAR's per-glyph pop): a spoken phrase whose letters drop in one
// by one and squash as they land, with an off-register shadow in the Short's accent colour.
import React from 'react';
import {CLAMP, Easing, FONT, interpolate, slot, theme} from '../kit';
import type {Overlay} from '../types';

const STAGGER = 0.032;
const LAND = 0.22;

export const KineticTitle: Overlay = ({graphic, t, start, end}) => {
	const tOut = end - 0.18;
	if (t < start || t > tOut) return null;
	const glyphs = [...graphic.text];
	const stagger = Math.min(STAGGER, 0.42 / Math.max(1, glyphs.length));
	const size = Math.min(124, 1680 / Math.max(8, glyphs.length)); // a long phrase gets smaller letters, never wraps
	const out = interpolate(t, [tOut - 0.18, tOut], [1, 0], CLAMP);
	return (
		<div style={{position: 'absolute', ...slot(graphic, 300), left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: out}}>
			<div
				style={{
					background: 'rgba(8,10,16,0.82)', border: '4px solid rgba(255,255,255,0.82)', borderRadius: 28,
					padding: '18px 38px 24px', boxShadow: '0 22px 50px rgba(0,0,0,0.58)',
					fontFamily: FONT, fontSize: size, lineHeight: 1, whiteSpace: 'pre', display: 'flex',
				}}
			>
				{glyphs.map((g, i) => {
					const local = t - start - i * stagger;
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
