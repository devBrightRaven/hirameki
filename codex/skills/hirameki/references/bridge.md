---
description: >
  Find hidden connections between two topics already in your vault.
  Use when the user names two subjects together and wonders how they relate, or says
  "這兩個有關係嗎", "X 跟 Y 怎麼連", "這兩條線接得起來嗎",
  "how do these two relate", "is there a link between", "connect X and Y".
  Also fires before writing, when two ideas keep co-occurring in the user's notes.
  Not for one concept's history (arc) or finding flaws (challenge).
argument-hint: "<topic A> and <topic B>"
---

Read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path and the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS
- Two topics separated by `and`, `與`, or `と`.
- If $ARGUMENTS is empty, ask: "Bridge which two topics?" in the language specified in `## Vault Structure` → `language`.
- If only one topic is given, ask for the second.

---

## Process

### Step 1 — Find direct intersections

Search the entire vault for files that mention both topics. For each match:
- Note the filename and the passage where both appear
- Describe how the two topics are related in that context

If no direct intersections exist, write "No direct intersections."

### Step 2 — Find bridge notes

Search for files that mention only one topic but could link to the other. Limit: 5 files.
For each bridge note, explain why it could connect the two topics.

### Step 3 — Generate hypotheses

Propose 1–3 hypotheses about deeper connections between the topics.
For each hypothesis:
- State the hypothesis in one sentence
- Assign confidence: strong / medium / weak
- Cite the vault evidence that supports it

### Step 4 — Output

```
# Bridge: {topic A} × {topic B}

## Direct intersections
- [[filename]] — how the two topics relate here
(or "No direct intersections.")

## Bridge notes
- [[filename]] — why this could connect them

## Hypotheses
1. [Hypothesis] — confidence: strong/medium/weak
   Evidence: [[filename]], [[filename]]
```

Always print the full output to the terminal. Do not write to a file unless the user asks.
If the user asks to save, write to `{research}/bridge/YYYY-MM-DD-{topic-A}-{topic-B}.md`. Print the full path after writing.

---

Write output in the language specified in `## Vault Structure` → `language`.
