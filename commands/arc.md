---
description: >
  Trace how one concept evolved across your vault: first appearance, timeline,
  current state, unexplored angles.
  Use when the user asks how an idea developed, when they first thought of it,
  what they used to believe, or whether their thinking has shifted; or says
  "這個想法怎麼來的", "我以前怎麼想", "這概念演變", "什麼時候開始的",
  "how did I get here", "when did I start thinking this", "trace this idea".
  Not for connecting two topics (bridge), attacking an argument (challenge),
  or a pending choice (decision-trace).
argument-hint: "<concept>"
---

Read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path, the research folder location, and the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS
- If $ARGUMENTS is empty, ask: "Trace which concept?" in the language specified in `## Vault Structure` → `language`. Wait for the answer.
- If $ARGUMENTS ends with `save`, strip `save` and write the result to a file after analysis.

Scan scope: entire vault, prioritising content folders.

---

## Analysis logic

1. Check `{research}/arc/` for an existing file about the same concept today (match by filename keyword):
   - Clear match found → **append mode**
   - Possibly related file, uncertain → list candidates and ask the user to confirm
   - No match → **create mode**

---

## Output structure (create mode)

```
# Concept tracking: {concept}

> Analysis time: YYYY-MM-DD HH:MM

## First appearance
Earliest file where this concept appeared, and the context. Quote up to 3 sentences.
Date: YYYY-MM-DD

## Evolution timeline
- YYYY-MM-DD | [[filename]] | How this concept was used or positioned (one line)
(chronological, oldest to newest)

## Current state
Which topics this concept connects to now, any contradictory uses, any drafts developing it.

## Unexplored angles
Aspects of this concept not yet addressed anywhere in the vault.
```

---

## Append mode

Add this block at the end of the matched file:

```
---

## Tracking update [HH:MM]

### Timeline additions
- YYYY-MM-DD | [[filename]] | (new mentions since last analysis, or "None")

### State changes
- (What changed since last analysis. If nothing significant: "No significant change")

### Unexplored angles (updated)
- (Re-evaluate what remains unexplored)
```

Mark any previously listed "Unexplored angles" that are now addressed with a note in the State changes section.

---

## Write logic

Write target: `{research}/arc/YYYY-MM-DD-{concept}.md`

Always print the full output to the terminal first.

If `save` was in the input (or user requests saving):
- Show filename and full path — wait for confirmation before writing
- Print the full path after writing

---

## Rules

- If search results exceed 20 files, list only the 20 most relevant
- Use `[[wiki link]]` format for all file references
- Timestamps use local time in HH:MM (24-hour)
- Write output in the language specified in `## Vault Structure` → `language`
