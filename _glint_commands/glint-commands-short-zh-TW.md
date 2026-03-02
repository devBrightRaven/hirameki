# Glint 指令

在 Claude Code CLI 中使用。所有指令以 `/glint-` 開頭。

---

## 日常節奏

### `/glint-status`
Vault 現況摘要。掃描內容主題、各資料夾近期活動。
無需輸入。適合在 session 開始時執行。

### `/glint-catchup [天數]`
進度銜接。讀取最近的 Wrap 進度 + inbox 待處理項目，建議今日焦點。
可選輸入：天數（預設 1），例如 `/glint-catchup 3` 回顧最近 3 天。

### `/glint-wrap [描述]`
進度快照。記錄已完成、進行中、下一步 — 追加到當天的 daily note。一天可執行多次。
可選輸入：本次 wrap 的重點描述。
寫入：`{daily-notes}/YYYY-MM-DD.md`

### `/glint-weekreview`
週回顧。比對聲稱的優先事項與實際檔案變更，找出意圖與行動之間的落差。
無需輸入。需至少 3 天的 daily notes 才能做落差分析。

---

## 概念考古

### `/glint-arc {概念}`
追蹤一個概念在 vault 中的演化軌跡。從首次出現到目前狀態的時間軸。同概念同天追加更新。
範例：`/glint-arc 能動性`、`/glint-arc 極簡主義`
寫入：`{analysis}/arc/`

### `/glint-bridge {主題A} 與 {主題B}`
找出兩個主題之間的隱藏連結。列出直接交集、橋樑筆記、潛在深層連結假設。同組合同天追加更新。
範例：`/glint-bridge 無障礙 與 prompt engineering`
寫入：`{analysis}/bridge/`

### `/glint-undercurrent [範圍]`
發掘潛流主題。找出反覆出現但沒有獨立文章的主題。同天追加更新。
可選輸入：聚焦特定目錄。
寫入：`{analysis}/undercurrent/`

### `/glint-cluster [範圍]`
想法群聚分析。找出正在聚攏成形的筆記群。同天追加更新。
可選輸入：聚焦特定範圍。
寫入：`{analysis}/cluster/`

---

## 思考工具

### `/glint-ghost {問題} [save]`
用你的語氣回答問題。根據你的寫作風格和既有立場。
範例：`/glint-ghost AI agent 應該有多少自主權？`
標註哪些部分有 vault 依據、哪些是推測延伸。
末尾加 `save` 寫入檔案：`/glint-ghost AI 自主權的上限？ save`
寫入：`{analysis}/ghost/`

### `/glint-stress-test {主題} [save]`
論述壓力測試。找出矛盾、未驗證假設、邏輯跳躍、證據缺口。
範例：`/glint-stress-test prompt engineering 的極限`
末尾加 `save` 寫入檔案。
寫入：`{analysis}/stress-test/`

### `/glint-harvest [save]`
從既有內容中收割可行動的想法。四個類別：可以寫的文章、可以做的工具、值得研究的主題、可以聯繫的人。
無需輸入。每類上限 5 個，附來源筆記。
輸入 `save` 寫入檔案：`/glint-harvest save`
寫入：`{analysis}/harvest/`

### `/glint-graduate`
讓半成形想法畢業為獨立筆記。掃描最近 14 天的 daily notes、logs、inbox、drafts、thoughts。
無需輸入。兩階段：先列候選清單，確認後再執行。
寫入：使用者指定的內容資料夾

---

## 維護

### `/glint-tidy [fix]`
屬性健檢。檢查 vault 所有檔案的 frontmatter 是否有缺漏欄位、tag 不一致、冗餘屬性。輸出健康度分數。
無需輸入即可產出報告。輸入 `fix` 確認後自動修正：`/glint-tidy fix`
寫入：`{analysis}/tidy/`

---

## 紀錄

### `/glint-journal {描述}`
工作紀錄與思考文章。記錄做了什麼、為什麼、靈感連結、可能的改進。同主題同天自動追加。
範例：`/glint-journal slash command 命名重構`
寫入：`{logs}/YYYY-MM-DD-{主題}.md`

---

## 寫入行為一覽

| 指令 | 寫入位置 | 觸發條件 | 同天重複 |
|---|---|---|---|
| `/glint-wrap` | daily-notes | 總是 | 追加新 Wrap 區塊 |
| `/glint-journal` | logs | 總是 | 同主題追加，不同主題建新檔 |
| `/glint-arc` | analysis/arc | 總是 | 同概念追加，不同概念建新檔 |
| `/glint-bridge` | analysis/bridge | 總是 | 同組合追加 |
| `/glint-undercurrent` | analysis/undercurrent | 總是 | 追加更新 |
| `/glint-cluster` | analysis/cluster | 總是 | 追加更新 |
| `/glint-ghost` | analysis/ghost | 僅加 `save` | 同問題追加 |
| `/glint-stress-test` | analysis/stress-test | 僅加 `save` | 同主題追加 |
| `/glint-harvest` | analysis/harvest | 僅加 `save` | 追加更新 |
| `/glint-graduate` | 內容資料夾 | 確認後 | 每次獨立 |
| `/glint-tidy` | analysis/tidy | 總是 | 追加更新 |

所有寫入檔案的指令都會在寫入前顯示預覽和完整路徑。

輸出語言在首次執行時設定，儲存在 vault 的 CLAUDE.md 中。
