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

Either way, `__init` writes a **split configuration**: your vault's folder structure goes into `<vault>/AGENTS.md` (agent-neutral — it travels with the vault and any AI agent can read it), and per-machine values (vault path, language) go into `~/.claude/vault-local.md`. After setup, every Hirameki command works no matter where you open Claude Code. If you sync `~/.claude/` across machines, `vault-local.md` should be gitignored — each machine runs `/hirameki:__init` once.

---

### Codex compatibility

Claude Code remains the command-native surface. The Codex adapter uses one umbrella skill with five primary purpose routes, permanent direct shortcuts and small transitional redirects. Only the needed contract is loaded; independent review uses the host's existing authorized pipeline. Each runtime resolves its own configuration; there is no other-agent migration fallback.

---

### Hirameki — five purpose-based entries — Detailed guide

> Version 2.2.0 consolidates the workflow entries; source validation, model acceptance, installation and scheduling are separate.

Every command reads its own `~/.claude/vault-local.md` only when vault access is needed, then `<vault>/AGENTS.md` (`## Vault Structure`) for canonical folders. Explicit task settings take precedence. Never read another agent's private configuration. Missing setup uses `/hirameki:__init`; setup writes require approval.

## Primary entries

| Entry | Purpose |
|---|---|
| `next` | Continue work, inspect effective tasks or blockers; `next tasks [N]`, `next stuck [N]`, `next week [N]`. |
| `lens` | Explore only the requested history, positions, relationships, weaknesses, opportunities or patterns; `lens cards` discovers concept cards and `lens random` requires an explicit request. |
| `compose` | Draft, edit, outline, voice, frame or review according to purpose; supplied drafts do not require a vault scan. |
| `decision-trace` | Form and preserve consequential choices without choosing for the user. |
| `triage` | Close with only useful wrap, journal, lesson or handoff drafts; no new confirmation before the first draft. |

## Specialized tools and permanent shortcuts

| Entry | Purpose |
|---|---|
| `tidy` | Maintenance: `tidy tasks` is read-only archive proposals; `tidy review` reviews corrections/lessons; `tidy snapshot` is read-only inventory. Claude bare tidy retains metadata checks; Codex bare tidy retains task proposals. |
| `mekiki` | External research intake; it does not start automatically during other workflows. |
| `init (`__init`)` | Configure the current machine and canonical folder layout; do not borrow another agent's setup. |
| `wrap` | Record one progress checkpoint without full triage. |
| `journal` | Record or append work, judgments or a qualified lesson. `journal review` uses the same `tidy review` capability. |
| `handoff` | Prepare a direct handoff without running full triage. |

## Migration redirects

Ten names remain as redirects for the first consolidation release only; eleven permanent callable names remain. Direct shortcuts do not expire. Host metadata hiding has not been verified.

| Old name | Destination |
|---|---|
| `arc` | lens history |
| `bridge` | lens bridge |
| `challenge` | lens challenge |
| `harvest` | lens opportunities |
| `graduate` | lens cards |
| `reflect` | compose voice |
| `frame` | compose frame |
| `critique` | compose review |
| `tasks` | next tasks; stuck → next stuck |
| `pulse` | next week; patterns → lens patterns; snapshot → tidy snapshot |

## Safety and evidence

Show complete content and target path before saving. `save all` covers only displayed drafts; display all remaining drafts before further writes. A changed draft needs a new display and approval. Analysis, redirect, rule-review proposal or a decision reminder is not write authority. Preserve partial success and retry only unfinished approved operations under the applicable contract.

An unresolved or forming trace may persist across sessions only after `save this`; it remains a discussion trace, not a decided node.

◆ **決策可記錄｜decision-trace** : reminder only, not saved or approved.

## Operational details

- The bundled task reader provides separately labelled active, uncertain and exceptions lists. State omitted counts and revision pins; never infer all done from an empty or partial page.
- Unmarked items without explicit status evidence stay visible as status uncertain, not confirmed active tasks, and are never automatically archived. A newer evidenced closure wins over an old Open item.
- Restore uses the delivered small operation guide, `--restore-contract`, `--validate-restore` and `--task-id`. Never print the entire index or search the implementation to discover schema. After separately approved immutable request/approval records, read back immediate visibility.
- Lens produces one coherent sourced result, not four mandatory reports. Atomic cards require provenance, existing-card checks, full draft approval and separately approved MOC updates.
- Compose preserves uncertainty, quotations, URLs and authored positions. Technical usefulness is not rejected for lacking literary tension. Independent review uses the actual authorized host pipeline, not simulated panels.
- Triage keeps zero-artifact and existing-spec exits, display-before-save and partial-save recovery. Review proposals never change rules through `save all`.
- The five-entry layout does not enable a scheduler, add hooks, deploy runtime copies or integrate akegarasu-no-yume automatically. Existing acceptance evidence retains its tested version and scope.

Executable contracts are in `commands/` and the Codex adapter's `references/`. Shared card/review capabilities live in package `references/capabilities/`; task capabilities preserve their host-specific reader roots. These summaries are not runtime configuration.

---

### Why commands, not agents

Hirameki is built as explicit commands rather than an autonomous background agent. Two reasons:

**Safety.** Every command that writes a file shows you the full content and target path before anything happens. Read-only commands (`pulse`, `tasks`, `next`) produce output you can act on or discard — they never touch your vault unless you explicitly ask. Write commands (`wrap`, `journal`, `decision-trace`, `handoff`) require confirmation at the point of writing. `tidy fix` separates what it can safely automate from what needs your judgment.

> **Limitation**: these safety behaviors are instructions written into each command prompt — not hard-coded enforcement. Claude follows them reliably in practice, but there is no programmatic gate that makes confirmation technically impossible to skip. This is a current constraint of how Claude Code commands work, not something Hirameki can resolve on its own.

**You stay in control.** The commands surface patterns, connections, and suggestions — but every decision is yours. `harvest` identifies candidates but waits for you to choose which ideas to graduate. `challenge` finds weaknesses in your arguments but doesn't rewrite them. `compose` drafts in your voice but marks what's grounded in vault evidence vs. inferred from style.

Your vault is a record of how *you* actually think. The goal is to amplify that — not to have a system quietly reshaping it.

---

### How it works

1. **Config**: `/hirameki:__init` writes a split configuration. Vault folder structure goes to `<vault>/AGENTS.md` under `## Vault Structure` (agent-neutral — it travels with the vault and any agent, Codex / Gemini / Claude, can read it). Per-machine values (vault path, language) go to `~/.claude/vault-local.md`. Every command resolves folder paths in this order: `<vault>/AGENTS.md` → `~/.claude/vault-local.md` → `~/.claude/CLAUDE.md`.
2. **Folder detection**: `__init` is audit-first — it looks for evidence of your existing organisation before proposing folders. When it finds no evidence, it falls back to common folder names. Missing folders are created on first use and saved to config.
3. **Content scanning**: All non-system folders in your vault root are treated as "content folders" — whatever structure you use, commands adapt.
4. **Write safety**: Every command that writes a file shows a full preview and path before writing. Nothing is written without confirmation.

---

### Folder name detection

When `__init` finds no evidence of an existing structure, it falls back to these common folder names, checked in order. First match wins. If none are found, it asks where to create the folder.

<details>
<summary>Fallback folder names</summary>

| Purpose | Fallback names (checked in this order) |
|---------|----------------------------------------|
| daily-notes | `wrap/` `_wrap/` `Wrap/` `daily/` `_daily/` `Daily/` `Journal/` `journal/` |
| inbox | `inbox/` `_inbox/` `Inbox/` `_Capture/` `Capture/` |
| journal | `journal/` `_journal/` `Journal/` `_logs/` `logs/` |
| research | `research/` `_research/` `Research/` `_analysis/` `analysis/` |
| handoff | `handoff/` `_handoff/` `Handoff/` |
| templates | `templates/` `_templates/` `Templates/` |

If your vault uses a different name, `__init` will ask and save your choice. The saved mapping is what all commands use — the detection list only runs once.

</details>

---

### Known Limitations

1. **Vault must be local.** Cloud-only vaults are not supported. iCloud or Google Drive sync can cause file conflicts when Claude Code reads/writes simultaneously with the sync client.
2. **Vault structure assumptions.** Commands expect specific folders (daily notes, journal, research, etc.). Running `/hirameki:__init` is required to map your vault structure before other commands work.
3. **No incremental indexing.** Commands like `/harvest` and `/pulse` scan the vault on each invocation. On large vaults (1000+ notes), this can be noticeably slow.
4. **Hooks run on every session.** Hook scripts (vault pulse, extract actions, etc.) execute on every Claude Code session start/stop. There is no per-project opt-out mechanism.
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

設定完成後，`__init` 會寫入**拆分設定**：vault 的資料夾結構寫進 `<vault>/AGENTS.md`（agent-neutral — 隨 vault 移動，任何 AI agent 都能讀），per-machine 值（vault 路徑、語言）寫進 `~/.claude/vault-local.md`。之後不管在哪裡開啟 Claude Code，所有 Hirameki 指令都能正常運作。若跨機器同步 `~/.claude/`，`vault-local.md` 應加入 gitignore，每台機器跑一次 `/hirameki:__init` 即可。

---

### Codex 相容層

Claude Code 是原生指令介面；Codex 以一個 umbrella skill 路由五個主要目的、永久捷徑與暫時轉向名稱，按需讀契約。兩側只讀自己的設定，沒有另一側設定的退路。

---

### Hirameki — 五個目的導向入口 — 完整指南

> 2.2.0 整合工作流程入口；來源驗證、模型驗收、安裝與排程分開判定。

每個指令先從自己的 `~/.claude/vault-local.md` 取得本機 vault 設定，再從 `<vault>/AGENTS.md` 的 `## Vault Structure` 讀取共用資料夾。只有需要讀寫 vault 時才解析；當前明示設定優先，不讀其他 agent 私有設定。缺少設定使用 `/hirameki:__init`，初始化寫入仍須核准。

## 五個主入口

| Entry | Purpose |
|---|---|
| `next` | 接續工作、查看有效待辦與卡點；支援 `next tasks [N]`、`next stuck [N]`、`next week [N]`。 |
| `lens` | 按問題探索歷史、立場、關聯、弱點、機會與模式；`lens cards` 找概念卡候選，`lens random` 只在明確要求時使用。 |
| `compose` | 按目的寫稿、改稿、大綱、語氣、構想評估或審查；已有稿件不必掃描整個 vault。 |
| `decision-trace` | 整理重要選擇與取捨，不替使用者拍板。 |
| `triage` | 只提出有新增價值的 wrap、journal、lesson 或 handoff；第一份草稿前不新增確認層。 |

## 專用工具與永久捷徑

| Entry | Purpose |
|---|---|
| `tidy` | 維護：`tidy tasks` 只提歸檔建議；`tidy review` 審查 corrections／lessons；`tidy snapshot` 唯讀盤點。Claude 無參數仍做 metadata 檢查，Codex 無參數仍提任務建議。 |
| `mekiki` | 外部研究入口，不隨其他流程自動執行。 |
| `init (`__init`)` | 設定本機與共用資料夾；不借用其他 agent 的設定。 |
| `wrap` | 直接記一筆進度，不必先跑完整 triage。 |
| `journal` | 寫入或追加工作、判斷與符合門檻的教訓；`journal review` 共用 `tidy review` 契約。 |
| `handoff` | 直接準備交接，不必先跑完整 triage。 |

## 舊名稱轉向

十個舊名稱只在首個整合發布版本保留轉向；永久可叫用名稱共十一個。直接捷徑不會到期移除；尚未驗證宿主能隱藏其 metadata。

| Old name | Destination |
|---|---|
| `arc` | lens history |
| `bridge` | lens bridge |
| `challenge` | lens challenge |
| `harvest` | lens opportunities |
| `graduate` | lens cards |
| `reflect` | compose voice |
| `frame` | compose frame |
| `critique` | compose review |
| `tasks` | next tasks; stuck → next stuck |
| `pulse` | next week; patterns → lens patterns; snapshot → tidy snapshot |

## 安全與證據

保存前完整展示內容與目標路徑。`save all` 只涵蓋已展示的草稿；後續寫入前須先展示其餘全部草稿，改稿後重新展示並取得核准。分析、轉向、規則提案或決策提醒都不代表寫入授權。部分成功如實保留，恢復只處理尚未完成且已核准的操作。

未決或形成中的 trace 若需跨 session 保存，仍須 `save this`；它是討論脈絡，不是已定案節點。

◆ **決策可記錄｜decision-trace** ：只是提醒，不代表已保存或取得授權。

## 操作細節

- 共用 reader 分列有效待辦、狀態未確認與例外，揭露未顯示筆數與分頁版本；空頁或不完整頁不能推成全部完成。
- 沒有明確狀態證據的未標記事項列在狀態未確認，不當成確定待辦、不自動歸檔；舊 Open item 不能推翻較新的明確結案。
- 取回使用套件內的小型操作文件、`--restore-contract`、`--validate-restore` 與 `--task-id`。不輸出整份索引或搜尋實作找 schema。每次核准的獨立申請與核准紀錄保存後，立即讀回可見性。
- lens 交付一份有來源的整合回答，不固定產生四份報告。概念卡須是單一主張，先查既有卡、展示全文並核准；MOC 修改另行核准。
- compose 保留不確定性、引文、URL 與作者立場；技術文件不因缺少文學張力被否決。獨立審查沿用實際授權管道，不模擬多人共識。
- triage 保留零產物、已有 spec、展示後保存與部分失敗恢復；`save all` 不授權修改規則。
- 入口整合不自動啟用排程、增加 hook、部署 runtime 或接入 akegarasu-no-yume。既有驗收只證明當時版本與受測範圍。

實際契約位於 `commands/` 與 Codex adapter 的 `references/`。共用概念卡／審查能力放在套件 `references/capabilities/`，待辦能力保留各宿主的 reader 路徑。摘要不是 runtime 設定。

---

### 為什麼是指令，而不是 Agent

Hirameki 設計為明確的指令，而不是自主在背景運作的 Agent。兩個原因：

**安全性。** 所有寫入檔案的指令在執行前都會顯示完整內容和目標路徑。唯讀指令（`pulse`、`tasks`、`next`）產出的結果你可以採用或忽略 — 沒有你的明確要求，它們不會動你的 vault。寫入指令（`wrap`、`journal`、`decision-trace`、`handoff`）在寫入時需要確認。`tidy fix` 把可以安全自動化的部分與需要你判斷的部分分開處理。

> **限制**：這些安全行為是寫入每個指令 prompt 中的規則 — 不是程式碼層面的強制機制。Claude 在實際執行時會遵守，但沒有任何程式閘道能從技術上確保確認步驟不可跳過。這是 Claude Code 指令系統目前的限制，不是 Hirameki 能自行解決的問題。

**主體可操控性。** 指令找出模式、連結和建議 — 但每個決定都是你的。`harvest` 找出候選想法，但等你決定哪些準備好畢業。`challenge` 找出論述的弱點，但不會幫你改寫。`compose` 用你的語氣起草，但會標注哪些有 vault 依據、哪些是風格推測。

你的 vault 記錄的是*你*真實的思考方式。目標是放大這個 — 而不是讓一個系統在背後悄悄改塑它。

---

### 運作方式

1. **設定**：`/hirameki:__init` 寫入拆分設定。vault 資料夾結構寫進 `<vault>/AGENTS.md` 的 `## Vault Structure`（agent-neutral — 隨 vault 移動，Codex / Gemini / Claude 任何 agent 都能讀）。per-machine 值（vault 路徑、語言）寫進 `~/.claude/vault-local.md`。每個指令依此順序解析資料夾路徑：`<vault>/AGENTS.md` → `~/.claude/vault-local.md` → `~/.claude/CLAUDE.md`。
2. **資料夾偵測**：`__init` 是 audit-first — 它先在 vault 中尋找你既有組織的證據，再提議資料夾。找不到證據時才退回常見資料夾名稱。找不到的資料夾在首次使用時建立並存入設定。
3. **內容掃描**：vault 根目錄下所有非系統資料夾視為「內容資料夾」— 無論你怎麼組織筆記，指令都能適應。
4. **寫入安全**：所有寫入檔案的指令在執行前都會顯示完整預覽和路徑。沒有確認不會寫入。

---

### 資料夾名稱偵測

當 `__init` 找不到既有結構的證據時，會退回依序尋找這些常見資料夾名稱。第一個找到的為準。找不到時會詢問建立位置。

<details>
<summary>退回使用的資料夾名稱</summary>

| 用途 | 依序偵測的名稱 |
|------|---------------|
| daily-notes | `wrap/` `_wrap/` `Wrap/` `daily/` `_daily/` `Daily/` `Journal/` `journal/` |
| inbox | `inbox/` `_inbox/` `Inbox/` `_Capture/` `Capture/` |
| journal | `journal/` `_journal/` `Journal/` `_logs/` `logs/` |
| research | `research/` `_research/` `Research/` `_analysis/` `analysis/` |
| handoff | `handoff/` `_handoff/` `Handoff/` |
| templates | `templates/` `_templates/` `Templates/` |

如果你的 vault 使用不同的名稱，`__init` 會詢問並儲存你的選擇。儲存後所有指令直接讀取設定，偵測清單只在首次執行時使用一次。

</details>

---

### 已知限制

1. **Vault 必須在本機。** 不支援純雲端 vault。iCloud 或 Google Drive 同步在 Claude Code 同時讀寫時可能造成檔案衝突。
2. **假設特定的 vault 結構。** 指令預期特定資料夾（daily notes、journal、research 等）。必須先執行 `/hirameki:__init` 完成資料夾對應，其他指令才能正常運作。
3. **無增量索引。** `/harvest` 和 `/pulse` 等指令每次都會完整掃描 vault。大型 vault（1000+ 篇筆記）會有明顯延遲。
4. **Hook 在每次 session 都會執行。** Hook 腳本（vault pulse、action 擷取等）在每次 Claude Code session 啟動/結束時都會執行，無法依專案個別關閉。
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

セットアップ後、`__init` は**分割設定**を書き込みます：vault のフォルダ構造は `<vault>/AGENTS.md`（エージェント中立 — vault と一緒に移動し、どの AI エージェントも読める）に、マシン固有の値（vault パス・言語）は `~/.claude/vault-local.md` に保存されます。以降は Claude Code をどこで開いても、すべての Hirameki コマンドが正常に動作します。`~/.claude/` をマシン間で同期する場合、`vault-local.md` は gitignore に追加してください。各マシンで `/hirameki:__init` を一度実行するだけで済みます。

---

### Hirameki — 目的別の五つの入口 — 詳細ガイド

> 2.2.0 ではワークフローの入口を統合しました。ソース検証、モデル評価、インストール、スケジュールは別々に扱います。

すべてのコマンドは、まず自分の `~/.claude/vault-local.md` を使い、共有フォルダーは `<vault>/AGENTS.md` の `## Vault Structure` から読みます。vault へのアクセスが必要な場合だけ設定を解決します。明示設定を優先し、他の agent の私有設定は読みません。不足時は `/hirameki:__init` を使い、初期設定の書き込みにも承認が必要です。

## 主な入口

| Entry | Purpose |
|---|---|
| `next` | 作業を再開し、有効なタスクや障害を確認します。`next tasks [N]`、`next stuck [N]`、`next week [N]` に対応します。 |
| `lens` | 問いに応じて履歴、立場、関係、弱点、機会、パターンを調べます。`lens cards` は概念カード候補、`lens random` は明示されたランダム探索です。 |
| `compose` | 目的に応じて執筆、編集、構成、文体、企画評価、レビューを行います。提供された原稿の編集に vault 全体の走査は不要です。 |
| `decision-trace` | 重要な選択とトレードオフを整理します。ユーザーの代わりに決定しません。 |
| `triage` | 新しい価値のある wrap、journal、lesson、handoff だけを提案します。最初の草稿の前に確認段階を増やしません。 |

## 専用ツールと恒久的なショートカット

| Entry | Purpose |
|---|---|
| `tidy` | 保守：`tidy tasks` はアーカイブ提案のみ、`tidy review` は corrections／lessons の検討、`tidy snapshot` は読み取り専用の棚卸しです。引数なしの Claude は metadata 検査、Codex はタスク提案を維持します。 |
| `mekiki` | 外部資料の研究入口です。他の処理から自動実行しません。 |
| `init (`__init`)` | この機械と共有フォルダーを設定します。他の agent の設定は借用しません。 |
| `wrap` | 進捗を一件記録します。全体の triage は不要です。 |
| `journal` | 作業・判断・条件を満たす lesson を記録または追記します。`journal review` は `tidy review` と同じ契約を使います。 |
| `handoff` | 直接引き継ぎを準備します。全体の triage は不要です。 |

## 旧名からの移行

十の旧名は最初の統合リリースでのみ転送として残します。恒久的に呼び出せる名前は十一です。直接記録のショートカットは失効しません。宿主での metadata 非表示は未検証です。

| Old name | Destination |
|---|---|
| `arc` | lens history |
| `bridge` | lens bridge |
| `challenge` | lens challenge |
| `harvest` | lens opportunities |
| `graduate` | lens cards |
| `reflect` | compose voice |
| `frame` | compose frame |
| `critique` | compose review |
| `tasks` | next tasks; stuck → next stuck |
| `pulse` | next week; patterns → lens patterns; snapshot → tidy snapshot |

## 安全と証拠

保存前に全文と保存先を表示します。`save all` は表示済みの草稿だけを対象とし、残りの書き込み前に残りの草稿をすべて表示します。変更した草稿は再表示して承認を得ます。分析、転送、規則の提案、決定のリマインダーは書き込み権限ではありません。一部成功を保持し、復旧では未完了の承認済み操作だけを扱います。

未解決または形成中の trace を session 間で保存する場合も `save this` が必要です。議論の経緯であり、確定した決定ノードではありません。

◆ **決策可記錄｜decision-trace** ：リマインダーであり、保存や承認ではありません。

## 操作の詳細

- 共通 reader は有効タスク、状態未確認、例外を分け、未表示件数とページの版を示します。空のページや部分表示を全件完了と解釈しません。
- 明確な状態証拠がない未マーク項目は状態未確認に残し、有効タスクとも自動アーカイブ対象とも扱いません。古い Open item は新しい明示的な完了を覆しません。
- 復元には同梱の小さな操作文書、`--restore-contract`、`--validate-restore`、`--task-id` を使います。索引全体を出力したり、schema を探して実装全体を検索したりしません。承認済みの独立した記録を保存後、可視性を直ちに読み返します。
- lens は出典付きの一つの回答を返し、四つのレポートを強制しません。概念カードは一つの主張とし、既存カードを確認し、全文への承認を得ます。MOC の変更は別途承認します。
- compose は不確実性、引用、URL、著者の立場を守ります。技術文書を文学的な緊張の欠如だけで否定しません。独立レビューには実際に許可された経路を使い、架空の合意を作りません。
- triage は成果物ゼロ、既存 spec、表示後の保存、一部失敗からの復旧を維持します。`save all` は規則変更を許可しません。
- 入口の統合はスケジュール、追加 hook、runtime 配備、akegarasu-no-yume 接続を自動的に有効化しません。既存の評価は、その版と対象範囲に限られます。

実行契約は `commands/` と Codex adapter の `references/` にあります。共通のカード／レビュー契約はパッケージの `references/capabilities/` に置き、タスク能力は各宿主の reader の場所を維持します。この要約は runtime 設定ではありません。

---

### なぜエージェントではなくコマンドなのか

Hirameki は、バックグラウンドで自律的に動くエージェントではなく、明示的なコマンドとして設計されています。理由は 2 つです。

**安全性。** ファイルを書き込むすべてのコマンドは、実行前に完全な内容と書き込み先パスを表示します。読み取り専用のコマンド（`pulse`・`tasks`・`next`）は採用しても無視してもいい出力を生成するだけで、明示的な要求なしには vault に触れません。書き込みコマンド（`wrap`・`journal`・`decision-trace`・`handoff`）は書き込み時に確認を求めます。`tidy fix` は安全に自動化できる部分と、あなたの判断が必要な部分を分けて処理します。

> **制限**：これらの安全動作は各コマンドのプロンプトに書かれた指示であり、コードレベルの強制機構ではありません。Claude は実際の動作でこれを守りますが、確認ステップを技術的にスキップ不可能にするプログラムのゲートは存在しません。これは Claude Code のコマンドシステム現在の制約であり、Hirameki 単独では解決できない問題です。

**主体としての操作性。** コマンドはパターン・つながり・提案を表面化しますが、すべての判断はあなたのものです。`harvest` は候補を特定しますが、どのアイデアを卒業させるかはあなたが決めます。`challenge` は論述の弱点を見つけますが、書き直しはしません。`compose` はあなたの語り口で下書きしますが、vault の根拠がある部分と推測の延長を明記します。

あなたの vault は、*あなた*が実際にどう考えるかの記録です。それを増幅するのが目的 — システムが静かに形を変えていくのではなく。

---

### 動作の仕組み

1. **設定**：`/hirameki:__init` が分割設定を書き込む。vault のフォルダ構造は `<vault>/AGENTS.md` の `## Vault Structure` に（エージェント中立 — vault と一緒に移動し、Codex / Gemini / Claude のどのエージェントも読める）。マシン固有の値（vault パス・言語）は `~/.claude/vault-local.md` に。各コマンドはこの順番でフォルダパスを解決：`<vault>/AGENTS.md` → `~/.claude/vault-local.md` → `~/.claude/CLAUDE.md`。
2. **フォルダ検出**：`__init` は audit-first — フォルダを提案する前に、vault 内の既存の組織の証拠を探します。証拠が見つからない場合のみ、一般的なフォルダ名にフォールバック。見つからないフォルダは初回使用時に作成して設定に保存。
3. **コンテンツスキャン**：vault ルート直下のすべての非システムフォルダを「コンテンツフォルダ」として扱う — どのような構成でも適応。
4. **書き込み安全性**：ファイルを書き込むすべてのコマンドは実行前に完全なプレビューとパスを表示。確認なしには書き込まない。

---

### フォルダ名の検出

`__init` が既存構造の証拠を見つけられない場合、これらの一般的なフォルダ名を順番に探します。最初に見つかったものを使用。見つからない場合は作成場所を確認します。

<details>
<summary>フォールバックのフォルダ名</summary>

| 用途 | 検出順 |
|------|--------|
| daily-notes | `wrap/` `_wrap/` `Wrap/` `daily/` `_daily/` `Daily/` `Journal/` `journal/` |
| inbox | `inbox/` `_inbox/` `Inbox/` `_Capture/` `Capture/` |
| journal | `journal/` `_journal/` `Journal/` `_logs/` `logs/` |
| research | `research/` `_research/` `Research/` `_analysis/` `analysis/` |
| handoff | `handoff/` `_handoff/` `Handoff/` |
| templates | `templates/` `_templates/` `Templates/` |

vault が別の名前を使っている場合、`__init` が確認して選択を保存します。保存後はすべてのコマンドが設定を直接読み込みます。検出リストは初回のみ使用されます。

</details>

---

### 既知の制限事項

1. **Vault はローカルである必要があります。** クラウドのみの vault はサポートされていません。iCloud や Google Drive の同期は、Claude Code が同時に読み書きする際にファイルの競合を引き起こす可能性があります。
2. **特定の vault 構造を前提としています。** コマンドは特定のフォルダ（daily notes、journal、research など）を想定しています。他のコマンドが動作する前に `/hirameki:__init` を実行してフォルダのマッピングを完了する必要があります。
3. **増分インデックスなし。** `/harvest` や `/pulse` などのコマンドは、実行のたびに vault 全体をスキャンします。大規模な vault（1000 件以上のノート）では顕著な遅延が発生する可能性があります。
4. **フックは毎セッションで実行されます。** フックスクリプト（vault pulse・アクション抽出など）は Claude Code のセッション開始/終了のたびに実行されます。プロジェクトごとにオプトアウトする仕組みはありません。
5. **オフライン LLM 非対応。** すべての分析は Claude API を経由します。有効な Claude サブスクリプションが必要です。
6. **言語検出は手動設定。** vault の言語は `__init` 実行時に一度だけ設定されます。vault の内容からの自動検出はありません。
7. **同時書き込み保護なし。** 複数の Claude Code セッションが同じ daily note に同時に書き込んだ場合、競合解決の仕組みはありません — 最後の書き込みが上書きします。

---

### ライセンス

MIT

</details>
