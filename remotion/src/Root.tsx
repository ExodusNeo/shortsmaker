import {CalculateMetadataFunction, Composition} from 'remotion';
import {Opener3D, StageProps, calculateOpener3D} from './Opener3D';
import {Short, ShortProps} from './Short';

// shortsmaker/remotion_render.py (render_remotion) writes the props (scene timings, images, graphics, words); duration and fps come from them.
const calculateMetadata: CalculateMetadataFunction<ShortProps> = ({props}) => ({
	fps: props.fps,
	durationInFrames: Math.max(1, Math.ceil(props.total * props.fps)),
});

export const Root: React.FC = () => (
	<>
	<Composition
		id="Short"
		component={Short}
		width={1080}
		height={1920}
		fps={30}
		durationInFrames={300}
		defaultProps={{fps: 30, total: 10, xfade: 0.3, scenes: [], flashes: [], words: [], cta: 7, ctaLine: 'for more strange history'}}
		calculateMetadata={calculateMetadata}
	/>
	{/* the 3D opener (shortsmaker/opener3d.py writes the stage props) */}
	<Composition id="Opener3D" component={Opener3D} width={1080} height={1920} fps={30} durationInFrames={120}
		defaultProps={{fps: 30, seconds: 4, dir: 'opener3d/job', place: 'room', mood: 'interior', props: [], cutouts: [], shots: [], effects: []} as StageProps}
		calculateMetadata={calculateOpener3D} />
	</>
);
