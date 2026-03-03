---
description: Progress snapshot written to today's daily note
arguments: [focus description] — optional, auto-detected from session if omitted
---

Read `## Vault Structure` from `~/.claude/CLAUDE.md` to get the vault path and the locations of the daily-notes and templates folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Record a progress snapshot for the current work session and append it to today's daily note. Can be run multiple times per day — each run appends a new timestamped block.

Input: $ARGUMENTS (optional — describes the focus of this wrap. If omitted, infer from session activity)

Scan sources:
- Session activity (files created, modified, deleted)
- Today's daily note in the daily-notes folder (format: YYYY-MM-DD.md)

Write target: {daily-notes}/YYYY-MM-DD.md (today's date)
- If the file does not exist and templates folder contains daily.md, create it from the template
- If the file does not exist and no template is found, create it with only a `# YYYY-MM-DD` heading
- If the file already exists, append a new Wrap block at the end, separated by a horizontal rule

Block format:

```
---

## Wrap [HH:MM]

### Done
- [Specific items completed this session, one per line]

### In progress
- [Started but not finished. If none, write "None"]

### Next
- [What comes next. If unknown, write "TBD"]
```

Rules:
- Timestamp uses local time in HH:MM format (24-hour)
- Do not modify earlier Wrap blocks already in the file — append only
- If $ARGUMENTS contains a description, use it to organise the content around that focus
- Show the full content and full path of the target file, and wait for confirmation before writing
- Print the full path after writing

Write section headings in the language specified in `## Vault Structure` → `language`.
