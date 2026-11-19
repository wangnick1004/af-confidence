import {Composition} from 'remotion';
import {HbSOpening, HBS_DURATION} from './scenes/HbSOpening';
import {HbSOpeningEditable, HBS_EDITABLE_DURATION} from './scenes/HbSOpeningEditable';

export const Root: React.FC = () => (
  <>
    {/* 可編輯版（每個元素一條軌道） */}
    <Composition
      id="HbSOpeningEditable"
      component={HbSOpeningEditable}
      durationInFrames={HBS_EDITABLE_DURATION}
      fps={30}
      width={1920}
      height={1080}
    />
    {/* 第一版試樣（保留做比較） */}
    <Composition
      id="HbSOpening"
      component={HbSOpening}
      durationInFrames={HBS_DURATION}
      fps={30}
      width={1920}
      height={1080}
    />
  </>
);
