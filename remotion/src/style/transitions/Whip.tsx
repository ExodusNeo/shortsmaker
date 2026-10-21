// Whip pan: the old scene flies off to the left with motion blur, the new one flies in from the right.
import {clamp01} from '../kit';
import type {Transition} from '../types';

export const Whip: Transition = {
	duration: 0.25,
	render: (p) => {
		const out = clamp01(p / 0.5);
		const inn = clamp01((p - 0.5) / 0.5);
		return {
			from: {transform: `translateX(${-35 * out}%)`, filter: `blur(${18 * out}px)`},
			to: p < 0.5 ? {opacity: 0} : {opacity: 1, transform: `translateX(${35 * (1 - inn)}%)`, filter: `blur(${18 * (1 - inn)}px)`},
		};
	},
};
