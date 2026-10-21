import React from 'react';
import {Custom0} from './generated/Custom0';
import {Custom1} from './generated/Custom1';
import {Custom2} from './generated/Custom2';
import {Custom3} from './generated/Custom3';
import type {CustomFull, FullProps} from './types';

/** Dispatches a custom AI-coded motion graphic scene to its generated slot component (0..3). */
export const CustomScene: React.FC<FullProps<CustomFull>> = (props) => {
	switch (props.full.slot) {
		case 1:
			return <Custom1 {...props} />;
		case 2:
			return <Custom2 {...props} />;
		case 3:
			return <Custom3 {...props} />;
		default:
			return <Custom0 {...props} />;
	}
};
