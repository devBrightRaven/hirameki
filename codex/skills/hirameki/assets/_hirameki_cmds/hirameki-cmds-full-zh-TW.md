# Hirameki 指令 — 完整規格

所有 Hirameki 指令的完整 prompt 規格。這是人類閱讀用的參考文件 — 實際的指令 prompt 在 `commands/` 資料夾中。

---

## 共用：`__init`

每個指令先從 `~/.claude/vault-local.md` 讀 `vault:` 取得 vault 根目錄，再從 `<vault>/AGENTS.md` 的 `## Vault Structure` 段落讀資料夾路徑（fallback：`~/.claude/vault-local.md`，再來是 `~/.claude/CLAUDE.md`）。

### Vault 偵測

1. 檢查當前工作目錄是否有 `.obsidian/` — 有則以此為 vault
2. 讀取 `~/.claude/CLAUDE.md` 中 `## Vault` 段落的 `path` 設定
3. 讀取 Obsidian 的 `obsidian.json`（依作業系統路徑）；過濾內建 sandbox 路徑；多個 vault 時詢問選擇
4. 都找不到時：詢問使用者路徑，確認包含 `.obsidian/`，寫入 `~/.claude/CLAUDE.md`

### 語言偵測

讀取 `vault-local.md` 中 `## Vault Structure` 的 `language` 設定。所有輸出使用此語言。

### 資料夾偵測

每個用途按順序匹配第一個存在的候選資料夾：

| 用途 | 候選名稱 |
|------|----------|
| daily | `_yorozuya/daily/`, `Daily/`, `_daily/`, `daily/`, `Journal/`, `journal/` |
| inbox | `Inbox/`, `_inbox/`, `inbox/`, `_Capture/`, `Capture/` |
| research | `_yorozuya/research/`, `_hirameki_analysis/`, `_agent_analysis/`, `Analysis/`, `_analysis/`, `analysis/` |
| journal | `_yorozuya/journal/`, `_hirameki_logs/`, `_agent_logs/`, `Logs/`, `_logs/`, `logs/` |
| handoff | `_yorozuya/handoff/`, `Handoff/`, `_handoff/`, `handoff/` |
| templates | `Templates/`, `_templates/`, `templates/` |

找不到時：詢問使用者、建立資料夾、印出完整路徑、存入 `<vault>/AGENTS.md`。

### 內容資料夾

「內容資料夾」= vault 根目錄下所有第一層資料夾，排除：
- 以 `.` 開頭的資料夾（`.obsidian/`、`.git/` 等）
- `_hirameki_cmds/`
- `## Vault Structure` 中列出的系統資料夾子樹（保留同一第一層資料夾內不相關的同層內容）

掃描內容資料夾時，略過隱藏資料夾、`node_modules` 等 dependency／build 資料夾，以及 vault 為 Git repository 時被 Git 忽略的檔案。

若無內容資料夾：改掃描 vault 根目錄下所有 `.md` 檔案。

---

## Orchestrators（編排指令）

### `/hirameki:triage`

**用途：** Session 結束整合 — wrap、journal、handoff 三步整合成一個引導式流程。
**輸入：** 無。Session 結尾時執行。

#### 共用 session 狀態收集（執行一次）

在第一個 sub-flow 開始前，從以下來源收集 session 脈絡：
- 本次 session 建立或修改的檔案（Edit/Write 歷史）
- 完成和未完成的任務（TaskList）
- 本次 session 做出的關鍵決定

三個 sub-flow 共用此狀態。

#### [1/3] Wrap

執行 wrap 邏輯（見 `/hirameki:wrap` 規格）。顯示完整草稿和寫入路徑。然後：

```
[1/3] Wrap — Action? (save this / save all / skip / edit)
```

- `save this` → 只將目前草稿寫入 `{daily}/YYYY-MM-DD.md`，進入 [2/3]
- `save all` → 寫入目前草稿並一次核准剩餘草稿；每份仍顯示完整內容與路徑，但不再停下詢問
- `skip` → 不寫入，進入 [2/3]
- `edit` → 問「要修改哪個部分？」→ 調整草稿 → 顯示更新後草稿 → 再顯示同一組 action 選項
- 舊的 `save` 視為 `save this`

#### [2/3] Journal

執行 journal 邏輯（見 `/hirameki:journal` 規格），從 session 活動推斷主題。顯示完整草稿和寫入路徑。然後：

```
[2/3] Journal — Action? (save this / save all / skip / edit)
```

沿用同一套 action model。無論選擇，都進入 [3/3]。

#### [3/3] Handoff

執行 handoff 邏輯（見 `/hirameki:handoff` 規格）。顯示完整草稿和寫入路徑。然後：

```
[3/3] Handoff — Action? (save this / save all / skip / edit)
```

完成後顯示摘要：

```
Triage 完成：wrap ✓ / journal – / handoff ✓
```

**規則：**
- 每步都必須顯示完整草稿 — 不因內容多寡自動跳過
- `save all` 生效後視為已核准所有剩餘 triage 草稿；顯示每份草稿與路徑後直接寫入，不再重複詢問
- skip 不中斷流程，永遠繼續下一個 sub-flow
- 各 sub-flow 的寫入邏輯（同天追加 vs. 建新檔）沿用對應基礎指令的規則

---

### `/hirameki:lens <概念>`

**用途：** 主題理解 — arc、立場萃取、bridge、challenge 的四步整合流程。
**輸入：** 單一主題或概念（必填）。若空白則詢問。

執行前印出：
```
Lens on: {概念}
```

#### Step 0 — 共用脈絡（執行一次）

掃描 vault 中有關此主題的所有資料。收集：
- 所有提及此主題的檔案
- 最早和最近的檔案日期（供 arc 時間軸使用）
- 與此主題共同出現的相關主題（供 bridge 建議使用）

#### [1/4] Arc

執行 arc 邏輯（見 `/hirameki:arc` 規格），使用共用脈絡。然後：

```
[1/4] Arc — Action? (save / skip / next)
```

- `save` → 寫入 `{research}/lens/YYYY-MM-DD-{概念}-arc.md`
- `skip` 或 `next` → 進入 [2/4]

#### [2/4] 立場萃取

從 vault 中提取所有關於此主題的明確立場和主張。

規則：
- 只提取直接關於此主題的主張 — 不含周邊提及
- 每個來源一個主張 — 取最具體或最清晰的一條
- 上限：10 個最相關來源
- 純萃取，不組成語氣回答

輸出：

```
## 立場彙整：{概念}

> 分析時間：YYYY-MM-DD HH:MM

| 來源 | 主張 |
|------|------|
| [[檔名]] | 該立場或主張（一句話） |

### 張力
（若兩個以上主張互相矛盾，指名張力所在。
若所有主張方向一致：「未發現顯著張力」。）

### 缺口
（這個主題在 vault 中尚未被探討的角度。）
```

然後：

```
[2/4] 立場萃取 — Action? (save / skip / next)
```

- `save` → 寫入 `{research}/lens/YYYY-MM-DD-{概念}-positions.md`

#### [3/4] Bridge

自動建議最可能的搭配主題（從 Step 0 中共同出現最頻繁的主題，或 arc 中最突出的空白地帶）。執行前顯示建議：

```
[3/4] Bridge — 建議搭配主題：{suggested}
  Action? (save / skip / change-partner)
```

- `save` 或 Enter → 接受，執行 bridge 邏輯，顯示結果，詢問最終存檔
- `skip` → 進入 [4/4]
- `change-partner` → 問「Bridge {概念} 與哪個主題？」→ 執行 bridge

Bridge 邏輯同 `/hirameki:bridge` 規格。存檔路徑：`{research}/lens/YYYY-MM-DD-{概念}-bridge.md`

#### [4/4] Challenge

執行 challenge 邏輯（見 `/hirameki:challenge` 規格），使用 [2/4] 中萃取的立場。然後：

```
[4/4] Challenge — Action? (save / skip / next)
```

- `save` → 寫入 `{research}/lens/YYYY-MM-DD-{概念}-challenge.md`

四步全部完成後顯示：

```
Lens 完成：arc {✓ 已儲存 | – 跳過} / 立場 {✓ 已儲存 | – 跳過} / bridge {✓ 已儲存 | – 跳過} / challenge {✓ 已儲存 | – 跳過}
```

---

### `/hirameki:compose <主題>`

**用途：** 主題創作 — 語氣作答和框架測試的兩步整合流程。
**輸入：** 主題或問題（必填）。若空白則詢問。
**Standalone：** 不需要先執行 `/hirameki:lens`。

執行前印出：
```
Compose on: {主題}
```

#### [1/2] Voice（語氣作答）

執行完整的 reflect 邏輯（見 `/hirameki:reflect` 規格）：
1. 從內容資料夾的完成文章分析寫作風格
2. 萃取 vault 中關於此主題的立場（上限：5 個來源）
3. 使用識別出的風格 + 立場，用作者的語氣寫出回答

輸出同 `/hirameki:reflect` 規格（回答 / 來源 / 信心標注）。然後：

```
[1/2] Voice — Action? (save / skip / edit-question)
```

- `save` → 寫入 `{research}/compose/YYYY-MM-DD-{主題}-voice.md`
- `skip` → 進入 [2/2]
- `edit-question` → 問「修改後的主題或問題？」→ 重新執行語氣步驟

#### [2/2] Frame（框架測試）

執行 frame 邏輯（見 `/hirameki:frame` 規格），以 [1/2] 的語氣輸出為要評估的想法。若 [1/2] 已跳過，問「Frame 哪個想法？」等待輸入。

完整的五問測試 + 裁決輸出。然後：

```
[2/2] Frame — Action? (save / skip / next)
```

- `save` → 寫入 `{research}/compose/YYYY-MM-DD-{主題}-frame.md`

兩步完成後：

```
Compose 完成：voice {✓ 已儲存 | – 跳過} / frame {✓ 已儲存 | – 跳過}
```

---

### `/hirameki:mekiki <輸入>`

**用途：** 外部資源捕獲 — 自動偵測 repo 或文章。
**輸入：** 必填 — GitHub URL、文章 URL、貼上的文字或本機檔案路徑。

#### 輸入路由

| 輸入形式 | 分支 |
|---------|------|
| 配對 `github.com/[^/]+/[^/]+` 或 `^[^/]+/[^/]+$` | Repo 分支 |
| 其他 URL（`http(s)://`） | 文章分支（URL） |
| 本機檔案路徑（以 `/`、磁碟機代號、`./` 開頭且存在於檔案系統） | 文章分支（檔案） |
| 其他 | 文章分支（貼上） |

偵測順序：repo 樣式 → URL → 檔案路徑 → 貼上。

#### Repo 分支

**第一階段 — 抓取（並行）：**
```bash
gh repo view owner/repo --json description,url,stargazerCount,primaryLanguage,updatedAt
gh api repos/owner/repo/readme -q .content | base64 -d
gh api repos/owner/repo/git/trees/HEAD?recursive=1 -q '.tree[].path' | head -150
```
識別 3–5 個關鍵原始碼檔案並抓取內容。

**第二階段 — 分析：**

Track A — 技術提取（總是執行）：對每個有趣的部分提取：模式名稱、是什麼（1–2 句）、為什麼有趣、可遷移至（使用者的實際專案）、具體下一步。

Track B — 引入評估（純模式/示範 repo 跳過）：讀取使用者的 CLAUDE.md 和專案記憶。將 repo 分類為工具/框架/函式庫/模式。建立比較表（功能 / Repo 提供 / 我們目前使用 / 落差）。裁決：**adopt**（附下一步和時程）/ **defer**（附觸發條件）/ **reject**（附替代方案）。

**第三階段 — 驗證（Sonnet 子代理）：** 檢查完整性、可信度、可執行性。不超過 10 個檔案的小型 repo 跳過。

**寫入：** `{research}/mekiki-{repo名稱}.md` — frontmatter：`tags: [mekiki, {裁決}]`、`status: reference`、`source: claude-code`。

#### 文章分支

**第一階段 — 抓取來源：**
- URL → WebFetch
- 檔案 → Read
- 貼上文字 → 直接使用

提取：標題、作者、日期、核心主張（1–3 句）、重要主張清單、vault 中尚未出現的詞彙或概念。

寫入來源筆記至 `{inbox}/YYYY-MM-DD-{slug}.md`：
```yaml
---
tags:
  - inbox
  - mekiki
status: draft
source: external
created: YYYY-MM-DD
url: {來源 URL，若有}
---
```

**第二階段 — 交叉引用：** 掃描內容資料夾和近期 wrap logs，找出觸及相同主張或概念的 vault 筆記。每筆：`[[檔名]]` + 該 vault 筆記與此文章的關係（支持 / 矛盾 / 延伸 / 被延伸）。

**第三階段 — 裁決：**

```
## 值得整合嗎？

**裁決：** integrate / revisit-later / skip
**理由：** 一句話
**下一步：** 一個具體動作（例：建立概念卡片主題、加入寫作 outline、無需進一步行動）
```

寫入後印出 inbox 檔案路徑。

---

## Session

### `/hirameki:next`

**用途：** Session 恢復後定向。
**輸入：** 無。
**不寫入檔案。**

掃描本次 session 的任務清單、檔案活動（建立或修改的檔案）、做出的決定和推送的 commit。產生簡潔的定向摘要：已完成的工作、未處理的事項、下一步。

---

### `/hirameki:wrap [描述]`

**用途：** 進度快照，追加到 wrap log。
**輸入：** 可選重點描述。
**需要的資料夾：** daily、templates。

掃描本次 session 的檔案操作（建立、修改、刪除）和今天的 wrap log。

寫入目標：`{daily}/YYYY-MM-DD.md`
- 檔案不存在 + `templates/daily.md` 存在 → 使用模板
- 檔案不存在，無模板 → 建立 `# YYYY-MM-DD` 標題
- 檔案存在 → 在末尾追加新的 Wrap 區塊，前面加水平分隔線

Wrap 格式：

```
---

## Wrap [HH:MM]

### 已完成
- [本次期間完成的具體項目，每條一句話]

### 進行中
- [已開始但未完成的項目。如果沒有，標註「無」]

### 下一步
- [接下來要做什麼。如果未決定，標註「待定」]
```

規則：
- 時間戳使用本地時間 HH:MM（24 小時制）
- 只追加，不修改之前的 Wrap 區塊
- 有輸入描述時，用它組織 Wrap 內容
- 寫入前顯示草稿和完整路徑，等確認後執行；寫入後印出實際路徑

---

### `/hirameki:journal <描述>`

**用途：** 工作紀錄與推理。
**輸入：** 主題描述（必填）。
**需要的資料夾：** journal + 所有內容資料夾（用於搜尋相關筆記）。

掃描：本次 session 的操作、vault 中與主題相關的筆記、今天在 journal 中已有的檔案。

邏輯：
1. 掃描 `{journal}/` 中今天的 `YYYY-MM-DD-*.md` 檔案
2. 比對檔名和標題與輸入主題的關鍵詞
3. 明確匹配 → 追加模式
4. 模糊匹配 → 列出候選，詢問使用者
5. 沒有匹配 → 建立模式

**建立模式** — 寫入 `{journal}/YYYY-MM-DD-HHMM-{主題摘要}.md`：

```
# {主題}

> 建立時間：YYYY-MM-DD HH:MM

## 背景
為什麼發生這件事。如果 vault 有相關既有筆記，用 [[wiki link]] 引用。

## 做了什麼
具體的操作和決策，附因果敘述。

## 為什麼這樣做
關鍵決策的理由。取捨：選擇了什麼、放棄了什麼。

## 判斷與決策過程
記錄判斷問題、原先判斷、觀察、推論、未驗證假設、新證據、判斷如何改變、目前行動、尚未知與重新檢視條件。沒有實質更新時直接寫明，不補成故事。

## 靈感連結
與其他想法的連結。[[wiki link]] 引用相關筆記。如果沒有，標註「無」。

## 可能的改進
未探索的方向、替代方案、潛在風險。如果沒有，標註「無」。

## 未完成與後續
需要跟進的項目。如果全部完成，標註「無待辦項目」。
```

**追加模式** — 在末尾加上：

```
---

## 追加紀錄 [HH:MM]

### 做了什麼
[新的操作和決策]

### 為什麼這樣做
[新的決策理由]

### 判斷與決策過程
[只記錄新形成或改變的判斷；觀察、推論與假設分開。]

### 靈感連結
[新的連結。如果沒有，標註「無」]

### 可能的改進
[新的方向。如果沒有，標註「無」]
```

同時檢查「未完成與後續」— 若項目已完成，標記完成時間戳。

---

### `/hirameki:decision <決策>`

**用途：** 把會長期約束後續工作的決策提升為有生命週期的獨立節點。
**寫入：** `{journal}/decisions/YYYY-MM-DD-{slug}.md`。

只有當決策會約束未來工作、存在實質替代方案、有回復成本、避免重複退化，或需要跨 session 保存理由時才提升。記錄決策、證據、替代方案、後果與重新檢視條件，狀態為 `active`、`superseded` 或 `closed`。只連結 journal 與 handoff，不重複它們的敘事。寫入前顯示提升依據、完整草稿、受影響路徑與精確 status 變更，等待確認。

---

### `/hirameki:handoff`

**用途：** Session 結束時建立移交文件，供下個 session 接續。
**輸入：** 無。主題和 slug 從 session 活動推斷。
**需要的資料夾：** handoff。

收集：本次 session 建立或修改的檔案、完成/未完成的任務、關鍵決定、遇到的阻礙。

從 session 活動的主要主題推斷話題。若不明確，詢問使用者。

寫入目標：`{handoff}/YYYY-MM-DD-{slug}.md`

```yaml
---
tags:
  - handoff
status: log
source: claude-code
created: YYYY-MM-DD
---
```

```
# Handoff：{主題} — {YYYY-MM-DD}

> Session 結束：YYYY-MM-DD HH:MM

## 完成了什麼
- [已完成項目]

## 目前狀態
[現在事情的狀態 — 什麼做了一半、什麼在等待]

## 未完成線索
- [未完成項目] — [剩餘什麼]

## 關鍵決定
- [決定] — [理由]

## 判斷更新
| 問題 | 原先判斷 | 改變依據 | 目前判斷 | 尚未知 | 重新檢視條件 |
|------|----------|----------|----------|--------|----------------|
只記錄會影響接手的更新；沒有時寫「本次沒有需要接手的判斷更新」。

## 下個 session：從這裡開始
1. [第一件要接手的事]
2. [第二件，若有]

## 注意事項
[下個 session 需要知道的事，避免錯誤或重工。若無則省略此段。]
```

寫入前顯示完整草稿和寫入路徑。寫入後印出路徑。

---

## 理解（Standalone）

### `/hirameki:arc <概念>`

**用途：** 追蹤某概念在 vault 中的演化歷程。
**輸入：** 概念或主題（必填）。
**需要的資料夾：** research + 所有內容資料夾。

邏輯：
1. 檢查 `{research}/arc/` 中今天是否已有同概念的檔案
2. 有 → 追加模式；沒有 → 建立模式

**建立模式** — 寫入 `{research}/arc/YYYY-MM-DD-{概念}.md`：

```
# 概念追蹤：{概念}

> 分析時間：YYYY-MM-DD HH:MM

## 首次出現
最早出現這個概念的檔案及脈絡。引用相關段落（不超過 3 句）。
日期：YYYY-MM-DD

## 演化時間軸
- YYYY-MM-DD | [[檔名]] | 該檔案中這個概念的用法或立場摘要（一句話）

## 目前狀態
這個概念連結到哪些主題、是否有矛盾的用法、是否有 draft 正在發展它。

## 空白地帶
這個概念有哪些面向在 vault 中尚未被探討。
```

**追加模式** — 在末尾加上：

```
---

## 追蹤更新 [HH:MM]

### 演化時間軸（新增）
- [自上次分析以來新出現的提及]

### 狀態變化
- [與上次分析相比有什麼變化。如果沒有，標註「無顯著變化」]

### 空白地帶（更新）
- [重新評估尚未探討的面向]
```

寫入前顯示草稿和路徑。寫入後印出路徑。

---

### `/hirameki:bridge <A> and <B>`

**用途：** 找出兩個主題之間的隱藏連結。
**輸入：** 兩個主題，以「and」、「與」或「と」分隔（必填）。
**需要的資料夾：** 所有內容資料夾。

邏輯：
1. 檢查 `{research}/bridge/` 中今天是否已有同組主題的檔案（不分順序）
2. 有 → 追加模式；沒有 → 建立模式

**建立模式** — 寫入 `{research}/bridge/YYYY-MM-DD-{A}-{B}.md`：

```
# 橋接分析：{A} × {B}

> 分析時間：YYYY-MM-DD HH:MM

## 直接交集
同時提及兩個主題的檔案。每筆：[[檔名]] — 兩個主題在該檔案中如何被關聯。
如果沒有，標註「無直接交集」。

## 橋樑筆記
只提及其中一個主題、但內容可能構成連結的檔案。說明為什麼它可能是橋樑。
上限 5 筆，每筆用 [[wiki link]] 引用。

## 潛在連結假設
1–3 個兩個主題可能的深層連結假設。每個標注信心程度（強 / 中 / 弱）和依據來源。
```

**追加模式：**

```
---

## 追蹤更新 [HH:MM]

### 新發現的交集
- [自上次分析以來新出現的交集或橋樑筆記]

### 假設驗證
- [之前的假設是否有新的支持或反駁證據]
```

寫入前顯示草稿和路徑。寫入後印出路徑。

---

### `/hirameki:challenge <主題>`

**用途：** 分析 vault 中關於某主題的主張的弱點。
**輸入：** 主題或論點（必填）。不需要任何前綴。
**需要的資料夾：** 所有內容資料夾。

對 vault 中每個關於此主題的主張，檢查以下弱點類型（只列適用的）：
- **內部矛盾**：vault 中不同檔案對同一件事說法不一致
- **未驗證假設**：主張建立在未被證明的前提上
- **邏輯跳躍**：論證中缺少中間步驟
- **證據缺口**：主張缺乏支撐的資料或案例

寫入 `{research}/challenge/YYYY-MM-DD-{主題摘要}.md`：

```
## 論點挑戰：{主題}

> 分析時間：YYYY-MM-DD HH:MM

## 主張清單
| 主張 | 來源 |
|------|------|
| [主張內容] | [[檔名]] |

## 弱點分析

### 主張：{主張} — [[來源]]
- 內部矛盾：[細節] — 見 [[檔名]]
- 邏輯跳躍：[細節]
（只列適用的弱點類型。沒有弱點的主張不列出。）

## 整體評估
穩固程度：穩固 / 大致穩固但有缺口 / 需要重大補強
最需要優先處理的 1–3 個弱點。
```

寫入前顯示草稿和路徑。寫入後印出路徑。

---

### `/hirameki:reflect <問題>`

**用途：** 用你自己的語氣回答問題，從 vault 立場中取材。
**輸入：** 問題或主題（必填）。加 `save` 才寫入結果。
**需要的資料夾：** 所有內容資料夾。

#### 第一步 — 分析寫作風格

掃描內容資料夾中的完成文章（排除 `drafts/` 和 `thoughts/` 子目錄）。

提取：句式偏好和典型長度、用詞習慣和反覆出現的短語、論述結構（主張如何引入、支撐、限定）、反覆出現的修辭手法。

#### 第二步 — 萃取立場

搜尋 vault 中與問題相關的筆記。優先：直接探討此主題的內容資料夾筆記、相關的永久概念卡片、作者表達立場的 journal 條目、有相關觀察的 wrap logs。上限：5 個最相關來源。

#### 第三步 — 組成回答

使用識別出的風格和萃取的立場寫出回答：
- 長度與使用者典型文章段落一致
- 使用作者自己的論點，不使用一般知識
- 不引入 vault 中沒有支持的立場
- 若 vault 中有矛盾的立場，呈現張力而非解決它

輸出：

```
[回答]
用作者的語氣回答。一到三段。

[來源]
- [[筆記標題]] — 引用的具體立場或段落
（上限：5 個來源）

[信心標注]
- Vault 支持：哪些部分有直接證據
- 風格推測：哪些部分是根據風格延伸，無直接依據
- 張力：vault 筆記之間發現的矛盾
```

加 `save` 時：寫入 `{research}/reflect/YYYY-MM-DD-{問題摘要}.md`。同問題同天追加。

---

## 創作（Standalone）

### `/hirameki:frame <想法>`

**用途：** 創作前檢查站 — 評估一個想法是否值得追求。
**輸入：** 必填 — 文章想法、產品概念、設計方向，或現有草稿的路徑。
**需要的資料夾：** 所有內容資料夾 + wrap logs + journal。

#### 第一階段：理解想法

從輸入信號判斷類型（文章 / 產品 / 設計）。若是檔案路徑，讀取檔案並提取論點。印出論點和類型後繼續。

#### 第二階段：五問框架測試

**Q1 — Only-I 測試：**「這個想法有什麼只有我能說或能做的？」
掃描 vault 中的獨特經歷、技能或立場。評估：強 / 弱 / 無。

**Q2 — 碰撞掃描：**「我已經做過類似的東西了嗎？」
- Tier 1（已發表）：已吸收 / 相鄰 / 已取代。Tier 1「已吸收」觸發 KILL。
- Tier 2（草稿）：競爭 / 相鄰 / 素材。觸發 CONSOLIDATE 問題，不觸發 KILL。

**Q3 — 賭注：**「讀者/用戶遇到這個之後會有什麼改變？」
重新框架 / 賦予工具 / 引發思考 / 無。「只是提供資訊」= 賭注太低。

**Q4 — 張力：**「有什麼令人驚訝、反直覺或不舒服的部分？」
作者願意承受的矛盾 / 翻轉 / 告白。沒有張力 = 摘要，不是創作。

**Q5 — 證據：**「什麼樣的親身經歷、數據或具體例子讓這個論點有信服力？」
親身體驗 / 研究支撐 / 推測性。

#### 第三階段：裁決

| 裁決 | 條件 |
|------|------|
| **PROCEED** | Q1 強 + Q3/Q4 至少一個強 + 無 Tier 1 已吸收碰撞 |
| **RETHINK** | Q1 弱，或 Tier 1 相鄰碰撞，或 Q3「只是提供資訊」 |
| **KILL** | Q1 無，或 Tier 1 已吸收碰撞，或 Q3 和 Q4 都為空 |
| **CONSOLIDATE** | 多篇 Tier 2 競爭草稿涵蓋相同論點 |

```
## Frame：PROCEED
**論點**：[一句話]
**獨特角度**：[來自 Q1]
**核心張力**：[來自 Q4]
**關鍵證據**：[來自 Q5]
### 動筆前
- [1–2 件需要確定的具體事項]

## Frame：RETHINK
**論點**：[一句話]
**問題**：[哪些問題沒通過，原因]
### 什麼條件讓這個值得做
- [1–3 個具體方向]
### 可以建立在其上的既有作品
- [[檔名]] — [關聯方式]

## Frame：KILL
**論點**：[一句話]
**理由**：[一句話]
**可搶救的部分**：[值得保留的片段，或「無」]

## Frame：CONSOLIDATE
**論點**：[一句話]
**競爭草稿**：
- [[草稿1]] — 優點：X，缺點：Y
**建議主體**：[[最強草稿]] — 因為 [理由]
**從其他草稿吸收的部分**：[具體內容]
**整合後可退場的草稿**：[清單]
```

規則：不要軟化裁決。KILL 就是停止。加 `save` 時寫入 `{research}/frame/YYYY-MM-DD-{slug}.md`。frame 不產生內容。

---

### `/hirameki:critique <檔案>`

**用途：** 多模型寫作評審。
**輸入：** 必填 — 檔案路徑（相對路徑從 vault 根目錄解析）。若空白，找最近修改的草稿並確認。
**需要的資料夾：** vault 根目錄（路徑解析）、`_writing_lab/benchmark/`（輸出）。

#### 第一階段：三模型並行評審

三個維度，各評 1–10 分：
1. **感官密度**：實體細節有多生動具體？
2. **結構張力**：文章是否能拉著讀者往前走？結尾是否落地？
3. **觸動力**：情感是否有落地？讀者明天還記得嗎？

每位評審同時找出：最強的 3 句（附理由）、最弱的 3 句（附理由）、一個結構建議。

**評審 1 — Claude Opus（Agent，model: opus）**
讀取檔案並評審。對三個維度評分。坦率直說。用 vault 語言撰寫。

**評審 2 — Codex GPT（Bash，codex CLI）**
```bash
codex exec "閱讀以下文章並作為文學批評家評審。
對三個維度各評 1-10 分：感官密度、結構張力、觸動力。
找出：最強的 3 句、最弱的 3 句（附理由）、一個結構建議。
用 vault 語言撰寫。誠實且批判。

$(cat '{file_path}')"
```

**評審 3 — Gemini Pro（Bash，gemini CLI）**
```bash
gemini -p "$(cat <<'PROMPT'
閱讀以下文章並作為文學批評家評審。
對三個維度各評 1-10 分：感官密度、結構張力、觸動力。
找出最強、最弱的句子和一個結構建議。
用 vault 語言撰寫。
$(cat '{file_path}')
PROMPT
)" --allowed-mcp-server-names none
```

若 codex 或 gemini CLI 不可用，跳過該評審並在輸出中標注。

#### 第二階段：整合結果

比較表（Opus / Codex GPT / Gemini Pro）。共識（2/3 以上一致）。2 個以上評審選中的最強句。2 個以上評審標記的最弱句。各家獨有觀點。

#### 第二‧五階段：寫入評審檔案

各維度共識分數 = 三位評審的平均值，四捨五入至小數點一位。

寫入 `{vault}/_writing_lab/benchmark/YYYY-MM-DD-{文章slug}-review.md`：

```yaml
---
tags:
  - writing-lab
  - review
status: reference
source: claude-code
created: YYYY-MM-DD
article: "{文章檔名}"
scores:
  sensory: {平均}
  structure: {平均}
  resonance: {平均}
  overall: {三者平均}
models:
  - opus
  - codex
  - gemini
phase: initial
---
```

印出檔案路徑。問：「要根據這些意見改稿嗎？還是先跑終審？」

#### 第三階段：終審（選擇性，使用者要求後執行）

改稿後，以 Opus + Codex GPT 並行執行終審。

兩位評審都確認：初審每個問題的修正狀態（已修正 / 部分修正 / 未修正 / 新問題引入）。再做整體印象 fresh read：三個維度重新評分、新問題、最強的 3 個時刻、一個剩餘建議。

將終審結果追加到同一個 benchmark 檔案。將 frontmatter 的 `phase` 更新為 `final` 並更新分數。

---

## Vault

### `/hirameki:pulse [week|patterns]`

**用途：** Vault 狀態概覽（三種模式）。
**輸入：** 無 / `week` / `patterns`
**不寫入檔案。**

#### 無參數模式 — 即時概覽

掃描：所有內容資料夾（深度 2 層）、wrap logs 最近 7 天。

**內容主題** — 每個內容資料夾及其子目錄：名稱、筆記總數、草稿數、最近修改日期。狀態：活躍（7 天內有修改）/ 休眠。

**近期活動** — 最近 7 天修改的檔案，按時間倒序。每筆：檔名、所屬資料夾、修改時間、變更性質（新建 / 修改 / 大幅改寫）。上限 15 筆。

**Vault 概覽** — 總檔案數、內容資料夾數量、最近 7 天活躍的資料夾。

空的區塊標注「無」，不跳過。

#### `pulse week` — 週回顧與落差分析

讀取：所有內容資料夾最近 7 天的修改紀錄、最近 7 天的 wrap logs。

**本週進度** — 每個有活動的內容資料夾：名稱、推進了什麼、下一步。

**近期動態** — 本週新增或修改的筆記，哪些接近完成。

**落差分析** — 比對 wrap logs 中的優先事項與實際檔案變更：
- 說了重要但沒動手的（聲稱優先但無對應檔案變更）
- 沒提到但花了時間的（有檔案變更但 wrap logs 未提及）

如果 wrap logs 不足 3 天，標注「紀錄不足，落差分析可能不準確」。

#### `pulse patterns` — 潛流與聚攏分析

掃描：所有內容資料夾、wrap logs（最近 30 天）、所有 inbox。

**潛流主題** — 反覆出現但沒有獨立文章的主題。標準：出現在 3 個以上不同檔案中，且沒有獨立文章或 draft。每個：主題名稱、出現次數和涉及檔案數（最多 5 個 [[wiki link]]）、判斷（值得展開嗎）。上限 10 個，按出現頻率倒序。

**聚攏中的想法群** — 3 篇以上涉及相似概念、撰寫時間分布不同、但沒有共同上層分類的筆記群。每個：建議群組名稱、涉及筆記（最多 5 個 [[wiki link]]）、共同主題摘要（2–3 句）、成熟度（高 / 中 / 低）、建議發展方向（文章 / 專案 / 概念框架 / 繼續累積）。上限 5 個，按成熟度倒序。

---

### `/hirameki:harvest [save]`

**用途：** 從既有內容中收割可行動的想法。
**輸入：** 可選 `save` 寫入摘要。
**需要的資料夾：** research、wrap logs、inbox + 所有內容資料夾。

掃描：所有內容資料夾、wrap logs（最近 30 天）、所有 inbox。

輸出 — 七個類別，各最多 5 個：

**可以寫的文章** — 已有足夠素材可以發展的主題。每筆：建議標題、素材來源（[[檔名]] 清單）、缺什麼才能動筆。

**可以做的工具或專案** — 筆記中提到的工具需求、流程痛點或明確的產品想法。每筆：描述、來源、預估複雜度（小 / 中 / 大）。

**值得研究的主題** — 被提及但未深入探討的外部概念或技術。每筆：主題、vault 中提及的脈絡、為什麼值得研究。

**可以聯繫的人或社群** — 被提及且與目前方向相關的人物或組織。每筆：名稱、vault 脈絡、聯繫理由。如果沒有，標注「無」。

**適合換個媒介的想法** — 更適合以不同形式呈現的內容（影片、視覺圖表、演講、電子報、podcast 等）。每筆：想法摘要、建議媒介、為什麼這個形式比文字更合適。

**尚未變現的價值** — 有但還沒有轉換成收益的專業知識或能力。每筆：技能或知識描述、可能的變現形式、vault 依據。如果沒有，標注「無」。

**可以畢業的想法** — 半成形但已有足夠密度可以獨立成筆記的想法。每筆：來源位置（[[檔名]] + 段落描述）、核心主張（一句話）、建議歸屬的內容資料夾、與哪些既有筆記相關。

畢業標準：有明確的核心主張、與 vault 中至少一個既有主題相關、有足夠的內容密度。

### 畢業流程（無論是否加 save，都是兩階段）

列出候選後暫停，等使用者確認哪些要執行畢業。

對每個選中的想法：
1. 顯示即將建立的完整路徑，等再次確認
2. 在對應的內容資料夾建立新的 markdown 檔案：標題、核心主張、出處脈絡、vault 關聯（[[wiki link]] 格式）、待展開的方向
3. 寫入後印出實際路徑

加 `save` 時：將主要收割摘要寫入 `{research}/harvest/`。同天追加更新。

---

### `/hirameki:graduate <筆記>`

**用途：** 將筆記升格為穩定的永久概念卡片。
**輸入：** 筆記標題或 [[wikilink]]（必填）。
**需要的資料夾：** 所有內容資料夾。

步驟：
1. 在 vault 中找到該筆記
2. 讀取並評估：是否有明確的核心主張？是否足夠穩定可以成為參考資料？
3. 驗證/補充 frontmatter：確認 `tags`、`status: reference`、`source` 都存在
4. 建議連結到 vault 中相關的概念卡片
5. 顯示提議的變更，等確認後才寫入
6. 寫入後印出路徑

---

### `/hirameki:tasks [天數|stuck]`

**用途：** 從 wrap logs 和 journal 彙整下一步行動。
**輸入：** 可選 — 天數（預設 3）或 `stuck` / `stuck N`。
**不寫入檔案。**

#### 預設模式 — 行動彙整

掃描最近 N 天的 `{daily}/YYYY-MM-DD.md`（從每個 Wrap 區塊提取「下一步」）。掃描今天和昨天的 `{journal}/YYYY-MM-DD-*.md`（提取「未完成與後續」中未標記完成的項目）。

1. 收集下一步行動
2. 去重和排序：正規化後將相同任務歸組，按出現次數倒序，再按最近出現時間倒序
3. 輸出：附來源的有序清單。出現 3 次以上的項目加 ⚠ 前綴。

#### Stuck 模式 — `tasks stuck [N]`

掃描 N 天（預設 7）。找出在「下一步」區塊出現 2 次以上且從未出現在「完成」區塊的任務。分類為：**blocked（被阻擋）** / **deferred（延後）** / **forgotten（遺忘）** / **persistent（持續）**。

規則：唯讀，不修改任何檔案。

---

## 維護

### `/hirameki:tidy [tags|fix|full|lint]`

**用途：** Frontmatter 屬性健檢與清理。
**輸入：** 可選模式參數。
**需要的資料夾：** 所有內容資料夾 + inbox + daily-notes。

**模式：**

| 呼叫方式 | 執行內容 |
|----------|---------|
| `tidy`（無參數） | 缺漏欄位 + 一致性檢查 |
| `tidy tags` | 僅 tag 收斂分析 |
| `tidy fix` | 缺漏欄位 + 一致性 + 自動修正 |
| `tidy full` | 全部區塊 |
| `tidy lint` | 僅內容健檢 |

**掃描範圍：** 所有內容資料夾（遞迴）、所有 inbox 檔案、wrap logs（最近 30 天）。略過隱藏資料夾、`node_modules` 等 dependency／build 資料夾，以及可取得時被 Git 忽略的檔案。

#### 缺漏欄位（tidy / fix / full）
- 無 frontmatter 的檔案
- 有 frontmatter 但缺少 `tags`、`status` 或 `source`
- 必填欄位為空或型別不正確

#### 逐篇 frontmatter review（tidy / fix / full）
先做輕量偵測。需要處理 frontmatter 的文章為 50 篇以下時，只 review／處理那些文章，不擴張成全 vault review，也不產生全 vault ledger。超過 50 篇才 review 範圍內每一篇，並在報告旁寫出逐篇 CSV ledger。分類為 `pass`、`pass-project-schema`、`auto-fixable`、`requires-judgment` 或 `exclude-candidate`。只有彙總數字不算完成全面 review。

#### 一致性檢查（tidy / fix / full）
- `status` 不在允許值：`published`、`draft`、`reference`、`outline`、`spec`、`log`、`archive`
- `source` 不在允許值（若欄位存在）：`self`、`claude-code`、`codex`、`agent`、`external`
- tag 大小寫不一致的同義 tag（例：`AI-alignment` vs `ai-alignment`）
- tag 中的底線 vs 連字號不一致
- `topic` 與 tag 之間的明顯重複

上述 status／source 是預設語彙，不代表所有專案自訂值都是壞資料。專案語彙優先。`source` 內的 URL 是有效 provenance；可以提出 `source: external` + `source_url` 遷移，但不得自動執行。

#### 冗餘檢查（full 限定）
- 超過 6 個 tag 的檔案
- `created` 格式不一致（應為 YYYY-MM 或 YYYY-MM-DD）

#### Tag 收斂分析（tags / full）
統計整個 vault 的 tag 使用情況：
- 前 10 個最常用的 tag（核心 tag）
- 語意相似但命名不同的 tag（合併候選群組）
- 只出現一次的 tag（孤立 tag — 逐一列出）

#### 內容健檢 — 僅限 lint 模式

**矛盾偵測：** 關於同一主題做出互相衝突主張的筆記對。每對：筆記 A [[檔名]] — 主張；筆記 B [[檔名]] — 矛盾主張；嚴重程度：直接矛盾 / 張力 / 演進（作者隨時間改變想法）。

**過時主張：** `status: published` 或 `reference` 且超過 90 天未修改的筆記。每筆：[[檔名]] — 最後修改日期 — 主題摘要 — 問題：這個主張現在還準確嗎？

**孤立筆記：** 從其他筆記沒有任何傳入 [[wiki link]] 的筆記（排除 daily、inbox、系統資料夾）。每筆：[[檔名]] — 建立日期 — 主題 — 建議。

**死連結：** 指向不存在檔案的 [[wiki link]]。每筆：來源 [[來源筆記]] — 破損連結文字 — 建議。

Lint 模式是唯讀的。Lint 輸出後，若任何區塊 N > 0，追加：

```
## Cross-reference 建議

### 深入矛盾主題
（僅限 contradictions N > 0）
對最多矛盾的主題執行 `/hirameki:lens <主題>` 第 4 步（challenge）做深入分析。
最多矛盾的主題：{主題}

### 追蹤 vault 模式
（僅限孤立 tag ≥ 5 或孤立筆記 ≥ 5）
執行 `/hirameki:pulse patterns` 查看整個 vault 的反覆主題和缺口。

### 處理過時主張
（僅限 stale claims N > 0）
對仍適用的過時主張：執行 `/hirameki:graduate <筆記>` 升格為穩定概念卡片。
對已過時的主張：將 `status` 改為 `archive`。
需要關注的過時檔案：N 個
```

若所有區塊 = 0，完全省略 cross-reference 段落。

#### Fix 模式（僅 fix 輸入時）

顯示所有計畫變更的完整清單。等確認後才執行。

可以自動修正的：
- 新增缺漏的 frontmatter 框架（空 tags + `status: draft`）
- 統一 tag 大小寫（多數決）
- 統一 tag 中的底線為連字號
- `topic` 與 tag 重複時移除 `topic`

需要逐一確認的：
- 合併語意相似的 tag
- 精簡超過 6 個 tag 的檔案
- 刪除孤立 tag

修正後重新計算健康度分數，輸出差異摘要。

**寫入：** `{research}/tidy/YYYY-MM-DD.md`。同天追加更新（含健康度變化）。每次最多回報 50 個問題。

---

### `/hirameki:__init`

**用途：** 首次設定和 vault 設定。
**輸入：** 無。

#### Mode A：首次設定

當 `<vault>/AGENTS.md`、`vault-local.md`、`CLAUDE.md` 中都沒有 `## Vault Structure` 時執行。

**第一步 — Vault 偵測：** 嘗試 CWD → CLAUDE.md 路徑 → obsidian.json（過濾內建 sandbox）。多個時詢問。都找不到：詢問使用者。

**第二步 — 語言：** 詢問：繁體中文 / English / 日本語 / 其他。

**第三步 — 資料夾解析：** 將每個用途匹配到第一個存在的候選（見上方資料夾表）。若無匹配：詢問使用者在哪裡建立，確認後建立。

**第四步 — 寫入設定：** 分兩處寫入，各自對應不同讀者。
```
# ~/.claude/vault-local.md  (per-machine)
## Vault Structure
vault: {完整 vault 路徑}
language: {語言}
```
```
# {vault}/AGENTS.md  (隨 vault 移動)
## Vault Structure
daily: {資料夾名稱}/
inbox: {資料夾名稱}/
research: {資料夾名稱}/
journal: {資料夾名稱}/
handoff: {資料夾名稱}/
templates: {資料夾名稱}/
```

**第五步 — 共享 policies vault（選擇性）：** 詢問。若是：確認路徑、建立 symlink `~/.claude/rules/policies/ → {policies 路徑}`、在 vault-local.md 加入 `shared-policies: {路徑}`。

**第五步 B — 個人 policies vault（選擇性）：** 詢問。同第五步流程，使用 `~/.claude/rules/personal/`。

**第六步 — Reference doc 同步：** 檢查 `{vault}/_hirameki_cmds/`。不存在 → 建立並複製對應語言的 reference docs。存在且非空 → 詢問是否覆蓋。

語言對應：
- 繁體中文 → `hirameki-cmds-short-zh-TW.md` + `hirameki-cmds-full-zh-TW.md`
- 日本語 → `hirameki-cmds-short-ja.md` + `hirameki-cmds-full-ja.md`
- English 或其他 → `hirameki-cmds-short.md` + `hirameki-cmds-full.md`

#### Mode B：重新設定

當設定已存在時執行。詢問要更新什麼（語言 / 特定資料夾 / 共享 policies / 個人 policies / reference docs / 全部重來）。只修改選擇的項目。語言與 vault 路徑寫入 `vault-local.md`，資料夾路徑寫入 `<vault>/AGENTS.md`。

---

## 寫入行為一覽

| 指令 | 寫入位置 | 觸發條件 | 同天重複 |
|------|----------|----------|----------|
| `triage` | daily + journal + handoff | 逐步（save/skip） | 各 sub-flow 沿用對應基礎指令的行為 |
| `lens` | research/lens/ | 逐步（save/skip） | 每步各自建檔 |
| `compose` | research/compose/ | 逐步（save/skip） | 每步各自建檔 |
| `wrap` | daily | 總是 | 追加新 Wrap 區塊 |
| `journal` | journal | 總是 | 同主題追加，不同主題建新檔 |
| `handoff` | handoff | 總是 | 同日期覆蓋 |
| `arc` | research/arc/ | 總是 | 同概念追加 |
| `bridge` | research/bridge/ | 總是 | 同組主題追加 |
| `challenge` | research/challenge/ | 總是 | 同主題追加 |
| `reflect` | research/reflect/ | 加 `save` | 同問題追加 |
| `frame` | research/frame/ | 加 `save` | 每個想法建新檔 |
| `mekiki`（Repo） | research/ | 總是 | 每個 repo 建新檔 |
| `mekiki`（文章） | inbox/ | 總是 | 每篇文章建新檔 |
| `graduate` | 內容資料夾 | 確認後 | 每次建新檔 |
| `harvest` | research/harvest/ | 加 `save` | 追加更新 |
| `tidy` | research/tidy/ | 總是 | 追加更新 |
| `critique` | _writing_lab/benchmark/ | 總是 | 每次建新檔 |
| `tasks` | 不寫入 | — | — |
| `next` | 不寫入 | — | — |
| `pulse` | 不寫入 | — | — |

## 共用規則

- 所有時間戳使用本地時間 HH:MM（24 小時制）
- 所有檔案引用使用 [[wiki link]] 格式
- 所有寫入指令在執行前顯示預覽和完整路徑，等確認後才執行；執行後印出實際路徑
- 輸出語言從 `~/.claude/vault-local.md` 的 `## Vault Structure` 讀取
- Vault 路徑總是在執行時從 vault-local.md 解析、資料夾從 `<vault>/AGENTS.md` 解析 — 永遠不硬編碼
