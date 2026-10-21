// Dot wipe (idea: Lemo-OPUSCAR Halftone Dossier): a grid of ink dots grows over the frame from one corner, the scene
// switches while it is covered, then the dots shrink away.
import React from 'react';
import {H, W, clamp01} from '../kit';
import type {Transition} from '../types';

const STEP = 72;
const R = STEP * 0.75; // a dot this big covers its whole cell
const SPREAD = 0.3; // how much later the far corner starts than the near one (fraction of the transition)

export const Wipe: Transition = {
	duration: 0.44,
	render: (p, inks) => {
		const dots: React.ReactNode[] = [];
		if (p > 0 && p < 1) {
			for (let y = STEP / 2; y < H + STEP; y += STEP) {
				for (let x = STEP / 2; x < W + STEP; x += STEP) {
					const d = ((x + y) / (W + H)) * SPREAD; // diagonal delay
					const grow = clamp01((p - d) / (0.5 - d));
					const shrink = clamp01((p - 0.5 - d) / (0.5 - d));
					const r = R * (p <= 0.5 ? grow : 1 - shrink);
					if (r > 0.5) dots.push(<circle key={`${x}-${y}`} cx={x} cy={y} r={r} />);
				}
			}
		}
		return {
			to: {opacity: p >= 0.5 ? 1 : 0},
			cover: dots.length ? (
				<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute', inset: 0}} fill={inks.ink}>
					{dots}
				</svg>
			) : null,
		};
	},
};
