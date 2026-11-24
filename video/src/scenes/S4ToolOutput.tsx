// 段 4｜工具輸出怎麼讀（設計腳本鏡頭 4-4）
// 事實來源：工具對 HBB E6V 的實際輸出（docs/video_script.md 3C）
//
// 結構說明：每個畫面元素是一個獨立的 <Sequence>（時間軸上一條軌道）；
// 元素裡的關鍵影格從元素開始算起；軌道越下面的畫在越上層。詳見 video/README.md。
import {
  AbsoluteFill,
  Easing,
  Img,
  Interactive,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
} from 'remotion';
import '../theme';

export const S4TOOLOUTPUT_DURATION = 300; // 10.0 秒 @ 30fps

// 終端機：工具輸出
const El01: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="終端機視窗"
      style={{
        position: 'absolute',
        left: 160,
        top: 300,
        width: 1600,
        height: 230,
        borderRadius: 20,
        backgroundColor: '#1E2230',
        opacity: interpolate(frame, [0, 12], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
        }),
      }}
    >
      <Interactive.Div
        name="第 1 行"
        style={{
          position: 'absolute',
          left: 50,
          top: 60,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 38,
          color: '#E6E9EF',
          whiteSpace: 'pre',
          fontVariantLigatures: 'none',
        }}
      >
        XX E6V: model has P at 6, not E
      </Interactive.Div>
      <Interactive.Div
        name="第 2 行"
        style={{
          position: 'absolute',
          left: 50,
          top: 130,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 38,
          color: '#E6E9EF',
          whiteSpace: 'pre',
          fontVariantLigatures: 'none',
        }}
      >
        {'     -> [medium] annotated_offset: +1: E7V matches …'}
      </Interactive.Div>
    </Interactive.Div>
  );
};

// 聚焦：XX
const El02: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="聚焦框"
      style={{
        position: 'absolute',
        left: 204,
        top: 358,
        width: 58,
        height: 58,
        borderRadius: 8,
        backgroundColor: 'transparent',
        borderWidth: 4,
        borderStyle: 'solid',
        borderColor: '#FFDB13',
        opacity: interpolate(frame, [0, 12, 258, 270], [0, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
        scale: interpolate(frame, [0, 12], ['1.08', '1'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          output: 'perceptual-scale',
          outputType: 'scale',
        }),
      }}
    />
  );
};

// 說明：XX
const El03: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="說明文字"
      style={{
        position: 'absolute',
        left: 210,
        top: 600,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 42,
        fontWeight: 700,
        color: '#1F2430',
        textAlign: 'left',
        opacity: interpolate(frame, [0, 12], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
        }),
        translate: interpolate(frame, [0, 12], ['0px 16px', '0px 0px'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          outputType: 'translate',
        }),
      }}
    >
      <Interactive.Span name="文字片段 1" style={{color: '#D9483B', whiteSpace: 'pre'}}>
        XX
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        ：對不上（OK：對得上）
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 聚焦：E7V
const El04: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="聚焦框"
      style={{
        position: 'absolute',
        left: 1093,
        top: 428,
        width: 80,
        height: 58,
        borderRadius: 8,
        backgroundColor: 'transparent',
        borderWidth: 4,
        borderStyle: 'solid',
        borderColor: '#FFDB13',
        opacity: interpolate(frame, [0, 12, 188, 200], [0, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
        scale: interpolate(frame, [0, 12], ['1.08', '1'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          output: 'perceptual-scale',
          outputType: 'scale',
        }),
      }}
    />
  );
};

// 說明：E7V
const El05: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="說明文字"
      style={{
        position: 'absolute',
        left: 1000,
        top: 600,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 42,
        fontWeight: 700,
        color: '#1F2430',
        textAlign: 'left',
        opacity: interpolate(frame, [0, 12], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
        }),
        translate: interpolate(frame, [0, 12], ['0px 16px', '0px 0px'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          outputType: 'translate',
        }),
      }}
    >
      <Interactive.Span name="文字片段 1" style={{color: '#2F6FEB', whiteSpace: 'pre'}}>
        {'->'}
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        {' '}
        後面：建議的位置
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 聚焦：[medium]
const El06: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="聚焦框"
      style={{
        position: 'absolute',
        left: 386,
        top: 428,
        width: 194,
        height: 58,
        borderRadius: 8,
        backgroundColor: 'transparent',
        borderWidth: 4,
        borderStyle: 'solid',
        borderColor: '#FFDB13',
        opacity: interpolate(frame, [0, 12, 118, 130], [0, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
        scale: interpolate(frame, [0, 12], ['1.08', '1'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          output: 'perceptual-scale',
          outputType: 'scale',
        }),
      }}
    />
  );
};

// 說明：[medium]
const El07: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="說明文字"
      style={{
        position: 'absolute',
        left: 330,
        top: 700,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 42,
        fontWeight: 700,
        color: '#1F2430',
        textAlign: 'left',
        opacity: interpolate(frame, [0, 12], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
        }),
        translate: interpolate(frame, [0, 12], ['0px 16px', '0px 0px'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          outputType: 'translate',
        }),
      }}
    >
      <Interactive.Span name="文字片段 1" style={{color: '#2F6FEB', whiteSpace: 'pre'}}>
        [medium]
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        ：這個建議有多可信
      </Interactive.Span>
    </Interactive.Div>
  );
};

export const S4ToolOutput: React.FC = () => {
  return (
    <AbsoluteFill>
      <Interactive.Div
        name="背景"
        from={0}
        durationInFrames={300}
        style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, backgroundColor: '#F6F4EF'}}
      />
      <Sequence name="終端機：工具輸出" from={0} durationInFrames={300}>
        <El01 />
      </Sequence>
      <Sequence name="聚焦：XX" from={30} durationInFrames={270}>
        <El02 />
      </Sequence>
      <Sequence name="說明：XX" from={30} durationInFrames={270}>
        <El03 />
      </Sequence>
      <Sequence name="聚焦：E7V" from={100} durationInFrames={200}>
        <El04 />
      </Sequence>
      <Sequence name="說明：E7V" from={100} durationInFrames={200}>
        <El05 />
      </Sequence>
      <Sequence name="聚焦：[medium]" from={170} durationInFrames={130}>
        <El06 />
      </Sequence>
      <Sequence name="說明：[medium]" from={170} durationInFrames={130}>
        <El07 />
      </Sequence>
    </AbsoluteFill>
  );
};
