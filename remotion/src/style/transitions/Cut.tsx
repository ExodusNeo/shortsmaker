import type {Transition} from '../types';

/** Hard cut: the new scene replaces the old one in a single frame. */
export const Cut: Transition = {duration: 0, render: (p) => ({to: {opacity: p >= 0.5 ? 1 : 0}})};
