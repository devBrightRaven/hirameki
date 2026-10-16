## Purpose

以可查證的有效狀態協助使用者接續與收尾，保留必要決策與接手脈絡，避免舊待辦反覆出現及已在 spec 保存的理由被重新抄成多份紀錄。

## ADDED Requirements

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
