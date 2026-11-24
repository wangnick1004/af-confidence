# 影片動畫（Remotion）

## 在 Mac 上預覽與輸出

```bash
cd ~/af-confidence/video
npm install
npm run studio    # 在瀏覽器開啟 Remotion Studio
npm run render    # 輸出 out/HbSOpeningEditable.mp4（其他段落見下方）
```

## 所有動畫（依影片順序）

| 名稱 | 對應設計腳本 | 長度 |
|---|---|---|
| `S1Question` | 段 1｜問題（鏡頭 1-1～1-3） | 30 秒 |
| `S2Tool` | 段 2｜工具與輸入（鏡頭 2-1～2-4） | 50 秒 |
| `HbSOpeningEditable` | 段 3｜鏡頭 3C'（兩套編號對照） | 32 秒 |
| `S4Plddt` | 段 4｜pLDDT 分級與 TP53 對比（鏡頭 4-1、4-2） | 46 秒 |
| `S4ToolOutput` | 段 4｜工具輸出怎麼讀（鏡頭 4-4） | 10 秒 |
| `S5Limits` | 段 5｜三個限制（鏡頭 5-1～5-3） | 51 秒 |
| `S5ToolLimit` | 段 5｜工具本身的限制（鏡頭 5-4） | 19 秒 |
| `S6Outro` | 段 6｜結尾（鏡頭 6-1、6-2） | 20 秒 |
| `HbSOpening`（「舊版試樣」資料夾） | 第一版試樣，無法在 Studio 編輯 | 32 秒 |

設計腳本見 `docs/video_script.md` 第四節。動畫的時間是照講稿估的，**錄好旁白後，請在 Studio 裡拖動片段對齊旁白**。

輸出單一段動畫：

```bash
npx remotion render src/index.ts S2Tool out/S2Tool.mp4
```

## 產生器（`generator/`）

`S1Question`～`S6Outro` 是用 `generator/scenes.py` 產生的初始檔。**產生器只在第一次建立時使用**：重新執行會覆蓋 `src/scenes/` 裡的檔案，包括你在 Studio 做的修改。之後請直接在 Studio 或 `.tsx` 檔裡修改。

## 在 Studio 裡編輯 `HbSOpeningEditable`

以下操作都已實際測試過，修改會**直接存回** `src/scenes/HbSOpeningEditable.tsx`：

| 想改什麼 | 怎麼做 |
|---|---|
| 元素出現的時間 | 在下方時間軸**拖動藍色片段**；元素裡的動畫會整個跟著移動 |
| 元素的長度 | 拖動片段的左右邊緣 |
| 文字內容 | 在左側軌道列表點選元素（例如「文字片段 2」），右側面板最下方的 **Text** 欄直接輸入 |
| 顏色、字級、粗細 | 點選元素，右側面板的 **Text** 區 |
| 位置、縮放、旋轉、透明度 | 點選元素，右側面板的 **Transform** 區（Offset = 位置） |
| 動畫（關鍵影格） | Transform 區每個欄位前的 ◆ 可新增關鍵影格；◀ ▶ 跳到前後一個關鍵影格 |
| 圖層上下順序 | 軌道列表中越下面的元素畫在越上層 |
| 暫時隱藏某個元素 | 軌道列表左邊的眼睛圖示 |

### 注意事項

- 如果時間軸只出現一條 `<AbsoluteFill>`，旁邊有 `+30` 之類的數字：代表 Studio 找不到元素在程式碼裡的位置。`remotion.config.ts` 已經修正這個問題；請確認已經 `git pull` 到最新版，並**重新啟動** `npm run studio`（在終端機按 `Ctrl + C` 停止後再執行一次）。

- **子元素要在播放頭位於該片段時間範圍內時才會展開**。例如「序列方塊與模型編號」從 5.5 秒開始，播放頭停在 0 秒時看不到裡面的「方塊 1：M」；把播放頭移到 6 秒以後就會出現。
- 元素的**淡出**動畫是寫死在片段結尾前 12～14 格；如果把片段拉長，淡出不會自動跟著移到新的結尾，要在 Opacity 的關鍵影格上手動移動最後兩個點。
- 一段文字裡有不同顏色時，拆成幾個「文字片段」，每段各自改文字與顏色。
- 「變暗遮罩」是一塊和背景同色、半透明的方塊，蓋在序列上讓其他格子變暗；「聚焦」元素再畫在遮罩上面。想改變暗程度，調整遮罩的 Opacity。
- 改壞了可以用 Studio 的復原（⌘Z），或在終端機執行 `git checkout src/scenes/HbSOpeningEditable.tsx` 回到上一次存的版本。

右下角的「來源 F5、F6」對應 `docs/video_handoff.md` 第四節，方便校對；正式版可以在軌道列表把它隱藏或刪除。
