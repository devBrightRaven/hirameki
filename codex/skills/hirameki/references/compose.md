---
description: >
  Topic-driven creation workflow — voice composition followed by a five-question
  frame test. Use before investing effort in writing.
  Compose is standalone — does not require /hirameki:lens to have run first.
  For standalone use: /hirameki:reflect (voice only), /hirameki:frame (frame only).
  For deep understanding before creating, run /hirameki:lens first.
argument-hint: "<topic or question>"
---

Read `## Vault Structure` from `~/.claude/vault-local.md` (fall back to `~/.claude/CLAUDE.md` if not found) to get the vault path, the research folder location, and the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS
- A topic or question to write about (required).
- If $ARGUMENTS is empty, ask: "Compose on which topic or question?" in the language specified in `## Vault Structure` → `language`. Wait for the answer.

Print before starting:
```
Compose on: {topic or question}
```

---

## [1/2] Voice — Write in my own voice

Run the same logic as `/hirameki:reflect`:

### Step 1 — Analyse writing style

Scan completed articles in content folders (exclude `drafts/` and `thoughts/` subdirectories if present).

Extract:
- Sentence patterns and typical length
- Vocabulary level and recurring phrasing
- Argument structure (how claims are introduced, supported, qualified)
- Rhetorical moves that appear repeatedly

### Step 2 — Extract positions

Search the full vault for notes relevant to the topic. Prioritise:
- Notes in content folders that address the topic directly
- Permanent concept cards related to the topic
- Journal entries where the author took a position
- Daily notes with relevant observations

Limit: 5 most relevant sources.

### Step 3 — Compose answer

Write an answer using the identified style and the extracted positions. Rules:
- Match the length of a typical paragraph from their writing
- Use the author's own arguments, not general knowledge
- Do not introduce positions the vault does not support
- If the vault has contradictory positions on the topic, surface the tension rather than resolving it

### Output

```
[Answer]
The answer in the author's voice. One to three paragraphs.

[Sources]
- [[note-title]] — the specific position or passage drawn from
(Limit: 5 sources)

[Confidence]
- Vault-supported: which parts have direct evidence
- Style-inferred: which parts extend the style without direct backing
- Tensions: any contradictions found across vault notes
```

Print full output. Then:

```
[1/2] Voice — Action? (save / skip / edit-question)
```

- `save` → write to `{research}/compose/YYYY-MM-DD-{topic}-voice.md`, print path, proceed to [2/2]
- `skip` → do not write, proceed to [2/2]
- `edit-question` → ask: "Revised topic or question?" — wait for input, rerun voice step with new input

---

## [2/2] Frame — Does this pass the five-question test?

Run the same logic as `/hirameki:frame`, treating the voice output from [1/2] as the idea to frame.

If [1/2] was skipped, ask: "Frame which idea?" — wait for the user to describe the idea.

### Phase 1: Understand the idea

Determine the type of creative work (Article / Product / Design).

Print the thesis and type, then proceed.

### Phase 2: Five-question frame test

**Q1 — Only-I test**: What is this saying that only I can say?
- Scan vault for personal experiences, unique perspectives, proprietary knowledge
- Evaluate: Strong / Weak / None

**Q2 — Collision scan**: Does something I've already made cover this?
- Tier 1 — Published work: absorbed / adjacent / superseded
- Tier 2 — Unpublished drafts: competing / adjacent / feeds

**Q3 — Stakes**: After encountering this, what changes for the reader?
- Reframes / Equips / Provokes / None of the above

**Q4 — Tension**: What is the surprising or counterintuitive part?
- Contradiction the author is willing to sit with / Reversal / Confession

**Q5 — Evidence**: What lived experience or data makes this credible?
- Embodied / Researched / Speculative

### Phase 3: Verdict

Assign one of: **PROCEED** / **RETHINK** / **KILL** / **CONSOLIDATE**

```
PROCEED — Q1 Strong + at least one of Q3/Q4 strong + no Tier 1 absorbed collision

## Frame: PROCEED
**Thesis**: [one sentence]
**Unique angle**: [from Q1]
**Core tension**: [from Q4]
**Key evidence**: [from Q5]
### Before starting
- [1-2 specific things to nail down]


RETHINK — Q1 Weak or adjacent collision or Q3 "informs only"

## Frame: RETHINK
**Thesis**: [one sentence]
**Problem**: [which questions failed and why]
### What would make this worth doing
- [1-3 specific directions]
### Existing work to build on
- [[filename]] — [how it relates]


KILL — Q1 None or Tier 1 absorbed or both Q3 and Q4 empty

## Frame: KILL
**Thesis**: [one sentence]
**Reason**: [one sentence]
**Salvageable parts**: [any fragments worth keeping, or "none"]


CONSOLIDATE — Q2 has multiple Tier 2 competing drafts

## Frame: CONSOLIDATE
**Thesis**: [one sentence]
**Competing drafts**:
- [[draft 1]] — strength: X, weakness: Y
**Recommended vessel**: [[strongest draft]] — because [reason]
**Parts to absorb from other drafts**: [specific content]
**Drafts to retire after consolidation**: [list]
```

Print full output. Then:

```
[2/2] Frame — Action? (save / skip / next)
```

- `save` → write to `{research}/compose/YYYY-MM-DD-{topic}-frame.md`, print path, then show summary
- `skip` or `next` → show summary

---

## Completion summary

```
Compose done: voice {✓ saved | – skipped} / frame {✓ saved | – skipped}
```

---

## Rules

- Do not hardcode vault paths — resolve from vault-local.md every time
- Use `[[wiki link]]` format for all vault note references
- Timestamps use local time in HH:MM (24-hour)
- Always print the full output for each step before the Action? prompt
- Do not skip any sub-flow automatically — always show and let the user decide
- Never soften the frame verdict — if KILL, say KILL
- Frame does not generate content — it only evaluates whether content should exist
- Print the full path after each write
- Write output in the language specified in `## Vault Structure` → `language`
