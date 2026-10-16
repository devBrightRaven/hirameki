## Purpose

確保進度、判斷、決策、教訓與改善狀態都有可回查證據，並在批次保存、跨 session 與跨 agent 工作中維持授權範圍、資料完整及可恢復性。

## ADDED Requirements

### Requirement: Evidence-backed trace
重要主張 SHALL 區分 observation/inference/assumption/preference/decision/outcome，提供來源與時間；只有 compaction 摘要時明寫其限制，不補造因果。

#### Scenario: Missing rationale
- **WHEN** 只剩摘要記錄某決策、沒有當時理由
- **THEN** 保存可知選擇與「理由未知」，不補一般最佳實踐當原始理由。

### Requirement: Separate save scopes
save this SHALL 只套用完整顯示的 current artifact；save all SHALL 僅含明示的 ordinary triage 草稿，不包含規則修改、decision lifecycle 或外部副作用；已有相同具體 session 授權須沿用。

#### Scenario: Superseding a decision during closing
- **WHEN** 使用者已 save all 而後提出取代舊決策
- **THEN** 顯示全部狀態變更並使用 decision-trace 專用保存 gate，不套用先前批次授權。

### Requirement: Partial save can resume without duplication
每次批次 SHALL 回報各項 written/not-written/failed/conflicted 與實際路徑；重試核對現有內容與 target revision，只補未完成項，有界 transient retry，持續失敗不能報完成。

#### Scenario: Second artifact fails
- **WHEN** wrap 已寫入而 journal 寫入失敗
- **THEN** 顯示兩者不同結果；重跑不再追加相同 wrap，不回滾其他已有資料。

#### Scenario: Changed destination
- **WHEN** 展示草稿後目標被另一 agent 修改
- **THEN** 該項標 conflict，重讀並更新提案，不能覆蓋或依舊 digest 寫入。

### Requirement: Shared identity and ownership
跨 agent 候選 SHALL 保持 proposal/evidence identity 與 revision，指定 owner 才套用；agent-comms 只運送不授權，runtime guidance 由各自 owner 部署。

#### Scenario: Concurrent agent proposals
- **WHEN** Claude/Codex 從同一事件提出同一改善但未確定 owner
- **THEN** 合併或連結來源，兩側只提案，不同時套用；不把 Syncthing 當分散式鎖。

### Requirement: Portable private boundaries
文件 SHALL 用 runtime-resolved vault keys 及相對 source 路徑，LF；runtime-local provenance 以 hash 識別，不複製 private memory、credentials 或其他 agent 設定進共享資料。

#### Scenario: Runtime-only evidence
- **WHEN** 改善來源是個人 runtime 檔
- **THEN** 共享紀錄記必要清理後主張與 hash，不送出完整私有檔。
