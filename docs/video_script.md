# 影片講稿與設計腳本（v1）

建立日期：2026-11-24
依據：`docs/video_outline.md`（大綱 v2）、`docs/video_handoff.md`（事實 F1～F12、用詞規則）
本文件新增事實 F13～F18（第一節），以及仍待確認的事項（第二節）

**閱讀方式**
- 第三節是**講稿**：照著念的旁白，每句後面的 `[F#]` 是來源編號，校對時對照第一節或 `video_handoff.md` 第四節
- 第四節是**設計腳本**：每個鏡頭的畫面、動畫重點、畫面文字、要用的 Remotion 畫面或錄影
- 第五節是**錄影清單**：你要在 Mac 上錄的所有畫面
- 錄旁白時，`[F#]` 和 `〔 〕` 裡的提示都不用念

---

## 一、本次新查證的事實

AFDB 的 FAQ 頁面（<https://alphafold.ebi.ac.uk/faq>）由網站程式動態產生。我在 2026-11-24 下載網站程式檔，從中取出 FAQ 原文；以下引文都是原文照抄。

| # | 事實 | 原文 | 校對方法 |
|---|---|---|---|
| F13 | pLDDT < 50 的區域座標不應解讀；這是無序的強力指標：這段在生理狀態下沒有固定結構，或只有成為複合體的一部分時才有結構（解決 U1） | "The 3D coordinates of regions with pLDDT < 50 often have a ribbon-like appearance and should not be interpreted. We show in our paper that pLDDT < 50 is a reasonably strong predictor of disorder, i.e. it suggests such a region is either unstructured in physiological conditions or only structured as part of a complex." | AFDB FAQ → "How confident should I be in a prediction?" |
| F14 | AlphaFold 沒有被驗證能預測突變的影響 | "AlphaFold has not been validated for predicting the effect of mutations. In particular, AlphaFold is not expected to produce an unfolded protein structure given a sequence containing a destabilising point mutation." | AFDB FAQ → "What use cases does AlphaFold not support?" |
| F15 | 搜尋框接受蛋白質名稱、基因名稱、UniProt 編號、物種名稱（解決 U6 的搜尋部分） | "The search bar at the top of the page accepts queries based on protein name …, gene name …, UniProt accession …, or organism name" | AFDB FAQ → "How do I search the database?" |
| F16 | PAE：(x, y) 的顏色代表「以殘基 y 對齊時，殘基 x 的預期位置誤差」；兩個結構域之間 PAE 低 → 相對位置與方向明確；PAE 高 → 不應解讀它們的相對位置（解決 U2） | "The colour at (x, y) indicates AlphaFold's expected position error at residue x if the predicted and true structures were aligned on residue y. If the PAE is generally low for residue pairs x, y from two different domains, it indicates that AlphaFold predicts well-defined relative positions and orientations for them. If the PAE is generally high …, then the relative positions and/or orientations of these domains … are uncertain and should not be interpreted." | AFDB FAQ → "How should I interpret the relative positions of domains?" |
| F17 | pLDDT 四級在網站上的顏色：非常高 `#0053D6`（深藍）、高 `#65CBF3`（淺藍）、低 `#FFDB13`（黃）、非常低 `#FF7D45`（橘） | 網站程式碼：`{min:90,label:"Very high",color:"#0053D6"},{min:70,label:"High",color:"#65CBF3"},{min:50,label:"Low",color:"#FFDB13"},{min:-1/0,label:"Very low",color:"#FF7D45"}` | 打開任一結構頁，看 3D 結構旁的顏色圖例 |
| F18 | 結構可從頁面右上角的選單下載，格式為 mmCIF 或 PDB；點序列檢視器上的殘基，3D 檢視器會顯示該位置（解決 U6 的下載與點選部分） | "Coordinate files can be downloaded from the menu in the top right of the structure page in mmCIF or PDB format." / "… as displayed in the molecule viewer when clicking on a residue in the sequence viewer." | AFDB FAQ → "How can I download a structure prediction?"、"What is included on a structure page for monomers?" |

**pLDDT 分級的一致性**：FAQ 的分級（> 90、70～90、50～70、< 50）與 F1（網站程式的 `getPlddtLevel`）一致。

---

## 二、仍待確認的事項

| # | 事項 | 影響 | 狀態 |
|---|---|---|---|
| U3 | ProtVar 輸入 `P05067 D23N` 是否不警告 | 講稿沒有用到，可略過 | 未查證（這個環境連不上 ProtVar） |
| U4 | 課程是否允許使用 AI 工具 | 誠信 | **需要你確認** |
| U5 | HbS 的聚合機制（去氧時 β6 纈胺酸與相鄰分子的疏水口袋結合） | **講稿已改寫，不再需要** | 只找到搜尋摘要，讀不到原文（PubMed Central 連不上）；講稿改用 F14 說明限制 |
| U7（新） | AFDB 現在會顯示「從文獻自動擷取的殘基與突變註解」（FAQ："How are residue and point mutation annotations generated in AlphaFold DB?"）。HBB 頁面是否已經標出 HbS？標在第 6 個還是第 7 個？ | 如果網站已經在第 7 個標出 HbS，講稿「網站沒有任何提醒」要改成「如果直接照教科書的編號去找，網站不會提醒你編號不同」 | **需要你錄影前在 HBB 頁面確認**（AFDB 網頁擋掉了這個環境的自動瀏覽器，我看不到頁面） |
| U8（新） | PAE 圖的配色（哪個顏色代表誤差小） | 講稿刻意不提顏色 | 錄影時照頁面上的圖例說即可 |

---

## 三、講稿

約 1,050 字（不含標點、來源標記與提示；英文與數字各算一個字），以每分鐘 215 字估算，旁白約 5 分鐘。加上示範時等畫面操作的時間與停頓，全片約 **6 分鐘**，距離 8 分鐘上限還有約 2 分鐘緩衝。如果想講慢一點，或在示範段多停一下，都還有空間。各段字數見每段標題。

### 段 1｜問題（0:00–0:30，約 84 字）

鐮刀型貧血，和血紅素 β 鏈上一個胺基酸的改變有關：麩胺酸，變成了纈胺酸。教科書把它寫成 E6V。[F6]

〔停頓〕

如果我們想知道：這個位置，在蛋白質的立體結構上的哪裡？那附近的結構，可不可信？

這支影片，我們用 AlphaFold DB 來回答。

### 段 2｜工具與輸入（0:30–1:20，約 164 字）

AlphaFold DB 是一個蛋白質結構資料庫，裡面是用 AI 預測的蛋白質立體結構，可以免費查詢和下載。[F2]

使用時，輸入蛋白質名稱、基因名稱，或 UniProt 編號都可以。[F15]

每個結構除了立體座標，還附上兩種信心分數：一種是每個胺基酸各自的 pLDDT，另一種是 PAE，表示兩個區域之間的相對位置有多可靠。[F16]

另外，我們會搭配一個自己寫的小工具。因為文獻的突變編號，不一定對得上模型的編號。它的輸入就是蛋白質加上突變，例如：HBB E6V。

### 段 3｜實際示範（1:20–3:30，約 304 字）

〔3A〕在搜尋框輸入 HBB，點進 P68871 這個條目。畫面中間就是預測的立體結構，顏色代表 pLDDT：深藍色最可信，橘色最不可信。[F1、F17]

〔3B〕照教科書，我們去找第 6 個胺基酸……結果，是 P，脯胺酸，不是 E。網站沒有任何提醒。[F5]〔U7 確認後可能要改這句〕

〔停頓一拍〕

〔3C〕這時候，換我們的工具上場。輸入 HBB E6V。它告訴我們：模型的第 6 個是 P；往後加 1，E7V 就對得上。原因是 UniProt 標註，這個蛋白質開頭的甲硫胺酸會被移除，所以文獻的編號少算了一個。這個建議的證據強度是 medium，這個位置的 pLDDT 是 96.56。[F5、F6、F12]

〔3D〕回到網站，看第 7 個：是 E，深藍色。所以開場的問題有答案了：這個位置的預測結構，可信度非常高。[F1、F5]

〔3E〕工具也可以一次查一整份清單。α1-抗胰蛋白酶缺乏症的兩個突變，Z 型和 S 型，文獻寫在第 342 和第 264 個。工具發現兩個都差 24，剛好是訊號胜肽的長度，證據強度是 strong。[F7；S 型的出處見 `examples/serpina1_alleles.txt`]

〔3F〕最後查 TP53。R175 和 P72，編號都對得上，但信心分數一個是 96.62，一個只有 48.25。這個差別代表什麼？[F4]

### 段 4｜輸出代表什麼（3:30–4:35，約 209 字）

pLDDT 是每個胺基酸的信心分數，從 0 到 100。大於 90 是非常高；70 到 90 是高，主鏈大致可信；50 到 70 是低，要小心；50 以下是非常低。[F1、F13]

TP53 的 R175 是 96.62，非常高。P72 只有 48.25。官方說明指出，50 以下的區域，座標不應該拿來解讀；這通常代表這一段在生理狀態下沒有固定的結構，或者只有和其他分子結合時才有結構。[F4、F13]

頁面下方的 PAE 圖，看的是兩個區域的相對位置：兩個結構域之間的誤差小，它們的相對擺放才可信；誤差大，就不應該解讀。[F16]〔錄影時照圖例說明哪個顏色代表誤差小〕

工具的輸出也很直接：OK 是對得上，XX 是對不上，箭頭後面是建議的位置，括號裡是這個建議有多可信。

### 段 5｜限制與注意（4:35–5:45，約 238 字）

使用 AlphaFold DB，有三件事要注意。

第一，pLDDT 低的區域，不能拿來解讀結構。[F13]

第二，這是正常序列的預測。官方說明寫得很清楚：AlphaFold 沒有被驗證能預測突變的影響。[F14] 所以我們看得到 E 在哪裡，卻看不到它變成 V 之後的樣子。而且這個模型，只是單一條 β 鏈的預測。[F3、F5]

第三，也是最容易忽略的：編號。文獻常用成熟蛋白質的編號，模型用的是完整序列的編號。[F6、F7] 現有工具像 ProtVar 會發出警告，但它會改用錯的位置，繼續分析。[F10]

我們的工具也有限制：如果錯的位置剛好是同一種胺基酸，就偵測不到。例如類澱粉前驅蛋白的 D23N，第 23 個剛好也是 D。單一突變大約有 7 到 9% 會這樣碰巧對上。[F8、F12] 所以，工具的建議是線索，不是結論。

### 段 6｜結尾（5:45–6:05，約 47 字）

整理一下：用 AlphaFold DB 看結構，先確認編號，再看 pLDDT。

我們的工具開源在 GitHub。它只做編號對應，不判斷突變是否致病。

謝謝收看。

---

## 四、設計腳本

**形式**：動畫 = Remotion 動畫（每個元素一條軌道，可在 Studio 編輯）；網頁 = 你錄的 AFDB 網頁；終端 = 你錄的工具指令
**視覺規則**：一次只亮一個重點，其他元素變暗到 25%；藍色 = 重點，紅色 = 對不上，綠色 = 對得上；pLDDT 一律用網站顏色（F17）
**Remotion 畫面名稱**：計畫中的 composition 名稱，已完成的標「✓」

### 段 1｜問題（0:00–0:30）

| 鏡頭 | 時間 | 形式 | 畫面 | 動畫重點 | 畫面文字 |
|---|---|---|---|---|---|
| 1-1 | 0:00–0:09 | 動畫 `S1Question` | 米白底；紅血球圖示從圓形變成鐮刀形 | 形狀變化是唯一的動作 | 鐮刀型貧血 |
| 1-2 | 0:09–0:19 | 動畫 `S1Question` | β 鏈畫成一排胺基酸方塊，其中一格從 E 翻成 V | 只有那一格是藍色，翻轉時放大 | E → V／教科書：E6V |
| 1-3 | 0:19–0:30 | 動畫 `S1Question` | 兩個問題依序出現 | 一次出現一個問題，前一個變暗 | 在結構的哪裡？／可不可信？ |

### 段 2｜工具與輸入（0:30–1:20）

| 鏡頭 | 時間 | 形式 | 畫面 | 動畫重點 | 畫面文字 |
|---|---|---|---|---|---|
| 2-1 | 0:30–0:45 | 動畫 `S2Tool` | 中央：AlphaFold DB 字樣＋一個蛋白質結構剪影 | 剪影用 F17 四色漸層上色 | AlphaFold DB／AI 預測的蛋白質結構 |
| 2-2 | 0:45–0:55 | 動畫 `S2Tool` | 一個搜尋框，三種輸入輪流打字出現 | 打字效果 | HBB／hemoglobin subunit beta／P68871 |
| 2-3 | 0:55–1:10 | 動畫 `S2Tool` | 三張卡片：立體座標、pLDDT、PAE | 依旁白順序逐張點亮 | 結構／每個胺基酸的信心／區域之間的信心 |
| 2-4 | 1:10–1:20 | 動畫 `S2Tool` | 一個終端機視窗輸入 `HBB E6V` | 終端機從右側滑入 | ＋編號檢查工具 |

### 段 3｜實際示範（1:20–3:30）

| 鏡頭 | 時間 | 形式 | 畫面 | 動畫重點（疊在錄影上） | 畫面文字 |
|---|---|---|---|---|---|
| 3A | 1:20–1:52 | 網頁 | AFDB 首頁 → 搜尋 HBB → P68871 頁面 → 旋轉 3D 結構 | 圓圈標出搜尋框、pLDDT 圖例 | — |
| 3B | 1:52–2:09 | 網頁 | 在序列檢視器點第 6 個 | 紅框標出第 6 個 P；**畫面停 1 秒** | 第 6 個是 P？ |
| 3C | 2:09–2:41 | 終端 | `python3 -m af_confidence HBB E6V` 的輸出 | 依旁白順序逐行亮起：`XX` 行 → `E7V matches` → `initiator Met removed` → `[medium]` → `96.56` | — |
| 3C' | 2:33–2:41 | 動畫 `HbSOpeningEditable` ✓（取後半段） | 兩套編號對照 | 已完成的試作：M 劃掉、文獻 6 = 模型 7 | 同一個突變，兩套編號 |
| 3D | 2:41–2:58 | 網頁 | 點第 7 個，3D 結構上該位置被標出 | 綠框標出第 7 個 E；箭頭指向 3D 結構上的位置 | 第 7 個：E，pLDDT 96.56 |
| 3E | 2:58–3:18 | 終端 | `python3 -m af_confidence P01009 E342K E264V` | 亮起兩行 `+24` 與 `[strong]` | 差 24 = 訊號胜肽 |
| 3F | 3:18–3:30 | 終端 | `python3 -m af_confidence P04637 R175H P72R` | 96.62 用深藍、48.25 用橘色標出（F17） | — |

### 段 4｜輸出代表什麼（3:30–4:35）

| 鏡頭 | 時間 | 形式 | 畫面 | 動畫重點 | 畫面文字 |
|---|---|---|---|---|---|
| 4-1 | 3:30–3:53 | 動畫 `S4Plddt` | 一條 0～100 的刻度尺，分成四段 F17 顏色 | 依旁白逐段亮起，其他段變暗 | 非常高 > 90／高 70–90／低 50–70／非常低 < 50 |
| 4-2 | 3:53–4:16 | 動畫 `S4Plddt` | 刻度尺上兩個標記：R175 落在深藍、P72 落在橘色 | 標記從刻度尺上方落下 | R175：96.62／P72：48.25 |
| 4-3 | 4:16–4:26 | 網頁（或截圖） | TP53 頁面的 PAE 圖 | 框出兩個結構域之間的區塊 | 區域之間的相對位置 |
| 4-4 | 4:26–4:35 | 動畫 `S4ToolOutput` | 工具輸出的一行，四個部分分別標註 | 逐一亮起：OK/XX → 箭頭 → 建議位置 → [strong/medium/weak] | 對不對得上／建議位置／可信程度 |

### 段 5｜限制與注意（4:35–5:45）

| 鏡頭 | 時間 | 形式 | 畫面 | 動畫重點 | 畫面文字 |
|---|---|---|---|---|---|
| 5-1 | 4:35–4:47 | 動畫 `S5Limits` | 三張卡片並排，編號 1、2、3 | 第 1 張亮，其他變暗 | ① 低 pLDDT 不解讀 |
| 5-2 | 4:47–5:06 | 動畫 `S5Limits` | 第 2 張亮；卡片上一個 E 方塊，旁邊的 V 是虛線框 | 虛線 V 閃一下，表示「看不到」 | ② 正常序列、單鏈預測，不模擬突變 |
| 5-3 | 5:06–5:26 | 動畫 `S5Limits` ＋ 截圖 | 第 3 張亮；接 ProtVar 截圖（`docs/images/protvar_P68871_E6V.webp`） | 截圖上框出「改用 Pro6 繼續分析」 | ③ 編號：網站不提醒 |
| 5-4 | 5:26–5:45 | 動畫 `S5ToolLimit` | APP 序列：第 23 個是 D，正確的第 694 個也是 D | 兩個 D 同時亮，中間一個「＝」 | 碰巧對上，偵測不到／約 7–9% |

### 段 6｜結尾（5:45–6:05）

| 鏡頭 | 時間 | 形式 | 畫面 | 動畫重點 | 畫面文字 |
|---|---|---|---|---|---|
| 6-1 | 5:45–5:55 | 動畫 `S6Outro` | 兩個步驟：① 確認編號 → ② 看 pLDDT | 箭頭從 ① 畫到 ② | 先確認編號，再看 pLDDT |
| 6-2 | 5:55–6:05 | 動畫 `S6Outro` | GitHub 網址 | 淡入 | github.com/wangnick1004/af-confidence／只做編號對應，不判斷致病性 |

---

## 五、錄影清單（你在 Mac 上錄）

| 錄影 | 內容 | 注意 |
|---|---|---|
| R1 | AFDB：首頁 → 搜尋 HBB → P68871 頁面 → 旋轉結構 → 點第 6 個 → 點第 7 個 | 先確認 U7；錄影時滑鼠移動慢一點，方便之後加標註 |
| R2 | 終端：`python3 -m af_confidence HBB E6V` | 用大字級（⌘ + 放大），背景單純 |
| R3 | 終端：`python3 -m af_confidence P01009 E342K E264V` | 同上 |
| R4 | 終端：`python3 -m af_confidence P04637 R175H P72R` | 同上 |
| R5 | AFDB：TP53（P04637）頁面的 PAE 圖 | 截圖也可以 |
| R6 | 旁白 | 照第三節逐段錄，每段一個檔案，方便對齊動畫 |

**錄影前在 Mac 上先跑一次 R2～R4**，確認輸出和第三節一致（我在雲端環境跑過 R3、R4，以及用 P68871 代替 HBB 的 R2，輸出一致）。

---

## 六、用詞檢查（對照 `video_handoff.md` 第七節）

| 規則 | 講稿中的處理 |
|---|---|
| 不說「致病」「無害」「破壞結構」 | 只說「和……有關」「突變的影響」；結尾明說工具不判斷致病性 |
| 不說「AFDB 只有單體」 | 說「這個模型，只是單一條 β 鏈的預測」 |
| 不說「現有工具都不會檢查」 | 說「ProtVar 會發出警告，但會改用錯的位置繼續分析」 |
| 不說低 pLDDT 是「AI 預測錯誤」 | 說「座標不應該拿來解讀；通常代表沒有固定結構」（F13） |
| 工具的建議是線索，不是結論 | 段 5 最後一句 |
| 不講歷史、DeepMind、諾貝爾獎 | 全片沒有提到 |
