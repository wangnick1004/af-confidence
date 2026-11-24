// 段 5｜工具本身的限制（設計腳本鏡頭 5-4）
// 事實來源：F8（APP：Aβ 第 1 個 = APP770 第 672 個；D23N 正確位置 D694N；第 23 個碰巧也是 D）、F12（約 7～9%）
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

export const S5TOOLLIMIT_DURATION = 570; // 19.0 秒 @ 30fps

// 標題：工具也有限制
const El01: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="標題文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 110,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 56,
        fontWeight: 700,
        color: '#1F2430',
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
      我們的工具也有限制
    </Interactive.Div>
  );
};

// 文字：D23N
const El02: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 220,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 44,
        fontWeight: 400,
        color: '#1F2430',
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
      <Interactive.Span name="文字片段 1" style={{color: '#8A8F99', whiteSpace: 'pre'}}>
        Aβ 編號的{' '}
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        D23N
      </Interactive.Span>
      <Interactive.Span name="文字片段 3" style={{color: '#8A8F99', whiteSpace: 'pre'}}>
        （Iowa 突變）
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 方塊：第 23 個
const El03: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      <Interactive.Div
        name="D 方塊"
        style={{
          position: 'absolute',
          left: 560,
          top: 330,
          width: 180,
          height: 180,
          borderRadius: 18,
          backgroundColor: '#FFFFFF',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 96,
          fontWeight: 700,
          color: '#1F2430',
          borderWidth: 6,
          borderStyle: 'solid',
          borderColor: '#D9483B',
          opacity: interpolate(frame, [0, 15], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          scale: interpolate(frame, [0, 15], ['0.9', '1'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            output: 'perceptual-scale',
            outputType: 'scale',
          }),
          fontVariantLigatures: 'none',
        }}
      >
        D
      </Interactive.Div>
      <Interactive.Div
        name="位置文字"
        style={{
          position: 'absolute',
          left: 450,
          top: 540,
          fontFamily: "'Noto Sans TC', sans-serif",
          fontSize: 36,
          fontWeight: 700,
          color: '#1F2430',
          textAlign: 'center',
          width: 400,
          whiteSpace: 'pre',
          lineHeight: 1.4,
          opacity: interpolate(frame, [0, 15], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      >
        <Interactive.Span name="文字片段 1" style={{color: '#1F2430', whiteSpace: 'pre'}}>
          {'APP 第 23 個\n'}
        </Interactive.Span>
        <Interactive.Span name="文字片段 2" style={{color: '#D9483B', whiteSpace: 'pre'}}>
          照文獻的數字
        </Interactive.Span>
      </Interactive.Div>
    </>
  );
};

// 方塊：第 694 個
const El04: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      <Interactive.Div
        name="D 方塊"
        style={{
          position: 'absolute',
          left: 1180,
          top: 330,
          width: 180,
          height: 180,
          borderRadius: 18,
          backgroundColor: '#FFFFFF',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 96,
          fontWeight: 700,
          color: '#1F2430',
          borderWidth: 6,
          borderStyle: 'solid',
          borderColor: '#1E9E6A',
          opacity: interpolate(frame, [0, 15], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          scale: interpolate(frame, [0, 15], ['0.9', '1'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            output: 'perceptual-scale',
            outputType: 'scale',
          }),
          fontVariantLigatures: 'none',
        }}
      >
        D
      </Interactive.Div>
      <Interactive.Div
        name="位置文字"
        style={{
          position: 'absolute',
          left: 1070,
          top: 540,
          fontFamily: "'Noto Sans TC', sans-serif",
          fontSize: 36,
          fontWeight: 700,
          color: '#1F2430',
          textAlign: 'center',
          width: 400,
          whiteSpace: 'pre',
          lineHeight: 1.4,
          opacity: interpolate(frame, [0, 15], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      >
        <Interactive.Span name="文字片段 1" style={{color: '#1F2430', whiteSpace: 'pre'}}>
          {'APP 第 694 個\n'}
        </Interactive.Span>
        <Interactive.Span name="文字片段 2" style={{color: '#1E9E6A', whiteSpace: 'pre'}}>
          正確位置
        </Interactive.Span>
      </Interactive.Div>
    </>
  );
};

// 等號
const El05: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="等號"
      style={{
        position: 'absolute',
        left: 860,
        top: 345,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 110,
        fontWeight: 400,
        color: '#1F2430',
        textAlign: 'center',
        width: 200,
        opacity: interpolate(frame, [0, 15], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
        }),
      }}
    >
      ＝
    </Interactive.Div>
  );
};

// 說明：碰巧對上
const El06: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="說明文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 690,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 46,
        fontWeight: 700,
        color: '#1F2430',
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
      錯的位置剛好也是 D → 偵測不到
    </Interactive.Div>
  );
};

// 說明：約 7–9%
const El07: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="說明文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 770,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 40,
        fontWeight: 400,
        color: '#8A8F99',
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
      單一突變約 7–9% 會碰巧對上
    </Interactive.Div>
  );
};

// 結論：線索，不是結論
const El08: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="結論文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 880,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 56,
        fontWeight: 700,
        color: '#1F2430',
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
      <Interactive.Span name="文字片段 1" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        工具的建議是
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#2F6FEB', whiteSpace: 'pre'}}>
        線索
      </Interactive.Span>
      <Interactive.Span name="文字片段 3" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        ，不是結論
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 來源標籤 F8、F12
const El09: React.FC = () => {
  return (
    <Interactive.Div
      name="來源文字"
      style={{
        position: 'absolute',
        right: 48,
        bottom: 36,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 24,
        color: '#8A8F99',
      }}
    >
      來源 F8、F12
    </Interactive.Div>
  );
};

export const S5ToolLimit: React.FC = () => {
  return (
    <AbsoluteFill>
      <Interactive.Div
        name="背景"
        from={0}
        durationInFrames={570}
        style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, backgroundColor: '#F6F4EF'}}
      />
      <Sequence name="標題：工具也有限制" from={0} durationInFrames={570}>
        <El01 />
      </Sequence>
      <Sequence name="文字：D23N" from={20} durationInFrames={550}>
        <El02 />
      </Sequence>
      <Sequence name="方塊：第 23 個" from={50} durationInFrames={520}>
        <El03 />
      </Sequence>
      <Sequence name="方塊：第 694 個" from={90} durationInFrames={480}>
        <El04 />
      </Sequence>
      <Sequence name="等號" from={130} durationInFrames={440}>
        <El05 />
      </Sequence>
      <Sequence name="說明：碰巧對上" from={160} durationInFrames={410}>
        <El06 />
      </Sequence>
      <Sequence name="說明：約 7–9%" from={260} durationInFrames={310}>
        <El07 />
      </Sequence>
      <Sequence name="結論：線索，不是結論" from={380} durationInFrames={190}>
        <El08 />
      </Sequence>
      <Sequence name="來源標籤 F8、F12" from={0} durationInFrames={570}>
        <El09 />
      </Sequence>
    </AbsoluteFill>
  );
};
