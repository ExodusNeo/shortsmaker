import React from 'react';
import {
	CustomFull,
	Easing,
	FlowArrow,
	FlowCard,
	FullProps,
	Paper,
	StampBadge,
	TitleBanner,
	appear,
	clamp,
	cueAt,
	focusCam,
	interpolate,
	skinOf,
} from '../toolkit';

/** Custom 2 (Cause-and-effect flow chain, hud skin): Step 1 -> Step 2 -> Twist/Payoff with animated
 * connectors and gauges, staying cleanly above y = 1080. */
export const Custom2: React.FC<FullProps<CustomFull>> = ({full, t, start, end}) => {
	const sk = skinOf(full.skin ?? 'hud');
	const c0 = cueAt(full, 0, start, end, 3);
	const c1 = cueAt(full, 1, start, end, 3);
	const c2 = cueAt(full, 2, start, end, 3);

	const fy = interpolate(t, [start, c1, c2 + 0.4], [520, 590, 625], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const fScale = interpolate(t, [start, c2 + 0.4], [1.06, 1.0], clamp);
	const meter = appear(t, c1, 0.7);

	return (
		<Paper t={t} start={start} seed={full.seed} cam={focusCam(540, fy, fScale)} skin={full.skin ?? 'hud'}>
			<TitleBanner title={full.title || 'THE RAINMAKER LOOPHOLE (1916)'} sub="CAUSE -> DISASTER -> CATCH-22" t={t} at={start + 0.05} skin={full.skin ?? 'hud'} />

			<FlowCard
				step="STEP 01 · THE DEAL"
				title="$10,000 IF IT RAINS"
				sub="Handshake deal with San Diego Council"
				x={540}
				y={365}
				w={800}
				h={155}
				t={t}
				at={c0}
				skin={full.skin ?? 'hud'}
			/>

			<FlowArrow x1={540} y1={446} x2={540} y2={535} t={t} at={c1 - 0.15} color={sk.accent} />

			<FlowCard
				step="STEP 02 · THE FLOOD"
				title="28 INCHES OF RAIN"
				sub="Dams burst · $3.5M in city damages"
				x={540}
				y={620}
				w={800}
				h={160}
				t={t}
				at={c1}
				skin={full.skin ?? 'hud'}
				highlight
			/>

			{/* Animated flood-damage bar inside the flow */}
			{meter > 0 ? (
				<div style={{position: 'absolute', left: 190, top: 715, width: 700, height: 18, background: 'rgba(255,255,255,0.1)', borderRadius: 9, overflow: 'hidden'}}>
					<div style={{width: `${meter * 100}%`, height: '100%', background: `linear-gradient(90deg, ${sk.accent}, #ff5a5f)`}} />
				</div>
			) : null}

			<FlowArrow x1={380} y1={742} x2={310} y2={825} curve={-20} t={t} at={c2 - 0.15} color={sk.accent} />
			<FlowArrow x1={700} y1={742} x2={770} y2={825} curve={20} t={t} at={c2 - 0.15} color="#ff5a5f" />

			<FlowCard
				step="OPTION A"
				title="CLAIM THE $10K"
				sub="Pay $3.5M in lawsuits"
				x={300}
				y={915}
				w={410}
				h={155}
				t={t}
				at={c2}
				skin={full.skin ?? 'hud'}
			/>

			<FlowCard
				step="OPTION B"
				title="ACT OF GOD"
				sub="Walk away with $0"
				x={780}
				y={915}
				w={410}
				h={155}
				t={t}
				at={c2 + 0.15}
				skin={full.skin ?? 'hud'}
				highlight
			/>

			<StampBadge text="PAID $0" x={780} y={915} rot={-12} t={t} at={c2 + 0.5} color="#ff5a5f" />
		</Paper>
	);
};
