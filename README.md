# af-confidence

[![tests](https://github.com/wangnick1004/af-confidence/actions/workflows/tests.yml/badge.svg)](https://github.com/wangnick1004/af-confidence/actions/workflows/tests.yml)

把文獻中的突變位置，正確對應到 AFDB 模型上

> 目前版本 v0.1.0（[更新紀錄](CHANGELOG.md)）。準確度驗證見 [Benchmark](#benchmark)；專案目標與方法見
> [專案目標、方法與實作規劃](#專案目標方法與實作規劃)。

## 中文使用說明

這份說明寫給**沒有程式背景**的使用者：照著做就能在自己的電腦上使用這個工具。
（專案目標、方法與準確度驗證請看本頁後面的 [專案目標、方法與實作規劃](#專案目標方法與實作規劃) 和 [Benchmark](#benchmark)。）

---

### 目錄

1. [這個工具能做什麼](#1-這個工具能做什麼)
2. [準備：確認電腦有 Python](#2-準備確認電腦有-python)
3. [下載工具](#3-下載工具)
4. [第一次使用](#4-第一次使用)
5. [怎麼輸入](#5-怎麼輸入)
6. [怎麼讀結果](#6-怎麼讀結果)
7. [把結果存成 Excel 可以開的檔案](#7-把結果存成-excel-可以開的檔案)
8. [常見問題](#8-常見問題)
9. [這個工具不做的事](#9-這個工具不做的事)
10. [引用與授權](#10-引用與授權)

---

### 1. 這個工具能做什麼

同一個突變，在不同文獻中常用不同的編號。例如鐮刀型貧血的突變，教科書寫 **E6V**（第 6 個胺基酸 E 變成 V），但 AlphaFold DB（AFDB）的模型上，**第 6 個是 P，E 在第 7 個**。AFDB 網站不會提醒你，你可能就看錯了位置。

這個工具會：

- 檢查你輸入的突變位置，在 AFDB 模型上**對不對得上**
- 對不上時，**說明可能的原因並指出正確位置**，並告訴你這個建議**有多可信**
- 一次檢查**一整份清單**，找出單獨看一個突變時發現不了的錯誤

只要輸入蛋白質名稱和突變，例如：

```
HBB E6V
```

工具就會回答：「第 6 個是 P，不是 E；加 1 之後 E7V 對得上，因為 UniProt 標註這個蛋白質的第一個胺基酸會被移除。」

---

### 2. 準備：確認電腦有 Python

這個工具用 Python 寫成，需要 **Python 3.9 或更新的版本**。除了 Python 本身，**不需要安裝任何其他東西**。

#### 打開終端機

| 電腦 | 怎麼打開 |
|---|---|
| **Mac** | 按 `⌘ + 空白鍵`，輸入「終端機」或「Terminal」，按 Enter |
| **Windows** | 按開始鍵，輸入「PowerShell」，按 Enter |

#### 確認 Python 版本

在終端機輸入以下指令，按 Enter：

| 電腦 | 指令 |
|---|---|
| Mac、Linux | `python3 --version` |
| Windows | `py --version` |

看到 `Python 3.9.x` 或更大的數字（3.10、3.11、3.12、3.13…）就可以了。

> **本說明之後的指令都寫 `python3`。Windows 使用者請一律改成 `py`。**

#### 如果顯示找不到指令

- **Mac：** 輸入 `python3 --version` 時，可能會跳出視窗，請你安裝「命令列開發者工具」。按「安裝」，等它裝完，再輸入一次指令。
- **Windows：** 到 <https://www.python.org/downloads/> 下載安裝。安裝的第一個畫面，**一定要勾選「Add python.exe to PATH」**，再按「Install Now」。裝完後關掉 PowerShell 再重新打開。

---

### 3. 下載工具

選一種方式就好。

#### 方式 A：下載 ZIP（不需要 git，最簡單）

1. 打開 <https://github.com/wangnick1004/af-confidence>
2. 按綠色的 **「Code」** 按鈕，選 **「Download ZIP」**
3. 解壓縮，會得到一個叫 `af-confidence-main` 的資料夾
4. 把這個資料夾放到好找的地方，例如「文件」

#### 方式 B：用 git 在終端機下載（之後更新比較方便）

```bash
git clone https://github.com/wangnick1004/af-confidence
```

```bash
cd af-confidence
```

之後要更新到最新版，進入資料夾後執行 `git pull` 即可。Mac 第一次使用 `git` 時，如果跳出視窗要求安裝「命令列開發者工具」，按「安裝」即可。

#### 方式 C：只用終端機下載 ZIP（沒有 git 時）

**Mac、Linux：**

```bash
curl -L -o af-confidence.zip https://github.com/wangnick1004/af-confidence/archive/refs/heads/main.zip
```

```bash
unzip af-confidence.zip
```

```bash
cd af-confidence-main
```

**Windows（PowerShell）：**

```powershell
Invoke-WebRequest -Uri https://github.com/wangnick1004/af-confidence/archive/refs/heads/main.zip -OutFile af-confidence.zip
```

```powershell
Expand-Archive af-confidence.zip -DestinationPath .
```

```powershell
cd af-confidence-main
```

#### 方式 D：安裝成指令（進階）

不想每次都進入資料夾的話，可以用 pip 直接從 GitHub 安裝（需要電腦有 git）：

```bash
python3 -m pip install git+https://github.com/wangnick1004/af-confidence
```

沒有 git 的話，改成：

```bash
python3 -m pip install https://github.com/wangnick1004/af-confidence/archive/refs/heads/main.zip
```

安裝後在**任何資料夾**都能執行 `python3 -m af_confidence HBB E6V`。注意：

- 這種方式**不包含**範例清單（`examples/`）和離線示範資料（`data/cache/`），需要連網使用。
- 有些電腦會擋這種安裝（出現 `externally-managed-environment` 錯誤），或裝好後輸入 `af-confidence` 找不到指令。遇到時，改用方式 A～C，或一律用 `python3 -m af_confidence` 執行。

#### 進入工具的資料夾

**之後每次使用，都要先讓終端機「進入」工具的資料夾。** 最簡單的方法：

1. 在終端機輸入 `cd`，**後面加一個空格**（先不要按 Enter）
2. 把工具的資料夾**直接拖進終端機視窗**，路徑會自動填上
3. 按 Enter

確認有沒有進對資料夾：Mac 輸入 `ls`、Windows 輸入 `dir`，應該會看到 `README.md`、`af_confidence`、`examples` 等檔案。

---

### 4. 第一次使用

進入工具的資料夾後，輸入：

```bash
python3 -m af_confidence HBB E6V
```

第一次使用需要連上網路，工具會從 AFDB 和 UniProt 下載資料，存在電腦裡；之後查同一個蛋白質就不用再下載。你會看到：

```
HBB -> P68871  (AlphaFold DB model AF-P68871-F1)
XX E6V: model has P at 6, not E
     -> [medium] annotated_offset: +1: E7V matches; UniProt: initiator Met removed; mature chain 'Hemoglobin subunit beta' starts at 2 (explains 1/1 mismatched input) [pLDDT 96.56]

Evidence: strong = several inputs agree and that is unlikely by chance; medium = one input fits (right about 9 times in 10 in the benchmark); weak = could easily be chance.
pLDDT values are shown as provided by AlphaFold DB, not reinterpreted. This tool does not predict variant effects.
```

逐行說明：

| 輸出 | 意思 |
|---|---|
| `HBB -> P68871` | 基因名稱 HBB 對應到 UniProt 編號 P68871 |
| `AlphaFold DB model AF-P68871-F1` | 比對的是這個 AFDB 模型 |
| `XX E6V: model has P at 6, not E` | ❌ 對不上：模型第 6 個是 P，不是 E |
| `-> [medium] annotated_offset: +1: E7V matches` | 建議：加 1 之後，E7V 對得上 |
| `UniProt: initiator Met removed` | 原因：UniProt 標註第一個甲硫胺酸（Met）會被移除，所以傳統編號從下一個開始算 |
| `[pLDDT 96.56]` | AFDB 對第 7 個位置的信心分數（照 AFDB 原值顯示） |
| `[medium]` | 這個建議的可信程度，見[第 6 節](#證據強度strong--medium--weak) |
| 最後兩行 | 證據強度的說明，以及「本工具不預測突變的影響」的聲明 |

如果改用正確的編號：

```bash
python3 -m af_confidence HBB p.Glu7Val
```

```
HBB -> P68871  (AlphaFold DB model AF-P68871-F1)
OK p.Glu7Val: matches the model sequence (pLDDT 96.56)
```

`OK` 表示對得上。

> **沒有網路時：** 工具資料夾裡已經存了幾個示範蛋白質（HBB、SERPINA1、TP53、APP、BTD）的資料。在指令後面加上 `--cache data/cache --offline`，不用網路也能執行這些示範。

---

### 5. 怎麼輸入

#### 基本格式

```
python3 -m af_confidence  蛋白質  突變1  突變2  ...
```

**第一個詞是蛋白質，後面是突變**，用空格或逗號分開。

#### 蛋白質可以這樣寫

| 寫法 | 範例 | 說明 |
|---|---|---|
| 基因名稱 | `HBB`、`TP53`、`p53` | 預設查人類；大小寫都可以，常見別名也查得到 |
| UniProt 編號 | `P68871` | 最準確；在 <https://www.uniprot.org> 查得到 |
| 異構體編號 | `P04637-2` | 比對該異構體的模型 |
| 其他物種的基因 | `Trp53 --organism 10090` | 10090 是小鼠，10116 是大鼠，7955 是斑馬魚 |

#### 突變可以這樣寫

| 寫法 | 範例 |
|---|---|
| 單字母 | `E6V` |
| 單字母加 `p.` | `p.E6V` |
| 三字母 | `Glu6Val` |
| 三字母加 `p.` | `p.Glu6Val`、`p.(Glu6Val)` |
| 無義突變（變成終止密碼子） | `R213*`、`p.Arg213Ter` |

**不支援：** DNA 層級的寫法（`c.20A>T`）、缺失或插入（`p.Glu6del`）、基因體座標。這些請改用 Ensembl VEP 或 EBI ProtVar。

#### 一次檢查一整份清單（建議這樣用）

如果你從文獻整理出一份突變清單，**把整份清單一起檢查，比一個一個檢查可靠得多**（原因見[第 6 節](#為什麼要整份清單一起檢查)）。

**步驟 1：建立清單檔**

每行寫一個蛋白質，後面接它的突變；`#` 後面可以寫註解，例如出處：

```
# 從三篇論文整理的突變
HBB      E6V            # 鐮刀型貧血，傳統編號
SERPINA1 E342K, E264V   # Z 型與 S 型
TP53     R175H R72P
```

用什麼軟體建立：

| 電腦 | 軟體 | 注意 |
|---|---|---|
| **Mac** | 「文字編輯」(TextEdit) | ⚠️ **一定要先選選單「格式」→「製作純文字」**，再存檔。預設的 RTF 格式工具讀不了 |
| **Windows** | 「記事本」(Notepad) | 直接存成 `.txt` 即可 |

檔名建議用英文，例如 `my_variants.txt`，存在工具的資料夾裡。

**步驟 2：執行**

```bash
python3 -m af_confidence -f my_variants.txt
```

如果整份清單都是同一個蛋白質，清單裡可以只寫突變，把蛋白質寫在指令上：

```bash
python3 -m af_confidence APP -f examples/app_abeta_numbering.txt
```

工具資料夾的 `examples/` 裡有三份範例清單可以參考。

清單中同一個蛋白質（不論寫基因名稱還是 UniProt 編號）的突變會合併在一起檢查；某個蛋白質查不到時，只會回報它的錯誤，其他照常輸出。

#### 所有選項

| 選項 | 說明 |
|---|---|
| `-f 檔案`、`--file 檔案` | 讀取清單檔；可以重複使用，一次讀多個檔案 |
| `--organism 物種代碼` | 查基因名稱時用的物種（NCBI taxonomy ID），預設 9606（人類） |
| `--format text`／`tsv`／`json` | 輸出格式：一般文字（預設）、TSV（可用 Excel 開啟）、JSON（給程式讀取） |
| `--cache 資料夾` | 下載資料的存放位置，預設 `~/.cache/af-confidence` |
| `--offline` | 不連網，只用已下載的資料 |
| `--version`、`-h` | 顯示版本、顯示說明 |

工具連網失敗時會自動重試 3 次。執行結束時的結束代碼（寫腳本時才會用到）：全部對得上為 0，有任何對不上或可能是巧合為 1，有蛋白質查不到或網路錯誤為 2。

---

### 6. 怎麼讀結果

#### 每個突變開頭的符號

| 符號 | 意思 | 你該做什麼 |
|---|---|---|
| `OK` | 對得上 | 可以直接使用這個位置 |
| `XX` | 對不上（或超出模型範圍） | 看下方的建議 |
| `!?` | **對得上，但可能是巧合** | 特別注意！見下方說明 |
| `??` | 突變寫法看不懂 | 檢查寫法，見[第 5 節](#突變可以這樣寫) |

#### 建議的種類

| 種類 | 意思 | 例子 |
|---|---|---|
| `annotated_offset` | 依 UniProt 的標註，加減某個數字後對得上。常見原因：傳統編號不算第一個甲硫胺酸、從去掉訊號胜肽的成熟蛋白質開始算、用片段自己的編號（例如 Aβ），或 UniProt 更新過序列 | HbS 的 E6V → E7V（+1）；Z 型的 E342K → E366K（+24） |
| `consistent_offset` | 沒有標註可以解釋，但同一個位移讓整份清單都對上 | 整份清單都少算了 5 格 |
| `isoform` | 在另一個異構體的模型上對得上 | 文獻用的是不同的異構體 |
| `swapped` | 模型在該位置已經是「變異後」的胺基酸，可能把前後寫反了 | TP53 的 R72P，其實應該是 P72R |
| `nearby` | 前後 3 格內有這個胺基酸 | 可能打錯字，但也很可能只是巧合 |
| `ambiguous_match` | 照原本寫法對得上，但也符合整份清單的共同位移 | 見下方說明 |

#### 證據強度：strong / medium / weak

每個建議前面的方括號，表示這個建議有多可信。數字來自用 735 個真實突變做的驗證：

| 強度 | 意思 | 實際表現 |
|---|---|---|
| **strong** | 好幾個突變都指向同一個解釋，光靠巧合幾乎不可能 | 2,401 筆測試中只有 2 筆指錯，**幾乎可以直接相信** |
| **medium** | 只有一個突變符合，或符合一個具體的情況（例如寫反） | 大約 **10 次中對 9 次**；剩下的是單看一個突變分辨不出來的巧合，例如「打錯一格」和「不算第一個胺基酸」看起來一模一樣 |
| **weak** | 很可能只是巧合 | 只當作參考，要自己回去查原始文獻 |

#### 為什麼要整份清單一起檢查

任何一種胺基酸在隨機位置出現的機率大約是 1/20。所以編號錯了的時候，**錯的位置剛好是同一種胺基酸的機會，大約有 7～9%**。這時候工具和網站都會顯示「對得上」，完全沒有警告。

整份清單一起檢查時，工具可以發現：「其他突變都差了同樣的格數，這一個照理也應該差那麼多。」這時就會用 `!?` 標示出來。例如阿茲海默症相關的 APP 蛋白質：

```bash
python3 -m af_confidence APP -f examples/app_abeta_numbering.txt
```

```
XX A2T: model has L at 2, not A
     -> [strong] annotated_offset: +671: A673T matches; UniProt: 'C99', 'Amyloid-beta protein 42', 'Amyloid-beta protein 40' start at 672 (explains 4/4 mismatched inputs) [pLDDT 36.44]
...（A21G、E22G、E22Q 也都是 +671）
!? D23N: matches as written, but D694N (+671) also matches, the shift that explains 4/4 mismatched inputs
```

D23N 照原寫法「對得上」，因為 APP 第 23 個位置剛好也是 D。但其他四個都是用 Aβ 編號（要加 671），所以 D23N 真正的位置很可能是 D694N。**只輸入 D23N 一個突變時，任何工具都發現不了這個錯誤。**

#### 警告（warning）

結果中如果出現 `warning:` 開頭的行，請一定要看。常見的兩種：

- **UniProt 序列和 AFDB 模型不一致**：UniProt 更新了序列，但 AFDB 的模型還是舊的。工具會告訴你差幾格；如果 AFDB 有另一個模型和新序列相同，也會告訴你改用哪一個。範例：

  ```bash
  python3 -m af_confidence P43251 F108V A151T P371S
  ```

- **UniProt 標註無法取得**：通常是網路問題，這時工具無法用標註來解釋位移，結果可能不完整。

#### pLDDT

每個建議後面的 `[pLDDT 數字]`，是 AlphaFold 對該位置結構的信心分數（0～100），**工具照 AFDB 的原值顯示，不另外判讀**。一般的解讀方式：90 以上非常高、70～90 高、50～70 低、50 以下非常低。分數低的區域，3D 結構通常不能拿來解讀。

---

### 7. 把結果存成 Excel 可以開的檔案

在指令後面加上 `--format tsv`，再用 `>` 把結果存成檔案：

```bash
python3 -m af_confidence -f my_variants.txt --format tsv > 結果.tsv
```

然後在 Excel 選「檔案」→「開啟」，選 `結果.tsv`（檔案類型選「所有檔案」）。每一列是一個建議，欄位包括：蛋白質、突變、狀態、模型上的胺基酸、建議的種類、強度、建議的位置、pLDDT、說明。

---

### 8. 常見問題

**Q：出現 `command not found: python3` 或「找不到指令」**
A：電腦沒有安裝 Python，或 Windows 使用者沒有改用 `py`。見[第 2 節](#2-準備確認電腦有-python)。

**Q：出現 `No module named af_confidence`**
A：終端機沒有在工具的資料夾裡。照[第 3 節](#進入工具的資料夾)重新進入資料夾。

**Q：出現 `cannot get data from ... after 3 attempts`**
A：連不上 AFDB 或 UniProt。檢查網路；學校或公司的網路有時會擋，可以換一個網路試試。工具會自動重試 3 次。

**Q：出現 `gene 'XXX': no reviewed UniProt entry`**
A：查不到這個基因名稱。檢查拼字；如果不是人類的基因，加上 `--organism` 和物種代碼；或者改用 UniProt 編號。

**Q：出現 `gene 'XXX' is ambiguous`**
A：這個名稱對應到好幾個蛋白質，工具會列出所有候選，請從中選一個 UniProt 編號重新輸入。

**Q：出現 `no AlphaFold DB model`**
A：AFDB 沒有這個蛋白質的模型，例如非常長的蛋白質 titin（TTN）。這不是工具的問題。

**Q：出現 `unsupported notation`**
A：突變的寫法工具看不懂，見[第 5 節](#突變可以這樣寫)。常見原因：少了變異後的胺基酸（寫成 `E6`）、用了 DNA 層級寫法（`c.20A>T`）。

**Q：清單檔每一行都出錯**
A：Mac 使用者請確認清單檔是**純文字**格式（見[第 5 節](#一次檢查一整份清單建議這樣用)）。也確認每行的第一個詞是蛋白質名稱。

**Q：有些基因名稱看起來像突變，例如 `C1S`、`F2R`**
A：在清單檔每行的開頭，工具會把它當作蛋白質；但如果你同時在指令上指定了蛋白質，它會被當成突變。不確定時，改用 UniProt 編號最保險。

**Q：工具把下載的資料存在哪裡？**
A：Mac 和 Linux 存在 `~/.cache/af-confidence`；Windows 存在使用者資料夾下的 `.cache\af-confidence`。可以直接刪除，下次使用時會重新下載。如果懷疑資料過期（例如 UniProt 剛更新），刪掉這個資料夾即可。

**Q：可以安裝成一般指令，不用每次都進入資料夾嗎？**
A：可以，見[第 3 節方式 D](#方式-d安裝成指令進階)。遇到安裝問題時，用進入資料夾執行的方式最穩定。

---

### 9. 這個工具不做的事

- **不判斷突變是否致病。** AFDB 的模型是正常（野生型）蛋白質，看不出突變後的結構變化。
- **不重新評估結構的可信度。** pLDDT 照 AFDB 原值顯示。
- **單獨一個突變碰巧對上時，無法發現。** 請盡量整份清單一起檢查。
- **不處理 DNA 層級寫法與基因體座標。**
- **模式生物的編號**（例如直接用小鼠的編號查人類蛋白質）只會顯示「對不上」，不會自動換算。

工具給的建議是**線索，不是結論**。重要的結果，請回到原始文獻確認作者使用的編號系統。

---

### 10. 引用與授權

- 結構預測資料來自 AlphaFold Protein Structure Database（EMBL-EBI 與 Google DeepMind），採用 CC-BY-4.0 授權。使用結果時，請引用 AlphaFold 與 AlphaFold DB 的論文。
- 加工標註與序列資料來自 UniProt。
- 本工具採用 MIT 授權（見 `LICENSE`）。
- 部分程式碼與文件由 Claude（Anthropic）協助撰寫。
- 有問題或建議，歡迎到 <https://github.com/wangnick1004/af-confidence/issues> 回報；最有幫助的是附上「工具給錯答案的突變清單」與該編號的出處。

---

## 專案目標、方法與實作規劃

### 要解決的問題

同一個蛋白質突變，在不同來源中常用不同的編號系統：教科書與早期文獻常不算起始甲硫胺酸（HbS 寫成 E6V），臨床文獻常從成熟蛋白質算起（α1-抗胰蛋白酶 Z 型寫成 E342K），阿茲海默症文獻用 Aβ 自己的編號（E22G），UniProt 也可能在更新時改變標準序列。AlphaFold DB（AFDB）的模型則使用 UniProt 的標準序列編號。

使用者拿文獻中的編號到 AFDB 上找位置時，網站只會顯示該編號上的胺基酸，**不會檢查、也不會警告**。ProtVar 這類完整工具會發現參考胺基酸不符，但不會指出正確位置：輸入 `P68871 E6V` 時，ProtVar（UI 2.0，2026-11-19 測試）警告 Glu 與第 6 個位置的 Pro 不符，接著就改用 Pro6 繼續分析（截圖：`docs/images/protvar_P68871_E6V.webp`）。更危險的是「碰巧對上」：編號錯了，但錯的位置剛好是同一種胺基酸（例如 APP 的 D23N），任何單一突變的檢查都無法察覺。

### 目標

1. **把文獻中蛋白質層級的突變寫法，正確對應到 AFDB 模型的殘基位置。**
2. 對不上時，**說明原因並指出可能的正確位置**，而且每個建議都附上**證據強度**，不把巧合說成答案。
3. 支援從文獻整理出的**整份清單**，利用多個突變之間的一致性，找出單一突變無法發現的錯誤。
4. **只做客觀的序列比對**：不重新判讀 pLDDT、不預測致病性。
5. 輕量、可離線、零第三方套件，非程式背景的研究者也裝得起來。

**刻意不做：** 重新評估結構可信度（AlphaFold 的 pLDDT 照原樣顯示）、致病性預測、DNA 層級與基因體座標的轉換（交給 Ensembl VEP、ProtVar）。

### 方法

```
輸入 ──► 1 解析 ──► 2 解析蛋白質 ──► 3 取得資料 ──► 4 序列比對 ──► 5 找候選解釋 ──► 6 證據分級 ──► 輸出
```

1. **解析突變寫法**：`E6V`、`p.Glu6Val` 等；DNA 層級寫法明確拒絕。清單檔中每行可以用不同蛋白質開頭。
2. **解析蛋白質**：UniProt 編號、異構體編號（`P04637-2`）或基因名稱。基因名稱透過 UniProt 查詢，只採用已審核（reviewed）的條目，名稱有歧義時列出所有候選。
3. **取得資料**：AFDB API 取得模型序列、異構體模型與 pLDDT；UniProt 取得加工標註（起始甲硫胺酸、訊號胜肽、前胜肽、轉運胜肽、成熟鏈與片段）與**現行序列**。資料快取在本機，網路暫時失敗時重試。
4. **序列比對**：參考胺基酸是否等於模型在該位置的胺基酸。同時比對 AFDB 模型序列與現行 UniProt 序列；兩者不同時（AFDB 落後 UniProt 更新），算出兩條序列的位移量，把 UniProt 標註換算到模型位置上，並指出 AFDB 中序列與 UniProt 相同的模型。輸入異構體編號時，UniProt 只在標準條目上標註加工區段，所以只有在異構體的 N 端與標準序列完全相同時，才沿用 N 端的標註（起始甲硫胺酸、訊號胜肽、轉運胜肽、前胜肽）。
5. **找候選解釋**（都是精確的序列比對）：
   - `annotated_offset`：依 UniProt 加工標註或序列更新的位移，對得上
   - `consistent_offset`：沒有標註依據，但同一個位移讓整批對不上的突變全部對上
   - `isoform`：在某個異構體模型的同一位置對得上
   - `swapped`：模型在該位置已是變異胺基酸，可能寫反
   - `nearby`：前後 3 個位置內有該胺基酸
   - `ambiguous_match`：照原寫法對得上，但也符合整批突變的共同位移，可能是巧合
6. **證據分級**：任一胺基酸在隨機位置出現的機率約 1/20，所以分級依「巧合的機率」而定。設 *pᵢ* 為胺基酸 *rᵢ* 在模型序列中的頻率：
   - 標註位移 *k* 說明了 *n* 個對不上的突變中的 *s* 個：巧合機率為二項分布尾端 P(X ≥ *s*)，X ~ Bin(*n*, *p̄*)。*s* ≥ 2 且機率 < 0.05 / *m*（*m* 為嘗試的標註位移數，Bonferroni 校正）時為 **strong**；只說明一個突變、而且是主要加工標註時為 **medium**；其他為 **weak**。
   - 無標註的共同位移：搜尋所有可能位移，只在恰好一個位移成立、且期望巧合次數 2L·∏*pᵢ* < 0.05 時回報（L 為序列長度），為 **strong**。
   - 異構體：同一個異構體說明了整批（≥ 2 個）對不上的突變時為 **strong**，否則為 **weak**；寫反（`swapped`）為 **medium**；前後 3 格內（`nearby`）為 **weak**，只在沒有更強的解釋時顯示。
   - 有 strong 或 medium 的解釋時，隱藏 weak 的雜訊。
7. **輸出**：文字、TSV（可用 Excel 開啟）或 JSON；每個建議附上對應的 AFDB 模型與該位置的 pLDDT（照 AFDB 原值）。

### 實作規劃與歷程

| 階段 | 目標 | 結果與決策 |
|---|---|---|
| 第 1 天 | 可行性檢查：AFDB API、pLDDT 讀取、序列比對 | 全部可行。發現 AFDB 檔案下載需要 User-Agent、AFDB 已收錄異構體模型。**範圍調整**：原本想依 pLDDT 給「可信度判讀」，但那只是把 AlphaFold 的分數換句話說；改為只做客觀、可驗證的「編號對應」 |
| 第 2 天 | v0.1 命令列工具與離線測試 | 完成解析、比對、位移與異構體檢查；以 UniProt 官方變異編號（VAR_002863、VAR_007004）證實 HbS 與 Z 型的位移成因。實測 ProtVar：會警告不符，但改用錯誤位置繼續分析 |
| 第 3 天 | 證據強度、清單輸入、巧合偵測 | 加入 strong／medium／weak；用 APP 的 Aβ 編號清單發現 D23N 碰巧對上的「靜默錯誤」，新增 `ambiguous_match` |
| 第 4 天 | 基礎補強 | 基因名稱、其他物種、異構體輸入、多蛋白質清單、網路重試、快取損壞處理、資料缺失警告 |
| 第 5 天 | 用真實資料驗證準確度 | 735 個 UniProt 天然變異的驗證（見 [Benchmark](#benchmark)）。發現 BTD（P43251）的 AFDB 模型落後 UniProt 序列更新，並修正標註位置換算的 bug；依數據把單一突變的標註位移從 strong 降為 medium，多突變改用二項檢定加 Bonferroni 校正 |
| 最終檢查 | 從全新 clone 驗證整個 repo | 修正 AFDB 查無模型時未快取（離線結果不一致）、驗證抽樣在不同執行間不穩定兩個問題 |
| 開源配備 | 自動測試、版本發布、測試補強 | GitHub Actions（3 種作業系統 × 5 個 Python 版本，加每週的線上 API 檢查）、CHANGELOG、貢獻指南、v0.1.0 版本標籤；補測試讓覆蓋率從 95% 提高到 99%；修正非 ASCII 字元在 Windows 終端機可能造成當機的問題 |

`docs/` 中的每日報告保留當天的狀態與查證紀錄，有些說法後來已修正；**以本 README 為準**。

### 驗證方式

- **自動化測試**：104 個，全部離線執行（使用 `data/cache` 中的真實 AFDB 與 UniProt 資料），程式碼覆蓋率 99%；網路行為（重試、404、逾時、快取損壞）用模擬回應測試。每次推送時由 GitHub Actions 在 Linux、macOS、Windows 與 Python 3.9～3.13 上自動執行；另有每週一次對真實 AFDB 與 UniProt API 的檢查，API 格式改變時會及早發現。自己執行測試：`python3 -m pip install pytest`，再執行 `python3 -m pytest`；參與開發請看 [CONTRIBUTING.md](CONTRIBUTING.md)。
- **真實資料驗證**：`benchmark/`，固定亂數種子、可重現。
- **人工核對**：示範案例的 pLDDT 與序列，對照 AFDB 與 UniProt 網站；ProtVar 行為以實際操作截圖記錄。

### 已知限制與未來規劃

限制見 [這個工具不做的事](#9-這個工具不做的事)。未來可能的方向（尚未排程）：

- 網頁介面（靜態頁面，放在 GitHub Pages），讓不用終端機的人也能貼上清單使用
- 透過 Ensembl VEP 支援 DNA 層級寫法；模式生物與人類同源蛋白質的編號對應

## Benchmark

`benchmark/run_benchmark.py` samples 200 reviewed human UniProt entries (fixed seed) with a signal
peptide or a removed initiator Met and uses their natural variants (positioned by UniProt, hence
ground truth) after rewriting them the way the literature often does. Full table:
[`benchmark/results.md`](benchmark/results.md); the sampled data: `benchmark/dataset.tsv`.

Main results (193 proteins, 735 variants, checked 2026-11-19):

| Scenario | True position is the top suggestion | A wrong position marked strong |
|---|---|---|
| Correct UniProt numbering (should simply match) | 735/735 match | – |
| Mature/legacy numbering, one variant at a time | 92.4% (as medium) | 0% |
| Mature/legacy numbering, whole list | 99.4% (92% strong) | 0% |
| Unannotated shift of 5–60, whole list (≥3 variants) | 81.6% | 0.3% |
| Unannotated shift or ±1–3 typo, one variant | – (cannot be known) | 0% |

What the numbers mean in practice:

- **Strong** suggestions pointed to a wrong position for 2 of 2,401 inputs. **Medium** (one variant, annotated
  shift) is right about 9 times in 10; the rest are coincidences that cannot be told apart from a
  single variant (e.g. a typo of −1 looks exactly like "initiator Met not counted").
- 7–9% of single variants written in legacy numbering match the model *by coincidence* and
  cannot be detected alone; in whole lists, most of these are flagged `ambiguous_match`
  (silent misses drop to < 1%). **Check whole lists, not single variants.**
- While building the benchmark the tool found a real discrepancy: UniProt changed the canonical
  sequence of biotinidase (P43251) in 2026, 20 residues shorter at the N-terminus, while the
  AlphaFold DB entry for P43251 still uses the old sequence, so all UniProt-numbered variants are
  off by 20 on that model. AlphaFold DB does have a model with the new sequence, filed under
  isoform 4 (AF-P43251-4-F1); the tool now points to it in its warning.

## Repository layout

```
af_confidence/  The tool (variant parser, data sources, mapper, CLI)
tests/          Offline tests against data/cache
examples/       Variant lists for the demo (APP amyloid-beta numbering, SERPINA1 alleles)
data/cache/     AlphaFold DB and UniProt responses for the demo proteins
benchmark/      Accuracy benchmark on real UniProt variants (script, sampled data, results)
scripts/        Day-1 feasibility checks
docs/           Daily reports (dated; this README is authoritative), demo commands, screenshots
.github/        Continuous integration (tests on Linux/macOS/Windows, weekly live API check)
```
