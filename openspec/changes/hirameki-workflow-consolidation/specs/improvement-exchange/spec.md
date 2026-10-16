## Purpose

提供可單獨使用、也可交接 dream-RSI 的改善資料與結果契約，讓假說和試驗能接回原始問題並決定維持、修正或撤回，而不把提案自動變成有效規則。

## ADDED Requirements

### Requirement: Improvement proposal envelope
交換 SHALL 包含 identity/revision、來源、scope、problem、hypothesis、alternatives、unknowns、acceptance、cost boundary、owner 與 review status；沒有 consumer 時 Hirameki 必須仍能獨立整理與提案。

#### Scenario: Dream service absent
- **WHEN** dream-RSI 未安裝或未接通
- **THEN** Hirameki 仍交付有來源候選，不阻塞 triage/tidy，不聲稱已交付實驗。

### Requirement: Experiment result links to tested revision
結果 SHALL 記 experiment identity、proposal/source revision、method、baseline/control、outcome、evidence 與 limitations；接受、套用與驗證有效須分開。

#### Scenario: Static check only
- **WHEN** 改技能後只有結構檢查通過
- **THEN** 可標 source checked，不能標自動路由有效或品質提升。

#### Scenario: Improvement fails in use
- **WHEN** 後續測試顯示採用修改沒有改善或造成回歸
- **THEN** 結果連回原提案並提維持/修正/撤回，原始假說與失敗證據保留。

### Requirement: Exploratory hypotheses remain hypotheses
dream-RSI SHALL 能提出新聯想，但來源缺口與反例須保留；任何假說 MUST NOT 自我授權修改技能或規則。

#### Scenario: Novel untested connection
- **WHEN** dream-RSI 提出尚無直接支持的改善方向
- **THEN** 標為待測假說，提出 observable experiment，不直接晉升規則。
