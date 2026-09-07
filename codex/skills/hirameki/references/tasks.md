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

Scan recent wrap logs and journal entries to produce a single prioritized action list.

### Step 1 — Collect sources

1. **Wrap logs**: Read `{daily}/YYYY-MM-DD.md` for today and the past N days. From each Wrap block, extract all items under「下一步」/「Next」.
2. **Journal logs**: Read all `{journal}/YYYY-MM-DD-*.md` files from today and yesterday. From each file, extract all items under「Open items」that are NOT marked with "✓ Done".

If no files exist, respond: "No recent notes found."

### Step 2 — Deduplicate and rank

1. Normalize items: trim whitespace, remove leading `- `.
2. Group items that refer to the same task (fuzzy match — same project name + similar action). Keep the most detailed wording.
3. Count how many times each unique item appears across all sources.
4. Sort by: occurrence count (descending), then most recent appearance (descending).

### Step 3 — Output

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
- Items appearing 3+ times: prepend ⚠ to signal potential procrastination
- Do NOT modify any source files — this is read-only
- Do NOT ask for input — run immediately and output the list

---

## Stuck mode — `tasks stuck`

Find tasks that keep appearing in「下一步」without ever being completed.

Run only for the current explicit request or an explicitly opted-in bootstrap, never because a project happens to be mentioned. Recurrence is a discovery signal, not proof of unfinished work.

### Reconcile authoritative status

Read the recent non-archived handoffs for candidate tasks (start with the newest 10; follow directly linked superseding/status notes when necessary). Match by explicit task/project identity and action target, not project name alone. Use the owning vault's documented status vocabulary.

For the same task, the latest authoritative handoff frontmatter status outranks repeated daily mentions. Exclude completed/closed items even if their old next-actions text or recent wraps repeat them. A superseded note is not an open task: follow its replacement. Only explicit reopening in newer authoritative evidence reopens a closed task. Do not close unrelated subtasks merely because a parent project or a different action is closed.

Surface explicitly open handoff actions even without repeated wraps. Distinguish external waiting (name the dependency), last-mile internal work (name the remaining action), and other unresolved work. A recurrence-only candidate without authoritative status is `status uncertain`, not confirmed open. Report missing/conflicting status and source paths, and label inferred blockers as inference. Completion mentions without a matching handoff can support completion, but cannot override a newer explicit reopening.

Keep the output read-only. A status check does not authorize fixing the issue, notifying someone, changing task status or restarting a job. Do not infer priority from repetition alone.

### Step 1 — Collect data

1. **Wrap logs**: Read `{daily}/YYYY-MM-DD.md` for the past N days. From each Wrap block, extract:
   - All items under「下一步」/「Next」
   - All items under「完成」/「Done」
2. **Journal logs**: Read all `{journal}/YYYY-MM-DD-*.md` for the same date range. Extract items under「Open items」.

### Step 2 — Reconcile candidates

1. Normalize items: trim whitespace, remove leading `- `, `[ ]`, `[x]`.
2. Group items that refer to the same task (fuzzy match — same project name + similar action verb + similar target).
3. Combine explicitly open handoff actions with items recurring in「下一步」2+ times. Count mentions for context, not as a required threshold for handoff actions.
4. Apply the authoritative status rules above to each candidate before reporting it. An older Done mention does not remove a newer explicitly reopened action. Recurrence alone leaves status uncertain.

### Step 3 — Categorize

Group confirmed unresolved work into external waiting, last-mile internal work, or other unresolved work. Show recurrence-only candidates separately under `status uncertain`. If an item appears deferred or forgotten, label that as an observation, not a proven blocker or priority.

### Step 4 — Output

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
