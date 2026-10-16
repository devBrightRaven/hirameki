---
description: >
  Aggregate next actions from wrap logs and journal; "stuck" surfaces items that
  keep reappearing unfinished.
  Use when the user asks what is outstanding, or says
  "還有什麼沒做", "待辦", "有什麼卡住", "一直沒完成的",
  "what's on my plate", "open items", "what keeps slipping", "anything stuck".
  Not for a session recap (next).
---

Read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path, wrap folder, and journal folder.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS (optional)
- Empty or a number → Default mode: aggregate next actions (number = days to look back, default 3).
- `stuck` or `stuck N` → Stuck mode: find recurring unfinished tasks (N = days, default 7).

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

---

Before classification, load `${CLAUDE_PLUGIN_ROOT}/references/capabilities/task-status.md`. This shared evidence contract governs both default and stuck modes.

## Default mode — action aggregation

Scan recent wrap logs and journal entries to produce a single prioritized action list. When the task view exists, it is the item list: show its three sections and skip Steps 1-2 re-scraping of raw notes (wrap/journal may only add context to listed items).

### Step 1 — Collect sources

1. **Wrap logs**: Read `{daily}/YYYY-MM-DD.md` for today and the past N days. From each Wrap block, extract all items under「下一步」/「Next」.
2. **Journal logs**: Read all `{journal}/YYYY-MM-DD-*.md` files from today and yesterday. From each file, extract all items under「Open items」that are NOT marked with "✓ Done".

3. **Reconcile status**: Open items are discovery candidates only; an unchecked Open item, even in the newest journal, is discovery evidence, not a reopening event. Authority is per task identity and scope. With a task view, its effective view wins and raw notes add context only. Without an index, authoritative status evidence is an owner-approved status record, or an explicit completed, withdrawn, superseded or reopened event for the same task in a Wrap/Journal block; order events only by task revision/supersession or an unambiguous dated explicit event; a filename, mtime, arrival time or copied text never establishes authority or order. For the same task identity, the latest authoritative status wins: newer done, closed, withdrawn or superseded evidence is not reopened by an older or unchecked Open item; only a newer explicit reopening reopens. "Old" means superseded for that same identity by an evidenced later event, not a file older than a threshold; a replacement is a separate task. Missing or conflicting identity, scope, order or evidence means `status uncertain`. A handoff's frontmatter status is not task status unless its scope and an explicit task statement match. Never reopen a task the task view lists as archived.

If no files exist, respond: "No recent notes found."

### Step 2 — Deduplicate and rank

1. Normalize items: trim whitespace, remove leading `- `.
2. Group only items with evidence of the same action target and task identity. Similar wording suggests a candidate match, not permission to merge; ambiguous matches stay separate with their sources.
3. Count how many times each unique item appears across all sources, as source context only.
4. Order by explicit user priority, documented deadlines and dependencies when available; otherwise by most recent appearance (descending). Current state outranks repetition: recurrence is context, never priority.

### Step 3 — Output

Template headings and labels are structure: render them and all prose in the vault `language`; keep paths, task text and quotes verbatim.

```
=== Tasks ===

1. [×N] item description
   └ Source: MM-DD wrap, MM-DD wrap, MM-DD journal
2. [×N] item description
   └ Source: ...
3. item description (single occurrence — no count)
   └ Source: ...

Status uncertain (missing or contradictory status evidence):
  4. item description
     └ Source: ...
     └ Missing or conflicting evidence: [what is not established]
     └ Competing events: [source path of each competing or conflicting event]

---
Scanned: N wrap logs, M journal entries
Total: X tasks; Y status uncertain
```

Rules:
- Items classified as status uncertain by the reconcile step go only in the Status uncertain group, never in the numbered list above it; this includes missing or conflicting identity, scope, order or evidence; list the source paths of the competing or conflicting events, not only the missing evidence
- Show recurrence counts only as source context; flag missing or conflicting status rather than inferring procrastination
- Do NOT modify any source files — this is read-only
- Do NOT ask for input — run immediately and output the list

---

## Stuck mode — `next stuck`

Find tasks that keep appearing in「下一步」without a recorded completion. Recurrence is a discovery signal, not proof of unfinished work; current state outranks repetition. When the task view exists, exclude any task it lists as archived, and still show 狀態未確認 and 例外. A recurrence-only candidate with no authoritative status is reported as `status uncertain`, not as confirmed open. Do not infer priority from repetition alone.

### Step 1 — Collect data

1. **Wrap logs**: Read `{daily}/YYYY-MM-DD.md` for the past N days. From each Wrap block, extract:
   - All items under「下一步」/「Next」
   - All items under「完成」/「Done」
2. **Journal logs**: Read all `{journal}/YYYY-MM-DD-*.md` for the same date range. Extract items under「Open items」.
3. **Reconcile status**: Open items are discovery candidates only; an unchecked Open item, even in the newest journal, is discovery evidence, not a reopening event. Authority is per task identity and scope. With a task view, its effective view wins and raw notes add context only. Without an index, authoritative status evidence is an owner-approved status record, or an explicit completed, withdrawn, superseded or reopened event for the same task in a Wrap/Journal block; order events only by task revision/supersession or an unambiguous dated explicit event; a filename, mtime, arrival time or copied text never establishes authority or order. For the same task identity, the latest authoritative status wins: newer done, closed, withdrawn or superseded evidence is not reopened by an older or unchecked Open item; only a newer explicit reopening reopens. "Old" means superseded for that same identity by an evidenced later event, not a file older than a threshold; a replacement is a separate task. Missing or conflicting identity, scope, order or evidence means `status uncertain`. A handoff's frontmatter status is not task status unless its scope and an explicit task statement match. Never reopen a task the task view lists as archived.

### Step 2 — Identify recurring items

1. Normalize items: trim whitespace, remove leading `- `, `[ ]`, `[x]`.
2. Match by evidenced task identity and action target. Fuzzy similarity only suggests candidates; keep ambiguous matches separate and do not merge unrelated subtasks.
3. For each unique task:
   - Count appearances in「下一步」sections
   - Check if it ever appeared in「完成」sections
   - Check if it was marked "✓ Done" in journal open items
4. Filter: keep items appearing in「下一步」2+ times AND no completion in「完成」 newer, by the order rule in Reconcile status, than their latest explicit reopening (a completed-then-reopened task stays a candidate; a completion with no newer explicit reopening excludes it) as candidates; a count is context, and recurrence alone leaves status uncertain.

### Step 3 — Categorize

For each recurring item, assign a category:
- **blocked**: item mentions a dependency, external person, or "待..." / "pending"
- **deferred**: item appeared then disappeared then reappeared (skipped some days)
- **forgotten**: item appeared in early days but not in recent days
- **persistent**: item appears continuously including the most recent note

These categories are observations about the pattern, not proof of a blocker or of priority. Label an inferred blocker as inference.

### Step 4 — Output

Template headings and labels are structure: render them and all prose in the vault `language`; keep paths, task text and quotes verbatim.

```
=== Stuck Tasks (past N days) ===

Confirmed unresolved (listed by the task view as active, or an explicit open statement for the same identity and scope with no newer closure by the order rule in Reconcile status, a raw candidate and not validated indexed active state; a bare old Open item is a candidate, not confirmed):
  1. task description
     └ Status evidence: source path and the explicit status or open marker
     └ Blocker: [documented dependency, or clearly labelled inference]

Status uncertain (recurrence only, no authoritative status):
  persistent:
    2. [×N] task description
       └ First seen: MM-DD → Last seen: MM-DD
       └ Missing or conflicting evidence: [what is not established]
       └ Competing events: [source path of each competing or conflicting event]
  blocked:
    3. [×N] task description
       └ First seen: MM-DD → Last seen: MM-DD
       └ Possible blocker (inference): [inferred blocker]
  deferred:
    4. [×N] task description
       └ Appeared: MM-DD, MM-DD (skipped MM-DD ~ MM-DD)
  forgotten:
    (none or listed items)

---
Scanned: N wrap logs, M journal entries
Total: X confirmed unresolved tasks; Y uncertain candidates
```

Rules:
- Read-only — do NOT modify any files
- Do NOT ask for input — run immediately
- If no recurring tasks found, respond: "No stuck tasks in the past N days."

---

Write output in the language specified in `## Vault Structure` → `language`.
