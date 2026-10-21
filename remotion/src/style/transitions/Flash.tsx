import type {Transition} from '../types';

/** Camera-flash cut: a hard cut; the white flash itself is drawn by Short.tsx's flash layer (with its sound). */
export const Flash: Transition = {duration: 0, render: (p) => ({to: {opacity: p >= 0.5 ? 1 : 0}})};
