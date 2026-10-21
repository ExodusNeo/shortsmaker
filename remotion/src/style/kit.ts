// Helpers for looks, overlays and transitions (presets and AI inventions import only from here, '../types' and react).
import {useEffect, useState} from 'react';
import {continueRender, delayRender} from 'remotion';
import type {Inks} from './types';

export type {Inks, Look, LookProps, Overlay, OverlayProps, Transition, TransitionFrame} from './types';
export {interpolate, spring, Easing, Img, AbsoluteFill} from 'remotion';
// the Short's shared graphic language: palette (`theme`, filled per Short), display font, text outline, graphic slot
export {theme, FONT, outline, slot} from '../Graphics';
export const CLAMP = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
/** Captions start at y 1150: nothing an overlay draws may come lower. */
export const CAPTION_TOP = 1150;

export const W = 1080;
export const H = 1920;
/** How a look shows its picture: fills the frame like the plain picture does. */
export const FILL = {width: '100%', height: '100%', objectFit: 'cover'} as const;

export const inksOf = (theme: {accent: string; emphasis: string; panel: string}): Inks => ({
	paper: '#EFE6D2',
	ink: theme.panel,
	accent: theme.accent,
	alarm: theme.emphasis,
});

/** Deterministic pseudo-random number in [0, 1) for a seed and a position/time (same inputs, same frame). */
export const noise = (seed: number, x: number): number => {
	const v = Math.sin(seed * 12.9898 + x * 78.233) * 43758.5453;
	return v - Math.floor(v);
};

export const clamp01 = (x: number): number => Math.min(1, Math.max(0, x));

/** Draws `img` to fill w x h like CSS object-fit: cover. */
export const drawCover = (ctx: CanvasRenderingContext2D, img: HTMLImageElement, w: number, h: number): void => {
	const s = Math.max(w / img.naturalWidth, h / img.naturalHeight);
	const dw = img.naturalWidth * s;
	const dh = img.naturalHeight * s;
	ctx.drawImage(img, (w - dw) / 2, (h - dh) / 2, dw, dh);
};

/** Luminance 0..1 of every pixel of `img` drawn cover-fit at w x h (for dot screens, hatching, ink bands). */
export const luminance = (ctx: CanvasRenderingContext2D, img: HTMLImageElement, w: number, h: number): Float32Array => {
	drawCover(ctx, img, w, h);
	const d = ctx.getImageData(0, 0, w, h).data;
	const out = new Float32Array(w * h);
	for (let i = 0; i < w * h; i++) out[i] = (0.299 * d[i * 4] + 0.587 * d[i * 4 + 1] + 0.114 * d[i * 4 + 2]) / 255;
	return out;
};

/** Auto levels: stretches luminance so the darkest 2 % become 0 and the lightest 2 % become 1 (faded archive photos
 *  otherwise turn into one flat tone in a dot or line look). Returns a new array. */
export const stretch = (lum: Float32Array): Float32Array => {
	const sorted = Float32Array.from(lum.filter((_, i) => i % 97 === 0)).sort();
	const lo = sorted[Math.floor(sorted.length * 0.02)];
	const hi = sorted[Math.floor(sorted.length * 0.98)];
	const span = Math.max(0.05, hi - lo);
	return lum.map((v) => clamp01((v - lo) / span));
};

/** Draws a styled version of the picture ONCE per scene on a 1080x1920 canvas and returns it as a data URL
 *  (the render waits for it). null while loading or when the picture can't be read: show the plain picture then. */
export const useOnceCanvas = (
	src: string,
	draw: (ctx: CanvasRenderingContext2D, img: HTMLImageElement, w: number, h: number) => void,
): string | null => {
	const [url, setUrl] = useState<string | null>(null);
	const [handle] = useState(() => delayRender(`style look for ${src}`));
	useEffect(() => {
		const img = new Image();
		img.onload = () => {
			try {
				const c = document.createElement('canvas');
				c.width = W;
				c.height = H;
				const ctx = c.getContext('2d', {willReadFrequently: true});
				if (ctx) {
					draw(ctx, img, W, H);
					setUrl(c.toDataURL('image/jpeg', 0.92));
				}
			} catch {
				setUrl(null); // a tainted or broken picture: the look shows the plain picture instead
			}
			continueRender(handle);
		};
		img.onerror = () => continueRender(handle);
		img.src = src;
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [src]);
	return url;
};
