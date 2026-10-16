# Hirameki — 目的別の五つの入口

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

未解決または形成中の trace は `save this` を使います。確定した決定ノードとは区別します。

◆ **決策可記錄｜decision-trace** ：リマインダーであり、保存や承認ではありません。
