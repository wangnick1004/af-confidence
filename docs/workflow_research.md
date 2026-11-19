# AlphaFold 使用者的日常工作流程與整合規劃

調查日期：2026-11-19
目的：了解研究者實際怎麼使用 AlphaFold，找出 af-confidence 可以接入的位置。本文件也是作業影片的內容之一（見 `docs/video_handoff.md`）。

> 查證說明：本調查透過網路搜尋結果的摘要完成；本環境連不到 EBI 主站與 NCBI。**AFDB 自訂標註的格式**是直接從 AFDB 網站的前端程式碼確認的（2026-11-19），可信度最高；ChimeraX 指令細節在實作時已直接對照官方使用手冊（rbvi.ucsf.edu）確認。

---

## 一、日常工作流程

| 階段 | 常見做法 | 常用工具 |
|---|---|---|
| 1. 查詢瀏覽 | 用 UniProt 編號在 AFDB 網站查蛋白質，看 3D 結構、pLDDT、PAE；2025 年改版後可疊加 AlphaMissense 與**自訂標註** | AFDB 網站（2025 年報告超過 450 萬名使用者）[1] |
| 2. 下載與視覺化 | 下載模型，依 pLDDT 著色、標記突變、疊加 AlphaMissense | ChimeraX（內建 `alphafold fetch`）[4][5]、PyMOL（社群著色腳本）[8] |
| 3. 批次與程式化 | 用 Python／Jupyter 呼叫 AFDB API | Python、Colab |
| 4. 突變判讀 | 從基因體變異出發，加上 AlphaMissense 與結構資訊 | Ensembl VEP 外掛 [6][7]、ProtVar、UniProt |
| 5. AI 助理（新興） | 透過 MCP 讓 AI 助理查詢 AlphaFold 與 UniProt | 多個社群 MCP 伺服器 [9][10] |

結構生物學的用法可歸納為：補完實驗結構、擬合或驗證結構域、推論功能（例如指引突變實驗）[3]。

## 二、編號錯位發生在哪裡

錯誤發生在「**把文獻中的位置帶進階段 1、2**」的那一步：讀到論文寫 E6V，就直接在 AFDB 網站或 ChimeraX 找第 6 個位置。

- PDB 結構檔的編號問題早已有工具處理（PDBrenum、SIFTS）：作者可能不算起始甲硫胺酸或訊號胜肽 [11][12]。但這些工具處理的是 **PDB 檔與 UniProt** 之間的對應，不是**文獻寫法與 AFDB 模型**之間的對應。
- UniProt 更新序列會讓對應關係失效，已有工作流程因此出錯 [13]；本專案在準確度驗證中也發現同類案例（生物素酶 P43251）。
- Ensembl VEP 沒有逐個突變提供 pLDDT 的外掛 [6]；ChimeraX、PyMOL 沒有檢查編號的功能。

## 三、整合規劃（依優先順序）

| 優先 | 整合方式 | 接入階段 | 狀態 |
|---|---|---|---|
| 1 | **輸出 AFDB 自訂標註**：印出可直接貼進 AFDB 網頁的校正後位置 | 1 | ✅ 完成（`--format afdb`，見 README 第 8 節） |
| 2 | 輸出 ChimeraX 腳本（`.cxc`）：開啟正確模型並標記校正後位置 | 2 | ✅ 完成（`--format chimerax`，見 README 第 9 節）；指令依官方使用手冊撰寫，尚待在 Mac 上用 ChimeraX 實測 |
| 3 | Python 函式庫介面與 Colab 範例 | 3 | ✅ 完成（見 README 第 10 節；筆記本每週由 CI 實際執行） |
| 4 | 輸出 PyMOL 腳本（`.pml`） | 2 | 規劃中 |
| 5 | MCP 伺服器：讓 AI 助理先檢查編號 | 5 | 規劃中 |

不建議：Ensembl VEP 外掛（VEP 處理基因體座標，輸入對不上）、Galaxy／nf-core（與使用情境距離較遠）。

## 四、AFDB 自訂標註的規格（直接從 AFDB 前端程式碼確認）

- 2025-11-11 的 AFDB v8.2.1 加入「Custom annotations track」。
- 在模型頁的 Annotations 區打開對話框「**Add your annotation track**」，填兩個欄位：
  - **Track name**（範例：`My track, Important residues`；顯示時超過 14 個字元會被截斷）
  - **Residues or ranges**（範例：`1, 56, 24-52, 367-458`；格式為數字或範圍、以逗號分隔；不能超出序列長度）
- 按「**Add track**」加入。**只能手動輸入，不能上傳檔案**；資料只保存在瀏覽器分頁中，關閉即刪除。
- 加入的軌跡可以用「Custom tracks (all)」匯出成 CSV（欄位 `Track Name,Residues`）。
- 模型頁網址格式：`https://alphafold.ebi.ac.uk/entry/<模型編號>`，例如 `AF-P43251-4-F1`（異構體也適用）。
- 尚未確認：開啟對話框的按鈕文字（推測是標註檢視器上的圖示按鈕）。

---

## 參考來源

1. AlphaFold Protein Structure Database 2025: a redesigned interface and updated structural coverage. *Nucleic Acids Research* (2025). https://academic.oup.com/nar/advance-article/doi/10.1093/nar/gkaf1226/8340156
2. AlphaFold Database launches custom annotations feature (EMBL-EBI). https://www.ebi.ac.uk/about/news/updates-from-data-resources/alphafold-database-custom-annotations
3. Advantages and Limitations of AlphaFold in Structural Biology. *The Protein Journal* (2025). https://link.springer.com/article/10.1007/s10930-025-10310-8
4. ChimeraX `alphafold` command documentation. https://rbvi.ucsf.edu/chimerax/docs/user/commands/alphafold.html
5. Mapping mutation effects onto structures (ChimeraX + AlphaMissense tutorial). https://cambiotraining.github.io/protein-structure-prediction/materials/08-chimerax_alphamissense.html
6. VEP ProtVar plugin. https://raw.githubusercontent.com/ensembl-variation/VEP_plugins/main/ProtVar.pm
7. AlphaMissense data integrated into Ensembl, UniProt, DECIPHER and AlphaFold DB. https://www.ebi.ac.uk/about/news/technology-and-innovation/alphamissense-data-integration/
8. Color AlphaFold predictions according to the pLDDT value (PyMOL). https://research.uni-leipzig.de/straeter/pymol/pymol_AlphaFold.html
9. protein-mcp-server. https://mcpservers.org/zh-TW/servers/cyanheads/protein-mcp-server
10. AlphaFold MCP Server (Augmented Nature). https://lobehub.com/en/mcp/augmented-nature-alphafold-mcp-server
11. PDBrenum. *PLoS ONE* (2021). https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8259974/
12. SIFTS Methodology (PDBe). https://www.ebi.ac.uk/pdbe/docs/sifts/methodology.html
13. Residue-mapping error because of sequence change in UniProt (CroMaSt issue). https://gitlab.inria.fr/capsid.public_codes/CroMaSt/-/issues/1
