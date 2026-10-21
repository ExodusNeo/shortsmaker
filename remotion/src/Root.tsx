import {CalculateMetadataFunction, Composition} from 'remotion';
import {Short, ShortProps} from './Short';

// make_shorts.py writes the props (scene timings, images, graphics, words); duration and fps come from them.
const calculateMetadata: CalculateMetadataFunction<ShortProps> = ({props}) => ({
	fps: props.fps,
	durationInFrames: Math.max(1, Math.ceil(props.total * props.fps)),
});

export const Root: React.FC = () => (
	<Composition
		id="Short"
		component={Short}
		width={1080}
		height={1920}
		fps={30}
		durationInFrames={300}
		defaultProps={{fps: 30, total: 10, xfade: 0.3, hook: 'PREVIEW', scenes: [], flashes: [], words: [], cta: 7, ctaLine: 'for more strange history'}}
		calculateMetadata={calculateMetadata}
	/>
);
