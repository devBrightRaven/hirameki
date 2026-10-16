> Codex 版生成指南。實際工作流以 `references/` 為準；這份翻譯摘要不是 runtime 設定。

# Hirameki — 五個目的導向入口

> 2.2.0 整合工作流程入口；來源驗證、模型驗收、安裝與排程分開判定。

先用當前明示設定或 `~/.codex/hirameki-local.md` 取得 vault 路徑與語言，再從 `<vault>/AGENTS.md` 讀取共用資料夾配置。不得以其他 agent 設定作為退路。

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

未決或形成中的 trace 使用 `save this`，不等於已定案節點。

◆ **決策可記錄｜decision-trace** ：只是提醒，不代表已保存或取得授權。
