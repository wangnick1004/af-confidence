// 段 1｜問題（設計腳本鏡頭 1-1～1-3）
// 事實來源：F6（HbS：β 鏈 E→V，教科書寫作 E6V）
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

export const S1QUESTION_DURATION = 900; // 30.0 秒 @ 30fps

// 紅血球（正常）
const El01: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="正常紅血球"
      style={{
        position: 'absolute',
        left: 800,
        top: 230,
        width: 320,
        height: 320,
        opacity: interpolate(frame, [0, 20, 135, 170], [0, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
      }}
    >
      <svg width="320" height="320" viewBox="0 0 320 320">
        <circle cx="160" cy="160" r="140" fill="#C8463D" />
        <circle cx="160" cy="160" r="70" fill="#D9675F" />
      </svg>
    </Interactive.Div>
  );
};

// 紅血球（鐮刀形）
const El02: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="鐮刀形紅血球"
      style={{
        position: 'absolute',
        left: 800,
        top: 230,
        width: 320,
        height: 320,
        opacity: interpolate(frame, [0, 30, 120, 135], [0, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
        rotate: interpolate(frame, [0, 40], ['-12deg', '0deg'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
        }),
      }}
    >
      <svg width="320" height="320" viewBox="0 0 320 320">
        <path d="M25,235 Q95,25 300,120 Q170,165 25,235 Z" fill="#C8463D" />
      </svg>
    </Interactive.Div>
  );
};

// 標題：鐮刀型貧血
const El03: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="標題文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 620,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 72,
        fontWeight: 700,
        color: '#1F2430',
        opacity: interpolate(frame, [0, 12, 235, 250], [0, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
        translate: interpolate(frame, [0, 12], ['0px 16px', '0px 0px'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          outputType: 'translate',
        }),
      }}
    >
      鐮刀型貧血
    </Interactive.Div>
  );
};

// 標籤：血紅素 β 鏈
const El04: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="標籤文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 250,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 40,
        fontWeight: 400,
        color: '#8A8F99',
        opacity: interpolate(frame, [0, 12, 288, 300], [0, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
        translate: interpolate(frame, [0, 12], ['0px 16px', '0px 0px'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          outputType: 'translate',
        }),
      }}
    >
      血紅素 β 鏈
    </Interactive.Div>
  );
};

// β 鏈的其他胺基酸
const El05: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      <Interactive.Div
        name="胺基酸 1"
        style={{
          position: 'absolute',
          left: 485,
          top: 360,
          width: 110,
          height: 110,
          borderRadius: 18,
          backgroundColor: '#E4E1DA',
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
      />
      <Interactive.Div
        name="胺基酸 2"
        style={{
          position: 'absolute',
          left: 625,
          top: 360,
          width: 110,
          height: 110,
          borderRadius: 18,
          backgroundColor: '#E4E1DA',
          opacity: interpolate(frame, [4, 19], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [4, 19], ['0px 20px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      />
      <Interactive.Div
        name="胺基酸 3"
        style={{
          position: 'absolute',
          left: 765,
          top: 360,
          width: 110,
          height: 110,
          borderRadius: 18,
          backgroundColor: '#E4E1DA',
          opacity: interpolate(frame, [8, 23], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [8, 23], ['0px 20px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      />
      <Interactive.Div
        name="胺基酸 5"
        style={{
          position: 'absolute',
          left: 1045,
          top: 360,
          width: 110,
          height: 110,
          borderRadius: 18,
          backgroundColor: '#E4E1DA',
          opacity: interpolate(frame, [16, 31], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [16, 31], ['0px 20px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      />
      <Interactive.Div
        name="胺基酸 6"
        style={{
          position: 'absolute',
          left: 1185,
          top: 360,
          width: 110,
          height: 110,
          borderRadius: 18,
          backgroundColor: '#E4E1DA',
          opacity: interpolate(frame, [20, 35], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [20, 35], ['0px 20px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      />
      <Interactive.Div
        name="胺基酸 7"
        style={{
          position: 'absolute',
          left: 1325,
          top: 360,
          width: 110,
          height: 110,
          borderRadius: 18,
          backgroundColor: '#E4E1DA',
          opacity: interpolate(frame, [24, 39], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [24, 39], ['0px 20px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      />
    </>
  );
};

// 方塊：E（原本）
const El06: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="E 方塊"
      style={{
        position: 'absolute',
        left: 905,
        top: 360,
        width: 110,
        height: 110,
        borderRadius: 18,
        backgroundColor: '#FFFFFF',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 64,
        fontWeight: 700,
        color: '#1F2430',
        borderWidth: 5,
        borderStyle: 'solid',
        borderColor: '#2F6FEB',
        opacity: interpolate(frame, [0, 15], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
        }),
        scale: interpolate(frame, [0, 108, 138], ['1 1', '1 1', '1 0'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1), Easing.bezier(0.33, 0, 0.2, 1)],
          output: 'perceptual-scale',
          outputType: 'scale',
        }),
        fontVariantLigatures: 'none',
      }}
    >
      E
    </Interactive.Div>
  );
};

// 方塊：V（突變後）
const El07: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="V 方塊"
      style={{
        position: 'absolute',
        left: 905,
        top: 360,
        width: 110,
        height: 110,
        borderRadius: 18,
        backgroundColor: '#FFFFFF',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 64,
        fontWeight: 700,
        color: '#2F6FEB',
        borderWidth: 5,
        borderStyle: 'solid',
        borderColor: '#2F6FEB',
        scale: interpolate(frame, [0, 30], ['1 0', '1.12 1.12'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          output: 'perceptual-scale',
          outputType: 'scale',
        }),
        opacity: interpolate(frame, [0, 1, 138, 150], [0, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
        fontVariantLigatures: 'none',
      }}
    >
      V
    </Interactive.Div>
  );
};

// 文字：E → V
const El08: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 560,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 64,
        fontWeight: 700,
        color: '#1F2430',
        opacity: interpolate(frame, [0, 12, 228, 240], [0, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
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
      <Interactive.Span name="文字片段 1" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        E
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#8A8F99', whiteSpace: 'pre'}}>
        {' '}
        →{' '}
      </Interactive.Span>
      <Interactive.Span name="文字片段 3" style={{color: '#2F6FEB', whiteSpace: 'pre'}}>
        V
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 文字：教科書 E6V
const El09: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 680,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 48,
        fontWeight: 400,
        color: '#1F2430',
        opacity: interpolate(frame, [0, 12, 108, 120], [0, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
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
        教科書：E
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#2F6FEB', whiteSpace: 'pre'}}>
        6
      </Interactive.Span>
      <Interactive.Span name="文字片段 3" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        V
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 來源標籤 F6
const El10: React.FC = () => {
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
      來源 F6
    </Interactive.Div>
  );
};

// 問題 1
const El11: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="問題 1 文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 300,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 80,
        fontWeight: 700,
        color: '#1F2430',
        opacity: interpolate(frame, [0, 15, 120, 140], [0, 1, 1, 0.3], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
        translate: interpolate(frame, [0, 12], ['0px 16px', '0px 0px'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          outputType: 'translate',
        }),
      }}
    >
      在結構的哪裡？
    </Interactive.Div>
  );
};

// 問題 2
const El12: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="問題 2 文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 460,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 80,
        fontWeight: 700,
        color: '#1F2430',
        opacity: interpolate(frame, [0, 15, 110, 130], [0, 1, 1, 0.3], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
        translate: interpolate(frame, [0, 12], ['0px 16px', '0px 0px'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          outputType: 'translate',
        }),
      }}
    >
      可不可信？
    </Interactive.Div>
  );
};

// 答案：AlphaFold DB
const El13: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="答案文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 660,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 72,
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
      <Interactive.Span name="文字片段 1" style={{color: '#8A8F99', whiteSpace: 'pre'}}>
        →{' '}
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#2F6FEB', whiteSpace: 'pre'}}>
        AlphaFold DB
      </Interactive.Span>
    </Interactive.Div>
  );
};

export const S1Question: React.FC = () => {
  return (
    <AbsoluteFill>
      <Interactive.Div
        name="背景"
        from={0}
        durationInFrames={900}
        style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, backgroundColor: '#F6F4EF'}}
      />
      <Sequence name="紅血球（正常）" from={0} durationInFrames={170}>
        <El01 />
      </Sequence>
      <Sequence name="紅血球（鐮刀形）" from={135} durationInFrames={135}>
        <El02 />
      </Sequence>
      <Sequence name="標題：鐮刀型貧血" from={20} durationInFrames={250}>
        <El03 />
      </Sequence>
      <Sequence name="標籤：血紅素 β 鏈" from={270} durationInFrames={300}>
        <El04 />
      </Sequence>
      <Sequence name="β 鏈的其他胺基酸" from={270} durationInFrames={300}>
        <El05 />
      </Sequence>
      <Sequence name="方塊：E（原本）" from={282} durationInFrames={138}>
        <El06 />
      </Sequence>
      <Sequence name="方塊：V（突變後）" from={420} durationInFrames={150}>
        <El07 />
      </Sequence>
      <Sequence name="文字：E → V" from={330} durationInFrames={240}>
        <El08 />
      </Sequence>
      <Sequence name="文字：教科書 E6V" from={450} durationInFrames={120}>
        <El09 />
      </Sequence>
      <Sequence name="來源標籤 F6" from={270} durationInFrames={300}>
        <El10 />
      </Sequence>
      <Sequence name="問題 1" from={570} durationInFrames={330}>
        <El11 />
      </Sequence>
      <Sequence name="問題 2" from={690} durationInFrames={210}>
        <El12 />
      </Sequence>
      <Sequence name="答案：AlphaFold DB" from={800} durationInFrames={100}>
        <El13 />
      </Sequence>
    </AbsoluteFill>
  );
};
