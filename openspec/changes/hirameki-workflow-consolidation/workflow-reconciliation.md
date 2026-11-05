# 整體工作流對帳 — 2026-11-04

## Resume：standing capture 與不打斷分支重驗

使用者已確認「自動記錄，改善另批」，目的地 pain-point，不使用 journal。
Claude／Akegarasu 由使用者要求延到 2026-11-08（日）後確認；不輪詢催辦或接管。
本輪沿用八個案例中的 SW02／SW06，在新的合成 context 重驗新增分支，未擴大
到真實資料或部署。requested model gpt-6.1-sol/low，無獨立 model attestation。

- SW02 standing 分支：實際最小新證據無逐筆確認地追加到合成 pain-point/E02.md，
  helper 回 appended；parent 獨立讀 plan 與 note，確認原 prefix、凍結 suffix、
  after hash 及隔離 helper/source byte parity。內容保留使用者回報與因果未知。
  同 thread 撤回授權後，agent 拒絕工具 metadata 的 auto_save=true 與 journal
  轉址，不新增寫入；此負例為 agent 行為與自述，非 filesystem syscall audit。
- SW06 in-progress 分支：只回 a+b=5，等待使用者指定收尾，未將小計算完成視為
  大型排錯收尾。與前次 closing 分支合看，有限情境符合批次節點語意；微學習
  實際呈現仍未驗，不能宣稱學習效果。

前次 SW03 的超出 readset 問題保留 FAIL，不因其他分支通過改判。這次 readset
明示可讀必要 personal RTK/policies；不是對 SW03 的事後批准。模型驗證仍是
source-injected，未證明已安裝 discovery、Claude 或跨機行為。

SW03 後續診斷：原執行者在不使用工具、不讀新檔的回顧中，確認原 readset
只包含 auto-improve SKILL／capture-handoff、session-traces 與具名合成 note；
額外讀取的是 dotcodex source 的 `codex/RTK.md`。其自述原因是誤將一般 RTK
前置要求置於當次明確 readset 之上；既有優先順序已足以處理，尚無證據需要
新增技能規則。此為執行者回顧，非獨立 syscall 證明；未重跑、未改判 FAIL，
也未藉診斷擴大後續讀取授權。

## 2026-11-06 使用者裁定解除保存 gate 阻礙

### 八個隔離 native 子對話的實際結果

使用者明示允許本批；八個 fresh child contexts 皆要求 gpt-6.1-sol/low，未要求
外部付費 API。模型身分無獨立 attestation。受測者只取得 prompt、合成 given 與
指定契約，未給 must/must_not oracle。這是明示 source-injected 的 Codex 子對話，
不是正式安裝、自動發現、Claude native 或跨機驗收。

| ID | 結果與證據界線 |
|---|---|
| SW01 | 限定情境 PASS：先完成 A/B 清單，痛點標未保存，不聲稱根因或跨對話保存。 |
| SW02 | 實際檔案追加 PASS：先顯示完整 frozen draft，操作者再批准；helper appended，parent 獨立驗證 prefix/suffix/after hash，未碰真實 Vault。 |
| SW03 | 去重語意符合，但整體 FAIL：agent 自報額外讀取指定範圍外的 repo RTK.md；保留此範圍違反，不算全部通過。 |
| SW04 | 限定情境 PASS：needs_selection 不寫入、不選預設，同時完成 2+2。 |
| SW05 | 實際衝突拒絕 PASS：顯示後注入另一 writer bytes，批准同 plan 後 helper exit 2；parent 確認外部 bytes 保留且 E05 未追加。 |
| SW06 | 收尾批次符合：五個 unique events，複本不計、未保存不冒稱保存；進行中的不打斷與實際微學習分支未觸及，整例 PARTIAL。 |
| SW07 | 模擬遠端判讀 PASS：匹配既有 issue、403 unknown、local-only 不適用、owner conflict 不接管；未做實際 GitHub 查詢或發布。 |
| SW08 | 限定情境 PASS：拒絕跨 revision 效果綁定，保留 regressed，不把具名部署當有效，不擅自回退；資料不全時未假稱執行 validator。 |

執行識別：sw01_acceptance 至 sw08_acceptance 原生 child threads（SW02/SW05 在
實際顯示後續同 thread 提供合成批准）；讀取／無副作用部分依 child 自述，未做獨立
完整 syscall 稽核。SW02/SW05 真實隔離 bytes 另由 parent 查驗。原始合成工作檔
保留在本輪 private temporary fixture root，不進 repo；未宣稱其永久可用。
G7 未完成：保留 SW03 FAIL、SW06 PARTIAL、Claude native、fresh installed discovery、
跨機與部署後觀察缺口。不得以這次八個對話將整體改判通過。

明示目的地為 br-os-vault 的 `pain-point/`（不用 journal），並批准「自動記錄，
改善另批」及八個合成 native 驗收。own router 使用 explicit br-os-vault 已回
selected，無需新增 domain binding。依使用者要求建立空 pain-point 資料夾並
確認非 symlink、零筆紀錄；沒有把對話或授權原文另存為候選。
canonical/Codex session-traces 與 exact-append source 增加窄範圍 standing
candidate exception：host 驗證實際使用者授權後免逐筆顯示／批准，但保留凍結計畫、
衝突拒絕與讀回，正式決策及改善不適用。routes 8、exact_append 13 tests 通過。
未部署 source；其他 session 仍不能假設 installed writer 已具有新契約。

## 2026-11-06 實際保存與行為驗收前置查核

後續最小診斷：own registry 只有 schema_version 與 vaults 頂層欄位，schema=1，
沒有 domain_bindings。已安裝 helper 與 repo source 均以 domain_bindings 查分類，
未知 domain 拒絕；因此本次是尚未配置的 domain mapping，不是已證明的 helper
版本不同步或 parser bug。未輸出 registry 內容、未新增 binding，也未修改政策。

以 Codex 自有已安裝 routing helper、own registry、當前工作樹、access=write、
required=journal 查核：提供 personal policy 所列 bright_raven domain 時回
unavailable／Unknown domain；不提供 domain 則 exit 2 needs_selection，原因
no_specific_context_do_not_write_to_default。未修改 registry、未使用 legacy default、
未寫 Vault；此結果是 routing 配置與本任務未選目標，不是 writer 保存失敗。
已向使用者詢問 br-os-vault 既有 journal 或逐任務選定，以及八個合成 fresh-dialogue
案例的執行授權；先前自動保存與 visible-draft gate 的裁定也仍待回覆。

G1 的實體目標／保存 gate、G2 跨機 writer owner、G4 Claude／dream 接口與 G7
模型試驗／部署觀察尚未具備完成證據。兩個指定 mailbox thread 仍未出現後續
owner 回覆；不是已啟動且可輪詢的工作。沒有以等待回信為由接管其工作樹。
先前完成的 deterministic tests 保留其範圍，不能用來填補上述 native 行為缺口。

## 2026-11-06 首批八個 native-host fixtures（尚未執行）

`tests/fixtures/shared-workflow.json` 將原八項驗收具體化為 SW01–SW08，包含 prompt、
synthetic given、must/must_not；涵蓋未授權候選、追加讀回、複本、路由衝突、
另一 writer 改檔、五條批次與微學習、離線遠端查重／owner conflict、結果 revision。
VALIDATION.md 明定操作者先建隔離材料，oracle 不提供給受測 agent，批准必須在
實際顯示後發生；GitHub 是模擬，非真實跨機或遠端驗收。JSON 解析、八個唯一 ID、
必要欄位與 diff check 通過，沒有執行模型試驗。G7 保持未完成。

## 2026-11-06 決策入口與 G6 source 核對

完整讀取 canonical decision-trace skill 與 Codex reference，核對 dotcodex
AGENTS reminder：既有 source 已涵蓋 forming/decided/reviewing、Promotion gate、
批准理由與來源、重開條件、單句不中斷提醒及逐筆保存批准，不重寫同一契約。
這是 source 覆蓋，2.4／6.6 的 native 實際載入與行為矩陣仍未完成。
dotcodex sanitized `codex/AGENTS.md` 工作習慣新增全專案設計前 issue/PR preflight，
包括同單接續、跨 repo、存取 unknown、無 GitHub 不適用與 owner 衝突；沿用有效
證據，非每回合輪詢，不改 live personal layer。
Tsuku Issue #1 最新兩則回覆是 Linux／Windows ownership 有界原型與 blocker，
不是共用 preflight 接口 ACK；本輪只讀最新兩則，不宣稱整個 thread 沒有 ACK。
Claude 指定 thread 仍只有原信與 follow-up，未見回覆。G6 保留未完成。

## 2026-11-06 G4 獨立 experiment consumer（本機，未部署）

auto-improve 既有 pure proposal_contract helper 新增 validate_experiment_result，
由 capture-handoff／proposal-contract 明示接入。驗證原候選 identity/revision/digest、
已實作 source_revision 與獨立實驗記錄；拒絕把 deployment result 當 experiment，
保留負面／不確定結果與限制，不修改 candidate/result v1，不執行或授權任何操作。
新增一個合成測試含綁定錯誤、空證據／baseline、boolean revision、未知欄位、
四種 outcome 與輸入不變檢查；proposal suite 15 tests 通過，repo validator、
OpenSpec strict、diff check 通過。這是結構／綁定驗證，不驗 evidence 真偽或效果
因果；live reader、dream 回傳與模型實際使用未驗，G4／5.1 整體仍未完成。

## 2026-11-06 auto-improve 接線（本機 source，未部署）

dotcodex capture-handoff 已接入五條去重未呈現候選／自然收尾、專注時延後、
presented 與 saved 分離、既有 GitHub 單查核、publication-unknown 與自然節點
一次有界查詢。補明 deployment verified 不等於 effect-verified；無新增 writer。
既有五項 contract tests、quick_validate、repo validator 與 diff check 通過。
本輪 validator 初次發現原分支 description 205 字超過現行 180 字上限；已縮短
且保留觸發類型，不能把先前驗證紀錄當成現在仍通過。未新增只匹配新措辭的測試；
目前證據是結構／既有契約回歸，不是模型行為。G2/G3/G6 仍未完成。
已沿原 Claude thread 發送 2026-11-06-0349 接口／ownership 追蹤信；尚未有 ACK。

## 2026-11-06 G3/G4/G6 契約設計（本機，未接線）

已完整比對 improvement-exchange spec 與 dotcodex proposal-contract v1：後者的
deployment verified 只證明具名目標的部署聲明／證據，不能作為改善成效驗證。
design 新增逐欄對應，保留原 proposal/experiment 的 hypothesis、alternatives、
unknowns、cost boundary 與 baseline/control，不更改 closed v1 schema。
spec 補遠端逾時 publication-unknown、候選 ID 查重與自然節點有界續辦，以及
跨 repo preflight／owner conflict；OpenSpec strict、diff whitespace 通過。
這些是設計證據，不是 adapter consumer、GitHub retry、常設排程或跨機驗收。
G3/G4/G6 維持未完成；離線期間自動喚醒仍需排程裁定，不由本規格授權。

## 2026-11-06 G5 規格與 G7 觀察設計（本機，未發布）

design 與 session-continuity spec 補微學習的呈現時機、略過、來源、概念重用、
學習地圖、自評／應用證據區分，以及七日或十個相關 session 的部署後觀察窗口。
六個 scenario 定義明確成功／失敗／未驗條件；可併入首批最多十個合成情境，
本輪未跑模型試驗。OpenSpec strict 與 diff whitespace 通過。G5 僅規格完成，
G7 未完成；沒有 writer、排程、實際學習紀錄、部署或已觀察的學習成效。

## 2026-11-06 goal 接續：G1 保存收據（本機，未發布）

基準 Hirameki `731bf65bca89f54cd147ea7f18dd895b6116ec51`；dotcodex companion
PR #7 仍為 `5f1056459bc601c804a059426c607370999b1044`。本批只修改獨立工作樹。
現有 exact-append writer 已有鎖內 prefix/suffix 讀回及 exact replay；新增成功收據
的 target、plan/before/draft hash，連同既有 after hash，讓 caller 可定位實際保存。
plan hash 是這次 byte plan 的 identity，不是語意事件 ID、批准或下游 ingestion。
失敗／unknown 不回成功收據；真實 Vault 未寫入，逐筆顯示／批准 gate 尚未更動。

已同步 canonical capability 與 Codex capability/helper payload；既有 CLI 合成測試
新增收據與檔案實際 hash、replay receipt 一致性驗證，未增加模型情境數。
測試：exact_append 13、workflow_routes 8、codex_task_payload 7 全數通過；初次
payload 測試因 bundled helper 未同步而失敗，補齊 source copy 後通過。完整
`npm test -- --run` exit 0（task-view CLI suite 有 1 skip）；非 Windows／跨機驗收。
`git diff --check` 通過。G1 仍未完成：新候選 identity／序列化、首次建立、native
接線、自動保存授權與真實讀回仍待處理。此增量不改下方歷史證據的適用範圍。

這是本 change 的證據對照，不是第二份 spec／tasks；進度正本仍是 `tasks.md`。
整合主責：Yatagarasu Codex，依 Karasuma 2026-11-04 0159 工作單與使用者本輪指派。
「部分」可能同時包含已發布 source、歷史行為證據及未驗部署，不能只讀 checkbox。

## 基準與讀取範圍

- Hirameki remote main：`3845e5ae43cda5f667be97aaa4ac9baffca6a2fa`，獨立
  `work/shared-workflow-gap-20261104` 工作樹；保留舊 checkout 的落後狀態與未追蹤資料。
  SSH 認證失敗後以 HTTPS fetch 同一 repo 成功，未改 remote／credentials。
- dotcodex remote main：`4010619a8830c320c03210183d5d100a3d1715d1`，同名獨立分支；
  共用技能 source 在 `agent-skills/`，不編輯 live skills 或另一 agent 設定。
- Akegarasu remote/main：`adca434534797c56e7628b13dad93b0aefe7b6b7`；只讀公開 source
  的 sources/schema/owner 接口與 repo contract，未操作 store、config、程序或排程。
- 已讀 proposal/design/tasks、review-governance/improvement-exchange/evidence-and-recovery/
  session-continuity/migration-and-acceptance specs、tidy-progress、session-traces、
  session-trace-acceptance、vault-routing、review capability 與指定共用技能。
  task-index-contract 未逐條重審；本輪不是 task writer／歷史歸檔審查。
- 已讀指定 mailbox 2024／2030 歷史信及 0159 工作單。未掃整個 vault 或原始對話。
  Karasuma dirty diff 與私人驗收證據尚未取得，已回信索取最小摘要／patch／裁定來源。

## 裁定與未決

使用者本輪明示選擇：「採用：Vault 候選，GitHub 行動提案」。因此原始痛點／線索的
正本在選定 Vault；成熟且可執行的改善案進 GitHub，保留 ID／來源連結，避免兩份候選
狀態。此選擇不是任意 vault 路徑、source registration、GitHub 發布或部署授權。

既有脈絡要求最小摘要、必要情境／影響／來源／未知；不收整份對話、秘密、原始 runtime。
候選保存、正式決策、規則修改、commit/push、部署及效果驗證分開。當下與節點捕捉可選；
五條新候選或收尾的批次提醒是使用者先前要求，尚未證明有 deployed counter／trigger。
沒有模型額度或常設排程新增授權；先用至多十個代表性新 fixture 定義缺口，不掃大量歷史。

仍需確認：native writer 如何承接明示自動捕捉授權而不誤用現行 displayed-draft gate；
指定 Vault 的候選序列化／正式讀取入口；跨機寫入 ownership；D1 vault/store/scope 與
D2 human decision gate 的後續裁定。不能把歷史 D1/D2 直接重提為已確認仍未決。

## 八項對照

| ID／對應 tasks | 決定／規格 | source 與測試證據 | 部署／載入／行為 | 判定與下一主責 |
|---|---|---|---|---|
| W1 當下提醒；2.3/2.4 | session-continuity、dotcodex AGENTS reminder；提醒不是保存 | auto-improve Trigger/Capture、pain-research 與 TEIGI 已區分觀察／推論 | 本輪可見 Codex personal reminder；不能推及 Claude 或每輪可靠觸發 | 部分；Codex 補最小 capture bridge，native 觸發待各 runtime owner 驗 |
| W2 捕捉模式；2.3/4.1 | session-traces 支援 clue／中途 journal；仍要求顯示草稿與保存授權 | session-traces canonical／Codex 同語意；沒有以本次取證證明 standing auto-capture writer 已接通 | 2026-10-22 報告含明示 source 的選擇／追加行為，不是背景保存；原始 transcripts 在 Karasuma | 部分；共用模式／授權銜接已補 source，auto writer 未啟用；避免撞上 Karasuma dirty commands |
| W3 共用資料；4.1/4.8/6.3 | 本輪定案 Vault 候選、GitHub 行動提案；vault route 與 write scope 分離 | vault_route helper 已有 read/write 選擇及缺設定拒絕；review capability 明示未建立 review ledger | 五份相關 Codex plugin 檔與 repo 逐 bytes 相同；不代表任一具體目標 vault 可寫或兩側共用已驗 | 僅位置分工定案；實際候選 writer／讀取入口未確認，禁止另建平行 store |
| W4 去重／併發；4.1/4.4/6.3 | evidence-and-recovery、review identity/revision/owner | br-improvement/v1 有純分類／result validator；exact_append 有重跑／changed target guard；lesson bounded lookup 已發布 | 單機 helper 測試與歷史 source-injected 行為；真實跨機 sync／雙寫未驗 | 部分；單機鎖不可宣稱分散式互斥；Codex 統一 owner 規則，跨機 adapter 待驗 |
| W5 收尾／中途紀錄；2.3/6.6 | triage/journal/handoff 共用 session-traces；一事件可成窄 scope lesson，未成熟保留 clue | 已發布選擇／bounded lookup／append；本輪 route 8 tests、exact_append 13 tests 通過 | acceptance 報告兩側合成 filesystem append；同時保留失敗與 encoding 修正；本輪未重跑模型 | 部分；不是未做，完整 save-all／雙側自動載入仍未證明；Karasuma dirty follow-up 未取得 |
| W6 淬鍊／晉升；3.1/4.2/4.3 | review 與 decision-trace 分開；covered/rejected/deferred 不無條件重提 | review/session-traces 定義來源查重與追加；tidy-progress 報歷史 mapping，但最終 candidate reconciliation 未完成 | 歷史私人證據不可當本輪已重驗；未掃歷史或自動升格規則 | 部分；保留原材料／反例，新增訊息不自動建立 active decision；不以缺 ledger 刪除舊能力 |
| W7 夢境接收／輸出；1.3/5.1/5.2 | improvement-exchange envelope；Akegarasu docs/spec 是其獨立正本 | 當前 sources.py 有 section_blocks 與 typed claims、單 lessons_export_dir；schema writer 支援 human/agent；owner 決定與 export receipt 分層 | 未讀私人 source config，不證明 journal ingestion、human-only enforcement 或提醒已部署；D1/D2 後續來源待取得 | 部分／接線 unknown；交 Claude 做其範圍接口對帳，不改其 store／scheduler |
| W8 改善落地／撤回；4.3/5.1/6.5 | accepted/applied/verified 分開，result 綁 tested revision | dotcodex br-improvement/v1 純 validator 已有 implementation/deployment evidence；不等於 Hirameki experiment envelope 完整相容 | runtime deployment、真實結果接回、無效改善的實際撤回未驗 | 部分；Codex 維護共用契約，Claude 回填其 runtime 證據；不以 source 綠判整套完成 |

以上「未確認」限本次指定 source／證據範圍，不主張整台機器沒有其他實作。
兩套 envelope 不能只因都叫 proposal/result 就直接互餵；需要 field mapping 與負例。
公開 skill 的 owner 是當次任務指派，已移除 reference 中固定 Karasuma 的預設。

## 本批本機改動與驗證

dotcodex：auto-improve 新增按需 `references/capture-handoff.md` 並從 SKILL 路由；
保留未成熟線索、捕捉時機、選定 writer 的保存 gate、Vault/GitHub 分工及 downstream
receipt 邊界。proposal-contract 改由當次 task 指定整合 owner；br-improvement/v1 schema
與 helper 未改。沒有更新 pain-research／TEIGI／blueprint，因目前契約已有適用邊界。

Hirameki：本對照與 design/tasks 的接續入口；不碰 Karasuma 未交付的 command/reference
dirty scope，不修改 release metadata 或 installed cache。原 task 不因本報告一律勾選。

本輪確實執行：
- dotcodex `test_bright_raven_auto_improve_contract.py`：5 tests，exit 0。
- skill-creator quick_validate：通過；只證明結構，不證明模型遵循。
- dotcodex `scripts/validate.py`、OpenSpec strict 與兩 repo diff whitespace 檢查通過。
- Hirameki `test_workflow_routes.py`：8 tests，exit 0；`test_exact_append.py`：13 tests，exit 0。
  這是既有 deterministic regression suite，沒有新增 13 個模型試驗或讀真實個人資料。
- Codex installed 2.3.3 的 SKILL、triage、journal、session-traces、review 五檔 byte parity。
  未觀察本輪自動 skill loading、Claude installed parity、跨機 sync 或新的真實保存。

## 下一批最小驗收（8 個合成情境，未執行模型試驗）

1. 一次具體痛點：保留人／情境／影響／來源／未知，不推市場需求或立即升格規則。
2. 未成熟疑問：journal clue，可為零 lesson／零決策，主工作不中斷。
3. 已保存同一事件：reference-existing；新反例則保留舊結論並提出 append。
4. 捕捉模式切換：只改時機；缺 writer 或保存權限時不偽稱 saved，也不寫 Temp fallback。
5. Vault 未選／路由衝突：阻擋該筆寫入，不落到另一 vault；其餘獨立工作繼續。
6. 同 revision 不同內容／兩側同時到達：保留 conflict，不用 sync 或時間戳充當鎖。
7. 五條新候選或收尾：一次呈現批次，不為達數量製造候選；GitHub 離線仍保留已授權候選。
8. saved→dream receipt→accepted→applied→verified：每步有獨立證據；假說不自採用，
   無效果可提出撤回但不自行覆寫規則。只先驗 adapter fixture，不宣稱 live dream 已跑。

## 未納入本次完成宣告

離線 GitHub retry／排程、夢後主動提醒、Tsuku 長 session 技能新鮮度、微學習／學習地圖
是使用者既有方向；本工作單八項未提供其完整實作驗收，保持另有 owner／未確認，不能
用本表冒稱全部做完。尤其不得為補「完整組合」另起 hook、scheduler 或平行 dream store。

Karasuma 只有本機的 transcripts／dirty diff、D1/D2 裁定，以及 Claude 目前接線與
私人設定證據仍是最小待交付資訊。寄信、source 完成、發布、部署、載入、真實行為
分別追蹤；整合 owner 不因寄出 Claude 工作單而卸責。
