---
description: Write or append a work log entry. Use "review" to extract rule updates from recent corrections.
---

Resolve vault configuration through the umbrella Hirameki adapter to get the vault path, journal folder, content folders, and language. This reference does not read another agent's configuration.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Write or append a work log and reasoning record for the given topic.

Input: $ARGUMENTS (topic description — optional). If the first argument is `review`, use Review mode below before any journal drafting or topic confirmation.
- If $ARGUMENTS is provided, use it as the topic directly.
- If $ARGUMENTS is empty, infer the topic from session activity (recently modified files, tasks completed, decisions made). Show the inferred topic as a single line — "Topic: {inferred topic} — proceed?" — and wait for a yes/no confirmation before continuing. Do NOT ask open-ended questions.

Before candidate selection, load and apply `references/capabilities/session-traces.md` under the currently loaded Hirameki skill root. Preserve this workflow's existing write gate.

Scan sources:
- Session activity
- Existing notes in the vault related to the topic (search all content folders)
- Existing journal files in the journal folder starting with today's date

Execution logic:
1. Scan the journal folder for all YYYY-MM-DD-*.md files starting with today's date
2. Compare each file's name and title against the keywords of the input topic
3. If a clear match is found → Append mode
4. If a possibly related file is found but uncertain → List candidates and ask whether to append or create new
5. If no match → Create mode

### Create mode

Create a file in the journal folder. Filename format: `YYYY-MM-DD-HHMM-{topic-slug}.md` (HHMM is the local time of creation, no colon).

Filename slug language rules:
- Language is Traditional Chinese → use Chinese (e.g. `2026-03-03-1430-hirameki指令精煉.md`)
- Language is Japanese → use Japanese (e.g. `2026-03-03-1430-hirameki指令改善.md`)
- Language is English or other → use English (e.g. `2026-03-03-1430-hirameki-command-refactor.md`)

Replace spaces with hyphens. Avoid special characters.

File structure:

```
---
tags:
  - journal
  - {relevant-topic-tags}
status: log
source: codex
actions:
  - type: {action-type}
    project: {project-name}
corrections: 0
---

# {topic}

> Created: YYYY-MM-DD HH:MM

## Background
What prompted this. If related prior notes exist in the vault, reference them with [[wiki links]].

## What was done
Specific actions and decisions taken, with cause-and-effect narrative.

## Why this approach
Reasoning behind key decisions. If trade-offs were made, describe what was chosen and what was set aside. Omit this section when 判斷與決策過程 already carries the reasoning; do not write the same prose twice.

## 判斷與決策過程

- 判斷的問題：
- 起點（原先判斷；尚未形成時寫「未形成判斷」）：
- 當時根據：
  - 觀察：
  - 推論：
  - 尚未驗證的假設：
- 新出現的證據或經驗：
- 判斷結果（形成／改變／維持，以及原因）：
- 行動狀態（提案／已決定／已執行／結果已驗證）：
- 現場（原始素材；每條標來源：可回查對話／spec／工具輸出／僅 compaction 摘要）：
- 仍然不知道什麼：
- 什麼情況值得重新檢視：

實質更新的判準：只有 session 明示新判斷，或新證據使結論、信心或行動產生可指認的形成、改變或有理由的維持，才算實質更新；未明說者留空，不合併、不補寫。 If there is no substantive update by this criterion, write only: "本次沒有需要保存的判斷更新。" Do not invent a trajectory.

## Emerging clues
Optional: preserve source/context, observation, interpretation and unknown using session-traces.md. Omit when empty.

## Inspiration connections
Links to other ideas, possible extensions, cross-topic connections. Use [[wiki links]]. If none, write "None."

## Possible improvements
Unexplored directions, alternatives, potential risks worth investigating. If none, write "None."

## Corrections
Things the user corrected the agent on during this session. Each item = one correction.
Format: "Wrong: [what the agent did] → Right: [what the user wanted]（範圍：本次任務／專案慣例／長期偏好／範圍未定）"
Add the scope tag only when it is clear from the conversation; otherwise write 範圍未定. A one-off instruction is not a long-term preference.
If no corrections happened, write "None."
These corrections are candidates for agent-guidance updates after review and explicit user approval; only 長期偏好 and repeated 專案慣例 are candidates.

## Open items
Things still to follow up on. If all done, write "No open items."
```

### Append mode

Add to the end of the matched file:

```
---

## Addendum [HH:MM]

### What was done
[New actions and decisions]

### Why this approach
[Reasoning for new decisions]

### 判斷與決策過程

[Record only judgment that formed, changed, or was maintained against new evidence, using the Create-mode fields. Keep observations, inferences, and unverified assumptions distinct. If there is no substantive update, write "本次沒有需要保存的判斷更新。"]

### Emerging clues
[Optional new clues with source/context, observation, interpretation and unknown; omit when empty.]

### Inspiration connections
[New connections or extensions. If none, write "None."]

### Possible improvements
[New directions to explore. If none, write "None."]
```

Optional block, only when this session produced the outcome of a judgment recorded in an earlier entry (same file or another journal file):

```
### 後續結果（接回 YYYY-MM-DD-HHMM 判斷）
- 當時預期：
- 實際結果：
- 後來修正：
- 原條目：[[YYYY-MM-DD-HHMM-{topic-slug}]]
```

The earlier text is never rewritten; the follow-up links back to it.

Also check the "Open items" section — if any items are now complete, mark them with "✓ Done [HH:MM]".

Rules:
- Timestamps use local time in HH:MM format (24-hour)
- Show filename, mode (create / append), content summary, and full path, then wait for confirmation before writing
- Print the full path after writing
- Append mode does not modify existing content — only adds to the end and updates completion status
- `Why this approach` explains the rationale for the action taken. `判斷與決策過程` records how a judgment formed or changed; do not repeat the same prose in both sections. Sections are written only when there is material: omit `Why this approach` when the judgment section carries it; when nothing substantive happened, the judgment section is only its one-line "no update" sentence.
- 判斷與行動分開：「判斷結果」說判斷本身，「行動狀態」只用四態之一（提案／已決定／已執行／結果已驗證），不混寫。
- 現場每條標明來源類型；只剩 compaction 摘要時標「僅 compaction 摘要」，拿不到的理由寫未知，不補。
- Label important claims by evidence level: explicitly stated, reasonably inferred, or insufficient data. Never turn missing evidence into a smooth narrative.
- 證據硬閘：「當時根據」與「新出現的證據或經驗」各至少包含一項本次對話可直接追溯的具體事實（原句、數值、命令或輸出片段、具名檔案／操作結果）；只寫概括結論不合格。
- 現場（原始素材）：最多六個依 session 發生順序排列的原始證據單位；每點標明來源角色或操作，保留最小充分原句、數字或輸出片段；未明說的利害關係、動機與因果不得補寫；某類材料不存在就省略，不為湊數改寫。
- 由判斷導致的行動寫在 `What was done` 並明指出自該判斷；判斷未產生行動就直說沒有。
- Frontmatter `actions` array is required in Create mode. Use action types from this list:
  `test-rewrite` `test-fix` `code-review` `config-update` `hook-setup`
  `automation` `feature` `bug-fix` `refactor` `research` `vault-write`
  `git-ops` `design` `infra` `skill-dev` `debug`
  If none fits, use a short descriptive slug. Project name should match the short name (e.g. journal, library, dotclaude, asagiri, hirameki, vault).

Write output in the language specified in `## Vault Structure` → `language`.

---

## Lesson entries — `{journal}/lessons/`

A lesson preserves a traceable reusable point within an explicit scope. Apply the session-traces.md selection contract: one event may qualify without cross-project generalization, but an untested hunch remains an emerging clue. State the evidence count and limits. A fully covered lesson is referenced or appended rather than duplicated; proposing it never promotes a rule. It is proposed by `/hirameki:triage`; there is no separate command. Successes qualify as much as failures.

Before selecting a lesson target, perform the bounded lesson lookup in session-traces.md across dates under `{journal}/lessons/`. Fully covered evidence uses reference-existing with no write. New evidence for one verified existing lesson uses the Lesson append procedure there, preserving its original bytes and showing the complete append block and existing target before approval. Unresolved coverage stays explicit and does not authorize a new duplicate.

New-entry target only: `{journal}/lessons/YYYY-MM-DD-{slug}.md` (create the folder on first approved use). Slug language follows the journal rule. Check that this target is absent; never overwrite a collision. The template below is for new entries, not append mode.

```
---
tags:
  - journal
  - lesson
status: reference
source: codex
created: YYYY-MM-DD HH:MM
---

# {one-line lesson}

## 適用範圍
Where it applies and where it does not.

## 教訓
The reusable point, in a few sentences.

## 反例
[[link to a real counterexample]] with one line on why it cuts the other way — or "尚無反例".

## 重新檢查條件
Observable events that should trigger a re-check.

## 未驗證的部分
(only when there is material)

## 來源
[[originating journal entry]], raw evidence links, and the record that holds the counterexample.
```

Do not retell the event; link to where it is recorded. One fact lives in one place: wrap may summarise the outcome and link here, the journal entry keeps the judgment at the time, the raw record keeps the evidence.

---

## Review mode — `journal review`

This is a permanent shortcut to `tidy review`, not a parallel rule-review implementation.
Before ordinary journal topic inference, recognize `review [N]` and load the delivered
`capabilities/review.md` under the loaded skill's `references/`.
Preserve the requested scope and date window, then execute that shared contract only.
No journal draft, save menu or rule write is implied by a review request.
