import {BigNumber} from './BigNumber';
import {Board} from './Board';
import {CustomScene} from './CustomScene';
import {DocumentScene} from './Document';
import {Journey} from './Journey';
import {Model3D} from './Model3D';
import type {AnyFull, FullProps} from './types';

/** One full-screen motion graphic scene, drawn instead of the scene's picture. */
export const FullScene: React.FC<FullProps<AnyFull>> = ({full, t, start, end}) => {
	switch (full.type) {
		case 'board':
			return <Board full={full} t={t} start={start} end={end} />;
		case 'document':
			return <DocumentScene full={full} t={t} start={start} end={end} />;
		case 'number':
			return <BigNumber full={full} t={t} start={start} end={end} />;
		case 'journey':
			return <Journey full={full} t={t} start={start} end={end} />;
		case 'custom':
			return <CustomScene full={full} t={t} start={start} end={end} />;
		case 'model':
			return <Model3D full={full} t={t} start={start} end={end} />;
	}
};
