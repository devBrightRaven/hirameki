---
description: Surface actionable ideas from vault
arguments: [save] — optional; append "save" to write output to file
---

Read `## Vault Structure` from `~/.claude/CLAUDE.md` to get the vault path and the locations of the analysis, daily-notes, and inbox folders, plus the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Scan the vault and surface actionable ideas from existing content.

Input: $ARGUMENTS (optional — no argument = display only; "save" = write result to file)

Scan scope:
- All content folders
- Last 30 days in the daily-notes folder
- All files in the inbox folder

Output in seven categories, limit 5 items each:

**Articles you could write**
Topics with enough existing material or perspective to develop into an article. For each: suggested title, source notes ([[filename]] list), what is still missing before writing can begin.

**Tools or projects to build**
Tool needs, workflow pain points, or product ideas mentioned in the vault. For each: description, source, estimated complexity (small / medium / large).

**Topics worth researching**
External concepts, theories, or technologies mentioned but not explored in depth. For each: topic, the context in which it was mentioned, why it is worth researching.

**People or communities to contact**
Individuals, organisations, or communities mentioned in the vault that are relevant to the current direction. For each: name, context, reason to reach out. If none, write "None."

**Ideas for a different medium**
Content that might work better in a non-text format (video, visual, talk, newsletter, podcast, etc.). For each: idea summary, suggested medium, reason why that format is more suitable than text.

**Untransacted value**
Expertise or capability you have but have not converted into any form of exchange. For each: skill or knowledge description, possible form (course, consulting, product, licensing), vault evidence. If none, write "None."

**Ideas ready to graduate**
Half-formed ideas with enough density to become a standalone note. For each: source location ([[filename]] + section description), core claim (one sentence), suggested destination folder, related existing notes.

Graduation criteria: has a clear core claim (not just a passing thought), relates to at least one existing theme in the vault, has enough content density to stand alone (not just a single line).

### Graduation confirmation flow

After listing "Ideas ready to graduate," pause and wait for the user to confirm which ones to act on. For each selected idea:
1. Show the full intended path and wait for a second confirmation before proceeding
2. Create a new markdown file in the appropriate content folder containing:
   - Title
   - Core claim
   - Origin context (which daily note or inbox item this developed from)
   - Connections to other vault notes ([[wiki link]] format)
   - Directions to develop further
3. Print the full path after writing

---

Write output in the language specified in `## Vault Structure` → `language`.

Write logic (only when $ARGUMENTS contains "save" — does not apply to the graduation flow):
1. Check `{analysis}/harvest/` for a file created today
2. If found → append to the existing file:

```
---

## Update [HH:MM]

### Newly found ideas
[Ideas found in this scan not listed before, using the seven-category format]

### Changes to existing ideas
[Status changes to previously listed ideas, if any]
```

3. If not found → create a new file

Write target: `{analysis}/harvest/YYYY-MM-DD.md`
Create the folder if it does not exist.

File structure (new file):

```
# Idea harvest

> Analysis time: YYYY-MM-DD HH:MM
> Scan scope: [list of folders actually scanned]

## Articles you could write
[list]

## Tools or projects to build
[list]

## Topics worth researching
[list]

## People or communities to contact
[list]

## Ideas for a different medium
[list]

## Untransacted value
[list]

## Ideas ready to graduate
[list]
```

Rules:
- Use [[wiki link]] format for all file references
- Timestamps use local time in HH:MM format (24-hour)
- Show filename, mode (create / append), content summary, and full path, then wait for confirmation before writing
- Print the full path after writing
