## Purpose

把資料歷史、關聯、矛盾、機會與概念晉升整合為有來源的探索服務，讓使用者直接問問題，同時避免固定階段、虛構關聯與沒有確認的筆記寫入。

## ADDED Requirements

### Requirement: Question selects exploration
lens SHALL 按主題選歷史、關聯、主張查核、機會或模式分析；顯示範圍及來源限制，MUST NOT 固定全套或為缺資料編造關聯。

#### Scenario: Two unrelated topics
- **WHEN** 讀取的資料不支持兩題之間有關係
- **THEN** 回報未找到支持；假說若提出須與已觀察事實分開。

#### Scenario: History only
- **WHEN** 問某想法何時形成
- **THEN** 交付可回查時間線，不額外列七類機會或固定四份檔案。

### Requirement: Graduating cards uses one contract
概念卡晉升 SHALL 沿用 atomic claim、來源、既有 card 查重與確認契約，harvest/graduate/lens 不得各自保存不同版本的同一 claim。

#### Scenario: Existing card covers claim
- **WHEN** 候選已被既有 card 完整涵蓋
- **THEN** 指出該 card 並不另建重複卡；只有明示新差異才提更新。

#### Scenario: Card save was not requested
- **WHEN** 探索找到成熟 claim 但使用者只要求分析
- **THEN** 可提候選，不建目錄、卡片或改 MOC。

### Requirement: One coherent exploration result
lens SHALL 交付一份整合回答，必要的來源、矛盾、未知與值得保存候選可追查；持久產物僅依需要提出。

#### Scenario: Multiple useful perspectives
- **WHEN** 歷史與反例一起改變理解
- **THEN** 在同一回答呈現關係，不能只拼接四份重複報告。

### Requirement: Repeated lessons prompt manual graduation
同一可重用教訓在兩個以上獨立來源事件出現時，triage 或 tidy review SHALL 簡短提示可人工晉升概念卡；同一事件的重複副本不得湊次數，提示須查既有卡與先前選擇，MUST NOT 自動寫卡。

#### Scenario: Lesson repeated across independent events
- **WHEN** 兩次獨立事件支持同一教訓且沒有既有卡涵蓋
- **THEN** 提一次來源錨定的升卡提示，使用者選擇後沿用共用 card 草稿及保存契約。

#### Scenario: Duplicate report of one event
- **WHEN** 兩個 agent 各記同一事件
- **THEN** 視為一次證據，不因此觸發第二次事件的升卡提示。
