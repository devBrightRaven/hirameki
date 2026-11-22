## Purpose

將作者素材與創作目的連接到既有語言、來源保護及審稿能力，減少重複寫作規則，保持不同品牌與作品的獨立契約，也避免文學標準阻擋技術寫作。

## ADDED Requirements

### Requirement: Purpose determines creation criteria
compose SHALL 依作品目的選查重、受眾、證據、作者立場或敘事檢查，MUST NOT 以欠缺個人獨特性/情緒張力一律 KILL 技術文件。

#### Scenario: Useful engineering tutorial
- **WHEN** 技術教學有可驗證方法但沒有文學轉折
- **THEN** 依正確性與讀者用途處理，不因只是提供資訊而否決。

#### Scenario: Sufficient context for a sourced artifact
- **WHEN** 請求或前文已讓交付物、讀者與主題明確，來源在已授權範圍且有足夠材料
- **THEN** 直接提出或交付使用者要求的成果。可逆的小選擇可自行處理，對結果有影響的假設要說明。

#### Scenario: A missing decision changes the artifact
- **WHEN** 合理解讀會產生不同交付物、讀者、主題或來源範圍，前文無法排除
- **THEN** 在依賴該決定的搜尋或 Vault 設定讀取前，只問一個聚焦的交付問題。沿用答案與已確認範圍，直接進入下一個已授權步驟，保留原保存批准門檻。

#### Scenario: The user delegates the topic
- **WHEN** 使用者明確請代理在已限定的材料中選主題，交付物與讀者已知
- **THEN** 選一個有來源支撐的主題並直接交付所需成果，說明影響結果的假設。維持已授權的搜尋及讀寫範圍。

#### Scenario: A short answer resolves the pending audience
- **WHEN** 使用者以簡短回覆選定仍待確認的讀者，原創作請求仍有效
- **THEN** 接回原創作請求，沿用材料範圍與保存／發布限制，完成下一個已授權步驟。無須使用者重述需求或指定工作流名稱。

### Requirement: Supplied draft does not require precreation ritual
compose SHALL 尊重只改稿/只審查/大綱的請求；已有材料足夠時不額外掃整個 vault，也不先生成全文再判斷是否值得寫。

#### Scenario: Short English edit
- **WHEN** 使用者只要求保留引文與 URL 的一段英文編修
- **THEN** 使用相應 writing entry，保留 protected material，無 vault 全掃或發布。

#### Scenario: Review only the technical behavior
- **WHEN** 使用者提供技術稿，只要求檢查可重現性與證據
- **THEN** 依指定項目交付審閱結果，寫作技能留給文稿產製、編修或語言審閱。只有在明確要求或適用契約規定時才走獨立審查。

### Requirement: Authorship and brand remain explicit
作者立場 SHALL 有 supplied/vault provenance；品牌、council、Ravenquill 及專案發布契約僅依明確要求或已批准契約接入，身份相同不代表語氣相同。

#### Scenario: Unsupported personal anecdote
- **WHEN** 作者材料缺少真實場景
- **THEN** 不編造生活經驗，標缺口並完成有依據的部分。

#### Scenario: Technical blog and brand
- **WHEN** 撰寫作者個人技術文章但未要求其另一創作品牌的檢查
- **THEN** 不自動套另一品牌的語氣或規則。

### Requirement: Independent review is an explicit option
compose SHALL 將明確要求的獨立審查路由到各 runtime 既有管道，記錄實際 reviewer/模型證據與分歧；MUST NOT 另建重複審查管道、將角色視角模擬當獨立模型或把平均分當可靠共識。

#### Scenario: Reviewer unavailable
- **WHEN** 授權的外部 reviewer 無法執行
- **THEN** 說明缺少可用結果，不能改標多模型通過。
