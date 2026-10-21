// Halftone dossier (idea: Lemo-OPUSCAR "Halftone Dossier"): a retro two-tone print on cream paper. The photo stays
// readable as an ink duotone; a fine dot screen in the ink and an off-register accent screen sit on top as texture.
// (Owner 2026-10-19: a picture built ONLY from dots was unreadable on a phone.)
import React from 'react';
import {FILL, Img, luminance, noise, stretch, useOnceCanvas} from '../kit';
import type {Inks, Look} from '../types';

const STEP = 8;
const rgb = (hex: string) => {
	const v = parseInt(hex.replace('#', '').slice(0, 6), 16);
	return [(v >> 16) & 255, (v >> 8) & 255, v & 255];
};

const screen = (ctx: CanvasRenderingContext2D, lum: Float32Array, w: number, h: number, deg: number, ink: string,
	density: (l: number) => number, dx: number) => {
	const a = (deg * Math.PI) / 180;
	const [c, s] = [Math.cos(a), Math.sin(a)];
	const reach = Math.hypot(w, h) / 2 + STEP;
	ctx.fillStyle = ink;
	ctx.beginPath();
	for (let v = -reach; v < reach; v += STEP) {
		for (let u = -reach; u < reach; u += STEP) {
			const x = w / 2 + u * c - v * s;
			const y = h / 2 + u * s + v * c;
			if (x < -STEP || y < -STEP || x > w + STEP || y > h + STEP) continue;
			const l = lum[Math.min(h - 1, Math.max(0, Math.round(y))) * w + Math.min(w - 1, Math.max(0, Math.round(x)))];
			const r = STEP * 0.72 * density(l);
			if (r < 0.5) continue;
			ctx.moveTo(x + dx + r, y + dx);
			ctx.arc(x + dx, y + dx, r, 0, Math.PI * 2);
		}
	}
	ctx.fill();
};

export const draw = (inks: Inks, seed: number) => (ctx: CanvasRenderingContext2D, img: HTMLImageElement, w: number, h: number) => {
	const lum = stretch(luminance(ctx, img, w, h));
	// 1. the readable picture: a duotone from cream paper (lights) to the ink (shadows)
	const [paper, ink] = [rgb(inks.paper), rgb(inks.ink)];
	const base = ctx.createImageData(w, h);
	for (let i = 0; i < w * h; i++) {
		const l = Math.pow(lum[i], 0.85);
		for (let k = 0; k < 3; k++) base.data[i * 4 + k] = ink[k] + (paper[k] - ink[k]) * l;
		base.data[i * 4 + 3] = 255;
	}
	ctx.putImageData(base, 0, 0);
	for (let i = 0; i < 700; i++) { // paper mottling
		ctx.fillStyle = `rgba(120, 90, 50, ${0.02 + 0.03 * noise(seed, i)})`;
		ctx.fillRect(noise(seed + 1, i) * w, noise(seed + 2, i) * h, 2 + 30 * noise(seed + 3, i), 2 + 30 * noise(seed + 4, i));
	}
	// 2. print texture on top: a fine ink screen in the mid-tones and an off-register accent screen
	ctx.globalCompositeOperation = 'multiply';
	ctx.globalAlpha = 0.55;
	screen(ctx, lum, w, h, 75, inks.accent, (l) => Math.max(0, 1 - Math.abs(l - 0.55) * 2.2) * 0.6, 3);
	ctx.globalAlpha = 0.5;
	screen(ctx, lum, w, h, 15, inks.ink, (l) => Math.max(0, 1 - Math.abs(l - 0.45) * 2) * 0.7, 0);
	ctx.globalAlpha = 1;
	ctx.globalCompositeOperation = 'source-over';
};

export const Halftone: Look = ({src, inks, seed}) => {
	const url = useOnceCanvas(src, draw(inks, seed));
	return <Img src={url ?? src} style={FILL} />;
};
