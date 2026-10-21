import React from 'react';
import type {Icon} from './types';

// Small ink figures for the big-number scene, drawn on a 100x100 grid. Simple silhouettes read at 60-90 px.
const SHAPES: Record<Icon, React.ReactNode> = {
	person: (
		<>
			<circle cx={50} cy={22} r={14} />
			<path d="M27 92 C27 60 32 44 50 42 C68 44 73 60 73 92 Z" />
		</>
	),
	soldier: (
		<>
			<rect x={38} y={2} width={24} height={14} rx={2} />
			<rect x={34} y={15} width={32} height={4} />
			<circle cx={50} cy={27} r={11} />
			<path d="M31 94 C31 64 35 41 50 40 C65 41 69 64 69 94 Z" />
			<rect x={74} y={8} width={5} height={84} rx={2} />
		</>
	),
	coin: (
		<>
			<circle cx={50} cy={50} r={40} />
			<circle cx={50} cy={50} r={30} fill="none" stroke="#efe3c8" strokeWidth={4} />
			<path d="M44 34 h12 v32 h-12 z" fill="#efe3c8" />
		</>
	),
	ship: (
		<>
			<path d="M8 66 L92 66 L80 88 L20 88 Z" />
			<rect x={48} y={8} width={4} height={58} />
			<path d="M53 12 L84 58 L53 58 Z" />
			<path d="M47 20 L22 58 L47 58 Z" />
		</>
	),
	house: (
		<>
			<path d="M10 50 L50 12 L90 50 Z" />
			<path d="M20 48 L80 48 L80 92 L20 92 Z" />
			<rect x={43} y={64} width={14} height={28} fill="#efe3c8" />
			<rect x={26} y={58} width={11} height={11} fill="#efe3c8" />
			<rect x={63} y={58} width={11} height={11} fill="#efe3c8" />
		</>
	),
	train: (
		<>
			<rect x={10} y={40} width={56} height={32} rx={4} />
			<rect x={58} y={24} width={32} height={48} rx={3} />
			<rect x={18} y={20} width={11} height={22} />
			<rect x={64} y={30} width={18} height={14} fill="#efe3c8" />
			<circle cx={24} cy={80} r={10} />
			<circle cx={50} cy={80} r={10} />
			<circle cx={76} cy={80} r={10} />
		</>
	),
	animal: (
		<>
			<path d="M18 46 C20 34 34 30 50 32 L70 32 C74 22 82 16 90 18 L92 30 L84 36 L80 52 L80 88 L72 88 L70 60 L36 60 L32 88 L24 88 L22 60 C14 56 12 50 18 46 Z" />
			<path d="M18 46 L6 58 L10 62 L22 52 Z" />
		</>
	),
	day: (
		<>
			<rect x={12} y={18} width={76} height={72} rx={6} />
			<rect x={12} y={18} width={76} height={18} rx={6} fill="#7a1d12" />
			<rect x={28} y={8} width={6} height={18} rx={3} />
			<rect x={66} y={8} width={6} height={18} rx={3} />
			<path d="M24 46 h52 v34 h-52 z" fill="#efe3c8" />
			<path d="M38 50 L50 50 L42 76 L36 76 L43 56 L38 56 Z" />
		</>
	),
	// Added 2026-10-18 (Emu War review: 20,000 emus were drawn as generic four-legged "animal" shapes).
	bird: (
		<>
			<ellipse cx={44} cy={54} rx={28} ry={17} />
			<path d="M62 48 C68 38 68 26 72 16 L80 17 C77 28 76 42 70 56 Z" />
			<circle cx={77} cy={15} r={7} />
			<path d="M83 12 L96 16 L83 19 Z" />
			<path d="M18 50 L4 40 L8 52 L18 58 Z" />
			<rect x={35} y={66} width={5} height={30} rx={2} />
			<rect x={50} y={66} width={5} height={30} rx={2} />
		</>
	),
	fish: (
		<>
			<path d="M8 50 C26 24 62 24 78 50 C62 76 26 76 8 50 Z" />
			<path d="M76 50 L96 32 L91 50 L96 68 Z" />
			<path d="M40 30 L54 16 L58 32 Z" />
		</>
	),
	insect: (
		<>
			<ellipse cx={50} cy={62} rx={14} ry={24} />
			<ellipse cx={50} cy={34} rx={10} ry={9} />
			<circle cx={50} cy={20} r={8} />
			{[38, 52, 66].flatMap((y) => [
				<rect key={`l${y}`} x={14} y={y} width={24} height={4} rx={2} transform={`rotate(${y < 50 ? -20 : 20} 38 ${y + 2})`} />,
				<rect key={`r${y}`} x={62} y={y} width={24} height={4} rx={2} transform={`rotate(${y < 50 ? 20 : -20} 62 ${y + 2})`} />,
			])}
			<rect x={40} y={4} width={3} height={14} rx={1.5} transform="rotate(-25 42 12)" />
			<rect x={57} y={4} width={3} height={14} rx={1.5} transform="rotate(25 58 12)" />
		</>
	),
	rat: (
		<>
			<ellipse cx={46} cy={60} rx={28} ry={16} />
			<path d="M70 52 L92 62 L70 70 Z" />
			<circle cx={70} cy={48} r={7} />
			<path d="M20 62 C8 66 4 78 12 86 C10 76 14 70 22 68 Z" />
			<rect x={34} y={72} width={5} height={12} rx={2} />
			<rect x={56} y={72} width={5} height={12} rx={2} />
		</>
	),
	horse: (
		<>
			<path d="M20 44 C22 34 34 32 48 34 L66 34 L74 18 L88 22 L92 34 L84 36 L80 50 L78 90 L70 90 L68 60 L36 60 L32 90 L24 90 L22 58 C14 56 12 50 20 44 Z" />
			<path d="M20 46 L6 64 L10 66 L22 52 Z" />
			<path d="M74 18 L70 8 L78 14 Z" />
		</>
	),
	car: (
		<>
			<path d="M6 66 L10 50 L26 46 L36 30 L68 30 L80 46 L94 50 L96 66 Z" />
			<circle cx={28} cy={68} r={11} />
			<circle cx={74} cy={68} r={11} />
		</>
	),
	plane: (
		<>
			<path d="M6 52 C6 46 14 44 24 44 L84 44 C92 44 96 48 96 50 C96 52 92 56 84 56 L24 56 C14 56 6 56 6 52 Z" />
			<path d="M40 46 L62 46 L46 14 L36 14 Z" />
			<path d="M40 54 L62 54 L46 86 L36 86 Z" />
			<path d="M10 46 L22 46 L14 28 L8 28 Z" />
		</>
	),
	gun: (
		<>
			<rect x={30} y={40} width={66} height={7} rx={2} />
			<path d="M4 44 L34 38 L48 38 L48 52 L36 54 L18 64 L6 62 Z" />
			<path d="M44 52 L54 52 L50 66 L42 66 Z" />
			<rect x={58} y={47} width={18} height={6} rx={2} />
		</>
	),
	barrel: (
		<>
			<path d="M26 10 L74 10 C80 20 80 30 79 32 L21 32 C20 30 20 20 26 10 Z" />
			<path d="M20 37 L80 37 C82 46 82 54 80 63 L20 63 C18 54 18 46 20 37 Z" />
			<path d="M21 68 L79 68 C80 70 80 80 74 90 L26 90 C20 80 20 70 21 68 Z" />
		</>
	),
	dollar: (
		<>
			<path d="M50 18 C40 18 36 10 40 6 L60 6 C64 10 60 18 50 18 Z" />
			<path d="M50 20 C24 24 12 50 14 70 C16 90 32 96 50 96 C68 96 84 90 86 70 C88 50 76 24 50 20 Z" />
			<text x={50} y={78} textAnchor="middle" fontSize={40} fontWeight={900} fontFamily="Georgia, serif" fill="#efe3c8">$</text>
		</>
	),
};

export const InkIcon: React.FC<{icon: Icon; size: number; color: string}> = ({icon, size, color}) => (
	<svg width={size} height={size} viewBox="0 0 100 100" fill={color} style={{display: 'block'}}>
		{SHAPES[icon] ?? SHAPES.person}
	</svg>
);
