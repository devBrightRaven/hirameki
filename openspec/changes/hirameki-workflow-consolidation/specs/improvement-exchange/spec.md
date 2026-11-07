## Purpose

提供可單獨使用、也可交接 dream-RSI 的改善資料與結果契約，讓假說和試驗能接回原始問題並決定維持、修正或撤回，而不把提案自動變成有效規則。

## ADDED Requirements

### Requirement: Per-machine collection has one consolidation owner
使用者選定此模式時，各 origin writer SHALL 在同一候選資料夾以明示 machine ID／唯一 candidate ID 新增自己的紀錄，只在 ownership 可確認時追加自己的筆記；MUST NOT 跨機改寫其他 origin 的來源。Candidate ID 與事件 identity 分開，離線副本可並存。單一指定 owner SHALL 在已授權整併筆記中只維護 ID／連結、去重理由、衝突、覆蓋限制、saved／presented 狀態及建議行動，不複製來源正文；只有該 owner 統一發出批次改善提醒。不新增 store、鎖服務、背景喚醒或自動選主，owner handoff 必須明示。

#### Scenario: Same event collected offline on two machines
- **WHEN** 兩台離線各保存同來源同事件的候選，後續同步可見
- **THEN** 保留兩份來源不覆寫，整併 owner 將其連結為同一事件、只計一次；整併紀錄不冒稱原始候選已刪除或取得兩個獨立證據。

#### Scenario: New counterexample belongs to another origin
- **WHEN** 另一機台發現可追溯反例，原 note 不屬於自己
- **THEN** 不追加原 note；在自己的已授權範圍保存新證據並引用原 ID，由 owner 整理衝突，不改寫原結論。

#### Scenario: Consolidation owner or synchronization is unavailable
- **WHEN** 無已確認主責，或部分來源尚未同步／不可讀
- **THEN** 已授權 origin 收集可繼續，整併狀態標 pending／partial；不自動接管、不宣稱完整去重或重複發出改善批次。

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

### Requirement: Explicit adapter mapping preserves experiment context
與 `br-improvement/v1` 交換時 SHALL 保留該 closed schema 原樣；Hirameki 的 hypothesis、alternatives、unknowns、cost boundary 與實驗結果 MUST 留在被引用的原提案／結果，不擠入未知欄位或丟棄。Adapter SHALL 明列 identity、revision、來源 digest 及對應位置；缺失必要來源時回 needs-evidence，不自造值。部署結果的 verified MUST NOT 被解讀為改善效果已驗證。

#### Scenario: Accepted source change has only deployment evidence
- **WHEN** br-improvement/v1 結果是 accepted、implemented 且 deployment verified，但沒有 baseline/control、outcome 與效果證據
- **THEN** 可報具名目標部署完成，改善成效保持未驗；不得自動關閉原實驗。

#### Scenario: Candidate has unresolved assumptions
- **WHEN** Hirameki 候選仍有 unknowns 或沒有可追溯的證據 artifact
- **THEN** 保留原候選，不偽造 evidence hash 或 accepted 結果；可先整理草稿，交付成熟度與批准分開。

### Requirement: Offline proposals resume through verified remote state
離線或 GitHub 存取失敗時 SHALL 保留已授權保存的 Vault 候選，標為尚未查遠端或發布未確認，不阻塞主工作、不寫另一份候選正本。恢復後 SHALL 先查既有 issue／PR 與穩定候選 ID，再依當批發布授權追加或建立。逾時／丟失回應 MUST 視為可能已寫入；讀回查明前不得重送。無權存取不等於不存在。

#### Scenario: Create response was lost
- **WHEN** GitHub 建立或追加呼叫逾時，無法確認遠端結果
- **THEN** 保留 publication-unknown，先以原候選 ID 與目標 repo 查遠端；找到符合內容則引用，找不到但查詢不完整則仍 unknown，不盲目重送。

#### Scenario: Network remains unavailable
- **WHEN** 主動工作節點嘗試查詢失敗
- **THEN** 本節點停止遠端重試，保留候選與具體失敗；下次自然接續或使用者要求才重查，不自行建立輪詢、hook 或常設排程。

### Requirement: Cross-repository preflight preserves ownership
開始、接續或重新設計改善工作流前 SHALL 查相關 repo 的既有 issue／PR 內容、討論、scope、owner、裁定與未決事項，必要時查 closed／merged 記錄；同需求沿用原單與原 spec。跨 repo SHALL 各自核對並連結，不因追蹤而建空 PR。沒有 GitHub 機制標不適用，存取失敗標 unknown；owner 衝突只停止有衝突的修改，不接管其他 agent。

#### Scenario: Existing proposal spans repositories
- **WHEN** 共用能力已有產品 issue，consumer repo 只有薄 adapter 變更
- **THEN** 產品需求留原 issue；consumer 只有確有變更且發布獲授權時才建或更新相連交付單，不複製 tasks。

#### Scenario: Owner or remote state is unavailable
- **WHEN** 無法讀既有單或無法確認正在修改同一檔案的 owner
- **THEN** 記錄 unknown／ownership conflict，繼續獨立查核，不以搜尋失敗推定沒有既有設計。
