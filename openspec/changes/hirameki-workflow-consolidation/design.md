# Design

## Context

目前發布版 2.1.0、source HEAD b11d002；Claude 使用 commands，Codex 使用 umbrella skill 加 references。動機見 proposal.md。實際盤點為 21 個指令、355 篇 journal 根目錄 Markdown；歷史包含不同 Corrections 標題及 Syncthing 衝突副本。尚未逐條分析 corrections，不能將檔案數當候選數。

本文件是完整待審方案，供使用者與 Claude 檢查；章節中的 Decisions 是提案採用的設計選擇，沒有取代使用者裁決。本次只完成規格，不啟動 apply。

## Goals / Non-Goals

Goals：使用者以目的呼叫；一次取材、按需分析、保存有價值的差異；舊資料可整理，改善可連回結果；兩個 runtime 共享行為契約而各自保持設定與部署邊界。

Non-Goals：常駐索引服務、全庫逐回合掃描、全自動規則修改、強制多模型、公開發布、重設模型設定、重規劃 dream-RSI、把 vault 當 runtime configuration。沒有通用「最長 trace」或每次必生文件。

## Decisions

### 1. 入口與能力分離

五個主要入口為 next/lens/compose/decision-trace/triage。tidy/mekiki/init 為專用入口。wrap/journal/handoff 永久保留為非主要清單的直接捷徑，共用能力契約，不強迫中途記一筆也跑完整 triage。其餘退役命令只留一個發布版本的輕量轉向：告知承接入口，不執行舊正文、不再出現在主要目錄；具體版本號待發布裁決。舊名字轉向不視為新 decision aliases；既有 decision-trace 的名稱限制保留。Claude 隱藏欄位是否可降低清單預算須實測，Codex 原本 umbrella 不宣稱有同等節省。

決策脈絡的提出條件不依收尾頻率：模型在當輪已載入契約且辨識到方向定案、重要異議撤回、證據推翻原判斷或決策取代時，按既有 decision-trace Promotion gate 判斷是否值得提出候選，不另設重要性門檻。本契約不提供 hook 或背景觸發機制，也不保證自動路由。主動提示只用一句有來源的話，不中斷當前工作、不追問；使用者要求展開時才呈現完整草稿。候選記問題、選項、依據與未知、取捨及放棄項、決策 owner、實際決定與狀態、重開條件，連回 agent-comms 或其他原始證據。agent-comms 是討論與更正證據，不是決策摘要的第二正本；已有 spec 或決策紀錄時只補差異與連結。triage 檢查漏記，不重抄。未授權不寫入；Promotion gate 不將形成中候選晉升 active node，兩 agent 合意或撤回異議也不等於使用者核准。

| 舊能力 | 承接 | 保留/移除 |
|---|---|---|
| next, tasks, pulse week | next | 接續、待辦、卡點；修正狀態推論 |
| arc, bridge, challenge, harvest, graduate, pulse patterns, lens | lens | 題目導向探索、機會與卡片；取消固定全套 |
| reflect, frame, compose | compose | 作者材料、作品用途、查重/證據；取消通用 KILL 規則 |
| critique | compose 路由到各 runtime 既有審查通道 | 移除固定三模型及平均分，不另建一套 reviewer 管道 |
| wrap, journal, handoff | triage 與非主要直接捷徑 | 共用契約，保留中途直接紀錄與 merge 等操作 |
| journal review | tidy 或 triage | 歷史/增量審查同一契約 |
| pulse snapshot | tidy 的只讀盤點 | 不每次自動顯示數量 |
| next lucky | lens 的明確隨機探索要求 | 移除開工時附帶的星座流程 |

避免另加八個公開技能。按需 reference 的實際目錄結構由後續實作遵循 repo 模式；同一能力只有一份 repo canonical，Claude/Codex 生成或檢查其投影，適配層只記 runtime 差異。

### 2. 保存既有位置，以連結組成 trace

daily 保存進度摘要；journal 保存實質判斷與更正；journal/decisions 保存已確認且通過晉升的決策；journal/lessons 保存跨任務可重用教訓；handoff 保存接手缺口。spec、測試報告及原始證據保留原位置。相同事實引用來源，不複製敘事。統一 trace 是使用者能追查這些關係的結果，沒有每次都產生 trace.md 的要求。

替代方案：每輪巨型 trace 加其他文件投影。未採用，因 consumer 遷移、雙份敘事及長文件成本高；若 Claude 提出證據支持再審，不偷偷更改本方案。

### 3. 審查紀錄是人類知識層，沒有直接 runtime 載入

第一次 tidy review 全面抽取 corrections/lessons，保留原文及來源位置、原始 hash 與 LF hash。題意相同不代表事件相同：先按來源證據 identity 去重，再分組語意。衝突副本不刪、不因檔名認定重複；內容分歧標待人工處理。範圍為 task/project/personal/shared/unknown，待確認不晉升。

durable review records 的檔案數、存放位置與序列化是實作細節，不預設每個候選一個檔或新增 reviews 子目錄。先完成全部歷史紀錄的唯讀盤點，依候選數量、來源型態與同步衝突情況比較最小索引及分檔方案，再記錄選擇理由。必要語意為 identity、kind、sources、scope、content revision、classification、review state、owner、related proposal、最後依據 digest、重開條件與結果連結。只讀盤點不得建立檔案；實際儲存按 canonical vault keys 解析，新增紀錄仍需適用寫入授權。

狀態：unreviewed → covered / needs-evidence / proposed → accepted / rejected / deferred；accepted 另有 applied、verified、ineffective、withdrawn 等改善結果。接受不等於已套用，已套用不等於有效。新增修訂以事件追加；原 corrections 不改成 lessons，不抹除舊結論。

去重比對包括候選來源 revision、審查規則版本及目標規則 digest，不能只有 note mtime。任一變化使相關判定標 stale 並窄範圍重審。rejected 無新證據不催；deferred 附使用者約定日期或 observable trigger，未約定則需明確重審要求。待證據候選遇到新相關證據可重開。

替代方案：直接改所有舊 note frontmatter。未採用，避免歷史重寫、Syncthing 衝突及侵入各筆記格式。是否序列化成 Markdown 或 JSON 不影響對外契約，實作前定最小可重建形式即可。

### 4. triage 預設只讀，寫入權分開

triage 讀一次 session state、相關已保存 baseline 及有限 review records；草稿按新增價值提出。plan line 只提供資訊，不新增 yes 停點。save this 保存目前草稿；save all 只批次授權目前已明示範圍的進度/journal/handoff/lesson 草稿，後續全文仍顯示。選 all/+artifact 只改選擇。

決策 create/append/supersede/close 必須完整顯示所有受影響節點及狀態，用 decision-trace 既有 save this gate；save all 不包含它。原規則 diff 的接受只授權明示 target/scope 的修改，不隱含 commit、push、deploy、跨 agent 修改。使用者已在 session 給相同具體授權時沿用，不重問。

增量審查自動比對，但只有成熟新候選才顯示一份合併提案；新 lesson 若尚未保存，可討論 draft candidate，未獲保存授權不寫 review state。既有規則覆蓋且沒有可保存產物時可短句回報，不為標「已審」自動寫檔。

### 5. next、lens、compose 的界線

next 優先明示專案/最新相關 handoff/有效決策/已保存狀態；狀態不依單純日期或頻率。lens 先依主題檢索候選，再讀必要來源；如需較大掃描，顯示原因與實際覆蓋，不自動增加寫入。compose 先辨作品目的與人類材料，已有草稿直接處理；以對應 writing entry 輸出文字，只有 explicit/approved contract 才追加 Ravenquill/council/brand。不能承諾基礎寫作都要掃 vault。

### 6. 跨 agent 與寫入恢復

shared candidates 使用穩定 identity；agent-comms 運送同一提案與回覆，沒有修改權。指定 owner 在送出前讀最新狀態及 hash，來源變更則停止該項寫入並報衝突。兩 agent 同時持相同 revision 並非互斥證據；ownership 未確定時兩邊只提案，禁止承諾 Syncthing 提供鎖。

批次保存逐項結果與來源/target before/after digest。重試先確認現有內容是否已套用；只補未完成項。暫時故障有證據時有界重試一次，持續失敗回報位置；不全批 rollback 造成原文遺失。若 durable receipt 未獲授權，只在當前結果中列清單；跨 session 接續須讀目標本身驗證，不能依記憶猜已成功。

### 7. dream-RSI 與改善模組化

Hirameki 提供來源錨定的候選、重複事件、反例及 outcome links。交換 envelope：proposal identity/revision、source identities/hashes、scope、problem、hypothesis、alternatives、unknowns、acceptance、cost boundary、owner、review status。dream-RSI 回傳 experiment identity、tested revision、method、baseline/control、outcome、evidence、limitations、建議與關聯 proposal。

獨立使用 Hirameki 能完成整理/提案/結果記錄，不依賴 dream-RSI 安裝。dream-RSI 可提出超出既有錯誤的新假說，但需標為 hypothesis；不能自我核准寫規則。實際 consumer 尚未定位，live integration task 必須先核對其契約並另行授權。以下 specs 定義 producer/consumer interface，不宣稱目前服務已支援。

### 8. 成本與模型

不因叫入口就委派或固定多模型。沿用當前 runtime 與使用者模型設定。可在執行 handoff 建議較便宜模型與 effort，但要列任務、驗收與何時需要再判斷；不自動降模型。本次 spec authoring 使用主 thread。跨場景 baseline 以實際檔案讀取數、模型/tool calls、耗時、可取得的 token usage 比較，缺 token 數時不宣稱比例節省。

### 9. tidy 共用任務收斂實作方案

tidy 是 Hirameki 的共用能力，不是 Claude 或 Codex 私有規則。repo 保持一份 canonical 契約，commands 與 Codex references 生成或驗證等價投影；各 adapter 只接工具、權限、路徑解析及來源標記。Vault Hygiene 使用同一契約，不另寫完成清單或 gate。

流程為 discover → collect evidence → classify → validate gate → reversible archive → receipt。Agent 從既有文件抽取最小任務資料：identity、scope、completion criteria、outcome evidence/source revision、open dependencies、reopen evidence。完成 gate 逐項驗證條件已滿足、無未結責任、證據可追查、來源未變且操作位於常設授權範圍；模型信心不代替 gate。資訊不足先查既有來源，仍不足保留；矛盾只列需要人類判斷的例外，不逐項請使用者重填。

第一版優先維護有效待辦索引，保留原始筆記及結果來源，不搬整篇混合 note、不刪原文、不改已交付 agent-comms、不自動 archive OpenSpec 或整個專案。索引格式、位置、identity 與恢復資料在完整歷史盤點後定案，不先製造第二個全文正本。無完成條件的歷史項不因 checkbox 或日期自動歸檔。

操作前核對 source revision，來源改變則該項停止；receipt 保存證據、before/after revision、gate version、owner、operation 與恢復資訊。重跑須冪等，部分失敗只補未完成項，後續重開恢復有效待辦。多機共享資料不等於互斥；首版只指定一個 Hygiene 寫入 owner，其他機器/agent 可查核及提案。跨機寫入擴大前另驗證協調機制。

接入順序：唯讀歷史 baseline 及實際 consumer 定位 → 共用契約與固定 gate → 隔離歸檔/恢復驗收 → 兩側 adapter 驗收 → 明確常設來源/操作授權 → 小範圍 Hygiene 部署。排程輸出只列處理數與真正例外，相關來源或 gate version 改變才重審，不只看 mtime。本輪不取得上述執行或部署權限。

### 9A. 已採納補充與首版索引契約

2026-10-01 使用者採納取回申請及未確認另列方向。詳細格式見 `task-index-contract.md`，Claude 與 Codex 不得各自建立另一份狀態清單。

next/tasks/triage MUST 使用同一有效視圖：正式索引 + 有效且未整合的取回申請 + 狀態未確認／衝突事項。原筆記只能補脈絡或發現尚未索引的候選，不得把已有歸檔判定的舊文字再次當成待辦。來源或 gate 變更而證據不足時列「狀態未確認」，不自動復活，也不得藏起來。

互動式 tidy task 預設只判定與提案，不改正式索引；使用者核准具體取回後，只寫不可變申請。申請立即反映在有效視圖，標「取回申請待整合」。正式索引及整合 receipt 只有指定 Hygiene owner 可寫。申請不是第二份正式索引，排程整合前不得聲稱正式狀態已更新。

常設授權必須是可讀取、可撤銷的實體紀錄，包含來源範圍、允許操作、owner、schema/gate version、批准來源／日期、有效條件與撤銷方式。位置由使用者裁定，未指定、缺失、撤銷、版本或範圍不符均唯讀；本 spec 不建立實際授權。首次部署先交一次 readonly dry-run，再另行批准寫入，不逐項增加確認層。

append-only 不代表無衝突。取回依 request identity、task revision、核准來源及來源 digest 判定，不按最新時間覆蓋。申請後出現新的正式狀態、重開證據或來源變動，無法安全套用便列衝突；舊申請不得推翻較新的有效歸檔。receipt 綁定申請與整合 revision；索引已引用該申請時，receipt 晚到也不讓 overlay 再次生效。

metadata 與 task ledger 分開，既有 CSV/JSONL 不混為同一契約。Hygiene 提示詞只指定共用 tidy 契約、scope、上限與授權，不重寫完成 gate。實際排程修改及部署仍另行授權。

### 10. 兩側完整行為驗收與完成 gate

驗收矩陣必須分別列 Claude、Codex 的 source digest、fixture hash、prompt、實際工具/契約讀取、可確認 model/effort、結果及限制。每列區分 PASS、FAIL、BLOCKED、NOT-EXERCISED、NOT-RUN；測試未碰到條件不能算 PASS，基礎設施失敗不算行為失敗也不算通過。靜態綠、正確答案或另一側通過都不能取代本側實測。常駐規則不可觀察時明列推論，不假稱直接證明載入。

| 能力 | 必測行為 |
|---|---|
| tidy | 完成/部分完成/待部署/矛盾/重開；混合 note；來源變動；重跑；部分失敗；可逆恢復；無常設授權不執行 |
| triage | 有價值才提產物；零產物；無額外確認；直接捷徑；save this/save all 範圍；決策不混入普通批次；部分保存失敗、重試及目標變動 |
| decision-trace | 拍板＋工作實際完成＋末尾一句直述提示；無草稿/選單/追問/擅寫；具體紀錄提案前讀契約；合法 node 狀態；形成中不當裁示；保存/取代/關閉/重新評估及既有理由去重 |

已知狀態：Claude 常駐直述提醒有兩次指定情境結果，但不代表完整矩陣通過；Codex 兩次有提醒，工作受唯讀/執行政策阻擋，完整工作情境仍 BLOCKED；具體紀錄操作前載入 gate 曾未被實際考到，仍 NOT-EXERCISED。這些狀態須按原始證據更新，不能勾掉整套驗收。先以無模型的方式確認隔離可讀寫及 fixture 邊界，再取得試驗額度授權跑 fresh dialogs，不繞過安全限制。

## Risks / Trade-offs

- 自然語言路由不穩 → 正反例 fresh dialogs，記錄實際 reference 讀取，不只看答案正確。
- 候選索引本身成 prompt debt → 只存 identity/狀態/來源與必要理由，不保存重複全文。
- 大改隱含覆寫既有工作 → consumer 盤點與 narrow diff；兩側獨立 deploy。
- 技術文件被文學標準阻擋 → 用途正反例；技術主張用證據而非張力評分。
- review 紀錄製造寫入打擾 → 可以零持久寫入結束，成熟候選合併呈現。
- 若過渡期舊名稱仍可發現，context savings 有限 → 明示主要/相容入口，版本到期有 consumer 證據後移除。

## Migration Plan

1. 規格審查及使用者確認 breaking changes/儲存位置/權限；此前停止在規格階段。
2. 全面歷史盤點先產 read-only baseline；分類確認後才持久化 review records。
3. 按能力建立共用契約與受影響測試，再改入口與各 runtime adapter。
4. 盤點 hooks、排程、文件引用、自然語言 routing 與第三方 writing dependencies；建立相容轉向與回退清單。
5. 用隔離 vault 在 Claude/Codex 新對話驗收，補真實跨機證據；未測項逐列留未驗證。
6. 使用者授權 release/deploy 才發布過渡版；來源 revision、生成副本、installed payload 及 fresh runtime 分開核對。回退保留原版 payload/設定與新增資料，不能刪已保存筆記。

## Review Gates

G1：Claude 的 1519 審查及 1527 更正已讀取；撤回的範圍拆分異議不再列阻礙。保留意見已納入本輪修訂，須交使用者裁定；規格修訂不是實作授權。

G2：退役規模與過渡期是完整提案的待審選擇；若不批准，必須同步改 proposal/specs/design/tasks。審查紀錄的儲存形狀依完整歷史唯讀盤點決定，不預設每候選一檔。

G3：dream-RSI 真實連接、跨機 concurrency 及 consumer 相容性未驗證，未完成前不可標整體完成或 archive。

## Open Questions

可延後且不改外部契約：review events 的最小存法、消費者測試 fixture 的檔名、發布版號。所有影響行為的方案已明寫為待審設計，不藏在本節。
