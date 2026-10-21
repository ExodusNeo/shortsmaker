// Light leak: a warm film burn flares over the cut while the new scene fades in underneath it.
import React from 'react';
import {clamp01} from '../kit';
import type {Transition} from '../types';

export const Leak: Transition = {
	duration: 0.5,
	render: (p, _inks, seed) => {
		const glow = 0.85 * Math.sin(Math.PI * clamp01(p));
		const x = 30 + (seed * 37) % 40; // the burn's centre moves a little from Short to Short
		return {
			to: {opacity: clamp01((p - 0.3) / 0.4)},
			cover: glow > 0.01 ? (
				<div
					style={{
						position: 'absolute', inset: 0, opacity: glow, mixBlendMode: 'screen',
						background: `radial-gradient(ellipse at ${x}% 40%, #FFE2A8 0%, #FFB347 30%, rgba(255,90,40,0.6) 55%, rgba(0,0,0,0) 80%)`,
					}}
				/>
			) : null,
		};
	},
};
