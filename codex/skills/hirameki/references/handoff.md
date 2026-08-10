---
description: Snapshot session state into a handoff doc for future-session pickup.
  Use when work isn't complete and the next session needs explicit guidance.
  Distinct from wrap (records what's done) — handoff captures what's left + how to resume.
argument-hint: "[topic-slug]"
---

Resolve vault configuration through the umbrella Hirameki adapter to get the vault path, handoff folder, templates folder, and language. The umbrella owns any migration fallback; this reference does not read Claude configuration directly.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS (optional)
- A short slug (e.g. `beacon-eval-v2`) → used as the filename slug
- Empty → infer a slug from the session's main topic (ask user to confirm before writing)

---

## Process

### Step 1 — Resolve paths

Use the vault root, `handoff`, and `templates` paths already resolved by the umbrella Hirameki adapter.

Handoff dir: `{vault}/{handoff}/`
Template file (optional reference, do not copy blindly): `{vault}/{templates}/handoff.md`

### Step 2 — Collect session state

Gather the following automatically. Do not ask the user for these:

**Tasks**: Inspect the current plan or task state available in the runtime. Note which are `in_progress` or `pending` (incomplete) and which are `completed`.

**Files touched this session**: Review tool history for Edit/Write calls. List unique file paths modified.

**Decisions made**: Scan conversation for explicit decisions (phrases like "決定", "decided", "we'll", "going with", "the approach is"). Keep only non-obvious choices worth preserving for the next session.

**Judgment updates**: Keep only judgment changes that affect the next session. For each, separate the earlier judgment, the evidence that changed it, the current judgment, remaining unknowns, and the condition for reopening it. Distinguish explicit statements from reasonable inference; omit items with insufficient data rather than completing the story.

**Deferred items**: Scan for items explicitly pushed out ("下次", "後面再做", "deferred", "skip for now", "not in scope"). Note what was deferred and why.

**Background tasks**: Note any `run_in_background` tasks from this session and their status.

### Step 3 — Infer slug

If $ARGUMENTS is not empty, use it as the slug.
If $ARGUMENTS is empty, infer from the main topic of the session. Keep it short (3–5 words, kebab-case, no dates). Show the inferred slug to the user and confirm before writing.

### Step 4 — Draft handoff

Write a handoff document using the following structure. Fill in all sections from Step 2 data. Leave a section blank or write "None" if there is nothing to report — do not omit sections.

```markdown
---
tags:
  - handoff
status: reference
source: codex
created: YYYY-MM-DD HH:MM
topic: <one-line: what the next session needs to resolve>
priority: <high / medium / low>
estimated_cost: <wall time + API cost estimate to complete remaining work>
---

# Handoff — <human-readable title>

> <one paragraph: what's happening, where we are, what the next session must do first>

---

## Re-pickup checklist

1. [ ] 讀本 handoff 全文
2. [ ] 確認相關 memory / vault notes（見「Related artifacts」）
3. [ ] 檢查 git / repo 狀態（見「In flight」）
4. [ ] 跑「Next actions」第一項確認環境正常

---

## What's done

<bulleted list of completed work with file paths where relevant>

---

## In flight

<incomplete tasks, open PRs, background jobs — or "None">

---

## What's deferred

| 項目 | 為什麼擱置 | Revisit trigger |
|------|-----------|-----------------|
<rows, or "None" if empty>

---

## Decisions made

<non-obvious decisions with why + reversal trigger — or "None">

<this section: current constraints or commitments only — formation or change history goes in 判斷更新 below, never repeated here>

---

## 判斷更新

### <問題，一句話>
- 原先判斷：<...>
- 改變依據：<...；推論處標「可合理推論」>
- 目前判斷：<...>
- 尚未知：<...>
- 重新檢視條件：<...>

<one block per judgment update that affects pickup — repeat the heading block, no table. If none, this section contains only: "本次沒有需要接手的判斷更新。">

---

## Next actions

<numbered list in priority order. Each action: one concrete step + expected outcome>

---

## Traps

<specific things the next session must NOT do, or pitfalls to watch for — or "None">

---

## Related artifacts

### Files
<paths with one-line description>

### Vault notes
<[[wikilinks]] with one-line description>
```

### Step 5 — Show draft and confirm

Print the full draft content and the target path:

```
Target: {vault}/{handoff}/YYYY-MM-DD-{slug}.md
```

Ask: "Save to this path? (yes / edit / different-slug)"

- If "yes" → write the file (Step 6)
- If "edit" → take edits inline, then write
- If "different-slug" → ask for new slug, update path, confirm again

### Step 6 — Write

Write to `{vault}/{handoff}/YYYY-MM-DD-{slug}.md`. Print the full path after writing.

### Step 7 — Suggest wrap

After writing, check if `/hirameki:wrap` has already been run this session (look for a Wrap block appended to today's wrap log). If not, suggest:

"Handoff written. If you're done for today, run `/hirameki:wrap` to log the session — wrap covers what happened, handoff covers what's next."

---

## Distinction from related commands

| Command | When | Output |
|---------|------|--------|
| `/hirameki:handoff` | Work unfinished, next session needs explicit guidance | New file in `{handoff}/` |
| `/hirameki:wrap` | End of session, log what happened today | Append to today's wrap log |
| `/hirameki:next` | Start of new session, orient self | Read-only, summarises recent work |
| `/hirameki:tasks` | Global view of open work across vault | Read-only, aggregates |

If unsure which to use: run both. They are complementary, not duplicates.

---

## Rules

- Do not write without user confirmation (Step 5)
- Show full draft content before asking — do not show a summary
- Do not hardcode vault paths — resolve the root from `vault-local.md` and folders from `<vault>/AGENTS.md` every time
- Slug must not contain dates (the filename already has YYYY-MM-DD prefix)
- Do not add a `name:` field to this file's frontmatter — it would break the `hirameki:` prefix
- Do not turn missing evidence into a judgment update. Keep observations, inferences, assumptions, decisions, and later outcomes distinct.
- Write output in the language specified in `## Vault Structure` → `language`
