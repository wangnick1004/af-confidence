// 段 2｜工具與輸入（設計腳本鏡頭 2-1～2-4）
// 事實來源：F2（免費、CC-BY-4.0）、F15（搜尋方式）、F16（pLDDT 與 PAE）
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

export const S2TOOL_DURATION = 1500; // 50.0 秒 @ 30fps

// 標題：AlphaFold DB
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
        fontSize: 120,
        fontWeight: 700,
        color: '#1F2430',
        opacity: interpolate(frame, [0, 12, 435, 450], [0, 1, 1, 0], {
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
      AlphaFold DB
    </Interactive.Div>
  );
};

// 副標：AI 預測的結構
const El02: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="副標文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 340,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 52,
        fontWeight: 400,
        color: '#8A8F99',
        opacity: interpolate(frame, [0, 12, 405, 420], [0, 1, 1, 0], {
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
      AI 預測的蛋白質立體結構
    </Interactive.Div>
  );
};

// 結構示意（pLDDT 配色）
const El03: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="結構示意圖"
      style={{
        position: 'absolute',
        left: 360,
        top: 470,
        width: 1200,
        height: 260,
        opacity: interpolate(frame, [0, 25, 375, 390], [0, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
        transformOrigin: 'left center',
        scale: interpolate(frame, [0, 40], ['0 1', '1 1'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          output: 'perceptual-scale',
          outputType: 'scale',
        }),
      }}
    >
      <svg width="1200" height="260" viewBox="0 0 1200 260">
        <defs>
          <linearGradient id="plddt" x1="0" x2="1">
            <stop offset="0" stop-color="#FF7D45" />
            <stop offset="0.3" stop-color="#FFDB13" />
            <stop offset="0.6" stop-color="#65CBF3" />
            <stop offset="1" stop-color="#0053D6" />
          </linearGradient>
        </defs>
        <path
          d="M30,130 C130,20 200,240 300,130 S470,20 570,130 S740,240 840,130 S1010,20 1170,130"
          fill="none"
          stroke="url(#plddt)"
          stroke-width="30"
          stroke-linecap="round"
        />
      </svg>
    </Interactive.Div>
  );
};

// 標籤：免費查詢與下載
const El04: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="標籤文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 820,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 40,
        fontWeight: 400,
        color: '#1F2430',
        opacity: interpolate(frame, [0, 12, 285, 300], [0, 1, 1, 0], {
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
      免費查詢與下載（CC-BY-4.0）
    </Interactive.Div>
  );
};

// 來源標籤 F2
const El05: React.FC = () => {
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
      來源 F2
    </Interactive.Div>
  );
};

// 標籤：輸入
const El06: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="標籤文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 230,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 44,
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
      輸入
    </Interactive.Div>
  );
};

// 搜尋框
const El07: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="搜尋框外框"
      style={{
        position: 'absolute',
        left: 460,
        top: 330,
        width: 1000,
        height: 130,
        borderRadius: 65,
        backgroundColor: '#FFFFFF',
        boxShadow: '0 8px 30px rgba(0,0,0,0.08)',
        opacity: interpolate(frame, [0, 15, 288, 300], [0, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
            Easing.bezier(0.33, 0, 0.2, 1),
          ],
        }),
      }}
    />
  );
};

// 輸入：HBB
const El08: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="打字區（超出部分隱藏）"
      style={{
        position: 'absolute',
        left: 520,
        top: 345,
        width: 880,
        height: 100,
        overflow: 'hidden',
        opacity: interpolate(frame, [0, 1, 90, 100], [0, 1, 1, 0], {
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
      <Interactive.Div
        name="輸入文字"
        style={{
          position: 'absolute',
          left: 0,
          top: 18,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 54,
          color: '#1F2430',
          whiteSpace: 'pre',
          fontVariantLigatures: 'none',
        }}
      >
        HBB
      </Interactive.Div>
      <Interactive.Div
        name="遮蓋塊（往右移＝打字）"
        style={{
          position: 'absolute',
          left: 0,
          top: 0,
          width: 900,
          height: 100,
          backgroundColor: '#FFFFFF',
          translate: interpolate(frame, [5, 14], ['0px 0px', '900px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      />
    </Interactive.Div>
  );
};

// 說明：基因名稱
const El09: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="說明文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 510,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 44,
        fontWeight: 700,
        color: '#2F6FEB',
        opacity: interpolate(frame, [0, 12, 90, 100], [0, 1, 1, 0], {
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
      基因名稱
    </Interactive.Div>
  );
};

// 輸入：hemoglobin subunit beta
const El10: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="打字區（超出部分隱藏）"
      style={{
        position: 'absolute',
        left: 520,
        top: 345,
        width: 880,
        height: 100,
        overflow: 'hidden',
        opacity: interpolate(frame, [0, 1, 90, 100], [0, 1, 1, 0], {
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
      <Interactive.Div
        name="輸入文字"
        style={{
          position: 'absolute',
          left: 0,
          top: 18,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 54,
          color: '#1F2430',
          whiteSpace: 'pre',
          fontVariantLigatures: 'none',
        }}
      >
        hemoglobin subunit beta
      </Interactive.Div>
      <Interactive.Div
        name="遮蓋塊（往右移＝打字）"
        style={{
          position: 'absolute',
          left: 0,
          top: 0,
          width: 900,
          height: 100,
          backgroundColor: '#FFFFFF',
          translate: interpolate(frame, [5, 74], ['0px 0px', '900px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      />
    </Interactive.Div>
  );
};

// 說明：蛋白質名稱
const El11: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="說明文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 510,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 44,
        fontWeight: 700,
        color: '#2F6FEB',
        opacity: interpolate(frame, [0, 12, 90, 100], [0, 1, 1, 0], {
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
      蛋白質名稱
    </Interactive.Div>
  );
};

// 輸入：P68871
const El12: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="打字區（超出部分隱藏）"
      style={{
        position: 'absolute',
        left: 520,
        top: 345,
        width: 880,
        height: 100,
        overflow: 'hidden',
        opacity: interpolate(frame, [0, 1, 50, 60], [0, 1, 1, 0], {
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
      <Interactive.Div
        name="輸入文字"
        style={{
          position: 'absolute',
          left: 0,
          top: 18,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 54,
          color: '#1F2430',
          whiteSpace: 'pre',
          fontVariantLigatures: 'none',
        }}
      >
        P68871
      </Interactive.Div>
      <Interactive.Div
        name="遮蓋塊（往右移＝打字）"
        style={{
          position: 'absolute',
          left: 0,
          top: 0,
          width: 900,
          height: 100,
          backgroundColor: '#FFFFFF',
          translate: interpolate(frame, [5, 23], ['0px 0px', '900px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: [Easing.bezier(0.33, 0, 0.2, 1)],
            outputType: 'translate',
          }),
        }}
      />
    </Interactive.Div>
  );
};

// 說明：UniProt 編號
const El13: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="說明文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 510,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 44,
        fontWeight: 700,
        color: '#2F6FEB',
        opacity: interpolate(frame, [0, 12, 50, 60], [0, 1, 1, 0], {
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
      UniProt 編號
    </Interactive.Div>
  );
};

// 來源標籤 F15
const El14: React.FC = () => {
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
      來源 F15
    </Interactive.Div>
  );
};

// 卡片 1：立體座標
const El15: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="卡片：立體座標"
      style={{
        position: 'absolute',
        left: 230,
        top: 300,
        width: 440,
        height: 420,
        borderRadius: 18,
        backgroundColor: '#FFFFFF',
        boxShadow: '0 8px 30px rgba(0,0,0,0.06)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 26,
        opacity: interpolate(frame, [0, 15, 40, 55], [0, 0.3, 0.3, 1], {
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
      <Interactive.Div name="圖示" style={{width: 200, height: 110}}>
        <svg width="200" height="110" viewBox="0 0 200 110">
          <path
            d="M10,60 C40,0 60,110 100,55 S160,0 190,55"
            fill="none"
            stroke="#1F2430"
            stroke-width="12"
            stroke-linecap="round"
          />
        </svg>
      </Interactive.Div>
      <Interactive.Div
        name="卡片標題"
        style={{fontFamily: "'Noto Sans TC', sans-serif", fontSize: 52, fontWeight: 700, color: '#1F2430'}}
      >
        立體座標
      </Interactive.Div>
      <Interactive.Div
        name="卡片說明"
        style={{fontFamily: "'Noto Sans TC', sans-serif", fontSize: 32, color: '#8A8F99'}}
      >
        蛋白質的 3D 結構
      </Interactive.Div>
    </Interactive.Div>
  );
};

// 卡片 2：pLDDT
const El16: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="卡片：pLDDT"
      style={{
        position: 'absolute',
        left: 740,
        top: 300,
        width: 440,
        height: 420,
        borderRadius: 18,
        backgroundColor: '#FFFFFF',
        boxShadow: '0 8px 30px rgba(0,0,0,0.06)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 26,
        opacity: interpolate(frame, [0, 15, 140, 155], [0, 0.3, 0.3, 1], {
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
      <Interactive.Div name="圖示" style={{width: 200, height: 110}}>
        <svg width="200" height="110" viewBox="0 0 200 110">
          <rect x="0" y="35" width="50" height="40" fill="#FF7D45" />
          <rect x="50" y="35" width="50" height="40" fill="#FFDB13" />
          <rect x="100" y="35" width="50" height="40" fill="#65CBF3" />
          <rect x="150" y="35" width="50" height="40" fill="#0053D6" />
        </svg>
      </Interactive.Div>
      <Interactive.Div
        name="卡片標題"
        style={{fontFamily: "'Noto Sans TC', sans-serif", fontSize: 52, fontWeight: 700, color: '#1F2430'}}
      >
        pLDDT
      </Interactive.Div>
      <Interactive.Div
        name="卡片說明"
        style={{fontFamily: "'Noto Sans TC', sans-serif", fontSize: 32, color: '#8A8F99'}}
      >
        每個胺基酸的信心分數
      </Interactive.Div>
    </Interactive.Div>
  );
};

// 卡片 3：PAE
const El17: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="卡片：PAE"
      style={{
        position: 'absolute',
        left: 1250,
        top: 300,
        width: 440,
        height: 420,
        borderRadius: 18,
        backgroundColor: '#FFFFFF',
        boxShadow: '0 8px 30px rgba(0,0,0,0.06)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 26,
        opacity: interpolate(frame, [0, 15, 260, 275], [0, 0.3, 0.3, 1], {
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
      <Interactive.Div name="圖示" style={{width: 200, height: 110}}>
        <svg width="200" height="110" viewBox="0 0 110 110">
          <rect x="0" y="0" width="21" height="21" fill="#3C4352" />
          <rect x="22" y="0" width="21" height="21" fill="#3C4352" />
          <rect x="44" y="0" width="21" height="21" fill="#C9CDD6" />
          <rect x="66" y="0" width="21" height="21" fill="#C9CDD6" />
          <rect x="88" y="0" width="21" height="21" fill="#C9CDD6" />
          <rect x="0" y="22" width="21" height="21" fill="#3C4352" />
          <rect x="22" y="22" width="21" height="21" fill="#3C4352" />
          <rect x="44" y="22" width="21" height="21" fill="#3C4352" />
          <rect x="66" y="22" width="21" height="21" fill="#C9CDD6" />
          <rect x="88" y="22" width="21" height="21" fill="#C9CDD6" />
          <rect x="0" y="44" width="21" height="21" fill="#C9CDD6" />
          <rect x="22" y="44" width="21" height="21" fill="#3C4352" />
          <rect x="44" y="44" width="21" height="21" fill="#3C4352" />
          <rect x="66" y="44" width="21" height="21" fill="#3C4352" />
          <rect x="88" y="44" width="21" height="21" fill="#C9CDD6" />
          <rect x="0" y="66" width="21" height="21" fill="#C9CDD6" />
          <rect x="22" y="66" width="21" height="21" fill="#C9CDD6" />
          <rect x="44" y="66" width="21" height="21" fill="#3C4352" />
          <rect x="66" y="66" width="21" height="21" fill="#3C4352" />
          <rect x="88" y="66" width="21" height="21" fill="#3C4352" />
          <rect x="0" y="88" width="21" height="21" fill="#C9CDD6" />
          <rect x="22" y="88" width="21" height="21" fill="#C9CDD6" />
          <rect x="44" y="88" width="21" height="21" fill="#C9CDD6" />
          <rect x="66" y="88" width="21" height="21" fill="#3C4352" />
          <rect x="88" y="88" width="21" height="21" fill="#3C4352" />
        </svg>
      </Interactive.Div>
      <Interactive.Div
        name="卡片標題"
        style={{fontFamily: "'Noto Sans TC', sans-serif", fontSize: 52, fontWeight: 700, color: '#1F2430'}}
      >
        PAE
      </Interactive.Div>
      <Interactive.Div
        name="卡片說明"
        style={{fontFamily: "'Noto Sans TC', sans-serif", fontSize: 32, color: '#8A8F99'}}
      >
        兩個區域之間的相對位置
      </Interactive.Div>
    </Interactive.Div>
  );
};

// 來源標籤 F16
const El18: React.FC = () => {
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
      來源 F16
    </Interactive.Div>
  );
};

// 終端機：HBB E6V
const El19: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="終端機視窗"
      style={{
        position: 'absolute',
        left: 360,
        top: 300,
        width: 1200,
        height: 280,
        borderRadius: 20,
        backgroundColor: '#1E2230',
        translate: interpolate(frame, [0, 25], ['700px 0px', '0px 0px'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
          outputType: 'translate',
        }),
        opacity: interpolate(frame, [0, 15], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: [Easing.bezier(0.33, 0, 0.2, 1)],
        }),
        boxShadow: '0 12px 40px rgba(0,0,0,0.18)',
      }}
    >
      <Interactive.Div
        name="視窗按鈕"
        style={{position: 'absolute', left: 28, top: 22, fontSize: 26, color: '#5B6275', letterSpacing: 6}}
      >
        ● ● ●
      </Interactive.Div>
      <Interactive.Div
        name="指令"
        style={{
          position: 'absolute',
          left: 50,
          top: 120,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 44,
          color: '#E6E9EF',
          whiteSpace: 'pre',
          fontVariantLigatures: 'none',
        }}
      >
        <Interactive.Span name="文字片段 1" style={{color: '#8A8F99', whiteSpace: 'pre'}}>
          ${' '}
        </Interactive.Span>
        <Interactive.Span name="文字片段 2" style={{color: '#E6E9EF', whiteSpace: 'pre'}}>
          python3 -m af_confidence{' '}
        </Interactive.Span>
        <Interactive.Span name="文字片段 3" style={{color: '#65CBF3', whiteSpace: 'pre'}}>
          HBB E6V
        </Interactive.Span>
      </Interactive.Div>
    </Interactive.Div>
  );
};

// 標籤：編號檢查工具
const El20: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="標籤文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 660,
        width: 1920,
        textAlign: 'center',
        fontFamily: "'Noto Sans TC', sans-serif",
        fontSize: 56,
        fontWeight: 700,
        color: '#2F6FEB',
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
      ＋ 我們的編號檢查工具
    </Interactive.Div>
  );
};

// 說明：檢查編號
const El21: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="說明文字"
      style={{
        position: 'absolute',
        left: 0,
        top: 760,
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
      檢查文獻的突變編號，在模型上對不對得上
    </Interactive.Div>
  );
};

export const S2Tool: React.FC = () => {
  return (
    <AbsoluteFill>
      <Interactive.Div
        name="背景"
        from={0}
        durationInFrames={1500}
        style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, backgroundColor: '#F6F4EF'}}
      />
      <Sequence name="標題：AlphaFold DB" from={0} durationInFrames={450}>
        <El01 />
      </Sequence>
      <Sequence name="副標：AI 預測的結構" from={30} durationInFrames={420}>
        <El02 />
      </Sequence>
      <Sequence name="結構示意（pLDDT 配色）" from={60} durationInFrames={390}>
        <El03 />
      </Sequence>
      <Sequence name="標籤：免費查詢與下載" from={150} durationInFrames={300}>
        <El04 />
      </Sequence>
      <Sequence name="來源標籤 F2" from={0} durationInFrames={450}>
        <El05 />
      </Sequence>
      <Sequence name="標籤：輸入" from={450} durationInFrames={300}>
        <El06 />
      </Sequence>
      <Sequence name="搜尋框" from={450} durationInFrames={300}>
        <El07 />
      </Sequence>
      <Sequence name="輸入：HBB" from={470} durationInFrames={100}>
        <El08 />
      </Sequence>
      <Sequence name="說明：基因名稱" from={470} durationInFrames={100}>
        <El09 />
      </Sequence>
      <Sequence name="輸入：hemoglobin subunit beta" from={580} durationInFrames={100}>
        <El10 />
      </Sequence>
      <Sequence name="說明：蛋白質名稱" from={580} durationInFrames={100}>
        <El11 />
      </Sequence>
      <Sequence name="輸入：P68871" from={690} durationInFrames={60}>
        <El12 />
      </Sequence>
      <Sequence name="說明：UniProt 編號" from={690} durationInFrames={60}>
        <El13 />
      </Sequence>
      <Sequence name="來源標籤 F15" from={450} durationInFrames={300}>
        <El14 />
      </Sequence>
      <Sequence name="卡片 1：立體座標" from={750} durationInFrames={450}>
        <El15 />
      </Sequence>
      <Sequence name="卡片 2：pLDDT" from={750} durationInFrames={450}>
        <El16 />
      </Sequence>
      <Sequence name="卡片 3：PAE" from={750} durationInFrames={450}>
        <El17 />
      </Sequence>
      <Sequence name="來源標籤 F16" from={750} durationInFrames={450}>
        <El18 />
      </Sequence>
      <Sequence name="終端機：HBB E6V" from={1200} durationInFrames={300}>
        <El19 />
      </Sequence>
      <Sequence name="標籤：編號檢查工具" from={1230} durationInFrames={270}>
        <El20 />
      </Sequence>
      <Sequence name="說明：檢查編號" from={1260} durationInFrames={240}>
        <El21 />
      </Sequence>
    </AbsoluteFill>
  );
};
