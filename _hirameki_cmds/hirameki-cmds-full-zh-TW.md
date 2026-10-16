# Hirameki — 五個目的導向入口 — 完整指南

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
