import {geoContains, geoMercator, geoPath} from 'd3-geo';
import {useMemo} from 'react';
import {Easing, interpolate, spring, useVideoConfig} from 'remotion';
import {feature} from 'topojson-client';
import type {GeometryCollection, Topology} from 'topojson-specification';
import world from 'world-atlas/countries-110m.json';
import {FONT, moveIn, Pin, useWindow, theme} from './Graphics';
import type {Graphic} from './Short';

// Offline Natural Earth country shapes (public domain): no tiles, no API key, same pixels every render.
const topo = world as unknown as Topology<{countries: GeometryCollection}>;
const countries = feature(topo, topo.objects.countries).features;

const MW = 880;
const MH = 680;
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/** Map card that flies from a world view down to the place, then drops a pin with a label. With a
 * `from` place it frames both and draws the route line from there while flying in. */
export const MapCard: React.FC<{graphic: Graphic; t: number; start: number; end: number; variant: number}> = ({graphic, t, start, end, variant}) => {
	const {fps} = useVideoConfig();
	const {visible, enter, leave, tIn} = useWindow(t, start, end);
	const lon = graphic.lon ?? 0;
	const lat = graphic.lat ?? 0;
	const from = graphic.from;
	const home = useMemo(() => countries.find((c) => geoContains(c, [lon, lat])), [lon, lat]);
	// Final view: ~10x zoom on the place, or zoomed just enough to frame both ends of a route.
	const target = useMemo(() => {
		if (!from) return {center: [lon, lat] as [number, number], zoom: 10};
		const fit = geoMercator().fitExtent([[110, 110], [MW - 110, MH - 150]], {type: 'MultiPoint', coordinates: [[from.lon, from.lat], [lon, lat]]});
		const center = (fit.invert?.([MW / 2, MH / 2]) ?? [lon, lat]) as [number, number];
		return {center, zoom: Math.min(10, Math.max(1, fit.scale() / (MW / (2 * Math.PI))))};
	}, [from, lon, lat]);
	if (!visible) return null;
	// Animation beat (seconds at full speed) -> time; make_shorts.py sets `pace` < 1 for short scenes.
	const at = (sec: number) => tIn + sec * (graphic.pace ?? 1);

	const fly = interpolate(t, [at(0.15), at(1.5)], [0, 1], {...clamp, easing: Easing.bezier(0.65, 0, 0.35, 1)});
	const scale = (MW / (2 * Math.PI)) * Math.pow(target.zoom, fly); // world view -> target view
	const projection = geoMercator()
		.center([interpolate(fly, [0, 1], [0, target.center[0]]), interpolate(fly, [0, 1], [15, target.center[1]])])
		.scale(scale)
		.translate([MW / 2, MH / 2]);
	const path = geoPath(projection);
	const [px, py] = projection([lon, lat]) ?? [MW / 2, MH / 2];
	const drop = spring({frame: (t - at(1.5)) * fps, fps, config: {damping: 9, stiffness: 200}});
	const pulse = ((t - at(1.6)) % 1.2) / 1.2;
	const route = from ? path({type: 'LineString', coordinates: [[from.lon, from.lat], [lon, lat]]}) : null;
	const drawn = interpolate(t, [at(0.8), at(1.5)], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const [fx, fy] = from ? projection([from.lon, from.lat]) ?? [0, 0] : [0, 0];

	return (
		<div
			style={{
				position: 'absolute', top: 250, left: (1080 - MW) / 2, width: MW, ...moveIn(enter, leave, variant), borderRadius: 36, overflow: 'hidden',
				background: theme.panel, border: '5px solid rgba(255,255,255,0.9)', boxShadow: '0 24px 60px rgba(0,0,0,0.6)',
			}}
		>
			<svg width={MW} height={MH} style={{display: 'block'}}>
				{countries.map((c, k) => (
					<path
						key={k}
						d={path(c) ?? undefined}
						fill={c === home ? interpolateColor(fly) : theme.land}
						stroke={c === home ? theme.accent : theme.border}
						strokeWidth={c === home ? 2.5 : 0.8}
					/>
				))}
				{route ? (
					<>
						<path d={route} fill="none" stroke="#000" strokeWidth={13} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - drawn} opacity={0.6} />
						<path d={route} fill="none" stroke={theme.accent} strokeWidth={7} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - drawn} />
						<circle cx={fx} cy={fy} r={13} fill="white" stroke="#000" strokeWidth={4} opacity={drawn > 0 ? 1 : 0} />
						<text x={fx} y={fy + (fy > MH / 2 ? -26 : 50)} textAnchor="middle" fontFamily={FONT} fontSize={38} fill="white" stroke="#000" strokeWidth={6} paintOrder="stroke" opacity={drawn > 0 ? 1 : 0}>
							{from?.text}
						</text>
					</>
				) : null}
				{t > at(1.6) ? (
					<circle cx={px} cy={py} r={20 + 70 * pulse} fill="none" stroke={theme.accent} strokeWidth={5} opacity={1 - pulse} />
				) : null}
				<g transform={`translate(${px - 30}, ${py - 80 - 120 * (1 - drop)})`} opacity={drop > 0.01 ? 1 : 0}>
					<Pin size={80} />
				</g>
			</svg>
			<div
				style={{
					position: 'absolute', left: 0, right: 0, bottom: 26, display: 'flex', justifyContent: 'center',
					opacity: interpolate(t, [at(1.5), at(1.8)], [0, 1], clamp),
					transform: `translateY(${interpolate(t, [at(1.5), at(1.8)], [30, 0], clamp)}px)`,
				}}
			>
				<div style={{background: 'rgba(0,0,0,0.75)', borderRadius: 50, padding: '12px 38px', fontFamily: FONT, fontSize: 60, color: 'white'}}>
					{graphic.text}
				</div>
			</div>
		</div>
	);
};

// The destination country warms from the base slate to a muted gold as the camera arrives.
const interpolateColor = (k: number) => {
	const rgb = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
	const [from, to] = [rgb(theme.land), rgb(theme.accent).map((v) => v * 0.48)];
	return `rgb(${from.map((v, i) => Math.round(v + (to[i] - v) * k)).join(', ')})`;
};
