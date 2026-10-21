import type {Transition} from '../types';

/** Crossfade (the original scene change): the new scene fades in over the old one. */
export const Fade: Transition = {duration: 0.3, render: (p) => ({to: {opacity: p}})};
