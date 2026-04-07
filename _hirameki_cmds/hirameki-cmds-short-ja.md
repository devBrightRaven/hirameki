# Hirameki コマンド

Claude Code CLI で使用します。すべてのコマンドは `/hirameki:` で始まります。

---

## セッション開始

### `/hirameki:catchup [日数]`
進捗の引き継ぎ。最近の Wrap 進捗 + inbox の未処理アイテムを読み込み、今日のフォーカスを提案。
オプション入力：日数（デフォルト 1）。例：`/hirameki:catchup 3` で直近 3 日を振り返る。

### `/hirameki:next`
セッション再開後の定位。完了した作業・未処理の事項・次のステップを整理。

## セッション終了

### `/hirameki:wrap [説明]`
進捗スナップショット。完了・進行中・次のステップを記録 — 当日の daily note に追記。1 日に複数回実行可能。
オプション入力：今回の wrap の重点説明。
書き込み先：`{daily-notes}/YYYY-MM-DD.md`

## Vault の状態

### `/hirameki:pulse [week|patterns]`
3 つのモード：
- **`pulse`** — 即時スナップショット：コンテンツテーマ・最近の活動・統計。セッション開始時に実行するのに最適。
- **`pulse week`** — 週次レビュー：宣言した優先事項と実際のファイル変更を比較してギャップを発見。
- **`pulse patterns`** — 潜流とクラスター：独立した記事のない繰り返し登場するテーマと、形成中のアイデアグループを表面化。

### `/hirameki:tasks [日数|stuck]`
daily notes と journal から次のアクションを集約し、重複を除去して出現頻度順に並べる。3 回以上登場するアイテムは先延ばしシグナルとしてフラグ表示。
- **`tasks`** — デフォルト：直近 3 日
- **`tasks N`** — N 日分を遡る
- **`tasks stuck`** — 「完了」セクションに一度も現れていない繰り返し未完了タスクを発見

## 深掘り

### `/hirameki:lucky [n]`
コンステレーション（星座）リーディング — N 件のノートをランダム抽出（デフォルト 5、範囲 2–20）。30 日以上触れていない放置ノートを優先選択。これらの交差点にある隠れたテーマと、vault が直接述べることなく周回している 1 つの問いを出力。出力はターミナルのみ。

### `/hirameki:explore {入力} [save]`
概念挖掘 — 入力の形からモードを自動判断：
- **単一の概念** → Arc：vault 内でのその概念の進化タイムライン
- **A と B**（または A and B / A 與 B）→ Bridge：2 つのトピック間の隠れたつながり
- **`?`や`？`で終わる** → Ghost：あなたの語り口で回答、vault の根拠を明記
- **`test:` で始まる** → Stress-test：矛盾・ギャップ・未検証の前提を発見

末尾に `save` を追加でファイルに保存。
書き込み先：`{analysis}/arc/`・`{analysis}/bridge/`・`{analysis}/ghost/`・`{analysis}/stress-test/`

## アクションプランニング

### `/hirameki:harvest [save]`
既存コンテンツから実行可能なアイデアを収穫。7 カテゴリ（各最大 5 件）：
書ける記事 / 作れるツールまたはプロジェクト / 研究すべきテーマ / 連絡すべき人またはコミュニティ / 別のメディアで表現したいアイデア / まだ取引していない価値 / 卒業できるアイデア

卒業カテゴリ：2 フェーズ — 候補を確認、選択後にファイルを作成。
末尾に `save` を追加でサマリーをファイルに保存。
書き込み先：`{analysis}/harvest/`；卒業はユーザー指定のコンテンツフォルダへ

## 創作

### `/hirameki:frame {アイデア} [save]`
制作前チェックポイント。5 つの問い（Only-I テスト・衝突スキャン・賭け・緊張・証拠）。4 つの判定：PROCEED / RETHINK / KILL / CONSOLIDATE。コンテンツを生成しない — 存在すべきかどうかのみを評価する。
`save` を追加で書き込み先：`{research}/frame/YYYY-MM-DD-{idea-slug}.md`

### `/hirameki:critique {ファイル|テキスト}`
マルチモデル文章クリティーク。3 評者を並列起動（Opus / Codex / Gemini）。各評者が感官密度・構造的緊張・共鳴を評点（1–10）。比較表に統合、3 点以上の差異を重点表示。
書き込み先：`{vault}/_writing_lab/benchmark/`

## 外部

### `/hirameki:mekiki {github-url}`
GitHub リポジトリ分析。転用可能なテクニックを抽出 + 採用適合度を評価。2 トラック：テクニック抽出（具体的な次のステップ付きパターン）と採用評価（機能比較 + adopt/defer/reject 判定）。
保存先：`{research}/mekiki-{repo名}.md`

## 意思決定サポート

### `/hirameki:decide {テーマ}`
意思決定前スキャン。vault の関連コンテキストをスキャンし、3 層構造で出力：現状（可逆性の判定含む）・詰まりポイント（逆算法：何が失敗を招くか）・核心の問い（提案ではなく 1 つの問い）。
ファイルには書き込まない。保存したい場合は `/hirameki:journal` を続けて実行。

## メンテナンス

### `/hirameki:tidy [tags|fix|full]`
プロパティの健全性チェック。デフォルトは欠落フィールド + 一致性チェックのみ（軽量）。
- **`tidy`** — 欠落フィールド + 一致性チェック
- **`tidy tags`** — タグ収束分析（主要タグ・孤立タグ・統合候補）
- **`tidy fix`** — 欠落フィールド + 一致性 + 自動修正
- **`tidy full`** — 全チェック

書き込み先：`{analysis}/tidy/`

## 作業推論ログ

### `/hirameki:journal {説明}`
作業ログと思考記録。何をしたか・なぜしたか・インスピレーションのつながり・未完了事項を記録。同テーマ・同日は自動追記。
例：`/hirameki:journal slash command のプレフィックスをリファクタリング`
書き込み先：`{logs}/YYYY-MM-DD-HHMM-{テーマ}.md`

---

## 書き込み動作一覧

| コマンド | 書き込み先 | トリガー | 同日重複 |
|----------|-----------|---------|---------|
| `/hirameki:wrap` | daily-notes | 常時 | 新しい Wrap ブロックを追記 |
| `/hirameki:journal` | logs | 常時 | 同テーマは追記、別テーマは新規作成 |
| `/hirameki:explore` | analysis/arc, bridge, ghost, stress-test | `save` のみ | 同概念/質問は追記 |
| `/hirameki:harvest` | analysis/harvest | `save` のみ | 追記更新 |
| `/hirameki:harvest`（卒業） | コンテンツフォルダ | 確認後 | 毎回独立 |
| `/hirameki:tidy` | analysis/tidy | 常時 | 追記更新 |
| `/hirameki:frame` | research/frame/ | `save` のみ | アイデアごとに新規 |
| `/hirameki:critique` | _writing_lab/benchmark/ | 常時 | 毎回新規 |
| `/hirameki:mekiki` | research/ | 常時 | リポジトリごとに新規 |
| `/hirameki:tasks` | なし | — | — |
| `/hirameki:lucky` | なし | — | — |

書き込みを行うすべてのコマンドは、実行前にプレビューと完全なパスを表示します。

出力言語は `/hirameki:__init` 初回実行時に設定され、`~/.claude/CLAUDE.md` に保存されます。
