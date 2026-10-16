---
description: >
  Aggregate next actions from wrap logs and journal; "stuck" surfaces items that
  keep reappearing unfinished.
  Use when the user asks what is outstanding, or says
  "還有什麼沒做", "待辦", "有什麼卡住", "一直沒完成的",
  "what's on my plate", "open items", "what keeps slipping", "anything stuck".
  Not for a session recap (next).
---

Resolve vault configuration through the umbrella Hirameki adapter for the daily, journal and handoff folders. Missing optional handoff data reduces confidence; do not fall back to another agent's runtime configuration or invent completion status.
If required vault configuration is missing, ask the user to run `/hirameki:__init`; do not initialize a real vault as part of this read-only check.

Input: $ARGUMENTS (optional)
- Empty or a number → Default mode: aggregate next actions (number = days to look back, default 3).
- `stuck` or `stuck N` → Stuck mode: find recurring unfinished tasks (N = days, default 7).

---

## Default mode — action aggregation
## Task view (shared step)

Resolve vault and `{research}` through the umbrella adapter. When `<vault>/<research>/tidy/tasks/index.json` exists, resolve `<HIRAMEKI_TASK_ROOT>` from an explicitly configured machine-local `task_view_root`, otherwise the directory containing the actually loaded Hirameki SKILL.md when it contains the bundled scripts, otherwise the verified source checkout containing this loaded reference. Check that both `scripts/task_view_cli.py` and `scripts/TASK_GATE_VERSION` exist there. Do not use Claude configuration, CLAUDE_PLUGIN_ROOT, a guessed cache path, or a recursive filesystem search. If an explicit root is invalid, report unavailable rather than silently switching roots. A plugin-only payload without these files is not yet wired; report that limitation.

`python3 -X utf8 "<HIRAMEKI_TASK_ROOT>/scripts/task_view_cli.py" --vault <vault> --data <research>/tidy/tasks --gate-version <G> --page-size 20 --offset 0`

This is a bounded preview, not a complete baseline when `pagination.all_displayed` is false. For each of active, uncertain and exceptions, retain the total, returned, earlier_not_displayed, remaining and next_offset in the report; do not claim all done, no exceptions or a complete inventory from an incomplete page. Totals describe the full validated view, not just the displayed items. Unshown uncertain items remain explicitly visible as a count, not silently discarded or promoted to active tasks.

For further pages, replace --offset with a reported next_offset and include --expected-revision <index_revision> and --expected-view-revision <view_revision> from the first response. Both tokens must match; index, source or restore-overlay changes invalidate a combined inventory. Report that change and discard any combined completeness claim; do not combine incompatible pages, retry via another interpreter, or silently fall back to old notes. A later empty page never proves an empty task list.

Read further pages when needed for the requested scope; a requested comprehensive inventory requires all relevant pages. A bounded orientation/checkpoint may report a preview with totals and deferred next offsets, but must not rank unseen tasks or conclude they are finished. If an individual page is too large for the output channel, reduce page size and read complete records; tool truncation is not successful inspection. This presentation option does not reduce full reader validation or change the writer/dry-run archive gate.

Read `<G>` from that root's `scripts/TASK_GATE_VERSION`; missing/blank/multiline version is unavailable, never a hard-coded fallback. Use a verified Python 3.10+ executable: python3 then python only when the first cannot launch (including a Store stub). Do not retry a real CLI data/schema failure as an interpreter failure. On Windows use PowerShell native argument arrays, not cmd wrappers. This step is read-only.

Invoke the script directly with that interpreter; do not nest interpreter subprocesses or replace the CLI with runpy. A policy or access denial makes this launch unavailable: report it, do not rewrite the launch to evade the denial. The missing-command/Store-stub fallback above is not permission to bypass an access restriction.

A valid restore_pending task is visible and actionable now; do not require waiting for scheduled integration before the task can resume. Only the designated writer integrates the formal index; do not suggest that this reader performs that operation. Restoring visibility does not grant permission to execute the underlying task or its external actions.

Show three separately labelled lists: 「有效待辦」 (active), 「狀態未確認」 (uncertain), 「例外」 (exceptions). Do not blend uncertain items into the active list; these lists may be nested inside the entry's normal output sections. Mark restore_pending as 「取回申請待整合」, source_changed as 「來源已變更」, and partial/unavailable explicitly. Retain all in-scope uncertainty and exception paths. An empty partial/unavailable result never means all done. Archived indexed items are not reopened by old note text. Raw notes may add context or identify unindexed candidates, not override existing dispositions.

If no index exists, print 「尚無有效待辦索引，以下由原始紀錄推導，未經歸檔驗證。」 and use the existing raw-note flow. If an existing index/CLI cannot be read, print 「待辦索引無法讀取」; any raw-note fallback is explicitly unverified candidates, not authoritative active or completed state. Do not write an index or add confirmation stops.

Raw-note fallback must respect explicit task dispositions: exclude the same item marked finished (已完成, 完成, [x], ✓ Done), withdrawn (撤回, withdrawn), or superseded (已取代, superseded), including a later closing Wrap block in the scanned window. Interpret the mark in context, not by substring: 未完成 is not closed; a replacement remains a separate open item. Unmarked items without explicit status evidence are `status uncertain`, not confirmed active tasks. Keep them visible in a separate uncertain list in default and stuck modes; never automatically archive them. Explicit unfinished or reopened evidence may establish active status; missing an index or repeating an Open item does not. Repetition does not reopen a closed item; only newer explicit reopening does.


When a valid task view exists, use its three sections instead of Steps 1-2 raw aggregation. Stuck mode can add source evidence about active items, but must not reintroduce archived items. Count or repetition alone does not establish unfinished status.

Scan recent wrap logs and journal entries for candidates. Before classification, load `references/capabilities/task-status.md` under the loaded skill root. Give separate active, status uncertain and exceptions groups; raw Open items alone never enter the active list.

### Step 1 — Collect sources

1. **Wrap logs**: Read `{daily}/YYYY-MM-DD.md` for today and the past N days. From each Wrap block, extract all items under「下一步」/「Next」.
2. **Journal logs**: Read all `{journal}/YYYY-MM-DD-*.md` files from today and yesterday. From each file, extract all items under「Open items」that are NOT marked with "✓ Done".

If no files exist, respond: "No recent notes found."

### Step 2 — Deduplicate and rank

1. Normalize items: trim whitespace, remove leading `- `.
2. Group only items with evidence of the same action target and task identity. Similar wording suggests a candidate match, not permission to merge. Ambiguous identity matches remain separate candidates with their sources; a parent project's closure does not close unrelated subtasks.
3. Count how many times each unique item appears across all sources.
4. Use explicit user priority, documented deadlines and dependencies when available; otherwise present recent source-backed items without inventing urgency. Recurrence is context, not priority or procrastination evidence.

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

---
Scanned: N wrap logs, M journal entries
```

Rules:
- Show recurrence counts only as source context; flag missing/conflicting status rather than inferred procrastination.
- Do NOT modify any source files — this is read-only
- Do NOT ask for input — run immediately and output the list

---

## Stuck mode — `next stuck`

Find tasks that keep appearing in「下一步」without ever being completed.

Run only for the current explicit request or an explicitly opted-in bootstrap, never because a project happens to be mentioned. Recurrence is a discovery signal, not proof of unfinished work.

### Reconcile authoritative status

Read the recent non-archived handoffs for candidate tasks (start with the newest 10; follow directly linked superseding/status notes when necessary). Match by explicit task/project identity and action target, not project name alone. Use the owning vault's documented status vocabulary.

For the same task identity and scope, the latest evidenced explicit task status outranks repeated daily mentions. Frontmatter alone is not task status; use it only when the scope and an explicit task statement match. Apply the shared task-status ordering rules, not filename, mtime or arrival order. Exclude completed/closed items unless a later explicit reopening exists. A superseded note is not an open task: follow its replacement. Do not close unrelated subtasks merely because a parent project or a different action is closed.

Surface explicitly open handoff actions even without repeated wraps. Distinguish external waiting (name the dependency), last-mile internal work (name the remaining action), and other unresolved work. A recurrence-only candidate without authoritative status is `status uncertain`, not confirmed open. Report missing/conflicting status and source paths, and label inferred blockers as inference. Completion mentions without a matching handoff can support completion, but cannot override a newer explicit reopening.

Keep the output read-only. A status check does not authorize fixing the issue, notifying someone, changing task status or restarting a job. Do not infer priority from repetition alone.

### Step 1 — Collect data

1. **Wrap logs**: Read `{daily}/YYYY-MM-DD.md` for the past N days. From each Wrap block, extract:
   - All items under「下一步」/「Next」
   - All items under「完成」/「Done」
2. **Journal logs**: Read all `{journal}/YYYY-MM-DD-*.md` for the same date range. Extract items under「Open items」.

### Step 2 — Reconcile candidates

1. Normalize items: trim whitespace, remove leading `- `, `[ ]`, `[x]`.
2. Match by evidenced task identity and action target. Fuzzy similarity only suggests candidates; keep ambiguous matches separate and do not merge unrelated subtasks.
3. Combine explicitly open handoff actions with items recurring in「下一步」2+ times. Count mentions for context, not as a required threshold for handoff actions.
4. Apply the authoritative status rules above to each candidate before reporting it. An older Done mention does not remove a newer explicitly reopened action. Recurrence alone leaves status uncertain.

### Step 3 — Categorize

Group confirmed unresolved work into external waiting, last-mile internal work, or other unresolved work. Show recurrence-only candidates separately under `status uncertain`. If an item appears deferred or forgotten, label that as an observation, not a proven blocker or priority.

### Step 4 — Output

Template headings and labels are structure: render them and all prose in the vault `language`; keep paths, task text and quotes verbatim.

```
=== Stuck Tasks (past N days) ===

External waiting / Last-mile internal / Other unresolved:
  - Task identity and remaining action
    Status evidence: handoff path and status, relevant daily/journal paths
    Dependency: documented dependency, or clearly labelled inference

Status uncertain:
  - Recurring candidate and missing/conflicting evidence

---
Scanned: N wrap logs, M journal entries, H handoffs
Total: X confirmed unresolved tasks; Y uncertain candidates
```

Rules:
- Read-only — do NOT modify any files
- Do NOT ask for input — run immediately
- Report no stuck tasks only when neither open handoff actions nor recurring unresolved candidates remain in the inspected scope. If sources are missing, state that limitation rather than claiming everything is complete.

---

Write output in the language specified in `## Vault Structure` → `language`.
