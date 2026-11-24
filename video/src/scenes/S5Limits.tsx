// 段 5｜三個限制（設計腳本鏡頭 5-1～5-3）
// 事實來源：F13（低 pLDDT）、F14（未驗證突變影響）、F3/F5（單鏈模型）、F6/F7（編號）、F10（ProtVar 截圖）
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

export const S5LIMITS_DURATION = 1530; // 51.0 秒 @ 30fps

// 卡片 1
const El01: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="卡片 1"
      style={{
        position: 'absolute',
        left: 160,
        top: 110,
        width: 520,
        height: 150,
        borderRadius: 18,
        backgroundColor: '#FFFFFF',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 44,
        fontWeight: 700,
        color: '#1F2430',
        boxShadow: '0 8px 30px rgba(0,0,0,0.06)',
        opacity: interpolate(frame, [0, 15, 360, 375, 930, 945], [0, 1, 1, 0.35, 0.35, 0.35], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
      }}
    >
      ① 低 pLDDT 不解讀
    </Interactive.Div>
  );
};

// 卡片 2
const El02: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="卡片 2"
      style={{
        position: 'absolute',
        left: 700,
        top: 110,
        width: 520,
        height: 150,
        borderRadius: 18,
        backgroundColor: '#FFFFFF',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 44,
        fontWeight: 700,
        color: '#1F2430',
        boxShadow: '0 8px 30px rgba(0,0,0,0.06)',
        opacity: interpolate(frame, [0, 15, 360, 375, 930, 945], [0, 0.35, 0.35, 1, 1, 0.35], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
      }}
    >
      ② 正常序列・單鏈預測
    </Interactive.Div>
  );
};

// 卡片 3
const El03: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="卡片 3"
      style={{
        position: 'absolute',
        left: 1240,
        top: 110,
        width: 520,
        height: 150,
        borderRadius: 18,
        backgroundColor: '#FFFFFF',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 44,
        fontWeight: 700,
        color: '#1F2430',
        boxShadow: '0 8px 30px rgba(0,0,0,0.06)',
        opacity: interpolate(frame, [0, 15, 360, 375, 930, 945], [0, 0.35, 0.35, 0.35, 0.35, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
      }}
    >
      ③ 編號：網站不提醒
    </Interactive.Div>
  );
};

// 圖：低信心區（橘色）
const El04: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="低信心區示意"
      style={{
        position: 'absolute',
        left: 300,
        top: 450,
        width: 560,
        height: 260,
        opacity: interpolate(frame, [0, 20, 315, 330], [0, 1, 1, 0], {
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
      <svg width="560" height="260" viewBox="0 0 560 260">
        <path
          d="M20,200 C90,40 150,250 230,120 S360,10 420,170 S520,220 540,60"
          fill="none"
          stroke="#FF7D45"
          stroke-width="22"
          stroke-linecap="round"
        />
      </svg>
    </Interactive.Div>
  );
};

// 文字：pLDDT < 50
const El05: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="文字"
      style={{
        position: 'absolute',
        left: 960,
        top: 470,
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 64,
        fontWeight: 700,
        color: '#1F2430',
        textAlign: 'left',
        opacity: interpolate(frame, [0, 15, 295, 310], [0, 1, 1, 0], {
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
      <Interactive.Span name="文字片段 1" style={{color: '#FF7D45', whiteSpace: 'pre'}}>
        {'pLDDT < 50'}
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 文字：座標不應解讀
const El06: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="文字"
      style={{
        position: 'absolute',
        left: 960,
        top: 570,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 50,
        fontWeight: 700,
        color: '#1F2430',
        textAlign: 'left',
        opacity: interpolate(frame, [0, 15, 265, 280], [0, 1, 1, 0], {
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
      座標不應拿來解讀
    </Interactive.Div>
  );
};

// 文字：常是無序區
const El07: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="文字"
      style={{
        position: 'absolute',
        left: 960,
        top: 650,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 36,
        fontWeight: 400,
        color: '#8A8F99',
        textAlign: 'left',
        opacity: interpolate(frame, [0, 15, 235, 250], [0, 1, 1, 0], {
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
      （常是沒有固定結構的區域）
    </Interactive.Div>
  );
};

// 來源標籤 F13
const El08: React.FC = () => {
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
      來源 F13
    </Interactive.Div>
  );
};

// 方塊：E（模型裡的）
const El09: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="E 方塊"
      style={{
        position: 'absolute',
        left: 300,
        top: 420,
        width: 170,
        height: 170,
        borderRadius: 18,
        backgroundColor: '#FFFFFF',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 80,
        fontWeight: 700,
        color: '#1F2430',
        borderWidth: 5,
        borderStyle: 'solid',
        borderColor: '#1F2430',
        opacity: interpolate(frame, [0, 15, 540, 555], [0, 1, 1, 0], {
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
      E
    </Interactive.Div>
  );
};

// 箭頭
const El10: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="箭頭"
      style={{
        position: 'absolute',
        left: 500,
        top: 445,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 90,
        fontWeight: 400,
        color: '#8A8F99',
        textAlign: 'left',
        opacity: interpolate(frame, [0, 15, 510, 525], [0, 1, 1, 0], {
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
      →
    </Interactive.Div>
  );
};

// 方塊：V（虛線，看不到）
const El11: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="V 方塊"
      style={{
        position: 'absolute',
        left: 620,
        top: 420,
        width: 170,
        height: 170,
        borderRadius: 18,
        backgroundColor: 'transparent',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 80,
        fontWeight: 700,
        color: '#8A8F99',
        borderWidth: 5,
        borderStyle: 'dashed',
        borderColor: '#2F6FEB',
        opacity: interpolate(frame, [0, 20, 50, 70, 90, 110, 480, 495], [0, 1, 0.3, 1, 0.3, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
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

// 文字：看不到突變後的形狀
const El12: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="文字"
      style={{
        position: 'absolute',
        left: 300,
        top: 630,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 40,
        fontWeight: 700,
        color: '#1F2430',
        textAlign: 'left',
        opacity: interpolate(frame, [0, 15, 445, 460], [0, 1, 1, 0], {
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
      看不到突變後的形狀
    </Interactive.Div>
  );
};

// 引文：未驗證突變影響
const El13: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="引文"
      style={{
        position: 'absolute',
        left: 960,
        top: 420,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 46,
        fontWeight: 700,
        color: '#1F2430',
        textAlign: 'left',
        whiteSpace: 'pre',
        lineHeight: 1.4,
        opacity: interpolate(frame, [0, 15, 395, 410], [0, 1, 1, 0], {
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
      <Interactive.Span name="文字片段 1" style={{color: '#8A8F99', whiteSpace: 'pre'}}>
        {'官方說明：\n'}
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        {'AlphaFold 沒有被驗證\n能預測突變的影響'}
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 文字：單一條 β 鏈
const El14: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="文字"
      style={{
        position: 'absolute',
        left: 960,
        top: 640,
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 40,
        fontWeight: 700,
        color: '#1F2430',
        textAlign: 'left',
        opacity: interpolate(frame, [0, 15, 235, 250], [0, 1, 1, 0], {
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
      <Interactive.Span name="文字片段 1" style={{color: '#8A8F99', whiteSpace: 'pre'}}>
        這個模型：
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        單一條 β 鏈的預測
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 來源標籤 F14、F3、F5
const El15: React.FC = () => {
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
      來源 F14、F3、F5
    </Interactive.Div>
  );
};

// 文字：兩種編號
const El16: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 430,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 50,
        fontWeight: 700,
        color: '#1F2430',
        opacity: interpolate(frame, [0, 12, 148, 160], [0, 1, 1, 0], {
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
      <Interactive.Span name="文字片段 1" style={{color: '#8A8F99', whiteSpace: 'pre'}}>
        文獻：
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        成熟蛋白質的編號
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 文字：兩種編號（模型）
const El17: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 530,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 50,
        fontWeight: 700,
        color: '#1F2430',
        opacity: interpolate(frame, [0, 12, 118, 130], [0, 1, 1, 0], {
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
      <Interactive.Span name="文字片段 1" style={{color: '#8A8F99', whiteSpace: 'pre'}}>
        模型：
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        完整序列的編號
      </Interactive.Span>
    </Interactive.Div>
  );
};

// ProtVar 截圖
const El18: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="截圖（位置與動畫）"
      style={{
        position: 'absolute',
        left: 160,
        top: 375,
        width: 1600,
        boxShadow: '0 8px 30px rgba(0,0,0,0.10)',
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
      <Img src={staticFile('protvar_P68871_E6V_crop.png')} style={{width: '100%', display: 'block'}} />
    </Interactive.Div>
  );
};

// 聚焦：改用 Pro 繼續
const El19: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="聚焦框"
      style={{
        position: 'absolute',
        left: 958,
        top: 402,
        width: 367,
        height: 38,
        borderRadius: 8,
        backgroundColor: 'transparent',
        borderWidth: 4,
        borderStyle: 'solid',
        borderColor: '#D9483B',
        opacity: interpolate(frame, [0, 12, 338, 350], [0, 1, 1, 0], {
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

// 聚焦：結果都是 Pro6
const El20: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="聚焦框"
      style={{
        position: 'absolute',
        left: 1172,
        top: 462,
        width: 97,
        height: 426,
        borderRadius: 10,
        backgroundColor: 'transparent',
        borderWidth: 4,
        borderStyle: 'solid',
        borderColor: '#D9483B',
        opacity: interpolate(frame, [0, 12, 238, 250], [0, 1, 1, 0], {
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

// 說明：ProtVar
const El21: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="說明文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 925,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 44,
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
        ProtVar 會警告，但改用
      </Interactive.Span>
      <Interactive.Span name="文字片段 2" style={{color: '#D9483B', whiteSpace: 'pre'}}>
        第 6 個（Pro）
      </Interactive.Span>
      <Interactive.Span name="文字片段 3" style={{color: '#1F2430', whiteSpace: 'pre'}}>
        繼續分析
      </Interactive.Span>
    </Interactive.Div>
  );
};

// 來源標籤 F6、F7
const El22: React.FC = () => {
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
      來源 F6、F7
    </Interactive.Div>
  );
};

// 來源標籤 F10
const El23: React.FC = () => {
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
      來源 F10
    </Interactive.Div>
  );
};

export const S5Limits: React.FC = () => {
  return (
    <AbsoluteFill>
      <Interactive.Div
        name="背景"
        from={0}
        durationInFrames={1530}
        style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, backgroundColor: '#F6F4EF'}}
      />
      <Sequence name="卡片 1" from={0} durationInFrames={1530}>
        <El01 />
      </Sequence>
      <Sequence name="卡片 2" from={0} durationInFrames={1530}>
        <El02 />
      </Sequence>
      <Sequence name="卡片 3" from={0} durationInFrames={1530}>
        <El03 />
      </Sequence>
      <Sequence name="圖：低信心區（橘色）" from={30} durationInFrames={330}>
        <El04 />
      </Sequence>
      <Sequence name="文字：pLDDT < 50" from={50} durationInFrames={310}>
        <El05 />
      </Sequence>
      <Sequence name="文字：座標不應解讀" from={80} durationInFrames={280}>
        <El06 />
      </Sequence>
      <Sequence name="文字：常是無序區" from={110} durationInFrames={250}>
        <El07 />
      </Sequence>
      <Sequence name="來源標籤 F13" from={0} durationInFrames={360}>
        <El08 />
      </Sequence>
      <Sequence name="方塊：E（模型裡的）" from={375} durationInFrames={555}>
        <El09 />
      </Sequence>
      <Sequence name="箭頭" from={405} durationInFrames={525}>
        <El10 />
      </Sequence>
      <Sequence name="方塊：V（虛線，看不到）" from={435} durationInFrames={495}>
        <El11 />
      </Sequence>
      <Sequence name="文字：看不到突變後的形狀" from={470} durationInFrames={460}>
        <El12 />
      </Sequence>
      <Sequence name="引文：未驗證突變影響" from={520} durationInFrames={410}>
        <El13 />
      </Sequence>
      <Sequence name="文字：單一條 β 鏈" from={680} durationInFrames={250}>
        <El14 />
      </Sequence>
      <Sequence name="來源標籤 F14、F3、F5" from={360} durationInFrames={570}>
        <El15 />
      </Sequence>
      <Sequence name="文字：兩種編號" from={945} durationInFrames={160}>
        <El16 />
      </Sequence>
      <Sequence name="文字：兩種編號（模型）" from={975} durationInFrames={130}>
        <El17 />
      </Sequence>
      <Sequence name="ProtVar 截圖" from={1100} durationInFrames={430}>
        <El18 />
      </Sequence>
      <Sequence name="聚焦：改用 Pro 繼續" from={1180} durationInFrames={350}>
        <El19 />
      </Sequence>
      <Sequence name="聚焦：結果都是 Pro6" from={1280} durationInFrames={250}>
        <El20 />
      </Sequence>
      <Sequence name="說明：ProtVar" from={1180} durationInFrames={350}>
        <El21 />
      </Sequence>
      <Sequence name="來源標籤 F6、F7" from={930} durationInFrames={170}>
        <El22 />
      </Sequence>
      <Sequence name="來源標籤 F10" from={1100} durationInFrames={430}>
        <El23 />
      </Sequence>
    </AbsoluteFill>
  );
};
