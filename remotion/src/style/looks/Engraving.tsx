// Copperplate engraving (idea: Lemo-OPUSCAR "Copperplate Engraving"): the photo drawn as fine parallel ink lines whose
// thickness follows the shading, cross-hatched in the shadows, sepia ink on cream paper.
import React from 'react';
import {FILL, Img, luminance, useOnceCanvas} from '../kit';
import type {Inks, Look} from '../types';

const SPACING = 7;
const MAX_W = 6;
const INK = '#3B2A1A';

const hatch = (ctx: CanvasRenderingContext2D, lum: Float32Array, w: number, h: number, deg: number, thick: (l: number) => number) => {
	const a = (deg * Math.PI) / 180;
	const [c, s] = [Math.cos(a), Math.sin(a)];
	const reach = Math.hypot(w, h) / 2;
	const at = (x: number, y: number) => (x < 0 || y < 0 || x >= w || y >= h ? 1 : lum[Math.floor(y) * w + Math.floor(x)]);
	ctx.fillStyle = INK;
	for (let v = -reach; v < reach; v += SPACING) {
		const top: number[] = [];
		const bottom: number[] = [];
		for (let u = -reach; u <= reach; u += 3) {
			const x = w / 2 + u * c - v * s;
			const y = h / 2 + u * s + v * c;
			const half = thick(at(x, y)) / 2;
			top.push(x - s * half, y + c * half);
			bottom.push(x + s * half, y - c * half);
		}
		ctx.beginPath();
		ctx.moveTo(top[0], top[1]);
		for (let i = 2; i < top.length; i += 2) ctx.lineTo(top[i], top[i + 1]);
		for (let i = bottom.length - 2; i >= 0; i -= 2) ctx.lineTo(bottom[i], bottom[i + 1]);
		ctx.closePath();
		ctx.fill();
	}
};

export const draw = (inks: Inks) => (ctx: CanvasRenderingContext2D, img: HTMLImageElement, w: number, h: number) => {
	const lum = luminance(ctx, img, w, h);
	ctx.fillStyle = inks.paper;
	ctx.fillRect(0, 0, w, h);
	hatch(ctx, lum, w, h, 30, (l) => MAX_W * Math.pow(1 - l, 1.1));
	hatch(ctx, lum, w, h, -30, (l) => (l < 0.35 ? MAX_W * 0.8 * ((0.35 - l) / 0.35) : 0)); // cross-hatch the shadows
};

export const Engraving: Look = ({src, inks}) => {
	const url = useOnceCanvas(src, draw(inks));
	return <Img src={url ?? src} style={FILL} />;
};
