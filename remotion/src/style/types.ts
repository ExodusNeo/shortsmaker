// The three kinds of style component. Presets and AI inventions share these interfaces, so they are interchangeable.
import type React from 'react';
import type {Graphic} from '../Short';

/** Print inks for this Short, from its palette (kit.inksOf). */
export type Inks = {paper: string; ink: string; accent: string; alarm: string};

/** A photo look: draws the scene's still picture in a style (under the scene's zoom/pan). */
export type LookProps = {src: string; t: number; start: number; end: number; inks: Inks; seed: number};
export type Look = React.FC<LookProps>;

/** An overlay: drawn in a scene's graphic slot, like the built-in cards. */
export type OverlayProps = {graphic: Graphic; t: number; start: number; end: number; variant: number};
export type Overlay = React.FC<OverlayProps>;

/** A scene change. `p` runs 0..1 across `duration` seconds, centred on the cut: `from` styles the outgoing scene,
 *  `to` the incoming one, `cover` is drawn above both. */
export type TransitionFrame = {from?: React.CSSProperties; to?: React.CSSProperties; cover?: React.ReactNode};
export type Transition = {duration: number; render: (p: number, inks: Inks, seed: number) => TransitionFrame};
