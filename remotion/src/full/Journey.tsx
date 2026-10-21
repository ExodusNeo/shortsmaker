import {geoBounds, geoCentroid, geoContains, geoGraticule10, geoMercator, geoPath} from 'd3-geo';
import type {GeoPermissibleObjects} from 'd3-geo';
import {Easing, interpolate, spring, useVideoConfig} from 'remotion';
import {feature} from 'topojson-client';
import type {GeometryCollection, Topology} from 'topojson-specification';
import world10 from 'world-atlas/countries-10m.json';
import world110 from 'world-atlas/countries-110m.json';
import world50 from 'world-atlas/countries-50m.json';
import {Paper, SERIF, skinOf} from './Paper';
import type {FullProps, JourneyFull} from './types';

// Natural Earth country shapes (public domain, offline) at three detail levels: 1:10m for a close-up of a
// region, coarser ones when the camera is far out (10m at world scale makes every frame very slow).
const load = (w: unknown) => {
	const topo = w as Topology<{countries: GeometryCollection<{name: string}>}>;
	const cs = feature(topo, topo.objects.countries).features;
	return {countries: cs, bounds: cs.map((c) => geoBounds(c))};
};
const LEVELS = [load(world110), load(world50), load(world10)];
const {countries, bounds} = LEVELS[2];
const level = (scale: number) => LEVELS[scale < 700 ? 0 : scale < 4000 ? 1 : 2];
const graticule = geoGraticule10();

const W = 1080;
const H = 1920;
const FOCUS: [[number, number], [number, number]] = [[110, 300], [970, 980]]; // stays clear of the captions (y > 1170)
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
type View = {lon: number; lat: number; scale: number};
type Rect = [number, number, number, number];
const INNER: [[number, number], [number, number]] = [[FOCUS[0][0] + 110, FOCUS[0][1] + 110], [FOCUS[1][0] - 110, FOCUS[1][1] - 90]];
const SAFE: Rect = [40, 140, 1040, 1120]; // labels: inside the frame, above the captions

const viewOf = (p: ReturnType<typeof geoMercator>): View => {
	const [lon, lat] = p.invert?.([(FOCUS[0][0] + FOCUS[1][0]) / 2, (FOCUS[0][1] + FOCUS[1][1]) / 2]) ?? [0, 0];
	return {lon, lat, scale: p.scale()};
};

/** Frames the points (plus a box of at least `min` degrees around their middle, so one place or two
 * close ones still show their surroundings). Points are never boxed by hand: a trip across the
 * dateline or half the world stays one sensible view. */
const fitPoints = (pts: [number, number][], min: number, extent = INNER): View => {
	const lon = pts.reduce((a, p) => a + p[0], 0) / pts.length;
	const lat = pts.reduce((a, p) => a + p[1], 0) / pts.length;
	const pad: [number, number][] = [
		[Math.max(-179.9, lon - min / 2), Math.max(-80, lat - min / 2)],
		[Math.min(179.9, lon + min / 2), Math.min(80, lat + min / 2)],
	];
	return viewOf(geoMercator().fitExtent(extent, {type: 'MultiPoint', coordinates: [...pts, ...pad]}));
};

const overlap = (a: Rect, b: Rect) => Math.max(0, Math.min(a[2], b[2]) - Math.max(a[0], b[0])) * Math.max(0, Math.min(a[3], b[3]) - Math.max(a[1], b[1]));
const outside = (r: Rect) => Math.max(0, SAFE[0] - r[0]) + Math.max(0, r[2] - SAFE[2]) + Math.max(0, SAFE[1] - r[1]) + Math.max(0, r[3] - SAFE[3]);

/** Puts each label above, below, right or left of its pin: the first side (preferring away from the
 * other stops) that stays on screen and clear of earlier labels and pins. */
const placeLabels = (xy: [number, number][], lines: string[][]) => {
	const taken: Rect[] = xy.map(([x, y]) => [x - 26, y - 26, x + 26, y + 26]);
	return xy.map(([x, y], i) => {
		const w = Math.max(...lines[i].map((l) => l.length)) * 31 + 20;
		const h = lines[i].length * 56 + 8;
		const others = xy.filter((_, j) => j !== i);
		const [ox, oy] = others.length ? [others.reduce((a, p) => a + p[0], 0) / others.length, others.reduce((a, p) => a + p[1], 0) / others.length] : [x, y + 1];
		const vertical = Math.abs(oy - y) >= Math.abs(ox - x);
		const sides = {
			above: [x - w / 2, y - 44 - h, x + w / 2, y - 44] as Rect,
			below: [x - w / 2, y + 40, x + w / 2, y + 40 + h] as Rect,
			right: [x + 36, y - h / 2, x + 36 + w, y + h / 2] as Rect,
			left: [x - 36 - w, y - h / 2, x - 36, y + h / 2] as Rect,
		};
		const order: (keyof typeof sides)[] = vertical
			? oy > y ? ['above', 'right', 'left', 'below'] : ['below', 'right', 'left', 'above']
			: ox > x ? ['left', 'above', 'below', 'right'] : ['right', 'above', 'below', 'left'];
		const cost = (r: Rect) => taken.reduce((a, b) => a + overlap(r, b), 0) + outside(r) * 400;
		const side = order.reduce((best, s) => (cost(sides[s]) < cost(sides[best]) - 1 ? s : best), order[0]);
		const r = sides[side];
		taken.push(r);
		return {side, x: side === 'right' ? r[0] : side === 'left' ? r[2] : (r[0] + r[2]) / 2, y: r[1] + 46};
	});
};

const wrap = (text: string, max = 14) =>
	text.split(' ').reduce<string[]>((lines, w) => {
		const last = lines[lines.length - 1];
		if (last && (last + ' ' + w).length <= max) lines[lines.length - 1] = last + ' ' + w;
		else lines.push(w);
		return lines;
	}, []);

/** Full-screen old-atlas map: the camera pushes from the country down to the places, each place gets an
 * ink pin and label as it is named, and a dashed red route draws itself from stop to stop. */
export const Journey: React.FC<FullProps<JourneyFull>> = ({full, t, start, end}) => {
	const {fps} = useVideoConfig();
	const stops = full.stops;
	const pts = stops.map((s) => [s.lon, s.lat] as [number, number]);
	const home = countries.find((c) => geoContains(c, pts[0]));
	const b = fitPoints(pts, stops.length > 1 ? 0.5 : 2.5);
	const hb = home ? bounds[countries.indexOf(home)] : null;
	// Start on the whole country (when it is a normal size), else on a wide box; always a real push-in.
	let a = hb && hb[1][0] - hb[0][0] < 120
		? viewOf(geoMercator().fitExtent(FOCUS, {type: 'FeatureCollection', features: [home!, {type: 'Feature', properties: {}, geometry: {type: 'MultiPoint', coordinates: pts}}]} as GeoPermissibleObjects))
		: fitPoints(pts, 40, FOCUS);
	if (a.scale > b.scale / 2.5) a = {lon: b.lon, lat: b.lat, scale: b.scale / 2.5};
	const arrive = Math.max(start + 1.2, Math.min(stops[0].at, end - 1.5));
	const k = interpolate(t, [start, arrive], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const view: View = {
		lon: a.lon + (b.lon - a.lon) * k,
		lat: a.lat + (b.lat - a.lat) * k,
		scale: a.scale * Math.pow(b.scale / a.scale, k), // even zoom speed
	};
	const projection = geoMercator()
		.center([view.lon, view.lat])
		.scale(view.scale)
		.translate([(FOCUS[0][0] + FOCUS[1][0]) / 2, (FOCUS[0][1] + FOCUS[1][1]) / 2])
		.clipExtent([[-20, -20], [W + 20, H + 20]]);
	const path = geoPath(projection);
	// Only countries near the view (10m shapes are heavy).
	// Visible longitudes without wrapping (at world scale the screen edge can pass 180°), visible latitudes.
	const cx = (FOCUS[0][0] + FOCUS[1][0]) / 2;
	const deg = 180 / (Math.PI * view.scale);
	const [vw, ve] = [view.lon - cx * deg, view.lon + (W - cx) * deg];
	const [vn, vs] = [projection.invert?.([cx, 0])?.[1] ?? 85, projection.invert?.([cx, H])?.[1] ?? -85];
	const lod = level(view.scale);
	const near = lod.countries.filter((c, i) => {
		const [[w, s], [e, n]] = lod.bounds[i];
		const lonHit = ve - vw >= 360 || [-360, 0, 360].some((sh) => (w > e ? true : e + sh >= vw - 5 && w + sh <= ve + 5));
		return lonHit && n >= vs - 5 && s <= vn + 5 && (c.properties.name !== 'Antarctica' || stops.some((st) => st.lat < -60));
	});
	const homeShape = near.find((c) => c.properties.name === home?.properties.name);
	// One path per layer (not one per country): far fewer SVG nodes per frame.
	const land = path({type: 'FeatureCollection', features: near} as GeoPermissibleObjects) ?? undefined;
	const homeLand = homeShape ? path(homeShape) ?? undefined : undefined;
	const xy = (p: [number, number]) => projection(p) ?? [W / 2, H / 2];
	const homeName = home?.properties?.name?.toUpperCase();
	const [hx, hy] = home ? xy(geoCentroid(home as GeoPermissibleObjects) as [number, number]) : [0, 0];
	const noteAt = full.noteAt ?? stops[stops.length - 1].at;
	const names = stops.map((st) => wrap(st.name.toUpperCase()));
	const labels = placeLabels(pts.map(xy), names);
	const sk = skinOf(full.skin);

	return (
		<Paper t={t} start={start} seed={full.seed} cam={{x: 540, y: 960, scale: 1}} skin={full.skin}>
			<svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
				<defs>
					{stops.slice(1).map((_, i) => (
						<mask key={i} id={`reveal${full.seed}_${i}`} maskUnits="userSpaceOnUse" x={0} y={0} width={W} height={H}>
							<path
								d={path({type: 'LineString', coordinates: [pts[i], pts[i + 1]]}) ?? undefined}
								fill="none" stroke="white" strokeWidth={30} pathLength={1} strokeDasharray={1}
								strokeDashoffset={1 - interpolate(t, [stops[i].at + 0.2, Math.max(stops[i].at + 0.5, stops[i + 1].at)], [0, 1], {...clamp, easing: Easing.inOut(Easing.quad)})}
							/>
						</mask>
					))}
					<pattern id={`hatch${full.seed}`} width={9} height={9} patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
						<line x1={0} y1={0} x2={0} y2={9} stroke={sk.ink} strokeOpacity={0.16} strokeWidth={1.4} />
					</pattern>
				</defs>
				<path d={path(graticule) ?? undefined} fill="none" stroke={sk.ink} strokeOpacity={0.12} strokeWidth={1} />
				{/* engraved water lines around the coasts, then land wash + hatching, then ink coastlines */}
				{[46, 26, 12].map((wd, r) => (
					<path key={`h${r}`} d={land} fill="none" stroke={sk.coast} strokeOpacity={0.1 + r * 0.07} strokeWidth={wd} strokeLinejoin="round" />
				))}
				<path d={land} fill={sk.landFill} stroke={sk.ink} strokeOpacity={0.85} strokeWidth={1.3} strokeLinejoin="round" />
				{homeLand ? <path d={homeLand} fill={sk.landFill} stroke={sk.ink} strokeOpacity={0.9} strokeWidth={2.2} strokeLinejoin="round" /> : null}
				<path d={land} fill={`url(#hatch${full.seed})`} stroke="none" />
				{homeName ? (
					<text
						x={hx} y={hy} textAnchor="middle" fontFamily={SERIF} fontSize={46} letterSpacing={14} fill={sk.ink}
						opacity={interpolate(k, [0, 0.15, 0.55], [0, 0.55, 0], clamp)}
					>
						{homeName}
					</text>
				) : null}
				{stops.slice(1).map((_, i) => (
					<path
						key={`r${i}`} d={path({type: 'LineString', coordinates: [pts[i], pts[i + 1]]}) ?? undefined}
						fill="none" stroke={sk.accent} strokeWidth={7} strokeDasharray="20 13" strokeLinecap="round"
						mask={`url(#reveal${full.seed}_${i})`}
					/>
				))}
				{stops.map((s, i) => {
					const [x, y] = xy(pts[i]);
					const drop = spring({frame: (t - s.at) * fps, fps, config: {damping: 12, stiffness: 180}});
					if (t < s.at) return null;
					const ring = interpolate(t, [s.at, s.at + 0.9], [0, 1], clamp);
					const lab = labels[i];
					const anchor = lab.side === 'right' ? 'start' : lab.side === 'left' ? 'end' : 'middle';
					return (
						<g key={i}>
							<circle cx={x} cy={y} r={14 + 60 * ring} fill="none" stroke={sk.accent} strokeWidth={4} opacity={1 - ring} />
							<g transform={`translate(${x}, ${y - 50 * (1 - drop)})`} opacity={Math.min(1, drop * 3)}>
								<circle r={17} fill={sk.halo} stroke={sk.ink} strokeWidth={3} />
								<circle r={10} fill={sk.accent} />
							</g>
							<text
								x={lab.x} y={lab.y} textAnchor={anchor}
								fontFamily={SERIF} fontStyle="italic" fontWeight={600} fontSize={58} fill={sk.ink}
								stroke={sk.halo} strokeWidth={12} paintOrder="stroke" strokeLinejoin="round"
								opacity={interpolate(t, [s.at + 0.1, s.at + 0.4], [0, 1], clamp)}
							>
								{names[i].map((l, j) => (
									<tspan key={j} x={lab.x} dy={j ? 56 : 0}>
										{l}
									</tspan>
								))}
							</text>
						</g>
					);
				})}
				{/* compass rose */}
				<g transform="translate(930, 1040)" stroke={sk.ink} strokeWidth={2} fill="none" opacity={0.7}>
					<circle r={38} />
					<circle r={30} strokeOpacity={0.5} />
					<path d="M0 -58 L9 0 L0 58 L-9 0 Z" fill={sk.ink} fillOpacity={0.75} />
					<path d="M-58 0 L0 7 L58 0 L0 -7 Z" fill={sk.ink} fillOpacity={0.35} />
					<text y={-66} textAnchor="middle" fontFamily={SERIF} fontSize={26} fill={sk.ink} stroke="none">
						N
					</text>
				</g>
			</svg>
			{full.note ? (
				<div
					style={{
						position: 'absolute', top: 175, left: 0, right: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 26,
						fontFamily: SERIF, fontSize: 52, letterSpacing: 10, color: sk.ink,
						opacity: interpolate(t, [noteAt, noteAt + 0.4], [0, 1], clamp),
					}}
				>
					<div style={{height: 2, width: 90, background: sk.ink}} />
					{full.note.toUpperCase()}
					<div style={{height: 2, width: 90, background: sk.ink}} />
				</div>
			) : null}
		</Paper>
	);
};
