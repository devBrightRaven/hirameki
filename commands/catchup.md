---
description: Progress handoff and suggested focus for the current session
arguments: [days] — optional, default 1
---

Read `## Vault Structure` from `~/.claude/CLAUDE.md` to get the vault path and the locations of the daily-notes and inbox folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Retrieve recent progress records and orient for the current session.

Input: $ARGUMENTS (optional — number of days to look back, default 1. Example: "3" reviews the last 3 days)

Scan sources:
- daily-notes folder: yesterday's daily note (or notes within the specified number of days)
- inbox folder: all files

Reading logic:
1. Find {daily-notes}/YYYY-MM-DD.md for yesterday (or each day in range)
2. If the file contains multiple Wrap blocks, read only the last one (most recent snapshot)
3. Extract "In progress" and "Next" from the last Wrap block

Output in three sections:

**Yesterday's progress**
List the "In progress" and "Next" items from the last Wrap block.
If no daily note or no Wrap block exists for that day, note "No progress record found."
If $ARGUMENTS specifies multiple days, list the last Wrap from each day in reverse chronological order.

**Inbox items**
List all files in the inbox folder. For each: filename, creation date, one-sentence summary.
If inbox is empty, note "Inbox is clear."
Limit: 10 items.

**Suggested focus**
Based on the above, suggest 1–3 items most worth advancing today.
For each, include a reason (why today rather than later).
Do not exceed 3 suggestions.

Write output in the language specified in `## Vault Structure` → `language`.
