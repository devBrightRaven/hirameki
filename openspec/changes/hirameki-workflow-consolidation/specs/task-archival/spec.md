## Purpose

讓 tidy 與既有 Vault Hygiene 依可追查的完成證據自動收斂有效待辦，減少使用者逐項審查，同時保留歷史、恢復路徑與未結責任，不把勾選或過期日期誤當完成。

## ADDED Requirements

### Requirement: Evidence gate precedes automatic archival
Agent SHALL 找出任務 identity、範圍、完成條件、結果及來源 revision、未結子任務或依賴、後續重開證據；固定歸檔 gate MUST 要求完成條件滿足、證據可追查且無未結事項。checkbox、mtime、日期或模型信心均不得單獨使 gate 通過。資訊不足先窄範圍查既有來源，仍不足保留；矛盾不得自行裁定。

#### Scenario: Implementation done but required deployment pending
- **WHEN** 程式完成但任務承諾的部署或驗收未完成
- **THEN** 保留有效待辦，不縮小任務範圍來歸檔。

#### Scenario: Historical unchecked item has completion evidence
- **WHEN** 舊清單仍未勾選，但可追查來源證實全部承諾已完成且沒有重開
- **THEN** 可以通過 gate，不以 checkbox 推翻結果證據。

### Requirement: Automatic execution requires standing bounded authority
tidy SHALL 將已完成任務移出有效待辦，而非預設搬走整篇筆記；只在使用者事先批准的來源範圍、操作及 gate 下自動執行，不逐項要求確認。不在該範圍則唯讀。MUST NOT 刪除原文、改已交付信件、直接 archive OpenSpec change、連帶歸檔專案或自動更改決策狀態。

#### Scenario: Completed task inside mixed note
- **WHEN** 同一筆記有完成與未完成任務
- **THEN** 只收斂已完成項目的有效索引，保留原始筆記與其他任務，具體格式待歷史盤點定案。

### Requirement: Archival is reversible and revision-aware
執行 SHALL 留 task identity、判定證據、來源及操作前後 revision、gate version、owner 與恢復資料；寫入前再核對來源，source 已變或衝突就停止該項。MUST 支援重複執行不重複歸檔、部分失敗有界恢復、後來重開重新列為有效；多機不因共享信箱存在就假設有鎖。

#### Scenario: Another machine reopens the task
- **WHEN** 計畫後另一台機器已更新任務並重開
- **THEN** 不用舊判定覆寫新狀態，保留衝突或依最新證據重新判定。

### Requirement: Existing hygiene integration is quiet and source-specific
能力 SHALL 接既有 Vault Hygiene，不新增排程；先確認排程實際載入規則與版本，不因 tidy source 已更新就宣稱排程生效。只回報歸檔/保留數量及需人類判斷的例外，unchanged 不足或拒絕項不反覆催。判定依來源 revision 與 gate version 失效，不只 mtime。

#### Scenario: Gate changes without note modification
- **WHEN** 原筆記未改但 gate 已更新
- **THEN** 相關舊判定可窄範圍重審，不永遠沿用錯誤結論。

### Requirement: All task readers use the same effective view
next、tasks、triage SHALL 依 task-index-contract.md 讀取同一正式索引與已核准未整合申請。未知與衝突 MUST 另列，不隱藏、不當作已完成，也不依舊原文重開已歸檔事項。

#### Scenario: Gate evidence becomes insufficient
- **WHEN** gate 改版但完成證據不足
- **THEN** 歸檔事項另列「狀態未確認」，不自動重開或消失。

### Requirement: Interactive restore writes an approved request only
互動式 tidy task SHALL 預設只提案，MUST NOT 修改正式索引。具體取回經使用者核准後可新增不可變申請；有效視圖即時標為待辦且待整合，正式索引仍由指定 Hygiene owner 更新。

#### Scenario: Approved restore before scheduled integration
- **WHEN** 核准申請有效，排程尚未執行
- **THEN** 三個讀取入口立即看見同一待整合待辦，不宣稱正式索引已更新。

### Requirement: Restore ordering is revision based
申請及 receipt SHALL 依 request identity、payload digest、task revision、source digest 與可核對授權套用，不以最新時間或同步到達順序決定。applied_requests MUST 防止 receipt 晚到造成重複套用。

#### Scenario: Later archive supersedes an older request
- **WHEN** 任務在申請後已有新 revision 的有效歸檔
- **THEN** 舊申請不得重開任務，衝突或未確認另列。

#### Scenario: Index and receipt arrive separately
- **WHEN** 同步只先到達索引或 receipt
- **THEN** 不重複套用、不靜默漏項，對不一致資料明列未確認。

### Requirement: Authority is durable and deployment starts read-only
自動寫入 SHALL 要求實體、有 provenance、可撤銷且涵蓋 scope/operation/owner/schema/gate 的常設授權；缺失或撤銷 MUST 唯讀。首次部署 MUST 先交付一次 readonly dry-run，另外核准後才開放寫入；本規格不是該授權。

#### Scenario: Existing metadata authority only
- **WHEN** 排程只獲准寫 metadata ledger 與報告
- **THEN** 不寫任務索引或取回整合 receipt。

### Requirement: Restore approval is individually recorded and immutable
核准紀錄 SHALL 依乙案存於 `{research}/tidy/tasks/restore-approvals/<approval-id>.json`，包含 schema、approval/request/task identity、request digest、operation、核准時間、對話或 session 來源及記錄 agent/machine。每次新增，不修改原紀錄；共用 CLI 核對紀錄與申請內容。MUST 明示程式只能確認紀錄相符，不能證明使用者真的核准，agent 在寫入時仍須照實記錄。

#### Scenario: Request changed after approval
- **WHEN** 申請內容改變或缺少相符核准紀錄
- **THEN** 不當作已核准，不產生取回效果。

### Requirement: Active work is not subject to archival freshness removal
active 任務 SHALL 在 assessment 未確認或歸檔 gate 升版時仍列 active；source 變動只附標記與來源，不將進行中的清單清空。Claude/Codex MUST 呼叫同一共用唯讀 CLI，不各自重寫驗證演算法。

#### Scenario: Archival gate upgraded during active work
- **WHEN** active 任務遇到 gate 升版
- **THEN** 待辦仍可見，不誤降成只有未確認。

### Requirement: Restoration reasons are evidence not automatic error labels
取回 SHALL 區分歸檔錯誤、需求改變、重新開工及原因未知，保留原 gate/operation/category 的可取得來源。dream-RSI MUST NOT 把所有取回直接當成歸檔錯誤，或用取回數單獨宣稱錯誤率。

#### Scenario: User expands previously completed scope
- **WHEN** 取回是新增需求而非原 gate 判錯
- **THEN** 記為 scope_changed，不當成原規則失敗。
