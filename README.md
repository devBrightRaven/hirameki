# Hirameki 閃き

> Obsidian vault knowledge management commands for [Claude Code](https://claude.com/claude-code).

<div align="center">
  <a href="#english">English</a> &nbsp;|&nbsp; <a href="#繁體中文">繁體中文</a> &nbsp;|&nbsp; <a href="#日本語">日本語</a>
</div>

---

<details open>
<summary><h2 id="english">English</h2></summary>

### Inspiration

Hirameki is inspired by [internetvin](https://x.com/internetvin) — specifically the workflow shown in this video by [Greg Isenberg](https://x.com/gregisenberg), founder of [The Idea Browser](https://theideabrowser.com):

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

Then run `/hirameki:__init` to set up your vault. It will:
- Detect your Obsidian vault
- Ask for your preferred output language
- Map your folder structure
- Copy reference docs into your vault

If you open Claude Code inside your vault directory, the path is auto-detected.

---

### Commands

#### Daily Rhythm

**`/hirameki:status`**
Vault overview. Scans all content folders (depth 2) and the last 7 days of daily notes. Outputs: content topics per folder with activity status, recent file changes, and vault-wide counts. Good to run at the start of a session.

**`/hirameki:catchup [days]`**
Progress catchup. Reads the last Wrap block from recent daily notes and all inbox items, then suggests 1–3 things to focus on today. Default: yesterday. Example: `/hirameki:catchup 3` reviews the last 3 days.

**`/hirameki:wrap [description]`**
Progress snapshot. Scans session file activity, appends a timestamped block to today's daily note with: completed, in-progress, and next steps. Can run multiple times a day — each run appends a new block. Optional: describe the session focus to shape the summary.

**`/hirameki:weekreview`**
Weekly review with gap analysis. Compares what you said was a priority (from daily notes) against what you actually worked on (from file changes). Surfaces drift between stated intentions and real effort. Requires at least 3 days of daily notes.

---

#### Concept Archaeology

**`/hirameki:arc {concept}`**
Tracks how a concept evolves across your vault. Finds all mentions, orders them by date, and produces a timeline from first appearance to current state. Highlights blank spots — angles the concept hasn't been explored yet. Same concept, same day: appends an update rather than creating a new file.

**`/hirameki:bridge {A} and {B}`** *(use 「と」 in Japanese, 「與」 in Chinese)*
Finds hidden connections between two topics. Outputs: files that mention both directly, bridge notes that mention only one but could link them, and 1–3 deep connection hypotheses with confidence levels. Same pair, same day: appends.

**`/hirameki:undercurrent [scope]`**
Surfaces recurring themes that don't have a dedicated article. Scans all content folders and daily notes for words or ideas that appear in 3+ different files but haven't been written about on their own. Optional: focus on a specific directory.

**`/hirameki:cluster [scope]`**
Finds groups of notes converging on unnamed themes. Looks for 3+ notes covering similar concepts without a shared parent category, written on different dates (not a one-time burst). Rates each cluster by maturity and suggests a direction: article, project, framework, or keep accumulating.

---

#### Thinking Tools

**`/hirameki:ghost {question} [save]`**
Answers a question in your voice. Reads your completed writing to extract style patterns and existing stances, then composes a response using that voice. Marks which parts are grounded in vault evidence vs. stylistic extrapolation. Add `save` at the end to write to file.

**`/hirameki:stress-test {topic} [save]`**
Pressure-tests your arguments on a topic. Collects all claims you've made, then checks each for: internal contradictions, unverified assumptions, logical gaps, and evidence shortfalls. Outputs an overall robustness rating and top 1–3 weaknesses to address. Add `save` to write to file.

**`/hirameki:harvest [save]`**
Harvests actionable ideas from existing content. Scans content folders, 30 days of daily notes, and inbox. Outputs four categories (max 5 each): articles you could write, tools/projects you could build, topics worth researching, people/communities worth reaching out to. Add `save` to write to file.

**`/hirameki:graduate`**
Graduates half-formed ideas into standalone notes. Scans the last 14 days of daily notes and logs for items stuck in "in-progress" or "next steps", plus inbox and draft folders. Applies three criteria: clear core claim, connection to existing vault themes, sufficient content density. Two-phase: shows candidates first, executes only after confirmation.

---

#### Maintenance

**`/hirameki:tidy [fix]`**
Frontmatter properties audit. Scans all content folders, inbox, and 30 days of daily notes. Checks four categories: missing fields (no frontmatter, no tags, no status), consistency (invalid status/source values, tag casing, underscore vs hyphen), redundancy (single-use tags, 6+ tag files, topic/tag duplicates), and tag convergence (frequency stats, merge candidates, orphan tags). Outputs a health score. Add `fix` to auto-correct what's safe to automate, with confirmation prompts for judgment calls.

---

#### Logging

**`/hirameki:journal {topic}`**
Work log with reasoning. Writes a structured entry covering: background, what you did, why you did it, inspiration connections, possible improvements, and open follow-ups. Same topic, same day: appends an update section and marks completed follow-ups. Searches related vault notes to surface context and [[wiki links]].

---

### Why commands, not agents

Hirameki is built as explicit commands rather than an autonomous background agent. Two reasons:

**Safety.** Every command that writes a file shows you the full content and target path before anything happens. Read-only commands (`status`, `arc`, `stress-test`) produce output you can act on or discard — they never touch your vault unless you explicitly ask. Write commands (`wrap`, `journal`, `graduate`) require confirmation at the point of writing. `tidy fix` separates what it can safely automate from what needs your judgment.

**You stay in control.** The commands surface patterns, connections, and suggestions — but every decision is yours. `graduate` identifies candidates but waits for you to choose which ideas are ready. `stress-test` finds weaknesses in your arguments but doesn't rewrite them. `ghost` drafts in your voice but marks what's grounded in evidence vs. inferred from style.

Your vault is a record of how *you* actually think. The goal is to amplify that — not to have a system quietly reshaping it.

---

### How it works

1. **Config**: Settings live in `~/.claude/CLAUDE.md` under `## Vault Structure` — vault path, language, and folder mappings. Written once by `/hirameki:__init`, read by all other commands.
2. **Folder detection**: Commands look for common folder names (`_daily/`, `Daily/`, `Journal/` etc.). Missing folders are created on first use and saved to config.
3. **Content scanning**: All non-system folders in your vault root are treated as "content folders" — whatever structure you use, commands adapt.
4. **Write safety**: Every command that writes a file shows a full preview and path before writing. Nothing is written without confirmation.

---

### License

MIT

</details>

---

<details>
<summary><h2 id="繁體中文">繁體中文</h2></summary>

### 靈感來源

Hirameki 的靈感來自 [internetvin](https://x.com/internetvin)，尤其是 [Greg Isenberg](https://x.com/gregisenberg)（[The Idea Browser](https://theideabrowser.com) 創辦人）在這支影片中展示的工作流程：

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

然後執行 `/hirameki:__init` 完成 vault 設定。它會：
- 偵測你的 Obsidian vault
- 詢問偏好的輸出語言
- 解析資料夾結構
- 把指令參考文件複製到 vault 中

如果在 vault 目錄內開啟 Claude Code，路徑會自動偵測。

---

### 指令說明

#### 日常節奏

**`/hirameki:status`**
Vault 現況摘要。掃描所有內容資料夾（深度 2 層）和最近 7 天的 daily notes。輸出：各資料夾的內容主題與活躍狀態、最近的檔案變更、vault 整體統計。適合每次 session 開始時執行。

**`/hirameki:catchup [天數]`**
進度銜接。讀取最近 daily notes 的最後一個 Wrap 區塊和所有 inbox 項目，提出 1–3 個今日建議焦點。預設為昨天。範例：`/hirameki:catchup 3` 回顧最近 3 天。

**`/hirameki:wrap [描述]`**
進度快照。掃描本次 session 的檔案操作，在今天的 daily note 末尾追加一個帶時間戳的區塊，包含：已完成、進行中、下一步。可一天執行多次，每次追加新區塊。可加入描述來聚焦 wrap 的摘要方向。

**`/hirameki:weekreview`**
週回顧與落差分析。比對 daily notes 中聲稱的優先事項與實際的檔案變更，找出意圖與行動之間的落差。需要至少 3 天的 daily notes。

---

#### 概念考古

**`/hirameki:arc {概念}`**
追蹤一個概念在 vault 中的演化軌跡。找出所有提及，按日期排列，產出從首次出現到目前狀態的時間軸。標出空白地帶 — 這個概念尚未被探討的面向。同概念同天：追加更新而不建新檔。

**`/hirameki:bridge {主題A} 與 {主題B}`**
找出兩個主題之間的隱藏連結。輸出：同時提到兩者的檔案、可能構成橋樑的筆記、1–3 個附信心度的深層連結假設。同組合同天：追加。

**`/hirameki:undercurrent [範圍]`**
發掘潛流主題。掃描所有內容資料夾和 daily notes，找出出現在 3 個以上不同檔案但沒有獨立文章的詞彙或想法。可選擇聚焦特定目錄。

**`/hirameki:cluster [範圍]`**
想法群聚分析。找出 3 篇以上涉及相似概念但沒有共同上層分類、且撰寫時間分布在不同日期的筆記群。按成熟度評分，建議發展方向：文章、專案、框架或繼續累積。

---

#### 思考工具

**`/hirameki:ghost {問題} [save]`**
用你的語氣回答問題。讀取你的完成文章，提取文風模式和既有立場，用那個聲音組成回答。標注哪些部分有 vault 依據、哪些是風格推測。加 `save` 寫入檔案。

**`/hirameki:stress-test {主題} [save]`**
對主題論述進行壓力測試。收集所有相關主張，逐一檢查：內部矛盾、未驗證假設、邏輯跳躍、證據缺口。輸出整體穩固度評分和最需優先處理的 1–3 個弱點。加 `save` 寫入檔案。

**`/hirameki:harvest [save]`**
從既有內容收割可行動想法。掃描內容資料夾、30 天 daily notes、inbox。輸出四個類別（各最多 5 個）：可以寫的文章、可以做的工具或專案、值得研究的主題、可以聯繫的人或社群。加 `save` 寫入檔案。

**`/hirameki:graduate`**
讓半成形想法畢業為獨立筆記。掃描最近 14 天的 daily notes 和 logs，找出卡在「進行中」或「下一步」的項目，加上 inbox 和草稿資料夾。三個畢業標準：明確核心主張、與既有 vault 主題相關、足夠的內容密度。兩個階段：先列候選清單，確認後才執行。

---

#### 維護

**`/hirameki:tidy [fix]`**
屬性健檢。掃描所有內容資料夾、inbox 和 30 天 daily notes。檢查四個類別：缺漏（無 frontmatter、無 tags、無 status）、一致性（無效 status/source 值、tag 大小寫、底線 vs 連字號）、冗餘（只出現 1 次的 tag、超過 6 個 tag 的檔案、topic/tag 重複）、tag 收斂（頻率統計、合併候選、孤立 tag）。輸出健康度分數。加 `fix` 自動修正可確定的問題，需判斷的逐一確認。

---

#### 紀錄

**`/hirameki:journal {描述}`**
工作紀錄與思考文章。寫入結構化記錄，包含：背景、做了什麼、為什麼這樣做、靈感連結、可能的改進方向、未完成事項。同主題同天：追加更新並標記已完成的後續。搜尋 vault 中相關筆記作為脈絡和 [[wiki link]]。

---

### 為什麼是指令，而不是 Agent

Hirameki 設計為明確的指令，而不是自主在背景運作的 Agent。兩個原因：

**安全性。** 所有寫入檔案的指令在執行前都會顯示完整內容和目標路徑。唯讀指令（`status`、`arc`、`stress-test`）產出的結果你可以採用或忽略 — 沒有你的明確要求，它們不會動你的 vault。寫入指令（`wrap`、`journal`、`graduate`）在寫入時需要確認。`tidy fix` 把可以安全自動化的部分與需要你判斷的部分分開處理。

**主體可操控性。** 指令找出模式、連結和建議 — 但每個決定都是你的。`graduate` 找出候選想法，但等你決定哪些準備好了。`stress-test` 找出論述的弱點，但不會幫你改寫。`ghost` 用你的語氣起草，但會標注哪些有 vault 依據、哪些是風格推測。

你的 vault 記錄的是*你*真實的思考方式。目標是放大這個 — 而不是讓一個系統在背後悄悄改塑它。

---

### 運作方式

1. **設定**：設定存在 `~/.claude/CLAUDE.md` 的 `## Vault Structure` 段落 — vault 路徑、語言、資料夾對應。由 `/hirameki:__init` 一次寫入，其他所有指令直接讀取。
2. **資料夾偵測**：指令依候選名稱順序尋找資料夾（`_daily/`、`Daily/`、`Journal/` 等）。找不到的在首次使用時建立並存入設定。
3. **內容掃描**：vault 根目錄下所有非系統資料夾視為「內容資料夾」— 無論你怎麼組織筆記，指令都能適應。
4. **寫入安全**：所有寫入檔案的指令在執行前都會顯示完整預覽和路徑。沒有確認不會寫入。

---

### 授權

MIT

</details>

---

<details>
<summary><h2 id="日本語">日本語</h2></summary>

### インスピレーション

Hirameki は [internetvin](https://x.com/internetvin) — 特に [The Idea Browser](https://theideabrowser.com) の創業者 [Greg Isenberg](https://x.com/gregisenberg) がこの動画で紹介しているワークフローからインスパイアされています：

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

次に `/hirameki:__init` を実行して vault をセットアップします。以下を行います：
- Obsidian vault を検出
- 希望する出力言語を確認
- フォルダ構造をマッピング
- リファレンスドキュメントを vault にコピー

vault ディレクトリ内で Claude Code を開いている場合、パスは自動検出されます。

---

### コマンド説明

#### 日常リズム

**`/hirameki:status`**
Vault の現況サマリー。すべてのコンテンツフォルダ（深さ 2 層）と直近 7 日の daily notes をスキャン。出力：各フォルダのコンテンツテーマとアクティビティ状態・最近のファイル変更・vault 全体の統計。セッション開始時に実行するのに最適。

**`/hirameki:catchup [日数]`**
進捗の引き継ぎ。最近の daily notes の最後の Wrap ブロックとすべての inbox アイテムを読み込み、今日のフォーカスとして 1〜3 件を提案。デフォルト：昨日。例：`/hirameki:catchup 3` で直近 3 日を振り返る。

**`/hirameki:wrap [説明]`**
進捗スナップショット。セッションのファイル操作をスキャンし、今日の daily note の末尾にタイムスタンプ付きのブロックを追記。内容：完了・進行中・次のステップ。1 日に複数回実行可能で、毎回新しいブロックを追記。オプションで説明を追加すると要約の方向性が定まる。

**`/hirameki:weekreview`**
週次レビューとギャップ分析。daily notes で宣言した優先事項と実際のファイル変更を比較し、意図と行動のずれを表面化。最低 3 日分の daily notes が必要。

---

#### 概念考古学

**`/hirameki:arc {概念}`**
Vault 内での概念の進化を追跡。すべての言及を見つけ、日付順に並べ、初出から現在の状態までのタイムラインを生成。空白地帯（その概念でまだ探求されていない角度）を特定。同概念・同日：新規ファイルではなく追記。

**`/hirameki:bridge {テーマA} と {テーマB}`**
2 つのテーマ間の隠れたつながりを発見。出力：両方に言及しているファイル・橋渡しになりうるノート・信頼度付きの深層つながり仮説 1〜3 件。同組み合わせ・同日：追記。

**`/hirameki:undercurrent [スコープ]`**
潜流テーマの発掘。すべてのコンテンツフォルダと daily notes をスキャンし、3 つ以上の異なるファイルに登場するが独立した記事がない単語やアイデアを表面化。オプションで特定ディレクトリに絞ることができる。

**`/hirameki:cluster [スコープ]`**
アイデアのクラスター分析。類似した概念を扱う 3 本以上のノートが、共通の上位カテゴリなしに異なる日付で書かれているグループを発見。成熟度でスコアリングし、発展方向を提案：記事・プロジェクト・フレームワーク・継続蓄積。

---

#### 思考ツール

**`/hirameki:ghost {質問} [save]`**
あなたの語り口で質問に回答。完成した文章を読み込み、文体パターンと既存のスタンスを抽出し、そのボイスで回答を構成。Vault の根拠がある部分とスタイルによる推測の延長を明記。`save` を末尾に追加でファイルに保存。

**`/hirameki:stress-test {テーマ} [save]`**
論述の圧力テスト。すべての関連主張を収集し、各主張について確認：内部矛盾・未検証の前提・論理の飛躍・証拠の欠如。総合的な堅牢度評価と優先的に対処すべき 1〜3 つの弱点を出力。`save` を追加でファイルに保存。

**`/hirameki:harvest [save]`**
既存コンテンツから実行可能なアイデアを収穫。コンテンツフォルダ・30 日分の daily notes・inbox をスキャン。4 カテゴリを出力（各最大 5 件）：書ける記事・作れるツールまたはプロジェクト・研究すべきテーマ・連絡すべき人またはコミュニティ。`save` を追加でファイルに保存。

**`/hirameki:graduate`**
半成形のアイデアを独立ノートに卒業させる。直近 14 日の daily notes と logs をスキャンし、「進行中」や「次のステップ」で止まっているアイテムを発見。inbox とドラフトフォルダも対象。3 つの卒業基準：明確な核心主張・既存 vault テーマとの関連・十分なコンテンツ密度。2 フェーズ：まず候補リストを表示し、確認後にのみ実行。

---

#### メンテナンス

**`/hirameki:tidy [fix]`**
プロパティの健全性チェック。すべてのコンテンツフォルダ・inbox・30 日分の daily notes をスキャン。4 カテゴリを確認：欠落（frontmatter なし・tags なし・status なし）・一貫性（無効な status/source 値・タグの大小文字・アンダースコア vs ハイフン）・冗長性（1 回だけ登場するタグ・6 個超のタグを持つファイル・topic/tag の重複）・タグの収束（頻度統計・統合候補・孤立タグ）。健全性スコアを出力。`fix` を追加で確実なものを自動修正、判断が必要なものは個別確認。

---

#### 記録

**`/hirameki:journal {説明}`**
作業ログと思考記事。構造化された記録を書き込み：背景・何をしたか・なぜしたか・インスピレーションのつながり・改善の可能性・未完了事項。同テーマ・同日：追記更新し完了した後続事項をマーク。関連する vault ノートを検索して文脈と [[wiki link]] を提供。

---

### なぜエージェントではなくコマンドなのか

Hirameki は、バックグラウンドで自律的に動くエージェントではなく、明示的なコマンドとして設計されています。理由は 2 つです。

**安全性。** ファイルを書き込むすべてのコマンドは、実行前に完全な内容と書き込み先パスを表示します。読み取り専用のコマンド（`status`・`arc`・`stress-test`）は採用しても無視してもいい出力を生成するだけで、明示的な要求なしには vault に触れません。書き込みコマンド（`wrap`・`journal`・`graduate`）は書き込み時に確認を求めます。`tidy fix` は安全に自動化できる部分と、あなたの判断が必要な部分を分けて処理します。

**主体としての操作性。** コマンドはパターン・つながり・提案を表面化しますが、すべての判断はあなたのものです。`graduate` は候補を特定しますが、どのアイデアが準備できているかはあなたが決めます。`stress-test` は論述の弱点を見つけますが、書き直しはしません。`ghost` はあなたの語り口で下書きしますが、根拠がある部分と推測の延長を明記します。

あなたの vault は、*あなた*が実際にどう考えるかの記録です。それを増幅するのが目的 — システムが静かに形を変えていくのではなく。

---

### 動作の仕組み

1. **設定**：設定は `~/.claude/CLAUDE.md` の `## Vault Structure` セクションに保存 — vault パス・言語・フォルダマッピング。`/hirameki:__init` が一度だけ書き込み、他のすべてのコマンドが直接読み込む。
2. **フォルダ検出**：候補名の順番でフォルダを探す（`_daily/`・`Daily/`・`Journal/` など）。見つからない場合は初回使用時に作成して設定に保存。
3. **コンテンツスキャン**：vault ルート直下のすべての非システムフォルダを「コンテンツフォルダ」として扱う — どのような構成でも適応。
4. **書き込み安全性**：ファイルを書き込むすべてのコマンドは実行前に完全なプレビューとパスを表示。確認なしには書き込まない。

---

### ライセンス

MIT

</details>
