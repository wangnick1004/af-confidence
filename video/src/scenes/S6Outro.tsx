// 段 6｜結尾（設計腳本鏡頭 6-1、6-2）
// 事實來源：無新事實（回顧）
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

export const S6OUTRO_DURATION = 600; // 20.0 秒 @ 30fps

// 步驟 ①：先確認編號
const El01: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="步驟 1"
      style={{
        position: 'absolute',
        left: 330,
        top: 320,
        width: 560,
        height: 150,
        borderRadius: 75,
        backgroundColor: '#FFFFFF',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 52,
        fontWeight: 700,
        color: '#1F2430',
        boxShadow: '0 8px 30px rgba(0,0,0,0.06)',
        opacity: interpolate(frame, [0, 15], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
        }),
        translate: interpolate(frame, [0, 15], ['0px 20px', '0px 0px'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          outputType: 'translate',
        }),
      }}
    >
      <Interactive.Span name="文字片段 1" style={{color: '#2F6FEB', whiteSpace: 'pre'}}>
        ①{' '}
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        先確認編號
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 箭頭
const El02: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="箭頭線"
      style={{
        position: 'absolute',
        left: 910,
        top: 390,
        width: 100,
        height: 10,
        borderRadius: 5,
        backgroundColor: '#2F6FEB',
        transformOrigin: 'left center',
        scale: interpolate(frame, [0, 25], ['0 1', '1 1'], {
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

// 步驟 ②：再看 pLDDT
const El03: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="步驟 2"
      style={{
        position: 'absolute',
        left: 1030,
        top: 320,
        width: 560,
        height: 150,
        borderRadius: 75,
        backgroundColor: '#FFFFFF',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 52,
        fontWeight: 700,
        color: '#1F2430',
        boxShadow: '0 8px 30px rgba(0,0,0,0.06)',
        opacity: interpolate(frame, [0, 15], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
        }),
        translate: interpolate(frame, [0, 15], ['0px 20px', '0px 0px'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          outputType: 'translate',
        }),
      }}
    >
      <Interactive.Span name="文字片段 1" style={{color: '#2F6FEB', whiteSpace: 'pre'}}>
        ②{' '}
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        再看 pLDDT
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 網址
const El04: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="網址文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 600,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 44,
        fontWeight: 500,
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
        fontVariantLigatures: 'none',
      }}
    >
      github.com/wangnick1004/af-confidence
    </Interactive.Div>
  );
};

// 說明：只做編號對應
const El05: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="說明文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 680,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 38,
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
      只做編號對應，不判斷突變是否致病
    </Interactive.Div>
  );
};

// 謝謝收看
const El06: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 840,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 60,
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
      謝謝收看
    </Interactive.Div>
  );
};

export const S6Outro: React.FC = () => {
  return (
    <AbsoluteFill>
      <Interactive.Div
        name="背景"
        from={0}
        durationInFrames={600}
        style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, backgroundColor: '#F6F4EF'}}
      />
      <Sequence name="步驟 ①：先確認編號" from={0} durationInFrames={600}>
        <El01 />
      </Sequence>
      <Sequence name="箭頭" from={60} durationInFrames={540}>
        <El02 />
      </Sequence>
      <Sequence name="步驟 ②：再看 pLDDT" from={90} durationInFrames={510}>
        <El03 />
      </Sequence>
      <Sequence name="網址" from={300} durationInFrames={300}>
        <El04 />
      </Sequence>
      <Sequence name="說明：只做編號對應" from={340} durationInFrames={260}>
        <El05 />
      </Sequence>
      <Sequence name="謝謝收看" from={420} durationInFrames={180}>
        <El06 />
      </Sequence>
    </AbsoluteFill>
  );
};
