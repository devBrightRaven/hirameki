---
description: End-of-session checkpoint — decides which of wrap, journal, handoff, lesson
  add value this time, shows a draft for each proposed one, and lets you save, skip,
  or edit before moving on. Wrap and journal and handoff remain callable individually.
---

Read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path and folder locations: daily, journal, handoff, templates.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS — ignored. Triage takes no arguments. (The user may adjust the plan at an `Action?` prompt; see Step 0.5.)

## Action model

Every sub-flow uses `save this / save all / skip / edit`.

For every existing-note append, first load the delivered
`references/capabilities/exact-append.md` under this workflow's own plugin/skill root.
Freeze and display its prepared plan before approval; apply that unchanged plan
only after the save action. No native Edit/Write or hand-built append fallback.
If preparation or byte verification is unavailable, stop and retain the draft.
Any append failure stops the batch without automatic retry. A changed append
plan requires fresh approval after redisplay; active save-all cannot cover it.
These append rules take precedence over the generic redisplay/retry rules below.
Prepared tool output is not a visible assistant reply. Before any append apply,
check that its full target, frozen draft and hashes appeared in an actual reply;
if absent, display them first. With save-all, display all remaining plans together
before applying any remaining plan. A candidate summary is not a full draft.

- `save this` writes only the current draft, prints its path, and continues to the next sub-flow.
- `save all` authorizes only drafts whose full content and target path have been displayed in a visible reply. Approval is bound to the displayed text: the written bytes must equal the displayed draft, with no recomposition between display and write.
- When `save all` is chosen, write the current (already shown) draft; then, before any further write, display every remaining proposed draft in full with its target path in one visible reply. Only after that display, write them in run order without another `Action?` pause, printing each path.
- A remaining draft that was not displayed before its write is not covered by `save all`. If a draft must change after display (for example a write failure changes a path), display the changed draft again before writing it.
- `skip` does not write the current draft and continues to the next sub-flow.
- `edit` takes inline edits, shows the full revised draft, then asks the same action menu again.
- Accept legacy `save` as an alias for `save this`.

---

## Task view (shared step)

A valid restore_pending task is visible and actionable now; do not require waiting for scheduled integration before the task can resume. Only the designated writer integrates the formal index; do not suggest that this reader performs that operation. Restoring visibility does not grant permission to execute the underlying task or its external actions.

Resolve `{research}` from `## Vault Structure`. If `<vault>/<research>/tidy/tasks/index.json` exists, run:

`python3 -B -X utf8 "${CLAUDE_PLUGIN_ROOT}/scripts/task_view_cli.py" --vault <vault> --data <research>/tidy/tasks --gate-version <G> --page-size 20 --offset 0`

This is a bounded preview when `pagination.all_displayed` is false. For active, uncertain and exceptions, report total, returned, earlier_not_displayed, remaining and next_offset. Unshown uncertain items stay visible as counts; never claim all done or a complete inventory from a partial page.

For subsequent pages use the reported next_offset and pin both --expected-revision <index_revision> and --expected-view-revision <view_revision> from the first response. Changed index, source or restore overlay invalidates the combined inventory: report it and stop. Discard the completeness claim, do not combine the pages, and do not retry through another interpreter or fall back to raw notes. A later empty page does not mean the full list is empty.

A comprehensive inventory requires all relevant pages. A bounded orientation may show a preview with totals and next offsets, but must not rank unseen tasks. If output is too large, reduce page size and read complete records; tool truncation is not successful inspection. “Every” below means every returned record plus explicit omitted counts until all requested pages have been read. Paging does not weaken full reader validation or the archive gate.


Before running, check that `${CLAUDE_PLUGIN_ROOT}/scripts/task_view_cli.py` exists. If it is missing, say so explicitly (「外掛目錄缺少任務檢視腳本」: the installed plugin payload does not yet ship the task-view scripts, a plugin payload limitation), then use the raw-note fallback below as unverified candidates only; never imply the task view ran or that nothing is open.

Run the line with `python3`; if it cannot start (command not found, or a Windows Store stub error / non-JSON output mentioning the Microsoft Store), run the same line with `python`. `<G>` is the single line of `${CLAUDE_PLUGIN_ROOT}/scripts/TASK_GATE_VERSION`. If that file is missing, empty or not exactly one line, the gate version is unavailable: report it, never substitute a remembered or hard-coded value, do not run the reader, and use the raw-note fallback below as unverified candidates only; never imply the task view ran or that nothing is open. The command is read-only. Parse its JSON (`active`, `uncertain`, `exceptions`) and show three sections:

- **有效待辦**: every `active` task with summary and source link. Mark `restore_pending` as 「取回申請待整合」 and `source_changed` as 「來源已變更」.
- **狀態未確認**: every `uncertain` task with its reason (the `exceptions` entry for that task_id) and source link. Keep each item's own reason visible (for example a stale gate version versus missing evidence); never merge uncertain items under one generic label.
- **例外**: every `exceptions` entry with its path.

Never hide uncertain tasks or exceptions, and never read an empty list as "all done" when `view_status` is not `complete`. A task the view lists as archived is not open: do not re-derive it from raw notes. List every returned record individually; never collapse records into ID ranges or "and N more" without the omitted counts above. A non-zero exit whose JSON exception reason is `page-index-revision-changed` or `page-effective-view-changed` (a revision mismatch on a later page) is not an unreadable index: report the mismatch and stop, with no raw-note fallback. Any other non-zero exit or unparseable output: say 「待辦索引無法讀取」 and fall back to the raw-note behavior below.

If no index exists, keep the raw-note behavior below unchanged and print exactly one line: 「尚無有效待辦索引，以下由原始紀錄推導，未經歸檔驗證。」

The raw-note fallback excludes items explicitly finished (「已完成」, 「完成」, `✓ Done`, `[x]`, `Done`), withdrawn (「撤回」, `withdrawn`) or superseded (「已取代」, `superseded`), including a later closing Wrap block in the scanned window. Interpret marks in context: 未完成 is not closed; a replacement is a separate item. Unmarked items without explicit status evidence are `status uncertain`, not confirmed active tasks. Keep them visible in a separate uncertain list in default and stuck modes; never automatically archive them. Explicit unfinished or reopened evidence may establish active status; missing an index or repeating an Open item does not. repetition cannot reopen a closed item, only newer explicit reopening does. If an existing index is unreadable, raw notes produce unverified candidates, not authoritative active or completed state; do not silently discard indexed closure or bypass a cross-page revision mismatch.

For triage the view is the saved baseline: wrap and handoff must not re-propose archived tasks as open, and uncertain tasks are listed as 「未確認」 in In progress / In flight. This adds no confirmation stop.

---

## Step 0 — Collect session state (shared)

Gather this once. All sub-flows draw from it — do not re-scan per sub-flow.

**Files touched**: Review Edit/Write tool history this session. Collect unique file paths modified or created.

**Tasks**: Call TaskList. Note which are `in_progress` or `pending` (incomplete) and which are `completed`.

**Decisions**: Scan conversation for non-obvious choices (phrases like "決定", "decided", "going with", "the approach is", "we'll"). Keep only decisions worth preserving.

**Judgment updates**: Scan for judgments that formed, changed, or were maintained against new evidence（只有可指認的形成／改變／有理由的維持才算實質更新）. Keep observations, inferences, unverified assumptions, decisions, later evidence, and outcomes distinct. Label each important claim as explicitly stated, reasonably inferred, or insufficient data. Never complete a missing trajectory.

**Corrections**: Scan conversation for anything the user corrected Claude on. Format each as "Wrong: [what Claude did] → Right: [what the user wanted]". Add a scope tag when it is clear: 本次任務 / 專案慣例 / 長期偏好; otherwise 範圍未定.

**Deferred items**: Scan for items pushed out ("下次", "後面再做", "deferred", "skip for now", "not in scope").

**Already saved**: Read today's `{daily}/YYYY-MM-DD.md`, today's `{journal}/YYYY-MM-DD-*.md`, the newest file in `{handoff}/`, and any spec the conversation explicitly named. For each lesson candidate, also perform the bounded lesson lookup in session-traces.md against `{journal}/lessons/` across dates before choosing new, append or reference-existing. Reuse those reads across sub-flows. Do not scan the whole vault.

---

Before candidate selection, load and apply `${CLAUDE_PLUGIN_ROOT}/references/capabilities/session-traces.md`. Preserve this workflow's existing write gate.

## Step 0.5 — Gap check (缺口判定)

Compare the collected state with what is already saved and decide which artifacts add value this time. Print exactly one plan line:

```
本次建議：wrap 寫入｜journal 略過（理由）｜handoff 略過（理由）｜lesson 略過（理由）
```

Rules for each artifact:

- **wrap**: propose when there is progress not yet in today's daily (new Done, In progress, Next, or a 撤回／重開／取代 of an earlier item). Skip when nothing moved.
- **journal**: propose for an uncovered judgment update, correction or worthwhile emerging clue. A named spec or closeout report is sufficient only after checking that it preserves the relevant context, alternatives and unknowns. Prefer append or reference-existing when covered; an immature clue does not need to satisfy the separate judgment-update gate.
- **handoff**: propose for uncovered future pickup context even when this batch is complete. Check deferred validation, authorization boundaries, environment constraints and recovery caveats. Skip only when there is no pickup need or a verified existing section fully covers it; a wrap Next line alone is not proof.
- **lesson**: propose a traceable, useful reusable point or boundary that is not already fully covered. One event can qualify within a narrow scope; report its evidence count and limits. It need not generalize beyond the project. An untested idea stays in journal, and no proposal promotes a rule.

Every 略過 carries a one-clause reason. The plan line is information, not a question: do not wait for an answer. Go straight to the first proposed sub-flow and show its draft; the existing action menu is the only write gate.

Adjusting the plan happens at any `Action?` prompt, in addition to the four actions:

- `all` adds wrap, journal, and handoff to this run regardless of the plan (lesson stays as planned); the current draft is still decided by its own action.
- `+journal` / `+handoff` / `+wrap` / `+lesson` adds one artifact; `-journal` etc. drops a proposed one that has not run yet.
- Neither `all` nor `+` is a save authorization; every draft still waits for its own `save this` / `save all`.

Run order is wrap → journal → handoff → lesson. If the plan proposes nothing, print `本次沒有新增價值，未寫任何檔。` and stop without asking anything.

---

## Sub-flow — Wrap

Generate a wrap block using the shared state above. Follow the same logic as `/hirameki:wrap`:

- Infer session focus from files touched and completed tasks
- Fill Done / In progress / Next sections
- Use action type tags (`#feature`, `#bug-fix`, `#research`, etc.) and project tags
- A Done item may carry one status suffix: 已完成 / 測試通過 / 實際使用有效. Write important verification gaps out loud (e.g. 未測試, 未在真實環境用過); a missing suffix means nothing by itself.
- Record 撤回：／重開：／取代：<舊> → <新> only when it happened this session
- A Done item may summarise its outcome and link to the spec, result, verification record, or lesson

Draft format:

```
## Wrap [HH:MM]

### Done
- **Item title** `#action-type` `#project` 已完成
  Description (optional)

### In progress
- item or "None"

### Next
- item or "TBD"
```

Write target: `{daily}/YYYY-MM-DD.md`
- If file does not exist and templates folder has daily.md → create from template
- If file does not exist and no template → create with `# YYYY-MM-DD` heading only
- If file exists → will append after `---` horizontal rule

Show the full draft and the target path. Then ask:

```
[Wrap] — Action? (save this / save all / skip / edit)
```

Apply the action model above, then proceed to the next proposed sub-flow.

---

## Sub-flow — Journal

Generate a journal entry using the shared state above. Follow the same logic as `/hirameki:journal`:

- Infer topic from session activity (files, tasks, decisions)
- Check `{journal}/` for a file matching today's date and the inferred topic keyword
  - Clear match → append mode (add Addendum block)
  - No match → create mode (new file with full structure)
- Sections are written only when there is material: `Why this approach` may be omitted when the judgment section already carries the reasoning; the judgment section shrinks to its one-line "no update" sentence when nothing substantive happened.

**Create mode** — filename: `YYYY-MM-DD-HHMM-{topic-slug}.md`

Slug language: Traditional Chinese slug if language setting is Chinese (e.g. `2026-05-14-1430-hirameki指令整合.md`).

File structure:

```markdown
---
tags:
  - journal
  - {relevant-topic-tags}
status: log
source: claude-code
actions:
  - type: {action-type}
    project: {project-name}
corrections: {count of corrections found in Step 0}
---

# {topic}

> Created: YYYY-MM-DD HH:MM

## Background
What prompted this. Reference related vault notes with [[wiki links]]. If the decision already lives in a spec, link the spec version and section instead of restating it.

## What was done
Specific actions and decisions taken.

## Why this approach
Reasoning behind key decisions. Omit this section when 判斷與決策過程 already carries it.

## 判斷與決策過程

<use the /hirameki:journal fields: 判斷的問題、起點（原先判斷）、觀察、推論、尚未驗證的假設、新出現的證據或經驗、判斷結果（形成／改變／維持）、行動狀態（提案／已決定／已執行／結果已驗證）、現場（原始素材，每條標來源：可回查對話／spec／工具輸出／僅 compaction 摘要）、仍然不知道什麼、什麼情況值得重新檢視 — if no substantive update, write only "本次沒有需要保存的判斷更新。">

## Emerging clues
<optional: preserve source/context, observation, interpretation and unknown using session-traces.md; omit when empty>

## Inspiration connections
Links to other ideas. [[wiki links]]. If none: "None."

## Possible improvements
Unexplored directions or risks. If none: "None."

## Corrections
{corrections from Step 0 — one line each with scope tag, or "None."}

## Open items
{incomplete tasks from Step 0, or "No open items."}
```

**Append mode** — add the `/hirameki:journal` Addendum block, including `### 判斷與決策過程` and optional `### Emerging clues`, at the end of the matched file. Record completed Open items as new "✓ Done [HH:MM]" statements in this append block; do not rewrite the earlier items. When this session produced the outcome of an earlier entry's judgment, add the optional `### 後續結果（接回 YYYY-MM-DD-HHMM 判斷）` block from `/hirameki:journal` instead of rewriting the earlier text.

Show the full draft and the target path. Then ask:

```
[Journal] — Action? (save this / save all / skip / edit)
```

Apply the action model above, then proceed to the next proposed sub-flow.

---

## Sub-flow — Handoff

Generate a handoff document using the shared state above. Follow the same logic as `/hirameki:handoff`:

- Infer slug from session's main topic (3–5 words, kebab-case, no dates)
- Show the inferred slug in the draft header — user confirms or adjusts via `edit`

Draft structure:

```markdown
---
tags:
  - handoff
status: reference
source: claude-code
created: YYYY-MM-DD HH:MM
topic: <one-line: what the next session needs to resolve>
priority: <high / medium / low>
estimated_cost: <wall time + API cost estimate>
---

# Handoff — <human-readable title>

> <one paragraph: current state and what the next session must do first>

---

## Re-pickup checklist

1. [ ] 讀本 handoff 全文
2. [ ] 確認相關 memory / vault notes（見「Related artifacts」）
3. [ ] 檢查 git / repo 狀態（見「In flight」）
4. [ ] 跑「Next actions」第一項確認環境正常

---

## What's done
<bulleted list of completed work with file paths>

---

## In flight
<incomplete tasks from Step 0, or "None">

---

## What's deferred

| 項目 | 為什麼擱置 | Revisit trigger |
|------|-----------|-----------------|
<rows from Step 0 deferred items, or "None">

---

## Decisions made
<non-obvious decisions from Step 0, or "None">

<this section: current constraints or commitments only — formation or change history goes in 判斷更新 below, never repeated here>

---

## 判斷更新

### <問題，一句話>
- 原先判斷：<...>
- 改變依據：<...；推論處標「可合理推論」>
- 目前判斷：<...>
- 尚未知：<...>
- 重新檢視條件：<...>

<one block per judgment update that affects pickup — repeat the heading block, no table. If none, this section contains only: "本次沒有需要接手的判斷更新。">

---

## Next actions
<numbered, priority-ordered concrete steps>

---

## Traps
<things the next session must NOT do, or "None">

---

## Related artifacts

### Files
<paths with one-line description from Step 0>

### Vault notes
<[[wikilinks]] with one-line description>
```

Write target: `{vault}/{handoff}/YYYY-MM-DD-{slug}.md`

Show the full draft and the target path. Then ask:

```
[Handoff] — Action? (save this / save all / skip / edit)
```

Apply the action model above, then proceed to the next proposed sub-flow.

---

## Sub-flow — Lesson

Only when the gap check proposed a new or append lesson. Use the verified disposition and target from the bounded lesson lookup; unresolved coverage is not a new-entry authorization.

- **Append**: use the Lesson append procedure in session-traces.md, the existing target and the complete displayed append block. Preserve the original bytes and verify the appended suffix. Do not use today's new-entry filename or replace the existing frontmatter. Then use the same Lesson action menu below.
- **Reference-existing**: show the existing path/section in the candidate summary; no Lesson write sub-flow.
- **New**: generate a lesson entry using the `/hirameki:journal` lesson format below; confirm the target is absent before saving.

- Write target: `{journal}/lessons/YYYY-MM-DD-{slug}.md`; create the `lessons/` folder on first use
- Frontmatter: `tags: [journal, lesson]`, `status: reference`, `source: claude-code`, `created: YYYY-MM-DD HH:MM`
- Required sections: 適用範圍（含限制）、教訓、反例（link a real counterexample or write「尚無反例」）、重新檢查條件
- Optional sections when there is material: 未驗證的部分、來源（wikilinks to the originating journal entry, raw evidence, and the record holding the counterexample）
- Do not retell the event; link to where it is recorded. One fact lives in one place.

Show the full draft and the target path. Then ask:

```
[Lesson] — Action? (save this / save all / skip / edit)
```

Apply the action model above. At the final sub-flow, `save all` is equivalent to `save this` because no sub-flow remains and no undisplayed draft exists.

---

## Completion summary

After the proposed sub-flows finish, print one line covering all four artifacts:

```
Triage done: wrap {✓ saved | – skipped | · 未提} / journal {✓ saved | – skipped | · 未提} / handoff {✓ saved | – skipped | · 未提} / lesson {✓ saved | – skipped | · 未提}
```

`未提` means the gap check did not propose it; `skipped` means the user declined a proposed draft.

---

## Rules

- Never write a file without `save this`, `save all`, or legacy `save` approval. An active `save all` is confirmation only for remaining drafts already displayed in full with their target path in a visible reply.
- Show the FULL draft content and target path before every write. With active `save all`, display every remaining draft before the first further write, then write them without another `Action?` pause; a draft changed after display is displayed again before it is written.
- A sub-flow that the gap check did not propose is not run; every 略過 in the plan line carries a reason. The plan line itself never pauses for an answer; the user adjusts the run with `all`, `+artifact`, or `-artifact` at any `Action?` prompt, and only `save this` / `save all` writes.
- Do not accept $ARGUMENTS input.
- Timestamps use local time in HH:MM format (24-hour)
- Print the full path after each write
- Write failure: first check whether the target file was partially written. Only a new-file create with a proven untouched target may retry a transient error at most twice; append failures follow exact-append.md and never retry automatically. A conflict, inconsistent content, or anything that needs a new decision stops immediately. Report per file: saved, failed, and retry count. A batch approval never hides a failure.
- Do not repeat action rationale in the judgment sections or turn insufficient evidence into a coherent story
- 證據硬閘：「當時根據」與「新出現的證據或經驗」各至少包含一項本次對話可直接追溯的具體事實（原句、數值、命令或輸出片段、具名檔案／操作結果）；只寫概括結論不合格。
- 現場（原始素材）：最多六個依 session 發生順序排列的原始證據單位；每點標明來源角色或操作，保留最小充分原句、數字或輸出片段；未明說的利害關係、動機與因果不得補寫；某類材料不存在就省略，不為湊數改寫。
- 由判斷導致的行動寫在 `What was done` 並明指出自該判斷；判斷未產生行動就直說沒有。
- Write section headings and output in the language specified in `## Vault Structure` → `language`
