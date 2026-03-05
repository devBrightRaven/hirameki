---
description: Write or append a work log entry
---

Read `## Vault Structure` from `~/.claude/CLAUDE.md` to get the vault path and the logs folder location. Also retrieve the list of content folders for searching related notes.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Write or append a work log and reasoning record for the given topic.

Input: $ARGUMENTS (topic description — optional)
- If $ARGUMENTS is provided, use it as the topic directly.
- If $ARGUMENTS is empty, infer the topic from session activity (recently modified files, tasks completed, decisions made). Show the inferred topic as a single line — "Topic: {inferred topic} — proceed?" — and wait for a yes/no confirmation before continuing. Do NOT ask open-ended questions.

Scan sources:
- Session activity
- Existing notes in the vault related to the topic (search all content folders)
- Existing journal files in the logs folder starting with today's date

Execution logic:
1. Scan the logs folder for all YYYY-MM-DD-*.md files starting with today's date
2. Compare each file's name and title against the keywords of the input topic
3. If a clear match is found → Append mode
4. If a possibly related file is found but uncertain → List candidates and ask whether to append or create new
5. If no match → Create mode

### Create mode

Create a file in the logs folder. Filename format: `YYYY-MM-DD-HHMM-{topic-slug}.md` (HHMM is the local time of creation, no colon).

Filename slug language rules:
- Language is Traditional Chinese → use Chinese (e.g. `2026-03-03-1430-hirameki指令精煉.md`)
- Language is Japanese → use Japanese (e.g. `2026-03-03-1430-hirameki指令改善.md`)
- Language is English or other → use English (e.g. `2026-03-03-1430-hirameki-command-refactor.md`)

Replace spaces with hyphens. Avoid special characters.

File structure:

```
# {topic}

> Created: YYYY-MM-DD HH:MM

## Background
What prompted this. If related prior notes exist in the vault, reference them with [[wiki links]].

## What was done
Specific actions and decisions taken, with cause-and-effect narrative.

## Why this approach
Reasoning behind key decisions. If trade-offs were made, describe what was chosen and what was set aside.

## Inspiration connections
Links to other ideas, possible extensions, cross-topic connections. Use [[wiki links]]. If none, write "None."

## Possible improvements
Unexplored directions, alternatives, potential risks worth investigating. If none, write "None."

## Open items
Things still to follow up on. If all done, write "No open items."
```

### Append mode

Add to the end of the matched file:

```
---

## Addendum [HH:MM]

### What was done
[New actions and decisions]

### Why this approach
[Reasoning for new decisions]

### Inspiration connections
[New connections or extensions. If none, write "None."]

### Possible improvements
[New directions to explore. If none, write "None."]
```

Also check the "Open items" section — if any items are now complete, mark them with "✓ Done [HH:MM]".

Rules:
- Timestamps use local time in HH:MM format (24-hour)
- Show filename, mode (create / append), content summary, and full path, then wait for confirmation before writing
- Print the full path after writing
- Append mode does not modify existing content — only adds to the end and updates completion status

Write output in the language specified in `## Vault Structure` → `language`.
