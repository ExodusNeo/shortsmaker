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

type XZ = [number, number];
export type Cutout = {name: string; frames: number; height: number; aspect: number; at: XZ; y?: number; wall?: boolean;
	flip?: boolean; talk?: [number, number]; fps?: number; path?: [number, number, number][]};
export type Prop = {type: string; id?: string; at: XZ; y?: number; wall?: boolean; turn?: number; size?: number; color?: string;
	lit?: boolean; open?: number; length?: number};
export type Shot = {at: number; target: string | string[]; distance: number; height?: number; turn?: number; fov?: number; move?: 'cut' | 'whip' | 'push'};
export type Effect = {type: 'rings' | 'dust' | 'shafts' | 'burst' | 'shake' | 'rain' | 'snow'; at?: number; on?: string};
export type StageProps = {fps: number; seconds: number; dir: string; place: 'room' | 'street' | 'outdoors';
	mood: 'day' | 'golden' | 'dusk' | 'night' | 'interior'; colors?: {wall?: string; floor?: string; ground?: string; sky?: string; trim?: string};
	props: Prop[]; cutouts: Cutout[]; shots: Shot[]; effects: Effect[]};

export const calculateOpener3D: CalculateMetadataFunction<StageProps> = ({props}) => ({
	fps: props.fps, durationInFrames: Math.max(1, Math.ceil(props.seconds * props.fps)),
});

const MOODS = {
	day: {sky: '#BFD8FF', ground: '#6A5A40', hemi: 1.6, sun: '#FFF1D6', sunI: 2.6, sunPos: [-6, 9, 4], fill: 0.6, fog: '#C9DCEA', bg: '#9CC8F0', glow: 'rgba(255,240,200,0.10)'},
	golden: {sky: '#FFD9A8', ground: '#5A3A28', hemi: 1.3, sun: '#FFB46A', sunI: 2.8, sunPos: [-8, 3.5, 2], fill: 0.5, fog: '#E8B88A', bg: '#F2B577', glow: 'rgba(255,190,110,0.16)'},
	dusk: {sky: '#C88AA0', ground: '#3A2440', hemi: 1.0, sun: '#FF8A5A', sunI: 2.0, sunPos: [-8, 2, -4], fill: 0.4, fog: '#7A5A78', bg: '#E07A5A', glow: 'rgba(255,140,90,0.14)'},
	night: {sky: '#5A6A9A', ground: '#141020', hemi: 0.6, sun: '#9EB6FF', sunI: 0.9, sunPos: [-5, 8, 2], fill: 0.25, fog: '#1A2040', bg: '#0E1430', glow: 'rgba(140,170,255,0.08)'},
	interior: {sky: '#9DB4D8', ground: '#4A2C18', hemi: 1.8, sun: '#FFD49A', sunI: 2.6, sunPos: [-6, 4.6, -0.6], fill: 1.3, fog: '#3a2618', bg: '#120c08', glow: 'rgba(255,200,130,0.10)'},
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
function targetOf(s: StageProps, name: string, t: number): THREE.Vector3 {
	const c = s.cutouts.find((q) => q.name === name);
	if (c) { const p = cutPos(c, t); return c.wall ? p : p.add(new THREE.Vector3(0, c.height * 0.62, 0)); }
	const p = s.props.find((q) => q.id === name);
	if (p) return p.wall ? new THREE.Vector3(p.at[0], p.at[1], BACK) : new THREE.Vector3(p.at[0], (p.y || 0) + 0.8 * (p.size || 1), p.at[1]);
	return new THREE.Vector3(0, 1.4, -2);
}

/** Where a shot aims, and how far back it must stand to fit everything it names (a list = the middle of them all,
 * wide enough to keep each one inside the frame: a live McLean draft cut the grocer off at the edge). */
function aim(s: StageProps, target: string | string[], fov: number, t: number) {
	const names = Array.isArray(target) ? target : [target];
	const pts = names.map((n) => targetOf(s, n, t));
	const tg = pts.reduce((a, b) => a.add(b), new THREE.Vector3()).divideScalar(pts.length);
	if (pts.length < 2) return {tg, fit: 0};
	const half = Math.max(...pts.map((p) => Math.abs(p.x - tg.x))) + 0.7; // each subject's half width plus a margin
	const hfov = 2 * Math.atan(Math.tan((fov * Math.PI) / 360) * (9 / 16)); // the portrait frame's horizontal view
	return {tg, fit: half / Math.tan(hfov / 2)};
}

function framing(s: StageProps, t: number) {
	const shots = s.shots.length ? s.shots : [{at: 0, target: '', distance: 5}];
	const one = (sh: Shot, at: number) => {
		const fov = clamp(sh.fov || 50, 28, 72), {tg, fit} = aim(s, sh.target, fov, at);
		const d = Math.max(sh.distance, fit) * (1 - 0.035 * Math.max(0, at - sh.at)); // every shot drifts in
		const a = ((sh.turn || 0) * Math.PI) / 180;
		const pos = new THREE.Vector3(tg.x + Math.sin(a) * d, tg.y + (sh.height || 0), tg.z + Math.cos(a) * d);
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

function useTextures(dir: string, cutouts: Cutout[]): Record<string, THREE.Texture[]> | null {
	const [tex, setTex] = useState<Record<string, THREE.Texture[]> | null>(null);
	const [handle] = useState(() => delayRender('opener3d cut-outs'));
	useEffect(() => {
		const loader = new THREE.TextureLoader();
		Promise.all(cutouts.map((c) => Promise.all(Array.from({length: c.frames}, (_, f) => loader.loadAsync(staticFile(`${dir}/${c.name}_${f}.png`))))))
			.then((lists) => {
				const out: Record<string, THREE.Texture[]> = {};
				lists.forEach((l, i) => { l.forEach((x) => { x.colorSpace = THREE.SRGBColorSpace; x.anisotropy = 8; }); out[cutouts[i].name] = l; });
				setTex(out);
				continueRender(handle);
			});
	}, []); // eslint-disable-line react-hooks/exhaustive-deps
	return tex;
}

/** A flat drawn cut-out standing in the set: lit by the scene, casting a shadow in its own shape. */
const Card: React.FC<{map: THREE.Texture; w: number; h: number; pos: THREE.Vector3; flip?: boolean; wall?: boolean}> = ({map, w, h, pos, flip, wall}) => {
	const depth = useMemo(() => new THREE.MeshDepthMaterial({depthPacking: THREE.RGBADepthPacking, map, alphaTest: 0.5}), [map]);
	return (
		<mesh position={[pos.x, wall ? pos.y : pos.y + h / 2, pos.z]} scale={[flip ? -1 : 1, 1, 1]} castShadow={!wall} customDepthMaterial={depth}>
			<planeGeometry args={[w, h]} />
			<meshStandardMaterial map={map} transparent alphaTest={0.5} roughness={0.9} side={THREE.DoubleSide} />
		</mesh>
	);
};

const Box: React.FC<{size: [number, number, number]; position: [number, number, number]; color: string; rough?: number; glow?: string}> = ({size, position, color, rough = 0.8, glow}) => (
	<mesh position={position} castShadow receiveShadow>
		<boxGeometry args={size} />
		<meshStandardMaterial color={color} roughness={rough} emissive={glow ?? '#000'} emissiveIntensity={glow ? 1.1 : 0} />
	</mesh>
);

const WOOD = '#6A3E1E', DARK = '#2A1A10', BOOKS = ['#7A2E22', '#2E4A3A', '#8A6A3A', '#3A3550', '#5A2A2A', '#2A3A4A'];

/** The prop library: each type built from boxes, cylinders and spheres, origin on the floor at its centre, facing +z. */
const PropMesh: React.FC<{p: Prop; night: boolean; i: number}> = ({p, night, i}) => {
	const c = p.color, lit = p.lit ?? night;
	switch (p.type) {
		case 'desk': return <><Box size={[2.3, 0.08, 1.0]} position={[0, 0.82, 0]} color={c || WOOD} rough={0.4} /><Box size={[2.2, 0.78, 0.9]} position={[0, 0.4, 0]} color={c || '#6A3E1E'} rough={0.5} /></>;
		case 'table': return <><Box size={[1.6, 0.07, 0.9]} position={[0, 0.76, 0]} color={c || WOOD} rough={0.4} />{[[-0.7, -0.35], [0.7, -0.35], [-0.7, 0.35], [0.7, 0.35]].map(([x, z], k) => <Box key={k} size={[0.07, 0.74, 0.07]} position={[x, 0.37, z]} color={c || WOOD} />)}</>;
		case 'chair': return <><Box size={[0.5, 0.06, 0.5]} position={[0, 0.48, 0]} color={c || WOOD} /><Box size={[0.5, 0.6, 0.06]} position={[0, 0.8, -0.22]} color={c || WOOD} />{[[-0.2, -0.2], [0.2, -0.2], [-0.2, 0.2], [0.2, 0.2]].map(([x, z], k) => <Box key={k} size={[0.05, 0.46, 0.05]} position={[x, 0.23, z]} color={c || WOOD} />)}</>;
		case 'door': {
			const a = -clamp(p.open || 0, 0, 1) * 1.4;
			return <><Box size={[1.3, 2.45, 0.1]} position={[0, 1.22, -0.06]} color={DARK} /><Box size={[1.0, 2.2, 0.04]} position={[0, 1.1, -0.02]} color="#120a06" glow={p.open ? '#3a2a18' : undefined} />
				<group position={[-0.5, 0, 0.02]} rotation={[0, a, 0]}><Box size={[1.0, 2.2, 0.06]} position={[0.5, 1.1, 0]} color={c || '#6A3E1E'} rough={0.5} /><mesh position={[0.88, 1.05, 0.06]}><sphereGeometry args={[0.04, 12, 12]} /><meshStandardMaterial color="#D9A23A" metalness={0.6} roughness={0.3} /></mesh></group></>;
		}
		case 'window': return <><mesh position={[0, 0, 0.01]}><planeGeometry args={[1.1, 1.6]} /><meshBasicMaterial color={night ? '#22305A' : '#FFE6B8'} fog={false} /></mesh>
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
		case 'house': {
			const h = 3.2, col = c || ['#B5563C', '#C9A878', '#7A8A6A', '#8A6A5A', '#D9C7A0'][i % 5];
			return <><Box size={[4, h, 4]} position={[0, h / 2, 0]} color={col} /><mesh position={[0, h + 0.7, 0]} castShadow><cylinderGeometry args={[2.9, 2.9, 4.1, 3, 1, false, Math.PI / 2]} /><meshStandardMaterial color="#5A2E22" roughness={0.8} /></mesh>
				<Box size={[0.9, 1.8, 0.06]} position={[0, 0.9, 2.02]} color="#3A200F" />{[-1.2, 1.2].map((x) => <Box key={x} size={[0.8, 0.8, 0.05]} position={[x, 2.1, 2.02]} color={lit ? '#FFD27A' : '#9CB8C8'} glow={lit ? '#FFB050' : undefined} />)}</>;
		}
		case 'shopfront': return <><Box size={[4, 3.6, 3]} position={[0, 1.8, 0]} color={c || '#2E4A3A'} /><Box size={[3, 1.6, 0.06]} position={[0, 1.4, 1.52]} color={lit ? '#FFD27A' : '#B8CCD8'} glow={lit ? '#FFB050' : undefined} /><Box size={[4.2, 0.12, 1.1]} position={[0, 2.6, 1.9]} color="#8A2E22" /></>;
		case 'tree': return <><mesh position={[0, 1.1, 0]} castShadow><cylinderGeometry args={[0.15, 0.22, 2.2, 10]} /><meshStandardMaterial color="#5A3A22" /></mesh>{[[0, 2.6, 0, 1.1], [-0.6, 2.2, 0.2, 0.8], [0.6, 2.3, -0.1, 0.85]].map(([x, y, z, r], k) => <mesh key={k} position={[x, y, z]} castShadow><icosahedronGeometry args={[r, 1]} /><meshStandardMaterial color={c || '#4E7A3A'} roughness={0.9} flatShading /></mesh>)}</>;
		case 'rock': return <mesh position={[0, 0.3, 0]} castShadow receiveShadow><dodecahedronGeometry args={[0.5, 0]} /><meshStandardMaterial color={c || '#8A8478'} flatShading /></mesh>;
		case 'fence': { const L = p.length || 4; return <>{Array.from({length: Math.floor(L / 0.8) + 1}, (_, k) => <Box key={k} size={[0.08, 1.0, 0.08]} position={[-L / 2 + k * 0.8, 0.5, 0]} color={c || '#8A6A44'} />)}<Box size={[L, 0.07, 0.05]} position={[0, 0.75, 0]} color={c || '#8A6A44'} /><Box size={[L, 0.07, 0.05]} position={[0, 0.4, 0]} color={c || '#8A6A44'} /></>; }
		case 'lamppost': return <><mesh position={[0, 1.6, 0]} castShadow><cylinderGeometry args={[0.05, 0.07, 3.2, 10]} /><meshStandardMaterial color="#1E1A18" /></mesh><Box size={[0.28, 0.36, 0.28]} position={[0, 3.3, 0]} color="#1E1A18" glow={lit ? '#FFC870' : undefined} />{lit ? <pointLight position={[0, 3.1, 0]} intensity={8} distance={9} decay={1.5} color="#FFC870" /> : null}</>;
		default: return <Box size={[0.6, 0.6, 0.6]} position={[0, 0.3, 0]} color={c || '#888'} />;
	}
};

const Place: React.FC<{s: StageProps; bg: string}> = ({s, bg}) => {
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
		<mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, -20]} receiveShadow><planeGeometry args={[80, 80]} /><meshStandardMaterial color={ground} roughness={1} /></mesh>
		{s.place === 'street'
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
	const look = {dust: ['#FFD9A0', 0.014, 0.6], rain: ['#B8C8E0', 0.02, 0.55], snow: ['#FFFFFF', 0.04, 0.9]}[kind] as [string, number, number];
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

export const Opener3D: React.FC<StageProps> = (s) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const t = frame / fps, m = MOODS[s.mood] || MOODS.interior, night = s.mood === 'night';
	const tex = useTextures(s.dir, s.cutouts);
	const win = s.props.find((p) => p.type === 'window');
	const outdoors = s.place !== 'room';
	const first = s.shots[0]?.target || '', centre = targetOf(s, Array.isArray(first) ? first[0] : first, t);
	return (
		<AbsoluteFill style={{background: m.bg}}>
			<ThreeCanvas width={width} height={height} shadows gl={{antialias: true}} camera={{fov: 50, near: 0.05, far: 200}}>
				<CameraRig s={s} t={t} />
				<fog attach="fog" args={[m.fog, outdoors ? 14 : 7, outdoors ? 70 : 20]} />
				<hemisphereLight args={[m.sky, m.ground, m.hemi]} />
				<directionalLight position={m.sunPos as unknown as [number, number, number]} intensity={m.sunI} color={m.sun} castShadow
					shadow-mapSize-width={2048} shadow-mapSize-height={2048} shadow-camera-left={-8} shadow-camera-right={8}
					shadow-camera-top={8} shadow-camera-bottom={-8} shadow-camera-far={40} shadow-bias={-0.0004} />
				<directionalLight position={[1.5, 2.5, 6]} intensity={m.fill} color="#FFE2C4" />
				<Place s={s} bg={m.bg} />
				{s.props.map((p, i) => (
					<group key={i} position={p.wall ? [p.at[0], p.at[1], BACK] : [p.at[0], p.y || 0, p.at[1]]} rotation={[0, ((p.turn || 0) * Math.PI) / 180, 0]} scale={p.size || 1}>
						<PropMesh p={p} night={night} i={i} />
					</group>
				))}
				{s.cutouts.filter((c) => c.wall).map((c) => <PictureLight key={`pl-${c.name}`} at={cutPos(c, 0)} />)}
				{tex ? s.cutouts.map((c) => {
					const list = tex[c.name], talking = c.talk && t >= c.talk[0] && t < c.talk[1];
					const f = talking ? Math.floor(t * (c.fps || 7)) % list.length : 0;
					return <Card key={c.name} map={list[f]} w={c.height * c.aspect} h={c.height} pos={cutPos(c, t)} flip={c.flip} wall={c.wall} />;
				}) : null}
				{s.effects.map((e, i) => {
					const pos = targetOf(s, e.on || '', t);
					if (e.type === 'rings') return <Rings key={i} at={e.at || 0} pos={pos} t={t} />;
					if (e.type === 'burst') return <Burst key={i} at={e.at || 0} pos={pos} t={t} />;
					if (e.type === 'shafts' && win) return <Shafts key={i} from={new THREE.Vector3(win.at[0], win.wall ? win.at[1] : 2.3, win.wall ? BACK : win.at[1])} t={t} />;
					if (e.type === 'dust' || e.type === 'rain' || e.type === 'snow') return <Particles key={i} kind={e.type} t={t} centre={centre} />;
					return null;
				})}
			</ThreeCanvas>
			{/* grade: the mood's glow from the light side, a vignette */}
			<AbsoluteFill style={{background: `radial-gradient(ellipse at 20% 25%, ${m.glow}, rgba(0,0,0,0) 55%), radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.5) 100%)`}} />
		</AbsoluteFill>
	);
};
