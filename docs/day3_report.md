# 第三天報告：證據強度、批次清單、巧合偵測

日期：2026-11-19
結論：**v0.1 功能完成，44 個測試在 Python 3.9～3.13 全部通過。** 影片的示範指令稿已準備好（`docs/demo_commands.md`）。

---

## 一、今天完成的事

| 項目 | 說明 |
|---|---|
| 證據強度分級 | 每個建議標示 strong／medium／weak，有強證據時隱藏弱證據 |
| 讀取突變清單檔 | `-f 檔案`，一行一個或多個突變，`#` 之後是註解（可註明出處） |
| 巧合偵測（`ambiguous_match`） | 照原本寫法對得上，但同時也符合整批突變的共同位移時，發出提醒 |
| 異構體 pLDDT | 異構體模型的 pLDDT 現在也會顯示（連網時自動抓取） |
| 片段標註 | 加入 UniProt 的 Peptide 標註；同一位移量對應多個片段時，名稱合併顯示 |
| 共同位移搜尋範圍 | 從 ±100 擴大到整條序列，機率門檻同步依搜尋次數調整 |
| Python 3.9 驗證 | 用 Python 3.9.25 跑過全部測試和示範指令 |
| README | 依 ProtVar 測試結果更新定位，加入 APP 的例子 |
| 示範指令稿 | `docs/demo_commands.md`：三個鏡頭、畫面重點、旁白要點 |

---

## 二、新的示範案例：APP 與阿茲海默症

阿茲海默症的文獻習慣用 β-類澱粉蛋白（Aβ）自己的編號，Aβ 的第 1 個胺基酸等於 APP（770 個胺基酸的版本）的第 672 個。

```
$ af-confidence P05067 -f examples/app_abeta_numbering.txt
XX A2T:  ... [strong] +671: A673T matches; UniProt: 'C99', 'Amyloid-beta protein 42', 'Amyloid-beta protein 40' start at 672 ...
XX A21G: ... [strong] +671: A692G matches ...
XX E22G: ... [strong] +671: E693G matches ...
XX E22Q: ... [strong] +671: E693Q matches ...
!? D23N: matches as written, but D694N (+671) also matches, the shift that explains 4/4 mismatched inputs
```

### 今天最重要的發現：巧合對上的「靜默錯誤」

Iowa 突變 D23N 的正確位置是第 694 個。但 APP 的第 23 個位置**剛好也是 D**，所以：

- AFDB 網站會顯示第 23 個位置，沒有任何警告
- ProtVar 會檢查參考胺基酸，但 D 對得上，所以應該也不會警告（**推論，未實測**）
- 本工具只輸入 D23N 時也顯示 OK，**單一突變在原理上就無法偵測**
- 但輸入整份清單時，工具發現其他四個都是 +671，而 D23N 加 671 也對得上，因此標示 `!?`

這比 E6V 更能說明工具的價值：**錯誤沒有任何徵兆時，只有整批檢查才抓得到。** 這也是工具建議「把來源裡的整份清單一起輸入」的原因。

### 單一突變的誠實處理

只輸入 A2T 時，APP 有很多加工片段，A2T 在 4 個片段的位移上都「剛好對得上」。工具把 4 個全部列出並標示 `[weak]`，不會假裝知道答案。影片的鏡頭 3 就是在展示這一點。

---

## 三、主張對照表（新增）

| # | 主張 | 來源 | 把握 |
|---|---|---|---|
| 12 | APP 的 Aβ42、Aβ40、C99 從第 672 個位置開始 | UniProt P05067 的 Chain 標註（2026-11-19 擷取） | 高 |
| 13 | APP 第 692 個 A→G 是 Flemish 突變；第 693 個 E→Q 是 Dutch 型；第 694 個 D→N 是 Iowa 型 | UniProt P05067 天然變異 VAR_000016、VAR_000017、VAR_014217 | 高 |
| 14 | APP 第 693 個 E→G 在 UniProt 中標註為「in AD1」 | UniProt P05067 VAR_014215 | 高 |
| 15 | E693G 在文獻中稱為 Arctic 突變 | **憑知識**，應出自 Nilsberth et al. 2001, *Nature Neuroscience* | 中：請查證 |
| 16 | A673T（Aβ A2T）是冰島族群中發現的保護性突變 | **憑知識**，應出自 Jonsson et al. 2012, *Nature* | 中：請查證 |
| 17 | APP 第 23 個位置是 D | AFDB 模型序列（與 UniProt 一致） | 高 |
| 18 | ProtVar 輸入 P05067 D23N 時不會警告 | **推論，未實測** | 低：請實測 |

如果第 15、16 條查不到來源，影片中就只用 UniProt 有標註名稱的 Flemish、Dutch、Iowa，A2T 和 E22G 不稱呼名稱。

---

## 四、已知限制（更新）

- 單一突變碰巧對得上時，無法偵測（原理上的限制，已寫進 README）
- 不處理 DNA 層級寫法、基因體座標
- 模式生物的編號只能回報「對不上」
- 只檢查 AFDB 有收錄的異構體

---

## 五、請你校對（約 25 分鐘）

### 1. 更新程式並跑示範指令

```bash
cd af-confidence
```

```bash
git pull
```

接著照 `docs/demo_commands.md` 跑三個鏡頭的指令，確認輸出與文件一致。這一步同時也是錄影前的彩排。

### 2. ProtVar 實測兩筆

到 <https://www.ebi.ac.uk/ProtVar/> 分別輸入：

```
P05067 D23N
```

```
P01009 E342K
```

回報它有沒有發出警告（主張第 18 條）。截圖可以放進影片。

### 3. 抽查 UniProt

打開 <https://www.uniprot.org/uniprotkb/P05067/entry>，在「PTM / Processing」區確認 Amyloid-beta protein 42 從 672 開始。

### 4. 第二天的未完成項目

- UniProt P68871 的 VAR_002863 是否標在第 7 個位置

---

## 六、第四天預計

- 依你的校對結果修正
- 寫影片逐字稿初稿（8 分鐘以內，約 1600 字），每個科學主張標上對應的來源編號
- 查證主張第 15、16 條，以及「低 pLDDT 與無序區」（限制段落用）
