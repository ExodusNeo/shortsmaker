import React from 'react';
import {
	CalloutTag,
	CustomFull,
	Easing,
	FullProps,
	Paper,
	SERIF,
	StampBadge,
	TYPE,
	TitleBanner,
	appear,
	clamp,
	cueAt,
	focusCam,
	interpolate,
	skinOf,
} from '../toolkit';

/** Custom 0 (Diagram, blueprint skin): Cross-section of the 1628 warship Vasa heeling 22° as wind hits
 * her tall sails and seawater pours through the open lower gunports. */
export const Custom0: React.FC<FullProps<CustomFull>> = ({full, t, start, end}) => {
	const sk = skinOf(full.skin ?? 'blueprint');
	const c0 = cueAt(full, 0, start, end, 3); // wind / heeled
	const c1 = cueAt(full, 1, start, end, 3); // gunports / water poured
	const c2 = cueAt(full, 2, start, end, 3); // sank
	const tiltK = interpolate(t, [c0, c1 + 0.8], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const floodK = interpolate(t, [c1, c2 + 0.4], [0, 1], {...clamp, easing: Easing.inOut(Easing.quad)});
	const sinkY = interpolate(t, [c2, end - 0.3], [0, 48], {...clamp, easing: Easing.in(Easing.quad)});
	const deg = Math.round(tiltK * 22);
	const cam = focusCam(
		540,
		interpolate(t, [start, end], [610, 640], clamp),
		interpolate(t, [start, c1, end], [1.0, 1.07, 1.0], clamp),
	);

	const waterY = 735;
	const waveShift = (t - start) * 90;

	return (
		<Paper t={t} start={start} seed={full.seed} cam={cam} skin={full.skin ?? 'blueprint'}>
			<TitleBanner title={full.title || 'VASA · CROSS-SECTION (1628)'} sub="TOP-HEAVY HULL & OPEN LOWER GUNPORTS" t={t} at={start + 0.1} skin={full.skin ?? 'blueprint'} />

			<svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
				<defs>
					<clipPath id="hullClip">
						<path d="M -200 -140 L 200 -140 L 165 120 C 120 205, -120 205, -165 120 Z" />
					</clipPath>
					<pattern id="bpWater" width={16} height={16} patternUnits="userSpaceOnUse" patternTransform="rotate(-25)">
						<line x1={0} y1={0} x2={0} y2={16} stroke="#4fc3ff" strokeOpacity={0.45} strokeWidth={3} />
					</pattern>
				</defs>

				{/* Angle protractor arc behind the ship */}
				<g transform={`translate(540, ${waterY - 35})`} opacity={0.8}>
					<path d="M 0 -350 A 350 350 0 0 1 148 -317" fill="none" stroke={sk.ink} strokeWidth={3} strokeDasharray="8 8" />
					<line x1={0} y1={-375} x2={0} y2={20} stroke={sk.ink} strokeOpacity={0.35} strokeWidth={2} strokeDasharray="10 10" />
					<text x={95} y={-360} textAnchor="middle" fontFamily={TYPE} fontSize={38} fill={sk.accent}>
						{deg}° HEEL
					</text>
				</g>

				{/* Wind gust arrows on the left */}
				{appear(t, c0, 0.4) > 0 ? (
					<g opacity={appear(t, c0, 0.4)}>
						{[400, 465, 530].map((y, i) => {
							const slide = interpolate(t, [c0 + i * 0.08, c0 + 0.7 + i * 0.08], [-50, 20], clamp);
							return (
								<g key={i} transform={`translate(${slide}, 0)`}>
									<line x1={90} y1={y} x2={255} y2={y} stroke={sk.accent} strokeWidth={6} strokeLinecap="round" />
									<path d={`M 245 ${y - 12} L 272 ${y} L 245 ${y + 12} Z`} fill={sk.accent} />
								</g>
							);
						})}
						<text x={175} y={368} textAnchor="middle" fontFamily={TYPE} fontSize={32} fill={sk.accent}>
							WIND GUST
						</text>
					</g>
				) : null}

				{/* Tilting ship cross-section */}
				<g transform={`translate(540, ${waterY + sinkY}) rotate(${deg})`}>
					{/* Mast & sails */}
					<line x1={0} y1={-140} x2={0} y2={-410} stroke={sk.ink} strokeWidth={10} strokeLinecap="round" />
					<line x1={-125} y1={-340} x2={125} y2={-340} stroke={sk.ink} strokeWidth={6} />
					<line x1={-155} y1={-230} x2={155} y2={-230} stroke={sk.ink} strokeWidth={6} />
					<path d="M -120 -340 Q -65 -285 -145 -230 L 145 -230 Q 190 -285 120 -340 Z" fill="rgba(232,244,253,0.12)" stroke={sk.ink} strokeWidth={3} />

					{/* Flooding water inside the hull */}
					<g clipPath="url(#hullClip)">
						<g transform={`rotate(${-deg})`}>
							<rect x={-280} y={155 - floodK * 215} width={560} height={300} fill="url(#bpWater)" />
							<rect x={-280} y={155 - floodK * 215} width={560} height={300} fill="rgba(79,195,255,0.28)" stroke="#4fc3ff" strokeWidth={4} />
						</g>
						<path d="M -120 128 L 120 128 L 92 182 L -92 182 Z" fill="rgba(255,255,255,0.18)" stroke={sk.ink} strokeWidth={2.5} />
						<text x={0} y={163} textAnchor="middle" fontFamily={TYPE} fontSize={23} fill={sk.ink}>
							LIGHT BALLAST
						</text>
					</g>

					{/* Hull outer timbers & two heavy gun decks */}
					<path
						d="M -200 -140 L 200 -140 L 165 120 C 120 205, -120 205, -165 120 Z"
						fill="rgba(19,42,70,0.55)"
						stroke={sk.ink}
						strokeWidth={8}
						strokeLinejoin="round"
					/>
					<line x1={-188} y1={-65} x2={188} y2={-65} stroke={sk.ink} strokeWidth={5} />
					<line x1={-176} y1={14} x2={176} y2={14} stroke={sk.ink} strokeWidth={5} />
					<line x1={-152} y1={96} x2={152} y2={96} stroke={sk.ink} strokeWidth={4} strokeDasharray="12 8" />

					{/* Heavy bronze cannons on both decks */}
					{[-120, -42, 42, 120].map((cx, i) => (
						<g key={i}>
							<rect x={cx - 20} y={-95} width={40} height={24} rx={5} fill={sk.accent} stroke={sk.ink} strokeWidth={2.5} />
							<rect x={cx - 20} y={-16} width={40} height={24} rx={5} fill={sk.accent} stroke={sk.ink} strokeWidth={2.5} />
						</g>
					))}

					{/* Open starboard lower gunport with water pouring in */}
					<circle cx={180} cy={-4} r={20} fill="#0b192c" stroke={sk.accent} strokeWidth={5} />
					{floodK > 0.05 ? (
						<path
							d="M 215 -14 Q 158 -4 115 70"
							fill="none"
							stroke="#4fc3ff"
							strokeWidth={12}
							strokeLinecap="round"
							strokeDasharray="18 10"
							opacity={Math.min(1, floodK * 2)}
						/>
					) : null}
				</g>

				{/* Sea surface line across the frame */}
				<path
					d={`M 60 ${waterY} Q ${280 + (waveShift % 80)} ${waterY - 14}, 540 ${waterY} T 1020 ${waterY}`}
					fill="none"
					stroke="#4fc3ff"
					strokeWidth={6}
				/>
				<rect x={60} y={waterY} width={960} height={280} fill="rgba(79,195,255,0.09)" />
				<text x={900} y={waterY + 44} textAnchor="middle" fontFamily={SERIF} fontStyle="italic" fontSize={34} fill="#4fc3ff">
					SEA LEVEL
				</text>
			</svg>

			<CalloutTag
				x={835}
				y={565}
				toX={708}
				toY={710}
				text="OPEN GUNPORTS"
				sub="Water floods lower deck"
				t={t}
				at={c1}
				skin={full.skin ?? 'blueprint'}
				accent
			/>

			<StampBadge text="SANK IN 30 MIN" x={540} y={985} rot={-6} t={t} at={c2} color={sk.accent} />
		</Paper>
	);
};
