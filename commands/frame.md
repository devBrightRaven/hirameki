---
description: Pre-creation checkpoint — validate core idea before investing effort
---

Read `## Vault Structure` from `~/.claude/vault-local.md` (fall back to `~/.claude/CLAUDE.md` if not found) to get the vault path, the language setting, and the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Validate the core idea of a creative work before investing effort. Applies to articles, products, designs, or any creative output.

Input: $ARGUMENTS
- If $ARGUMENTS is empty, ask: "Frame what? (article idea, product concept, design direction, or path to existing draft)" in the language specified in `## Vault Structure` → `language`. Wait for the answer before continuing.
- If $ARGUMENTS is a file path (relative or absolute), read the file and extract the idea from its content.

---

## Phase 1: Understand the idea

Determine the type of creative work:

| Signal | Type |
|--------|------|
| File path to a draft `.md` in the vault | **Article** |
| Mentions audience, readers, publishing | **Article** |
| Mentions users, features, UX, interface | **Product** |
| Mentions visual, layout, brand, identity | **Design** |
| Ambiguous | Ask: "This is for an article, product, or design?" |

For articles from existing drafts: read the file, extract the working thesis in one sentence.
For new ideas: restate the idea as a single sentence thesis.

Print the thesis and type, then proceed.

---

## Phase 2: Five-question frame test

Run all five questions. For each, scan the vault for evidence.

### Q1: Only-I test

> "What is this saying or doing that only I can say or do?"

Scan: all content folders + daily notes + journal for related personal experiences, unique perspectives, proprietary knowledge, or lived situations.

Evaluate:
- **Strong**: The idea is grounded in a specific experience, skill combination, or position that few others share
- **Weak**: The idea could be written/built by anyone with the same information
- **None**: There is nothing unique about the creator's relationship to this idea

### Q2: Collision scan

> "Does something I've already made cover this?"

Scan: all content folders + drafts for published or in-progress work that overlaps with this thesis.

Separate results into two tiers:

**Tier 1 — Published work** (status: published in frontmatter, or in a non-draft folder):
For each collision found, report:
- File: `[[filename]]`
- Overlap: what it already covers
- Verdict: **absorbed** (the published work already said it better), **adjacent** (related but distinct angle), or **superseded** (this new idea would replace the old one)

A Tier 1 **absorbed** collision is a strong signal to kill or rethink. The idea is already out there under the creator's name.

**Tier 2 — Unpublished drafts** (status: draft, or in a draft/ folder):
For each collision found, report:
- File: `[[filename]]`
- Overlap: what it covers
- Verdict: **competing** (covers the same thesis, question is which draft is the stronger vessel), **adjacent** (related but distinct angle), or **feeds** (this draft's best parts could strengthen the current idea)

Tier 2 collisions do not trigger KILL. They trigger a different question: "Which draft is the strongest vessel for this idea?" List the competing drafts and assess which one has the best combination of Q1 (uniqueness) + Q4 (tension) + Q5 (evidence).

### Q3: Stakes

> "After encountering this, what changes for the reader/user?"

Evaluate what the audience gains:
- **Reframes**: Changes how they see something they thought they understood
- **Equips**: Gives them a tool, method, or capability they didn't have
- **Provokes**: Forces them to confront something uncomfortable
- **None of the above**: Informs without transforming

If the answer is only "informs," the stakes are too low.

### Q4: Tension

> "What is the surprising, counterintuitive, or uncomfortable part?"

Look for:
- A contradiction the creator is willing to sit with
- A reversal of common assumption
- A confession or admission that costs something

If there is no tension, the idea is a summary, not a creation.

### Q5: Evidence

> "What lived experience, data, or concrete example makes this credible?"

Scan: vault for specific incidents, experiments, results, or external research that supports the thesis.

Evaluate:
- **Embodied**: The creator has personally experienced or built what they're talking about
- **Researched**: Supported by external data or others' work
- **Speculative**: Based on reasoning without direct experience or data

---

## Phase 3: Frame verdict

Based on the five answers, assign one of three verdicts:

### PROCEED

Requirements: Q1 is Strong + at least one of Q3/Q4 is strong + Q2 has no "absorbed" collisions.

Output:
```
## Frame: PROCEED

**Thesis**: [one sentence]
**Type**: [article / product / design]
**Unique angle**: [from Q1]
**Core tension**: [from Q4]
**Key evidence**: [from Q5]

### Before starting
- [1-2 specific things to nail down before beginning work]
```

### RETHINK

Requirements: Q1 is Weak or Q2 has an "adjacent" collision or Q3 is "informs only."

Output:
```
## Frame: RETHINK

**Thesis**: [one sentence]
**Problem**: [which questions failed and why]

### What would make this worth doing
- [1-3 specific directions that could strengthen the idea]

### Existing work to build on
- [[filename]] — [how it relates]
```

### KILL

Requirements: Q1 is None, or Q2 Tier 1 has an "absorbed" collision, or both Q3 and Q4 are empty.

Output:
```
## Frame: KILL

**Thesis**: [one sentence]
**Reason**: [one sentence — why this isn't worth the effort]
**Salvageable parts**: [any fragments worth keeping for other work, or "none"]
```

### CONSOLIDATE

Requirements: Q2 has multiple Tier 2 "competing" drafts covering the same thesis. The idea has merit but is scattered across too many drafts.

Output:
```
## Frame: CONSOLIDATE

**Thesis**: [one sentence]
**Competing drafts**:
- [[draft 1]] — strength: X, weakness: Y
- [[draft 2]] — strength: X, weakness: Y

**Recommended vessel**: [[strongest draft]] — because [reason]
**Parts to absorb from other drafts**: [specific sentences, scenes, or arguments to move]
**Drafts to retire after consolidation**: [list]
```

---

## Rules

- Never soften the verdict. If the answer is KILL, say KILL.
- Do not suggest improvements unless the verdict is RETHINK. KILL means stop, not pivot.
- The scan should cover the entire vault but prioritise published articles over drafts.
- Print the full analysis to the terminal. Do not write to a file unless the user appends `save` to the input.
- Write target (when saving): `{research}/frame/YYYY-MM-DD-{idea-slug}.md`
- All output in the language specified in `## Vault Structure` → `language`.
- Frame is not a writing tool. It does not generate content. It only evaluates whether content should exist.
