# 影片示範指令稿（工具段落，約 1～1.5 分鐘）

所有指令都使用 repo 內的快取資料，**錄影時不需要網路**。
錄影前先在終端機進入 repo 資料夾：

```bash
cd af-confidence
```

建議把終端機字體放大到 18pt 以上，視窗寬度至少 120 個字元，避免輸出被折行。

---

## 鏡頭 1：鐮刀型貧血（約 20 秒）

```bash
python3 -m af_confidence P68871 E6V --cache data/cache --offline
```

**畫面重點：** `model has P at 6, not E` 和 `+1: E7V matches; UniProt: initiator Met removed`

**旁白要點：** 教科書寫 E6V，但模型第 6 個是 P。工具指出正確位置是第 7 個，並說明原因：成熟蛋白質去掉了第一個甲硫胺酸，傳統編號從那之後才開始算。

**可並排畫面：** ProtVar 截圖（`docs/images/protvar_P68871_E6V.webp`），它改用 Pro6 繼續分析。

---

## 鏡頭 2：一整份文獻清單（約 30 秒）

```bash
cat examples/app_abeta_numbering.txt
```

```bash
python3 -m af_confidence P05067 -f examples/app_abeta_numbering.txt --cache data/cache --offline
```

**畫面重點：**
1. 四個突變都是 `+671`，原因是 UniProt 標註 Aβ 從第 672 個位置開始
2. **`!? D23N`**：照原本的寫法也對得上，但這是巧合

**旁白要點：** 阿茲海默症的文獻習慣用 Aβ 自己的編號。D23N 最危險：第 23 個位置剛好也是 D，任何網站都不會警告；只有把整份清單一起檢查，才看得出它應該是 D694N。

---

## 鏡頭 3：工具不會說得比證據更肯定（約 20 秒，可省略）

```bash
python3 -m af_confidence P05067 A2T --cache data/cache --offline
```

**畫面重點：** 只有一個突變時，所有建議都標示 `[weak]`

**旁白要點：** 單一突變很容易在某個片段上「剛好對得上」，所以工具只標示為弱證據，不會假裝確定。這也是在提醒使用者：要把來源裡的整份清單一起輸入。

---

## 結尾一句（約 10 秒）

**旁白要點：** 工具只做序列比對，不判斷突變是否致病，pLDDT 也照 AlphaFold 提供的數值顯示。程式碼開源在 GitHub。

---

## 錄影前檢查

- [ ] 三個指令都在你的 Mac 上跑過一次，輸出與本文件一致
- [ ] 終端機字體夠大、沒有折行
- [ ] 關掉通知，避免錄到彈出視窗
