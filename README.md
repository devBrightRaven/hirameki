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

Either way, the vault path is saved locally to `~/.claude/vault-local.md`. After setup, every Hirameki command works no matter where you open Claude Code. If you sync `~/.claude/` across machines, `vault-local.md` should be gitignored — each machine runs `/hirameki:__init` once.

---

### Commands

20 commands, grouped by how you use them.

---

#### Orchestrators

Guided flows that bundle related primitives into a single interactive sequence. Each step shows a full draft — save, skip, or edit before moving on. The underlying primitives all work standalone.

**`/hirameki:triage`**

*Use when: you're wrapping up a session and want to capture everything in one go.*

End-of-session bundle. Walks through wrap → journal → handoff in sequence. Each step shows a full draft with save / skip / edit before the next begins. Shares a single session-state scan across all three sub-flows. Run once at session end. No arguments.

---

**`/hirameki:lens <concept>`**

*Use when: you want to deeply understand how a concept lives in your vault — its history, your positions on it, how it connects to something else, and where the arguments might be weak.*

Topic understanding flow. Four steps in sequence: arc → position extraction → bridge → challenge. Bridge auto-suggests a related topic from the arc step; you can accept or change it. Each step can be saved or skipped individually. Saves to `{research}/lens/`.

---

**`/hirameki:compose <topic>`**

*Use when: you want to write something grounded in your vault, and want to validate the idea before fully committing.*

Topic creation flow. Two steps: voice (writes a response in your style, drawing on your vault positions) → frame (runs the five-question validation test). Standalone — does not require running `/hirameki:lens` first. Each step can be saved or skipped. Saves to `{research}/compose/`.

---

**`/hirameki:mekiki <input>`**

*Use when: you want to capture an external resource — a GitHub repo, a web article, or a piece of text — and integrate it into your vault.*

External resource capture. Auto-detects input type:

| Input | Route | Output |
|-------|-------|--------|
| GitHub URL or `owner/repo` | Repo analysis: technique extraction + adopt/defer/reject | `{research}/mekiki-{repo}.md` |
| Article URL | Article capture + vault cross-reference + integration verdict | `{inbox}/YYYY-MM-DD-{slug}.md` |
| Pasted text or local file path | Article capture + vault cross-reference + integration verdict | `{inbox}/YYYY-MM-DD-{slug}.md` |

---

#### Session

**`/hirameki:next`**

*Use when: you're resuming mid-session and need a quick orientation.*

Orient after resuming a session. Summarises what was done, what's open, and what to do next. Scans the current session's task list, file activity, and recent decisions.

---

**`/hirameki:wrap [description]`**

*Use when: you're done for the day (or pausing a session) and want a record of what happened.*

Progress snapshot. Scans session file activity, appends a timestamped block to today's daily note with: completed, in-progress, and next steps. Can run multiple times a day — each run appends a new block. Optional: describe the session focus to shape the summary.

---

**`/hirameki:journal <topic>`**

*Use when: you made a non-obvious decision and want to record why — so future-you (or a collaborator) can understand the reasoning.*

Work log with reasoning. Writes a structured entry covering: background, what you did, why you did it, inspiration connections, possible improvements, and open follow-ups. Same topic, same day: appends an update section and marks completed follow-ups. Searches related vault notes to surface context and [[wiki links]].

Different from `wrap`: wrap records what happened in a session. Journal records why you made a specific decision.

---

**`/hirameki:handoff`**

*Use when: work isn't finished and the next session needs explicit guidance to pick up.*

Snapshots session state into a new handoff document at `{handoff}/YYYY-MM-DD-{slug}.md`. Automatically collects incomplete tasks, files edited, decisions made, and deferred items — then shows a full draft for confirmation before writing. Topic auto-inferred from session activity. Distinct from wrap: wrap records what happened, handoff captures what's left and how to resume.

---

#### Understanding — standalone

These are the primitives that `/hirameki:lens` orchestrates. Call them directly for quick, targeted investigation.

**`/hirameki:arc <concept>`**

*Use when: you keep returning to the same concept and want to see how your thinking has changed.*

Concept evolution tracker. Shows first appearance, evolution timeline, current state, and unexplored angles across your vault. Same concept, same day: appends. Saves to `{research}/arc/YYYY-MM-DD-{concept}.md`.

---

**`/hirameki:bridge <A> and <B>`**

*Use when: two interests feel separate but might be related, and you want to find the connection.*

Hidden connections between two topics. Finds direct intersections, bridge notes, and proposes deep connection hypotheses. Same pair, same day: appends. Saves to `{research}/bridge/YYYY-MM-DD-{A}-{B}.md`.

---

**`/hirameki:challenge <topic>`**

*Use when: before publishing something — find the holes before your readers do.*

Argument weakness analysis. Checks each claim in the vault about a topic for: internal contradictions, unverified assumptions, logic gaps, and evidence gaps. Saves to `{research}/challenge/YYYY-MM-DD-{topic}.md`.

---

**`/hirameki:reflect <question>`**

*Use when: you need a position statement or first draft in your actual voice.*

Answer in your vault's voice. Analyzes your writing style, extracts your existing positions, and writes a response in your voice with source citations and confidence notes. Add `save` to write to `{research}/reflect/YYYY-MM-DD-{question}.md`.

---

#### Creation — standalone

These are the primitives that `/hirameki:compose` orchestrates.

**`/hirameki:frame <idea>`**

*Use when: you have a creative idea (article, product, design) and want to validate it before investing effort.*

Pre-creation checkpoint. Runs five questions against your vault: Only-I test (what makes this uniquely yours?), collision scan (have you already published this?), stakes (what changes for the reader/user?), tension (what's the surprising or uncomfortable part?), and evidence (what grounds this in lived experience?). Produces one of four verdicts: **PROCEED** / **RETHINK** / **KILL** / **CONSOLIDATE**. Does not generate content — only evaluates whether content should exist. Add `save` to write result to file.

---

**`/hirameki:critique <file>`**

*Use when: you want independent feedback on a piece of writing.*

Multi-model writing critique. Dispatches three reviewers in parallel — Claude Opus, Codex (via `codex exec`), and Gemini (via `gemini -p`) — each scoring three dimensions: sensory density, structural tension, and resonance (1–10). Synthesises results into a comparison table highlighting where reviewers agree and where they diverge by 3+ points. Strongest line, weakest line, and recommended edits from all three. Saves output to `{vault}/_writing_lab/benchmark/`.

---

#### Vault

**`/hirameki:pulse [week|patterns]`**

*Use when: you want to know what's going on across your vault without diving in manually.*

Three modes depending on what you need:

- **`/hirameki:pulse`** — Immediate snapshot. Scans all content folders (depth 2) and the last 7 days of daily notes. Shows content topics per folder, recent file changes, and vault-wide counts. Good to run at session start.

- **`/hirameki:pulse week`** — Weekly gap analysis. Compares what you said was a priority (from daily notes) against what you actually worked on (from file changes). Surfaces drift between intentions and effort. Requires at least 3 days of daily notes.

- **`/hirameki:pulse patterns`** — Undercurrents and clusters. Surfaces recurring themes without dedicated articles (appears in 3+ files, no standalone write-up), and groups of notes converging on unnamed themes. Good for finding what's been quietly accumulating.

---

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

**`/hirameki:graduate <note>`**

*Use when: a note has matured into a stable concept and you want to formalize it.*

Promotes a note to a stable concept card. Validates and completes frontmatter, sets a formal status, and links related cards with wiki links.

---

**`/hirameki:tasks [days|stuck]`**

*Use when: you want a single prioritised list of everything you said you'd do next.*

Aggregates next actions from daily notes and journal entries. Default: scans the last 3 days, deduplicates and ranks by recurrence. Items appearing 3+ times are flagged as potential procrastination. Use `tasks stuck` to find recurring unfinished tasks that have never appeared in a "Done" section.

---

#### Maintenance

**`/hirameki:tidy [tags|fix|full|lint]`**

*Use when: you notice your frontmatter has drifted, tags have multiplied inconsistently, or you want a health check.*

Frontmatter and content health check. Five modes:

- **`tidy`** — Missing fields + consistency check (lightweight default).
- **`tidy tags`** — Tag convergence analysis: dominant tags, orphan tags, merge candidates.
- **`tidy fix`** — Missing fields + consistency + auto-correct (with confirmation prompts for judgment calls).
- **`tidy full`** — All checks combined.
- **`tidy lint`** — Content health: contradiction detection, stale claims, orphan notes, dead wiki links. Surfaces follow-up suggestions for lens, pulse, and graduate when issues are found.

Saves output to `{research}/tidy/`.

---

**`/hirameki:__init`**

*Use when: first time setup on a new machine, or reconfiguring an existing setup.*

First-time setup: vault detection, language setting, folder resolution, writes to `~/.claude/vault-local.md`. Run once per machine. If config already exists, runs as Mode B (reconfigure individual settings).

---

### Why commands, not agents

Hirameki is built as explicit commands rather than an autonomous background agent. Two reasons:

**Safety.** Every command that writes a file shows you the full content and target path before anything happens. Read-only commands (`pulse`, `tasks`, `next`) produce output you can act on or discard — they never touch your vault unless you explicitly ask. Write commands (`wrap`, `journal`, `handoff`) require confirmation at the point of writing. `tidy fix` separates what it can safely automate from what needs your judgment.

> **Limitation**: these safety behaviors are instructions written into each command prompt — not hard-coded enforcement. Claude follows them reliably in practice, but there is no programmatic gate that makes confirmation technically impossible to skip. This is a current constraint of how Claude Code commands work, not something Hirameki can resolve on its own.

**You stay in control.** The commands surface patterns, connections, and suggestions — but every decision is yours. `harvest` identifies candidates but waits for you to choose which ideas to graduate. `challenge` finds weaknesses in your arguments but doesn't rewrite them. `compose` drafts in your voice but marks what's grounded in vault evidence vs. inferred from style.

Your vault is a record of how *you* actually think. The goal is to amplify that — not to have a system quietly reshaping it.

---

### How it works

1. **Config**: Settings live in `~/.claude/vault-local.md` under `## Vault Structure` — vault path, language, and folder mappings. Written once by `/hirameki:__init`, read by all other commands. Falls back to `~/.claude/CLAUDE.md` for backwards compatibility.
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
| research | `_hirameki_research/` `_agent_research/` `_claude_code_research/` `Research/` `_research/` `research/` |
| handoff | `_yorozuya/handoff/` `Handoff/` `_handoff/` `handoff/` |
| templates | `Templates/` `_templates/` `templates/` |

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

設定完成後，vault 路徑存入 `~/.claude/vault-local.md`。之後不管在哪裡開啟 Claude Code，所有 Hirameki 指令都能正常運作。若跨機器同步 `~/.claude/`，`vault-local.md` 應加入 gitignore -- 每台機器跑一次 `/hirameki:__init` 即可。

---

### 指令說明

20 個指令，依照使用方式分組。

---

#### Orchestrators（編排指令）

每個編排指令把相關的基礎指令整合成一個引導式互動流程。每一步都會顯示完整草稿，讓你選擇 save / skip / edit 後才繼續。各基礎指令仍可單獨呼叫。

**`/hirameki:triage`**

*適合：session 即將結束，想一次完成所有記錄工作時。*

Session 結束整合。依序執行 wrap → journal → handoff 三步。每步顯示完整草稿，選擇 save / skip / edit 後才進入下一步。三個子流程共用同一次 session 狀態掃描。Session 結尾時執行，不需要任何參數。

---

**`/hirameki:lens <概念>`**

*適合：想深入了解某個概念在 vault 中的樣貌 — 它的演化歷史、你對它的立場、與其他主題的連結，以及論述的薄弱之處。*

主題理解流程。四步依序執行：arc → 立場萃取 → bridge → challenge。Bridge 步驟會從 arc 結果自動推薦一個相關主題，你可以接受或更換。每步可單獨 save 或 skip。寫入：`{research}/lens/`。

---

**`/hirameki:compose <主題>`**

*適合：想圍繞某個主題寫點東西，希望植根於 vault，並在全力投入前先驗證想法時。*

主題創作流程。兩步：voice（用你的文風、依據 vault 的立場作答）→ frame（執行五問驗證）。Standalone — 不需要先跑 `/hirameki:lens`。每步可單獨 save 或 skip。寫入：`{research}/compose/`。

---

**`/hirameki:mekiki <輸入>`**

*適合：想捕獲一個外部資源並整合進 vault 時。*

外部資源捕獲。自動偵測輸入類型：

| 輸入 | 路由 | 輸出位置 |
|------|------|----------|
| GitHub URL 或 `owner/repo` | Repo 分析：技術提取 + adopt/defer/reject 裁決 | `{research}/mekiki-{repo}.md` |
| 文章 URL | 文章捕獲 + vault 交叉引用 + 整合裁決 | `{inbox}/YYYY-MM-DD-{slug}.md` |
| 貼上文字或本機檔案路徑 | 文章捕獲 + vault 交叉引用 + 整合裁決 | `{inbox}/YYYY-MM-DD-{slug}.md` |

---

#### Session

**`/hirameki:next`**

*適合：在 session 中途回來，需要快速定向時。*

恢復 session 後定向。整理已完成的工作、待處理的事項、下一步。掃描本次 session 的任務清單、檔案活動和近期決定。

---

**`/hirameki:wrap [描述]`**

*適合：一天結束（或暫停 session）時，記錄發生了什麼。*

進度快照。掃描本次 session 的檔案操作，在今天的 daily note 末尾追加一個帶時間戳的區塊，包含：已完成、進行中、下一步。可一天執行多次，每次追加新區塊。可加入描述來聚焦摘要方向。

---

**`/hirameki:journal <描述>`**

*適合：做了一個不直觀的決定，想記錄下為什麼時。*

工作紀錄與思考記錄。寫入結構化記錄，包含：背景、做了什麼、為什麼這樣做、靈感連結、可能的改進方向、未完成事項。同主題同天：追加更新並標記已完成的後續。搜尋 vault 中相關筆記作為脈絡和 [[wiki link]]。

與 `wrap` 的差別：wrap 記錄一個 session 發生了什麼。journal 記錄你為什麼做某個特定決定。

---

**`/hirameki:handoff`**

*適合：工作尚未完成，下一個 session 需要明確指引才能銜接時。*

將 session 狀態快照寫入 `{handoff}/YYYY-MM-DD-{slug}.md`。自動收集未完成的任務、已編輯的檔案、已做的決定和擱置的事項，顯示完整草稿確認後才寫入。主題從 session 活動自動推斷。與 wrap 的差別：wrap 記錄發生了什麼，handoff 記錄還剩什麼以及如何銜接。

---

#### 理解（Standalone）

這些是 `/hirameki:lens` 整合的基礎指令，可以直接單獨呼叫做快速的針對性調查。

**`/hirameki:arc <概念>`**

*適合：你不斷回到同一個概念，想看看自己的思考如何演變時。*

概念演化追蹤。顯示某概念在 vault 中的首次出現、演化時間軸、目前狀態與空白地帶。同概念同天：追加。寫入：`{research}/arc/YYYY-MM-DD-{概念}.md`。

---

**`/hirameki:bridge <A> and <B>`**

*適合：兩個感覺分開但可能相關的興趣，想找出連結時。*

兩主題間的隱藏連結。找出直接交集、橋樑筆記，並提出深層連結假設。同組主題同天：追加。寫入：`{research}/bridge/YYYY-MM-DD-{A}-{B}.md`。

---

**`/hirameki:challenge <主題>`**

*適合：發表前 — 在讀者找到漏洞之前先找到它時。*

論點弱點分析。對 vault 中關於此主題的每個主張，逐一檢查內部矛盾、未驗證假設、邏輯跳躍與證據缺口。寫入：`{research}/challenge/YYYY-MM-DD-{主題}.md`。

---

**`/hirameki:reflect <問題>`**

*適合：需要一個初稿或立場陳述，用自己真實的語氣時。*

Vault 語氣作答。分析你的寫作風格、萃取你的立場，用你的語氣寫出一段回答，附上出處引用與信心標注。加 `save` 才寫入：`{research}/reflect/YYYY-MM-DD-{問題}.md`。

---

#### 創作（Standalone）

這些是 `/hirameki:compose` 整合的基礎指令。

**`/hirameki:frame <想法>`**

*適合：有一個創作想法（文章、產品、設計），想在投入心力之前先驗證時。*

創作前檢查站。針對 vault 執行五個問題：Only-I 測試、碰撞掃描、賭注、張力、證據。產出四種裁決之一：**PROCEED** / **RETHINK** / **KILL** / **CONSOLIDATE**。不產生內容 — 只評估內容是否應該存在。加 `save` 可寫入檔案。

---

**`/hirameki:critique <檔案>`**

*適合：想對一篇文章獲得獨立回饋時。*

多模型寫作評審。同時啟動三位評審：Claude Opus、Codex（透過 `codex exec`）、Gemini（透過 `gemini -p`），各自對三個維度評分：感官密度、結構張力、觸動力（1–10）。整合結果為比較表，重點標出評審之間分差 3 分以上的地方。三方各自的最強句、最弱句和修改建議。輸出儲存至 `{vault}/_writing_lab/benchmark/`。

---

#### Vault

**`/hirameki:pulse [week|patterns]`**

*適合：想不深入文件就能掌握 vault 整體狀況時。*

三種模式：

- **`/hirameki:pulse`** — 即時概覽。掃描所有內容資料夾（深度 2 層）和最近 7 天 daily notes。顯示各資料夾的主題、最近的檔案變更、vault 整體統計。適合每次 session 開始時執行。

- **`/hirameki:pulse week`** — 週回顧與落差分析。比對 daily notes 中聲稱的優先事項與實際的檔案變更，找出意圖與行動之間的落差。需要至少 3 天的 daily notes。

- **`/hirameki:pulse patterns`** — 潛流與聚攏分析。找出繁複出現但沒有獨立文章的主題（出現在 3 個以上不同檔案），以及正在聚攏成形但尚未命名的筆記群。適合找出悄悄在積累的東西。

---

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

**`/hirameki:graduate <筆記>`**

*適合：一篇筆記已成熟為穩定概念，想將它正式化時。*

將筆記升格為穩定概念卡片。驗證並補全 frontmatter、設定正式 status、用 wiki link 連結相關卡片。

---

**`/hirameki:tasks [天數|stuck]`**

*適合：想把所有「下一步」整合成一份清單時。*

從 daily notes 和 journal 彙整下一步行動。預設掃描最近 3 天，去重後依出現頻率排序。出現 3 次以上的項目會標記為可能的拖延信號。使用 `tasks stuck` 可找出反覆出現、從未進入「完成」的卡住任務。

---

#### 維護

**`/hirameki:tidy [tags|fix|full|lint]`**

*適合：發現 frontmatter 開始亂掉、tag 越來越不一致，或在一次大整理前先做健檢時。*

Frontmatter 與內容健檢。五種模式：

- **`tidy`** — 缺漏欄位 + 一致性檢查（輕量預設）。
- **`tidy tags`** — Tag 收斂分析：核心標籤、孤立標籤、合併建議。
- **`tidy fix`** — 缺漏 + 一致性 + 自動修正（需判斷的逐一確認）。
- **`tidy full`** — 全部檢查。
- **`tidy lint`** — 內容健檢：矛盾偵測、過時主張、孤立筆記、死連結。找到問題時提示 lens、pulse、graduate 的後續建議。

寫入：`{research}/tidy/`。

---

**`/hirameki:__init`**

*適合：新機器的首次設定，或重新設定現有配置時。*

首次設定：偵測 vault、設定語言、解析資料夾、寫入 `~/.claude/vault-local.md`。每台機器執行一次。已有設定時執行進入 Mode B（重新設定個別項目）。

---

### 為什麼是指令，而不是 Agent

Hirameki 設計為明確的指令，而不是自主在背景運作的 Agent。兩個原因：

**安全性。** 所有寫入檔案的指令在執行前都會顯示完整內容和目標路徑。唯讀指令（`pulse`、`tasks`、`next`）產出的結果你可以採用或忽略 — 沒有你的明確要求，它們不會動你的 vault。寫入指令（`wrap`、`journal`、`handoff`）在寫入時需要確認。`tidy fix` 把可以安全自動化的部分與需要你判斷的部分分開處理。

> **限制**：這些安全行為是寫入每個指令 prompt 中的規則 — 不是程式碼層面的強制機制。Claude 在實際執行時會遵守，但沒有任何程式閘道能從技術上確保確認步驟不可跳過。這是 Claude Code 指令系統目前的限制，不是 Hirameki 能自行解決的問題。

**主體可操控性。** 指令找出模式、連結和建議 — 但每個決定都是你的。`harvest` 找出候選想法，但等你決定哪些準備好畢業。`challenge` 找出論述的弱點，但不會幫你改寫。`compose` 用你的語氣起草，但會標注哪些有 vault 依據、哪些是風格推測。

你的 vault 記錄的是*你*真實的思考方式。目標是放大這個 — 而不是讓一個系統在背後悄悄改塑它。

---

### 運作方式

1. **設定**：設定存在 `~/.claude/vault-local.md` 的 `## Vault Structure` 段落 — vault 路徑、語言、資料夾對應。由 `/hirameki:__init` 一次寫入，其他所有指令直接讀取。向後相容：若 `vault-local.md` 不存在，會退回讀取 `~/.claude/CLAUDE.md`。
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
| research | `_hirameki_research/` `_agent_research/` `_claude_code_research/` `Research/` `_research/` `research/` |
| handoff | `_yorozuya/handoff/` `Handoff/` `_handoff/` `handoff/` |
| templates | `Templates/` `_templates/` `templates/` |

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

セットアップ後、vault パスは `~/.claude/vault-local.md` にローカル保存されます。以降は Claude Code をどこで開いても、すべての Hirameki コマンドが正常に動作します。`~/.claude/` をマシン間で同期する場合、`vault-local.md` は gitignore に追加してください。各マシンで `/hirameki:__init` を一度実行するだけで済みます。

---

### コマンド説明

20 のコマンド、使い方でグループ化。

---

#### Orchestrators（オーケストレーター）

関連するプリミティブを一つのインタラクティブなシーケンスにまとめたガイド付きフロー。各ステップで完全なドラフトを表示 — save / skip / edit を選択してから次へ進む。各プリミティブはスタンドアロンでも使用可能。

**`/hirameki:triage`**

*使うとき：セッションを終了する段階で、すべての記録を一気にまとめたいとき。*

セッション終了バンドル。wrap → journal → handoff を順番に実行。各ステップで完全なドラフトを表示し、save / skip / edit を選択してから次へ進む。3 つのサブフローで一度のセッション状態スキャンを共有。セッション終了時に実行。引数なし。

---

**`/hirameki:lens <概念>`**

*使うとき：ある概念が vault にどのように存在するかを深く理解したいとき — その歴史、立場、他のテーマとの繋がり、論述の弱点まで。*

トピック理解フロー。四ステップ順番に実行：arc → 立場萃取 → bridge → challenge。Bridge ステップは arc の結果から関連トピックを自動提案。受け入れるか変更するかを選択。各ステップを個別に save または skip 可能。書き込み先：`{research}/lens/`。

---

**`/hirameki:compose <トピック>`**

*使うとき：vault に根ざした形で何かを書きたいとき、そして全力投入する前にアイデアを検証したいとき。*

トピック創作フロー。二ステップ：voice（あなたのスタイルで、vault の立場を踏まえて回答を作成）→ frame（五問テストを実行）。スタンドアロン — `/hirameki:lens` を先に実行する必要なし。各ステップを個別に save または skip 可能。書き込み先：`{research}/compose/`。

---

**`/hirameki:mekiki <入力>`**

*使うとき：外部リソースをキャプチャして vault に統合したいとき。*

外部リソースキャプチャ。入力タイプを自動検出：

| 入力 | ルーティング | 出力先 |
|------|-------------|--------|
| GitHub URL または `owner/repo` | リポジトリ分析：技術抽出 + adopt/defer/reject 判定 | `{research}/mekiki-{repo}.md` |
| 記事 URL | 記事キャプチャ + vault クロスリファレンス + 統合判定 | `{inbox}/YYYY-MM-DD-{slug}.md` |
| 貼り付けたテキストまたはローカルファイルパス | 記事キャプチャ + vault クロスリファレンス + 統合判定 | `{inbox}/YYYY-MM-DD-{slug}.md` |

---

#### セッション

**`/hirameki:next`**

*使うとき：セッションの途中で再開して、素早く状況を把握したいとき。*

セッション再開後の定位。完了した作業・未処理の事項・次のステップを整理。現在のセッションのタスクリスト・ファイル活動・最近の決定をスキャン。

---

**`/hirameki:wrap [説明]`**

*使うとき：1 日が終わった（またはセッションを一時停止する）時に、何が起きたかを記録するとき。*

進捗スナップショット。セッションのファイル操作をスキャンし、今日の daily note の末尾にタイムスタンプ付きのブロックを追記。内容：完了・進行中・次のステップ。1 日に複数回実行可能で、毎回新しいブロックを追記。オプションで説明を追加すると要約の方向性が定まる。

---

**`/hirameki:journal <説明>`**

*使うとき：直感的でない決断を下して、なぜそうしたかを記録したいとき。*

作業ログと思考記録。構造化された記録を書き込み：背景・何をしたか・なぜしたか・インスピレーションのつながり・改善の可能性・未完了事項。同テーマ・同日：追記更新し完了した後続事項をマーク。関連する vault ノートを検索して文脈と [[wiki link]] を提供。

`wrap` との違い：wrap はセッションで何が起きたかを記録。journal は特定の決断をなぜ下したかを記録。

---

**`/hirameki:handoff`**

*使うとき：作業が未完了で、次のセッションが引き継ぐために明確なガイダンスが必要なとき。*

セッション状態を `{handoff}/YYYY-MM-DD-{slug}.md` にスナップショットとして保存。未完了タスク・編集したファイル・決定事項・保留項目を自動収集し、完全なドラフトを表示して確認後に書き込む。トピックはセッション活動から自動推定。wrap との違い：wrap は「何が起きたか」を記録し、handoff は「何が残っているか・どう再開するか」を記録する。

---

#### 理解（スタンドアロン）

これらは `/hirameki:lens` がまとめるプリミティブです。素早いピンポイント調査には直接呼び出せます。

**`/hirameki:arc <概念>`**

*使うとき：同じ概念に繰り返し戻ってきて、思考がどう変わったか見たいとき。*

概念進化トラッカー。vault 全体でその概念の最初の登場・タイムライン・現在の状態・未探索の角度を表示。同概念・同日：追記。書き込み先：`{research}/arc/YYYY-MM-DD-{概念}.md`。

---

**`/hirameki:bridge <A> and <B>`**

*使うとき：別々に見える 2 つの興味が実はつながっているかもしれないと感じるとき。*

二つのトピック間の隠れたつながり。直接の交差点・橋渡しノート・より深いつながりの仮説を提案。同ペア・同日：追記。書き込み先：`{research}/bridge/YYYY-MM-DD-{A}-{B}.md`。

---

**`/hirameki:challenge <トピック>`**

*使うとき：公開前に — 読者に見つけられる前に穴を見つけるとき。*

論証の弱点分析。このトピックに関する vault の各主張について、内部矛盾・未検証の前提・論理の飛躍・証拠の欠缺を確認。書き込み先：`{research}/challenge/YYYY-MM-DD-{トピック}.md`。

---

**`/hirameki:reflect <質問>`**

*使うとき：自分の実際の声で立場表明や初稿が必要なとき。*

Vault 文体での回答。あなたの文章スタイルを分析し、ポジションを抽出し、あなたの文体で回答を記述。出典引用と確信度の注記付き。`save` を追加で書き込み：`{research}/reflect/YYYY-MM-DD-{質問}.md`。

---

#### 創作（スタンドアロン）

これらは `/hirameki:compose` がまとめるプリミティブです。

**`/hirameki:frame <アイデア>`**

*使うとき：クリエイティブなアイデア（記事・製品・デザイン）があり、労力を投じる前に検証したいとき。*

制作前チェックポイント。五問フレーム（Only-I テスト・衝突スキャン・賭け・緊張・証拠）。四つの判定：PROCEED / RETHINK / KILL / CONSOLIDATE。コンテンツを生成しない — 存在すべきかどうかのみを評価。`save` を追加でファイルに保存。

---

**`/hirameki:critique <ファイル>`**

*使うとき：文章に対する独立したフィードバックを得たいとき。*

マルチモデル文章クリティーク。三評者を並列起動：Claude Opus・Codex（`codex exec` 経由）・Gemini（`gemini -p` 経由）。各評者が三つの次元をスコアリング：感官密度・構造的緊張・共鳴（1–10）。比較表に統合し、不一致を強調表示。三者それぞれの最強の一文・最弱の一文・推奨編集。書き込み先：`{vault}/_writing_lab/benchmark/`。

---

#### Vault

**`/hirameki:pulse [week|patterns]`**

*使うとき：ファイルを深く掘り下げずに vault 全体の状況を把握したいとき。*

3 つのモード：

- **`/hirameki:pulse`** — 即時スナップショット。すべてのコンテンツフォルダ（深さ 2 層）と直近 7 日の daily notes をスキャン。各フォルダのコンテンツテーマ・最近のファイル変更・vault 全体の統計を表示。セッション開始時に実行するのに最適。

- **`/hirameki:pulse week`** — 週次レビューとギャップ分析。daily notes で宣言した優先事項と実際のファイル変更を比較し、意図と行動のずれを表面化。最低 3 日分の daily notes が必要。

- **`/hirameki:pulse patterns`** — 潜流とクラスター分析。独立した記事がないのに繰り返し登場するテーマ（3 つ以上の異なるファイルに出現）と、名前のついていないテーマに収束しつつあるノートのグループを表面化。静かに蓄積されてきたものを見つけるのに最適。

---

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

**`/hirameki:graduate <ノート>`**

*使うとき：ノートが安定した概念として成熟し、正式化したいとき。*

ノートを安定した概念カードに昇格。フロントマターを検証・補完し、正式ステータスを設定、wiki link で関連カードにリンク。

---

**`/hirameki:tasks [日数|stuck]`**

*使うとき：すべての「次のステップ」を 1 つのリストにまとめたいとき。*

daily notes と journal から次のアクションを集約。デフォルトは直近 3 日をスキャンし、重複を除去して出現頻度順に並べる。3 回以上登場するアイテムは先延ばしのシグナルとしてフラグ表示。`tasks stuck` を使うと、繰り返し登場するのに「完了」セクションに一度も現れたことのないスタック中タスクを発見できる。

---

#### メンテナンス

**`/hirameki:tidy [tags|fix|full|lint]`**

*使うとき：frontmatter が崩れてきた、タグの一貫性が失われてきた、または大きな整理の前に健全性チェックをしたいとき。*

フロントマターとコンテンツの健全性チェック。5 つのモード：

- **`tidy`** — 欠落フィールド + 一致性チェック（軽量デフォルト）。
- **`tidy tags`** — タグ収束分析：主要タグ・孤立タグ・統合候補。
- **`tidy fix`** — 欠落 + 一致性 + 自動修正（判断が必要なものは個別確認）。
- **`tidy full`** — 全チェック。
- **`tidy lint`** — コンテンツ健全性：矛盾検出・古い主張・孤立ノート・デッドリンク。問題が見つかった場合は lens・pulse・graduate の後続提案を表示。

書き込み先：`{research}/tidy/`。

---

**`/hirameki:__init`**

*使うとき：新しいマシンへの初回セットアップ、または既存の設定を変更したいとき。*

初回セットアップ：vault の検出・言語設定・フォルダー解決・`~/.claude/vault-local.md` への書き込み。マシンごとに一回実行。設定が存在する場合は Mode B（再設定）として動作。

---

### なぜエージェントではなくコマンドなのか

Hirameki は、バックグラウンドで自律的に動くエージェントではなく、明示的なコマンドとして設計されています。理由は 2 つです。

**安全性。** ファイルを書き込むすべてのコマンドは、実行前に完全な内容と書き込み先パスを表示します。読み取り専用のコマンド（`pulse`・`tasks`・`next`）は採用しても無視してもいい出力を生成するだけで、明示的な要求なしには vault に触れません。書き込みコマンド（`wrap`・`journal`・`handoff`）は書き込み時に確認を求めます。`tidy fix` は安全に自動化できる部分と、あなたの判断が必要な部分を分けて処理します。

> **制限**：これらの安全動作は各コマンドのプロンプトに書かれた指示であり、コードレベルの強制機構ではありません。Claude は実際の動作でこれを守りますが、確認ステップを技術的にスキップ不可能にするプログラムのゲートは存在しません。これは Claude Code のコマンドシステム現在の制約であり、Hirameki 単独では解決できない問題です。

**主体としての操作性。** コマンドはパターン・つながり・提案を表面化しますが、すべての判断はあなたのものです。`harvest` は候補を特定しますが、どのアイデアを卒業させるかはあなたが決めます。`challenge` は論述の弱点を見つけますが、書き直しはしません。`compose` はあなたの語り口で下書きしますが、vault の根拠がある部分と推測の延長を明記します。

あなたの vault は、*あなた*が実際にどう考えるかの記録です。それを増幅するのが目的 — システムが静かに形を変えていくのではなく。

---

### 動作の仕組み

1. **設定**：設定は `~/.claude/vault-local.md` の `## Vault Structure` セクションに保存 — vault パス・言語・フォルダマッピング。`/hirameki:__init` が一度だけ書き込み、他のすべてのコマンドが直接読み込む。後方互換性：`vault-local.md` がない場合は `~/.claude/CLAUDE.md` にフォールバック。
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
| research | `_hirameki_research/` `_agent_research/` `_claude_code_research/` `Research/` `_research/` `research/` |
| handoff | `_yorozuya/handoff/` `Handoff/` `_handoff/` `handoff/` |
| templates | `Templates/` `_templates/` `templates/` |

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
