---
description: Hirameki 系統共用的 vault 偵測與資料夾解析邏輯（供其他 commands 引用，不單獨執行）
---

## Vault 偵測

依照以下順序找到 Obsidian vault：

1. 檢查當前工作目錄是否有 `.obsidian/` 資料夾 → 如果有，當前目錄就是 vault
2. 如果沒有，讀取 `~/.claude/CLAUDE.md`，找 `## Vault` 段落中的 `path` 設定
3. 如果都沒有，問使用者：「你的 Obsidian vault 在哪裡？請提供完整路徑」
   - 確認該路徑存在且包含 `.obsidian/`
   - 確認後寫入 `~/.claude/CLAUDE.md` 的 `## Vault` 段落：
     ```
     ## Vault
     path: {使用者提供的路徑}
     ```
   - 印出：「已記錄 vault 路徑：{路徑}」

## 語言偵測

檢查 vault 的 CLAUDE.md 中 `## Vault Structure` 是否已有 `language` 設定。

如果沒有，問使用者：「Hirameki 輸出要用什麼語言？」並提供選項：
- 繁體中文
- English
- 日本語
- 其他（使用者自行輸入）

將結果記錄到 vault 的 CLAUDE.md 的 `## Vault Structure` 段落中的 `language` 欄位。

之後所有 hirameki command 的輸出（終端顯示和檔案寫入）都使用這個語言。

## 資料夾解析

在 vault 中尋找以下用途的資料夾。每個用途有一組候選名稱，按順序匹配第一個存在的：

- **daily-notes**：`Daily/`, `_daily/`, `daily/`, `Journal/`, `journal/`
- **inbox**：`Inbox/`, `_inbox/`, `inbox/`, `_Capture/`, `Capture/`
- **analysis**：`_hirameki_analysis/`, `_agent_analysis/`, `_claude_code_analysis/`, `Analysis/`, `_analysis/`, `analysis/`
- **logs**：`_hirameki_logs/`, `_agent_logs/`, `_claude_code_feedback/`, `Logs/`, `_logs/`, `logs/`
- **templates**：`Templates/`, `_templates/`, `templates/`

如果某個用途找不到對應的資料夾：
1. 問使用者：「找不到 {用途} 資料夾。要建立在哪裡？建議名稱：{第一個候選名稱}」
2. 使用者確認或自訂名稱後，建立資料夾
3. 印出：「已建立：{vault 完整路徑}/{資料夾名稱}/」
4. 將結果記錄到 vault 根目錄的 `CLAUDE.md` 的 `## Vault Structure` 段落：
   ```
   ## Vault Structure
   language: {語言}
   daily-notes: {實際資料夾名稱}/
   inbox: {實際資料夾名稱}/
   analysis: {實際資料夾名稱}/
   logs: {實際資料夾名稱}/
   templates: {實際資料夾名稱}/
   ```

下次執行任何 hirameki command 時，如果 vault 的 CLAUDE.md 裡已有 `## Vault Structure`，直接讀取，不再偵測。

## 參考文件同步

_init 完成資料夾解析後，將 hirameki 的指令參考文件複製到 vault 中，方便使用者在 Obsidian 內查閱。

目標位置：`{vault}/_hirameki_cmds/`

邏輯：
1. 檢查 vault 中是否存在 `_hirameki_cmds/` 資料夾，沒有則建立
2. 根據語言設定選擇要複製的檔案：
   - 繁體中文 → `hirameki-cmds-short-zh-TW.md` + `hirameki-cmds-full-zh-TW.md`
   - English → `hirameki-cmds-short.md` + `hirameki-cmds-full.md`
   - 日本語 → 英文版（尚無日文版）
   - 其他 → 英文版
3. 比對 vault 中現有檔案與 plugin 來源檔案的內容，有差異才覆寫
4. 如果是首次複製，印出：「參考文件已複製到 {vault}/_hirameki_cmds/」
5. 如果有更新，印出：「參考文件已更新」
6. 如果沒有變化，不印出任何訊息

## 掃描範圍解析

部分 commands 需要掃描使用者的內容資料夾。內容資料夾的定義是：vault 根目錄下的第一層資料夾，排除以下之後剩下的全部：

**隱藏/工具資料夾（以 `.` 開頭的全部排除）：**
- `.obsidian/`, `.claude/`, `.git/`, `.smart-env/`, `.stfolder/`, `.stversions/` 等

**Hirameki 系統資料夾（記錄在 `## Vault Structure` 中的）：**
- daily-notes 對應的資料夾
- inbox 對應的資料夾
- analysis 對應的資料夾
- logs 對應的資料夾
- templates 對應的資料夾

排除以上之後，剩下的就是使用者的內容資料夾。例如使用者建了 `Writing/`、`Projects/`、`Research/`、`Notes/`，這些全部會被 status、weekreview、harvest、ghost、graduate 等 command 掃描。

如果 vault 裡除了系統資料夾外沒有任何其他資料夾，commands 會掃描 vault 根目錄下的所有 .md 檔案。
