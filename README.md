# af-confidence

把文獻中的突變位置，正確對應到 AFDB 模型上

Map protein-level variants written in the literature (e.g. `E6V`) onto the correct residue of the
AlphaFold DB model, and explain numbering mismatches with evidence before anyone interprets a
structure.

> Status: v0.1 complete on the command line; 86 offline tests pass on Python 3.9 and 3.13.
> Accuracy measured on 735 real UniProt variants: see [Benchmark](#benchmark).
> Goals, method and development plan (in Chinese): see [專案目標、方法與實作規劃](#專案目標方法與實作規劃).

## Why

The same variant is often numbered differently in different sources:

| Variant as usually written | AlphaFold DB model residue at that number | Actual position | Reason (UniProt annotation) |
|---|---|---|---|
| HBB `E6V` (sickle-cell, HbS) | P | E7 | initiator Met removed |
| SERPINA1 `E342K` (Z allele) | L | E366 | signal peptide 1–24 |
| APP `E22G` (amyloid-beta numbering) | T | E693 | amyloid-beta starts at 672 |
| APP `D23N` (Iowa, amyloid-beta numbering) | **D (matches by coincidence)** | D694 | amyloid-beta starts at 672 |

AlphaFold DB itself shows whatever residue sits at the number you look up. Full annotation tools
do check the reference residue: for `P68871 E6V`, EBI ProtVar (UI 2.0, checked 2026-11-19) warns that
Glu does not match Pro at position 6, then **continues with Pro6** and does not point to Glu7
(screenshot: `docs/images/protvar_P68871_E6V.webp`). And when the residue matches by coincidence,
as for `D23N`, no single-variant check can notice.

This tool adds the missing step: *why* it does not match and *where* the residue probably is,
with an explicit strength of evidence.

## 專案目標、方法與實作規劃

### 要解決的問題

同一個蛋白質突變，在不同來源中常用不同的編號系統：教科書與早期文獻常不算起始甲硫胺酸（HbS 寫成 E6V），臨床文獻常從成熟蛋白質算起（α1-抗胰蛋白酶 Z 型寫成 E342K），阿茲海默症文獻用 Aβ 自己的編號（E22G），UniProt 也可能在更新時改變標準序列。AlphaFold DB（AFDB）的模型則使用 UniProt 的標準序列編號。

使用者拿文獻中的編號到 AFDB 上找位置時，網站只會顯示該編號上的胺基酸，**不會檢查、也不會警告**。ProtVar 這類完整工具會發現參考胺基酸不符，但不會指出正確位置。更危險的是「碰巧對上」：編號錯了，但錯的位置剛好是同一種胺基酸（例如 APP 的 D23N），任何單一突變的檢查都無法察覺。

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
4. **序列比對**：參考胺基酸是否等於模型在該位置的胺基酸。同時比對 AFDB 模型序列與現行 UniProt 序列；兩者不同時（AFDB 落後 UniProt 更新），算出兩條序列的位移量，把 UniProt 標註換算到模型位置上，並指出 AFDB 中序列與 UniProt 相同的模型。
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

`docs/` 中的每日報告保留當天的狀態與查證紀錄，有些說法後來已修正；**以本 README 為準**。

### 驗證方式

- **自動化測試**：86 個，全部離線執行（使用 `data/cache` 中的真實 AFDB 與 UniProt 資料），在 Python 3.9 與 3.13 通過；網路行為（重試、404、快取損壞）用模擬回應測試。
- **真實資料驗證**：`benchmark/`，固定亂數種子、可重現。
- **人工核對**：示範案例的 pLDDT 與序列，對照 AFDB 與 UniProt 網站；ProtVar 行為以實際操作截圖記錄。

### 已知限制與未來規劃

限制見 [What it does NOT do](#what-it-does-not-do)。未來可能的方向（尚未排程）：

- 網頁介面（靜態頁面，放在 GitHub Pages），讓不用終端機的人也能貼上清單使用
- GitHub Actions 自動測試、版本標籤與發布
- 給非程式背景使用者的中文使用說明
- 透過 Ensembl VEP 支援 DNA 層級寫法；模式生物與人類同源蛋白質的編號對應

## Install and run

Requires Python 3.9+; no third-party packages. On macOS and most Linux systems the command is
`python3` (not `python`); on Windows it is usually `py`.

```bash
git clone https://github.com/wangnick1004/af-confidence
cd af-confidence
python3 -m pip install .
af-confidence P68871 E6V
```

Without installing: `python3 -m af_confidence P68871 E6V`.

```
P68871  (AlphaFold DB model AF-P68871-F1)
XX E6V: model has P at 6, not E
     -> [medium] annotated_offset: +1: E7V matches; UniProt: initiator Met removed; mature chain
        'Hemoglobin subunit beta' starts at 2 (explains 1/1 mismatched input) [pLDDT 96.56]
```

### Input

The first word is the protein, the rest are variants:

| Protein as | Example |
|---|---|
| UniProt accession | `af-confidence P68871 E6V` |
| Gene name (human by default) | `af-confidence HBB E6V` |
| Isoform accession | `af-confidence P04637-2 R175H` |
| Gene name in another organism | `af-confidence Trp53 R172H --organism 10090` |

Variants: `E6V`, `p.E6V`, `Glu6Val`, `p.Glu6Val`, `p.(Glu6Val)`, nonsense `R213*` / `p.Arg213Ter`;
separate them with spaces or commas.

A list from one or more papers: `-f FILE` (can be repeated). One line per protein, `#` starts a
comment:

```
# variants collected from several papers
HBB      E6V            # sickle cell, legacy numbering
SERPINA1 E342K, E264V   # Z and S alleles
P04637   R175H R72P
```

```bash
af-confidence -f my_variants.txt
```

Lines without a protein use the one given on the command line, e.g.
`af-confidence APP -f examples/app_abeta_numbering.txt`. Entries for the same protein (by gene name
or accession) are checked together, so batch evidence uses all of them. A protein that cannot be
loaded is reported as an error without stopping the others.

Some gene names look like variants (`C1S`, `F2R`, `C4A`): at the start of a line in a file they are
read as the protein; when a protein is also given on the command line they are read as variants.
Use the UniProt accession if in doubt.

### Options and output

| Option | Meaning |
|---|---|
| `-f`, `--file FILE` | read `[PROTEIN] VARIANT ...` lines (repeatable) |
| `--organism TAXID` | NCBI taxonomy ID for gene-name lookup (default 9606, human; mouse 10090) |
| `--format text\|tsv\|json` | `tsv` opens in Excel; one row per suggestion |
| `--cache DIR` | cache directory (default `~/.cache/af-confidence`) |
| `--offline` | use cached files only |

The demo proteins are cached in `data/cache`, so `--cache data/cache --offline` works without network.
Network requests are retried 3 times with back-off; cache files are written atomically and a
corrupt cache file is fetched again.

Exit code: 0 if every variant matches unambiguously, 1 otherwise, 2 if a protein could not be
loaded or a network error occurred.

Run the tests: `python3 -m pip install pytest && python3 -m pytest`.

## What it checks

Status per variant: `OK` match, `!?` ambiguous match, `XX` mismatch or out of range, `??` unparseable.

For a mismatch, explanations that are exact sequence comparisons, each labelled with how likely it
is to be a coincidence (any single residue matches a random position about 1 time in 20):

| Kind | Meaning | Strength |
|---|---|---|
| `annotated_offset` | shifting by a UniProt processing feature (initiator Met, signal/transit peptide, propeptide, mature chain, other fragments), or by a UniProt sequence update the AlphaFold DB model has not caught up with, gives a match | **strong** if it explains ≥2 inputs and that many coincidences has probability < 0.05 / number of shifts tried; **medium** if a primary feature explains this one input and no other shift is strong; **weak** otherwise |
| `consistent_offset` | one unannotated shift makes *all* mismatched inputs match; expected number of such shifts by chance < 0.05 | **strong** (needs ≥2 inputs) |
| `isoform` | matches at the same number in an AlphaFold DB isoform model | **strong** if one isoform explains every mismatched input (≥2), else **weak** |
| `swapped` | the model already has the alternate residue | **medium** |
| `nearby` | the residue is within ±3 positions | **weak**, shown only if nothing stronger applies |

A variant that matches as written is flagged `ambiguous_match` when it also matches under a shift
that strongly explains the other inputs of the same batch.

Each suggestion shows the AlphaFold DB model and the pLDDT at that residue, as provided by
AlphaFold DB (not reinterpreted).

Warnings are printed when UniProt annotations could not be loaded (offsets not checked) or when
the AlphaFold DB model was built on an older UniProt sequence than the current one. In that case
the tool aligns the two sequences: if one is a stretch of the other (e.g. UniProt moved the
canonical start codon), UniProt annotations are converted to model positions and the shift is
offered as an explanation; otherwise UniProt annotations are not used.

For an isoform accession, UniProt annotates processing on the canonical entry only; N-terminal
features (initiator Met, signal/transit peptide, propeptide) are used for the isoform when its
N-terminus is identical over that stretch.

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

## What it does NOT do

- It does not judge structural confidence beyond showing AlphaFold's own pLDDT.
- It does not predict whether a variant is pathogenic. AlphaFold DB models are wild-type
  structures; the mutation itself is not modelled.
- A single variant that matches by coincidence cannot be detected; give the whole list from the
  source so batch evidence can be used.
- No DNA/transcript notation (`c.20A>T`) or genomic coordinates: use Ensembl VEP or EBI ProtVar.
- Model-organism numbering (e.g. mouse) is reported as a mismatch but not corrected.

## Repository layout

```
af_confidence/  The tool (variant parser, data sources, mapper, CLI)
tests/          Offline tests against data/cache
examples/       Variant lists for the demo (APP amyloid-beta numbering, SERPINA1 alleles)
data/cache/     AlphaFold DB and UniProt responses for the demo proteins
benchmark/      Accuracy benchmark on real UniProt variants (script, sampled data, results)
scripts/        Day-1 feasibility checks
docs/           Daily reports (dated; this README is authoritative), demo commands, screenshots
```

## Data and licence

Structure predictions come from the AlphaFold Protein Structure Database (EMBL-EBI / Google DeepMind).
AlphaFold DB data are available under CC-BY-4.0; cite the AlphaFold and AlphaFold DB papers when
using the output. Processing-feature annotations come from UniProt. Code licence: MIT (see `LICENSE`).

Parts of the code and documentation were drafted with help from Claude (Anthropic).
