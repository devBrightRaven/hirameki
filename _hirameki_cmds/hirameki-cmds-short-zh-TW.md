# Hirameki 指令

在 Claude Code CLI 中使用。所有指令以 `/hirameki:` 開頭。

---

## Orchestrators（編排指令）

從這裡開始 — 每個 orchestrator 把相關的基礎指令整合成一個引導式流程。各基礎指令仍可單獨呼叫。

### `/hirameki:triage`
Session 結束整合：依序執行 wrap → journal → handoff。每步顯示完整草稿，選擇 save / skip / edit 後繼續。
無參數。Session 結尾時執行。

### `/hirameki:lens <概念>`
主題理解流程：arc → 立場萃取 → bridge → challenge。每步可單獨 save 或 skip。
輸入：單一概念或主題（必填）。

### `/hirameki:compose <主題>`
主題創作流程：用你的語氣作答 → 五問框架測試。每步可單獨 save 或 skip。
輸入：主題或問題（必填）。Standalone — 不需要先執行 `/hirameki:lens`。

### `/hirameki:mekiki <輸入>`
外部資源捕獲。自動偵測輸入類型：
- GitHub URL 或 `owner/repo` → Repo 分析（技術提取 + adopt/defer/reject 裁決）
- 文章 URL → 網路文章捕獲 + vault 交叉引用
- 貼上文字或本機檔案路徑 → 文章捕獲 + vault 交叉引用

Repo 輸出：`{research}/mekiki-{repo名稱}.md`
文章輸出：`{inbox}/YYYY-MM-DD-{slug}.md`

---

## Session

### `/hirameki:next`
Session 恢復後定向。整理已完成的工作、待處理事項和下一步。無輸入。不寫入檔案。

### `/hirameki:wrap [描述]`
進度快照。記錄已完成、進行中、下一步 — 追加到當天的 daily note。一天可執行多次。
可選輸入：本次 wrap 的重點描述。
寫入：`{daily}/YYYY-MM-DD.md`

### `/hirameki:journal <描述>`
工作紀錄與推理。記錄做了什麼、為什麼、靈感連結、未完成事項。同主題同天追加；不同主題建新檔。
輸入：主題描述（必填）。
寫入：`{journal}/YYYY-MM-DD-HHMM-{主題}.md`

### `/hirameki:handoff`
Session 移交文件。記錄當前狀態、未完成線索、下個 session 的接續指引。從 session 活動自動推斷主題。
寫入：`{handoff}/YYYY-MM-DD-{slug}.md`

---

## 理解（Standalone）

這些是 `/hirameki:lens` 整合的基礎指令，可以直接單獨呼叫。

### `/hirameki:arc <概念>`
概念演化追蹤。顯示某概念在 vault 中的首次出現、演化時間軸、目前狀態與空白地帶。
寫入：`{research}/arc/YYYY-MM-DD-{概念}.md`。同概念同天追加。

### `/hirameki:bridge <A> and <B>`
兩主題間的隱藏連結。找出直接交集、橋樑筆記，並提出深層連結假設。
寫入：`{research}/bridge/YYYY-MM-DD-{A}-{B}.md`。同組主題同天追加。

### `/hirameki:challenge <主題>`
論點弱點分析。對 vault 中關於此主題的每個主張，逐一檢查內部矛盾、未驗證假設、邏輯跳躍與證據缺口。
寫入：`{research}/challenge/YYYY-MM-DD-{主題}.md`

### `/hirameki:reflect <問題>`
Vault 語氣作答。分析你的寫作風格、萃取你的立場，用你的語氣寫出一段回答，附上出處引用與信心標注。
加 `save` 才寫入：`{research}/reflect/YYYY-MM-DD-{問題}.md`

---

## 創作（Standalone）

這些是 `/hirameki:compose` 整合的基礎指令。

### `/hirameki:frame <想法>`
創作前檢查站。五問框架（Only-I 測試、碰撞掃描、賭注、張力、證據）。四種裁決：PROCEED / RETHINK / KILL / CONSOLIDATE。不產生內容，只評估內容是否應該存在。
加 `save` 才寫入：`{research}/frame/YYYY-MM-DD-{slug}.md`

### `/hirameki:critique <檔案>`
多模型寫作評審。三位評審同時執行（Opus / Codex GPT / Gemini Pro），各自對感官密度、結構張力、觸動力評分（1–10）。整合為比較表，重點標出分歧。
寫入：`{vault}/_writing_lab/benchmark/`

---

## Vault

### `/hirameki:pulse [week|patterns]`
三種模式：
- **`pulse`** — 即時概覽：內容主題、近期活動、統計數據。
- **`pulse week`** — 週回顧：比對聲稱的優先事項與實際檔案變更，找出落差。
- **`pulse patterns`** — 潛流與聚攏：找出反覆出現但沒有獨立文章的主題，以及正在形成的想法群。
不寫入檔案。

### `/hirameki:harvest [save]`
從既有內容中收割可行動的想法。七個類別（各最多 5 個）：可以寫的文章 / 可以做的工具或專案 / 值得研究的主題 / 可以聯繫的人或社群 / 適合換個媒介的想法 / 尚未變現的價值 / 可以畢業的想法。
畢業類別：兩階段，確認候選清單後才建立檔案。
加 `save` 才寫入摘要：`{research}/harvest/`

### `/hirameki:graduate <筆記>`
將筆記升格為穩定概念卡片。驗證 frontmatter、設定正式 status、連結相關卡片。

### `/hirameki:tasks [天數|stuck]`
從 daily notes 和 journal 彙整下一步行動，去重後依出現頻率排序。出現 3 次以上的項目標記為拖延信號。
- **`tasks`** — 最近 3 天
- **`tasks N`** — 回溯 N 天
- **`tasks stuck`** — 從未出現在「完成」區塊的反覆未完成任務
不寫入檔案。

---

## 維護

### `/hirameki:tidy [tags|fix|full|lint]`
Frontmatter 屬性健檢。預設只跑缺漏 + 一致性（輕量）。
- **`tidy`** — 缺漏 + 一致性檢查
- **`tidy tags`** — tag 收斂分析（核心標籤、孤立標籤、合併建議）
- **`tidy fix`** — 缺漏 + 一致性 + 自動修正
- **`tidy full`** — 全部區塊
- **`tidy lint`** — 內容健檢（矛盾、過時主張、孤立筆記、死連結）

寫入：`{research}/tidy/`

### `/hirameki:__init`
首次設定：偵測 vault、設定語言、解析資料夾、寫入 `~/.claude/vault-local.md`。每台機器執行一次。已有設定時執行進入 Mode B（重新設定）。

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

所有寫入檔案的指令都會在寫入前顯示預覽和完整路徑。

輸出語言在首次執行 `/hirameki:__init` 時設定，儲存在 `~/.claude/vault-local.md` 中。
