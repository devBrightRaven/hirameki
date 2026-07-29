---
description: >
  Vault pulse: `snapshot` for a folder-by-folder overview, `week` for gap analysis
  between stated priorities and actual file changes, `patterns` for recurring
  undercurrents across notes.
  Use when the user asks how the vault is doing, what has gone quiet, what they
  said they would do but did not, or says
  "vault 現在什麼狀況", "哪些荒廢了", "這週做了什麼", "我最近在想什麼",
  "how's my vault", "what went stale", "what did I actually work on".
  Not for open action items (tasks) or a session recap (next).
---

Read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path, the wrap folder location, and the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS (required — `snapshot`, `week`, or `patterns`)
- If $ARGUMENTS is empty, respond: "Which pulse? `snapshot` (vault overview), `week` (gap analysis), or `patterns` (undercurrents)."

Note: the snapshot used to run automatically at session start. It was moved here because it reported the same numbers every session, which trains the reader to skip the whole block. SessionStart now speaks only when something is new or waiting.

---

## `pulse snapshot` — vault overview

Scan every content folder at the vault root, skipping dotfolders and `_hirameki_cmds`, `_templates`, `node_modules`.

Report:
- Total note count
- Per folder: note count, and whether it is active (any file modified in the last 7 days) or dormant
- Inbox: item count, and the name and age of each item

Close with one line naming the folder that has gone longest without a change, so dormancy is visible rather than merely listed.

---

## `pulse week` — weekly gap analysis

Read:
- Modification history of all content folders over the last 7 days
- Wrap logs from the last 7 days in the wrap folder

Output in three sections:

**This week's progress**
For each content folder with activity: name, what was advanced (inferred from file changes), what comes next.

**Recent updates**
Notes added or modified this week. Flag any that appear close to completion (if drafts/ has content).

**Gap analysis**
Compare stated priorities in wrap logs against actual file changes. Find:
- Declared important but untouched (mentioned as priority but no matching file changes)
- Worked on but unmentioned (file changes with no mention in wrap logs)

If fewer than 3 days of wrap logs are available, note "Insufficient records — gap analysis may be inaccurate."

---

## `pulse patterns` — undercurrent and cluster scan

Scan scope:
- All content folders (unlimited depth)
- Last 30 days in the wrap folder
- All files in the inbox folder

Output in two sections:

**Undercurrents**
Themes that recur across notes but have no standalone article. For each:
- Theme name
- Occurrence count and number of files involved (up to 5 example [[wiki links]])
- Assessment: is this theme worth developing?

Criteria: appears in 3+ distinct files, no standalone article or draft uses it as the primary subject.
Limit: 10 undercurrents, sorted by frequency descending.

**Forming idea clusters**
Groups of 3+ notes covering similar concepts without a shared category. For each:
- Suggested cluster name
- Notes involved ([[wiki link]] format, limit 5)
- Shared theme summary (2-3 sentences)
- Maturity: high / medium / low
- Suggested direction: article / project / conceptual framework / keep accumulating

Limit: 5 clusters, sorted by maturity descending.

---

Write output in the language specified in `## Vault Structure` → `language`.
