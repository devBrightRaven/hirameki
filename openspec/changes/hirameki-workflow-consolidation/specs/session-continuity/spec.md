## Purpose

以可查證的有效狀態協助使用者接續與收尾，保留必要決策與接手脈絡，避免舊待辦反覆出現及已在 spec 保存的理由被重新抄成多份紀錄。

## ADDED Requirements

### Requirement: Exclusive creation for authorized minimal candidates
明示常設候選保存授權下的新建候選 SHALL 使用既有 exact-append helper 的獨占建立模式，凍結完整 UTF-8 草稿與計畫後才 apply；準備階段不得建立 Vault 目標。目標必須位於已選定且存在的資料夾，MUST NOT 覆寫碰撞、連結或未知狀態。僅 fsync 與完整讀回相符才回 created 收據，包含目標、計畫、草稿與結果 hash；收據不證明跨機同步、事件去重或下游接收。既有追加計畫保持相容。

#### Scenario: Another writer creates the target after preparation
- **WHEN** 準備後、apply 前，另一 writer 建立相同目標，即使內容相同
- **THEN** 拒絕建立且保留原 bytes，不將相同內容推定為本操作先前成功。

#### Scenario: New note has uncertain readback
- **WHEN** 已開始建立或寫入，但寫入、fsync 或讀回失敗
- **THEN** 標 write_unverified，停止受影響批次；不自動刪除、覆寫或重試，不能宣稱 saved。

### Requirement: Contextual microlearning without task interruption
微學習 SHALL 取材自當前工作中有來源的概念、取捨或已驗證教訓，每次最多提出一個短片段，包含概念、當前例子及可選的下次應用。SHALL 在自然完成節點呈現，不要求使用者答題或開新學習任務。高負荷工作中 MUST 延後到收尾；沒有新價值或使用者要求安靜時不呈現，不以每輪配額產生內容。一次片段不是已學會的證據。

#### Scenario: Useful concept after completed work
- **WHEN** 工作已完成一個自然節點，且有可追溯、尚未重複呈現的相關概念
- **THEN** 最多提供一個簡短片段並連結當前例子；不增加批准或答題停點。

#### Scenario: User is concentrating or declines learning
- **WHEN** 使用者正在大型改動、排錯，或明示本輪不需學習提醒
- **THEN** 不插入教學；可在原候選草稿保留待整理線索，但未獲保存授權不持久寫入。

### Requirement: Evidence-based learning map and optional review
學習地圖 SHALL 使用既有選定 Vault 的知識紀錄與來源連結，不新增私人 runtime 學習正本。片段須區分已呈現、使用者自評、實際應用證據與未知；MUST NOT 由閱讀、沉默、重複次數或 agent 推論標為已掌握。相同概念優先連回既有紀錄；有新例子或反例才提追加。回顧 SHALL 在使用者要求或自然收尾提供可選的一個應用問題，允許略過，不新增排程、評分或強制複習。

#### Scenario: Repeated concept without new evidence
- **WHEN** 同一概念已呈現，沒有新例子、反例或使用者回顧要求
- **THEN** 不重複教學、不新建紀錄，也不增加掌握程度。

#### Scenario: Later independent application
- **WHEN** 後續工作中有可定位的概念應用結果
- **THEN** 將其視為應用證據候選，保留結果與限制，依既有保存 gate 提追加；不推論全面掌握。

### Requirement: Bounded post-deployment observation
部署後觀察 SHALL 由核准部署後的首個實際 session 起算七日或十個有相關機會的 session，以先到者為檢查點；沒有機會不計成功樣本。SHALL 分側記錄來源版本、已載入證據、機會、提醒、保存收據、拒絕／衝突與使用者回饋的最小摘要，不收原始對話。任何未授權寫入、錯誤 Vault、覆寫、重複套用或錯稱保存均為失敗，停止受影響寫入並提出修正；一般漏提醒記為未達成，不以其他成功抵銷。零樣本、未知載入或未部署 MUST 保持未驗證，不宣稱學習增益或普遍可靠。

#### Scenario: Observation window has no eligible session
- **WHEN** 七日檢查點到達但沒有符合條件的實際 session
- **THEN** 報樣本為零、行為未驗證，不將無錯誤當成成功；後續觀察安排由使用者決定。

#### Scenario: Save receipt contradicts reported success
- **WHEN** 工作流宣稱 saved，但沒有可定位的成功讀回收據或收據與目標不符
- **THEN** 該項驗收失敗，保留未知寫入狀態，停止受影響批次並查證，不自動重試。

### Requirement: Current state outranks repetition
next SHALL 依相關 handoff、明示決策及實際結果判定待辦；頻率、mtime、未見 Done MUST NOT 單獨證明優先級、拖延或尚未完成。

#### Scenario: Repeated task was withdrawn
- **WHEN** 舊 wrap 多次列一個待辦，後續證據明示撤回
- **THEN** 不再列有效待辦，能指出撤回來源。

#### Scenario: Incomplete evidence
- **WHEN** 只有檔案更新紀錄而無完成證據
- **THEN** 標進度未確認，不宣稱完成或未執行。

### Requirement: Selective closing with one shared collection
triage SHALL 收集一次 session context 並對照相關已保存 baseline；只提有新增價值的 wrap/journal/handoff/lesson/decision 保存候選，計畫行 MUST 不增加確認停點。

#### Scenario: Progress only
- **WHEN** 只有尚未保存的新進度
- **THEN** 直接展示 wrap 草稿，其他產物附簡短略過理由，不先問 yes。

#### Scenario: No new value
- **WHEN** 所有 relevant facts 已有來源保存且無新更正
- **THEN** 安靜結束或短句回報，零文件寫入。

#### Scenario: Existing specification
- **WHEN** 判斷理由已在具名 spec，沒有實質判斷更新
- **THEN** 必要摘要引用 spec，不另生重複 journal。

### Requirement: Preserve decision formation and lifecycle
Hirameki SHALL 區分 unresolved/forming/decided/reviewing 與 node active/superseded/closed；只有使用者明示選擇且通過既有晉升門檻才可提決策 node，保存依 decision-trace 契約。

#### Scenario: Emerging preference
- **WHEN** 使用者仍在比較且只表達傾向
- **THEN** 標形成中，不保存 active 決策 node。

#### Scenario: Confirmed decision changes
- **WHEN** 使用者確認取代一個現有決策
- **THEN** 展示新舊節點、相互連結及精確狀態變更，等待適用的保存授權。

### Requirement: Handoff preserves actionable ownership
handoff 候選 SHALL 只在跨 session 接手存在具體缺口時提出，包含相關 source revision、dirty ownership、未完成背景工作、首個步驟與驗收限制；可由原文連結補足資訊。

#### Scenario: Real pickup needed
- **WHEN** 工作未完成且下一個 session 需要陷阱與程序狀態
- **THEN** 提 handoff 並記查證時間，不沿用未驗證 PID。

### Requirement: Decision context proposal conditions and provenance
decision-trace SHALL 在已載入契約且模型辨識到方向定案、重要異議撤回、證據推翻原判斷或決策被取代時，沿用既有 Promotion gate 判斷候選價值，不依賴 triage、不另設重要性門檻。本契約只規定提出條件及保存、來源、狀態、去重與授權，不提供任何觸發機制。主動提示 MUST 只用一句有來源的話，不中斷工作、不追問；使用者要求展開時才呈現完整草稿。完整候選 MUST 記錄問題、選項、依據與未知、取捨及放棄項、決策 owner、實際決定與狀態、重開條件及原始證據連結。未知欄位明標未知，不為填滿格式虛構。未授權不寫入、不新增 hook，保存及 node 晉升仍依既有契約。

#### Scenario: Decision between closing sessions
- **WHEN** 使用者明示選定重要方向，但本輪未呼叫 triage
- **THEN** 通過既有 Promotion gate 時只用一句有來源的候選提示並繼續當前工作，不追問、不自行展開完整草稿；未取得適用保存授權前不寫入。

#### Scenario: Agents agree without user ruling
- **WHEN** 兩個 agent 合意或其中一方撤回重要異議，使用者尚未核准方案
- **THEN** 記為討論進展或形成中候選，不能宣稱使用者裁示或建立 active 決策 node。

#### Scenario: Evidence overturns an earlier conclusion
- **WHEN** 新證據推翻已記錄的判斷，但尚未決定替代方案
- **THEN** 提出有新舊來源及未知的重新評估中的討論階段，不將 reviewing/review 當節點狀態，不自行選定替代方案或修改舊 node。

### Requirement: Standing reminders and record operations have separate routing
普通工作中的決策提醒 SHALL 由各 runtime 的已載入 personal-layer 常駐規則處理，不依賴先叫用 Hirameki、不新增 hook，技能 description 僅供能力探索。一般證據查核不強制載入 decision-trace；在提議任何具體紀錄操作前 MUST 先讀其契約。常駐提醒只在明示定案、符合既有 Promotion gate、尚未保存時，完成工作後用一句有來源的直述句提出，不追問、不展開草稿、不重複提醒；契約詳情保持 on-demand，不在常駐層複製。

#### Scenario: Decision embedded in implementation request
- **WHEN** 使用者同時明示定案及要求繼續工作，且常駐規則已載入
- **THEN** 完成工作後才附一句可記錄提示，不停工或先要求保存確認；環境拒絕工作時記為基礎設施失敗，不能宣稱完整驗收通過。

#### Scenario: Ordinary check proposes invalid record state
- **WHEN** 原本一般查核將轉為提議改決策紀錄狀態
- **THEN** 提案前載入契約，只使用合法 node 狀態；若未提出紀錄操作，該次不能證明此讀取門檻已通過。

#### Scenario: Closing after a saved decision
- **WHEN** 決策理由已保存於 spec 或決策紀錄，稍後呼叫 triage 且無新增判斷
- **THEN** 只連結既有來源並檢查漏記，不再生成重複決策正文。
