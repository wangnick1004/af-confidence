# 更新紀錄

記錄本專案所有重要的變更。版本號依照[語意化版本](https://semver.org/lang/zh-TW/)。

## [尚未發布]

### 新增
- 新輸出格式 `--format afdb`：產生可直接貼進 AlphaFold DB 模型頁「自訂標註」的軌跡名稱與位置，位置
  已換算成該模型的編號；依證據分成 OK as written、Fixed strong、Fixed medium、Ambiguous 四條軌跡，
  只有 weak 證據的突變列為未放入。每個位置字串都依 AlphaFold DB 網頁本身的格式規則驗證。
- 新輸出格式 `--format chimerax`：產生 ChimeraX 腳本（`.cxc`），以帶版本號的模型編號開啟工具比對用的
  同一個 AlphaFold DB 模型，依四種軌跡為檢查過的位置顯示側鏈、上色、加標籤，並建立具名的選取範圍；
  多個模型時並排顯示。指令依 ChimeraX 官方使用手冊撰寫，尚未在實際的 ChimeraX 中執行過。
- Python 函式庫介面：`import af_confidence as afc` 後可用 `check`、`check_list`（接受對照表、配對清單或
  清單檔）、`to_text`、`to_records`、`to_dataframe`（需要 pandas）、`afdb_tracks`、`chimerax_script`；
  核心仍不需要任何第三方套件。
- Colab 範例筆記本（`examples/colab_quickstart.ipynb`），可從 README 的「Open in Colab」按鈕直接執行；
  每週的線上檢查會實際執行一次（`scripts/check_notebook.py`）。
- AlphaFold 使用者日常工作流程的調查與整合規劃（`docs/workflow_research.md`）。
- 給非程式背景使用者的中文使用說明，放在 README 開頭：安裝 Python、四種下載方式（git、用 curl
  或 PowerShell 下載 ZIP、用 pip 從 GitHub 安裝）、建立突變清單、看懂輸出與證據強度、存成 Excel、
  常見問題。

### 變更
- 清單解析移到獨立模組 `af_confidence/inputs.py`，供命令列與 Python 介面共用。
- README 改為全中文：中文使用說明併入 README，刪除獨立的 `使用說明.md`；移除與中文重複的英文段落，
  只有英文版才有的資訊先移入中文段落；準確度驗證與檔案結構也翻成中文。
- 更新紀錄與貢獻指南改為中文。
- 準確度驗證報告（`benchmark/results.md`）改為中文，並加上名詞說明；修正 D/E 段落的說法：單一突變
  原理上只能保證不出現 strong，medium 偶爾會因巧合出現。報告寫檔時明確使用 UTF-8。
- 範例清單（`examples/`）改用中文註解，並為每個突變註明出處（UniProt 變異編號或論文）與標準編號；
  說明 `mixed_proteins.txt` 中的 R72P 是故意寫反的示範。查證了 UniProt 未標註的兩個突變名稱：
  Arctic（E693G，Nilsberth et al. 2001）與 Icelandic（A673T，Jonsson et al. 2012）。

### 修正
- 離線執行生物素酶（P43251）範例時，異構體 4 模型的建議現在也會顯示 pLDDT：原本 `data/cache` 裡
  缺少該模型的信心分數檔（[#1](https://github.com/wangnick1004/af-confidence/pull/1)）。

## [0.1.0] - 2026-11-19

第一個正式版本：一個命令列工具，把文獻中蛋白質層級的突變寫法對應到 AlphaFold DB 模型上，並以
分級的證據說明編號不符的原因。

### 新增
- 突變寫法：`E6V`、`p.E6V`、`Glu6Val`、`p.Glu6Val`、`p.(Glu6Val)`，以及無義突變（`*`、`Ter`）。
- 蛋白質可以輸入 UniProt 編號、異構體編號（`P04637-2`）或基因名稱（非人類用 `--organism`）；
  可以從清單檔讀入，每行一個蛋白質（`-f`）。
- 編號不符時的解釋：標註位移（UniProt 加工標註或 UniProt 序列更新）、共同位移、異構體、參考與變異
  胺基酸寫反、鄰近位置；整批輸入時偵測碰巧對上的突變（`ambiguous_match`）。
- 依巧合機率分級的證據強度 strong／medium／weak（二項分布尾端機率加 Bonferroni 校正；無標註位移
  則用期望的巧合次數）。
- 偵測以舊版 UniProt 序列建立的 AlphaFold DB 模型：把 UniProt 標註換算到模型位置，並指出序列與
  現行 UniProt 相同的模型。
- 輸出格式：文字、TSV、JSON；結束代碼 0／1／2。
- 本機快取、`--offline` 離線模式、逐次加長等待的網路重試、不會寫一半的快取檔、快取「查無模型」的
  結果；不需要任何第三方套件；支援 Python 3.9 以上。
- 用 735 個 UniProt 天然變異做的準確度驗證（`benchmark/`）。
- 104 個離線測試；在 Linux、macOS、Windows 與 Python 3.9～3.13 上自動測試，並每週檢查一次真實的
  AlphaFold DB 與 UniProt API。

[尚未發布]: https://github.com/wangnick1004/af-confidence/compare/v0.1.0...main
[0.1.0]: https://github.com/wangnick1004/af-confidence/releases/tag/v0.1.0
