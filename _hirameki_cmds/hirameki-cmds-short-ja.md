# Hirameki コマンド

Claude Code CLI で使用します。すべてのコマンドは `/hirameki:` で始まります。

---

## 日常リズム

### `/hirameki:status`
Vault の現況サマリー。コンテンツのテーマと各フォルダの最近の活動をスキャン。
入力不要。セッション開始時に実行するのに適しています。

### `/hirameki:catchup [日数]`
進捗の引き継ぎ。最近の Wrap 進捗 + inbox の未処理アイテムを読み込み、今日のフォーカスを提案。
オプション入力：日数（デフォルト 1）。例：`/hirameki:catchup 3` で直近 3 日を振り返る。

### `/hirameki:wrap [説明]`
進捗スナップショット。完了・進行中・次のステップを記録 — 当日の daily note に追記。1 日に複数回実行可能。
オプション入力：今回の wrap の重点説明。
書き込み先：`{daily-notes}/YYYY-MM-DD.md`

### `/hirameki:weekreview`
週次レビュー。宣言した優先事項と実際のファイル変更を比較し、意図と行動のギャップを発見。
入力不要。ギャップ分析には最低 3 日分の daily notes が必要。

---

## 概念考古学

### `/hirameki:arc {概念}`
Vault 内での概念の進化を追跡。初出から現在の状態までのタイムライン。同概念・同日は追記。
例：`/hirameki:arc 能動性`、`/hirameki:arc ミニマリズム`
書き込み先：`{analysis}/arc/`

### `/hirameki:bridge {テーマA} と {テーマB}`
2 つのテーマ間の隠れたつながりを発見。直接の交点、橋渡しノート、潜在的な深層仮説を列挙。同組み合わせ・同日は追記。
例：`/hirameki:bridge アクセシビリティ と prompt engineering`
書き込み先：`{analysis}/bridge/`

### `/hirameki:undercurrent [スコープ]`
潜流テーマの発掘。繰り返し登場するが独立した記事がないテーマを発見。同日は追記。
オプション入力：特定ディレクトリに絞る。
書き込み先：`{analysis}/undercurrent/`

### `/hirameki:cluster [スコープ]`
アイデアのクラスター分析。まとまりつつあるノートグループを発見。同日は追記。
オプション入力：特定スコープに絞る。
書き込み先：`{analysis}/cluster/`

---

## 思考ツール

### `/hirameki:ghost {質問} [save]`
あなたの語り口で質問に回答。あなたの文章スタイルと既存のスタンスに基づく。
例：`/hirameki:ghost AI エージェントはどれほど自律的であるべき？`
Vault の根拠がある部分と推測による延長を明記。
`save` を末尾に追加でファイルに保存：`/hirameki:ghost AI 自律性の上限？ save`
書き込み先：`{analysis}/ghost/`

### `/hirameki:stress-test {テーマ} [save]`
論述の圧力テスト。矛盾・未検証の前提・論理の飛躍・証拠の欠如を発見。
例：`/hirameki:stress-test prompt engineering の限界`
`save` を末尾に追加でファイルに保存。
書き込み先：`{analysis}/stress-test/`

### `/hirameki:harvest [save]`
既存コンテンツから実行可能なアイデアを収穫。4 カテゴリ：書ける記事・作れるツール・研究すべきテーマ・連絡すべき人。
入力不要。各カテゴリ最大 5 件、ソースノート付き。
`save` を入力してファイルに保存：`/hirameki:harvest save`
書き込み先：`{analysis}/harvest/`

### `/hirameki:graduate`
半成形のアイデアを独立ノートに卒業させる。直近 14 日の daily notes・logs・inbox・drafts・thoughts をスキャン。
入力不要。2 段階：候補リストを先に表示し、確認後に実行。
書き込み先：ユーザーが指定したコンテンツフォルダ

---

## メンテナンス

### `/hirameki:tidy [fix]`
プロパティの健全性チェック。Vault 内の全ファイルの frontmatter に欠落フィールド・タグの不整合・冗長なプロパティがないか確認。健全性スコアを出力。
入力不要でレポート生成。`fix` を入力で確認後に自動修正：`/hirameki:tidy fix`
書き込み先：`{analysis}/tidy/`

---

## 記録

### `/hirameki:journal {説明}`
作業ログと思考記事。何をしたか・なぜしたか・インスピレーションのつながり・改善の可能性を記録。同テーマ・同日は自動追記。
例：`/hirameki:journal slash command の命名リファクタリング`
書き込み先：`{logs}/YYYY-MM-DD-{テーマ}.md`

---

## 書き込み動作一覧

| コマンド | 書き込み先 | トリガー | 同日重複 |
|---|---|---|---|
| `/hirameki:wrap` | daily-notes | 常時 | 新しい Wrap ブロックを追記 |
| `/hirameki:journal` | logs | 常時 | 同テーマは追記、別テーマは新規作成 |
| `/hirameki:arc` | analysis/arc | 常時 | 同概念は追記、別概念は新規作成 |
| `/hirameki:bridge` | analysis/bridge | 常時 | 同組み合わせは追記 |
| `/hirameki:undercurrent` | analysis/undercurrent | 常時 | 追記更新 |
| `/hirameki:cluster` | analysis/cluster | 常時 | 追記更新 |
| `/hirameki:ghost` | analysis/ghost | `save` のみ | 同質問は追記 |
| `/hirameki:stress-test` | analysis/stress-test | `save` のみ | 同テーマは追記 |
| `/hirameki:harvest` | analysis/harvest | `save` のみ | 追記更新 |
| `/hirameki:graduate` | コンテンツフォルダ | 確認後 | 毎回独立 |
| `/hirameki:tidy` | analysis/tidy | 常時 | 追記更新 |

書き込みを行うすべてのコマンドは、実行前にプレビューと完全なパスを表示します。

出力言語は `__init` 初回実行時に設定され、`~/.claude/CLAUDE.md` に保存されます。
