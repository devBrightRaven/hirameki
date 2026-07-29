# Hirameki コマンド

Claude Code CLI で使用します。すべてのコマンドは `/hirameki:` で始まります。

---

## Orchestrators（オーケストレーター）

ここから始めましょう — 各 orchestrator は関連するプリミティブを一つのガイド付きフローにまとめます。個々のプリミティブは単独でも引き続き使用できます。

### `/hirameki:triage`
セッション終了バンドル：wrap → journal → handoff を順番に実行。各ステップで完全なドラフトを表示し、save / skip / edit を選択してから次へ進みます。
引数なし。セッション終了時に実行。

### `/hirameki:lens <概念>`
トピック理解フロー：arc → ポジション抽出 → bridge → challenge。各ステップを個別に保存またはスキップできます。
入力：単一の概念またはトピック（必須）。

### `/hirameki:compose <トピック>`
トピック創作フロー：あなたの文体で回答を作成 → 五問フレームテスト。各ステップを個別に保存またはスキップできます。
入力：トピックまたは質問（必須）。スタンドアロン — `/hirameki:lens` を先に実行する必要はありません。

### `/hirameki:mekiki <入力>`
外部リソースキャプチャ。入力タイプを自動検出：
- GitHub URL または `owner/repo` → リポジトリ分析（テクニック抽出 + adopt/defer/reject 判定）
- 記事 URL → Web 記事キャプチャ + vault クロスリファレンス
- 貼り付けたテキストまたはローカルファイルパス → 記事キャプチャ + vault クロスリファレンス

リポジトリ出力：`{research}/mekiki-{repo名}.md`
記事出力：`{inbox}/YYYY-MM-DD-{slug}.md`

---

## セッション

### `/hirameki:next`
セッション再開後の定位。完了した作業・未処理事項・次のステップを整理。入力不要。ファイルへの書き込みなし。

### `/hirameki:wrap [説明]`
進捗スナップショット。完了・進行中・次のステップを記録 — 当日の daily note に追記。1 日に複数回実行可能。
オプション入力：今回の wrap の重点説明。
書き込み先：`{daily}/YYYY-MM-DD.md`

### `/hirameki:journal <説明>`
作業ログと推論記録。何をしたか・なぜしたか・インスピレーションのつながり・未完了事項を記録。同テーマ・同日は追記、異なるテーマは新規作成。
入力：トピック説明（必須）。
書き込み先：`{journal}/YYYY-MM-DD-HHMM-{トピック}.md`

### `/hirameki:handoff`
セッション引き継ぎ文書。現在の状態・未完了スレッド・次セッションへの引き継ぎ指示を記録。セッション活動からトピックを自動推定。
書き込み先：`{handoff}/YYYY-MM-DD-{slug}.md`

---

## 理解（スタンドアロン）

これらは `/hirameki:lens` がまとめるプリミティブです。素早いピンポイント調査には直接呼び出せます。

### `/hirameki:arc <概念>`
概念進化トラッカー。vault 全体でその概念の最初の登場・タイムライン・現在の状態・未探索の角度を表示。
書き込み先：`{research}/arc/YYYY-MM-DD-{概念}.md`。同概念・同日は追記。

### `/hirameki:bridge <A> and <B>`
二つのトピック間の隠れたつながり。直接の交差点・橋渡しノート・より深いつながりの仮説を提案。
書き込み先：`{research}/bridge/YYYY-MM-DD-{A}-{B}.md`。同ペア・同日は追記。

### `/hirameki:challenge <トピック>`
論証の弱点分析。このトピックに関する vault の各主張について、内部矛盾・未検証の前提・論理の飛躍・証拠の欠缺を確認。
書き込み先：`{research}/challenge/YYYY-MM-DD-{トピック}.md`

### `/hirameki:reflect <質問>`
Vault 文体での回答。あなたの文章スタイルを分析し、ポジションを抽出し、あなたの文体で回答を記述。出典引用と確信度の注記付き。
`save` を追加で書き込み：`{research}/reflect/YYYY-MM-DD-{質問}.md`

---

## 創作（スタンドアロン）

これらは `/hirameki:compose` がまとめるプリミティブです。

### `/hirameki:frame <アイデア>`
制作前チェックポイント。五問フレーム（Only-I テスト・衝突スキャン・賭け・緊張・証拠）。四つの判定：PROCEED / RETHINK / KILL / CONSOLIDATE。コンテンツを生成しない — 存在すべきかどうかのみを評価。
`save` を追加で書き込み：`{research}/frame/YYYY-MM-DD-{slug}.md`

### `/hirameki:critique <ファイル>`
マルチモデル文章クリティーク。三評者を並列起動（Opus / Codex GPT / Gemini Pro）。各評者が感官密度・構造的緊張・共鳴を評点（1–10）。比較表に統合し、不一致を強調表示。
書き込み先：`{vault}/_writing_lab/benchmark/`

---

## Vault

### `/hirameki:pulse [week|patterns]`
3 つのモード：
- **`pulse`** — 即時概要：コンテンツテーマ・最近の活動・統計。
- **`pulse week`** — 週次レビュー：宣言した優先事項と実際のファイル変更のギャップ分析。
- **`pulse patterns`** — 潜流とクラスター：独立した記事のない繰り返しテーマと形成中のアイデアグループ。
ファイルへの書き込みなし。

### `/hirameki:harvest [save]`
既存コンテンツから実行可能なアイデアを収穫。7 カテゴリ（各最大 5 件）：書ける記事 / 作れるツールまたはプロジェクト / 研究すべきテーマ / 連絡すべき人またはコミュニティ / 別のメディアで表現したいアイデア / まだ取引していない価値 / 卒業できるアイデア。
卒業カテゴリ：2 フェーズ — 候補を確認後にファイルを作成。
`save` を追加でサマリーを書き込み：`{research}/harvest/`

### `/hirameki:graduate <ノート>`
ノートを安定した概念カードに昇格。フロントマターを検証し、正式ステータスを設定、関連カードにリンク。

### `/hirameki:tasks [日数|stuck]`
daily notes と journal から次のアクションを集約。重複除去して出現頻度順に並べる。3 回以上登場するアイテムは先延ばしシグナルとしてフラグ表示。
- **`tasks`** — 直近 3 日
- **`tasks N`** — N 日分を遡る
- **`tasks stuck`** — 「完了」セクションに一度も現れていない繰り返し未完了タスク
ファイルへの書き込みなし。

---

## メンテナンス

### `/hirameki:tidy [tags|fix|full|lint]`
フロントマター健全性チェック。デフォルトは欠落フィールド + 一致性チェックのみ（軽量）。
- **`tidy`** — 欠落フィールド + 一致性チェック
- **`tidy tags`** — タグ収束分析（主要タグ・孤立タグ・統合候補）
- **`tidy fix`** — 欠落フィールド + 一致性 + 自動修正
- **`tidy full`** — 全チェック
- **`tidy lint`** — コンテンツ健全性（矛盾・陳腐な主張・孤立ノート・デッドリンク）

書き込み先：`{research}/tidy/`

### `/hirameki:__init`
初回セットアップ：vault の検出・言語設定・フォルダー解決、`~/.claude/vault-local.md`（vault パス・言語）と `<vault>/AGENTS.md`（フォルダー構造）への書き込み。マシンごとに一回実行。設定が存在する場合は Mode B（再設定）として動作。

---

## 書き込み動作一覧

| コマンド | 書き込み先 | トリガー | 同日重複 |
|----------|-----------|---------|---------|
| `triage` | daily + journal + handoff | ステップごと（save/skip） | 各サブフローはプリミティブの動作に従う |
| `lens` | research/lens/ | ステップごと（save/skip） | 各ステップで独立したファイル |
| `compose` | research/compose/ | ステップごと（save/skip） | 各ステップで独立したファイル |
| `wrap` | daily | 常時 | 新しい Wrap ブロックを追記 |
| `journal` | journal | 常時 | 同テーマは追記、別テーマは新規作成 |
| `handoff` | handoff | 常時 | 同日付は上書き |
| `arc` | research/arc/ | 常時 | 同概念は追記 |
| `bridge` | research/bridge/ | 常時 | 同ペアは追記 |
| `challenge` | research/challenge/ | 常時 | 同トピックは追記 |
| `reflect` | research/reflect/ | `save` のみ | 同質問は追記 |
| `frame` | research/frame/ | `save` のみ | アイデアごとに新規 |
| `mekiki`（リポジトリ） | research/ | 常時 | リポジトリごとに新規 |
| `mekiki`（記事） | inbox/ | 常時 | 記事ごとに新規 |
| `graduate` | コンテンツフォルダー | 確認後 | 毎回独立 |
| `harvest` | research/harvest/ | `save` のみ | 追記更新 |
| `tidy` | research/tidy/ | 常時 | 追記更新 |
| `critique` | _writing_lab/benchmark/ | 常時 | 毎回新規 |
| `tasks` | なし | — | — |
| `next` | なし | — | — |
| `pulse` | なし | — | — |

書き込みを行うすべてのコマンドは、実行前にプレビューと完全なパスを表示します。

出力言語は `/hirameki:__init` 初回実行時に設定され、`~/.claude/vault-local.md` に保存されます。
