# 第二天報告：查證與 v0.1 程式

日期：2026-11-19
結論：**v0.1 可以在命令列使用，34 個離線測試全部通過。** 查證項目大多完成，只有 ProtVar 的行為需要你實際測試。

---

## 一、查證結果

### 1. 兩個示範案例的位移成因：✅ 已用 UniProt 官方標註證實

| 主張 | UniProt 的證據（rest.uniprot.org，2026-11-19 擷取） |
|---|---|
| HbS 在標準編號中位於第 7 個位置 | P68871 天然變異 **VAR_002863**：位置 7，E→V，標註「Hb S」 |
| HBB 的起始甲硫胺酸在成熟蛋白質中被移除 | P68871 特徵「Initiator methionine 1, Removed」；成熟鏈「Chain 2–147」 |
| Z 型突變在標準編號中位於第 366 個位置 | P01009 天然變異 **VAR_007004**：位置 366，E→K，標註「Z」 |
| SERPINA1 有 24 個胺基酸的訊號胜肽 | P01009 特徵「Signal 1–24」；成熟鏈「Chain 25–418」 |
| S 型突變（文獻常寫 E264V）在標準編號中位於第 288 個位置 | P01009 天然變異 **VAR_007000**：位置 288，E→V，標註「S」 |

這些證據直接來自 UniProt 的資料，不是憑記憶。工具本身也是讀取同一組 UniProt 標註來解釋位移，所以給出的理由有出處。

### 2. AFDB 資料授權：✅ CC-BY-4.0

AFDB 首頁原文：「Data is available for academic and commercial use, under a CC-BY-4.0 licence.」（擷取自網站前端程式碼中的首頁文字）。README 已更新。

### 3. AFDB 有複合體預測：✅ 證實，但與本工具無關

首頁列出「Proteome-scale complex prediction」、「Viral complexes」等資料集（由 Steinegger Lab、Mirdita Lab 提供）。影片講限制時說「**這個**模型是單體預測」即可。

### 4. Ensembl VEP 和 EBI ProtVar 能否處理傳統編號：⚠️ 部分查證

- **ProtVar** 接受「UniProt accession＋位置＋參考與變異胺基酸」的蛋白質層級輸入，並對應到**標準異構體**的位置（[ProtVar 論文，NAR 2024](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11223857/)，經搜尋結果摘要得知）。
- **VEP** 接受 HGVS 蛋白質寫法，但只在能明確對應到單一基因體變化時才處理（[VEP 文件](https://Grch37.Ensembl.org/info/docs/tools/vep/vep_formats.html)，經搜尋結果摘要得知）。
- **尚未確認：** 參考胺基酸對不上時（例如輸入 E6V），它們會不會**主動建議**位移或異構體。論文全文所在的 NCBI 網站不在本環境允許的網址內，我讀不到。**請你實際測試（見第四節）。**

如果它們已經會主動建議位移，我們的工具就和它們重疊，影片中的定位要調整為「輕量、可離線、可批次、會說明理由的檢查工具」。

### 5. 低 pLDDT 與無序區的關係

新範圍下工具不再依賴這一條，只在影片的「限制」段落使用。這條目前仍是憑知識，第四天寫逐字稿時再找文獻。

---

## 二、程式說明

### 結構

```
af_confidence/
  variants.py   解析突變寫法：E6V、p.E6V、Glu6Val、p.Glu6Val、p.(Glu6Val)
  sources.py    從 AFDB 和 UniProt 抓資料，存到本機快取（只用 Python 標準函式庫）
  mapper.py     核心：比對序列、解釋對不上的原因
  cli.py        命令列介面
tests/          34 個測試，全部離線執行
```

### 對不上時，工具會檢查的五種原因（證據由強到弱）

| 種類 | 意思 | 判斷依據 |
|---|---|---|
| `annotated_offset` | 位移量剛好等於 UniProt 標註的加工區段長度（起始甲硫胺酸、訊號胜肽等） | UniProt 官方標註 |
| `consistent_offset` | 同一個位移量讓**所有**對不上的突變都對上 | 依蛋白質的胺基酸組成，計算「隨機發生的期望次數」，必須小於 0.05 才回報；**只有一個突變時絕不回報** |
| `isoform` | 在某個異構體模型的同一位置對得上 | 序列比對 |
| `swapped` | 模型在該位置已經是變異胺基酸，可能寫反了 | 序列比對 |
| `nearby` | 前後 3 個位置內有該胺基酸 | **弱證據**：大約四分之一的機率是巧合，所以只在沒有更強的解釋時才顯示 |

### 一個重要的設計決定：避免「巧合」被當成答案

只有一個突變時，在 ±100 的範圍內，隨便都能找到好幾個位移量剛好對得上（每個位移約有 1/20 的機率）。所以：

- 單一突變的位移，只接受有 UniProt 標註佐證的（`annotated_offset`）。
- 多個突變的共同位移，要通過機率門檻才回報。
- 前後幾格對得上（`nearby`），明確標示「可能是巧合」。

這也是第一天 F20 那個例子的教訓：「F 在第 19 個」可能只是巧合，工具不應該說得比證據更肯定。

### 實際輸出

```
$ af-confidence P68871 E6V
XX E6V: model has P at 6, not E
     -> [annotated_offset] +1: E7V matches; UniProt annotates initiator Met removed,
        so E6V is probably numbered without it [pLDDT 96.56]

$ af-confidence P01009 E342K E264V
XX E342K: model has L at 342, not E
     -> [annotated_offset] +24: E366K matches; UniProt annotates signal peptide 1-24 ... [pLDDT 93.25]
XX E264V: model has L at 264, not E
     -> [annotated_offset] +24: E288V matches; UniProt annotates signal peptide 1-24 ... [pLDDT 97.25]

$ af-confidence P04637 R175H F20L R72P
OK R175H: matches the model sequence (pLDDT 96.62)
XX F20L: model has S at 20, not F
     -> [nearby] F found at 19 (-1); weak evidence, could be chance [pLDDT 61.56]
XX R72P: model has P at 72, not R
     -> [swapped] model already has P at 72: did the source write P72R? ... [pLDDT 48.25]
```

### 測試涵蓋的情境

- 各種突變寫法的解析，以及應該被拒絕的寫法（DNA 層級寫法、缺失突變等）
- HbS（+1）、Z 型（+24）、Z 型和 S 型同時輸入
- 沒有 UniProt 標註時的共同位移（把 TP53 熱點突變故意寫少 5 格）
- 單一突變不會被誤判為共同位移
- 異構體：TP53 第 332 個位置在標準序列是 I，在異構體 P04637-3 是 M
- 寫反、超出範圍、離線時查無資料
- 命令列的三種輸出格式（text、tsv、json）與結束代碼

### 另外驗證過

- 在全新的 Python 虛擬環境中用 `pip install .` 安裝成功
- 沒有快取時，能直接從 AFDB 和 UniProt 網站抓資料

---

## 三、已知限制（v0.1）

- 異構體模型的 pLDDT 目前不會顯示（顯示 n/a），只顯示標準模型的。
- 只檢查 ±100 範圍內的共同位移。
- 不處理 DNA 層級寫法和基因體座標（這是刻意的範圍限制）。
- 小鼠等模式生物的編號只能回報「對不上」，無法自動修正。

---

## 四、請你校對（約 30 分鐘）

### 1. 在你的電腦上跑程式（原訂第三天，可以提前做）

```bash
git clone https://github.com/wangnick1004/af-confidence
```

```bash
cd af-confidence
```

```bash
python -m af_confidence P68871 E6V --cache data/cache --offline
```

應該看到 `annotated_offset` 和 `E7V`。再試一次不加 `--cache data/cache --offline`，確認能從網路抓資料：

```bash
python -m af_confidence P01009 E342K
```

想跑測試的話：

```bash
pip install pytest
```

```bash
python -m pytest
```

應該看到 `34 passed`。任何錯誤訊息請**全文**貼給我。Windows 上如果 `python` 不能用，改成 `py`。

### 2. 對照 UniProt 網頁（抽查證據）

- 打開 <https://www.uniprot.org/uniprotkb/P68871/entry>，在「Variants」或「Disease & Variants」區找到 **VAR_002863**，確認位置是 7、標註 Hb S。
- 打開 <https://www.uniprot.org/uniprotkb/P01009/entry>，在「PTM / Processing」區確認 **Signal 1–24**。

### 3. 測試 ProtVar（決定我們的定位，很重要）

打開 <https://www.ebi.ac.uk/ProtVar/>，在輸入框分別輸入：

```
P68871 E6V
```

```
P01009 E342K
```

請回報：
- 它有沒有報錯，或說參考胺基酸不符？
- 它有沒有**主動建議**「可能是第 7 個／第 366 個」？
- 截圖最好。

---

## 五、第三天預計

- 依你的校對結果修正程式
- 依 ProtVar 測試結果，決定影片中工具的定位說法
- 補上異構體模型的 pLDDT 顯示
- 開始準備示範腳本（工具的錄影片段要跑哪些指令）
