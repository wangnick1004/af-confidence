import {Composition} from 'remotion';
import {HbSOpening, HBS_DURATION} from './scenes/HbSOpening';

export const Root: React.FC = () => (
  <Composition
    id="HbSOpening"
    component={HbSOpening}
    durationInFrames={HBS_DURATION}
    fps={30}
    width={1920}
    height={1080}
  />
);
