---
description: Snapshot session progress to wrap log. Use "merge" to consolidate multiple wrap blocks.
---

Read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path and the locations of the daily and templates folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS (optional)
- `merge` → Merge mode: consolidate multiple Wrap blocks into one (see Merge mode below).
- Any other text → describes the focus of this wrap. If omitted, infer from session activity.

---

## Default mode — snapshot

Record a progress snapshot for the current work session and append it to today's wrap log. Can be run multiple times per day — each run appends a new timestamped block.

Scan sources:
- Session activity (files created, modified, deleted)
- Today's wrap log in the wrap folder (format: YYYY-MM-DD.md)

Write target: {daily}/YYYY-MM-DD.md (today's date)
- If the file does not exist and templates folder contains daily.md, create it from the template
- If the file does not exist and no template is found, create it with only a `# YYYY-MM-DD` heading
- If the file already exists, append a new Wrap block at the end, separated by a horizontal rule

Block format (append after a `---` horizontal rule):

    ## Wrap [HH:MM]

    ### Done
    - **Item title** `#action-type` `#project` 已完成
      Description of what was done (optional, can be multi-line with sub-items)

    ### In progress
    - item or "None"

    ### Next
    - item or "TBD"

Status suffix on a Done item (optional, one of three): `已完成` / `測試通過` / `實際使用有效`. Write important verification gaps out loud (e.g. `未測試`, `未在真實環境用過`); a missing suffix means nothing by itself. A Done item may summarise its outcome and link to the spec, result, verification record, or lesson so the reader does not have to open another file for the gist.

Change of state (write only when it happened this session, as its own Done line):
- `撤回：<original Done item>` — a previously reported completion no longer holds
- `重開：<item>` — a previously completed or dropped item is active again
- `取代：<old> → <new>` — a new item supersedes an earlier one

Action type tags (use the closest match, one per item):
  `#test-rewrite` `#test-fix` `#code-review` `#config-update` `#hook-setup`
  `#automation` `#feature` `#bug-fix` `#refactor` `#research` `#vault-write`
  `#git-ops` `#design` `#infra` `#skill-dev` `#debug`
If none fits, use a short descriptive tag like `#migration` or `#cleanup`.

Project tags: use the short project name, e.g. `#journal` `#library` `#dotclaude` `#asagiri` `#hirameki` `#vault`.

Rules:
- Timestamp uses local time in HH:MM format (24-hour)
- Do not modify earlier Wrap blocks already in the file — append only
- If $ARGUMENTS is empty, do NOT ask the user for input — proceed immediately by inferring focus from session activity
- If $ARGUMENTS contains a description, use it to organise the content around that focus
- Show the full content and full path of the target file, and wait for confirmation before writing
- Print the full path after writing

---

## Merge mode — `wrap merge`

Merge multiple Wrap blocks from today's wrap log into a single unified summary.

### Step 1 — Read today's wrap log

Read `{daily}/YYYY-MM-DD.md` for today.
If no file exists, respond: "No wrap log found for today."

Parse all Wrap blocks. For each block, extract:
- Timestamp
- 「完成」/「Done」items
- 「進行中」/「In progress」items
- 「下一步」/「Next」items

### Step 2 — Merge

1. **Done**: Union of all items across all Wrap blocks. Deduplicate only items that describe the same task with the same result; similar wording with a different time or outcome stays as separate items. Keep the most detailed wording and the status suffix. Preserve chronological order.
2. **In progress**: Union. If an item appears in「進行中」in an earlier wrap and「完成」in a later wrap, keep it only in「完成」.
3. **Next**: Union. Deduplicate. If an item appears in「下一步」in an earlier wrap and「完成」in a later wrap, remove it from「下一步」.
4. **State changes**: a `撤回：` line moves the matching Done item into a `### 已撤回` section (shown only when at least one exists) with the withdrawal time; a `重開：` line moves the item back to In progress; a `取代：` line shows the new item in Done annotated with what it replaced. Original Wrap blocks are never edited.

### Step 3 — Output

Print the merged summary:

```
=== Merge Summary: YYYY-MM-DD ===
Source: N Wrap blocks ([HH:MM], [HH:MM], ...)

### Done (N items)
- item
- item

### In progress
- item (or "None")

### Next (N items)
- item
- item

### 已撤回
- item (撤回 HH:MM) — only when a withdrawal happened

---
Duplicates removed: N
Completed "Next" items removed: N
State changes applied: N
```

Rules:
- Read-only — do NOT modify the wrap log until confirmed
- Show the merged result and ask if the user wants to write it
- If user confirms, insert as `## Wrap [HH:MM] (merged)` block at the TOP of the wrap log (after the `# YYYY-MM-DD` heading), before all individual Wrap blocks — the merged summary is the day's overview, individual wraps are the detail log below

---

Write section headings in the language specified in `## Vault Structure` → `language`.
