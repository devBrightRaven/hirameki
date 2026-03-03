---
description: 進度快照寫入 daily note
arguments: [重點描述] — 可選，無則自動判斷
---

從 `~/.claude/CLAUDE.md` 讀取 `## Vault Structure`，取得 vault 路徑和 daily-notes、templates 資料夾位置。
若不存在或缺少必要欄位，停止並回應：「尚未完成初始設定，請先執行 `/hirameki:__init`」

記錄當前的工作進度快照，寫入當天的 daily note。一天內可執行多次，每次追加一個帶時間戳的區塊。

輸入：$ARGUMENTS（可選，用來描述這次 wrap 的重點。無參數則自動從 session 操作紀錄判斷）

掃描來源：
- 本次 session 的操作紀錄（建立、修改、刪除了哪些檔案）
- daily-notes 資料夾中今天的 daily note（格式 YYYY-MM-DD.md）

寫入目標：{daily-notes}/YYYY-MM-DD.md（今天日期）
- 如果檔案不存在且 templates 資料夾中有 daily.md，用模板建立
- 如果檔案不存在且沒有模板，建立只含 `# YYYY-MM-DD` 標題的檔案
- 如果已存在，在檔案末尾追加新的 Wrap 區塊，用水平線分隔

每次寫入的格式：

```
---

## Wrap [HH:MM]

### 完成
- [這個時段完成的具體事項，一筆一句話]

### 進行中
- [已開始但未完成的事項。如果沒有，標註「無」]

### 下一步
- [接下來要做的事。如果暫時沒有，標註「待定」]
```

規則：
- 時間戳使用本地時間 HH:MM 格式（24 小時制）
- 如果今天已有之前的 Wrap 區塊，不要修改之前的內容，只在末尾追加
- 如果 $ARGUMENTS 有描述，用它作為這次 Wrap 的重點方向來組織內容
- 寫入前顯示即將寫入的內容與目標檔案完整路徑，等確認後再執行
- 寫入後印出實際寫入的完整路徑

以 __init.md 中偵測到的語言撰寫。
