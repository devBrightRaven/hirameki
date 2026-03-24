---
description: Resume from yesterday + inbox scan. Use "plan" to generate a written checklist.
---

Read `## Vault Structure` from `~/.claude/vault-local.md` (fall back to `~/.claude/CLAUDE.md` if not found) to get the vault path and the locations of the daily, journal, and inbox folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Retrieve recent progress records and orient for the current session.

Input: $ARGUMENTS (optional)
- A number → days to look back (default 1). Example: "3" reviews the last 3 days.
- `plan` → generate a written checklist file (see Plan mode below).
- `plan 3` → plan mode with 3-day lookback.

---

## Default mode — read-only orientation

Scan sources:
- daily folder: yesterday's daily note (or notes within the specified number of days)
- inbox folder: all files

Reading logic:
1. Find {daily}/YYYY-MM-DD.md for yesterday (or each day in range)
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

**Reminders**

Run `node ~/.claude/scripts/catchup-reminders.mjs` via Bash tool.
If the script produces output, include it as-is.
If the script produces no output, skip this section entirely (no "Reminders" heading).
If the script is missing or errors, skip silently.

---

## Plan mode — `catchup plan`

Generate today's checklist from recent wrap entries and journal open items, then write it to the vault.

### Step 1 — Collect sources

1. **Daily notes**: Read `{daily}/YYYY-MM-DD.md` for today and the past 3 days (4 files max). From each Wrap block, extract all items under「下一步」/「Next」.
2. **Journal logs**: Read all `{journal}/YYYY-MM-DD-*.md` files from today and the past 2 days. From each file, extract all items under「Open items」that are NOT marked with "✓ Done".
3. **Previous checklist**: If yesterday's checklist exists (`{daily}/YYYY-MM-DD-checklist.md`), read it. Any item still unchecked (`- [ ]`) carries forward automatically.

If no files exist, respond: "No recent notes found."

### Step 2 — Deduplicate, categorize, and rank

1. Normalize items: trim whitespace, remove leading `- `, `- [ ] `, `- [x] `.
2. Group items that refer to the same task (fuzzy match — same project name + similar action). Keep the most detailed wording.
3. Count how many times each unique item appears across all sources.
4. Sort by: occurrence count (descending), then most recent appearance (descending).
5. Categorize by project name (extract from backtick tags, heading context, or explicit project mentions).

### Step 3 — Write checklist file

Write to `{daily}/YYYY-MM-DD-checklist.md` (today's date).

Format:

```markdown
---
tags:
  - checklist
  - daily
status: log
source: agent
created: YYYY-MM-DD
---

# Checklist: YYYY-MM-DD

> Scanned: N daily notes, M journal entries, carried forward: K items

## Project Name

- [ ] item description
  - Source: MM-DD wrap, MM-DD journal
- [ ] item description (carried forward from MM-DD)
  - Source: MM-DD checklist

## Another Project

- [ ] item description
  - Source: ...

## General

- [ ] items not tied to a specific project
```

Rules:
- Items appearing 3+ times across sources: prepend `[!]` to flag potential procrastination
- Items carried forward from yesterday's unchecked checklist: append `(carried forward from MM-DD)`
- Group under project headings. Use `## General` for items without a clear project.
- Each item has a `- Source:` line indented below it (smaller context)
- Use Obsidian checkbox syntax `- [ ]` so items can be ticked in Obsidian

### Step 4 — Embed in daily note

Check if today's daily note `{daily}/YYYY-MM-DD.md` exists.

If it exists:
- Check if `![[YYYY-MM-DD-checklist.md]]` already appears. If yes, skip.
- Otherwise, find the first `## ` heading and insert before it:
  ```
  ## Today's Checklist

  ![[YYYY-MM-DD-checklist.md]]

  ```

If it does not exist:
- Create it with minimal frontmatter and the embed.

### Step 5 — Print summary to terminal

Print a concise summary:

```
=== Checklist ===

Written: {daily}/YYYY-MM-DD-checklist.md
Items: N total (K carried forward, J new)
Projects: list of project names

Top 3 priorities:
1. [!] item (appears N times — consider acting today)
2. item
3. item
```

Rules:
- Do NOT ask for input — run immediately
- Do NOT modify source files (wraps, journals) — only write the checklist and embed
- If a checklist for today already exists, regenerate it (overwrite) to pick up any new items

---

Write output in the language specified in `## Vault Structure` → `language`.
