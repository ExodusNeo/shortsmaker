// Full-screen motion graphic scenes (archival parchment, dark blueprint, dark crimson dossier, or dark HUD).
// make_shorts.py validates the AI's plan (clean_full), times every element to the spoken words (full_cues),
// codes any custom scene (code_custom_scenes), and sends one of these per scene.
// All times are absolute seconds, like the other graphics.

export type SkinName = 'parchment' | 'blueprint' | 'dossier' | 'hud';
export type FullBase = {
	type: 'board' | 'journey' | 'number' | 'document' | 'custom';
	seed: number;
	skin?: SkinName;
};
export type FullProps<T> = {full: T; t: number; start: number; end: number};

export type JourneyFull = FullBase & {
	type: 'journey';
	stops: {name: string; lat: number; lon: number; at: number}[];
	note?: string;
	noteAt?: number;
};

export type Icon =
	| 'person' | 'coin' | 'ship' | 'house' | 'train' | 'soldier' | 'animal' | 'day'
	| 'bird' | 'fish' | 'insect' | 'rat' | 'horse' | 'car' | 'plane' | 'gun' | 'barrel' | 'dollar';
export type NumberFull = FullBase & {
	type: 'number';
	value: number;
	show: string; // final text, e.g. "30,000" or "1.5 MILLION" (formatted in Python)
	label: string;
	icon: Icon;
	each: number; // what one figure stands for
	figures: number; // how many figures to draw (<= 60)
	image?: string; // the counted thing painted as an ink silhouette (job/fig<i>.png); else the built-in icon
	at: number;
	compare?: {a_label: string; a_value: number; b_label: string; b_value: number};
};

export type BoardFull = FullBase & {
	type: 'board';
	items: {image: string; aspect: number; label: string; at: number}[];
	links: [number, number][];
};

export type DocumentFull = FullBase & {
	type: 'document';
	kind: 'newspaper' | 'letter' | 'telegram' | 'form';
	key_line: string;
	date?: string;
	paper?: string; // masthead: only a real paper that covered the story
	image?: string; // a real scan of the document, when one was found
	aspect?: number;
	at: number; // the red underline starts
	lineEnd: number; // ... and is finished
};

export type CustomPhoto = {image: string; aspect: number; label: string; at: number};
export type CustomFull = FullBase & {
	type: 'custom';
	slot: number; // 0..3 -> generated/Custom<slot>.tsx
	kind: 'diagram' | 'collage' | 'flow' | 'clock';
	title?: string;
	cues: number[]; // spoken word timestamps (absolute seconds) in order
	photos?: CustomPhoto[];
};

export type AnyFull = JourneyFull | NumberFull | BoardFull | DocumentFull | CustomFull;
