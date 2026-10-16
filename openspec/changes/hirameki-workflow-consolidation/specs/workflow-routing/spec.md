## Purpose

讓使用者依接續、探索、創作與收尾目的呼叫 Hirameki，由共用能力按需工作，減少記指令與重複載入，同時保持專用工具與各 runtime 的清楚邊界。

## ADDED Requirements

### Requirement: Five purpose-based entries
Hirameki SHALL 提供 next、lens、compose、decision-trace、triage 五個主要入口，並將明確自然語言目的映射到同一契約；必要的實質歧義 MUST 明說，單純機械情況直接處理。

#### Scenario: Natural continuation request
- **WHEN** 使用者要求接續具名專案
- **THEN** 使用 next 契約，保留該專案範圍，不額外執行探索或創作。

#### Scenario: Mechanical action is not a decision
- **WHEN** 使用者只要求修改一個明示 typo
- **THEN** 不因存在選擇文字而啟動 decision-trace 或全套 Hirameki。

### Requirement: Shared capability contract
同一能力 SHALL 有一份 canonical 行為契約，runtime adapter MUST 僅處理其工具、設定及來源標記差異，按需載入必要 context。

#### Scenario: One narrow exploration
- **WHEN** 使用者只問某概念的演變
- **THEN** 載入其歷史分析所需 context，不載入其他三個探索流程或完整 writing council。

### Requirement: Specialized entries remain available
tidy、mekiki、init SHALL 保留明確用途；全面維護、多模型審查及外部研究 MUST NOT 隨五入口隱含啟動。

#### Scenario: Ordinary session closing
- **WHEN** 使用者要求 triage
- **THEN** 不初始化 vault、不跑全面 tidy、不呼叫外部審查 CLI。

### Requirement: Direct recording shortcuts remain available
wrap、journal、handoff SHALL 保留非主要清單的直接捷徑，共用能力契約，不能強迫單筆紀錄先跑完整 triage；隱藏方式 MUST 依各 runtime 實測，不能假設 metadata 欄位有效。

#### Scenario: Mid-session progress capture
- **WHEN** 使用者做完一項工作後直接呼叫 wrap，準備接著做下一項
- **THEN** 只提供該筆進度草稿與適用保存動作，不進整套收尾或轉向失效入口。
