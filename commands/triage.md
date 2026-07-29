---
description: End-of-session checkpoint — walks wrap, journal, and handoff in one flow.
  Shows a draft for each and lets you save, skip, or edit before moving on.
  Wrap and journal and handoff remain callable individually.
---

Read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path and folder locations: daily, journal, handoff, templates.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS — ignored. Triage takes no arguments.

---

## Step 0 — Collect session state (shared)

Gather this once. All three sub-flows draw from it — do not re-scan per sub-flow.

**Files touched**: Review Edit/Write tool history this session. Collect unique file paths modified or created.

**Tasks**: Call TaskList. Note which are `in_progress` or `pending` (incomplete) and which are `completed`.

**Decisions**: Scan conversation for non-obvious choices (phrases like "決定", "decided", "going with", "the approach is", "we'll"). Keep only decisions worth preserving.

**Corrections**: Scan conversation for anything the user corrected Claude on. Format each as "Wrong: [what Claude did] → Right: [what the user wanted]".

**Deferred items**: Scan for items pushed out ("下次", "後面再做", "deferred", "skip for now", "not in scope").

---

## Sub-flow 1 of 3 — Wrap

Generate a wrap block using the shared state above. Follow the same logic as `/hirameki:wrap`:

- Infer session focus from files touched and completed tasks
- Fill Done / In progress / Next sections
- Use action type tags (`#feature`, `#bug-fix`, `#research`, etc.) and project tags

Draft format:

```
## Wrap [HH:MM]

### Done
- **Item title** `#action-type` `#project`
  Description (optional)

### In progress
- item or "None"

### Next
- item or "TBD"
```

Write target: `{daily}/YYYY-MM-DD.md`
- If file does not exist and templates folder has daily.md → create from template
- If file does not exist and no template → create with `# YYYY-MM-DD` heading only
- If file exists → will append after `---` horizontal rule

Show the full draft and the target path. Then ask:

```
[1/3] Wrap — Action? (save / skip / edit)
```

- `save` → write immediately, print path, proceed to sub-flow 2
- `skip` → do not write, proceed to sub-flow 2
- `edit` → take inline edits, show revised draft, confirm, then proceed

---

## Sub-flow 2 of 3 — Journal

Generate a journal entry using the shared state above. Follow the same logic as `/hirameki:journal`:

- Infer topic from session activity (files, tasks, decisions)
- Check `{journal}/` for a file matching today's date and the inferred topic keyword
  - Clear match → append mode (add Addendum block)
  - No match → create mode (new file with full structure)

**Create mode** — filename: `YYYY-MM-DD-HHMM-{topic-slug}.md`

Slug language: Traditional Chinese slug if language setting is Chinese (e.g. `2026-05-14-1430-hirameki指令整合.md`).

File structure:

```markdown
---
tags:
  - journal
  - {relevant-topic-tags}
status: log
source: claude-code
actions:
  - type: {action-type}
    project: {project-name}
corrections: {count of corrections found in Step 0}
---

# {topic}

> Created: YYYY-MM-DD HH:MM

## Background
What prompted this. Reference related vault notes with [[wiki links]].

## What was done
Specific actions and decisions taken.

## Why this approach
Reasoning behind key decisions.

## Inspiration connections
Links to other ideas. [[wiki links]]. If none: "None."

## Possible improvements
Unexplored directions or risks. If none: "None."

## Corrections
{corrections from Step 0 — one line each, or "None."}

## Open items
{incomplete tasks from Step 0, or "No open items."}
```

**Append mode** — add Addendum block at end of matched file. Mark completed Open items with "✓ Done [HH:MM]".

Show the full draft and the target path. Then ask:

```
[2/3] Journal — Action? (save / skip / edit)
```

- `save` → write immediately, print path, proceed to sub-flow 3
- `skip` → do not write, proceed to sub-flow 3
- `edit` → take inline edits, show revised draft, confirm, then proceed

---

## Sub-flow 3 of 3 — Handoff

Generate a handoff document using the shared state above. Follow the same logic as `/hirameki:handoff`:

- Infer slug from session's main topic (3–5 words, kebab-case, no dates)
- Show the inferred slug in the draft header — user confirms or adjusts via `edit`

Draft structure:

```markdown
---
tags:
  - handoff
status: reference
source: claude-code
created: YYYY-MM-DD HH:MM
topic: <one-line: what the next session needs to resolve>
priority: <high / medium / low>
estimated_cost: <wall time + API cost estimate>
---

# Handoff — <human-readable title>

> <one paragraph: current state and what the next session must do first>

---

## Re-pickup checklist

1. [ ] 讀本 handoff 全文
2. [ ] 確認相關 memory / vault notes（見「Related artifacts」）
3. [ ] 檢查 git / repo 狀態（見「In flight」）
4. [ ] 跑「Next actions」第一項確認環境正常

---

## What's done
<bulleted list of completed work with file paths>

---

## In flight
<incomplete tasks from Step 0, or "None">

---

## What's deferred

| 項目 | 為什麼擱置 | Revisit trigger |
|------|-----------|-----------------|
<rows from Step 0 deferred items, or "None">

---

## Decisions made
<non-obvious decisions from Step 0, or "None">

---

## Next actions
<numbered, priority-ordered concrete steps>

---

## Traps
<things the next session must NOT do, or "None">

---

## Related artifacts

### Files
<paths with one-line description from Step 0>

### Vault notes
<[[wikilinks]] with one-line description>
```

Write target: `{vault}/{handoff}/YYYY-MM-DD-{slug}.md`

Show the full draft and the target path. Then ask:

```
[3/3] Handoff — Action? (save / skip / edit)
```

- `save` → write immediately, print path
- `skip` → do not write
- `edit` → take inline edits, show revised draft, confirm, then write

---

## Completion summary

After all three sub-flows finish, print one line:

```
Triage done: wrap {✓ saved | – skipped} / journal {✓ saved | – skipped} / handoff {✓ saved | – skipped}
```

---

## Rules

- Never write any file without confirmation at the `Action?` prompt
- Show the FULL draft content — not a summary — before each prompt
- Do not skip any sub-flow automatically, even if content seems sparse; always show the draft and let the user decide
- Do not accept $ARGUMENTS input — triage always runs all three sub-flows
- Timestamps use local time in HH:MM format (24-hour)
- Print the full path after each write
- Do not add a `name:` field to this file's frontmatter — it would break the `hirameki:` prefix
- Write section headings and output in the language specified in `## Vault Structure` → `language`
