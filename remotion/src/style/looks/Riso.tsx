// Risograph (idea: Lemo-OPUSCAR "Risograph Print"): two flat spot inks by tone, grainy, the second ink slightly off
// register, on paper.
import React from 'react';
import {FILL, Img, luminance, noise, useOnceCanvas} from '../kit';
import type {Inks, Look} from '../types';

const OFFSET = 4;
const rgb = (hex: string) => {
	const v = parseInt(hex.replace('#', '').slice(0, 6), 16);
	return [(v >> 16) & 255, (v >> 8) & 255, v & 255].map((c) => c / 255);
};

export const draw = (inks: Inks, seed: number) => (ctx: CanvasRenderingContext2D, img: HTMLImageElement, w: number, h: number) => {
	const lum = luminance(ctx, img, w, h);
	const [paper, ink, accent] = [rgb(inks.paper), rgb(inks.ink), rgb(inks.accent)];
	const out = ctx.createImageData(w, h);
	const d = out.data;
	for (let y = 0; y < h; y++) {
		for (let x = 0; x < w; x++) {
			const i = y * w + x;
			const grain = noise(seed, i * 0.618) * 0.35; // ink skips a little, like a real riso drum
			const la = lum[Math.min(h - 1, y + OFFSET) * w + Math.min(w - 1, x + OFFSET)]; // accent drum, off register
			const accentCover = la < 0.72 ? Math.min(1, (0.72 - la) / 0.3) * (1 - grain) : 0;
			const inkCover = lum[i] < 0.4 ? Math.min(1, (0.4 - lum[i]) / 0.18) * (1 - grain) : 0;
			for (let k = 0; k < 3; k++) {
				const c = paper[k] * (1 - accentCover + accentCover * accent[k]) * (1 - inkCover + inkCover * ink[k]); // multiply
				d[i * 4 + k] = Math.round(c * 255);
			}
			d[i * 4 + 3] = 255;
		}
	}
	ctx.putImageData(out, 0, 0);
};

export const Riso: Look = ({src, inks, seed}) => {
	const url = useOnceCanvas(src, draw(inks, seed));
	return <Img src={url ?? src} style={FILL} />;
};
