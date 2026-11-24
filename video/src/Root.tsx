import {Composition, Folder} from 'remotion';
import {HbSOpening, HBS_DURATION} from './scenes/HbSOpening';
import {HbSOpeningEditable, HBS_EDITABLE_DURATION} from './scenes/HbSOpeningEditable';
import {S1Question, S1QUESTION_DURATION} from './scenes/S1Question';
import {S2Tool, S2TOOL_DURATION} from './scenes/S2Tool';
import {S4Plddt, S4PLDDT_DURATION} from './scenes/S4Plddt';
import {S4ToolOutput, S4TOOLOUTPUT_DURATION} from './scenes/S4ToolOutput';
import {S5Limits, S5LIMITS_DURATION} from './scenes/S5Limits';
import {S5ToolLimit, S5TOOLLIMIT_DURATION} from './scenes/S5ToolLimit';
import {S6Outro, S6OUTRO_DURATION} from './scenes/S6Outro';

const common = {fps: 30, width: 1920, height: 1080} as const;

// 依影片順序排列；名稱對應 docs/video_script.md 第四節的設計腳本
export const Root: React.FC = () => (
  <>
    <Composition id="S1Question" component={S1Question} durationInFrames={S1QUESTION_DURATION} {...common} />
    <Composition id="S2Tool" component={S2Tool} durationInFrames={S2TOOL_DURATION} {...common} />
    <Composition
      id="HbSOpeningEditable"
      component={HbSOpeningEditable}
      durationInFrames={HBS_EDITABLE_DURATION}
      {...common}
    />
    <Composition id="S4Plddt" component={S4Plddt} durationInFrames={S4PLDDT_DURATION} {...common} />
    <Composition
      id="S4ToolOutput"
      component={S4ToolOutput}
      durationInFrames={S4TOOLOUTPUT_DURATION}
      {...common}
    />
    <Composition id="S5Limits" component={S5Limits} durationInFrames={S5LIMITS_DURATION} {...common} />
    <Composition
      id="S5ToolLimit"
      component={S5ToolLimit}
      durationInFrames={S5TOOLLIMIT_DURATION}
      {...common}
    />
    <Composition id="S6Outro" component={S6Outro} durationInFrames={S6OUTRO_DURATION} {...common} />
    <Folder name="舊版試樣">
      <Composition id="HbSOpening" component={HbSOpening} durationInFrames={HBS_DURATION} {...common} />
    </Folder>
  </>
);
