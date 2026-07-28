---
description: Write or append a work log entry. Use "review" to extract rule updates from recent corrections.
---

Resolve vault configuration through the umbrella Hirameki adapter to get the vault path, journal folder, content folders, and language. The umbrella owns any migration fallback; this reference does not read Claude configuration directly.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Write or append a work log and reasoning record for the given topic.

Input: $ARGUMENTS (topic description — optional)
- If $ARGUMENTS is provided, use it as the topic directly.
- If $ARGUMENTS is empty, infer the topic from session activity (recently modified files, tasks completed, decisions made). Show the inferred topic as a single line — "Topic: {inferred topic} — proceed?" — and wait for a yes/no confirmation before continuing. Do NOT ask open-ended questions.

Scan sources:
- Session activity
- Existing notes in the vault related to the topic (search all content folders)
- Existing journal files in the journal folder starting with today's date

Execution logic:
1. Scan the journal folder for all YYYY-MM-DD-*.md files starting with today's date
2. Compare each file's name and title against the keywords of the input topic
3. If a clear match is found → Append mode
4. If a possibly related file is found but uncertain → List candidates and ask whether to append or create new
5. If no match → Create mode

### Create mode

Create a file in the journal folder. Filename format: `YYYY-MM-DD-HHMM-{topic-slug}.md` (HHMM is the local time of creation, no colon).

Filename slug language rules:
- Language is Traditional Chinese → use Chinese (e.g. `2026-03-03-1430-hirameki指令精煉.md`)
- Language is Japanese → use Japanese (e.g. `2026-03-03-1430-hirameki指令改善.md`)
- Language is English or other → use English (e.g. `2026-03-03-1430-hirameki-command-refactor.md`)

Replace spaces with hyphens. Avoid special characters.

File structure:

```
---
tags:
  - journal
  - {relevant-topic-tags}
status: log
source: codex
actions:
  - type: {action-type}
    project: {project-name}
corrections: 0
---

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

## Corrections
Things the user corrected the agent on during this session. Each item = one correction.
Format: "Wrong: [what the agent did] → Right: [what the user wanted]"
If no corrections happened, write "None."
These corrections are candidates for agent-guidance updates after review and explicit user approval.

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
- Frontmatter `actions` array is required in Create mode. Use action types from this list:
  `test-rewrite` `test-fix` `code-review` `config-update` `hook-setup`
  `automation` `feature` `bug-fix` `refactor` `research` `vault-write`
  `git-ops` `design` `infra` `skill-dev` `debug`
  If none fits, use a short descriptive slug. Project name should match the short name (e.g. journal, library, dotclaude, asagiri, hirameki, vault).

Write output in the language specified in `## Vault Structure` → `language`.

---

## Review mode — `journal review`

Input: $ARGUMENTS = `review` or `review N` (N = number of days to scan, default 7)

Scan recent journal entries for `## Corrections` sections and propose updates to the owning Codex personal- or project-layer guidance.

### Step 1 — Collect corrections

Read all `{journal}/YYYY-MM-DD-*.md` files from the past N days.
Extract items from `## Corrections` sections.
Skip entries marked "None."
If no corrections found, respond: "No corrections found in the past N days." and stop.

### Step 2 — Deduplicate against existing rules

For each correction, search for existing coverage:
- Search `~/.codex/AGENTS.md` and existing Codex personal-layer guidance for personal workflow facts
- Search the applicable project `AGENTS.md` files for repository requirements
- If already covered → mark as "SKIP — already exists in {file}:{line}"

### Step 3 — Filter one-time issues

For each remaining correction, assess:
- Did this type of issue appear in 2+ different sessions? → KEEP
- Is it a general pattern that could recur? → KEEP
- Was it a one-time situational mistake? → mark as "SKIP — one-time"

### Step 4 — Route to correct file

For each KEEP correction, determine the target file:

| Fact ownership | Target file |
|-------|------------|
| Personal workflow, environment, communication, cross-project preferences | `~/.codex/AGENTS.md` or the existing owning Codex personal-layer file |
| Requirements needed by any agent working in one repository | Applicable project `AGENTS.md` |
| Vault knowledge or reflection | Keep in the vault; do not treat it as runtime guidance |

Before proposing a personal-layer edit, read `~/.codex/agent-docs-constitution.md` when present. Do not create a parallel rules file when an existing file already owns the fact.

### Step 5 — Check for merge opportunities

Before adding a new rule, check if it can be merged with an existing rule in the target file.
Prefer updating an existing bullet point over adding a new one.

### Step 6 — Output

Show a table:

```
=== Corrections Review (past N days) ===

SKIP (already covered):
  - "..." → exists in rules/common/testing.md:12

SKIP (one-time):
  - "..." → one-time situational issue

PROPOSED UPDATES:
  1. [UPDATE] rules/common/coding-style.md
     Merge into existing rule: "..."
     + "new wording"

  2. [ADD] ~/.codex/AGENTS.md → ## Environment
     + "new rule"
```

Wait for user confirmation before making any changes.
Apply only the changes the user approves (user may approve selectively).

Rules:
- NEVER add a rule without checking for duplicates first
- NEVER modify Codex or project guidance without explicit user approval
- NEVER copy Claude personal config into a repository or use the vault as runtime config
- Prefer merging into existing rules over adding new ones
- Show the exact diff (old → new) for merge operations
