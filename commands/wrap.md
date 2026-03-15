---
description: Snapshot session progress to daily note. Use "merge" to consolidate multiple wrap blocks.
---

Read `## Vault Structure` from `~/.claude/CLAUDE.md` to get the vault path and the locations of the daily and templates folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS (optional)
- `merge` → Merge mode: consolidate multiple Wrap blocks into one (see Merge mode below).
- Any other text → describes the focus of this wrap. If omitted, infer from session activity.

---

## Default mode — snapshot

Record a progress snapshot for the current work session and append it to today's daily note. Can be run multiple times per day — each run appends a new timestamped block.

Scan sources:
- Session activity (files created, modified, deleted)
- Today's daily note in the daily folder (format: YYYY-MM-DD.md)

Write target: {daily}/YYYY-MM-DD.md (today's date)
- If the file does not exist and templates folder contains daily.md, create it from the template
- If the file does not exist and no template is found, create it with only a `# YYYY-MM-DD` heading
- If the file already exists, append a new Wrap block at the end, separated by a horizontal rule

Block format (append after a `---` horizontal rule):

    ## Wrap [HH:MM]

    ### Done
    - **Item title** `#action-type` `#project`
      Description of what was done (optional, can be multi-line with sub-items)

    ### In progress
    - item or "None"

    ### Next
    - item or "TBD"

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

Merge multiple Wrap blocks from today's daily note into a single unified summary.

### Step 1 — Read today's daily note

Read `{daily}/YYYY-MM-DD.md` for today.
If no file exists, respond: "No daily note found for today."

Parse all Wrap blocks. For each block, extract:
- Timestamp
- 「完成」/「Done」items
- 「進行中」/「In progress」items
- 「下一步」/「Next」items

### Step 2 — Merge

1. **Done**: Union of all items across all Wrap blocks. Deduplicate items that describe the same action (fuzzy match). Keep the most detailed wording. Preserve chronological order.
2. **In progress**: Union. If an item appears in「進行中」in an earlier wrap and「完成」in a later wrap, keep it only in「完成」.
3. **Next**: Union. Deduplicate. If an item appears in「下一步」in an earlier wrap and「完成」in a later wrap, remove it from「下一步」.

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

---
Duplicates removed: N
Completed "Next" items removed: N
```

Rules:
- Read-only — do NOT modify the daily note until confirmed
- Show the merged result and ask if the user wants to write it
- If user confirms, insert as `## Wrap [HH:MM] (merged)` block at the TOP of the daily note (after the `# YYYY-MM-DD` heading), before all individual Wrap blocks — the merged summary is the day's overview, individual wraps are the detail log below

---

Write section headings in the language specified in `## Vault Structure` → `language`.
