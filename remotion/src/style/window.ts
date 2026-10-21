import {transitionFor} from './index';

/** When a scene's incoming transition runs: it starts `lead` seconds before the cut and `p(t)` goes 0..1 across it
 *  (an instant cut jumps from 0 to 1 at the cut). */
export const transitionWindow = (scene: {start: number; transition?: string | null}): {lead: number; p: (t: number) => number} => {
	const d = transitionFor(scene.transition).duration;
	return {
		lead: d / 2,
		p: (t: number) => (d > 0 ? Math.min(1, Math.max(0, (t - (scene.start - d / 2)) / d)) : t >= scene.start ? 1 : 0),
	};
};
