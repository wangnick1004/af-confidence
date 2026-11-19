# 貢獻指南

歡迎在 GitHub 的 Issues 回報問題或提出建議。最有幫助的是：一份工具給出錯誤或誤導答案的突變清單，
並附上該編號的出處（論文或資料庫）。

## 開發環境

```bash
git clone https://github.com/wangnick1004/af-confidence
cd af-confidence
python3 -m pip install -e . pytest
python3 -m pytest
```

## 開發原則

- 工具必須只用 Python 標準函式庫就能執行（不加入任何執行時需要的第三方套件），並支援 Python 3.9
  以上。
- 測試全部離線執行，使用 `data/cache` 中真實的 AlphaFold DB 與 UniProt 資料。要為測試新增一個
  蛋白質時，先連網執行一次工具並加上 `--cache data/cache`，再把新產生的檔案一起 commit。
- 每個建議都必須是精確的序列比對。修改證據強度的判斷方式時，請在修改前後各跑一次準確度驗證，
  比較結果：

  ```bash
  python3 benchmark/run_benchmark.py --cache /path/to/benchmark-cache
  ```

- 維持工具的範圍：只做編號對應，不重新判讀 pLDDT，也不預測突變的影響。
