# Proposal

## Why

Hirameki 的 21 個指令讓使用者必須記住內部分工；lens、compose 等編排又重複子流程。2.1 的 triage 已示範按缺口選產物，但決策保存、歷史 corrections 整理與改善結果仍未形成一致契約。本次收斂入口並建立有來源、可恢復、可追蹤結果的工作流。

## What Changes

- 主要入口收斂為 next（接續）、lens（探索）、compose（創作）、decision-trace（決策脈絡）、triage（收尾），可用自然語言選擇所需能力。
- decision-trace 在重要決策形成或改變時提出有來源的脈絡候選，不依賴 triage 頻率；agent-comms 保留原始討論，triage 只檢查漏記並連結既有決策。
- 保留 tidy、mekiki、init 等專用入口。tidy 承接歷史 corrections/lessons 整理；triage 自動審查增量候選。
- **BREAKING**：退役 reflect、frame、critique、harvest、graduate、arc、bridge、challenge、tasks、pulse 的主要入口，提供一個發布版本的轉向期；能力按下述契約保留、重設或明確移除，不能只改名字。
- wrap、journal、handoff 保留可直接叫用的非主要捷徑，共用 triage 的能力契約，支援 session 中途紀錄而不跑整個收尾。graduate 保留重複教訓的人工晉升提示；critique 的獨立審查接各 runtime 既有通道。
- **BREAKING**：移除 next lucky、固定 lens 四階段、compose 先寫後判值、frame 通用 KILL 裁判及 critique 固定三模型平均分流程。
- 使用共用能力契約及按需 reference，避免平行正文。保留來源文件位置，以連結與精簡索引呈現 trace，不新增每次必生的巨型 trace 文件。
- 審查自動化止於候選檢查與具體提案；保存、規則修改、決策 lifecycle、部署仍各依授權處理。
- 定義跨 agent 去重、候選審查狀態、部分寫入恢復、改善結果接回及可獨立使用的 dream-RSI 資料接口。

## Capabilities

新增 tidy 任務收斂：以完成證據及未結依賴 gate 自動可逆歸檔，接既有 Vault Hygiene；實際執行仍須批准常設授權範圍，本次只編寫規格與唯讀盤點。

### New Capabilities

首次建立 OpenSpec baseline；下列為現行能力與變更後契約的完整描述，不宣稱全部是新功能。

- `workflow-routing`: 五入口、自然語言路由、專用入口、共用契約及按需載入。
- `task-archival`: 任務證據 gate、常設授權、可逆歸檔及既有 Hygiene integration。
- `session-continuity`: 接續、待辦狀態、進度查證、選擇性收尾與決策保存。
- `knowledge-exploration`: 有範圍的探索、歷史/關聯/反駁、機會辨識及概念卡晉升。
- `creation-workflow`: 作者材料、作品目的、按需寫作/審稿、外部技能邊界。
- `review-governance`: tidy 歷史整理、triage 增量審查、候選去重與規則修改提案。
- `evidence-and-recovery`: trace、授權、跨 agent ownership、寫入失敗及重試。
- `improvement-exchange`: 改善假說與結果回覆，包含可選 dream-RSI 交接。
- `migration-and-acceptance`: 入口遷移、consumer 盤點、兩側部署及分層驗收。

### Modified Capabilities

無既有 OpenSpec capability。早期 decision-trace 設計仍是 baseline 證據；不可將本草案視為已取代發布版。

## Impact

影響 commands/、skills/decision-trace/、codex/skills/hirameki/、相關 tests、README/使用說明及已有 consumer；實際修改清單由遷移盤點決定。hooks 必須列入相容檢查，但不因本案新增 hook。五入口不自動降低模型或增加委派。

目前授權只包含規格編寫、討論、唯讀盤點及 OpenSpec CLI 更新。本文是待審設計：Claude 的 1519 審查與 1527 更正已納入，範圍拆分異議已撤回；退役清單仍待使用者裁定，實作/部署/commit/push/release/archive 均未授權。規格詳盡與 strict 通過不代表行為通過。
