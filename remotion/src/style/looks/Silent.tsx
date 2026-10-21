// 1920s silent film (idea: Lemo-OPUSCAR "1920s Silent Film"): sepia monochrome with a vignette (drawn once), then
// per-frame flicker, grain, a scratch now and then and a little gate weave.
import React from 'react';
import {AbsoluteFill} from 'remotion';
import {FILL, Img, drawCover, noise, useOnceCanvas} from '../kit';
import type {Look} from '../types';

export const draw = (ctx: CanvasRenderingContext2D, img: HTMLImageElement, w: number, h: number) => {
	ctx.filter = 'grayscale(1) sepia(0.35) contrast(1.12) brightness(0.98)';
	drawCover(ctx, img, w, h);
	ctx.filter = 'none';
	const v = ctx.createRadialGradient(w / 2, h / 2, h * 0.25, w / 2, h / 2, h * 0.62);
	v.addColorStop(0, 'rgba(0,0,0,0)');
	v.addColorStop(1, 'rgba(20,12,4,0.75)');
	ctx.fillStyle = v;
	ctx.fillRect(0, 0, w, h);
};

export const Silent: Look = ({src, t, seed}) => {
	const url = useOnceCanvas(src, draw);
	const frame = Math.floor(t * 24); // the film runs at 24 fps: its life changes on its own frames
	const flicker = 0.9 + 0.1 * noise(seed, frame);
	const weave = (noise(seed + 7, frame) - 0.5) * 3;
	const beat = Math.floor(frame / 6);
	const scratch = noise(seed + 3, beat) > 0.55 ? noise(seed + 4, beat) * 1080 : null;
	return (
		<AbsoluteFill style={{transform: `translateY(${weave}px)`}}>
			<Img src={url ?? src} style={FILL} />
			<AbsoluteFill style={{backgroundColor: '#000', opacity: 1 - flicker}} />
			<svg width="100%" height="100%" style={{position: 'absolute', inset: 0, opacity: 0.14, mixBlendMode: 'overlay'}}>
				<filter id={`grain-${seed}`}>
					<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={Math.floor(frame / 2) % 1000} />
				</filter>
				<rect width="100%" height="100%" filter={`url(#grain-${seed})`} />
			</svg>
			{scratch !== null ? (
				<div style={{position: 'absolute', top: 0, bottom: 0, left: scratch, width: 2, background: 'rgba(255,248,230,0.55)'}} />
			) : null}
		</AbsoluteFill>
	);
};
