# Hirameki 指令

在 Claude Code CLI 中使用。所有指令以 `/hirameki:` 開頭。

---

## Session 開始

### `/hirameki:catchup [天數]`
進度銜接。讀取最近的 Wrap 進度 + inbox 待處理項目，建議今日焦點。
可選輸入：天數（預設 1），例如 `/hirameki:catchup 3` 回顧最近 3 天。

## Session 結束

### `/hirameki:wrap [描述]`
進度快照。記錄已完成、進行中、下一步 — 追加到當天的 daily note。一天可執行多次。
可選輸入：本次 wrap 的重點描述。
寫入：`{daily-notes}/YYYY-MM-DD.md`

## 查看 Vault 狀態

### `/hirameki:pulse [week|patterns]`
三種模式：
- **`pulse`** — 即時概覽：內容主題、近期活動、統計數據。適合 session 開始時執行。
- **`pulse week`** — 週回顧：比對聲稱的優先事項與實際檔案變更，找出落差。
- **`pulse patterns`** — 潛流與聚攏：找出反覆出現但沒有獨立文章的主題，以及正在形成的想法群。

## 深入一個特定想法

### `/hirameki:explore {輸入} [save]`
概念挖掘 — 根據輸入形式自動選擇模式：
- **單一概念** → Arc：該概念在 vault 中的演化時間軸
- **A 與 B**（或 A and B / A と B）→ Bridge：兩個主題之間的隱藏連結
- **以 `?` 或 `？` 結尾** → Ghost：用你的語氣回答，標注 vault 依據與推測
- **以 `test:` 開頭** → Stress-test：找出矛盾、缺口、未驗證假設

末尾加 `save` 可寫入檔案。
寫入：`{analysis}/arc/`、`{analysis}/bridge/`、`{analysis}/ghost/`、`{analysis}/stress-test/`

## 行動規劃

### `/hirameki:harvest [save]`
從既有內容中收割可行動的想法。七個類別（各最多 5 個）：
可以寫的文章 / 可以做的工具或專案 / 值得研究的主題 / 可以聯繫的人或社群 / 適合換個媒介的想法 / 尚未變現的價值 / 可以畢業的想法

畢業類別：兩階段 — 先確認候選清單，選擇後才建立檔案。
末尾加 `save` 可寫入摘要。
寫入：`{analysis}/harvest/`；畢業項目寫入使用者指定的內容資料夾

## 決策支援

### `/hirameki:decide {主題}`
決策前掃描。掃描 vault 相關脈絡，輸出三層結構：現況（含可逆性判斷）、卡點（反轉法找出失敗條件）、關鍵問（一個問題，不是建議）。
不寫入檔案。想保存請接著執行 `/hirameki:journal`。

## 維護

### `/hirameki:tidy [tags|fix|full]`
屬性健檢。預設只跑缺漏 + 一致性（輕量）。
- **`tidy`** — 缺漏 + 一致性檢查
- **`tidy tags`** — tag 收斂分析（核心標籤、孤立標籤、合併建議）
- **`tidy fix`** — 缺漏 + 一致性 + 自動修正
- **`tidy full`** — 全部區塊

寫入：`{analysis}/tidy/`

## 工作推理紀錄

### `/hirameki:journal {描述}`
工作紀錄與思考文章。記錄做了什麼、為什麼、靈感連結、未完成事項。同主題同天自動追加。
範例：`/hirameki:journal 重構 slash command 前綴`
寫入：`{logs}/YYYY-MM-DD-HHMM-{主題}.md`

---

## 寫入行為一覽

| 指令 | 寫入位置 | 觸發條件 | 同天重複 |
|------|----------|----------|----------|
| `/hirameki:wrap` | daily-notes | 總是 | 追加新 Wrap 區塊 |
| `/hirameki:journal` | logs | 總是 | 同主題追加，不同主題建新檔 |
| `/hirameki:explore` | analysis/arc, bridge, ghost, stress-test | 僅加 `save` | 同概念/問題追加 |
| `/hirameki:harvest` | analysis/harvest | 僅加 `save` | 追加更新 |
| `/hirameki:harvest`（畢業） | 內容資料夾 | 確認後 | 每次建新檔 |
| `/hirameki:tidy` | analysis/tidy | 總是 | 追加更新 |

所有寫入檔案的指令都會在寫入前顯示預覽和完整路徑。

輸出語言在首次執行 `/hirameki:__init` 時設定，儲存在 `~/.claude/CLAUDE.md` 中。
