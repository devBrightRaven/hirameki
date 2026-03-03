---
description: Hirameki 初始設定 — vault 偵測、語言設定、資料夾解析、參考文件同步
---

## 概述

__init 負責首次設定 Hirameki 環境。設定完成後，結果寫入 `~/.claude/CLAUDE.md`，日常 commands 直接讀取，不再呼叫 __init。

## 日常 Commands 的讀取方式

所有其他 hirameki commands 在執行前：

1. 讀取 `~/.claude/CLAUDE.md` 中的 `## Vault Structure` 段落
2. 若不存在或缺少必要欄位 → 停止，回應：「尚未完成初始設定，請先執行 `/hirameki:__init`」
3. 若存在 → 直接使用，不做額外驗證
4. 若執行過程中發現路徑無效或讀取失敗 → 回應：「設定異常，請執行 `/hirameki:__init` 重新設定」

Vault 根目錄的判斷：`## Vault Structure` 中若有 `vault:` 欄位則使用該路徑；否則從 `~/.claude/CLAUDE.md` 的 `## Vault` 段落讀取 `path`。

## 執行模式

### 模式 A：首次設定

觸發條件：`~/.claude/CLAUDE.md` 不存在 `## Vault Structure`，或使用者主動執行 `/hirameki:__init` 且現有設定為空。

**步驟 1 — Vault 偵測**

依序嘗試：
1. 當前工作目錄有 `.obsidian/` → 設為 vault
2. 讀取 `~/.claude/CLAUDE.md` 的 `## Vault` 段落中的 `path`
3. 都沒有 → 詢問使用者提供完整路徑，確認路徑存在且含 `.obsidian/` 後，寫入 `~/.claude/CLAUDE.md`：
   ```
   ## Vault
   path: {路徑}
   ```

**步驟 2 — 語言設定**

詢問使用者：「Hirameki 輸出要用什麼語言？」
- 繁體中文
- English
- 日本語
- 其他（使用者自行輸入）

**步驟 3 — 資料夾解析**

在 vault 中依候選名稱順序匹配各用途資料夾（取第一個存在的）：

- **daily-notes**：`Daily/`, `_daily/`, `daily/`, `Journal/`, `journal/`
- **inbox**：`Inbox/`, `_inbox/`, `inbox/`, `_Capture/`, `Capture/`
- **analysis**：`_hirameki_analysis/`, `_agent_analysis/`, `_claude_code_analysis/`, `Analysis/`, `_analysis/`, `analysis/`
- **logs**：`_hirameki_logs/`, `_agent_logs/`, `_claude_code_feedback/`, `Logs/`, `_logs/`, `logs/`
- **templates**：`Templates/`, `_templates/`, `templates/`

找不到的用途 → 詢問使用者建立位置（預設建議第一個候選名稱），確認後建立。

**步驟 4 — 寫入設定**

將以下內容寫入 `~/.claude/CLAUDE.md`（不存在則建立）：

```
## Vault Structure
vault: {vault 完整路徑}
language: {語言}
daily-notes: {資料夾名稱}/
inbox: {資料夾名稱}/
analysis: {資料夾名稱}/
logs: {資料夾名稱}/
templates: {資料夾名稱}/
```

**步驟 5 — 參考文件同步**

- 檢查 `{vault}/_hirameki_cmds/` 是否存在
- 不存在 → 建立資料夾，複製對應語言的參考文件，印出：「參考文件已複製到 _hirameki_cmds/」
- 存在且非空 → 詢問使用者是否覆寫（使用者可能已有自訂修改）
- 存在且為空 → 直接複製

語言對應：
- 繁體中文 → `hirameki-cmds-short-zh-TW.md` + `hirameki-cmds-full-zh-TW.md`
- English / 日本語 / 其他 → `hirameki-cmds-short.md` + `hirameki-cmds-full.md`

若 plugin 來源檔案找不到（cache 被清除）→ 跳過此步驟，告知使用者手動前往 GitHub 下載。

---

### 模式 B：重新設定

觸發條件：`## Vault Structure` 已存在，使用者主動執行 `/hirameki:__init`。

讀取現有設定後，詢問使用者要更新什麼：
1. 語言設定
2. 特定資料夾路徑
3. 更新參考文件（`_hirameki_cmds/`）
4. 全部重新來過

只修改使用者選擇的項目，其他欄位保留不動。

全部重新來過時，走模式 A 的完整流程，並在覆寫現有設定前先確認。

## 掃描範圍解析

部分 commands 需要掃描使用者的內容資料夾時，計算方式如下：

vault 根目錄第一層資料夾，排除：
- `.` 開頭的隱藏資料夾（`.obsidian/`, `.claude/`, `.git/`, `.smart-env/` 等）
- `_hirameki_cmds/`
- `## Vault Structure` 中記錄的所有系統資料夾

剩下的全部視為使用者內容資料夾。若無內容資料夾，掃描 vault 根目錄下的所有 `.md` 檔案。
