// 風格設定集中在這裡：改顏色、字型、節奏，所有畫面一起變。
// 字型打包在專案裡（npm 套件），離線也能輸出
import '@fontsource/noto-sans-tc/400.css';
import '@fontsource/noto-sans-tc/700.css';
import '@fontsource/jetbrains-mono/500.css';
import '@fontsource/jetbrains-mono/700.css';

const sans = {fontFamily: "'Noto Sans TC', sans-serif"};
const mono = {fontFamily: "'JetBrains Mono', monospace"};

export const theme = {
  font: {sans: sans.fontFamily, mono: mono.fontFamily},
  color: {
    bg: '#F6F4EF', // 米白底
    ink: '#1F2430', // 主要文字
    muted: '#8A8F99', // 次要、變暗的元素
    accent: '#2F6FEB', // 重點（藍）
    good: '#1E9E6A', // 對得上
    bad: '#D9483B', // 對不上
    card: '#FFFFFF',
  },
  // 節奏：數字越大越慢、越柔和
  spring: {damping: 200, mass: 1},
  dimOpacity: 0.25, // 非重點元素變暗的程度
};

// 等字型載入完成再開始畫，避免輸出時出現備用字型
import {continueRender, delayRender} from 'remotion';
if (typeof document !== 'undefined') {
  const handle = delayRender('Loading fonts');
  Promise.all([
    document.fonts.load("400 40px 'Noto Sans TC'", '鐮刀型貧血教科書胺基酸'),
    document.fonts.load("700 40px 'Noto Sans TC'", '模型的第個是不在'),
    document.fonts.load("700 40px 'JetBrains Mono'", 'E6V'),
    document.fonts.load("500 40px 'JetBrains Mono'", '123'),
  ]).then(() => document.fonts.ready).then(() => continueRender(handle));
}
