---
description: Promote a half-formed idea into a permanent concept card in 0 Material/.
  Use after a research session, or when an idea keeps resurfacing across notes.
argument-hint: "[source-note or topic]"
---

Read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path and content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Permanent cards live in `{vault}/0 Material/`. Existing cards there are the reference for structure and naming.

Input: $ARGUMENTS (optional)
- A note path, a topic keyword, or empty.
- Empty → scan recent notes for graduation candidates.
- A topic → find ideas about that topic worth graduating.
- A file path → treat that file as the source to graduate from.

---

## Mode: Scan (no args or topic)

### Step 1 — Collect candidates

Scan these sources from the past 14 days:
- `{inbox}/` — all files
- `{journal}/` — all journal entries
- `{daily}/` — Wrap blocks and "Next" items
- `{research}/` — any arc, bridge, reflect, or harvest outputs

For each source, extract ideas that pass the graduation threshold:
- Has a clear, statable core claim (not just an observation or question)
- Relates to at least one existing theme in `0 Material/`
- Has enough substance to stand alone as a concept card

Check `{vault}/0 Material/` — skip any idea already covered by an existing card.

Limit: 8 candidates.

### Step 2 — Present candidates

For each candidate, show:
```
[N] Core claim: one sentence stating the atomic idea
    Source: [[filename]] — the passage it comes from
    Related cards: [[existing-card-1]], [[existing-card-2]]
    Missing before graduating: what would make this card stronger (or "Ready")
```

Ask: "Which to graduate? (numbers, or 'none')"

### Step 3 — Graduate selected

For each selected candidate, follow the card creation flow below.

---

## Mode: Direct (file path given)

Read the source file. Extract the core atomic ideas in it. Treat each as a candidate and follow Step 2 above.

---

## Card creation flow

For each idea being graduated:

1. **Draft the card** using this structure:

```markdown
---
tags: [concept, <topic-tags>]
status: reference
source: claude-code
read: false
created: YYYY-MM-DD
up:
  - "[[<most relevant MOC>]]"
related:
  - "[[<related card 1>]]"
  - "[[<related card 2>]]"
says: "<core claim in one sentence — author's voice>"
series:
published_at:
published_to:
description: "<one-sentence description of what this card covers>"
---

# <Card title>

## 核心主張

<2–4 sentences expanding the core claim. Specific, not generic.>

## <Supporting section — name based on content>

<Evidence, mechanism, design implications, or connections.>

## 來源

<Where this idea comes from — vault note(s) with [[wikilinks]] or external source.>
```

2. **Show the draft** — full content and proposed filename.
   Proposed filename: `{vault}/0 Material/<Title>.md`
   (Use the same language as existing cards in that folder — English title if most existing cards are English, etc.)

3. **Ask**: "Save as `<filename>`? (yes / edit / different-title)"

4. **On confirm**, write the file. Print the full path.

5. **After writing**, check if the new card should be linked from an existing MOC. If yes, show the MOC and the proposed link line. Ask if the user wants to add it.

---

## Rules

- One card = one atomic claim. If a source has multiple ideas, create multiple cards (one confirmation per card).
- Do not restate what the source says — extract the generalisable principle.
- `says:` field must be a claim, not a description. "X is Y" or "X does Z", not "this note discusses X".
- Never write without user confirmation.
- Scan `0 Material/` before creating — if a card already covers the same ground, say so and stop.

---

Write output in the language specified in `## Vault Structure` → `language`.
