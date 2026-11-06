// Opener3D: the 3D opener (owner, 2026-11-05: openers as clean as the "Second Draw" Short, which puts flat cartoon
// characters inside a lit 3D set). A fixed three.js set (room / street / outdoors) furnished from a fixed prop
// library, with the drawn kit's cut-outs standing in it (drawn/cutouts.mjs paints them), one light mood, real
// shadows, fog for depth, effects and camera shots aimed at named things. The AI only writes the stage description
// (drawn/STAGE3D.md); shortsmaker/opener3d.py resolves word times and renders it. Lesson from the removed Blender
// openers: fixed sets and parts, the AI places and frames them.
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import {useEffect, useMemo, useState} from 'react';
import {AbsoluteFill, CalculateMetadataFunction, continueRender, delayRender, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import * as THREE from 'three';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {Bloom, DepthOfField, EffectComposer} from '@react-three/postprocessing';

type XZ = [number, number];
export type Cutout = {name: string; frames: number; height: number; aspect: number; at: XZ; y?: number; wall?: boolean;
	flip?: boolean; talk?: [number, number]; fps?: number; path?: [number, number, number][]; hits?: number[]; focus?: number;
	contact?: [number, number]; // a knocker: where his fist meets the door (x from the board's centre, height), in metres
	wide?: number; tall?: number; steps?: number; // the board cropped round the drawing / the painter's canvas; drawings per cycle (cutouts.mjs)
	held?: Held; // a 3D object in one hand (owner, 2026-11-06: people stay drawn, every object is 3D)
	hands?: [number, number][][]}; // per drawing, both hands on the board (0..1 across from the left, 0..1 up from the feet)
/** A 3D object a cut-out holds: a library model (`type`) or an AI-made part (`shapes`), `height` metres tall. */
export type Held = {type: string; shapes?: Shape[]; height: number; hand?: number};
/** One primitive of an AI-made 3D part (opener_crew.make_part3d): metres, origin on the floor at the part's centre. */
export type Shape = {shape: 'box' | 'cylinder' | 'sphere' | 'cone' | 'torus'; size: [number, number, number];
	at: [number, number, number]; turn?: [number, number, number]; color: string; metal?: boolean; glow?: boolean};
export type Prop = {type: string; id?: string; at: XZ; y?: number; wall?: boolean; turn?: number; size?: number; color?: string;
	lit?: boolean; open?: number; length?: number; shapes?: Shape[]; h?: number}; // h: an object's height (shots aim at its middle) // shapes: type 'made', an AI-made 3D part
export type Shot = {at: number; target: string | string[]; distance: number; height?: number; turn?: number; fov?: number; move?: 'cut' | 'whip' | 'push';
	over?: string; size?: 'wide' | 'medium' | 'close' | 'low' | 'top' | 'over'};
export type Effect = {type: 'rings' | 'dust' | 'shafts' | 'burst' | 'shake' | 'rain' | 'snow' | 'jolt' | 'puff' | 'sparks' | 'smoke' | 'glow' | 'aurora';
	at?: number; on?: string; color?: string};
export type StageProps = {fps: number; seconds: number; dir: string; place: 'room' | 'street' | 'outdoors';
	mood: 'day' | 'golden' | 'dusk' | 'night' | 'interior'; colors?: {wall?: string; floor?: string; ground?: string; sky?: string; trim?: string};
	props: Prop[]; cutouts: Cutout[]; shots: Shot[]; effects: Effect[]};

export const calculateOpener3D: CalculateMetadataFunction<StageProps> = ({props}) => ({
	fps: props.fps, durationInFrames: Math.max(1, Math.ceil(props.seconds * props.fps)),
});

const MOODS = {
	// rim = a cool light from behind that separates things from the warm key light; card = the unlit cut-outs' tint
	// (they stay bright and clean, never muddy; interior was one orange-brown wash on the McLean test, 2026-11-05)
	day: {sky: '#BFD8FF', ground: '#6A5A40', hemi: 1.6, sun: '#FFF1D6', sunI: 2.6, sunPos: [-6, 9, 4], fill: 0.6, fog: '#C9DCEA', bg: '#9CC8F0', glow: 'rgba(255,240,200,0.10)', rim: '#CFE0FF', rimI: 0.8, card: '#FFFFFF'},
	golden: {sky: '#FFD9A8', ground: '#5A3A28', hemi: 1.3, sun: '#FFB46A', sunI: 2.8, sunPos: [-8, 3.5, 2], fill: 0.5, fog: '#E8B88A', bg: '#F2B577', glow: 'rgba(255,190,110,0.16)', rim: '#8FB4FF', rimI: 1.0, card: '#FFF1E0'},
	dusk: {sky: '#C88AA0', ground: '#3A2440', hemi: 1.0, sun: '#FF8A5A', sunI: 2.0, sunPos: [-8, 2, -4], fill: 0.4, fog: '#7A5A78', bg: '#E07A5A', glow: 'rgba(255,140,90,0.14)', rim: '#7A9CFF', rimI: 1.0, card: '#F2DCD8'},
	night: {sky: '#5A6A9A', ground: '#141020', hemi: 0.6, sun: '#9EB6FF', sunI: 0.9, sunPos: [-5, 8, 2], fill: 0.25, fog: '#1A2040', bg: '#0E1430', glow: 'rgba(140,170,255,0.08)', rim: '#9EB6FF', rimI: 1.2, card: '#B8C2E0'},
	interior: {sky: '#B4C6E8', ground: '#4A2C18', hemi: 1.5, sun: '#FFD49A', sunI: 2.6, sunPos: [-6, 4.6, -0.6], fill: 0.85, fog: '#2A2430', bg: '#120c08', glow: 'rgba(255,200,130,0.10)', rim: '#8FB0FF', rimI: 1.4, card: '#FFF4E6'},
} as const;

const BACK = -3.92; // the room's back wall (things with wall: true hang on it)
const ease = (u: number) => (u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2);
const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const rand = (i: number) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

/** Where a cut-out stands at time t (its path, if any, overrides `at`). */
function cutPos(c: Cutout, t: number): THREE.Vector3 {
	let [x, z] = c.at;
	const path = c.path || [];
	if (path.length) {
		const k = path.findIndex((p) => p[0] > t);
		if (k === -1) [, x, z] = path[path.length - 1];
		else if (k === 0) [, x, z] = path[0];
		else { const [t0, x0, z0] = path[k - 1], [t1, x1, z1] = path[k], u = (t - t0) / Math.max(1e-3, t1 - t0); x = x0 + (x1 - x0) * u; z = z0 + (z1 - z0) * u; }
	}
	if (c.wall) return new THREE.Vector3(c.at[0], c.at[1], BACK + 0.05);
	return new THREE.Vector3(x, c.y || 0, z);
}

/** The point a shot aims at: a cut-out's upper body / centre, or a prop's centre. */
function targetOf(s: StageProps, name: string, t: number, size?: Shot['size']): THREE.Vector3 {
	const c = s.cutouts.find((q) => q.name === name);
	// how high on the board a shot aims: a close-up at the face (a person's head sits ~0.8 up its board; a knocker's
	// board is taller, for its door, so his face is ~0.6), a medium at the chest, the rest at the upper body
	const up = c?.focus != null ? (size === 'close' ? 0.6 : size === 'medium' ? 0.55 : 0.5) : (size === 'close' ? 0.8 : size === 'medium' ? 0.68 : 0.62);
	if (c) { const p = cutPos(c, t); return c.wall ? p : p.add(new THREE.Vector3(c.focus || 0, c.height * up, 0)); } // focus: an off-centre subject (k.knock)
	const p = s.props.find((q) => q.id === name);
	if (p) return p.wall ? new THREE.Vector3(p.at[0], p.at[1], BACK) : new THREE.Vector3(p.at[0], (p.y || 0) + (p.h != null ? p.h / 2 : 0.8 * (p.size || 1)), p.at[1]);
	return new THREE.Vector3(0, 1.4, -2);
}

/** Where a shot aims, and how far back it must stand to fit everything it names (a list = the middle of them all,
 * wide enough to keep each one inside the frame: a live McLean draft cut the grocer off at the edge). */
function aim(s: StageProps, target: string | string[], fov: number, t: number, size?: Shot['size']) {
	const names = Array.isArray(target) ? target : [target];
	const pts = names.map((n) => targetOf(s, n, t, names.length > 1 ? undefined : size));
	// a list of people and props aims mostly at the people: "the operator and his desk" stood so far back to fit the
	// desk across a 9:16 frame that he was tiny (2026-11-06); props only pull the aim a little toward them
	const people = names.map((n) => s.cutouts.some((q) => q.name === n && !q.wall));
	const wt = (i: number) => (people.some(Boolean) && !people[i] ? 0.3 : 1);
	const tg = pts.reduce((a, b, i) => a.add(b.clone().multiplyScalar(wt(i))), new THREE.Vector3()).divideScalar(pts.reduce((m, _, i) => m + wt(i), 0));
	const hfov = 2 * Math.atan(Math.tan((fov * Math.PI) / 360) * (9 / 16)); // the portrait frame's horizontal view
	if (pts.length < 2) { // one cut-out: stand back far enough that it is never cut off at the side (2026-11-06)
		const c = s.cutouts.find((q) => q.name === names[0]);
		if (!c || c.wall) return {tg, fit: 0};
		const half = size === 'close' ? Math.min(0.75, 0.5 * c.height * c.aspect) : 0.42 * c.height * c.aspect + 0.12; // a close-up keeps the face and what the hands hold
		const tall = size === 'wide' || size === 'low' || size === 'top' ? (0.62 * c.height + 0.2) / Math.tan((fov * Math.PI) / 360) : 0; // the feet too
		return {tg, fit: Math.max(half / Math.tan(hfov / 2), tall)};
	}
	// people must fit whole; a big prop in the list (a 2.3 m desk) may run off the edge: it is where, not who
	const half = Math.max(...names.map((n, i) => { const c = s.cutouts.find((q) => q.name === n);
		return c ? Math.abs(pts[i].x - tg.x) + 0.42 * c.height * c.aspect + 0.1 : people.some(Boolean) ? 0 : Math.abs(pts[i].x - tg.x) + 0.25; }));
	return {tg, fit: half / Math.tan(hfov / 2)};
}

function framing(s: StageProps, t: number) {
	const shots = s.shots.length ? s.shots : [{at: 0, target: '', distance: 5}];
	const one = (sh: Shot, at: number) => {
		const fov = clamp(sh.fov || 50, 28, 72), {tg, fit} = aim(s, sh.target, fov, at, sh.size), held = Math.max(0, at - sh.at);
		const d = Math.max(sh.distance, fit) * (1 - 0.035 * held); // every shot drifts in...
		const a = ((sh.turn || 0) * Math.PI) / 180 + 0.035 * held * ((sh.turn || 0) < 0 ? -1 : 1); // ...and orbits a little
		let pos = new THREE.Vector3(tg.x + Math.sin(a) * d, tg.y + (sh.height || 0), tg.z + Math.cos(a) * d);
		if (sh.over) { // over the shoulder: the camera stands just behind `over`, which fills the near side of the frame
			const o = targetOf(s, sh.over, at), back = o.clone().sub(tg).setY(0).normalize();
			const side = new THREE.Vector3(-back.z, 0, back.x).multiplyScalar((sh.turn || 0) < 0 ? -0.22 : 0.22);
			pos = o.clone().add(back.multiplyScalar(1.15 - 0.03 * held)).add(side).add(new THREE.Vector3(0, 0.1 + (sh.height || 0), 0));
			if (s.place === 'room') { pos.x = clamp(pos.x, -3.7, 3.7); pos.z = Math.min(pos.z, 4.4); pos.y = clamp(pos.y, 0.3, 4.1); }
			return {pos, look: tg.clone().lerp(o, 0.1), fov};
		}
		if (s.place === 'room') { pos.x = clamp(pos.x, -3.7, 3.7); pos.z = Math.min(pos.z, 4.4); pos.y = clamp(pos.y, 0.3, 4.1); } else pos.y = Math.max(0.3, pos.y);
		return {pos, look: tg, fov};
	};
	let i = 0;
	while (i + 1 < shots.length && t >= shots[i + 1].at) i++;
	const sh = shots[i], to = one(sh, t);
	if (!i || (sh.move || 'cut') === 'cut') return to;
	const dur = sh.move === 'push' ? Math.max(0.3, (shots[i + 1]?.at ?? s.seconds) - sh.at) : 0.32;
	const from = one(shots[i - 1], sh.at), u = ease(clamp((t - sh.at) / dur, 0, 1));
	return {pos: from.pos.lerp(to.pos, u), look: from.look.lerp(to.look, u), fov: from.fov + (to.fov - from.fov) * u};
}

const CameraRig: React.FC<{s: StageProps; t: number}> = ({s, t}) => {
	const {camera} = useThree();
	const f = framing(s, t);
	const shake = s.effects.filter((e) => e.type === 'shake' && e.at != null && t >= e.at && t < e.at + 0.45)
		.reduce((m, e) => Math.max(m, 1 - (t - (e.at as number)) / 0.45), 0);
	camera.position.copy(f.pos).add(new THREE.Vector3(Math.sin(t * 61) * 0.04 * shake, Math.sin(t * 47) * 0.04 * shake, 0));
	camera.lookAt(f.look);
	const cam = camera as THREE.PerspectiveCamera;
	cam.fov = f.fov; // vertical: a portrait frame needs a wide one for a set to read
	cam.updateProjectionMatrix();
	return null;
};

// The model library (Kenney, CC0; remotion/public/opener3d/models). Each one is scaled so its `fit` side matches the
// prop's size in STAGE3D.md (x = width, y = height, z = depth), centred on its spot with its base on the floor, and
// turned by `face` degrees so it fronts +z like every prop. Props not listed keep their box-built shape.
const MODELS: Record<string, {file: string; fit: ['x' | 'y' | 'z', number]; face?: number}> = {
	desk: {file: 'furniture/desk', fit: ['y', 0.86]}, table: {file: 'furniture/tableCloth', fit: ['y', 0.8]},
	chair: {file: 'furniture/chair', fit: ['y', 1.0]},
	cabinet: {file: 'furniture/bookcaseClosedDoors', fit: ['y', 1.8]}, bed: {file: 'furniture/bedDouble', fit: ['z', 2.0]},
	lamp: {file: 'furniture/lampRoundTable', fit: ['y', 0.5]}, tree: {file: 'nature/tree_oak', fit: ['y', 4.6]},
	rock: {file: 'nature/rock_largeA', fit: ['x', 1.1]}, lamppost: {file: 'town/lantern', fit: ['y', 3.3]},
	// set dressing and market/town pieces (2026-11-06: reviews called the sets plain); sizes = opener3d.FOOT
	stall: {file: 'town/stall', fit: ['x', 2.4]}, cart: {file: 'town/cart', fit: ['x', 2.0]}, fountain: {file: 'town/fountain-round', fit: ['x', 2.6]},
	hedge: {file: 'nature/plant_bushLarge', fit: ['x', 2.0]}, bookcase: {file: 'furniture/bookcaseOpen', fit: ['y', 2.0]},
	coatrack: {file: 'furniture/coatRackStanding', fit: ['y', 1.8]}, walllamp: {file: 'furniture/lampWall', fit: ['y', 0.3]},
	sidetable: {file: 'furniture/sideTable', fit: ['y', 0.6]},
	// objects (owner, 2026-11-06: "for objects make it 3d"); sizes = opener3d.FOOT
	books: {file: 'furniture/books', fit: ['y', 0.22]}, radio: {file: 'furniture/radio', fit: ['y', 0.32]},
	box: {file: 'furniture/cardboardBoxClosed', fit: ['x', 0.5]}, plant: {file: 'furniture/pottedPlant', fit: ['y', 0.8]},
	bench: {file: 'furniture/bench', fit: ['x', 1.6]}, roundtable: {file: 'furniture/tableRound', fit: ['y', 0.75]},
	stool: {file: 'town/stall-stool', fit: ['y', 0.5]}, wheel: {file: 'town/wheel', fit: ['y', 1.0]},
	pumpkin: {file: 'nature/crop_pumpkin', fit: ['x', 0.45]}, turnip: {file: 'nature/crop_turnip', fit: ['y', 0.3]},
	carrot: {file: 'nature/crop_carrot', fit: ['y', 0.3]}, logs: {file: 'nature/log_stack', fit: ['x', 1.2]},
	campfire: {file: 'nature/campfire_logs', fit: ['x', 0.9]}, pot: {file: 'nature/pot_large', fit: ['y', 0.6]},
	canoe: {file: 'nature/canoe', fit: ['x', 3.0]}, tent: {file: 'nature/tent_detailedOpen', fit: ['x', 2.4]},
	statue: {file: 'nature/statue_head', fit: ['y', 1.2]}, stump: {file: 'nature/stump_round', fit: ['y', 0.5]},
};
const TOWN = ['wall-wood', 'wall-wood-door', 'wall-wood-window-shutters', 'wall-wood-window-glass', 'wall', 'wall-door',
	'wall-window-shutters', 'wall-window-glass', 'roof-gable', 'overhang', 'wall-wood-detail-cross', 'wall-wood-detail-diagonal',
	'wall-detail-cross', 'wall-detail-diagonal'].map((n) => `town/${n}`);
type Library = Record<string, THREE.Object3D>;

// patches built from several small CC0 nature-kit models (2026-11-06: a farm story had no garden for its pig to raid)
const PATCHES: Record<string, {files: string[]; cols: number; rows: number; cell: number}> = {
	garden: {files: ['nature/crops_dirtDoubleRow', 'nature/crops_leafsStageB'], cols: 3, rows: 3, cell: 1.0}, // = opener3d.FOOT
	field: {files: ['nature/crops_wheatStageB'], cols: 5, rows: 4, cell: 0.8},
};
const Patch: React.FC<{lib: Library; kind: string}> = ({lib, kind}) => {
	const pt = PATCHES[kind], [ground, plant] = pt.files;
	if (!lib[ground]) return null;
	const cells = Array.from({length: pt.cols * pt.rows}, (_, k) => [(k % pt.cols - (pt.cols - 1) / 2) * pt.cell, (Math.floor(k / pt.cols) - (pt.rows - 1) / 2) * pt.cell]);
	return <>{cells.map(([x, z], k) => <group key={k} position={[x, 0, z]}>
		<Model src={lib[ground]} fit={['x', pt.cell]} />
		{/* planted in the 5 cm dirt row (crops_dirtDoubleRow is 0.05 tall): at 0.12 every plant floated (owner, 2026-11-07) */}
		{plant && lib[plant] ? <group position={[0, 0.03, 0]}><Model src={lib[plant]} fit={['y', 0.38]} /></group> : null}
	</group>)}</>;
};

function useModels(s: StageProps): Library | null {
	const files = useMemo(() => [...new Set([...[...s.props.map((p) => p.type), ...s.cutouts.map((c) => c.held?.type || '')].map((k) => MODELS[k]?.file).filter(Boolean) as string[],
		...s.props.flatMap((p) => PATCHES[p.type]?.files || []),
		...(s.place === 'street' || s.props.some((p) => p.type === 'house' || p.type === 'shopfront' || p.type === 'cabin') ? TOWN : [])])], []); // eslint-disable-line react-hooks/exhaustive-deps
	const [lib, setLib] = useState<Library | null>(files.length ? null : {});
	const [handle] = useState(() => (files.length ? delayRender('opener3d models') : 0));
	useEffect(() => {
		if (!files.length) return;
		const loader = new GLTFLoader();
		Promise.all(files.map((f) => loader.loadAsync(staticFile(`opener3d/models/${f}.glb`)).then((g) => [f, g.scene] as const).catch(() => [f, null] as const)))
			.then((list) => { // a missing model leaves that prop box-built: never a failed render
				const out: Library = {};
				for (const [f, o] of list) if (o) { o.traverse((m) => { if ((m as THREE.Mesh).isMesh) { m.castShadow = true; m.receiveShadow = true; } }); out[f] = o; }
				setLib(out);
			});
	}, []); // eslint-disable-line react-hooks/exhaustive-deps
	useCommitted(lib && files.length ? lib : null, handle);
	return lib;
}

/** A library model, scaled to fit and standing on its spot. */
const RECOLOUR: Record<string, string> = {wood: '#6E4426', woodDark: '#4A2C18', metal: '#B08A3A'};
const Model: React.FC<{src: THREE.Object3D; fit: ['x' | 'y' | 'z', number]; face?: number; color?: string}> = ({src, fit, face, color}) => {
	const obj = useMemo(() => {
		const o = src.clone(true), g = new THREE.Group();
		o.traverse((m) => {
			const mesh = m as THREE.Mesh;
			if (!mesh.isMesh) return;
			const one = (mat: THREE.Material) => {
				const want = mat.name === 'wood' && color ? color : RECOLOUR[mat.name];
				if (!want) return mat;
				const c = (mat as THREE.MeshStandardMaterial).clone();
				c.color = new THREE.Color(want);
				return c;
			};
			mesh.material = Array.isArray(mesh.material) ? mesh.material.map(one) : one(mesh.material);
		});
		o.rotation.y = ((face || 0) * Math.PI) / 180;
		g.add(o);
		const box = new THREE.Box3().setFromObject(g), size = box.getSize(new THREE.Vector3()), c = box.getCenter(new THREE.Vector3());
		o.position.set(-c.x, -box.min.y, -c.z);
		const outer = new THREE.Group();
		outer.add(g);
		outer.scale.setScalar(fit[1] / Math.max(1e-3, size[fit[0]]));
		return outer;
	}, [src, fit, face, color]);
	return <primitive object={obj} />;
};

/** An AI-made 3D part: its primitives in the flat-shaded, Kenney-like look of the library. */
const Assembly: React.FC<{shapes: Shape[]}> = ({shapes}) => <>{shapes.map((p, i) => (
	<mesh key={i} position={p.at} rotation={(p.turn || [0, 0, 0]).map((d) => (d * Math.PI) / 180) as unknown as THREE.Euler} scale={p.size} castShadow receiveShadow>
		{p.shape === 'box' ? <boxGeometry args={[1, 1, 1]} /> : p.shape === 'cylinder' ? <cylinderGeometry args={[0.5, 0.5, 1, 24]} />
			: p.shape === 'sphere' ? <sphereGeometry args={[0.5, 24, 16]} /> : p.shape === 'cone' ? <coneGeometry args={[0.5, 1, 24]} />
			: <torusGeometry args={[0.35, 0.15, 12, 32]} />}
		<meshStandardMaterial color={p.color} roughness={p.metal ? 0.35 : 0.75} metalness={p.metal ? 0.6 : 0} flatShading
			emissive={p.glow ? p.color : '#000'} emissiveIntensity={p.glow ? 0.9 : 0} />
	</mesh>))}</>;

/** A held 3D object, centred on the hand point (Card puts it there). */
const HeldThing: React.FC<{held: Held; lib: Library}> = ({held, lib}) => {
	const m = MODELS[held.type];
	return <group position={[0, -held.height / 2, 0.06]}>
		{held.shapes ? <Assembly shapes={held.shapes} /> : m && lib[m.file] ? <Model src={lib[m.file]} fit={m.fit} face={m.face} /> : null}
	</group>;
};

/** A cobblestone texture in the street's ground colour (2026-11-06: reviews called the flat street plain; the
 * Kenney road tile is plain stone): rounded stones in staggered rows, each a little lighter or darker, dark joints. */
const cobbleCache: Record<string, THREE.Texture> = {};
function cobbles(base: string): THREE.Texture {
	if (cobbleCache[base]) return cobbleCache[base];
	const n = 512, c = document.createElement('canvas'); c.width = c.height = n;
	const g = c.getContext('2d')!, col = new THREE.Color(base);
	g.fillStyle = `#${col.clone().multiplyScalar(0.45).getHexString()}`; g.fillRect(0, 0, n, n);
	const rows = 8, cols = 6, h = n / rows, w = n / cols;
	for (let r = 0; r < rows; r++) for (let k = -1; k <= cols; k++) {
		const x = k * w + (r % 2 ? w / 2 : 0), y = r * h, v = 0.82 + rand(r * 31 + k * 7) * 0.32;
		g.fillStyle = `#${col.clone().multiplyScalar(v).getHexString()}`;
		g.beginPath(); g.roundRect(x + 4, y + 4, w - 8, h - 8, 18); g.fill();
		g.fillStyle = 'rgba(255,255,255,0.10)'; g.beginPath(); g.roundRect(x + 10, y + 8, w - 26, (h - 8) * 0.35, 12); g.fill();
	}
	const t = new THREE.CanvasTexture(c);
	t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(40, 40); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
	return (cobbleCache[base] = t);
}

/** A town building from the fantasy-town kit: `wide` wall modules across, two floors, a gable roof; fronts +z.
 * `seed` varies doors, windows and timber vs plaster, so a street of them doesn't repeat. */
const Building: React.FC<{lib: Library; wide: number; seed: number; unit?: number; floors?: number; wood?: boolean}> = ({lib, wide, seed, unit = 1.45, floors = 2, wood}) => {
	const pick = (k: number, list: string[]) => list[Math.floor(rand(seed * 13 + k) * list.length)];
	const pre = wood || rand(seed) > 0.45 ? 'town/wall-wood' : 'town/wall', door = seed % wide; // opener3d.front_door puts `door` cut-outs at this door
	const cells: [string, number, number][] = [];
	for (let x = 0; x < wide; x++) {
		cells.push([x === door ? `${pre}-door` : pick(x, wood ? [`${pre}-window-shutters`, `${pre}-detail-diagonal`] : [`${pre}-window-shutters`, `${pre}-window-glass`, `${pre}-detail-diagonal`]), x, 0]);
		// timbered upper floors: cross beams between the windows (2026-11-06: reviews wanted timbered fronts)
		for (let y = 1; y < floors; y++) cells.push([pick(x + 9 * y, [`${pre}-window-shutters`, `${pre}-window-glass`, `${pre}-detail-cross`]), x, y]);
	}
	if (!cells.every(([f]) => lib[f]) || !lib['town/roof-gable']) return null;
	return <group scale={unit}>
		{cells.map(([f, x, y], i) => <group key={i} position={[x - (wide - 1) / 2, y, 0]} rotation={[0, WALL_FACE, 0]}><primitive object={lib[f].clone(true)} /></group>)}
		{Array.from({length: wide}, (_, x) => <group key={`r${x}`} position={[x - (wide - 1) / 2, floors, -0.05]} rotation={[0, ROOF_FACE, 0]}><primitive object={lib['town/roof-gable'].clone(true)} /></group>)}
		<mesh position={[0, floors / 2, -0.05]} castShadow receiveShadow><boxGeometry args={[wide, floors, 0.9]} /><meshStandardMaterial color="#6A5A48" /></mesh>
	</group>;
};
// one wall module = one storey: 2.4 m, so a person and a door fit it (at 1.35 m a 2.2 m door covered the upstairs window)
const HOUSE = 2.4; // = opener3d.HOUSE_UNIT
const WALL_FACE = -Math.PI / 2, ROOF_FACE = 0; // the kit's wall modules face +x; turned to front +z

/** Lets the render go on once `ready` has reached the three.js scene: the frame after the React commit, not the
 * moment the files load (frame 0 of a live 2026-11-06 draft was captured before its set existed: empty sky). */
function useCommitted(ready: unknown, handle: number) {
	useEffect(() => {
		if (!ready) return;
		requestAnimationFrame(() => requestAnimationFrame(() => continueRender(handle)));
	}, [ready]); // eslint-disable-line react-hooks/exhaustive-deps
}

function useTextures(dir: string, cutouts: Cutout[]): Record<string, THREE.Texture[]> | null {
	const [tex, setTex] = useState<Record<string, THREE.Texture[]> | null>(null);
	const [handle] = useState(() => delayRender('opener3d cut-outs'));
	useEffect(() => {
		const loader = new THREE.TextureLoader();
		Promise.all(cutouts.map((c) => Promise.all(Array.from({length: c.steps || c.frames}, (_, f) => loader.loadAsync(staticFile(`${dir}/${c.name}_${f}.png`))))))
			.then((lists) => {
				const out: Record<string, THREE.Texture[]> = {};
				lists.forEach((l, i) => { l.forEach((x) => { x.colorSpace = THREE.SRGBColorSpace; x.anisotropy = 8; }); out[cutouts[i].name] = l; });
				setTex(out);
			});
	}, []); // eslint-disable-line react-hooks/exhaustive-deps
	useCommitted(tex, handle);
	return tex;
}

/** A flat drawn cut-out standing in the set: lit by the scene, casting a shadow in its own shape. */
const Card: React.FC<{map: THREE.Texture; w: number; h: number; lift?: number; pos: THREE.Vector3; flip?: boolean; wall?: boolean; face?: THREE.Vector3 | null; tint: string; squash: number; t: number; seed: number;
	hold?: React.ReactNode; hand?: [number, number]}> = ({map, w, h, lift = 0, pos, flip, wall, face, tint, squash, t, seed, hold, hand}) => {
	// `face`: the board turns toward the camera (up to 60 degrees) so a side-on shot never shows a paper-thin stripe
	// (live dancing plague, 2026-11-06); a knocker stays flush with his door, a wall picture with its wall
	const yaw = face ? clamp(Math.atan2(face.x - pos.x, face.z - pos.z), -1.05, 1.05) : 0; // face = this frame's camera (framing)
	const depth = useMemo(() => new THREE.MeshDepthMaterial({depthPacking: THREE.RGBADepthPacking, map, alphaTest: 0.5}), [map]);
	// idle life: a slow breath and sway from the feet, so no standing figure is ever a still board (2026-11-06)
	const breath = wall ? 0 : 0.012 * Math.sin(t * 2.4 + seed), sway = wall ? 0 : 0.018 * Math.sin(t * 1.6 + seed * 2.1);
	const sy = 1 - 0.07 * squash + breath, sx = 1 + 0.05 * squash; // squashed from the feet: the base stays on the floor
	return ( // unlit: the drawing keeps its own clean colours in any light (lit, figures went brown on a brown wall)
		<group position={[pos.x, pos.y, pos.z]} rotation={[0, yaw, sway]}>
			<mesh position={[0, wall ? lift : (h * sy) / 2, 0]} scale={[(flip ? -1 : 1) * sx, sy, 1]} castShadow={!wall} customDepthMaterial={depth}>
				<planeGeometry args={[w, h]} />
				<meshBasicMaterial map={map} color={tint} transparent alphaTest={0.5} side={THREE.DoubleSide} />
			</mesh>
			{hold && hand ? <group position={[(hand[0] - 0.5) * w * sx * (flip ? -1 : 1), hand[1] * h * sy, 0]}>{hold}</group> : null}
		</group>
	);
};

/** 0..1 over a short hit (a knock, a stamp) at each of `times`: up fast, down slower. */
const hitAt = (t: number, times: number[] = [], d = 0.22) => times.reduce((m, h) => { const u = (t - h) / d; return u < 0 || u > 1 ? m : Math.max(m, u < 0.25 ? u / 0.25 : (1 - u) / 0.75); }, 0);
/** A thing's sideways jolt (a door that's knocked on), from the stage's `jolt` effects aimed at it. */
const joltOf = (s: StageProps, name: string, t: number) => {
	const k = hitAt(t, s.effects.filter((e) => e.type === 'jolt' && e.on === name).map((e) => e.at || 0), 0.3);
	return k ? Math.sin(t * 90) * 0.025 * k : 0;
};

const Box: React.FC<{size: [number, number, number]; position: [number, number, number]; color: string; rough?: number; glow?: string}> = ({size, position, color, rough = 0.8, glow}) => (
	<mesh position={position} castShadow receiveShadow>
		<boxGeometry args={size} />
		<meshStandardMaterial color={color} roughness={rough} emissive={glow ?? '#000'} emissiveIntensity={glow ? 1.1 : 0} />
	</mesh>
);

const WOOD = '#6A3E1E', DARK = '#2A1A10', BOOKS = ['#7A2E22', '#2E4A3A', '#8A6A3A', '#3A3550', '#5A2A2A', '#2A3A4A'];

/** The prop library: each type built from boxes, cylinders and spheres, origin on the floor at its centre, facing +z. */
const PropMesh: React.FC<{p: Prop; night: boolean; i: number; lib: Library; sky?: THREE.Texture | null}> = ({p, night, i, lib, sky}) => {
	const c = p.color, lit = p.lit ?? night, model = MODELS[p.type];
	if (model && lib[model.file]) {
		const glow = p.type === 'walllamp' && lit ? <pointLight position={[0, 0.2, 0.35]} intensity={2.5} distance={5} decay={1.5} color="#FFB060" />
			: p.type === 'lamp' && lit ? <pointLight position={[0, 0.42, 0.1]} intensity={6} distance={6} decay={1.5} color="#FFB060" />
			: p.type === 'lamppost' && lit ? <pointLight position={[0, 3.0, 0.2]} intensity={8} distance={9} decay={1.5} color="#FFC870" /> : null;
		return <><Model src={lib[model.file]} fit={model.fit} face={model.face} color={c} />{glow}</>;
	}
	switch (p.type) {
		case 'desk': return <><Box size={[2.3, 0.08, 1.0]} position={[0, 0.82, 0]} color={c || WOOD} rough={0.4} /><Box size={[2.2, 0.78, 0.9]} position={[0, 0.4, 0]} color={c || '#6A3E1E'} rough={0.5} /></>;
		case 'table': return <><Box size={[1.6, 0.07, 0.9]} position={[0, 0.76, 0]} color={c || WOOD} rough={0.4} />{[[-0.7, -0.35], [0.7, -0.35], [-0.7, 0.35], [0.7, 0.35]].map(([x, z], k) => <Box key={k} size={[0.07, 0.74, 0.07]} position={[x, 0.37, z]} color={c || WOOD} />)}</>;
		case 'chair': return <><Box size={[0.5, 0.06, 0.5]} position={[0, 0.48, 0]} color={c || WOOD} /><Box size={[0.5, 0.6, 0.06]} position={[0, 0.8, -0.22]} color={c || WOOD} />{[[-0.2, -0.2], [0.2, -0.2], [-0.2, 0.2], [0.2, 0.2]].map(([x, z], k) => <Box key={k} size={[0.05, 0.46, 0.05]} position={[x, 0.23, z]} color={c || WOOD} />)}</>;
		case 'door': {
			const a = -clamp(p.open || 0, 0, 1) * 1.4;
			return <><Box size={[1.3, 2.45, 0.1]} position={[0, 1.22, -0.06]} color={DARK} /><Box size={[1.0, 2.2, 0.04]} position={[0, 1.1, -0.02]} color="#120a06" glow={p.open ? '#3a2a18' : undefined} />
				<group position={[-0.5, 0, 0.02]} rotation={[0, a, 0]}><Box size={[1.0, 2.2, 0.06]} position={[0.5, 1.1, 0]} color={c || '#6A3E1E'} rough={0.5} /><mesh position={[0.88, 1.05, 0.06]}><sphereGeometry args={[0.04, 12, 12]} /><meshStandardMaterial color="#D9A23A" metalness={0.6} roughness={0.3} /></mesh></group></>;
		}
		case 'window': return <><mesh position={[0, 0, 0.01]}><planeGeometry args={[1.1, 1.6]} /><meshBasicMaterial color={sky ? '#060C1E' : night ? '#22305A' : '#FFE6B8'} fog={false} /></mesh>
			{sky ? <mesh position={[0, 0, 0.015]}><planeGeometry args={[1.1, 1.6]} /><meshBasicMaterial map={sky} transparent blending={THREE.AdditiveBlending} depthWrite={false} fog={false} /></mesh> : null}
			<Box size={[1.24, 0.08, 0.08]} position={[0, 0.8, 0.04]} color={DARK} /><Box size={[1.24, 0.08, 0.08]} position={[0, -0.8, 0.04]} color={DARK} /><Box size={[0.07, 1.7, 0.06]} position={[0, 0, 0.04]} color={DARK} /><Box size={[1.2, 0.06, 0.06]} position={[0, 0.15, 0.04]} color={DARK} /></>;
		case 'frame': return <><Box size={[0.9, 1.1, 0.05]} position={[0, 0, 0.02]} color={c || '#C9A050'} rough={0.35} /><mesh position={[0, 0, 0.05]}><planeGeometry args={[0.7, 0.9]} /><meshStandardMaterial color="#3A3428" /></mesh></>;
		case 'shelf': return <><Box size={[1.3, 2.3, 0.45]} position={[0, 1.15, 0]} color={c || '#3B2418'} />{[0.45, 1.0, 1.55, 2.05].map((y, r) => Array.from({length: 9}, (_, k) => { const h = 0.3 + rand(r * 20 + k + i) * 0.15; return <Box key={`${r}-${k}`} size={[0.11, h, 0.3]} position={[-0.52 + k * 0.13, y + h / 2 - 0.12, 0.05]} color={BOOKS[Math.floor(rand(r * 7 + k * 3 + i) * BOOKS.length)]} />; }))}</>;
		case 'lamp': return <><Box size={[0.06, 0.45, 0.06]} position={[0, 0.25, 0]} color="#C9A050" rough={0.3} /><mesh position={[0, 0.55, 0]}><coneGeometry args={[0.2, 0.22, 24, 1, true]} /><meshStandardMaterial color={c || '#2E5A3A'} emissive="#FFB060" emissiveIntensity={lit ? 0.6 : 0} side={THREE.DoubleSide} /></mesh>{lit ? <pointLight position={[0, 0.5, 0.1]} intensity={6} distance={6} decay={1.5} color="#FFB060" /> : null}</>;
		case 'bed': return <><Box size={[1.2, 1.1, 0.1]} position={[0, 0.55, -1.0]} color={c || WOOD} /><Box size={[1.1, 0.3, 2.0]} position={[0, 0.35, 0]} color={WOOD} /><Box size={[1.05, 0.18, 1.95]} position={[0, 0.58, 0]} color="#F2EDE2" /><Box size={[1.08, 0.2, 1.3]} position={[0, 0.62, 0.32]} color="#5A7AA8" /><Box size={[0.7, 0.14, 0.35]} position={[0, 0.74, -0.75]} color="#FFFFFF" /></>;
		case 'rug': return <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.006, 0]} receiveShadow><planeGeometry args={[3, 2]} /><meshStandardMaterial color={c || '#6E1E1A'} roughness={1} /></mesh>;
		case 'crate': return <Box size={[0.7, 0.7, 0.7]} position={[0, 0.35, 0]} color={c || '#9A6B3E'} />;
		case 'barrel': return <mesh position={[0, 0.45, 0]} castShadow receiveShadow><cylinderGeometry args={[0.3, 0.3, 0.9, 20]} /><meshStandardMaterial color={c || '#7A4E2C'} roughness={0.7} /></mesh>;
		case 'cabinet': return <><Box size={[1.0, 1.8, 0.5]} position={[0, 0.9, 0]} color={c || '#3B2418'} /><Box size={[0.02, 1.6, 0.02]} position={[0, 0.9, 0.26]} color={DARK} /></>;
		case 'counter': return <><Box size={[3, 1.0, 0.7]} position={[0, 0.5, 0]} color={c || '#5A3820'} /><Box size={[3.1, 0.06, 0.8]} position={[0, 1.03, 0]} color={WOOD} rough={0.35} /></>;
		case 'fireplace': return <><Box size={[1.6, 1.3, 0.45]} position={[0, 0.65, 0]} color={c || '#8A8070'} /><Box size={[0.9, 0.7, 0.05]} position={[0, 0.45, 0.21]} color="#120a06" glow="#FF7A2A" /><pointLight position={[0, 0.5, 0.6]} intensity={4} distance={5} decay={1.5} color="#FF8A3A" /></>;
		case 'garden': case 'field': return <Patch lib={lib} kind={p.type} />;
		case 'cabin': if (lib['town/roof-gable']) return <Building lib={lib} wide={2} seed={i + 13} unit={HOUSE} floors={1} wood />; // = opener3d.BUILDINGS
			return <><Box size={[4.6, 2.4, 3.4]} position={[0, 1.2, 0]} color={c || '#7A5234'} /><Box size={[0.9, 1.9, 0.06]} position={[0, 0.95, 1.72]} color="#3A200F" /></>;
		case 'house': if (lib['town/roof-gable']) return <Building lib={lib} wide={3} seed={i + 1} unit={HOUSE} />; {
			const h = 3.2, col = c || ['#B5563C', '#C9A878', '#7A8A6A', '#8A6A5A', '#D9C7A0'][i % 5];
			return <><Box size={[4, h, 4]} position={[0, h / 2, 0]} color={col} /><mesh position={[0, h + 0.7, 0]} castShadow><cylinderGeometry args={[2.9, 2.9, 4.1, 3, 1, false, Math.PI / 2]} /><meshStandardMaterial color="#5A2E22" roughness={0.8} /></mesh>
				<Box size={[0.9, 1.8, 0.06]} position={[0, 0.9, 2.02]} color="#3A200F" />{[-1.2, 1.2].map((x) => <Box key={x} size={[0.8, 0.8, 0.05]} position={[x, 2.1, 2.02]} color={lit ? '#FFD27A' : '#9CB8C8'} glow={lit ? '#FFB050' : undefined} />)}</>;
		}
		case 'shopfront': if (lib['town/roof-gable']) return <><Building lib={lib} wide={3} seed={i + 7} unit={HOUSE} /><Box size={[3 * HOUSE + 0.2, 0.1, 1.2]} position={[0, HOUSE * 0.95, HOUSE * 0.5 + 0.6]} color={c || '#8A2E22'} /></>;
			return <><Box size={[4, 3.6, 3]} position={[0, 1.8, 0]} color={c || '#2E4A3A'} /><Box size={[3, 1.6, 0.06]} position={[0, 1.4, 1.52]} color={lit ? '#FFD27A' : '#B8CCD8'} glow={lit ? '#FFB050' : undefined} /><Box size={[4.2, 0.12, 1.1]} position={[0, 2.6, 1.9]} color="#8A2E22" /></>;
		case 'tree': return <><mesh position={[0, 1.1, 0]} castShadow><cylinderGeometry args={[0.15, 0.22, 2.2, 10]} /><meshStandardMaterial color="#5A3A22" /></mesh>{[[0, 2.6, 0, 1.1], [-0.6, 2.2, 0.2, 0.8], [0.6, 2.3, -0.1, 0.85]].map(([x, y, z, r], k) => <mesh key={k} position={[x, y, z]} castShadow><icosahedronGeometry args={[r, 1]} /><meshStandardMaterial color={c || '#4E7A3A'} roughness={0.9} flatShading /></mesh>)}</>;
		case 'rock': return <mesh position={[0, 0.3, 0]} castShadow receiveShadow><dodecahedronGeometry args={[0.5, 0]} /><meshStandardMaterial color={c || '#8A8478'} flatShading /></mesh>;
		case 'fence': { const L = p.length || 4; return <>{Array.from({length: Math.floor(L / 0.8) + 1}, (_, k) => <Box key={k} size={[0.08, 1.0, 0.08]} position={[-L / 2 + k * 0.8, 0.5, 0]} color={c || '#8A6A44'} />)}<Box size={[L, 0.07, 0.05]} position={[0, 0.75, 0]} color={c || '#8A6A44'} /><Box size={[L, 0.07, 0.05]} position={[0, 0.4, 0]} color={c || '#8A6A44'} /></>; }
		case 'lamppost': return <><mesh position={[0, 1.6, 0]} castShadow><cylinderGeometry args={[0.05, 0.07, 3.2, 10]} /><meshStandardMaterial color="#1E1A18" /></mesh><Box size={[0.28, 0.36, 0.28]} position={[0, 3.3, 0]} color="#1E1A18" glow={lit ? '#FFC870' : undefined} />{lit ? <pointLight position={[0, 3.1, 0]} intensity={8} distance={9} decay={1.5} color="#FFC870" /> : null}</>;
		default: return <Box size={[0.6, 0.6, 0.6]} position={[0, 0.3, 0]} color={c || '#888'} />;
	}
};

const Place: React.FC<{s: StageProps; bg: string; lib: Library}> = ({s, bg, lib}) => {
	const col = s.colors || {};
	if (s.place === 'room') {
		const wall = col.wall || '#7E5A40', trim = col.trim || '#3B2418';
		return <>
			<mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[9, 9]} /><meshStandardMaterial color={col.floor || '#5A3820'} roughness={0.55} /></mesh>
			<mesh position={[0, 2.2, -4]} receiveShadow><planeGeometry args={[9, 4.4]} /><meshStandardMaterial color={wall} roughness={0.9} /></mesh>
			<mesh position={[-4, 2.2, 0]} rotation={[0, Math.PI / 2, 0]} receiveShadow><planeGeometry args={[9, 4.4]} /><meshStandardMaterial color={wall} roughness={0.9} /></mesh>
			<mesh position={[4, 2.2, 0]} rotation={[0, -Math.PI / 2, 0]} receiveShadow><planeGeometry args={[9, 4.4]} /><meshStandardMaterial color={wall} roughness={0.9} /></mesh>
			<mesh position={[0, 4.4, 0]} rotation={[Math.PI / 2, 0, 0]}><planeGeometry args={[9, 9]} /><meshStandardMaterial color={DARK} /></mesh>
			<Box size={[9, 1.1, 0.08]} position={[0, 0.55, -3.96]} color={trim} /><Box size={[0.08, 1.1, 9]} position={[-3.96, 0.55, 0]} color={trim} /><Box size={[0.08, 1.1, 9]} position={[3.96, 0.55, 0]} color={trim} />
		</>;
	}
	const ground = col.ground || (s.place === 'street' ? '#9A8A70' : '#6F8A4A'), night = s.mood === 'night';
	return <>
		<mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, -20]} receiveShadow><planeGeometry args={[80, 80]} /><meshStandardMaterial color={s.place === 'street' ? '#FFFFFF' : ground} map={s.place === 'street' ? cobbles(ground) : null} roughness={1} /></mesh>
		{s.place === 'street' && lib['town/roof-gable'] // rows of town buildings, each different
			? Array.from({length: 12}, (_, k) => { const side = k % 2 ? 1 : -1, z = 1 - Math.floor(k / 2) * 7.8, wide = 2 + Math.floor(rand(k + 40) * 2);
				return <group key={k} position={[side * 5.4, 0, z]} rotation={[0, -side * Math.PI / 2, 0]}><Building lib={lib} wide={wide} seed={k + 20} unit={2.5} /></group>; })
			: s.place === 'street'
			? Array.from({length: 12}, (_, k) => { const side = k % 2 ? 1 : -1, z = 1 - Math.floor(k / 2) * 4.6, h = 2.8 + rand(k) * 1.6;
				return <group key={k} position={[side * 5.2, 0, z]} rotation={[0, -side * Math.PI / 2, 0]}><Box size={[4.4, h, 3]} position={[0, h / 2, 0]} color={['#B5563C', '#C9A878', '#7A8A6A', '#8A6A5A', '#5A6A8A', '#D9C7A0'][k % 6]} />
					<Box size={[4.6, 0.25, 3.2]} position={[0, h + 0.12, 0]} color="#3A2418" />{[-1.2, 0, 1.2].map((x) => <Box key={x} size={[0.7, 0.9, 0.05]} position={[x, h * 0.62, 1.52]} color={night ? '#FFD27A' : '#9CB8C8'} glow={night ? '#FFB050' : undefined} />)}
					<Box size={[0.9, 1.9, 0.05]} position={[1.4, 0.95, 1.52]} color="#3A200F" /></group>; })
			: [[-14, -38, 9], [6, -42, 12], [24, -36, 8]].map(([x, z, r], k) => <mesh key={k} position={[x, -r * 0.55, z]} scale={[1.8, 1, 1]}><sphereGeometry args={[r, 24, 16]} /><meshStandardMaterial color={['#5E7A4A', '#6A845A', '#58704A'][k]} roughness={1} /></mesh>)}
		<mesh position={[0, 20, -60]}><planeGeometry args={[200, 60]} /><meshBasicMaterial color={col.sky || bg} fog={false} /></mesh>
	</>;
};

const Shafts: React.FC<{from: THREE.Vector3; t: number}> = ({from, t}) => {
	const grad = useMemo(() => {
		const c = document.createElement('canvas'); c.width = 4; c.height = 256;
		const g = c.getContext('2d')!, lg = g.createLinearGradient(0, 0, 0, 256);
		lg.addColorStop(0, 'rgba(255,214,150,0.9)'); lg.addColorStop(1, 'rgba(255,214,150,0)');
		g.fillStyle = lg; g.fillRect(0, 0, 4, 256);
		return new THREE.CanvasTexture(c);
	}, []);
	return (
		<group position={[from.x, from.y, from.z + 0.08]} rotation={[-0.62, 0.35, 0]}>
			{[0, 1, 2].map((i) => (
				<mesh key={i} position={[-0.4 + i * 0.4, 0, 2.1]} rotation={[-Math.PI / 2, 0, 0]}>
					<planeGeometry args={[0.38, 4.4]} />
					<meshBasicMaterial map={grad} transparent opacity={0.16 + 0.04 * Math.sin(t * 1.3 + i)} blending={THREE.AdditiveBlending} depthWrite={false} side={THREE.DoubleSide} fog={false} />
				</mesh>
			))}
		</group>
	);
};

const Particles: React.FC<{kind: 'dust' | 'rain' | 'snow'; t: number; centre: THREE.Vector3}> = ({kind, t, centre}) => {
	const geo = useMemo(() => new THREE.BufferGeometry(), []);
	const n = kind === 'dust' ? 220 : 900, pts = new Float32Array(n * 3);
	for (let i = 0; i < n; i++) {
		const fall = kind === 'rain' ? 9 : kind === 'snow' ? 0.6 : -0.05 - rand(i + 9) * 0.05;
		pts[i * 3] = centre.x - 4 + rand(i) * 8 + (kind === 'dust' ? Math.sin(t * 0.4 + i) * 0.08 : kind === 'snow' ? Math.sin(t + i) * 0.2 : 0);
		pts[i * 3 + 1] = (((rand(i + 50) * 4.4 - t * fall) % 4.4) + 4.4) % 4.4 + 0.1;
		pts[i * 3 + 2] = centre.z - 4 + rand(i + 99) * 7;
	}
	geo.setAttribute('position', new THREE.BufferAttribute(pts, 3));
	const look = {dust: ['#FFD9A0', 0.009, 0.45], rain: ['#B8C8E0', 0.02, 0.55], snow: ['#FFFFFF', 0.04, 0.9]}[kind] as [string, number, number];
	return <points geometry={geo}><pointsMaterial color={look[0]} size={look[1]} transparent opacity={look[2]} blending={THREE.AdditiveBlending} depthWrite={false} fog={false} /></points>;
};

/** A picture light above a thing hung on the wall, so it stands out from the wall behind it. */
const PictureLight: React.FC<{at: THREE.Vector3}> = ({at}) => {
	const target = useMemo(() => { const o = new THREE.Object3D(); o.position.copy(at); return o; }, [at.x, at.y, at.z]); // eslint-disable-line react-hooks/exhaustive-deps
	return <><primitive object={target} /><spotLight position={[at.x, Math.min(4.3, at.y + 1.4), at.z + 1.1]} angle={0.6} penumbra={0.8} intensity={14} distance={6} decay={1.5} color="#FFD7A0" target={target} /></>;
};

/** Radio / sound rings rolling out of a thing from its time on. */
const Rings: React.FC<{at: number; pos: THREE.Vector3; t: number}> = ({at, pos, t}) => (
	<group position={[pos.x, pos.y, pos.z + 0.12]}>
		{[0, 1, 2, 3, 4].map((i) => {
			const u = (t - at - i * 0.32) / 1.1;
			if (u < 0 || u > 1) return null;
			const r = 0.5 + u * 1.15;
			return <mesh key={i} scale={[r, r, 1]}><torusGeometry args={[1, 0.03, 8, 96]} /><meshBasicMaterial color="#FF7A3A" transparent opacity={(1 - u) * 0.95} blending={THREE.AdditiveBlending} depthWrite={false} fog={false} /></mesh>;
		})}
	</group>
);

/** An impact: short bright streaks bursting out of a point. */
const Burst: React.FC<{at: number; pos: THREE.Vector3; t: number}> = ({at, pos, t}) => {
	const u = (t - at) / 0.4;
	if (u < 0 || u > 1) return null;
	return <group position={[pos.x, pos.y, pos.z + 0.2]}>{Array.from({length: 10}, (_, i) => { const a = (i / 10) * Math.PI * 2, r = 0.25 + u * 0.6;
		return <mesh key={i} position={[Math.cos(a) * r, Math.sin(a) * r, 0]} rotation={[0, 0, a]}><boxGeometry args={[0.28 * (1 - u) + 0.05, 0.03, 0.01]} /><meshBasicMaterial color="#FFE7A0" transparent opacity={1 - u} blending={THREE.AdditiveBlending} depthWrite={false} fog={false} /></mesh>; })}</group>;
};

/** A puff of dust rolling out of a point (a knock on a door, a landing, a stamp): soft sprites, in the world. */
const Puff: React.FC<{at: number; pos: THREE.Vector3; t: number; color: string}> = ({at, pos, t, color}) => {
	const sprite = useMemo(() => {
		const c = document.createElement('canvas'); c.width = c.height = 64;
		const g = c.getContext('2d')!, rg = g.createRadialGradient(32, 32, 0, 32, 32, 32);
		rg.addColorStop(0, 'rgba(255,255,255,0.9)'); rg.addColorStop(1, 'rgba(255,255,255,0)');
		g.fillStyle = rg; g.fillRect(0, 0, 64, 64);
		return new THREE.CanvasTexture(c);
	}, []);
	const u = (t - at) / 0.8;
	if (u < 0 || u > 1) return null;
	return <group position={[pos.x, pos.y, pos.z + 0.15]}>{Array.from({length: 12}, (_, i) => {
		const a = rand(i + 3) * Math.PI * 2, r = (0.06 + rand(i + 7) * 0.18) * Math.sqrt(u), z = (0.1 + rand(i + 11) * 0.14) * (0.6 + u); // small: it must not hide a face
		return <sprite key={i} position={[Math.cos(a) * r, Math.sin(a) * r * 0.6 + u * 0.15, rand(i) * 0.1]} scale={[z, z, 1]}>
			<spriteMaterial map={sprite} color={color} transparent opacity={(1 - u) * 0.45} depthWrite={false} fog={false} /></sprite>; })}</group>;
};

/** A soft round sprite (smoke, glows). */
const useSoft = () => useMemo(() => {
	const c = document.createElement('canvas'); c.width = c.height = 64;
	const g = c.getContext('2d')!, rg = g.createRadialGradient(32, 32, 0, 32, 32, 32);
	rg.addColorStop(0, 'rgba(255,255,255,0.9)'); rg.addColorStop(1, 'rgba(255,255,255,0)');
	g.fillStyle = rg; g.fillRect(0, 0, 64, 64);
	return new THREE.CanvasTexture(c);
}, []);

/** Electric sparks crackling off a point: jagged bolts that change every frame, flying sparks and a flickering
 *  blue-white light (electricity where there should be none: the Carrington telegraphs, 2026-11-06). */
const Sparks: React.FC<{at: number; pos: THREE.Vector3; t: number}> = ({at, pos, t}) => {
	if (t < at) return null;
	const k = Math.floor(t * 30), on = rand(k * 3.1) > 0.25; // crackles: most frames, not all
	const bolts: React.ReactNode[] = [];
	if (on) for (let b = 0; b < 3; b++) {
		let x = 0, y = 0, a = rand(k * 7 + b) * Math.PI * 2;
		for (let sg = 0; sg < 4; sg++) {
			const len = 0.06 + rand(k * 13 + b * 5 + sg) * 0.08, nx = x + Math.cos(a) * len, ny = y + Math.sin(a) * len;
			bolts.push(<mesh key={`${b}-${sg}`} position={[(x + nx) / 2, (y + ny) / 2, 0]} rotation={[0, 0, a]}><boxGeometry args={[len, 0.012, 0.005]} />
				<meshBasicMaterial color="#DDEBFF" transparent opacity={0.95} blending={THREE.AdditiveBlending} depthWrite={false} fog={false} /></mesh>);
			x = nx; y = ny; a += (rand(k * 17 + b * 3 + sg) - 0.5) * 1.6;
		}
	}
	const flying = Array.from({length: 10}, (_, i) => {
		const run = (t - at) * 1.6 + i / 10, u = run % 1, a = rand(i * 4.3 + Math.floor(run)) * Math.PI * 2, v = 0.5 + rand(i) * 0.4;
		return <mesh key={`f${i}`} position={[Math.cos(a) * v * u, Math.abs(Math.sin(a)) * v * u - 1.6 * u * u, 0]}><sphereGeometry args={[0.009, 6, 6]} />
			<meshBasicMaterial color="#FFE9A8" transparent opacity={1 - u} blending={THREE.AdditiveBlending} depthWrite={false} fog={false} /></mesh>;
	});
	return <group position={[pos.x, pos.y, pos.z + 0.15]}>{bolts}{flying}
		<pointLight intensity={on ? 3 + rand(k) * 4 : 0.6} distance={3.5} decay={1.5} color="#B8D4FF" /></group>;
};

/** Smoke rising from a point, from its time on (scorching, burning). */
const Smoke: React.FC<{at: number; pos: THREE.Vector3; t: number; night: boolean}> = ({at, pos, t, night}) => {
	const soft = useSoft();
	if (t < at) return null;
	return <group position={[pos.x, pos.y, pos.z + 0.1]}>{Array.from({length: 14}, (_, i) => {
		const u = ((t - at) * 0.45 + i / 14) % 1, z = 0.15 + u * 0.6;
		return <sprite key={i} position={[Math.sin(i * 2.1 + t * 0.8) * 0.06 + u * 0.25, u * 1.5, rand(i) * 0.05]} scale={[z, z, 1]}>
			<spriteMaterial map={soft} color={night ? '#4A4E5C' : '#5E5850'} transparent opacity={Math.min(1, (t - at) * 2) * (1 - u) * 0.85} depthWrite={false} fog={false} /></sprite>;
	})}</group>;
};

/** A thing glowing and pulsing (hot, charged or lit): a soft halo and a coloured light. */
const Glow: React.FC<{at: number; pos: THREE.Vector3; t: number; color: string}> = ({at, pos, t, color}) => {
	const soft = useSoft();
	if (t < at) return null;
	const k = Math.min(1, (t - at) * 3) * (0.8 + 0.2 * Math.sin(t * 6));
	return <group position={[pos.x, pos.y, pos.z + 0.12]}>
		<sprite scale={[0.9 * k, 0.9 * k, 1]}><spriteMaterial map={soft} color={color} transparent opacity={0.7 * k} blending={THREE.AdditiveBlending} depthWrite={false} fog={false} /></sprite>
		<pointLight intensity={4 * k} distance={4} decay={1.5} color={color} /></group>;
};

/** Northern lights: green and red curtains rippling, redrawn each frame (outdoors the sky, in a room the windows). */
const useAurora = (on: boolean, t: number) => {
	const tex = useMemo(() => { if (!on) return null; const c = document.createElement('canvas'); c.width = 512; c.height = 256; return new THREE.CanvasTexture(c); }, [on]);
	if (!tex) return null;
	const g = (tex.image as HTMLCanvasElement).getContext('2d')!;
	g.globalCompositeOperation = 'source-over'; g.fillStyle = '#000'; g.fillRect(0, 0, 512, 256);
	for (let i = 0; i < 40; i++) { g.fillStyle = `rgba(240,240,220,${0.4 + 0.4 * rand(i + 3)})`; g.fillRect(rand(i) * 512, rand(i + 70) * 256, 2, 2); }
	g.globalCompositeOperation = 'lighter';
	for (let b = 0; b < 3; b++) for (let x = 0; x < 512; x += 4) {
		const y = 90 + b * 35 + Math.sin(x * 0.014 + t * (0.7 + b * 0.25) + b * 2) * 34 + Math.sin(x * 0.045 - t * 1.2) * 9;
		const h = 70 + 45 * Math.sin(x * 0.021 + t * 0.9 + b), col = b === 1 ? '255,70,120' : '70,255,150';
		const lg = g.createLinearGradient(0, y - h, 0, y + 16);
		lg.addColorStop(0, `rgba(${col},0)`); lg.addColorStop(0.75, `rgba(${col},${b === 1 ? 0.35 : 0.55})`); lg.addColorStop(1, `rgba(${col},0)`);
		g.fillStyle = lg; g.fillRect(x, y - h, 4, h + 16);
	}
	tex.needsUpdate = true;
	return tex;
};

export const Opener3D: React.FC<StageProps> = (s) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const t = frame / fps, m = MOODS[s.mood] || MOODS.interior, night = s.mood === 'night';
	const tex = useTextures(s.dir, s.cutouts), lib = useModels(s);
	const win = s.props.find((p) => p.type === 'window');
	const outdoors = s.place !== 'room';
	const first = s.shots[0]?.target || '', centre = targetOf(s, Array.isArray(first) ? first[0] : first, t);
	const focus = framing(s, t).look; // the lens focuses on what the shot aims at; the rest goes soft
	const aurora = useAurora(s.effects.some((e) => e.type === 'aurora'), t);
	return (
		<AbsoluteFill style={{background: m.bg}}>
			{/* the canvas mounts only when every model and drawing is loaded: it draws on mount and on frame changes,
			    so pieces arriving later were missing from the first frames (frame 0 of the live tests: empty sky) */}
			{lib && tex ? <ThreeCanvas width={width} height={height} shadows gl={{antialias: true}} camera={{fov: 50, near: 0.05, far: 200}}>
				<CameraRig s={s} t={t} />
				<fog attach="fog" args={[m.fog, outdoors ? 14 : 7, outdoors ? 70 : 20]} />
				<hemisphereLight args={[m.sky, m.ground, m.hemi]} />
				<directionalLight position={m.sunPos as unknown as [number, number, number]} intensity={m.sunI} color={m.sun} castShadow
					shadow-mapSize-width={2048} shadow-mapSize-height={2048} shadow-camera-left={-8} shadow-camera-right={8}
					shadow-camera-top={8} shadow-camera-bottom={-8} shadow-camera-far={40} shadow-bias={-0.0004} />
				<directionalLight position={[1.5, 2.5, 6]} intensity={m.fill} color="#FFE2C4" />
				<directionalLight position={[3, 5, -8]} intensity={m.rimI} color={m.rim} />
				<Place s={s} bg={m.bg} lib={lib} />
				{s.props.map((p, i) => {
					const j = p.id ? joltOf(s, p.id, t) : 0;
					return <group key={i} position={p.wall ? [p.at[0] + j, p.at[1], BACK] : [p.at[0] + j, p.y || 0, p.at[1]]} rotation={[0, ((p.turn || 0) * Math.PI) / 180, 0]} scale={p.size || 1}>
						{p.type === 'made' && p.shapes ? <Assembly shapes={p.shapes} /> : <PropMesh p={p} night={night} i={i} lib={lib} sky={aurora} />}
					</group>;
				})}
				{s.cutouts.filter((c) => c.wall).map((c) => <PictureLight key={`pl-${c.name}`} at={cutPos(c, 0)} />)}
				{(() => { const cam = framing(s, t).pos; return s.cutouts.map((c, ci) => {
					// drawings cycle all the time unless `talk` limits them; a knock (focus set) never stops: a live knock froze
					const list = tex[c.name], talking = c.talk && c.focus == null ? t >= c.talk[0] && t < c.talk[1] : list.length > 1;
					const f = talking ? Math.floor((t * (c.fps || 7) * list.length) / c.frames) % list.length : 0; // list = steps drawings per cycle of c.frames
					const pos = cutPos(c, t);
					pos.x += joltOf(s, c.name, t);
					const bw = c.height * c.aspect * (c.wide || 1), bh = c.height * (c.tall || 1); // a wall board keeps its bottom edge
					return <Card key={c.name} map={list[f]} w={bw} h={bh} lift={(bh - c.height) / 2} pos={pos} face={!c.wall && c.focus == null && !c.contact ? cam : null} flip={c.flip} wall={c.wall} tint={m.card} squash={hitAt(t, c.hits)} t={t} seed={ci * 1.7 + 0.4}
							hold={c.held ? <HeldThing held={c.held} lib={lib} /> : null} hand={c.held && c.hands ? c.hands[f % c.hands.length]?.[c.held.hand ?? 1] : undefined} />;
				}); })()}
				{s.effects.map((e, i) => {
					const hit = s.cutouts.find((c) => c.name === e.on && c.contact); // a puff or burst on a knock lands at the fist, not the face
					// on a person, dust and bursts come up from the feet (on the chest they read as smoke, 2026-11-06)
					const who = s.cutouts.find((c) => c.name === e.on && !c.wall);
					const pos = hit && (e.type === 'puff' || e.type === 'burst') ? cutPos(hit, t).add(new THREE.Vector3(hit.contact![0], hit.contact![1], 0.05))
						: who && (e.type === 'puff' || e.type === 'burst') ? cutPos(who, t).add(new THREE.Vector3(0, 0.12, 0.1)) : targetOf(s, e.on || '', t);
					if (e.type === 'rings') return <Rings key={i} at={e.at || 0} pos={pos} t={t} />;
					if (e.type === 'burst') return <Burst key={i} at={e.at || 0} pos={pos} t={t} />;
					if (e.type === 'puff') return <Puff key={i} at={e.at || 0} pos={pos} t={t} color={night ? '#8A90A8' : '#E8DCC8'} />;
					if (e.type === 'shafts' && win) return <Shafts key={i} from={new THREE.Vector3(win.at[0], win.wall ? win.at[1] : 2.3, win.wall ? BACK : win.at[1])} t={t} />;
					if (e.type === 'dust' || e.type === 'rain' || e.type === 'snow') return <Particles key={i} kind={e.type} t={t} centre={centre} />;
						if (e.type === 'sparks') return <Sparks key={i} at={e.at || 0} pos={pos} t={t} />;
						if (e.type === 'smoke') return <Smoke key={i} at={e.at || 0} pos={pos} t={t} night={night} />;
						if (e.type === 'glow') return <Glow key={i} at={e.at || 0} pos={pos} t={t} color={e.color || '#FF9A3A'} />;
						if (e.type === 'aurora' && outdoors && aurora) return <mesh key={i} position={[0, 17, -57]}><planeGeometry args={[150, 36]} />
							<meshBasicMaterial map={aurora} transparent blending={THREE.AdditiveBlending} depthWrite={false} fog={false} /></mesh>;
					return null;
				})}
				{/* the lens: depth of field (the reference's close-ups blur the set behind the subject) and a soft
					    glow on lamps, windows and fire */}
					<EffectComposer multisampling={4}>
						<DepthOfField target={[focus.x, focus.y, focus.z]} worldFocusRange={outdoors ? 3.5 : 1.6} bokehScale={outdoors ? 3 : 4} />
						<Bloom luminanceThreshold={0.82} luminanceSmoothing={0.2} intensity={0.45} mipmapBlur />
					</EffectComposer>
			</ThreeCanvas> : null}
			{/* grade: the mood's glow from the light side, a vignette */}
			<AbsoluteFill style={{background: `radial-gradient(ellipse at 20% 25%, ${m.glow}, rgba(0,0,0,0) 55%), radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.5) 100%)`}} />
		</AbsoluteFill>
	);
};
