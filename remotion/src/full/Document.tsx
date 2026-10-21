import {Easing, Img, interpolate, spring, staticFile, useVideoConfig} from 'remotion';
import {INK, Paper, RED, SERIF, TYPE, rng} from './Paper';
import type {DocumentFull, FullProps} from './types';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const SHEET_W = 900;
const CX = 540;
const SHEET_TOP = 260;

const wrapText = (text: string, maxChars: number) =>
	text.split(' ').reduce<string[]>((lines, w) => {
		const last = lines[lines.length - 1];
		if (last !== undefined && (last + ' ' + w).length <= maxChars) lines[lines.length - 1] = last + ' ' + w;
		else lines.push(w);
		return lines;
	}, []);

/** Grey bars where body text would be: the page looks full, but nothing invented can be read. */
const Filler: React.FC<{seed: number; rows: number; width: number; gap?: number; height?: number}> = ({seed, rows, width, gap = 26, height = 10}) => {
	const r = rng(seed);
	return (
		<div style={{filter: 'blur(1.2px)'}}>
			{Array.from({length: rows}, (_, i) => (
				<div
					key={i}
					style={{height, marginBottom: gap - height, borderRadius: 4, background: 'rgba(44,31,14,0.28)', width: i % 6 === 5 ? width * (0.3 + r() * 0.3) : width * (0.86 + r() * 0.14)}}
				/>
			))}
		</div>
	);
};

/** A full-screen old document: the camera pushes in on the one line that matters while it is
 * underlined in red ink, as it is spoken. Real scans are shown as they are, with the key line typed on a
 * slip clipped to them (we never claim where on the scan the words are). */
export const DocumentScene: React.FC<FullProps<DocumentFull>> = ({full, t, start, end}) => {
	const {fps} = useVideoConfig();
	const r = rng(full.seed);
	const rot = (r() - 0.5) * 4;
	const enter = spring({frame: (t - start) * fps, fps, config: {damping: 15, stiffness: 120}});
	const words = full.key_line.split(' ').length;
	const fs = words <= 6 ? 78 : words <= 10 ? 66 : 56;
	const typed = full.kind === 'telegram' || full.kind === 'form' || !!full.image;
	const cw = typed ? 0.62 : full.kind === 'newspaper' ? 0.44 : 0.47; // average letter width per font size
	const lines = wrapText(typed ? full.key_line.toUpperCase() : full.key_line, Math.floor(760 / (fs * cw)));
	const lh = fs * 1.22;
	const at = Math.max(start + 0.5, Math.min(full.at, end - 1.0));
	const lineEnd = Math.max(at + 0.4, Math.min(full.lineEnd, end - 0.3));

	// Layout per kind: where the key line block sits on the sheet (y from the sheet top) and the sheet height.
	const keyTop = full.image ? 0 : full.kind === 'newspaper' ? (full.paper ? 250 : 140) : full.kind === 'telegram' ? 250 : full.kind === 'form' ? 330 : 360;
	const sheetH = full.kind === 'telegram' ? Math.max(720, keyTop + lines.length * lh + 260) : 1220;
	const scanH = full.image ? Math.min(1250, SHEET_W / (full.aspect || 0.8)) : 0;
	const keyY = full.image ? SHEET_TOP + scanH * 0.58 + 40 + (lines.length * lh) / 2 : SHEET_TOP + keyTop + (lines.length * lh) / 2;
	const push = interpolate(t, [start + 0.3, lineEnd + 0.3], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const cam = {x: CX, y: interpolate(push, [0, 1], [SHEET_TOP + sheetH / 2 + 120, keyY + 260]), scale: interpolate(push, [0, 1], [0.98, full.kind === 'letter' && !full.image ? 1.18 : 1.3])};

	const keyBlock = (
		<div style={{position: 'relative', textAlign: full.kind === 'letter' ? 'left' : 'center'}}>
			{lines.map((l, i) => {
				const per = (lineEnd - at) / lines.length;
				const k = interpolate(t, [at + i * per, at + (i + 1) * per], [0, 1], {...clamp, easing: Easing.inOut(Easing.quad)});
				const w = Math.min(780, l.length * fs * cw);
				return (
					<div key={i} style={{position: 'relative', height: lh}}>
						<span
							style={{
								fontFamily: typed ? TYPE : SERIF, fontSize: fs, lineHeight: `${lh}px`, color: INK, whiteSpace: 'nowrap',
								fontStyle: full.kind === 'letter' ? 'italic' : 'normal', fontWeight: full.kind === 'newspaper' ? 700 : 400,
								...(typed ? {background: '#f7efdc', padding: '0 14px', boxShadow: '0 3px 6px rgba(0,0,0,0.18)'} : {}),
							}}
						>
							{l}
						</span>
						<svg
							width={w + 40} height={30}
							style={{position: 'absolute', left: full.kind === 'letter' ? -10 : (780 - w) / 2 - 10, top: lh - 16, overflow: 'visible'}}
						>
							<path
								d={`M6 ${14 + r() * 6} C ${w * 0.3} ${8 + r() * 10}, ${w * 0.6} ${18 + r() * 8}, ${w + 30} ${10 + r() * 8}`}
								fill="none" stroke={RED} strokeWidth={7} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - k} opacity={0.9}
							/>
						</svg>
					</div>
				);
			})}
		</div>
	);

	return (
		<Paper t={t} start={start} seed={full.seed} cam={cam} skin={full.skin}>
			<div
				style={{
					position: 'absolute', left: CX - SHEET_W / 2, top: SHEET_TOP, width: SHEET_W,
					transform: `translateY(${260 * (1 - enter)}px) rotate(${rot + 4 * (1 - enter)}deg)`, opacity: Math.min(1, enter * 3),
				}}
			>
				{full.image ? (
					<div style={{position: 'relative'}}>
						<Img src={staticFile(full.image)} style={{display: 'block', width: SHEET_W, maxHeight: 1250, objectFit: 'contain', filter: 'sepia(0.3)', boxShadow: '0 30px 60px rgba(0,0,0,0.45)'}} />
						<div style={{position: 'absolute', left: 60, right: 60, top: '58%', padding: '30px 10px 34px', background: '#efe3c8', boxShadow: '0 12px 30px rgba(0,0,0,0.5)', transform: `rotate(${-rot * 1.5}deg)`}}>
							<div style={{width: 780, margin: '0 auto'}}>{keyBlock}</div>
						</div>
					</div>
				) : (
					<div style={{position: 'relative', height: sheetH, background: '#f1e6cc', boxShadow: '0 30px 60px rgba(0,0,0,0.45)', padding: '60px 60px', boxSizing: 'border-box'}}>
						{full.kind === 'newspaper' ? (
							<>
								{full.paper ? (
									<div style={{fontFamily: SERIF, fontWeight: 800, fontSize: Math.min(96, Math.floor(1300 / full.paper.length)), textAlign: 'center', color: INK, letterSpacing: 2, lineHeight: 1}}>
										{full.paper.toUpperCase()}
									</div>
								) : null}
								<div style={{borderTop: `5px solid ${INK}`, borderBottom: `2px solid ${INK}`, height: 8, margin: full.paper ? '22px 0 10px' : '0 0 10px'}} />
								<div style={{fontFamily: SERIF, fontSize: 30, letterSpacing: 6, textAlign: 'center', color: INK, height: 40}}>{full.date ?? ''}</div>
								<div style={{position: 'absolute', left: 60, right: 60, top: keyTop}}>{keyBlock}</div>
								<div style={{position: 'absolute', left: 60, right: 60, top: keyTop + lines.length * lh + 50, display: 'flex', gap: 34}}>
									{[0, 1, 2].map((c) => (
										<Filler key={c} seed={full.seed * 7 + c} rows={Math.floor((sheetH - keyTop - lines.length * lh - 130) / 26)} width={(780 - 68) / 3} />
									))}
								</div>
							</>
						) : full.kind === 'telegram' ? (
							<>
								<div style={{display: 'flex', alignItems: 'center', gap: 20, borderBottom: `3px solid ${RED}`, paddingBottom: 14}}>
									<div style={{width: 18, height: 50, background: RED}} />
									<div style={{fontFamily: TYPE, fontSize: 56, letterSpacing: 18, color: RED}}>TELEGRAM</div>
								</div>
								<div style={{marginTop: 26, display: 'flex', justifyContent: 'space-between', fontFamily: TYPE, fontSize: 30, color: INK, opacity: 0.8}}>
									<span>No. ____</span>
									<span>{full.date ?? ''}</span>
								</div>
								<div style={{position: 'absolute', left: 60, right: 60, top: keyTop}}>{keyBlock}</div>
								<div style={{position: 'absolute', left: 60, right: 60, bottom: 60}}>
									<Filler seed={full.seed * 3} rows={3} width={780} gap={34} height={3} />
								</div>
							</>
						) : (
							<>
								{full.kind === 'form' ? (
									<>
										<div style={{border: `3px double ${INK}`, height: 120, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
											<div style={{width: 520}}>
												<Filler seed={full.seed * 5} rows={2} width={520} gap={34} height={12} />
											</div>
										</div>
										<div style={{marginTop: 30}}>
											<Filler seed={full.seed * 9} rows={3} width={780} gap={40} height={3} />
										</div>
									</>
								) : (
									<>
										<div style={{textAlign: 'right', fontFamily: SERIF, fontStyle: 'italic', fontSize: 40, color: INK, height: 60}}>{full.date ?? ''}</div>
										<div style={{marginTop: 30}}>
											<Filler seed={full.seed * 5} rows={7} width={780} gap={40} height={6} />
										</div>
									</>
								)}
								<div style={{position: 'absolute', left: 60, right: 60, top: keyTop}}>{keyBlock}</div>
								<div style={{position: 'absolute', left: 60, right: 60, top: keyTop + lines.length * lh + 70}}>
									<Filler seed={full.seed * 11} rows={full.kind === 'form' ? 6 : 9} width={780} gap={40} height={full.kind === 'form' ? 3 : 6} />
								</div>
							</>
						)}
					</div>
				)}
			</div>
		</Paper>
	);
};
