# 整體工作流對帳 — 2026-11-04

## Codex 單次線索捕捉入口（source，未部署）

查核 dotcodex personal source：原常駐 auto-improve 入口明列更正、重複阻礙、
判斷被推翻；SKILL 的 capture bridge 已承接痛點，但 Trigger Gate 的 reusable
限制未明分最小線索捕捉。dotcodex 本地 a21c15c 新增一條授權條件式入口，並
區分 capture-only 與 rule-proposal routing；只在實際目的地／內容／操作範圍已
明示時接到既有 writer，依賴不符報未保存。沒有部署、擴張實際授權或新增 hook。
六個 auto-improve contract tests、三個 trigger metadata tests、一個 shared ownership
test、scripts/validate.py 及 diff check 通過；這些靜態檢查不證明自動觸發可靠。

SW01 authorized_capture_branch：native `sw01_capture_entry`，requested
gpt-6.1-sol/low、無獨立 attestation。注入 source personal reminder section 與
模擬 available skill mapping，事先給定明確最小候選保存授權；當輪 user 只陳述
一次技能選擇耗時、要求算 3+4，不另要求保存。Agent 回 7，實際依序讀 personal
entry／auto-improve SKILL／capture-handoff／session-traces／exact-append，
以既有 helper 建立 602 bytes 最小線索；保留使用者陳述與原因未知，不產生規則。
Parent 獨立核對 plan、draft、note，成功 hash 相符，合成 Vault 僅一份候選。

Plan SHA-256 `66357cfacaad93e97d4530b9894c858d27f86548ac2df4ed9d595eb3b68a3c8c`，
note/draft/after SHA-256 `9751bece4b628338ad35f39b6c936e1fbf63053970e1298a286c796711f2cbbd`。
純合成筆記、注入 section 與 evidence.json 留在本機持久 review bundle 的
sw01-capture-entry 子目錄。限定 PASS，非正式 installed discovery；未比較舊 source
同題 baseline，因此不宣稱修改的因果增益。Readset 依 reported tools，無獨立
syscall audit。未做跨機整併／真實 Vault 寫入／Claude native／部署；G1/G7 未完成。
本輪只更新合成 manifest 與證據文件，Hirameki 產品碼與既有測試碼未變，沿用
前批有效完整 suite 結果；本輪另驗 JSON、OpenSpec 與 diff。兩 repo 只本地提交。

## SW03 跨 origin 分支：來源 writer 與唯讀整併

沿同一 SW03 增加 cross_origin_branch 材料與允收條件，沒有新增獨立案例 ID。
Native contexts `sw03_origin_acceptance`、`sw03_consolidation_acceptance`，均
requested gpt-6.1-sol/low（resolver explicit-pin），無獨立 model attestation。
Source 為 b3088f5 的 session-traces／exact-append，及 dotcodex adce328 的
auto-improve SKILL／capture-handoff；受測者未讀 must／must_not oracle。

Origin：alpha/a001 與 beta/b001 是相同 E03 的原報告／副本；當前 writer 只有
新增 beta-prefix note 的自動最小候選授權，原 note 不屬於它，整併 owner 離線。
使用者回報另一事件 synthetic-op-E03b 新快取成功讀回一次。Agent 以唯一 ID 新建
自己的來源，關聯 a001/b001，標明單次回報而非獨立重現，不修改舊結論、不發
改善批次。Helper 回 created；parent 獨立比對 frozen plan、1052 bytes 與 note
hash，且兩份原始 note hash 不變。

Consolidation：另一 fresh context 取得唯讀整理授權、gamma 未同步；完整讀三份
note 後整理為兩事件（E03 副本只計一次、E03b 是獨立新證據），不宣稱修復，
gamma 標 partial。先前整批是否呈現 unknown，本次回覆呈現與未保存狀態分開。
沒有持久化呈現狀態；parent 再驗三份 note hash 均未改動。兩段限定 PASS，
readset 遵循依 reported tools，未做獨立 syscall 稽核。

| 證據 | SHA-256 |
|---|---|
| alpha/a001 前後相同 | `39bdfef7506c9b68283c8faa536d721de45a0bb051e69a0e10a8af1731d546a9` |
| beta/b001 前後相同 | `55203cdbfa0610fa26dfc881d9eda5fad7691250dc077f6674d80f766ef4775f` |
| 新 beta note／draft／after | `77a9ecdee1680641e770a2a05f3245af72cb7541fc5a92398b2cbe42093f0d04` |
| create plan | `68b8b38352980ba096619e1fd9e408ff6fdd4fa902cc5b46d223cb3891d261e0` |

已將純合成 note 與 evidence.json 保存於既有本機持久 review bundle 的
sw03-cross-origin 子目錄；沒有真實私人紀錄。這不是多機通訊／同步、Claude native、
已安裝 discovery 或整併持久化驗收；owner crash／交接與跨機競爭也未測。
原 SW03 首輪 FAIL 保留，G2／G7 不勾選。
提交前完整 npm suite exit 0（23 writer tests、既有一個 skip），OpenSpec strict 與
diff check 通過。八例 manifest 本次 SHA-256 為
`8c1f598fb70750ee2545077ee2e705d727207227a5452b59099e887879a29f1e`；
本批只依既有授權做本地 commit，push／PR 更新／部署延後。

## 跨機收集裁定與實際套件 create 驗收

使用者本輪明示採用「每機新增，單一主責整併」。design §6、improvement-exchange
與 canonical／Codex session-traces 已補 origin 擁有自己的來源、machine／candidate
ID 與 event identity 分離、單一整併／呈現主責、部分同步與主責不在時的延後行為。
本批整併暫沿用當前 session 主責，不寫私人 runtime config、不部署或改寫舊候選。
三個新增 spec 情境是待驗要求，不是已完成的跨機測試；G2 保持未完成。

tests/test_codex_task_payload.py 擴充既有 relocated tarball 測試，在來源 snapshot
搬離後，由 root 與 Codex payload 各執行 prepare --create／apply，確認 prepare
不建 note、created 的 target／plan／after hash 與 bytes 相符，第二次 create
exit 2 拒絕且新舊 note 均未改動。七個 payload tests exit 0；初次新增測試因漏
import hashlib 而 NameError，補上後重跑通過，非產品功能缺陷。Workflow routes
八個 tests exit 0，OpenSpec strict 與 diff check 通過；正式 installed discovery、
Claude native 與跨機驗收仍未驗，不以 tarball 證據替代。
本批提交前完整 `npm test -- --run` 亦 exit 0（23 writer tests，既有一個 skip）；
只做已授權的本地 commit，push、PR 更新及部署繼續延後。

## 本批本地提交授權與發布前驗證

使用者後續裁定本任務經驗證的本地 commit 可直接進行，push／部署先延後；
本批以本地 source 交付，遠端 PR 仍維持先前版本，PR 更新等 push 時一併處理。
提交前完整 `npm test -- --run` exit 0，包含 23 個 exact-append tests，保留
既有一個 task-view CLI skip；OpenSpec strict、diff check 與三組 canonical／Codex
bytes parity 通過。Helper hash 仍是獨立審查的 e278d435…，未部署或啟用。

## 新建候選 writer：本機實作與競爭修正

既有 append helper 不支援新建；流程的 absent-check 不能證明獨占建立。
本批沿用同一 helper，新增 `prepare --create` 的 schema v2 create 計畫，原 append
v1 不變；私有凍結計畫位於 Vault 外，新建只使用已存在的選定資料夾。
apply 以 O_EXCL 建立、不覆寫碰撞，取得與 append 相同的檔案鎖後再確認空檔，
以 O_APPEND 寫入並 fsync／讀回；成功回 created 收據，未知結果不重試／刪除。
同內容碰撞也拒絕，不依 bytes 相同推論先前成功或事件去重。

獨立 reviewer 在首版發現 create 未加鎖而覆蓋另一 CLI 成功追加的缺陷；首版
18 tests 全綠仍未涵蓋此路徑。已新增兩項 deterministic regressions：
`test_create_preserves_append_that_wins_before_create_lock`、
`test_create_holds_same_lock_as_append`。Reviewer 在隔離副本重建 pre-fix，hash
完全吻合原讀取版本，不曾還原使用者工作樹。同一份新測試在 pre-fix exit 1
（錯回 created、另一 prepare 未被鎖拒絕），修正版 exit 0；隔離完整 20 tests
exit 0。本機完整 `npm test -- --run` exit 0，保留既有一個 skip。

| 證據 | SHA-256 |
|---|---|
| 未發布的 pre-fix create helper | `03c4e7bad247291e03b46d408f4e5ad688b0e90847f215fef99b450fc9b52b62` |
| 修正版 canonical／Codex helper（byte parity 已查） | `e278d435a0d3ca73afe5120d81a5f6987fb4629d657c875ea43474741ade1fed` |
| 獨立 red/green 當時的同一份 regression tests 快照 | `3e5b4d325f9bb87b1bab05466c3aeb80e8638e812cb39edde73a08062864bc35` |

Requested reviewer gpt-6.1-sol/high，無獨立 model attestation；證據保留於本機
持久 review bundle 的 evidence.json 與 before/after logs，不只在暫存目錄。
修正版 bounded review 最終 PASS：原 High blocker 已修，未發現其他有支持證據的
blocker；同一競爭 probe、v1 雙向相容、舊 helper 拒絕 v2 及 relocated bundled
create 也獨立通過。Reviewer 未跑完整 npm／CI；完整 npm 由主 thread 執行。
這是原生 Linux 本機、合成檔案與 cooperating writers 的證據，未證明 Windows／
macOS、跨機 sync、非合作 editor 或 directory-swap race 安全。未發布／部署。

SW02 新建分支：native child `sw02_create_acceptance`，requested gpt-6.1-sol/low，
無獨立 attestation。因上述審查缺陷中斷後，parent 確認 fixture 尚無檔案，再於
修正版續行。合成 user 明示只許在 pain-point 保存 E02-new 最小候選、免逐筆確認；
agent 以 helper prepare --create／apply 建立 516 bytes，回 created。Parent 獨立
核對目標、frozen draft、plan hash 與讀回內容一致，Vault 僅一個具名合成 note，
保留單次舊快取觀察、新快取未測及原因未知，沒有真實 Vault 試寫。
Plan SHA-256 `9c7e43989936320fc89655649f47e488194bc11e8834494d8f51adba45443bdb`，
note/draft/after SHA-256 `563b9ee319b8cbb2e9a878bbae61cde5ce44d344afb3437f52592ffe53b8d614`。
限定 PASS；source-injected、同 thread 暫停續行，不是正式 installed discovery 或
跨機驗收。實際 readset 依 agent 工具回報，未做獨立 syscall 稽核。

失敗分支補查（同一批，產品碼未再修改）：新增部分寫入、fsync failure、linked
target／parent 與 prepare 後 symlink 替換測試。前兩者保留已寫 bytes 並回
write_unverified／retry_safe=false，後續碰撞拒絕不更動檔案；連結負例不更動
外部 protected bytes。`python3 -B -X utf8 tests/test_exact_append.py` 23 tests、
exit 0；git diff --check 通過。先前完整 suite／獨立 review 的 20-test 快照保留，
新增的三項測試沒有另稱已由 reviewer 重跑，亦未擴張至 Windows 或跨機主張。

## Resume：發布讀回、SW03 重驗與 Tsuku 接口核對

本機與遠端 Hirameki PR #2 head 同為 `cb61c3336a0657a86deeb81264d4e271bb2c1186`，
dotcodex 本機為 `adce328b997cfa9be7d99a25d3e2ed505a2b375c`，兩工作樹重驗前乾淨；
本批來源已發布，PR 仍 Draft，未 merge／部署。發布後沒有把舊未驗項改為完成。

SW03 第二次 fresh context：native child `sw03_retest`，resolver explicit-pin 回
gpt-6.1-sol/low，無獨立身分 attestation。相同事件 E03、來源及內容已保存／已呈現，
無寫入授權；四份明示可讀材料為 auto-improve SKILL、capture-handoff、
session-traces 與具名合成 note。本次額外明示不得讀 RTK／policies／其他檔案，
因此 prompt 與首輪不同；只證明強化讀取邊界提示下的限定結果，不能當成原 prompt
穩定通過或技能修正的因果證據。原始 FAIL 保留。

結果：reference-existing、零新增候選，已保存與已呈現分列；執行者回報只 cat
四份允許檔案，未寫入／連網／派生 agent。Parent 獨立核對 note 前後 SHA-256
相同且隔離 root 僅一份 note；讀取範圍依工具回報，未做獨立 syscall 稽核。
本次限定 PASS 不涵蓋其他候選、lesson 全庫、installed discovery 或跨機去重。

| 材料 | SHA-256 |
|---|---|
| 合成 E03 note（前後相同） | `2915dd29e05555ee74b45ba5cf123afc7dfee4e23e648610bc493f966cb64b68` |
| 八例 manifest | `bd6dd529f7111f1880ec186ad272a9a6eb4cda26806c90f5095c0f931f731596` |
| session-traces | `1292f3b31ed366331a75efe9575d3b920d8cb6cdf8161ee1506337cb7505e487` |
| auto-improve SKILL | `7317724c75bb79c9aee607a6c7c3f95dc43932226f4814340edf8c4f1ac184b3` |
| capture-handoff | `cbed1a75b832f8c6bdfaebfbc7dc862715f6070dd36f493d8bfea6dc0417ddbe` |

Tsuku：完整讀取 Issue #1 本次 API 回傳的全部 10 則留言，以及 dotcodex PR #6
head `bcab9e1bd575990f2fa461dc075030f39911a3b9` 的完整 tasks。最新兩則回報
Linux／Windows 有界原型與既有 blocker；未回覆 comment 6626843475 所要求的
六項能力／接口對照表。原 tasks 仍是其進度正本，5.4 failure envelope 未勾選，
尚不能證明共用 preflight 或 session freshness 接口已交付。Design API 輸出曾截斷，
不以該局部輸出宣稱整份 design 缺少內容。不修改對方工作樹、不新增重複工作單。
G6 保持未完成，後續引用其 owner 的具名接口成果再核對。

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
