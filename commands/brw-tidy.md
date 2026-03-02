---
description: 屬性健檢與精簡
arguments: [fix] — 可選，加 fix 直接修正
---

先執行 _brw-init.md 中的 vault 偵測與資料夾解析，取得 vault 路徑和所有內容資料夾清單。

定期檢查 vault 中所有 .md 檔案的 YAML frontmatter 屬性，找出缺漏、不一致、冗餘的問題，並提出精簡建議。

輸入：$ARGUMENTS（可選。無參數則純報告。輸入 "fix" 則在確認後直接修正）

掃描範圍：
- 所有內容資料夾（遞迴）
- inbox 資料夾全部
- daily-notes 資料夾最近 30 天

## 檢查項目

### 1. 缺漏檢查
- 沒有 frontmatter 的檔案
- 有 frontmatter 但缺少必要欄位的檔案（必要欄位：tags, status）
- `tags` 為空陣列或未填寫
- `status` 未填寫

### 2. 一致性檢查
- `status` 值是否在允許範圍內（published, draft, reference, outline, spec, log, archive）
- `source` 值是否在允許範圍內（self, claude-code, agent, external）——如果有填寫的話
- `tags` 中是否有大小寫不一致的同義標籤（例如 `AI-alignment` 和 `ai-alignment`）
- `tags` 中是否有底線 vs 連字號不一致（例如 `ai_alignment` 和 `ai-alignment`）
- `topic` 與 `tags` 是否有明顯重複（例如 topic: accessibility 同時 tags 裡也有 accessibility）

### 3. 冗餘檢查
- 全 vault 中只出現一次的 tag（可能是拼錯或過度細分）
- 超過 6 個 tags 的檔案（可能需要精簡）
- `created` 欄位格式是否一致（應為 YYYY-MM 或 YYYY-MM-DD）

### 4. Tag 收斂建議
統計全 vault 的 tag 使用頻率，找出：
- 語意相近但命名不同的 tags（列出候選合併組）
- 使用次數最多的前 10 個 tags（作為核心標籤參考）
- 使用次數只有 1 次的 tags（逐一列出，建議合併或刪除）

## 輸出格式

```
# 屬性健檢報告

> 檢查時間：YYYY-MM-DD HH:MM
> 掃描範圍：[列出實際掃描的目錄]
> 掃描檔案數：N

## 缺漏問題（N 個）
- [[檔名]] — 缺少 frontmatter / 缺少 tags / 缺少 status
...

## 一致性問題（N 個）
- [[檔名]] — status 值 "xxx" 不在允許範圍
- Tag 大小寫不一致：`AI-alignment`（3 次）vs `ai-alignment`（5 次）→ 建議統一為 `ai-alignment`
...

## 冗餘問題（N 個）
- [[檔名]] — 有 8 個 tags，建議精簡
- Tag `xxx` 只出現 1 次，於 [[檔名]]
...

## Tag 總覽
### 核心標籤（前 10）
| Tag | 使用次數 |
|-----|---------|
| ... | ... |

### 建議合併
- `ai_alignment` → `ai-alignment`（共 N 個檔案需更新）
...

### 孤立標籤（僅出現 1 次）
| Tag | 出現於 |
|-----|--------|
| ... | [[...]] |

## 摘要
- 需修正：N 個檔案
- 建議精簡：N 個標籤
- 健康度：N%（無問題檔案數 / 總檔案數）
```

如果某個區塊沒有問題，標註「無」而不是跳過。

以 _brw-init.md 中偵測到的語言撰寫。

## 修正邏輯（僅當 $ARGUMENTS 包含 "fix" 時執行）

修正前先顯示即將執行的所有變更清單，等確認後再執行。

可自動修正的項目：
- 補上缺少的 frontmatter 骨架（空的 tags 和 status: draft）
- 統一 tag 大小寫（以使用次數多的為準）
- 統一底線 vs 連字號（以連字號為準）
- 移除 `topic` 與 `tags` 的明顯重複（保留 tags 中的，移除 topic）

需要使用者逐一確認的項目：
- 合併語意相近的 tags
- 精簡超過 6 個 tags 的檔案
- 刪除孤立標籤

修正後重新計算健康度並輸出差異摘要。

## 寫入邏輯

每次執行都將報告寫入：{analysis}/tidy/YYYY-MM-DD.md
如果資料夾不存在，先建立。

如果同一天已有報告，追加在末尾：

```
---

## 追蹤更新 [HH:MM]

### 變更摘要
- [本次修正了什麼、還剩什麼未處理]

### 健康度變化
- 上次：N% → 本次：N%
```

規則：
- 所有檔案引用使用 [[wiki link]] 格式
- 時間戳使用本地時間 HH:MM 格式（24 小時制）
- 寫入前顯示即將寫入的檔名和完整路徑，等確認後再執行
- 寫入後印出實際寫入的完整路徑
- 每次掃描最多報告 50 個問題，超過的標註總數並建議分批處理
