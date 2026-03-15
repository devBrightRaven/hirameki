---
description: Pre-decision vault scan
---

Read `## Vault Structure` from `~/.claude/CLAUDE.md` to get the vault path and the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS (the decision being considered — required)
- If $ARGUMENTS is empty, ask: "What decision? (one sentence)" and wait for the answer before continuing. Ask in the language specified in `## Vault Structure` → `language`.

Before committing, scan the vault for relevant context and surface the structure of the decision. No recommendations. No conclusions.

## Execution

1. Scan all content folders for notes related to the topic (title, tags, body keywords)
2. Scan the last 14 days of daily notes and journal files for relevant records
3. Organise output using the three-layer structure below

## Three-layer structure

### Current state
Relevant context found in the vault — what you already know, any prior examples, anything in progress that touches this decision.

Also assess reversibility:
- **Two-way door** — can reverse if wrong; deep analysis is not essential; bias toward action
- **One-way door** — hard to reverse once made; worth spending more time here

### Friction
What is keeping this decision unresolved. Apply inversion: what conditions would guarantee this decision fails? Work backward from failure to find where the tension actually lies. If the vault contains relevant failure records or hesitation logs, surface them.

### Key question
One question only. Not an answer, not a recommendation, not a list of options. The question is: if you knew this, the decision would become clear.

## Output format

```
# Decision scan: {topic}

> Scan time: YYYY-MM-DD HH:MM
> Relevant context: [[note1]], [[note2]], ... (sources found)
> Reversibility: two-way door / one-way door

## Current state
[vault context, with cited sources]

## Friction
[where the tension lies, failure conditions from inversion]

## Key question
[one question]
```

Rules:
- Use [[wiki link]] format for all note references
- If the vault has almost no relevant context, say so directly in Current state — do not fill in
- Do not write "I recommend...", "You should...", or "The best option is..."
- Key question must be a single question — never a list
- This command does not write to any file — output goes to the terminal only. To save the result, run `/hirameki:journal` afterward

Write output in the language specified in `## Vault Structure` → `language`.
