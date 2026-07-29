---
description: >
  Orient after resuming: what was done, what is still open, what to do next.
  Use at the start of a session when the user asks where they left off, or says
  "我做到哪", "上次進度", "接下來做什麼", "回顧一下",
  "where was I", "what's the state", "catch me up", "what should I do next".
  Not for listing open action items across notes (tasks).
---

Read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path and the locations of the daily-notes and inbox folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS (optional)
- Empty → default mode
- `lucky` → default mode + constellation reading appended at the end
- A number (e.g. `3`) → look back N days for daily notes context (default 1)

Scan the current session and vault to produce a concise orientation summary.

## Scan sources

- Task list (all tasks and their status)
- Session activity: files created or modified, decisions made, commits pushed
- Any open items, blockers, or unresolved questions raised during the session
- **Inbox folder**: all files in `{inbox}/`
- **Yesterday's daily note**: last Wrap block from `{daily}/YYYY-MM-DD.md` (yesterday, or N days back if a number is given)

## Output format

Respond in the language specified in `## Vault Structure` → `language`.

### 做了什麼 / Done
Bullet list of what was accomplished this session. Max 5 items. Be specific — name files, features, or decisions, not vague summaries.

### 還開著的 / Open
Bullet list of things that are in-progress, blocked, or explicitly deferred. If nothing, write "無".

### 收件匣 / Inbox
List all files in the inbox folder. For each: filename, creation date, one-sentence summary.
If inbox is empty, write "收件匣清空" / "Inbox clear".
Limit: 10 items.

### 昨天的脈絡 / Yesterday
Extract "In progress" and "Next" items from the last Wrap block in yesterday's daily note (or N days back).
If no daily note or no Wrap block exists, write "無紀錄" / "No record".

### 下一步 / Next
2–4 concrete, actionable options ranked by naturalness:
- Continue the most obvious incomplete thread
- A smaller side task that could be done quickly
- If inbox has actionable items, suggest processing them
- If both main tracks are done: suggest ending the session

### 該結束了嗎 / Wrap up?
One sentence: either "還有明確的下一步，繼續吧。" or "這個 session 已到自然結束點。建議執行 `/hirameki:wrap`。"

---

## Lucky mode — `next lucky`

After the standard output above, append a constellation reading.

### Selection logic

Draw 5 notes from content folders with the following weighting:

- **Prefer neglected notes** — not modified in the last 30 days (weight: 3×)
- **Include recent notes** — modified in the last 30 days (weight: 1×)
- **Exclude** system folders, `_hirameki_cmds/`, daily-notes, inbox, analysis, logs

Read the content of each selected note (up to 500 words per note).

### Analysis

Find what sits at the **centre** of all 5 notes — not a surface keyword match, but the underlying tension, preoccupation, or unresolved question that could have generated all of them.

### Output (appended after Wrap up? section)

```
---

### 星座 / Constellation

> [[note1]], [[note2]], [[note3]], [[note4]], [[note5]]

**隱藏主題 / Hidden theme**
[The concept or tension at the centre — 3 to 5 sentences.
Cite which notes point to which aspect using [[wiki links]].]

**你可能在問的問題 / The question you might be asking**
[One question. Not an answer. Not a summary.]
```

---

## Rules

- Do not ask clarifying questions — infer everything from session context and vault
- Keep each section tight: no padding, no filler
- If the task list is empty and session activity is minimal, say so directly and suggest wrapping
- Use [[wiki link]] format for all note references
- The constellation question must be one sentence — never a list
- If the drawn notes have nothing in common, say so directly — do not fabricate a connection
