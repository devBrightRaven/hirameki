## Purpose

讓歷史與新增的更正及教訓可被整理、去重、審查與提出規則改善，同時保留當時證據，避免反覆提醒、以過期判定阻擋重審，以及未確認內容晉升成規則。

## ADDED Requirements

### Requirement: Historical review supports heterogeneous sources
tidy review SHALL 讀 corrections 的實際段落及 lessons，不只相信 frontmatter count；辨識不同標題、空段、追加段與衝突副本，保留來源及衝突。

#### Scenario: Syncthing conflict differs
- **WHEN** 同一 note 有內容不同的 sync-conflict 副本
- **THEN** 列衝突及來源，不刪檔、不任選較新者、不重複當獨立事件。

#### Scenario: Count is inaccurate
- **WHEN** corrections: 0 但追加段有具體更正
- **THEN** 該更正仍成候選，指出 count 不一致；不自行修原文。

### Requirement: Review classification preserves scope
候選 SHALL 分為 covered、duplicate/merge、proposable、task-only、superseded/expired、needs-evidence，並帶 task/project/personal/shared/unknown scope；候選合併依來源事件與語意，MUST 不把單次要求推成長期偏好。

#### Scenario: One-off formatting request
- **WHEN** 更正只明示這次文件使用一個格式
- **THEN** 分 task-only，不提全局永久規則。

### Requirement: Review revisions invalidate stale results
審查 SHALL 依來源內容 revision、review contract version 與相關 target rule digest 決定新舊；mtime 相同不能使舊結果永遠有效。

#### Scenario: Rules change without note edit
- **WHEN** 原 note mtime 未變但目標規則已更新
- **THEN** 相關舊 review 標 stale 並窄範圍重審。

### Requirement: Incremental review is automatic and quiet
triage SHALL 自動比對本次新增或已達明示重開條件的候選，只呈現成熟且未涵蓋提案；完整歷史整理交 tidy，審查不得以寫入索引為默認權限。

#### Scenario: Candidate already covered
- **WHEN** 本次更正已存在適用規則且無新差異
- **THEN** 不重複提案、不全掃歷史、不新增 lesson 湊紀錄。

#### Scenario: Rejected unchanged proposal
- **WHEN** 候選已拒絕且來源/相關規則沒有實質新證據
- **THEN** 不在下一次 triage 再催。

#### Scenario: Deferred without a due date
- **WHEN** 使用者選稍後但未設定日期或事件
- **THEN** 保持 deferred，只有明確重審或新證據才再次呈現。

### Requirement: Concrete proposals and separate authority
提案 SHALL 顯示來源、scope、target、原文/新文與理由，可 ADD/UPDATE/NARROW/EXCEPTION/WITHDRAW/KEEP；MUST 依使用者明示接受的項目才修改規則，保存 note 不授權規則修改。

#### Scenario: Lesson saved only
- **WHEN** 使用者 save all 保存收尾草稿
- **THEN** 不套用任何規則 diff，也不 commit/deploy。

### Requirement: Retain historical records
整理 SHALL 保留原 corrections 與 lessons，連結到審查結果；不得將全部 corrections 重寫成 lesson，未批准持久化時只交付讀取結果。

#### Scenario: Read-only full review
- **WHEN** 使用者只要求全面盤點
- **THEN** 原 note、rule 與 review records 均無寫入，候選數及覆蓋範圍如實報告。
