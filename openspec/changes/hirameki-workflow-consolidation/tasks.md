# Tasks

2026-10-01 使用者授權接續 tidy source 工作；真實任務歸檔、runtime/排程部署及發布外部行動仍需各自授權。未勾不等於基礎設施失敗，all_done 不可由規格齊全推得。每階段先完成其受影響契約與驗收，再進下一階段。

## 1. Review and baseline

- [ ] 1.1 核對已納入的 Claude 1519/1527 審查與後續異議；交付逐項採納/未採納及使用者裁決，驗證退役、保留捷徑及權限同時反映於全部 artifacts。
- [ ] 1.2 盤點 21 commands、decision skill、Codex references、hooks、排程及文件 consumer；交付每個來源的承接與現有啟用證據，未知不報不存在。
- [ ] 1.3 定位 dream-RSI canonical 與接口；比對 improvement-exchange 並記相容/差異，不執行未授權服務。
- [ ] 1.4 tidy 歷史 read-only baseline：從頭到尾讀歷史紀錄，逐條抽取 corrections/lessons、辨衝突及去重；交付完整覆蓋、候選數量/型態與來源分類，再依數據定最小存法，原筆記 hash 不變，盤點期間不寫任何檔案。

- [ ] 1.5 確認 Hygiene 實際 consumer、source/installed 規則及執行權限；對歷史任務建立 identity/完成條件/證據/未結依賴分類，不能以結構掃描數字宣稱逐項審查完成。

## 2. Shared routing and continuity

- [ ] 2.1 建立共用契約與五入口路由，適配 Claude/Codex；以明確/自然語言正反例驗證 actual reference loading 與按需讀取，補相應使用說明。
- [ ] 2.2 next 承接有效待辦/卡點；用完成、撤回、取代、mtime-only fixture 驗證不重撈失效待辦，不以次數推拖延。
- [ ] 2.3 triage 選擇性產物、保留直接捷徑與 decision lifecycle；驗證 plan 無新停點、mid-session wrap、zero artifact、existing spec、forming/decided 與 save scopes，更新文件。
- [ ] 2.4 decision-trace 決策脈絡的提出條件與雙側驗收；用共用隔離 fixture（既有 active node、mailbox 範例、spec）測未 triage 的定案、agent 合意、異議撤回、新證據推翻、已保存理由及 typo。各情境兩次、同側同模型/effort 有無契約對照；驗證 Promotion gate、一句提示不中斷不追問、未授權不寫入、不改舊 node，分別報行為/實際載入/增益，記 source/fixture hashes、完整輸入輸出與工具紀錄、個人層及模型可確認限制。額度未授權不執行，不新增 hook、不宣稱少量測試代表普遍可靠。

## 3. Exploration and creation

- [ ] 3.1 lens 問題導向探索與共用 card flow；驗證無支持關聯不虛構、窄題不跑全套、已有卡不重建、兩獨立事件提示升卡而同事件副本不觸發、不保存時 vault 不變，更新文件。
- [ ] 3.2 compose 按用途接 writing entries；以技術教學/散文/short edit/unsupported anecdote/brand-negative cases 驗證，不硬套 KILL 或外部 council，更新文件。
- [ ] 3.3 critique 承接各 runtime 既有 explicit independent review 管道；驗證 unavailable reviewer、actual model identity 與分歧保留，不報固定平均共識，不另建一套。

## 4. Review records and recovery

- [ ] 4.1 定最小 review record 序列化及 identity/revision；用重複事件、跨 agent、conflict file fixture 驗證與舊 notes 不變，記 schema。
- [ ] 4.2 tidy review 和 triage 增量審查共用契約；驗證 unchanged rejected/deferred 不重提、rule digest/contract version 變更可重審、成熟候選合併呈現。
- [ ] 4.3 授權分類、accepted/applied/verified 結果；驗證 save all 不改規則，精確 diff 核准只改所選 scope。
- [ ] 4.4 實作有界 retry/partial save/source conflict recovery；故障注入驗證第二項失敗後第一項不重複、變更 target 不被覆蓋，補恢復說明。

- [ ] 4.5 完成歷史盤點後定最小任務索引及可逆歸檔格式；固定 gate 驗證完成、部分完成、待部署、矛盾、重開、同 note 混合、source 變更、重跑、部分失敗及恢復；未取得常設範圍授權不得操作真實 vault。
- [ ] 4.6 接既有 Hygiene consumer 並驗證 source/installed/排程結果，不新增排程；去重摘要及 contract version 失效測試，驗收後另取得排程部署授權。
- [ ] 4.7 依 task-index-contract.md 實作三入口共同有效視圖；測核准申請即時生效、重送冪等、後續歸檔、receipt/index 分批到達與未確認另列。
- [ ] 4.8 常設授權位置交使用者裁定；測缺失／撤銷／版本與 scope 不符唯讀，首次部署先 readonly dry-run，不把 metadata 授權當 task 寫入授權。
- [ ] 4.9 Hygiene 後續寫入與三個 reader 共用 scripts/TASK_GATE_VERSION，缺失／空值／多行即停止該項，不內嵌另一份 gate 常數；本輪不修改 live 排程。

## 5. Improvement exchange

- [ ] 5.1 交付 proposal/result envelopes 與可獨立 fixture consumer；驗證無 dream-RSI 時正常、有 result 時接回 tested revision、假說不自動套用。
- [ ] 5.2 在取得 consumer 執行授權後做實際 dream-RSI 交換；來源、成本與實驗結果可查，未測則保留 live integration 未完成。

## 6. Migration and integration

- [ ] 6.1 安裝退役入口轉向期、保留直接捷徑與清 consumer 依賴；檢查 Stop 提示/手動捷徑仍可用、隱藏 metadata 實測、無平行正文，備份/回退清單可恢復。
- [ ] 6.2 跑 repo 必要檢查及兩 runtime 隔離 fresh dialogs；證據附 source digest、fixture hash、prompt、tool loading、method、model/effort 可確認部分及限制，不把 regex 當完整行為。
- [ ] 6.3 跨機確認共享候選去重及 ownership；真實併發與真實 sync 未測不得替代為普通雙程序 PASS。
- [ ] 6.4 用同任務 baseline 比對 read/call/time/可取得 token，保持品質標準；缺 usage 時只報可觀察成本，不估節省百分比。
- [ ] 6.5 得到 commit/push/release/deploy 授權後逐側交付；驗證 Git/source/generated/installed/fresh runtime，列所有未驗證行為；archive 僅在批准的驗收範圍完成後處理。
- [ ] 6.6 完成 design 第10節 tidy/triage/decision-trace 雙側矩陣；先驗證隔離讀寫，再按另行批准的額度跑 fresh dialogs，保留 BLOCKED/NOT-EXERCISED，不以另一側或靜態結果補成 PASS；實際保存、取代、失敗恢復不可只用提醒題替代。
- [ ] 6.7 task_view.py／task_view_cli.py 在 next/tasks/triage 實際接入及兩側驗收完成後，才加入 package files；此前 source/tests 留 repo，但不隨套件發布。提交前 npm test 必須包含兩份 task-view 測試，release test chain 同步，不以獨立指令取代 gate。
- [ ] 6.8 發布檢查涵蓋實際 marketplace/plugin payload：npm files 不是唯一控制點。repo scripts 一旦 commit 並發布可能隨 plugin 出貨，故未完成雙側驗收前不 commit/push/release 此批接入；不以「npm 未打包」宣稱 plugin 不會出貨。Codex plugin 根目錄目前為 codex/，shared scripts 不在該 payload，必須另驗證 source root 解析／實際交付，不能猜 cache 或沿用 Claude 變數。
