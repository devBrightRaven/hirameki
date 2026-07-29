---
description: >
  Deep-dive one topic by walking arc, positions, bridge and challenge as a single flow;
  each step saves or skips independently.
  Use when the user wants to understand a topic thoroughly rather than answer one
  question about it, or says "我想把這個搞懂", "完整看一遍", "深入研究這個主題",
  "help me really understand X", "go deep on this", "give me the full picture".
  Not for a single narrow question, which the individual steps answer faster.
argument-hint: "<topic or concept>"
---

Read `## Vault Structure` from `~/.claude/vault-local.md` (fall back to `~/.claude/CLAUDE.md` if not found) to get the vault path, the research folder location, and the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS
- A single topic or concept (required).
- If $ARGUMENTS is empty, ask: "Lens on which topic?" in the language specified in `## Vault Structure` → `language`. Wait for the answer.

Print before starting:
```
Lens on: {topic}
```

---

## Step 0 — Shared context (run once, all steps draw from it)

Before the first sub-flow, scan the vault for the topic. Collect:
- All files that mention the topic (used in steps 1, 2, 4)
- The earliest and most recent file dates (for step 1 timeline)
- Related topics that co-appear with this one (for step 3 partner suggestion)

---

## [1/4] Arc — How did this concept evolve?

Run the same logic as `/hirameki:arc`:

1. Check `{research}/arc/` for an existing arc file for this concept today:
   - Match found → append mode (add a Tracking update block)
   - No match → create mode

**Create mode output**:

```
# Concept tracking: {topic}

> Analysis time: YYYY-MM-DD HH:MM

## First appearance
Earliest file where this concept appeared. Quote up to 3 sentences.
Date: YYYY-MM-DD

## Evolution timeline
- YYYY-MM-DD | [[filename]] | How this concept was used or positioned (one line)

## Current state
Topics this concept connects to now, contradictory uses, drafts developing it.

## Unexplored angles
Aspects not yet addressed anywhere in the vault.
```

**Append mode**: add a Tracking update block (same as arc.md append mode).

Print full output. Then:

```
[1/4] Arc — Action? (save / skip / next)
```

- `save` → write to `{research}/lens/YYYY-MM-DD-{topic}-arc.md`, print path, proceed to [2/4]
- `skip` → do not write, proceed to [2/4]
- `next` → same as skip

---

## [2/4] Positions — What has the vault said about this topic?

Extract all explicit positions and claims about the topic from the vault.

Rules:
- Only claims directly about this topic — no tangential mentions
- One claim per source — the most specific or clearly-stated one
- Limit: 10 most relevant sources
- Do NOT compose an answer or voice response — pure extraction only

Output:

```
## Positions on: {topic}

> Analysis time: YYYY-MM-DD HH:MM

| Source | Claim |
|--------|-------|
| [[filename]] | The specific position or claim (one sentence) |
| [[filename]] | ... |

### Tensions
(If two or more claims contradict each other, name the tension here.
If all claims point in the same direction: "No significant tension found.")

### Gaps
(Angles on this topic that appear in no vault note — aspects that remain unaddressed.)
```

Print full output. Then:

```
[2/4] Positions — Action? (save / skip / next)
```

- `save` → write to `{research}/lens/YYYY-MM-DD-{topic}-positions.md`, print path, proceed to [3/4]
- `skip` or `next` → proceed to [3/4]

---

## [3/4] Bridge — What topic connects here?

Auto-suggest the most likely partner topic from step 0 shared context (the topic that co-appears most frequently with this one, or the most prominent theme in the Unexplored angles from step 1).

Print the suggestion before running:

```
[3/4] Bridge — Partner topic suggested: {suggested-topic}
  Action? (save / skip / change-partner)
```

- `save` or pressing enter → accept the partner, run bridge, print result, then prompt final save
- `skip` → do not run bridge, proceed to [4/4]
- `change-partner` → ask: "Bridge {topic} with which other topic?" — wait for input, then run bridge

Bridge logic (same as `/hirameki:bridge`):
1. Find direct intersections — files mentioning both topics
2. Find bridge notes — files mentioning one that could link to the other (limit 5)
3. Propose 1–3 hypotheses about deeper connections

Output format:

```
# Bridge: {topic} × {partner-topic}

## Direct intersections
- [[filename]] — how the two topics relate here

## Bridge notes
- [[filename]] — why this could connect them

## Hypotheses
1. [Hypothesis] — confidence: strong/medium/weak
   Evidence: [[filename]]
```

After showing output:

```
[3/4] Bridge — Save this? (save / skip)
```

- `save` → write to `{research}/lens/YYYY-MM-DD-{topic}-bridge.md`, print path, proceed to [4/4]
- `skip` → proceed to [4/4]

---

## [4/4] Challenge — What are the weaknesses in these positions?

Run the same logic as `/hirameki:challenge` using the positions surfaced in step 2 (plus any additional claims from the vault scan).

For each claim, check:
- Internal contradiction: conflicting statements across vault files
- Unverified assumption: claim rests on an unproven premise
- Logic gap: missing steps in the argument
- Evidence gap: claim lacks supporting data or examples

Output:

```
## Challenge: {topic}

> Analysis time: YYYY-MM-DD HH:MM

## Claims assessed
(Same claims as step 2, or extended from vault scan)

## Weaknesses
### Claim: {claim} — [[source]]
- [Only list weakness types that apply]

(Omit claims with no weaknesses)

## Assessment
Overall: solid / mostly solid with gaps / needs major work
Top 1–3 weaknesses worth addressing first.
```

Print full output. Then:

```
[4/4] Challenge — Action? (save / skip / next)
```

- `save` → write to `{research}/lens/YYYY-MM-DD-{topic}-challenge.md`, print path, then show summary
- `skip` or `next` → show summary

---

## Completion summary

After all four sub-flows:

```
Lens done: arc {✓ saved | – skipped} / positions {✓ saved | – skipped} / bridge {✓ saved | – skipped} / challenge {✓ saved | – skipped}
```

---

## Rules

- Do not hardcode vault paths — resolve from vault-local.md every time
- Use `[[wiki link]]` format for all vault note references
- Timestamps use local time in HH:MM (24-hour)
- Always print the full output for each step before the Action? prompt
- Do not skip any sub-flow automatically — always show and let the user decide
- Print the full path after each write
- Write output in the language specified in `## Vault Structure` → `language`
