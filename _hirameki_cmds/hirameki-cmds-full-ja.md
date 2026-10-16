# Hirameki — 目的別の五つの入口 — 詳細ガイド

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
