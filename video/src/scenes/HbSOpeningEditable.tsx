// 可編輯版試作：HbS 開場（影片第一段「問題」的前半）
// 事實來源：F5（AFDB 模型序列開頭 MVHLTPEEK）、F6（UniProt：HbS 標在第 7 個；起始 M 標為 Removed）
//
// 結構說明（給在 Remotion Studio 裡編輯的人）：
// - 每個畫面元素是一個獨立的 <Sequence>，在 Studio 時間軸上各佔一條軌道；拖動軌道就能改出現時間與長度
// - 每個元素裡的動畫（淡入、位移、縮放）都是關鍵影格，影格數從「該元素開始」算起，
//   所以拖動元素時，動畫會整個跟著移動
// - 所有數值（文字、顏色、大小、位置、關鍵影格）都直接寫在這個檔案裡，Studio 才能編輯並存回檔案
// - 軌道由上往下排列：越下面的軌道畫在越上層
import {AbsoluteFill, Easing, Interactive, Sequence, interpolate, useCurrentFrame} from 'remotion';
import '../theme';

export const HBS_EDITABLE_DURATION = 960; // 32 秒 @ 30fps

const TitleE6V: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="標題組（位置與縮放）"
      style={{
        position: 'absolute',
        left: 0,
        top: 0,
        width: 1920,
        height: 1080,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        opacity: interpolate(frame, [10, 35], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
        }),
        translate: interpolate(frame, [0, 135, 165], ['0px -40px', '0px -40px', '-620px -390px'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1), Easing.bezier(0.33, 0, 0.2, 1)],
          outputType: 'translate',
        }),
        scale: interpolate(frame, [0, 135, 165], ['1', '1', '0.42'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1), Easing.bezier(0.33, 0, 0.2, 1)],
          output: 'perceptual-scale',
          outputType: 'scale',
        }),
      }}
    >
      <Interactive.Div
        name="小標：鐮刀型貧血 HbS"
        style={{fontFamily: "'Noto Sans TC', sans-serif", fontSize: 52, color: '#8A8F99', marginBottom: 12}}
      >
        鐮刀型貧血 HbS
      </Interactive.Div>
      <Interactive.Div
        name="大字：E6V"
        style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 240,
          fontWeight: 700,
          letterSpacing: 8,
          color: '#1F2430',
        }}
      >
        <Interactive.Span name="文字片段 1" style={{color: '#1F2430', whiteSpace: 'pre'}}>
          E
        </Interactive.Span>
        <Interactive.Span name="文字片段 2" style={{color: '#2F6FEB', whiteSpace: 'pre'}}>
          6
        </Interactive.Span>
        <Interactive.Span name="文字片段 3" style={{color: '#1F2430', whiteSpace: 'pre'}}>
          V
        </Interactive.Span>
      </Interactive.Div>
    </Interactive.Div>
  );
};

const SubtitleTextbook: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="副標文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 760,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 50,
        color: '#1F2430',
        opacity: interpolate(frame, [0, 12, 98, 110], [0, 1, 1, 0], {
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
        教科書：第{' '}
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#2F6FEB', whiteSpace: 'pre'}}>
        6
      </Interactive.Span>
      <Interactive.Span name="文字片段 3" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        {' '}
        個胺基酸，E 變成 V
      </Interactive.Span>
    </Interactive.Div>
  );
};

const SequenceLabel: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="序列標題文字"
      style={{
        position: 'absolute',
        left: 332,
        top: 260,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 34,
        color: '#8A8F99',
        opacity: interpolate(frame, [0, 20], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
        }),
      }}
    >
      AlphaFold DB 模型（P68871）序列開頭
    </Interactive.Div>
  );
};

const SequenceRow: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      <Interactive.Div
        name="方塊 1：M"
        style={{
          position: 'absolute',
          left: 332,
          top: 430,
          width: 120,
          height: 120,
          borderRadius: 18,
          backgroundColor: '#FFFFFF',
          boxShadow: '0 6px 20px rgba(0,0,0,0.06)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 72,
          fontWeight: 700,
          color: '#1F2430',
          opacity: interpolate(frame, [0, 18], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [0, 18], ['0px 30px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        M
      </Interactive.Div>
      <Interactive.Div
        name="編號 1"
        style={{
          position: 'absolute',
          left: 332,
          top: 564,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 500,
          color: '#8A8F99',
          opacity: interpolate(frame, [0, 18], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      >
        1
      </Interactive.Div>
      <Interactive.Div
        name="方塊 2：V"
        style={{
          position: 'absolute',
          left: 474,
          top: 430,
          width: 120,
          height: 120,
          borderRadius: 18,
          backgroundColor: '#FFFFFF',
          boxShadow: '0 6px 20px rgba(0,0,0,0.06)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 72,
          fontWeight: 700,
          color: '#1F2430',
          opacity: interpolate(frame, [6, 24], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [6, 24], ['0px 30px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        V
      </Interactive.Div>
      <Interactive.Div
        name="編號 2"
        style={{
          position: 'absolute',
          left: 474,
          top: 564,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 500,
          color: '#8A8F99',
          opacity: interpolate(frame, [6, 24], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      >
        2
      </Interactive.Div>
      <Interactive.Div
        name="方塊 3：H"
        style={{
          position: 'absolute',
          left: 616,
          top: 430,
          width: 120,
          height: 120,
          borderRadius: 18,
          backgroundColor: '#FFFFFF',
          boxShadow: '0 6px 20px rgba(0,0,0,0.06)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 72,
          fontWeight: 700,
          color: '#1F2430',
          opacity: interpolate(frame, [12, 30], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [12, 30], ['0px 30px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        H
      </Interactive.Div>
      <Interactive.Div
        name="編號 3"
        style={{
          position: 'absolute',
          left: 616,
          top: 564,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 500,
          color: '#8A8F99',
          opacity: interpolate(frame, [12, 30], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      >
        3
      </Interactive.Div>
      <Interactive.Div
        name="方塊 4：L"
        style={{
          position: 'absolute',
          left: 758,
          top: 430,
          width: 120,
          height: 120,
          borderRadius: 18,
          backgroundColor: '#FFFFFF',
          boxShadow: '0 6px 20px rgba(0,0,0,0.06)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 72,
          fontWeight: 700,
          color: '#1F2430',
          opacity: interpolate(frame, [18, 36], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [18, 36], ['0px 30px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        L
      </Interactive.Div>
      <Interactive.Div
        name="編號 4"
        style={{
          position: 'absolute',
          left: 758,
          top: 564,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 500,
          color: '#8A8F99',
          opacity: interpolate(frame, [18, 36], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      >
        4
      </Interactive.Div>
      <Interactive.Div
        name="方塊 5：T"
        style={{
          position: 'absolute',
          left: 900,
          top: 430,
          width: 120,
          height: 120,
          borderRadius: 18,
          backgroundColor: '#FFFFFF',
          boxShadow: '0 6px 20px rgba(0,0,0,0.06)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 72,
          fontWeight: 700,
          color: '#1F2430',
          opacity: interpolate(frame, [24, 42], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [24, 42], ['0px 30px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        T
      </Interactive.Div>
      <Interactive.Div
        name="編號 5"
        style={{
          position: 'absolute',
          left: 900,
          top: 564,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 500,
          color: '#8A8F99',
          opacity: interpolate(frame, [24, 42], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      >
        5
      </Interactive.Div>
      <Interactive.Div
        name="方塊 6：P"
        style={{
          position: 'absolute',
          left: 1042,
          top: 430,
          width: 120,
          height: 120,
          borderRadius: 18,
          backgroundColor: '#FFFFFF',
          boxShadow: '0 6px 20px rgba(0,0,0,0.06)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 72,
          fontWeight: 700,
          color: '#1F2430',
          opacity: interpolate(frame, [30, 48], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [30, 48], ['0px 30px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        P
      </Interactive.Div>
      <Interactive.Div
        name="編號 6"
        style={{
          position: 'absolute',
          left: 1042,
          top: 564,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 500,
          color: '#8A8F99',
          opacity: interpolate(frame, [30, 48], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      >
        6
      </Interactive.Div>
      <Interactive.Div
        name="方塊 7：E"
        style={{
          position: 'absolute',
          left: 1184,
          top: 430,
          width: 120,
          height: 120,
          borderRadius: 18,
          backgroundColor: '#FFFFFF',
          boxShadow: '0 6px 20px rgba(0,0,0,0.06)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 72,
          fontWeight: 700,
          color: '#1F2430',
          opacity: interpolate(frame, [36, 54], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [36, 54], ['0px 30px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        E
      </Interactive.Div>
      <Interactive.Div
        name="編號 7"
        style={{
          position: 'absolute',
          left: 1184,
          top: 564,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 500,
          color: '#8A8F99',
          opacity: interpolate(frame, [36, 54], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      >
        7
      </Interactive.Div>
      <Interactive.Div
        name="方塊 8：E"
        style={{
          position: 'absolute',
          left: 1326,
          top: 430,
          width: 120,
          height: 120,
          borderRadius: 18,
          backgroundColor: '#FFFFFF',
          boxShadow: '0 6px 20px rgba(0,0,0,0.06)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 72,
          fontWeight: 700,
          color: '#1F2430',
          opacity: interpolate(frame, [42, 60], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [42, 60], ['0px 30px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        E
      </Interactive.Div>
      <Interactive.Div
        name="編號 8"
        style={{
          position: 'absolute',
          left: 1326,
          top: 564,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 500,
          color: '#8A8F99',
          opacity: interpolate(frame, [42, 60], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      >
        8
      </Interactive.Div>
      <Interactive.Div
        name="方塊 9：K"
        style={{
          position: 'absolute',
          left: 1468,
          top: 430,
          width: 120,
          height: 120,
          borderRadius: 18,
          backgroundColor: '#FFFFFF',
          boxShadow: '0 6px 20px rgba(0,0,0,0.06)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 72,
          fontWeight: 700,
          color: '#1F2430',
          opacity: interpolate(frame, [48, 66], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [48, 66], ['0px 30px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        K
      </Interactive.Div>
      <Interactive.Div
        name="編號 9"
        style={{
          position: 'absolute',
          left: 1468,
          top: 564,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 500,
          color: '#8A8F99',
          opacity: interpolate(frame, [48, 66], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      >
        9
      </Interactive.Div>
    </>
  );
};

const StrikeM: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      <Interactive.Div
        name="M 變淡"
        style={{
          position: 'absolute',
          left: 332,
          top: 430,
          width: 120,
          height: 190,
          backgroundColor: '#F6F4EF',
          opacity: interpolate(frame, [0, 30], [0, 0.65], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      ></Interactive.Div>
      <Interactive.Div
        name="紅色劃線"
        style={{
          position: 'absolute',
          left: 346,
          top: 487,
          width: 92,
          height: 6,
          backgroundColor: '#D9483B',
          transformOrigin: 'left center',
          scale: interpolate(frame, [0, 30], ['0 1', '1 1'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            output: 'perceptual-scale',
            outputType: 'scale',
          }),
        }}
      ></Interactive.Div>
    </>
  );
};

const LiteratureRow: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      <Interactive.Div
        name="文獻編號 1"
        style={{
          position: 'absolute',
          left: 474,
          top: 366,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 700,
          color: '#2F6FEB',
          opacity: interpolate(frame, [0, 30], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [0, 30], ['0px 12px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        1
      </Interactive.Div>
      <Interactive.Div
        name="文獻編號 2"
        style={{
          position: 'absolute',
          left: 616,
          top: 366,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 700,
          color: '#2F6FEB',
          opacity: interpolate(frame, [0, 30], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [0, 30], ['0px 12px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        2
      </Interactive.Div>
      <Interactive.Div
        name="文獻編號 3"
        style={{
          position: 'absolute',
          left: 758,
          top: 366,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 700,
          color: '#2F6FEB',
          opacity: interpolate(frame, [0, 30], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [0, 30], ['0px 12px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        3
      </Interactive.Div>
      <Interactive.Div
        name="文獻編號 4"
        style={{
          position: 'absolute',
          left: 900,
          top: 366,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 700,
          color: '#2F6FEB',
          opacity: interpolate(frame, [0, 30], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [0, 30], ['0px 12px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        4
      </Interactive.Div>
      <Interactive.Div
        name="文獻編號 5"
        style={{
          position: 'absolute',
          left: 1042,
          top: 366,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 700,
          color: '#2F6FEB',
          opacity: interpolate(frame, [0, 30], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [0, 30], ['0px 12px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        5
      </Interactive.Div>
      <Interactive.Div
        name="文獻編號 6"
        style={{
          position: 'absolute',
          left: 1184,
          top: 366,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 700,
          color: '#2F6FEB',
          opacity: interpolate(frame, [0, 30], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [0, 30], ['0px 12px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        6
      </Interactive.Div>
      <Interactive.Div
        name="文獻編號 7"
        style={{
          position: 'absolute',
          left: 1326,
          top: 366,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 700,
          color: '#2F6FEB',
          opacity: interpolate(frame, [0, 30], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [0, 30], ['0px 12px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        7
      </Interactive.Div>
      <Interactive.Div
        name="文獻編號 8"
        style={{
          position: 'absolute',
          left: 1468,
          top: 366,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 700,
          color: '#2F6FEB',
          opacity: interpolate(frame, [0, 30], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
          translate: interpolate(frame, [0, 30], ['0px 12px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      >
        8
      </Interactive.Div>
    </>
  );
};

const NumberingLabels: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      <Interactive.Div
        name="標籤：文獻的數法"
        style={{
          position: 'absolute',
          left: 72,
          top: 370,
          width: 230,
          textAlign: 'right',
          fontFamily: "'Noto Sans TC', sans-serif",
          fontSize: 30,
          color: '#2F6FEB',
          opacity: interpolate(frame, [0, 30], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      >
        文獻的數法
      </Interactive.Div>
      <Interactive.Div
        name="標籤：模型的數法"
        style={{
          position: 'absolute',
          left: 72,
          top: 568,
          width: 230,
          textAlign: 'right',
          fontFamily: "'Noto Sans TC', sans-serif",
          fontSize: 30,
          color: '#8A8F99',
          opacity: interpolate(frame, [0, 30], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          }),
        }}
      >
        模型的數法
      </Interactive.Div>
    </>
  );
};

const Dimmer1: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="遮罩"
      style={{
        position: 'absolute',
        left: 312,
        top: 340,
        width: 1296,
        height: 290,
        backgroundColor: '#F6F4EF',
        opacity: interpolate(frame, [0, 14, 292, 306], [0, 0.75, 0.75, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
      }}
    ></Interactive.Div>
  );
};

const Dimmer2: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="遮罩"
      style={{
        position: 'absolute',
        left: 312,
        top: 340,
        width: 1296,
        height: 290,
        backgroundColor: '#F6F4EF',
        opacity: interpolate(frame, [0, 14, 206, 220], [0, 0.75, 0.75, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
      }}
    ></Interactive.Div>
  );
};

const Focus6: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      <Interactive.Div
        name="聚焦方塊：P"
        style={{
          position: 'absolute',
          left: 1042,
          top: 430,
          width: 120,
          height: 120,
          borderRadius: 18,
          backgroundColor: '#FFFFFF',
          boxShadow: '0 6px 20px rgba(0,0,0,0.06)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 72,
          fontWeight: 700,
          color: '#1F2430',
          borderWidth: 5,
          borderStyle: 'solid',
          borderColor: '#D9483B',
          opacity: interpolate(frame, [0, 14, 136, 150], [0, 1, 1, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [
              Easing.bezier(0.33, 0, 0.2, 1),
              Easing.bezier(0.33, 0, 0.2, 1),
              Easing.bezier(0.33, 0, 0.2, 1),
            ],
          }),
          scale: interpolate(frame, [0, 14], ['1', '1.12'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            output: 'perceptual-scale',
            outputType: 'scale',
          }),
        }}
      >
        P
      </Interactive.Div>
      <Interactive.Div
        name="聚焦編號：6"
        style={{
          position: 'absolute',
          left: 1042,
          top: 564,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 700,
          color: '#D9483B',
          opacity: interpolate(frame, [0, 14, 136, 150], [0, 1, 1, 0], {
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
        6
      </Interactive.Div>
    </>
  );
};

const Focus7: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      <Interactive.Div
        name="聚焦方塊：E"
        style={{
          position: 'absolute',
          left: 1184,
          top: 430,
          width: 120,
          height: 120,
          borderRadius: 18,
          backgroundColor: '#FFFFFF',
          boxShadow: '0 6px 20px rgba(0,0,0,0.06)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 72,
          fontWeight: 700,
          color: '#1F2430',
          borderWidth: 5,
          borderStyle: 'solid',
          borderColor: '#1E9E6A',
          opacity: interpolate(frame, [0, 14, 142, 156], [0, 1, 1, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [
              Easing.bezier(0.33, 0, 0.2, 1),
              Easing.bezier(0.33, 0, 0.2, 1),
              Easing.bezier(0.33, 0, 0.2, 1),
            ],
          }),
          scale: interpolate(frame, [0, 14], ['1', '1.12'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            output: 'perceptual-scale',
            outputType: 'scale',
          }),
        }}
      >
        E
      </Interactive.Div>
      <Interactive.Div
        name="聚焦編號：7"
        style={{
          position: 'absolute',
          left: 1184,
          top: 564,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 700,
          color: '#1E9E6A',
          opacity: interpolate(frame, [0, 14, 142, 156], [0, 1, 1, 0], {
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
        7
      </Interactive.Div>
    </>
  );
};

const FocusLink: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      <Interactive.Div
        name="聚焦方塊：E"
        style={{
          position: 'absolute',
          left: 1184,
          top: 430,
          width: 120,
          height: 120,
          borderRadius: 18,
          backgroundColor: '#FFFFFF',
          boxShadow: '0 6px 20px rgba(0,0,0,0.06)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 72,
          fontWeight: 700,
          color: '#1F2430',
          borderWidth: 5,
          borderStyle: 'solid',
          borderColor: '#2F6FEB',
          opacity: interpolate(frame, [0, 14, 206, 220], [0, 1, 1, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [
              Easing.bezier(0.33, 0, 0.2, 1),
              Easing.bezier(0.33, 0, 0.2, 1),
              Easing.bezier(0.33, 0, 0.2, 1),
            ],
          }),
          scale: interpolate(frame, [0, 14], ['1', '1.12'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            output: 'perceptual-scale',
            outputType: 'scale',
          }),
        }}
      >
        E
      </Interactive.Div>
      <Interactive.Div
        name="聚焦編號：7"
        style={{
          position: 'absolute',
          left: 1184,
          top: 564,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 700,
          color: '#2F6FEB',
          opacity: interpolate(frame, [0, 14, 206, 220], [0, 1, 1, 0], {
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
        7
      </Interactive.Div>
      <Interactive.Div
        name="聚焦文獻編號：6"
        style={{
          position: 'absolute',
          left: 1184,
          top: 366,
          width: 120,
          textAlign: 'center',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 36,
          fontWeight: 700,
          color: '#2F6FEB',
          opacity: interpolate(frame, [0, 14, 206, 220], [0, 1, 1, 0], {
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
        6
      </Interactive.Div>
    </>
  );
};

const Caption1: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="字幕文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 840,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 54,
        fontWeight: 700,
        color: '#1F2430',
        opacity: interpolate(frame, [0, 12, 128, 140], [0, 1, 1, 0], {
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
        模型的第 6 個是{' '}
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#D9483B', whiteSpace: 'pre'}}>
        P
      </Interactive.Span>
      <Interactive.Span name="文字片段 3" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        ，不是 E
      </Interactive.Span>
    </Interactive.Div>
  );
};

const Caption2: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="字幕文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 840,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 54,
        fontWeight: 700,
        color: '#1F2430',
        opacity: interpolate(frame, [0, 12, 128, 140], [0, 1, 1, 0], {
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
        E 在第{' '}
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#1E9E6A', whiteSpace: 'pre'}}>
        7
      </Interactive.Span>
      <Interactive.Span name="文字片段 3" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        {' '}
        個
      </Interactive.Span>
    </Interactive.Div>
  );
};

const Caption3: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="字幕文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 840,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 54,
        fontWeight: 700,
        color: '#1F2430',
        opacity: interpolate(frame, [0, 12, 188, 200], [0, 1, 1, 0], {
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
      成熟的蛋白質去掉了開頭的 M，文獻從 V 開始數
    </Interactive.Div>
  );
};

const Caption4: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="字幕文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 840,
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
      <Interactive.Span name="文字片段 1" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        同一個突變，
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#2F6FEB', whiteSpace: 'pre'}}>
        兩套編號
      </Interactive.Span>
    </Interactive.Div>
  );
};

const SourceA: React.FC = () => {
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

const SourceB: React.FC = () => {
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
      來源 F5、F6
    </Interactive.Div>
  );
};

export const HbSOpeningEditable: React.FC = () => {
  return (
    <AbsoluteFill>
      <Interactive.Div
        name="背景"
        from={0}
        durationInFrames={960}
        style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, backgroundColor: '#F6F4EF'}}
      />
      <Sequence name="開場標題 E6V" from={0} durationInFrames={960}>
        <TitleE6V />
      </Sequence>
      <Sequence name="副標：教科書" from={35} durationInFrames={110}>
        <SubtitleTextbook />
      </Sequence>
      <Sequence name="序列標題" from={155} durationInFrames={805}>
        <SequenceLabel />
      </Sequence>
      <Sequence name="序列方塊與模型編號" from={165} durationInFrames={795}>
        <SequenceRow />
      </Sequence>
      <Sequence name="劃掉 M" from={630} durationInFrames={330}>
        <StrikeM />
      </Sequence>
      <Sequence name="文獻的編號列" from={670} durationInFrames={290}>
        <LiteratureRow />
      </Sequence>
      <Sequence name="標籤：兩種數法" from={670} durationInFrames={290}>
        <NumberingLabels />
      </Sequence>
      <Sequence name="變暗遮罩 1（第 6、7 格）" from={330} durationInFrames={306}>
        <Dimmer1 />
      </Sequence>
      <Sequence name="變暗遮罩 2（文獻 6 = 模型 7）" from={740} durationInFrames={220}>
        <Dimmer2 />
      </Sequence>
      <Sequence name="聚焦：第 6 個是 P（紅）" from={330} durationInFrames={150}>
        <Focus6 />
      </Sequence>
      <Sequence name="聚焦：第 7 個是 E（綠）" from={480} durationInFrames={156}>
        <Focus7 />
      </Sequence>
      <Sequence name="聚焦：文獻 6 = 模型 7（藍）" from={740} durationInFrames={220}>
        <FocusLink />
      </Sequence>
      <Sequence name="字幕 1：第 6 個是 P" from={340} durationInFrames={140}>
        <Caption1 />
      </Sequence>
      <Sequence name="字幕 2：E 在第 7 個" from={490} durationInFrames={140}>
        <Caption2 />
      </Sequence>
      <Sequence name="字幕 3：去掉 M" from={640} durationInFrames={200}>
        <Caption3 />
      </Sequence>
      <Sequence name="字幕 4：兩套編號" from={845} durationInFrames={115}>
        <Caption4 />
      </Sequence>
      <Sequence name="來源標籤 F6" from={0} durationInFrames={135}>
        <SourceA />
      </Sequence>
      <Sequence name="來源標籤 F5、F6" from={135} durationInFrames={825}>
        <SourceB />
      </Sequence>
    </AbsoluteFill>
  );
};
