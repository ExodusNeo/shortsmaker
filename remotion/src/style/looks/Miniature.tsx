// Tilt-shift miniature (idea: Showtime's tilt-shift look): blurred bands top and bottom and richer colour make a wide
// shot of a town or crowd look like a toy model.
import React from 'react';
import {FILL, Img, drawCover, useOnceCanvas} from '../kit';
import type {Look} from '../types';

const COLOUR = 'saturate(1.35) contrast(1.15)';

export const draw = (ctx: CanvasRenderingContext2D, img: HTMLImageElement, w: number, h: number) => {
	ctx.filter = `blur(14px) ${COLOUR}`;
	drawCover(ctx, img, w, h);
	ctx.filter = 'none';
	const sharp = document.createElement('canvas');
	sharp.width = w;
	sharp.height = h;
	const s = sharp.getContext('2d');
	if (!s) return;
	s.filter = COLOUR;
	drawCover(s, img, w, h);
	s.filter = 'none';
	const band = s.createLinearGradient(0, 0, 0, h); // the sharp band in the middle, fading out above and below
	band.addColorStop(0.28, 'rgba(0,0,0,0)');
	band.addColorStop(0.42, 'rgba(0,0,0,1)');
	band.addColorStop(0.6, 'rgba(0,0,0,1)');
	band.addColorStop(0.74, 'rgba(0,0,0,0)');
	s.globalCompositeOperation = 'destination-in';
	s.fillStyle = band;
	s.fillRect(0, 0, w, h);
	ctx.drawImage(sharp, 0, 0);
};

export const Miniature: Look = ({src}) => {
	const url = useOnceCanvas(src, draw);
	return <Img src={url ?? src} style={FILL} />;
};
