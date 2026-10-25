// Whip pan: the old scene flies off to the left with motion blur while the new one flies in edge-to-edge from the right.
import {clamp01} from '../kit';
import type {Transition} from '../types';

export const Whip: Transition = {
	duration: 0.25,
	render: (p) => {
		const k = clamp01(p);
		const e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
		const s = 1 + 0.08 * Math.sin(Math.PI * k);
		const blur = 16 * Math.sin(Math.PI * k);
		return {
			from: {transform: `translateX(${-100 * e}%) scale(${s})`, filter: `blur(${blur}px)`},
			to: k <= 0 ? {opacity: 0} : {opacity: 1, transform: `translateX(${100 * (1 - e)}%) scale(${s})`, filter: `blur(${blur}px)`},
		};
	},
};
