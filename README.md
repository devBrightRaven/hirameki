# Hirameki 閃き

> Obsidian vault knowledge management commands for [Claude Code](https://claude.com/claude-code).

<div align="center">
  <a href="#english">English</a> &nbsp;|&nbsp; <a href="#繁體中文">繁體中文</a> &nbsp;|&nbsp; <a href="#日本語">日本語</a>
</div>

---

<details open>
<summary><h2 id="english">English</h2></summary>

### Inspiration

Hirameki is inspired by [internetvin](https://x.com/internetvin) — specifically the workflow shown in this video by [Greg Isenberg](https://x.com/gregisenberg), CEO of [Late Checkout](https://latecheckout.agency) and creator of [Idea Browser](https://www.ideabrowser.com):

**[How I Use Obsidian + Claude Code to Run My Life](https://youtu.be/6MBq1paspVU)**

The idea: your Obsidian vault is a goldmine of accumulated thinking. Hirameki gives Claude Code the commands to excavate, connect, and act on what's already there — rather than starting from scratch every time.

> **What is an Obsidian vault?** [Obsidian](https://obsidian.md) is a free note-taking app that stores everything as plain markdown files in a local folder — your "vault". No cloud lock-in, no proprietary format. Because it's just files, Claude Code can read and write directly to it.

---

### Install

```bash
# 1. Add the marketplace
claude /plugin marketplace add devBrightRaven/hirameki

# 2. Install the plugin
claude /plugin install hirameki@hirameki
```

---

### Setup (one time)

Run `/hirameki:__init` once. It handles everything — vault detection, language, folder mapping, and copying reference docs into your vault.

**Fastest path — open Claude Code from inside your vault:**

```bash
cd /path/to/your/obsidian-vault
claude
/hirameki:__init
```

Vault is auto-detected. No path needed.

**From anywhere else — run it wherever you are:**

```bash
claude   # anywhere
/hirameki:__init
```

`__init` reads Obsidian's app config to find your vaults automatically — no need to know the path. If you have multiple vaults, it shows a list to choose from.

Either way, the vault path is saved globally to `~/.claude/CLAUDE.md`. After setup, every Hirameki command works no matter where you open Claude Code.

---

### Commands

7 commands, grouped by when you reach for them.

---

#### Session Start

**`/hirameki:catchup [days]`**

*Use when: you're reopening the vault after time away and need to pick up the thread.*

Progress catchup. Reads the last Wrap block from recent daily notes and all inbox items, then suggests 1–3 things to focus on today. Default: yesterday. Example: `/hirameki:catchup 3` reviews the last 3 days.

---

#### Session End

**`/hirameki:wrap [description]`**

*Use when: you're done for the day (or pausing a session) and want a record of what happened.*

Progress snapshot. Scans session file activity, appends a timestamped block to today's daily note with: completed, in-progress, and next steps. Can run multiple times a day — each run appends a new block. Optional: describe the session focus to shape the summary.

---

#### Vault State Check

**`/hirameki:pulse [week|patterns]`**

*Use when: you want to know what's going on across your vault without diving in manually.*

Three modes depending on what you need:

- **`/hirameki:pulse`** — Immediate snapshot. Scans all content folders (depth 2) and the last 7 days of daily notes. Shows content topics per folder, recent file changes, and vault-wide counts. Good to run at session start.

- **`/hirameki:pulse week`** — Weekly gap analysis. Compares what you said was a priority (from daily notes) against what you actually worked on (from file changes). Surfaces drift between intentions and effort. Requires at least 3 days of daily notes.

- **`/hirameki:pulse patterns`** — Undercurrents and clusters. Surfaces recurring themes without dedicated articles (appears in 3+ files, no standalone write-up), and groups of notes converging on unnamed themes. Good for finding what's been quietly accumulating.

---

#### Deep Work on a Specific Idea

**`/hirameki:explore {input} [save]`**

*Use when: you want to dig into a concept, find hidden connections, get a draft take in your voice, or pressure-test an argument.*

One command that detects mode from the shape of your input:

| Input shape | Mode | What it does |
|-------------|------|-------------|
| Single concept | **Arc** | Tracks evolution of that concept across your vault — timeline from first mention to current state |
| Two topics with `and` / `與` / `と` | **Bridge** | Finds hidden connections between the two — shared files, bridge notes, deep hypotheses |
| Ends with `?` | **Ghost** | Answers in your voice — extracts your existing stances and style, then drafts a response |
| Starts with `test:` | **Stress-test** | Pressure-tests your arguments — finds contradictions, gaps, and unverified assumptions |

Add `save` at the end to write the result to file. Examples:
- `explore 能動性` — arc
- `explore design and engineering` — bridge
- `explore Should I publish more? save` — ghost, saved to file
- `explore test: the limits of prompt engineering` — stress-test

**When to reach for each mode:**
- **Arc**: you keep returning to the same concept and want to see how your thinking has changed
- **Bridge**: two interests that feel separate but might be related, and you want to find out
- **Ghost**: you need a first draft or a position statement, in your actual voice
- **Stress-test**: before publishing something — find the holes before your readers do

---

#### Action Planning

**`/hirameki:harvest [save]`**

*Use when: you have a lot of accumulated content and want to know what to do with it.*

Harvests actionable ideas from existing content. Scans content folders, 30 days of daily notes, and inbox. Outputs seven categories (max 5 each):

1. **Articles you could write** — topics with enough material to develop now
2. **Tools or projects to build** — tool needs, pain points, or product ideas mentioned in your notes
3. **Topics worth researching** — things mentioned but not explored
4. **People or communities to contact** — mentioned and relevant to where you're headed
5. **Ideas that want a different medium** — content better suited to video, visual, talk, or newsletter
6. **Value you're not transacting on** — expertise worth productizing or pitching
7. **Ideas ready to graduate** — half-formed ideas dense enough to become a standalone note

The graduate category has a second phase: after seeing the candidates, you confirm which ones to execute. Each selected idea gets a new note in the appropriate content folder, with source context and wiki links back to related notes.

Add `save` to write the harvest summary to file.

---

#### Housekeeping

**`/hirameki:tidy [fix]`**

*Use when: you notice your frontmatter has drifted, tags have multiplied inconsistently, or you want a health check before a big push.*

Frontmatter properties audit. Scans all content folders, inbox, and 30 days of daily notes. Checks: missing fields (no frontmatter, no tags, no status), consistency issues (invalid values, tag casing, underscores vs hyphens), redundancy (single-use tags, files with 6+ tags, topic/tag duplicates), and tag convergence (frequency stats, merge candidates, orphan tags). Outputs a health score. Add `fix` to auto-correct what's safe to automate, with confirmation prompts for judgment calls.

---

#### Work Reasoning Log

**`/hirameki:journal {topic}`**

*Use when: you made a non-obvious decision and want to record why — so future-you (or a collaborator) can understand the reasoning.*

Work log with reasoning. Writes a structured entry covering: background, what you did, why you did it, inspiration connections, possible improvements, and open follow-ups. Same topic, same day: appends an update section and marks completed follow-ups. Searches related vault notes to surface context and [[wiki links]].

Different from `wrap`: wrap records what happened in a session. Journal records why you made a specific decision.

---

#### Decision Support

**`/hirameki:decide {topic}`**

*Use when: you're facing a decision and want to see what your vault already knows about it before committing.*

Pre-decision scan. Searches all content folders and the last 14 days of notes for relevant context, then outputs three layers: **Current State** (what the vault knows, plus a reversibility check — two-way door vs. one-way door), **Friction** (inversion: what conditions would guarantee this fails?), and **Key Question** (one question — if you knew this, the decision would be clear).

Does not write to file. To save the output, run `/hirameki:journal` afterward.

---

### Why commands, not agents

Hirameki is built as explicit commands rather than an autonomous background agent. Two reasons:

**Safety.** Every command that writes a file shows you the full content and target path before anything happens. Read-only commands (`pulse`, `explore`) produce output you can act on or discard — they never touch your vault unless you explicitly ask. Write commands (`wrap`, `journal`, `harvest`) require confirmation at the point of writing. `tidy fix` separates what it can safely automate from what needs your judgment.

> **Limitation**: these safety behaviors are instructions written into each command prompt — not hard-coded enforcement. Claude follows them reliably in practice, but there is no programmatic gate that makes confirmation technically impossible to skip. This is a current constraint of how Claude Code commands work, not something Hirameki can resolve on its own.

**You stay in control.** The commands surface patterns, connections, and suggestions — but every decision is yours. `harvest` identifies candidates but waits for you to choose which ideas are ready to graduate. `explore test:` finds weaknesses in your arguments but doesn't rewrite them. `explore ?` drafts in your voice but marks what's grounded in evidence vs. inferred from style.

Your vault is a record of how *you* actually think. The goal is to amplify that — not to have a system quietly reshaping it.

---

### How it works

1. **Config**: Settings live in `~/.claude/CLAUDE.md` under `## Vault Structure` — vault path, language, and folder mappings. Written once by `/hirameki:__init`, read by all other commands.
2. **Folder detection**: Commands look for common folder names (`_daily/`, `Daily/`, `Journal/` etc.). Missing folders are created on first use and saved to config.
3. **Content scanning**: All non-system folders in your vault root are treated as "content folders" — whatever structure you use, commands adapt.
4. **Write safety**: Every command that writes a file shows a full preview and path before writing. Nothing is written without confirmation.

---

### Folder name detection

`__init` looks for these folder names in your vault root, in order. First match wins. If none are found, it asks where to create the folder.

<details>
<summary>Detected folder names</summary>

| Purpose | Detected names (checked in this order) |
|---------|----------------------------------------|
| daily-notes | `Daily/` `_daily/` `daily/` `Journal/` `journal/` |
| inbox | `Inbox/` `_inbox/` `inbox/` `_Capture/` `Capture/` |
| analysis | `_hirameki_analysis/` `_agent_analysis/` `_claude_code_analysis/` `Analysis/` `_analysis/` `analysis/` |
| logs | `_hirameki_logs/` `_agent_logs/` `_claude_code_logs/` `Logs/` `_logs/` `logs/` |
| templates | `Templates/` `_templates/` `templates/` |

If your vault uses a different name, `__init` will ask and save your choice. The saved mapping is what all commands use — the detection list only runs once.

</details>

---

### Known Limitations

1. **Vault must be local.** Cloud-only vaults are not supported. iCloud or Google Drive sync can cause file conflicts when Claude Code reads/writes simultaneously with the sync client.
2. **Vault structure assumptions.** Commands expect specific folders (daily notes, journal, research, etc.). Running `/hirameki:__init` is required to map your vault structure before other commands work.
3. **No incremental indexing.** Commands like `/harvest` and `/lucky` scan the vault on each invocation. On large vaults (1000+ notes), this can be noticeably slow.
4. **Hooks run on every session.** Hook scripts (catchup reminders, extract actions, etc.) execute on every Claude Code session start/stop. There is no per-project opt-out mechanism.
5. **No offline LLM support.** All analysis goes through the Claude API. An active Claude subscription is required.
6. **Language detection is manual.** The vault language is set once during `__init`. There is no auto-detection from vault content.
7. **No concurrent write protection.** If multiple Claude Code sessions write to the same daily note simultaneously, there is no conflict resolution — the last write wins.

---

### License

MIT

</details>

---

<details>
<summary><h2 id="繁體中文">繁體中文</h2></summary>

### 靈感來源

Hirameki 的靈感來自 [internetvin](https://x.com/internetvin)，尤其是 [Greg Isenberg](https://x.com/gregisenberg)（[Late Checkout](https://latecheckout.agency) CEO、[Idea Browser](https://www.ideabrowser.com) 創辦人）在這支影片中展示的工作流程：

**[How I Use Obsidian + Claude Code to Run My Life](https://youtu.be/6MBq1paspVU)**

核心概念：你的 Obsidian vault 是多年累積思考的寶庫。Hirameki 讓 Claude Code 能夠挖掘、串聯並行動 — 而不是每次都從零開始。

> **什麼是 Obsidian vault？** [Obsidian](https://obsidian.md) 是一款免費的筆記軟體，所有內容以純 markdown 檔案儲存在本地資料夾（即「vault」）。沒有雲端鎖定、沒有專有格式。因為一切都是純文字檔案，Claude Code 可以直接讀寫。

---

### 安裝

```bash
# 1. 加入 marketplace
claude /plugin marketplace add devBrightRaven/hirameki

# 2. 安裝 plugin
claude /plugin install hirameki@hirameki
```

---

### 初始設定（只做一次）

執行 `/hirameki:__init`，它會自動處理所有設定：vault 偵測、語言、資料夾對應、複製參考文件到 vault。

**最快的方式 — 在 vault 目錄裡開啟 Claude Code：**

```bash
cd /path/to/your/obsidian-vault
claude
/hirameki:__init
```

路徑自動偵測，不需要手動輸入。

**從其他地方開啟也可以：**

```bash
claude   # 任何地方
/hirameki:__init
```

`__init` 會自動讀取 Obsidian 的 app 設定檔，找出你已有的 vault，不需要手動輸入路徑。有多個 vault 時會列出清單讓你選擇。

設定完成後，vault 路徑存入 `~/.claude/CLAUDE.md`。之後不管在哪裡開啟 Claude Code，所有 Hirameki 指令都能正常運作。

---

### 指令說明

7 個指令，依照使用時機分組。

---

#### Session 開始

**`/hirameki:catchup [天數]`**

*適合：重新打開 vault，需要接回上次的思路時。*

進度銜接。讀取最近 daily notes 的最後一個 Wrap 區塊和所有 inbox 項目，提出 1–3 個今日建議焦點。預設為昨天。範例：`/hirameki:catchup 3` 回顧最近 3 天。

---

#### Session 結束

**`/hirameki:wrap [描述]`**

*適合：一天結束（或暫停 session）時，記錄發生了什麼。*

進度快照。掃描本次 session 的檔案操作，在今天的 daily note 末尾追加一個帶時間戳的區塊，包含：已完成、進行中、下一步。可一天執行多次，每次追加新區塊。可加入描述來聚焦摘要方向。

---

#### 查看 Vault 狀態

**`/hirameki:pulse [week|patterns]`**

*適合：想不深入文件就能掌握 vault 整體狀況時。*

三種模式：

- **`/hirameki:pulse`** — 即時概覽。掃描所有內容資料夾（深度 2 層）和最近 7 天 daily notes。顯示各資料夾的主題與活躍狀態、最近的檔案變更、vault 整體統計。適合每次 session 開始時執行。

- **`/hirameki:pulse week`** — 週回顧與落差分析。比對 daily notes 中聲稱的優先事項與實際的檔案變更，找出意圖與行動之間的落差。需要至少 3 天的 daily notes。

- **`/hirameki:pulse patterns`** — 潛流與聚攏分析。找出繁複出現但沒有獨立文章的主題（出現在 3 個以上不同檔案），以及正在聚攏成形但尚未命名的筆記群。適合找出悄悄在積累的東西。

---

#### 深入一個特定想法

**`/hirameki:explore {輸入} [save]`**

*適合：想挖掘一個概念、找到隱藏連結、用自己的語氣起草觀點，或壓力測試一個論述時。*

一個指令，根據輸入的形式自動選擇模式：

| 輸入格式 | 模式 | 做什麼 |
|----------|------|--------|
| 單一概念 | **Arc** | 追蹤該概念在 vault 中的演化，從首次出現到目前狀態的時間軸 |
| 兩個主題，以「與」、「and」或「と」分隔 | **Bridge** | 找出兩者之間的隱藏連結 — 共同提及的檔案、橋樑筆記、深層假設 |
| 以 `?` 或 `？` 結尾 | **Ghost** | 用你的語氣回答 — 提取你既有的立場和文風，然後起草回應 |
| 以 `test:` 開頭 | **Stress-test** | 壓力測試你的論述 — 找出矛盾、缺口、未驗證的假設 |

末尾加 `save` 可將結果寫入檔案。範例：
- `explore 能動性` — arc
- `explore 設計 與 工程` — bridge
- `explore 我應該多發表嗎？ save` — ghost，存入檔案
- `explore test: prompt engineering 的極限` — stress-test

**各模式的使用時機：**
- **Arc**：你不斷回到同一個概念，想看看自己的思考如何演變
- **Bridge**：兩個感覺分開但可能相關的興趣，想找出連結
- **Ghost**：需要一個初稿或立場陳述，用自己真實的語氣
- **Stress-test**：發表前 — 在讀者找到漏洞之前先找到它

---

#### 行動規劃

**`/hirameki:harvest [save]`**

*適合：累積了大量內容，想知道下一步該怎麼做時。*

從既有內容收割可行動想法。掃描內容資料夾、30 天 daily notes、inbox。輸出七個類別（各最多 5 個）：

1. **可以寫的文章** — 已有足夠素材可以發展的主題
2. **可以做的工具或專案** — 筆記中提到的工具需求、流程痛點、產品想法
3. **值得研究的主題** — 被提及但未深入探討的東西
4. **可以聯繫的人或社群** — 被提及且與你目前方向相關的人
5. **適合換個媒介的想法** — 更適合影片、視覺圖表、演講或電子報的內容
6. **尚未變現的價值** — 值得產品化或推銷的專業知識
7. **可以畢業的想法** — 半成形但已有足夠密度可以獨立成筆記的想法

「可以畢業的想法」有第二階段：看到候選清單後，你確認哪些要執行畢業。每個選中的想法會在對應的內容資料夾下建立新筆記，附上出處脈絡和 wiki link 連回相關筆記。

末尾加 `save` 可將收割摘要寫入檔案。

---

#### 維護

**`/hirameki:tidy [fix]`**

*適合：發現 frontmatter 開始亂掉、tag 越來越不一致，或在一次大整理前先做健檢時。*

屬性健檢。掃描所有內容資料夾、inbox 和 30 天 daily notes。檢查：缺漏欄位（無 frontmatter、無 tags、無 status）、一致性問題（無效值、tag 大小寫、底線 vs 連字號）、冗餘（只出現 1 次的 tag、超過 6 個 tag 的檔案、topic/tag 重複）、tag 收斂（頻率統計、合併候選、孤立 tag）。輸出健康度分數。加 `fix` 自動修正可確定的問題，需判斷的逐一確認。

---

#### 工作推理紀錄

**`/hirameki:journal {描述}`**

*適合：做了一個不直觀的決定，想記錄下為什麼 — 讓未來的自己（或協作者）能理解推理過程時。*

工作紀錄與思考文章。寫入結構化記錄，包含：背景、做了什麼、為什麼這樣做、靈感連結、可能的改進方向、未完成事項。同主題同天：追加更新並標記已完成的後續。搜尋 vault 中相關筆記作為脈絡和 [[wiki link]]。

與 `wrap` 的差別：wrap 記錄一個 session 發生了什麼。journal 記錄你為什麼做某個特定決定。

---

#### 決策支援

**`/hirameki:decide {主題}`**

*適合：面對一個決定，想在承諾之前先看看 vault 裡已經知道什麼時。*

決策前掃描。搜尋所有內容資料夾和最近 14 天的筆記，找出相關脈絡，輸出三層：**現況**（vault 找到的內容，含可逆性判斷：雙向門 vs 單向門）、**卡點**（反轉法：什麼條件會讓這個決定確定搞砸）、**關鍵問**（一個問題——知道了這件事，決定就清楚了）。

不寫入檔案。想保存請接著執行 `/hirameki:journal`。

---

### 為什麼是指令，而不是 Agent

Hirameki 設計為明確的指令，而不是自主在背景運作的 Agent。兩個原因：

**安全性。** 所有寫入檔案的指令在執行前都會顯示完整內容和目標路徑。唯讀指令（`pulse`、`explore`）產出的結果你可以採用或忽略 — 沒有你的明確要求，它們不會動你的 vault。寫入指令（`wrap`、`journal`、`harvest`）在寫入時需要確認。`tidy fix` 把可以安全自動化的部分與需要你判斷的部分分開處理。

> **限制**：這些安全行為是寫入每個指令 prompt 中的規則 — 不是程式碼層面的強制機制。Claude 在實際執行時會遵守，但沒有任何程式閘道能從技術上確保確認步驟不可跳過。這是 Claude Code 指令系統目前的限制，不是 Hirameki 能自行解決的問題。

**主體可操控性。** 指令找出模式、連結和建議 — 但每個決定都是你的。`harvest` 找出候選想法，但等你決定哪些準備好了。`explore test:` 找出論述的弱點，但不會幫你改寫。`explore ?` 用你的語氣起草，但會標注哪些有 vault 依據、哪些是風格推測。

你的 vault 記錄的是*你*真實的思考方式。目標是放大這個 — 而不是讓一個系統在背後悄悄改塑它。

---

### 運作方式

1. **設定**：設定存在 `~/.claude/CLAUDE.md` 的 `## Vault Structure` 段落 — vault 路徑、語言、資料夾對應。由 `/hirameki:__init` 一次寫入，其他所有指令直接讀取。
2. **資料夾偵測**：指令依候選名稱順序尋找資料夾（`_daily/`、`Daily/`、`Journal/` 等）。找不到的在首次使用時建立並存入設定。
3. **內容掃描**：vault 根目錄下所有非系統資料夾視為「內容資料夾」— 無論你怎麼組織筆記，指令都能適應。
4. **寫入安全**：所有寫入檔案的指令在執行前都會顯示完整預覽和路徑。沒有確認不會寫入。

---

### 資料夾名稱偵測

`__init` 在 vault 根目錄依序尋找這些資料夾名稱，第一個找到的為準。找不到時會詢問建立位置。

<details>
<summary>偵測的資料夾名稱</summary>

| 用途 | 依序偵測的名稱 |
|------|---------------|
| daily-notes | `Daily/` `_daily/` `daily/` `Journal/` `journal/` |
| inbox | `Inbox/` `_inbox/` `inbox/` `_Capture/` `Capture/` |
| analysis | `_hirameki_analysis/` `_agent_analysis/` `_claude_code_analysis/` `Analysis/` `_analysis/` `analysis/` |
| logs | `_hirameki_logs/` `_agent_logs/` `_claude_code_logs/` `Logs/` `_logs/` `logs/` |
| templates | `Templates/` `_templates/` `templates/` |

如果你的 vault 使用不同的名稱，`__init` 會詢問並儲存你的選擇。儲存後所有指令直接讀取設定，偵測清單只在首次執行時使用一次。

</details>

---

### 已知限制

1. **Vault 必須在本機。** 不支援純雲端 vault。iCloud 或 Google Drive 同步在 Claude Code 同時讀寫時可能造成檔案衝突。
2. **假設特定的 vault 結構。** 指令預期特定資料夾（daily notes、journal、research 等）。必須先執行 `/hirameki:__init` 完成資料夾對應，其他指令才能正常運作。
3. **無增量索引。** `/harvest` 和 `/lucky` 等指令每次都會完整掃描 vault。大型 vault（1000+ 篇筆記）會有明顯延遲。
4. **Hook 在每次 session 都會執行。** Hook 腳本（catchup 提醒、action 擷取等）在每次 Claude Code session 啟動/結束時都會執行，無法依專案個別關閉。
5. **不支援離線 LLM。** 所有分析都透過 Claude API 進行，需要有效的 Claude 訂閱。
6. **語言偵測為手動設定。** Vault 語言在 `__init` 時設定一次，不會自動偵測 vault 內容的語言。
7. **無並行寫入保護。** 如果多個 Claude Code session 同時寫入同一份 daily note，沒有衝突解決機制 — 最後寫入的覆蓋前者。

---

### 授權

MIT

</details>

---

<details>
<summary><h2 id="日本語">日本語</h2></summary>

### インスピレーション

Hirameki は [internetvin](https://x.com/internetvin) — 特に [Late Checkout](https://latecheckout.agency) CEO・[Idea Browser](https://www.ideabrowser.com) 創業者の [Greg Isenberg](https://x.com/gregisenberg) がこの動画で紹介しているワークフローからインスパイアされています：

**[How I Use Obsidian + Claude Code to Run My Life](https://youtu.be/6MBq1paspVU)**

コアコンセプト：Obsidian vault は長年蓄積してきた思考の宝庫です。Hirameki は Claude Code に、すでにそこにあるものを掘り起こし・つなげ・行動に移すためのコマンドを与えます — 毎回ゼロから始めるのではなく。

> **Obsidian vault とは？** [Obsidian](https://obsidian.md) は無料のノートアプリで、すべてのコンテンツをローカルフォルダ（「vault」）にプレーンな markdown ファイルとして保存します。クラウドロックインなし、独自フォーマットなし。すべてがただのテキストファイルなので、Claude Code が直接読み書きできます。

---

### インストール

```bash
# 1. マーケットプレイスを追加
claude /plugin marketplace add devBrightRaven/hirameki

# 2. プラグインをインストール
claude /plugin install hirameki@hirameki
```

---

### セットアップ（1 回だけ）

`/hirameki:__init` を 1 回実行します。vault の検出・言語設定・フォルダのマッピング・リファレンスドキュメントのコピーをすべて自動で行います。

**最速の方法 — vault ディレクトリ内で Claude Code を開く：**

```bash
cd /path/to/your/obsidian-vault
claude
/hirameki:__init
```

パスは自動検出されます。手動入力不要。

**どこからでも実行できます：**

```bash
claude   # どこからでも
/hirameki:__init
```

`__init` は Obsidian のアプリ設定ファイルを自動的に読み込み、既存の vault を検出します。パスを手動で入力する必要はありません。複数の vault がある場合はリストから選択できます。

セットアップ後、vault パスは `~/.claude/CLAUDE.md` にグローバルに保存されます。以降は Claude Code をどこで開いても、すべての Hirameki コマンドが正常に動作します。

---

### コマンド説明

7 つのコマンド、使うタイミングでグループ化。

---

#### セッション開始

**`/hirameki:catchup [日数]`**

*使うとき：vault を再開して、前回の続きを拾い上げる必要があるとき。*

進捗の引き継ぎ。最近の daily notes の最後の Wrap ブロックとすべての inbox アイテムを読み込み、今日のフォーカスとして 1〜3 件を提案。デフォルト：昨日。例：`/hirameki:catchup 3` で直近 3 日を振り返る。

---

#### セッション終了

**`/hirameki:wrap [説明]`**

*使うとき：1 日が終わった（またはセッションを一時停止する）時に、何が起きたかを記録するとき。*

進捗スナップショット。セッションのファイル操作をスキャンし、今日の daily note の末尾にタイムスタンプ付きのブロックを追記。内容：完了・進行中・次のステップ。1 日に複数回実行可能で、毎回新しいブロックを追記。オプションで説明を追加すると要約の方向性が定まる。

---

#### Vault の状態確認

**`/hirameki:pulse [week|patterns]`**

*使うとき：ファイルを深く掘り下げずに vault 全体の状況を把握したいとき。*

3 つのモード：

- **`/hirameki:pulse`** — 即時スナップショット。すべてのコンテンツフォルダ（深さ 2 層）と直近 7 日の daily notes をスキャン。各フォルダのコンテンツテーマとアクティビティ状態・最近のファイル変更・vault 全体の統計を表示。セッション開始時に実行するのに最適。

- **`/hirameki:pulse week`** — 週次レビューとギャップ分析。daily notes で宣言した優先事項と実際のファイル変更を比較し、意図と行動のずれを表面化。最低 3 日分の daily notes が必要。

- **`/hirameki:pulse patterns`** — 潜流とクラスター分析。独立した記事がないのに繰り返し登場するテーマ（3 つ以上の異なるファイルに出現）と、名前のついていないテーマに収束しつつあるノートのグループを表面化。静かに蓄積されてきたものを見つけるのに最適。

---

#### 特定のアイデアを深掘り

**`/hirameki:explore {入力} [save]`**

*使うとき：概念を掘り下げたい、隠れたつながりを見つけたい、自分の語り口で草稿を書きたい、または論述を圧力テストしたいとき。*

入力の形から自動でモードを判断する 1 つのコマンド：

| 入力の形 | モード | 何をするか |
|----------|--------|-----------|
| 単一の概念 | **Arc** | その概念の vault 内での進化を追跡 — 初出から現在の状態までのタイムライン |
| 2 つのテーマを「と」「and」「與」で区切る | **Bridge** | 2 つの間の隠れたつながりを発見 — 共通ファイル・橋渡しノート・深層仮説 |
| `?`や`？`で終わる | **Ghost** | あなたの語り口で回答 — 既存のスタンスとスタイルを抽出して草稿を作成 |
| `test:` で始まる | **Stress-test** | 論述を圧力テスト — 矛盾・ギャップ・未検証の前提を発見 |

末尾に `save` を追加で結果をファイルに保存。例：
- `explore 能動性` — arc
- `explore design と engineering` — bridge
- `explore もっと発信すべき？ save` — ghost、ファイルに保存
- `explore test: prompt engineering の限界` — stress-test

**各モードを使うとき：**
- **Arc**：同じ概念に繰り返し戻ってきて、思考がどう変わったか見たいとき
- **Bridge**：別々に見える 2 つの興味が実はつながっているかもしれないと感じるとき
- **Ghost**：自分の実際の声で、初稿や立場表明が必要なとき
- **Stress-test**：公開前に — 読者に見つけられる前に穴を見つけるとき

---

#### アクションプランニング

**`/hirameki:harvest [save]`**

*使うとき：コンテンツが蓄積されていて、次に何をすべきか知りたいとき。*

既存コンテンツから実行可能なアイデアを収穫。コンテンツフォルダ・30 日分の daily notes・inbox をスキャン。7 カテゴリを出力（各最大 5 件）：

1. **書ける記事** — 今すぐ発展させるだけの素材があるテーマ
2. **作れるツールまたはプロジェクト** — ノートで言及されたツールのニーズ・痛点・プロダクトアイデア
3. **研究すべきテーマ** — 言及されたが深掘りされていないもの
4. **連絡すべき人またはコミュニティ** — 言及されていて、今の方向性に関連する人
5. **別のメディアで表現したいアイデア** — 動画・ビジュアル・講演・ニュースレターの方が合うコンテンツ
6. **まだ取引していない価値** — 商品化したり売り込む価値のある専門知識
7. **卒業できるアイデア** — 独立したノートになれるだけの密度を持つ半成形アイデア

「卒業できるアイデア」は第 2 フェーズあり：候補リストを確認した後、どれを実行するか選択。選んだアイデアは対応するコンテンツフォルダに新しいノートとして作成され、出典の脈絡と関連ノートへの wiki link が付く。

末尾に `save` を追加で収穫サマリーをファイルに保存。

---

#### メンテナンス

**`/hirameki:tidy [fix]`**

*使うとき：frontmatter が崩れてきた、タグの一貫性が失われてきた、または大きな整理の前に健全性チェックをしたいとき。*

プロパティの健全性チェック。すべてのコンテンツフォルダ・inbox・30 日分の daily notes をスキャン。確認項目：欠落フィールド（frontmatter なし・tags なし・status なし）・一貫性の問題（無効な値・タグの大小文字・アンダースコア vs ハイフン）・冗長性（1 回だけ登場するタグ・6 個超のタグを持つファイル・topic/tag の重複）・タグの収束（頻度統計・統合候補・孤立タグ）。健全性スコアを出力。`fix` を追加で確実なものを自動修正、判断が必要なものは個別確認。

---

#### 作業推論ログ

**`/hirameki:journal {説明}`**

*使うとき：直感的でない決断を下して、なぜそうしたかを記録したいとき — 将来の自分（または協力者）が推論を理解できるように。*

作業ログと思考記録。構造化された記録を書き込み：背景・何をしたか・なぜしたか・インスピレーションのつながり・改善の可能性・未完了事項。同テーマ・同日：追記更新し完了した後続事項をマーク。関連する vault ノートを検索して文脈と [[wiki link]] を提供。

`wrap` との違い：wrap はセッションで何が起きたかを記録。journal は特定の決断をなぜ下したかを記録。

---

#### 意思決定サポート

**`/hirameki:decide {テーマ}`**

*使うとき：何かを決断しようとしていて、コミットする前に vault が何を知っているか確認したいとき。*

意思決定前スキャン。全コンテンツフォルダと直近 14 日のノートを検索して関連コンテキストを探し、3 層で出力：**現状**（vault が知っていること＋可逆性判定：両方向ドア vs 一方向ドア）、**詰まりポイント**（逆算法：この決定が確実に失敗する条件は何か）、**核心の問い**（1 つの問い――これを知れば決定が明確になる）。

ファイルには書き込まない。保存したい場合は `/hirameki:journal` を続けて実行。

---

### なぜエージェントではなくコマンドなのか

Hirameki は、バックグラウンドで自律的に動くエージェントではなく、明示的なコマンドとして設計されています。理由は 2 つです。

**安全性。** ファイルを書き込むすべてのコマンドは、実行前に完全な内容と書き込み先パスを表示します。読み取り専用のコマンド（`pulse`・`explore`）は採用しても無視してもいい出力を生成するだけで、明示的な要求なしには vault に触れません。書き込みコマンド（`wrap`・`journal`・`harvest`）は書き込み時に確認を求めます。`tidy fix` は安全に自動化できる部分と、あなたの判断が必要な部分を分けて処理します。

> **制限**：これらの安全動作は各コマンドのプロンプトに書かれた指示であり、コードレベルの強制機構ではありません。Claude は実際の動作でこれを守りますが、確認ステップを技術的にスキップ不可能にするプログラムのゲートは存在しません。これは Claude Code のコマンドシステム現在の制約であり、Hirameki 単独では解決できない問題です。

**主体としての操作性。** コマンドはパターン・つながり・提案を表面化しますが、すべての判断はあなたのものです。`harvest` は候補を特定しますが、どのアイデアが卒業の準備できているかはあなたが決めます。`explore test:` は論述の弱点を見つけますが、書き直しはしません。`explore ?` はあなたの語り口で下書きしますが、根拠がある部分と推測の延長を明記します。

あなたの vault は、*あなた*が実際にどう考えるかの記録です。それを増幅するのが目的 — システムが静かに形を変えていくのではなく。

---

### 動作の仕組み

1. **設定**：設定は `~/.claude/CLAUDE.md` の `## Vault Structure` セクションに保存 — vault パス・言語・フォルダマッピング。`/hirameki:__init` が一度だけ書き込み、他のすべてのコマンドが直接読み込む。
2. **フォルダ検出**：候補名の順番でフォルダを探す（`_daily/`・`Daily/`・`Journal/` など）。見つからない場合は初回使用時に作成して設定に保存。
3. **コンテンツスキャン**：vault ルート直下のすべての非システムフォルダを「コンテンツフォルダ」として扱う — どのような構成でも適応。
4. **書き込み安全性**：ファイルを書き込むすべてのコマンドは実行前に完全なプレビューとパスを表示。確認なしには書き込まない。

---

### フォルダ名の検出

`__init` は vault ルートでこれらのフォルダ名を順番に探します。最初に見つかったものを使用。見つからない場合は作成場所を確認します。

<details>
<summary>検出されるフォルダ名</summary>

| 用途 | 検出順 |
|------|--------|
| daily-notes | `Daily/` `_daily/` `daily/` `Journal/` `journal/` |
| inbox | `Inbox/` `_inbox/` `inbox/` `_Capture/` `Capture/` |
| analysis | `_hirameki_analysis/` `_agent_analysis/` `_claude_code_analysis/` `Analysis/` `_analysis/` `analysis/` |
| logs | `_hirameki_logs/` `_agent_logs/` `_claude_code_logs/` `Logs/` `_logs/` `logs/` |
| templates | `Templates/` `_templates/` `templates/` |

vault が別の名前を使っている場合、`__init` が確認して選択を保存します。保存後はすべてのコマンドが設定を直接読み込みます。検出リストは初回のみ使用されます。

</details>

---

### 既知の制限事項

1. **Vault はローカルである必要があります。** クラウドのみの vault はサポートされていません。iCloud や Google Drive の同期は、Claude Code が同時に読み書きする際にファイルの競合を引き起こす可能性があります。
2. **特定の vault 構造を前提としています。** コマンドは特定のフォルダ（daily notes、journal、research など）を想定しています。他のコマンドが動作する前に `/hirameki:__init` を実行してフォルダのマッピングを完了する必要があります。
3. **増分インデックスなし。** `/harvest` や `/lucky` などのコマンドは、実行のたびに vault 全体をスキャンします。大規模な vault（1000 件以上のノート）では顕著な遅延が発生する可能性があります。
4. **フックは毎セッションで実行されます。** フックスクリプト（catchup リマインダー、アクション抽出など）は Claude Code のセッション開始/終了のたびに実行されます。プロジェクトごとにオプトアウトする仕組みはありません。
5. **オフライン LLM 非対応。** すべての分析は Claude API を経由します。有効な Claude サブスクリプションが必要です。
6. **言語検出は手動設定。** vault の言語は `__init` 実行時に一度だけ設定されます。vault の内容からの自動検出はありません。
7. **同時書き込み保護なし。** 複数の Claude Code セッションが同じ daily note に同時に書き込んだ場合、競合解決の仕組みはありません — 最後の書き込みが上書きします。

---

### ライセンス

MIT

</details>
