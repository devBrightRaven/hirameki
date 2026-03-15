---
description: Aggregate next actions from daily notes and journal. Use "stuck" to find recurring unfinished tasks.
---

Read `## Vault Structure` from `~/.claude/CLAUDE.md` to get the vault path, daily folder, and journal folder.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS (optional)
- Empty or a number → Default mode: aggregate next actions (number = days to look back, default 3).
- `stuck` or `stuck N` → Stuck mode: find recurring unfinished tasks (N = days, default 7).

---

## Default mode — action aggregation

Scan recent daily notes and journal entries to produce a single prioritized action list.

### Step 1 — Collect sources

1. **Daily notes**: Read `{daily}/YYYY-MM-DD.md` for today and the past N days. From each Wrap block, extract all items under「下一步」/「Next」.
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
Scanned: N daily notes, M journal entries
```

Rules:
- Items appearing 3+ times: prepend ⚠ to signal potential procrastination
- Do NOT modify any source files — this is read-only
- Do NOT ask for input — run immediately and output the list

---

## Stuck mode — `tasks stuck`

Find tasks that keep appearing in「下一步」without ever being completed.

### Step 1 — Collect data

1. **Daily notes**: Read `{daily}/YYYY-MM-DD.md` for the past N days. From each Wrap block, extract:
   - All items under「下一步」/「Next」
   - All items under「完成」/「Done」
2. **Journal logs**: Read all `{journal}/YYYY-MM-DD-*.md` for the same date range. Extract items under「Open items」.

### Step 2 — Identify recurring items

1. Normalize items: trim whitespace, remove leading `- `, `[ ]`, `[x]`.
2. Group items that refer to the same task (fuzzy match — same project name + similar action verb + similar target).
3. For each unique task:
   - Count appearances in「下一步」sections
   - Check if it ever appeared in「完成」sections
   - Check if it was marked "✓ Done" in journal open items
4. Filter: keep only items appearing in「下一步」2+ times AND never appearing in「完成」.

### Step 3 — Categorize

For each recurring item, assign a category:
- **blocked**: item mentions a dependency, external person, or "待..." / "pending"
- **deferred**: item appeared then disappeared then reappeared (skipped some days)
- **forgotten**: item appeared in early days but not in recent days
- **persistent**: item appears continuously including the most recent note

### Step 4 — Output

```
=== Stuck Tasks (past N days) ===

persistent:
  1. [×N] task description
     └ First seen: MM-DD → Last seen: MM-DD
     └ Suggestion: Split into smaller tasks? Blocker?

blocked:
  2. [×N] task description
     └ First seen: MM-DD → Last seen: MM-DD
     └ Blocker: [inferred blocker]

deferred:
  3. [×N] task description
     └ Appeared: MM-DD, MM-DD (skipped MM-DD ~ MM-DD)

forgotten:
  (none or listed items)

---
Scanned: N daily notes, M journal entries
Total: X stuck tasks
```

Rules:
- Read-only — do NOT modify any files
- Do NOT ask for input — run immediately
- If no recurring tasks found, respond: "No stuck tasks in the past N days."

---

Write output in the language specified in `## Vault Structure` → `language`.
