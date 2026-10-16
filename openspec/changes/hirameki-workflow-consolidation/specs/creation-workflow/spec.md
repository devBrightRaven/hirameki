## Purpose

將作者素材與創作目的連接到既有語言、來源保護及審稿能力，減少重複寫作規則，保持不同品牌與作品的獨立契約，也避免文學標準阻擋技術寫作。

## ADDED Requirements

### Requirement: Purpose determines creation criteria
compose SHALL 依作品目的選查重、受眾、證據、作者立場或敘事檢查，MUST NOT 以欠缺個人獨特性/情緒張力一律 KILL 技術文件。

#### Scenario: Useful engineering tutorial
- **WHEN** 技術教學有可驗證方法但沒有文學轉折
- **THEN** 依正確性與讀者用途處理，不因只是提供資訊而否決。

### Requirement: Supplied draft does not require precreation ritual
compose SHALL 尊重只改稿/只審查/大綱的請求；已有材料足夠時不額外掃整個 vault，也不先生成全文再判斷是否值得寫。

#### Scenario: Short English edit
- **WHEN** 使用者只要求保留引文與 URL 的一段英文編修
- **THEN** 使用相應 writing entry，保留 protected material，無 vault 全掃或發布。

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
