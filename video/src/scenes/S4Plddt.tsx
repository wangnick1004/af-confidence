// 段 4｜pLDDT 分級與 TP53 對比（設計腳本鏡頭 4-1、4-2）
// 事實來源：F1（分級）、F17（網站顏色）、F4（TP53 R175 96.62、P72 48.25）、F13（< 50 不應解讀）
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

export const S4PLDDT_DURATION = 1380; // 46.0 秒 @ 30fps

// 標題：pLDDT
const El01: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="標題文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 170,
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
      <Interactive.Span name="文字片段 1" style={{color: '#2F6FEB', whiteSpace: 'pre'}}>
        pLDDT
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        ：每個胺基酸的信心分數
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 刻度尺（四個色段）
const El02: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      <Interactive.Div
        name="色段：非常低"
        style={{
          position: 'absolute',
          left: 260,
          top: 450,
          width: 700,
          height: 80,
          borderRadius: 0,
          backgroundColor: '#FF7D45',
          opacity: interpolate(frame, [10, 25], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      />
      <Interactive.Div
        name="色段：低"
        style={{
          position: 'absolute',
          left: 960,
          top: 450,
          width: 280,
          height: 80,
          borderRadius: 0,
          backgroundColor: '#FFDB13',
          opacity: interpolate(frame, [18, 33], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      />
      <Interactive.Div
        name="色段：高"
        style={{
          position: 'absolute',
          left: 1240,
          top: 450,
          width: 280,
          height: 80,
          borderRadius: 0,
          backgroundColor: '#65CBF3',
          opacity: interpolate(frame, [26, 41], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      />
      <Interactive.Div
        name="色段：非常高"
        style={{
          position: 'absolute',
          left: 1520,
          top: 450,
          width: 140,
          height: 80,
          borderRadius: 0,
          backgroundColor: '#0053D6',
          opacity: interpolate(frame, [34, 49], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      />
      <Interactive.Div
        name="刻度 0"
        style={{
          position: 'absolute',
          left: 210,
          top: 542,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 30,
          fontWeight: 400,
          color: '#8A8F99',
          textAlign: 'center',
          width: 100,
          opacity: interpolate(frame, [30, 45], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          fontVariantLigatures: 'none',
        }}
      >
        0
      </Interactive.Div>
      <Interactive.Div
        name="刻度 50"
        style={{
          position: 'absolute',
          left: 910,
          top: 542,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 30,
          fontWeight: 400,
          color: '#8A8F99',
          textAlign: 'center',
          width: 100,
          opacity: interpolate(frame, [30, 45], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          fontVariantLigatures: 'none',
        }}
      >
        50
      </Interactive.Div>
      <Interactive.Div
        name="刻度 70"
        style={{
          position: 'absolute',
          left: 1190,
          top: 542,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 30,
          fontWeight: 400,
          color: '#8A8F99',
          textAlign: 'center',
          width: 100,
          opacity: interpolate(frame, [30, 45], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          fontVariantLigatures: 'none',
        }}
      >
        70
      </Interactive.Div>
      <Interactive.Div
        name="刻度 90"
        style={{
          position: 'absolute',
          left: 1470,
          top: 542,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 30,
          fontWeight: 400,
          color: '#8A8F99',
          textAlign: 'center',
          width: 100,
          opacity: interpolate(frame, [30, 45], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          fontVariantLigatures: 'none',
        }}
      >
        90
      </Interactive.Div>
      <Interactive.Div
        name="刻度 100"
        style={{
          position: 'absolute',
          left: 1610,
          top: 542,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 30,
          fontWeight: 400,
          color: '#8A8F99',
          textAlign: 'center',
          width: 100,
          opacity: interpolate(frame, [30, 45], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          fontVariantLigatures: 'none',
        }}
      >
        100
      </Interactive.Div>
    </>
  );
};

// 聚焦：非常高
const El03: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="聚焦框"
      style={{
        position: 'absolute',
        left: 1512,
        top: 442,
        width: 156,
        height: 96,
        borderRadius: 8,
        backgroundColor: 'transparent',
        borderWidth: 4,
        borderStyle: 'solid',
        borderColor: '#1F2430',
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

// 標籤：非常高 > 90
const El04: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="標籤文字"
      style={{
        position: 'absolute',
        left: 1440,
        top: 600,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 40,
        fontWeight: 700,
        color: '#1F2430',
        textAlign: 'center',
        width: 300,
        whiteSpace: 'pre',
        lineHeight: 1.3,
        opacity: interpolate(frame, [0, 12, 585, 600], [0, 1, 1, 0], {
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
      <Interactive.Span name="文字片段 1" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        {'非常高\n'}
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#8A8F99', whiteSpace: 'pre'}}>
        {'> 90'}
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 聚焦：高
const El05: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="聚焦框"
      style={{
        position: 'absolute',
        left: 1232,
        top: 442,
        width: 296,
        height: 96,
        borderRadius: 8,
        backgroundColor: 'transparent',
        borderWidth: 4,
        borderStyle: 'solid',
        borderColor: '#1F2430',
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

// 標籤：高 70–90
const El06: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="標籤文字"
      style={{
        position: 'absolute',
        left: 1230,
        top: 600,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 40,
        fontWeight: 700,
        color: '#1F2430',
        textAlign: 'center',
        width: 300,
        whiteSpace: 'pre',
        lineHeight: 1.3,
        opacity: interpolate(frame, [0, 12, 455, 470], [0, 1, 1, 0], {
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
      <Interactive.Span name="文字片段 1" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        {'高\n'}
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#8A8F99', whiteSpace: 'pre'}}>
        70–90
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 聚焦：低
const El07: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="聚焦框"
      style={{
        position: 'absolute',
        left: 952,
        top: 442,
        width: 296,
        height: 96,
        borderRadius: 8,
        backgroundColor: 'transparent',
        borderWidth: 4,
        borderStyle: 'solid',
        borderColor: '#1F2430',
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

// 標籤：低 50–70
const El08: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="標籤文字"
      style={{
        position: 'absolute',
        left: 950,
        top: 600,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 40,
        fontWeight: 700,
        color: '#1F2430',
        textAlign: 'center',
        width: 300,
        whiteSpace: 'pre',
        lineHeight: 1.3,
        opacity: interpolate(frame, [0, 12, 325, 340], [0, 1, 1, 0], {
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
      <Interactive.Span name="文字片段 1" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        {'低\n'}
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#8A8F99', whiteSpace: 'pre'}}>
        50–70
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 聚焦：非常低
const El09: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="聚焦框"
      style={{
        position: 'absolute',
        left: 252,
        top: 442,
        width: 716,
        height: 96,
        borderRadius: 8,
        backgroundColor: 'transparent',
        borderWidth: 4,
        borderStyle: 'solid',
        borderColor: '#1F2430',
        opacity: interpolate(frame, [0, 12, 198, 210], [0, 1, 1, 0], {
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

// 標籤：非常低 < 50
const El10: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="標籤文字"
      style={{
        position: 'absolute',
        left: 460,
        top: 600,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 40,
        fontWeight: 700,
        color: '#1F2430',
        textAlign: 'center',
        width: 300,
        whiteSpace: 'pre',
        lineHeight: 1.3,
        opacity: interpolate(frame, [0, 12, 195, 210], [0, 1, 1, 0], {
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
      <Interactive.Span name="文字片段 1" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        {'非常低\n'}
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#8A8F99', whiteSpace: 'pre'}}>
        {'< 50'}
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 來源標籤 F1、F17
const El11: React.FC = () => {
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
      來源 F1、F17
    </Interactive.Div>
  );
};

// 標記：R175 96.62
const El12: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="標記（位置與動畫）"
      style={{
        position: 'absolute',
        left: 0,
        top: 0,
        width: 1920,
        height: 1080,
        opacity: interpolate(frame, [0, 15], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
        }),
        translate: interpolate(frame, [0, 20], ['0px -40px', '0px 0px'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          outputType: 'translate',
        }),
      }}
    >
      <Interactive.Div
        name="標記線"
        style={{
          position: 'absolute',
          left: 1610,
          top: 380,
          width: 6,
          height: 150,
          borderRadius: 3,
          backgroundColor: '#1F2430',
        }}
      />
      <Interactive.Div
        name="標記文字"
        style={{
          position: 'absolute',
          left: 1433,
          top: 300,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 48,
          fontWeight: 700,
          color: '#1F2430',
          textAlign: 'center',
          width: 360,
          fontVariantLigatures: 'none',
        }}
      >
        <Interactive.Span name="文字片段 1" style={{color: '#1F2430', whiteSpace: 'pre'}}>
          R175：
        </Interactive.Span>
        <Interactive.Span name="文字片段 2" style={{color: '#0053D6', whiteSpace: 'pre'}}>
          96.62
        </Interactive.Span>
      </Interactive.Div>
    </Interactive.Div>
  );
};

// 標記：P72 48.25
const El13: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="標記（位置與動畫）"
      style={{
        position: 'absolute',
        left: 0,
        top: 0,
        width: 1920,
        height: 1080,
        opacity: interpolate(frame, [0, 15], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
        }),
        translate: interpolate(frame, [0, 20], ['0px -40px', '0px 0px'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          outputType: 'translate',
        }),
      }}
    >
      <Interactive.Div
        name="標記線"
        style={{
          position: 'absolute',
          left: 933,
          top: 380,
          width: 6,
          height: 150,
          borderRadius: 3,
          backgroundColor: '#1F2430',
        }}
      />
      <Interactive.Div
        name="標記文字"
        style={{
          position: 'absolute',
          left: 756,
          top: 300,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 48,
          fontWeight: 700,
          color: '#1F2430',
          textAlign: 'center',
          width: 360,
          fontVariantLigatures: 'none',
        }}
      >
        <Interactive.Span name="文字片段 1" style={{color: '#1F2430', whiteSpace: 'pre'}}>
          P72：
        </Interactive.Span>
        <Interactive.Span name="文字片段 2" style={{color: '#FF7D45', whiteSpace: 'pre'}}>
          48.25
        </Interactive.Span>
      </Interactive.Div>
    </Interactive.Div>
  );
};

// 結論：< 50 不應解讀
const El14: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="結論文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 700,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 54,
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
      <Interactive.Span name="文字片段 1" style={{color: '#FF7D45', whiteSpace: 'pre'}}>
        {'pLDDT < 50'}
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        ：座標不應拿來解讀
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 說明：可能沒有固定結構
const El15: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="說明文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 790,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 36,
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
      可能在生理狀態下沒有固定結構，或只在和其他分子結合時才有結構
    </Interactive.Div>
  );
};

// 來源標籤 F4、F13
const El16: React.FC = () => {
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
      來源 F4、F13
    </Interactive.Div>
  );
};

export const S4Plddt: React.FC = () => {
  return (
    <AbsoluteFill>
      <Interactive.Div
        name="背景"
        from={0}
        durationInFrames={1380}
        style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, backgroundColor: '#F6F4EF'}}
      />
      <Sequence name="標題：pLDDT" from={0} durationInFrames={1380}>
        <El01 />
      </Sequence>
      <Sequence name="刻度尺（四個色段）" from={20} durationInFrames={1360}>
        <El02 />
      </Sequence>
      <Sequence name="聚焦：非常高" from={90} durationInFrames={130}>
        <El03 />
      </Sequence>
      <Sequence name="標籤：非常高 > 90" from={90} durationInFrames={600}>
        <El04 />
      </Sequence>
      <Sequence name="聚焦：高" from={220} durationInFrames={130}>
        <El05 />
      </Sequence>
      <Sequence name="標籤：高 70–90" from={220} durationInFrames={470}>
        <El06 />
      </Sequence>
      <Sequence name="聚焦：低" from={350} durationInFrames={130}>
        <El07 />
      </Sequence>
      <Sequence name="標籤：低 50–70" from={350} durationInFrames={340}>
        <El08 />
      </Sequence>
      <Sequence name="聚焦：非常低" from={480} durationInFrames={210}>
        <El09 />
      </Sequence>
      <Sequence name="標籤：非常低 < 50" from={480} durationInFrames={210}>
        <El10 />
      </Sequence>
      <Sequence name="來源標籤 F1、F17" from={0} durationInFrames={690}>
        <El11 />
      </Sequence>
      <Sequence name="標記：R175 96.62" from={720} durationInFrames={660}>
        <El12 />
      </Sequence>
      <Sequence name="標記：P72 48.25" from={870} durationInFrames={510}>
        <El13 />
      </Sequence>
      <Sequence name="結論：< 50 不應解讀" from={1000} durationInFrames={380}>
        <El14 />
      </Sequence>
      <Sequence name="說明：可能沒有固定結構" from={1060} durationInFrames={320}>
        <El15 />
      </Sequence>
      <Sequence name="來源標籤 F4、F13" from={690} durationInFrames={690}>
        <El16 />
      </Sequence>
    </AbsoluteFill>
  );
};
