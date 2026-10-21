import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Img, cancelRender, continueRender, delayRender, staticFile} from 'remotion';
import type {SkinName} from './types';

// Default archival constants (parchment skin); scenes can also call skinOf(full.skin) to adapt to any mood.
export const INK = '#2c1f0e';
export const RED = '#7a1d12';
export const SERIF = '"EB Garamond", Georgia, serif';
export const TYPE = '"Special Elite", "Courier New", monospace';

export type Skin = {
	name: SkinName;
	bg: string;
	ink: string;
	accent: string;
	card: string;
	cardInk: string;
	sub: string;
	halo: string;
	landFill: string;
	coast: string;
	vignette: string;
	dark: boolean;
};

export const SKINS: Record<SkinName, Skin> = {
	parchment: {
		name: 'parchment',
		bg: '#e2d2b0',
		ink: '#2c1f0e',
		accent: '#7a1d12',
		card: '#f1e6cc',
		cardInk: '#2c1f0e',
		sub: 'rgba(44,31,14,0.28)',
		halo: '#efe3c8',
		landFill: 'rgba(150,120,70,0.22)',
		coast: '#8a7449',
		vignette: 'rgba(59,42,20,0.55)',
		dark: false,
	},
	blueprint: {
		name: 'blueprint',
		bg: '#0b192c',
		ink: '#e8f4fd',
		accent: '#ff9f43',
		card: '#132a46',
		cardInk: '#e8f4fd',
		sub: 'rgba(232,244,253,0.22)',
		halo: '#0b192c',
		landFill: 'rgba(79,195,255,0.18)',
		coast: '#3b7ea1',
		vignette: 'rgba(4,10,20,0.68)',
		dark: true,
	},
	dossier: {
		name: 'dossier',
		bg: '#181214',
		ink: '#f2e9dc',
		accent: '#e63946',
		card: '#281d20',
		cardInk: '#f2e9dc',
		sub: 'rgba(242,233,220,0.22)',
		halo: '#181214',
		landFill: 'rgba(230,57,70,0.16)',
		coast: '#8c353d',
		vignette: 'rgba(8,4,6,0.72)',
		dark: true,
	},
	hud: {
		name: 'hud',
		bg: '#0c1018',
		ink: '#f0f6fc',
		accent: '#2ee6c5',
		card: '#172132',
		cardInk: '#f0f6fc',
		sub: 'rgba(240,246,252,0.22)',
		halo: '#0c1018',
		landFill: 'rgba(46,230,197,0.16)',
		coast: '#257a6b',
		vignette: 'rgba(4,6,12,0.72)',
		dark: true,
	},
};

export const skinOf = (skin?: SkinName): Skin => SKINS[skin ?? 'parchment'] ?? SKINS.parchment;

const FONTS: [string, string, string][] = [
	['EB Garamond', 'fonts/EBGaramond.ttf', 'normal'],
	['EB Garamond', 'fonts/EBGaramond-Italic.ttf', 'italic'],
	['Special Elite', 'fonts/SpecialElite-Regular.ttf', 'normal'],
];
let fontsReady: Promise<void> | null = null;

/** Loads the bundled fonts (no network) before the first frame that uses them is captured. */
export const useFonts = () => {
	const [handle] = useState(() => delayRender('archival fonts'));
	useEffect(() => {
		fontsReady ??= Promise.all(
			FONTS.map(([family, file, style]) =>
				new FontFace(family, `url(${staticFile(file)})`, {style, weight: '400 800'}).load().then((f) => {
					document.fonts.add(f);
				}),
			),
		).then(() => undefined);
		fontsReady.then(() => continueRender(handle)).catch((e) => cancelRender(e));
	}, [handle]);
};

/** Deterministic 0..1 random numbers per scene (layouts, camera paths) so a re-render looks the same. */
export const rng = (seed: number) => {
	let s = (seed * 9301 + 49297) % 233280 || 1;
	return () => {
		s = (s * 9301 + 49297) % 233280;
		return s / 233280;
	};
};

export type Cam = {x: number; y: number; scale: number};

export const CamContext = React.createContext<Cam>({x: 540, y: 960, scale: 1});

/** The table/backdrop the scene lies on. Children are laid out in "world" pixels (the screen is 1080x1920 at
 * scale 1); `cam` says which world point sits at the screen centre and how close the camera is. A slow
 * drift keeps even a still moment alive. Grain and vignette stay fixed to the lens. */
export const Paper: React.FC<{
	t: number;
	start: number;
	seed: number;
	cam: Cam;
	dark?: boolean;
	skin?: SkinName;
	children?: React.ReactNode;
}> = ({t, start, seed, cam, dark, skin, children}) => {
	useFonts();
	const sk = skinOf(skin);
	const r = rng(seed);
	const dir = r() * Math.PI * 2;
	const drift = (t - start) * 6; // px per second, world space
	const x = cam.x + Math.cos(dir) * drift;
	const y = cam.y + Math.sin(dir) * drift;
	const grain = Math.floor(t * 12) % 6;
	const isDark = dark || sk.dark;
	return (
		<AbsoluteFill style={{backgroundColor: dark && sk.name === 'parchment' ? '#2b2017' : sk.bg, overflow: 'hidden'}}>
			<div
				style={{
					position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, transformOrigin: '0 0',
					transform: `translate(540px, 960px) scale(${cam.scale}) translate(${-x}px, ${-y}px)`,
				}}
			>
				{!isDark ? (
					<Img src={staticFile('paper/paper.jpg')} style={{position: 'absolute', left: -1200, top: -2000, width: 3480, height: 5920}} />
				) : sk.name === 'blueprint' ? (
					<div
						style={{
							position: 'absolute', left: -1200, top: -2000, width: 3480, height: 5920,
							backgroundImage:
								'linear-gradient(rgba(120,195,255,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(120,195,255,0.08) 1px, transparent 1px), linear-gradient(rgba(120,195,255,0.18) 2px, transparent 2px), linear-gradient(90deg, rgba(120,195,255,0.18) 2px, transparent 2px)',
							backgroundSize: '45px 45px, 45px 45px, 225px 225px, 225px 225px',
						}}
					/>
				) : sk.name === 'hud' ? (
					<div
						style={{
							position: 'absolute', left: -1200, top: -2000, width: 3480, height: 5920,
							backgroundImage:
								'radial-gradient(rgba(46,230,197,0.16) 2px, transparent 2px), linear-gradient(rgba(255,255,255,0.03) 2px, transparent 2px)',
							backgroundSize: '54px 54px, 100% 8px',
						}}
					/>
				) : sk.name === 'dossier' ? (
					<Img
						src={staticFile('paper/paper.jpg')}
						style={{position: 'absolute', left: -1200, top: -2000, width: 3480, height: 5920, filter: 'brightness(0.18) sepia(0.6) hue-rotate(-35deg) saturate(1.6)'}}
					/>
				) : null}
				<CamContext.Provider value={{x, y, scale: cam.scale}}>
					{children}
				</CamContext.Provider>
			</div>
			<Img
				src={staticFile(`paper/grain${grain}.png`)}
				style={{position: 'absolute', inset: 0, width: '100%', height: '100%', mixBlendMode: isDark ? 'screen' : 'multiply', opacity: isDark ? 0.35 : 1}}
			/>
			<AbsoluteFill style={{background: `radial-gradient(ellipse 75% 60% at 50% 48%, rgba(0,0,0,0) 52%, ${sk.vignette} 100%)`}} />
		</AbsoluteFill>
	);
};
