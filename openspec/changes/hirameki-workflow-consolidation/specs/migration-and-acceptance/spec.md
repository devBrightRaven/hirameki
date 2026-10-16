## Purpose

使入口退役與共用契約遷移有完整相容證據，兩個 runtime 各自能驗證來源、安裝與行為，並避免靜態成功、規格完成或單一題目被誤報為整體完成。

## ADDED Requirements

### Requirement: Explicit retirement and consumer migration
遷移 SHALL 列出全部 21 個現有 command、decision skill、Codex references、hooks、排程與文件 consumer 的承接/移除結果，退役入口一個發布版本轉向後才移除；wrap/journal/handoff 是保留的直接捷徑，不列入到期移除；現有 decisions/notes 不搬移或刪除。

#### Scenario: Old journal review call
- **WHEN** 使用者呼叫保留捷徑的 journal review
- **THEN** 路由到 tidy review 的同一能力契約，不執行平行舊正文，捷徑不因轉向期結束而失效。

#### Scenario: Stop reminder after migration
- **WHEN** Stop hook 或其他已知 consumer 顯示收尾提示
- **THEN** 提示指向可使用且契約一致的入口；證據附實際啟用狀態及提示，不只比對文字。

### Requirement: Evidence levels are separate
完成報告 SHALL 分 source/static、isolated behavior、fresh runtime routing、installed parity、cross-machine、real-use acceptance；任何缺口逐列呈現。

#### Scenario: Both runtimes not tested
- **WHEN** Claude 行為通過但 Codex 只有靜態檢查
- **THEN** 只宣稱 Claude 指定情境通過，不稱兩側完成。

### Requirement: Acceptance covers useful omission and failure
驗收 SHALL 覆蓋零產物、已有 spec、正反例路由、重跑去重、拒絕/延後、新證據重開、partial write、cross-agent ownership、用途差異與未驗證 evidence。

#### Scenario: Correct answer without routing
- **WHEN** 模型答對但測試要求的 specialized context 未讀取
- **THEN** 答案品質可另評，routing 不得標 PASS。

### Requirement: Release and cost claims require evidence
實作完成 SHALL 附相關測試與 diff，release/install/archive 依獨立授權；成本結論須同任務 baseline 與實際 usage，不因較少入口自稱 token 節省。

#### Scenario: Specification completed
- **WHEN** proposal/design/specs/tasks 已齊且 strict 通過
- **THEN** 只報規格結構完成，未執行的 tasks 仍未勾，不啟動 apply/archive。
