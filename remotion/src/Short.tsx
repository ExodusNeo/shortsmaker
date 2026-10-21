import {AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {MarkCard, StatCard, TimelineCard} from './Cards';
import {Captions} from './Captions';
import {CompareCard, HeadlineCard, QuoteCard, StampCard} from './Extras';
import {Callout, HookTitle, PersonCard, SubscribeCta, theme} from './Graphics';
import {MapCard} from './MapCard';
import {FullScene} from './full/FullScene';
import type {AnyFull} from './full/types';
import {lookFor, overlayFor, transitionFor} from './style/index';
import {inksOf} from './style/kit';
import type {Inks} from './style/types';
import {transitionWindow} from './style/window';

export type Move = 'in' | 'out' | 'left' | 'right' | 'up' | 'down';
export type Graphic = {
	// question / kinetic / invented are style-library overlays (remotion/src/style)
	style: 'date' | 'place' | 'fact' | 'stat' | 'timeline' | 'mark' | 'headline' | 'quote' | 'compare' | 'stamp' | 'question' | 'kinetic' | 'invented';
	text: string;
	at: number; // when it appears
	trigger?: string; // the spoken word it appears on
	lat?: number | null;
	lon?: number | null;
	from?: {text: string; lat: number; lon: number}; // place: a route line starts here
	value?: number; // stat
	of?: number; // stat: dot grid of this many
	start?: string; // timeline ends
	end?: string;
	x?: number; // mark: detail position in the picture, 0..1
	y?: number;
	shape?: 'circle' | 'arrow';
	image?: string;
	aspect?: number;
	low?: boolean; // the picture's subject is at the top: sit just above the captions instead
	pace?: number; // map: 1 = full-speed fly-in, less = faster so the place name gets its hold in a short scene
	paper?: string; // headline: masthead (only a real paper that covered it)
	date?: string; // headline: dateline
	by?: string; // quote: who said it
	a_label?: string; // compare: the two bars
	a_value?: number;
	a_show?: string;
	b_label?: string;
	b_value?: number;
	b_show?: string;
};
export type Card = {image: string; name: string; on: number; off: number};
export type Scene = {
	image: string;
	start: number;
	end: number;
	move: Move;
	transition: string; // a style-library transition name: cut, fade, flash, wipe, ... (unknown = fade)
	look?: string | null; // a style-library photo look for this still picture (null = the plain picture)
	lookSeed?: number;
	graphic: Graphic | null;
	card: Card | null;
	clip: {src: string; duration: number} | null; // AI motion clip made on the user's GPU
	credit?: string | null; // CC BY material on screen: a small credit tag at the start of the scene
	full?: AnyFull | null; // full-screen motion graphic drawn instead of the picture
};
export type Word = {start: number; end: number; text: string; emphasis: boolean; line: number};
export type ShortProps = {
	fps: number;
	total: number;
	xfade: number;
	hook: string;
	scenes: Scene[];
	flashes: number[];
	words: Word[];
	cta: number | null; // when the silent subscribe button appears
	ctaLine: string;
	palette?: typeof theme; // this Short's colours (make_shorts.py PALETTES)
};

const ZMAX = 1.12;

// All timing is in absolute seconds (`t`), matching the edit plan make_shorts.py writes.
const Background: React.FC<{scene: Scene; next?: Scene; t: number; xfade: number; first: boolean; span: number; inks: Inks}> = ({
	scene, next, t, xfade, first, span, inks,
}) => {
	const p = Math.min(Math.max((t - scene.start + xfade / 2) / (scene.end - scene.start + xfade), 0), 1);
	const z = scene.move === 'in' ? 1 + (ZMAX - 1) * p : scene.move === 'out' ? ZMAX - (ZMAX - 1) * p : ZMAX;
	const max = ((z - 1) / (2 * z)) * 100; // % the image can slide before its edge shows
	const tx = scene.move === 'right' ? max * (1 - 2 * p) : scene.move === 'left' ? -max * (1 - 2 * p) : 0;
	const ty = scene.move === 'down' ? max * (1 - 2 * p) : scene.move === 'up' ? -max * (1 - 2 * p) : 0;
	// this scene's own transition styles it coming in; once the next scene's transition starts, that one styles it
	// going out (never both: the entry's resting transform would undo the exit's)
	const leaving = next ? transitionWindow(next).p(t) > 0 : false;
	const style = leaving && next
		? transitionFor(next.transition).render(transitionWindow(next).p(t), inks, next.lookSeed ?? 0).from
		: first ? undefined : transitionFor(scene.transition).render(transitionWindow(scene).p(t), inks, scene.lookSeed ?? 0).to;
	const Look = scene.full || scene.clip ? null : lookFor(scene.look);
	return (
		<AbsoluteFill style={style}>
			{scene.full ? (
				<FullScene full={scene.full} t={t} start={scene.start} end={scene.end} />
			) : scene.clip ? (
				// The clip is slowed (or sped up) so it plays exactly once across the whole scene.
				<OffthreadVideo
					src={staticFile(scene.clip.src)}
					muted
					playbackRate={scene.clip.duration / span}
					style={{width: '100%', height: '100%', objectFit: 'cover'}}
				/>
			) : Look ? (
				<AbsoluteFill style={{transform: `scale(${z}) translate(${tx}%, ${ty}%)`}}>
					<Look src={staticFile(scene.image)} t={t} start={scene.start} end={scene.end} inks={inks} seed={scene.lookSeed ?? 0} />
				</AbsoluteFill>
			) : (
				<Img
					src={staticFile(scene.image)}
					style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${z}) translate(${tx}%, ${ty}%)`}}
				/>
			)}
		</AbsoluteFill>
	);
};

/** Camera-flash curve: snaps white over the 2 frames before the cut, then decays (~0.4s). */
const flashAlpha = (t: number, cut: number) =>
	t >= cut - 0.07 && t < cut ? (0.9 * (t - (cut - 0.07))) / 0.07 : t >= cut && t < cut + 0.5 ? 0.9 * Math.exp(-(t - cut) / 0.11) : 0;

const GraphicFor: React.FC<{graphic: Graphic; t: number; start: number; end: number; variant: number}> = (p) => {
	const Overlay = overlayFor(p.graphic.style); // a style-library overlay (question, kinetic, an invention)
	return Overlay ? <Overlay {...p} /> : <BuiltInGraphic {...p} />;
};

const BuiltInGraphic: React.FC<{graphic: Graphic; t: number; start: number; end: number; variant: number}> = (p) =>
	p.graphic.style === 'place' && p.graphic.lat != null && p.graphic.lon != null ? <MapCard {...p} />
		: p.graphic.style === 'stat' ? <StatCard {...p} />
		: p.graphic.style === 'timeline' ? <TimelineCard {...p} />
		: p.graphic.style === 'mark' ? <MarkCard {...p} />
		: p.graphic.style === 'headline' ? <HeadlineCard {...p} />
		: p.graphic.style === 'quote' ? <QuoteCard {...p} />
		: p.graphic.style === 'compare' ? <CompareCard {...p} />
		: p.graphic.style === 'stamp' ? <StampCard {...p} />
		: <Callout {...p} />;

export const Short: React.FC<ShortProps> = ({total, xfade, hook, scenes, flashes, words, cta, ctaLine, palette}) => {
	if (palette) Object.assign(theme, palette); // before any child draws: every card reads `theme`
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const i = Math.max(0, scenes.findIndex((s) => t < s.end));
	const current = scenes[i];
	const g = current?.graphic;
	const variant = scenes.slice(0, i).filter((s) => s.graphic).length; // rotates entrance styles
	const inks = inksOf(theme);
	// a transition's cover (a dot wipe, a light leak) is drawn above both scenes while it runs
	const cut = scenes.find((s, k) => k > 0 && Math.abs(t - s.start) < transitionFor(s.transition).duration / 2);
	const cover = cut ? transitionFor(cut.transition).render(transitionWindow(cut).p(t), inks, cut.lookSeed ?? 0).cover : null;
	return (
		<AbsoluteFill style={{backgroundColor: '#121218'}}>
			{scenes.map((scene, k) => {
				const next = scenes[k + 1];
				const from = k === 0 ? 0 : Math.round((scene.start - transitionWindow(scene).lead) * fps);
				// stay on screen until the next scene's transition has finished (at least today's xfade/2)
				const until = next ? Math.round((scene.end + Math.max(xfade / 2, transitionWindow(next).lead)) * fps) : Math.ceil(total * fps);
				return (
					<Sequence key={scene.image + k} from={from} durationInFrames={Math.max(1, until - from)} premountFor={fps}>
						<Background scene={scene} next={next} t={t} xfade={xfade} first={k === 0} span={Math.max(1, until - from) / fps} inks={inks} />
					</Sequence>
				);
			})}
			{cover ? <AbsoluteFill>{cover}</AbsoluteFill> : null}
			{g ? <GraphicFor graphic={g} t={t} start={g.at} end={current.end} variant={variant} /> : null}
			{current?.card ? <PersonCard card={current.card} t={t} /> : null}
			{hook ? <HookTitle text={hook} t={t} /> : null}
			<Captions words={words} t={t} />
			{current?.credit && t < current.start + 3.1 && (cta == null || t < cta) ? (
				// shown for the first ~2.8 s of the scene, then it fades out of the picture's way
				<div
					style={{
						position: 'absolute', top: 1500, left: 36, background: 'rgba(0,0,0,0.5)', borderRadius: 8,
						padding: '4px 10px', fontFamily: 'Arial, sans-serif', fontWeight: 700, fontSize: 22, color: 'rgba(255,255,255,0.9)',
						opacity: interpolate(t, [current.start + 2.8, current.start + 3.1], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
					}}
				>
					{current.credit}
				</div>
			) : null}
			{cta != null ? <SubscribeCta line={ctaLine} t={t} start={cta} end={total} /> : null}
			<AbsoluteFill style={{backgroundColor: 'white', opacity: Math.max(0, ...flashes.map((c) => flashAlpha(t, c)))}} />
		</AbsoluteFill>
	);
};
