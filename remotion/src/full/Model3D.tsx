import {ThreeCanvas} from '@remotion/three';
import React, {useEffect, useMemo, useState} from 'react';
import {AbsoluteFill, cancelRender, continueRender, delayRender, Easing, interpolate, spring, staticFile, useVideoConfig} from 'remotion';
import * as THREE from 'three';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {TYPE, skinOf, useFonts} from './Paper';
import type {FullProps, ModelFull} from './types';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const DROP = 0.45; // seconds the model falls before it lands

/** Three light bands, like the Blender openers' toon look (look_toon.apply). */
const bands = (() => {
	const tex = new THREE.DataTexture(new Uint8Array([90, 170, 255]), 3, 1, THREE.RedFormat);
	tex.minFilter = tex.magFilter = THREE.NearestFilter;
	tex.needsUpdate = true;
	return tex;
})();

/** Inverted-hull ink outline: the mesh pushed out along its normals, back faces only. */
const outline = (ink: string, width: number) =>
	new THREE.ShaderMaterial({
		side: THREE.BackSide,
		uniforms: {ink: {value: new THREE.Color(ink)}, w: {value: width}},
		vertexShader: 'uniform float w; void main(){ gl_Position = projectionMatrix * modelViewMatrix * vec4(position + normal * w, 1.0); }',
		fragmentShader: 'uniform vec3 ink; void main(){ gl_FragColor = vec4(ink, 1.0); }',
	});

/** The GLB, toon-shaded and outlined, scaled to 2 units tall at most and stood on y = 0. */
const useModel = (src: string, ink: string) => {
	const [handle] = useState(() => delayRender(`model ${src}`));
	const [model, setModel] = useState<{root: THREE.Group; height: number; width: number} | null>(null);
	useEffect(() => {
		new GLTFLoader().load(
			staticFile(src),
			(gltf) => {
				const root = gltf.scene;
				const box = new THREE.Box3().setFromObject(root);
				const size = box.getSize(new THREE.Vector3());
				const k = 2 / Math.max(size.x, size.y, size.z, 1e-6);
				root.scale.setScalar(k);
				const c = box.getCenter(new THREE.Vector3());
				root.position.set(-c.x * k, -box.min.y * k, -c.z * k);
				const meshes: THREE.Mesh[] = [];
				root.traverse((o) => o instanceof THREE.Mesh && meshes.push(o));
				for (const m of meshes) {
					const old = (Array.isArray(m.material) ? m.material[0] : m.material) as THREE.MeshStandardMaterial;
					m.material = new THREE.MeshToonMaterial({color: old.color ?? new THREE.Color('#cccccc'), map: old.map ?? null, gradientMap: bands});
					m.add(new THREE.Mesh(m.geometry, outline(ink, 0.012 / Math.max(m.getWorldScale(new THREE.Vector3()).x, 1e-6))));
				}
				const group = new THREE.Group();
				group.add(root);
				setModel({root: group, height: size.y * k, width: Math.max(size.x, size.z) * k});
				continueRender(handle);
			},
			undefined,
			(e) => cancelRender(e),
		);
	}, [src, ink, handle]);
	return model;
};

/** The one real thing at the heart of the hook as a low-poly 3D model: it drops onto the frame from the first
 * frame, lands with a squash, and turns while the camera cranes round; the headline stamps in above it. */
export const Model3D: React.FC<FullProps<ModelFull>> = ({full, t, start, end}) => {
	useFonts();
	const {width, height, fps} = useVideoConfig();
	const sk = skinOf(full.skin);
	const model = useModel(full.src, sk.dark ? '#05070a' : '#2c1f0e');
	const s = t - start;
	const span = Math.max(1, end - start);
	const fall = interpolate(s, [0, DROP], [0.45, 0], {...clamp, easing: Easing.in(Easing.quad)}); // in shot from frame 0
	const land = spring({frame: Math.max(0, (s - DROP) * fps), fps, config: {damping: 9, stiffness: 180}});
	const squash = s < DROP ? 1 : 1 - 0.14 * Math.sin(Math.PI * Math.min(1, land)) * (1 - land);
	const orbit = interpolate(s, [0, span], [-0.4, 0.25], {...clamp, easing: Easing.inOut(Easing.sin)});
	const crane = interpolate(s, [0, span], [0.18, 0.42], clamp);
	const h = model?.height ?? 1.5;
	// framed to fill about 85% of the width or 38% of the height (whichever is reached first), then pushing in: the band
	// between the headline (to 22% down) and the captions (from 64% down)
	const fit = Math.max((model?.width ?? 2) / (0.3226 * 0.85), h / (0.573 * 0.38));
	const dist = fit * interpolate(s, [0, span], [1.08, 0.92], {...clamp, easing: Easing.out(Easing.cubic)});
	const cam = useMemo(() => new THREE.PerspectiveCamera(32, width / height, 0.1, 100), [width, height]);
	cam.position.set(Math.sin(orbit) * dist, h * 0.5 + Math.sin(crane) * dist, Math.cos(orbit) * dist);
	cam.lookAt(0, h * 0.5 - 0.03 * dist, 0); // the model's centre sits 45% down the screen, clear of the captions below
	const label = spring({frame: Math.max(0, (t - full.at) * fps), fps, config: {damping: 14, stiffness: 160}});
	const note = full.note ? spring({frame: Math.max(0, (t - (full.noteAt ?? full.at + 0.5)) * fps), fps, config: {damping: 16}}) : 0;
	return (
		<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 62%, ${sk.card} 0%, ${sk.bg} 70%)`}}>
			<ThreeCanvas width={width} height={height} camera={cam} gl={{antialias: true}}>
				<ambientLight intensity={0.55} />
				<directionalLight position={[3, 6, 4]} intensity={2.2} color="#ffe8c8" />
				<directionalLight position={[-4, 3, -5]} intensity={1.2} color={sk.accent} />
				<mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.001, 0]} scale={(1.1 - 0.5 * fall) * 0.65 * (model?.width ?? 2)}>
					<circleGeometry args={[1, 48]} />
					<meshBasicMaterial color="#000000" transparent opacity={0.35 * (1 - fall * 0.8)} />
				</mesh>
				{model ? (
					<group position={[0, fall * 4, 0]} scale={[1 / Math.sqrt(squash), squash, 1 / Math.sqrt(squash)]} rotation={[0, orbit * -0.6, 0]}>
						<primitive object={model.root} />
					</group>
				) : null}
			</ThreeCanvas>
			<div style={{position: 'absolute', left: 60, right: 60, top: 190, textAlign: 'center', opacity: Math.min(1, label * 1.4),
				transform: `scale(${interpolate(label, [0, 1], [1.6, 1])})`}}>
				<div style={{fontFamily: TYPE, fontSize: 124, lineHeight: 1.05, color: sk.ink, letterSpacing: 2,
					textShadow: sk.dark ? '0 4px 24px rgba(0,0,0,0.8)' : 'none'}}>{full.label}</div>
				<div style={{height: 8, margin: '22px auto 0', background: sk.accent, width: `${interpolate(label, [0, 1], [0, 70])}%`}} />
				{full.note ? (
					<div style={{fontFamily: TYPE, fontSize: 68, color: sk.accent, marginTop: 22, opacity: note}}>{full.note}</div>
				) : null}
			</div>
			<AbsoluteFill style={{boxShadow: `inset 0 0 260px ${sk.vignette}`, pointerEvents: 'none'}} />
		</AbsoluteFill>
	);
};
