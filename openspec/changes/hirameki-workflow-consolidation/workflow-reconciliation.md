# 整體工作流對帳 — 2026-11-04

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
