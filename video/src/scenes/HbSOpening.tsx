// 試樣：HbS 開場（影片第一段「問題」的前半）
// 事實來源：F5（AFDB 模型序列開頭 MVHLTPEEK）、F6（UniProt：HbS 標在第 7 個；起始 M 標為 Removed）
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {theme} from '../theme';
import {Caption, SourceTag, useEnter, useWindow} from '../components/primitives';

export const HBS_DURATION = 960; // 32 秒 @ 30fps

// 每個段落（beat）的開始格數，改這裡就能調整節奏
const B = {
  intro: 0,
  sequence: 135,
  focus6: 330,
  focus7: 480,
  explain: 630,
  takeaway: 840,
};

const SEQ = ['M', 'V', 'H', 'L', 'T', 'P', 'E', 'E', 'K'];
const BOX = 120;
const GAP = 22;
const ROW_W = SEQ.length * BOX + (SEQ.length - 1) * GAP;

export const HbSOpening: React.FC = () => {
  const frame = useCurrentFrame();
  const c = theme.color;

  // ---- 開場的大字 E6V：先置中，再縮小移到左上當「查詢條件」
  const introIn = useEnter(B.intro + 10, 25);
  const moveUp = useEnter(B.sequence, 30);
  const titleScale = interpolate(moveUp, [0, 1], [1, 0.42]);
  const titleX = interpolate(moveUp, [0, 1], [0, -620]);
  const titleY = interpolate(moveUp, [0, 1], [-40, -390]);
  const subtitleO = useWindow(B.intro + 35, B.sequence + 10);

  // ---- 聚光燈：目前要看哪一格
  const focus6 = useWindow(B.focus6, B.focus7 + 6, 14);
  const focus7 = useWindow(B.focus7, B.explain + 6, 14);
  const explain = useEnter(B.explain, 30);
  const anyFocus = Math.max(focus6, focus7);

  // 文獻的數法（去掉 M 之後從 V 開始數）
  const litRow = useEnter(B.explain + 40, 30);
  // 把兩套編號接起來：文獻的 6 = 模型的 7
  const link = useWindow(B.explain + 110, B.takeaway + 200, 14);
  const takeaway = useEnter(B.takeaway, 30);

  const rowLeft = (1920 - ROW_W) / 2;
  const rowTop = 430;

  return (
    <AbsoluteFill style={{backgroundColor: c.bg, fontFamily: theme.font.sans, color: c.ink}}>
      {/* 開場標題 */}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            transform: `translate(${titleX}px, ${titleY}px) scale(${titleScale})`,
            opacity: introIn,
            textAlign: 'center',
          }}
        >
          <div style={{fontSize: 52, color: c.muted, marginBottom: 12}}>鐮刀型貧血 HbS</div>
          <div style={{fontFamily: theme.font.mono, fontSize: 240, fontWeight: 700, letterSpacing: 8}}>
            <span style={{color: c.ink}}>E</span>
            <span style={{color: c.accent}}>6</span>
            <span style={{color: c.ink}}>V</span>
          </div>
        </div>
      </AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          top: 760,
          width: '100%',
          textAlign: 'center',
          fontSize: 50,
          opacity: subtitleO,
        }}
      >
        教科書：第 <b style={{color: c.accent}}>6</b> 個胺基酸，E 變成 V
      </div>

      {/* 序列 */}
      <div
        style={{
          position: 'absolute',
          left: rowLeft,
          top: rowTop - 170,
          fontSize: 34,
          color: c.muted,
          opacity: useEnter(B.sequence + 20, 20),
        }}
      >
        AlphaFold DB 模型（P68871）序列開頭
      </div>
      {SEQ.map((aa, i) => {
        const pos = i + 1;
        const appear = useEnter(B.sequence + 30 + i * 6, 18);
        const isLink = pos === 7 && link > 0.01;
        const isFocus = (pos === 6 && focus6 > 0.01) || (pos === 7 && focus7 > 0.01) || isLink;
        const strength = pos === 6 ? focus6 : pos === 7 ? Math.max(focus7, link) : 0;
        const ring = pos === 6 ? c.bad : isLink ? c.accent : c.good;
        // M 在解釋段被劃掉
        const mStrike = pos === 1 ? explain : 0;
        let opacity = appear * interpolate(Math.max(anyFocus, link), [0, 1], [1, isFocus ? 1 : theme.dimOpacity]);
        if (pos === 1) opacity *= interpolate(mStrike, [0, 1], [1, 0.35]);
        const x = rowLeft + i * (BOX + GAP);
        return (
          <div key={i} style={{position: 'absolute', left: x, top: rowTop, opacity}}>
            <div
              style={{
                width: BOX,
                height: BOX,
                borderRadius: 18,
                background: c.card,
                boxShadow: '0 6px 20px rgba(0,0,0,0.06)',
                border: `5px solid ${isFocus ? ring : 'transparent'}`,
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                fontFamily: theme.font.mono,
                fontSize: 72,
                fontWeight: 700,
                transform: `translateY(${(1 - appear) * 30}px) scale(${1 + strength * 0.12})`,
                position: 'relative',
              }}
            >
              {aa}
              {pos === 1 && (
                <div
                  style={{
                    position: 'absolute',
                    left: 14,
                    right: 14,
                    top: '50%',
                    height: 6,
                    background: c.bad,
                    transformOrigin: 'left',
                    transform: `scaleX(${mStrike})`,
                  }}
                />
              )}
            </div>
            {/* 模型的編號 */}
            <div
              style={{
                width: BOX,
                textAlign: 'center',
                marginTop: 14,
                fontFamily: theme.font.mono,
                fontSize: 36,
                color: isFocus ? ring : c.muted,
                fontWeight: isFocus ? 700 : 500,
              }}
            >
              {pos}
            </div>
            {/* 文獻的編號（從 V 開始） */}
            {pos > 1 && (
              <div
                style={{
                  position: 'absolute',
                  top: -64,
                  width: BOX,
                  textAlign: 'center',
                  fontFamily: theme.font.mono,
                  fontSize: 36,
                  fontWeight: 700,
                  color: c.accent,
                  opacity: litRow,
                  transform: `translateY(${(1 - litRow) * 12}px)`,
                }}
              >
                {pos - 1}
              </div>
            )}
          </div>
        );
      })}

      {/* 兩排編號的標籤 */}
      <div
        style={{
          position: 'absolute',
          left: rowLeft - 260,
          top: rowTop - 60,
          width: 230,
          textAlign: 'right',
          fontSize: 30,
          color: c.accent,
          opacity: litRow,
        }}
      >
        文獻的數法
      </div>
      <div
        style={{
          position: 'absolute',
          left: rowLeft - 260,
          top: rowTop + BOX + 18,
          width: 230,
          textAlign: 'right',
          fontSize: 30,
          color: c.muted,
          opacity: litRow,
        }}
      >
        模型的數法
      </div>

      {/* 一次一句的字幕 */}
      <Caption from={B.focus6 + 10} to={B.focus7}>
        模型的第 6 個是 <span style={{color: c.bad}}>P</span>，不是 E
      </Caption>
      <Caption from={B.focus7 + 10} to={B.explain}>
        E 在第 <span style={{color: c.good}}>7</span> 個
      </Caption>
      <Caption from={B.explain + 10} to={B.takeaway}>
        成熟的蛋白質去掉了開頭的 M，文獻從 V 開始數
      </Caption>
      <Caption from={B.takeaway + 5} to={HBS_DURATION + 20}>
        <span style={{opacity: takeaway}}>
          同一個突變，<span style={{color: c.accent}}>兩套編號</span>
        </span>
      </Caption>

      <SourceTag ids={frame < B.sequence ? 'F6' : 'F5、F6'} />
    </AbsoluteFill>
  );
};
