---
description: Vault pulse check — weekly gaps or undercurrent patterns. Default snapshot runs automatically via SessionStart hook.
---

Read `## Vault Structure` from `~/.claude/vault-local.md` (fall back to `~/.claude/CLAUDE.md` if not found) to get the vault path, the daily folder location, and the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS (required — `week` or `patterns`)
- If $ARGUMENTS is empty, respond: "Which pulse? `week` (gap analysis) or `patterns` (undercurrents). The default snapshot runs automatically at session start."

Note: The instant vault snapshot (content themes, recent activity, vault overview) now runs automatically via the SessionStart hook. Use this command for deeper analysis.

---

## `pulse week` — weekly gap analysis

Read:
- Modification history of all content folders over the last 7 days
- Daily notes from the last 7 days in the daily folder

Output in three sections:

**This week's progress**
For each content folder with activity: name, what was advanced (inferred from file changes), what comes next.

**Recent updates**
Notes added or modified this week. Flag any that appear close to completion (if drafts/ has content).

**Gap analysis**
Compare stated priorities in daily notes against actual file changes. Find:
- Declared important but untouched (mentioned as priority but no matching file changes)
- Worked on but unmentioned (file changes with no mention in daily notes)

If fewer than 3 days of daily notes are available, note "Insufficient records — gap analysis may be inaccurate."

---

## `pulse patterns` — undercurrent and cluster scan

Scan scope:
- All content folders (unlimited depth)
- Last 30 days in the daily folder
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
