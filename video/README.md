# 影片動畫（Remotion）

## 在 Mac 上預覽與輸出

```bash
cd ~/af-confidence/video
npm install
npm run studio    # 在瀏覽器開啟預覽，可拖時間軸、即時看修改
npm run render    # 輸出 out/HbSOpening.mp4
```

## 改風格時看哪裡

- `src/theme.ts`：顏色、字型、動畫柔和度、非重點元素變暗的程度
- `src/scenes/HbSOpening.tsx` 開頭的 `B`：每個段落開始的格數（30 格 = 1 秒），改這裡調整節奏
- `src/components/primitives.tsx`：字幕、來源標籤的樣式

右下角的「來源 F5、F6」對應 `docs/video_handoff.md` 第四節，方便校對；正式版可以關掉。
